"""Published values: the model reads a source, and code keeps only what the passage prints."""

from __future__ import annotations

import json
import logging
from datetime import date
from decimal import Decimal
from typing import Any

import pytest

from core.contracts import GroundingCorpus, GroundingDocument, ValueKey
from core.grounding.corpus import SourceText
from core.grounding.values import (
    SECTION_CHARS,
    SYSTEM,
    ExtractedValue,
    collapse,
    extract_values,
    number_tokens,
    parse_value,
    printed_in,
    split_sections,
)
from core.runtime.ollama import Generated, ModelUnavailable


class ScriptedClient:
    """Returns the replies the test wrote, in order, then an empty list of values."""

    def __init__(self, *replies: dict[str, Any] | Exception) -> None:
        self._replies = list(replies)
        self.systems: list[str] = []
        self.prompts: list[str] = []
        self.schemas: list[dict[str, Any]] = []

    def constrained(
        self,
        system: str,
        prompt: str,
        schema: dict[str, Any],
        *,
        images: list[str] | None = None,
        temperature: float = 0.0,
    ) -> Generated:
        self.systems.append(system)
        self.prompts.append(prompt)
        self.schemas.append(schema)
        reply: dict[str, Any] | Exception = (
            self._replies.pop(0) if self._replies else {"values": []}
        )
        if isinstance(reply, Exception):
            raise reply
        return Generated(json.dumps(reply), "fake", 1)


KEYS = [
    ValueKey(
        key="cover_multiple",
        unit="multiple",
        description="How many times annual income the cover should be",
    ),
    ValueKey(
        key="contribution_cap",
        unit="money",
        description="The most that may be contributed in a year",
        qualifiers=["residency"],
    ),
    ValueKey(key="rate_pct", unit="percent", description="The published rate, as a percentage"),
    ValueKey(key="term_years", unit="years", description="How many years the rule runs for"),
]

TEXT = """# Guidance

A rule of thumb is cover of 9 times annual income for a family.
The cap is 15,300 a year for residents.
The limit of 40,000 applies to everyone.
The rate is 3.5% this year, and the rule runs for 10 years.

| Residency | Cap |
|---|---|
| Residents | 15,300.00 |
| Others | 35,700 |
"""


def _source(text: str = TEXT) -> SourceText:
    document = GroundingDocument(
        file="guide.md",
        title="A published guide",
        publisher="A publisher",
        publisher_kind="government",
        url="https://example.org/guide",
        retrieved=date(2026, 9, 1),
        applies_to="everyone",
        review_by=date(2027, 9, 1),
    )
    corpus = GroundingCorpus(
        corpus_id="guides",
        applies_to="everyone",
        maintained_by="a maintainer",
        reviewed_by="a reviewer",
        documents=[document],
    )
    return SourceText(
        pack_id="a_pack",
        corpus=corpus,
        document=document,
        text=text,
        sha256=b"\x00" * 32,
        reviewed_by=None,
        reviewed_on=None,
    )


def _reply(*values: dict[str, Any]) -> dict[str, Any]:
    return {"values": [{"qualifiers": {}, **value} for value in values]}


def _run(*values: dict[str, Any], text: str = TEXT) -> list[ExtractedValue]:
    return extract_values(ScriptedClient(_reply(*values)), _source(text), KEYS)


# ------------------------------------------------------------------------------------ kept


def test_a_value_with_an_exact_passage_is_kept() -> None:
    [kept] = _run(
        {
            "key": "contribution_cap",
            "value": "15,300",
            "passage": "The cap is 15,300 a year for residents.",
            "qualifiers": {"residency": "resident"},
        }
    )
    assert kept == ExtractedValue(
        key="contribution_cap",
        unit="money",
        value_num=Decimal("15300"),
        value_text="15,300",
        qualifiers={"residency": "resident"},
        passage="The cap is 15,300 a year for residents.",
        confidence=0.9,
    )


TIMES = "\N{MULTIPLICATION SIGN}"


@pytest.mark.parametrize("value", ["9 times", "9x", "9 x", f"9{TIMES}", f"9 {TIMES}", "9", "9 X"])
def test_a_multiple_is_kept_in_the_forms_it_is_written(value: str) -> None:
    [kept] = _run(
        {
            "key": "cover_multiple",
            "value": value,
            "passage": "A rule of thumb is cover of 9 times annual income for a family.",
        }
    )
    assert kept.unit == "multiple"
    assert kept.value_num == Decimal("9")
    assert kept.value_text == value


