"""The evaluation harness, scored without a model.

Everything code-scored is exact, so it is tested exactly: a fake graph answers from a lookup
table, the recorder is fed by a fake retriever, and the numbers that come out are the numbers
arithmetic says. The judge is not run here — `make check` must pass on a machine with no
Ollama — but the file the harness writes has the nine keys either way, which is the contract.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path

import pytest

from core.graph.answer import Answer, Citation, Cited
from core.graph.ports import Passage
from eval import harness, score
from eval.run import _runtime_numbers, _table
from eval.sets_io import MalformedQuestion, Question, load_set, subset

ROOT = Path(__file__).resolve().parents[1]


# ------------------------------------------------------------------------------- the sets


def test_lane_b_questions_load_and_every_answerable_one_cites_a_page() -> None:
    questions = load_set(ROOT, "A")
    assert len(questions) >= 12
    assert all(q.gradeable_citation for q in questions)
    assert all(q.expected.kind != "abstain" for q in questions)
    hard = load_set(ROOT, "B")
    assert all(q.expected.kind == "abstain" and not q.gradeable_citation for q in hard)


def _write(tmp_path: Path, folder: str, *lines: str) -> Path:
    target = tmp_path / "eval" / "sets" / folder
    target.mkdir(parents=True)
    (target / "x.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return tmp_path


def test_an_abstention_that_cites_a_document_is_refused(tmp_path: Path) -> None:
    root = _write(
        tmp_path,
        "hard_negatives",
        '{"id": "b-1", "set": "B", "lane": "x", "question": "q", '
        '"expected": {"kind": "abstain"}, "must_cite_doc": "b1-0001"}',
    )
    with pytest.raises(MalformedQuestion, match="cites nothing"):
        load_set(root, "B")


def test_a_fact_question_needs_a_value_and_a_page(tmp_path: Path) -> None:
    root = _write(
        tmp_path,
        "answerable",
        '{"id": "a-1", "set": "A", "lane": "x", "question": "q", '
        '"expected": {"kind": "fact", "key": "expiry_date"}, "must_cite_doc": "b1-0001", '
        '"must_cite_page": 1}',
    )
    with pytest.raises(MalformedQuestion, match=r"expected\.value"):
        load_set(root, "A")


def test_a_question_filed_under_the_wrong_set_is_refused(tmp_path: Path) -> None:
    root = _write(
        tmp_path,
        "answerable",
        '{"id": "b-1", "set": "B", "lane": "x", "question": "q", "expected": {"kind": "abstain"}}',
    )
    with pytest.raises(MalformedQuestion, match="under answerable/"):
        load_set(root, "A")


def test_subset_is_stable_and_spread_across_lanes() -> None:
    questions = [
        _question(f"q{i}", lane=("packs", "retrieval", "governance")[i % 3]) for i in range(30)
    ]
    first, second = subset(questions, 9, seed=7), subset(questions, 9, seed=7)
    assert first == second
    assert {q.lane for q in first} == {"packs", "retrieval", "governance"}
    assert [q.lane for q in first].count("packs") == 3
    assert subset(questions, 3, seed=1) != subset(questions, 3, seed=2)


# ------------------------------------------------------------------------------- value matching


@pytest.mark.parametrize(
    ("value", "text", "expected"),
    [
        ("2027-04-11", "It expires on 11 April 2027.", True),
        ("2027-04-11", "Expiry: 2027-04-11", True),
        ("2027-04-11", "renews 11 Apr 2027", True),
        ("2027-04-11", "expires 12 April 2027", False),
        ("1284.00", "The premium is $1,284.00 a year.", True),
        ("1284.00", "premium payable: 1284", True),
        ("1284.00", "sum insured 12840.00", False),
        ("40000.00", "insured for S$40,000", True),
        ("Meridian Assurance", "Issued by MERIDIAN  Assurance Ltd.", True),
        ("Meridian Assurance", "Issued by Lionhead Life Assurance.", False),
    ],
)
def test_a_register_value_is_recognised_however_it_is_printed(
    value: str, text: str, expected: bool
) -> None:
    assert score.mentions(text, value) is expected


def test_same_value_normalises_dates_numbers_and_text() -> None:
    assert score.same_value("2027-04-11", "2027-04-11")
    assert score.same_value("1284.00", "1284")
    assert score.same_value("Meridian Assurance", "meridian  assurance")
    assert not score.same_value("1284.00", "1284.50")
    assert not score.same_value("2027-04-11", "11 April 2027")  # the schema types a date
    assert not score.same_value("", "anything")
    assert not score.same_value("1284.00", None)


# ------------------------------------------------------------------------------- extraction F1


def test_extraction_f1_scores_only_indexed_documents_against_the_register() -> None:
    register = [
        {
            "doc_id": "b1-0001",
            "doc_type": "policy_schedule",
            "pack_id": "insurance_agent",
            "tier": "clean",
            "policy_no": "MV-1",
            "expiry_date": "2027-04-11",
            "premium_payable": "1284.00",
            "excess": "",
            "field_pages": "",
            "notes": "",
        },
        {
            "doc_id": "b1-0002",
            "doc_type": "payslip",
            "pack_id": "iras_tax",
            "tier": "clean",
            "gross_salary": "5000.00",
            "field_pages": "",
            "notes": "never ingested",
        },
    ]
    facts = [
        score.FactRow("b1-0001", "policy_no", "MV-1"),  # hit
        score.FactRow("b1-0001", "expiry_date", "2027-04-12"),  # wrong: a false claim and a miss
        score.FactRow("b1-0001", "excess", "750.00"),  # the register says none printed
        # premium_payable never extracted: a miss
    ]
    scored = score.extraction_f1(register, facts)
    assert set(scored) == {"all", "policy_schedule"}
    assert (scored["all"].tp, scored["all"].fp, scored["all"].fn) == (1, 2, 2)
    assert scored["all"].f1 == pytest.approx(1 / 3)
    assert score.extraction_f1(register, []) == {}


# ------------------------------------------------------------------------------- end to end


def _question(
    id: str,
    *,
    lane: str = "retrieval",
    set_id: str = "A",
    text: str = "q",
    kind: str = "fact",
    value: str = "2027-04-11",
    doc: str = "b1-0001",
    page: int = 1,
) -> Question:
    from eval.sets_io import Expected

    if kind == "abstain":
        return Question(id, "B", lane, text, Expected("abstain"))
    return Question(
        id,
        "A" if set_id == "A" else "B",
        lane,
        text,
        Expected("fact", "insurance_agent", "expiry_date", value),
        doc,
        page,
    )


def _passage(chunk_id: int, doc: str, page: int, text: str = "…") -> Passage:
    return Passage(chunk_id, f"uuid-{doc}", page, text, 0.5, document_name=f"{doc}.pdf")


def _answered(text: str, doc: str, page: int) -> Answer:
    citation = Citation(f"uuid-{doc}", f"{doc}.pdf", page, f"{doc}.pdf, page {page}")
    return Answer(text, [citation.text], claims=[Cited(text, (1,), [citation])])


class FakeGraph:
    """Answers from a table. `retriever.search` is called so the recorder sees passages."""

    def __init__(self, recorder: harness.Recorder, answers: dict[str, Answer]) -> None:
        self.recorder = recorder
        self.answers = answers

    def ask(
        self, question: str, *, thread_id: str = "local", history: Sequence[tuple[str, str]] = ()
    ) -> Answer:
        found = self.recorder.retriever.search(question, candidates=40)
        self.recorder.reranker.rerank(question, found, keep=6)
        return self.answers[question]


class FakeRetriever:
    def __init__(self, by_question: dict[str, list[Passage]]) -> None:
        self.by_question = by_question

    def search(self, question: str, *, candidates: int) -> list[Passage]:
        return self.by_question.get(question, [])


class KeepAll:
    def rerank(self, question: str, passages: list[Passage], *, keep: int) -> list[Passage]:
        return passages[:keep]


def test_the_code_scored_metrics_come_out_as_arithmetic_says(tmp_path: Path) -> None:
    questions = [
        _question("a-1", text="when does the car policy expire?"),
        _question("a-2", text="what is the premium?", value="1284.00"),
        _question("a-3", text="what is the excess?", value="750.00"),
        _question("b-1", kind="abstain", text="travel insurance?"),
        _question("b-2", kind="abstain", text="named driver?"),
    ]
    passages = {
        "when does the car policy expire?": [_passage(1, "b1-0001", 1), _passage(2, "b1-0002", 1)],
        "what is the premium?": [_passage(1, "b1-0001", 1)],
        "what is the excess?": [_passage(9, "b1-0003", 2)],  # the wrong document
        "travel insurance?": [_passage(2, "b1-0002", 1)],
        "named driver?": [],
    }
    answers = {
        "when does the car policy expire?": _answered("It expires on 11 April 2027.", "b1-0001", 1),
        "what is the premium?": _answered(
            "The premium is $1,284.00.", "b1-0002", 1
        ),  # right value, wrong page
        "what is the excess?": Answer("I can't answer that from your documents.", abstained=True),
        "travel insurance?": Answer("I can't answer that from your documents.", abstained=True),
        "named driver?": _answered(
            "The named driver is Marcus.", "b1-0001", 1
        ),  # should have abstained
    }
    recorder = harness.Recorder(
        harness.RecordingRetriever(FakeRetriever(passages)), harness.RecordingReranker(KeepAll())
    )
    traces = harness.trace_all(FakeGraph(recorder, answers), recorder, questions)

    assert [t.candidates for t in traces] == [2, 1, 1, 1, 0]
    assert [len(t.contexts) for t in traces] == [2, 1, 1, 1, 0]

    scored = score.grade(traces)
    assert [s.outcome for s in scored] == [
        "answered",
        "answered",
        "abstained",
        "abstained",
        "answered",
    ]
    assert [s.correct for s in scored] == [True, True, False, None, None]
    assert [s.cited for s in scored] == [True, False, False, None, None]
    assert [s.shown for s in scored] == [True, True, False, None, None]

    metrics, also, why = score.summarise(
        scored, extraction={"all": score.F1(9, 1, 0)}, runtime=None, judged=False
    )
    assert tuple(metrics) == score.METRIC_KEYS
    assert metrics["abstention_rate"] == 0.5
    assert metrics["extraction_f1"] == pytest.approx(0.9474, abs=1e-4)
    assert metrics["context_recall"] is None and "judge" in why["context_recall"]
    assert metrics["obligation_precision"] is None and "W7" in why["obligation_precision"]
    assert also["fact_accuracy"] == pytest.approx(2 / 3, abs=1e-4)
    assert also["citation_hit"] == 0.5
    assert also["page_shown"] == pytest.approx(2 / 3, abs=1e-4)
    assert also["abstention_precision"] == 0.5  # two abstentions, one of them on Set B
    assert also["n"] == {"A": 3, "B": 2, "C": 0}

    # The per-question lines and the table are plain data: they survive JSON and a terminal.
    lines = [s.as_dict() for s in scored]
    json.loads(json.dumps(lines))
    assert lines[0]["contexts"] == ["document:1", "document:2"]
    assert lines[0]["citations"] == ["b1-0001.pdf, page 1"]
    printed = _table(metrics, why)
    assert "abstention_rate" in printed and "✗" in printed and "✓" in printed


def test_runtime_numbers_are_read_from_the_benchmark_file_not_typed() -> None:
    numbers, source = _runtime_numbers(ROOT / "eval" / "results", 16384)
    assert source.endswith("hardware.md")
    assert numbers["decode_tok_s"] == 130.0
    assert numbers["peak_vram_gb"] == 7.4


def test_reference_for_a_fact_question_states_the_value_in_its_printed_forms() -> None:
    reference = score.reference_for(_question("a-1"), "")
    assert reference.startswith("The expiry date is 2027-04-11")
    assert "11 april 2027" in reference
    passage = _question("a-2", kind="fact")
    assert (
        score.reference_for(
            Question("p", "A", "x", "q", passage.expected.__class__("passage"), "b1-0001", 2),
            "page two",
        )
        == "page two"
    )
