"""Router → retrieve → rerank → decide → answer, one verified sentence at a time.

A LangGraph state machine, because the interesting part is the *order* and the fact that one of
the edges goes to "abstain". Retrieval is one tool call we wrote ourselves; there is no agent
deciding what to do next.

    route ──► retrieve ──► rerank ──┬──► abstain        (the evidence is not good enough)
       │                            └──► answer ──► one Sentence event per kept claim
       ├──► refuse                                      (a request to act, not to explain)
       └──► advise ──► whose ──► consent ──► calculate ──► card ──► explain   (ADR 0016)
                 └──► decline      (no adviser, no advice in the pack, or no shape phrase asked)

`route` exists for one reason worth stating: `never_acts` and `verdict_by_code` are
`Literal[True]` in every pack manifest, and a pack without advice declines, so a question like
"renew it for me" or "should I buy critical illness cover?" must be turned away at the top of the
graph rather than politely declined at the bottom by a model that might not.

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

import hashlib
import logging
import re
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field, replace
from datetime import date
from typing import Any, TypedDict

from core.calendar import Line, Reply
from core.contracts import DEFAULT_DECLINE, AdviceShape
from core.graph.advice import (
    AdviceLog,
    AdviceRecord,
    Adviser,
    Calculation,
    ConsentBook,
    Input,
    Missing,
    kind_of,
    passages_for,
)
from core.graph.calendar import Drafted, HouseholdCalendar, draft, wants_entry
from core.graph.gate import (
    Claim,
    check_advice,
    check_content,
    check_one,
    precheck,
    states_a_printed_value,
)
from core.graph.inventory import Holding, Inventory
from core.graph.knowledge import categories_asked, glossary, mentions, reworded
from core.graph.period import asked_period, outside
from core.graph.ports import Kind, Passage, Reranker, Retriever
from core.graph.scope import HouseholdScope, Scoped, Subject
from core.graph.sentences import SentenceScanner
from core.grounding.corpus import load_corpus
from core.packs import InstalledPack, catalog, installed_packs
from core.runtime.ollama import ModelUnavailable, Ollama

log = logging.getLogger(__name__)

CANDIDATES = 40  # what retrieval returns
KEEP = 6  # what survives reranking and is actually read

HISTORY_TURNS = 6  # the most recent turns the understanding step reads to resolve a follow-up
HISTORY_CHARS = 600  # of each; an earlier answer is context, not evidence

# 14 September: the phrase "whether a claim will be approved" made "warded for dengue 3 days,
# can claim?", "got warded 2 days, claimable?" and "can i claim tax relief for my donations?"
# read as requests for a judgement, and all three were declined before anything was searched.
# They are questions about what the documents say. The fix says so plainly: asking whether
# something is covered or can be claimed is explain, not advise.
ROUTE_SYSTEM = (
    "You decide what kind of request you are looking at. 'explain' means the person wants to "
    "know what their documents say: what is covered or excluded, whether something can be "
    "claimed, what something costs or pays, when it ends, how to claim. 'act' means they are "
    "asking you to do something in the world: pay, renew, book, file, cancel, send or sign. "
    "'advise' means they want a recommendation or a judgement about a choice: whether to buy, "
    "keep, cancel, switch or add something, which option is better, or whether what they have "
    "is enough. Asking whether something is covered or can be claimed is explain; asking you to "
    "pay it is act; asking whether to buy it is advise."
)

_ROUTE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"intent": {"type": "string", "enum": ["explain", "act", "advise"]}},
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
    " Answer the question in your first sentence. Do not copy tables or lists the question did "
    "not ask for. Copy every number exactly as its passage prints it and never calculate one. "
    "Never recommend, compare, or say whether something is enough. When a passage is a document "
    "on file and the question asks whether such a document exists, name it as that passage "
    "prints it and give its dates."
    # 14 September: a verdict on one person's claim that the documents do not make.
    " List passage numbers only in supports, never in a sentence's text."
    " Never say whether a particular claim, stay or event will be covered, paid or rejected;"
    " say which conditions in the passages apply to it."
)


# The core's own voice, for evidence no pack speaks for (ADR 0017). Not decoration: on 17 September,
# with the rules alone, the 4B generator returned no sentences for "When was Marcus born?" while
# the NRIC passage printing the date ranked first. This wording answered that, Rachel's NRIC number
# and Lucas's date of birth; a near paraphrase lost the NRIC one.
# ponytail: tuned on three live questions; golden-set rows should hold it once eval covers them.
CORE_PERSONA = (
    "You explain a household's own documents plainly and briefly, naming the document and the "
    "line each point comes from."
)


def answer_system(installed: InstalledPack | None) -> str:
    """The voice first, the core's rules last: a persona cannot loosen what follows it."""
    limit = _max_sentences(installed)
    rules = f"{ANSWER_SYSTEM} Write at most {limit} sentences."
    voice = installed.manifest.persona.system.strip() if installed else CORE_PERSONA
    return f"{voice}\n\n{rules}"


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

# ------------------------------------------------------------------------------- advice
#
# ADR 0016. Every word here is pack-neutral: what advice is about, what it needs and how it is
# signed all come from the pack's `advice` block, and the arithmetic from `modules/advice/`.

# An explanation of a worked result is short on purpose: the verdict and the figures are already
# on the card, and every further sentence is one more chance for a 4B model to restate a figure
# in the wrong role.
ADVICE_SENTENCES = 3

# The calculation passage has no document, page or publisher to cite. It is named for what it is,
# so a chip on a sentence stating a figure says the figure was worked out, not printed.
CALCULATION_CITATION = "Worked out by Parrot from the inputs above"

NO_OWNER = "Say who you are on the Household page first."
REVIEW = "review"  # the shape id a coverage review is recorded and checked under


def _review_asked(
    question: str, packs: Sequence[InstalledPack]
) -> tuple[InstalledPack, AdviceShape] | None:
    """The first advising pack whose review a question asks for, as a shape the advise branch can
    carry: the review's id, label and phrases, and every reviewed shape's `never_say`."""
    for installed in packs:
        advice = installed.manifest.advice
        review = advice.review if advice else None
        if advice is None or review is None:
            continue
        if any(mentions(question, phrase) for phrase in review.asked):
            reviewed = [shape for shape in advice.shapes if shape.id in review.shapes]
            shape = reviewed[0].model_copy(
                update={
                    "id": REVIEW,
                    "label": review.label,
                    "asked": review.asked,
                    "never_say": sorted({p for s in reviewed for p in s.never_say}),
                }
            )
            return installed, shape
    return None


ADULT_AGE = 21


def _minor(subject: Subject, today: date) -> str | None:
    """Why advice about this person is withheld as not about an adult, or None when it is not."""
    name = subject.name or "this person"
    if subject.born is None:
        if subject.relation == "child":
            return (
                f"Advice is given only about adults, and {name}'s date of birth is not on file. "
                "File their NRIC, passport or birth certificate."
            )
        return None
    before_birthday = (today.month, today.day) < (subject.born.month, subject.born.day)
    if today.year - subject.born.year - before_birthday < ADULT_AGE:
        return f"Advice is given only about adults, and {name} is under {ADULT_AGE}."
    return None


WHOSE_REASON = "the question could be about more than one person"
WHOSE_MISSING = "Name one person, then ask again."


