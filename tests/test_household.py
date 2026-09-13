"""Who is asking, and whose documents may answer.

Two halves, deliberately split. `is_first_person` and the scoping arithmetic are pure and are
tested against no database at all, because they are where the judgement lives and they must be
cheap to re-run. The roster and the alias index are tested against Postgres, inside a
transaction that is rolled back, because a unique index is not a thing a fake can have an
opinion about — the same reasoning as `test_registration.py`.

The case this whole module exists for: with two term life policies filed, one on Marcus and one
on Rachel, "what is my term life premium?" must not answer from Rachel's. It is the only wrong
answer in this system that arrives with a correct citation, so it is the only one the grounding
gate cannot catch. See ADR 0011.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from core import household
from core.graph.ports import Passage
from core.graph.scope import Scoped, is_first_person, scope_passages
from core.runtime.settings import Settings

ROOT = Path(__file__).resolve().parents[1]


# ------------------------------------------------------------------- whose question is this


@pytest.mark.parametrize(
    "question",
    [
        "what is my term life premium?",
        "When is my road tax due",
        "Do I have hospital cover",
        "how much did I donate last year?",
        "show me my policy number",
    ],
)
def test_first_person_questions_are_recognised(question: str) -> None:
    assert is_first_person(question)


@pytest.mark.parametrize(
    "question",
    [
        # No first person at all: about the household, or about a named person.
        "when does the car insurance renew?",
        "what is the hospital policy premium",
        # First person, but about somebody else. These are the ones that matter: they open
        # exactly like a question about yourself and are not one.
        "what is my wife's term life premium?",
        "is my dad's hospital cover still active",
        "when does my son's policy renew",
        "what do we pay for home contents",
        "how much does our household spend on premiums",
    ],
)
def test_questions_about_other_people_are_not_scoped(question: str) -> None:
    assert not is_first_person(question)


def test_a_named_household_member_wins_over_the_pronoun() -> None:
    """ "What is Rachel's premium on my policy" is a question about Rachel.

    A relationship word is not the only way to mean somebody else, and a filter that scoped
    this to the owner would drop the only document that answers it.
    """
    others = ("Rachel Ng Hui Shan", "Lucas Lim Kai En")
    assert not is_first_person("what is Rachel Ng Hui Shan's premium", others)
    assert is_first_person("what is my premium", others)


# ------------------------------------------------------------------------ scoping passages


def _passage(chunk_id: int, document_id: str) -> Passage:
    return Passage(
        chunk_id=chunk_id,
        document_id=document_id,
        page=1,
        text="term life premium 1,240.00",
        score=0.9,
        document_name=f"policy-{document_id}.pdf",
    )


def _conn_returning(rows: list[tuple[Any, ...]]) -> Any:
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = rows
    return conn


def test_another_persons_documents_are_set_aside() -> None:
    mine, theirs = _passage(1, "doc-mine"), _passage(2, "doc-theirs")
    conn = _conn_returning([("doc-mine", 1, "Marcus"), ("doc-theirs", 2, "Rachel")])

    scoped = scope_passages(conn, [mine, theirs], owner_id=1, owner_name="Marcus")

    assert scoped.passages == [mine]
    assert scoped.dropped_people == ("Rachel",)
    assert scoped.scoped


def test_a_document_with_no_subject_belongs_to_everybody() -> None:
    """The third bucket. Home contents, a utility bill — nobody's name on it, everybody's.

    Leaving this out is how "my home insurance" breaks, and it breaks quietly: the filter
    returns nothing and the screen says the vault cannot answer, which is a lie.
    """
    household_doc = _passage(3, "doc-household")
    conn = _conn_returning([])  # no fact on it resolves to anyone

    scoped = scope_passages(conn, [household_doc], owner_id=1, owner_name="Marcus")

    assert scoped.passages == [household_doc]
    assert scoped.dropped_people == ()


def test_a_document_naming_the_owner_and_somebody_else_is_kept() -> None:
    """A joint policy is the owner's too. Presence wins over exclusion."""
    joint = _passage(4, "doc-joint")
    conn = _conn_returning([("doc-joint", 1, "Marcus"), ("doc-joint", 2, "Rachel")])

    scoped = scope_passages(conn, [joint], owner_id=1, owner_name="Marcus")

    assert scoped.passages == [joint]


def test_nothing_of_mine_is_the_interesting_abstention() -> None:
    """Asked about my policy; the vault holds Rachel's. Say so, rather than answer hers."""
    theirs = _passage(5, "doc-theirs")
    conn = _conn_returning([("doc-theirs", 2, "Rachel Ng Hui Shan")])

    scoped = scope_passages(conn, [theirs], owner_id=1, owner_name="Marcus Lim")

    assert scoped.passages == []
    assert scoped.empty_for_owner
    assert scoped.dropped_people == ("Rachel Ng Hui Shan",)


def test_an_unscoped_result_is_not_empty_for_the_owner() -> None:
    """`empty_for_owner` must never fire on a question that was never scoped — otherwise a
    household with no owner set would abstain on everything."""
    assert not Scoped([], None).empty_for_owner


# --------------------------------------------------------------------- the roster, for real


@pytest.fixture
def conn() -> Iterator[Any]:
    psycopg = pytest.importorskip("psycopg")
    try:
        connection = psycopg.connect(
            Settings.load(ROOT).database_url, autocommit=False, connect_timeout=3
        )
    except psycopg.OperationalError as error:
        pytest.skip(f"no local database: {type(error).__name__}")
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT to_regclass('public.people')")
            row = cur.fetchone()
        if row is None or row[0] is None:
            pytest.skip("the 0002_household migration has not been applied")
        yield connection
    finally:
        connection.rollback()  # nothing this test did survives
        connection.close()


