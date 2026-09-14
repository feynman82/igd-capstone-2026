"""Read-only dependency diagnostics; installation is never treated as inference validation."""

from __future__ import annotations

import asyncio
import socket
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

import httpx
import psycopg
from redis import Redis
from redis.exceptions import RedisError

from core.runtime.settings import Settings

CAPTURE_QUERY = """
SELECT count(*),
       count(*) FILTER (WHERE status = 'indexed'),
       count(*) FILTER (WHERE status = 'quarantined')
  FROM documents
"""

TELEGRAM_QUERY = """
SELECT count(*) FROM documents WHERE source_channel = 'telegram'
"""

SCHEMA_QUERY = """
SELECT current_setting('server_version_num')::int,
       EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector'),
       to_regclass('public.documents') IS NOT NULL,
       to_regclass('public.chunks') IS NOT NULL,
       to_regclass('public.facts') IS NOT NULL,
       to_regclass('public.obligations') IS NOT NULL,
       to_regclass('public.packs') IS NOT NULL,
       to_regclass('public.modules') IS NOT NULL,
       to_regclass('public.traces') IS NOT NULL
"""


@dataclass(frozen=True)
class Check:
    name: str
    state: Literal["available", "blocked", "unverified"]
    detail: str

    def payload(self) -> dict[str, str]:
        return asdict(self)


def database_check(settings: Settings) -> Check:
    try:
        with psycopg.connect(
            settings.database_url,
            connect_timeout=2,
            options="-c statement_timeout=2000 -c default_transaction_read_only=on",
        ) as connection:
            row = connection.execute(SCHEMA_QUERY).fetchone()
        if row and 170000 <= row[0] < 180000 and all(row[1:]):
            return Check("Database", "available", "PostgreSQL 17, pgvector and base tables found.")
        return Check(
            "Database",
            "blocked",
            "PostgreSQL 17, pgvector or base tables are missing. See setup guide.",
        )
    except psycopg.Error:
        return Check(
            "Database", "blocked", "Cannot connect. Start local PostgreSQL and check credentials."
        )


def capture_check(settings: Settings) -> Check:
    """The watched folder, and how many documents have been registered from any channel."""
    folder = Path(settings.watch_folder)
    if not folder.is_dir():
        return Check("Capture", "blocked", f"The watched folder does not exist yet: {folder}")
    try:
        with psycopg.connect(
            settings.database_url,
            connect_timeout=2,
            options="-c statement_timeout=2000 -c default_transaction_read_only=on",
        ) as connection:
            row = connection.execute(CAPTURE_QUERY).fetchone()
    except psycopg.Error:
        return Check("Capture", "blocked", "The watched folder exists but the database does not.")
    registered, indexed, quarantined = row or (0, 0, 0)
    detail = f"Watching {folder}. {registered} registered, {indexed} indexed"
    if quarantined:
        detail += f", {quarantined} needing your eyes"
    return Check("Capture", "available", detail + ".")


def telegram_check(settings: Settings) -> Check:
    """Whether a bot is configured, and how much has actually arrived through it.

    It deliberately makes no call to Telegram. This runs on every poll of the startup page, and
    a diagnostic that reaches out to a third party every few seconds is not the privacy claim
    `docs/governance/` makes — so it reports configuration and the count of documents that came
    in on this channel, which is the question a person is really asking. `getMe` stays where it
    belongs: `scripts/telegram_bot.py --check`, run once, by a person.
    """
    if not settings.telegram_configured:
        return Check(
            "Telegram capture",
            "unverified",
            "No bot token configured, so documents arrive only through the watched folder. "
            "Set TELEGRAM_BOT_TOKEN in .env to file from a phone.",
        )
    try:
        with psycopg.connect(
            settings.database_url,
            connect_timeout=2,
            options="-c statement_timeout=2000 -c default_transaction_read_only=on",
        ) as connection:
            row = connection.execute(TELEGRAM_QUERY).fetchone()
    except psycopg.Error:
        return Check("Telegram capture", "blocked", "A bot is configured but the database is not.")
    filed = row[0] if row else 0
    chats = (
        "any chat"
        if not settings.telegram_chat_ids
        else f"{len(settings.telegram_chat_ids)} chat(s)"
    )
    if not filed:
        return Check(
            "Telegram capture",
            "unverified",
            f"A bot is configured and accepted from {chats}, but nothing has arrived through it "
            "yet. Send the bot a photograph; the Parrot window says what happened to it.",
        )
    return Check(
        "Telegram capture",
        "available",
        f"{filed} document(s) filed from Telegram, accepted from {chats}.",
    )


