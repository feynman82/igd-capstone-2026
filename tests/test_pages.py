"""Drawing one page of one document.

The thing worth protecting here is the page *number*. A citation says "policy.pdf, page 3" and
a person clicks it expecting page 3 — so the arithmetic between a one-based citation and a
zero-based renderer is tested directly rather than assumed, and an out-of-range page is an
error with a sentence rather than the last page or a blank image.
"""

from __future__ import annotations

import base64
import io

import pytest

from core.pages import (
    PageUnavailable,
    RendererUnavailable,
    page_count,
    render_page,
)

pypdfium2 = pytest.importorskip("pypdfium2")

# A real 1x1 PNG. An image document is already one page of pixels.
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


@pytest.fixture(scope="module")
def three_pages() -> bytes:
    """A three-page PDF, each page a different size so a render can be told from its neighbour."""
    document = pypdfium2.PdfDocument.new()
    for width, height in ((200, 300), (400, 300), (200, 600)):
        document.new_page(width, height)
    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def test_a_pdf_is_counted_by_the_file_not_by_what_the_parser_managed(
    three_pages: bytes,
) -> None:
    assert page_count(three_pages, "application/pdf") == 3


def test_an_image_document_is_one_page() -> None:
    assert page_count(PNG, "image/png") == 1


def test_something_with_no_pages_counts_zero() -> None:
    assert page_count(b"key,value\n1,2\n", "text/csv") == 0


def test_page_numbers_are_the_ones_a_citation_says(three_pages: bytes) -> None:
    """Page 2 is the wide one. If the off-by-one ever returns, this is what catches it."""
    first, _ = render_page(three_pages, "application/pdf", 1)
    second, _ = render_page(three_pages, "application/pdf", 2)
    third, _ = render_page(three_pages, "application/pdf", 3)

    assert _size(first) != _size(second) != _size(third)
    assert _size(second)[0] > _size(first)[0], "page 2 is the wide one"
    assert _size(third)[1] > _size(first)[1], "page 3 is the tall one"


def test_a_rendered_page_is_a_png(three_pages: bytes) -> None:
    drawn, media_type = render_page(three_pages, "application/pdf", 1)
    assert media_type == "image/png"
    assert drawn.startswith(b"\x89PNG\r\n\x1a\n")


def test_an_image_is_handed_back_untouched() -> None:
    """Re-encoding a photograph of a receipt costs quality and buys nothing."""
    drawn, media_type = render_page(PNG, "image/png", 1)
    assert drawn is PNG
    assert media_type == "image/png"


def test_a_page_past_the_end_says_how_many_there_are(three_pages: bytes) -> None:
    with pytest.raises(PageUnavailable, match="3 page"):
        render_page(three_pages, "application/pdf", 4)


def test_page_zero_is_refused(three_pages: bytes) -> None:
    with pytest.raises(PageUnavailable, match="numbered from 1"):
        render_page(three_pages, "application/pdf", 0)


def test_a_second_page_of_a_photograph_does_not_exist() -> None:
    with pytest.raises(PageUnavailable, match="1 page"):
        render_page(PNG, "image/png", 2)


def test_a_file_that_is_not_a_document_says_which_kind_it_is() -> None:
    with pytest.raises(PageUnavailable, match="text/csv"):
        render_page(b"key,value\n", "text/csv", 1)


def test_a_damaged_pdf_is_a_sentence_not_a_traceback() -> None:
    with pytest.raises(PageUnavailable):
        render_page(b"%PDF-1.7\nthis is not a pdf", "application/pdf", 1)


def test_an_install_without_the_renderer_says_so(monkeypatch: pytest.MonkeyPatch) -> None:
    """The interface has an error state for "this cannot be shown". It has none for a bad PNG."""
    import builtins

    real_import = builtins.__import__

    def no_pdfium(name: str, *args: object, **kwargs: object) -> object:
        if name == "pypdfium2":
            raise ImportError("no module named pypdfium2")
        return real_import(name, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(builtins, "__import__", no_pdfium)
    with pytest.raises(RendererUnavailable, match="pypdfium2"):
        render_page(b"%PDF-1.7", "application/pdf", 1)


def _size(png: bytes) -> tuple[int, int]:
    """Width and height straight out of the PNG header, so the test needs no image library."""
    width = int.from_bytes(png[16:20], "big")
    height = int.from_bytes(png[20:24], "big")
    return width, height
