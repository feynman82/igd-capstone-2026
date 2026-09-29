"""The tax pack's advice, run on batch 1's own SRS statements and Notices of Assessment.

Every figure below is worked out by hand from the register and the published YA2024-onwards
resident rates, so a change to the shapes or to the calculator that moves one is caught here
rather than in front of a household. The rates are test fixtures standing in for approved
grounding values: the pack names the key, never the number (ADR 0016).
"""

from __future__ import annotations

import csv
from dataclasses import replace
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from core.contracts import AdviceShape
from core.graph.advice import Calculation, Missing
from core.graph.answer import AnswerGraph
from core.graph.knowledge import mentions
from core.packs import pack
from modules.advice import Basis, FactRow, ValueRow, calculate

REGISTER = Path(__file__).resolve().parents[1] / "corpus" / "register" / "batch1.csv"
MARCUS = "Marcus Lim Jun Wei"
RACHEL = "Rachel Ng Hui Shan"

# Resident rates on chargeable income, YA2024 onwards: (lower, upper, rate in percent).
RESIDENT_BANDS = [
    (0, 20000, "0"),
    (20000, 30000, "2"),
    (30000, 40000, "3.5"),
    (40000, 80000, "7"),
    (80000, 120000, "11.5"),
    (120000, 160000, "15"),
    (160000, 200000, "18"),
    (200000, 240000, "19"),
    (240000, 280000, "19.5"),
    (280000, 320000, "20"),
    (320000, 500000, "22"),
    (500000, 1000000, "23"),
    (1000000, None, "24"),
]


def _register() -> list[dict[str, str]]:
    with REGISTER.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(line for line in handle if not line.startswith("#")))


def _latest(doc_type: str, subject: str, field: str) -> FactRow:
    """The subject's newest `doc_type` in the register, as the fact extraction wrote it."""
    rows = [r for r in _register() if r["doc_type"] == doc_type and r["subject"] == subject]
    assert rows, f"no {doc_type} for {subject} in {REGISTER.name}"
    newest = max(rows, key=lambda r: r["issued_date"])
    return FactRow(
        fact_id=int(newest["doc_id"].split("-")[1]),
        document_id=newest["doc_id"],
        name=f"{newest['doc_id']}.pdf",
        doc_type=doc_type,
        page=1,
        key=field,
        value=Decimal(newest[field]),
        subject=subject,
        when=datetime.fromisoformat(newest["issued_date"]).replace(tzinfo=UTC),
        field_type="money",
    )


def _published(value_id: int, key: str, number: str, unit: str, **qualifiers: object) -> ValueRow:
    return ValueRow(
        value_id=value_id,
        key=key,
        unit=unit,
        value_num=Decimal(number),
        value_text=None,
        qualifiers=qualifiers,
        passage="as printed on the IRAS page",
        effective_from=None,
        title="IRAS guidance",
        publisher="Inland Revenue Authority of Singapore",
        url="https://www.iras.gov.sg/",
        published_on=None,
        retrieved_on=date(2026, 9, 29),
    )


def _shape(shape_id: str) -> AdviceShape:
    advice = pack("iras_tax").manifest.advice
    assert advice is not None
    return next(shape for shape in advice.shapes if shape.id == shape_id)


def _basis(shape_id: str, subject: str) -> Basis:
    shape = _shape(shape_id)
    srs = _latest("srs_statement", subject, "contributions_ytd")
    if shape.calculator == "remaining_room":
        facts = {"used": [srs]}
        rules = {"cap": [_published(1, "srs_contribution_cap", "15300", "money")]}
    else:
        facts = {
            "income": [_latest("notice_of_assessment", subject, "assessable_income")],
            "amount": [srs],
        }
        rules = {
            "rate": [
                _published(10 + i, "tax_rate", rate, "rate", band_lower=lower, band_upper=upper)
                for i, (lower, upper, rate) in enumerate(RESIDENT_BANDS)
            ]
        }
    qualifiers = {"tax_rate": ("band_lower", "band_upper")}
    return Basis("iras_tax", shape, subject, (1,), facts, rules, {}, {}, qualifiers)


@pytest.mark.parametrize(
    ("subject", "verdict", "room"),
    [
        (MARCUS, "no_room", "0.00"),  # SGD 15,300 contributed against a 15,300 cap
        (RACHEL, "room_left", "7300.00"),  # SGD 8,000 contributed
    ],
)
def test_srs_room_is_the_cap_less_this_years_contributions(
    subject: str, verdict: str, room: str
) -> None:
    result = calculate(_basis("srs_room", subject))
    assert isinstance(result, Calculation)
    assert result.verdict == verdict
    assert {f.name: f.value for f in result.figures}["room"] == Decimal(room)


@pytest.mark.parametrize(
    ("subject", "saving"),
    [
        (MARCUS, "1759.50"),  # SGD 112,800 falls in the 11.5% band; 15,300 x 11.5%
        (RACHEL, "560.00"),  # SGD 75,000 falls in the 7% band; 8,000 x 7%
    ],
)
def test_the_srs_saving_is_an_estimate_at_the_band_the_assessed_income_falls_in(
    subject: str, saving: str
) -> None:
    result = calculate(_basis("srs_saving", subject))
    assert isinstance(result, Calculation)
    assert (result.verdict, result.estimate) == ("estimate", True)
    assert result.verdict_text.startswith("Estimated:")
    assert {f.name: f.value for f in result.figures}["saving"] == Decimal(saving)


def test_no_saving_is_estimated_without_a_notice_of_assessment() -> None:
    basis = _basis("srs_saving", RACHEL)
    result = calculate(replace(basis, facts={**basis.facts, "income": []}))
    assert isinstance(result, Missing)
    assert result.items == (_shape("srs_saving").facts[0].missing,)


def _matched(question: str) -> str | None:
    """The shape id the answer graph picks for a question with both packs enabled, insurance
    first, as the registry lists them."""
    graph = object.__new__(AnswerGraph)  # the matcher reads only the packs it is handed
    found = graph._advice_shape(question, [pack("insurance_agent"), pack("iras_tax")])
    return f"{found[0].id}.{found[1].id}" if found else None


@pytest.mark.parametrize(
    ("question", "expected"),
    [
        ("How much more can I put in SRS this year?", "iras_tax.srs_room"),
        ("what's my SRS cap left", "iras_tax.srs_room"),
        ("How much tax will SRS save me?", "iras_tax.srs_saving"),
        ("How can I reduce my tax?", "iras_tax.review"),
        ("Which reliefs am I missing?", "iras_tax.review"),
        ("Am I underinsured?", "insurance_agent.review"),  # the tax pack takes nothing from it
        ("Do I have enough critical illness cover?", "insurance_agent.ci_cover"),
    ],
)
def test_a_tax_question_reaches_the_tax_shape_and_insurance_keeps_its_own(
    question: str, expected: str
) -> None:
    assert _matched(question) == expected


def test_the_review_runs_only_declared_shapes_and_never_names_a_bill() -> None:
    manifest = pack("iras_tax").manifest
    advice = manifest.advice
    assert advice is not None and advice.review is not None
    assert advice.review.shapes == ["srs_room", "srs_saving"]
    assert all(not mentions(p, "tax payable") for p in advice.review.asked)
    assert manifest.grounding.corpus == "iras_tax_ya2025_ya2027"


def test_the_persona_is_voice_and_the_decline_names_what_advice_would_calculate() -> None:
    manifest = pack("iras_tax").manifest
    assert "never" not in manifest.persona.system.lower()  # rules live in the core, not the voice
    assert "SRS" in manifest.guardrails.advice_decline
