"""The insurance pack's categories, against the product names that would misfile them.

Every row is a trap the council named on 13 September. Precision matters more than recall here:
`None` is an allowed answer, a wrong category is not, because a wrong category silently hides a
policy from an answer.
"""

from __future__ import annotations

import pytest

from core.contracts import Categories
from core.graph.knowledge import categorise
from core.packs import pack


def _categories() -> Categories:
    categories = pack("insurance_agent").manifest.answering.categories
    assert categories is not None
    return categories


@pytest.mark.parametrize(
    ("printed", "expected"),
    [
        ("Hospital Income Protection Plan", "hospital_cash"),  # cash per day, not the bill
        ("PrivateCare Hospital and Surgical Plan", "hospital_expense"),
        ("AIA HealthShield Gold Max (Integrated Shield Plan)", "hospital_expense"),
        ("CareShield Critical Illness Plan", "critical_illness"),  # not CareShield Life
        ("CareShield Life Supplement", "long_term_care"),
        ("Heritage Whole Life Plan", "whole_life"),
        ("Term Life Protector", "term_life"),
        ("Private Car Insurance Policy", "motor"),
        ("HomeShelter Contents Policy", "home"),
        ("TravelEasy Annual Travel Insurance", "travel"),
        ("Maid Protection Plan", "domestic_helper"),
        ("PawCare Pet Insurance", "pet"),
        ("SmileGuard Dental Plan", "dental"),
        ("Lionhead Life Assurance", None),  # an insurer's name is not a kind of cover
        ("Wealth Accumulator", None),
    ],
)
def test_a_printed_product_name_falls_in_exactly_the_category_a_person_would_file_it_under(
    printed: str, expected: str | None
) -> None:
    found = categorise(printed, _categories())
    assert (found.id if found else None) == expected


def test_the_persona_is_voice_and_the_decline_refuses_a_recommendation() -> None:
    manifest = pack("insurance_agent").manifest
    assert "recommend" in manifest.guardrails.advice_decline
    assert "never" not in manifest.persona.system.lower()  # rules live in the core, not the voice
