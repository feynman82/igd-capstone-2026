"""Metrics 7 and 8: obligation precision and the alert false-positive rate.

No database and no modules sweep here. Both metrics compare rows against the register, so the
rows can be built by hand — which is also the only way to test the failure cases, because a
correct system does not produce them.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from eval.modules import (
    ALERT_TARGET,
    OBLIGATION_TARGET,
    AlertVerdict,
    Measured,
    ModuleMetrics,
    Obligation,
    alert_fpr,
    obligation_precision,
    obligations_possible,
    register_cpf_contributions_ytd,
    register_days_uncovered,
    register_donations_ytd,
    register_srs_contributions_ytd,
    render,
    score_alerts,
    score_obligations,
)

TODAY = date(2026, 10, 1)

REGISTER = [
    {
        "doc_id": "b1-0001",
        "doc_type": "policy_schedule",
        "subject": "Marcus Lim Jun Wei",
        "policy_no": "MV-2026-448120",
        "expiry_date": "2027-04-11",
    },
    # A renewal notice printing last year's expiry for a policy whose schedule runs to 2027.
    {
        "doc_id": "b2-0007",
        "doc_type": "renewal_notice",
        "subject": "Rachel Ng Hui Shan",
        "policy_no": "PH-2024-912404",
        "expiry_date": "2026-02-28",
    },
    {
        "doc_id": "b2-0004",
        "doc_type": "policy_schedule",
        "subject": "Rachel Ng Hui Shan",
        "policy_no": "PH-2024-912404",
        "expiry_date": "2027-02-28",
    },
    {
        "doc_id": "b2-0020",
        "doc_type": "passport",
        "subject": "Rachel Ng Hui Shan",
        "full_name": "RACHEL NG HUI SHAN",
        "date_of_expiry": "2033-02-28",
    },
]


class Config:
    """A `ReminderConfig` as far as this module reads one."""

    def __init__(self, key: str, from_field: str | None = None, on_date: date | None = None):
        self.key = key
        self.from_field = from_field
        self.on_date = on_date
        self.lead_days = [60, 30, 7]


DECLARED = [
    Config("policy_expiry", from_field="expiry_date"),
    Config("passport_expiry", from_field="date_of_expiry"),
    Config("filing_deadline", on_date=date(2027, 4, 18)),
]


def _obligation(**kwargs: object) -> Obligation:
    fields: dict[str, object] = {
        "obligation_id": 1,
        "label": "policy expiry — Marcus Lim Jun Wei",
        "due_date": date(2027, 4, 11),
        "subject": "Marcus Lim Jun Wei",
        "key": "expiry_date",
        "doc_id": "b1-0001",
        "recurrence": None,
    }
    fields.update(kwargs)
    return Obligation(**fields)  # type: ignore[arg-type]


# ------------------------------------------------------------------------------- obligations


def test_an_obligation_whose_date_the_document_prints_is_correct() -> None:
    verdicts = score_obligations([_obligation()], REGISTER, DECLARED)
    assert [v.verdict for v in verdicts] == ["matches the register"]
    assert obligation_precision(verdicts) == 1.0


def test_a_date_the_document_does_not_print_is_a_false_obligation() -> None:
    """The failure this metric exists for: a reminder for a date nobody printed."""
    wrong = _obligation(due_date=date(2027, 4, 1))
    verdicts = score_obligations([wrong], REGISTER, DECLARED)
    assert verdicts[0].verdict == "a date the document does not print"
    assert verdicts[0].expected == "2027-04-11"  # what the register holds instead
    assert obligation_precision(verdicts) == 0.0


def test_the_right_date_against_the_wrong_person_is_also_false() -> None:
    verdicts = score_obligations([_obligation(subject="Rachel Ng Hui Shan")], REGISTER, DECLARED)
    assert verdicts[0].verdict == "the wrong person"


def test_case_is_not_a_disagreement_about_who_someone_is() -> None:
    """A passport prints RACHEL NG HUI SHAN; the register writes it in title case."""
    passport = _obligation(
        label="passport expiry — RACHEL NG HUI SHAN",
        due_date=date(2033, 2, 28),
        subject="RACHEL NG HUI SHAN",
        key="date_of_expiry",
        doc_id="b2-0020",
    )
    assert score_obligations([passport], REGISTER, DECLARED)[0].correct


def test_a_calendar_deadline_is_checked_against_the_catalogue_and_counted_apart() -> None:
    """It belongs to no document, so the register cannot speak for it, and scoring it against the
    register would read as a failure of the module rather than an absence of ground truth."""
    filing = _obligation(
        label="filing deadline", due_date=date(2027, 4, 18), subject=None, key=None, doc_id=None
    )
    invented = _obligation(
        label="filing deadline", due_date=date(2027, 7, 1), subject=None, key=None, doc_id=None
    )
    verdicts = score_obligations([filing, invented], REGISTER, DECLARED)
    assert [v.verdict for v in verdicts] == [
        "declared in the catalogue",
        "no catalogue deadline says so",
    ]
    # Neither one moves the precision, which is over document-derived rows only.
    assert obligation_precision(verdicts) is None
    assert (
        obligation_precision(score_obligations([_obligation(), filing], REGISTER, DECLARED)) == 1.0
    )


def test_an_obligation_for_a_document_the_register_does_not_have() -> None:
    verdicts = score_obligations([_obligation(doc_id="not-a-row")], REGISTER, DECLARED)
    assert verdicts[0].verdict == "no register row for that document"


def test_what_the_register_supports_is_reported_beside_the_precision() -> None:
    """Precision over three rows is not a reminder system that found everything, so the number of
    obligations the register could support is reported next to it."""
    assert obligations_possible(REGISTER, DECLARED) == 4  # three expiry dates and one passport


# ------------------------------------------------------------------------------- alerts


class Fired:
    """A `modules.alert.Alert` as far as `score_alerts` reads one."""

    def __init__(
        self,
        metric: str,
        value: Decimal,
        ceiling: float,
        warn_at: float = 1.0,
        subject: str | None = None,
        item: str | None = None,
    ):
        self.metric = metric
        self.value = value
        self.ceiling = ceiling
        self.warn_at = warn_at
        self.subject = subject
        self.item = item


def test_an_alert_the_register_contradicts_is_a_false_positive() -> None:
    """The real case, as of this corpus: the vault extracted the renewal notice's 2026 expiry and
    not the schedule's 2027 one, so the module believes a live policy lapsed 215 days ago."""
    fired = Fired(
        "days_uncovered",
        Decimal(215),
        ceiling=0.0,
        subject="Rachel Ng Hui Shan",
        item="PH-2024-912404",
    )
    verdicts = score_alerts([fired], REGISTER, TODAY)
    assert verdicts[0].false_positive
    assert verdicts[0].register_value == Decimal(-150)  # cover still to run, not a gap
    assert "2027-02-28" in verdicts[0].reason
    assert alert_fpr(verdicts) == 1.0


