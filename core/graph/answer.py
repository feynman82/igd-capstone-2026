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
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Literal, TypedDict

from core.graph.gate import Claim, check_one, precheck
from core.graph.ports import Passage, Reranker, Retriever
from core.graph.scope import HouseholdScope, Scoped
from core.graph.sentences import SentenceScanner
from core.packs import InstalledPack, installed_packs
from core.runtime.ollama import ModelUnavailable, Ollama

log = logging.getLogger(__name__)

CANDIDATES = 40  # what retrieval returns
KEEP = 6  # what survives reranking and is actually read

HISTORY_TURNS = 6  # the most recent turns the understanding step reads to resolve a follow-up
HISTORY_CHARS = 600  # of each; an earlier answer is context, not evidence

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

# Understanding the question is its own model call, after routing. Measured on 13 September
# against the household vault:
#
# - **The question as the documents would say it.** "if i had a fall, and warded for 1 night,
#   does my insurance cover the cost?" put the right clause first at 0.416 and abstained under the
#   pack's 0.45 floor, while "…warded in the hospital…" answered. Searching the question as asked
#   *and* in the document's words, keeping each passage's best score, is what fixed it. One
#   rewrite cleared the floor for 8 of 10 colloquial questions ("got warded 2 days, claimable?",
#   "car kena scratched"); two or three short searches in the documents' words cleared it for all
#   10, the fall question at 0.511, with the right document in the top six every time. The cost is
#   that three near-miss questions of eight also clear it (a domestic helper, a maid's bills,
#   dental insurance), so what reads them has to say "not covered" honestly — see ANSWER_SYSTEM
#   and the possessive scoping in `core/graph/scope.py`.
# - **A follow-up as a whole question.** "when does it expire?" after the car policy became a
#   question about that policy, and was answered "11 April 2027", cited.
#
# Two things were tried and rejected. Folding this into the router's call saved about a second
# and cost the router its judgement — "how much is my pet insurance premium?" was refused as a
# request to act — and wrote weaker search wording, so the fall question fell back under the
# floor. Lowering the floor instead let a 4B reader answer near-misses: "do i have travel
# insurance?" (0.38) came back "You have travel insurance".
UNDERSTAND_SYSTEM = (
    "You turn a person's latest message about their own household documents into two things. "
    "question: the message as a complete question that makes sense on its own, resolving words "
    "like it, that, those and what about from the conversation so far, in the person's own "
    "voice; with no conversation, repeat the message as it is. searches: two or three short "
    "search queries, each in the words the document itself would print for what is being asked "
    "about - the benefit, the event, the condition, the amount or the date - instead of "
    "informal, abbreviated or Singapore colloquial wording. Keep every specific the question "
    "gives. Do not answer the question."
)

MAX_SEARCHES = 3

_UNDERSTAND_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "searches": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": MAX_SEARCHES,
        },
    },
    "required": ["question", "searches"],
}

