"""What the graph needs from retrieval, stated as a contract rather than an import.

Lane B owns `core/retrieve/`: hybrid search, RRF fusion, the cross-encoder reranker and the
abstain floor. The graph owns the order those happen in and what is done with the result. This
file is the seam between the two, so neither lane has to wait for the other and neither lane
ends up with its own copy of the other's work.

A `Passage` is deliberately small. It carries a chunk id, a document, a page and text — the four
things a citation needs — and a score whose scale is retrieval's business, not the graph's.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Protocol

Kind = Literal["document", "inventory", "guidance", "fact", "rule", "calculation", "calendar"]


@dataclass(frozen=True, slots=True)
class Passage:
    chunk_id: int
    document_id: Any
    page: int
    text: str
    score: float
    document_name: str = ""
    context_prefix: str = ""
    pack_id: str = ""  # the pack id its document was written under; `core` since ADR 0017
    doc_type: str = ""  # the catalogue type; a pack speaking for it governs the answer
    # a page of a document, a document on file, published guidance, or (ADR 0016) a cited fact,
    # a cited rule value, or the one calculation passage a `Calculation`'s figures are printed on
    kind: Kind = "document"

    def cite(self) -> str:
        """How a passage names itself: the document and the page, as a person would say it."""
        return f"{self.document_name or self.document_id}, page {self.page}"

    @property
    def ref(self) -> str:
        """Unique across kinds: chunk ids, fact ids and guidance ids are three sequences."""
        return f"{self.kind}:{self.chunk_id}"


class Retriever(Protocol):
    """Implemented by `core/retrieve/` when Lane B's hybrid search lands.

    `candidates` is how many passages to return before reranking. The graph asks for more than
    it will use, because that is the reranker's whole purpose.
    """

    def search(self, question: str, *, candidates: int) -> list[Passage]: ...


class Reranker(Protocol):
    """A cross-encoder, scoring question against passage. Returns the best `keep`, reordered."""

    def rerank(self, question: str, passages: list[Passage], *, keep: int) -> list[Passage]: ...
