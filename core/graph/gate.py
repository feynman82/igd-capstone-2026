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

**The three checks split into two groups, and the split is what makes streaming honest.**
Checks 1 and 2 are about one sentence and nothing else: whether a given sentence can be kept
never depends on any other sentence. Check 3 is about the evidence, so it is decided by
retrieval before a single token is generated.

That means a sentence can be verified the moment the model finishes writing it, and released
with its citations already attached — rather than the interface showing text it may have to take
back. `precheck` is the evidence question, `check_one` is the sentence question, and `check` is
the two of them composed for a caller that has the whole answer in hand. There is one set of
rules; the streaming path and the batch path are two ways of asking it.
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


def precheck(passages: list[Passage], *, abstain_below: float) -> str | None:
    """Is this evidence worth answering from at all? The reason to abstain, or `None`.

    Decided from retrieval alone, which is the point: it runs **before** generation, so a
    question the vault cannot answer costs a retrieval rather than a retrieval and a full pass
    through a 4B model whose output is then thrown away.
    """
    if not passages:
        return "no document in your vault covers this"
    best = max(passage.score for passage in passages)
    if best < abstain_below:
        # Two places is how a person reads a similarity, until it would say "0.45, above 0.45"
        # about a match of 0.4499 — which on 13 September it did.
        places = 3 if f"{best:.2f}" == f"{abstain_below:.2f}" else 2
        return (
            f"the closest document is not close enough (best match {best:.{places}f}, "
            f"this pack answers above {abstain_below:.{places}f})"
        )
    return None


def check_one(claim: Claim, retrieved: set[int]) -> str | None:
    """Why this one sentence cannot be kept, or `None` if it can.

    Depends on nothing but the sentence and what was retrieved, which is what lets a sentence be
    released the moment the model finishes writing it.
    """
    if not claim.text.strip():
        return "empty"
    if not claim.supports:
        return "no supporting passage"
    unknown = [chunk_id for chunk_id in claim.supports if chunk_id not in retrieved]
    if unknown:
        return f"cites passage(s) that were not retrieved: {unknown}"
    return None


def check(
    claims: list[Claim],
    passages: list[Passage],
    *,
    abstain_below: float,
) -> Verdict:
    """Never raises, never rewrites a claim. It keeps, drops, or abstains.

    The whole-answer form, for a caller holding every sentence at once. `precheck` and
    `check_one` are the same rules, asked one at a time.
    """
    refusal = precheck(passages, abstain_below=abstain_below)
    if refusal is not None:
        return Verdict([], [], True, refusal)

    retrieved = {passage.chunk_id for passage in passages}
    grounded: list[Claim] = []
    dropped: list[tuple[str, str]] = []
    for claim in claims:
        why = check_one(claim, retrieved)
        if why is None:
            grounded.append(claim)
        elif why != "empty":  # an empty sentence is not a dropped claim, it is nothing
            dropped.append((claim.text, why))

    for sentence, why in dropped:
        log.info("gate dropped a sentence (%s): %.80s", why, sentence)

    if not grounded:
        return Verdict([], dropped, True, "nothing in the answer could be traced to a document")
    return Verdict(grounded, dropped, False)
