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
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from core.contracts import Exclusions
from core.graph.advice import Figure
from core.graph.ports import Passage

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Claim:
    text: str
    supports: tuple[str, ...]  # passage refs, "document:11"

    def with_citation(self, by_ref: dict[str, Passage]) -> str:
        cited = [by_ref[ref].cite() for ref in self.supports if ref in by_ref]
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


def check_one(claim: Claim, retrieved: set[str]) -> str | None:
    """Why this one sentence cannot be kept, or `None` if it can.

    Depends on nothing but the sentence and what was retrieved, which is what lets a sentence be
    released the moment the model finishes writing it.
    """
    # "See passages 1, 2." is "." once its passage numbers are removed: a citation, not a claim.
    if not re.search(r"[^\W_]", claim.text):
        return "empty"
    if not claim.supports:
        return "no supporting passage"
    unknown = [ref for ref in claim.supports if ref not in retrieved]
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

    retrieved = {passage.ref for passage in passages}
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


_NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")

# A policy number, claim reference or the like: letters, a hyphen, then digits and letters —
# "MV-2026-448120", "Covid-19". Digits inside one of these are not independent numbers; the
# whole token is the identifier, and it either matches or it doesn't.
_IDENTIFIER = re.compile(r"(?<![\w-])[A-Za-z]{1,10}-[A-Za-z0-9-]*\d[A-Za-z0-9-]*")


def _normal(number: str) -> str:
    """ "1,860.00", "1860" and "01" → "1860", "1860", "1": formatting is not a different number."""
    plain = number.replace(",", "")
    if "." in plain:
        plain = plain.rstrip("0").rstrip(".")
    return plain.lstrip("0") or "0"


def unprinted_numbers(text: str, cited: Sequence[Passage]) -> list[str]:
    """Every number or identifier in a sentence that no cited passage prints. An identifier (a
    policy number, a claim reference) is copied whole, verbatim, or it is unprinted — its digits
    are not independent numbers that can be satisfied by matching fragments elsewhere. Every other
    number may be reformatted (comma grouping, trailing zeros, a leading zero) and is compared by
    value."""
    haystacks = [f"{passage.context_prefix}\n{passage.text}".lower() for passage in cited]

    identifiers: list[str] = []
    covered: list[tuple[int, int]] = []
    for match in _IDENTIFIER.finditer(text):
        identifier = match.group().rstrip("-.")
        identifiers.append(identifier)
        covered.append((match.start(), match.start() + len(identifier)))

    missing = [
        identifier
        for identifier in identifiers
        if not any(identifier.lower() in haystack for haystack in haystacks)
    ]

    printed = {
        _normal(found)
        for passage in cited
        for found in _NUMBER.findall(f"{passage.context_prefix}\n{passage.text}")
    }
    for found in _NUMBER.finditer(text):
        if any(start <= found.start() < end for start, end in covered):
            continue  # part of an identifier already checked above
        if _normal(found.group()) not in printed:
            missing.append(found.group())
    return missing


def states_a_printed_value(text: str, cited: Sequence[Passage]) -> bool:
    """Does this sentence state a number or identifier, and is every one printed by what it cites?

    Asked of a sentence read from documents on file alone. That line names a document, its
    numbers and its dates; a sentence cited to it that states none of them — "your car policy
    covers flood damage" — says more than the line does, however well it is cited.
    """
    if not (_NUMBER.search(text) or _IDENTIFIER.search(text)):
        return False
    return not unprinted_numbers(text, cited)


def _says(text: str, phrases: Sequence[str]) -> bool:
    lowered = text.lower()
    return any(re.search(rf"(?<!\w){re.escape(p.lower())}(?!\w)", lowered) for p in phrases)


def check_content(
    claim: Claim, by_ref: Mapping[str, Passage], *, exclusions: Exclusions | None = None
) -> str | None:
    """Why a cited sentence still cannot be kept, or `None`. Asked after `check_one` passes."""
    cited = [by_ref[ref] for ref in claim.supports if ref in by_ref]
    missing = unprinted_numbers(claim.text, cited)
    if missing:
        return f"states a number no cited passage prints: {missing}"
    if (
        exclusions is not None
        and cited
        and _says(claim.text, exclusions.claims)
        and not _says(claim.text, exclusions.negations)
        and all(_says(passage.context_prefix, exclusions.headings) for passage in cited)
    ):
        return "claims cover from an exclusion"
    return None


VERDICT_WORDS = (
    "enough",
    "adequate",
    "adequately",
    "sufficient",
    "insufficient",
    "should",
    "shouldn't",
    "recommend",
    "recommended to",
    "must",
    "better",
    "best",
    "worse",
    "buy",
    "surrender",
    "cancel",
    "switch",
    "upgrade",
    "downgrade",
)


def check_advice(
    claim: Claim,
    by_ref: Mapping[str, Passage],
    figures: Sequence[Figure],
    *,
    never_say: Sequence[str] = (),
) -> str | None:
    """Why an advice explanation cannot be kept, or `None`. Asked of a claim built over
    `advice.passages_for` instead of `check_content`: the calculator has already produced the
    verdict and every figure (ADR 0016), so what is left to police is not whether a number was
    printed but whether the *words* around it claim more than the calculator did.

    Checks, in order:

    1. A verdict word (`VERDICT_WORDS`, matched whole and case-insensitive by `_says`) — the
       calculator decides "should", "recommend", "buy"; the model only explains.
    2. A `never_say` phrase, matched the same way — a pack's own list of things this advice
       must never say.
    3. `unprinted_numbers`, exactly as `check_content` asks it: a number no cited passage prints.
    4. A number token in the text equal, by `_normal`, to one of `figures`' printed values, used
       without any of that figure's `words` — "you are short by SGD 451,200.00" when
       SGD 451,200.00 is the *target*, not the *gap*. Matched against `_normal` of the `_NUMBER`
       tokens found in `figure.text`, never `str(figure.value)`: `_NUMBER` carries no sign, so a
       `meets` gap of Decimal("-48800.00") is only found through the "48,800.00" its text
       prints. Asked only when the claim cites `calculation:0` — a number that equals a
       figure's value but is cited to the fact or rule passage that printed it first is that
       input's own number, not a mislabelled figure, and check 4 leaves it alone.
    """
    if _says(claim.text, VERDICT_WORDS):
        return "a verdict is said by code, not the explanation"
    if never_say and _says(claim.text, never_say):
        return "says what this advice never says"

    cited = [by_ref[ref] for ref in claim.supports if ref in by_ref]
    missing = unprinted_numbers(claim.text, cited)
    if missing:
        return f"states a number no cited passage prints: {missing}"

    if "calculation:0" in claim.supports:
        covered: list[tuple[int, int]] = []
        for match in _IDENTIFIER.finditer(claim.text):
            identifier = match.group().rstrip("-.")
            covered.append((match.start(), match.start() + len(identifier)))
        for found in _NUMBER.finditer(claim.text):
            if any(start <= found.start() < end for start, end in covered):
                continue  # part of an identifier, already ruled on above
            token = _normal(found.group())
            for figure in figures:
                figure_numbers = {_normal(n) for n in _NUMBER.findall(figure.text)}
                if token in figure_numbers and not _says(claim.text, figure.words):
                    return f"states {figure.text} without saying it is the {figure.name}"
    return None