class State(TypedDict, total=False):
    """What the graph carries. It ends at the evidence; the answer is streamed, not stated."""

    question: str  # as the person typed it
    history: list[tuple[str, str]]  # earlier (role, text) turns, oldest first
    intent: str
    standalone: str  # the question made whole, resolving a follow-up against the history
    searches: list[str]  # the question in the words a document would print
    reworded: str  # the question in the documents' words, from the pack's vocabulary
    passages: list[Passage]
    scoped: Scoped | None  # whose question it is, decided over every candidate
    categories: list[str]  # category ids the question named
    held: list[str]  # document ids on file in those categories, as strings
    reranked: list[Passage]


@dataclass(frozen=True, slots=True)
class Citation:
    """A passage, named the way a person cites it and identified the way a link needs.

    Both, deliberately. `text` is what a terminal prints and what a chip is labelled with;
    `document_id` and `page` are what makes that chip open the page. Keeping them together from
    the moment the passage is retrieved is what stops the interface having to find the document
    again by name — a lookup that has to guess when two files share one.

    The four trailing fields are a rule value's own citation (ADR 0016): a published number has
    no page to open, only who published it, under what title, on what date, at what URL. They
    default to empty so every existing document citation, which has none of them, is unchanged.
    """

    document_id: Any
    document_name: str
    page: int
    text: str  # "policy.pdf, page 1"
    kind: Kind = "document"  # a page of a document, or a document on file
    publisher: str = ""
    title: str = ""
    dated: str = ""
    url: str = ""


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
    disclaimer: str = ""


@dataclass(frozen=True, slots=True)
class Refused:
    text: str = ""


@dataclass(frozen=True, slots=True)
class Declined:
    """A request for a recommendation or a judgement, declined before anything is searched.

    A pack without advice declines, and no model writes a verdict. `offer` is a neutral question
    Parrot can answer instead, shown as a suggestion and never answered on its own: a policy
    summary placed under "should I buy critical illness cover?" reads as an answer to it.
    """

    text: str
    disclaimer: str = ""
    offer: str = ""


@dataclass(frozen=True, slots=True)
class Finished:
    """Everything that is only knowable once the last sentence is in.

    `quarantined` counts documents held back from the vault, reported when an answer said "none
    on file" — the one answer a quarantined document could make untrue. `truncated` is set when
    the answer stopped at the pack's sentence limit. `unanswered` is set when code said something
    about the documents on file and nothing the model wrote survived the gate: "On file: …" names
    a policy, and it is not the answer to "does it cover floods?".
    """

    citations: list[str]
    disclaimer: str
    passages_read: int
    dropped: int
    person: str | None = None
    quarantined: int = 0
    truncated: bool = False
    unanswered: bool = False


@dataclass(frozen=True, slots=True)
class ConsentRequired:
    """Advice was asked for and the owner has not agreed to this pack's current consent wording.

    Terminal, and nothing happens before it: no calculation, no explanation, no record. Consent is
    a separate action a person takes (`core/advice_consent.py`), never something an answer does on
    their behalf, so this only carries the words a screen needs to ask for it.
    """

    pack_id: str
    pack_name: str
    version: str
    consent_text: str
    disclaimer: str
    label: str


@dataclass(frozen=True, slots=True)
class AdviceWithheld:
    """Advice could not be worked out, and `missing` says what it needs, in the pack's words.

    ADR 0016: the honest answer to a missing fact is to name it, not to estimate around it. Also
    the ending when nobody has said who they are yet, since advice is always about somebody.
    """

    pack_id: str
    label: str
    person: str | None
    missing: list[str]
    disclaimer: str


@dataclass(frozen=True, slots=True)
class AdviceCard:
    """A worked result, every word of it written by code, given before the model says anything.

    Not terminal: at most three gated sentences of explanation follow, then `Finished`. The card
    comes first so a model that is down or writes nothing usable still leaves a whole answer.
    `inputs` are built from each `Input` directly, so a published value's chip carries its
    publisher, title, date and URL rather than a page it does not have. `product_disclosure` is
    empty unless the calculation names a product.
    """

    pack_id: str
    label: str
    person: str | None
    verdict: str
    verdict_text: str
    figures: list[tuple[str, str]]  # (name, text)
    inputs: list[Citation]
    rows: list[list[str]]
    estimate: bool
    disclaimer: str
    product_disclosure: str
    consent_version: str


Event = (
    Reading
    | Sentence
    | Abstained
    | Refused
    | Declined
    | Finished
    | ConsentRequired
    | AdviceWithheld
    | AdviceCard
    | Drafted
)


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
    declined: bool = False
    offer: str = ""  # a question that can be answered instead, when it declined
    quarantined: int = 0  # documents not checked, when the answer said "none on file"
    truncated: bool = False  # the pack's sentence limit ended the answer
    unanswered: bool = False  # only a line about the documents on file was said
    advice: bool = False  # a worked result was given
    consent_required: bool = False  # advice was asked for before consent was given
    withheld: bool = False  # advice could not be worked out; `missing` says why
    verdict_text: str = ""  # the code-written verdict, when advice was given
    draft: Drafted | None = None  # a calendar entry written down and not saved (ADR 0020)

    @property
    def grounded(self) -> bool:
        """Answered. Asking for consent and naming what is missing are endings, not answers."""
        return not (
            self.abstained
            or self.refused
            or self.declined
            or self.consent_required
            or self.withheld
            or self.draft is not None
        )


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


def _citations(passages: Iterable[Passage]) -> list[Citation]:
    return _distinct(
        Citation(p.document_id, p.document_name, p.page, p.cite(), p.kind) for p in passages
    )


# 14 September: "…SGD 1,860.00, as stated in the policy document (6) and confirmed on file (7)." was
# dropped because the number check read the model's own passage numbers as unprinted figures.
# A passage number is citation, not claim: it is removed when every number in the mention is one
# of that sentence's supports. "thirty (30) days" survives, because 30 is not a support.
#
#
# The rule is structural, so removing a mention never changes what the sentence says:
# - A citation clause, an optional connective ("according to", "as per", "in", ...) followed by
#   a mention, goes as a whole only when the mention closes its clause, i.e. it is followed by
#   , . ; : ) ! ? or the end. "According to (2), cover ends." -> "Cover ends."
# - A bracketed mention that does not close its clause goes on its own and leaves its connective,
#   which is still part of the prose: "due per [1] the terms." -> "due per the terms."
# - A bare "passage 2" is removed only as a closing citation clause; mid-clause it is prose.
# - A bracket glued to a word or digit ("4(1)") is a clause number, never a mention.
_NUMBERS = r"(?>\d+(?:\s*(?:,|and|&)\s*\d+)*)"
_BRACKETED = rf"(?<![\w)\]])(?:\(\s*(?:(?:see|passages?)\s+)?{_NUMBERS}\s*\)|\[\s*{_NUMBERS}\s*\])"
_CLOSES_CLAUSE = r"\s*(?:[,.;:)!?]|\Z)"
_CITATION_CLAUSE = re.compile(
    r"\s*(?:\b(?:as\s+(?:stated|shown|listed)\s+in|as\s+per|according\s+to|refer\s+to"
    r"|see|per|from|in)\s+)?"
    rf"(?:{_BRACKETED}|\bpassages?\s+{_NUMBERS})(?={_CLOSES_CLAUSE})",
    re.IGNORECASE,
)
_STANDALONE_BRACKET = re.compile(rf"\s*{_BRACKETED}(?!{_CLOSES_CLAUSE})", re.IGNORECASE)


def _without_passage_numbers(text: str, numbers: Sequence[int]) -> str:
    """Every removable passage mention, removed. One removal can expose the next — in "2027
    [1][2]." the second bracket is glued to the first — so it repeats until nothing changes."""
    supports = set(numbers)
    while True:
        removed = _without_one_round_of_passage_numbers(text, supports)
        if removed == text:
            return text
        text = removed


