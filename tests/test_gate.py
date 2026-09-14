"""What the gate checks beyond "is there a citation".

A cited sentence can still say something its passage never did. Two cheap, deterministic cases
are caught here: a number the passage never printed — "3 days pays SGD 3,000" when the plan
prints SGD 1,000 a day and a SGD 3,500 deductible — and cover claimed from an exclusion clause.
"""

from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from core.contracts import Exclusions
from core.graph.advice import Calculation, Figure, Input, passages_for
from core.graph.gate import Claim, check_advice, check_content, check_one, unprinted_numbers
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


def test_a_policy_number_is_kept_only_when_it_is_printed_whole() -> None:
    printed = Passage(1, DOC, 1, "Policy MV-2026-448120. Reference 448121.", 0.5)
    assert unprinted_numbers("Your policy number is MV-2026-448121.", [printed]) == [
        "MV-2026-448121"
    ]
    assert unprinted_numbers("Your policy number is MV-2026-448120.", [printed]) == []


def test_a_sentence_left_with_no_word_or_figure_is_empty() -> None:
    """ "See passages 1, 2." is "." once its passage numbers are removed: a citation, no claim."""
    assert check_one(Claim(".", ("document:11",)), {"document:11"}) == "empty"
    assert check_one(Claim("(  ).", ("document:11",)), {"document:11"}) == "empty"


def test_a_date_on_file_may_be_written_the_way_a_person_says_it() -> None:
    on_file = Passage(
        4, DOC, 1, "Private Car Insurance Policy. expiry date: 2027-04-11.", 1.0, kind="inventory"
    )
    assert unprinted_numbers("It expires on 11 April 2027.", [on_file]) == []


# ------------------------------------------------------------------------------- check_advice


def _advice_calculation() -> Calculation:
    return Calculation(
        pack_id="sample_pack",
        shape_id="need",
        label="Sample need",
        subject="Alex Tan",
        person_ids=(1,),
        inputs=(
            Input(
                ref="fact:5",
                role="amount",
                label="amount on file",
                value_text="SGD 100,000.00",
                citation="statement.pdf, page 1",
                document_id="doc-1",
                page=1,
            ),
        ),
        figures=(
            Figure(
                name="target",
                value=Decimal("451200.00"),
                text="SGD 451,200.00",
                words=("target", "guideline"),
            ),
            Figure(
                name="gap",
                value=Decimal("251200.00"),
                text="SGD 251,200.00",
                words=("gap", "shortfall"),
            ),
        ),
        verdict="no_room",
        verdict_text="Alex Tan has a gap of SGD 251,200.00.",
    )


ADVICE_FIGURES = _advice_calculation().figures
BY_REF_ADVICE = {p.ref: p for p in passages_for(_advice_calculation())}


def _shared_value_calculation() -> Calculation:
    """An input that happens to print the same value as a figure, so the role check (which asks
    only about `calculation:0`) has something to prove it correctly leaves alone."""
    return Calculation(
        pack_id="sample_pack",
        shape_id="need",
        label="Sample need",
        subject="Alex Tan",
        person_ids=(1,),
        inputs=(
            Input(
                ref="fact:9",
                role="held",
                label="amount held",
                value_text="SGD 451,200.00",
                citation="statement.pdf, page 2",
                document_id="doc-2",
                page=2,
            ),
        ),
        figures=ADVICE_FIGURES,
        verdict="no_room",
        verdict_text="Alex Tan has a gap of SGD 251,200.00.",
    )


BY_REF_SHARED_VALUE = {p.ref: p for p in passages_for(_shared_value_calculation())}


def _meets_calculation() -> Calculation:
    """A `meets` outcome: the gap figure is negative, and only its printed text carries the
    number — `_NUMBER` matches through `figure.text`, never through the signed `Decimal`."""
    return Calculation(
        pack_id="sample_pack",
        shape_id="need",
        label="Sample need",
        subject="Alex Tan",
        person_ids=(1,),
        inputs=(),
        figures=(
            Figure(
                name="gap",
                value=Decimal("-48800.00"),
                text="SGD 48,800.00 above the guideline",
                words=("above the guideline", "surplus"),
            ),
        ),
        verdict="meets",
        verdict_text="Alex Tan is SGD 48,800.00 above the guideline.",
    )


MEETS_FIGURES = _meets_calculation().figures
BY_REF_MEETS = {p.ref: p for p in passages_for(_meets_calculation())}


def test_check_advice_drops_a_verdict_word() -> None:
    claim = Claim("You should buy more cover.", ("calculation:0",))
    assert (
        check_advice(claim, BY_REF_ADVICE, ADVICE_FIGURES)
        == "a verdict is said by code, not the explanation"
    )


def test_check_advice_keeps_a_figure_stated_with_its_own_word() -> None:
    claim = Claim("The gap is SGD 251,200.00.", ("calculation:0",))
    assert check_advice(claim, BY_REF_ADVICE, ADVICE_FIGURES) is None


def test_check_advice_drops_a_figures_value_stated_in_the_wrong_role() -> None:
    claim = Claim("You are short by SGD 451,200.00.", ("calculation:0",))
    assert (
        check_advice(claim, BY_REF_ADVICE, ADVICE_FIGURES)
        == "states SGD 451,200.00 without saying it is the target"
    )


def test_check_advice_keeps_a_figures_value_stated_with_a_different_one_of_its_words() -> None:
    claim = Claim("The guideline works out to SGD 451,200.00.", ("calculation:0",))
    assert check_advice(claim, BY_REF_ADVICE, ADVICE_FIGURES) is None


def test_check_advice_keeps_recommended_alone_but_recommended_to_is_a_verdict() -> None:
    claim = Claim("The recommended guideline works out to SGD 451,200.00.", ("calculation:0",))
    assert check_advice(claim, BY_REF_ADVICE, ADVICE_FIGURES) is None


def test_check_advice_keeps_a_number_printed_only_by_a_cited_fact() -> None:
    claim = Claim("The amount on file is SGD 100,000.00.", ("fact:5",))
    assert check_advice(claim, BY_REF_ADVICE, ADVICE_FIGURES) is None


def test_check_advice_does_not_role_check_a_number_cited_only_to_its_input() -> None:
    # SGD 451,200.00 is also the target figure's value, but this claim cites fact:9, not
    # calculation:0, so check 4 never runs — it would otherwise drop this for using neither
    # of the target figure's words.
    claim = Claim("The amount held is SGD 451,200.00.", ("fact:9",))
    assert check_advice(claim, BY_REF_SHARED_VALUE, ADVICE_FIGURES) is None


def test_check_advice_drops_a_never_say_phrase() -> None:
    claim = Claim("This plan is a good fit for you.", ("calculation:0",))
    assert (
        check_advice(claim, BY_REF_ADVICE, ADVICE_FIGURES, never_say=("good fit",))
        == "says what this advice never says"
    )


def test_check_advice_matches_a_negative_figure_through_its_printed_text() -> None:
    claim = Claim("You are SGD 48,800.00 above the guideline.", ("calculation:0",))
    assert check_advice(claim, BY_REF_MEETS, MEETS_FIGURES) is None


def test_check_advice_drops_a_negative_figures_value_stated_without_its_words() -> None:
    claim = Claim("You are SGD 48,800.00 clear of the minimum.", ("calculation:0",))
    assert (
        check_advice(claim, BY_REF_MEETS, MEETS_FIGURES)
        == "states SGD 48,800.00 above the guideline without saying it is the gap"
    )
