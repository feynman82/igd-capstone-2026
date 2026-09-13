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
from dataclasses import dataclass
from typing import Any

from core.graph.ports import Passage

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
    r"father|mother|dad|mum|mom|papa|parent|parents|grandfather|grandmother|"
    r"grandpa|grandma|brother|sister|sibling|in-law|our|we|us|everyone|household|family)\b"
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
    # People who work for a household rather than belong to it. No relation matches them, so a
    # question about "my maid's hospital bills" says Parrot does not know who that is rather than
    # answering from the owner's own hospital plan — which it did, on 13 September.
    **dict.fromkeys(("maid", "helper", "nanny", "driver", "tenant"), "outside"),
}
_RELATION = re.compile(
    r"(?i)\bmy\s+("
    + "|".join(sorted(_RELATION_WORDS, key=len, reverse=True))
    + r")(?:'s|\u2019s|s'|'|\u2019)"  # a straight or a typographic apostrophe
)


def relation_asked(question: str) -> tuple[str, str] | None:
    """`(word, relation)` when the question asks about a relation's own documents, else `None`."""
    match = _RELATION.search(question)
    if match is None:
        return None
    word = match.group(1).lower()
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
) -> Scoped:
    """Keep the passages of these people and of the household; set aside everybody else's."""
    if not passages:
        return Scoped([], name, about=about)

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
    return Scoped(kept, name, tuple(sorted(dropped)), about=about)


@dataclass(frozen=True, slots=True)
class HouseholdScope:
    """What `AnswerGraph` is handed so it can scope without holding a connection.

    Built per request by whoever has one — `api/routes.py` and `scripts/ask.py` — and passed in.
    The graph asks it one question and does not know what a person is.
    """

    conn: Any

    def apply(self, question: str, passages: list[Passage]) -> Scoped:
        from core import household

        owner = household.owner(self.conn)
        if owner is None:
            # Nobody has said who they are. Every question is about the household, which is
            # exactly how Parrot behaved before any of this existed.
            return Scoped(passages, None)

        roster = household.roster(self.conn)
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
                return Scoped(passages, None, unknown_relation=word)
            return scope_to(
                self.conn,
                passages,
                person_ids=frozenset(person.id for person in members),
                name=" and ".join(person.display_name for person in members),
                about=word,
            )

        others = tuple(
            name
            for person in roster
            if person.id != owner.id
            for name in (person.display_name, *person.aliases)
        )
        if not is_first_person(question, others):
            return Scoped(passages, None)

        return scope_passages(self.conn, passages, owner_id=owner.id, owner_name=owner.display_name)
