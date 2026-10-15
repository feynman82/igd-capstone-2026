"""Set C in its own vault: the two guards that keep the planted documents where they belong.

No database. The guards decide from what the vault holds, which is a set of ids, so they can be
tested on sets of ids. Cloning and ingesting are the holdout's machinery, tested there.
"""

from __future__ import annotations

from pathlib import Path

from eval.run import _fixture_guards
from eval.score import has_ground_truth
from eval.setc import FIXTURE_REGISTER, NEEDS_FIXTURES, fixture_ids
from eval.sets_io import Expected, Question, read_register

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = fixture_ids(ROOT)


def _q(id: str, set_id: str, category: str = "") -> Question:
    if set_id == "A":
        return Question(id, "A", "retrieval", "q", Expected("fact", "core", "k", "v"), "b1-0001", 1)
    return Question(id, set_id, "governance", "q", Expected("abstain"), category=category)


def test_the_fixtures_are_read_from_their_register_and_carry_no_ground_truth() -> None:
    """What makes a row a fixture rather than ground truth: it records nothing to score. Read from
    the register so a renamed or extended batch is picked up rather than hard-coded."""
    assert {"b3-0001", "b3-0002", "b3-0003"} == FIXTURES
    rows = read_register(ROOT / FIXTURE_REGISTER)
    assert rows and not any(has_ground_truth(row) for row in rows)


def test_an_injection_item_is_skipped_when_the_fixtures_are_absent() -> None:
    """5 October's failure: scored without its planted document, an injection item passes
    against nothing and the 3/3 means nothing."""
    run = [_q("c-c04", "C", "injection"), _q("c-c01", "C", "act")]
    kept, untestable, contaminating = _fixture_guards(run, {"b1-0001"})
    assert untestable == ["c-c04"]
    assert [q.id for q in kept] == ["c-c01"]  # an act item needs no fixture and still runs
    assert contaminating == []


def test_an_injection_item_runs_when_the_fixtures_are_present() -> None:
    run = [_q("c-c04", "C", "injection")]
    kept, untestable, _ = _fixture_guards(run, {"b1-0001", *FIXTURES})
    assert untestable == [] and [q.id for q in kept] == ["c-c04"]


def test_a_partial_fixture_set_still_skips_the_injection_items() -> None:
    """Two of three planted documents is not the test the set describes."""
    run = [_q("c-c05", "C", "injection")]
    _, untestable, _ = _fixture_guards(run, {"b3-0001", "b3-0002"})
    assert untestable == ["c-c05"]


def test_fixtures_in_a_vault_scoring_set_a_are_flagged() -> None:
    """14 October's failure: the planted notice prints the real car policy's number, ties the
    real schedule on the identifier boost, and wins. Every Set A number in that vault is partly
    measuring the fixtures."""
    _, _, contaminating = _fixture_guards([_q("a-1", "A")], {"b1-0001", "b3-0001"})
    assert contaminating == ["b3-0001"]


def test_fixtures_are_not_flagged_when_only_set_c_is_scored() -> None:
    """That is where they belong."""
    run = [_q("c-c04", "C", "injection")]
    _, _, contaminating = _fixture_guards(run, {"b1-0001", *FIXTURES})
    assert contaminating == []


def test_only_injection_needs_the_fixtures() -> None:
    assert {"injection"} == NEEDS_FIXTURES
