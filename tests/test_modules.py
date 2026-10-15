"""Reminder and Alert: what fires, once, and with what behind it.

Both modules are pure functions over rows, so most of this is tested with a fake cursor rather
than a database. That is deliberate — the behaviour worth protecting is "nothing fires twice" and
"nothing fires uncited", and neither of those is a property of Postgres.

Whose number a metric is, and for which year, *is* a property of the SQL, and a fake cursor
returns whatever it is given. So the scoping of the Alert metrics is tested against Postgres too,
with the batch1 register loaded as facts inside a transaction that is rolled back.
"""

from __future__ import annotations

import csv
import hashlib
from collections.abc import Iterator
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from core.contracts import FACT_COLUMN, AlertConfig
from core.ingest.sql import INSERT_FACT
from core.packs import CORE, catalog
from core.runtime.settings import Settings
from modules import alert, reminder
from modules.reminder import already_said, current_lead

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "corpus" / "register" / "batch1.csv"

TODAY = date(2026, 9, 11)
RENEWAL = date(2026, 11, 30)  # 80 days out
LEADS = [60, 30, 7]


class FakeCursor:
    def __init__(self, results: list[list[tuple[Any, ...]]]) -> None:
        self._results = results
        self._current: list[tuple[Any, ...]] = []
        self.executed: list[tuple[str, dict[str, Any]]] = []

    def execute(self, query: str, params: Any = None) -> None:
        self.executed.append((query, params or {}))
        self._current = self._results.pop(0) if self._results else []

    def fetchall(self) -> list[tuple[Any, ...]]:
        return self._current

    def fetchone(self) -> tuple[Any, ...] | None:
        return self._current[0] if self._current else None

    def __enter__(self) -> FakeCursor:
        return self

    def __exit__(self, *exc: object) -> None:
        return None


class FakeConn:
    def __init__(self, *results: list[tuple[Any, ...]]) -> None:
        self.cursor_obj = FakeCursor(list(results))
        self.commits = 0

    def cursor(self) -> FakeCursor:
        return self.cursor_obj

    def commit(self) -> None:
        self.commits += 1


def obligation_row(
    due: date = RENEWAL,
    last_notified: datetime | None = None,
    leads: list[int] | None = None,
) -> tuple[Any, ...]:
    return (
        1,
        "insurance_agent",
        "policy expiry — Marcus Fernandez",
        due,
        leads if leads is not None else LEADS,
        "pending",
        last_notified,
        "doc-uuid",
        1,
        "renewal-notice.pdf",
    )


# ------------------------------------------------------------------------ the lead windows


@pytest.mark.parametrize(
    ("days_left", "expected"),
    [(80, None), (60, 60), (45, 60), (30, 30), (8, 30), (7, 7), (0, 7)],
)
def test_the_tightest_entered_window_is_the_current_one(
    days_left: int, expected: int | None
) -> None:
    assert current_lead(days_left, LEADS) == expected


def test_a_window_already_mentioned_is_not_mentioned_again() -> None:
    # The 30-day window opened on 31 October; a notification that day has served it.
    assert already_said(datetime(2026, 10, 31, 7, 0), RENEWAL, 30) is True
    assert already_said(datetime(2026, 11, 20, 7, 0), RENEWAL, 30) is True


def test_an_earlier_window_does_not_serve_a_later_one() -> None:
    # Notified on 2 October, inside the 60-day window. The 30-day window is still unserved.
    assert already_said(datetime(2026, 10, 2, 7, 0), RENEWAL, 30) is False


def test_never_notified_is_never_said() -> None:
    assert already_said(None, RENEWAL, 60) is False


# ---------------------------------------------------------------------------- the sweep


def test_an_obligation_outside_every_window_is_not_surfaced() -> None:
    conn = FakeConn([obligation_row()])  # 80 days out, widest lead is 60
    assert reminder.sweep(conn, TODAY) == []


def test_an_obligation_inside_a_window_is_surfaced_with_its_document() -> None:
    conn = FakeConn([obligation_row(due=TODAY + timedelta(days=21))], [])
    due = reminder.sweep(conn, TODAY)

    assert len(due) == 1
    assert due[0].days_left == 21
    assert due[0].lead == 30
    assert "renewal-notice.pdf" in due[0].line()
    assert conn.commits == 1, "the sweep records that it was said"


def test_nothing_fires_twice_in_the_same_window() -> None:
    due_date = TODAY + timedelta(days=21)
    said_yesterday = datetime(2026, 9, 10, 7, 0)
    conn = FakeConn([obligation_row(due=due_date, last_notified=said_yesterday)])

    assert reminder.sweep(conn, TODAY) == []
    assert conn.commits == 0