# The last three sentences are measured, not decoration. Each passage is printed under its context
# prefix — document title, type, section, page — and without being told that line is evidence the
# 4B generator returned no sentences at all on 13 September for "do i have a hospitalisation
# plan?" and for "what is my private car insurance policy?", with the schedule itself in the
# passages. The first wording that fixed those ("when the question asks whether a document exists,
# answer from that line") also produced "You have travel insurance." from passages about car,
# home and hospital cover; the last sentence is the one that stopped it while keeping both answers.
ANSWER_SYSTEM = (
    "You answer only from the numbered passages you are given. Every sentence you write must "
    "list the passage numbers it came from. If the passages do not answer the question, you "
    "return no sentences and say which document would have answered it. You never use "
    "knowledge from outside the passages, and you never soften a number. Each passage starts "
    "with a line naming the document it comes from: its title, its type and its section. That "
    "line is evidence too. Never say that a kind of cover or document exists unless a passage's "
    "document line or text names that kind of cover or document."
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

    question: str  # as the person typed it
    history: list[tuple[str, str]]  # earlier (role, text) turns, oldest first
    intent: str
    standalone: str  # the question made whole, resolving a follow-up against the history
    searches: list[str]  # the question in the words a document would print
    passages: list[Passage]
    scoped: Scoped | None  # whose question it is, decided over every candidate
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


def _conversation(history: list[tuple[str, str]]) -> str:
    turns = [
        f"{'assistant' if role == 'assistant' else 'person'}: "
        + " ".join(text.split())[:HISTORY_CHARS]
        for role, text in history[-HISTORY_TURNS:]
        if text and text.strip()
    ]
    return "\n".join(turns)


def _asked(state: State) -> str:
    """The question to answer and to scope. A follow-up is the whole question it was made into; a
    first question keeps the person's own words, because a rewrite that dropped "my son's" would
    scope the answer to the wrong person."""
    question = state["question"]
    return (state.get("standalone") or question) if state.get("history") else question


def fuse(results: list[list[Passage]], limit: int) -> list[Passage]:
    """Several searches as one list: each passage once, at the best score any phrasing gave it.

    The best score rather than a rank fusion, because the pack's floor is a similarity and must
    stay comparable with one: a passage the documents' own wording finds at 0.45 is as good as the
    same passage found at 0.45 by the person's wording.
    """
    best: dict[int, Passage] = {}
    for passages in results:
        for passage in passages:
            held = best.get(passage.chunk_id)
            if held is None or passage.score > held.score:
                best[passage.chunk_id] = passage
    return sorted(best.values(), key=lambda passage: passage.score, reverse=True)[:limit]


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
        today: date | None = None,
    ) -> None:
        self._today = today  # fixed for tests and the demonstration; otherwise the real date
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

    def understand(self, state: State) -> State:
        """The question made whole, and said in the documents' words. See `UNDERSTAND_SYSTEM`."""
        question = state["question"]
        conversation = _conversation(state.get("history") or [])
        prompt = (
            f"Conversation so far:\n{conversation}\n\n" if conversation else ""
        ) + f"Latest message: {question}"
        try:
            reply = self._client.constrained(UNDERSTAND_SYSTEM, prompt, _UNDERSTAND_SCHEMA).json()
            standalone = " ".join(str(reply.get("question") or "").split()) or question
            found = reply.get("searches")
            searches = [
                " ".join(str(search).split())
                for search in (found if isinstance(found, list) else [])
                if str(search).strip()
            ][:MAX_SEARCHES]
        except ModelUnavailable:
            # A step that cannot run must not block an answer: the question as asked is still
            # searched, exactly as it was before anything rewrote it.
            standalone, searches = question, []
        return {"standalone": standalone, "searches": searches}

    def retrieve(self, state: State) -> State:
        """Every phrasing of the question, searched and fused. The person's own words always
        among them, so a rewrite can add a passage but never take one away."""
        phrasings = [state["question"], state.get("standalone", ""), *(state.get("searches") or [])]
        queries = list(dict.fromkeys(q for q in phrasings if q and q.strip()))
        results = [self._retriever.search(q, candidates=self._candidates) for q in queries]
        return {"passages": fuse(results, self._candidates)}

    def rerank(self, state: State) -> State:
        """Whose question is it, over every candidate, and then the few that are read.

        Scoping comes first, as `core/graph/scope.py` has always said it should. After the cut it
        could only narrow six passages, and "is my dad's hospital cover still active?" lost his
        own policy to six passages about the owner's before it was ever asked whose they were.
        """
        passages = state.get("passages") or []
        question = state["question"]
        asked = _asked(state)
        scoped = self._household.apply(asked, passages) if self._household else None
        if scoped is not None and scoped.scoped:
            passages = scoped.passages
        kept = self._reranker.rerank(asked or question, passages, keep=self._keep)
        return {"reranked": kept, "scoped": scoped}

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
        builder.add_node("understand", self.understand)
        builder.add_node("retrieve", self.retrieve)
        builder.add_node("rerank", self.rerank)

        builder.add_edge(START, "route")
        builder.add_conditional_edges(
            "route",
            lambda state: "refuse" if state.get("intent") == "act" else "explain",
            {"refuse": END, "explain": "understand"},
        )
        builder.add_edge("understand", "retrieve")
        builder.add_edge("retrieve", "rerank")
        builder.add_edge("rerank", END)
        return builder.compile(checkpointer=MemorySaver())

    # ------------------------------------------------------------------------- the call

    def stream(
        self,
        question: str,
        *,
        thread_id: str = "local",
        history: Sequence[tuple[str, str]] = (),
    ) -> Iterator[Event]:
        """The implementation. Yields each sentence once it has passed the gate, never before.

        The order is worth reading as a sequence of promises. Nothing is claimed until `Reading`;
        after that every `Sentence` is final; and exactly one of `Abstained`, `Refused` or
        `Finished` ends the stream.

        `history` is the conversation before this question, as `(role, text)`. It is read by the
        router alone, to make a follow-up whole; it is never evidence, and nothing an earlier
        answer said can be cited by this one.
        """
        final: State = self._graph.invoke(
            {"question": question, "history": list(history)},
            {"configurable": {"thread_id": thread_id}},
        )
        if final.get("intent") == "act":
            yield Refused(REFUSAL)
            return

        passages = final.get("reranked") or []
        asked = _asked(final)

        # Whose question is this? Decided in `rerank`, over every candidate, and acted on here
        # before the floor, so an abstention about the wrong person is not reported as weak
        # evidence. See `core/graph/scope.py`.
        scoped = final.get("scoped")
        if scoped is not None and scoped.unknown_relation:
            word = scoped.unknown_relation
            yield Abstained(
                f"Parrot does not know who your {word} is yet",
                (
                    "When a document names them, say who they are on the Household page, and "
                    f"questions about your {word} will be answered from their documents."
                ),
                0,
                0,
                None,
            )
            return
        person = scoped.person_name if scoped is not None and scoped.scoped else None

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
        if scoped is not None and scoped.scoped and scoped.about:
            # Somebody else's documents, asked about by the owner. Telling the model that the
            # person in the passages is the one asking made it write nothing at all on
            # "is my dad's hospital cover still active?".
            whose = (
                f"The question is about {person}, the asker's {scoped.about}. "
                f"'My {scoped.about}' means {person}.\n\n"
            )
        elif person:
            whose = f"The person asking is {person}. 'My', 'I' and 'mine' mean them.\n\n"
        else:
            whose = ""
        # "Still active", "due soon", "expired": a document's dates mean nothing without today's.
        today = f"Today is {(self._today or date.today()):%d %B %Y}.\n"
        words = f"\n(The person's own words: {question})" if asked != question else ""
        prompt = f"{today}{whose}Question: {asked}{words}\n\nPassages:\n{_numbered(passages)}"
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

    def ask(
        self,
        question: str,
        *,
        thread_id: str = "local",
        history: Sequence[tuple[str, str]] = (),
    ) -> Answer:
        """Every event, collected. `scripts/ask.py` and the screen ask the same question of the
        same code, so they cannot disagree about the answer."""
        claims: list[Cited] = []
        passages_read = 0

        for event in self.stream(question, thread_id=thread_id, history=history):
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
