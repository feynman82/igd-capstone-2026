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


# ------------------------------------------------------------------------------ closing one
#
# Three things a person can do to a row on Today, and only two of them need a new column — so
# only two of them are here. `queries.MARK_DONE` and `queries.MARK_DISMISSED` were written when
# the table was designed and have had no caller until now.


class UnknownObligation(LookupError):
    """Safe to show: there is no obligation with that id, or it is already closed."""


def close(conn: Any, obligation_id: int, *, state: str) -> None:
    """Mark an obligation done or dismissed. Both are final; neither deletes anything.

    `done` means the person did the thing. `dismissed` means it was never theirs to do. The
    distinction is not cosmetic: an evaluation that counts missed obligations has to be able to
    tell "renewed it" from "this reminder should not have existed".
    """
    statement = {"done": queries.MARK_DONE, "dismissed": queries.MARK_DISMISSED}.get(state)
    if statement is None:  # pragma: no cover - the caller's type already forbids it
        raise ValueError(f"an obligation is closed as done or dismissed, not {state!r}")
    with conn.cursor() as cur:
        cur.execute(queries.SELECT_OPEN, {"obligation_id": obligation_id})
        if cur.fetchone() is None:
            raise UnknownObligation(f"no open obligation with id {obligation_id}")
        cur.execute(statement, {"obligation_id": obligation_id})
    conn.commit()
    log.info("obligation %s marked %s", obligation_id, state)


def snooze(conn: Any, obligation_id: int, on: date | None = None) -> date | None:
    """Quiet until the next lead window opens. Returns the date it will speak again, if any.

    **Snooze here means "not again until it gets more urgent", not "not for N days".** A pack
    declares its lead windows — insurance uses 60, 30 and 7 — and snoozing at 60 days out
    silences the row until day 30, when the situation has genuinely changed. That is a better
    default than an arbitrary number of days a person has to pick while they are busy, and it
    is the only version that needs no new column: it stamps `last_notified_at`, which is exactly
    what `already_said` reads.

    The cost of that choice, stated plainly because someone will ask: a person cannot say "next
    Tuesday". Giving them that means an `obligations.snoozed_until` column, which is a
    migration, which is its own reviewed pull request.
    """
    when = on or date.today()
    stamp = datetime.combine(when, time.min).astimezone()
    with conn.cursor() as cur:
        cur.execute(queries.SELECT_OPEN, {"obligation_id": obligation_id})
        row = cur.fetchone()
        if row is None:
            raise UnknownObligation(f"no open obligation with id {obligation_id}")
        _id, due_date, lead_days = row
        cur.execute(queries.MARK_NOTIFIED, {"obligation_id": obligation_id, "now": stamp})
    conn.commit()

    return next_window(when, due_date, list(lead_days or []))


def next_window(after: date, due: date, lead_days: list[int]) -> date | None:
    """The day this obligation is allowed to speak again, or None when it has no window left.

    The tightest window it is already inside is the one being silenced, so the answer is the day
    the *next* one down opens. Past the last window there is nothing further to say until the
    date itself passes and it becomes overdue, which is a different list on a different part of
    the screen.
    """
    days_left = (due - after).days
    current = current_lead(days_left, lead_days)
    tighter = [lead for lead in sorted(lead_days) if current is None or lead < current]
    if not tighter:
        return None
    return due - timedelta(days=tighter[-1])
