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
from uuid import UUID, uuid4

import pytest

from core.graph.answer import (
    ANSWER_SYSTEM,
    Abstained,
    AnswerGraph,
    Declined,
    Finished,
    Reading,
    Refused,
    Sentence,
)
from core.graph.gate import Claim, check
from core.graph.inventory import Holding
from core.graph.knowledge import categorise
from core.graph.ports import Passage
from core.packs import InstalledPack, pack
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
        self.prompts: list[str] = []
        self.systems: list[str] = []

    def constrained(
        self,
        system: str,
        prompt: str,
        schema: dict[str, Any],
        *,
        images: list[str] | None = None,
        temperature: float = 0.0,
    ) -> Generated:
        self.systems.append(system)
        self.prompts.append(prompt)
        # The understanding step, when a test did not script it: an empty reply, which the graph
        # reads as "search the question as asked". Most tests here are about the gate, not it.
        scripted = bool(self._replies) and isinstance(self._replies[0], dict)
        if "searches" in schema.get("properties", {}) and not (
            scripted and "searches" in self._replies[0]  # type: ignore[operator]
        ):
            return Generated("{}", "fake", 1)
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
        self.systems.append(system)
        self.prompts.append(prompt)
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


# ------------------------------------------------------------------ understanding the question
#
# 13 September: "if i had a fall, and warded for 1 night, does my insurance cover the cost?" put
# the right clause first at 0.416 and abstained under the 0.45 floor; the same question with "in
# the hospital" answered. The router now says the question in the document's words too, every
# phrasing is searched, and each passage keeps its best score.


class PhrasingRetriever:
    """Scores one passage differently depending on which phrasing found it."""

    def __init__(self, scores: dict[str, float]) -> None:
        self.scores = scores
        self.queries: list[str] = []

    def search(self, question: str, *, candidates: int) -> list[Passage]:
        self.queries.append(question)
        score = self.scores.get(question, 0.2)
        return [
            Passage(
                21,
                DOC,
                2,
                "4.1 Room and board for Inpatient Confinement.",
                score,
                "privatecare.pdf",
                pack_id="insurance_agent",
            )
        ]


ANSWERED = {"sentences": [{"text": "Room and board is reimbursed.", "supports": [1]}]}


def test_every_phrasing_is_searched_and_a_passage_keeps_its_best_score() -> None:
    asked = "if i had a fall, and warded for 1 night, does my insurance cover the cost?"
    search = "inpatient hospital confinement following an injury"
    retriever = PhrasingRetriever({asked: 0.416, search: 0.452})
    client = ScriptedOllama(
        {"intent": "explain"},
        {"question": asked, "searches": [search]},
        ANSWERED,
    )
    graph = AnswerGraph(client, retriever, PassThroughReranker())

    events = list(graph.stream(asked))

    # "warded" is in the pack's vocabulary, so the question as the policy prints it is searched too.
    printed = asked.replace("warded", "hospitalised as an inpatient")
    assert retriever.queries == [asked, printed, search], "the person's words are always searched"
    assert isinstance(events[0], Reading), "the document's wording cleared the floor"
    assert isinstance(events[-1], Finished)


def test_a_follow_up_is_understood_from_the_conversation_and_answered_whole() -> None:
    whole = "When does my private car insurance policy expire?"
    retriever = PhrasingRetriever({whole: 0.6})
    client = ScriptedOllama(
        {"intent": "explain"},
        {"question": whole, "searches": ["policy expiry date MV-2026-448120"]},
        ANSWERED,
    )
    graph = AnswerGraph(client, retriever, PassThroughReranker())

    list(
        graph.stream(
            "when does it expire?",
            history=[
                ("user", "what is my private car insurance policy?"),
                ("assistant", "MV-2026-448120 with Meridian Assurance."),
            ],
        )
    )

    route_prompt, understand_prompt, answer_prompt = client.prompts
    assert route_prompt == "when does it expire?"
    assert "Conversation so far" in understand_prompt
    assert "what is my private car insurance policy?" in understand_prompt
    assert f"Question: {whole}" in answer_prompt
    assert "(The person's own words: when does it expire?)" in answer_prompt
    assert whole in retriever.queries


