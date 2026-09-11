"""Split extracted text into retrieval-sized chunks.

Paperwork is short and structured — a receipt is one chunk, a policy is a few
dozen. We split on paragraph boundaries first and only fall back to hard
character cuts inside a very long paragraph, so a line item never gets sliced
in half. Page numbers are carried through so answers can cite "page 3".
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import pairwise

_WS = re.compile(r"[ \t]+")
_BLANKS = re.compile(r"\n{3,}")


@dataclass
class Chunk:
    ordinal: int
    page: int | None
    text: str


def clean(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _WS.sub(" ", text)
    text = _BLANKS.sub("\n\n", text)
    return text.strip()


def _split_page(text: str, size: int, overlap: int) -> list[str]:
    text = clean(text)
    if not text:
        return []
    if len(text) <= size:
        return [text]

    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    out: list[str] = []
    buf = ""

    def flush() -> None:
        nonlocal buf
        if buf.strip():
            out.append(buf.strip())
        buf = ""

    for para in paragraphs:
        if len(para) > size:
            flush()
            step = max(size - overlap, 1)
            for start in range(0, len(para), step):
                piece = para[start : start + size]
                if piece.strip():
                    out.append(piece.strip())
                if start + size >= len(para):
                    break
            continue
        if len(buf) + len(para) + 2 > size:
            flush()
            buf = para
        else:
            buf = f"{buf}\n\n{para}" if buf else para
    flush()

    # Stitch a little context from the previous chunk onto each chunk.
    if overlap > 0 and len(out) > 1:
        stitched = [out[0]]
        for prev, cur in pairwise(out):
            tail = prev[-overlap:]
            stitched.append(f"{tail}\n\n{cur}" if tail.strip() else cur)
        out = stitched
    return out


def chunk_pages(pages: list[str], size: int = 1100, overlap: int = 200) -> list[Chunk]:
    chunks: list[Chunk] = []
    ordinal = 0
    for page_index, page_text in enumerate(pages):
        for piece in _split_page(page_text, size, overlap):
            chunks.append(Chunk(ordinal=ordinal, page=page_index + 1, text=piece))
            ordinal += 1
    return chunks
