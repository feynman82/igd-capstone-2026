"""Split parsed pages into retrieval-sized chunks that still know their page number.

Paperwork is short and structured, so the split is conservative: paragraph boundaries first,
a hard character cut only inside a paragraph longer than the target. A line item must never be
sliced in half, because a chunk that ends mid-table is a chunk that cites a number without its
label.

The context prefix here is **deliberately deterministic** — the document type, the filename and
the page. Lane B owns contextualised chunking (their W4 task, `core/retrieve/`), where a model
writes a real one-line description. This is the honest placeholder until then, not a second
implementation of it.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.ingest.parse import ParsedPage

TARGET_CHARS = 1200
OVERLAP_CHARS = 150
MIN_CHARS = 40


@dataclass(frozen=True, slots=True)
class Chunk:
    page: int
    ordinal: int  # position within the whole document, 0-based
    context_prefix: str
    text: str

    @property
    def embedding_input(self) -> str:
        """What is actually embedded: the prefix plus the text, matching the tsvector column."""
        return f"{self.context_prefix}\n{self.text}"


def _paragraphs(text: str) -> list[str]:
    blocks = [block.strip() for block in text.split("\n\n")]
    return [block for block in blocks if block]


def _pack(paragraphs: list[str]) -> list[str]:
    """Greedily fill chunks up to the target, then carry a little tail into the next one."""
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if len(paragraph) > TARGET_CHARS:
            if current:
                chunks.append(current)
                current = ""
            for start in range(0, len(paragraph), TARGET_CHARS - OVERLAP_CHARS):
                piece = paragraph[start : start + TARGET_CHARS].strip()
                if piece:
                    chunks.append(piece)
            continue
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= TARGET_CHARS:
            current = candidate
            continue
        chunks.append(current)
        tail = current[-OVERLAP_CHARS:].strip()
        current = f"{tail}\n\n{paragraph}".strip() if tail else paragraph
    if current:
        chunks.append(current)
    return chunks


def chunk_pages(
    pages: list[ParsedPage],
    *,
    original_name: str,
    doc_type: str | None = None,
) -> list[Chunk]:
    """One flat list of chunks, ordinal running across the whole document."""
    label = doc_type.replace("_", " ") if doc_type else "document"
    out: list[Chunk] = []
    ordinal = 0
    for page in pages:
        for text in _pack(_paragraphs(page.text)) or []:
            if len(text) < MIN_CHARS and len(pages) > 1:
                continue  # a stray page number or a footer on its own
            out.append(
                Chunk(
                    page=page.page,
                    ordinal=ordinal,
                    context_prefix=f"{label} — {original_name}, page {page.page}",
                    text=text,
                )
            )
            ordinal += 1
    return out