def redis_check(settings: Settings) -> Check:
    try:
        with Redis.from_url(
            settings.redis_url, socket_connect_timeout=2, socket_timeout=2
        ) as client:
            client.ping()
        return Check("Queue broker", "available", "Redis responds.")
    except (RedisError, ValueError):
        return Check("Queue broker", "blocked", "Cannot reach Redis. Start the local queue broker.")


def interface_check(settings: Settings) -> Check:
    """Whether the screens are answering on their port.

    This used to be a sentence asserting that the interface existed, which is not a check —
    it was true whether or not anything was running, and the one time a person reads this page
    is the time something is not running. `scripts/run_parrot.py` starts the screens beside
    this server now, so "did that work" is a real question with a real answer.

    It asks for a connection and nothing more. Fetching a page would make the setup screen wait
    on a Next.js cold compile, and a check that takes twenty seconds is a check people stop
    waiting for.
    """
    try:
        with socket.create_connection(("127.0.0.1", settings.web_port), timeout=2):
            pass
    except OSError:
        return Check(
            "Household interface",
            "blocked",
            f"Nothing is answering on port {settings.web_port}. Today, Ask, Vault and Packs are "
            "built; they are served by a Next.js process, which START.cmd starts beside this "
            "one. If it did not start, this window says why.",
        )
    return Check(
        "Household interface",
        "available",
        f"Today, Ask, Vault and Packs are answering on http://localhost:{settings.web_port}.",
    )


def worker_check(settings: Settings) -> Check:
    """Whether a worker is listening — which is a different question from whether Redis is up.

    A reachable broker and no worker is the failure this check exists for: documents would be
    registered, queued, and then sit there looking filed while nothing read them.
    """
    try:
        from core.worker.tasks import application
    except ImportError:
        return Check("Ingestion worker", "blocked", "Celery is not installed. Run uv sync.")
    try:
        app = application(settings)
        app.conf.broker_transport_options = {"socket_connect_timeout": 2, "socket_timeout": 2}
        replies = app.control.inspect(timeout=2).ping()
    except Exception:
        return Check(
            "Ingestion worker",
            "blocked",
            "Cannot ask the queue whether a worker is listening. Check the broker.",
        )
    if not replies:
        return Check(
            "Ingestion worker",
            "blocked",
            "No worker is listening. Documents would queue unread. "
            "Start it with `uv run python scripts/worker.py --beat`.",
        )
    return Check(
        "Ingestion worker",
        "available",
        f"{len(replies)} worker(s) listening. This does not verify that a parse succeeds.",
    )


async def model_check(
    client: httpx.AsyncClient,
    name: str,
    url: str,
    model: str,
    required: set[str],
) -> Check:
    try:
        response = await client.post(f"{url}/api/show", json={"model": model})
        if response.status_code == 404:
            return Check(
                name, "blocked", "Configured model is not installed on its Ollama endpoint."
            )
        response.raise_for_status()
        data = response.json()
        capabilities = data.get("capabilities") if isinstance(data, dict) else None
        if not isinstance(capabilities, list) or not all(isinstance(x, str) for x in capabilities):
            return Check(name, "unverified", "Ollama did not provide valid capability metadata.")
        missing = required.difference(capabilities)
        if missing:
            return Check(
                name,
                "blocked",
                "Required model capabilities are missing: " + ", ".join(sorted(missing)),
            )
        return Check(
            name,
            "unverified",
            "Installed; metadata checked. Actual inference is not yet validated.",
        )
    except (httpx.HTTPError, ValueError):
        return Check(
            name,
            "blocked",
            "Ollama is unavailable or returned an invalid response. Check local setup.",
        )


async def collect_checks(settings: Settings) -> list[Check]:
    async with httpx.AsyncClient(timeout=3, trust_env=False, follow_redirects=False) as client:
        checks = await asyncio.gather(
            asyncio.to_thread(database_check, settings),
            asyncio.to_thread(redis_check, settings),
            asyncio.to_thread(worker_check, settings),
            asyncio.to_thread(capture_check, settings),
            asyncio.to_thread(telegram_check, settings),
            asyncio.to_thread(interface_check, settings),
            model_check(
                client,
                "Generator and vision",
                settings.generation_url,
                settings.generation_model,
                {"completion", "vision"},
            ),
            model_check(
                client,
                "Embeddings",
                settings.auxiliary_url,
                settings.embedding_model,
                {"embedding"},
            ),
            model_check(client, "Reranker", settings.auxiliary_url, settings.rerank_model, set()),
        )
    return [
        *checks,
        Check(
            "Document processing",
            "unverified",
            "Parse, classify, extract and quarantine run. Retrieval is the dense-only stopgap "
            "in core/graph/baseline.py, so answer quality is not yet measured.",
        ),
    ]
