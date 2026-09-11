"""The grounding gate, and the graph's two ways of not answering.

Rule 3 says no claim without a citation. These tests are that rule: a sentence the model wrote
without a supporting passage does not reach the person, a sentence citing a passage that was
never retrieved does not reach the person, and a question the documents do not cover produces
an abstention with a reason rather than a plausible paragraph.

The retriever and the model are both fakes. That is the point — the behaviour under test is the
graph's, and it must hold whatever Lane B's hybrid retrieval eventually scores.
"""

from __future__ import annotations

import json
from typing import Any
from uuid import uuid4

import pytest

from core.graph.answer import AnswerGraph
from core.graph.gate import Claim, check
from core.graph.ports import Passage
from core.runtime.ollama import Generated, ModelUnavailable

DOC = uuid4()

PASSAGES = [
    Passage(
        chunk_id=11,
        document_id=DOC,
        page=1,
        text="Annual premium: SGD 1,248.90. Policy AIA-882401 renews on 30 November 2026.",
        score=0.81,
        document_name="renewal-notice.pdf",
        pack_id="insurance_agent",
    ),
    Passage(
        chunk_id=12,
        document_id=DOC,
        page=2,
        text="Excluded: damage caused by wear and tear.",
        score=0.55,
        document_name="renewal-notice.pdf",
        pack_id="insurance_agent",
    ),
]


class ScriptedOllama:
    """Returns the replies the test wrote, in order."""

    def __init__(self, *replies: dict[str, Any] | Exception) -> None:
        self._replies = list(replies)

    def constrained(
        self,
        system: str,
        prompt: str,
        schema: dict[str, Any],
        *,
        images: list[str] | None = None,
        temperature: float = 0.0,
    ) -> Generated:
        reply = self._replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return Generated(json.dumps(reply), "fake", 1)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 768 for _ in texts]


class FixedRetriever:
    def __init__(self, passages: list[Passage]) -> None:
        self.passages = passages

    def search(self, question: str, *, candidates: int) -> list[Passage]:
        return self.passages


class PassThroughReranker:
    def rerank(self, question: str, passages: list[Passage], *, keep: int) -> list[Passage]:
        return passages[:keep]


def build(client: Any, passages: list[Passage] | None = None) -> AnswerGraph:
    return AnswerGraph(
        client,
        FixedRetriever(PASSAGES if passages is None else passages),
        PassThroughReranker(),
    )


# ------------------------------------------------------------------------------- the gate


def test_a_sentence_with_no_supporting_passage_is_dropped() -> None:
    verdict = check(
        [Claim("The premium is SGD 1,248.90.", (11,)), Claim("It is good value.", ())],
        PASSAGES,
        abstain_below=0.45,
    )

    assert [claim.text for claim in verdict.grounded] == ["The premium is SGD 1,248.90."]
    assert verdict.dropped[0][1] == "no supporting passage"


def test_a_sentence_citing_a_passage_that_was_never_retrieved_is_dropped() -> None:
    verdict = check([Claim("The excess is SGD 500.", (99,))], PASSAGES, abstain_below=0.45)

    assert verdict.grounded == []
    assert verdict.abstained
    assert "not retrieved" in verdict.dropped[0][1]


def test_weak_evidence_abstains_before_anything_is_written() -> None:
    weak = [Passage(11, DOC, 1, "unrelated text", 0.2, "note.pdf")]
    verdict = check([Claim("Something.", (11,))], weak, abstain_below=0.45)

    assert verdict.abstained
    assert "not close enough" in (verdict.reason or "")


def test_no_passages_at_all_abstains() -> None:
    verdict = check([Claim("Something.", (1,))], [], abstain_below=0.45)

    assert verdict.abstained
    assert not verdict.has_answer


def test_a_grounded_claim_renders_its_document_and_page() -> None:
    claim = Claim("The premium is SGD 1,248.90.", (11,))
    rendered = claim.with_citation({p.chunk_id: p for p in PASSAGES})

    assert rendered.endswith("[renewal-notice.pdf, page 1]")


def test_a_claim_citing_the_same_document_twice_says_it_once() -> None:
    claim = Claim("It renews on 30 November 2026.", (11, 11))
    rendered = claim.with_citation({p.chunk_id: p for p in PASSAGES})

    assert rendered.count("renewal-notice.pdf") == 1


# ------------------------------------------------------------------------------ the graph


def test_a_grounded_question_is_answered_with_its_source() -> None:
    client = ScriptedOllama(
        {"intent": "explain"},
        {"sentences": [{"text": "The annual premium is SGD 1,248.90.", "supports": [1]}]},
    )
    answer = build(client).ask("what is the premium?")

    assert answer.grounded
    assert "SGD 1,248.90" in answer.text
    assert answer.citations == ["renewal-notice.pdf, page 1"]
    assert answer.disclaimer.startswith("Informational analysis")


def test_a_request_to_act_is_refused_at_the_router() -> None:
    client = ScriptedOllama({"intent": "act"})
    answer = build(client).ask("renew the policy for me")

    assert answer.refused
    assert not answer.grounded
    assert "do not act" in answer.text


def test_an_ungrounded_answer_abstains_rather_than_being_published() -> None:
    client = ScriptedOllama(
        {"intent": "explain"},
        {"sentences": [{"text": "Your excess is probably SGD 500.", "supports": []}]},
    )
    answer = build(client).ask("what is my excess?")

    assert answer.abstained
    assert "SGD 500" not in answer.text
    assert answer.dropped == 1


def test_nothing_retrieved_abstains_and_says_what_is_missing() -> None:
    client = ScriptedOllama({"intent": "explain"})
    answer = build(client, []).ask("what does my travel policy cover?")

    assert answer.abstained
    assert "vault" in answer.text or "documents" in answer.text


def test_a_model_that_is_not_running_abstains_rather_than_inventing() -> None:
    client = ScriptedOllama({"intent": "explain"}, ModelUnavailable("Ollama is not running"))
    answer = build(client).ask("what is the premium?")

    assert answer.abstained
    assert "not running" in answer.text


def test_the_router_failing_still_lets_a_question_be_answered() -> None:
    client = ScriptedOllama(
        ModelUnavailable("the router is down"),
        {"sentences": [{"text": "The annual premium is SGD 1,248.90.", "supports": [1]}]},
    )
    answer = build(client).ask("what is the premium?")

    assert answer.grounded, "a broken router must not block an explanation"


@pytest.mark.parametrize("supports", [[0], [7], [-1]])
def test_a_passage_number_outside_the_evidence_is_ignored(supports: list[int]) -> None:
    client = ScriptedOllama(
        {"intent": "explain"},
        {"sentences": [{"text": "An invented claim.", "supports": supports}]},
    )
    answer = build(client).ask("what is the premium?")

    assert answer.abstained
    assert "An invented claim." not in answer.text