def _without_one_round_of_passage_numbers(text: str, supports: set[int]) -> str:
    # The two patterns cannot overlap: one needs the mention to close its clause, the other not.
    spans = sorted(
        match.span()
        for pattern in (_CITATION_CLAUSE, _STANDALONE_BRACKET)
        for match in pattern.finditer(text)
        if {int(n) for n in re.findall(r"\d+", match.group())} <= supports
    )
    if not spans:
        return text

    kept: list[str] = []
    at = 0
    for start, end in spans:
        kept.append(text[at:start])
        at = end
    kept.append(text[at:])
    # Joined with a space, so a bracket that followed a removed one is not glued to the word
    # before it, where it would read as a clause number ("2027[2]").
    result = re.sub(r" ([,.;:!?])", r"\1", " ".join(" ".join(kept).split())).lstrip(",;: ")
    if not text[: spans[0][0]].strip():
        result = result[:1].upper() + result[1:]
    return result


def _either(labels: list[str]) -> str:
    """ "a dental plan", or "a term life plan or a whole life plan". "An" only before a, e, i or
    o: "a unit-linked plan" is said with a consonant."""
    named = [
        f"{'an' if label[:1].lower() in ('a', 'e', 'i', 'o') else 'a'} {label}"
        for label in dict.fromkeys(labels)
    ]
    return named[0] if len(named) == 1 else ", ".join(named[:-1]) + f" or {named[-1]}"


def _closes(shape: AdviceShape, labels: dict[str, str], held: set[str]) -> str:
    """Which kinds of cover close a short shape's gap, written by code.

    The pack declares `closed_by` and the verdict is the calculator's, so naming the cover adds
    no judgement of its own — it states the consequence of arithmetic ADR 0016 already keeps out
    of the model's hands. It names a *kind* of cover and never a product: the household holds no
    market data and PARROT holds no licence to sell against it.

    "More" when some is already on file, because that is usually the true shape of a shortfall.
    On 20 September Marcus held a critical illness plan and was SGD 251,200.00 short of the
    guideline; "you have no critical illness cover" would have been a false sentence about a
    policy he can point to.
    """
    names = [labels[c] for c in shape.closed_by if c in labels]
    if not names:
        return ""
    owned = [labels[c] for c in shape.closed_by if c in held and c in labels]
    spare = [label for label in names if label not in owned]
    if owned and spare:
        line = f"{_either(owned)} is on file; more cover under it, or {_either(spare)}, closes it."
    elif owned:
        line = f"{_either(owned)} is on file; more cover under it closes it."
    else:
        line = f"{_either(names)} closes it, and none is on file."
    return line[:1].upper() + line[1:]


def _max_sentences(installed: InstalledPack | None) -> int:
    """The answering pack's limit when one is in play, else the core catalogue's (ADR 0017)."""
    answering = installed.manifest.answering if installed else catalog().documents.answering
    return answering.max_sentences


def _pack_for(passages: list[Passage], packs: Sequence[InstalledPack]) -> InstalledPack | None:
    """The pack that speaks for the best-scoring passage's document type, or None for the core.

    A pack speaks for the core document types in its `answering.documents` (ADR 0017), and its
    guardrails, persona and exclusions govern an answer built on them.

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

    The best-scoring passage decides. When no enabled pack speaks for its document type, this is
    None and the core governs — the default floor, no disclaimer, no persona, the catalogue's
    sentence limit. A weaker policy passage further down must not sign an answer read from an
    identity card: on 17 September "When was Marcus born?" came back with the insurance
    disclaimer because it did. Only with no evidence at all does the strictest pack stand in.
    """
    if not packs:
        return None
    if not passages:
        return max(packs, key=lambda p: p.manifest.guardrails.abstain_below)
    best = max(passages, key=lambda passage: passage.score)
    return next((p for p in packs if best.doc_type in p.manifest.answering.documents), None)


def _unknown_relation(word: str, disclaimer: str = "") -> Abstained:
    """One wording for "who is your son?", shared by explaining and advising so they cannot drift.
    Advice signs it with the pack's advice disclaimer; an explanation leaves it unsigned, as it
    always has."""
    return Abstained(
        f"Parrot does not know who your {word} is yet",
        (
            "When a document names them, say who they are on the Household page, and "
            f"questions about your {word} will be answered from their documents."
        ),
        0,
        0,
        None,
        disclaimer,
    )


def _input_citation(item: Input) -> Citation:
    """A chip built from the `Input` itself, never from `Passage.cite()`.

    `passages_for` makes passages the gate can check, and their `cite()` prints "doc-1, page 1"
    for a fact with no name and "None, page 0" for a published value. The input already carries
    its citation as a person reads it, and a published value's publisher, title, date and URL.
    """
    kind = kind_of(item.ref)
    return Citation(
        document_id=item.document_id,
        document_name=item.title if kind == "rule" else "",
        page=item.page or 0,
        text=item.citation,
        kind=kind,
        publisher=item.publisher,
        title=item.title,
        dated=item.dated,
        url=item.url,
    )


def _guidance(installed: InstalledPack, today: date) -> list[tuple[Passage, Citation]]:
    """The review's `explained_by` steps, in order, as passages the explanation may cite.

    A step is kept only when its source is reviewed, not past `review_by`, and still prints the
    quote (whitespace aside, since a PDF extraction keeps its line breaks): a quote nobody can
    find in a signed-off source is not guidance. Read from the pack's own folder, never
    retrieved — the author chose these words, so the order they give is the order explained.
    """
    advice = installed.manifest.advice
    steps = advice.review.explained_by if advice and advice.review else []
    if not steps:
        return []
    sources = {source.document.file: source for source in load_corpus(installed)}
    out: list[tuple[Passage, Citation]] = []
    for number, step in enumerate(steps, start=1):
        source = sources.get(step.file)
        quote = " ".join(step.quote.split())
        if (
            source is None
            or source.reviewed_on is None
            or source.document.review_by < today
            or quote not in " ".join(source.text.split())
        ):
            log.warning("%s: explained_by step %d is not cited", installed.id, number)
            continue
        document = source.document
        day = document.published or document.retrieved
        dated = f"{day.day} {day:%B} {day.year}"
        text = f"{document.publisher}, {document.title}, {dated}"
        passage = Passage(
            chunk_id=number,
            document_id=None,
            page=0,
            text=quote,
            score=1.0,
            document_name=document.title,
            context_prefix=text,
            pack_id=installed.id,
            kind="guidance",
        )
        chip = Citation(
            None, document.title, 0, text, "guidance", document.publisher, document.title,
            dated, document.url,
        )  # fmt: skip
        out.append((passage, chip))
    return out


def _distinct(citations: Iterable[Citation]) -> list[Citation]:
    """Each chip once, first use first: a sentence citing one input twice shows it once."""
    out: list[Citation] = []
    for citation in citations:
        if all(citation.text != seen.text for seen in out):
            out.append(citation)
    return out


