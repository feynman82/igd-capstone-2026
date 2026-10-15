"""The household calendar (ADR 0020): repeats, questions answered by code, drafts, and the API.

The pure parts run anywhere. The rest runs the real SQL against Postgres, inside temporary
copies of the tables it touches, so a test never sees — or leaves — a row in the live household.

What these protect, in order of how much it would hurt to lose:

- **Nothing is written without a person.** A request to add an entry ends in a draft; the only
  path into `calendar_events` is the API a person's Confirm calls.
- **A deadline is cited to its page** and an event to the calendar on its date.
- **A series is one row.** Expanding it never invents a 31 April, and an edit or a delete is to
  every date of it.
- **"What's on" never reaches the model.** Its answer is in the rows.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import date, time
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from api import routes
from api.main import create_app
from core import calendar
from core.calendar import Event, EventFields
from core.graph.answer import AnswerGraph, Drafted, Finished, Reading, Sentence
from core.graph.calendar import HouseholdCalendar, draft, wants_entry
from core.runtime.ollama import ModelUnavailable
from core.runtime.settings import Settings
from tests.test_answer_graph import FixedRetriever, PassThroughReranker, ScriptedOllama

ROOT = Path(__file__).resolve().parents[1]
TODAY = date(2026, 10, 15)  # a Thursday
NOTICE = UUID("33333333-3333-3333-3333-333333333333")
TEMPORARY = ("documents", "facts", "obligations", "people", "packs", "calendar_events")


def event(
    title: str = "Swimming lesson",
    starts_on: date = date(2026, 10, 17),
    *,
    repeat: calendar.Repeat = "never",
    until: date | None = None,
    ends_on: date | None = None,
    person: str | None = None,
) -> Event:
    return Event(
        1,
        title,
        starts_on,
        ends_on,
        None,
        None,
        None,
        None,
        None,
        person,
        repeat,
        until,
        "form",
        "local",
    )


# ----------------------------------------------------------------------------- repeats


def test_a_weekly_series_lands_on_the_same_weekday_inside_the_range() -> None:
    swim = event(repeat="weekly")
    days = calendar.first_days(swim, date(2026, 11, 1), date(2026, 11, 30))
    assert days == [date(2026, 11, 7), date(2026, 11, 14), date(2026, 11, 21), date(2026, 11, 28)]


def test_a_series_stops_on_its_last_day() -> None:
    swim = event(repeat="weekly", until=date(2026, 10, 31))
    assert calendar.first_days(swim, date(2026, 10, 1), date(2026, 11, 30)) == [
        date(2026, 10, 17),
        date(2026, 10, 24),
        date(2026, 10, 31),
    ]


def test_a_monthly_series_on_the_31st_skips_the_months_without_one() -> None:
    bill = event("Credit card bill", date(2026, 1, 31), repeat="monthly")
    days = calendar.first_days(bill, date(2026, 1, 1), date(2026, 7, 31))
    assert days == [date(2026, 1, 31), date(2026, 3, 31), date(2026, 5, 31), date(2026, 7, 31)]


def test_a_birthday_on_29_february_waits_for_a_leap_year() -> None:
    leap = event("Birthday", date(2024, 2, 29), repeat="yearly")
    assert calendar.first_days(leap, date(2025, 1, 1), date(2028, 12, 31)) == [date(2028, 2, 29)]


def test_a_trip_that_began_before_the_range_still_shows_its_remaining_days() -> None:
    trip = event("Penang", date(2026, 10, 30), ends_on=date(2026, 11, 2))
    shown = calendar.expand([trip], date(2026, 11, 1), date(2026, 11, 30))
    assert [(o.on, o.day) for o in shown] == [(date(2026, 11, 1), 3), (date(2026, 11, 2), 4)]
    assert calendar.when(shown[0]) == "all day (day 3 of 4)"


# ----------------------------------------------------------------------------- periods


@pytest.mark.parametrize(
    ("question", "start", "end"),
    [
        ("what's on today", TODAY, TODAY),
        ("anything on tomorrow?", date(2026, 10, 16), date(2026, 10, 16)),
        ("what's on this week", TODAY, date(2026, 10, 18)),
        ("what's on next week", date(2026, 10, 19), date(2026, 10, 25)),
        ("are we free this weekend", date(2026, 10, 17), date(2026, 10, 18)),
        ("what's on on Friday", date(2026, 10, 16), date(2026, 10, 16)),
        ("what's on next Thursday", date(2026, 10, 22), date(2026, 10, 22)),
        ("what is on next month", date(2026, 11, 1), date(2026, 11, 30)),
    ],
)
def test_a_period_is_whole_calendar_units(question: str, start: date, end: date) -> None:
    assert calendar.period(question, TODAY) == (start, end)


def test_an_insurance_question_is_not_a_calendar_question() -> None:
    assert not wants_entry("add up all my insurance premiums")
    assert not wants_entry("when does my car insurance expire?")
    assert wants_entry("Add Dad's polyclinic review on Friday at 10am")
    assert wants_entry("please put Lucas's dental check-up in the calendar for next Tuesday")
    assert wants_entry("remind me to renew the road tax on 1 November")


# ----------------------------------------------------------------------------- drafts


PEOPLE = [(1, "Marcus Lim", "self"), (2, "Lim Ah Kow", "parent"), (3, "Lucas Lim Kai En", "child")]


def test_a_draft_takes_the_household_id_and_never_a_made_up_name() -> None:
    client = ScriptedOllama(
        {
            "title": "Polyclinic review",
            "date": "2026-10-16",
            "start": "10:00",
            "end": "",
            "person": "lim ah kow",
            "location": "Tampines Polyclinic",
        }
    )
    drafted = draft(client, "add Dad's polyclinic review on Friday at 10am", TODAY, PEOPLE)  # type: ignore[arg-type]
    assert drafted == Drafted(
        "Polyclinic review",
        date(2026, 10, 16),
        time(10),
        None,
        2,
        "Lim Ah Kow",
        "Tampines Polyclinic",
    )
    # The model is handed a table of dates, so "Friday" is a lookup and not arithmetic, and each
    # name with how they are related to the asker, so "Dad" is resolvable at all.
    assert "Friday = 2026-10-16" in client.prompts[0]
    assert "- Lim Ah Kow (their parent)" in client.prompts[0]

    stranger = ScriptedOllama(
        {
            "title": "Tea",
            "date": "next week",
            "start": "25:00",
            "end": "",
            "person": "Uncle Bob",
            "location": "",
        }
    )
    drafted = draft(stranger, "add tea with Uncle Bob", TODAY, PEOPLE)  # type: ignore[arg-type]
    assert (drafted.person_id, drafted.person, drafted.starts_on, drafted.start_time) == (
        None,
        None,
        TODAY,  # an unreadable date is today, for the person to correct on the card
        None,
    )


def test_what_code_can_read_exactly_it_reads_and_the_model_does_not_overrule() -> None:
    """15 October 2026: the 4B model put "next Tuesday" on the 27th, "Mum" on Ah Kow, and missed
    "Lucas's". A day name, a clock time and a typed name are code's; the model keeps the title,
    the place, the end time and relation words."""
    client = ScriptedOllama(
        {
            "title": "Dental check-up",
            "date": "2026-10-27",
            "start": "16:00",
            "end": "15:30",
            "person": "Lucas",
            "location": "Tampines Polyclinic",
        }
    )
    drafted = draft(client, "add Lucas's dental check-up tomorrow 3pm to 3.30pm", TODAY, PEOPLE)  # type: ignore[arg-type]
    assert (drafted.starts_on, drafted.start_time, drafted.end_time) == (
        date(2026, 10, 16),
        time(15),
        time(15, 30),
    )
    assert (drafted.person_id, drafted.person) == (3, "Lucas Lim Kai En")
    # A surname three people share names nobody.
    assert (
        draft(
            ScriptedOllama(ModelUnavailable("down")), "add Lim family dinner", TODAY, PEOPLE
        ).person_id
        is None
    )  # type: ignore[arg-type]


def test_mum_with_two_parents_is_left_for_the_person_to_choose() -> None:
    """The roster says Ah Kow and Mei Ling are both parents and not which is which. The model put
    "Mum's bone density scan" on Ah Kow; with two parents, nobody is chosen for the person."""
    family = [*PEOPLE, (4, "Tan Mei Ling", "parent"), (5, "Rachel Ng Hui Shan", "partner")]
    reply = {
        "title": "Bone density scan",
        "date": "",
        "start": "",
        "end": "",
        "person": "Lim Ah Kow",
        "location": "",
    }
    mum = draft(ScriptedOllama(reply), "put Mum's bone density scan in", TODAY, family)  # type: ignore[arg-type]
    assert (mum.person_id, mum.person) == (None, None)
    # One partner on the roster: "my wife" is exactly one person, whatever the model said.
    wife = draft(
        ScriptedOllama({**reply, "person": ""}), "add my wife's team dinner", TODAY, family
    )  # type: ignore[arg-type]
    assert (wife.person_id, wife.person) == (5, "Rachel Ng Hui Shan")


def test_a_draft_survives_the_model_being_down() -> None:
    client = ScriptedOllama(ModelUnavailable("Ollama is not running"))
    drafted = draft(client, "Add swimming for Lucas on Saturday at 9.30am", TODAY, PEOPLE)  # type: ignore[arg-type]
    # Code still reads the day and the time, and lifts them out of the title.
    assert (drafted.title, drafted.starts_on, drafted.start_time) == (
        "swimming for Lucas",
        date(2026, 10, 17),
        time(9, 30),
    )


# --------------------------------------------------------------------- against Postgres


@pytest.fixture
def db() -> Iterator[Any]:
    psycopg = pytest.importorskip("psycopg")
    try:
        url = Settings.load(ROOT).database_url
        conn = psycopg.connect(url, autocommit=False, connect_timeout=3)
    except psycopg.OperationalError as error:
        pytest.skip(f"no local database: {type(error).__name__}")
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass('public.calendar_events')")
            row = cur.fetchone()
            if row is None or row[0] is None:
                pytest.skip("the 0004_calendar migration has not been applied")
            # Empty copies, searched before public: the queries under test are unqualified.
            for table in TEMPORARY:
                cur.execute(f"CREATE TEMP TABLE {table} (LIKE public.{table} INCLUDING ALL)")
            cur.execute(
                "INSERT INTO people (id, display_name, relation, is_owner) VALUES "
                "(1, 'Marcus Lim', 'self', true), (2, 'Lim Ah Kow', 'parent', false), "
                "(3, 'Lucas Lim Kai En', 'child', false)"
            )
            cur.execute(
                "INSERT INTO documents (id, sha256, source_channel, original_name, mime) "
                "VALUES (%s, '\\x00', 'folder', 'b1-0028.pdf', 'application/pdf')",
                (NOTICE,),
            )
            cur.execute(
                "INSERT INTO facts (id, document_id, page, pack_id, pack_version, key, value_date, "
                "confidence) VALUES (9, %s, 1, 'core', '1', 'payment_due_date', '2026-10-15', 1)",
                (NOTICE,),
            )
            cur.execute(
                "INSERT INTO obligations (fact_id, pack_id, label, due_date, lead_days) "
                "VALUES (9, 'core', 'Income tax payment', '2026-10-15', '{30,7}')"
            )
        yield conn
    finally:
        conn.rollback()
        conn.close()


def _seed(conn: Any) -> Event:
    calendar.create(
        conn,
        EventFields(
            "Swimming lesson",
            date(2026, 10, 3),
            start_time=time(9),
            end_time=time(10),
            location="Tampines West CC",
            person_id=3,
            repeat="weekly",
        ),
    )
    return calendar.create(
        conn, EventFields("Polyclinic review", date(2026, 10, 16), start_time=time(10), person_id=2)
    )


def test_what_is_on_this_week_is_every_event_and_deadline_each_cited(db: Any) -> None:
    _seed(db)
    reply = calendar.answer(db, "What's on this week?", TODAY)
    assert reply is not None
    assert [line.text for line in reply.lines] == [
        "Thursday 15 October: Income tax payment is due.",
        "Friday 16 October, 10:00 am: Polyclinic review (Lim Ah Kow).",
        "Saturday 17 October, 9:00 am to 10:00 am: Swimming lesson (Lucas Lim Kai En), "
        "at Tampines West CC.",
    ]
    tax, review, _ = reply.lines
    assert (tax.document_name, tax.page) == ("b1-0028.pdf", 1)  # a deadline cites its page
    assert (review.document_name, review.on) == (None, date(2026, 10, 16))  # an event, its day


def test_when_is_the_next_one_finds_the_series_by_its_words(db: Any) -> None:
    _seed(db)
    reply = calendar.answer(db, "When is Lucas's next swim?", TODAY)
    assert reply is not None
    assert reply.lines[0].text.startswith("Saturday 17 October, 9:00 am to 10:00 am: Swimming")
    last = calendar.answer(db, "when was the last swimming lesson", TODAY)
    assert last is not None and last.lines[0].on == date(2026, 10, 10)


def test_a_document_question_is_left_to_the_graph(db: Any) -> None:
    _seed(db)
    assert calendar.answer(db, "When does my car insurance expire?", TODAY) is None
    assert calendar.answer(db, "What is the excess on my policy?", TODAY) is None


def test_an_empty_period_says_so_rather_than_saying_nothing(db: Any) -> None:
    reply = calendar.answer(db, "anything on next month?", TODAY)
    assert reply is not None
    assert [line.text for line in reply.lines] == [
        "Nothing is on the calendar for Sunday 1 November to Monday 30 November."
    ]


def test_the_graph_answers_the_calendar_without_asking_the_model(db: Any) -> None:
    _seed(db)
    client = ScriptedOllama()  # any model call would pop an empty list and fail
    graph = AnswerGraph(
        client,  # type: ignore[arg-type]
        FixedRetriever([]),
        PassThroughReranker(),
        today=TODAY,
        calendar=HouseholdCalendar(db),
    )
    events = list(graph.stream("what's on tomorrow?"))
    assert isinstance(events[0], Reading) and isinstance(events[-1], Finished)
    (sentence,) = [e for e in events if isinstance(e, Sentence)]
    assert sentence.text == "Friday 16 October, 10:00 am: Polyclinic review (Lim Ah Kow)."
    (cited,) = sentence.citations
    assert (cited.kind, cited.text, cited.url) == (
        "calendar",
        "Calendar, Fri 16 Oct",
        "/calendar?d=2026-10-16",
    )
    assert client.prompts == []


def test_asking_to_add_an_entry_drafts_it_and_writes_nothing(db: Any) -> None:
    client = ScriptedOllama(
        {
            "title": "Dental check-up",
            "date": "2026-10-20",
            "start": "15:00",
            "end": "15:30",
            "person": "Lucas Lim Kai En",
            "location": "",
        }
    )
    graph = AnswerGraph(
        client,  # type: ignore[arg-type]
        FixedRetriever([]),
        PassThroughReranker(),
        today=TODAY,
        calendar=HouseholdCalendar(db),
    )
    answer = graph.ask("Add Lucas's dental check-up next Tuesday 3pm to 3.30pm")
    assert answer.draft is not None and not answer.grounded
    assert (answer.draft.title, answer.draft.person_id, answer.draft.end_time) == (
        "Dental check-up",
        3,
        time(15, 30),
    )
    with db.cursor() as cur:
        cur.execute("SELECT count(*) FROM calendar_events")
        assert cur.fetchone() == (0,)


# --------------------------------------------------------------------------- the API


@pytest.fixture
def api(db: Any) -> TestClient:
    """Loopback, as `TrustedHostMiddleware` requires, and without the lifespan, which
    `tests/test_api.py` covers. Every request is handed the temporary tables' connection."""
    app = create_app(Settings.load(ROOT))

    def temporary() -> Iterator[Any]:
        yield db

    app.dependency_overrides[routes.connection] = temporary
    return TestClient(app, base_url="http://127.0.0.1")


