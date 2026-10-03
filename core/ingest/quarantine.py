"""The second stage of quarantine: the page image, read by the vision-language model.

The first stage is a parser recovering text. When it fails — a faint scan, a photograph at an
angle, a layout the parser cannot follow — there is still a document there, and a 4B
vision-language generator can look at the pixels. Docling is not replaced: it stays faster,
cheaper and better on digital PDFs. This is what happens when it loses.

The number this module exists to produce is the **recovery rate**: of the documents that
quarantined, how many the image pass rescued. That is a finding for the report, so it is
measured rather than asserted, and it is measured per failure reason so it can be said *which*
kind of failure the image pass fixes.

Nothing here lowers a standard to get a document through. A recovered document is still held to
the pack's schema and still has every field attributed to a page; a document that cannot meet
that stays in quarantine and is surfaced as "needs your eyes".

One honest limitation, which belongs in the report rather than in a comment nobody reads: on
this path a page is the model's own transcription, so attributing a field to a page checks
the model against itself. A misread character survives that check - an observed run turned
"Harborline" into "Harbordine" and stored it as a cited fact. The text path does not have this
problem, because the parser and the extractor are different components. Scoring the image path
against Desmond's register, not against its own output, is the only thing that measures it.
"""

from __future__ import annotations

import base64
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.ingest import sql
from core.ingest.parse import ParsedDocument, ParsedPage
from core.ingest.pipeline import read_and_commit
from core.ingest.source import index_folder
from core.pages import PageUnavailable, RendererUnavailable, page_count, render_page
from core.runtime.ollama import ModelUnavailable, Ollama

log = logging.getLogger(__name__)

MAX_IMAGE_PAGES = 4  # a household document; beyond this the context cost is not worth it

READ_SYSTEM = (
    "You are looking at a photograph or scan of one household document. You transcribe what is "
    "printed, including tables, in reading order. You never complete a value you cannot see. "
    "Where a character is illegible you write a single question mark in its place."
)

_TRANSCRIBE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "pages": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "page": {"type": "integer", "minimum": 1},
                    "text": {"type": "string"},
                },
                "required": ["page", "text"],
            },
        }
    },
    "required": ["pages"],
}


@dataclass(frozen=True, slots=True)
class QuarantinedDocument:
    document_id: Any
    original_name: str
    mime: str
    reason: str | None
    pages: int | None


@dataclass(frozen=True, slots=True)
class Recovery:
    document_id: Any
    recovered: bool
    reason: str | None
    facts: int = 0
    chunks: int = 0
    pages_read: int = 0


def queue(conn: Any, limit: int = 50) -> list[QuarantinedDocument]:
    """What is waiting for a person's eyes, oldest first."""
    with conn.cursor() as cur:
        cur.execute(sql.SELECT_QUARANTINED, {"limit": limit})
        rows = cur.fetchall()
    return [QuarantinedDocument(*row) for row in rows]


def blocked_reasons(
    conn: Any, documents: list[QuarantinedDocument], folder: Path
) -> dict[Any, str | None]:
    """Per document: `None` when the image pass can run, or the sentence saying why it cannot.

    v1 keeps the inbox as the document store, so a document whose file has been moved or
    deleted cannot be retried. A screen that offers a Retry button which is certain to fail is
    worse than one that explains itself, so the folder is hashed once — not once per row — and
    each document is told apart from the others by the digest it was registered under.
    """
    if not documents:
        return {}
    ids = [document.document_id for document in documents]
    with conn.cursor() as cur:
        cur.execute(sql.SELECT_DIGESTS, {"document_ids": ids})
        digests = {document_id: bytes(digest) for document_id, digest in cur.fetchall()}
    available = set(index_folder(folder))
    blocked: dict[Any, str | None] = {}
    for document in documents:
        digest = digests.get(document.document_id)
        if digest is None or digest not in available:
            blocked[document.document_id] = "the original file is no longer in the inbox"
        else:
            blocked[document.document_id] = None
    return blocked


class StillInInbox(ValueError):
    """Safe to show. Forgetting a document whose file is still there would not last."""