@pytest.mark.parametrize("passage", ["| Others | 35,700 |", "Others 35,700", "Others | 35,700"])
def test_a_value_in_a_table_row_is_kept_with_or_without_its_pipes(passage: str) -> None:
    [kept] = _run({"key": "contribution_cap", "value": "35,700", "passage": passage})
    assert kept.value_num == Decimal("35700")


def test_a_number_matches_its_printed_decimal_form() -> None:
    [kept] = _run(
        {"key": "contribution_cap", "value": "15,300", "passage": "Residents | 15,300.00"}
    )
    assert kept.value_num == Decimal("15300")


def test_a_percentage_is_stored_as_the_number_not_the_fraction() -> None:
    [kept] = _run(
        {"key": "rate_pct", "value": "3.5%", "passage": "The rate is 3.5% this year, and the rule"}
    )
    assert kept.value_num == Decimal("3.5")


def test_a_passage_is_matched_across_line_breaks_and_repeated_spaces() -> None:
    [kept] = _run(
        {
            "key": "term_years",
            "value": "10",
            "passage": "The  rate is 3.5% this year,\n and the rule runs for 10 years.",
        }
    )
    assert kept.value_num == Decimal("10")


# ------------------------------------------------------------------------------------ dropped


def test_a_passage_not_in_the_text_is_dropped(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="core.grounding.values"):
        kept = _run(
            {"key": "contribution_cap", "value": "15,300", "passage": "The cap is 15,300 a month."}
        )
    assert kept == []
    assert "contribution_cap" in caplog.text
    assert "The cap is 15,300 a month." in caplog.text


def test_a_passage_differing_only_in_case_is_dropped() -> None:
    assert (
        _run({"key": "contribution_cap", "value": "15,300", "passage": "the cap is 15,300"}) == []
    )


def test_a_number_not_in_its_passage_is_dropped() -> None:
    kept = _run(
        {"key": "contribution_cap", "value": "35,700", "passage": "The cap is 15,300 a year"}
    )
    assert kept == []


def test_a_number_printed_inside_a_larger_number_is_dropped() -> None:
    kept = _run(
        {"key": "contribution_cap", "value": "4,000", "passage": "The limit of 40,000 applies"}
    )
    assert kept == []


def test_a_passage_cut_off_inside_a_number_is_dropped() -> None:
    assert _run({"key": "contribution_cap", "value": "40", "passage": "The limit of 40"}) == []


def test_an_undeclared_qualifier_is_dropped() -> None:
    kept = _run(
        {
            "key": "contribution_cap",
            "value": "15,300",
            "passage": "The cap is 15,300 a year for residents.",
            "qualifiers": {"residency": "resident", "age_band": "all"},
        }
    )
    assert kept == []


def test_an_unknown_key_is_dropped() -> None:
    kept = _run({"key": "made_up_key", "value": "15,300", "passage": "The cap is 15,300 a year"})
    assert kept == []


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("contribution_cap", "NaN"),
        ("contribution_cap", "1e4"),
        ("contribution_cap", "about 15,300"),
        ("term_years", "10.5"),
        ("cover_multiple", "9 times annual income"),
    ],
)
def test_a_value_that_does_not_parse_for_its_unit_is_dropped(key: str, value: str) -> None:
    passage = "The cap is 15,300 a year for residents. The limit of 40,000 applies to everyone."
    assert _run({"key": key, "value": value, "passage": passage}) == []


def test_an_empty_passage_is_dropped() -> None:
    assert _run({"key": "contribution_cap", "value": "15,300", "passage": "  "}) == []


def test_one_bad_value_does_not_drop_its_neighbours() -> None:
    kept = _run(
        {"key": "contribution_cap", "value": "4,000", "passage": "The limit of 40,000 applies"},
        {"key": "contribution_cap", "value": "40,000", "passage": "The limit of 40,000 applies"},
    )
    assert [value.value_num for value in kept] == [Decimal("40000")]


def test_a_model_that_is_down_returns_nothing() -> None:
    client = ScriptedClient(ModelUnavailable("the model did not answer"))
    assert extract_values(client, _source(), KEYS) == []


def test_no_keys_means_no_model_call() -> None:
    client = ScriptedClient()
    assert extract_values(client, _source(), []) == []
    assert client.prompts == []


# ------------------------------------------------------------------------------------ the call


