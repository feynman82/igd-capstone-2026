"""The grounding gate.

Rule 3 in AGENTS.md: no claim without a citation. This module is where that stops being a
sentence in a document and becomes a thing the code will not do.

The answer node is constrained to return sentences, each with the passage ids that support it.
The gate then does three checks, in order of how cheaply they catch a lie:

1. **Every sentence names at least one passage.** A sentence with an empty `supports` list is
   the model writing prose, and prose is what we are here to refuse.
2. **Every named passage was actually retrieved.** A model that cites passage 9 when six were
   supplied has invented a source, which is worse than inventing a fact.
3. **The evidence was good enough to be worth answering from.** Each pack declares
   `guardrails.abstain_below`; when the best passage scores under it, the honest answer is that
   we do not have the document.

What survives all three is the answer. If nothing survives, the graph abstains and says what
document would have answered the question. An abstention is a correct outcome here, not a
failure — it is the behaviour the demonstration deliberately shows.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from core.graph.ports import Passage

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Claim:
    text: str
    supports: tuple[int, ...]  # chunk ids

    def with_citation(self, by_id: dict[int, Passage]) -> str:
        cited = [by_id[chunk_id].cite() for chunk_id in self.supports if chunk_id in by_id]
        seen: list[str] = []
        for citation in cited:
            if citation not in seen:
                seen.append(citation)
        return f"{self.text} [{'; '.join(seen)}]" if seen else self.text


@dataclass(frozen=True, slots=True)
class Verdict:
    grounded: list[Claim]
    dropped: list[tuple[str, str]]  # (sentence, why)
    abstained: bool
    reason: str | None = None

    @property
    def has_answer(self) -> bool:
        return bool(self.grounded) and not self.abstained


def check(
    claims: list[Claim],
    passages: list[Passage],
    *,
    abstain_below: float,
) -> Verdict:
    """Never raises, never rewrites a claim. It keeps, drops, or abstains."""
    if not passages:
        return Verdict([], [], True, "no document in your vault covers this")

    best = max(passage.score for passage in passages)
    if best < abstain_below:
        return Verdict(
            [],
            [],
            True,
            f"the closest document is not close enough (best match {best:.2f}, "
            f"this pack answers above {abstain_below:.2f})",
        )

    retrieved = {passage.chunk_id for passage in passages}
    grounded: list[Claim] = []
    dropped: list[tuple[str, str]] = []
    for claim in claims:
        if not claim.text.strip():
            continue
        if not claim.supports:
            dropped.append((claim.text, "no supporting passage"))
            continue
        unknown = [chunk_id for chunk_id in claim.supports if chunk_id not in retrieved]
        if unknown:
            dropped.append((claim.text, f"cites passage(s) that were not retrieved: {unknown}"))
            continue
        grounded.append(claim)

    for sentence, why in dropped:
        log.info("gate dropped a sentence (%s): %.80s", why, sentence)

    if not grounded:
        return Verdict([], dropped, True, "nothing in the answer could be traced to a document")
    return Verdict(grounded, dropped, False)
