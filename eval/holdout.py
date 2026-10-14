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
merge. Retrieval and generation metrics need questions about these documents; generate them
from the holdout register with `eval.generate --out` once it exists, then run `eval.run`
against the same vault.

**This never reads `corpus/holdout/` by default.** That folder is gitignored and may hold the
real documents on one machine; the path is given explicitly so that running this is a
deliberate act, and `--documents` is refused if it points inside the repository, where the
watcher would see it.
"""

from __future__ import annotations

import argparse
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


def synthetic_baseline(results: Path) -> float | None:
    """The newest committed synthetic extraction F1, so the gap is computed rather than typed."""
    best: tuple[str, float] | None = None
    for path in sorted(results.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        value = (data.get("metrics") or {}).get("extraction_f1")
        when = (data.get("run") or {}).get("date", "")
        if isinstance(value, int | float) and (best is None or when > best[0]):
            best = (when, float(value))
    return None if best is None else best[1]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--documents", type=Path, required=True, help="folder, outside this repo")
    parser.add_argument("--register", type=Path, required=True, help="the holdout's register CSV")
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
        settings = Settings.load(ROOT)
    except (HoldoutRefused, ConfigurationError) as error:
        print(error)
        return 2

    admin = vault_url(settings.database_url, "postgres")
    holdout = vault_url(settings.database_url, args.vault)
    print(f"{len(found)} document(s) in {args.documents}")
    print(f"vault {args.vault} (the development vault is not opened)")
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

    baseline = synthetic_baseline(ROOT / "eval" / "results")
    real = measured["extraction_f1"]
    gap = None if baseline is None or real is None else round(baseline - real, 4)
    result = {
        "run": {
            "date": datetime.now(UTC).isoformat(timespec="seconds"),
            "label": args.label,
            "kind": "holdout",
            "documents": len(found),
            "vault": args.vault,
            "generator": settings.generation_model,
            "embedder": settings.embedding_model,
        },
        "holdout": measured,
        "synthetic_extraction_f1": baseline,
        "gap": gap,
        "documents": [{"name": n, "status": s, "facts": f} for n, s, f in read],
    }
    args.out.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print()
    print(f"extraction F1 on real documents : {real}")
    print(f"extraction F1 on synthetic      : {baseline}")
    print(f"the gap                         : {gap}  <- this is the result")
    print(f"\nwrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
