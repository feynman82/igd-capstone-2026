"""The holdout is scored in a vault of its own. These are the guards that keep it that way.

No database here: what is worth testing is the refusals, which happen before anything is
created, and the URL arithmetic that decides *which* database is opened. The ingestion and the
scoring are the same functions the synthetic path already uses and are tested there.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from eval.holdout import (
    ROOT,
    HoldoutRefused,
    check_outside_the_repository,
    documents_in,
    main,
    migrations,
    synthetic_baseline,
    vault_url,
)


def test_a_holdout_inside_the_repository_is_refused(tmp_path: Path) -> None:
    """The failure this exists to prevent, and it cannot be undone: `inbox/` is the watched
    folder, `make corpus-load` copies into it, and a document the development vault has read is
    no longer a holdout."""
    with pytest.raises(HoldoutRefused, match="inside the repository"):
        check_outside_the_repository(ROOT / "inbox")
    with pytest.raises(HoldoutRefused, match="inside the repository"):
        check_outside_the_repository(ROOT / "corpus" / "batches" / "batch1")
    with pytest.raises(HoldoutRefused, match="inside the repository"):
        check_outside_the_repository(ROOT / "corpus" / "holdout")
    # Somewhere the watcher cannot see is fine.
    check_outside_the_repository(tmp_path)


def test_the_vault_is_a_different_database_on_the_same_server() -> None:
    """Isolation is a separate database, not a flag: the holdout's chunks must not share an
    index with the corpus every retrieval change is measured against."""
    dev = "postgresql://parrot:parrot@127.0.0.1:5432/parrot"
    assert (
        vault_url(dev, "parrot_holdout")
        == "postgresql://parrot:parrot@127.0.0.1:5432/parrot_holdout"
    )
    assert vault_url(dev, "postgres") == "postgresql://parrot:parrot@127.0.0.1:5432/postgres"
    # Host, port and credentials are carried over untouched; only the database changes.
    assert vault_url("postgresql://u:p@127.0.0.1:6000/parrot", "x").endswith("@127.0.0.1:6000/x")


def test_only_documents_are_picked_up(tmp_path: Path) -> None:
    (tmp_path / "a.pdf").write_bytes(b"%PDF")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "b.JPG").write_bytes(b"\xff\xd8")
    (tmp_path / "register.csv").write_text("doc_id\n", encoding="utf-8")  # not a document
    (tmp_path / ".DS_Store").write_bytes(b"")
    assert [p.name for p in documents_in(tmp_path)] == ["a.pdf", "b.JPG"]


def test_an_empty_or_missing_folder_is_refused(tmp_path: Path) -> None:
    with pytest.raises(HoldoutRefused, match="not a folder"):
        documents_in(tmp_path / "nope")
    (tmp_path / "empty").mkdir()
    with pytest.raises(HoldoutRefused, match="No documents"):
        documents_in(tmp_path / "empty")


def test_the_schema_is_read_from_the_committed_migrations() -> None:
    """Applied, never modified — `db/migrations/` is its own reviewed PR (AGENTS.md rule 4)."""
    names = [p.name for p in migrations()]
    assert names == sorted(names) and names[0].startswith("0001")
    assert all(p.suffix == ".sql" for p in migrations())


def test_the_gap_is_computed_from_the_newest_committed_synthetic_run(tmp_path: Path) -> None:
    """The number that matters is the gap, so the synthetic side is read from the results rather
    than typed into a slide."""
    (tmp_path / "old.json").write_text(
        json.dumps(
            {"run": {"date": "2026-09-29T00:00:00+00:00"}, "metrics": {"extraction_f1": 0.898}}
        ),
        encoding="utf-8",
    )
    (tmp_path / "new.json").write_text(
        json.dumps(
            {"run": {"date": "2026-10-14T00:00:00+00:00"}, "metrics": {"extraction_f1": 0.9028}}
        ),
        encoding="utf-8",
    )
    (tmp_path / "note.md").write_text("not a result", encoding="utf-8")
    assert synthetic_baseline(tmp_path) == 0.9028
    assert synthetic_baseline(tmp_path / "nothing-here") is None


def test_a_dry_run_creates_nothing(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "a.pdf").write_bytes(b"%PDF")
    register = tmp_path / "register.csv"
    register.write_text("doc_id,doc_type\n", encoding="utf-8")
    assert main(["--documents", str(tmp_path), "--register", str(register), "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "nothing created" in out and "development vault is not opened" in out


def test_a_holdout_in_the_repository_fails_before_anything_is_opened(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = main(["--documents", str(ROOT / "inbox"), "--register", str(ROOT / "README.md")])
    assert code == 2
    assert "inside the repository" in capsys.readouterr().out
