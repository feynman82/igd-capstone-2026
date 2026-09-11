"""Turn a dated fact into a commitment to do something about it.

A fact is a statement about the world: *this policy expires on 30 November 2026*. An obligation
is what follows from it: *something has to happen before then, and you want warning at 60, 30
and 7 days*. The pack says which of its fields become obligations, in `registers.reminder`, so
adding a reminder is a change to one YAML file rather than to any code here.

This runs in the facts lane of the ingestion pipeline, inside the same transaction, because an
obligation that outlives the fact it came from is exactly the disagreement the single
transaction exists to prevent. `obligations.fact_id` cascades on delete, so re-extracting a
document replaces its obligations rather than accumulating them.

The Reminder module reads what this writes. It never writes facts, and this never notifies.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

from core.contracts import ReminderConfig
from core.ingest import sql
from core.ingest.extract import ExtractedFact
from core.packs import InstalledPack

log = logging.getLogger(__name__)


def _label(config: ReminderConfig, subject: str | None) -> str:
    """What a person is shown. The key is the pack's word for it; the subject says whose."""
    readable = config.key.replace("_", " ")
    return f"{readable} — {subject}" if subject else readable


def from_facts(
    cur: Any,
    installed: InstalledPack,
    facts: list[tuple[int, ExtractedFact]],
) -> int:
    """Create the obligations this pack declares for these newly written facts.

    `facts` is (fact_id, fact) because an obligation cites the row it came from, which is how a
    reminder can say *which document* said so.
    """
    configs = installed.manifest.registers.reminder or []
    written = 0
    for config in configs:
        if config.from_field is None:
            continue
        for fact_id, fact in facts:
            if fact.key != config.from_field or fact.value_date is None:
                continue
            cur.execute(
                sql.INSERT_OBLIGATION,
                {
                    "fact_id": fact_id,
                    "pack_id": installed.id,
                    "label": _label(config, fact.subject),
                    "due_date": fact.value_date,
                    "lead_days": list(config.lead_days),
                    "recurrence": None,
                },
            )
            written += 1
    return written


def fixed(cur: Any, installed: InstalledPack, today: date | None = None) -> int:
    """Create the pack's calendar obligations — a filing deadline belongs to no document.

    Inserted once and recognised thereafter by pack, label and date, because there is no fact to
    hang it on and therefore no cascade to clean it up. A deadline already in the past is not
    created: a reminder for it could only ever be wrong.
    """
    now = today or date.today()
    written = 0
    for config in installed.manifest.registers.reminder or []:
        if config.on_date is None or config.on_date < now:
            continue
        cur.execute(
            sql.INSERT_FIXED_OBLIGATION,
            {
                "pack_id": installed.id,
                "label": _label(config, None),
                "due_date": config.on_date,
                "lead_days": list(config.lead_days),
                "recurrence": "annual",
            },
        )
        if cur.fetchone() is not None:
            written += 1
    return written