def test_a_dry_run_records_nothing() -> None:
    conn = FakeConn([obligation_row(due=TODAY + timedelta(days=3))])
    due = reminder.sweep(conn, TODAY, mark=False)

    assert len(due) == 1
    assert conn.commits == 0, "a dry run must leave it to be said again"


def test_the_sweep_is_stamped_with_the_day_it_was_run_for() -> None:
    """A sweep for a date in the future must record that date, or it repeats itself."""
    as_of = date(2026, 11, 20)
    conn = FakeConn([obligation_row(due=RENEWAL)], [])
    reminder.sweep(conn, as_of)

    marks = [p for q, p in conn.cursor_obj.executed if q.lstrip().startswith("UPDATE")]
    assert marks and marks[0]["now"].date() == as_of


def test_the_most_urgent_comes_first() -> None:
    rows = [
        obligation_row(due=TODAY + timedelta(days=25)),
        obligation_row(due=TODAY + timedelta(days=3)),
    ]
    conn = FakeConn(rows, [])
    due = reminder.sweep(conn, TODAY)

    assert [item.days_left for item in due] == [3, 25]


# ---------------------------------------------------------------------------- the alert


SRS = AlertConfig(metric="srs_contributions_ytd", ceiling=15300, warn_at=0.9)


def srs_row(value: str) -> tuple[Any, ...]:
    """One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order."""
    return ("Marcus Fernandez", Decimal(value), "srs-2026.pdf", 2)


def test_a_threshold_crossing_fires_with_the_document_behind_it() -> None:
    conn = FakeConn([srs_row("14000.00")], [], [])
    firing = alert.sweep(conn, TODAY, configs=(SRS,))  # type: ignore[arg-type]

    assert len(firing) == 1
    assert firing[0].citations == ["srs-2026.pdf, page 2"]
    assert "92%" in firing[0].line(), "14000 of 15300 is 91.5%, which rounds to 92"
    assert conn.commits == 1


def test_below_the_warning_share_nothing_fires() -> None:
    conn = FakeConn([srs_row("5000.00")])
    assert alert.sweep(conn, TODAY, configs=(SRS,)) == []  # type: ignore[arg-type]


def test_a_recent_firing_is_debounced() -> None:
    just_fired = [(datetime.now(UTC) - timedelta(hours=2), {"value": "14000.00"})]
    conn = FakeConn([srs_row("14000.00")], just_fired)

    assert alert.sweep(conn, TODAY, configs=(SRS,)) == []  # type: ignore[arg-type]
    assert conn.commits == 0


def test_a_firing_older_than_the_debounce_window_fires_again() -> None:
    long_ago = [(datetime.now(UTC) - timedelta(days=30), {"value": "9000.00"})]
    conn = FakeConn([srs_row("14000.00")], long_ago, [])

    firing = alert.sweep(conn, TODAY, configs=(SRS,))  # type: ignore[arg-type]
    assert len(firing) == 1


def test_a_metric_no_query_defines_cannot_fire() -> None:
    invented = AlertConfig(metric="made_up_metric", ceiling=10, warn_at=0.5)
    conn = FakeConn()

    assert alert.sweep(conn, TODAY, configs=(invented,)) == []  # type: ignore[arg-type]


def test_the_debounce_key_separates_people() -> None:
    one = alert.Alert(
        "insurance_agent", "days_uncovered", Decimal(3), 0, 1.0, ["a.pdf, page 1"], "A"
    )
    two = alert.Alert(
        "insurance_agent", "days_uncovered", Decimal(3), 0, 1.0, ["b.pdf, page 1"], "B"
    )

    assert one.key != two.key


def test_the_debounce_key_separates_two_policies_of_one_person() -> None:
    """Two lapsed policies on one person are two alerts, and saying one must not silence the
    other for a week."""
    motor = alert.Alert(
        "insurance_agent", "days_uncovered", Decimal(3), 0, 1.0, ["a.pdf, page 1"], "A", "MV-1"
    )
    home = alert.Alert(
        "insurance_agent", "days_uncovered", Decimal(9), 0, 1.0, ["b.pdf, page 1"], "A", "HM-2"
    )

    assert motor.key != home.key
    assert "MV-1" in motor.line()


