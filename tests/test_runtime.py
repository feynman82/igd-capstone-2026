"""Setup diagnostics use controlled service responses, never live household documents."""

import json
from pathlib import Path
from typing import Any
from unittest.mock import patch

import httpx
import pytest
from fastapi.testclient import TestClient

from api.main import create_app
from core.runtime.checks import Check, database_check, model_check
from core.runtime.settings import ConfigurationError, Settings
from scripts import run_parrot


def test_defaults_share_one_local_ollama_endpoint(tmp_path: Path) -> None:
    settings = Settings.load(tmp_path, {})
    assert settings.generation_url == settings.auxiliary_url == "http://127.0.0.1:11434"


@pytest.mark.parametrize(
    "key,value",
    [
        ("OLLAMA_GEN_URL", "https://cloud.example"),
        ("OLLAMA_AUX_URL", "http://192.168.1.2:11434"),
        ("DATABASE_URL", "postgresql://user:secret@127.0.0.1/db?host=remote.example"),
        ("REDIS_URL", "redis://remote.example:6379/0"),
        ("OLLAMA_GEN_URL", "http://127.0.0.1:wrong"),
    ],
)
def test_remote_or_ambiguous_endpoints_fail_without_leaking_values(
    tmp_path: Path,
    key: str,
    value: str,
) -> None:
    with pytest.raises(ConfigurationError) as error:
        Settings.load(tmp_path, {key: value})
    assert key in str(error.value)
    assert value not in str(error.value)
    assert "secret" not in str(error.value)


# `infra/docker-compose.yml` publishes Redis on ${PARROT_REDIS_PORT:-6379} and Postgres on
# ${PARROT_DB_PORT:-5432}. Those are the only two variables a person editing .env sees, so the
# client defaults have to follow them: setting PARROT_REDIS_PORT alone used to move the container
# and leave the engine dialling 6379, which reads as "the queue broker did not answer" and
# silently drops ingestion back to inline.
def test_the_broker_port_follows_the_port_compose_publishes(tmp_path: Path) -> None:
    settings = Settings.load(tmp_path, {"PARROT_REDIS_PORT": "6380"})
    assert settings.redis_url == "redis://127.0.0.1:6380/0"


def test_the_database_port_follows_the_port_compose_publishes(tmp_path: Path) -> None:
    settings = Settings.load(tmp_path, {"PARROT_DB_PORT": "5433"})
    assert "5433" in settings.database_url


def test_an_explicit_url_still_wins_over_the_port_variable(tmp_path: Path) -> None:
    settings = Settings.load(
        tmp_path,
        {"PARROT_REDIS_PORT": "6380", "REDIS_URL": "redis://127.0.0.1:6399/2"},
    )
    assert settings.redis_url == "redis://127.0.0.1:6399/2"


# With Postgres stopped, a connection attempt with no timeout was still waiting after more than
# 80 seconds, and every /api route opens one per request, so every screen hung rather than saying
# the database is down. The attempt must be bounded, and the timeout must arrive as the one safe
# error the routes turn into a 503 — this raises the exact class psycopg raised on 2026-09-13.
def test_a_database_that_does_not_answer_fails_in_seconds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import psycopg
    from psycopg.errors import ConnectionTimeout

    from core.runtime import db

    passed: dict[str, object] = {}

    def never_answers(url: str, **kwargs: object) -> object:
        passed.update(kwargs)
        raise ConnectionTimeout("connection timeout expired")

    monkeypatch.setattr(psycopg, "connect", never_answers)
    with pytest.raises(db.DatabaseUnavailable), db.connect(Settings.load(tmp_path, {})):
        pass
    timeout = passed["connect_timeout"]
    assert isinstance(timeout, int | float) and 0 < timeout <= 5


