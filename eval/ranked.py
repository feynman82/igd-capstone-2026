"""What one question's evidence looked like, recorded so the floor can be replayed later.

The graph decides whether to answer by comparing the best passage's cosine score with the
floor of the pack that speaks for it. `eval/bands.py` replays that decision — and a banded
top 3 beside it — from a result file, so the file has to carry the score, the pack, the floor
and every document the model read. This module turns one trace into those fields.

Which pack governs is asked of the graph (`_pack_for`), not decided again here: a replay that
chose its own pack would measure its own opinion rather than the product.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any

from core.graph.answer import _pack_for
from core.graph.ports import Passage
from core.packs import InstalledPack
from eval.score import doc_stem

if TYPE_CHECKING:
    from eval.harness import Trace

# The floor the graph applies when no pack speaks for the evidence: `else 0.42` in
# `AnswerGraph.stream`, the same number as `Guardrails.abstain_below`'s default. A pack copy
# cannot lower it, so a floor-off run still holds back core evidence under it — see `capped`.
CORE_FLOOR = 0.42


def governing(
    contexts: Sequence[Passage], packs: Sequence[InstalledPack]
) -> tuple[str | None, float | None]:
    """The pack whose floor decides, and that floor. `core` when no pack speaks for the best
    passage; `(None, None)` when nothing was read at all."""
    if not contexts:
        return None, None
    pack = _pack_for(list(contexts), packs)
    if pack is None:
        return "core", CORE_FLOOR
    return pack.id, pack.manifest.guardrails.abstain_below


def documents(
    contexts: Sequence[Passage], relevance: Sequence[float], packs: Sequence[InstalledPack]
) -> list[dict[str, Any]]:
    """Every distinct document among the passages read, in the order the reranker put them.

    The quote and page are the reranker's first passage of each document — what a person would
    be shown. The scores are the document's best, because the floor reads the best passage.
    Relevance that does not line up one-to-one with the passages is recorded as unknown rather
    than guessed at.
    """
    scores: list[float | None] = (
        list(relevance) if len(relevance) == len(contexts) else [None] * len(contexts)
    )
    by_doc: dict[str, dict[str, Any]] = {}
    for passage, rel in zip(contexts, scores, strict=True):
        doc = doc_stem(passage.document_name) if passage.document_name else str(passage.document_id)
        item = by_doc.get(doc)
        if item is None:
            pack = _pack_for([passage], packs)
            by_doc[doc] = {
                "doc": doc,
                "page": passage.page,
                "cosine": passage.score,
                "relevance": rel,
                "pack": pack.id if pack else "core",
                "quote": passage.text,
            }
            continue
        item["cosine"] = max(item["cosine"], passage.score)
        if rel is not None:
            item["relevance"] = rel if item["relevance"] is None else max(item["relevance"], rel)
    return list(by_doc.values())


def record(trace: Trace, packs: Sequence[InstalledPack]) -> dict[str, Any]:
    """The four fields `eval/bands.py` replays from, for one question.

    `packs` are the **production** packs, never the floorless copies a floor-off run hands the
    graph: `floor_in_force` is the floor today's PARROT would have applied.
    """
    pack, floor = governing(trace.contexts, packs)
    return {
        "best_score": max((p.score for p in trace.contexts), default=None),
        "governing_pack": pack,
        "floor_in_force": floor,
        "ranked": documents(trace.contexts, getattr(trace, "relevance", ()), packs),
    }


def capped(lines: Sequence[Mapping[str, Any]]) -> list[str]:
    """The questions a floor-off run still held back: core evidence under the core floor."""
    return [
        line["id"]
        for line in lines
        if line.get("governing_pack") == "core"
        and line.get("best_score") is not None
        and line["best_score"] < CORE_FLOOR
    ]
