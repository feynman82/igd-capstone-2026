"""One place that opens a connection to the one database.

`Settings.database_url` is already validated as a loopback PostgreSQL URL, so nothing here
needs to parse it again. Import psycopg lazily: the diagnostic server in `api/main.py` must
be able to tell a person their database is missing without itself failing to import.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from core.runtime.settings import Settings


class DatabaseUnavailable(RuntimeError):
    """Safe to show: the message never carries the connection string."""


@contextmanager
def connect(settings: Settings) -> Iterator[Any]:
    """Yield an open psycopg connection with autocommit off. The caller commits."""
    try:
        import psycopg
    except ImportError as error:  # pragma: no cover - the dependency is declared
        raise DatabaseUnavailable("psycopg is not installed. Run uv sync.") from error

    try:
        conn = psycopg.connect(settings.database_url, autocommit=False)
    except psycopg.OperationalError as error:
        raise DatabaseUnavailable(
            "Cannot reach the local database. Start it with "
            "`docker compose -f infra/docker-compose.yml up -d`."
        ) from error
    try:
        yield conn
    finally:
        conn.close()
