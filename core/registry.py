"""The `packs` and `modules` tables: what is installed, and what is switched on.

Both tables have existed since `0001_init.sql` and until now nothing wrote to them, which
meant the registry was the filesystem and nothing could be turned off. This module installs
what is on disk into those two tables at startup and reads the enabled flag back out.

Two properties are worth stating because they are the whole point:

**Installing never re-enables.** A person who switches the tax pack off and restarts the
application has switched it off. The upsert updates the version and the manifest and leaves
`enabled` exactly as it found it — so that column belongs to the person, and everything else
in the row belongs to the YAML.

**Empty is not the same as all-disabled.** `enabled_pack_ids` returns `None` when the table
has no rows at all, and a caller reads `None` as "do not filter". A registry that failed to
install therefore shows a household everything, which is wrong in a visible way; the
alternative — an empty set — would silently show them nothing and stop every reminder.

Rule 1: every statement here is hand-written and parameterised.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from core.contracts import ModuleManifest, PackManifest
from core.modules import installed_modules
from core.packs import CORE, InstalledPack, installed_packs
from core.runtime.db import DatabaseUnavailable, connect
from core.runtime.settings import Settings

log = logging.getLogger(__name__)

# --------------------------------------------------------------------------------- the SQL

# `enabled` is deliberately absent from the UPDATE clause: see the module docstring.
UPSERT_PACK = """
INSERT INTO packs (id, version, manifest, enabled)
VALUES (%(id)s, %(version)s, %(manifest)s, true)
ON CONFLICT (id) DO UPDATE
   SET version  = EXCLUDED.version,
       manifest = EXCLUDED.manifest
"""

UPSERT_MODULE = """
INSERT INTO modules (id, version, manifest, enabled)
VALUES (%(id)s, %(version)s, %(manifest)s, true)
ON CONFLICT (id) DO UPDATE
   SET version  = EXCLUDED.version,
       manifest = EXCLUDED.manifest
"""

SELECT_PACKS = """
SELECT id, version, manifest, enabled, installed_at
  FROM packs
 ORDER BY id
"""

SELECT_MODULES = """
SELECT id, version, manifest, enabled
  FROM modules
 ORDER BY id
"""

SELECT_PACK_FLAGS = "SELECT id, enabled FROM packs ORDER BY id"

SET_PACK_ENABLED = """
UPDATE packs
   SET enabled = %(enabled)s
 WHERE id = %(id)s
RETURNING id, version, manifest, enabled, installed_at
"""

SET_MODULE_ENABLED = """
UPDATE modules
   SET enabled = %(enabled)s
 WHERE id = %(id)s
RETURNING id, version, manifest, enabled
"""

# What a pack has to show for itself on the settings screen. Counted rather than estimated,
# because "7 documents, 41 facts" is what makes switching one off a considered decision.
COUNT_DOCUMENTS_BY_PACK = """
SELECT pack_id, count(*)
  FROM documents
 WHERE pack_id IS NOT NULL
 GROUP BY pack_id