def test_the_owner_is_found_by_any_of_their_names(conn: Any) -> None:
    household.add_person(
        conn,
        "Testowner Quah",
        "self",
        is_owner=True,
        aliases=("TESTOWNER QUAH ZI", "Quah Zi, Testowner"),
    )
    owner = household.owner(conn)
    assert owner is not None
    assert set(owner.aliases) >= {"TESTOWNER QUAH ZI", "Quah Zi, Testowner", "Testowner Quah"}
    # The comparison the resolver does: case and surrounding space are not a different person.
    assert household.resolve(conn, "  testowner quah zi ") is not None


def test_an_unconfirmed_alias_resolves_to_nobody(conn: Any) -> None:
    """The sentence that makes a wrong model guess cost a tap instead of a wrong answer."""
    person = household.add_person(conn, "Rachel Ng", "partner")
    with conn.cursor() as cur:
        cur.execute(
            household.INSERT_ALIAS,
            {
                "person_id": person.id,
                "alias": "R. NG HUI SHAN",
                "source": "model",
                "confirmed": False,
                "confidence": 0.91,
                "document_id": None,
            },
        )
    assert household.resolve(conn, "R. NG HUI SHAN") is None
    assert household.pending_count(conn) == 1

    pending = household.pending(conn)
    household.confirm(conn, pending[0].id, person.id)
    resolved = household.resolve(conn, "R. NG HUI SHAN")
    assert resolved is not None and resolved.id == person.id


def test_one_name_cannot_belong_to_two_people(conn: Any) -> None:
    """A second document must never silently move a name from one member to another."""
    first = household.add_person(conn, "Testowner Quah", "self", is_owner=True)
    household.add_person(conn, "Testowner Quah", "other")  # same printed name, different row
    resolved = household.resolve(conn, "Testowner Quah")
    assert resolved is not None and resolved.id == first.id


def test_the_owner_can_be_handed_over(conn: Any) -> None:
    """A daughter takes over her father's paperwork. The install follows."""
    father = household.add_person(conn, "Lim Ah Kow", "self", is_owner=True)
    daughter = household.add_person(conn, "Lim Mei Ling", "child")

    household.set_owner(conn, daughter.id)

    owner = household.owner(conn)
    assert owner is not None and owner.id == daughter.id
    # Exactly one owner, held by the unique index rather than by hope.
    assert [p.id for p in household.roster(conn) if p.is_owner] == [daughter.id]
    # The previous owner needs a relation and Parrot does not know which. `other`, not a guess.
    previous = next(p for p in household.roster(conn) if p.id == father.id)
    assert previous.relation == "other"


def test_a_member_can_be_placed_but_the_owner_cannot(conn: Any) -> None:
    owner = household.add_person(conn, "Testowner Quah", "self", is_owner=True)
    father = household.add_person(conn, "Testparent Quah", "other")

    household.place(conn, father.id, "parent")
    placed = next(p for p in household.roster(conn) if p.id == father.id)
    assert placed.relation == "parent" and not placed.external

    with pytest.raises(ValueError):
        household.place(conn, owner.id, "parent")
    with pytest.raises(ValueError):
        household.place(conn, father.id, "self")


@pytest.mark.parametrize(
    "question,expected",
    [
        ("how much is my son's life insurance?", ("son", "child")),
        ("is my dad's hospital cover still active", ("dad", "parent")),
        ("when does my wife\u2019s policy renew", ("wife", "partner")),
        ("what are my parents' premiums", ("parents", "parent")),
        # Not possessive: the owner's own policy may be what answers it.
        ("does my policy cover my son?", None),
        # Somebody who works for the household: no relation matches, so Parrot says so.
        ("does my policy pay for my maid's hospital bills?", ("maid", "outside")),
        ("what is my premium?", None),
    ],
)
def test_a_possessive_relation_names_whose_documents_are_asked_about(
    question: str, expected: tuple[str, str] | None
) -> None:
    from core.graph.scope import relation_asked

    assert relation_asked(question) == expected


def test_my_dads_question_is_scoped_to_the_parent_and_an_unknown_relation_says_so(
    conn: Any,
) -> None:
    from core.graph.scope import HouseholdScope

    household.add_person(conn, "Testowner Quah", "self", is_owner=True)
    household.add_person(conn, "Testparent Quah", "parent")
    passages = [_passage(1, "00000000-0000-0000-0000-00000000abcd")]

    dads = HouseholdScope(conn).apply("is my dad's hospital plan still active?", passages)
    assert dads.scoped and "Testparent Quah" in (dads.person_name or "")
    assert dads.passages == passages, "a document with no subject is the household's"

    with conn.cursor() as cur:
        cur.execute("UPDATE people SET relation = 'other' WHERE relation = 'child'")
    sons = HouseholdScope(conn).apply("how much is my son's life insurance?", passages)
    assert sons.unknown_relation == "son"
    assert not sons.scoped


def test_handing_over_to_nobody_is_an_error(conn: Any) -> None:
    household.add_person(conn, "Marcus Lim", "self", is_owner=True)
    with pytest.raises(ValueError):
        household.set_owner(conn, 999_999)


def test_a_household_with_no_owner_scopes_nothing(conn: Any) -> None:
    """A fresh install is not broken. It answers about the household, as it always did.

    The owner is cleared inside this transaction rather than assumed absent, so the test says
    what it means on a developer's machine that already has a real household in it — and the
    rollback puts it back.
    """
    from core.graph.scope import HouseholdScope

    with conn.cursor() as cur:
        cur.execute(household.CLEAR_OWNER)
    assert household.owner(conn) is None

    scoped = HouseholdScope(conn).apply("what is my premium", [_passage(1, "doc")])
    assert not scoped.scoped
    assert len(scoped.passages) == 1
