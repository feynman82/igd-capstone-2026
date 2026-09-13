"""Split parsed pages into retrieval-sized chunks that follow the document's own structure.

**A chunk starts where the document starts a section.** Until 13 September chunks were cut every
1,050 characters regardless of what was there. The parser joins what it finds on a page with
single newlines and the old splitter only broke at blank lines, so every page arrived as one
"paragraph" and was sliced by count: chunks of a four-page policy began "e payment of the
required Annual Premium" and "llness or accidental injury". A clause cut in half is retrieved by
neither half. Measured on that policy, "what is the waiting period for appendicitis?" put the
definitions page first at 0.33; cut at its headings, clause 6 came first at 0.49.

The rules, in the order they apply:

- A page boundary always ends a chunk, because a citation names one page.
- A heading ends the chunk before it, and names every chunk after it until the next heading.
- A line — one parsed item, or one row of a table — is packed whole, up to `TARGET_CHARS`.
- A line longer than that is split at sentence ends, and only a sentence longer than that is cut,
  at a space.
- Runs of spaces and tabs become one space: PDF text often separates every word with a tab.
- A chunk that is only a heading is not kept. It is context for the chunks under it, not evidence.

The context prefix is **deterministic**: the document's title, its type, the section heading and
the page. Lane B owns contextualised chunking, where a model writes a real description; this is
the honest placeholder until then, now carrying the one thing a chunk from the middle of a
contract could not say for itself — which contract, and which section.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from core.ingest.parse import ParsedPage

TARGET_CHARS = 900
MIN_CHARS = 40

_SPACE = re.compile("[ \t\u00a0\u2009]+")
_SENTENCE_END = re.compile(r"(?<=[.;])\s+(?=[A-Z(\d])")
# Only for pages the parser gave no structure for — plain text and the vision pass. A numbered
# section title in capitals ("6. WAITING PERIODS AND PRE-EXISTING CONDITIONS"), or a short line
# in capitals ("POLICY SCHEDULE").
_HEADING_LINE = re.compile(r"^(\d+(\.\d+)*\.?\s+)?[A-Z][A-Z0-9 ,&'()/\-]{3,80}$")


@dataclass(frozen=True, slots=True)
class Chunk:
    page: int
    ordinal: int  # position within the whole document, 0-based
    context_prefix: str
    text: str
    title: str = ""  # the document as a person would name it; the embedding model's title slot

    @property
    def embedding_input(self) -> str:
        """What is actually embedded: the prefix plus the text, matching the tsvector column."""
        return f"{self.context_prefix}\n{self.text}"


def _clean(line: str) -> str:
    return _SPACE.sub(" ", line).strip()


def _lines(page: ParsedPage) -> list[tuple[bool, str]]:
    """The page as `(is_heading, line)`, from the parser's structure when it has any."""
    if page.blocks:
        return [
            (block.kind == "heading", line)
            for block in page.blocks
            for line in (_clean(raw) for raw in block.text.split("\n"))
            if line
        ]
    lines = (_clean(raw) for raw in page.text.split("\n"))
    return [(bool(_HEADING_LINE.match(line)), line) for line in lines if line]


def _pieces(line: str) -> list[str]:
    """A line, in pieces no longer than the target, broken at sentences and then at spaces."""
    if len(line) <= TARGET_CHARS:
        return [line]
    pieces: list[str] = []
    for sentence in _SENTENCE_END.split(line):
        while len(sentence) > TARGET_CHARS:
            cut = sentence.rfind(" ", 0, TARGET_CHARS)
            cut = cut if cut > 0 else TARGET_CHARS
            pieces.append(sentence[:cut].strip())
            sentence = sentence[cut:].strip()
        if sentence:
            pieces.append(sentence)
    return pieces


def _page_chunks(page: ParsedPage, heading: str) -> tuple[list[tuple[str, str]], str]:
    """`(heading, text)` for each chunk on one page, and the heading still open at its end."""
    chunks: list[tuple[str, str]] = []
    current: list[str] = []
    current_heading = heading
    body = False  # whether `current` holds anything besides a heading

    def flush() -> None:
        nonlocal current, body
        if current and body:
            chunks.append((current_heading, "\n".join(current)))
        current, body = [], False

    for is_heading, line in _lines(page):
        if is_heading:
            flush()
            heading = line
            current_heading = heading
            current = [line]
            continue
        for index, piece in enumerate(_pieces(line)):
            size = sum(len(part) + 1 for part in current)
            if current and size + len(piece) > TARGET_CHARS:
                flush()
                current_heading = heading
            if index and current:
                current[-1] = f"{current[-1]} {piece}"  # the rest of the same line
            else:
                current.append(piece)
            body = True
    flush()
    return chunks, heading


def chunk_pages(
    pages: list[ParsedPage],
    *,
    original_name: str,
    doc_type: str | None = None,
    title: str | None = None,
) -> list[Chunk]:
    """One flat list of chunks, ordinal running across the whole document."""
    label = doc_type.replace("_", " ") if doc_type else "document"
    name = title or original_name
    out: list[Chunk] = []
    heading = ""
    for page in pages:
        found, heading = _page_chunks(page, heading)
        for section, text in found:
            if len(text) < MIN_CHARS and len(pages) > 1:
                continue  # a stray page number or a footer on its own
            parts = [name, label, section, f"page {page.page}"]
            out.append(
                Chunk(
                    page=page.page,
                    ordinal=len(out),
                    context_prefix=" — ".join(part for part in parts if part),
                    text=text,
                    title=name,
                )
            )
    return out
