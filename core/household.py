"""Who lives here, what they are called on paper, and which one of them is you.

`facts.subject` has always carried whose a fact is — the string the document printed. What was
missing is the other half: which of those strings mean the person typing. Without it "what is
my term life premium?" retrieves every term life policy in the house and answers from whichever
one ranked first, **with a correct citation to the wrong person's policy**. That is the single
failure the grounding gate cannot catch, because the sentence really is supported by the
passage it names. See ADR 0011.

Three ideas hold this module up.

**A person is a row; the strings are aliases.** `MARCUS LIM JUN WEI`, `Lim Jun Wei, Marcus` and
`M. J. W. Lim` are three aliases of one person. `facts.subject` is never rewritten to match —
what the page said stays what the page said, and the mapping lives beside it. A household that
later corrects its roster does not thereby edit its own documents' history.

**The roster is derived, then confirmed.** Setup asks one question: the name on your documents.
Everyone else arrives off a document, is classified by the generator, and is shown to a person
as a question before it is allowed to scope anything. `resolve` and `owner_aliases` read only
confirmed aliases, which is the sentence that makes a wrong model guess cost a tap instead of a
wrong answer.

**Absent is not excluded.** A question about "my" documents wants three things: facts that
resolve to the owner, *and* facts with no subject at all — the home contents policy, the
utility bill, the things that belong to the household rather than to a member of it. Only facts
that resolve to a different person are excluded. Two buckets instead of three breaks "my home
insurance" quietly, which is the worst way for it to break.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Literal

log = logging.getLogger(__name__)

Relation = Literal["self", "partner", "child", "parent", "other"]

RELATIONS: tuple[Relation, ...] = ("self", "partner", "child", "parent", "other")

# A model proposal below this is still written down, still shown, and still needs a person —
# it simply does not get to pre-select an answer in the interface. It is not a gate on
# correctness (nothing unconfirmed scopes anything) but on how confidently a question is
# phrased, which is worth a number rather than a guess.
SUGGEST_ABOVE = 0.6


@dataclass(frozen=True, slots=True)
class Person:
    id: int
    display_name: str
    relation: Relation
    is_owner: bool
    external: bool
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PendingAlias:
    """An unknown name off a document, and what the model thinks it is.

    `person_id` is the model's proposal and may be wrong; `person_name` is that person's
    display name, so a screen can ask "is this Rachel?" without a second query.
    """

    id: int
    alias: str
    person_id: int | None
    person_name: str | None
    confidence: float | None
    document_id: Any | None
    document_name: str | None


# --------------------------------------------------------------------------------- the SQL
#
# Rule 1: every statement is written here and parameterised. Nothing is assembled at runtime.

SELECT_PEOPLE = """
SELECT p.id, p.display_name, p.relation, p.is_owner, p.external,
       coalesce(
           array_agg(a.alias ORDER BY a.alias) FILTER (WHERE a.id IS NOT NULL AND a.confirmed),
           '{}'
       )
  FROM people p
  LEFT JOIN person_aliases a ON a.person_id = p.id
 GROUP BY p.id
 ORDER BY p.is_owner DESC, p.external, p.display_name
"""

SELECT_OWNER = """
SELECT p.id, p.display_name, p.relation, p.is_owner, p.external,
       coalesce(
           array_agg(a.alias ORDER BY a.alias) FILTER (WHERE a.id IS NOT NULL AND a.confirmed),
           '{}'
       )
  FROM people p
  LEFT JOIN person_aliases a ON a.person_id = p.id
 WHERE p.is_owner
 GROUP BY p.id
"""

INSERT_PERSON = """
INSERT INTO people (display_name, relation, is_owner, external)
VALUES (%(display_name)s, %(relation)s, %(is_owner)s, %(external)s)
RETURNING id
"""

# `ON CONFLICT` on the lower(btrim(alias)) index: filing the same name twice is not an error,
# it is Tuesday. An existing alias keeps the person it already resolves to — a second document
# must never silently move a name from one member of the household to another.
INSERT_ALIAS = """
INSERT INTO person_aliases
       (person_id, alias, source, confirmed, confidence, document_id, decided_at)
