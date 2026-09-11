"""A person fixing a field the extractor got wrong.

This is the one place in the system where a human writes to `facts`, and it exists because the
extractor will be wrong sometimes. Designing for that honestly is what separates a system
people keep using from one they abandon after the third bad date.

Two things happen on a correction, and the second is the one that matters later:

1. The fact is updated in place, its confidence set to 1.0 and `verified_by_user` to true. It
   stops being flagged, because a person has looked at the paper.
2. **What it used to say is written to `traces`.** An UPDATE on its own loses the model's
   answer, and the model's answer beside the right one is precisely what a labelled example is
   — `db/migrations/0001_init.sql` calls `verified_by_user` "a labelled example" and this is
   what makes that true rather than aspirational. `traces` already describes itself as "both
   the evaluation dataset and the audit trail", so the corrections land there under
   `node = 'correction'` and Lane B can read them without a new table.

**The pack decides what a value is, not the caller.** A screen cannot say "store this as text";
it sends what the person typed and the field's declared type in `pack.yaml` decides which
column it lands in, via the same `FACT_COLUMN` map the extractor and the scorer use. A value
that will not parse as the declared type is refused with a sentence, not coerced — a premium
silently stored as the text "four hundred" would be worse than the wrong number it replaced.

All three value columns are written on every correction, two of them as NULL. That is
deliberate: a fact the extractor put in the wrong column is repaired by the same statement
rather than left with two values and no rule about which one wins.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from core import vault
from core.contracts import FACT_COLUMN
from core.ingest import sql

log = logging.getLogger(__name__)

# The fact as it stands, plus the document context needed to ask the pack what its type is.
SELECT_FACT = """
SELECT f.id,
       f.document_id,
       f.page,
       f.pack_id,
       f.key,
       f.subject,
       f.value_text,
       f.value_num,
       f.value_date,
       f.confidence,
       f.verified_by_user,
       d.doc_type,
       d.original_name
  FROM facts f
  JOIN documents d ON d.id = f.document_id
 WHERE f.id = %(fact_id)s
"""

# Every value column written, so a value that was extracted into the wrong one is repaired
# rather than duplicated. `page` is never touched: a person correcting what a field says is not
# telling us it came from somewhere else.
UPDATE_FACT = """
UPDATE facts
   SET value_text = %(value_text)s,
       value_num  = %(value_num)s,
       value_date = %(value_date)s,
       confidence = 1.0,
       verified_by_user = true
 WHERE id = %(fact_id)s
"""


class UnknownFact(LookupError):
    """Safe to show: there is no fact with that id."""


class CorrectionRejected(ValueError):
    """Safe to show: the value does not fit what this field is declared to be."""


@dataclass(frozen=True, slots=True)
class Corrected:
    """What changed, in the words the screen will use to confirm it."""

    fact_id: int
    key: str
    document_id: Any
    document_name: str
    page: int
    was: str | float | None
    now: str | float | None
    was_confidence: float
    value_type: str


def _columns(value: str, field_type: str) -> tuple[str | None, Decimal | None, date | None]:
    """`(value_text, value_num, value_date)` — exactly one of them set.

    The declared type chooses the column. `core/contracts.py` already owns that map; this reads
    it rather than repeating it, so a type added to a pack cannot land somewhere new here.
    """
    text = value.strip()
    if not text:
        raise CorrectionRejected("a corrected field cannot be left empty")

    column = FACT_COLUMN.get(field_type, "value_text")

    if column == "value_date":
        try:
            return None, None, date.fromisoformat(text)
        except ValueError as error:
            raise CorrectionRejected(
                f"{text!r} is not a date. Write it as YYYY-MM-DD, for example 2026-10-14."
            ) from error

    if column == "value_num":
        try:
            return None, Decimal(text.replace(",", "").lstrip("$")), None
        except (InvalidOperation, ArithmeticError) as error:
            raise CorrectionRejected(f"{text!r} is not a number.") from error

    return text, None, None


def correct(conn: Any, fact_id: int, value: str) -> Corrected:
    """Store what a person says this field actually says, and keep what it used to say.

    Commits both writes together: a correction whose trace was lost is a correction that cannot
    be scored, which is most of the reason for making it.
    """
    with conn.cursor() as cur:
        cur.execute(SELECT_FACT, {"fact_id": fact_id})
        row = cur.fetchone()
    if row is None:
        raise UnknownFact(f"no fact with id {fact_id}")

    (
        _id,
        document_id,
        page,
        pack_id,
        key,
        subject,
        value_text,
        value_num,
        value_date,
        confidence,
        _verified,
        doc_type,
        original_name,
    ) = row

    before = vault.Fact(
        id=int(fact_id),
        key=key,
        subject=subject,
        page=int(page),
        confidence=float(confidence),
        verified_by_user=bool(_verified),
        pack_id=pack_id,
        value_text=value_text,
        value_num=value_num,
        value_date=value_date,
        declared_type=vault.declared_type(pack_id, doc_type, key),
    )

    field_type = before.value_type
    text, number, when = _columns(value, field_type)

    after = vault.Fact(
        id=int(fact_id),
        key=key,
        subject=subject,
        page=int(page),
        confidence=1.0,
        verified_by_user=True,
        pack_id=pack_id,
        value_text=text,
        value_num=number,
        value_date=when,
        declared_type=before.declared_type,
    )

    with conn.cursor() as cur:
        cur.execute(
            UPDATE_FACT,
            {
                "fact_id": fact_id,
                "value_text": text,
                "value_num": number,
                "value_date": when,
            },
        )
        cur.execute(
            sql.INSERT_TRACE,
            {
                "thread_id": str(document_id),
                "node": "correction",
                "latency_ms": 0,  # a person, not a model; the column is NOT NULL
                "model": None,
                "payload": json.dumps(
                    {
                        "fact_id": int(fact_id),
                        "pack_id": pack_id,
                        "key": key,
                        "subject": subject,
                        "page": int(page),
                        "type": field_type,
                        "was": before.value,
                        "now": after.value,
                        "was_confidence": float(confidence),
                    }
                ),
            },
        )
    conn.commit()

    log.info("corrected %s on %s page %s", key, original_name, page)
    return Corrected(
        fact_id=int(fact_id),
        key=key,
        document_id=document_id,
        document_name=original_name,
        page=int(page),
        was=before.value,
        now=after.value,
        was_confidence=float(confidence),
        value_type=field_type,
    )