def test_env_file_is_literal_and_process_environment_wins(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text(
        "PARROT_GEN_MODEL='$(do-not-execute)'\nPARROT_EMBED_MODEL=from-file\n",
        encoding="utf-8",
    )
    settings = Settings.load(tmp_path, {"PARROT_EMBED_MODEL": "override"})
    assert settings.generation_model == "$(do-not-execute)"
    assert settings.embedding_model == "override"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "capabilities,state",
    [
        (["completion"], "blocked"),
        (["completion", "vision"], "unverified"),
        (None, "unverified"),
        ("vision", "unverified"),
    ],
)
async def test_model_metadata_never_claims_inference_validation(
    capabilities: object,
    state: str,
) -> None:
    calls = []

    def respond(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        return httpx.Response(200, json={"capabilities": capabilities})

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        result = await model_check(client, "Vision", "http://127.0.0.1:11434", "model", {"vision"})
    assert result.state == state
    assert calls == ["/api/show"]


@pytest.mark.asyncio
async def test_model_redirect_is_not_followed() -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda _: httpx.Response(302, headers={"location": "https://external.example"})
        ),
    ) as client:
        result = await model_check(client, "Model", "http://127.0.0.1:11434", "model", set())
    assert result.state == "blocked"


def test_liveness_is_independent_of_dependency_checks(tmp_path: Path) -> None:
    with patch("api.main.collect_checks", side_effect=AssertionError("must not probe")):
        client = TestClient(create_app(Settings.load(tmp_path, {})), base_url="http://127.0.0.1")
        assert client.get("/healthz").json() == {
            "service": "parrot",
            "stage": "setup",
            "status": "alive",
        }


def test_setup_does_not_claim_assistant_readiness_and_escapes_content(tmp_path: Path) -> None:
    with patch(
        "api.main.collect_checks", return_value=[Check("<script>", "available", "<bad>")]
    ) as probe:
        client = TestClient(create_app(Settings.load(tmp_path, {})), base_url="http://127.0.0.1")
        response = client.get("/setup")
        assert response.status_code == 200
        assert "&lt;script&gt;" in response.text
        assert "<script>" not in response.text
        ready = client.get("/readyz")
        assert ready.status_code == 503
        assert ready.json()["ready"] is False
        assert probe.call_count == 1
        assert response.headers["cache-control"] == "no-store"


def test_the_startup_page_opens_without_probing_and_runs_only_its_own_script(
    tmp_path: Path,
) -> None:
    """The browser opens on this within a second of a double-click, so it must not wait on the
    checks, and it is the one engine page with a script, so the policy has to allow exactly that
    script and nothing from anywhere else."""
    with patch("api.main.collect_checks", side_effect=AssertionError("must not probe")):
        client = TestClient(create_app(Settings.load(tmp_path, {})), base_url="http://127.0.0.1")
        first = client.get("/")
        second = client.get("/")
    assert first.status_code == 200
    assert "Getting Parrot ready" in first.text
    policy = first.headers["content-security-policy"]
    nonce = policy.split("'nonce-")[1].split("'")[0]
    assert f'<script nonce="{nonce}">' in first.text
    assert "connect-src 'self'" in policy and "default-src 'none'" in policy
    assert nonce not in second.headers["content-security-policy"], "a nonce is per response"
    assert "http://localhost:3000/" in first.text, "where Today is, as data rather than script"
    assert "fonts.googleapis" not in first.text, "nothing on this page leaves the machine"


def test_system_status_carries_the_model_and_the_screens(tmp_path: Path) -> None:
    from api.startup import ModelWarmth

    with patch("api.main.collect_checks", return_value=[]):
        app = create_app(Settings.load(tmp_path, {}))
        app.state.model = ModelWarmth("ready", "cpu")
        body = TestClient(app, base_url="http://127.0.0.1").get("/api/system").json()
    assert body["model"] == {"state": "ready", "device": "cpu", "detail": ""}
    assert body["screens"] == {"url": "http://localhost:3000/", "expected": True}


def _ollama_answering(tmp_path: Path, handler: Any) -> Any:
    from core.runtime.ollama import Ollama

    client = Ollama(Settings.load(tmp_path, {}))
    client._client = lambda base_url: httpx.Client(  # type: ignore[method-assign]
        base_url=base_url, transport=httpx.MockTransport(handler)
    )
    return client


