"""Read and validate a pack's grounding corpus from its own folder on disk.

A pack's `sources.yaml` is the single record of what may be cited: which files exist, who
published them, and who reviewed them. This module checks the folder against that record
rather than trusting either one alone, because a corpus that silently drifted from its
provenance file is exactly the failure ADR 0016 exists to rule out.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

from core.contracts import GroundingCorpus, GroundingDocument
from core.packs import PACKS_DIR, InstalledPack


class CorpusInvalid(RuntimeError):
    """A pack's grounding corpus on disk does not match what its `sources.yaml` records."""


@dataclass(frozen=True, slots=True)
class SourceText:
    pack_id: str
    corpus: GroundingCorpus
    document: GroundingDocument
    text: str
    sha256: bytes
    reviewed_by: str | None
    reviewed_on: date | None


def corpus_dir(installed: InstalledPack, root: Path = PACKS_DIR) -> Path | None:
    """Where this pack's grounding corpus lives on disk, or `None` if it declares none."""
    corpus = installed.manifest.grounding.corpus
    if corpus is None:
        return None
    return root / installed.id / "grounding" / corpus


def load_corpus(installed: InstalledPack, root: Path = PACKS_DIR) -> list[SourceText]:
    """Read, validate and hash every source this pack's corpus records.

    Raises `CorpusInvalid` when the folder and its `sources.yaml` disagree: the manifest is
    missing, its `corpus_id` does not match the directory it lives in, a `.md` file nobody
    recorded sits beside it, or a recorded file is not there. A pack that declares no corpus
    is not an error — it is simply empty, since a pack may not have been given sources yet.
    """
    directory = corpus_dir(installed, root)
    if directory is None:
        return []

    sources_path = directory / "sources.yaml"
    if not sources_path.is_file():
        raise CorpusInvalid(f"{installed.id}: {sources_path} is missing")

    raw = yaml.safe_load(sources_path.read_text(encoding="utf-8"))
    corpus = GroundingCorpus.model_validate(raw)

    if corpus.corpus_id != directory.name:
        raise CorpusInvalid(
            f"{installed.id}: sources.yaml declares corpus_id {corpus.corpus_id!r}, which does "
            f"not match its directory {directory.name!r}"
        )

    recorded = {document.file for document in corpus.documents}
    for md_file in sorted(directory.glob("*.md")):
        if md_file.name not in recorded:
            raise CorpusInvalid(
                f"{installed.id}/{corpus.corpus_id}: {md_file.name} is not recorded in sources.yaml"
            )

    results: list[SourceText] = []
    for document in corpus.documents:
        file_path = directory / document.file
        if not file_path.is_file():
            raise CorpusInvalid(
                f"{installed.id}/{corpus.corpus_id}: recorded file {document.file} is missing"
            )
        text = file_path.read_text(encoding="utf-8")
        sha256 = hashlib.sha256(text.encode("utf-8")).digest()
        if document.reviewed_on is not None:
            reviewed_by, reviewed_on = document.reviewed_by, document.reviewed_on
        elif corpus.reviewed_on is not None:
            reviewed_by, reviewed_on = corpus.reviewed_by, corpus.reviewed_on
        else:
            reviewed_by, reviewed_on = None, None
        results.append(
            SourceText(
                pack_id=installed.id,
                corpus=corpus,
                document=document,
                text=text,
                sha256=sha256,
                reviewed_by=reviewed_by,
                reviewed_on=reviewed_on,
            )
        )
    return results
