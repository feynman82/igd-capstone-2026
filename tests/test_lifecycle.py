"""Restart and shut down: the engine asks its supervisor, and nothing else can ask for it.

Two things are protected here, in order of how much it would hurt to lose them.

- **Nobody but Parrot's own screens can stop Parrot.** The engine trusts any request whose Host
  is loopback, and a `POST` from any web page a person has open satisfies that. So a lifecycle
  request must not come from a browser at all — every browser sends `Sec-Fetch-Site` and the
  Next.js server never does — and it must carry an intent header naming the action, which a
  cross-origin page cannot add without a CORS preflight the engine never grants.
- **A restart comes back as new code.** It is a fresh child process under a supervisor, not a
  loop inside one interpreter with every module still cached, and the screens stay up across it
  so there is something on the page while the engine returns.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterator
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api import main as api_main
from api.main import create_app
from core.runtime.checks import Check
from core.runtime.lifecycle import RESTART_EXIT_CODE, Lifecycle
from core.runtime.settings import Settings
from scripts import run_parrot

LOOPBACK = "http://127.0.0.1"


@pytest.fixture(autouse=True)
def quiet_engine(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """No real probes, no startup writes, no deliberate pause before exiting.

    The startup registry write is stubbed because a `TestClient` used as a context manager runs
    the lifespan, and the lifespan would otherwise write pack rows into whatever Postgres is
    listening on this machine — which, on a developer's laptop, is the household's own.
    """
    monkeypatch.setattr(api_main, "install_best_effort", lambda config: None)
    monkeypatch.setattr(api_main, "LIFECYCLE_DELAY_SECONDS", 0.0)
    with patch("api.main.collect_checks", return_value=[Check("Database", "available", "ok")]):
        yield


def _client(tmp_path: Path, lifecycle: Lifecycle | None) -> TestClient:
    app = create_app(Settings.load(tmp_path, {}))
    app.state.lifecycle = lifecycle
    return TestClient(app, base_url=LOOPBACK)


def _eventually(predicate: Callable[[], bool], seconds: float = 2.0) -> bool:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.02)
    return predicate()


# ------------------------------------------------------------------------------- the engine


def test_status_says_whether_this_engine_can_restart_itself(tmp_path: Path) -> None:
    with _client(tmp_path, None) as client:
        body = client.get("/api/system").json()
    assert body["engine"] == "running"
    assert body["can_restart"] is False
    assert body["checks"][0]["name"] == "Database"

    with _client(tmp_path, Lifecycle(lambda: None)) as client:
        assert client.get("/api/system").json()["can_restart"] is True


@pytest.mark.parametrize("action", ["restart", "shutdown"])
def test_a_request_without_the_intent_header_is_refused(tmp_path: Path, action: str) -> None:
    lifecycle = Lifecycle(lambda: None)
    with _client(tmp_path, lifecycle) as client:
        response = client.post(f"/api/system/{action}")
    assert response.status_code == 403
    assert lifecycle.requested is None


def test_the_intent_header_must_name_the_action_it_is_for(tmp_path: Path) -> None:
    lifecycle = Lifecycle(lambda: None)
    with _client(tmp_path, lifecycle) as client:
        response = client.post("/api/system/shutdown", headers={"x-parrot-intent": "restart"})
    assert response.status_code == 403
    assert lifecycle.requested is None


@pytest.mark.parametrize("site", ["cross-site", "same-site", "same-origin", "none"])
def test_a_browser_cannot_reach_the_engine_directly_even_with_the_header(
    tmp_path: Path, site: str
) -> None:
    lifecycle = Lifecycle(lambda: None)
    with _client(tmp_path, lifecycle) as client:
        response = client.post(
            "/api/system/shutdown",
            headers={"x-parrot-intent": "shutdown", "sec-fetch-site": site},
        )
    assert response.status_code == 403
    assert lifecycle.requested is None


def test_an_engine_nobody_supervises_says_so_instead_of_pretending(tmp_path: Path) -> None:
    with _client(tmp_path, None) as client:
        response = client.post("/api/system/restart", headers={"x-parrot-intent": "restart"})
    assert response.status_code == 409
    assert "START.cmd" in response.json()["detail"]


def test_an_unknown_action_is_not_found(tmp_path: Path) -> None:
    lifecycle = Lifecycle(lambda: None)
    with _client(tmp_path, lifecycle) as client:
        response = client.post("/api/system/reboot", headers={"x-parrot-intent": "reboot"})
    assert response.status_code == 404
    assert lifecycle.requested is None


@pytest.mark.parametrize("action", ["restart", "shutdown"])
def test_an_accepted_request_answers_first_and_then_asks_the_server_to_stop(
    tmp_path: Path, action: str
) -> None:
    stopped: list[bool] = []
    lifecycle = Lifecycle(lambda: stopped.append(True))
    with _client(tmp_path, lifecycle) as client:
        response = client.post(f"/api/system/{action}", headers={"x-parrot-intent": action})
        assert response.status_code == 202
        assert response.json() == {"action": action}
        assert _eventually(lambda: stopped == [True]), "the server was never asked to exit"
    assert lifecycle.requested == action


# ---------------------------------------------------------------------------- the lifecycle


def test_the_first_request_wins_and_exit_is_asked_for_once() -> None:
    calls: list[str] = []
    lifecycle = Lifecycle(lambda: calls.append("exit"))
    lifecycle.request("restart")
    lifecycle.request("shutdown")
    assert lifecycle.requested == "restart"
    assert calls == ["exit"]


def test_exit_codes_tell_the_supervisor_what_to_do() -> None:
    assert Lifecycle(lambda: None).exit_code(started=True) == 0
    assert Lifecycle(lambda: None).exit_code(started=False) == 1

    shutdown = Lifecycle(lambda: None)
    shutdown.request("shutdown")
    assert shutdown.exit_code(started=True) == 0

    restart = Lifecycle(lambda: None)
    restart.request("restart")
    assert restart.exit_code(started=True) == RESTART_EXIT_CODE


# --------------------------------------------------------------------------- the supervisor


class Screens:
    """Stands in for `start_web` and `stop`: counts, and never touches npm."""

    def __init__(self) -> None:
        self.started = 0
        self.stopped: list[object] = []

    def start(self, api_port: int, web_port: int) -> object:
        self.started += 1
        return "web-process"

    def stop(self, web: object) -> None:
        self.stopped.append(web)


def _launcher(codes: list[int]) -> tuple[list[list[str]], Callable[[list[str]], int]]:
    launched: list[list[str]] = []

    def spawn(argv: list[str]) -> int:
        launched.append(argv)
        return codes[len(launched) - 1]

    return launched, spawn


def _supervise(
    tmp_path: Path, argv: list[str], codes: list[int], screens: Screens
) -> tuple[int, list[list[str]]]:
    launched, spawn = _launcher(codes)
    code = run_parrot.supervise(
        argv,
        spawn=spawn,
        start_screens=screens.start,
        stop_screens=screens.stop,
        load_settings=lambda: Settings.load(tmp_path, {}),
    )
    return code, launched


def test_the_supervisor_relaunches_on_restart_and_keeps_the_screens_up(tmp_path: Path) -> None:
    screens = Screens()
    code, launched = _supervise(tmp_path, [], [RESTART_EXIT_CODE, RESTART_EXIT_CODE, 0], screens)

    assert code == 0
    assert len(launched) == 3, "two restarts, then a shutdown"
    assert screens.started == 1, "the screens are started once, not once per engine"
    assert screens.stopped == ["web-process"], "and stopped once, when Parrot really stops"
    assert all("--web-managed" in argv for argv in launched)
    assert "--no-browser" not in launched[0], "the first launch opens the browser"
    assert all("--no-browser" in argv for argv in launched[1:]), "a restart opens no new tab"


def test_a_start_that_fails_is_not_retried(tmp_path: Path) -> None:
    screens = Screens()
    code, launched = _supervise(tmp_path, [], [2], screens)
    assert code == 2
    assert len(launched) == 1
    assert screens.stopped == ["web-process"]


def test_no_web_means_the_supervisor_starts_no_screens(tmp_path: Path) -> None:
    screens = Screens()
    code, launched = _supervise(tmp_path, ["--no-web"], [0], screens)
    assert code == 0
    assert screens.started == 0
    assert "--no-web" in launched[0]
    assert "--web-managed" not in launched[0]


def test_the_supervisor_still_refuses_a_lan_bind_before_starting_anything(tmp_path: Path) -> None:
    screens = Screens()
    with pytest.raises(SystemExit) as error:
        _supervise(tmp_path, ["--bind-address", "0.0.0.0"], [0], screens)
    assert error.value.code == 2
    assert screens.started == 0
