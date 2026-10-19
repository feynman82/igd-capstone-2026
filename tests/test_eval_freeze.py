"""Loading a frozen corpus commit for Run 3: the manifest, the household, and the refusals.

No database. The manifest and the register are read from Git, so they are tested against this
repository's own history; loading and verifying need a vault, as `eval.holdout`'s do.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from eval.freeze import (
    Entry,
    FreezeRefused,
    corpus_files,
    differences,
    household,
    manifest,
    manifest_sha,
    register_rows,
    resolve,
    role,
)

ROOT = Path(__file__).resolve().parents[1]


def test_set_c_documents_are_listed_and_held_out() -> None:
    assert role("corpus/batches/batch3/b3-0001.pdf") == "set_c"
    assert role("corpus/batches/batch1/b1-0001.pdf") == "vault"


def test_the_manifest_is_read_from_the_commit_and_matches_its_bytes() -> None:
    commit = resolve("HEAD")
    entries = corpus_files(commit)
    by_path = {entry.path: entry for entry in entries}
    car = by_path["corpus/batches/batch1/b1-0001.pdf"]
    on_disk = ROOT / car.path
    assert car.sha256 == hashlib.sha256(on_disk.read_bytes()).hexdigest()
    assert car.size == on_disk.stat().st_size
    assert {e.role for e in entries if e.path.startswith("corpus/batches/batch3/")} == {"set_c"}
    assert not any(e.path.startswith("inbox/") for e in entries), "never the watched folder"


def test_a_short_ref_is_recorded_as_the_full_commit() -> None:
    full = resolve("HEAD")
    assert len(full) == 40 and resolve(full[:10]) == full


def test_the_manifest_hash_does_not_depend_on_listing_order() -> None:
    a, b = Entry("x/a.pdf", "1" * 64, 3, "vault"), Entry("x/b.pdf", "2" * 64, 4, "vault")
    assert manifest_sha([a, b]) == manifest_sha([b, a])
    assert manifest_sha([a]) != manifest_sha([a, b])


def test_every_difference_from_a_published_manifest_is_named() -> None:
    a, b = Entry("x/a.pdf", "1" * 64, 3, "vault"), Entry("x/b.pdf", "2" * 64, 4, "vault")
    published = manifest("c" * 40, [a, b])
    assert differences(published, [a, b]) == []
    changed = Entry("x/b.pdf", "3" * 64, 4, "vault")
    extra = Entry("x/c.pdf", "4" * 64, 5, "vault")
    assert differences(published, [changed, extra]) == [
        "missing at this commit: x/a.pdf",
        "not in the published manifest: x/c.pdf",
        "changed: x/b.pdf",
    ]


def test_the_register_is_read_as_committed() -> None:
    rows = register_rows(resolve("HEAD"))
    assert any(row.get("doc_id") == "b1-0001" for row in rows)


def _declaration(tmp_path: Path, people: list[dict[str, object]]) -> Path:
    path = tmp_path / "household.json"
    path.write_text(json.dumps({"people": people}), encoding="utf-8")
    return path


def test_the_draft_household_loads() -> None:
    people = household(ROOT / "eval" / "run3" / "household.draft.json")
    assert [p.name for p in people if p.owner] == ["Marcus Lim Jun Wei"]


@pytest.mark.parametrize(
    ("people", "why"),
    [
        ([{"name": "A", "relation": "other"}], "exactly one owner"),
        (
            [
                {"name": "A", "relation": "self", "owner": True},
                {"name": "B", "relation": "self", "owner": True},
            ],
            "exactly one owner",
        ),
        (
            [{"name": "A", "relation": "self", "owner": True}, {"name": "B", "relation": "cousin"}],
            "unknown relation",
        ),
        ([{"name": "A", "relation": "parent", "owner": True}], "only the owner is 'self'"),
        (
            [
                {"name": "Marcus Lim", "relation": "self", "owner": True},
                {"name": "Marcus Lim", "relation": "other"},
            ],
            "one person only",
        ),
    ],
)
def test_a_household_that_cannot_be_true_is_refused(
    tmp_path: Path, people: list[dict[str, object]], why: str
) -> None:
    """The development vault's own household fails the last case: 'Marcus Lim Jun Wei' is both
    the owner's alias and a second person."""
    with pytest.raises(FreezeRefused, match=why):
        household(_declaration(tmp_path, people))
