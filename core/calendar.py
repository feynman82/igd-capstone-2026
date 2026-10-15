"""The household calendar: what the family has on, and the deadlines its documents set. ADR 0020.

Two kinds of entry, kept apart on purpose.

**An event is typed in by a person.** Lucas's swimming, Dad's polyclinic review, dinner at Mum's.
It lives in `calendar_events`, it can be created, changed and deleted, and nothing about it is a
claim about a document.

**A deadline is read off a document.** A renewal date or a tax due date is already an
`obligations` row with a fact and a page behind it. The calendar shows it, cited to that page,
and never copies it: a date written down twice is a date that can disagree with itself.

**Repeats are expanded here, in Python**, between two dates. A series is one row; an edit or a
delete is to the whole series (ADR 0020, as SDRR's ADR 0052 decided for the same reason: a
household calendar that half-edits a series is one nobody trusts). A monthly event on the 31st
skips the months that have no 31st, as iCalendar does, rather than moving to the 30th.

**Questions about it are answered by code.** "What's on this week?" and "when is Lucas's next
swimming lesson?" have exact answers in these rows, so no model is asked to paraphrase them: a
4B model handed eight events once dropped one and, on SDRR, once named the wrong person. Every
line is cited — an event to the calendar on its date, a deadline to its document's page.

Rule 1 holds: every query is hand-written and parameterised below.
"""

from __future__ import annotations

import calendar as months
import re
from dataclasses import dataclass, field
from datetime import date, time, timedelta
from typing import Any, Literal

Repeat = Literal["never", "daily", "weekly", "monthly", "yearly"]
REPEATS: tuple[Repeat, ...] = ("never", "daily", "weekly", "monthly", "yearly")

# A month grid is six weeks. Anything wider is not a screen, it is an export.
MAX_RANGE_DAYS = 62

_COLUMNS = """
       e.id, e.title, e.starts_on, e.ends_on, e.start_time, e.end_time, e.location, e.notes,
       e.person_id, p.display_name, e.repeat, e.repeat_until, e.created_via, e.source
"""

# Everything that could have a date inside [start, end]: one-off events overlapping it, and every
# series that began before its end and has not finished before its start.
SELECT_BETWEEN = f"""
SELECT {_COLUMNS}
  FROM calendar_events e
  LEFT JOIN people p ON p.id = e.person_id
 WHERE e.starts_on <= %(end)s
   AND (   (e.repeat = 'never' AND coalesce(e.ends_on, e.starts_on) >= %(start)s)
        OR (e.repeat <> 'never' AND (e.repeat_until IS NULL OR e.repeat_until >= %(start)s)))
 ORDER BY e.starts_on, e.start_time NULLS FIRST, e.id
"""

SELECT_ONE = f"""
SELECT {_COLUMNS}
  FROM calendar_events e
  LEFT JOIN people p ON p.id = e.person_id
 WHERE e.id = %(id)s
"""

INSERT = """
INSERT INTO calendar_events (title, starts_on, ends_on, start_time, end_time, location, notes,
                             person_id, repeat, repeat_until, created_via)
VALUES (%(title)s, %(starts_on)s, %(ends_on)s, %(start_time)s, %(end_time)s, %(location)s,
        %(notes)s, %(person_id)s, %(repeat)s, %(repeat_until)s, %(created_via)s)
RETURNING id
"""

UPDATE = """
UPDATE calendar_events
   SET title = %(title)s, starts_on = %(starts_on)s, ends_on = %(ends_on)s,
       start_time = %(start_time)s, end_time = %(end_time)s, location = %(location)s,
       notes = %(notes)s, person_id = %(person_id)s, repeat = %(repeat)s,
       repeat_until = %(repeat_until)s, updated_at = now()
 WHERE id = %(id)s
"""

DELETE = "DELETE FROM calendar_events WHERE id = %(id)s"

# The demonstration's synthetic entries, and only those: `scripts/seed_calendar.py` re-seeds by
# forgetting its own rows, never a person's.
DELETE_SEEDED = "DELETE FROM calendar_events WHERE created_via = 'seed'"

# Open deadlines inside a range, with the page they were read from. Done and dismissed ones are
# finished business and stay off the calendar, as they stay off Today.
DEADLINES = """
SELECT o.id, o.pack_id, o.label, o.due_date, f.document_id, f.page, d.original_name
  FROM obligations o
  LEFT JOIN facts f     ON f.id = o.fact_id
  LEFT JOIN documents d ON d.id = f.document_id
 WHERE o.state IN ('pending', 'notified')
   AND o.due_date BETWEEN %(start)s AND %(end)s
 ORDER BY o.due_date, o.id
"""


# ------------------------------------------------------------------------------- the shapes


