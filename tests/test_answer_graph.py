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
from collections.abc import Iterator
from typing import Any
from uuid import uuid4

import pytest

from core.graph.answer import Abstained, AnswerGraph, Finished, Reading, Refused, Sentence
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

    def constrained_stream(
        self,
        system: str,
        prompt: str,
        schema: dict[str, Any],
        *,
        temperature: float = 0.0,
    ) -> Iterator[str]:
        """The same scripted reply, in five-character pieces.

        Deliberately chopped: every test in this file now runs through the real
        `SentenceScanner`, so a sentence that only survives when the whole reply arrives at once
        fails here rather than on the demonstration machine.
        """
        reply = self._replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        text = json.dumps(reply)
        for start in range(0, len(text), 5):
            yield text[start : start + 5]

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 768 for _ in texts]

    def embed_query(self, text: str) -> list[float]:
        return self.embed([text])[0]


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


# --------------------------------------------------------------------------- the stream
#
# `ask` is `stream` drained, so everything above already exercises the streaming path. What
# these add is the *order*, which is the part a screen depends on and a collected answer cannot
# show: that a sentence is released before the reply has finished arriving, and that nothing
# released is ever taken back.


def events(client: Any, question: str, passages: list[Passage] | None = None) -> list[Any]:
    return list(build(client, passages).stream(question))


def test_a_sentence_is_released_before_the_answer_has_finished() -> None:
    """The promise the Ask surface is built on. Two sentences, two separate events, in order."""
    client = ScriptedOllama(
        {"intent": "explain"},
        {
            "sentences": [
                {"text": "The annual premium is SGD 1,248.90.", "supports": [1]},
                {"text": "Wear and tear is excluded.", "supports": [2]},
            ]
        },
    )
    stream = events(client, "what does it cost and what is excluded?")

    assert isinstance(stream[0], Reading)
    assert stream[0].passages_read == 2
    assert [event.text for event in stream if isinstance(event, Sentence)] == [
        "The annual premium is SGD 1,248.90.",
        "Wear and tear is excluded.",
    ]
    assert isinstance(stream[-1], Finished)


def test_every_sentence_arrives_with_its_citations_already_on_it() -> None:
    """Nothing is added afterwards, so a chip can never appear late or change."""
    client = ScriptedOllama(
        {"intent": "explain"},
        {"sentences": [{"text": "The annual premium is SGD 1,248.90.", "supports": [1]}]},
    )
    sentence = next(e for e in events(client, "premium?") if isinstance(e, Sentence))

    assert [citation.text for citation in sentence.citations] == ["renewal-notice.pdf, page 1"]
    assert sentence.chunk_ids == (11,)
    # The id came off the passage. Nothing had to go and find the document again by name.
    assert sentence.citations[0].document_id == DOC
    assert sentence.citations[0].page == 1


def test_a_sentence_the_gate_drops_is_never_yielded_at_all() -> None:
    """Not yielded and then withdrawn — never yielded. There is no retraction event by design."""
    client = ScriptedOllama(
        {"intent": "explain"},
        {
            "sentences": [
                {"text": "The annual premium is SGD 1,248.90.", "supports": [1]},
                {"text": "It is good value.", "supports": []},
                {"text": "The excess is SGD 500.", "supports": [9]},
            ]
        },
    )
    stream = events(client, "tell me about the policy")

    said = [event.text for event in stream if isinstance(event, Sentence)]
    assert said == ["The annual premium is SGD 1,248.90."]
    assert "good value" not in " ".join(said)
    assert stream[-1].dropped == 2


def test_weak_evidence_abstains_without_running_the_model() -> None:
    """The floor is a retrieval question, so it is asked first. The scripted answer is left
    unused — if the model had been called, `ScriptedOllama` would have popped it."""
    weak = [Passage(11, DOC, 1, "unrelated", 0.2, "note.pdf", pack_id="insurance_agent")]
    client = ScriptedOllama({"intent": "explain"}, {"sentences": [{"text": "no", "supports": [1]}]})
    stream = events(client, "what is my excess?", weak)

    assert len(stream) == 1
    assert isinstance(stream[0], Abstained)
    assert "not close enough" in stream[0].reason
    assert client._replies == [{"sentences": [{"text": "no", "supports": [1]}]}], (
        "the model was asked a question whose answer was already known to be unusable"
    )


