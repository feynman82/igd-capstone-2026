"""Ask PARROT the golden questions the way `scripts/ask.py` does, and keep what it read.

`Answer` says how many passages the graph read but not which, because a screen has no use for
them. Ragas does: context recall and precision are judged on the passages, not on the answer.
So the harness stands a recorder between the graph and Lane B's retriever and reranker and
keeps, per question, the passages the model was actually shown. Nothing in `core/graph/`
changes, and the graph is built by the same constructor call `scripts/ask.py` makes, so the
harness cannot score a different PARROT from the one a person talks to.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol

from core.graph.answer import Answer, AnswerGraph
from core.graph.ports import Passage, Reranker, Retriever
from core.runtime.settings import Settings
from eval.sets_io import Question


class Asks(Protocol):
    """The one method of `AnswerGraph` the harness uses. A test supplies a fake."""

    def ask(
        self, question: str, *, thread_id: str = ..., history: Sequence[tuple[str, str]] = ...
    ) -> Answer: ...


@dataclass
class RecordingRetriever:
    """Counts candidates. What the model read is recorded by the reranker, which runs last."""

    inner: Retriever
    candidates_seen: int = 0

    def search(self, question: str, *, candidates: int) -> list[Passage]:
        passages = self.inner.search(question, candidates=candidates)
        self.candidates_seen += len(passages)
        return passages


@dataclass
class RecordingReranker:
    """Keeps the passages the graph handed to the model. The graph scopes, filters and cuts
    before it reranks, so the reranker's output is exactly the evidence the answer was written
    from — and, when the floor then refused it, exactly the evidence that was too weak."""

    inner: Reranker
    kept: list[Passage] = field(default_factory=list)

    def rerank(self, question: str, passages: list[Passage], *, keep: int) -> list[Passage]:
        self.kept = self.inner.rerank(question, passages, keep=keep)
        return self.kept


@dataclass
class Recorder:
    retriever: RecordingRetriever
    reranker: RecordingReranker

    def take(self) -> tuple[list[Passage], int]:
        """The last question's contexts and candidate count, then a clean slate."""
        contexts, seen = self.reranker.kept, self.retriever.candidates_seen
        self.reranker.kept, self.retriever.candidates_seen = [], 0
        return contexts, seen


@dataclass(frozen=True, slots=True)
class Trace:
    question: Question
    answer: Answer
    contexts: tuple[Passage, ...]  # what the model was shown, in the order it was shown
    candidates: int  # how many passages retrieval offered before the cut
    latency_ms: int


def trace_all(
    graph: Asks,
    recorder: Recorder,
    questions: Sequence[Question],
    *,
    on_each: Callable[[Trace], None] | None = None,
) -> list[Trace]:
    """Each question on its own thread, so no answer is a follow-up to the one before."""
    traces: list[Trace] = []
    for question in questions:
        recorder.take()
        started = time.monotonic()
        answer = graph.ask(question.question, thread_id=f"eval-{question.id}")
        elapsed = int((time.monotonic() - started) * 1000)
        contexts, candidates = recorder.take()
        trace = Trace(question, answer, tuple(contexts), candidates, elapsed)
        traces.append(trace)
        if on_each is not None:
            on_each(trace)
    return traces


RetrieverName = Literal["hybrid", "dense"]
RerankerName = Literal["cross-encoder", "none"]


def build(
    conn: Any,
    settings: Settings,
    *,
    candidates: int = 40,
    keep: int = 6,
    retriever: RetrieverName = "hybrid",
    reranker: RerankerName = "cross-encoder",
    rerank_floor: float | None = None,
) -> tuple[AnswerGraph, Recorder]:
    """The graph `scripts/ask.py` builds, with the recorder in the seam. Kept in step with that
    script by hand. `retriever="dense"` and `reranker="none"` are the stopgaps in
    `core/graph/baseline.py`, kept selectable so a change is measured against them on the same
    vault, one variable at a time."""
    from core.advice_consent import HouseholdConsents
    from core.advice_records import HouseholdAdviceLog
    from core.graph.baseline import DenseRetriever, NoReranker
    from core.graph.inventory import HouseholdInventory
    from core.graph.scope import HouseholdScope
    from core.registry import enabled_pack_ids, enabled_packs
    from core.retrieve.hybrid import HybridRetriever
    from core.retrieve.rerank import RELEVANCE_FLOOR, CrossEncoderReranker
    from core.runtime.ollama import Ollama
    from modules.advice import ModuleAdviser

    client = Ollama(settings)
    enabled = enabled_pack_ids(conn)
    packs = None if enabled is None else tuple(sorted(enabled))
    retriever_impl: Retriever = (
        DenseRetriever(conn, client, packs)
        if retriever == "dense"
        else HybridRetriever(conn, client, packs)
    )
    retriever_rec = RecordingRetriever(retriever_impl)
    reranker_impl: Reranker = (
        NoReranker()
        if reranker == "none"
        else CrossEncoderReranker(
            settings.rerank_model,
            RELEVANCE_FLOOR if rerank_floor is None else rerank_floor,
        )
    )
    reranker_rec = RecordingReranker(reranker_impl)
    graph = AnswerGraph(
        client,
        retriever_rec,
        reranker_rec,
        candidates=candidates,
        keep=keep,
        household=HouseholdScope(conn),
        inventory=HouseholdInventory(conn),
        packs=enabled_packs(conn),
        adviser=ModuleAdviser(conn),
        consents=HouseholdConsents(conn),
        advice_log=HouseholdAdviceLog(conn),
    )
    return graph, Recorder(retriever_rec, reranker_rec)
