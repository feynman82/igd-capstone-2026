"""Whose question is this, and whose documents may answer it.

"What is my term life premium?" retrieves every term life policy in the house. Reranking scores
text against text and has no opinion about people, so the answer node writes a sentence from
whichever policy ranked first and cites it correctly. The citation is true. The answer is about
the wrong person. Nothing downstream can catch that, because every check the graph has is a
check that a sentence is supported — and it is. See ADR 0011.

This module is the missing filter. It does two things and refuses to do a third.

**It decides whether a question is first-person at all**, conservatively. "My term life premium"
is; "my wife's premium" is not, even though it starts the same way, and neither is "Rachel's
premium". A question that names somebody else, or that uses a relationship word, is left
unscoped — an over-eager filter that silently drops the only document that would have answered
is worse than no filter, because the failure looks like an empty vault rather than like a bug.

**It scopes a question that names exactly one person**, whether or not it says "my". "What is
Marcus's premium?" from Marcus is his; "when does Rachel's policy renew?" is Rachel's. A name is a
whole display name or confirmed alias, or a possessive word — "Rachel's" — that belongs to one
person only, so "Lim's", shared by a son and his father, names nobody. A question naming two
people, or somebody else alongside "my", is about more than one person and is left unscoped. See
ADR 0015.

**It partitions retrieved passages into mine, theirs and the household's.** A passage is the
household's when the documents behind it carry no subject at all — the home contents policy, the
utility bill. Those always survive the filter. Only passages that resolve to a *different*
person are dropped.

**It does not push the filter into SQL.** `core/graph/ports.py` is the contract with Lane B's
`core/retrieve/`, and widening `search()` with a `subject` argument would break every
implementation of it the week two lanes are building against it. So scoping happens after
retrieval and before reranking, which costs one round trip and a documented limitation: a
passage that did not survive the candidate cut cannot be scoped back in. When Lane B's hybrid
search lands, pushing the predicate down into the query is theirs to do, and the eval number
will say whether it was worth it.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

from core.graph.ports import Passage

if TYPE_CHECKING:
    from core.household import Person

log = logging.getLogger(__name__)

# "My", "mine", "I" and "me" as whole words. `I` is case-sensitive on purpose: the pronoun is
# always capitalised in English, and a lowercase `i` in a household question is far more often
# a stray keystroke than a first person.
_FIRST_PERSON = re.compile(r"(?i)\b(?:my|mine|myself|me)\b|\bI\b")

# Words that make a question somebody else's even when it opens with "my". "My wife's policy"
# is a question about the wife. Rather than try to resolve the relationship — which needs a
# roster we may not have and grammar we certainly do not — the question is simply left unscoped
# and answered from the whole vault, which is what Parrot did before any of this existed.
_SOMEONE_ELSE = re.compile(
    r"(?i)\b(?:wife|husband|spouse|partner|son|daughter|child|children|kid|kids|"
    r"father|mother|dad|daddy|mum|mummy|mom|mommy|mama|papa|parent|parents|grandfather|"
    r"grandmother|grandpa|grandma|grandparent|grandparents|granddad|grandad|granny|grandmum|"
    r"ah\s+gong|ah\s+kong|ah\s+ma|ah\s+mah|popo|"
    r"brother|sister|sibling|in-law|our|we|us|everyone|household|family)\b"
)


# "My son's", "my dad's": a possessive relationship word is a question about that member of the
# household's own documents. Only the possessive: "does my policy cover my son?" may well be
# answered by the owner's policy, and is left unscoped.
#
# Measured on 13 September: "how much is my son's life insurance?" retrieved the owner's whole
# life policy above the pack's floor, and the generator wrote "the life insurance policy for your
# son, Marcus Lim Jun Wei, has a Sum Assured of SGD 300,000.00" — cited, and about the wrong
# person. No household member is recorded as a child, so the honest answer is that Parrot does
# not know who that is yet.
_RELATION_WORDS: dict[str, str] = {
    **dict.fromkeys(("wife", "husband", "spouse", "partner"), "partner"),
    **dict.fromkeys(("son", "daughter", "child", "children", "kid", "kids"), "child"),
    **dict.fromkeys(
        (
            "father",
            "mother",
            "dad",
            "daddy",
            "mum",
            "mummy",
            "mom",
            "mommy",
            "mama",
            "papa",
            "parent",
            "parents",
        ),
        "parent",
    ),
    # A relation `people.relation` cannot record — the roster stops at parent, and "anything
    # finer is `other` plus a display name" (0002_household.sql). Nobody holds it, so the question
    # is an abstention unless somebody is recorded under the word itself: a person whose display
    # name or confirmed alias is "Grandpa" is who "my grandpa" means. Mapping it to `parent`
    # would answer from the father's policy, which is what it did on 13 September; mapping it to
    # `other` would answer from whoever was once the owner.
    **dict.fromkeys(
        (
            "grandfather",
            "grandmother",
            "grandpa",
            "grandma",
            "grandparent",
            "grandparents",
            "granddad",
            "grandad",
            "granny",
            "grandmum",
            "ah gong",
            "ah kong",
            "ah ma",
            "ah mah",
            "popo",
        ),
        "grandparent",
    ),
    # People who work for a household rather than belong to it. No relation matches them, so a
    # question about "my maid's hospital bills" says Parrot does not know who that is rather than
    # answering from the owner's own hospital plan — which it did, on 13 September.
    **dict.fromkeys(("maid", "helper", "nanny", "driver", "tenant"), "outside"),
}
_RELATION = re.compile(
    r"(?i)\bmy\s+("
    + "|".join(
        re.escape(word).replace(r"\ ", r"\s+")
        for word in sorted(_RELATION_WORDS, key=len, reverse=True)
    )
    + r")(?:'s|\u2019s|s'|'|\u2019)"  # a straight or a typographic apostrophe
)


def relation_asked(question: str) -> tuple[str, str] | None:
    """`(word, relation)` when the question asks about a relation's own documents, else `None`."""
    match = _RELATION.search(question)
    if match is None:
        return None
    word = " ".join(match.group(1).lower().split())
    return word, _RELATION_WORDS[word]


