"""The advice calculators: every figure worked out in code, every input cited, nothing guessed.

The arithmetic is tested over rows, with no database, because the behaviour worth protecting is
"the gap is SGD 251,200.00" and "a missing payslip is named, not estimated around", and neither
is a property of Postgres.

Which facts are whose, and which published values are fit to read, *are* properties of the SQL.
So `FACTS_FOR`, `NAMES_FOR` and `VALUES_FOR` are also run against Postgres, on empty temporary
copies of their tables, inside a transaction that is rolled back.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator
from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
import yaml

from core import modules as module_loader
from core.contracts import AdviceShape, PackManifest
from core.graph.advice import Calculation, Missing, passages_for
from core.packs import InstalledPack
from core.runtime.settings import Settings
from modules import advice
from modules.advice import (
    FEWER_THAN_TWO,
    NOTHING_SHARED,
    Basis,
    FactRow,
    ModuleAdviser,
    ValueRow,
    calculate,
    facts_for,
    money,
    names_for,
    take,
    values_for,
)

ROOT = Path(__file__).resolve().parents[1]
TODAY = date(2026, 9, 14)
INGESTED = datetime(2026, 9, 1, 9, 0, tzinfo=UTC)
MARCUS = "Marcus Lim Jun Wei"

INCOME_MISSING = "A recent payslip, to know your income."
HELD_MISSING = "The schedule of each critical illness plan you hold."
MULTIPLE_MISSING = "Reviewed guidance on how much cover to hold."
MARKET_MISSING = "Reviewed published premiums to compare against."
RATE_MISSING = "The published tax rate for your income band."
CAP_MISSING = "The published SRS contribution cap."
HELD_PLAN_MISSING = "The schedule of the hospital plan you hold."
VALUE_MISSING = "The statement that prints what the plan is worth now."
PAID_MISSING = "The statement that prints the premiums paid to date."


# ---------------------------------------------------------------------------------- fakes


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

    def __enter__(self) -> FakeCursor:
        return self

    def __exit__(self, *exc: object) -> None:
        return None


class FakeConn:
    def __init__(self, *results: list[tuple[Any, ...]]) -> None:
        self.cursor_obj = FakeCursor(list(results))

    def cursor(self) -> FakeCursor:
        return self.cursor_obj


# --------------------------------------------------------------------------------- builders


def fact(
    fact_id: int,
    document: str,
    value: Any,
    *,
    key: str = "sum_insured",
    field_type: str = "money",
    doc_type: str = "policy_schedule",
) -> FactRow:
    numeric = field_type in {"money", "integer", "percent"}
    return FactRow(
        fact_id=fact_id,
        document_id=document,
        name=f"{document}.pdf",
        doc_type=doc_type,
        page=1,
        key=key,
        value=Decimal(value) if numeric else value,
        subject=MARCUS,
        when=INGESTED,
        field_type=field_type,
    )


def published(
    value_id: int,
    key: str,
    number: str | None,
    *,
    unit: str = "money",
    text: str | None = None,
    **qualifiers: Any,
) -> ValueRow:
    return ValueRow(
        value_id=value_id,
        key=key,
        unit=unit,
        value_num=None if number is None else Decimal(number),
        value_text=text,
        qualifiers=qualifiers,
        passage="as printed in the guide",
        effective_from=None,
        title="Guide title",
        publisher="Publisher",
        url="https://example.gov.sg/guide",
        published_on=date(2023, 9, 26),
        retrieved_on=date(2026, 9, 1),
    )


def shape(calculator: str, facts: list[dict[str, Any]], **extra: Any) -> AdviceShape:
    return AdviceShape.model_validate(
        {
            "id": f"shape_{calculator}",
            "calculator": calculator,
            "label": extra.pop("label", "the figure asked about"),
            "asked": ["how much"],
            "facts": facts,
            **extra,
        }
    )


def basis(
    advice_shape: AdviceShape,
    facts: dict[str, list[FactRow]],
    rules: dict[str, list[ValueRow]] | None = None,
    *,
    compared: dict[str, list[FactRow]] | None = None,
    market: dict[str, list[ValueRow]] | None = None,
    qualifiers: dict[str, tuple[str, ...]] | None = None,
) -> Basis:
    return Basis(
        "insurance_agent",
        advice_shape,
        MARCUS,
        (1,),
        facts,
        rules or {},
        compared or {},
        market or {},
        qualifiers or {},
    )


GAP_SHAPE: dict[str, Any] = {
    "id": "ci_gap",
    "calculator": "gap",
    "label": "critical illness cover gap",
    "asked": ["critical illness gap"],
    "facts": [
        {
            "role": "income",
            "doc_types": ["payslip"],
            "field": "gross_salary",
            "per": "month",
            "missing": INCOME_MISSING,
        },
        {
            "role": "held",
            "doc_types": ["policy_schedule"],
            "field": "sum_insured",
            "category": "critical_illness",
            "take": "sum",
            "missing": HELD_MISSING,
        },
    ],
    "rules": [{"role": "multiple", "key": "ci_multiple", "missing": MULTIPLE_MISSING}],
}
GAP = AdviceShape.model_validate(GAP_SHAPE)


def advised_pack() -> InstalledPack:
    """The insurance pack with a fixture advice block. The real wording is Zee's, reviewed by
    Siew, so it is built here and never written into pack.yaml."""
    raw = yaml.safe_load((ROOT / "packs/insurance_agent/pack.yaml").read_text(encoding="utf-8"))
    raw["answering"] = {
        "categories": {
            "match_field": "product_name",
            "noun": "policies",
            "rules": [
                {
                    "id": "hospital_cash",
                    "label": "hospital cash plan",
                    "printed": ["hospital cash"],
                },
                {
                    "id": "critical_illness",
                    "label": "critical illness plan",
                    "printed": ["critical illness"],
                },
            ],
        }
    }
    raw["grounding"] = {
        "corpus": None,
        "top_k": 0,
        "values": [
            {
                "key": "ci_multiple",
                "unit": "multiple",
                "description": "Multiple of annual income a household is guided to hold as cover",
                "qualifiers": ["age_band"],
            },
            {
                "key": "annual_premium",
                "unit": "money",
                "description": "A published annual premium for a named plan and age band",
                "qualifiers": ["product", "insurer", "age_band"],
            },
        ],
    }
    raw["advice"] = {
        "consent_version": "1.0.0",
        "consent_text": (
            "I agree that Parrot may calculate advice from my household's documents and the "
            "published guidance it holds."
        ),
        "disclaimer": (
            "A calculation from your own documents and published guidance, not a recommendation "
            "from a licensed adviser."
        ),
        "product_disclosure": "Where a product is named, only what both sides print is compared.",
        "shapes": [GAP_SHAPE],
    }
    return InstalledPack(PackManifest.model_validate(raw))


def figures_of(result: Calculation) -> dict[str, Decimal]:
    return {figure.name: figure.value for figure in result.figures}


def assert_nothing_negative(result: Calculation) -> None:
    """No figure below zero, and no "-SGD" in anything a sentence or the gate could read.

    The gate's number check ignores signs, so a negative figure beside its role word would let
    "a gap of SGD 48,800.00" through when the holding is SGD 48,800.00 above the guideline.
    """
    assert all(figure.value >= 0 for figure in result.figures)
    printed = [
        result.verdict_text,
        *(figure.text for figure in result.figures),
        *(passage.text for passage in passages_for(result)),
    ]
    assert not [text for text in printed if "-SGD" in text]


# ------------------------------------------------------------------------------ formatting


def test_money_is_printed_the_way_a_sentence_states_it() -> None:
    assert money(Decimal("188000")) == "SGD 188,000.00"
    assert money(Decimal("333.5")) == "SGD 333.50"
    assert money(Decimal("-48800")) == "-SGD 48,800.00"
    assert advice.number(Decimal("15300")) == "15,300"
    assert advice.number(Decimal("11.50")) == "11.5"


def test_the_advice_module_manifest_loads() -> None:
    manifest = module_loader.manifest("advice")
    assert manifest.id == "advice"
    assert manifest.reads == ["facts", "grounding_values"]
    assert manifest.config_schema == "core.contracts:AdviceShape"


# ------------------------------------------------------------------------------------ gap


def _gap_basis(held: list[FactRow], *, income: bool = True, rule: bool = True) -> Basis:
    return basis(
        GAP,
        {
            "income": (
                [fact(1, "payslip", "9400", key="gross_salary", doc_type="payslip")]
                if income
                else []
            ),
            "held": held,
        },
        {"multiple": [published(7, "ci_multiple", "4", unit="multiple")] if rule else []},
    )


def test_a_gap_is_the_guideline_less_what_is_held() -> None:
    result = calculate(_gap_basis([fact(2, "ci-a", "200000")]))

    assert isinstance(result, Calculation)
    figures = figures_of(result)
    assert figures["annual income"] == Decimal("112800.00")
    assert figures["target"] == Decimal("451200.00")
    assert figures["held"] == Decimal("200000.00")
    assert figures["gap"] == Decimal("251200.00")
    assert result.verdict == "short"
    assert "SGD 251,200.00" in result.verdict_text
    assert result.verdict_text.startswith("Critical illness cover gap for Marcus Lim Jun Wei:")

    assert [item.ref for item in result.inputs] == ["fact:1", "fact:2", "rule:7"]
    income, _held, multiple = result.inputs
    assert income.citation == "payslip.pdf, page 1"
    assert multiple.citation == "Publisher, Guide title, 26 September 2023"
    assert multiple.url == "https://example.gov.sg/guide"
    texts = [passage.text for passage in passages_for(result)]
    assert texts[:3] == [
        "gross salary: SGD 9,400.00",
        "sum insured: SGD 200,000.00",
        "ci multiple: 4 times",
    ]
    # How the year's income was made is not printed anywhere a sentence's number could match.
    assert "annual income: SGD 112,800.00" in texts[-1]
    for text in texts:
        assert "\N{MULTIPLICATION SIGN}" not in text
        assert "monthly" not in text


def test_holding_more_than_the_guideline_is_stated_as_above_it_never_as_a_negative_gap() -> None:
    result = calculate(_gap_basis([fact(2, "ci-a", "500000")]))

    assert isinstance(result, Calculation)
    figures = figures_of(result)
    assert "gap" not in figures
    assert figures["above"] == Decimal("48800.00")
    assert result.verdict == "meets"
    assert result.verdict_text.endswith(
        "SGD 500,000.00 is held, which meets the guideline and is SGD 48,800.00 above it."
    )
    assert_nothing_negative(result)


def test_a_guideline_published_per_age_band_is_not_guessed() -> None:
    held = [fact(2, "ci-a", "200000")]
    by_band = replace(
        _gap_basis(held),
        rules={
            "multiple": [
                published(7, "ci_multiple", "4", unit="multiple", age_band="35-44"),
                published(8, "ci_multiple", "3", unit="multiple", age_band="45-54"),
            ]
        },
        qualifiers={"ci_multiple": ("age_band",)},
    )

    result = calculate(by_band)
    assert isinstance(result, Missing)
    assert result.items == (MULTIPLE_MISSING, "which age band applies")

    # Two current values for the same band settle nothing to ask: the newest is read.
    same_band = replace(
        by_band,
        rules={
            "multiple": [
                published(7, "ci_multiple", "4", unit="multiple", age_band="35-44"),
                published(6, "ci_multiple", "3", unit="multiple", age_band="35-44"),
            ]
        },
    )
    newest = calculate(same_band)
    assert isinstance(newest, Calculation)
    assert "rule:7" in {item.ref for item in newest.inputs}
    assert figures_of(newest)["target"] == Decimal("451200.00")


def test_a_missing_income_is_named_in_the_packs_words() -> None:
    result = calculate(_gap_basis([fact(2, "ci-a", "200000")], income=False))

    assert isinstance(result, Missing)
    assert result.items == (INCOME_MISSING,)


def test_a_missing_rule_is_named_and_every_missing_input_is_named_in_order() -> None:
    only_rule = calculate(_gap_basis([fact(2, "ci-a", "200000")], rule=False))
    both = calculate(_gap_basis([fact(2, "ci-a", "200000")], income=False, rule=False))

    assert isinstance(only_rule, Missing)
    assert only_rule.items == (MULTIPLE_MISSING,)
    assert isinstance(both, Missing)
    assert both.items == (INCOME_MISSING, MULTIPLE_MISSING)


def test_a_fact_with_no_number_is_not_read_as_zero() -> None:
    blank = fact(1, "payslip", None, key="gross_salary", field_type="string")
    result = calculate(
        basis(
            GAP,
            {"income": [blank], "held": [fact(2, "ci-a", "200000")]},
            {"multiple": [published(7, "ci_multiple", "4", unit="multiple")]},
        )
    )
    assert isinstance(result, Missing)
    assert result.items == (INCOME_MISSING,)


def test_a_sum_counts_the_latest_fact_of_each_document_once() -> None:
    # Newest first, as FACTS_FOR orders them: ci-a was extracted twice.
    held = [fact(3, "ci-a", "200000"), fact(2, "ci-a", "150000"), fact(4, "ci-b", "50000")]

    assert [row.fact_id for row in take(held, "sum")] == [3, 4]
    assert [row.fact_id for row in take(held, "latest")] == [3]
    result = calculate(_gap_basis(held))
    assert isinstance(result, Calculation)
    assert figures_of(result)["held"] == Decimal("250000.00")
    assert "fact:2" not in {item.ref for item in result.inputs}


# ------------------------------------------------------------------- the adviser, over a fake


def _facts_tuple(
    fact_id: int, document: str, key: str, value: str, doc_type: str
) -> tuple[Any, ...]:
    return (
        fact_id,
        document,
        f"{document}.pdf",
        doc_type,
        1,
        key,
        Decimal(value),
        None,
        None,
        MARCUS,
        INGESTED,
    )


def test_the_category_filter_leaves_a_hospital_cash_plan_out_of_critical_illness_cover() -> None:
    pack = advised_pack()
    conn = FakeConn(
        [(1, "Marcus", MARCUS)],
        [_facts_tuple(1, "payslip", "gross_salary", "9400", "payslip")],
        [
            _facts_tuple(2, "ci-a", "sum_insured", "200000", "policy_schedule"),
            _facts_tuple(3, "hc-b", "sum_insured", "100000", "policy_schedule"),
        ],
        [("hc-b", "HealthShield Hospital Cash Plan"), ("ci-a", "CritiCare Critical Illness Plan")],
        [
            (
                7,
                "ci_multiple",
                "multiple",
                Decimal("4"),
                None,
                {"age_band": "35-44"},
                "4 times annual income",
                None,
                "Guide title",
                "Publisher",
                "https://example.gov.sg/guide",
                None,
                date(2026, 9, 1),
            )
        ],
    )

    result = ModuleAdviser(conn).calculate(
        pack, GAP, person_ids=frozenset({1}), subject="Marcus", today=TODAY
    )

    assert isinstance(result, Calculation)
    assert figures_of(result)["held"] == Decimal("200000.00")
    assert "fact:3" not in {item.ref for item in result.inputs}
    assert result.inputs[0].value_text == "SGD 9,400.00", "the iras_tax field type is money"
    assert result.inputs[-1].citation == "Publisher, Guide title, 1 September 2026"

    executed = conn.cursor_obj.executed
    assert executed[0][1] == {"ids": [1]}
    assert executed[1][1]["pack"] == "core", "every fact is read as the core's (ADR 0017)"
    assert executed[1][1]["names"] == ["marcus", "marcus lim jun wei"]
    assert executed[2][1]["pack"] == "core"
    assert executed[3][1] == {"ids": ["ci-a", "hc-b"], "match_field": "product_name"}
    assert executed[4][1]["oldest"] == TODAY - timedelta(days=365), "a multiple is a rule"


def test_an_unanswerable_shape_reads_nothing_more() -> None:
    conn = FakeConn([(1, "Marcus", None)], [], [], [])
    result = ModuleAdviser(conn).calculate(
        advised_pack(), GAP, person_ids=frozenset({1}), subject="Marcus", today=TODAY
    )

    assert isinstance(result, Missing)
    assert result.items == (INCOME_MISSING, HELD_MISSING, MULTIPLE_MISSING)
    assert len(conn.cursor_obj.executed) == 4, "no product names are read for no facts"


@pytest.mark.parametrize("people", [frozenset(), frozenset({1, 2})])
def test_advice_is_calculated_for_exactly_one_person(people: frozenset[int]) -> None:
    conn = FakeConn()
    with pytest.raises(ValueError, match="exactly one person"):
        ModuleAdviser(conn).calculate(
            advised_pack(), GAP, person_ids=people, subject="Marcus", today=TODAY
        )
    assert conn.cursor_obj.executed == [], "nothing is read for a question the graph must ask"


def test_a_price_goes_stale_sooner_than_a_rule() -> None:
    conn = FakeConn([])
    values_for(conn, advised_pack(), "annual_premium", TODAY)
    assert conn.cursor_obj.executed[0][1]["oldest"] == TODAY - timedelta(days=120)


# --------------------------------------------------------------------------- the other sums


ROOM = shape(
    "remaining_room",
    [
        {
            "role": "used",
            "doc_types": ["srs_statement"],
            "field": "contributions_ytd",
            "missing": "Your SRS statement for this year.",
        }
    ],
    rules=[{"role": "cap", "key": "srs_cap", "missing": CAP_MISSING}],
    label="SRS contribution room",
)


def _used(value: str) -> list[FactRow]:
    return [fact(1, "srs", value, key="contributions_ytd", doc_type="srs_statement")]


def test_a_cap_published_for_one_age_band_beside_one_for_every_age_is_not_guessed() -> None:
    """A row that carries no age band counts as its own value, not as a match for every band."""
    result = calculate(
        basis(
            ROOM,
            {"used": _used("12400")},
            {
                "cap": [
                    published(8, "srs_cap", "15300"),
                    published(9, "srs_cap", "35700", age_band="55-64"),
                ]
            },
            qualifiers={"srs_cap": ("age_band",)},
        )
    )
    assert isinstance(result, Missing)
    assert result.items == (CAP_MISSING, "which age band applies")


def test_a_total_declared_per_month_is_refused_rather_than_read_once() -> None:
    """The contract refuses it on load; a shape built without a manifest is refused here."""
    monthly = shape(
        "remaining_room",
        [
            {
                "role": "used",
                "doc_types": ["srs_statement"],
                "field": "contributions_ytd",
                "per": "month",
                "missing": "Your SRS statement for this year.",
            }
        ],
        rules=[{"role": "cap", "key": "srs_cap", "missing": CAP_MISSING}],
    )
    with pytest.raises(ValueError, match="reads 'used' per month, which only income may be"):
        calculate(
            basis(monthly, {"used": _used("1000")}, {"cap": [published(8, "srs_cap", "15300")]})
        )


@pytest.mark.parametrize(
    ("used", "room", "verdict"),
    [("12400", Decimal("2900.00"), "room_left"), ("16000", Decimal("0.00"), "no_room")],
)
def test_room_is_the_cap_less_what_is_used_and_never_below_zero(
    used: str, room: Decimal, verdict: str
) -> None:
    result = calculate(
        basis(
            ROOM,
            {"used": [fact(1, "srs", used, key="contributions_ytd", doc_type="srs_statement")]},
            {"cap": [published(8, "srs_cap", "15300")]},
        )
    )

    assert isinstance(result, Calculation)
    assert figures_of(result)["room"] == room
    assert result.verdict == verdict
    assert f"the room left is {money(room)}." in result.verdict_text


def _keep_shape(
    value_missing: str = VALUE_MISSING, paid_missing: str = PAID_MISSING
) -> AdviceShape:
    return shape(
        "keep_or_surrender",
        [
            {
                "role": "value_now",
                "doc_types": ["policy_anniversary_statement"],
                "field": "surrender_value",
                "missing": value_missing,
            },
            {
                "role": "paid_to_date",
                "doc_types": ["policy_anniversary_statement"],
                "field": "premiums_paid_to_date",
                "missing": paid_missing,
            },
        ],
        label="whole life plan",
    )


KEEP = _keep_shape()


def _value_now(fact_id: int, document: str, value: str, **changes: Any) -> FactRow:
    return replace(fact(fact_id, document, value, key="surrender_value"), **changes)


def _paid(fact_id: int, document: str, value: str, **changes: Any) -> FactRow:
    return replace(fact(fact_id, document, value, key="premiums_paid_to_date"), **changes)


def test_surrendering_below_what_was_paid_states_both_figures_and_the_difference() -> None:
    result = calculate(
        basis(
            KEEP,
            {
                "value_now": [_value_now(1, "stmt", "24800")],
                "paid_to_date": [_paid(2, "stmt", "39600")],
            },
        )
    )

    assert isinstance(result, Calculation)
    assert figures_of(result)["loss"] == Decimal("14800.00")
    assert result.verdict == "loses"
    for printed in ("SGD 39,600.00", "SGD 24,800.00", "SGD 14,800.00"):
        assert printed in result.verdict_text
    assert not any(word in result.verdict_text.lower() for word in ("should", "recommend", "keep"))


def test_a_value_above_what_was_paid_is_a_gain_never_a_negative_loss() -> None:
    result = calculate(
        basis(
            KEEP,
            {
                "value_now": [_value_now(1, "stmt", "39600")],
                "paid_to_date": [_paid(2, "stmt", "24800")],
            },
        )
    )

    assert isinstance(result, Calculation)
    figures = figures_of(result)
    assert "loss" not in figures
    assert figures["gain"] == Decimal("14800.00")
    assert result.verdict == "gains"
    assert result.verdict_text.endswith("a gain of SGD 14,800.00 more than has been paid.")
    assert_nothing_negative(result)


def test_both_surrender_figures_come_from_the_newest_statement_that_prints_both() -> None:
    later = INGESTED + timedelta(days=300)
    # Newest document first, as FACTS_FOR orders them: this year's statement prints only the
    # value now, so last year's, which prints both, is the one compared.
    result = calculate(
        basis(
            KEEP,
            {
                "value_now": [
                    _value_now(3, "stmt-2026", "26000", when=later),
                    _value_now(1, "stmt-2025", "24800"),
                ],
                "paid_to_date": [_paid(2, "stmt-2025", "39600")],
            },
        )
    )

    assert isinstance(result, Calculation)
    assert figures_of(result)["loss"] == Decimal("14800.00")
    assert [item.ref for item in result.inputs] == ["fact:2", "fact:1"]
    assert "SGD 26,000.00" not in result.verdict_text


def test_no_statement_printing_both_surrender_figures_names_what_the_newest_leaves_out() -> None:
    later = INGESTED + timedelta(days=300)
    result = calculate(
        basis(
            KEEP,
            {
                "value_now": [_value_now(3, "stmt-2026", "26000", when=later)],
                "paid_to_date": [_paid(2, "stmt-2025", "39600")],
            },
        )
    )

    assert isinstance(result, Missing)
    assert result.items == (PAID_MISSING,)


def test_two_inputs_worded_alike_are_asked_for_once() -> None:
    statement = "Your latest anniversary statement."
    result = calculate(
        basis(_keep_shape(statement, statement), {"value_now": [], "paid_to_date": []})
    )

    assert isinstance(result, Missing)
    assert result.items == (statement,)


SAVING = shape(
    "estimate_saving",
    [
        {
            "role": "income",
            "doc_types": ["notice_of_assessment"],
            "field": "assessable_income",
            "missing": INCOME_MISSING,
        },
        {
            "role": "amount",
            "doc_types": ["srs_statement"],
            "field": "contributions_ytd",
            "missing": "Your SRS statement for this year.",
        },
    ],
    rules=[{"role": "rate", "key": "tax_rate", "missing": RATE_MISSING}],
    label="SRS tax saving",
    estimate=True,
)


def _saving_basis(income: str, bands: list[ValueRow]) -> Basis:
    return basis(
        SAVING,
        {
            "income": [
                fact(1, "noa", income, key="assessable_income", doc_type="notice_of_assessment")
            ],
            "amount": [fact(2, "srs", "2900", key="contributions_ytd", doc_type="srs_statement")],
        },
        {"rate": bands},
        qualifiers={"tax_rate": ("band_lower", "band_upper", "assessment_year")},
    )


def test_an_estimated_saving_reads_the_rate_band_the_income_falls_in() -> None:
    bands = [
        published(20, "tax_rate", "7", unit="rate", band_lower=40000, band_upper=80000),
        published(21, "tax_rate", "11.5", unit="rate", band_lower="80000", band_upper="120000"),
        published(22, "tax_rate", "15", unit="rate", band_lower=120000, band_upper=160000),
    ]

    def run(income: str) -> Calculation | Missing:
        return calculate(_saving_basis(income, bands))

    result = run("112800")
    assert isinstance(result, Calculation)
    assert figures_of(result)["saving"] == Decimal("333.50")
    assert (result.verdict, result.estimate) == ("estimate", True)
    assert result.verdict_text.startswith("Estimated:")
    assert "11.5%" in result.verdict_text and "SGD 333.50" in result.verdict_text
    assert [item.ref for item in result.inputs] == ["fact:1", "fact:2", "rule:21"]

    outside = run("500000")
    assert isinstance(outside, Missing)
    assert outside.items == (RATE_MISSING,)


def test_a_rate_published_for_two_years_in_the_same_band_is_not_guessed() -> None:
    def rate(value_id: int, number: str, year: str, lower: int, upper: int) -> ValueRow:
        return published(
            value_id,
            "tax_rate",
            number,
            unit="rate",
            band_lower=lower,
            band_upper=upper,
            assessment_year=year,
        )

    two_years = calculate(
        _saving_basis(
            "112800",
            [rate(21, "11.5", "2026", 80000, 120000), rate(23, "12", "2025", 80000, 120000)],
        )
    )
    assert isinstance(two_years, Missing)
    assert two_years.items == (RATE_MISSING, "which assessment year applies")

    # A different year in a band the income is not in is not a choice to make.
    one_year = calculate(
        _saving_basis(
            "112800",
            [rate(21, "11.5", "2026", 80000, 120000), rate(22, "15", "2025", 120000, 160000)],
        )
    )
    assert isinstance(one_year, Calculation)
    assert figures_of(one_year)["saving"] == Decimal("333.50")


# ------------------------------------------------------------------------------ comparisons


OWN = shape(
    "compare_own",
    [
        {
            "role": "items",
            "doc_types": ["policy_schedule"],
            "field": "product_name",
            "take": "each",
            "missing": "The schedule of each hospital plan you hold.",
        }
    ],
    compare_fields=["deductible", "premium_payable"],
    order_by="deductible",
)


def _names(*documents: str) -> list[FactRow]:
    return [
        fact(i, doc, f"Plan {doc}", key="product_name", field_type="string")
        for i, doc in enumerate(documents, start=1)
    ]


def test_own_plans_are_compared_only_on_the_fields_both_print() -> None:
    result = calculate(
        basis(
            OWN,
            {"items": _names("a", "b")},
            compared={
                "deductible": [
                    fact(10, "a", "3000", key="deductible"),
                    fact(11, "b", "1500", key="deductible"),
                ],
                "premium_payable": [fact(12, "a", "400", key="premium_payable")],
            },
        )
    )

    assert isinstance(result, Calculation)
    assert result.rows == (
        ("document", "deductible"),
        ("b.pdf", "SGD 1,500.00"),
        ("a.pdf", "SGD 3,000.00"),
    )
    assert result.verdict == "ranked"
    assert result.verdict_text == (
        "Ranked by deductible (lowest first), only on fields both print: b.pdf then a.pdf."
    )
    assert {item.ref for item in result.inputs} == {"fact:10", "fact:11"}


def test_own_plans_sharing_no_field_are_not_compared() -> None:
    result = calculate(
        basis(
            OWN,
            {"items": _names("a", "b")},
            compared={
                "deductible": [fact(10, "a", "3000", key="deductible")],
                "premium_payable": [fact(12, "b", "400", key="premium_payable")],
            },
        )
    )
    assert isinstance(result, Missing)
    assert result.items == (NOTHING_SHARED,)


def test_one_plan_is_not_a_comparison() -> None:
    result = calculate(
        basis(
            OWN,
            {"items": _names("a")},
            compared={"deductible": [fact(10, "a", "3000", key="deductible")]},
        )
    )
    assert isinstance(result, Missing)
    assert result.items == (FEWER_THAN_TWO,)


MARKET = shape(
    "compare_market",
    [
        {
            "role": "held",
            "doc_types": ["policy_schedule"],
            "field": "product_name",
            "missing": HELD_PLAN_MISSING,
        }
    ],
    rules=[{"role": "market", "key": "annual_premium", "missing": MARKET_MISSING}],
    compare_fields=["annual_premium", "ward_class"],
    order_by="annual_premium",
)


def _held() -> list[FactRow]:
    return [fact(1, "h", "MyShield Standard", key="product_name", field_type="string")]


def _premium(
    value_id: int, number: str, product: str, insurer: str | None, age_band: str = "35-44"
) -> ValueRow:
    qualifiers = {"product": product, "age_band": age_band}
    if insurer is not None:
        qualifiers["insurer"] = insurer
    return published(value_id, "annual_premium", number, **qualifiers)


def _ward(value_id: int, ward: str, product: str, insurer: str) -> ValueRow:
    return published(
        value_id, "ward_class", None, unit="count", text=ward, product=product, insurer=insurer
    )


def test_a_market_product_sharing_no_field_is_left_out_and_the_rest_are_ranked() -> None:
    premiums = [
        _premium(30, "900", "Shield A", "Insurer X"),
        _premium(31, "1500", "Shield B", "Insurer Y"),
        _premium(32, "700", "Shield Z", None),  # no insurer: cannot be told apart, left out
    ]
    result = calculate(
        basis(
            MARKET,
            {"held": _held()},
            {"market": premiums},
            compared={
                "annual_premium": [fact(2, "h", "1200", key="annual_premium")],
                "ward_class": [],
            },
            market={
                "annual_premium": premiums,
                "ward_class": [_ward(33, "B1", "Shield C", "Insurer Z")],
            },
        )
    )

    assert isinstance(result, Calculation)
    assert result.rows == (
        ("name", "annual premium"),
        ("Shield A (Insurer X)", "SGD 900.00"),
        ("h.pdf (held)", "SGD 1,200.00"),
        ("Shield B (Insurer Y)", "SGD 1,500.00"),
    )
    assert result.names_product is True
    assert result.verdict == "ranked"
    assert "Shield C" not in result.verdict_text
    assert {item.ref for item in result.inputs} == {"fact:1", "fact:2", "rule:30", "rule:31"}
    assert "annual premium for Shield A (Insurer X)" in {item.label for item in result.inputs}


def test_a_market_product_without_the_ordering_field_is_listed_after_the_ranked_ones() -> None:
    premiums = [_premium(30, "900", "Shield A", "Insurer X")]
    result = calculate(
        basis(
            MARKET,
            {"held": _held()},
            {"market": premiums},
            compared={
                "annual_premium": [fact(2, "h", "1200", key="annual_premium")],
                "ward_class": [fact(3, "h", "B1", key="ward_class", field_type="string")],
            },
            market={
                "annual_premium": premiums,
                "ward_class": [
                    _ward(34, "A", "Shield E", "Insurer V"),
                    _ward(35, "B1", "Shield D", "Insurer W"),
                ],
            },
        )
    )

    assert isinstance(result, Calculation)
    assert [row[0] for row in result.rows] == [
        "name",
        "Shield A (Insurer X)",
        "h.pdf (held)",
        "Shield D (Insurer W)",
        "Shield E (Insurer V)",
    ]
    assert result.rows[3] == ("Shield D (Insurer W)", "", "B1")
    assert result.verdict_text.endswith(
        "Listed without annual premium: Shield D (Insurer W), Shield E (Insurer V)."
    )


def _held_ward() -> dict[str, list[FactRow]]:
    """The held plan prints its ward class and no premium."""
    return {
        "annual_premium": [],
        "ward_class": [fact(3, "h", "B1", key="ward_class", field_type="string")],
    }


def test_no_market_product_sharing_a_field_withholds_in_the_rules_words() -> None:
    premiums = [_premium(30, "900", "Shield A", "Insurer X")]
    result = calculate(
        basis(
            MARKET,
            {"held": _held()},
            {"market": premiums},
            compared=_held_ward(),
            market={"annual_premium": premiums},
        )
    )
    assert isinstance(result, Missing)
    assert result.items == (MARKET_MISSING,)


def test_a_held_plan_printing_no_compared_field_withholds_in_the_held_facts_words() -> None:
    premiums = [_premium(30, "900", "Shield A", "Insurer X")]
    result = calculate(
        basis(
            MARKET,
            {"held": _held()},
            {"market": premiums},
            compared={},
            market={"annual_premium": premiums},
        )
    )
    assert isinstance(result, Missing)
    assert result.items == (HELD_PLAN_MISSING,)


def test_a_market_comparison_with_nothing_to_rank_by_is_withheld_naming_the_ordering_field() -> (
    None
):
    premiums = [_premium(30, "900", "Shield A", "Insurer X")]
    result = calculate(
        basis(
            MARKET,
            {"held": _held()},
            {"market": premiums},
            compared=_held_ward(),
            market={
                "annual_premium": premiums,
                "ward_class": [_ward(35, "B1", "Shield D", "Insurer W")],
            },
        )
    )
    assert isinstance(result, Missing)
    assert result.items == ("annual premium printed on every one compared",)


def test_a_market_premium_published_per_age_band_is_not_guessed() -> None:
    premiums = [
        _premium(30, "900", "Shield A", "Insurer X", age_band="35-44"),
        _premium(36, "1400", "Shield A", "Insurer X", age_band="45-54"),
    ]
    result = calculate(
        basis(
            MARKET,
            {"held": _held()},
            {"market": premiums},
            compared={
                "annual_premium": [fact(2, "h", "1200", key="annual_premium")],
                "ward_class": [],
            },
            market={"annual_premium": premiums},
            qualifiers={"annual_premium": ("product", "insurer", "age_band")},
        )
    )
    assert isinstance(result, Missing)
    assert result.items == (MARKET_MISSING, "which age band applies")


# ------------------------------------------------------------------------ against Postgres


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
            cur.execute("SELECT to_regclass('public.grounding_values')")
            row = cur.fetchone()
            if row is None or row[0] is None:
                pytest.skip("the 0003_advice migration has not been applied")
            # Empty copies in pg_temp, which the session searches before public, so the module's
            # unqualified queries see only the rows written below.
            cur.execute("CREATE TEMP TABLE documents (LIKE public.documents INCLUDING ALL)")
            cur.execute("CREATE TEMP TABLE facts (LIKE public.facts INCLUDING ALL)")
            cur.execute("CREATE TEMP TABLE people (LIKE public.people INCLUDING ALL)")
            cur.execute(
                "CREATE TEMP TABLE person_aliases (LIKE public.person_aliases INCLUDING ALL)"
            )
            cur.execute(
                "CREATE TEMP TABLE grounding_sources (LIKE public.grounding_sources INCLUDING ALL)"
            )
            cur.execute(
                "CREATE TEMP TABLE grounding_values (LIKE public.grounding_values INCLUDING ALL)"
            )
        yield connection
    finally:
        connection.rollback()  # nothing this test did survives, the temporary tables included
        connection.close()


def _source(
    cur: Any,
    file: str,
    *,
    reviewed: bool,
    review_by: date,
    retrieved_on: date,
    pack: str = "insurance_agent",
) -> int:
    cur.execute(
        "INSERT INTO grounding_sources (pack_id, corpus_id, file, title, publisher,"
        " publisher_kind, url, retrieved_on, applies_to, review_by, reviewed_by, reviewed_on,"
        " sha256)"
        " VALUES (%(pack)s, 'guides', %(file)s, 'Guide title', 'Publisher', 'regulator',"
        " 'https://example.gov.sg/guide', %(retrieved_on)s, 'Singapore households',"
        " %(review_by)s, %(reviewer)s, %(reviewed_on)s, %(sha)s)"
        " RETURNING id",
        {
            "pack": pack,
            "file": file,
            "retrieved_on": retrieved_on,
            "review_by": review_by,
            "reviewer": "Siew" if reviewed else None,
            "reviewed_on": TODAY - timedelta(days=10) if reviewed else None,
            "sha": hashlib.sha256(file.encode()).digest(),
        },
    )
    (source_id,) = cur.fetchone()
    return int(source_id)


def _value(
    cur: Any,
    source_id: int,
    key: str,
    *,
    status: str = "approved",
    unit: str = "multiple",
    effective_from: date | None = None,
    effective_to: date | None = None,
    pack: str = "insurance_agent",
) -> int:
    cur.execute(
        "INSERT INTO grounding_values (source_id, pack_id, key, unit, value_num, qualifiers,"
        " passage, extracted_by, status, reviewed_by, reviewed_on, effective_from, effective_to)"
        " VALUES (%(source_id)s, %(pack)s, %(key)s, %(unit)s, 4, %(qualifiers)s::jsonb,"
        " 'four times annual income', 'model', %(status)s, %(reviewer)s, %(reviewed_on)s,"
        " %(effective_from)s, %(effective_to)s)"
        " RETURNING id",
        {
            "source_id": source_id,
            "pack": pack,
            "effective_from": effective_from,
            "key": key,
            "unit": unit,
            "qualifiers": json.dumps({"product": "Shield A", "insurer": "Insurer X"}),
            "status": status,
            "reviewer": None if status == "pending" else "Siew",
            "reviewed_on": None if status == "pending" else TODAY,
            "effective_to": effective_to,
        },
    )
    (value_id,) = cur.fetchone()
    return int(value_id)


def test_only_approved_reviewed_current_and_recent_values_are_read(db: Any) -> None:
    later = TODAY + timedelta(days=100)
    with db.cursor() as cur:
        fresh = _source(
            cur, "fresh.md", reviewed=True, review_by=later, retrieved_on=TODAY - timedelta(days=30)
        )
        unreviewed = _source(
            cur, "unreviewed.md", reviewed=False, review_by=later, retrieved_on=TODAY
        )
        expired = _source(
            cur,
            "expired.md",
            reviewed=True,
            review_by=TODAY - timedelta(days=1),
            retrieved_on=TODAY,
        )
        aged = _source(
            cur, "aged.md", reviewed=True, review_by=later, retrieved_on=TODAY - timedelta(days=200)
        )
        due_today = _source(
            cur, "due.md", reviewed=True, review_by=TODAY, retrieved_on=TODAY - timedelta(days=60)
        )
        other_pack = _source(
            cur, "tax.md", reviewed=True, review_by=later, retrieved_on=TODAY, pack="iras_tax"
        )

        rule_fresh = _value(cur, fresh, "ci_multiple")
        _value(cur, fresh, "ci_multiple", status="pending")
        _value(cur, fresh, "ci_multiple", status="rejected")
        _value(cur, unreviewed, "ci_multiple")
        _value(cur, expired, "ci_multiple")
        _value(cur, fresh, "ci_multiple", effective_to=TODAY - timedelta(days=1))
        _value(cur, fresh, "ci_multiple", effective_from=TODAY + timedelta(days=1))
        _value(cur, other_pack, "ci_multiple", pack="iras_tax")
        rule_due = _value(cur, due_today, "ci_multiple")  # review_by today is still in date
        rule_aged = _value(cur, aged, "ci_multiple")  # 200 days is within a rule's 365

        price_fresh = _value(cur, fresh, "annual_premium", unit="money")
        _value(cur, aged, "annual_premium", unit="money")  # 200 days is past a price's 120

    pack = advised_pack()
    rules = values_for(db, pack, "ci_multiple", TODAY)
    prices = values_for(db, pack, "annual_premium", TODAY)

    # Newest retrieval first: 30, 60 and 200 days ago.
    assert [row.value_id for row in rules] == [rule_fresh, rule_due, rule_aged]
    assert [row.value_id for row in prices] == [price_fresh]
    assert prices[0].qualifiers == {"product": "Shield A", "insurer": "Insurer X"}
    assert prices[0].value_num == Decimal(4)


def _document(
    cur: Any,
    name: str,
    *,
    status: str = "indexed",
    doc_type: str = "policy_schedule",
    ingested_at: datetime = INGESTED,
) -> Any:
    cur.execute(
        "INSERT INTO documents (sha256, source_channel, original_name, mime, doc_type, pack_id,"
        " status, synthetic, ingested_at)"
        " VALUES (%s, 'folder', %s, 'application/pdf', %s, 'insurance_agent', %s, true, %s)"
        " RETURNING id",
        (hashlib.sha256(name.encode()).digest(), name, doc_type, status, ingested_at),
    )
    (document_id,) = cur.fetchone()
    return document_id


def _sum_insured(cur: Any, document_id: Any, subject: str | None) -> None:
    cur.execute(
        "INSERT INTO facts (document_id, page, pack_id, pack_version, key, subject, value_num,"
        " confidence)"
        " VALUES (%s, 1, 'insurance_agent', '1.0.0', 'sum_insured', %s, 200000, 1.0)",
        (document_id, subject),
    )


def test_facts_are_read_only_under_a_persons_confirmed_names(db: Any) -> None:
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO people (display_name, relation, is_owner)"
            " VALUES ('Marcus', 'self', true) RETURNING id"
        )
        (marcus,) = cur.fetchone()
        cur.execute(
            "INSERT INTO people (display_name, relation) VALUES ('Rachel', 'partner') RETURNING id"
        )
        (rachel,) = cur.fetchone()
        cur.executemany(
            "INSERT INTO person_aliases (person_id, alias, source, confirmed)"
            " VALUES (%s, %s, %s, %s)",
            [
                (marcus, "MARCUS LIM JUN WEI", "setup", True),
                (marcus, "M. Lim", "model", False),  # proposed, never confirmed
                (rachel, "Rachel Ng Hui Shan", "setup", True),
            ],
        )
        _sum_insured(cur, _document(cur, "marcus.pdf"), f" {MARCUS} ")
        # Ingested a year earlier but inserted later, so its fact id is higher: only
        # `ingested_at` can put it second.
        older = _document(cur, "marcus-2025.pdf", ingested_at=INGESTED - timedelta(days=365))
        _sum_insured(cur, older, MARCUS)
        _sum_insured(cur, _document(cur, "guessed.pdf"), "M. Lim")
        _sum_insured(cur, _document(cur, "rachel.pdf"), "Rachel Ng Hui Shan")
        _sum_insured(cur, _document(cur, "quarantined.pdf", status="quarantined"), MARCUS)
        _sum_insured(cur, _document(cur, "nobody.pdf"), None)
        _sum_insured(cur, _document(cur, "renewal.pdf", doc_type="renewal_notice"), MARCUS)

    names = names_for(db, [marcus])
    rows = facts_for(
        db,
        "insurance_agent",
        ["policy_schedule"],
        "sum_insured",
        names,
        {("policy_schedule", "sum_insured"): "money"},
    )

    assert names == ["marcus", "marcus lim jun wei"]
    assert [row.name for row in rows] == ["marcus.pdf", "marcus-2025.pdf"]
    assert rows[0].value == Decimal(200000)
    assert rows[0].field_type == "money"