def test_a_sum_is_per_person_and_cites_only_that_persons_receipts() -> None:
    rows = [
        ("Marcus Fernandez", Decimal("500.00"), "receipt-a.pdf", 1),
        ("Priya Nair", Decimal("250.00"), "receipt-b.pdf", 1),
        ("Marcus Fernandez", Decimal("300.00"), "receipt-c.pdf", 2),
    ]
    conn = FakeConn(rows)
    measured = {m.subject: m for m in alert.donations_ytd(conn, TODAY)}

    assert measured["Marcus Fernandez"].value == Decimal("800.00")
    assert measured["Marcus Fernandez"].citations == [
        "receipt-a.pdf, page 1",
        "receipt-c.pdf, page 2",
    ]
    assert measured["Priya Nair"].value == Decimal("250.00")
    assert measured["Priya Nair"].citations == ["receipt-b.pdf, page 1"]
    _query, params = conn.cursor_obj.executed[0]
    assert params["year_start"] == date(2026, 1, 1), "a year-to-date metric is given its year"


def test_each_policy_lapses_on_its_own() -> None:
    """A live travel policy must not make a lapsed motor policy read as covered."""
    rows = [
        ("Marcus Fernandez", "TR-9", date(2026, 12, 1), "travel.pdf", 1),
        ("Marcus Fernandez", "MV-1", date(2026, 6, 13), "motor-renewal.pdf", 2),
        ("Marcus Fernandez", "MV-1", date(2025, 6, 13), "motor-schedule.pdf", 1),
    ]
    lapses = alert.days_uncovered(FakeConn(rows), TODAY)

    assert [(m.subject, m.item, m.value) for m in lapses] == [
        ("Marcus Fernandez", "MV-1", Decimal(90))
    ]
    assert lapses[0].citations == ["motor-renewal.pdf, page 2"], "cites the latest expiry"


def test_the_catalogue_declares_metrics_that_exist() -> None:
    """A metric nobody implemented is a silent no-op, so it is caught here."""
    for config in catalog().documents.registers.alert or []:
        assert config.metric in alert.METRICS, (
            f"core/documents.yaml declares {config.metric}, which modules/alert/queries.py "
            "does not define"
        )


# ---------------------------------------------------- the alert metrics, against Postgres

MARCUS = "Marcus Lim Jun Wei"
RACHEL = "Rachel Ng Hui Shan"
AH_KOW = "Lim Ah Kow"


@pytest.fixture
def db() -> Iterator[Any]:
    psycopg = pytest.importorskip("psycopg")
    try:
        connection = psycopg.connect(
            Settings.load(ROOT).database_url, autocommit=False, connect_timeout=3
        )
    except psycopg.OperationalError as error:
        pytest.skip(f"no local database: {type(error).__name__}")
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT to_regclass('public.facts')")
            row = cur.fetchone()
            if row is None or row[0] is None:
                pytest.skip("the 0001_init migration has not been applied")
            # Empty copies of the three tables the Alert module reads, created in pg_temp. The
            # session searches pg_temp before public, so the module's unqualified queries see
            # only the register loaded below and never a document somebody has actually filed.
            cur.execute("CREATE TEMP TABLE documents (LIKE public.documents INCLUDING ALL)")
            cur.execute("CREATE TEMP TABLE facts (LIKE public.facts INCLUDING ALL)")
            cur.execute("CREATE TEMP TABLE traces (LIKE public.traces INCLUDING ALL)")
        yield connection
    finally:
        connection.rollback()  # nothing this test did survives, the temporary tables included
        connection.close()


def load_register(conn: Any, overrides: dict[tuple[str, str], str] | None = None) -> None:
    """Every batch1 row as the facts extraction would write, through the statement it uses.

    `overrides` replaces one field of one document, keyed by `(doc_id, field)`. Pages are 1:
    batch1 records no `field_pages`, and every one of its documents is a single page.
    """
    installed = catalog()
    with REGISTER.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(line for line in handle if not line.startswith("#")))

    with conn.cursor() as cur:
        for row in rows:
            cur.execute(
                "INSERT INTO documents (sha256, source_channel, original_name, mime, doc_type,"
                " pack_id, status, synthetic)"
                " VALUES (%s, 'folder', %s, 'application/pdf', %s, %s, 'indexed', true)"
                " RETURNING id",
                (
                    hashlib.sha256(row["doc_id"].encode()).digest(),
                    f"{row['doc_id']}.pdf",
                    row["doc_type"],
                    CORE,
                ),
            )
            (document_id,) = cur.fetchone()
            for spec in installed.spec(row["doc_type"]).fields:
                raw = (overrides or {}).get((row["doc_id"], spec.name), row.get(spec.name, ""))
                if not raw:
                    continue
                column = FACT_COLUMN[spec.type]
                cur.execute(
                    INSERT_FACT,
                    {
                        "document_id": document_id,
                        "page": 1,
                        "pack_id": CORE,
                        "pack_version": installed.version,
                        "key": spec.name,
                        "subject": row["subject"],
                        "value_text": raw if column == "value_text" else None,
                        "value_num": Decimal(raw) if column == "value_num" else None,
                        "value_date": date.fromisoformat(raw) if column == "value_date" else None,
                        "confidence": 1.0,
                    },
                )


