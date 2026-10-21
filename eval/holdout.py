"""Score the real-document holdout in a vault of its own, so it is never tuned on.

    uv run python -m eval.holdout --documents ~/holdout --register ~/holdout/register.csv
    uv run python -m eval.holdout --documents ~/holdout --register … --keep  # keep the vault

`eval/README.md` calls this the honesty check: synthetic documents are cleaner and more
consistent than real ones, so a score measured only on them overstates the system. The holdout
is 40 real documents from team members, redacted, **never used for tuning**, scored once in
week 8 — and the number that matters is not the holdout score but the *gap* between it and the
synthetic one.

"Never used for tuning" was a sentence in `docs/RUNNING.md` that nothing enforced, and the
documented way to load a batch would have broken it on the first try:

    make corpus-load BATCH=<batch>   # copies into inbox/
    make dev                         # the watcher registers and reads whatever landed there

One `corpus-load` aimed at the holdout and those documents are in the development vault for
good — their chunks in the same index every retrieval change is measured against, recoverable
only by rebuilding the database. So this module does not use `inbox/` and does not touch the
development vault at all:

1. a **separate Postgres database** on the same local server, created here and dropped at the
   end unless `--keep`;
2. the schema applied from `db/migrations/`, read and never modified;
3. each document ingested **directly** through `core.ingest.pipeline.process`, so nothing is
   ever written into the watched folder;
4. extraction scored against the holdout's own register, beside the synthetic baseline;
5. the vault dropped.

Why extraction and not the whole metric list: extraction is the one metric that needs no
golden questions — every value is checked against the register — so it can be compared between
a synthetic corpus and a real one with nothing else in place. It is also the metric most
sensitive to the thing being tested, since a real document is messier to read than a mail
merge. Retrieval and generation metrics need questions about these documents, and there is no safe
way to run them yet: `eval.generate` reads only the registers in `corpus/register/` and
`eval.run` only the questions in `eval/sets/`, and holdout questions must never be written
there, since their expected answers are real people's values (`eval/README.md`, "Running the
holdout").

**This never reads `corpus/holdout/` by default.** That folder is gitignored and may hold the
real documents on one machine; the path is given explicitly so that running this is a
deliberate act, and `--documents` is refused if it points inside the repository, where the
watcher would see it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections.abc import Sequence
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT_SUFFIXES = frozenset({".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp"})
VAULT = "parrot_holdout"
# The synthetic side of the gap: Run 3, the frozen corpus every Set A question was answerable
# from. Named, not found. Until 21 October this was "the newest committed result with an
# extraction F1", and a rehearsal that day picked a reranker experiment from that morning: the
# right number by coincidence, and the next commit could have changed it without anyone seeing.
BASELINE = ROOT / "eval" / "results" / "2026-10-19-run3.json"


class HoldoutRefused(RuntimeError):
    """Safe to show. Raised before anything is created, read or written."""


def vault_url(database_url: str, name: str) -> str:
    """The same local server, a different database. Nothing else about the URL changes."""
    parts = urlsplit(database_url)
    return urlunsplit((parts.scheme, parts.netloc, f"/{name}", parts.query, parts.fragment))


def check_outside_the_repository(documents: Path) -> None:
    """Refuse a holdout folder the watcher could see.

    `inbox/` is the watched folder and `corpus/batches/` is copied into it by
    `scripts/load_corpus.py`. A holdout under either is one `make dev` away from being in the
    development vault, which is the exact thing this module exists to prevent — and it cannot
    be undone, because tuning against a document is not an event you can roll back.
    """
    resolved = documents.resolve()
    if resolved.is_relative_to(ROOT):
        raise HoldoutRefused(
            f"{resolved} is inside the repository. The holdout must live outside it: the watcher "
            f"reads {ROOT / 'inbox'}, and a document the development vault has seen is no longer "
            "a holdout. Keep it somewhere the repository cannot reach and pass that path."
        )


def documents_in(folder: Path) -> list[Path]:
    if not folder.is_dir():
        raise HoldoutRefused(f"{folder} is not a folder.")
    found = sorted(
        path
        for path in folder.rglob("*")
        if path.is_file()
        and path.suffix.lower() in DOCUMENT_SUFFIXES
        and not path.name.startswith(".")
    )
    if not found:
        raise HoldoutRefused(f"No documents under {folder}. Expected PDFs or images.")
    return found


def migrations() -> list[Path]:
    """The schema, read in order. Never edited here — `db/migrations/` is a reviewed PR of its
    own (AGENTS.md rule 4), and this only applies what is already there."""
    return sorted((ROOT / "db" / "migrations").glob("*.sql"))


def create_vault(admin_url: str, name: str) -> None:
    """Create the holdout database, dropping any left behind by an interrupted run."""
    import psycopg

    with psycopg.connect(admin_url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute(f'DROP DATABASE IF EXISTS "{name}"')
        cur.execute(f'CREATE DATABASE "{name}"')


def drop_vault(admin_url: str, name: str) -> None:
    import psycopg

    with psycopg.connect(admin_url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')


def apply_schema(url: str) -> None:
    import psycopg

    with psycopg.connect(url, autocommit=True) as conn, conn.cursor() as cur:
        for path in migrations():
            cur.execute(path.read_text(encoding="utf-8"))


def ingest(settings: Any, documents: Sequence[Path]) -> list[tuple[str, str, int]]:
    """Read each document straight into the holdout vault. Returns (name, status, facts).

    Deliberately not through `inbox/`: the watched folder belongs to the development vault, and
    a holdout document that lands there has already lost the property that makes it a holdout.
    """
    import mimetypes

    from core.ingest import register as reg
    from core.ingest.pipeline import process
    from core.runtime.db import connect
    from core.runtime.ollama import Ollama

    client = Ollama(settings)
    out: list[tuple[str, str, int]] = []
    with connect(settings) as conn:
        for path in documents:
            payload = path.read_bytes()
            mime = mimetypes.guess_type(path.name)[0] or "application/pdf"
            row = reg.register_document(
                conn,
                payload=payload,
                mime=mime,
                original_name=path.name,
                source_channel="holdout",
                synthetic=False,
            )
            conn.commit()
            outcome = process(
                conn,
                client,
                document_id=row.document_id,
                payload=payload,
                mime=mime,
                original_name=path.name,
            )
            out.append((path.name, outcome.status, outcome.facts))
            print(f"  {path.name:<44} {outcome.status:<12} {outcome.facts:>3} facts")
    return out


def score(settings: Any, register_path: Path) -> dict[str, Any]:
    """Extraction against the holdout's own register, in the holdout's own vault."""
    from core.runtime.db import connect
    from eval.run import _facts, _indexed
    from eval.score import extraction_by_type, extraction_f1, without_ground_truth
    from eval.sets_io import read_register

    rows = read_register(register_path)
    with connect(settings) as conn:
        facts, indexed = _facts(conn), _indexed(conn)
    overall = extraction_f1(rows, facts, indexed).get("all")
    return {
        "register_rows": len(rows),
        "indexed": len(indexed),
        "extraction_f1": None if overall is None else round(overall.f1 or 0.0, 4),
        "extraction": None if overall is None else overall.as_dict(),
        "by_doc_type": {
            s.doc_type: {"documents": s.documents, **s.overall.as_dict()}
            for s in extraction_by_type(rows, facts, indexed)
        },
        "no_ground_truth": without_ground_truth(rows, indexed),
    }


def synthetic_baseline(result: Path) -> dict[str, Any] | None:
    """The synthetic side of the gap, read from one named result file so it is computed rather
    than typed, and so the file it came from is recorded beside it. `None` if the file has no
    extraction F1."""
    try:
        data = json.loads(result.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    value = (data.get("metrics") or {}).get("extraction_f1")
    if not isinstance(value, int | float):
        return None
    by_type = (data.get("also") or {}).get("extraction_by_doc_type") or {}
    return {
        "file": result.name,
        "git_sha": (data.get("run") or {}).get("git_sha"),
        "extraction_f1": float(value),
        "by_doc_type": {
            kind: float(scores["f1"])
            for kind, scores in by_type.items()
            if isinstance(scores, dict) and isinstance(scores.get("f1"), int | float)
        },
    }


def gaps_by_type(
    holdout: dict[str, dict[str, Any]], synthetic: dict[str, float]
) -> dict[str, dict[str, Any]]:
    """The gap for each document type the holdout has, beside how many documents it rests on.

    The overall gap compares a few real documents of a few types against a synthetic average
    over every type, so the mix alone moves it: six *synthetic* stand-ins scored 0.919 against
    Run 3's 0.949 in the rehearsal on 21 October, a "gap" of 0.03 with nothing real in it. Type
    against type is the comparison that can be read; a type with one document is a sample of one.
    """
    out: dict[str, dict[str, Any]] = {}
    for kind, scores in sorted(holdout.items()):
        real = scores.get("f1")
        other = synthetic.get(kind)
        out[kind] = {
            "documents": scores.get("documents"),
            "holdout_f1": None if real is None else round(real, 4),
            "synthetic_f1": None if other is None else round(other, 4),
            "gap": None if real is None or other is None else round(other - real, 4),
        }
    return out


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--documents", type=Path, required=True, help="folder, outside this repo")
    parser.add_argument("--register", type=Path, required=True, help="the holdout's register CSV")
    parser.add_argument(
        "--baseline",
        type=Path,
        default=BASELINE,
        help=f"the synthetic result to compare with (default {BASELINE.name})",
    )
    parser.add_argument("--out", type=Path, default=ROOT / "eval" / "results")
    parser.add_argument("--label", default="holdout")
    parser.add_argument("--vault", default=VAULT, help=f"database name (default {VAULT})")
    parser.add_argument("--keep", action="store_true", help="do not drop the vault at the end")
    parser.add_argument("--dry-run", action="store_true", help="check only; create nothing")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    from core.runtime.settings import ConfigurationError, Settings

    try:
        check_outside_the_repository(args.documents)
        found = documents_in(args.documents)
        if not args.register.is_file():
            raise HoldoutRefused(f"{args.register} is not a file.")
        baseline = synthetic_baseline(args.baseline)
        if baseline is None:
            raise HoldoutRefused(f"{args.baseline} has no extraction F1 to compare with.")
        settings = Settings.load(ROOT)
    except (HoldoutRefused, ConfigurationError) as error:
        print(error)
        return 2

    admin = vault_url(settings.database_url, "postgres")
    holdout = vault_url(settings.database_url, args.vault)
    print(f"{len(found)} document(s) in {args.documents}")
    print(f"vault {args.vault} (the development vault is not opened)")
    print(f"compared with {baseline['file']} (extraction F1 {baseline['extraction_f1']})")
    if args.dry_run:
        print("dry run: nothing created, nothing read.")
        return 0

    isolated = Settings.load(ROOT, {**os.environ, "DATABASE_URL": holdout})
    target = args.out / f"{date.today().isoformat()}-{args.label}.json"
    if target.exists():
        print(f"{target} already exists and results are append-only. Choose another --label.")
        return 2

    try:
        create_vault(admin, args.vault)
        apply_schema(holdout)
        read = ingest(isolated, found)
        measured = score(isolated, args.register)
    finally:
        if args.keep:
            print(f'vault {args.vault} kept. Drop it with: DROP DATABASE "{args.vault}";')
        else:
            drop_vault(admin, args.vault)

    from eval.run import _git_sha

    real = measured["extraction_f1"]
    synthetic = baseline["extraction_f1"]
    gap = None if real is None else round(synthetic - real, 4)
    by_type = gaps_by_type(measured["by_doc_type"], baseline["by_doc_type"])
    result = {
        "run": {
            "date": datetime.now(UTC).isoformat(timespec="seconds"),
            "label": args.label,
            "kind": "holdout",
            "documents": len(found),
            "vault": args.vault,
            "generator": settings.generation_model,
            "embedder": settings.embedding_model,
            "git_sha": _git_sha(),
            # The register's digest, never its contents: it holds real people's values.
            "register_sha256": hashlib.sha256(args.register.read_bytes()).hexdigest(),
            "baseline_file": baseline["file"],
            "baseline_git_sha": baseline["git_sha"],
        },
        "holdout": measured,
        "synthetic_extraction_f1": synthetic,
        "gap": gap,
        "gap_by_doc_type": by_type,
        "documents": [{"name": n, "status": s, "facts": f} for n, s, f in read],
    }
    args.out.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print()
    print(f"extraction F1 on real documents : {real}")
    print(f"extraction F1 on synthetic      : {synthetic}  ({baseline['file']})")
    print(f"the gap                         : {gap}  <- this is the result")
    print("\nby document type (read these; the overall gap mixes types):")
    for kind, row in by_type.items():
        print(
            f"  {kind:<30} {row['documents']:>2} doc(s)  holdout {row['holdout_f1']}  "
            f"synthetic {row['synthetic_f1']}  gap {row['gap']}"
        )
    print(f"\nwrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