def _advice_prompt(
    calc: Calculation, shape: AdviceShape, subject: Subject, today: date, evidence: list[Passage]
) -> str:
    """What the model is shown to explain a worked result: the verdict it must not restate as its
    own, the cited inputs and figures as numbered passages, and the pack's own points to mention.

    Each passage is labelled with the input's own citation rather than `Passage.cite()`, for the
    reason `_input_citation` gives. Somebody other than the asker is named as such, for the reason
    the explain path gives: told nothing, a model writes "your" about Rachel's documents.
    """
    name = subject.name
    if name and subject.about:
        whose = (
            f"The result is about {name}, the asker's {subject.about}: say {name}'s, not your.\n"
        )
        addressee = f"the person asking, about {name}"
    elif name and subject.someone_else:
        whose = (
            f'The result is about {name}, not the person asking: write "{name}\'s", not "your".\n'
        )
        addressee = f"the person asking, about {name}"
    else:
        whose = f"The person asking is {name}. 'You' and 'your' mean them.\n" if name else ""
        addressee = name or "the person asking"
    numbered = "\n\n".join(
        f"[{index}] ({passage.context_prefix or CALCULATION_CITATION})\n{passage.text}"
        for index, passage in enumerate(evidence, start=1)
    )
    points = "\n".join(f"- {point}" for point in shape.disadvantages)
    order = (
        " Follow the order of a licensed adviser's needs analysis that the published guidance "
        "passages describe, citing them: first what is on file and the guideline it is measured "
        "against, then each gap and the kind of cover that closes it, then the next step the "
        "guidance describes."
        if any(passage.kind == "guidance" for passage in evidence)
        else ""
    )
    return (
        f"Today is {today:%d %B %Y}.\n{whose}\n"
        f"Explain this worked result to {addressee} in at most three sentences. Do not add a "
        f"verdict or advice; the verdict is already given.{order}\n\n"
        f"Verdict: {calc.verdict_text}\n\n"
        f"Passages:\n{numbered}"
        + (f"\n\nPoints to mention if relevant:\n{points}" if points else "")
    )


def _advice_basis(
    calc: Calculation,
    kept: Sequence[str],
    dropped: Sequence[tuple[str, str]],
    explanation: str,
    product_disclosure: str,
) -> dict[str, Any]:
    """Everything an advised answer rested on, so it can be reconstructed from its record alone
    (ADR 0016) — including what the gate refused to say, which is what a reviewer checks first.

    `explanation` says how the explanation stream ended: "complete" (the model finished or the
    sentence cap stopped it), "model_unavailable" (the card stands alone), or "stopped" (a
    consumer closed the stream, or anything else cut it off) — the default, so a record written
    from `finally` on an exit nobody named still says so honestly.

    `product_disclosure_sha256` is written only when the calculation names a product: the hash
    lets a reviewer confirm which wording of the pack's disclosure the person actually saw,
    without the record carrying that text a second time. `basis` is jsonb, so no migration is
    needed for either field.
    """
    basis: dict[str, Any] = {
        "inputs": [
            {
                "ref": item.ref,
                "role": item.role,
                "label": item.label,
                "value_text": item.value_text,
                "citation": item.citation,
                "document_id": None if item.document_id is None else str(item.document_id),
                "page": item.page,
                "publisher": item.publisher,
                "title": item.title,
                "dated": item.dated,
                "url": item.url,
            }
            for item in calc.inputs
        ],
        "figures": [
            {"name": figure.name, "value": str(figure.value), "text": figure.text}
            for figure in calc.figures
        ],
        "rows": [list(row) for row in calc.rows],
        "estimate": calc.estimate,
        "names_product": calc.names_product,
        "kept": list(kept),
        "dropped": [{"text": text, "why": why} for text, why in dropped],
        "explanation": explanation,
    }
    if calc.names_product:
        basis["product_disclosure_sha256"] = hashlib.sha256(
            product_disclosure.encode("utf-8")
        ).hexdigest()
    return basis


def _calendar_citation(line: Line) -> Citation:
    """A deadline cites the page its date came from; an event cites the calendar on its day."""
    if line.document_name:
        return Citation(
            line.document_id,
            line.document_name,
            line.page or 0,
            f"{line.document_name}, page {line.page}" if line.page else line.document_name,
        )
    on = line.on
    return Citation(
        None,
        "Calendar",
        0,
        f"Calendar, {on:%a} {on.day} {on:%b}" if on else "Calendar",
        kind="calendar",
        url=f"/calendar?d={on.isoformat()}" if on else "/calendar",
    )


def _calendar_events(reply: Reply) -> Iterator[Event]:
    """A calendar answer as the stream every other answer is: read, sentences, finished."""
    yield Reading(len(reply.lines))
    cited: list[str] = []
    for line in reply.lines:
        citation = _calendar_citation(line)
        cited.append(citation.text)
        yield Sentence(line.text, (), [citation])
    yield Finished(sorted(set(cited)), "", len(reply.lines), 0)