@pytest.mark.parametrize(
    "size,in_vram,placement", [(100, 100, "gpu"), (100, 40, "partial"), (100, 0, "cpu")]
)
def test_warming_says_where_the_generator_landed(
    tmp_path: Path, size: int, in_vram: int, placement: str
) -> None:
    """13 September: size_vram was 0 on every model and nothing on screen said so."""
    settings = Settings.load(tmp_path, {})
    asked: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        asked.append(request.url.path)
        if request.url.path == "/api/ps":
            model = {"name": settings.generation_model, "size": size, "size_vram": in_vram}
            return httpx.Response(200, json={"models": [model]})
        return httpx.Response(200, json={})

    assert _ollama_answering(tmp_path, handler).warm() == placement
    assert asked == ["/api/generate", "/api/ps", "/api/embed"]


def test_a_model_that_cannot_load_is_recorded_rather_than_raised(tmp_path: Path) -> None:
    from api.startup import ModelWarmth, warm_models

    client = _ollama_answering(tmp_path, lambda request: httpx.Response(500))
    warmth = ModelWarmth()
    warm_models(warmth, client)
    assert warmth.state == "unavailable"
    assert "could not be loaded" in warmth.detail


def test_queries_and_passages_are_embedded_with_the_models_task_prompts(tmp_path: Path) -> None:
    sent: list[list[str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        texts = json.loads(request.content)["input"]
        sent.append(texts)
        return httpx.Response(200, json={"embeddings": [[0.0] * 768 for _ in texts]})

    client = _ollama_answering(tmp_path, handler)
    client.embed_query("do i have a hospitalisation plan?")
    client.embed_documents([("PrivateCare Hospital and Surgical Plan", "6.1 Waiting Period")])
    assert sent == [
        ["task: search result | query: do i have a hospitalisation plan?"],
        ["title: PrivateCare Hospital and Surgical Plan | text: 6.1 Waiting Period"],
    ]


def test_an_embedding_model_without_task_prompts_is_sent_the_text_alone(tmp_path: Path) -> None:
    from core.runtime.ollama import Ollama

    sent: list[list[str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        texts = json.loads(request.content)["input"]
        sent.append(texts)
        return httpx.Response(200, json={"embeddings": [[0.0] * 768 for _ in texts]})

    client = Ollama(Settings.load(tmp_path, {"PARROT_EMBED_MODEL": "nomic-embed-text"}))
    client._client = lambda base_url: httpx.Client(  # type: ignore[method-assign]
        base_url=base_url, transport=httpx.MockTransport(handler)
    )
    client.embed_query("premium")
    assert sent == [["premium"]]


def test_untrusted_host_is_rejected(tmp_path: Path) -> None:
    client = TestClient(create_app(Settings.load(tmp_path, {})))
    assert client.get("/healthz", headers={"host": "attacker.example"}).status_code == 400


def test_runner_rejects_lan_bind_before_starting() -> None:
    with pytest.raises(SystemExit) as error:
        run_parrot.main(["--bind-address", "0.0.0.0"])
    assert error.value.code == 2


@pytest.mark.parametrize(
    "version,vector,tables,state",
    [
        (170005, True, True, "available"),
        (160005, True, True, "blocked"),
        (170005, False, True, "blocked"),
        (170005, True, False, "blocked"),
    ],
)
def test_database_version_extension_and_tables_are_required(
    tmp_path: Path,
    version: int,
    vector: bool,
    tables: bool,
    state: str,
) -> None:
    with patch("core.runtime.checks.psycopg.connect") as connect:
        connection = connect.return_value.__enter__.return_value
        connection.execute.return_value.fetchone.return_value = (version, vector, *([tables] * 7))
        assert database_check(Settings.load(tmp_path, {})).state == state
        assert "default_transaction_read_only=on" in connect.call_args.kwargs["options"]


def test_busy_port_does_not_open_browser(tmp_path: Path) -> None:
    import socket

    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        with (
            patch("api.main.create_app", return_value=create_app(Settings.load(tmp_path, {}))),
            patch("scripts.run_parrot.webbrowser.open") as browser,
        ):
            assert run_parrot.main(["--port", str(listener.getsockname()[1])]) == 2
            browser.assert_not_called()
