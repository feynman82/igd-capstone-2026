"""The Reminder module: a nightly sweep of obligations, and nothing fires twice.

Reads `obligations`, writes only its own bookkeeping on them. It never touches `facts`, never
touches retrieval, and — rule 7 — never imports from `web/` or `api/`. What it returns is typed
rows; something else decides how to draw them.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Any

from modules.reminder import queries

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Due:
    obligation_id: int
    pack_id: str
    label: str
    due_date: date
    days_left: int
    lead: int  # the window it fell into: 60, 30, 7
    document_id: Any | None
    page: int | None
    document_name: str | None

    @property
    def urgency(self) -> int:
        """Smaller is more urgent. The Today surface orders by this."""
        return self.days_left

    def line(self) -> str:
        when = "today" if self.days_left == 0 else f"in {self.days_left} day(s)"
        source = f" — {self.document_name}, page {self.page}" if self.document_name else ""
        return f"{self.label}: due {when} ({self.due_date}){source}"


def current_lead(days_left: int, lead_days: list[int]) -> int | None:
    """The tightest lead window this obligation has entered, or None if it has entered none."""
    active = [lead for lead in sorted(lead_days) if days_left <= lead]
    return active[0] if active else None


def already_said(last_notified_at: datetime | None, due: date, lead: int) -> bool:
    """True when this exact window has already been mentioned.

    The comparison is by date rather than by timestamp: a person who is reminded at 07:00 and
    again at 23:00 on the same day has been reminded twice, whatever the clock says.
    """
    if last_notified_at is None:
        return False
    window_opened = due - timedelta(days=lead)
    return last_notified_at.date() >= window_opened


def sweep(
    conn: Any,
    today: date | None = None,
    *,
    mark: bool = True,
    enabled: frozenset[str] | None = None,
) -> list[Due]:
    """Everything inside a lead window that has not already been said for that window.

    `mark=False` runs the sweep without recording it, which is what a dry run and the tests use.

    `enabled` is the set of pack ids a person has left switched on, from
    `core.registry.enabled_pack_ids`. A disabled pack's obligations are skipped before anything
    is marked, so switching a pack off silences it rather than burning its lead windows. `None`
    means no filter — the registry is the caller's business, not the module's.
    """
    now = today or date.today()
    with conn.cursor() as cur:
        cur.execute(queries.DUE_SWEEP, {"floor": now})
        rows = cur.fetchall()

    due: list[Due] = []
    for (
        obligation_id,
        pack_id,
        label,
        due_date,
        lead_days,
        _state,
        last_notified_at,
        document_id,
        page,
        document_name,
    ) in rows:
        if enabled is not None and pack_id not in enabled:
            continue
        days_left = (due_date - now).days
        lead = current_lead(days_left, list(lead_days or []))
        if lead is None:
            continue
        if already_said(last_notified_at, due_date, lead):
            continue
        due.append(
            Due(
                obligation_id=obligation_id,
                pack_id=pack_id,
                label=label,
                due_date=due_date,
                days_left=days_left,
                lead=lead,
                document_id=document_id,
                page=page,
                document_name=document_name,
            )
        )

    due.sort(key=lambda item: item.urgency)
    if mark and due:
        # Stamped with the date the sweep was run *for*, not the wall clock. `--as-of` has to
        # move the whole sweep or it cannot demonstrate the second window at all, and
        # `already_said` compares dates, so midnight loses nothing.
        stamp = datetime.combine(now, time.min).astimezone()
        with conn.cursor() as cur:
            for item in due:
                cur.execute(
                    queries.MARK_NOTIFIED,
                    {"obligation_id": item.obligation_id, "now": stamp},
                )
        conn.commit()
    return due


def overdue(
    conn: Any,
    today: date | None = None,
    *,
    enabled: frozenset[str] | None = None,
) -> list[tuple[int, str, str, date, str | None]]:
    """Past their date and never closed. A different problem from a reminder, shown separately.

    Filtered by the same enabled set as `sweep`: a pack that is switched off does not get to
    keep shouting about the dates it missed.
    """
    with conn.cursor() as cur:
        cur.execute(queries.OVERDUE, {"today": today or date.today()})
        rows = list(cur.fetchall())
    if enabled is None:
        return rows
    return [row for row in rows if row[1] in enabled]