@dataclass(frozen=True, slots=True)
class Scoped:
    """The result of asking "whose is this?" of a question and its passages."""

    passages: list[Passage]
    """What survived. Unscoped questions return everything, unchanged."""

    person_name: str | None
    """Who it was scoped to, for the chip on the answer. `None` when nothing was scoped."""

    dropped_people: tuple[str, ...] = ()
    """Whose documents were set aside. This is what makes the abstention useful: "you have no
    term life policy filed; there is one for Rachel Ng Hui Shan" needs the name."""

    about: str | None = None
    """The relationship word when the question is about a household member rather than the person
    asking — "dad" in "is my dad's hospital cover still active?". `person_name` is then who the
    question is about, and the answer must not be told that they are the one asking."""

    unknown_relation: str | None = None
    """The relationship word asked about when nobody in the household holds that relation — "son"
    in "my son's life insurance" when no child is recorded. The graph abstains on it rather than
    answering from the owner's documents."""

    someone_else: bool = False
    """Scoped to a household member the question named — "when does Rachel's policy renew?" —
    who is not the person asking. There is no relationship word to put in the prompt, and the
    answer must still not be told that they are the one asking."""

    @property
    def scoped(self) -> bool:
        return self.person_name is not None

    @property
    def empty_for_owner(self) -> bool:
        """A first-person question that nothing of the owner's can answer.

        The interesting case, and the one worth abstaining on rather than answering around:
        somebody asked about their own policy and the vault holds somebody else's.
        """
        return self.scoped and not self.passages


def is_first_person(question: str, other_names: tuple[str, ...] = ()) -> bool:
    """Whether this question is about the person asking.

    `other_names` are the display names and aliases of everybody who is not the owner. A
    question that names one of them is theirs, whatever pronouns surround it: "is my dad's
    hospital cover still active" and "when does Rachel's policy renew" are both questions the
    owner is asking about somebody else.
    """
    if not _FIRST_PERSON.search(question):
        return False
    if _SOMEONE_ELSE.search(question):
        return False
    lowered = question.lower()
    return not any(name.strip() and name.strip().lower() in lowered for name in other_names)


# A word of a name, for the possessive match. Three letters or more: "Ng" and "Ah" are names, and
# also far too often something else in a typed question.
_NAME_WORD = re.compile(r"[^\W\d_]{3,}")
_POSSESSIVE = r"(?:['\N{RIGHT SINGLE QUOTATION MARK}]s?)(?!\w)"


def _names(person: Person) -> set[str]:
    return {" ".join(n.split()) for n in (person.display_name, *person.aliases) if n.strip()}


