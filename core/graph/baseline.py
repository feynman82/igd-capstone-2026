"""A dense-only retriever, so the graph can be run and tested before Lane B's hybrid search.

**This is a stopgap.** `core/retrieve/hybrid.py` has replaced it in `scripts/ask.py`, the API
and the evaluation harness. It stays for two reasons: `NoReranker` is still the reranker until
W4, and `eval.run --retriever dense` measures a retrieval change against it on the same vault.

It is here rather than in `core/retrieve/` on purpose: two people's agents writing into the same
directory in the same week is exactly the failure the lane split exists to prevent. It is
deliberately naive — one embedding, one `ORDER BY`, no fusion and no reranking — so that nobody
mistakes it for the baseline Yew Mun has to measure. His baseline is a measurement; this is
scaffolding.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from core.graph.ports import Passage
from core.runtime.db import vector_literal
from core.runtime.ollama import Ollama

log = logging.getLogger(__name__)

# Hand-written and parameterised, per rule 1. `<=>` is pgvector's cosine distance, so smaller is
# closer and the score below is turned back into "bigger is better" for the graph.
#
# The `packs` predicate is how "a disabled pack hides its facts" reaches an answer: a passage
# from a switched-off pack is never retrieved, so it can never be cited, so no sentence can be
# built on it. Passing NULL means no filter. A document belonging to no pack is always visible
# — nothing disabled it.
DENSE_SEARCH = """
SELECT c.id,
       c.document_id,
       c.page,
       c.text,
       c.context_prefix,
       d.original_name,
       d.pack_id,
       c.embedding <=> %(query)s::vector AS distance,
       d.doc_type
  FROM chunks c
  JOIN documents d ON d.id = c.document_id
 WHERE d.status = 'indexed'
   AND c.embedding IS NOT NULL
   AND (%(packs)s::text[] IS NULL
        OR d.pack_id IS NULL
        OR d.pack_id = ANY(%(packs)s::text[]))
 ORDER BY c.embedding <=> %(query)s::vector
 LIMIT %(limit)s
"""


@dataclass(frozen=True, slots=True)
class DenseRetriever:
    conn: Any
    client: Ollama
    packs: tuple[str, ...] | None = None  # the enabled pack ids; None means do not filter

    def search(self, question: str, *, candidates: int) -> list[Passage]:
        # The query prompt must match the one chunks were embedded with. See `QUERY_PROMPT`.
        vector = self.client.embed_query(question)
        allowed = sorted(self.packs) if self.packs is not None else None
        query = {"query": vector_literal(vector), "limit": candidates, "packs": allowed}
        with self.conn.cursor() as cur:
            cur.execute(DENSE_SEARCH, query)
            rows = cur.fetchall()
        return [
            Passage(
                chunk_id=row[0],
                document_id=row[1],
                page=row[2],
                text=row[3],
                score=1.0 - float(row[7]),  # cosine distance -> similarity
                document_name=row[5],
                context_prefix=row[4] or "",
                pack_id=row[6] or "",
                doc_type=row[8] or "",
            )
            for row in rows
        ]


@dataclass(frozen=True, slots=True)
class NoReranker:
    """Keeps the top `keep` in the order retrieval gave them. Lane B replaces this with
    bge-reranker-v2-m3, which is the thing that actually cuts 40 candidates to 6."""

    def rerank(self, question: str, passages: list[Passage], *, keep: int) -> list[Passage]:
        return passages[:keep]
