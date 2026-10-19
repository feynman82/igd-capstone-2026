"""Load a frozen corpus commit into an isolated vault, verify it, and report — for Run 3.

    uv run python -m eval.freeze --commit <sha> --household <file> --dry-run   # manifest only
    uv run python -m eval.freeze --commit <sha> --household <file> --expect-manifest <file>

Issue #85 decided that Run 3 is not measured against the shared development vault: it holds
September copies of documents that were regenerated since, lacks documents committed since, and
its household was curated by hand. Run 3 runs against **a frozen Git commit and a SHA-256
manifest of the committed corpus**, loaded once into a vault of its own and then left alone.

This is that load, as one command that never opens the development vault:

1. **The manifest is read from the commit, not the working tree.** Every file under
   `corpus/batches/` is listed with `git ls-tree` and hashed from `git cat-file`, so a file
   edited, regenerated or deleted on disk cannot change what is loaded. With `--expect-manifest`
   the load is refused if a single path or hash differs from the published one.
2. **A separate database** on the same server, with the schema from `db/migrations/`, the packs
   and modules registered as the application registers them at startup, and the household
   loaded from a **declaration file**: who the owner is, how each person is related to them and
   the names they appear under on paper. That is state a person curates; it is declared, not
   copied from another vault.
3. **Each document ingested from the commit's bytes** through `core.ingest.pipeline.process`,
   never through `inbox/`. Set C's planted documents (`corpus/batches/batch3/`) are listed in
   the manifest but **held out** under the Set C protocol: `eval.setc` adds them to a copy.
4. **A verification report**: every document's stored hash against the manifest, indexed and
   quarantined counts with reasons, and extraction against the register *as committed at that
   commit*. Written to `eval/results/`, which is append-only.

The vault is kept: it is Run 3's. Score it with `eval.run --vault <name>`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import subprocess
import sys
import tempfile
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VAULT = "parrot_run3"
BATCHES = "corpus/batches"
REGISTERS = "corpus/register"
SET_C = "corpus/batches/batch3/"
DOCUMENT_SUFFIXES = frozenset({".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp"})
RELATIONS = ("self", "partner", "child", "parent", "other")


class FreezeRefused(RuntimeError):
    """Safe to show. Raised before anything is created or written."""


# ------------------------------------------------------------------------------ the manifest


@dataclass(frozen=True, slots=True)
class Entry:
    path: str  # repository-relative, as Git names it
    sha256: str
    size: int
    role: str  # "vault" is loaded; "set_c" is listed and held out for eval.setc

    @property
    def name(self) -> str:
        return self.path.rsplit("/", 1)[-1]


def _git(root: Path, *args: str) -> bytes:
    try:
        return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True).stdout
    except subprocess.CalledProcessError as error:
        detail = error.stderr.decode(errors="replace").strip()
        raise FreezeRefused(f"git {' '.join(args)} failed: {detail}") from error


def resolve(commit: str, root: Path = ROOT) -> str:
    """The full commit id: a branch name or a short id moves, and a frozen run must not."""
    return _git(root, "rev-parse", "--verify", f"{commit}^{{commit}}").decode().strip()


def blob(commit: str, path: str, root: Path = ROOT) -> bytes:
    return _git(root, "cat-file", "blob", f"{commit}:{path}")


def role(path: str) -> str:
    return "set_c" if path.startswith(SET_C) else "vault"


def corpus_files(commit: str, root: Path = ROOT) -> list[Entry]:
    """Every document under `corpus/batches/` at `commit`, hashed from the commit's own bytes."""
    listed = _git(root, "ls-tree", "-r", "-z", "--name-only", commit, "--", BATCHES)
    paths = sorted(
        path
        for path in listed.decode().split("\0")
        if path
        and Path(path).suffix.lower() in DOCUMENT_SUFFIXES
        and not Path(path).name.startswith(".")
    )
    entries = []
    for path in paths:
        payload = blob(commit, path, root)
        entries.append(Entry(path, hashlib.sha256(payload).hexdigest(), len(payload), role(path)))
    return entries


