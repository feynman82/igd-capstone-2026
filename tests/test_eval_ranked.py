"""The replay fields, from passages alone. Real packs, fake passages: which pack governs is
the graph's decision, so the test asks the installed manifests rather than restating them."""

from __future__ import annotations

import pytest

from core.graph.answer import Answer
from core.graph.ports import Passage
from core.packs import installed_packs
from eval import harness, ranked
from eval.sets_io import Expected, Question

PACKS = installed_packs()
INSURANCE = next(p for p in PACKS if p.id == "insurance_agent")
TAX = next(p for p in PACKS if p.id == "iras_tax")
POLICY = sorted(INSURANCE.manifest.answering.documents)[0]
RECEIPT = sorted(TAX.manifest.answering.documents)[0]


def _p(
    chunk: int, doc: str, score: float, doc_type: str, text: str = "…", page: int = 1
) -> Passage:
    return Passage(
        chunk, f"uuid-{doc}", page, text, score, document_name=f"{doc}.pdf", doc_type=doc_type
    )


def test_the_pack_that_speaks_for_the_best_passage_governs_with_its_own_floor() -> None:
    contexts = [_p(1, "b3-0001", 0.40, RECEIPT), _p(2, "b1-0001", 0.47, POLICY)]
    assert ranked.governing(contexts, PACKS) == (
        "insurance_agent",
        INSURANCE.manifest.guardrails.abstain_below,
    )


def test_evidence_no_pack_speaks_for_is_governed_by_the_core_floor() -> None:
    assert ranked.governing([_p(1, "x-1", 0.5, "no_such_type")], PACKS) == ("core", 0.42)


def test_no_evidence_has_no_governing_pack() -> None:
    assert ranked.governing([], PACKS) == (None, None)


def test_six_passages_from_two_documents_are_two_items_in_reranker_order() -> None:
    contexts = [
        _p(1, "b1-0001", 0.44, POLICY, "first policy passage", page=2),
        _p(2, "b3-0001", 0.41, RECEIPT, "receipt"),
        _p(3, "b1-0001", 0.49, POLICY, "second policy passage"),
        _p(4, "b3-0001", 0.39, RECEIPT),
        _p(5, "b1-0001", 0.30, POLICY),
        _p(6, "b3-0001", 0.43, RECEIPT),
    ]
    items = ranked.documents(contexts, [0.9, 0.2, 0.95, 0.1, 0.3, 0.25], PACKS)
    assert [i["doc"] for i in items] == ["b1-0001", "b3-0001"]
    policy, receipt = items
    # The quote and page are the reranker's first passage of the document; the scores are the
    # document's best, because the floor reads the best passage.
    assert (policy["quote"], policy["page"]) == ("first policy passage", 2)
    assert policy["cosine"] == 0.49 and policy["relevance"] == 0.95
    assert receipt["cosine"] == 0.43 and receipt["relevance"] == 0.25
    assert (policy["pack"], receipt["pack"]) == ("insurance_agent", "iras_tax")


def test_relevance_that_does_not_line_up_with_the_passages_is_not_guessed() -> None:
    items = ranked.documents([_p(1, "b1-0001", 0.5, POLICY)], [], PACKS)
    assert items[0]["relevance"] is None


def test_record_carries_the_four_fields_replay_reads() -> None:
    question = Question("a-1", "A", "retrieval", "q", Expected("fact", "x", "k", "v"), "b1-0001", 1)
    trace = harness.Trace(question, Answer("…"), (_p(1, "b1-0001", 0.47, POLICY),), 1, 1)
    fields = ranked.record(trace, PACKS)
    assert fields["best_score"] == 0.47
    assert fields["governing_pack"] == "insurance_agent"
    assert fields["floor_in_force"] == pytest.approx(0.45)
    assert [i["doc"] for i in fields["ranked"]] == ["b1-0001"]


def test_capped_names_core_questions_under_the_core_floor_only() -> None:
    lines = [
        {"id": "a", "governing_pack": "core", "best_score": 0.40},
        {"id": "b", "governing_pack": "core", "best_score": 0.42},
        {"id": "c", "governing_pack": "insurance_agent", "best_score": 0.30},
        {"id": "d", "governing_pack": None, "best_score": None},
    ]
    assert ranked.capped(lines) == ["a"]