"""

COUNT_FACTS_BY_PACK = "SELECT pack_id, count(*) FROM facts GROUP BY pack_id"


# --------------------------------------------------------------------------------- the rows


@dataclass(frozen=True, slots=True)
class RegisteredPack:
    """One row of `packs`, with the manifest validated back out of its jsonb column."""

    id: str
    version: str
    enabled: bool
    installed_at: datetime | None
    manifest: PackManifest | None  # None when the stored jsonb no longer validates
    on_disk: bool
    documents: int = 0
    facts: int = 0


@dataclass(frozen=True, slots=True)
class RegisteredModule:
    id: str
    version: str
    enabled: bool
    manifest: ModuleManifest | None
    on_disk: bool


@dataclass(frozen=True, slots=True)
class Installed:
    """What `install` did, so a startup line can say it in one sentence."""

    packs: tuple[str, ...]
    modules: tuple[str, ...]

    def line(self) -> str:
        names = ", ".join(self.packs + self.modules) or "none"
        return (
            f"registry: {len(self.packs)} pack(s) and {len(self.modules)} module(s) "
            f"installed ({names})"
        )


class UnknownPack(KeyError):
    """No row in `packs` with that id."""


class UnknownModule(KeyError):
    """No row in `modules` with that id."""


# ------------------------------------------------------------------------------ installation


def install(conn: Any) -> Installed:
    """Write every pack and module on disk into its table. Idempotent; never re-enables.

    This commits, because it is a startup step that either happened or did not and there is
    no larger transaction it belongs to.
    """
    packs_on_disk = installed_packs()
    modules_on_disk = installed_modules()
    with conn.cursor() as cur:
        for installed_pack in packs_on_disk:
            cur.execute(
                UPSERT_PACK,
                {
                    "id": installed_pack.id,
                    "version": installed_pack.version,
                    "manifest": json.dumps(installed_pack.manifest.model_dump(mode="json")),
                },
            )
        for installed_module in modules_on_disk:
            cur.execute(
                UPSERT_MODULE,
                {
                    "id": installed_module.id,
                    "version": installed_module.version,
                    "manifest": json.dumps(installed_module.manifest.model_dump(mode="json")),
                },
            )
    conn.commit()
    done = Installed(
        tuple(p.id for p in packs_on_disk),
        tuple(m.id for m in modules_on_disk),
    )
    log.info("%s", done.line())
    return done


def install_best_effort(settings: Settings) -> Installed | None:
    """Install at startup without being able to stop startup.

    Both processes that own a registry call this — the API server and the Celery worker — and
    neither of them may refuse to come up because the database is not running yet. The setup
    page exists precisely so a person can be told their database is missing; a server that
    cannot start cannot tell them anything. So this logs and returns `None`.
    """
    try:
        with connect(settings) as conn:
            return install(conn)
    except DatabaseUnavailable as error:
        log.warning("registry: not installed — %s", error)
        return None
    except Exception as error:  # startup must survive a bad pack on disk
        log.warning("registry: not installed — %s: %s", type(error).__name__, error)
        return None


# ---------------------------------------------------------------------------------- reading


def enabled_pack_ids(conn: Any) -> frozenset[str] | None:
    """The packs left switched on, plus `core`, or `None` when nothing has been installed yet.

    `None` means "do not filter". See the module docstring for why that is not the same as
    a set holding only `core`, which means "a person has switched every pack off". `core` is
    always in the set and never a row: every document and fact is the core's (ADR 0017), so
    every filter on this set keeps the household's documents whatever is switched off.
    """
    with conn.cursor() as cur:
        cur.execute(SELECT_PACK_FLAGS)
        rows = cur.fetchall()
    if not rows:
        return None
    return frozenset({CORE, *(pack_id for pack_id, enabled in rows if enabled)})


def enabled_packs(conn: Any) -> tuple[InstalledPack, ...]:
    """The installed packs a person has left switched on, as loaded pack objects.

    This is what `modules.alert.sweep` takes, so a disabled pack's thresholds never fire.
    """
    allowed = enabled_pack_ids(conn)
    if allowed is None:
        return installed_packs()
    return tuple(pack for pack in installed_packs() if pack.id in allowed)


def enabled_module_ids(conn: Any) -> frozenset[str] | None:
    """The modules left switched on, or `None` when nothing has been installed yet."""
    with conn.cursor() as cur:
        cur.execute(SELECT_MODULES)
        rows = cur.fetchall()
    if not rows:
        return None
    return frozenset(row[0] for row in rows if row[3])


def _pack_row(
    row: tuple[Any, ...],
    on_disk: set[str],
    documents: dict[str, int],
    facts: dict[str, int],
) -> RegisteredPack:
    pack_id, version, raw, enabled, installed_at = row
    manifest: PackManifest | None
    try:
        manifest = PackManifest.model_validate(raw)
    except ValueError:
        # A stored manifest that no longer validates is data, not a crash. The row still says
        # what is installed and whether it is on; the screen shows it without its detail.
        log.warning("packs.%s holds a manifest that no longer validates", pack_id)
        manifest = None
    return RegisteredPack(
        id=pack_id,
        version=version,
        enabled=bool(enabled),
        installed_at=installed_at,
        manifest=manifest,
        on_disk=pack_id in on_disk,
        documents=documents.get(pack_id, 0),
        facts=facts.get(pack_id, 0),
    )


def packs(conn: Any) -> list[RegisteredPack]:
    """Every installed pack, with what it has extracted so far."""
    on_disk = {installed.id for installed in installed_packs()}
    with conn.cursor() as cur:
        cur.execute(COUNT_DOCUMENTS_BY_PACK)
        documents = {pack_id: count for pack_id, count in cur.fetchall()}
        cur.execute(COUNT_FACTS_BY_PACK)
        facts = {pack_id: count for pack_id, count in cur.fetchall()}
        cur.execute(SELECT_PACKS)
        rows = cur.fetchall()
    return [_pack_row(row, on_disk, documents, facts) for row in rows]


def _module_row(row: tuple[Any, ...], on_disk: set[str]) -> RegisteredModule:
    module_id, version, raw, enabled = row
    manifest: ModuleManifest | None
    try:
        manifest = ModuleManifest.model_validate(raw)
    except ValueError:
        log.warning("modules.%s holds a manifest that no longer validates", module_id)
        manifest = None
    return RegisteredModule(
        id=module_id,
        version=version,
        enabled=bool(enabled),
        manifest=manifest,
        on_disk=module_id in on_disk,
    )


def modules(conn: Any) -> list[RegisteredModule]:
    on_disk = {installed.id for installed in installed_modules()}
    with conn.cursor() as cur:
        cur.execute(SELECT_MODULES)
        rows = cur.fetchall()
    return [_module_row(row, on_disk) for row in rows]


# ---------------------------------------------------------------------------------- writing


def set_pack_enabled(conn: Any, pack_id: str, *, enabled: bool) -> RegisteredPack:
    """Switch one pack on or off. Raises `UnknownPack` rather than silently doing nothing."""
    with conn.cursor() as cur:
        cur.execute(SET_PACK_ENABLED, {"id": pack_id, "enabled": enabled})
        row = cur.fetchone()
    if row is None:
        conn.rollback()
        raise UnknownPack(pack_id)
    conn.commit()
    log.info("pack %s is now %s", pack_id, "enabled" if enabled else "disabled")
    return _pack_row(row, {installed.id for installed in installed_packs()}, {}, {})


def set_module_enabled(conn: Any, module_id: str, *, enabled: bool) -> RegisteredModule:
    with conn.cursor() as cur:
        cur.execute(SET_MODULE_ENABLED, {"id": module_id, "enabled": enabled})
        row = cur.fetchone()
    if row is None:
        conn.rollback()
        raise UnknownModule(module_id)
    conn.commit()
    log.info("module %s is now %s", module_id, "enabled" if enabled else "disabled")
    return _module_row(row, {installed.id for installed in installed_modules()})
