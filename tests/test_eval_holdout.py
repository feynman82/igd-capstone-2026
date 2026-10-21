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
    BASELINE,
    ROOT,
    HoldoutRefused,
    check_outside_the_repository,
    documents_in,
    gaps_by_type,
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


def test_the_gap_is_computed_from_one_named_synthetic_run(tmp_path: Path) -> None:
    """The number that matters is the gap, so the synthetic side is read from a result file
    rather than typed into a slide, and the file is named rather than found: on 21 October
    "the newest result" was a reranker experiment from that morning."""
    run = tmp_path / "run.json"
    run.write_text(
        json.dumps(
            {
                "run": {"git_sha": "d45f12d"},
                "metrics": {"extraction_f1": 0.9487},
                "also": {"extraction_by_doc_type": {"payslip": {"f1": 1.0, "tp": 6}}},
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "newer.json").write_text(
        json.dumps({"run": {"date": "2099-01-01"}, "metrics": {"extraction_f1": 0.5}}),
        encoding="utf-8",
    )
    assert synthetic_baseline(run) == {
        "file": "run.json",
        "git_sha": "d45f12d",
        "extraction_f1": 0.9487,
        "by_doc_type": {"payslip": 1.0},
    }
    assert synthetic_baseline(tmp_path / "nothing-here.json") is None


def test_the_default_baseline_is_run_3() -> None:
    baseline = synthetic_baseline(BASELINE)
    assert baseline is not None and baseline["file"] == "2026-10-19-run3.json"
    assert baseline["extraction_f1"] == 0.9487
    assert "policy_schedule" in baseline["by_doc_type"]


def test_the_gap_is_also_read_type_against_type() -> None:
    """Six synthetic stand-ins showed a "gap" of 0.03 overall from their mix of types alone."""
    holdout = {
        "payslip": {"documents": 3, "f1": 0.8},
        "passport": {"documents": 1, "f1": 1.0},
    }
    gaps = gaps_by_type(holdout, {"payslip": 1.0})
    assert gaps["payslip"] == {"documents": 3, "holdout_f1": 0.8, "synthetic_f1": 1.0, "gap": 0.2}
    assert gaps["passport"]["gap"] is None, "no synthetic score for the type: no gap, not zero"


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