def test_a_request_to_act_yields_only_a_refusal() -> None:
    stream = events(ScriptedOllama({"intent": "act"}), "renew it for me")

    assert len(stream) == 1
    assert isinstance(stream[0], Refused)


def test_a_model_that_dies_mid_answer_keeps_what_it_already_proved() -> None:
    """A sentence that passed the gate was true when it passed. Losing the connection afterwards
    does not make it untrue, so it is not withdrawn."""

    class DiesAfterFirstSentence(ScriptedOllama):
        def constrained_stream(self, *args: Any, **kwargs: Any) -> Iterator[str]:
            reply = {"sentences": [{"text": "The premium is SGD 1,248.90.", "supports": [1]}]}
            text = json.dumps(reply)
            yield text[: text.index("}]") + 2]
            raise ModelUnavailable("the model stopped answering")

    stream = events(DiesAfterFirstSentence({"intent": "explain"}), "premium?")

    assert [e.text for e in stream if isinstance(e, Sentence)] == ["The premium is SGD 1,248.90."]
    assert isinstance(stream[-1], Finished)


def test_a_model_that_dies_before_any_sentence_abstains() -> None:
    class DiesImmediately(ScriptedOllama):
        def constrained_stream(self, *args: Any, **kwargs: Any) -> Iterator[str]:
            raise ModelUnavailable("Ollama is not running")
            yield ""  # pragma: no cover - makes this a generator

    stream = events(DiesImmediately({"intent": "explain"}), "premium?")

    assert isinstance(stream[-1], Abstained)
    assert "not running" in stream[-1].reason


# ------------------------------------------------------------------- whose guardrails apply
#
# The pack that owns the best passage decides the abstain floor and signs the answer. It used
# to be the pack owning the most passages, which stamped a tax disclaimer on an insurance
# answer whenever the vault happened to hold more payslips than policies.


def passage(chunk_id: int, score: float, pack_id: str) -> Passage:
    return Passage(chunk_id, DOC, 1, "text", score, "doc.pdf", pack_id=pack_id)


def test_the_best_passage_chooses_the_pack_even_when_it_is_outnumbered() -> None:
    evidence = [
        passage(1, 0.88, "insurance_agent"),
        passage(2, 0.51, "iras_tax"),
        passage(3, 0.49, "iras_tax"),
        passage(4, 0.47, "iras_tax"),
    ]
    client = ScriptedOllama(
        {"intent": "explain"},
        {"sentences": [{"text": "It expires on 30 November 2026.", "supports": [1]}]},
    )
    answer = build(client, evidence).ask("when does the motor policy expire?")

    assert answer.grounded
    assert "insurance" in answer.disclaimer.lower(), (
        "an insurance answer was signed with another pack's disclaimer"
    )


def test_a_passage_belonging_to_no_pack_does_not_choose_one() -> None:
    """The RAG core answers from any document. A chunk that belongs to nothing cannot pick the
    disclaimer, so the pack comes from the best passage that names one."""
    evidence = [
        Passage(1, DOC, 1, "text", 0.95, "loose.pdf"),
        passage(2, 0.60, "insurance_agent"),
    ]
    client = ScriptedOllama(
        {"intent": "explain"},
        {"sentences": [{"text": "It expires on 30 November 2026.", "supports": [2]}]},
    )
    answer = build(client, evidence).ask("when?")

    assert "insurance" in answer.disclaimer.lower()


def test_the_floor_that_is_applied_belongs_to_the_passage_that_has_to_clear_it() -> None:
    """insurance_agent declares 0.45; iras_tax is looser. A best passage at 0.44 is insurance's
    to reject, and it must not be let through on the tax floor because tax had more passages."""
    evidence = [
        passage(1, 0.44, "insurance_agent"),
        passage(2, 0.43, "iras_tax"),
        passage(3, 0.42, "iras_tax"),
    ]
    client = ScriptedOllama({"intent": "explain"}, {"sentences": []})
    stream = events(client, "what is my excess?", evidence)

    assert isinstance(stream[0], Abstained)
    assert "0.45" in stream[0].reason, stream[0].reason
