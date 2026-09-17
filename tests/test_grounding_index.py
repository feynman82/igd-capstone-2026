"""Indexing a pack's sources into pending values, and a reviewer approving or rejecting them.

`core.grounding.corpus.load_corpus` and `core.grounding.values.extract_values` are each tested
on their own (`tests/test_grounding.py`, `tests/test_grounding_values.py`); here they are
monkeypatched to canned results, because what this module tests is `index_pack`'s own judgement
— upsert always, extract only when the text changed, supersede what a person already approved of
the old text — not the reading of a corpus or the model's proposals.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
import yaml

from core.contracts import GroundingCorpus, GroundingDocument, PackManifest
from core.grounding import index as index_module
from core.grounding import review as review_module
from core.grounding.corpus import SourceText
from core.grounding.review import PendingValue
from core.grounding.values import ExtractedValue
from core.packs import InstalledPack
from core.runtime.ollama import ModelUnavailable
from scripts import index_grounding, review_grounding_values

IRAS_MANIFEST = "packs/iras_tax/pack.yaml"
TODAY = date(2026, 9, 14)
ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------------------------------------- fixtures


def _installed(pack_id: str = "iras_tax") -> InstalledPack:
    with open(IRAS_MANIFEST, encoding="utf-8") as fh:
        manifest = PackManifest.model_validate(yaml.safe_load(fh))
    return InstalledPack(manifest.model_copy(update={"id": pack_id}))


def _source(pack_id: str = "iras_tax", sha256: bytes = b"\x11" * 32) -> SourceText:
    document = GroundingDocument(
        file="relief_rates.md",
        title="Individual Income Tax Reliefs, Rebates and Deductions",
        publisher="Inland Revenue Authority of Singapore",
        publisher_kind="government",
        url="https://www.iras.gov.sg/reliefs",
        retrieved=date(2026, 2, 1),
        applies_to="Year of Assessment 2026",
        review_by=date(2027, 4, 1),
    )
    corpus = GroundingCorpus(
        corpus_id="test_corpus",
        applies_to="Year of Assessment 2026",
        maintained_by="Zee",
        reviewed_by="Siew",
        reviewed_on=date(2026, 3, 1),
        documents=[document],
    )
    return SourceText(
        pack_id=pack_id,
        corpus=corpus,
        document=document,
        text="Qualifying child relief is $4,000 per child.",
        sha256=sha256,
        reviewed_by="Siew",
        reviewed_on=date(2026, 3, 1),
    )


def _extracted(**overrides: Any) -> ExtractedValue:
    base: dict[str, Any] = {
        "key": "relief_cap",
        "unit": "money",
        "value_num": Decimal("4000"),
        "value_text": "4,000",
        "qualifiers": {},
        "passage": "Qualifying child relief is $4,000 per child.",
        "confidence": 0.9,
    }
    base.update(overrides)
    return ExtractedValue(**base)


# --------------------------------------------------------------------------------- fake db


class FakeCursor:
    def __init__(self, conn: FakeConn) -> None:
        self._conn = conn
        self._rows: list[tuple[Any, ...]] = []
        self.rowcount = 0

    def execute(self, query: str, params: Any = None) -> None:
        self._conn.calls.append((query, params))
        self._rows, self.rowcount = ([], 0)
        for needle, (rows, rowcount) in self._conn.scripted.items():
            if needle in query:
                self._rows, self.rowcount = rows, rowcount
                break

    def fetchone(self) -> tuple[Any, ...] | None:
        return self._rows[0] if self._rows else None

    def fetchall(self) -> list[tuple[Any, ...]]:
        return self._rows

    def __enter__(self) -> FakeCursor:
        return self

    def __exit__(self, *exc: object) -> None:
        return None


class FakeConn:
    """A recording fake in the house style (see `tests/test_api.py`'s `FakeConn`): every
    statement and its parameters are kept in `calls`, and a test scripts what a query answers
    by a substring of it, rather than parsing SQL."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []
        self.commits = 0
        self.rollbacks = 0
        self.scripted: dict[str, tuple[list[tuple[Any, ...]], int]] = {}

    def script(
        self, needle: str, rows: list[tuple[Any, ...]] | None = None, rowcount: int | None = None
    ) -> None:
        rows = rows or []
        self.scripted[needle] = (rows, rowcount if rowcount is not None else len(rows))

    def cursor(self) -> FakeCursor:
        return FakeCursor(self)

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1

    def params_for(self, needle: str) -> Any:
        for query, params in self.calls:
            if needle in query:
                return params
        raise AssertionError(f"no statement containing {needle!r} was executed")

    def all_params_for(self, needle: str) -> list[Any]:
        return [params for query, params in self.calls if needle in query]


# ----------------------------------------------------------------------------- index_pack


def test_a_new_source_is_extracted_and_inserted_as_pending(monkeypatch: pytest.MonkeyPatch) -> None:
    source = _source()
    monkeypatch.setattr(index_module, "load_corpus", lambda installed, root: [source])
    monkeypatch.setattr(index_module, "extract_values", lambda client, src, keys: [_extracted()])
    conn = FakeConn()
    conn.script("FROM grounding_sources", rows=[])  # nothing stored yet
    conn.script("INSERT INTO grounding_sources", rows=[(7,)])

    report = index_module.index_pack(conn, object(), _installed(), today=TODAY)

    assert report == index_module.IndexReport(sources=1, unchanged=0, pending=1, superseded=0)
    assert conn.commits == 1
    assert not any("DELETE FROM grounding_values" in q for q, _ in conn.calls)
    assert not any("UPDATE grounding_values" in q for q, _ in conn.calls)

    insert_params = conn.params_for("INSERT INTO grounding_values")
    assert insert_params["source_id"] == 7
    assert insert_params["pack_id"] == "iras_tax"
    assert insert_params["key"] == "relief_cap"
    assert insert_params["unit"] == "money"
    assert insert_params["value_num"] == Decimal("4000")
    assert insert_params["value_text"] == "4,000"
    assert json.loads(insert_params["qualifiers"]) == {}
    assert insert_params["passage"] == source.text
    assert insert_params["confidence"] == 0.9


def test_an_unchanged_sha256_inserts_nothing_but_upserts_the_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _source(sha256=b"\x11" * 32)
    monkeypatch.setattr(index_module, "load_corpus", lambda installed, root: [source])
    extraction_calls: list[SourceText] = []
    monkeypatch.setattr(
        index_module,
        "extract_values",
        lambda client, src, keys: extraction_calls.append(src) or [],
    )
    conn = FakeConn()
    conn.script("FROM grounding_sources", rows=[(3, b"\x11" * 32)])  # same hash already stored
    conn.script("INSERT INTO grounding_sources", rows=[(3,)])

    report = index_module.index_pack(conn, object(), _installed(), today=TODAY)

    assert report == index_module.IndexReport(sources=1, unchanged=1, pending=0, superseded=0)
    assert extraction_calls == []  # extraction is skipped entirely
    assert not any("DELETE FROM grounding_values" in q for q, _ in conn.calls)
    assert not any("UPDATE grounding_values" in q for q, _ in conn.calls)
    assert not any("INSERT INTO grounding_values" in q for q, _ in conn.calls)

    # the source row is still refreshed every run
    upsert_params = conn.params_for("INSERT INTO grounding_sources")
    assert upsert_params["title"] == source.document.title
    assert upsert_params["sha256"] == source.sha256
    assert conn.commits == 1


def test_a_changed_sha256_deletes_pending_supersedes_approved_then_inserts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _source(sha256=b"\x22" * 32)
    monkeypatch.setattr(index_module, "load_corpus", lambda installed, root: [source])
    monkeypatch.setattr(index_module, "extract_values", lambda client, src, keys: [_extracted()])
    conn = FakeConn()
    conn.script("FROM grounding_sources", rows=[(9, b"\x11" * 32)])  # a different old hash
    conn.script("INSERT INTO grounding_sources", rows=[(9,)])
    conn.script("UPDATE grounding_values", rowcount=2)  # two approved rows superseded

    report = index_module.index_pack(conn, object(), _installed(), today=TODAY)

    assert report == index_module.IndexReport(sources=1, unchanged=0, pending=1, superseded=2)
    assert conn.params_for("DELETE FROM grounding_values") == {"s": 9}
    assert conn.params_for("UPDATE grounding_values") == {"s": 9, "today": TODAY}
    insert_params = conn.params_for("INSERT INTO grounding_values")
    assert insert_params["source_id"] == 9
    assert conn.commits == 1


def test_a_changed_source_is_extracted_before_anything_is_written(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _source(sha256=b"\x22" * 32)
    monkeypatch.setattr(index_module, "load_corpus", lambda installed, root: [source])
    conn = FakeConn()
    conn.script("FROM grounding_sources", rows=[(9, b"\x11" * 32)])
    conn.script("INSERT INTO grounding_sources", rows=[(9,)])
    statements_at_extraction: list[int] = []

    def extract(client: Any, src: SourceText, keys: Any) -> list[ExtractedValue]:
        statements_at_extraction.append(len(conn.calls))
        return [_extracted()]

    monkeypatch.setattr(index_module, "extract_values", extract)

    index_module.index_pack(conn, object(), _installed(), today=TODAY)

    assert statements_at_extraction == [1]  # only the SELECT had run
    kinds = (
        "SELECT id, sha256",
        "DELETE FROM grounding_values",
        "UPDATE grounding_values",
        "INSERT INTO grounding_sources",
        "INSERT INTO grounding_values",
    )
    order = [next(kind for kind in kinds if kind in query) for query, _ in conn.calls]
    assert order == list(kinds)


@pytest.mark.parametrize("stored", [None, b"\x11" * 32], ids=["new", "changed"])
def test_an_unreadable_source_is_skipped_and_the_rest_committed(
    monkeypatch: pytest.MonkeyPatch, stored: bytes | None
) -> None:
    unchanged = _source(sha256=b"\x33" * 32)
    changed = _source(sha256=b"\x22" * 32)
    monkeypatch.setattr(index_module, "load_corpus", lambda installed, root: [unchanged, changed])

    def extract(client: Any, src: SourceText, keys: Any) -> list[ExtractedValue]:
        raise ModelUnavailable("the model did not answer")

    monkeypatch.setattr(index_module, "extract_values", extract)
    conn = FakeConn()
    # the first source is stored with the same hash; the second is new or changed
    selects = iter([[(3, b"\x33" * 32)], [(9, stored)] if stored is not None else []])
    real_execute = FakeCursor.execute

    def execute(self: FakeCursor, query: str, params: Any = None) -> None:
        real_execute(self, query, params)
        if "FROM grounding_sources" in query and "INSERT" not in query:
            self._rows = next(selects)

    monkeypatch.setattr(FakeCursor, "execute", execute)
    conn.script("INSERT INTO grounding_sources", rows=[(3,)])

    report = index_module.index_pack(conn, object(), _installed(), today=TODAY)

    assert (report.unread, report.pending) == (1, 0)
    assert conn.commits == 1
    assert conn.rollbacks == 0
    touched = [q for q, _ in conn.calls if "grounding_values" in q]
    assert touched == []  # the unread source's values are neither deleted nor superseded
    upserted = conn.all_params_for("INSERT INTO grounding_sources")
    # only the unchanged source: the unread one keeps its old hash, so the next run retries it
    assert [params["sha256"] for params in upserted] == [unchanged.sha256]


def test_a_pack_with_no_corpus_returns_all_zeros(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(index_module, "load_corpus", lambda installed, root: [])
    conn = FakeConn()

    report = index_module.index_pack(conn, object(), _installed(), today=TODAY)

    assert report == index_module.IndexReport(sources=0, unchanged=0, pending=0, superseded=0)
    assert conn.calls == []


# ------------------------------------------------------------------------------------ review


def test_approve_passes_only_the_ids_and_the_pending_condition() -> None:
    conn = FakeConn()
    conn.script("status = 'approved'", rowcount=2)

    count = review_module.approve(conn, [3, 4], reviewer="Siew", on=TODAY)

    assert count == 2
    query, params = conn.calls[-1]
    assert "status = 'pending'" in query
    assert "status = 'approved'" in query
    assert params == {"ids": [3, 4], "reviewer": "Siew", "on": TODAY}
    assert conn.commits == 1


def test_reject_requires_a_note_and_touches_only_pending_rows() -> None:
    conn = FakeConn()
    conn.script("status = 'rejected'", rowcount=1)

    count = review_module.reject(conn, [8], reviewer="Siew", on=TODAY, note="wrong year")

    assert count == 1
    query, params = conn.calls[-1]
    assert "status = 'pending'" in query
    assert params == {"ids": [8], "reviewer": "Siew", "on": TODAY, "note": "wrong year"}


def test_pending_reads_every_column_of_a_value_and_its_source() -> None:
    conn = FakeConn()
    conn.script(
        "JOIN grounding_sources",
        rows=[
            (
                42,
                "iras_tax",
                "relief_cap",
                "money",
                Decimal("4000"),
                "4,000",
                {"assessment_year": "2026"},
                "Qualifying child relief is $4,000 per child.",
                "Individual Income Tax Reliefs, Rebates and Deductions",
                "Inland Revenue Authority of Singapore",
                "https://www.iras.gov.sg/reliefs",
                "Year of Assessment 2026",
                date(2027, 4, 1),
            )
        ],
    )

    [value] = review_module.pending(conn, "iras_tax")

    assert value == PendingValue(
        id=42,
        pack_id="iras_tax",
        key="relief_cap",
        unit="money",
        value_num=Decimal("4000"),
        value_text="4,000",
        qualifiers={"assessment_year": "2026"},
        passage="Qualifying child relief is $4,000 per child.",
        source_title="Individual Income Tax Reliefs, Rebates and Deductions",
        publisher="Inland Revenue Authority of Singapore",
        url="https://www.iras.gov.sg/reliefs",
        applies_to="Year of Assessment 2026",
        review_by=date(2027, 4, 1),
    )
    assert conn.params_for("JOIN grounding_sources")["pack_id"] == "iras_tax"


# -------------------------------------------------------------------------------- index CLI


class _Connected:
    def __init__(self, conn: FakeConn) -> None:
        self._conn = conn

    def __enter__(self) -> FakeConn:
        return self._conn

    def __exit__(self, *exc: object) -> None:
        return None


def _script_env(monkeypatch: pytest.MonkeyPatch, *, enabled: tuple[InstalledPack, ...]) -> None:
    """Patch the settings, database and pack lookups `scripts/index_grounding.py` imports."""
    from core import packs, registry
    from core.runtime import db, settings

    conn = FakeConn()
    monkeypatch.setattr(settings.Settings, "load", staticmethod(lambda root: object()))
    monkeypatch.setattr(db, "connect", lambda loaded: _Connected(conn))
    monkeypatch.setattr(packs, "pack", lambda pack_id: _installed(pack_id))
    monkeypatch.setattr(registry, "enabled_packs", lambda c: enabled)


def test_index_cli_stops_with_2_when_the_model_is_down(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _script_env(monkeypatch, enabled=(_installed("iras_tax"),))

    def down(*args: Any, **kwargs: Any) -> index_module.IndexReport:
        raise ModelUnavailable("gemma did not answer")

    monkeypatch.setattr(index_module, "index_pack", down)

    code = index_grounding.main(["--pack", "iras_tax"])

    assert code == 2
    lines = [line for line in capsys.readouterr().out.splitlines() if line.strip()]
    assert len(lines) == 1
    assert "iras_tax" in lines[0] and "gemma did not answer" in lines[0]


def test_index_cli_warns_about_a_pack_that_is_not_enabled_and_indexes_it(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _script_env(monkeypatch, enabled=())
    indexed: list[str] = []

    def index(conn: Any, client: Any, installed: InstalledPack, **kwargs: Any) -> Any:
        indexed.append(installed.id)
        return index_module.IndexReport(sources=0, unchanged=0, pending=0, superseded=0)

    monkeypatch.setattr(index_module, "index_pack", index)

    code = index_grounding.main(["--pack", "iras_tax"])

    assert code == 0
    assert indexed == ["iras_tax"]
    out = capsys.readouterr().out
    assert "iras_tax is not enabled" in out


# ------------------------------------------------------------------------------- review CLI


def test_list_block_shows_id_pack_key_value_source_and_an_indented_passage() -> None:
    value = PendingValue(
        id=42,
        pack_id="iras_tax",
        key="relief_cap",
        unit="money",
        value_num=Decimal("4000"),
        value_text="4,000",
        qualifiers={"assessment_year": "2026"},
        passage="Qualifying child relief\nis $4,000  per child.",
        source_title="Individual Income Tax Reliefs, Rebates and Deductions",
        publisher="Inland Revenue Authority of Singapore",
        url="https://www.iras.gov.sg/reliefs",
        applies_to="Year of Assessment 2026",
        review_by=date(2027, 4, 1),
    )

    lines = review_grounding_values._block(value).splitlines()

    assert lines[0] == "[42] iras_tax / relief_cap"
    assert "4,000" in lines[1] and "money" in lines[1] and "assessment_year=2026" in lines[1]
    assert "Inland Revenue Authority of Singapore" in lines[2]
    assert "Individual Income Tax Reliefs, Rebates and Deductions" in lines[2]
    assert lines[3] == "  applies to Year of Assessment 2026, review by 2027-04-01"
    assert lines[4] == "  https://www.iras.gov.sg/reliefs"
    assert lines[5] == '    "Qualifying child relief is $4,000 per child."'  # newlines collapsed


def test_review_cli_needs_by_to_approve() -> None:
    with pytest.raises(SystemExit) as error:
        review_grounding_values.main(["--approve", "1", "2"])
    assert error.value.code == 2


def test_review_cli_needs_a_note_to_reject() -> None:
    with pytest.raises(SystemExit) as error:
        review_grounding_values.main(["--reject", "1", "--by", "Siew"])
    assert error.value.code == 2


def test_review_cli_approve_and_reject_together_is_a_parser_error() -> None:
    with pytest.raises(SystemExit) as error:
        review_grounding_values.main(["--approve", "1", "--reject", "2", "--by", "Siew"])
    assert error.value.code == 2


def test_review_cli_pack_is_only_valid_with_list() -> None:
    with pytest.raises(SystemExit) as error:
        review_grounding_values.main(["--approve", "1", "--by", "Siew", "--pack", "iras_tax"])
    assert error.value.code == 2


def _review_env(monkeypatch: pytest.MonkeyPatch) -> FakeConn:
    """Patch the settings and database `scripts/review_grounding_values.py` imports."""
    from core.runtime import db, settings

    conn = FakeConn()
    monkeypatch.setattr(settings.Settings, "load", staticmethod(lambda root: object()))
    monkeypatch.setattr(db, "connect", lambda loaded: _Connected(conn))
    return conn


def test_review_cli_approving_an_already_decided_id_exits_1(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    conn = _review_env(monkeypatch)
    conn.script("status = 'approved'", rowcount=0)  # nothing was still pending

    code = review_grounding_values.main(["--approve", "9", "--by", "Siew"])

    assert code == 1
    assert "0 value(s) approved." in capsys.readouterr().out


@pytest.mark.parametrize(
    ("script", "needle"),
    [
        ("scripts/review_grounding_values.py", "--approve"),
        ("scripts/index_grounding.py", "--pack"),
    ],
)
def test_help_runs_without_importing_core_before_sys_path_is_set(script: str, needle: str) -> None:
    """`--help` must work even though `core` is not on `sys.path` until the script inserts it
    itself: a module-level `from core... import ...` above that insertion breaks this with
    `ModuleNotFoundError: No module named 'core'` (see `scripts/reindex.py` for the pattern)."""
    result = subprocess.run(
        [sys.executable, script, "--help"], cwd=ROOT, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    assert needle in result.stdout
