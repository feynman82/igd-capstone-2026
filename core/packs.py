"""Load the core document catalogue and the installed packs at runtime.

The core owns documents (ADR 0017): `core/documents.yaml` declares every document type, its
fields and registers, and `python -m packs.build` generates `core/document_schemas.py` from it —
the Pydantic models the extractor constrains the generator to. A pack is grounding, persona, its
own answering and advice, and every core name it uses is checked against the catalogue here.

Nothing here writes a generated file. Rule 6 — the YAML generates its outputs and the outputs are
never edited — is enforced by `python -m packs.build --check` in `make check`, not by us.
"""

from __future__ import annotations

import hashlib
import importlib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel

from core.contracts import DocumentCatalog, DocumentTypeSpec, PackManifest

PACKS_DIR = Path(__file__).resolve().parents[1] / "packs"
CATALOG_FILE = Path(__file__).resolve().parent / "documents.yaml"

# The pack_id every document, fact and obligation is written with. Always enabled, never listed
# as a pack: disabling a pack switches off its voice and advice, never the household's documents.
CORE = "core"


class PackUnavailable(RuntimeError):
    """A pack names what the catalogue does not declare, or the pack does not exist."""


@dataclass(frozen=True, slots=True)
class Catalog:
    documents: DocumentCatalog
    models: dict[str, type[BaseModel]]  # doc_type -> generated extraction model
    fact_columns: dict[str, str]  # field name -> the facts column it lands in
    version: str  # sha256 of core/documents.yaml, first 12 hex: which field list read a fact

    def spec(self, doc_type: str) -> DocumentTypeSpec:
        try:
            return self.documents.document_types[doc_type]
        except KeyError as error:
            raise PackUnavailable(f"the core catalogue does not declare {doc_type}") from error


@lru_cache(maxsize=1)
def catalog() -> Catalog:
    raw = CATALOG_FILE.read_bytes()
    documents = DocumentCatalog.model_validate(yaml.safe_load(raw))
    schemas = importlib.import_module("core.document_schemas")
    models: dict[str, type[BaseModel]] = dict(schemas.MODELS)
    if missing := set(documents.document_types) - set(models):
        raise PackUnavailable(
            f"core/document_schemas.py has no model for {sorted(missing)}. "
            "Run python -m packs.build."
        )
    version = hashlib.sha256(raw).hexdigest()[:12]
    return Catalog(documents, models, dict(schemas.FACT_COLUMNS), version)


@dataclass(frozen=True, slots=True)
class InstalledPack:
    manifest: PackManifest

    @property
    def id(self) -> str:
        return self.manifest.id

    @property
    def version(self) -> str:
        return self.manifest.version


def _load_one(pack_dir: Path) -> InstalledPack:
    raw = yaml.safe_load((pack_dir / "pack.yaml").read_text(encoding="utf-8"))
    manifest = PackManifest.model_validate(raw)
    try:
        manifest.check_against(catalog().documents)
    except ValueError as error:
        raise PackUnavailable(str(error)) from error
    return InstalledPack(manifest)


@lru_cache(maxsize=1)
def installed_packs() -> tuple[InstalledPack, ...]:
    """Every pack directory holding a pack.yaml, in a stable order.

    Directories whose name starts with an underscore are skipped, which is the same rule
    `packs/build.py` applies: `_template` is a worked example to copy, not a pack.
    """
    found = []
    for pack_dir in sorted(PACKS_DIR.iterdir()):
        if pack_dir.name.startswith("_"):
            continue  # `_template` is a worked example to copy, not an installed pack
        if pack_dir.is_dir() and (pack_dir / "pack.yaml").is_file():
            found.append(_load_one(pack_dir))
    return tuple(found)


def pack(pack_id: str) -> InstalledPack:
    for installed in installed_packs():
        if installed.id == pack_id:
            return installed
    raise PackUnavailable(f"no installed pack with id {pack_id}")


def document_types() -> dict[str, DocumentTypeSpec]:
    """doc_type -> spec. The classifier's whole candidate list, from the catalogue alone."""
    return dict(catalog().documents.document_types)