def test_an_alert_the_register_agrees_with_is_not_counted_against_the_module() -> None:
    lapsed = [{**REGISTER[0], "expiry_date": "2026-01-01"}]
    fired = Fired(
        "days_uncovered",
        Decimal(273),
        ceiling=0.0,
        subject="Marcus Lim Jun Wei",
        item="MV-2026-448120",
    )
    verdicts = score_alerts([fired], lapsed, TODAY)
    assert not verdicts[0].false_positive
    assert alert_fpr(verdicts) == 0.0


def test_nothing_fired_is_unmeasured_rather_than_zero() -> None:
    """A module that never fires must not be able to claim a false-positive rate of 0.00."""
    assert alert_fpr([]) is None


def test_a_metric_with_no_register_equivalent_is_not_guessed_at() -> None:
    fired = Fired("something_new", Decimal(5), ceiling=1.0, subject="Marcus Lim Jun Wei")
    verdict = score_alerts([fired], REGISTER, TODAY)[0]
    assert not verdict.false_positive  # unscorable; counting it either way would be a guess
    assert "no register equivalent" in verdict.reason


# ------------------------------------------------------------------------------- the metrics


def test_the_register_metrics_mirror_the_modules_queries() -> None:
    """Each one recomputed from register columns, not from the module's SQL — a metric checked by
    the query that produced it is not checked at all."""
    # The latest expiry per policy wins, so the renewal notice does not lapse the policy.
    gaps = {m.item: m.value for m in register_days_uncovered(REGISTER, TODAY)}
    assert gaps["PH-2024-912404"] == Decimal(-150)
    assert gaps["MV-2026-448120"] == Decimal(-192)

    srs = [
        {"subject": "A", "contributions_ytd": "13000.00", "statement_year": "2026"},
        {"subject": "A", "contributions_ytd": "15300.00", "statement_year": "2026"},
        {
            "subject": "A",
            "contributions_ytd": "99999.00",
            "statement_year": "2025",
        },  # not this year
    ]
    assert register_srs_contributions_ytd(srs, TODAY) == [
        Measured(Decimal("15300.00"), "A")  # restated, so the largest wins rather than the sum
    ]

    receipts = [
        {
            "subject": "A",
            "donation_amount": "100.00",
            "donation_date": "2026-03-01",
            "tax_deductible": "true",
        },
        {
            "subject": "A",
            "donation_amount": "50.00",
            "donation_date": "2026-04-01",
            "tax_deductible": "TRUE",
        },
        {
            "subject": "A",
            "donation_amount": "25.00",
            "donation_date": "2026-05-01",
            "tax_deductible": "",
        },  # says nothing, so it is not claimed
        {
            "subject": "A",
            "donation_amount": "70.00",
            "donation_date": "2025-05-01",
            "tax_deductible": "true",
        },  # last year
    ]
    assert register_donations_ytd(receipts, TODAY) == [Measured(Decimal("150.00"), "A")]

    payslips = [
        {"subject": "A", "cpf_employee": "1200.00", "pay_period": "2026-01"},
        {"subject": "A", "cpf_employee": "1200.00", "pay_period": "2026-02"},
        {"subject": "A", "cpf_employee": "1200.00", "pay_period": "2025-12"},
    ]
    assert register_cpf_contributions_ytd(payslips, TODAY) == [Measured(Decimal("2400.00"), "A")]