def by_subject(measurements: list[alert.Measurement]) -> dict[str | None, Any]:
    return {m.subject: (m.value, m.citations) for m in measurements}


def test_srs_is_each_holders_own_statement_for_this_year(db: Any) -> None:
    """One member's statement must never drive another member's 15,300 cap."""
    load_register(db)

    assert by_subject(alert.srs_contributions_ytd(db, date(2025, 12, 20))) == {
        # Marcus's 2024 statement also reads 15,300; it is the 2025 one that is cited.
        MARCUS: (Decimal("15300.00"), ["b1-0025.pdf, page 1"]),
        RACHEL: (Decimal("8000.00"), ["b1-0027.pdf, page 1"]),
    }
    assert alert.srs_contributions_ytd(db, date(2026, 9, 13)) == [], "no 2026 statement is filed"


def test_donations_are_this_years_deductible_receipts_per_donor(db: Any) -> None:
    load_register(db)

    assert by_subject(alert.donations_ytd(db, date(2026, 9, 13))) == {
        MARCUS: (Decimal("500.00"), ["b1-0019.pdf, page 1"]),
        RACHEL: (Decimal("250.00"), ["b1-0020.pdf, page 1"]),
    }
    assert alert.donations_ytd(db, date(2025, 12, 20)) == [], (
        "Marcus's only 2025 receipt, b1-0021, states it is not tax deductible"
    )


def test_a_deductible_receipt_counts_in_its_own_year_only(db: Any) -> None:
    # A model returning a JSON boolean is stored as "True"; the register writes "true".
    load_register(db, overrides={("b1-0021", "tax_deductible"): "True"})

    assert by_subject(alert.donations_ytd(db, date(2026, 9, 13)))[MARCUS] == (
        Decimal("500.00"),
        ["b1-0019.pdf, page 1"],
    )
    assert by_subject(alert.donations_ytd(db, date(2025, 12, 20))) == {
        MARCUS: (Decimal("1000.00"), ["b1-0021.pdf, page 1"]),
    }


def test_cpf_is_this_years_payslips_per_employee(db: Any) -> None:
    load_register(db)

    assert by_subject(alert.cpf_contributions_ytd(db, date(2026, 9, 13))) == {
        MARCUS: (Decimal("3200.00"), ["b1-0017.pdf, page 1", "b1-0016.pdf, page 1"]),
        RACHEL: (Decimal("1250.00"), ["b1-0018.pdf, page 1"]),
    }
    assert alert.cpf_contributions_ytd(db, date(2025, 12, 20)) == []


def test_a_lapsed_policy_is_not_masked_by_another_that_still_runs(db: Any) -> None:
    """On 10 February 2027 Marcus's home contents cover has lapsed, while his motor and
    hospital policies still run. Grouped by person alone, he would read as covered."""
    load_register(db)

    lapses = {
        (m.subject, m.item): (m.value, m.citations)
        for m in alert.days_uncovered(db, date(2027, 2, 10))
    }

    assert set(lapses) == {(MARCUS, "HM-2024-559013"), (AH_KOW, "HS-2023-771904")}
    assert lapses[(MARCUS, "HM-2024-559013")] == (Decimal(10), ["b1-0002.pdf, page 1"])
    days, citations = lapses[(AH_KOW, "HS-2023-771904")]
    assert days == Decimal(27)
    assert citations[0] in {"b1-0003.pdf, page 1", "b1-0005.pdf, page 1"}  # both end 14 Jan


@pytest.mark.parametrize(
    ("as_of", "expected"),
    [
        (date(2025, 12, 20), {("srs_contributions_ytd", MARCUS)}),  # Rachel is at 8,000
        (
            date(2027, 2, 10),
            {("days_uncovered", MARCUS), ("days_uncovered", AH_KOW)},
        ),
    ],
)
def test_every_firing_is_scoped_and_cites_a_page(
    db: Any, as_of: date, expected: set[tuple[str, str]]
) -> None:
    load_register(db)

    firing = alert.sweep(db, as_of, mark=False)

    assert {(f.metric, f.subject) for f in firing} == expected
    assert len({f.key for f in firing}) == len(firing), "two alerts share a debounce key"
    for f in firing:
        assert f.citations, f"{f.key} fired uncited"
        assert all(c.startswith("b1-") and ", page " in c for c in f.citations)
