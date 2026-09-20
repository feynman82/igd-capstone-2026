"""The insurance pack's categories, against the product names that would misfile them.

Every row is a trap the council named on 13 September. Precision matters more than recall here:
`None` is an allowed answer, a wrong category is not, because a wrong category silently hides a
policy from an answer.
"""

from __future__ import annotations

import pytest

from core.contracts import Categories
from core.graph.knowledge import categorise, mentions
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


@pytest.mark.parametrize(
    "question",
    [
        "recommend the type of policies i should get",
        "What should I get?",
        "what insurance do I need?",
        "Can you recommend a policy for me?",
        "what policies should i be looking at",
        "should i get more cover?",
        "What is lacking in my insurance?",  # the wording that already worked
    ],
)
def test_asking_what_to_get_reaches_the_coverage_review(question: str) -> None:
    """Asking what to get is asking what is missing, and the review is what answers it.

    On 20 September "recommend the type of policies i should get" was declined: the router read
    it as `advise`, no shape phrase matched, and the generic decline came back. The gap between
    the two wordings was the whole failure — the arithmetic behind the answer already ran.
    """
    advice = pack("insurance_agent").manifest.advice
    assert advice is not None and advice.review is not None
    assert any(mentions(question, phrase) for phrase in advice.review.asked), question


def test_every_gap_the_review_runs_names_the_cover_that_closes_it() -> None:
    """A shortfall nobody can act on is half an answer. `closed_by` is what makes the review say
    which kind of cover closes each gap, so a shape the review runs without it is a bug."""
    advice = pack("insurance_agent").manifest.advice
    assert advice is not None and advice.review is not None
    by_id = {shape.id: shape for shape in advice.shapes}
    for shape_id in advice.review.shapes:
        assert by_id[shape_id].closed_by, f"{shape_id} states a gap with no way to close it"
