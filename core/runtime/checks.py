"""Read-only dependency diagnostics; installation is never treated as inference validation."""

from __future__ import annotations

import asyncio
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


def redis_check(settings: Settings) -> Check:
    try:
        with Redis.from_url(
            settings.redis_url, socket_connect_timeout=2, socket_timeout=2
        ) as client:
            client.ping()
        return Check(
            "Queue broker", "available", "Redis responds; this does not verify an ingestion worker."
        )
    except (RedisError, ValueError):
        return Check("Queue broker", "blocked", "Cannot reach Redis. Start the local queue broker.")


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
            asyncio.to_thread(capture_check, settings),
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
            "Parse, classify, extract and quarantine run. Hybrid retrieval is not built yet, "
            "so answer quality is not yet measured.",
        ),
        Check(
            "Household interface",
            "blocked",
            "The Today, Ask, Vault and Packs interface is not built yet.",
        ),
    ]
