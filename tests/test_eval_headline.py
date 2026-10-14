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