def test_the_model_is_held_to_the_keys_and_told_what_each_one_is() -> None:
    client = ScriptedClient(_reply())
    extract_values(client, _source(), KEYS)

    [system], [prompt], [schema] = client.systems, client.prompts, client.schemas
    assert system == SYSTEM
    item = schema["properties"]["values"]["items"]
    assert item["properties"]["key"]["enum"] == [key.key for key in KEYS]
    assert item["properties"]["qualifiers"] == {
        "type": "object",
        "additionalProperties": {"type": "string"},
    }
    for key in KEYS:
        assert key.key in prompt
        assert key.description in prompt
        assert key.unit in prompt
    assert "residency" in prompt
    assert "| Residents | 15,300.00 |" in prompt


# ------------------------------------------------------------------------------------ sections


def _long_text() -> str:
    rows = "\n".join(f"| Row {n} | {n * 1000:,} |" for n in range(120))
    return f"# First\n\n{rows}\n\n# Second\n\n{rows}\n\n# Third\n\nThe cap is 15,300 a year.\n"


def test_a_long_text_is_sent_in_more_than_one_call() -> None:
    text = _long_text()
    client = ScriptedClient()
    extract_values(client, _source(text), KEYS)
    assert len(client.prompts) > 1
    assert any("The cap is 15,300 a year." in prompt for prompt in client.prompts)


def test_sections_rejoin_to_the_text_and_never_cut_a_line() -> None:
    text = _long_text()
    sections = split_sections(text)
    assert len(sections) > 1
    assert "".join(sections) == text
    lines = set(text.splitlines())
    for section in sections:
        assert len(section) <= SECTION_CHARS
        assert section.endswith("\n")
        assert set(section.splitlines()) <= lines


def test_an_oversized_heading_section_is_split_at_blank_lines() -> None:
    paragraph = "A sentence that is printed in the guide.\n" * 60
    text = f"# Only heading\n\n{paragraph}\n{paragraph}\n{paragraph}"
    sections = split_sections(text, limit=3000)
    assert "".join(sections) == text
    assert len(sections) == 3
    assert all(len(section) <= 3000 for section in sections)


def test_a_paragraph_longer_than_a_section_is_split_at_line_boundaries() -> None:
    text = "# Heading\n" + "".join(f"line {n} of one long paragraph\n" for n in range(400))
    sections = split_sections(text, limit=1000)
    assert "".join(sections) == text
    assert all(len(section) <= 1000 for section in sections)
    assert all(section.endswith("\n") for section in sections)


def test_short_sections_are_packed_together() -> None:
    text = "# One\nfirst\n# Two\nsecond\n# Three\nthird\n"
    assert split_sections(text) == [text]


def test_an_empty_text_has_no_sections() -> None:
    assert split_sections("") == []
    assert split_sections("\n\n  \n") == []


# ------------------------------------------------------------------------------------ helpers


def test_collapse_folds_whitespace_and_table_pipes() -> None:
    assert collapse("  a\n\tb   c ") == "a b c"
    assert collapse("| Residents | 15,300 |") == "Residents 15,300"
    assert collapse("Residents | 15,300") == collapse("| Residents  |  15,300 |")


def test_printed_in_accepts_both_forms_of_a_table_row() -> None:
    text = "| Residency | Cap |\n|---|---|\n| Residents | 15,300 |\n"
    assert printed_in("| Residents | 15,300 |", text)
    assert printed_in("Residents 15,300", text)
    assert not printed_in("Residents 15,30", text)
    assert not printed_in("residents 15,300", text)


def test_number_tokens_are_whole_numbers() -> None:
    assert number_tokens("from 40,000 to 15,300.00, or 3.5% over 10 years.") == [
        Decimal("40000"),
        Decimal("15300.00"),
        Decimal("3.5"),
        Decimal("10"),
    ]


@pytest.mark.parametrize(
    ("unit", "value", "expected"),
    [
        ("money", "15,300", Decimal("15300")),
        ("money", " 15300.50 ", Decimal("15300.50")),
        ("money", "$15,300", None),
        ("percent", "3.5 %", Decimal("3.5")),
        ("rate", "4", Decimal("4")),
        ("multiple", "9 times", Decimal("9")),
        ("multiple", "9 lots", None),
        ("years", "10", Decimal("10")),
        ("count", "1,000", Decimal("1000")),
        ("count", "2.5", None),
        ("money", "", None),
    ],
)
def test_parse_value_by_unit(unit: str, value: str, expected: Decimal | None) -> None:
    assert parse_value(unit, value) == expected