def test_a_person_creates_edits_and_deletes_an_entry(api: TestClient) -> None:
    created = api.post(
        "/api/calendar/events",
        json={
            "title": "Family dinner",
            "starts_on": "2026-10-18",
            "start_time": "18:30",
            "location": "Mum's",
            "repeat": "weekly",
            "repeat_until": "2026-11-08",
        },
    )
    assert created.status_code == 201, created.text
    entry = created.json()
    assert (entry["created_via"], entry["source"], entry["person"]) == ("form", "local", None)

    month = api.get("/api/calendar", params={"start": "2026-10-01", "end": "2026-11-30"}).json()
    dinners = [e["on"] for e in month["entries"] if e["title"] == "Family dinner"]
    assert dinners == ["2026-10-18", "2026-10-25", "2026-11-01", "2026-11-08"]
    tax = next(e for e in month["entries"] if e["kind"] == "deadline")
    assert tax["sources"][0]["text"] == "b1-0028.pdf, page 1" and tax["event_id"] is None

    moved = api.put(
        f"/api/calendar/events/{entry['id']}",
        json={
            **entry,
            "starts_on": "2026-10-17",
            "person_id": 1,
            "repeat": "never",
            "repeat_until": None,
        },
    )
    assert moved.status_code == 200, moved.text
    assert (moved.json()["starts_on"], moved.json()["person"]) == ("2026-10-17", "Marcus Lim")

    gone = api.delete(f"/api/calendar/events/{entry['id']}")
    assert gone.json() == {"id": entry["id"], "title": "Family dinner"}
    assert api.delete(f"/api/calendar/events/{entry['id']}").status_code == 404


