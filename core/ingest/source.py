"""Find the bytes behind a registered document again.

v1 keeps the inbox as the document store — nothing is copied into the database — so a worker
handed a `document_id` has to go back to the file. It does it by digest rather than by path,
because a path is a guess the moment somebody tidies their folder, while the SHA-256 is the
thing the `documents` row is keyed on: whatever file in the inbox hashes to it *is* the
document, under whatever name it now has.

This is what `scripts/quarantine.py` has always done for the retry queue. Having one
implementation is what stops the queue and the worker disagreeing about where a document is.

When nothing in the folder hashes to it the caller is told, and says so, rather than reading
the wrong file. Hashing the inbox on every task is a few milliseconds against eight seconds of
parsing, for a folder that holds a household's week.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from core.adapters.base import sha256

log = logging.getLogger(__name__)

DIGEST_OF_DOCUMENT = "SELECT sha256 FROM documents WHERE id = %(document_id)s"


class SourceMissing(LookupError):
    """Safe to show: the bytes for this document are no longer anywhere we look."""


def index_folder(folder: Path) -> dict[bytes, Path]:
    """SHA-256 of every file sitting in the watched folder. The document row holds the same key.

    The first path wins, so a file copied under two names resolves to the one sorted first
    rather than to whichever the filesystem happened to list first.
    """
    found: dict[bytes, Path] = {}
    if not folder.is_dir():
        return found
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        try:
            found.setdefault(sha256(path.read_bytes()), path)
        except OSError:
            continue
    return found


def digest_of_document(conn: Any, document_id: Any) -> bytes | None:
    with conn.cursor() as cur:
        cur.execute(DIGEST_OF_DOCUMENT, {"document_id": document_id})
        row = cur.fetchone()
    return None if row is None else bytes(row[0])


def bytes_for(digest: bytes, folder: Path) -> bytes:
    """The payload for `digest`, found by hashing what is in the watched folder."""
    found = index_folder(folder).get(digest)
    if found is None:
        raise SourceMissing("the original file is no longer in the inbox")
    return found.read_bytes()
