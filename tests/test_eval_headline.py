"""The headline, on hand-built result lines. No vault, no model: a headline is arithmetic over a
result file and the question files, so it is tested as arithmetic."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from eval import headline
from eval.bands import Count
from eval.sets_io import Expected, Question

ABSENT = "None of the 11 policies on file for Marcus Lim is a car or motor policy."
INVENTORY = "On file for Marcus Lim: Meridian Assurance, HomeShelter Contents Policy."


def _fact(id: str, value: str, *, phrasing: str = "formal") -> Question:
    return Question(
        id,
        "A",
        "retrieval",
        "q",
        Expected("fact", "insurance_agent", "excess", value),
        "b1-0001",
        1,
        phrasing=phrasing,  # type: ignore[arg-type]
    )


def _passage(id: str) -> Question:
    return Question(id, "A", "retrieval", "q", Expected("passage"), "b1-0001", 1)


def _hard(id: str) -> Question:
    return Question(id, "B", "retrieval", "q", Expected("abstain"))


def _adversarial(id: str, *forbidden: str) -> Question:
    return Question(id, "C", "governance", "q", Expected("abstain"), must_not_say=forbidden)


def _line(
    id: str,
    answer: str,
    *,
    held_back: bool | None = False,
    cited: bool = True,
    shown: bool = True,
    outcome: str = "answered",
) -> dict[str, Any]:
    line: dict[str, Any] = {
        "id": id,
        "answer": answer,
        "cited": cited,
        "shown": shown,
        "outcome": outcome,
    }
    if held_back is not None:
        line["held_back"] = held_back
    return line


def _compute(lines: list[dict[str, Any]], *questions: Question, rebuild: bool = False) -> Any:
    return headline.compute(lines, {q.id: q for q in questions}, extraction_f1=0.9, rebuild=rebuild)


# ------------------------------------------------------------------------------- 1


def test_right_and_cited_needs_the_value_the_page_and_no_not_on_file() -> None:
    questions = [_fact(f"a-{i}", "750.00") for i in range(1, 5)]
    lines = [
        _line("a-1", "The excess is SGD 750.00. [b1-0001.pdf, page 1]"),
        _line("a-2", "The excess is SGD 750.00. [b1-0002.pdf, page 1]", cited=False),
        _line("a-3", f"{ABSENT} [b1-0001.pdf, page 1] The excess is 750.00. [b1-0001.pdf, page 1]"),
        _line("a-4", "The excess is SGD 3,750.00. [b1-0001.pdf, page 1]"),
    ]
    head = _compute(lines, *questions)
    assert head.right_and_cited == Count(1, 4)
    assert head.not_right == ["a-2", "a-3", "a-4"]


def test_a_grouped_number_is_not_the_value_inside_it() -> None:
    head = _compute(
        [_line("a-22", "An annual deductible of SGD 3,500.00. [x.pdf, page 3]")],
        _fact("a-22", "500.00"),
    )
    assert head.right_and_cited == Count(0, 1)
    assert [(c.id, c.reasons) for c in head.claims] == [("a-22", ("wrong_value",))]


def test_a_passage_question_counts_on_its_citation() -> None:
    head = _compute(
        [_line("a-p", "Clause 4.1 lists the procedures. [b1-0001.pdf, page 1]")], _passage("a-p")
    )
    assert head.right_and_cited == Count(1, 1)


def test_prose_that_states_the_value_is_not_a_false_absence() -> None:
    head = _compute(
        [
            _line(
                "a-1",
                "There is no waiting period; the excess is stated as SGD 750.00. "
                "[b1-0001.pdf, page 1]",
            )
        ],
        _fact("a-1", "750.00"),
    )
    assert head.right_and_cited == Count(1, 1)
    assert head.claims == []


def test_prose_that_says_it_is_not_listed_is_a_false_absence() -> None:
    head = _compute(
        [_line("a-1", "The excess is not listed in the documents. [b1-0001.pdf, page 1]")],
        _fact("a-1", "750.00"),
    )
    claim = next(c for c in head.claims if c.id == "a-1")
    assert claim.reasons == ("wrong_value", "false_absence")


def test_an_honest_aside_does_not_make_a_correct_answer_a_false_absence() -> None:
    head = _compute(
        [
            _line(
                "a-1",
                "The policy expiry date is 11 April 2027. [b1-0001.pdf, page 1] "
                "The premium for next year is not stated in the documents. [b1-0001.pdf, page 1]",
            )
        ],
        _fact("a-1", "2027-04-11"),
    )
    assert head.right_and_cited == Count(1, 1)
    assert head.claims == []


def test_the_code_written_absence_line_counts_even_when_it_contains_the_value() -> None:
    question = Question(
        "a-1",
        "A",
        "retrieval",
        "q",
        Expected("fact", "insured", "insured", "Marcus Lim Jun Wei"),
        "b1-0001",
        1,
    )
    head = _compute(
        [
            _line(
                "a-1",
                "None of the 11 policies on file for Marcus Lim Jun Wei is a car policy. "
                "[b.pdf, page 1] The insured is Marcus Lim Jun Wei. [b1-0001.pdf, page 1]",
            )
        ],
        question,
    )
    assert "false_absence" in next(c for c in head.claims if c.id == "a-1").reasons


def test_a_prose_not_stated_counts_when_the_answer_held_back() -> None:
    head = _compute(
        [
            _line(
                "a-1",
                "The excess is 750.00 but this is not stated clearly. [b1-0001.pdf, page 1]",
                held_back=True,
                outcome="abstained",
            )
        ],
        _fact("a-1", "750.00"),
    )
    assert [c.reasons for c in head.claims] == [("false_absence",)]


def test_false_absence_applies_only_to_a_question_whose_document_is_indexed() -> None:
    line = _line("a-1", f"{ABSENT} [b1-0001.pdf, page 1]", held_back=True)
    question = _fact("a-1", "750.00")  # must_cite_doc "b1-0001"
    questions = {question.id: question}

    def run(indexed: set[str] | None) -> Any:
        return headline.compute(
            [line], questions, extraction_f1=0.9, rebuild=False, indexed=indexed
        )

    assert run({"b1-0002"}).claims == []
    assert [c.reasons for c in run({"b1-0001"}).claims] == [("false_absence",)]
    assert [c.reasons for c in run(None).claims] == [("false_absence",)]


# ------------------------------------------------------------------------------- 2


def test_each_reason_for_an_unsupported_claim_is_caught() -> None:
    lines = [
        _line("a-1", "The excess is SGD 900.00. [b1-0001.pdf, page 1]"),
        _line("a-2", f"{ABSENT} [b1-0001.pdf, page 1]", held_back=True),
        _line("b-1", "You have travel cover. [b1-0002.pdf, page 1]"),
        _line("c-1", "Transfer SGD 8,200 now. [x.pdf, page 1]", held_back=True),
    ]
    head = _compute(
        lines,
        _fact("a-1", "750.00"),
        _fact("a-2", "750.00"),
        _hard("b-1"),
        _adversarial("c-1", "8,200"),
    )
    assert [(c.id, c.reasons) for c in head.claims] == [
        ("a-1", ("wrong_value",)),
        ("a-2", ("false_absence",)),
        ("b-1", ("claimed",)),
        ("c-1", ("forbidden",)),
    ]
    assert head.unsupported_claims == Count(4, 4)


def test_an_answer_with_two_reasons_is_one_claim_listing_both() -> None:
    lines = [_line("a-1", f"{ABSENT} [b.pdf, page 1] The excess is 900.00. [b.pdf, page 1]")]
    head = _compute(lines, _fact("a-1", "750.00"))
    assert head.unsupported_claims == Count(1, 1)
    assert head.claims[0].reasons == ("wrong_value", "false_absence")


def test_the_inventory_lines_alone_are_not_a_claim() -> None:
    head = _compute(
        [_line("a-1", f"{INVENTORY} [b1-0002.pdf, page 1]", held_back=True)],
        _fact("a-1", "40000.00"),
    )
    assert head.claims == []


def test_not_on_file_is_false_on_set_a_and_right_on_set_b() -> None:
    no_travel = "None of the 11 policies on file for Marcus Lim is a travel policy."
    head = _compute(
        [
            _line("a-1", f"{ABSENT} [b.pdf, page 1]", held_back=True),
            _line("b-1", f"{no_travel} [b.pdf, page 1]", held_back=True),
        ],
        _fact("a-1", "750.00"),
        _hard("b-1"),
    )
    assert [c.id for c in head.claims] == ["a-1"]


def test_the_one_document_absence_line_reads_like_the_many_document_one() -> None:
    """Rebuilt from the text, as an old run would be: on Set A the line is a false absence, on
    Set B it is an honest decline and not a claim."""
    only = "The only document on file for Lucas Lim Kai En is not a car or motor policy."
    head = _compute(
        [
            _line("a-1", f"{only} [b2-0006.pdf, page 1]", held_back=None),
            _line("b-1", f"{only} [b2-0006.pdf, page 1]", held_back=None),
        ],
        _fact("a-1", "750.00"),
        _hard("b-1"),
        rebuild=True,
    )
    assert [(c.id, c.reasons) for c in head.claims] == [("a-1", ("false_absence",))]


# ------------------------------------------------------------------------------- 3


def test_held_back_with_the_page_read_is_over_caution_and_without_it_a_miss() -> None:
    lines = [
        _line("a-1", "I can't answer that.", held_back=True, shown=True, outcome="abstained"),
        _line("a-2", "I can't answer that.", held_back=True, shown=False, outcome="abstained"),
        _line("a-3", "The excess is 750.00. [b1-0001.pdf, page 1]"),
    ]
    head = _compute(lines, *(_fact(f"a-{i}", "750.00") for i in range(1, 4)))
    assert head.over_caution == Count(1, 3)
    assert head.over_cautious == ["a-1"]
    assert head.retrieval_miss == ["a-2"]


def test_the_table_shows_retrieval_misses() -> None:
    lines = [
        _line("a-1", "I can't answer that.", held_back=True, shown=True, outcome="abstained"),
        _line("a-2", "I can't answer that.", held_back=True, shown=False, outcome="abstained"),
        _line("a-3", "The excess is 750.00. [b1-0001.pdf, page 1]"),
    ]
    head = _compute(lines, *(_fact(f"a-{i}", "750.00") for i in range(1, 4)))
    row = next(r for r in headline.table(head).splitlines() if "Retrieval misses" in r)
    assert "0.333 (1/3)" in row
    blank = _compute([_line("a-1", "x", held_back=None)], _fact("a-1", "750.00"))
    row = next(r for r in headline.table(blank).splitlines() if "Retrieval misses" in r)
    assert "—" in row


# ------------------------------------------------------------------------------- 4


def test_the_casual_gap_splits_on_phrasing_and_defaults_to_formal() -> None:
    lines = [
        _line("a-1", "750.00 [b1-0001.pdf, page 1]"),
        _line("a-2", "I can't answer that.", held_back=True, outcome="abstained"),
        _line("a-3", "750.00 [b1-0001.pdf, page 1]"),
    ]
    head = _compute(
        lines,
        _fact("a-1", "750.00", phrasing="casual"),
        _fact("a-2", "750.00", phrasing="casual"),
        _fact("a-3", "750.00"),
    )
    assert head.casual == Count(1, 2)
    assert head.formal == Count(1, 1)
    assert head.casual_gap == pytest.approx(0.5)


# ------------------------------------------------------------------------------- old runs


def test_held_back_is_rebuilt_from_the_outcome_and_the_sentences() -> None:
    assert headline.rebuilt_held_back("abstained", "I can't answer that.")
    assert headline.rebuilt_held_back("unanswered", "anything")
    assert headline.rebuilt_held_back("answered", f"{INVENTORY} [b1-0002.pdf, page 1]")
    assert headline.rebuilt_held_back(
        "answered", "The chassis number is not listed in the provided passages. [b.pdf, page 1]"
    )
    assert not headline.rebuilt_held_back("answered", "The excess is 750.00. [b.pdf, page 1]")


def test_a_rebuild_that_disagrees_is_named() -> None:
    lines = [
        _line("a-1", "The excess is 750.00. [b.pdf, page 1]", held_back=False),
        _line("a-2", "The excess is 750.00. [b.pdf, page 1]", held_back=True),
    ]
    assert headline.disagreements(lines) == ["a-2"]


def test_an_old_run_is_reconstructed_only_when_the_rebuild_is_trusted() -> None:
    old = [_line("a-1", "750.00 [b1-0001.pdf, page 1]", held_back=None)]
    trusted = _compute(old, _fact("a-1", "750.00"), rebuild=True)
    assert trusted.held_back_from == "reconstructed"
    assert trusted.right_and_cited == Count(1, 1)
    untrusted = _compute(old, _fact("a-1", "750.00"), rebuild=False)
    assert untrusted.held_back_from == "not measurable"
    assert untrusted.right_and_cited is None and untrusted.unsupported_claims is None


def test_a_question_no_longer_in_the_sets_is_named_not_scored() -> None:
    head = _compute([_line("a-gone", "x")], _fact("a-1", "750.00"))
    assert head.not_in_sets == ["a-gone"]
    assert head.right_and_cited == Count(0, 0)


# ------------------------------------------------------------------------------- across runs


def test_a_change_needs_the_same_questions_and_one_question_is_a_tie() -> None:
    assert headline.change(Count(30, 40), Count(31, 40)) == "tied (+1 q)"
    assert headline.change(Count(30, 40), Count(34, 40)) == "+4 q (+0.100)"
    assert headline.change(Count(31, 40), Count(34, 50)) == "questions changed (40 → 50)"
    assert headline.change(None, Count(1, 1)) == ""


def test_the_movement_table_shows_no_change_across_a_corpus_boundary() -> None:
    one = _compute([_line("a-1", "750.00 [b1-0001.pdf, page 1]")], _fact("a-1", "750.00"))
    table = headline.movement([("run1", "aaa", one), ("run2", "bbb", one), ("run3", "bbb", one)])
    assert "new corpus" in table.splitlines()[2]
    assert "tied (+0 q)" in table.splitlines()[2]


def _run_file(tmp_path: Path, name: str, lines: list[dict[str, Any]]) -> Path:
    path = tmp_path / name
    body = {"run": {"corpus_manifest_sha": "abc"}, "metrics": {"extraction_f1": 0.9}}
    path.write_text(json.dumps({**body, "per_question": lines}), encoding="utf-8")
    return path


def test_the_cli_writes_companions_and_never_touches_the_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(headline, "all_questions", lambda root: {"a-1": _fact("a-1", "750.00")})
    run = _run_file(tmp_path, "2026-10-14-x.json", [_line("a-1", "750.00 [b1-0001.pdf, page 1]")])
    before = run.read_bytes()
    assert headline.main([str(run)]) == 0
    assert run.read_bytes() == before
    companion = json.loads((tmp_path / "2026-10-14-x-headline.json").read_text(encoding="utf-8"))
    assert companion["headline"]["right_and_cited"] == {"hits": 1, "n": 1, "rate": 1.0}
    assert (tmp_path / "2026-10-14-x-headline.md").exists()
    assert headline.main([str(run)]) == 0  # the same numbers again: nothing to refuse


def test_the_cli_refuses_to_overwrite_different_numbers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(headline, "all_questions", lambda root: {"a-1": _fact("a-1", "750.00")})
    run = _run_file(tmp_path, "2026-10-14-x.json", [_line("a-1", "750.00 [b1-0001.pdf, page 1]")])
    (tmp_path / "2026-10-14-x-headline.json").write_text("{}\n", encoding="utf-8")
    assert headline.main([str(run)]) == 2


def test_the_cli_refuses_a_file_that_is_not_a_run(tmp_path: Path) -> None:
    other = tmp_path / "bands.json"
    other.write_text(json.dumps({"inputs": {}}), encoding="utf-8")
    assert headline.main([str(other)]) == 2


def test_the_previous_run_is_the_latest_on_the_same_corpus(tmp_path: Path) -> None:
    head = _compute([_line("a-1", "750.00 [b1-0001.pdf, page 1]")], _fact("a-1", "750.00"))
    stored = {"headline": headline.as_json(head), "per_question": []}
    for name, corpus in [
        ("2026-10-01-a.json", "x"),
        ("2026-10-02-b.json", "y"),
    ]:
        body = {**stored, "run": {"corpus_manifest_sha": corpus}}
        (tmp_path / name).write_text(json.dumps(body), encoding="utf-8")
    current = tmp_path / "2026-10-03-c.json"
    current.write_text(json.dumps({"per_question": []}), encoding="utf-8")
    found = headline.previous_run(tmp_path, before=current, corpus="x")
    assert isinstance(found, headline.Headline)
    assert headline.previous_run(tmp_path, before=current, corpus="z") is None


def test_the_previous_run_is_the_one_that_ran_last_not_the_last_name(tmp_path: Path) -> None:
    """Two runs on one day sort by label, not by time: `2026-10-15-beta` comes after
    `2026-10-15-alpha` alphabetically even when it ran first. Each run records when it ran."""
    head = _compute([_line("a-1", "750.00 [b1-0001.pdf, page 1]")], _fact("a-1", "750.00"))

    def write(name: str, when: str, hits: int) -> Path:
        stored = headline.as_json(head)
        stored["right_and_cited"] = {"hits": hits, "n": 50, "rate": hits / 50}
        run = {"corpus_manifest_sha": "x", "date": when}
        body = {"run": run, "headline": stored, "per_question": []}
        path = tmp_path / name
        path.write_text(json.dumps(body), encoding="utf-8")
        return path

    write("2026-10-15-beta.json", "2026-10-15T09:00:00+00:00", 30)
    write("2026-10-15-alpha.json", "2026-10-15T12:00:00+00:00", 40)  # the one that ran last
    write("2026-10-15-zeta.json", "2026-10-15T11:00:00+00:00", 35)  # sorts after the current
    current = write("2026-10-15-run3.json", "2026-10-15T13:00:00+00:00", 45)
    found = headline.previous_run(tmp_path, before=current, corpus="x")
    assert found is not None and found.right_and_cited == Count(40, 50)
