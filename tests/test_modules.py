"""Reminder and Alert: what fires, once, and with what behind it.

Both modules are pure functions over rows, so both are tested with a fake cursor rather than a
database. That is deliberate — the behaviour worth protecting is "nothing fires twice" and
"nothing fires uncited", and neither of those is a property of Postgres.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any

import pytest

from core.contracts import AlertConfig
from modules import alert, reminder
from modules.reminder import already_said, current_lead

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


class FakePack:
    def __init__(self, pack_id: str, configs: list[AlertConfig]) -> None:
        self.id = pack_id
        self.manifest = type(
            "M",
            (),
            {"registers": type("R", (), {"alert": configs})()},
        )()


SRS = AlertConfig(metric="srs_contributions_ytd", ceiling=15300, warn_at=0.9)


def test_a_threshold_crossing_fires_with_the_document_behind_it() -> None:
    measurement = [(Decimal("14000.00"), "Marcus Fernandez", "doc", 2, "srs-2026.pdf")]
    conn = FakeConn(measurement, [], [])
    firing = alert.sweep(conn, TODAY, packs=(FakePack("iras_tax", [SRS]),))  # type: ignore[arg-type]

    assert len(firing) == 1
    assert firing[0].citations == ["srs-2026.pdf, page 2"]
    assert "92%" in firing[0].line(), "14000 of 15300 is 91.5%, which rounds to 92"
    assert conn.commits == 1


def test_below_the_warning_share_nothing_fires() -> None:
    conn = FakeConn([(Decimal("5000.00"), "Marcus Fernandez", "doc", 2, "srs-2026.pdf")])
    assert alert.sweep(conn, TODAY, packs=(FakePack("iras_tax", [SRS]),)) == []  # type: ignore[arg-type]


def test_a_recent_firing_is_debounced() -> None:
    measurement = [(Decimal("14000.00"), "Marcus Fernandez", "doc", 2, "srs-2026.pdf")]
    just_fired = [(datetime.now(UTC) - timedelta(hours=2), {"value": "14000.00"})]
    conn = FakeConn(measurement, just_fired)

    assert alert.sweep(conn, TODAY, packs=(FakePack("iras_tax", [SRS]),)) == []  # type: ignore[arg-type]
    assert conn.commits == 0


def test_a_firing_older_than_the_debounce_window_fires_again() -> None:
    measurement = [(Decimal("14000.00"), "Marcus Fernandez", "doc", 2, "srs-2026.pdf")]
    long_ago = [(datetime.now(UTC) - timedelta(days=30), {"value": "9000.00"})]
    conn = FakeConn(measurement, long_ago, [])

    firing = alert.sweep(conn, TODAY, packs=(FakePack("iras_tax", [SRS]),))  # type: ignore[arg-type]
    assert len(firing) == 1


def test_a_metric_no_query_defines_cannot_fire() -> None:
    invented = AlertConfig(metric="made_up_metric", ceiling=10, warn_at=0.5)
    conn = FakeConn()

    assert alert.sweep(conn, TODAY, packs=(FakePack("iras_tax", [invented]),)) == []  # type: ignore[arg-type]


def test_the_debounce_key_separates_people() -> None:
    one = alert.Alert(
        "insurance_agent", "days_uncovered", Decimal(3), 0, 1.0, ["a.pdf, page 1"], "A"
    )
    two = alert.Alert(
        "insurance_agent", "days_uncovered", Decimal(3), 0, 1.0, ["b.pdf, page 1"], "B"
    )

    assert one.key != two.key


def test_the_real_packs_declare_metrics_that_exist() -> None:
    """A pack naming a metric nobody implemented is a silent no-op, so it is caught here."""
    from core.packs import installed_packs

    for installed in installed_packs():
        for config in installed.manifest.registers.alert or []:
            assert config.metric in alert.METRICS, (
                f"{installed.id} declares {config.metric}, which modules/alert/queries.py "
                "does not define"
            )
