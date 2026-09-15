"""The record of every advised or withheld answer (ADR 0016).

`advice_records` keeps the full basis an advice answer was given on: which facts and rule values
it read, the figures a calculator produced, the verdict, which consent covered it and a hash of
the disclaimer it was signed with. It never keeps the number a rule value held — that lives in
`grounding_values` and can change — so `basis` is a snapshot, not a second source of truth.

This module writes but never commits: an advice answer's consent check, its calculation and its
record belong to one transaction, and only the caller that opened it knows when that transaction
is done.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from core.graph.advice import AdviceRecord

# --------------------------------------------------------------------------------- the SQL
#
# Rule 1: every statement is written here and parameterised. Nothing is assembled at runtime.

INSERT_RECORD = """
INSERT INTO advice_records
    (thread_id, pack_id, pack_version, shape, subject, subject_person_ids, consent_id,
     outcome, verdict, basis, disclaimer_sha256, answer_text)
VALUES
    (%(thread_id)s, %(pack_id)s, %(pack_version)s, %(shape)s, %(subject)s,
     %(subject_person_ids)s, %(consent_id)s, %(outcome)s, %(verdict)s, %(basis)s::jsonb,
     %(disclaimer_sha256)s, %(answer_text)s)
"""


@dataclass(frozen=True, slots=True)
class HouseholdAdviceLog:
    """`core.graph.advice.AdviceLog` over a live connection.

    `basis` is dumped with `default=str` because it may hold a `Decimal` figure or a `date` a
    rule value's effective range named, and neither is JSON-native; a hand-rolled serialiser
    that special-cased them would be one more thing to keep in step with `core.graph.advice`.
    """

    conn: Any

    def record(self, entry: AdviceRecord) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                INSERT_RECORD,
                {
                    "thread_id": entry.thread_id,
                    "pack_id": entry.pack_id,
                    "pack_version": entry.pack_version,
                    "shape": entry.shape,
                    "subject": entry.subject,
                    "subject_person_ids": list(entry.person_ids),
                    "consent_id": entry.consent_id,
                    "outcome": entry.outcome,
                    "verdict": entry.verdict,
                    "basis": json.dumps(entry.basis, default=str),
                    "disclaimer_sha256": hashlib.sha256(entry.disclaimer.encode("utf-8")).digest(),
                    "answer_text": entry.answer_text,
                },
            )