def test_the_api_refuses_what_a_calendar_cannot_hold(api: TestClient) -> None:
    bad = [
        {"title": " ", "starts_on": "2026-10-18"},
        {"title": "Trip", "starts_on": "2026-10-18", "ends_on": "2026-10-17"},
        {"title": "Call", "starts_on": "2026-10-18", "end_time": "10:00"},
        {"title": "Call", "starts_on": "2026-10-18", "start_time": "11:00", "end_time": "10:00"},
    ]
    for body in bad:
        assert api.post("/api/calendar/events", json=body).status_code == 422, body
    stranger = {"title": "Tea", "starts_on": "2026-10-18", "person_id": 999}
    assert api.post("/api/calendar/events", json=stranger).status_code == 422
    wide = api.get("/api/calendar", params={"start": "2026-01-01", "end": "2026-12-31"})
    assert wide.status_code == 400
    missing = api.put("/api/calendar/events/424242", json={"title": "x", "starts_on": "2026-10-18"})
    assert missing.status_code == 404


def test_a_confirmed_draft_is_recorded_as_one(api: TestClient) -> None:
    body = {
        "title": "Polyclinic review",
        "starts_on": "2026-10-16",
        "person_id": 2,
        "created_via": "ask",
    }
    assert api.post("/api/calendar/events", json=body).json()["created_via"] == "ask"
    seeded = {**body, "created_via": "seed"}  # seeding is a script's, never a screen's
    assert api.post("/api/calendar/events", json=seeded).status_code == 422


