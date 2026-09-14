"""The types a calculator hands back, the owner's consent, and the record of an advice answer.

`core.graph.advice.Adviser` is `modules/advice/`'s to implement; nothing here computes a figure.
What is tested is the shared shape — `Input`, `Figure`, `Calculation`, `Missing`, `passages_for`
— and the two SQL modules built on `core.household.owner`, `core.advice_consent` and
`core.advice_records` (ADR 0016).
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from typing import Any

import pytest

from core import advice_consent, advice_records
from core.graph import advice

# --------------------------------------------------------------------------------- fake db


class FakeCursor:
    def __init__(self, conn: FakeConn) -> None:
        self._conn = conn
        self._rows: list[tuple[Any, ...]] = []
        self.rowcount = 0

    def execute(self, query: str, params: Any = None) -> None:
        self._conn.calls.append((query, params))
        self._rows, self.rowcount = ([], 0)
        for needle, (rows, rowcount) in self._conn.scripted.items():
            if needle in query:
                self._rows, self.rowcount = rows, rowcount
                break

    def fetchone(self) -> tuple[Any, ...] | None:
        return self._rows[0] if self._rows else None

    def fetchall(self) -> list[tuple[Any, ...]]:
        return self._rows

    def __enter__(self) -> FakeCursor:
        return self

    def __exit__(self, *exc: object) -> None:
        return None


class FakeConn:
    """A recording fake in the house style (see `tests/test_grounding_index.py`'s `FakeConn`):
    every statement and its parameters are kept in `calls`, and a test scripts what a query
    answers by a substring of it, rather than parsing SQL."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []
        self.commits = 0
        self.rollbacks = 0
        self.scripted: dict[str, tuple[list[tuple[Any, ...]], int]] = {}

    def script(
        self, needle: str, rows: list[tuple[Any, ...]] | None = None, rowcount: int | None = None
    ) -> None:
        rows = rows or []
        self.scripted[needle] = (rows, rowcount if rowcount is not None else len(rows))

    def cursor(self) -> FakeCursor:
        return FakeCursor(self)

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1

    def params_for(self, needle: str) -> Any:
        for query, params in self.calls:
            if needle in query:
                return params
        raise AssertionError(f"no statement containing {needle!r} was executed")


def _owned(conn: FakeConn, person_id: int = 1) -> None:
    """Script the owner household.owner reads: one person, `is_owner`."""
    conn.script("FROM people p", rows=[(person_id, "Marcus Lim", "self", True, False, [])])


def _no_owner(conn: FakeConn) -> None:
    conn.script("FROM people p", rows=[])


# ------------------------------------------------------------------------------ advice_consent


def test_current_returns_the_id_of_the_latest_granted_row_at_the_same_version() -> None:
    conn = FakeConn()
    _owned(conn)
    conn.script("FROM advice_consents", rows=[(42, "granted", "1.0.0")])

    assert advice_consent.current(conn, "iras_tax", "1.0.0") == 42


def test_current_is_none_when_the_latest_grant_is_a_different_version() -> None:
    conn = FakeConn()
    _owned(conn)
    conn.script("FROM advice_consents", rows=[(42, "granted", "0.9.0")])

    assert advice_consent.current(conn, "iras_tax", "1.0.0") is None


def test_a_withdrawal_after_a_grant_gives_none() -> None:
    conn = FakeConn()
    _owned(conn)
    # The latest row is the withdrawal; an earlier grant at the same version does not count.
    conn.script("FROM advice_consents", rows=[(43, "withdrawn", "1.0.0")])

    assert advice_consent.current(conn, "iras_tax", "1.0.0") is None
    assert advice_consent.status(conn, "iras_tax", "1.0.0") == "withdrawn"


def test_an_older_version_gives_status_outdated() -> None:
    conn = FakeConn()
    _owned(conn)
    conn.script("FROM advice_consents", rows=[(42, "granted", "0.9.0")])

    assert advice_consent.status(conn, "iras_tax", "1.0.0") == "outdated"


def test_no_owner_gives_none_from_current_and_grant_raises() -> None:
    conn = FakeConn()
    _no_owner(conn)

    assert advice_consent.current(conn, "iras_tax", "1.0.0") is None
    assert advice_consent.status(conn, "iras_tax", "1.0.0") == "none"
    with pytest.raises(advice_consent.NoOwner):
        advice_consent.grant(conn, "iras_tax", "1.0.0", "I consent to advice on this basis.", "web")


def test_grant_inserts_the_owner_and_the_wording_hash() -> None:
    conn = FakeConn()
    _owned(conn, person_id=9)
    conn.script("INSERT INTO advice_consents", rows=[(101,)])
    wording = "I consent to advice on this basis."

    row_id = advice_consent.grant(conn, "iras_tax", "1.0.0", wording, "telegram")

    assert row_id == 101
    params = conn.params_for("INSERT INTO advice_consents")
    assert params["person_id"] == 9
    assert params["pack_id"] == "iras_tax"
    assert params["version"] == "1.0.0"
    assert params["action"] == "granted"
    assert params["channel"] == "telegram"
    assert params["wording_sha256"] == hashlib.sha256(wording.encode("utf-8")).digest()
    assert conn.commits == 1


def test_withdraw_inserts_a_withdrawn_row() -> None:
    conn = FakeConn()
    _owned(conn)
    conn.script("INSERT INTO advice_consents", rows=[(102,)])

    advice_consent.withdraw(conn, "iras_tax", "1.0.0", "I withdraw my consent.", "cli")

    params = conn.params_for("INSERT INTO advice_consents")
    assert params["action"] == "withdrawn"


def test_household_consents_implements_the_consent_book_port() -> None:
    conn = FakeConn()
    _owned(conn)
    conn.script("FROM advice_consents", rows=[(42, "granted", "1.0.0")])
    book: advice.ConsentBook = advice_consent.HouseholdConsents(conn)

    assert book.current("iras_tax", "1.0.0") == 42


# ------------------------------------------------------------------------------------ advice


def _calculation() -> advice.Calculation:
    return advice.Calculation(
        pack_id="iras_tax",
        shape_id="gap",
        label="Protection gap",
        subject="Marcus Lim",
        person_ids=(1,),
        inputs=(
            advice.Input(
                ref="fact:12",
                role="income",
                label="annual income",
                value_text="SGD 9,400.00",
                citation="payslip.pdf, page 1",
                document_id="doc-1",
                page=1,
            ),
            advice.Input(
                ref="rule:7",
                role="multiple",
                label="protection multiple",
                value_text="4 times",
                citation="MoneySense, Basic Financial Planning Guide, 26 September 2023",
                publisher="MoneySense",
                title="Basic Financial Planning Guide",
                dated="26 September 2023",
                url="https://www.moneysense.gov.sg/basic-financial-planning-guide",
            ),
        ),
        figures=(
            advice.Figure(
                name="target", value=Decimal("37600.00"), text="SGD 37,600.00", words=("target",)
            ),
            advice.Figure(
                name="gap",
                value=Decimal("28200.00"),
                text="SGD 28,200.00",
                words=("gap", "shortfall"),
            ),
        ),
        verdict="no_room",
        verdict_text="Marcus Lim has a protection gap of SGD 28,200.00.",
    )


def test_passages_for_gives_fact_rule_and_calculation_refs() -> None:
    passages = advice.passages_for(_calculation())

    assert [p.ref for p in passages] == ["fact:12", "rule:7", "calculation:0"]


def test_passages_for_prints_every_figure_on_the_calculation_passage() -> None:
    passages = advice.passages_for(_calculation())

    calculation_passage = passages[-1]
    assert calculation_passage.kind == "calculation"
    assert "target: SGD 37,600.00" in calculation_passage.text
    assert "gap: SGD 28,200.00" in calculation_passage.text


# ---------------------------------------------------------------------------- advice_records


def test_record_insert_includes_the_sha256_of_the_disclaimer() -> None:
    conn = FakeConn()
    disclaimer = "This is not financial advice. A licensed professional can help you decide."
    entry = advice.AdviceRecord(
        thread_id="thread-1",
        pack_id="iras_tax",
        pack_version="1.0.0",
        shape="gap",
        subject="Marcus Lim",
        person_ids=(1,),
        consent_id=42,
        outcome="advised",
        verdict="no_room",
        basis={"income": Decimal("9400.00")},
        disclaimer=disclaimer,
        answer_text="Your protection gap is SGD 28,200.00.",
    )

    advice_records.HouseholdAdviceLog(conn).record(entry)

    params = conn.params_for("INSERT INTO advice_records")
    assert params["disclaimer_sha256"] == hashlib.sha256(disclaimer.encode("utf-8")).digest()
    assert params["consent_id"] == 42
    assert params["outcome"] == "advised"
    assert params["subject_person_ids"] == [1]
    assert json.loads(params["basis"]) == {"income": "9400.00"}
    assert conn.commits == 0  # the caller's transaction, not this module's