VALUES (%(person_id)s, %(alias)s, %(source)s, %(confirmed)s, %(confidence)s, %(document_id)s,
        CASE WHEN %(confirmed)s THEN now() ELSE NULL END)
ON CONFLICT (lower(btrim(alias))) DO NOTHING
RETURNING id
"""

# Confirmed only. This is the sentence that keeps an unreviewed model guess out of retrieval.
RESOLVE_ALIAS = """
SELECT p.id, p.display_name, p.relation, p.is_owner, p.external
  FROM person_aliases a
  JOIN people p ON p.id = a.person_id
 WHERE a.confirmed
   AND lower(btrim(a.alias)) = lower(btrim(%(alias)s))
"""

SELECT_ALIASES_FOR = """
SELECT a.alias
  FROM person_aliases a
 WHERE a.confirmed AND a.person_id = %(person_id)s
 ORDER BY a.alias
"""

SELECT_PENDING = """
SELECT a.id, a.alias, a.person_id, p.display_name, a.confidence, a.document_id, d.original_name
  FROM person_aliases a
  LEFT JOIN people p    ON p.id = a.person_id
  LEFT JOIN documents d ON d.id = a.document_id
 WHERE NOT a.confirmed
 ORDER BY a.created_at
"""

COUNT_PENDING = "SELECT count(*) FROM person_aliases WHERE NOT confirmed"

CONFIRM_ALIAS = """
UPDATE person_aliases
   SET person_id = %(person_id)s, confirmed = true, source = 'user', decided_at = now()
 WHERE id = %(id)s
RETURNING alias
"""

DELETE_ALIAS = "DELETE FROM person_aliases WHERE id = %(id)s RETURNING alias"

# Where somebody sits in the household, decided by a person on a screen. Never the owner: the
# owner's relation is `self` by definition, and changing who that is is `set_owner`.
SET_PLACE = """
UPDATE people
   SET relation = %(relation)s, external = %(external)s
 WHERE id = %(id)s AND NOT is_owner
RETURNING id
"""

CLEAR_OWNER = "UPDATE people SET is_owner = false WHERE is_owner"

SET_OWNER = """
UPDATE people
   SET is_owner = true, relation = 'self', external = false
 WHERE id = %(id)s
RETURNING id
"""

# Relation follows the owner, so promoting somebody leaves the previous owner needing one. They
# become `other` rather than a guess: Parrot does not know whether the person handing over the
# paperwork is a parent, a partner or a landlord, and inventing it would be worse than asking.
DEMOTE_PREVIOUS_OWNER = "UPDATE people SET relation = 'other' WHERE id = %(id)s"

SELECT_TELEGRAM_PERSON = """
SELECT person_id FROM telegram_identities WHERE chat_id = %(chat_id)s
"""

UPSERT_TELEGRAM_IDENTITY = """
INSERT INTO telegram_identities (chat_id, person_id)
VALUES (%(chat_id)s, %(person_id)s)
ON CONFLICT (chat_id) DO UPDATE SET person_id = EXCLUDED.person_id
"""

UPSERT_ATTRIBUTION = """
INSERT INTO document_attribution (document_id, person_id, source)
VALUES (%(document_id)s, %(person_id)s, %(source)s)
ON CONFLICT (document_id) DO UPDATE
    SET person_id = EXCLUDED.person_id, source = EXCLUDED.source
"""

SELECT_UNKNOWN_SUBJECTS = """
SELECT DISTINCT f.subject, min(f.document_id::text)
  FROM facts f
 WHERE f.subject IS NOT NULL
   AND btrim(f.subject) <> ''
   AND NOT EXISTS (
       SELECT 1 FROM person_aliases a
        WHERE lower(btrim(a.alias)) = lower(btrim(f.subject))
   )
 GROUP BY f.subject