def test_a_router_that_cannot_run_still_searches_the_question_as_asked() -> None:
    retriever = PhrasingRetriever({"what is my premium?": 0.8})
    client = ScriptedOllama(ModelUnavailable("the router is down"), ANSWERED)
    graph = AnswerGraph(client, retriever, PassThroughReranker())

    events = list(graph.stream("what is my premium?"))

    assert retriever.queries == ["what is my premium?"]
    assert isinstance(events[-1], Finished)


def test_a_question_about_a_relation_nobody_holds_is_not_answered_from_the_owners_documents() -> (
    None
):
    """13 September: "how much is my son's life insurance?" came back as the owner's own policy,
    cited, with the owner called "your son"."""
    from core.graph.scope import Scoped

    class NoChild:
        def apply(self, question: str, passages: list[Passage]) -> Scoped:
            return Scoped(passages, None, unknown_relation="son")

    client = ScriptedOllama({"intent": "explain"})
    graph = AnswerGraph(
        client,
        FixedRetriever(PASSAGES),
        PassThroughReranker(),
        household=NoChild(),  # type: ignore[arg-type]
    )

    [event] = list(graph.stream("how much is my son's life insurance?"))

    assert isinstance(event, Abstained)
    assert "who your son is" in event.reason
    assert len(client.prompts) == 2, "routed and understood, and the answer model never asked"


def test_a_request_to_act_is_refused_before_anything_is_rewritten_or_searched() -> None:
    retriever = PhrasingRetriever({})
    client = ScriptedOllama({"intent": "act"})
    graph = AnswerGraph(client, retriever, PassThroughReranker())

    [event] = list(graph.stream("ok renew it for me"))

    assert isinstance(event, Refused)
    assert retriever.queries == []
    assert client.prompts == ["ok renew it for me"]


def test_a_question_about_a_parent_names_them_as_who_it_is_about_and_carries_todays_date() -> None:
    """13 September: "is my dad's hospital cover still active?" was scoped to Lim Ah Kow, and the
    model was told he was the one asking and not told the date, and wrote nothing."""
    from datetime import date

    from core.graph.scope import Scoped

    class Dad:
        def apply(self, question: str, passages: list[Passage]) -> Scoped:
            return Scoped(passages, "Lim Ah Kow", about="dad")

    client = ScriptedOllama({"intent": "explain"}, ANSWERED)
    graph = AnswerGraph(
        client,
        FixedRetriever(PASSAGES),
        PassThroughReranker(),
        household=Dad(),  # type: ignore[arg-type]
        today=date(2026, 9, 13),
    )

    list(graph.stream("is my dad's hospital cover still active?"))

    answer_prompt = client.prompts[-1]
    assert answer_prompt.startswith("Today is 13 September 2026.")
    assert "The question is about Lim Ah Kow, the asker's dad." in answer_prompt
    assert "The person asking is Lim Ah Kow" not in answer_prompt


# ------------------------------------------------------------------------------- the gate


def test_a_sentence_with_no_supporting_passage_is_dropped() -> None:
    verdict = check(
        [
            Claim("The premium is SGD 1,248.90.", ("document:11",)),
            Claim("It is good value.", ()),
        ],
        PASSAGES,
        abstain_below=0.45,
    )

    assert [claim.text for claim in verdict.grounded] == ["The premium is SGD 1,248.90."]
    assert verdict.dropped[0][1] == "no supporting passage"


def test_a_sentence_citing_a_passage_that_was_never_retrieved_is_dropped() -> None:
    verdict = check(
        [Claim("The excess is SGD 500.", ("document:99",))], PASSAGES, abstain_below=0.45
    )

    assert verdict.grounded == []
    assert verdict.abstained
    assert "not retrieved" in verdict.dropped[0][1]


def test_weak_evidence_abstains_before_anything_is_written() -> None:
    weak = [Passage(11, DOC, 1, "unrelated text", 0.2, "note.pdf")]
    verdict = check([Claim("Something.", ("document:11",))], weak, abstain_below=0.45)

    assert verdict.abstained
    assert "not close enough" in (verdict.reason or "")


def test_no_passages_at_all_abstains() -> None:
    verdict = check([Claim("Something.", ("document:1",))], [], abstain_below=0.45)

    assert verdict.abstained
    assert not verdict.has_answer


def test_a_grounded_claim_renders_its_document_and_page() -> None:
    claim = Claim("The premium is SGD 1,248.90.", ("document:11",))
    rendered = claim.with_citation({p.ref: p for p in PASSAGES})

    assert rendered.endswith("[renewal-notice.pdf, page 1]")