@dataclass(frozen=True, slots=True)
class EventFields:
    """What a person can set. The API validates it; this is what the queries are given."""

    title: str
    starts_on: date
    ends_on: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    location: str | None = None
    notes: str | None = None
    person_id: int | None = None
    repeat: Repeat = "never"
    repeat_until: date | None = None


@dataclass(frozen=True, slots=True)
class Event:
    id: int
    title: str
    starts_on: date
    ends_on: date | None
    start_time: time | None
    end_time: time | None
    location: str | None
    notes: str | None
    person_id: int | None
    person: str | None
    repeat: Repeat
    repeat_until: date | None
    created_via: str
    source: str

    @property
    def days(self) -> int:
        """How many days one occurrence spans: 1 for a one-day event."""
        return ((self.ends_on or self.starts_on) - self.starts_on).days + 1


@dataclass(frozen=True, slots=True)
class Occurrence:
    """One event on one date. A three-day event is three of these, `day` 1 to 3 of 3."""

    event: Event
    on: date
    day: int = 1


@dataclass(frozen=True, slots=True)
class Deadline:
    obligation_id: int
    pack_id: str
    label: str
    due_date: date
    document_id: Any | None
    page: int | None
    document_name: str | None


@dataclass(frozen=True, slots=True)
class Line:
    """One sentence of a calendar answer and what it rests on.

    A line with a `document_name` is a deadline and is cited to the page its date was read from;
    any other line is cited to the calendar on `on`, the date it is about.
    """

    text: str
    on: date | None = None
    document_id: Any | None = None
    document_name: str | None = None
    page: int | None = None


@dataclass(frozen=True, slots=True)
class Reply:
    lines: list[Line] = field(default_factory=list)
    start: date | None = None
    end: date | None = None


# ------------------------------------------------------------------------------- repeats


def _shift(start: date, repeat: Repeat, step: int) -> date | None:
    """The `step`-th date of a series, or None when that month or year has no such day."""
    if repeat == "daily":
        return start + timedelta(days=step)
    if repeat == "weekly":
        return start + timedelta(weeks=step)
    if repeat == "monthly":
        month0 = start.month - 1 + step
        year, month = start.year + month0 // 12, month0 % 12 + 1
    else:  # yearly
        year, month = start.year + step, start.month
    if start.day > months.monthrange(year, month)[1]:
        return None  # 31 April does not exist, and 29 February mostly does not
    return date(year, month, start.day)


