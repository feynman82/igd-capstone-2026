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
from core.graph.scope import Scoped, is_first_person, scope_to
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
    cursor.fetchone.return_value = None  # no date of birth on file (`scope.AGE_BASIS`)
    return conn


def test_another_persons_documents_are_set_aside() -> None:
    mine, theirs = _passage(1, "doc-mine"), _passage(2, "doc-theirs")
    conn = _conn_returning([("doc-mine", 1, "Marcus"), ("doc-theirs", 2, "Rachel")])

    scoped = scope_to(conn, [mine, theirs], person_ids=frozenset({1}), name="Marcus")

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

    scoped = scope_to(conn, [household_doc], person_ids=frozenset({1}), name="Marcus")

    assert scoped.passages == [household_doc]
    assert scoped.dropped_people == ()


def test_a_document_naming_the_owner_and_somebody_else_is_kept() -> None:
    """A joint policy is the owner's too. Presence wins over exclusion."""
    joint = _passage(4, "doc-joint")
    conn = _conn_returning([("doc-joint", 1, "Marcus"), ("doc-joint", 2, "Rachel")])

    scoped = scope_to(conn, [joint], person_ids=frozenset({1}), name="Marcus")

    assert scoped.passages == [joint]


def test_nothing_of_mine_is_the_interesting_abstention() -> None:
    """Asked about my policy; the vault holds Rachel's. Say so, rather than answer hers."""
    theirs = _passage(5, "doc-theirs")
    conn = _conn_returning([("doc-theirs", 2, "Rachel Ng Hui Shan")])

    scoped = scope_to(conn, [theirs], person_ids=frozenset({1}), name="Marcus Lim")

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
    # A count, not a total. The transaction rolls back what this test writes, but it cannot roll
    # back what was already committed: a vault with documents ingested in it has unconfirmed
    # aliases of its own, and this assertion used to fail the moment anybody ran the real thing.
    before = household.pending_count(conn)
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
    assert household.pending_count(conn) == before + 1

    pending = [item for item in household.pending(conn) if item.alias == "R. NG HUI SHAN"]
    assert len(pending) == 1
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
        # A relation the roster cannot hold. 13 September: left unscoped, answered from the
        # father's policy.
        ("is my grandpa's hospital plan active?", ("grandpa", "grandparent")),
        (
            "when does my grandmother\N{RIGHT SINGLE QUOTATION MARK}s policy renew",
            ("grandmother", "grandparent"),
        ),
        ("is my ah ma's hospital plan active?", ("ah ma", "grandparent")),
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


# ------------------------------------------------- who the question names, against a fake roster

OWNER_DOC, RACHEL_DOC, FATHER_DOC = "doc-marcus", "doc-rachel", "doc-father"

MARCUS = household.Person(1, "Marcus Lim Jun Wei", "self", True, False, ("MARCUS LIM JUN WEI",))
RACHEL = household.Person(2, "Rachel Ng Hui Shan", "partner", False, False, ("Rachel Ng Hui Shan",))
FATHER = household.Person(3, "Lim Ah Kow", "parent", False, False, ("LIM AH KOW",))


def _household_scope(monkeypatch: pytest.MonkeyPatch, *people: household.Person) -> Any:
    """`HouseholdScope` over a roster held in memory, with every document resolved by name."""
    from core.graph.scope import HouseholdScope

    monkeypatch.setattr(household, "roster", lambda conn: list(people))
    monkeypatch.setattr(
        household, "owner", lambda conn: next((p for p in people if p.is_owner), None)
    )
    ids = {1: OWNER_DOC, 2: RACHEL_DOC, 3: FATHER_DOC}
    conn = _conn_returning([(ids[p.id], p.id, p.display_name) for p in people if p.id in ids])
    return HouseholdScope(conn)


EVERYONES = [_passage(1, OWNER_DOC), _passage(2, RACHEL_DOC), _passage(3, FATHER_DOC)]


def test_a_grandparent_nobody_holds_is_an_unknown_relation_not_the_fathers_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    scoped = scope.apply("is my grandpa's hospital plan active?", EVERYONES)

    assert scoped.unknown_relation == "grandpa"
    assert not scoped.scoped


