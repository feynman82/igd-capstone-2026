"""Router → retrieve → rerank → grounding gate → answer or abstain.

A LangGraph state machine, because the interesting part is the *order* and the fact that one of
the edges goes to "abstain". Retrieval is one tool call we wrote ourselves; there is no agent
deciding what to do next.

    route ──► retrieve ──► rerank ──► answer ──► gate ──┬──► respond
       │                                                └──► abstain
       └──► refuse            (a request to act, not to explain)

`route` exists for one reason worth stating: `never_acts` is `Literal[True]` in every pack
manifest, and a question like "renew it for me" must be refused at the top of the graph rather
than politely declined at the bottom by a model that might not.

The checkpointer is `MemorySaver`, not `PostgresSaver`. The Postgres checkpointer creates its
own tables, and creating tables at runtime is exactly what rule 4 forbids — `db/migrations/` is
a separate reviewed pull request. The swap is one line once that migration lands.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Literal, TypedDict

from core.graph.gate import Claim, Verdict, check
from core.graph.ports import Passage, Reranker, Retriever
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
    question: str
    intent: str
    passages: list[Passage]
    reranked: list[Passage]
    claims: list[Claim]
    missing: str
    verdict: Verdict
    disclaimer: str
    answer: str


@dataclass(frozen=True, slots=True)
class Cited:
    """One sentence and the passages it was traced to. What rule 3 looks like as data.

    `Answer.text` joins these for a terminal; a screen wants them apart, so that a person can
    put a finger on one sentence and see the page it came from rather than a list at the end.
    """

    text: str
    chunk_ids: tuple[int, ...]
    citations: list[str] = field(default_factory=list)


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

    @property
    def grounded(self) -> bool:
        return not self.abstained and not self.refused


def _numbered(passages: list[Passage]) -> str:
    return "\n\n".join(
        f"[{index}] ({passage.cite()}) {passage.context_prefix}\n{passage.text}"
        for index, passage in enumerate(passages, start=1)
    )


def _pack_for(passages: list[Passage], packs: tuple[InstalledPack, ...]) -> InstalledPack | None:
    """Whichever pack owns the most of the evidence. Its guardrails govern the answer.

    Packs declare different abstain floors - insurance is stricter than tax - so this is not a
    detail. When the evidence is split, the majority owner wins; when it names no pack at all,
    the caller falls back to the strictest floor rather than the loosest.
    """
    if not packs:
        return None
    counts: dict[str, int] = {}
    for passage in passages:
        if passage.pack_id:
            counts[passage.pack_id] = counts.get(passage.pack_id, 0) + 1
    if not counts:
        return max(packs, key=lambda p: p.manifest.guardrails.abstain_below)
    winner = max(counts, key=lambda pack_id: counts[pack_id])
    for installed in packs:
        if installed.id == winner:
            return installed
    return None


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
    ) -> None:
        self._client = client
        self._retriever = retriever
        self._reranker = reranker
        self._candidates = candidates
        self._keep = keep
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

    def answer(self, state: State) -> State:
        passages = state.get("reranked") or []
        if not passages:
            return {"claims": [], "missing": "no document in your vault covers this"}
        prompt = f"Question: {state['question']}\n\nPassages:\n{_numbered(passages)}"
        try:
            reply = self._client.constrained(ANSWER_SYSTEM, prompt, _ANSWER_SCHEMA).json()
        except ModelUnavailable as error:
            return {"claims": [], "missing": str(error)}

        claims: list[Claim] = []
        for item in reply.get("sentences") or []:
            text = str(item.get("text", "")).strip()
            numbers = [int(n) for n in item.get("supports") or [] if isinstance(n, int)]
            # The model cites 1-based positions; the gate checks real chunk ids.
            supports = tuple(passages[n - 1].chunk_id for n in numbers if 1 <= n <= len(passages))
            claims.append(Claim(text, supports))
        return {"claims": claims, "missing": str(reply.get("missing", "")).strip()}

    def gate(self, state: State) -> State:
        passages = state.get("reranked") or []
        installed = _pack_for(passages, installed_packs())
        floor = installed.manifest.guardrails.abstain_below if installed else 0.42
        return {
            "verdict": check(state.get("claims") or [], passages, abstain_below=floor),
            "disclaimer": installed.manifest.guardrails.disclaimer.strip() if installed else "",
        }

    # ------------------------------------------------------------------------ the graph

    def _build(self) -> Any:
        from langgraph.checkpoint.memory import MemorySaver
        from langgraph.graph import END, START, StateGraph

        builder: Any = StateGraph(State)
        builder.add_node("route", self.route)
        builder.add_node("retrieve", self.retrieve)
        builder.add_node("rerank", self.rerank)
        builder.add_node("answer", self.answer)
        builder.add_node("gate", self.gate)

        builder.add_edge(START, "route")
        builder.add_conditional_edges(
            "route",
            lambda state: "refuse" if state.get("intent") == "act" else "explain",
            {"refuse": END, "explain": "retrieve"},
        )
        builder.add_edge("retrieve", "rerank")
        builder.add_edge("rerank", "answer")
        builder.add_edge("answer", "gate")
        builder.add_edge("gate", END)
        return builder.compile(checkpointer=MemorySaver())

    # ------------------------------------------------------------------------- the call

    def ask(self, question: str, *, thread_id: str = "local") -> Answer:
        final: State = self._graph.invoke(
            {"question": question}, {"configurable": {"thread_id": thread_id}}
        )
        if final.get("intent") == "act":
            return Answer(REFUSAL, refused=True)

        passages = final.get("reranked") or []
        verdict = final.get("verdict")
        if verdict is None or not verdict.has_answer:
            reason = (verdict.reason if verdict else None) or "this is not in your documents"
            missing = final.get("missing") or ""
            text = f"I can't answer that from your documents: {reason}."
            if missing:
                text = f"{text} {missing}"
            return Answer(
                text,
                abstained=True,
                passages_read=len(passages),
                dropped=len(verdict.dropped) if verdict else 0,
                reason=reason,
                missing=missing,
            )

        by_id = {passage.chunk_id: passage for passage in passages}
        lines = [claim.with_citation(by_id) for claim in verdict.grounded]
        citations = sorted(
            {by_id[cid].cite() for claim in verdict.grounded for cid in claim.supports}
        )
        cited = [
            Cited(
                text=claim.text,
                chunk_ids=tuple(claim.supports),
                citations=[by_id[cid].cite() for cid in claim.supports if cid in by_id],
            )
            for claim in verdict.grounded
        ]
        return Answer(
            " ".join(lines),
            citations=citations,
            passages_read=len(passages),
            dropped=len(verdict.dropped),
            disclaimer=final.get("disclaimer") or "",
            claims=cited,
        )


Intent = Literal["explain", "act"]