def first_days(event: Event, start: date, end: date) -> list[date]:
    """The first day of every occurrence that touches [start, end]."""
    span = timedelta(days=event.days - 1)
    if event.repeat == "never":
        return (
            [event.starts_on] if event.starts_on <= end and event.starts_on + span >= start else []
        )
    last = min(end, event.repeat_until or end)
    # Jump close to the range rather than walking a daily series from 2019.
    if event.repeat in ("daily", "weekly"):
        period = 1 if event.repeat == "daily" else 7
        step = max(0, ((start - span - event.starts_on).days) // period)
    elif event.repeat == "monthly":
        step = max(
            0, (start.year - event.starts_on.year) * 12 + start.month - event.starts_on.month - 1
        )
    else:
        step = max(0, start.year - event.starts_on.year - 1)
    out: list[date] = []
    while True:
        when = _shift(event.starts_on, event.repeat, step)
        step += 1
        if when is None:
            continue
        if when > last:
            return out
        if when + span >= start:
            out.append(when)


def expand(events: list[Event], start: date, end: date) -> list[Occurrence]:
    """Every day of every occurrence inside [start, end], ordered as a day is read."""
    out: list[Occurrence] = []
    for event in events:
        for first in first_days(event, start, end):
            for offset in range(event.days):
                on = first + timedelta(days=offset)
                if start <= on <= end:
                    out.append(Occurrence(event, on, offset + 1))
    out.sort(
        key=lambda o: (
            o.on,
            o.event.start_time is not None,
            o.event.start_time or time(),
            o.event.id,
        )
    )
    return out


# ------------------------------------------------------------------------------- the store


def _event(row: tuple[Any, ...]) -> Event:
    return Event(*row)


def _params(fields: EventFields) -> dict[str, Any]:
    return {
        "title": fields.title.strip(),
        "starts_on": fields.starts_on,
        "ends_on": fields.ends_on if fields.ends_on and fields.ends_on > fields.starts_on else None,
        "start_time": fields.start_time,
        "end_time": fields.end_time if fields.start_time else None,
        "location": (fields.location or "").strip() or None,
        "notes": (fields.notes or "").strip() or None,
        "person_id": fields.person_id,
        "repeat": fields.repeat,
        "repeat_until": fields.repeat_until if fields.repeat != "never" else None,
    }


def get(conn: Any, event_id: int) -> Event | None:
    with conn.cursor() as cur:
        cur.execute(SELECT_ONE, {"id": event_id})
        row = cur.fetchone()
    return _event(row) if row else None


def events_between(conn: Any, start: date, end: date) -> list[Event]:
    with conn.cursor() as cur:
        cur.execute(SELECT_BETWEEN, {"start": start, "end": end})
        return [_event(row) for row in cur.fetchall()]


def between(conn: Any, start: date, end: date) -> list[Occurrence]:
    return expand(events_between(conn, start, end), start, end)


def create(conn: Any, fields: EventFields, *, created_via: str = "form") -> Event:
    with conn.cursor() as cur:
        cur.execute(INSERT, {**_params(fields), "created_via": created_via})
        row = cur.fetchone()
    created = get(conn, int(row[0]))
    assert created is not None
    return created


def update(conn: Any, event_id: int, fields: EventFields) -> Event | None:
    with conn.cursor() as cur:
        cur.execute(UPDATE, {**_params(fields), "id": event_id})
        if cur.rowcount == 0:
            return None
    return get(conn, event_id)


def delete(conn: Any, event_id: int) -> bool:
    with conn.cursor() as cur:
        cur.execute(DELETE, {"id": event_id})
        return bool(cur.rowcount)


def forget_seeded(conn: Any) -> int:
    with conn.cursor() as cur:
        cur.execute(DELETE_SEEDED)
        return int(cur.rowcount)


def deadlines(
    conn: Any, start: date, end: date, *, enabled: frozenset[str] | set[str] | None = None
) -> list[Deadline]:
    """Open obligations due inside [start, end]. `enabled` hides a switched-off pack's, as Today
    does; `None` is every pack."""
    with conn.cursor() as cur:
        cur.execute(DEADLINES, {"start": start, "end": end})
        rows = cur.fetchall()
    # One deadline per label and date: the same SRS cutoff written under two packs is one date.
    # Of two, the one with a page behind it is kept, so the calendar cites when it can.
    kept: dict[tuple[str, date], Deadline] = {}
    for row in rows:
        if enabled is not None and row[1] not in enabled:
            continue
        found = Deadline(*row)
        held = kept.get((found.label, found.due_date))
        if held is None or (held.document_id is None and found.document_id is not None):
            kept[(found.label, found.due_date)] = found
    return sorted(kept.values(), key=lambda d: (d.due_date, d.obligation_id))


# ------------------------------------------------------------------------------- the words


def clock(at: time) -> str:
    """9:00 am, 2:30 pm. How a household says a time."""
    hour = at.hour % 12 or 12
    return f"{hour}:{at.minute:02d} {'am' if at.hour < 12 else 'pm'}"


def when(occurrence: Occurrence) -> str:
    event = occurrence.event
    if event.days > 1:
        return f"all day (day {occurrence.day} of {event.days})"
    if event.start_time is None:
        return "all day"
    if event.end_time is None:
        return clock(event.start_time)
    return f"{clock(event.start_time)} to {clock(event.end_time)}"


def day_name(on: date) -> str:
    return f"{on:%A} {on.day} {on:%B}"


def describe(occurrence: Occurrence) -> str:
    """ "Saturday 17 October, 9:00 am to 10:00 am: Swimming lesson (Lucas Lim Kai En), at
    Tampines West CC." One line, every part of it from the row."""
    event = occurrence.event
    who = f" ({event.person})" if event.person else ""
    where = f", at {event.location}" if event.location else ""
    return f"{day_name(occurrence.on)}, {when(occurrence)}: {event.title}{who}{where}."


def _deadline_line(deadline: Deadline) -> Line:
    return Line(
        f"{day_name(deadline.due_date)}: {deadline.label} is due.",
        on=deadline.due_date,
        document_id=deadline.document_id,
        document_name=deadline.document_name,
        page=deadline.page,
    )


# ------------------------------------------------------------------------------- questions

# A question about the calendar names it, or asks what is on. Kept narrow on purpose: "plan" is
# in a whole life policy's product name, and "event" in an insurance schedule's insured events.
_ABOUT = re.compile(
    r"\b(calendar|schedule|diary|agenda|appointments?|what'?s on|what is on|anything on|"
    r"coming up|am i free|are we free|busy)\b",
    re.IGNORECASE,
)
_WHEN = re.compile(r"\b(when|what time|where|next|last)\b", re.IGNORECASE)
_WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
_STOP = frozenset(
    re.findall(
        r"\w+",
        "a an and are at be calendar day did do does for from has have i in is it last me my next "
        "of on our please s schedule that the this time to us was we what when where will",
    )
)


def period(question: str, today: date) -> tuple[date, date] | None:
    """The dates a question names, as whole calendar units (SDRR ADR 0018): "next week" from a
    Thursday is Monday to Sunday of the week after, not the next seven days."""
    q = question.lower()
    week_start = today - timedelta(days=today.weekday())
    if "today" in q or "tonight" in q:
        return today, today
    if "tomorrow" in q:
        return today + timedelta(days=1), today + timedelta(days=1)
    if "next week" in q:
        return week_start + timedelta(days=7), week_start + timedelta(days=13)
    if "weekend" in q:
        saturday = week_start + timedelta(days=5)
        return max(today, saturday), week_start + timedelta(days=6)
    if "this week" in q or "the week" in q:
        return today, week_start + timedelta(days=6)
    if "next month" in q:
        first = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
        return first, first.replace(day=months.monthrange(first.year, first.month)[1])
    if "this month" in q or "the month" in q:
        return today, today.replace(day=months.monthrange(today.year, today.month)[1])
    for index, name in enumerate(_WEEKDAYS):
        if re.search(rf"\b{name}\b", q):
            ahead = (index - today.weekday()) % 7
            if f"next {name}" in q and ahead == 0:
                ahead = 7
            return today + timedelta(days=ahead), today + timedelta(days=ahead)
    return None


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower().replace("'s", "")) if w not in _STOP}


