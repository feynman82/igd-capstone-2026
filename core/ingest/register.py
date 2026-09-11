"""Register a document, idempotently, on a SHA-256 of the source bytes.

This is the first thing that happens to anything captured, on every channel, and it is the
only place a `documents` row is created. Re-ingesting the same bytes updates that row in
place; it never creates a second one. The unique index on `documents.sha256` — declared in
`db/migrations/0001_init.sql`, not here — is what makes that true even when two adapters
register the same file at the same moment.

The SQL is written out in full and parameterised, per rule 1 in AGENTS.md. Nothing in this
module builds a query from a string at runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol
from uuid import UUID

from core.adapters.base import sha256 as digest_of

# `xmax = 0` is true only for a row this statement inserted. On the conflict path Postgres
# updates the existing row, which carries the transaction id that locked it, so the flag
# tells insert from update without a second round trip.
REGISTER_SQL = """
INSERT INTO documents (sha256, source_channel, original_name, mime, synthetic)
VALUES (%(sha256)s, %(source_channel)s, %(original_name)s, %(mime)s, %(synthetic)s)
ON CONFLICT (sha256) DO UPDATE
   SET original_name = EXCLUDED.original_name,
       mime          = EXCLUDED.mime
RETURNING id, ingested_at, source_channel, status, (xmax = 0) AS inserted
"""


@dataclass(frozen=True, slots=True)
class Registration:
    """The row as it now stands, plus whether this call is the one that created it."""

    document_id: UUID
    sha256: bytes
    source_channel: str
    original_name: str
    mime: str
    status: str
    ingested_at: datetime
    inserted: bool

    @property
    def already_registered(self) -> bool:
        return not self.inserted


class Cursor(Protocol):
    def execute(self, query: str, params: Any = ..., /) -> Any: ...
    def fetchone(self) -> Any: ...
    def __enter__(self) -> Cursor: ...
    def __exit__(self, *exc: object) -> None: ...


class Connection(Protocol):
    """Just enough of `psycopg.Connection` to register a document and to be faked in a test."""

    def cursor(self) -> Cursor: ...


class Registrar(Protocol):
    """What a capture adapter is handed. It does not know psycopg exists."""

    def __call__(
        self,
        *,
        payload: bytes,
        mime: str,
        original_name: str,
        source_channel: str,
        synthetic: bool = False,
    ) -> Registration: ...


def register_document(
    conn: Connection,
    *,
    payload: bytes,
    mime: str,
    original_name: str,
    source_channel: str,
    synthetic: bool = False,
) -> Registration:
    """Insert or update the `documents` row for these bytes and say which happened.

    The caller owns the transaction. Registration is deliberately not committed here: the
    ingestion worker commits the retrieval lane and the facts lane together, and the document
    row belongs in that same transaction.
    """
    if not payload:
        raise ValueError("refusing to register an empty document")
    if not original_name.strip():
        raise ValueError("documents.original_name is NOT NULL; a capture must supply a name")

    key = digest_of(payload)
    with conn.cursor() as cur:
        cur.execute(
            REGISTER_SQL,
            {
                "sha256": key,
                "source_channel": source_channel,
                "original_name": original_name,
                "mime": mime,
                "synthetic": synthetic,
            },
        )
        row = cur.fetchone()
    if row is None:  # pragma: no cover - RETURNING always yields a row on insert or update
        raise RuntimeError("documents upsert returned no row")

    document_id, ingested_at, stored_channel, status, inserted = row
    return Registration(
        document_id=document_id,
        sha256=key,
        source_channel=stored_channel,
        original_name=original_name,
        mime=mime,
        status=status,
        ingested_at=ingested_at,
        inserted=bool(inserted),
    )
