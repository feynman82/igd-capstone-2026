"""The vault: what is in the house, what state it is in, and what was read off it.

One read model, used by the interface and by anything else that wants to show a document
beside its facts. It is deliberately not part of retrieval — nothing here embeds, ranks or
answers. It lists rows.

Two queries, never more. The documents are fetched once and their facts are fetched once with
`document_id = ANY(...)`, because a facts query per document is the difference between one
round trip and fifty on a screen that shows a household's whole vault.

**Filters are parameters, not string-building.** Rule 1 forbids generating SQL at runtime, so
every optional filter is written into the one statement as `%(name)s IS NULL OR column = ...`
and passing `None` means "any". The statement below is the whole statement; there is no code
path that assembles a different one.

**A disabled pack's documents are hidden.** Not deleted and not unindexed — hidden from this
listing, which is what switching a pack off is supposed to mean. `include_disabled=True`
shows them again with `pack_enabled` false, so the settings screen can honestly say what
turning a pack back on would bring back. A document belonging to no pack is never hidden:
nothing disabled it.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from core.packs import PackUnavailable, pack

log = logging.getLogger(__name__)

# --------------------------------------------------------------------------------- the SQL
#
# The casts are not decoration. An untyped parameter compared with IS NULL gives Postgres
# nothing to infer the type from, so each one says what it is.

_WHERE = """
 WHERE (%(status)s::text IS NULL OR d.status = %(status)s::text)
   AND (%(doc_type)s::text IS NULL OR d.doc_type = %(doc_type)s::text)
   AND (%(pack_id)s::text IS NULL OR d.pack_id = %(pack_id)s::text)
   AND (%(packs)s::text[] IS NULL
        OR d.pack_id IS NULL
        OR d.pack_id = ANY(%(packs)s::text[]))
"""

SELECT_DOCUMENTS = (
    """
SELECT d.id,
       d.original_name,
       d.mime,
       d.pages,
       d.doc_type,
       d.pack_id,
       d.status,
       d.quarantine_reason,
       d.ingested_at,
       d.synthetic
  FROM documents d
"""
    + _WHERE
    + """
 ORDER BY d.ingested_at DESC, d.id
 LIMIT %(limit)s OFFSET %(offset)s
"""
)

COUNT_DOCUMENTS = "SELECT count(*) FROM documents d" + _WHERE

# Every fact carries the page it was read off, because `facts.page` is NOT NULL and this is
# the screen where a person checks that claim against the document.
SELECT_FACTS_FOR_DOCUMENTS = """
SELECT f.document_id,
       f.key,
       f.subject,
       f.value_text,
       f.value_num,
       f.value_date,
       f.page,
       f.confidence,
       f.verified_by_user,
       f.pack_id
  FROM facts f
 WHERE f.document_id = ANY(%(document_ids)s::uuid[])
 ORDER BY f.document_id, f.page, f.key