def _as_sentence(text: str) -> str:
    """ "which age band applies" -> "Which age band applies.": a pack's wording and a calculator's
    fragment read alike when a terminal joins them."""
    text = text.strip()
    return text[:1].upper() + text[1:] + ("" if text.endswith((".", "?", "!")) else ".")


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
        inventory: Inventory | None = None,
        packs: Sequence[InstalledPack] | None = None,
        adviser: Adviser | None = None,
        consents: ConsentBook | None = None,
        advice_log: AdviceLog | None = None,
        calendar: HouseholdCalendar | None = None,
    ) -> None:
        self._today = today  # fixed for tests and the demonstration; otherwise the real date
        # The three advice ports (ADR 0016), injected because `core/` never imports the modules
        # that calculate and holds no connection to read consent or write a record. Any of them
        # `None` and a request for advice is declined, as it was before advice existed: advice
        # that could not be recorded could not be reconstructed, so it is not given.
        self._adviser = adviser
        self._consents = consents
        self._advice_log = advice_log
        self._client = client
        self._retriever = retriever
        self._reranker = reranker
        self._candidates = candidates
        self._keep = keep
        # Injected rather than built here, because this class holds no connection and scoping
        # needs one. `None` is the honest state of a fresh install: nobody has said who they
        # are yet, so no question is first-person and every answer is about the household.
        self._household = household
        # The enabled packs, handed in by whoever read the registry. `None` means every installed
        # pack, which is what a test or a fresh install without a registry row expects.
        self._pack_list = tuple(packs) if packs is not None else None
        # The documents on file, read from facts. `None` is a caller with no connection: nothing
        # is known to be on file, so "none on file" is never said and no passage is set aside.
        self._inventory = inventory
        # The household calendar (ADR 0020). `None` is a caller with no connection, and then a
        # calendar question is just a question: searched, and most likely abstained on.
        self._calendar = calendar
        self._graph = self._build()

    def _packs(self) -> tuple[InstalledPack, ...]:
        return self._pack_list if self._pack_list is not None else installed_packs()

    # ------------------------------------------------------------------------ the nodes

    def route(self, state: State) -> State:
        try:
            reply = self._client.constrained(ROUTE_SYSTEM, state["question"], _ROUTE_SCHEMA).json()
            intent = str(reply.get("intent", "explain"))
        except ModelUnavailable:
            intent = "explain"  # a router that cannot run must not block an explanation
        if _review_asked(state["question"], self._packs()) is not None:
            # "What is lacking in my insurance coverage?" is a review however the router reads it:
            # matched by the pack's own phrases, as a shape is, and costing no extra model call.
            intent = "advise"
        return {"intent": intent if intent in {"explain", "act", "advise"} else "explain"}

    def understand(self, state: State) -> State:
        """The question made whole, and said in the documents' words. See `UNDERSTAND_SYSTEM`.

        The pack's vocabulary is applied twice, both without trusting a model with it: the words
        the question used are listed in the prompt, and the question with them replaced is
        searched as a phrasing of its own.
        """
        question = state["question"]
        packs = self._packs()
        conversation = _conversation(state.get("history") or [])
        words = glossary(question, packs)
        prompt = (
            (f"Conversation so far:\n{conversation}\n\n" if conversation else "")
            + (
                "Words this household uses, and what its documents print instead:\n"
                + "\n".join(words)
                + "\n\n"
                if words
                else ""
            )
            + f"Latest message: {question}"
        )
        said = reworded(question, packs) or ""
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
        return {"standalone": standalone, "searches": searches, "reworded": said}

    def retrieve(self, state: State) -> State:
        """Every phrasing of the question, searched and fused. The person's own words always
        among them, so a rewrite can add a passage but never take one away."""
        phrasings = [
            state["question"],
            state.get("reworded", ""),
            state.get("standalone", ""),
            *(state.get("searches") or []),
        ]
        queries = list(dict.fromkeys(q for q in phrasings if q and q.strip()))
        results = [self._retriever.search(q, candidates=self._candidates) for q in queries]
        return {"passages": fuse(results, self._candidates)}

    def rerank(self, state: State) -> State:
        """Whose question, which kind of document, then the few that are read.

        Scoping comes first, as `core/graph/scope.py` has always said it should. After the cut it
        could only narrow six passages, and "is my dad's hospital cover still active?" lost his
        own policy to six passages about the owner's before it was ever asked whose they were.

        The category filter sits with scoping and before the cut for the same reason scoping
        does: on 13 September the car policy's benefit table was the sixth passage read for
        "warded for dengue 3 days, can claim?". A passage from a document on file in a category
        the question did not ask about is set aside; a passage from a document with no category
        — a letter, a notice, anything the pack could not name — is always kept.
        """
        passages = state.get("passages") or []
        question = state["question"]
        asked = _asked(state)
        scoped = self._household.apply(asked, passages) if self._household else None
        if scoped is not None and scoped.scoped:
            passages = scoped.passages
        packs = self._packs()
        wanted = sorted({a.category.id for a in categories_asked(asked, packs)})
        held: list[str] = []
        if wanted and self._inventory is not None:
            on_file = self._inventory.holdings(packs)
            held = sorted(
                str(h.document_id) for h in on_file if h.category and h.category.id in wanted
            )
            named = {str(h.document_id) for h in on_file if h.category is not None}
            if held:
                passages = [
                    p
                    for p in passages
                    if str(p.document_id) in held or str(p.document_id) not in named
                ]
        kept = self._reranker.rerank(asked or question, passages, keep=self._keep)
        return {"reranked": kept, "scoped": scoped, "categories": wanted, "held": held}

    def _claim(self, item: dict[str, Any], passages: list[Passage]) -> Claim:
        """One streamed sentence object, turned into the thing the gate understands.

        The model cites 1-based positions in the prompt it was given; the gate checks real
        passage refs. A position outside the range is silently not translated, which means the
        claim ends up with fewer supports than the model named — and `check_one` then drops it
        for citing a passage that was not retrieved, which is the correct outcome and the one
        rule 3 wants.
        """
        text = str(item.get("text", "")).strip()
        numbers = [n for n in item.get("supports") or [] if isinstance(n, int)]
        text = _without_passage_numbers(text, numbers)
        supports = tuple(passages[n - 1].ref for n in numbers if 1 <= n <= len(passages))
        if len(supports) != len(numbers):
            # a ref no passage has: the gate sees an invented one
            supports = (*supports, "unknown:-1")
        return Claim(text, supports)

    def _on_file(
        self, asked: str, packs: Sequence[InstalledPack], scoped: Scoped | None
    ) -> list[Holding]:
        """The documents on file, narrowed to the same people the passages were."""
        if self._inventory is None:
            return []
        on_file = self._inventory.holdings(packs)
        if scoped is None or not scoped.scoped:
            return on_file
        return self._narrowed(asked, on_file)

    def _narrowed(self, question: str, on_file: list[Holding]) -> list[Holding]:
        """The holdings whose documents scoping keeps for `question`, as it keeps passages."""
        if self._household is None:
            return on_file
        passages = self._household.apply(question, [h.passage() for h in on_file]).passages
        kept = {str(p.document_id) for p in passages}
        return [h for h in on_file if str(h.document_id) in kept]

    def _absence(
        self,
        on_file: list[Holding],
        wanted: set[str],
        packs: Sequence[InstalledPack],
        person: str | None,
    ) -> Sentence | None:
        """ "None of the 5 policies on file is a dental plan." Written by code, never by the model:
        a 4B reader asked "do i have travel insurance?" once wrote "You have travel insurance."
        The sentence cites every document it counted, so it is a claim about the vault only.

        It is only sayable when every document it counts was read as some kind. A document whose
        printed name names no category may be exactly the kind asked about: on 15 October the car
        schedule's product name was extracted as its "Coverage Type: Comprehensive Cover" line, and
        five car questions opened with "None of the 11 policies … is a car or motor policy" while
        citing that schedule. Then nothing is said here, and the passages answer or the floor
        abstains, as for any other question."""
        if not on_file or not wanted or any(h.category is None for h in on_file):
            return None
        rules = [
            (declared.noun, rule.label)
            for installed in packs
            if (declared := installed.manifest.answering.categories) is not None
            for rule in declared.rules
            if rule.id in wanted
        ]
        if not rules:
            return None
        whose = f" for {person}" if person else ""
        labels = _either([label for _, label in rules])
        text = (
            f"The only document on file{whose} is not {labels}."
            if len(on_file) == 1
            else f"None of the {len(on_file)} {rules[0][0]} on file{whose} is {labels}."
        )
        return Sentence(text, (), _citations(h.passage() for h in on_file))

    def _presence(
        self, present: list[Holding], packs: Sequence[InstalledPack], person: str | None
    ) -> list[Sentence]:
        """ "On file for Marcus Lim: MERIDIAN ASSURANCE, Private Car Insurance Policy (policy no
        MV-2026-448120; expiry date 2027-04-11)." Written by code, one sentence per document on file
        in the categories the question named. On 14 September the 4B reader was handed that line and
        still answered "Yes, you have car insurance." — which policy, and until when, is the answer.
        Only identifier and date fields are named, as printed, so nothing here is a judgement."""
        out: list[Sentence] = []
        for holding in present:
            spec = catalog().documents.document_types.get(holding.doc_type)
            types = {f.name: f.type for f in spec.fields} if spec else {}
            shown = [
                f"{name.replace('_', ' ')} {value}"
                for name, value in holding.details
                if types.get(name) in {"identifier", "date"}
            ]
            whose = person or holding.subject
            lead = f"On file for {whose}: {holding.title}" if whose else f"On file: {holding.title}"
            text = f"{lead} ({'; '.join(shown)})." if shown else f"{lead}."
            out.append(Sentence(text, (), _citations([holding.passage()])))
        return out

    def _declined(self, question: str, packs: Sequence[InstalledPack]) -> Declined:
        """The pack's own decline, signed with its disclaimer, and a question it can answer."""
        asked = categories_asked(question, packs)
        owner = next((p for p in packs if asked and p.id == asked[0].pack_id), None)
        if owner is None and len(packs) == 1:
            owner = packs[0]
        text = owner.manifest.guardrails.advice_decline.strip() if owner else DEFAULT_DECLINE
        # Every ending is signed. With no single owner, the pack that answers questions about kinds
        # of document signs it; failing that, the strictest. Unsigned only with no pack enabled.
        signer = owner or next(
            (p for p in packs if p.manifest.answering.categories is not None),
            max(packs, key=lambda p: p.manifest.guardrails.abstain_below) if packs else None,
        )
        disclaimer = signer.manifest.guardrails.disclaimer.strip() if signer else ""
        offer = ""
        wanted = {a.category.id for a in asked}
        if wanted and self._inventory is not None:
            match = next(
                (
                    h
                    for h in self._inventory.holdings(packs)
                    if h.category and h.category.id in wanted
                ),
                None,
            )
            offer = f"What does my {match.printed_name} say?" if match else ""
        return Declined(text, disclaimer, offer)

    def _advice_shape(
        self, question: str, packs: Sequence[InstalledPack]
    ) -> tuple[InstalledPack, AdviceShape] | None:
        """The shape a question asks for, matched from the pack's own phrases without a model.

        The first pack in `packs` order that advises and has a phrase in the question wins, and
        within it the longest phrase, which is the more specific question. ADR 0016 rejected a
        model call here: a wrong shape is correct arithmetic on the wrong question.
        """
        if (review := _review_asked(question, packs)) is not None:
            return review
        for installed in packs:
            advice = installed.manifest.advice
            if advice is None:
                continue
            best: AdviceShape | None = None
            longest = 0
            for shape in advice.shapes:
                for phrase in shape.asked:
                    if len(phrase) > longest and mentions(question, phrase):
                        best, longest = shape, len(phrase)
            if best is not None:
                return installed, best
        return None

    def _review(
        self,
        installed: InstalledPack,
        adviser: Adviser,
        subject: Subject,
        question: str,
        today: date,
    ) -> Calculation | Missing:
        """Every shape the pack's review lists, for one person, as one calculation (ADR 0016
        addendum). Each shape's verdict and missing facts are code-written rows of one table, and
        each `holds` category nothing on file is gets its own row; the explanation that follows is
        the same single model call a shape gets."""
        advice = installed.manifest.advice
        assert advice is not None and advice.review is not None
        review, by_id = advice.review, {shape.id: shape for shape in advice.shapes}
        rows: list[tuple[str, ...]] = [("Check", "Finding")]
        inputs: dict[str, Input] = {}
        figures: list[Any] = []
        found: list[str] = []
        missing: list[str] = []
        short = False
        # What the household holds, read once before the shapes run: a short verdict names the
        # cover that closes it, and the `holds` rows below say what is on file. Both are the same
        # reading of the same documents, so reading it twice could disagree with itself.
        categories = installed.manifest.answering.categories
        labels: dict[str, str] = {}
        held: set[str] = set()
        on_file: list[Holding] = []
        if self._inventory is not None and categories is not None:
            on_file = self._narrowed(question, self._inventory.holdings([installed]))
            held = {h.category.id for h in on_file if h.category}
            labels = {rule.id: rule.label for rule in categories.rules}
        for shape_id in review.shapes:
            result = adviser.calculate(
                installed,
                by_id[shape_id],
                person_ids=subject.person_ids,
                subject=subject.name,
                today=today,
            )
            if isinstance(result, Calculation):
                finding = result.verdict_text
                if result.verdict == "short" and (closes := _closes(by_id[shape_id], labels, held)):
                    finding = f"{finding} {closes}"
                rows.append((result.label, finding))
                found.append(finding)
                inputs.update((item.ref, item) for item in result.inputs if item.ref not in inputs)
                figures.extend(result.figures)
                short = short or result.verdict == "short"
            else:
                rows.append((result.label, "Not checked yet. Needed: " + " ".join(result.items)))
                missing.extend(result.items)
        if self._inventory is not None and categories is not None:
            for category in review.holds:
                line = (
                    f"A {labels[category]} is on file."
                    if category in held
                    else f"No {labels[category]} is on file."
                )
                rows.append((labels[category], line))
                found.append(line)
        if not inputs:
            return Missing(installed.id, REVIEW, review.label, subject.name, tuple(missing + found))
        text = " ".join(found + ([f"Not checked yet: {' '.join(missing)}"] if missing else []))
        return Calculation(
            pack_id=installed.id,
            shape_id=REVIEW,
            label=review.label,
            subject=subject.name,
            person_ids=tuple(sorted(subject.person_ids)),
            inputs=tuple(inputs.values()),
            figures=tuple(figures),
            verdict="short" if short else "meets",
            verdict_text=text,
            rows=tuple(rows),
        )

    def _advise(
        self, question: str, packs: Sequence[InstalledPack], thread_id: str
    ) -> Iterator[Event]:
        """ADR 0016's advise branch. Two model calls in all: the router's, and this explanation.

        Nothing is retrieved and the question is not rewritten, because the evidence is the
        calculation, every input of it already cited. The order is the order of what may stop it:
        whose situation, then consent, then whether the inputs are there, and only then a model.

        A withheld or refused record is written *before* the ending it records is yielded, for the
        same reason: a consumer may stop at the first terminal event — `ask` does. An advised
        record is written from a single `finally`, whose `try` opens with the card's own `yield`
        and continues through the explanation, so a consumer may stop right there — at the card
        itself, at a `yield Sentence`, or between one and the next — and the record is still
        written for what was actually shown.
        """
        adviser, consents, advice_log = self._adviser, self._consents, self._advice_log
        match = self._advice_shape(question, packs)
        if match is None or adviser is None or consents is None or advice_log is None:
            yield self._declined(question, packs)
            return
        installed, shape = match
        advice = installed.manifest.advice
        assert advice is not None  # `_advice_shape` only matches a pack that advises
        disclaimer = advice.disclaimer.strip()

        subject = (
            self._household.whose(question)
            if self._household is not None
            else Subject(frozenset(), "", no_owner=True)
        )
        if subject.no_owner:
            yield AdviceWithheld(installed.id, shape.label, None, [NO_OWNER], disclaimer)
            return
        if subject.unknown_relation:
            yield _unknown_relation(subject.unknown_relation, disclaimer)
            return
        if subject.ambiguous or len(subject.person_ids) != 1:
            # A calculator adds up one person's documents. Two people's documents against one
            # person's guideline is a sum nobody could check, so the question is asked back. The
            # length check is the same refusal for a `Subject` that forgot to say it was ambiguous.
            yield Abstained(WHOSE_REASON, WHOSE_MISSING, 0, 0, None, disclaimer)
            return
        person = subject.name or None

        # The owner's consent covers adult members only (ADR 0016 addendum): a member under 21, or
        # a child whose date of birth is not on file, is withheld before consent is even asked.
        today = self._today or date.today()
        if (minor := _minor(subject, today)) is not None:
            yield AdviceWithheld(installed.id, shape.label, person, [minor], disclaimer)
            return

        consent_id = consents.current(installed.id, advice.consent_version)
        if consent_id is None:
            yield ConsentRequired(
                installed.id,
                installed.manifest.display_name,
                advice.consent_version,
                advice.consent_text.strip(),
                disclaimer,
                shape.label,
            )
            return

        result = (
            self._review(installed, adviser, subject, question, today)
            if shape.id == REVIEW
            else adviser.calculate(
                installed,
                shape,
                person_ids=subject.person_ids,
                subject=subject.name,
                today=today,
            )
        )
        entry = AdviceRecord(
            thread_id=thread_id,
            pack_id=installed.id,
            pack_version=installed.version,
            shape=shape.id,
            subject=subject.name,
            person_ids=tuple(sorted(subject.person_ids)),
            consent_id=consent_id,
            outcome="withheld",
            verdict=None,
            basis={},
            disclaimer=disclaimer,
            answer_text="",
        )
        if not isinstance(result, Calculation):
            items = list(result.items)
            advice_log.record(replace(entry, basis={"missing": items}, answer_text=" ".join(items)))
            yield AdviceWithheld(installed.id, result.label, person, items, disclaimer)
            return
        calc = result
        # A calculator that returned someone else's figures, or the wrong shape's, must never be
        # shown: showing them would be one household reading another's numbers. `_advise` already
        # guarantees a single-person subject before `calculate` is called, so a mismatch here is a
        # calculator bug, not a state this branch can recover from.
        if (
            calc.pack_id != installed.id
            or calc.shape_id != shape.id
            or set(calc.person_ids) != subject.person_ids
        ):
            raise ValueError(
                f"calculation for pack={calc.pack_id!r} shape={calc.shape_id!r} "
                f"person_ids={set(calc.person_ids)!r} does not match the question asked "
                f"(pack={installed.id!r} shape={shape.id!r} person_ids={subject.person_ids!r})"
            )

        evidence = passages_for(calc)
        chips = {
            passage.ref: _input_citation(item)
            for passage, item in zip(evidence[:-1], calc.inputs, strict=True)
        }
        cards = list(chips.values())
        chips[evidence[-1].ref] = Citation(None, "", 0, CALCULATION_CITATION, "calculation")
        # A review is explained in the order its pack's published guidance gives, and may cite
        # it (ADR 0016 addendum, 2 October). Not on the card: the card is the calculation's.
        guidance = _guidance(installed, today) if shape.id == REVIEW else []
        chips.update((passage.ref, chip) for passage, chip in guidance)
        evidence = [*evidence, *(passage for passage, _ in guidance)]
        product_disclosure = advice.product_disclosure.strip() if calc.names_product else ""
        exclusions = installed.manifest.answering.exclusions
        scanner = SentenceScanner()
        # The verdict on the card rests on every input, but never on the calculation passage
        # itself: "Worked out by Parrot from the inputs above" is not a source a screen can open,
        # so it is left out of what `Finished.citations` lists. A kept sentence's own
        # `citations` still carries it when the sentence cited the calculation, for the card.
        cited = [chip.text for chip in cards]
        kept: list[str] = []
        dropped: list[tuple[str, str]] = []
        truncated = False
        deltas: Iterator[str] = iter(())
        # How the explanation ended, written into the record below regardless of how this exits.
        # "stopped" is the honest default: a consumer that closes the stream at or after the card
        # — the card's own `yield` below is the first statement in the `try` — or any exception
        # besides `ModelUnavailable`, leaves it as is. The `try` sets "complete" only once its
        # body runs to its own end — whether the model exhausted itself or the sentence cap broke
        # the loop, both from inside the `try` — and the `except` sets "model_unavailable".
        # Nothing else may write to it.
        explanation = "stopped"
        try:
            # The card is yielded first, inside the `try`, so a `GeneratorExit` thrown into this
            # `yield` reaches the same `finally` as one thrown into a `yield Sentence` below —
            # a consumer that closes the stream exactly at the card still leaves a record.
            yield AdviceCard(
                pack_id=installed.id,
                label=calc.label,
                person=person,
                verdict=calc.verdict,
                verdict_text=calc.verdict_text,
                figures=[(figure.name, figure.text) for figure in calc.figures],
                inputs=cards,
                rows=[list(row) for row in calc.rows],
                estimate=calc.estimate,
                disclaimer=disclaimer,
                product_disclosure=product_disclosure,
                consent_version=advice.consent_version,
            )
            by_ref = {passage.ref: passage for passage in evidence}
            retrieved = set(by_ref)
            prompt = _advice_prompt(calc, shape, subject, today, evidence)
            deltas = self._client.constrained_stream(
                answer_system(installed), prompt, _ANSWER_SCHEMA
            )
            for delta in deltas:
                for item in scanner.feed(delta):
                    claim = self._claim(item, evidence)
                    why = (
                        check_one(claim, retrieved)
                        or check_content(claim, by_ref, exclusions=exclusions)
                        or check_advice(claim, by_ref, calc.figures, never_say=shape.never_say)
                    )
                    if why is not None:
                        if why != "empty":
                            dropped.append((claim.text, why))
                            log.info("gate dropped an explanation (%s): %.80s", why, claim.text)
                        continue
                    citations = _distinct(chips[ref] for ref in claim.supports)
                    cited.extend(c.text for c in citations if c.kind != "calculation")
                    kept.append(claim.text)
                    yield Sentence(claim.text, (), citations)
                    if len(kept) >= ADVICE_SENTENCES:
                        truncated = True
                        break
                if truncated:
                    break
            explanation = "complete"
        except ModelUnavailable as error:
            # The card is the answer and it has been given. An explanation that could not be
            # written is an explanation missing, not advice withdrawn.
            log.info("advice explanation stopped: %s", error)
            explanation = "model_unavailable"
        finally:
            close = getattr(deltas, "close", None)
            if callable(close):
                close()
            # Written here, after the stream is closed, so that a consumer stopping anywhere from
            # the card onward — a `GeneratorExit` thrown into the card's own `yield` above, or
            # into a `yield Sentence` further down, both included — still leaves a record: the
            # card is the first statement of the `try`, so a close from either point reaches this
            # one `finally`. This is the only place the advised outcome is recorded, so it is
            # written exactly once whichever way the `try` exits.
            advice_log.record(
                replace(
                    entry,
                    outcome="advised",
                    verdict=calc.verdict,
                    basis=_advice_basis(calc, kept, dropped, explanation, product_disclosure),
                    answer_text=" ".join([calc.verdict_text, *kept]),
                )
            )

        yield Finished(
            sorted(set(cited)),
            disclaimer,
            len(evidence),
            len(dropped),
            person,
            truncated=truncated,
            unanswered=False,
        )

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
            lambda state: "stop" if state.get("intent") in {"act", "advise"} else "explain",
            {"stop": END, "explain": "understand"},
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
        after that every `Sentence` is final; and exactly one of `Abstained`, `Refused`,
        `Declined` or `Finished` ends the stream. A `Sentence` with no chunk ids, written by
        code, may come first: "none of the policies on file is …", cited to the documents on file.

        `history` is the conversation before this question, as `(role, text)`. It is read by the
        router alone, to make a follow-up whole; it is never evidence, and nothing an earlier
        answer said can be cited by this one.
        """
        # The calendar first, and in code (ADR 0020): its rows are the whole answer to "what's
        # on", and a request to add an entry is drafted for a person to confirm, never refused
        # by the router as an act and never done.
        if self._calendar is not None:
            day = self._today or date.today()
            if wants_entry(question):
                yield draft(self._client, question, day, self._calendar.people())
                return
            reply = self._calendar.answer(question, day)
            if reply is not None:
                yield from _calendar_events(reply)
                return

        final: State = self._graph.invoke(
            {"question": question, "history": list(history)},
            {"configurable": {"thread_id": thread_id}},
        )
        packs = self._packs()
        if final.get("intent") == "act":
            yield Refused(REFUSAL)
            return
        if final.get("intent") == "advise":
            yield from self._advise(question, packs, thread_id)
            return

        passages = final.get("reranked") or []
        asked = _asked(final)

        # Whose question is this? Decided in `rerank`, over every candidate, and acted on here
        # before the floor, so an abstention about the wrong person is not reported as weak
        # evidence. See `core/graph/scope.py`.
        scoped = final.get("scoped")
        if scoped is not None and scoped.unknown_relation:
            yield _unknown_relation(scoped.unknown_relation)
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

        # Which kinds of document the question named, and which of them are on file. When none
        # is, "no" is a fact about the vault, and code says it — see `_absence`.
        wanted = set(final.get("categories") or [])
        on_file = self._on_file(asked, packs, scoped) if wanted else []
        present = [h for h in on_file if h.category and h.category.id in wanted]
        absence = self._absence(on_file, wanted, packs, person) if not present else None

        installed = _pack_for(passages or [h.passage() for h in on_file], packs)
        floor = installed.manifest.guardrails.abstain_below if installed else 0.42
        disclaimer = installed.manifest.guardrails.disclaimer.strip() if installed else ""
        limit = _max_sentences(installed)
        exclusions = installed.manifest.answering.exclusions if installed else None
        quarantined = self._inventory.quarantined() if absence and self._inventory else 0

        # Asked before the model runs. A question the evidence cannot support costs a retrieval,
        # not a retrieval and a generation that is then thrown away.
        refusal = precheck(passages, abstain_below=floor)
        if refusal is not None and absence is None and not present:
            yield Abstained(refusal, "", len(passages), 0, person, disclaimer)
            return

        # Weak passages are not read; the documents on file still are — their lines are facts.
        records = passages if refusal is None else []
        evidence = [*records, *(h.passage() for h in present)]
        yield Reading(len(evidence), person)
        kept: list[str] = []
        said_by_code = ([absence] if absence is not None else []) + self._presence(
            present, packs, person
        )
        for sentence in said_by_code:
            kept.extend(citation.text for citation in sentence.citations)
            yield sentence
        if not evidence:  # the inventory said "no" and nothing else can add to it
            yield Finished(sorted(set(kept)), disclaimer, 0, 0, person, quarantined)
            return

        by_ref = {passage.ref: passage for passage in evidence}
        retrieved = set(by_ref)
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
        elif scoped is not None and scoped.someone_else:
            # Named rather than related: "when does Rachel's policy renew?". Same reason as above.
            whose = f"The question is about {person}, not the person asking.\n\n"
        elif person:
            whose = f"The person asking is {person}. 'My', 'I' and 'mine' mean them.\n\n"
        else:
            whose = ""
        # "Still active", "due soon", "expired": a document's dates mean nothing without today's.
        today = f"Today is {(self._today or date.today()):%d %B %Y}.\n"
        words = f"\n(The person's own words: {question})" if asked != question else ""
        prompt = f"{today}{whose}Question: {asked}{words}\n\nPassages:\n{_numbered(evidence)}"
        scanner = SentenceScanner()
        dropped = said = 0
        truncated = False
        # "Last year", "last month": a sentence must cite a document from then. See `period.py`.
        when = asked_period(asked, self._today or date.today())
        periods = (
            self._inventory.periods([passage.document_id for passage in evidence])
            if when is not None and self._inventory is not None
            else {}
        )
        deltas = self._client.constrained_stream(answer_system(installed), prompt, _ANSWER_SCHEMA)
        try:
            for delta in deltas:
                for item in scanner.feed(delta):
                    claim = self._claim(item, evidence)
                    why = check_one(claim, retrieved) or check_content(
                        claim, by_ref, exclusions=exclusions
                    )
                    # The passages failed the floor, so only documents on file were read. Their
                    # lines print numbers, identifiers and dates; a sentence that states none of
                    # those is saying something the line does not.
                    if (
                        why is None
                        and refusal is not None
                        and not states_a_printed_value(
                            claim.text, [by_ref[ref] for ref in claim.supports]
                        )
                    ):
                        why = "says more than the documents on file"
                    if (
                        why is None
                        and when is not None
                        and self._inventory is not None
                        and outside(
                            when, (by_ref[ref].document_id for ref in claim.supports), periods
                        )
                    ):
                        why = f"cites no document from {when}"
                    if why is not None:
                        if why != "empty":
                            dropped += 1
                            log.info("gate dropped a sentence (%s): %.80s", why, claim.text)
                        continue
                    citations = _citations(by_ref[ref] for ref in claim.supports)
                    kept.extend(citation.text for citation in citations)
                    chunk_ids = tuple(
                        by_ref[ref].chunk_id
                        for ref in claim.supports
                        if by_ref[ref].kind == "document"
                    )
                    yield Sentence(claim.text, chunk_ids, citations)
                    said += 1
                    if said >= limit:
                        truncated = True
                        break
                if truncated:
                    break
        except ModelUnavailable as error:
            # Sentences already yielded were verified and stay said. What follows is the honest
            # account of why there are no more of them.
            if kept:
                yield Finished(
                    sorted(set(kept)),
                    disclaimer,
                    len(evidence),
                    dropped,
                    person,
                    quarantined,
                    unanswered=bool(said_by_code) and said == 0,
                )
            else:
                yield Abstained(str(error), "", len(evidence), dropped, person, disclaimer)
            return
        finally:
            close = getattr(deltas, "close", None)
            if callable(close):
                close()  # a capped answer stops the generator, and the GPU with it

        if not kept:
            # The model wrote nothing, or nothing it wrote could be traced to a document. Its own
            # `missing` says which document would have answered, when it offered one.
            yield Abstained(
                "nothing in the answer could be traced to a document",
                scanner.missing(),
                len(evidence),
                dropped,
                person,
                disclaimer,
            )
            return
        yield Finished(
            sorted(set(kept)),
            disclaimer,
            len(evidence),
            dropped,
            person,
            quarantined,
            truncated,
            # Code said what is on file and the model added nothing that survived: that line is
            # not the answer, and the trace says so.
            unanswered=bool(said_by_code) and said == 0,
        )

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
        card: AdviceCard | None = None

        for event in self.stream(question, thread_id=thread_id, history=history):
            if isinstance(event, Refused):
                return Answer(event.text, refused=True)
            if isinstance(event, Drafted):
                when = event.starts_on.strftime("%A %d %B").replace(" 0", " ")
                return Answer(
                    f"Draft calendar entry: {event.title}, {when}. {event.note}", draft=event
                )
            if isinstance(event, Declined):
                return Answer(
                    event.text, declined=True, disclaimer=event.disclaimer, offer=event.offer
                )
            if isinstance(event, ConsentRequired):
                return Answer(
                    event.consent_text, consent_required=True, disclaimer=event.disclaimer
                )
            if isinstance(event, AdviceWithheld):
                missing = " ".join(_as_sentence(item) for item in event.missing)
                return Answer(
                    f"{event.label[:1].upper()}{event.label[1:]} cannot be worked out yet. "
                    f"{missing}",
                    withheld=True,
                    missing=missing,
                    disclaimer=event.disclaimer,
                    person=event.person or "",
                )
            if isinstance(event, AdviceCard):
                card = event
            elif isinstance(event, Reading):
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
                    disclaimer=event.disclaimer,
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
                if card is not None:
                    # The verdict leads, because it is the answer; the explanation follows it.
                    signed = [event.disclaimer, card.product_disclosure]
                    return Answer(
                        " ".join([card.verdict_text, *lines]),
                        citations=event.citations,
                        passages_read=event.passages_read,
                        dropped=event.dropped,
                        disclaimer=" ".join(part for part in signed if part),
                        claims=claims,
                        person=event.person or "",
                        truncated=event.truncated,
                        advice=True,
                        verdict_text=card.verdict_text,
                    )
                return Answer(
                    " ".join(lines),
                    citations=event.citations,
                    passages_read=event.passages_read,
                    dropped=event.dropped,
                    disclaimer=event.disclaimer,
                    claims=claims,
                    person=event.person or "",
                    quarantined=event.quarantined,
                    truncated=event.truncated,
                    unanswered=event.unanswered,
                )

        # Unreachable: `stream` always ends on a terminal event. Kept because a silent `None`
        # here would be the worst possible failure in this file.
        return Answer(
            "I can't answer that from your documents: the answer did not finish.",
            abstained=True,
            passages_read=passages_read,
            reason="the answer did not finish",
        )