def test_a_claim_citing_the_same_document_twice_says_it_once() -> None:
    claim = Claim("It renews on 30 November 2026.", ("document:11", "document:11"))
    rendered = claim.with_citation({p.ref: p for p in PASSAGES})

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
    # Prints the date the scripted sentences state: a sentence stating a number no cited passage
    # prints is dropped by the gate, and these tests are about which pack signs, not about that.
    return Passage(
        chunk_id, DOC, 1, "Expires on 30 November 2026.", score, "doc.pdf", pack_id=pack_id
    )


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


# ----------------------------------------------------------------- what a pack makes of a question
#
# 13 September, live vault: "do i have dental insurance?" was answered with the hospital plan's
# dental exclusion; "warded for dengue 3 days, can claim?" was misread as "awarded" and cited the
# car policy's benefit table; "should i buy critical illness cover?" was explained, not declined.


def insurance() -> InstalledPack:
    return pack("insurance_agent")


def holding(name: str, printed: str, fact_id: int, document_id: UUID | None = None) -> Holding:
    categories = insurance().manifest.answering.categories
    assert categories is not None
    return Holding(
        document_id=document_id or uuid4(),
        document_name=name,
        pack_id="insurance_agent",
        doc_type="policy_schedule",
        title=f"Meridian Assurance, {printed}",
        subject="Marcus Lim Jun Wei",
        category=categorise(printed, categories),
        printed_name=printed,
        fact_id=fact_id,
        page=1,
        details=(("product_name", printed),),
    )


class FakeInventory:
    def __init__(self, held: list[Holding], quarantined: int = 0) -> None:
        self.held = held
        self._quarantined = quarantined

    def holdings(self, packs: Any) -> list[Holding]:
        return self.held

    def quarantined(self) -> int:
        return self._quarantined


def test_a_request_for_a_recommendation_is_declined_before_anything_is_searched() -> None:
    client = ScriptedOllama({"intent": "advise"})
    retriever = PhrasingRetriever({})
    graph = AnswerGraph(client, retriever, PassThroughReranker(), packs=[insurance()])

    got = list(graph.stream("should i buy critical illness cover?"))

    assert len(got) == 1 and isinstance(got[0], Declined)
    assert "recommend" in got[0].text
    assert got[0].disclaimer
    assert retriever.queries == []


def test_a_decline_offers_the_question_it_can_answer_without_answering_it() -> None:
    held = [holding("b1-0033.pdf", "CareShield Critical Illness Plan", 7)]
    graph = AnswerGraph(
        ScriptedOllama({"intent": "advise"}),
        PhrasingRetriever({}),
        PassThroughReranker(),
        packs=[insurance()],
        inventory=FakeInventory(held),
    )
    (declined,) = list(graph.stream("is my critical illness cover enough?"))
    assert isinstance(declined, Declined)
    assert declined.offer == "What does my CareShield Critical Illness Plan say?"


def test_a_kind_of_cover_nobody_holds_is_answered_with_what_is_on_file() -> None:
    held = [
        holding("b1-0001.pdf", "Private Car Insurance Policy", 501),
        holding("b1-0032.pdf", "PrivateCare Hospital and Surgical Plan", 502),
    ]
    client = ScriptedOllama({"intent": "explain"}, {"sentences": []})
    graph = AnswerGraph(
        client,
        FixedRetriever(PASSAGES),
        PassThroughReranker(),
        packs=[insurance()],
        inventory=FakeInventory(held, quarantined=1),
    )

    got = list(graph.stream("do i have dental insurance?"))

    sentences = [event for event in got if isinstance(event, Sentence)]
    assert sentences[0].text == "None of the 2 policies on file is a dental plan."
    assert {citation.kind for citation in sentences[0].citations} == {"inventory"}
    assert len(sentences[0].citations) == 2
    assert isinstance(got[-1], Finished) and got[-1].quarantined == 1


def test_no_is_still_said_when_the_passages_are_too_weak_to_answer_from() -> None:
    weak: list[Passage] = []
    held = [holding("b1-0001.pdf", "Private Car Insurance Policy", 501)]
    client = ScriptedOllama({"intent": "explain"})
    graph = AnswerGraph(
        client,
        FixedRetriever(weak),
        PassThroughReranker(),
        packs=[insurance()],
        inventory=FakeInventory(held),
    )

    got = list(graph.stream("how much is my pet insurance premium?"))

    assert [type(event) for event in got] == [Reading, Sentence, Finished]
    assert got[1].text == "None of the 1 policies on file is a pet policy."  # type: ignore[union-attr]


