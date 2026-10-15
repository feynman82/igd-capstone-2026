"""The calendar, as the answer graph meets it. ADR 0020.

Two things a question can ask of the calendar, and neither is a search.

**"What's on this week?"** is answered by `core.calendar.answer`, in code, before the graph runs
at all: the rows hold the exact answer, so no router, retrieval or model is spent on it.

**"Add Dad's polyclinic review on Friday at 10am"** asks Parrot to act, and v1 never acts — the
router would refuse it. So it is not done; it is *drafted*. The model reads the title, date,
time, person and place out of the sentence, a `Drafted` event carries them to the screen, and
nothing is written until a person presses Confirm there. That is OpenJarvis's approval queue
reduced to the one tier this product has: always ask. The model is handed a table of the next
fourteen dates, so "Friday" and "next Tuesday" are a lookup for it rather than arithmetic, and
the person checks the date on the card before anything is saved.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from datetime import date, time, timedelta
from typing import Any

from core import calendar
from core.household import roster
from core.registry import enabled_pack_ids
from core.runtime.ollama import ModelUnavailable, Ollama

# "Add …", "put … in the calendar", "remind me to …". Not "add up my premiums", which is a sum.
_ENTRY = re.compile(
    r"^\s*(please\s+)?((can|could|would) you\s+)?"
    r"(add(?!\s+up)|put|pencil|schedule|block|note down|remind (me|us))\b"
    r"|\b(add|put)\b.*\b(to|on|in|into)\s+(the|my|our)\s+(calendar|diary|schedule)\b",
    re.IGNORECASE,
)
_CLOCK = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")

NOTE = (
    "Nothing is saved until you confirm. This adds it to your household calendar on this "
    "computer; it does not book or tell anybody."
)

DRAFT_SYSTEM = """You read one request to add an entry to a household calendar and return its \
parts as JSON. Copy, never invent.

