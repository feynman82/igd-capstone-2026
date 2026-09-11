"""The one interface every capture channel satisfies.

    receive(payload, mime, sender, ts) -> IngestJob

`original_name` is keyword-only rather than folded into `sender`: a channel knows both who
sent a document and what the file was called, and conflating the two would lose the filename
that `documents.original_name` is declared NOT NULL to hold. Nothing in `core/contracts.py`
is touched by this interface — a capture adapter is transport, not a contract.
"""

from __future__ import annotations

import hashlib
import mimetypes
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable
from uuid import UUID

# Magic bytes for the formats a household actually photographs or downloads. Filenames lie;
# a suffix is a hint and these are the confirmation.
_MAGIC: tuple[tuple[bytes, str], ...] = (
    (b"%PDF-", "application/pdf"),
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"II*\x00", "image/tiff"),
    (b"MM\x00*", "image/tiff"),
    (b"PK\x03\x04", "application/zip"),  # also docx/xlsx; Docling sorts that out later
)
FALLBACK_MIME = "application/octet-stream"


def sha256(payload: bytes) -> bytes:
    """The idempotency key for the whole platform. Bytes, not hex: `documents.sha256` is bytea."""
    return hashlib.sha256(payload).digest()


def sniff_mime(payload: bytes, original_name: str) -> str:
    """Magic bytes first, filename suffix second, `application/octet-stream` last.

    A phone that names every photograph `image.jpg` and a scanner that names every scan
    `scan.pdf` are both common, and a renamed file must not change how it is parsed.
    """
    head = payload[:16]
    for signature, mime in _MAGIC:
        if not head.startswith(signature):
            continue
        if mime != "application/zip":
            return mime
        break  # a zip container: docx, xlsx and odt all look identical here
    guessed, _ = mimetypes.guess_type(original_name)
    return guessed or FALLBACK_MIME


@dataclass(frozen=True, slots=True)
class IngestJob:
    """What a capture returns: a registered document, and whether we had seen it before.

    `already_registered` is the duplicate answer. It is deliberately not an error — the same
    payslip photographed twice is a person being careful, not a fault, and the correct
    response is to say "already filed" rather than to file it again.
    """

    document_id: UUID
    sha256: bytes
    source_channel: str
    original_name: str
    mime: str
    received_at: datetime
    ingested_at: datetime
    already_registered: bool

    @property
    def digest_hex(self) -> str:
        return self.sha256.hex()


@runtime_checkable
class CaptureAdapter(Protocol):
    """Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call."""

    channel: str

    def receive(
        self,
        payload: bytes,
        mime: str,
        sender: str,
        ts: datetime,
        *,
        original_name: str,
    ) -> IngestJob: ...