# ------------------------------------------------------------------------------- the report


def test_the_report_marks_both_metrics_against_their_target() -> None:
    """Metric 7 is a floor and metric 8 is a ceiling, so one is met by being high and the other
    by being low. Getting that backwards would report a broken module as passing."""
    metrics = ModuleMetrics(
        as_of=TODAY,
        obligations=score_obligations([_obligation()], REGISTER, DECLARED),
        alerts=[
            AlertVerdict(
                "days_uncovered",
                "Rachel Ng Hui Shan",
                "PH-2024-912404",
                Decimal(215),
                Decimal(-150),
                crosses=False,
                ceiling=0.0,
                reason="the register's latest expiry for it is 2027-02-28",
            )
        ],
        possible=4,
        due_today=0,
        overdue=1,
    )
    assert metrics.precision == 1.0 and metrics.fpr == 1.0
    text = render(metrics, git_sha="abc1234", corpus_sha="0f0f0f0f0f0f0f0f")
    assert f"| Obligation precision | ≥ {OBLIGATION_TARGET:.2f} | 1.000 ✓ |" in text
    assert f"| Alert false-positive rate | ≤ {ALERT_TARGET:.2f} | 1.000 ✗ |" in text
    assert "false positive ✗" in text
    assert "2027-02-28" in text
    assert "negative value in the register column is cover still to run" in text
    assert "0 obligation(s) inside a lead window and 1 overdue" in text
    assert text.rstrip().endswith("_(one paragraph, written on the day)_")


def test_the_report_says_nothing_fired_rather_than_printing_a_rate() -> None:
    metrics = ModuleMetrics(
        as_of=TODAY, obligations=[], alerts=[], possible=4, due_today=0, overdue=0
    )
    text = render(metrics, git_sha="abc1234", corpus_sha="0f0f0f0f0f0f0f0f")
    assert "| Alert false-positive rate | ≤ 0.05 | — |" in text
    assert "unmeasured rather than 0.00" in text


def test_the_detail_in_a_result_file_explains_its_own_score() -> None:
    metrics = ModuleMetrics(
        as_of=TODAY,
        obligations=score_obligations(
            [_obligation(), _obligation(obligation_id=2, due_date=date(2030, 1, 1))],
            REGISTER,
            DECLARED,
        ),
        alerts=[],
        possible=4,
        due_today=0,
        overdue=1,
    )
    detail = metrics.as_dict()
    assert detail["as_of"] == "2026-10-01"
    assert detail["obligations"]["by_verdict"] == {
        "a date the document does not print": 1,
        "matches the register": 1,
    }
    assert detail["obligations"]["the_register_supports"] == 4
    assert detail["alerts"] == {"fired": 0, "false": 0, "each": []}
    assert detail["reminders_on_the_day"] == {"due": 0, "overdue": 1}