def test_a_grandparent_recorded_under_that_name_is_who_the_question_means(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The roster has no grandparent relation, so the household says it the only way it can: a
    person recorded as `other` whose display name or confirmed alias is the word itself."""
    grandpa = household.Person(3, "Grandpa", "other", False, False, ("TAN AH BENG", "Grandpa"))
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, grandpa)

    scoped = scope.apply("is my grandpa's hospital plan active?", EVERYONES)

    assert scoped.person_name == "Grandpa"
    assert scoped.about == "grandpa"
    assert [p.document_id for p in scoped.passages] == [FATHER_DOC]


def test_the_owner_asking_about_themselves_by_name_is_scoped_to_the_owner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """13 September: "what is Marcus's premium?" has no "my", so nothing was scoped and Rachel's
    and Lim Ah Kow's policies mixed in."""
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    scoped = scope.apply("what is Marcus's premium?", EVERYONES)

    assert scoped.person_name == "Marcus Lim Jun Wei"
    assert not scoped.someone_else
    assert [p.document_id for p in scoped.passages] == [OWNER_DOC]
    assert scoped.dropped_people == ("Lim Ah Kow", "Rachel Ng Hui Shan")


def test_a_question_naming_one_other_member_is_scoped_to_them(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    for question in ("when does Rachel's policy renew?", "does rachel ng hui shan have cover"):
        scoped = scope.apply(question, EVERYONES)
        assert scoped.person_name == "Rachel Ng Hui Shan", question
        assert scoped.someone_else, "the answer must not be told Rachel is the one asking"
        assert [p.document_id for p in scoped.passages] == [RACHEL_DOC]


@pytest.mark.parametrize(
    "question",
    [
        # About two people: a filter would drop one of the documents that answers it.
        "is my premium higher than Rachel's?",
        "compare Marcus's and Rachel's premiums",
        # "Lim" is Marcus's and his father's. A shared word names nobody.
        "what is Lim's premium?",
        # A given name that is not possessive is not enough to be sure it is a name at all.
        "what is the premium for rachel",
    ],
)
def test_a_name_that_is_not_exactly_one_person_scopes_nothing(
    monkeypatch: pytest.MonkeyPatch, question: str
) -> None:
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    scoped = scope.apply(question, EVERYONES)

    assert not scoped.scoped
    assert scoped.passages == EVERYONES


def test_a_person_nobody_has_confirmed_is_not_named(monkeypatch: pytest.MonkeyPatch) -> None:
    """A model proposal is a question on Today, not a member yet — the same rule relations obey."""
    unconfirmed = household.Person(2, "Rachel Ng Hui Shan", "partner", False, False, ())
    scope = _household_scope(monkeypatch, MARCUS, unconfirmed, FATHER)

    scoped = scope.apply("when does Rachel's policy renew?", EVERYONES)

    assert not scoped.scoped


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


# --------------------------------------------------------------- whose a piece of advice is about


def test_whose_gives_the_owner_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Nothing named, nothing ruled out: the question is the owner's, same as `apply` would
    have scoped it."""
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    subject = scope.whose("is my critical illness cover enough?")

    assert subject.person_ids == frozenset({MARCUS.id})
    assert subject.name == "Marcus Lim Jun Wei"
    assert subject.about is None
    assert subject.unknown_relation is None
    assert not subject.no_owner


def test_whose_gives_the_relation_it_resolves_to(monkeypatch: pytest.MonkeyPatch) -> None:
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    subject = scope.whose("is my dad's hospital cover enough?")

    assert subject.person_ids == frozenset({FATHER.id})
    assert subject.name == "Lim Ah Kow"
    assert subject.about == "dad"


def test_whose_gives_a_person_named_outright(monkeypatch: pytest.MonkeyPatch) -> None:
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    subject = scope.whose("is Rachel's cover enough?")

    assert subject.person_ids == frozenset({RACHEL.id})
    assert subject.name == "Rachel Ng Hui Shan"
    assert subject.about is None
    assert subject.someone_else is True
    assert subject.unknown_relation is None
    assert not subject.no_owner


def test_whose_reports_an_unknown_relation_rather_than_guessing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No child is recorded, so "son" cannot resolve to anybody -- reported, not defaulted to
    the owner, the same abstention `apply` makes."""
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    subject = scope.whose("my son's critical illness plan, is it enough?")

    assert subject.unknown_relation == "son"
    assert subject.person_ids == frozenset()
    assert not subject.no_owner


def test_whose_says_no_owner_when_nobody_has_claimed_the_household(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from core.graph.scope import HouseholdScope

    monkeypatch.setattr(household, "owner", lambda conn: None)
    scope = HouseholdScope(MagicMock())

    subject = scope.whose("is my critical illness cover enough?")

    assert subject.no_owner
    assert subject.person_ids == frozenset()
    assert subject.name == ""


def test_whose_refuses_to_guess_between_two_people_named_at_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """ "Compare Rachel's and Marcus's plans" names two people. `apply` can safely answer from
    everything -- a wrong inclusion is still correctly cited -- but advice is written about one
    person, so `whose` reports the ambiguity rather than picking one of them."""
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    subject = scope.whose("compare Rachel's and Marcus's plans")

    assert subject.ambiguous is True
    assert subject.person_ids == frozenset()
    assert subject.name == ""


def test_whose_refuses_to_guess_when_a_someone_else_word_is_used(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """ "My wife" has no possessive "'s", so `relation_asked` does not match it -- it is not
    "my wife's cover", which the relation branch would resolve to Rachel outright. Without the
    possessive there is only the someone-else word "wife", and that is real ambiguity for advice
    even though `apply` would happily answer this from the whole vault."""
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    subject = scope.whose("how much cover does my wife need?")

    assert subject.ambiguous is True
    assert subject.person_ids == frozenset()


def test_whose_refuses_to_guess_between_two_confirmed_parents(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Two confirmed members hold `parent` -- a father and a mother. `apply` keeps scoping to
    both of them (Fix I2's `apply` requirement, unchanged); `whose` cannot honestly write advice
    about one of two fathers, so it reports the ambiguity instead, with nobody in `person_ids`."""
    mother = household.Person(4, "Lim Guek Hua", "parent", False, False, ("LIM GUEK HUA",))
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER, mother)

    subject = scope.whose("is my dad's hospital cover enough?")

    assert subject.ambiguous is True
    assert subject.person_ids == frozenset()


def test_whose_gives_the_owner_when_the_owner_names_themselves(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The owner naming themselves is unambiguous, unlike anybody else being named -- and it is
    not `someone_else` either, since the owner is exactly who advice about them should address."""
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    subject = scope.whose("is Marcus's cover enough?")

    assert subject.person_ids == frozenset({MARCUS.id})
    assert subject.name == "Marcus Lim Jun Wei"
    assert not subject.someone_else
    assert not subject.ambiguous


def test_whose_gives_the_owner_when_nobody_and_no_relation_is_named(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No first-person word, no relation word, no someone-else word, nobody named: there is
    nothing here to be unsure about, so `whose` makes the same guess of last resort it makes for
    an unambiguous first-person question, rather than reporting it as ambiguous."""
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    subject = scope.whose("is the hospital cover enough?")

    assert subject.person_ids == frozenset({MARCUS.id})
    assert subject.name == "Marcus Lim Jun Wei"
    assert not subject.ambiguous
    assert not subject.no_owner


def test_whose_asks_whose_when_a_member_is_named_without_a_possessive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """ "Does Rachel have enough critical illness cover?" and "is critical illness cover enough
    for Rachel?" both name Rachel, but `named_in` only matches a whole name/alias or a possessive
    single word ("Rachel's") -- neither is true here, so `_decide` falls through to
    `"impersonal"` and would otherwise hand the question to the owner: advice would sum Marcus's
    facts against Rachel's question. `whose` catches this the way `named_in`'s possessive rule
    would if the question had put an apostrophe on it -- the same word, without requiring one."""
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    for question in (
        "does Rachel have enough critical illness cover?",
        "is critical illness cover enough for Rachel?",
    ):
        subject = scope.whose(question)
        assert subject.ambiguous is True, question
        assert subject.person_ids == frozenset(), question
        assert subject.name == "", question


def test_whose_still_gives_the_owner_when_no_word_names_a_member(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A common word that happens not to be any confirmed member's own name word must not trip
    the bare-word check `whose` now makes -- this stays the same "nothing to be unsure about"
    fall-through the owner-by-default test above covers."""
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    subject = scope.whose("is the reasonable cover enough?")

    assert subject.person_ids == frozenset({MARCUS.id})
    assert subject.name == "Marcus Lim Jun Wei"
    assert not subject.ambiguous


def test_whose_gives_the_owner_their_own_first_name_without_a_possessive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The owner's own first name, unpossessive, is not somebody else's name in the question --
    it is the owner, same as "my", and the new bare-word check must not flip that to ambiguous."""
    scope = _household_scope(monkeypatch, MARCUS, RACHEL, FATHER)

    subject = scope.whose("Is Marcus covered enough?")

    assert subject.person_ids == frozenset({MARCUS.id})
    assert subject.name == "Marcus Lim Jun Wei"
    assert not subject.ambiguous
