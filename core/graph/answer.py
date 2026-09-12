"""Router → retrieve → rerank → decide → answer, one verified sentence at a time.

A LangGraph state machine, because the interesting part is the *order* and the fact that one of
the edges goes to "abstain". Retrieval is one tool call we wrote ourselves; there is no agent
deciding what to do next.

    route ──► retrieve ──► rerank ──┬──► abstain        (the evidence is not good enough)
       │                            └──► answer ──► one Sentence event per kept claim
       └──► refuse                                      (a request to act, not to explain)

`route` exists for one reason worth stating: `never_acts` is `Literal[True]` in every pack
manifest, and a question like "renew it for me" must be refused at the top of the graph rather
than politely declined at the bottom by a model that might not.

**`stream` is the implementation and `ask` drains it.** There is one path through this file, so
`scripts/ask.py` and the Ask screen cannot come to different conclusions about the same
question — the same thing rule 6 protects for field names, applied to the answer.

**The gate moved either side of generation, and that is what makes streaming honest.** The
question "is this evidence worth answering from" is settled by retrieval, so it is asked
*before* the model runs — which also means a question the vault cannot answer costs a retrieval
instead of a full pass through a 4B model whose output is discarded. The question "can this
sentence be kept" depends on nothing but that sentence, so it is asked the moment the sentence
is finished. Nothing reaches a screen before it has passed both. An interface built on this
never shows a claim it has to withdraw, which is rule 3 holding at the pixel rather than only
in the response body.

The answering is therefore not a LangGraph node: a node returns a state dict, and this yields.
The graph declares the part that is a pipeline — routing and gathering evidence — and stops
there.

The checkpointer is `MemorySaver`, not `PostgresSaver`. The Postgres checkpointer creates its
own tables, and creating tables at runtime is exactly what rule 4 forbids — `db/migrations/` is
a separate reviewed pull request. The swap is one line once that migration lands.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any, Literal, TypedDict

from core.graph.gate import Claim, check_one, precheck
from core.graph.ports import Passage, Reranker, Retriever
from core.graph.scope import HouseholdScope
from core.graph.sentences import SentenceScanner
from core.packs import InstalledPack, installed_packs
from core.runtime.ollama import ModelUnavailable, Ollama

log = logging.getLogger(__name__)

CANDIDATES = 40  # what retrieval returns
KEEP = 6  # what survives reranking and is actually read

ROUTE_SYSTEM = (
    "You decide what kind of request you are looking at. 'explain' means the person wants to "
    "know what their documents say. 'act' means they are asking you to do something in the "
    "world: pay, renew, book, file, cancel, send or sign. Asking what something costs is "
    "explain; asking you to pay it is act."
)

_ROUTE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"intent": {"type": "string", "enum": ["explain", "act"]}},
    "required": ["intent"],
}

ANSWER_SYSTEM = (
    "You answer only from the numbered passages you are given. Every sentence you write must "
    "list the passage numbers it came from. If the passages do not answer the question, you "
    "return no sentences and say which document would have answered it. You never use "
    "knowledge from outside the passages, and you never soften a number."
)

_ANSWER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "sentences": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "supports": {"type": "array", "items": {"type": "integer", "minimum": 1}},
                },
                "required": ["text", "supports"],
            },
        },
        "missing": {"type": "string"},
    },
    "required": ["sentences"],
}

REFUSAL = (
    "I can explain what your documents say, but I do not act on them. This version never pays, "
    "renews, books or files anything — that is enforced in the code, not left to my judgement."
)


class State(TypedDict, total=False):
    """What the graph carries. It ends at the evidence; the answer is streamed, not stated."""

    question: str
    intent: str
    passages: list[Passage]
    reranked: list[Passage]


@dataclass(frozen=True, slots=True)
class Citation:
    """A passage, named the way a person cites it and identified the way a link needs.

    Both, deliberately. `text` is what a terminal prints and what a chip is labelled with;
    `document_id` and `page` are what makes that chip open the page. Keeping them together from
    the moment the passage is retrieved is what stops the interface having to find the document
    again by name — a lookup that has to guess when two files share one.
    """

    document_id: Any
    document_name: str
    page: int
    text: str  # "policy.pdf, page 1"


@dataclass(frozen=True, slots=True)
class Cited:
    """One sentence and the passages it was traced to. What rule 3 looks like as data.

    `Answer.text` joins these for a terminal; a screen wants them apart, so that a person can
    put a finger on one sentence and see the page it came from rather than a list at the end.
    """

    text: str
    chunk_ids: tuple[int, ...]
    citations: list[Citation] = field(default_factory=list)


# ------------------------------------------------------------------------------- the events
#
# What a caller receives, in the order it happens. A screen renders each as it arrives; `ask`
# collects them into one `Answer`. Every one of them is terminal except `Reading` and
# `Sentence`, so a consumer can stop at the first of the others.


@dataclass(frozen=True, slots=True)
class Reading:
    """Evidence gathered, floor cleared, the model is now writing. Nothing is claimed yet.

    `person` is set when the question was first-person and the evidence was narrowed to one
    member of the household. It is shown for the same reason a citation is: the defence against
    answering about the wrong person is showing whose answer this is, not being careful.
    """

    passages_read: int
    person: str | None = None


@dataclass(frozen=True, slots=True)
class Sentence:
    """One sentence that has passed the gate, with the citations it passed on.

    It will not be withdrawn, reworded or re-cited. That promise is the reason the gate was
    split in two, and it is the whole difference between this and streaming raw tokens.
    """

    text: str
    chunk_ids: tuple[int, ...]
    citations: list[Citation]


@dataclass(frozen=True, slots=True)
class Abstained:
    reason: str
    missing: str
    passages_read: int
    dropped: int
    person: str | None = None


@dataclass(frozen=True, slots=True)
class Refused:
    text: str = ""


@dataclass(frozen=True, slots=True)
class Finished:
    """Everything that is only knowable once the last sentence is in."""

    citations: list[str]
    disclaimer: str
    passages_read: int
    dropped: int
    person: str | None = None


Event = Reading | Sentence | Abstained | Refused | Finished


@dataclass(frozen=True, slots=True)
class Answer:
    text: str
    citations: list[str] = field(default_factory=list)
    abstained: bool = False
    refused: bool = False
    passages_read: int = 0
    dropped: int = 0
    disclaimer: str = ""
    claims: list[Cited] = field(default_factory=list)
    reason: str = ""  # why it abstained, when it did
    missing: str = ""  # what document would have answered it
    person: str = ""  # whose documents this was narrowed to, when it was

    @property
    def grounded(self) -> bool:
        return not self.abstained and not self.refused


def _numbered(passages: list[Passage]) -> str:
    return "\n\n".join(
        f"[{index}] ({passage.cite()}) {passage.context_prefix}\n{passage.text}"
        for index, passage in enumerate(passages, start=1)
    )


def _pack_for(passages: list[Passage], packs: tuple[InstalledPack, ...]) -> InstalledPack | None:
    """The pack owning the best-scoring passage. Its guardrails govern the answer.

    Packs declare different abstain floors — insurance is stricter than tax — and a different
    disclaimer, so this is not a detail: it decides both what it takes to answer and what the
    answer is signed with.

    **The best passage, not the most passages.** The majority rule this replaced went wrong in
    the ordinary case: ask about a motor policy in a vault that mostly holds payslips, and five
    retrieved passages can be three tax ones and two insurance ones — so the answer came back
    stamped with a tax disclaimer even though every sentence in it was traced to the renewal
    notice. Counting evidence measured what the household files most of, which is not what the
    question was about.

    Taking the best passage also makes the floor coherent with itself. `precheck` compares that
    same passage's score against the floor, so the passage that has to clear the bar is now the
    passage whose pack sets it.

    A passage with no pack is skipped rather than counted: the RAG core answers from any
    document, pack or no pack, and a chunk that belongs to nothing cannot be the one that
    chooses a disclaimer. When nothing in the evidence names a pack, the caller falls back to
    the strictest floor rather than the loosest.
    """
    if not packs:
        return None
    owned = [passage for passage in passages if passage.pack_id]
    if not owned:
        return max(packs, key=lambda p: p.manifest.guardrails.abstain_below)
    winner = max(owned, key=lambda passage: passage.score).pack_id
    for installed in packs:
        if installed.id == winner:
            return installed
    # The evidence names a pack that is not installed any more. Strictest, not loosest.
    return max(packs, key=lambda p: p.manifest.guardrails.abstain_below)


class AnswerGraph:
    """Built once, asked many times. Holds no connection: retrieval does."""

    def __init__(
        self,
        client: Ollama,
        retriever: Retriever,
        reranker: Reranker,
        *,
        candidates: int = CANDIDATES,
        keep: int = KEEP,
        household: HouseholdScope | None = None,
    ) -> None:
        self._client = client
        self._retriever = retriever
        self._reranker = reranker
        self._candidates = candidates
        self._keep = keep
        # Injected rather than built here, because this class holds no connection and scoping
        # needs one. `None` is the honest state of a fresh install: nobody has said who they
        # are yet, so no question is first-person and every answer is about the household.
        self._household = household
        self._graph = self._build()

    # ------------------------------------------------------------------------ the nodes

    def route(self, state: State) -> State:
        try:
            reply = self._client.constrained(ROUTE_SYSTEM, state["question"], _ROUTE_SCHEMA).json()
            intent = str(reply.get("intent", "explain"))
        except ModelUnavailable:
            intent = "explain"  # a router that cannot run must not block an explanation
        return {"intent": intent if intent in {"explain", "act"} else "explain"}

    def retrieve(self, state: State) -> State:
        return {"passages": self._retriever.search(state["question"], candidates=self._candidates)}

    def rerank(self, state: State) -> State:
        passages = state.get("passages") or []
        return {"reranked": self._reranker.rerank(state["question"], passages, keep=self._keep)}

    def _claim(self, item: dict[str, Any], passages: list[Passage]) -> Claim:
        """One streamed sentence object, turned into the thing the gate understands.

        The model cites 1-based positions in the prompt it was given; the gate checks real chunk
        ids. A position outside the range is silently not translated, which means the claim ends
        up with fewer supports than the model named — and `check_one` then drops it for citing a
        passage that was not retrieved, which is the correct outcome and the one rule 3 wants.
        """
        text = str(item.get("text", "")).strip()
        numbers = [n for n in item.get("supports") or [] if isinstance(n, int)]
        supports = tuple(passages[n - 1].chunk_id for n in numbers if 1 <= n <= len(passages))
        if len(supports) != len(numbers):
            supports = (*supports, -1)  # an id no passage has, so the gate sees it invented one
        return Claim(text, supports)

    # ------------------------------------------------------------------------ the graph

    def _build(self) -> Any:
        """Routing and evidence. The answering is not a node — it yields, and a node returns."""
        from langgraph.checkpoint.memory import MemorySaver
        from langgraph.graph import END, START, StateGraph

        builder: Any = StateGraph(State)
        builder.add_node("route", self.route)
        builder.add_node("retrieve", self.retrieve)
        builder.add_node("rerank", self.rerank)

        builder.add_edge(START, "route")
        builder.add_conditional_edges(
            "route",
            lambda state: "refuse" if state.get("intent") == "act" else "explain",
            {"refuse": END, "explain": "retrieve"},
        )
        builder.add_edge("retrieve", "rerank")
        builder.add_edge("rerank", END)
        return builder.compile(checkpointer=MemorySaver())

    # ------------------------------------------------------------------------- the call

    def stream(self, question: str, *, thread_id: str = "local") -> Iterator[Event]:
        """The implementation. Yields each sentence once it has passed the gate, never before.

        The order is worth reading as a sequence of promises. Nothing is claimed until `Reading`;
        after that every `Sentence` is final; and exactly one of `Abstained`, `Refused` or
        `Finished` ends the stream.
        """
        final: State = self._graph.invoke(
            {"question": question}, {"configurable": {"thread_id": thread_id}}
        )
        if final.get("intent") == "act":
            yield Refused(REFUSAL)
            return

        passages = final.get("reranked") or []

        # Whose question is this? Asked after reranking, so the filter runs over the passages
        # that were actually going to be used, and before the floor, so an abstention about the
        # wrong person is not reported as weak evidence. See `core/graph/scope.py`.
        scoped = self._household.apply(question, passages) if self._household else None
        person = scoped.person_name if scoped is not None and scoped.scoped else None
        if scoped is not None and scoped.scoped:
            passages = scoped.passages

        # The interesting failure, and the one worth its own sentence: they asked about their
        # own policy and the vault holds somebody else's. Saying so is more use than a number
        # they did not ask for, and it tells them something they did not know.
        if scoped is not None and scoped.empty_for_owner:
            others = ", ".join(scoped.dropped_people)
            yield Abstained(
                f"nothing filed under {scoped.person_name} answers that",
                (
                    f"There are documents for {others}, but none for {scoped.person_name}."
                    if others
                    else f"No document in your vault is filed under {scoped.person_name}."
                ),
                0,
                0,
                person,
            )
            return

        installed = _pack_for(passages, installed_packs())
        floor = installed.manifest.guardrails.abstain_below if installed else 0.42
        disclaimer = installed.manifest.guardrails.disclaimer.strip() if installed else ""

        # Asked before the model runs. A question the evidence cannot support costs a retrieval,
        # not a retrieval and a generation that is then thrown away.
        refusal = precheck(passages, abstain_below=floor)
        if refusal is not None:
            yield Abstained(refusal, "", len(passages), 0, person)
            return

        yield Reading(len(passages), person)

        by_id = {passage.chunk_id: passage for passage in passages}
        retrieved = set(by_id)
        # Naming the asker is not what makes the answer right — the passages were already
        # narrowed to them — it is what stops the model writing "Marcus's premium is" when the
        # question said "my". The filter does the work; this only does the wording.
        whose = (
            f"The person asking is {person}. 'My', 'I' and 'mine' mean them.\n\n" if person else ""
        )
        prompt = f"{whose}Question: {question}\n\nPassages:\n{_numbered(passages)}"
        scanner = SentenceScanner()
        kept: list[str] = []
        dropped = 0

        try:
            for delta in self._client.constrained_stream(ANSWER_SYSTEM, prompt, _ANSWER_SCHEMA):
                for item in scanner.feed(delta):
                    claim = self._claim(item, passages)
                    why = check_one(claim, retrieved)
                    if why is not None:
                        if why != "empty":
                            dropped += 1
                            log.info("gate dropped a sentence (%s): %.80s", why, claim.text)
                        continue
                    citations: list[Citation] = []
                    for chunk_id in claim.supports:
                        passage = by_id[chunk_id]
                        cited = Citation(
                            document_id=passage.document_id,
                            document_name=passage.document_name,
                            page=passage.page,
                            text=passage.cite(),
                        )
                        if all(cited.text != seen.text for seen in citations):
                            citations.append(cited)
                    kept.extend(citation.text for citation in citations)
                    yield Sentence(claim.text, tuple(claim.supports), citations)
        except ModelUnavailable as error:
            # Sentences already yielded were verified and stay said. What follows is the honest
            # account of why there are no more of them.
            if kept:
                yield Finished(sorted(set(kept)), disclaimer, len(passages), dropped, person)
            else:
                yield Abstained(str(error), "", len(passages), dropped, person)
            return

        if not kept:
            # The model wrote nothing, or nothing it wrote could be traced to a document. Its own
            # `missing` says which document would have answered, when it offered one.
            yield Abstained(
                "nothing in the answer could be traced to a document",
                scanner.missing(),
                len(passages),
                dropped,
                person,
            )
            return

        yield Finished(sorted(set(kept)), disclaimer, len(passages), dropped, person)

    def ask(self, question: str, *, thread_id: str = "local") -> Answer:
        """Every event, collected. `scripts/ask.py` and the screen ask the same question of the
        same code, so they cannot disagree about the answer."""
        claims: list[Cited] = []
        passages_read = 0

        for event in self.stream(question, thread_id=thread_id):
            if isinstance(event, Refused):
                return Answer(event.text, refused=True)
            if isinstance(event, Reading):
                passages_read = event.passages_read
            elif isinstance(event, Sentence):
                claims.append(Cited(event.text, event.chunk_ids, event.citations))
            elif isinstance(event, Abstained):
                text = f"I can't answer that from your documents: {event.reason}."
                if event.missing:
                    text = f"{text} {event.missing}"
                return Answer(
                    text,
                    abstained=True,
                    passages_read=event.passages_read,
                    dropped=event.dropped,
                    reason=event.reason,
                    missing=event.missing,
                    person=event.person or "",
                )
            elif isinstance(event, Finished):
                lines = [
                    f"{claim.text} [{'; '.join(c.text for c in claim.citations)}]"
                    if claim.citations
                    else claim.text
                    for claim in claims
                ]
                return Answer(
                    " ".join(lines),
                    citations=event.citations,
                    passages_read=event.passages_read,
                    dropped=event.dropped,
                    disclaimer=event.disclaimer,
                    claims=claims,
                    person=event.person or "",
                )

        # Unreachable: `stream` always ends on a terminal event. Kept because a silent `None`
        # here would be the worst possible failure in this file.
        return Answer(
            "I can't answer that from your documents: the answer did not finish.",
            abstained=True,
            passages_read=passages_read,
            reason="the answer did not finish",
        )


Intent = Literal["explain", "act"]
