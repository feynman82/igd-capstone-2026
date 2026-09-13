"""What the gate checks beyond "is there a citation".

A cited sentence can still say something its passage never did. Two cheap, deterministic cases
are caught here: a number the passage never printed — "3 days pays SGD 3,000" when the plan
prints SGD 1,000 a day and a SGD 3,500 deductible — and cover claimed from an exclusion clause.
"""

from __future__ import annotations

from uuid import uuid4

from core.contracts import Exclusions
from core.graph.gate import Claim, check_content, check_one, unprinted_numbers
from core.graph.ports import Passage

DOC = uuid4()
SCHEDULE = Passage(
    31,
    DOC,
    4,
    "9.1 The Annual Premium of SGD 1,860.00 is due on or before 20 February 2026.",
    0.6,
    "privatecare.pdf",
    "Meridian Assurance, PrivateCare — policy schedule — 9. PREMIUMS — page 4",
    "insurance_agent",
)
EXCLUSION = Passage(
    32,
    DOC,
    3,
    "Dental treatment, oral surgery, except emergency treatment to sound natural teeth.",
    0.5,
    "privatecare.pdf",
    "Meridian Assurance, PrivateCare — policy schedule — 7. EXCLUSIONS — page 3",
    "insurance_agent",
)
EXCLUDED = Exclusions(
    headings=["exclusions", "what is not covered"],
    claims=["covers", "covered", "pays"],
    negations=["not", "except", "excluded", "unless"],
)
BY_REF = {passage.ref: passage for passage in (SCHEDULE, EXCLUSION)}


def test_a_number_copied_from_the_passage_is_kept_however_it_is_formatted() -> None:
    claim = Claim("The annual premium is SGD 1860, due by 20 February 2026.", (SCHEDULE.ref,))
    assert check_content(claim, BY_REF) is None


def test_a_number_no_cited_passage_printed_is_dropped() -> None:
    claim = Claim("Three days in hospital pays SGD 3,000.", (SCHEDULE.ref,))
    why = check_content(claim, BY_REF)
    assert why is not None and "3,000" in why


def test_a_leading_zero_does_not_make_a_printed_date_unprinted() -> None:
    printed = Passage(1, DOC, 1, "Policy Inception (01 September 2019)", 0.5)
    assert unprinted_numbers("Cover began on 1 September 2019.", [printed]) == []


def test_cover_claimed_from_an_exclusion_is_dropped() -> None:
    claim = Claim("Your plan covers emergency dental treatment.", (EXCLUSION.ref,))
    assert check_content(claim, BY_REF, exclusions=EXCLUDED) == "claims cover from an exclusion"


def test_an_exclusion_quoted_as_an_exclusion_is_kept() -> None:
    claim = Claim("Dental treatment is not covered, except emergency treatment.", (EXCLUSION.ref,))
    assert check_content(claim, BY_REF, exclusions=EXCLUDED) is None


def test_a_page_and_a_document_on_file_with_the_same_id_are_different_citations() -> None:
    page = Passage(7, DOC, 1, "a page", 0.5)
    on_file = Passage(7, DOC, 1, "a document on file", 1.0, kind="inventory")
    assert page.ref != on_file.ref
    assert check_one(Claim("x", (on_file.ref,)), {page.ref}) is not None
