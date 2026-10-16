"""Which period a question names, and which period a document's printed dates cover."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from core.graph.period import Period, asked_period, document_period, outside

TODAY = date(2026, 10, 17)


@pytest.mark.parametrize(
    ("question", "expected"),
    [
        (
            "What was the premium on the car policy last year?",
            Period(date(2025, 1, 1), date(2025, 12, 31)),
        ),
        (
            "How much did I claim on the car last year?",
            Period(date(2025, 1, 1), date(2025, 12, 31)),
        ),
        ("What was last month's gross salary?", Period(date(2026, 9, 1), date(2026, 9, 30))),
        ("previous month salary how much", Period(date(2026, 9, 1), date(2026, 9, 30))),
    ],
)
def test_a_relative_period_is_the_previous_calendar_one(question: str, expected: Period) -> None:
    assert asked_period(question, TODAY) == expected


def test_last_month_in_january_is_last_december() -> None:
    assert asked_period("last month's pay?", date(2027, 1, 9)) == Period(
        date(2026, 12, 1), date(2026, 12, 31)
    )


@pytest.mark.parametrize(
    "question",
    [
        "When does the car insurance expire?",
        "What is my assessable income for YA2025?",  # named outright: retrieval finds it by label
        "How much of the PrivateCare deductible have I used this policy year?",
        "What did the yearly premium come to?",
    ],
)
def test_a_question_naming_no_relative_period_names_none(question: str) -> None:
    assert asked_period(question, TODAY) is None


def test_a_policy_covers_its_cover_date_to_its_expiry_and_not_its_holders_birthday() -> None:
    facts = [
        ("cover_from", date(2026, 4, 12)),
        ("expiry_date", date(2027, 4, 11)),
        ("date_of_birth", date(1987, 5, 8)),
        ("premium_payable", Decimal("1284.00")),
    ]
    assert document_period("policy_schedule", facts) == Period(date(2026, 4, 12), date(2027, 4, 11))


def test_a_payslip_covers_its_pay_month() -> None:
    period = document_period("payslip", [("pay_period", "2026-06"), ("net_pay", Decimal("7800"))])
    assert period == Period(date(2026, 6, 1), date(2026, 6, 30))


def test_a_statement_year_is_that_year_and_an_assessment_year_the_one_before() -> None:
    assert document_period("srs_statement", [("statement_year", Decimal("2025"))]) == Period(
        date(2025, 1, 1), date(2025, 12, 31)
    )
    # YA2026 assesses 2025's income; its payment due date is in 2026.
    noa = [("assessment_year", Decimal("2026")), ("payment_due_date", date(2026, 5, 30))]
    assert document_period("notice_of_assessment", noa) == Period(
        date(2025, 1, 1), date(2026, 5, 30)
    )


def test_a_document_that_prints_no_date_has_no_period() -> None:
    assert document_period("policy_schedule", [("insurer", "Meridian Assurance")]) is None
    assert document_period("not_a_type", [("cover_from", date(2026, 1, 1))]) is None


def test_a_sentence_is_outside_unless_some_cited_document_reaches_into_the_period() -> None:
    last_year = Period(date(2025, 1, 1), date(2025, 12, 31))
    periods = {
        "car": Period(date(2026, 4, 12), date(2027, 4, 11)),
        "old": Period(date(2025, 4, 12), date(2026, 4, 11)),
        "undated": None,
    }
    assert outside(last_year, ["car"], periods)
    assert outside(last_year, ["undated"], periods), "a claim placed nowhere is not placed then"
    assert not outside(last_year, ["car", "old"], periods)