- title: what the entry is, in a few words, without the date, the time or the person's name \
("Polyclinic review", "Swimming lesson"). Never empty.
- date: YYYY-MM-DD. Read a day name or a relative day off the table of dates you are given; \
use today's date when none is said.
- start and end: 24-hour HH:MM, or "" when the request gives no time. "3pm" is "15:00".
- person: one name from the household list exactly as written there, or "" when the entry is \
for the whole household or the request names nobody in the list. Each name says how that \
person is related to the one asking: "Dad", "Mum" or "my father" is one of their parents, "my \
son" or "my daughter" their child, "my wife" or "my husband" their partner. The person asking \
is only the answer when they say "me" or "I", or name nobody else.
- location: the place if one is said, else ""."""

# How each relation in the roster is put to the model, from the asker's side.
_RELATION = {
    "self": "the person asking",
    "partner": "their partner",
    "child": "their child",
    "parent": "their parent",
    "other": "lives with them",
}

_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "date": {"type": "string"},
        "start": {"type": "string"},
        "end": {"type": "string"},
        "person": {"type": "string"},
        "location": {"type": "string"},
    },
    "required": ["title", "date", "start", "end", "person", "location"],
}


@dataclass(frozen=True, slots=True)
class Drafted:
    """A calendar entry Parrot wrote down and has not saved. Terminal: it ends the answer.

    Everything here is a proposal for the form the person confirms; `person_id` is one of the
    household's own ids or None, never a name the model made up.
    """

    title: str
    starts_on: date
    start_time: time | None
    end_time: time | None
    person_id: int | None
    person: str | None
    location: str
    note: str = NOTE


def wants_entry(question: str) -> bool:
    return _ENTRY.search(question) is not None


def _dates(today: date) -> str:
    return "\n".join(
        f"{'today' if n == 0 else 'tomorrow' if n == 1 else ''} {d:%A} = {d.isoformat()}".strip()
        for n, d in ((n, today + timedelta(days=n)) for n in range(14))
    )


def _clock(text: str) -> time | None:
    found = _CLOCK.match(text.strip())
    return time(int(found.group(1)), int(found.group(2))) if found else None


def _iso(text: str, today: date) -> date:
    try:
        return date.fromisoformat(text.strip())
    except ValueError:
        return today


# "10am", "3.30pm", "15:00", with the "at" before it, so it can be lifted out of a title.
_SAID_TIME = re.compile(
    r"\s*\b(?:at\s+)?(?:(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm)|([01]?\d|2[0-3]):([0-5]\d))\b",
    re.IGNORECASE,
)
_SAID_DAY = re.compile(
    r"\s*\b(?:on\s+|this\s+|next\s+)*"
    r"(?:today|tonight|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    re.IGNORECASE,
)


def _said_time(question: str) -> time | None:
    found = _SAID_TIME.search(question)
    if found is None:
        return None
    if found.group(4):
        return time(int(found.group(4)), int(found.group(5)))
    hour, minute = int(found.group(1)), int(found.group(2) or 0)
    if not 1 <= hour <= 12 or minute > 59:
        return None
    return time(hour % 12 + (12 if found.group(3).lower() == "pm" else 0), minute)


def _without_model(question: str, today: date) -> Drafted:
    """The request read by code alone: the day and time it names, and what is left as the title.

    For when the model is down. Coarser than the model — no person, no place — but the card still
    has the right day on it, which is the field a person is least likely to notice is wrong.
    """
    day = calendar.period(question, today)
    title = re.sub(_ENTRY, "", question, count=1)
    title = _SAID_DAY.sub("", _SAID_TIME.sub("", title)).strip(" .?!,")
    return Drafted(
        title=(title or question).strip()[:200],
        starts_on=day[0] if day and day[0] == day[1] else today,
        start_time=_said_time(question),
        end_time=None,
        person_id=None,
        person=None,
        location="",
    )


def draft(
    client: Ollama, question: str, today: date, people: list[tuple[int, str, str]]
) -> Drafted:
    """The request, as a draft entry. A model that is down still leaves a card to fill in.

    `people` is (id, name, relation to the owner). The relation goes to the model beside each
    name, because "Dad" is only resolvable by knowing who is whose parent; the name it returns is
    then matched back to an id here, so it can never hand back somebody who is not in the list.
    """
    names = (
        "\n".join(
            f"- {name} ({_RELATION.get(relation, 'lives with them')})"
            for _, name, relation in people
        )
        or "- (nobody set up yet)"
    )
    prompt = (
        f"Today is {today:%A} {today.isoformat()}.\nDates:\n{_dates(today)}\n\n"
        f"Household:\n{names}\n\nRequest: {question}"
    )
    # What code can read exactly, it reads, and the model is not asked to agree: a day name, a
    # clock time, a name the person typed. The model keeps what only it can do — the title, the
    # place, and "Mum" or "Dad", which takes knowing who is whose parent.
    by_code = _without_model(question, today)
    typed = _person_in(question, people)
    try:
        reply = client.constrained(DRAFT_SYSTEM, prompt, _SCHEMA).json()
    except ModelUnavailable:
        return replace(by_code, person_id=typed[0], person=typed[1]) if typed else by_code
    said = str(reply.get("person", "")).split("(")[0]  # "(their parent)", if it was copied
    kin = _relation_in(question)
    who: tuple[int, str] | None
    if typed is not None:
        who = typed
    elif kin is not None:
        # "Mum" with two parents on the roster is not a choice to hand a model: the roster does
        # not say which is which, and a confident wrong name is worse than none (ADR 0015).
        related = [(p, name) for p, name, relation in people if relation == kin]
        who = related[0] if len(related) == 1 else None
    else:
        who = _person_in(said, people)
    pid, person = who if who else (None, None)
    named_day = calendar.period(question, today)
    start = by_code.start_time or _clock(str(reply.get("start", "")))
    end = _clock(str(reply.get("end", ""))) if start else None
    return Drafted(
        title=str(reply.get("title", "")).strip()[:200] or by_code.title,
        starts_on=by_code.starts_on
        if named_day and named_day[0] == named_day[1]
        else _iso(str(reply.get("date", "")), today),
        start_time=start,
        end_time=end if end and start and end > start else None,
        person_id=pid,
        person=person,
        location=str(reply.get("location", "")).strip()[:200],
    )


_KIN = {
    "parent": "mum mom mummy mother mama ma dad daddy father papa pa",
    "child": "son daughter kid boy girl",
    "partner": "wife husband hubby spouse partner",
}


def _relation_in(text: str) -> str | None:
    """The relation a request names from the asker's side: "Mum" is a parent, "my son" a child."""
    asked = set(re.findall(r"[a-z]+", text.lower().replace("'s", "")))
    return next((relation for relation, words in _KIN.items() if asked & set(words.split())), None)


def _person_in(text: str, people: list[tuple[int, str, str]]) -> tuple[int, str] | None:
    """The one household member `text` names, by a word of their name only they have.

    "Lucas's dental check-up" is Lucas; "Ah Kow" is Lim Ah Kow by "kow". "Lim" names three
    people and so names nobody, and a word shorter than three letters is never a name here.
    """
    owners: dict[str, set[int]] = {}
    for pid, name, _ in people:
        for word in re.findall(r"[a-z]+", name.lower()):
            if len(word) >= 3:
                owners.setdefault(word, set()).add(pid)
    asked = set(re.findall(r"[a-z]+", text.lower().replace("'s", "")))
    found = {next(iter(ids)) for word, ids in owners.items() if word in asked and len(ids) == 1}
    if len(found) != 1:
        return None
    pid = found.pop()
    return pid, next(name for p, name, _ in people if p == pid)


class HouseholdCalendar:
    """The graph's view of the calendar. Holds the connection the graph does not."""

    def __init__(self, conn: Any) -> None:
        self._conn = conn

    def answer(self, question: str, today: date) -> calendar.Reply | None:
        return calendar.answer(self._conn, question, today, enabled=enabled_pack_ids(self._conn))

    def people(self) -> list[tuple[int, str, str]]:
        return [(p.id, p.display_name, p.relation) for p in roster(self._conn) if not p.external]