"""


# --------------------------------------------------------------------------------- the rows


@dataclass(frozen=True, slots=True)
class Fact:
    """One extracted field, collapsed to the single value column it actually landed in."""

    key: str
    subject: str | None
    page: int
    confidence: float
    verified_by_user: bool
    pack_id: str
    value_text: str | None = None
    value_num: Decimal | None = None
    value_date: date | None = None
    declared_type: str | None = None  # what the pack calls it, when the pack is still on disk

    @property
    def value(self) -> str | float | None:
        """The one value this fact has. JSON-ready: a date becomes its ISO string."""
        if self.value_date is not None:
            return self.value_date.isoformat()
        if self.value_num is not None:
            return float(self.value_num)
        return self.value_text

    @property
    def value_type(self) -> str:
        """The pack's own name for the type when it is knowable, else the column it sits in.

        `core/contracts.py` maps a declared type to a facts column; this is that map read
        backwards, which is lossy — `money`, `integer` and `percent` all land in `value_num`.
        So the pack is asked first and the column is only the fallback, which is what keeps
        the screen right for a pack that has since been uninstalled.
        """
        if self.declared_type is not None:
            return self.declared_type
        if self.value_date is not None:
            return "date"
        if self.value_num is not None:
            return "number"
        return "string"


@dataclass(frozen=True, slots=True)
class VaultDocument:
    document_id: Any
    original_name: str
    mime: str
    pages: int | None
    doc_type: str | None
    pack_id: str | None
    pack_enabled: bool
    status: str
    quarantine_reason: str | None
    ingested_at: datetime | None
    synthetic: bool
    facts: list[Fact] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class VaultPage:
    documents: list[VaultDocument]
    total: int
    limit: int
    offset: int


# ------------------------------------------------------------------------------- the lookup


def _declared_type(pack_id: str | None, doc_type: str | None, key: str) -> str | None:
    """What the pack says this field is, or None when the pack is gone or does not declare it."""
    if not pack_id or not doc_type:
        return None
    try:
        spec = pack(pack_id).manifest.field_index().get((doc_type, key))
    except PackUnavailable:
        return None
    return spec.type if spec else None


def _facts_for(
    conn: Any, document_ids: list[Any], doc_types: dict[Any, tuple[str | None, str | None]]
) -> dict[Any, list[Fact]]:
    if not document_ids:
        return {}
    with conn.cursor() as cur:
        cur.execute(SELECT_FACTS_FOR_DOCUMENTS, {"document_ids": document_ids})
        rows = cur.fetchall()

    grouped: dict[Any, list[Fact]] = {}
    for (
        document_id,
        key,
        subject,
        value_text,
        value_num,
        value_date,
        page,
        confidence,
        verified_by_user,
        fact_pack_id,
    ) in rows:
        pack_id, doc_type = doc_types.get(document_id, (fact_pack_id, None))
        grouped.setdefault(document_id, []).append(
            Fact(
                key=key,
                subject=subject,
                page=page,
                confidence=float(confidence),
                verified_by_user=bool(verified_by_user),
                pack_id=fact_pack_id,
                value_text=value_text,
                value_num=value_num,
                value_date=value_date,
                declared_type=_declared_type(pack_id or fact_pack_id, doc_type, key),
            )
        )
    return grouped


def documents(
    conn: Any,
    *,
    status: str | None = None,
    doc_type: str | None = None,
    pack_id: str | None = None,
    enabled: frozenset[str] | None = None,
    include_disabled: bool = False,
    limit: int = 50,
    offset: int = 0,
) -> VaultPage:
    """A page of documents, newest first, each with the facts read off it.

    `enabled` is the set from `core.registry.enabled_pack_ids`. `None` means the registry has
    nothing installed, which is read as "do not filter" rather than "hide everything".
    """
    allowed = None if (include_disabled or enabled is None) else sorted(enabled)
    params: dict[str, Any] = {
        "status": status,
        "doc_type": doc_type,
        "pack_id": pack_id,
        "packs": allowed,
        "limit": limit,
        "offset": offset,
    }
    with conn.cursor() as cur:
        cur.execute(COUNT_DOCUMENTS, params)
        row = cur.fetchone()
        total = int(row[0]) if row else 0
        cur.execute(SELECT_DOCUMENTS, params)
        rows = cur.fetchall()

    doc_types = {row[0]: (row[5], row[4]) for row in rows}
    facts = _facts_for(conn, [row[0] for row in rows], doc_types)

    listed = [
        VaultDocument(
            document_id=row[0],
            original_name=row[1],
            mime=row[2],
            pages=row[3],
            doc_type=row[4],
            pack_id=row[5],
            pack_enabled=row[5] is None or enabled is None or row[5] in enabled,
            status=row[6],
            quarantine_reason=row[7],
            ingested_at=row[8],
            synthetic=bool(row[9]),
            facts=facts.get(row[0], []),
        )
        for row in rows
    ]
    return VaultPage(documents=listed, total=total, limit=limit, offset=offset)