def forget(conn: Any, document_id: Any, folder: Path) -> str | None:
    """Remove a quarantined document from Parrot's memory. Its name, or `None` if there is no such
    quarantined document.

    Refused while the file is still in the inbox. Capture registers any file whose digest it has
    not seen, so a forgotten document that is still there is registered and read again within a
    minute — a button that appears to work and does not. On 13 September the case that asked for
    this was the other one: `b1-0032.pdf` had been deleted from the inbox, its row stayed
    quarantined, and Today said it needed attention with nothing a person could do about it.
    """
    waiting = [item for item in queue(conn, limit=200) if str(item.document_id) == str(document_id)]
    if not waiting:
        return None
    if blocked_reasons(conn, waiting, folder).get(waiting[0].document_id) is None:
        raise StillInInbox(
            "The file is still in the inbox, so Parrot would read it again. Take it out of the "
            "inbox first, or read it again instead."
        )
    with conn.cursor() as cur:
        cur.execute(sql.DELETE_QUARANTINED, {"document_id": str(document_id)})
        row = cur.fetchone()
    conn.commit()
    log.info("forgot quarantined document %s", document_id)
    return str(row[0]) if row else None


def page_images(payload: bytes, mime: str) -> list[str]:
    """Base64 page images, in page order. Empty when this document cannot be rendered.

    Capped at `MAX_IMAGE_PAGES`, which is a context-budget decision belonging to this pass and
    to nothing else — `core.pages` will happily draw page nine for a person who clicked a
    citation. The drawing itself is `core.pages`' job so that the page this model reads and the
    page the interface shows are the same page.

    The names are imported rather than the module, because `transcribe` below already has a
    local called `pages` and one of them would have shadowed the other.
    """
    try:
        total = page_count(payload, mime)
    except RendererUnavailable as error:
        log.warning("%s", error)
        return []

    images: list[str] = []
    for number in range(1, min(total, MAX_IMAGE_PAGES) + 1):
        try:
            drawn, _ = render_page(payload, mime, number)
        except PageUnavailable as error:
            log.info("stopping at page %d: %s", number, error)
            break
        images.append(base64.b64encode(drawn).decode("ascii"))
    return images


def transcribe(client: Ollama, images: list[str]) -> ParsedDocument:
    """Ask the vision-language model to read the pages. One request per page, so a page that
    defeats it does not cost the pages that did not."""
    pages: list[ParsedPage] = []
    for number, image in enumerate(images, start=1):
        try:
            reply = client.constrained(
                READ_SYSTEM,
                f"Transcribe page {number} of this document.",
                _TRANSCRIBE_SCHEMA,
                images=[image],
            ).json()
        except ModelUnavailable as error:
            log.info("the image pass could not read page %d: %s", number, error)
            continue
        for item in reply.get("pages") or []:
            text = str(item.get("text", "")).strip()
            if text:
                pages.append(ParsedPage(number, text))
                break
    if not pages:
        return ParsedDocument(False, "vision", reason="the image pass recovered no text")
    return ParsedDocument(True, "vision", pages)


def retry(
    conn: Any,
    client: Ollama,
    *,
    document_id: Any,
    payload: bytes,
    mime: str,
    original_name: str,
) -> Recovery:
    """Send the pages as images and try the whole pack pipeline again on what comes back."""
    images = page_images(payload, mime)
    if not images:
        return _still_quarantined(conn, document_id, "this document cannot be rendered as pages")

    read = transcribe(client, images)
    if not read.ok:
        return _still_quarantined(conn, document_id, read.reason or "the image pass failed")

    outcome = read_and_commit(
        conn, client, document_id=document_id, parsed=read, name=original_name
    )
    if isinstance(outcome, str):
        return _still_quarantined(conn, document_id, outcome)
    log.info("recovered %s from the page image: %d cited fact(s)", document_id, outcome.facts)
    return Recovery(document_id, True, None, outcome.facts, outcome.chunks, outcome.pages)


def _still_quarantined(conn: Any, document_id: Any, reason: str) -> Recovery:
    with conn.cursor() as cur:
        cur.execute(
            sql.MARK_QUARANTINED,
            {"document_id": document_id, "pages": None, "reason": f"image pass: {reason}"[:500]},
        )
    conn.commit()
    return Recovery(document_id, False, reason)


def recovery_rate(recoveries: list[Recovery]) -> str:
    """The reportable line. Deliberately a rate and a count, because a rate over three
    documents is not a finding and the count is what says so."""
    if not recoveries:
        return "no quarantined documents were retried"
    rescued = sum(1 for r in recoveries if r.recovered)
    return (
        f"the image pass recovered {rescued} of {len(recoveries)} ({rescued / len(recoveries):.0%})"
    )
