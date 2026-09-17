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
nothing disabled it. Nor is a document written as `core`, which is every document since ADR 0017:
`core.registry.enabled_pack_ids` always includes it.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from core.packs import catalog

log = logging.getLogger(__name__)

# Below this, a field is shown to a person to check rather than presented as read.
#
# It is not a pack rule and deliberately not in `pack.yaml`: `guardrails.abstain_below` governs
# whether an *answer* may be given, which is a different question from whether an extracted
# field is worth a second look. One number, here, so that the screen cannot invent its own and
# the command line and the interface flag the same rows.
#
# 0.75 is a starting point, not a finding. The number that belongs here is the one where the
# extractor's confidence stops predicting agreement with Desmond's register — Lane B can measure
# it once extraction is scored, and when they do, this constant and an ADR are what change.
NEEDS_REVIEW_BELOW = 0.75

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

# One document, by id. The same column list in the same order as `SELECT_DOCUMENTS`, because
# `_as_document` below reads both by position and a divergence would be silent.
SELECT_DOCUMENT = """
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
 WHERE d.id = %(document_id)s::uuid
"""

# What a citation has, turned into what a link needs.
#
# The modules and the answer graph format a citation the way a person says it — "policy.pdf,
# page 3" — so by the time it reaches a screen the id has been thrown away. Rather than change
# every caller's citation format, the names are looked up again here, once per response.
#
# `DISTINCT ON` keeps the most recently filed document when two files share a name. That is a
# guess, and it is the only guess in this module: a household with two `policy.pdf` gets a link
# to the newer one. The fix is for a citation to carry the id, which is a change to the answer
# graph and therefore not this pull request.
RESOLVE_NAMES = """
SELECT DISTINCT ON (d.original_name)
       d.original_name,
       d.id,
       d.pages
  FROM documents d
 WHERE d.original_name = ANY(%(names)s::text[])
 ORDER BY d.original_name, d.ingested_at DESC
"""

# Every fact carries the page it was read off, because `facts.page` is NOT NULL and this is
# the screen where a person checks that claim against the document.
SELECT_FACTS_FOR_DOCUMENTS = """
SELECT f.id,
       f.document_id,
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

    id: int  # what a correction addresses; see `core/corrections.py`
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
    def needs_review(self) -> bool:
        """Worth a person's eyes: the extractor was unsure and nobody has looked yet.

        A field a person has confirmed is never flagged again, whatever the model thought of it
        at the time. That is the correction loop closing rather than a screen nagging.
        """
        return not self.verified_by_user and self.confidence < NEEDS_REVIEW_BELOW

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


def declared_type(pack_id: str | None, doc_type: str | None, key: str) -> str | None:
    """What the core catalogue says this field is, or None when it does not declare it.

    `pack_id` is ignored: every document type is the catalogue's (ADR 0017), whichever pack id a
    row was written under.
    """
    if not doc_type:
        return None
    spec = catalog().documents.field_index().get((doc_type, key))
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
        fact_id,
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
                id=int(fact_id),
                key=key,
                subject=subject,
                page=page,
                confidence=float(confidence),
                verified_by_user=bool(verified_by_user),
                pack_id=fact_pack_id,
                value_text=value_text,
                value_num=value_num,
                value_date=value_date,
                declared_type=declared_type(pack_id or fact_pack_id, doc_type, key),
            )
        )
    return grouped


def _as_document(
    row: tuple[Any, ...], enabled: frozenset[str] | None, facts: list[Fact]
) -> VaultDocument:
    """One row of `SELECT_DOCUMENTS` or `SELECT_DOCUMENT` — the two share a column list."""
    return VaultDocument(
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
        facts=facts,
    )


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

    listed = [_as_document(row, enabled, facts.get(row[0], [])) for row in rows]
    return VaultPage(documents=listed, total=total, limit=limit, offset=offset)


def document(
    conn: Any, document_id: Any, *, enabled: frozenset[str] | None = None
) -> VaultDocument | None:
    """One document and its facts, or `None` when there is no such id.

    Deliberately not filtered by the enabled set. A person who followed a citation to a
    document is looking at a specific thing and asking what it says; hiding it because its pack
    is switched off would be a dead end rather than an answer. `pack_enabled` tells the screen
    the truth and lets it say so.
    """
    with conn.cursor() as cur:
        cur.execute(SELECT_DOCUMENT, {"document_id": str(document_id)})
        row = cur.fetchone()
    if row is None:
        return None
    facts = _facts_for(conn, [row[0]], {row[0]: (row[5], row[4])})
    return _as_document(row, enabled, facts.get(row[0], []))


@dataclass(frozen=True, slots=True)
class NamedDocument:
    """What a citation's document name resolves to."""

    document_id: Any
    pages: int | None


def resolve_names(conn: Any, names: list[str]) -> dict[str, NamedDocument]:
    """Document names to ids, so a citation becomes something a person can open.

    One query for every name in a response, not one per chip. Names that match nothing are
    simply absent from the result: a citation whose document has since been deleted still says
    what it said, it just stops being a link.
    """
    wanted = sorted({name for name in names if name})
    if not wanted:
        return {}
    with conn.cursor() as cur:
        cur.execute(RESOLVE_NAMES, {"names": wanted})
        rows = cur.fetchall()
    return {
        str(original_name): NamedDocument(document_id=document_id, pages=pages)
        for original_name, document_id, pages in rows
    }