def _matches(asked: set[str], event: Event) -> bool:
    """At least two thirds of the question's own words are in the event's title or its person's
    name, a word matching on a shared stem of four letters ("swim" and "swimming")."""
    own = _words(f"{event.title} {event.person or ''}")

    def hit(word: str) -> bool:
        return any(
            w == word
            or (min(len(w), len(word)) >= 4 and (w.startswith(word) or word.startswith(w)))
            for w in own
        )

    return bool(asked) and sum(hit(w) for w in asked) * 3 >= len(asked) * 2


def answer(
    conn: Any,
    question: str,
    today: date,
    *,
    enabled: frozenset[str] | set[str] | None = None,
) -> Reply | None:
    """A calendar answer written by code, or None when this is not a calendar question.

    Two shapes. "When is Lucas's next swimming lesson?" names an event: the next date from
    today, or the last before it if the question says last. "What's on this week?" names a
    period: every event and every deadline in it, a line each. Anything else is not ours.
    """
    asked = _words(question)
    if _WHEN.search(question):
        horizon = today + timedelta(days=366)
        events = [
            e
            for e in events_between(conn, today - timedelta(days=366), horizon)
            if _matches(asked, e)
        ]
        if events:
            past = re.search(r"\b(last|previous)\b", question, re.IGNORECASE) is not None
            if past:
                found = [
                    o
                    for o in expand(events, today - timedelta(days=366), today - timedelta(days=1))
                    if o.day == 1
                ]
                found = found[-1:]
            else:
                found = [o for o in expand(events, today, horizon) if o.day == 1][:1]
            if found:
                return Reply([Line(describe(found[0]), on=found[0].on)], found[0].on, found[0].on)
            return Reply(
                [
                    Line(
                        f"{events[0].title} has no date {'before' if past else 'after'} today "
                        "on the calendar."
                    )
                ]
            )

    if not _ABOUT.search(question):
        return None
    start, end = period(question, today) or (today, today + timedelta(days=6))
    lines = [Line(describe(o), on=o.on) for o in between(conn, start, end)]
    lines += [_deadline_line(d) for d in deadlines(conn, start, end, enabled=enabled)]
    lines.sort(key=lambda line: line.on or start)  # stable: events keep their time order
    if not lines:
        span = day_name(start) if start == end else f"{day_name(start)} to {day_name(end)}"
        lines = [Line(f"Nothing is on the calendar for {span}.", on=start)]
    return Reply(lines, start, end)


# ------------------------------------------------------------------------------- the digest


def digest(
    conn: Any, today: date, *, enabled: frozenset[str] | set[str] | None = None
) -> str | None:
    """The morning message: today, then the rest of the week. None when the week is empty.

    OpenJarvis's morning digest, cut to what this household's own rows can say: no news, no
    weather, nothing from outside the computer. It is sent at 07:10, after the Reminder and Alert
    sweeps, and it reads; it never marks a reminder as said, so it cannot use up a lead window.
    """
    end = today + timedelta(days=6)
    lines = [Line(describe(o), on=o.on) for o in between(conn, today, end)]
    lines += [_deadline_line(d) for d in deadlines(conn, today, end, enabled=enabled)]
    if not lines:
        return None
    lines.sort(key=lambda line: line.on or today)
    first = [line.text for line in lines if line.on == today]
    rest = [line.text for line in lines if line.on != today]
    parts = [f"Good morning. Today is {day_name(today)}."]
    name = day_name(today)
    first = [text.removeprefix(f"{name}, ").removeprefix(f"{name}: ") for text in first]
    parts += ["Today:", *(f"• {text}" for text in first)] if first else []
    parts += ["Later this week:", *(f"• {text}" for text in rest)] if rest else []
    parts.append("From your Parrot calendar and documents, on this computer.")
    return "\n".join(parts)