"""


# ------------------------------------------------------------------------------- reading it


def _person(row: tuple[Any, ...]) -> Person:
    return Person(
        id=int(row[0]),
        display_name=row[1],
        relation=row[2],
        is_owner=bool(row[3]),
        external=bool(row[4]),
        aliases=tuple(row[5]) if len(row) > 5 and row[5] else (),
    )


def roster(conn: Any) -> list[Person]:
    """Everyone, owner first, then the household, then the people it has decided are outside."""
    with conn.cursor() as cur:
        cur.execute(SELECT_PEOPLE)
        return [_person(row) for row in cur.fetchall()]


def owner(conn: Any) -> Person | None:
    """The person asking. `None` before setup has run, which every caller must handle: an
    install with no owner is not broken, it is new, and Parrot still answers — it simply
    answers about the household rather than about anybody in particular."""
    with conn.cursor() as cur:
        cur.execute(SELECT_OWNER)
        row = cur.fetchone()
    return _person(row) if row else None


def owner_aliases(conn: Any) -> list[str]:
    """Every confirmed string that means the owner. This is what scopes a first-person question.

    Empty when there is no owner, and empty is meaningful: it says "scope nothing", not "scope
    to nobody". A caller that treats an empty list as an impossible filter turns every question
    into an abstention on a fresh install.
    """
    person = owner(conn)
    return list(person.aliases) if person else []


def resolve(conn: Any, subject: str | None) -> Person | None:
    """The person a printed name means, or `None` if nobody has confirmed what it means."""
    if not subject or not subject.strip():
        return None
    with conn.cursor() as cur:
        cur.execute(RESOLVE_ALIAS, {"alias": subject})
        row = cur.fetchone()
    return _person(row) if row else None


def pending(conn: Any) -> list[PendingAlias]:
    """Names off documents that nobody has placed yet. The 'who is this?' row on Today."""
    with conn.cursor() as cur:
        cur.execute(SELECT_PENDING)
        rows = cur.fetchall()
    return [
        PendingAlias(
            id=int(row[0]),
            alias=row[1],
            person_id=int(row[2]) if row[2] is not None else None,
            person_name=row[3],
            confidence=float(row[4]) if row[4] is not None else None,
            document_id=row[5],
            document_name=row[6],
        )
        for row in rows
    ]


def pending_count(conn: Any) -> int:
    with conn.cursor() as cur:
        cur.execute(COUNT_PENDING)
        row = cur.fetchone()
    return int(row[0]) if row else 0


# ------------------------------------------------------------------------------- writing it


def add_person(
    conn: Any,
    display_name: str,
    relation: Relation = "other",
    *,
    is_owner: bool = False,
    external: bool = False,
    aliases: tuple[str, ...] = (),
) -> Person:
    """Add somebody, with the names they are known by on paper already confirmed.

    Aliases added here are `source='setup'` and confirmed: a person typing a name into a screen
    IS the confirmation, and asking them to confirm what they just typed is the kind of thing
    that makes people stop using software.
    """
    if not display_name.strip():
        raise ValueError("A person needs a name.")
    if relation not in RELATIONS:
        raise ValueError(f"Unknown relation: {relation}")
    with conn.cursor() as cur:
        if is_owner:
            cur.execute(CLEAR_OWNER)
        cur.execute(
            INSERT_PERSON,
            {
                "display_name": display_name.strip(),
                "relation": "self" if is_owner else relation,
                "is_owner": is_owner,
                "external": external,
            },
        )
        row = cur.fetchone()
        person_id = int(row[0])
        for alias in {a.strip() for a in (*aliases, display_name) if a and a.strip()}:
            cur.execute(
                INSERT_ALIAS,
                {
                    "person_id": person_id,
                    "alias": alias,
                    "source": "setup",
                    "confirmed": True,
                    "confidence": None,
                    "document_id": None,
                },
            )
    log.info("household: added %s (%s)", display_name.strip(), relation)
    return Person(person_id, display_name.strip(), relation, is_owner, external, tuple(aliases))


def set_owner(conn: Any, person_id: int) -> Person | None:
    """Hand the household over. The owner is a row, not a value baked in at install.

    Households change hands — a daughter takes over her father's paperwork — and an install
    that cannot follow that is an install that gets abandoned rather than corrected.
    """
    previous = owner(conn)
    with conn.cursor() as cur:
        cur.execute(CLEAR_OWNER)
        cur.execute(SET_OWNER, {"id": person_id})
        if cur.fetchone() is None:
            raise ValueError(f"No person with id {person_id}")
        if previous is not None and previous.id != person_id:
            cur.execute(DEMOTE_PREVIOUS_OWNER, {"id": previous.id})
    log.info("household: owner is now person %s", person_id)
    return owner(conn)


def confirm(conn: Any, alias_id: int, person_id: int) -> None:
    """A person answered the question. From here the alias scopes retrieval."""
    with conn.cursor() as cur:
        cur.execute(CONFIRM_ALIAS, {"id": alias_id, "person_id": person_id})
        if cur.fetchone() is None:
            raise ValueError(f"No pending name with id {alias_id}")


def place(conn: Any, person_id: int, relation: Relation, *, external: bool = False) -> None:
    """Say how somebody is related to the owner, or that they are not part of the household.

    The model proposes a relation when it creates a person off a document, and a person answers
    it. Before this existed the only answer on Today was "someone else here", which recorded
    `other` whatever the truth was: on 13 September "Lim Ah Kow" could not be recorded as the
    owner's father, and the screen said "Lim Ah Kow is Lim Ah Kow".
    """
    if relation not in RELATIONS or relation == "self":
        raise ValueError(f"Not a relation somebody other than the owner can have: {relation}")
    with conn.cursor() as cur:
        cur.execute(SET_PLACE, {"id": person_id, "relation": relation, "external": external})
        if cur.fetchone() is None:
            raise ValueError(f"No household member with id {person_id} other than the owner")


def dismiss(conn: Any, alias_id: int) -> None:
    """Delete a proposal outright, so the same question is asked again next time the name is
    seen. Used when none of the offered answers is right and the person wants to move on."""
    with conn.cursor() as cur:
        cur.execute(DELETE_ALIAS, {"id": alias_id})


def attribute(conn: Any, document_id: Any, person_id: int, source: str = "user") -> None:
    """Say whose a captured document is, before anything has been read off it."""
    with conn.cursor() as cur:
        cur.execute(
            UPSERT_ATTRIBUTION,
            {"document_id": document_id, "person_id": person_id, "source": source},
        )


def link_telegram(conn: Any, chat_id: int, person_id: int) -> None:
    with conn.cursor() as cur:
        cur.execute(UPSERT_TELEGRAM_IDENTITY, {"chat_id": chat_id, "person_id": person_id})


def person_for_chat(conn: Any, chat_id: int) -> int | None:
    """Whose Telegram chat this is.

    The only ownership signal that arrives *before* the document is parsed. A photograph of a
    payslip sent from Rachel's phone is Rachel's payslip whatever the OCR makes of the name at
    the top, and this is how that is known.
    """
    with conn.cursor() as cur:
        cur.execute(SELECT_TELEGRAM_PERSON, {"chat_id": chat_id})
        row = cur.fetchone()
    return int(row[0]) if row else None


# ------------------------------------------------------------------- letting the model guess

CLASSIFY_SYSTEM = (
    "You are given the people in one household and a name printed on a document that has just "
    "been filed there. You decide who that name refers to. Answer 'existing' when it is one of "
    "the people listed, giving their id -- initials, a reversed surname, a missing middle name "
    "and a changed case are all the same person. Answer 'new_member' when it is somebody who "
    "plausibly lives in this household and is not listed. Answer 'outside' when it is a "
    "landlord, an employer, an insurer's officer, a doctor, another driver, or anyone else who "
    "is not a member of the household. You never invent a person who is not in the name you "
    "were given."
)

CLASSIFY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["existing", "new_member", "outside"]},
        "person_id": {"type": "integer"},
        "relation": {"type": "string", "enum": list(RELATIONS)},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    },
    "required": ["verdict", "confidence"],
}


def classify_prompt(subject: str, people: list[Person], document_name: str | None) -> str:
    if people:
        known = "\n".join(
            f"  id={p.id} name={p.display_name!r} relation={p.relation}"
            + (f" also known as {', '.join(p.aliases)}" if p.aliases else "")
            + (" [the owner]" if p.is_owner else "")
            + (" [outside the household]" if p.external else "")
            for p in people
        )
    else:
        known = "  (nobody has been recorded yet)"
    where = f"\nIt was printed on: {document_name}" if document_name else ""
    return f"The household so far:\n{known}\n\nThe name on the document: {subject!r}{where}"


def propose(
    conn: Any,
    client: Any,
    subject: str,
    *,
    document_id: Any | None = None,
    document_name: str | None = None,
) -> PendingAlias | None:
    """Ask the generator who a newly-seen name is, and write the answer down **unconfirmed**.

    Nothing this returns scopes a question. `resolve` and `owner_aliases` read confirmed aliases
    only, so the worst a wrong guess does is put a wrong suggestion on a screen next to the
    document that prompted it, where a person can see both and say no. That is the whole reason
    the model is allowed to guess at all.

    A model that is not running is not an error here. The name is still recorded, still asked
    about, simply without a suggestion attached — Parrot has to keep filing documents on a
    machine where Ollama was never started.
    """
    from core.runtime.ollama import ModelUnavailable

    subject = subject.strip()
    if not subject:
        return None

    people = roster(conn)
    verdict, person_id, relation, confidence = "new_member", None, "other", None
    try:
        reply = client.constrained(
            CLASSIFY_SYSTEM, classify_prompt(subject, people, document_name), CLASSIFY_SCHEMA
        ).json()
        verdict = str(reply.get("verdict", "new_member"))
        confidence = float(reply.get("confidence", 0.0))
        relation = str(reply.get("relation", "other"))
        if relation not in RELATIONS:
            relation = "other"
        proposed = reply.get("person_id")
        person_id = int(proposed) if isinstance(proposed, int) else None
    except (ModelUnavailable, TypeError, ValueError) as error:
        log.info("household: no suggestion for %r (%s)", subject, error)

    known = {p.id for p in people}
    if verdict == "existing" and person_id in known:
        target = person_id
    else:
        # A proposed person who does not exist is created here, unconfirmed against them. The
        # row is cheap and it is what lets the screen offer "yes, that is a new person" as one
        # tap instead of a form. `external` follows the verdict, so an insurer's officer does
        # not arrive in the household list.
        created = add_person(
            conn,
            subject,
            "other" if verdict == "outside" else relation,  # type: ignore[arg-type]
            external=verdict == "outside",
        )
        target = created.id
        # add_person confirms the name it was given, and for a *proposal* that is too strong.
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE person_aliases SET confirmed = false, source = 'model', "
                "confidence = %(confidence)s, document_id = %(document_id)s, decided_at = NULL "
                "WHERE person_id = %(person_id)s",
                {"confidence": confidence, "document_id": document_id, "person_id": target},
            )

    with conn.cursor() as cur:
        cur.execute(
            INSERT_ALIAS,
            {
                "person_id": target,
                "alias": subject,
                "source": "model",
                "confirmed": False,
                "confidence": confidence,
                "document_id": document_id,
            },
        )

    log.info("household: %r proposed as %s (%s)", subject, verdict, confidence)
    return next((row for row in pending(conn) if row.alias.strip() == subject), None)


def sweep_unknown_subjects(conn: Any, client: Any) -> int:
    """Classify every subject in `facts` that no alias covers yet. Returns how many were asked.

    Runs after ingestion rather than inside it: a document that has just been read should not
    also wait on a second model call before it counts as filed, and a name that appears on six
    documents should be asked about once.
    """
    with conn.cursor() as cur:
        cur.execute(SELECT_UNKNOWN_SUBJECTS)
        unknown = cur.fetchall()

    asked = 0
    for subject, document_id in unknown:
        if propose(conn, client, subject, document_id=document_id) is not None:
            asked += 1
    return asked
