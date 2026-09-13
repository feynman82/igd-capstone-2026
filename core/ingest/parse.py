"""Turn captured bytes into pages of text, or say why it could not be done.

Every page of text keeps its page number, because `facts.page` is NOT NULL and a citation
that cannot name a page is not a citation. A parser that loses pagination is therefore not an
option here, however good its text is.

Two parsers, one interface:

- `DoclingParser` for PDFs and photographs. Docling is the stack's parser and it preserves
  tables, which is most of what a payslip or a policy schedule actually is.
- `PlainTextParser` for text and markdown, which need no model and no OCR.

Failure is a return value, not an exception. `ParsedDocument.ok` false with a reason is what
routes a document to quarantine, and quarantine is where the vision-language second pass picks
it up. Nothing is ever silently dropped.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Protocol

log = logging.getLogger(__name__)

TEXT_MIMES = frozenset({"text/plain", "text/markdown", "text/csv"})
DOCLING_MIMES = frozenset(
    {
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/tiff",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
)

# Below this, a "successful" parse recovered so little text that the document is almost
# certainly a scan the parser could not read. It goes to quarantine for the image pass.
MIN_CHARS_PER_PAGE = 40


@dataclass(frozen=True, slots=True)
class Block:
    """One thing the parser found on a page, and what kind of thing it is."""

    kind: str  # heading | text | table
    text: str


@dataclass(frozen=True, slots=True)
class ParsedPage:
    page: int  # 1-based, as a person would say it
    text: str
    # The same page as the parser saw it, when it saw structure. `text` stays the plain join that
    # classification and extraction read; `core/ingest/chunk.py` reads these to cut at headings
    # instead of at a character count. Empty for plain text and the vision pass.
    blocks: tuple[Block, ...] = ()


@dataclass(frozen=True, slots=True)
class ParsedDocument:
    ok: bool
    parser: str
    pages: list[ParsedPage] = field(default_factory=list)
    reason: str | None = None

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def text(self) -> str:
        return "\n\n".join(page.text for page in self.pages)


class Parser(Protocol):
    name: str

    def handles(self, mime: str) -> bool: ...

    def parse(self, payload: bytes, original_name: str) -> ParsedDocument: ...


class PlainTextParser:
    name = "plaintext"

    def handles(self, mime: str) -> bool:
        return mime in TEXT_MIMES

    def parse(self, payload: bytes, original_name: str) -> ParsedDocument:
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = payload.decode("cp1252")
            except UnicodeDecodeError:
                return ParsedDocument(False, self.name, reason="not decodable as text")
        if not text.strip():
            return ParsedDocument(False, self.name, reason="the file is empty")
        # A text file has no pages. Calling it page 1 is honest: it is one page of evidence.
        return ParsedDocument(True, self.name, [ParsedPage(1, text.strip())])


class DoclingParser:
    """Docling, held at arm's length: imported on first use, and never at module import.

    A missing or broken Docling must quarantine a document, not stop the worker from starting.
    """

    name = "docling"

    def handles(self, mime: str) -> bool:
        return mime in DOCLING_MIMES

    def parse(self, payload: bytes, original_name: str) -> ParsedDocument:
        try:
            pages = self._convert(payload, original_name)
        except ImportError:
            return ParsedDocument(False, self.name, reason="Docling is not installed")
        except Exception as error:  # Docling raises a wide range on malformed input
            log.info("docling could not parse %s: %s", original_name, error)
            return ParsedDocument(
                False, self.name, reason=f"the parser failed: {type(error).__name__}"
            )

        if not pages:
            return ParsedDocument(False, self.name, reason="no pages were recovered")
        recovered = sum(len(p.text) for p in pages)
        if recovered < MIN_CHARS_PER_PAGE * len(pages):
            return ParsedDocument(
                False,
                self.name,
                pages,
                reason=f"only {recovered} characters recovered from {len(pages)} page(s)",
            )
        return ParsedDocument(True, self.name, pages)

    def _convert(self, payload: bytes, original_name: str) -> list[ParsedPage]:
        from io import BytesIO

        from docling.datamodel.base_models import DocumentStream
        from docling.document_converter import DocumentConverter
        from docling_core.types.doc.document import DoclingDocument

        converter = DocumentConverter()
        result = converter.convert(DocumentStream(name=original_name, stream=BytesIO(payload)))
        document: DoclingDocument = result.document
        return _pages_from(document)


def _pages_from(document: object) -> list[ParsedPage]:
    """Group Docling's items by the page they were found on.

    Docling's markdown export is one string for the whole document, which would throw away the
    page numbers `facts.page` needs. Its item provenance carries them, so they are read from
    there instead. A table carries its content in its cells rather than in `.text`, and is read
    through `_table_text`.
    """
    by_page: dict[int, list[Block]] = {}
    for item, _level in document.iterate_items():  # type: ignore[attr-defined]
        text = getattr(item, "text", None)
        kind = _kind(item)
        if not text or not str(text).strip():
            text = _table_text(item)
            kind = "table"
        if not text or not str(text).strip():
            continue
        provenance = getattr(item, "prov", None) or []
        page_no = getattr(provenance[0], "page_no", 1) if provenance else 1
        by_page.setdefault(int(page_no), []).append(Block(kind, str(text).strip()))
    return [
        ParsedPage(page, "\n".join(block.text for block in blocks), tuple(blocks))
        for page, blocks in sorted(by_page.items())
    ]


_HEADING_LABELS = frozenset({"title", "section_header"})


def _kind(item: object) -> str:
    """Docling's label, reduced to the one distinction chunking needs: is this a heading."""
    label = getattr(item, "label", None)
    value = str(getattr(label, "value", label) or "")
    return "heading" if value in _HEADING_LABELS else "text"


def _table_text(item: object) -> str | None:
    """A table as lines of text, one row per line: `label: value` when a row has two cells.

    Docling puts a table's content in its cells, not in `.text`, so keeping only items with text
    dropped every table without a trace. On 2026-09-13 that was a policy's whole schedule — policy
    number, insured, period and premium, all on page 1, all found by Docling as one table — and the
    document quarantined as "required fields not found on any page" while the values sat in the
    parsed document. A benefit table would have been lost to retrieval the same way.

    Read through the cell grid and duck-typed, so nothing here imports Docling. A spanned cell is
    repeated across the columns it covers, so consecutive identical cells are counted once.
    """
    try:
        grid = getattr(getattr(item, "data", None), "grid", None)
    except Exception:  # a malformed table must not take the rest of the page with it
        return None
    if not grid:
        return None
    lines: list[str] = []
    for row in grid:
        cells: list[str] = []
        for cell in row:
            value = " ".join(str(getattr(cell, "text", "") or "").split())
            if value and (not cells or cells[-1] != value):
                cells.append(value)
        if cells:
            lines.append(f"{cells[0]}: {cells[1]}" if len(cells) == 2 else " | ".join(cells))
    return "\n".join(lines) or None


PARSERS: tuple[Parser, ...] = (PlainTextParser(), DoclingParser())


def parse(payload: bytes, mime: str, original_name: str) -> ParsedDocument:
    """The one call the pipeline makes. An unhandled mime type quarantines rather than raises."""
    for parser in PARSERS:
        if parser.handles(mime):
            return parser.parse(payload, original_name)
    return ParsedDocument(False, "none", reason=f"no parser handles {mime}")
