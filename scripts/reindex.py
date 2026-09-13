"""Rebuild every indexed document's chunks and vectors, keeping its facts.

    uv run python scripts/reindex.py                    # every indexed document
    uv run python scripts/reindex.py --only b1-0031.pdf # one of them

Run it once after a change to chunking or embedding, before asking questions: a vault embedded
the old way is not searchable the new way. It reads each file back out of the inbox by digest,
exactly as the quarantine retry does, so a document whose file has gone is skipped and named.
Facts, obligations and corrections are not touched. See `core/ingest/reindex.py`.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOISY = ("httpx", "docling", "RapidOCR", "huggingface_hub", "filelock", "transformers")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="the original filename of one document to rebuild")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for name in NOISY:
        logging.getLogger(name).setLevel(logging.WARNING)

    from core.ingest.reindex import ReindexFailed, indexed, reindex_document
    from core.ingest.source import SourceMissing, bytes_for, digest_of_document
    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.ollama import Ollama
    from core.runtime.settings import ConfigurationError, Settings

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    folder = Path(settings.watch_folder)
    client = Ollama(settings, timeout=600.0)
    failures = 0
    try:
        with connect(settings) as conn:
            documents = [
                document
                for document in indexed(conn)
                if args.only is None or document.original_name == args.only
            ]
            if not documents:
                print("No indexed document matches." if args.only else "Nothing is indexed yet.")
                return 1 if args.only else 0
            for document in documents:
                started = time.monotonic()
                digest = digest_of_document(conn, document.document_id)
                try:
                    if digest is None:
                        raise SourceMissing("the document has no digest")
                    payload = bytes_for(digest, folder)
                    count = reindex_document(conn, client, document, payload)
                except (SourceMissing, ReindexFailed) as error:
                    failures += 1
                    print(f"  {document.original_name}: kept as it was — {error}")
                    continue
                print(
                    f"  {document.original_name}: {count} chunk(s) "
                    f"in {time.monotonic() - started:.0f}s"
                )
    except DatabaseUnavailable as error:
        print(str(error))
        return 2
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
