"""Show the quarantine queue, and run the vision second pass over it.

    uv run python scripts/quarantine.py               # what needs your eyes, and why
    uv run python scripts/quarantine.py --retry       # send the page images to the model

The retry reads the original bytes back out of the watched folder, matched by SHA-256. v1 keeps
the inbox as the document store — nothing is copied into the database — so a document whose file
has been moved or deleted cannot be retried, and this script says so rather than pretending.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NOISY = ("httpx", "docling", "RapidOCR", "huggingface_hub", "filelock")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retry", action="store_true", help="run the vision pass over the queue")
    parser.add_argument("--limit", type=int, default=25)
    args = parser.parse_args(argv)
    if args.limit < 1:
        parser.error("limit must be at least 1")

    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for name in NOISY:
        logging.getLogger(name).setLevel(logging.WARNING)

    from core.ingest.quarantine import Recovery, queue, recovery_rate, retry
    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.ollama import Ollama
    from core.runtime.settings import ConfigurationError, Settings

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    folder = Path(settings.watch_folder)
    try:
        with connect(settings) as conn:
            waiting = queue(conn, args.limit)
            if not waiting:
                print("Nothing is in quarantine.")
                return 0

            print(f"{len(waiting)} document(s) need your eyes:")
            for document in waiting:
                print(f"  {document.original_name} [{document.mime}] — {document.reason}")
            if not args.retry:
                print("\nRun with --retry to send the page images to the vision-language model.")
                return 0

            print(f"\nRetrying against the files still in {folder}:")
            recoveries: list[Recovery] = []
            client = Ollama(settings)
            for document in waiting:
                payload = _payload_for(conn, document.document_id, folder)
                if payload is None:
                    print(
                        f"  {document.original_name}: the original file is no longer in the inbox"
                    )
                    continue
                recovery = retry(
                    conn,
                    client,
                    document_id=document.document_id,
                    payload=payload,
                    mime=document.mime,
                    original_name=document.original_name,
                )
                recoveries.append(recovery)
                if recovery.recovered:
                    print(
                        f"  {document.original_name}: recovered, "
                        f"{recovery.facts} cited fact(s) from {recovery.pages_read} page(s)"
                    )
                else:
                    print(f"  {document.original_name}: still quarantined — {recovery.reason}")
            print(f"\n{recovery_rate(recoveries)}")
            return 0
    except DatabaseUnavailable as error:
        print(str(error))
        return 2


def _payload_for(conn: Any, document_id: Any, folder: Path) -> bytes | None:
    """The document's bytes, found by digest. `core/ingest/source.py` is the one implementation;
    the worker's retry task uses the same one."""
    from core.ingest.source import SourceMissing, bytes_for, digest_of_document

    digest = digest_of_document(conn, document_id)
    if digest is None:
        return None
    try:
        return bytes_for(digest, folder)
    except SourceMissing:
        return None


if __name__ == "__main__":
    raise SystemExit(main())
