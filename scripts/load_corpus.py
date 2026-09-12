"""Load a handed-over corpus batch into this computer's database.

    uv run python scripts/load_corpus.py --batch batch1
    uv run python scripts/load_corpus.py --batch batch1 --dry-run
    make corpus-load BATCH=batch1

**The database is a derived artifact.** Nobody ships one. Five people each run their own
Postgres, and what travels between them is the corpus batch plus the register that describes
it — so this script is the step that turns one into the other. Run it and your `documents`,
`chunks`, `facts` and `obligations` are rebuilt from the same inputs as everybody else's.

It copies the batch into the watched folder rather than reading it in place, because v1 keeps
the inbox as the document store: a fact cites a document, and a document is found again by
hashing the inbox. A batch left in `corpus/batches/` would produce facts whose source
disappears the moment the folder is cleaned.

Nothing here generates a document. `corpus/` holds the register and its validator, and the
documents are authored by Lane E — that is rule "never write code that generates corpus
documents" in AGENTS.md, and this script only moves and registers what it was handed.

What it does NOT do is decide whether the batch is any good. Run the validator first:

    uv run python -m corpus.validate corpus/register/batch1.csv
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCHES = ROOT / "corpus" / "batches"
NOISY = ("httpx", "docling", "RapidOCR", "huggingface_hub", "filelock")

# What a household document arrives as. Anything else in the batch folder is a note, a
# checksum file or an editor's leftovers, and is skipped rather than registered.
DOCUMENT_SUFFIXES = frozenset({".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp"})


def documents_in(batch: Path) -> list[Path]:
    """Every document in the batch, in a stable order, recursing into tier subfolders."""
    return sorted(
        path
        for path in batch.rglob("*")
        if path.is_file() and path.suffix.lower() in DOCUMENT_SUFFIXES
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", required=True, help="a folder name under corpus/batches/")
    parser.add_argument(
        "--dry-run", action="store_true", help="list what would be loaded, and load nothing"
    )
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for name in NOISY:
        logging.getLogger(name).setLevel(logging.WARNING)

    batch = (BATCHES / args.batch).resolve()
    if not str(batch).startswith(str(BATCHES.resolve())):
        print("--batch names a folder under corpus/batches/, not a path.")
        return 2
    if not batch.is_dir():
        print(
            f"There is no batch at corpus/batches/{args.batch}.\n"
            "Corpus batches are not in git — they are handed over by Lane E. "
            "See docs/RUNNING.md, 'Moving a corpus between machines'."
        )
        return 2

    found = documents_in(batch)
    if not found:
        print(f"corpus/batches/{args.batch} holds no documents.")
        return 2

    from core.runtime.settings import ConfigurationError, Settings

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    folder = Path(settings.watch_folder)
    print(f"{len(found)} document(s) in corpus/batches/{args.batch}")
    if args.dry_run:
        for path in found:
            print(f"  would copy {path.relative_to(batch)} -> {folder.name}/")
        print("\n(dry run: nothing was copied and nothing was registered)")
        return 0

    folder.mkdir(parents=True, exist_ok=True)
    copied = 0
    for path in found:
        target = folder / path.name
        if target.exists() and target.stat().st_size == path.stat().st_size:
            continue  # already here; the SHA-256 upsert would make this a no-op anyway
        shutil.copy2(path, target)
        copied += 1
    print(f"copied {copied} new document(s) into {folder}")

    print(
        "\nStart Parrot and the watcher will register and read them:\n"
        "    make dev          (or double-click START.cmd on Windows)\n\n"
        "Re-reading the same bytes updates in place — documents.sha256 is unique — so "
        "loading a batch twice does not duplicate anything."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