def named_in(question: str, people: Sequence[Person]) -> list[Person]:
    """Everybody in `people` the question names.

    A person is named by a whole display name or confirmed alias anywhere in the question, or by
    one word of those names written possessively — "Rachel's" — when that word is nobody else's.
    Only people with a confirmed name can be named: a model proposal is a question on Today, not
    a member yet.
    """
    whose_word: dict[str, set[int]] = {}
    for person in people:
        for name in _names(person):
            for word in _NAME_WORD.findall(name.lower()):
                whose_word.setdefault(word, set()).add(person.id)

    named: list[Person] = []
    for person in people:
        if not person.aliases:
            continue
        names = _names(person)
        whole = any(
            re.search(r"(?i)(?<!\w)" + re.escape(name).replace(r"\ ", r"\s+") + r"(?!\w)", question)
            for name in names
        )
        own_words = {
            word
            for name in names
            for word in _NAME_WORD.findall(name.lower())
            if whose_word[word] == {person.id}
        }
        possessive = any(
            re.search(r"(?i)(?<!\w)" + re.escape(word) + _POSSESSIVE, question)
            for word in own_words
        )
        if whole or possessive:
            named.append(person)
    return named


# One statement, parameterised, per rule 1. Which people the documents behind a set of passages
# resolve to — confirmed aliases only, so an unreviewed model guess can never scope an answer.
DOCUMENT_PEOPLE = """
SELECT f.document_id, p.id, p.display_name
  FROM facts f
  JOIN person_aliases a ON lower(btrim(a.alias)) = lower(btrim(f.subject)) AND a.confirmed
  JOIN people p         ON p.id = a.person_id
 WHERE f.document_id = ANY(%(document_ids)s::uuid[])
 GROUP BY f.document_id, p.id, p.display_name
"""


def scope_passages(
    conn: Any,
    passages: list[Passage],
    *,
    owner_id: int,
    owner_name: str,
) -> Scoped:
    """Keep the owner's passages and the household's; set aside everybody else's.

    A document with no resolvable subject is the household's and is kept. That is the third
    bucket, and leaving it out is how "my home insurance" breaks quietly.
    """
    return scope_to(conn, passages, person_ids=frozenset({owner_id}), name=owner_name)


def scope_to(
    conn: Any,
    passages: list[Passage],
    *,
    person_ids: frozenset[int],
    name: str,
    about: str | None = None,
    someone_else: bool = False,
) -> Scoped:
    """Keep the passages of these people and of the household; set aside everybody else's."""
    if not passages:
        return Scoped([], name, about=about, someone_else=someone_else)

    ids = list({p.document_id for p in passages})
    with conn.cursor() as cur:
        cur.execute(DOCUMENT_PEOPLE, {"document_ids": ids})
        rows = cur.fetchall()

    by_document: dict[Any, set[int]] = {}
    names: dict[int, str] = {}
    for document_id, person_id, display_name in rows:
        by_document.setdefault(document_id, set()).add(int(person_id))
        names[int(person_id)] = display_name

    kept: list[Passage] = []
    dropped: set[str] = set()
    for passage in passages:
        people = by_document.get(passage.document_id)
        # No resolvable subject: the household's, and everybody's. Keep it.
        if not people or people & person_ids:
            kept.append(passage)
            continue
        dropped.update(names[person_id] for person_id in people)

    if dropped:
        log.info("scope: kept %d of %d passages for %s", len(kept), len(passages), name)
    return Scoped(kept, name, tuple(sorted(dropped)), about=about, someone_else=someone_else)


@dataclass(frozen=True, slots=True)
class Subject:
    """Whose situation a piece of advice is about — `whose`'s answer, with no passages in it.

    Advice is written about exactly one person, so unlike `Scoped` there is no "unscoped" state
    the way `apply` has one: every question resolves to somebody, a name the household does not
    recognise (`unknown_relation`), or the honest refusal to guess (`ambiguous`). `no_owner` is
    the one case with nobody to guess: an install nobody has claimed yet.

    `ambiguous` is set instead of a person whenever the question could reasonably be about more
    than one person: somebody other than the owner named, two or more people named, a
    someone-else or household word, or a relation word more than one confirmed member holds
    ("my dad's" with a father and a mother both recorded as `parent`). `apply` answers those same
    questions from everything rather than narrowing — a wrong inclusion in retrieval is a passage
    that should have been dropped, still correctly cited, so it costs nothing to fall back. Advice
    has no "everything" to fall back to: a wrong single person is a wrong sum silently handed to a
    calculator, so `whose` reports the uncertainty instead of guessing through it. `person_ids`
    and `name` are empty whenever `ambiguous` is set — there is deliberately no fallback person to
    read them as.
    """

    person_ids: frozenset[int]
    name: str
    about: str | None = None
    unknown_relation: str | None = None
    no_owner: bool = False
    someone_else: bool = False
    """Scoped to a household member the question named who is not the person asking — "is
    Rachel's cover enough?" gives Rachel with `someone_else=True`. Carried through from the same
    decision `apply` makes, so advice never addresses somebody as if they had asked it themselves.
    """
    ambiguous: bool = False


