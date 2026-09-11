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
import io
import logging
from dataclasses import dataclass
from typing import Any

from core.ingest import sql
from core.ingest.chunk import chunk_pages
from core.ingest.classify import classify
from core.ingest.extract import extract
from core.ingest.parse import ParsedDocument, ParsedPage
from core.ingest.pipeline import commit_both_lanes
from core.packs import PackUnavailable, pack
from core.runtime.ollama import ModelUnavailable, Ollama

log = logging.getLogger(__name__)

RENDER_DPI = 150  # enough for 8pt print; 300 quadruples the tokens for no measured gain yet
MAX_IMAGE_PAGES = 4  # a household document; beyond this the context cost is not worth it

IMAGE_MIMES = frozenset({"image/jpeg", "image/png", "image/tiff"})

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


def page_images(payload: bytes, mime: str) -> list[str]:
    """Base64 page images, in page order. Empty when this document cannot be rendered."""
    if mime in IMAGE_MIMES:
        return [base64.b64encode(payload).decode("ascii")]
    if mime != "application/pdf":
        return []
    try:
        import pypdfium2
    except ImportError:
        log.warning("cannot render PDF pages: pypdfium2 is not installed")
        return []
    try:
        document = pypdfium2.PdfDocument(payload)
        images = []
        for index in range(min(len(document), MAX_IMAGE_PAGES)):
            bitmap = document[index].render(scale=RENDER_DPI / 72)
            buffer = io.BytesIO()
            bitmap.to_pil().save(buffer, format="PNG")
            images.append(base64.b64encode(buffer.getvalue()).decode("ascii"))
        return images
    except Exception as error:  # pdfium raises its own errors on damaged files
        log.info("could not render pages: %s", error)
        return []


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

    classification = classify(client, read.pages[0].text)
    if not classification.recognised:
        return _still_quarantined(
            conn, document_id, classification.reason or "still not recognised by any pack"
        )
    assert classification.pack_id is not None and classification.doc_type is not None

    try:
        installed = pack(classification.pack_id)
    except PackUnavailable as error:
        return _still_quarantined(conn, document_id, str(error))

    extraction = extract(
        client,
        installed,
        classification.doc_type,
        read.pages,
        confidence=classification.confidence,
    )
    if not extraction.ok:
        return _still_quarantined(
            conn, document_id, extraction.reason or "the pack's fields are still not satisfied"
        )

    chunks = chunk_pages(read.pages, original_name=original_name, doc_type=classification.doc_type)
    try:
        vectors = client.embed([chunk.embedding_input for chunk in chunks])
    except ModelUnavailable as error:
        return _still_quarantined(conn, document_id, str(error))

    written = commit_both_lanes(
        conn,
        document_id=document_id,
        parsed=read,
        chunks=chunks,
        vectors=vectors,
        extraction=extraction,
        installed_id=installed.id,
        installed_version=installed.version,
        doc_type=classification.doc_type,
    )
    log.info("recovered %s from the page image: %d cited fact(s)", document_id, written)
    return Recovery(document_id, True, None, written, len(chunks), len(read.pages))


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