def manifest_sha(entries: Iterable[Entry]) -> str:
    """One hash over every path and its content hash, independent of listing order."""
    digest = hashlib.sha256()
    for entry in sorted(entries, key=lambda e: e.path):
        digest.update(f"{entry.path}\t{entry.sha256}\n".encode())
    return digest.hexdigest()


def manifest(commit: str, entries: Sequence[Entry]) -> dict[str, Any]:
    return {
        "commit": commit,
        "manifest_sha256": manifest_sha(entries),
        "files": [asdict(entry) for entry in entries],
    }


def differences(expected: dict[str, Any], entries: Sequence[Entry]) -> list[str]:
    """Every path added, removed or changed against a published manifest. Empty means equal."""
    want = {f["path"]: f["sha256"] for f in expected.get("files", [])}
    have = {entry.path: entry.sha256 for entry in entries}
    out = [f"missing at this commit: {p}" for p in sorted(set(want) - set(have))]
    out += [f"not in the published manifest: {p}" for p in sorted(set(have) - set(want))]
    out += [f"changed: {p}" for p in sorted(set(want) & set(have)) if want[p] != have[p]]
    return out


def register_rows(commit: str, root: Path = ROOT) -> list[dict[str, str]]:
    """The batch registers as committed at `commit`, templates excluded. The register on disk
    may have moved since; the one the documents were made against is the one at the commit."""
    from eval.sets_io import read_register

    listed = _git(root, "ls-tree", "-r", "-z", "--name-only", commit, "--", REGISTERS)
    names = [
        p
        for p in listed.decode().split("\0")
        if p.endswith(".csv") and "template" not in p and "columns" not in p
    ]
    rows: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory() as folder:
        for name in names:
            copy = Path(folder) / Path(name).name
            copy.write_bytes(blob(commit, name, root))
            rows.extend(read_register(copy))
    return rows


# ----------------------------------------------------------------------------- the household


@dataclass(frozen=True, slots=True)
class Declared:
    name: str
    relation: str
    owner: bool = False
    external: bool = False
    aliases: tuple[str, ...] = field(default_factory=tuple)


def household(path: Path) -> list[Declared]:
    """A household declaration: `{"people": [{"name", "relation", "owner"?, "external"?,
    "aliases"?}]}`. Exactly one owner, whose relation is `self`; nobody else is `self`."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise FreezeRefused(f"{path}: not a readable household declaration ({error})") from error
    people = [
        Declared(
            name=str(p.get("name", "")).strip(),
            relation=str(p.get("relation", "other")),
            owner=bool(p.get("owner", False)),
            external=bool(p.get("external", False)),
            aliases=tuple(str(a).strip() for a in p.get("aliases", []) if str(a).strip()),
        )
        for p in raw.get("people", [])
    ]
    owners = [p for p in people if p.owner]
    if len(owners) != 1:
        raise FreezeRefused(f"{path}: a household has exactly one owner, not {len(owners)}")
    for person in people:
        if not person.name:
            raise FreezeRefused(f"{path}: a person needs a name")
        if person.relation not in RELATIONS:
            raise FreezeRefused(f"{path}: {person.name}: unknown relation {person.relation!r}")
        if (person.relation == "self") != person.owner:
            raise FreezeRefused(f"{path}: {person.name}: only the owner is 'self'")
    names = Counter(alias.casefold() for p in people for alias in (p.name, *p.aliases))
    repeated = sorted(alias for alias, count in names.items() if count > 1)
    if repeated:
        raise FreezeRefused(f"{path}: a name can belong to one person only: {repeated}")
    return people


def apply_household(conn: Any, people: Sequence[Declared]) -> None:
    """Through `core.household`, as the setup screen does: the owner first."""
    from core import household as hh

    for person in sorted(people, key=lambda p: not p.owner):
        hh.add_person(
            conn,
            person.name,
            "other" if person.owner else person.relation,  # type: ignore[arg-type]
            is_owner=person.owner,
            external=person.external,
            aliases=person.aliases,
        )
    conn.commit()


# ------------------------------------------------------------------------- load and verify


def _mime(name: str) -> str:
    return mimetypes.guess_type(name)[0] or "application/pdf"


def load(
    settings: Any, commit: str, entries: Sequence[Entry], root: Path = ROOT
) -> list[dict[str, Any]]:
    """Register and read every `vault` document from the commit's bytes, one at a time."""
    from core.ingest import register as reg
    from core.ingest.pipeline import process
    from core.runtime.db import connect
    from core.runtime.ollama import Ollama

    client = Ollama(settings)
    out: list[dict[str, Any]] = []
    with connect(settings) as conn:
        for entry in entries:
            if entry.role != "vault":
                continue
            payload = blob(commit, entry.path, root)
            row = reg.register_document(
                conn,
                payload=payload,
                mime=_mime(entry.name),
                original_name=entry.name,
                source_channel="freeze",
                synthetic=True,
            )
            conn.commit()
            outcome = process(
                conn,
                client,
                document_id=row.document_id,
                payload=payload,
                mime=_mime(entry.name),
                original_name=entry.name,
            )
            out.append(
                {
                    "path": entry.path,
                    "status": outcome.status,
                    "doc_type": outcome.doc_type,
                    "facts": outcome.facts,
                    "chunks": outcome.chunks,
                    "reason": outcome.reason,
                }
            )
            print(f"  {entry.path:<64} {outcome.status:<12} {outcome.facts:>3} facts", flush=True)
    return out