def test_passages_from_a_policy_of_another_kind_are_not_read() -> None:
    car_id, hospital_id = uuid4(), uuid4()
    held = [
        holding("b1-0001.pdf", "Private Car Insurance Policy", 501, car_id),
        holding("b1-0032.pdf", "PrivateCare Hospital and Surgical Plan", 502, hospital_id),
    ]
    passages = [
        Passage(
            1,
            car_id,
            1,
            "Third Party Property Damage limit.",
            0.60,
            "b1-0001.pdf",
            pack_id="insurance_agent",
        ),
        Passage(
            2,
            hospital_id,
            4,
            "Infectious diseases are covered as inpatient treatment.",
            0.55,
            "b1-0032.pdf",
            pack_id="insurance_agent",
        ),
    ]
    reply = {
        "sentences": [
            {"text": "Infectious diseases are covered as inpatient treatment.", "supports": [1]}
        ]
    }
    client = ScriptedOllama({"intent": "explain"}, reply)
    graph = AnswerGraph(
        client,
        FixedRetriever(passages),
        PassThroughReranker(),
        packs=[insurance()],
        inventory=FakeInventory(held),
    )

    got = list(graph.stream("warded for dengue 3 days, can claim?"))

    assert "Third Party Property Damage" not in client.prompts[-1]
    cited = [c.document_name for e in got if isinstance(e, Sentence) for c in e.citations]
    assert cited == ["b1-0032.pdf"]


def test_the_households_word_is_searched_the_way_the_policy_prints_it() -> None:
    retriever = PhrasingRetriever({})
    client = ScriptedOllama({"intent": "explain"})
    graph = AnswerGraph(client, retriever, PassThroughReranker(), packs=[insurance()])

    list(graph.stream("got warded 2 days, claimable?"))

    assert "got hospitalised as an inpatient 2 days, can claim?" in retriever.queries
    assert any("warded = hospitalised as an inpatient" in prompt for prompt in client.prompts)


def test_an_answer_stops_at_the_packs_sentence_limit() -> None:
    reply = {"sentences": [{"text": f"Clause {n} applies.", "supports": [1]} for n in range(1, 10)]}
    passage = Passage(
        11, DOC, 1, "Clauses 1 2 3 4 5 6 7 8 9 apply.", 0.8, "p.pdf", pack_id="insurance_agent"
    )
    graph = AnswerGraph(
        ScriptedOllama({"intent": "explain"}, reply),
        FixedRetriever([passage]),
        PassThroughReranker(),
        packs=[insurance()],
    )

    got = list(graph.stream("what applies?"))

    assert sum(isinstance(event, Sentence) for event in got) == 6
    assert isinstance(got[-1], Finished) and got[-1].truncated


def test_a_sentence_stating_a_number_the_passage_never_printed_is_not_said() -> None:
    reply = {"sentences": [{"text": "Three days pays SGD 3,000.", "supports": [1]}]}
    graph = AnswerGraph(
        ScriptedOllama({"intent": "explain"}, reply),
        FixedRetriever(PASSAGES),
        PassThroughReranker(),
        packs=[insurance()],
    )
    got = list(graph.stream("how much will I get for 3 days?"))
    assert isinstance(got[-1], Abstained) and got[-1].dropped == 1


def test_an_abstention_is_signed_with_the_packs_disclaimer() -> None:
    weak = [Passage(11, DOC, 1, "Nothing relevant.", 0.2, "p.pdf", pack_id="insurance_agent")]
    graph = AnswerGraph(
        ScriptedOllama({"intent": "explain"}),
        FixedRetriever(weak),
        PassThroughReranker(),
        packs=[insurance()],
    )
    (abstained,) = list(graph.stream("what about the thing?"))
    assert isinstance(abstained, Abstained) and "Financial Advisers Act" in abstained.disclaimer


def test_the_persona_speaks_before_the_rules_and_never_replaces_them() -> None:
    client = ScriptedOllama({"intent": "explain"}, ANSWERED)
    graph = AnswerGraph(
        client, FixedRetriever(PASSAGES), PassThroughReranker(), packs=[insurance()]
    )
    list(graph.stream("when does it renew?"))
    system = client.systems[-1]
    assert system.startswith(insurance().manifest.persona.system.strip())
    assert ANSWER_SYSTEM in system
