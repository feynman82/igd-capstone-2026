"""Finding the label printed beside a value a sentence states, and asking whether it agrees."""

from __future__ import annotations

import json
from typing import Any
from uuid import uuid4

from core.graph.labels import SCHEMA, label_supports, labelled_lines
from core.graph.ports import Passage
from core.runtime.ollama import Generated, ModelUnavailable

SCHEDULE = (
    "1. POLICY SCHEDULE\n"
    "Name of Insured: Lee Wen Hui\n"
    "Period of Insurance From: 3 May 2026\n"
    "Annual Premium: SGD 1,560.00\n"
    "Excess: SGD 600.00\n"
    "Notify the insurer within 24 hours of any accident: the policy may otherwise lapse."
)


def _page(text: str, kind: str = "document") -> Passage:
    return Passage(1, uuid4(), 1, text, 0.6, "schedule.pdf", pack_id="insurance_agent", kind=kind)


def test_a_name_a_sentence_repeats_brings_its_label() -> None:
    lines = labelled_lines("The named driver is Lee Wen Hui.", [_page(SCHEDULE)])
    assert lines == ["Name of Insured: Lee Wen Hui"]


def test_a_date_and_a_reformatted_amount_bring_theirs() -> None:
    assert labelled_lines("Cover starts on 3 May 2026.", [_page(SCHEDULE)]) == [
        "Period of Insurance From: 3 May 2026"
    ]
    assert labelled_lines("You pay 1560 a year.", [_page(SCHEDULE)]) == [
        "Annual Premium: SGD 1,560.00"
    ]


def test_a_value_printed_without_a_label_brings_nothing() -> None:
    letterhead = _page("WESTGATE ASSURANCE\nServicing Branch · Hotline 1800-000-0000")
    assert labelled_lines("Your agent is from WESTGATE ASSURANCE.", [letterhead]) == []


def test_prose_with_a_colon_and_a_short_value_are_not_labels() -> None:
    assert labelled_lines("Notify within 24 hours.", [_page(SCHEDULE)]) == []
    assert labelled_lines("Item 1 applies.", [_page("Rider: 1")]) == []


def test_the_documents_on_file_lines_are_written_by_code_and_not_checked() -> None:
    inventory = _page("Westgate, Motor Plan. insured: Lee Wen Hui; premium: 1560.", "inventory")
    assert labelled_lines("The insured is Lee Wen Hui.", [inventory]) == []


class Judge:
    def __init__(self, supported: bool) -> None:
        self.supported = supported
        self.prompts: list[str] = []
        self.schemas: list[dict[str, Any]] = []

    def constrained(self, system: str, prompt: str, schema: dict[str, Any], **_: Any) -> Generated:
        self.prompts.append(prompt)
        self.schemas.append(schema)
        return Generated(json.dumps({"supported": self.supported}), "fake", 1)


def test_the_judge_reads_the_printed_lines_and_the_sentence_and_answers_yes_or_no() -> None:
    judge = Judge(False)
    lines = ["Name of Insured: Lee Wen Hui"]
    assert not label_supports(judge, "The named driver is Lee Wen Hui.", lines)
    assert "- Name of Insured: Lee Wen Hui" in judge.prompts[0]
    assert "The sentence: The named driver is Lee Wen Hui." in judge.prompts[0]
    assert judge.schemas[0] == SCHEMA
    assert label_supports(Judge(True), "The insured is Lee Wen Hui.", lines)


def test_the_examples_come_from_no_document_parrot_holds() -> None:
    """They teach the task; they must not teach the answers to the question sets."""
    judge = Judge(True)
    label_supports(judge, "x", ["Annual Premium: SGD 1,560.00"])
    examples = judge.prompts[0].split("The document prints:")[0]
    for word in ("Marcus", "Meridian", "road tax", "named driver", "SLK"):
        assert word.lower() not in examples.lower()


def test_a_value_the_question_names_is_a_reference_not_an_answer() -> None:
    """19 October: "The lender on facility HP-2021-448190 is Crescent Bank Limited" was checked
    against `Agreement No: HP-2021-448190` and the right answer dropped. The question had named
    the facility; the sentence was only pointing at it."""
    page = _page("Agreement No: WG-2022-118204\nLender: Westgate Finance")
    sentence = "The lender on facility WG-2022-118204 is Westgate Finance."
    assert labelled_lines(sentence, [page], "Who is the lender on facility WG-2022-118204?") == [
        "Lender: Westgate Finance"
    ]
    assert labelled_lines(sentence, [page]) == [
        "Agreement No: WG-2022-118204",
        "Lender: Westgate Finance",
    ]


class Failing:
    def constrained(self, *_: Any, **__: Any) -> Generated:
        raise ModelUnavailable("the generator did not answer")


def test_a_check_that_cannot_run_leaves_the_sentence_unchecked() -> None:
    """19 October: a failed call ended a whole answer and took a right one with it."""
    assert label_supports(Failing(), "You pay 1560 a year.", ["Annual Premium: SGD 1,560.00"])
