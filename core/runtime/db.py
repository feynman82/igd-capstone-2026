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

# How long one connection attempt may take before the database is reported unavailable.
#
# libpq's default is no limit. With Postgres stopped, psycopg.connect() to 127.0.0.1 was still
# waiting after more than 80 seconds on 2026-09-13, although the port itself refused a raw socket
# in 2.03s; with connect_timeout=3 psycopg gave up in 3.09s. Every /api route opens a connection
# per request, so an unbounded attempt meant every screen hung instead of rendering its "the
# database is not running" state. Three seconds rather than one, because a refused loopback
# connection on Windows takes two on its own.
CONNECT_TIMEOUT_SECONDS = 3


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
        conn = psycopg.connect(
            settings.database_url, autocommit=False, connect_timeout=CONNECT_TIMEOUT_SECONDS
        )
    except psycopg.OperationalError as error:
        raise DatabaseUnavailable(
            "Cannot reach the local database. Start it with "
            "`docker compose -f infra/docker-compose.yml up -d`."
        ) from error
    try:
        yield conn
    finally:
        conn.close()