# --------------------------------------------------------------------------- the digest


def test_the_morning_digest_says_today_first_then_the_week(db: Any) -> None:
    _seed(db)
    text = calendar.digest(db, TODAY)
    assert text == (
        "Good morning. Today is Thursday 15 October.\n"
        "Today:\n"
        "• Income tax payment is due.\n"
        "Later this week:\n"
        "• Friday 16 October, 10:00 am: Polyclinic review (Lim Ah Kow).\n"
        "• Saturday 17 October, 9:00 am to 10:00 am: Swimming lesson (Lucas Lim Kai En), "
        "at Tampines West CC.\n"
        "From your Parrot calendar and documents, on this computer."
    )
    assert calendar.digest(db, date(2027, 6, 1)) is not None  # the swim is weekly, forever
    with db.cursor() as cur:
        cur.execute("DELETE FROM calendar_events")
        cur.execute("DELETE FROM obligations")
    assert calendar.digest(db, TODAY) is None  # an empty week sends nothing


def test_the_digest_speaks_only_to_the_allow_list() -> None:
    import httpx

    from core.adapters import telegram

    asked: list[int] = []

    def bot(request: httpx.Request) -> httpx.Response:
        import json

        asked.append(json.loads(request.content)["chat_id"])
        return httpx.Response(200, json={"ok": True, "result": {}})

    transport = httpx.MockTransport(bot)
    allowed = telegram.TelegramSettings("token", frozenset({11, 22}))
    assert telegram.send(allowed, "hello", transport=transport) == 2
    assert sorted(asked) == [11, 22]
    nobody = telegram.TelegramSettings("token", frozenset())
    assert telegram.send(nobody, "hello", transport=transport) == 0  # closed when empty
    assert sorted(asked) == [11, 22]
