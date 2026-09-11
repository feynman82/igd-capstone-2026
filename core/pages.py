"""One page of one document, as an image.

Two callers want the same thing for opposite reasons. The quarantine retry wants the pixels
because the parser could not read them, and the interface wants the pixels because a person is
checking a cited claim against the paper it came from. Rendering them twice, slightly
differently, is how a citation ends up pointing at page 3 of one rendering and page 3 of
another — so it is rendered here, once.

**A page number in this module is the same page number that is in `facts.page`.** One-based,
counted the way the document is printed, which is what a citation says out loud ("policy.pdf,
page 3") and therefore what has to be true when the page opens.

The renderer is optional at runtime. `pypdfium2` is declared in `pyproject.toml`, but an
install that is missing it must say so rather than return a broken image: the interface has an
error state for "this cannot be shown", and it does not have one for a PNG that is not a PNG.
"""

from __future__ import annotations

import io
import logging
from typing import Any

log = logging.getLogger(__name__)

RENDER_DPI = 150  # enough for 8pt print; 300 quadruples the bytes for no legibility a person gains

# Documents that are already one page of pixels. Nothing renders them; they are handed over.
IMAGE_MIMES = frozenset({"image/jpeg", "image/png", "image/tiff"})

PDF_MIME = "application/pdf"


class PageUnavailable(LookupError):
    """Safe to show a person: there is no such page, or this file cannot be drawn."""


class RendererUnavailable(RuntimeError):
    """Safe to show a person: this install cannot render PDF pages at all."""


def _pdfium() -> Any:
    try:
        import pypdfium2
    except ImportError as error:  # pragma: no cover - exercised by the test that fakes it
        raise RendererUnavailable(
            "this install cannot open PDF pages: pypdfium2 is not installed"
        ) from error
    return pypdfium2


def page_count(payload: bytes, mime: str) -> int:
    """How many pages this file has, or 0 when it is not something with pages.

    `documents.pages` holds what the *parser* counted, which is the right number for a person
    to read and the wrong number to index a renderer with — a parser that gave up after two
    pages recorded two. This counts the file.
    """
    if mime in IMAGE_MIMES:
        return 1
    if mime != PDF_MIME:
        return 0
    try:
        return len(_pdfium().PdfDocument(payload))
    except RendererUnavailable:
        raise
    except Exception as error:  # pdfium raises its own class on a damaged file
        log.info("could not count pages: %s", error)
        return 0


def render_page(payload: bytes, mime: str, page: int) -> tuple[bytes, str]:
    """`(bytes, media type)` for one page, one-based.

    An image document is returned untouched under its own media type: re-encoding a photograph
    of a receipt to PNG costs size and quality and buys nothing, since the whole file already
    is the page.
    """
    if page < 1:
        raise PageUnavailable("pages are numbered from 1")

    if mime in IMAGE_MIMES:
        if page != 1:
            raise PageUnavailable(f"this document has 1 page, not {page}")
        return payload, mime

    if mime != PDF_MIME:
        raise PageUnavailable(f"a {mime} document has no pages to show")

    pdfium = _pdfium()
    try:
        document = pdfium.PdfDocument(payload)
    except Exception as error:
        log.info("could not open the document: %s", error)
        raise PageUnavailable("this file could not be opened") from error

    total = len(document)
    if page > total:
        raise PageUnavailable(f"this document has {total} page(s), not {page}")

    try:
        bitmap = document[page - 1].render(scale=RENDER_DPI / 72)
        buffer = io.BytesIO()
        bitmap.to_pil().save(buffer, format="PNG")
    except Exception as error:
        log.info("could not render page %d: %s", page, error)
        raise PageUnavailable(f"page {page} could not be drawn") from error

    return buffer.getvalue(), "image/png"
