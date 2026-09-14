"""A person's approval, standing between a model's extraction and any calculator that reads it.

`core.grounding.index` writes every value it keeps as `pending`. Nothing else in the codebase
may set a row `approved`: that is Siew's decision alone, made from the passage and the source it
came from, never from the number by itself (ADR 0016). `approve` and `reject` therefore only
ever touch rows that are still `pending` — a value already decided is not silently redecided by
a second run of the reviewer's tool.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any

# --------------------------------------------------------------------------------- the SQL
#
# The cast on %(pack_id)s follows core/vault.py: an untyped NULL gives Postgres nothing to
# infer a type from, so the optional filter says what it is.

SELECT_PENDING = """
SELECT v.id, v.pack_id, v.key, v.unit, v.value_num, v.value_text, v.qualifiers, v.passage,
       s.title, s.publisher, s.url
  FROM grounding_values v
  JOIN grounding_sources s ON s.id = v.source_id
 WHERE v.status = 'pending'
   AND (%(pack_id)s::text IS NULL OR v.pack_id = %(pack_id)s::text)
 ORDER BY v.created_at, v.id
"""

APPROVE = """
UPDATE grounding_values
   SET status = 'approved', reviewed_by = %(reviewer)s, reviewed_on = %(on)s
 WHERE id = ANY(%(ids)s) AND status = 'pending'
"""

REJECT = """
UPDATE grounding_values
   SET status = 'rejected', reviewed_by = %(reviewer)s, reviewed_on = %(on)s, note = %(note)s
 WHERE id = ANY(%(ids)s) AND status = 'pending'
"""


# -------------------------------------------------------------------------------- the rows


@dataclass(frozen=True, slots=True)
class PendingValue:
    """One value waiting for a person to sign off, with what they need to see to do it."""

    id: int
    pack_id: str
    key: str
    unit: str
    value_num: Decimal | None
    value_text: str | None
    qualifiers: dict[str, str]
    passage: str
    source_title: str
    publisher: str
    url: str


def pending(conn: Any, pack_id: str | None = None) -> list[PendingValue]:
    """Every value still waiting for review, oldest first, optionally for one pack."""
    with conn.cursor() as cur:
        cur.execute(SELECT_PENDING, {"pack_id": pack_id})
        rows = cur.fetchall()
    return [
        PendingValue(
            id=row[0],
            pack_id=row[1],
            key=row[2],
            unit=row[3],
            value_num=row[4],
            value_text=row[5],
            qualifiers=dict(row[6]),
            passage=row[7],
            source_title=row[8],
            publisher=row[9],
            url=row[10],
        )
        for row in rows
    ]


def approve(conn: Any, ids: Sequence[int], *, reviewer: str, on: date) -> int:
    """Approve these ids, ignoring any that are no longer `pending`. Returns the count changed."""
    with conn.cursor() as cur:
        cur.execute(APPROVE, {"ids": list(ids), "reviewer": reviewer, "on": on})
        count: int = cur.rowcount
    conn.commit()
    return count


def reject(conn: Any, ids: Sequence[int], *, reviewer: str, on: date, note: str) -> int:
    """Reject these ids with a note, ignoring any that are no longer `pending`."""
    with conn.cursor() as cur:
        cur.execute(REJECT, {"ids": list(ids), "reviewer": reviewer, "on": on, "note": note})
        count: int = cur.rowcount
    conn.commit()
    return count
