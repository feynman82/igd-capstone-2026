"""When the nightly sweeps run, read from the modules' own manifests.

A module already declares how it is triggered — `modules/reminder/module.yaml` says
`cron: "0 7 * * *"`. Writing that cron out a second time here would be the same mistake as
hand-editing a generated file: the schedule would be true in two places and eventually in
neither. So the manifest is parsed, validated against `ModuleManifest`, and the cron becomes
a beat entry.

Alert is the exception, and it is a deliberate one. Its manifest says `on: fact_write`, which
is the right trigger and is not built yet. Until it is, a nightly sweep is what surfaces a
crossed threshold, and the module's own 168-hour debounce is what stops the nightly sweep
becoming a nightly notification. It runs five minutes after Reminder so the two are not
competing for the same connection. That divergence is recorded in ADR 0008 rather than by
quietly editing the manifest — the manifest describes the design, and this describes today.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from core.contracts import ModuleManifest

MODULES_DIR = Path(__file__).resolve().parents[2] / "modules"

ALERT_FALLBACK_CRON = "5 7 * * *"  # not in the manifest; see the note above and ADR 0008
# The calendar digest (ADR 0020) is not a module, so it has no manifest to read a cron from; this
# line is its one place. After both sweeps, so it never races them for a connection.
DIGEST_CRON = "10 7 * * *"


def manifest(module_id: str) -> ModuleManifest:
    raw = yaml.safe_load((MODULES_DIR / module_id / "module.yaml").read_text(encoding="utf-8"))
    return ModuleManifest.model_validate(raw)


def crontab_from(expression: str) -> Any:
    """A five-field cron expression as Celery understands it."""
    from celery.schedules import crontab

    minute, hour, day_of_month, month_of_year, day_of_week = expression.split()
    return crontab(
        minute=minute,
        hour=hour,
        day_of_month=day_of_month,
        month_of_year=month_of_year,
        day_of_week=day_of_week,
    )


def cron_expressions() -> dict[str, str]:
    """The cron line for each swept module, by module id. Testable without Celery installed."""
    reminder = manifest("reminder").runs
    if reminder.on != "schedule" or not reminder.cron:
        raise ValueError("modules/reminder/module.yaml no longer declares a cron schedule")
    return {"reminder": reminder.cron, "alert": ALERT_FALLBACK_CRON}


def beat_schedule() -> dict[str, dict[str, Any]]:
    crons = cron_expressions()
    return {
        "reminder-nightly": {
            "task": "parrot.sweep_reminders",
            "schedule": crontab_from(crons["reminder"]),
        },
        "alert-nightly": {
            "task": "parrot.sweep_alerts",
            "schedule": crontab_from(crons["alert"]),
        },
        "calendar-digest": {
            "task": "parrot.calendar_digest",
            "schedule": crontab_from(DIGEST_CRON),
        },
    }
