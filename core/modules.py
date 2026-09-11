"""Load the installed capability modules at runtime.

The mirror of `core/packs.py`. A pack is a YAML file plus generated schemas; a module is a
YAML file plus a hand-written `queries.py`, and both are discovered the same way — by walking
their directory and validating what is found against the contract in `core/contracts.py`.

This file exists so that the manifest is parsed in exactly one place. It was previously read
only by `core/worker/schedule.py`, which wanted the cron line; the registry wants the whole
manifest, and two readers of the same YAML is how the two of them eventually disagree.

Nothing here imports Celery, a database driver or the interface. A module manifest is data.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

from core.contracts import ModuleManifest

MODULES_DIR = Path(__file__).resolve().parents[1] / "modules"


class ModuleUnavailable(RuntimeError):
    """A module's YAML is missing, or does not validate against `ModuleManifest`."""


@dataclass(frozen=True, slots=True)
class InstalledModule:
    manifest: ModuleManifest

    @property
    def id(self) -> str:
        return self.manifest.id

    @property
    def version(self) -> str:
        return self.manifest.version


def manifest(module_id: str) -> ModuleManifest:
    """One module's manifest, validated. Raises rather than returning a partial object."""
    path = MODULES_DIR / module_id / "module.yaml"
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ModuleUnavailable(f"modules/{module_id}/module.yaml cannot be read") from error
    return ModuleManifest.model_validate(raw)


@lru_cache(maxsize=1)
def installed_modules() -> tuple[InstalledModule, ...]:
    """Every module directory holding a `module.yaml`, in a stable order.

    Directories whose name starts with an underscore are skipped, the same rule `core/packs.py`
    applies: `_template` is a worked example to copy, not an installed module.
    """
    found = []
    for module_dir in sorted(MODULES_DIR.iterdir()):
        if module_dir.name.startswith("_"):
            continue
        if module_dir.is_dir() and (module_dir / "module.yaml").is_file():
            found.append(InstalledModule(manifest(module_dir.name)))
    return tuple(found)