@dataclass(frozen=True, slots=True)
class _Decision:
    """Who a question is about, decided once and read differently by `apply` and `whose`.

    `fallthrough` is why `apply` would leave the question unscoped, or `"none"` when it would not:

    - `"named_other"` — somebody other than the owner was named, or two or more people were.
    - `"someone_else"` — a someone-else or household word (`_SOMEONE_ELSE`), or another person's
      name found in the text some other way, made the question not first-person.
    - `"impersonal"` — no first-person word, no someone-else word, nobody named: there is nothing
      here to be unsure about, only nothing said.

    `apply` treats all three exactly alike — any value other than `"none"` means "answer from
    everything" — because widening only risks a wrong inclusion, still correctly cited, so it
    never needs to tell them apart. `person_ids`/`name` are pre-filled with the owner for all
    three, which is what lets `apply`'s pre-refactor behaviour and `whose`'s guess-the-owner case
    share one code path.

    `whose` cannot fall back to "everything" — advice is about one person — so it tells
    `"impersonal"` apart from the other two: a question with nothing said about anybody is the
    same guess of last resort `whose` makes for an unambiguous first-person question, so it reads
    the pre-filled owner off `person_ids`/`name`. `"named_other"` and `"someone_else"` are real
    ambiguity — more than one person could be meant — and `whose` refuses to guess between them.

    `relation_ambiguous` is a second, independent axis: a relation word matched more than one
    confirmed member (a father and a mother both recorded as `parent`). `apply` keeps scoping to
    all of them, which is still only a wrong-inclusion risk, so it never reads this field —
    `person_ids` holds every match either way. `whose` does read it, because advice about "my dad"
    cannot honestly pick one of two fathers.
    """

    owner: Person | None
    person_ids: frozenset[int] = frozenset()
    name: str = ""
    about: str | None = None
    unknown_relation: str | None = None
    someone_else: bool = False
    fallthrough: Literal["none", "named_other", "someone_else", "impersonal"] = "none"
    relation_ambiguous: bool = False


