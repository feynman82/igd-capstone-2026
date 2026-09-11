"""Load the installed packs at runtime.

A pack is authored as one YAML file and `python -m packs.build` generates the Pydantic
extraction models beside it. This module reads both: the manifest for what a document type is
and what the guardrails say, and the generated `schemas.py` for the model the extractor
constrains the generator to.

Nothing here writes to `packs/`. Rule 6 — the YAML generates its outputs and the outputs are
never edited — is enforced by `python -m packs.build --check` in `make check`, not by us.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel

from core.contracts import DocumentTypeSpec, PackManifest

PACKS_DIR = Path(__file__).resolve().parents[1] / "packs"


class PackUnavailable(RuntimeError):
    """A pack's YAML and its generated schemas disagree, or the pack does not exist."""


@dataclass(frozen=True, slots=True)
class InstalledPack:
    manifest: PackManifest
    models: dict[str, type[BaseModel]]  # doc_type -> generated extraction model
    fact_columns: dict[str, str]  # field name -> the facts column it lands in

    @property
    def id(self) -> str:
        return self.manifest.id

    @property
    def version(self) -> str:
        return self.manifest.version

    def spec(self, doc_type: str) -> DocumentTypeSpec:
        try:
            return self.manifest.document_types[doc_type]
        except KeyError as error:
            raise PackUnavailable(f"{self.id} does not declare {doc_type}") from error


def _load_one(pack_dir: Path) -> InstalledPack:
    raw = yaml.safe_load((pack_dir / "pack.yaml").read_text(encoding="utf-8"))
    manifest = PackManifest.model_validate(raw)
    try:
        schemas = importlib.import_module(f"packs.{pack_dir.name}.schemas")
    except ImportError as error:
        raise PackUnavailable(
            f"packs/{pack_dir.name}/schemas.py is missing. Run python -m packs.build."
        ) from error
    models: dict[str, type[BaseModel]] = dict(schemas.MODELS)
    missing = set(manifest.document_types) - set(models)
    if missing:
        raise PackUnavailable(
            f"{manifest.id}: schemas.py has no model for {sorted(missing)}. "
            "Run python -m packs.build."
        )
    return InstalledPack(manifest, models, dict(schemas.FACT_COLUMNS))


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


def document_types() -> dict[str, tuple[str, DocumentTypeSpec]]:
    """`"<pack>.<doc_type>"` -> (pack_id, spec). The classifier's whole candidate list.

    Qualified by pack id because two packs may legitimately both recognise a `renewal_notice`,
    and a fact has to be attributed to the pack whose field names it used.
    """
    return {
        f"{installed.id}.{doc_type}": (installed.id, spec)
        for installed in installed_packs()
        for doc_type, spec in installed.manifest.document_types.items()
    }
