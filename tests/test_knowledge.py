"""A pack's words, matched whole. "warded" is in the question; "awarded" is not "warded"."""

from __future__ import annotations

from core.graph.knowledge import categories_asked, glossary, mentions, reworded
from core.packs import pack


def test_warded_is_said_the_way_the_policy_prints_it() -> None:
    packs = [pack("insurance_agent")]
    assert (
        reworded("got warded 2 days, claimable?", packs)
        == "got hospitalised as an inpatient 2 days, can claim?"
    )


def test_the_longest_phrase_wins() -> None:
    packs = [pack("insurance_agent")]
    assert reworded("i kena warded", packs) == "i was hospitalised as an inpatient"


def test_a_word_inside_another_word_is_not_a_match() -> None:
    assert not mentions("what was I awarded?", "warded")
    assert reworded("what was I awarded?", [pack("insurance_agent")]) is None


def test_the_understanding_step_is_told_only_the_words_the_question_used() -> None:
    assert glossary("warded for dengue", [pack("insurance_agent")]) == [
        "warded = hospitalised as an inpatient"
    ]


def test_a_question_names_the_categories_it_is_about() -> None:
    packs = [pack("insurance_agent")]
    assert [a.category.id for a in categories_asked("do i have dental insurance?", packs)] == [
        "dental"
    ]
    assert {a.category.id for a in categories_asked("warded for dengue 3 days", packs)} == {
        "hospital_cash",
        "hospital_expense",
    }
    assert categories_asked("when does it expire?", packs) == []