def verify(settings: Any, entries: Sequence[Entry], rows: list[dict[str, str]]) -> dict[str, Any]:
    """What the vault now holds, checked against the manifest and the committed register."""
    from core.runtime.db import connect
    from eval.run import _facts, _indexed
    from eval.score import extraction_by_type, extraction_f1

    expected = {entry.name: entry.sha256 for entry in entries if entry.role == "vault"}
    with connect(settings) as conn, conn.cursor() as cur:
        cur.execute("SELECT original_name, encode(sha256, 'hex'), status FROM documents")
        stored = cur.fetchall()
        facts, indexed = _facts(conn), _indexed(conn)
    by_name = {name: (digest, status) for name, digest, status in stored}
    mismatched = sorted(
        name for name, digest in expected.items() if by_name.get(name, ("", ""))[0] != digest
    )
    overall = extraction_f1(rows, facts, indexed).get("all")
    return {
        "documents_expected": len(expected),
        "documents_stored": len(stored),
        "status": dict(Counter(status for _, _, status in stored)),
        "hash_mismatches": mismatched,
        "not_in_manifest": sorted(set(by_name) - set(expected)),
        "extraction_f1": None if overall is None else round(overall.f1 or 0.0, 4),
        "extraction": None if overall is None else overall.as_dict(),
        "by_doc_type": {
            s.doc_type: {"documents": s.documents, **s.overall.as_dict()}
            for s in extraction_by_type(rows, facts, indexed)
        },
    }