def _decide(conn: Any, question: str) -> _Decision:
    """The one place `apply` and `whose` agree on who a question is about.

    Pulled out of `apply` so the two questions it and `whose` each ask — which passages does this
    question license, and whose situation is a piece of advice about — read the same roster the
    same way, and cannot quietly drift onto different answers for the same input.
    """
    from core import household

    owner = household.owner(conn)
    if owner is None:
        return _Decision(owner=None)

    roster = household.roster(conn)
    asked = relation_asked(question)
    if asked is not None:
        word, relation = asked
        # A person with no confirmed name is still a question on Today, not a member yet.
        members = [
            person
            for person in roster
            if not person.is_owner
            and not person.external
            and person.relation == relation
            and person.aliases
        ]
        if not members:
            # Nobody holds it — always so for a grandparent. The household may still have
            # recorded somebody under the word itself: "Grandpa", placed as `other`.
            members = [
                person
                for person in roster
                if not person.is_owner
                and person.aliases
                and word in {name.lower() for name in _names(person)}
            ]
        if not members:
            return _Decision(owner=owner, unknown_relation=word)
        return _Decision(
            owner=owner,
            person_ids=frozenset(person.id for person in members),
            name=" and ".join(person.display_name for person in members),
            about=word,
            # More than one confirmed member holds this relation: `apply` still scopes to all of
            # them (see the class docstring), but `whose` has to write advice about one person and
            # cannot honestly pick between, say, a father and a mother.
            relation_ambiguous=len(members) > 1,
        )

    # A question that names one person is theirs, "my" or not. The owner naming themselves —
    # "what is Marcus's premium?" — is the owner's; anybody else is scoped only when the
    # question does not also say "my", which would make it about two people.
    named = named_in(question, roster)
    if len(named) == 1 and named[0].id == owner.id:
        return _Decision(owner=owner, person_ids=frozenset({owner.id}), name=owner.display_name)
    if len(named) == 1 and not _FIRST_PERSON.search(question):
        return _Decision(
            owner=owner,
            person_ids=frozenset({named[0].id}),
            name=named[0].display_name,
            someone_else=True,
        )
    if any(person.id != owner.id for person in named):
        # Somebody other than the owner was named, or two or more people were — either way, more
        # than one person could be meant. `person_ids`/`name` are pre-filled with the owner so
        # `apply`'s call site does not have to know that; `whose` ignores them (see `fallthrough`).
        return _Decision(
            owner=owner,
            person_ids=frozenset({owner.id}),
            name=owner.display_name,
            fallthrough="named_other",
        )

    others = tuple(
        name
        for person in roster
        if person.id != owner.id
        for name in (person.display_name, *person.aliases)
    )
    if not is_first_person(question, others):
        # `is_first_person` folds three different reasons into one `False`: no first-person word
        # at all, a someone-else/household word, or another person's name found some other way.
        # `apply` does not need to tell them apart — any of the three leaves it unscoped — but
        # `whose` does: only the first of the three has nothing to be unsure about (see
        # `_Decision.fallthrough`), so it is named apart from the other two here rather than
        # re-deriving `is_first_person`'s internals a second time.
        fallthrough: Literal["someone_else", "impersonal"] = (
            "impersonal"
            if _FIRST_PERSON.search(question) is None and not _SOMEONE_ELSE.search(question)
            else "someone_else"
        )
        return _Decision(
            owner=owner,
            person_ids=frozenset({owner.id}),
            name=owner.display_name,
            fallthrough=fallthrough,
        )

    return _Decision(owner=owner, person_ids=frozenset({owner.id}), name=owner.display_name)


@dataclass(frozen=True, slots=True)
class HouseholdScope:
    """What `AnswerGraph` is handed so it can scope without holding a connection.

    Built per request by whoever has one — `api/routes.py` and `scripts/ask.py` — and passed in.
    The graph asks it one question and does not know what a person is.
    """

    conn: Any

    def apply(self, question: str, passages: list[Passage]) -> Scoped:
        decision = _decide(self.conn, question)
        if decision.owner is None:
            # Nobody has said who they are. Every question is about the household, which is
            # exactly how Parrot behaved before any of this existed.
            return Scoped(passages, None)
        if decision.unknown_relation is not None:
            return Scoped(passages, None, unknown_relation=decision.unknown_relation)
        if decision.fallthrough != "none":
            return Scoped(passages, None)
        return scope_to(
            self.conn,
            passages,
            person_ids=decision.person_ids,
            name=decision.name,
            about=decision.about,
            someone_else=decision.someone_else,
        )

    def whose(self, question: str) -> Subject:
        """Whose situation a piece of advice is about — the judgement `apply` makes, without
        passages to filter.

        A piece of advice is written about exactly one person, unlike retrieval, which can fall
        back to "everything" when a question does not narrow cleanly. Where `apply` leaves a
        question unscoped because there is nothing to lose by widening — a wrong inclusion is
        still correctly cited — `whose` has no "everything" to hand a calculator, so it refuses to
        guess: `ambiguous=True` and an empty `Subject`, whenever the question named somebody other
        than the owner, named two or more people, used a someone-else or household word, or asked
        about a relation more than one confirmed member holds (`_Decision.fallthrough` and
        `relation_ambiguous`). The one fall-through `apply` also makes that is *not* ambiguity —
        a question that names nobody and uses no relation word or someone-else word, so there is
        nothing here to be unsure about — resolves to the owner, the same guess `whose` makes for
        an unambiguous first-person question: `_decide` already put the owner in
        `person_ids`/`name` for that case, so this reads no differently.
        """
        decision = _decide(self.conn, question)
        if decision.owner is None:
            return Subject(person_ids=frozenset(), name="", no_owner=True)
        if decision.unknown_relation is not None:
            return Subject(
                person_ids=frozenset(), name="", unknown_relation=decision.unknown_relation
            )
        if decision.relation_ambiguous or decision.fallthrough in ("named_other", "someone_else"):
            return Subject(person_ids=frozenset(), name="", ambiguous=True)
        return Subject(
            person_ids=decision.person_ids,
            name=decision.name,
            about=decision.about,
            someone_else=decision.someone_else,
        )
