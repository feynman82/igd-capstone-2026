"""Tests for core.grounding.corpus: reading and validating a pack's corpus from disk."""

from __future__ import annotations

import hashlib
from datetime import date
from pathlib import Path
from typing import Any

import pytest
import yaml

from core.contracts import PackManifest
from core.grounding.corpus import CorpusInvalid, corpus_dir, load_corpus
from core.packs import InstalledPack

IRAS_MANIFEST = "packs/iras_tax/pack.yaml"


def _installed(corpus: str | None) -> InstalledPack:
    """The iras_tax manifest, with `grounding.corpus` set to point at a tmp_path root."""
    with open(IRAS_MANIFEST, encoding="utf-8") as fh:
        manifest = PackManifest.model_validate(yaml.safe_load(fh))
    grounding = manifest.grounding.model_copy(update={"corpus": corpus})
    return InstalledPack(manifest.model_copy(update={"grounding": grounding}), {}, {})


def _document(file: str, **overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "file": file,
        "title": "Individual Income Tax Reliefs, Rebates and Deductions",
        "publisher": "Inland Revenue Authority of Singapore",
        "publisher_kind": "government",
        "url": "https://www.iras.gov.sg/reliefs",
        "retrieved": date(2026, 2, 1),
        "applies_to": "Year of Assessment 2026",
        "review_by": date(2027, 4, 1),
    }
    base.update(overrides)
    return base


def _write_sources(
    directory: Path,
    corpus_id: str,
    documents: list[dict[str, Any]],
    reviewed_on: date | None,
) -> None:
    directory.mkdir(parents=True)
    raw = {
        "corpus_id": corpus_id,
        "applies_to": "Year of Assessment 2026",
        "maintained_by": "Zee",
        "reviewed_by": "Siew",
        "reviewed_on": reviewed_on,
        "documents": documents,
    }
    (directory / "sources.yaml").write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")


def test_a_recorded_source_loads_with_review_inherited_from_the_corpus(tmp_path: Path) -> None:
    installed = _installed("test_corpus")
    directory = tmp_path / "iras_tax" / "grounding" / "test_corpus"
    _write_sources(
        directory,
        "test_corpus",
        [_document("relief_rates.md")],
        reviewed_on=date(2026, 3, 1),
    )
    text = "# Reliefs\n\nQualifying child relief is $4,000 per child.\n"
    (directory / "relief_rates.md").write_text(text, encoding="utf-8")

    loaded = load_corpus(installed, root=tmp_path)

    assert len(loaded) == 1
    source = loaded[0]
    assert source.pack_id == "iras_tax"
    assert source.corpus.corpus_id == "test_corpus"
    assert source.document.file == "relief_rates.md"
    assert source.text == text
    assert source.sha256 == hashlib.sha256(text.encode("utf-8")).digest()
    # Not set on the document itself, so it is inherited from the corpus.
    assert source.reviewed_by == "Siew"
    assert source.reviewed_on == date(2026, 3, 1)


def test_an_unrecorded_md_file_is_refused_and_named(tmp_path: Path) -> None:
    installed = _installed("test_corpus")
    directory = tmp_path / "iras_tax" / "grounding" / "test_corpus"
    _write_sources(directory, "test_corpus", [], reviewed_on=None)
    (directory / "orphan.md").write_text("stray text", encoding="utf-8")

    with pytest.raises(CorpusInvalid, match=r"orphan\.md"):
        load_corpus(installed, root=tmp_path)


def test_a_missing_recorded_file_is_refused(tmp_path: Path) -> None:
    installed = _installed("test_corpus")
    directory = tmp_path / "iras_tax" / "grounding" / "test_corpus"
    _write_sources(directory, "test_corpus", [_document("ghost.md")], reviewed_on=None)

    with pytest.raises(CorpusInvalid, match=r"ghost\.md"):
        load_corpus(installed, root=tmp_path)


def test_a_pack_with_no_corpus_gives_none_and_empty(tmp_path: Path) -> None:
    installed = _installed(None)

    assert corpus_dir(installed, root=tmp_path) is None
    assert load_corpus(installed, root=tmp_path) == []