def report_markdown(result: dict[str, Any]) -> str:
    run, check = result["run"], result.get("verification") or {}
    held = [f["path"] for f in result["manifest"]["files"] if f["role"] == "set_c"]
    quarantined = [d for d in result.get("documents", []) if d["status"] != "indexed"]
    lines = [
        f"# Frozen vault `{run['vault']}` — {run['date'][:10]}",
        "",
        f"Commit `{run['commit']}` · manifest SHA-256 `{result['manifest']['manifest_sha256']}` · "
        f"{len(result['manifest']['files'])} files, {len(held)} held out for Set C.",
        "",
    ]
    if run.get("dry_run"):
        lines += ["Dry run: the manifest only. Nothing was created or read into a database.", ""]
    else:
        lines += [
            "| Check | Result |",
            "|---|---|",
            f"| Documents loaded | {check.get('documents_stored')} of "
            f"{check.get('documents_expected')} |",
            f"| Status | {check.get('status')} |",
            f"| Stored hash differs from the manifest | {check.get('hash_mismatches') or 'none'} |",
            f"| In the vault but not the manifest | {check.get('not_in_manifest') or 'none'} |",
            f"| Extraction F1 against the register at this commit | {check.get('extraction_f1')} |",
            "",
        ]
        if quarantined:
            lines += ["Not indexed:", ""]
            lines += [f"- `{d['path']}`: {d['status']} — {d['reason']}" for d in quarantined]
            lines += [""]
    lines += ["Held out under the Set C protocol (`eval.setc` adds them to a copy):", ""]
    lines += [f"- `{path}`" for path in held] or ["- none"]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------------------------- main


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--commit", required=True, help="the frozen commit (any ref; recorded in full)"
    )
    parser.add_argument(
        "--household", type=Path, required=True, help="household declaration (JSON)"
    )
    parser.add_argument("--expect-manifest", type=Path, help="refuse unless the commit matches it")
    parser.add_argument("--vault", default=VAULT, help=f"database name (default {VAULT})")
    parser.add_argument("--replace", action="store_true", help="drop the vault if it exists")
    parser.add_argument("--dry-run", action="store_true", help="manifest and plan only")
    parser.add_argument("--label", default="frozen-vault")
    parser.add_argument("--out", type=Path, default=ROOT / "eval" / "results")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    from core.runtime.settings import ConfigurationError, Settings
    from eval.holdout import apply_schema, create_vault, vault_url

    try:
        commit = resolve(args.commit)
        people = household(args.household)
        entries = corpus_files(commit)
        if not entries:
            raise FreezeRefused(f"No documents under {BATCHES} at {commit}.")
        if args.expect_manifest:
            expected = json.loads(args.expect_manifest.read_text(encoding="utf-8"))
            diff = differences(expected, entries)
            if diff:
                raise FreezeRefused(
                    "The commit does not match the published manifest:\n  " + "\n  ".join(diff)
                )
        settings = Settings.load(ROOT)
    except (FreezeRefused, ConfigurationError, OSError, json.JSONDecodeError) as error:
        print(error)
        return 2

    stem = f"{date.today().isoformat()}-{args.label}"
    target = args.out / f"{stem}.json"
    if target.exists():
        print(f"{target} already exists and results are append-only. Choose another --label.")
        return 2
    roles = Counter(entry.role for entry in entries)
    print(f"commit {commit}: {roles['vault']} document(s) to load, {roles['set_c']} held for Set C")
    result: dict[str, Any] = {
        "run": {
            "date": datetime.now(UTC).isoformat(timespec="seconds"),
            "kind": "frozen-vault",
            "label": args.label,
            "commit": commit,
            "vault": args.vault,
            "dry_run": args.dry_run,
            "household": str(args.household),
            "people": len(people),
            "generator": settings.generation_model,
            "embedder": settings.embedding_model,
        },
        "manifest": manifest(commit, entries),
    }

    if not args.dry_run:
        import psycopg

        admin = vault_url(settings.database_url, "postgres")
        url = vault_url(settings.database_url, args.vault)
        with psycopg.connect(admin, autocommit=True) as conn:
            exists = conn.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s", (args.vault,)
            ).fetchone()
        if exists and not args.replace:
            print(
                f"Vault {args.vault} already exists. It may be Run 3's; pass --replace to rebuild."
            )
            return 2
        print(f"vault {args.vault} (the development vault is not opened)")
        create_vault(admin, args.vault)
        apply_schema(url)
        isolated = Settings.load(ROOT, {**os.environ, "DATABASE_URL": url})
        from core import registry
        from core.runtime.db import connect

        with connect(isolated) as conn:
            registry.install(conn)
            apply_household(conn, people)
        result["documents"] = load(isolated, commit, entries)
        result["verification"] = verify(isolated, entries, register_rows(commit))

    args.out.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (args.out / f"{stem}.md").write_text(report_markdown(result), encoding="utf-8")
    print(f"wrote {target}")
    if not args.dry_run:
        print(f"Score it with: uv run python -m eval.run --vault {args.vault} --corpus all")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
