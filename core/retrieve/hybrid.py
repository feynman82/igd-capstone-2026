"""Hybrid retrieval: pgvector cosine search and Postgres full-text search, fused by rank.

Dense search alone misses exact identifiers. On 13 September `MV-2026-448120` and the one-digit-
off `MV-2026-448121` sat at the same cosine similarity, because an embedding of a policy number
is an embedding of "a policy number". Full-text search alone misses paraphrase: "my car cover"
shares no stem with "vehicle". So both run, in one query, and reciprocal rank fusion decides
which `candidates` chunks are worth reranking: a chunk ranked by both arms outscores a chunk
ranked by one, and a chunk only one arm found is still in the set.

What the fusion does *not* do is replace the score. `core/graph` compares a passage's score
against the pack's abstain floor, which is a cosine similarity, and re-sorts by it when it fuses
several phrasings of one question — so `Passage.score` stays the cosine similarity for every
passage, including the ones only the lexical arm found. The one exception is an exact identifier
hit: when the question names something with digits in it and the chunk prints those very
characters, the document contains the thing the person typed, and that is what a similarity
of 0.95 means. The floor keeps its meaning and the near-miss number stays where cosine put it.

Postgres already parses a hyphenated identifier as a phrase (`'mv' <-> '-2026' <-> '-448120'`),
so `websearch_to_tsquery` finds the exact policy number and nothing for the near-miss one; the
boost is what lifts the exact hit over the floor, not what finds it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from core.graph.ports import Passage
from core.runtime.ollama import Ollama

RRF_K = 60  # the standard constant; every rank contributes 1 / (k + rank)
IDENTIFIER_HIT = 0.95  # the similarity an exact identifier match is worth, on the cosine scale
# A policy number (MV-2026-448120), a registration plate as printed (SLK 8842 D) or as typed
# (SLK8842D), a long reference (20260312-7). Not a bare year: "2027" names a date, not a thing.
IDENTIFIER = re.compile(
    r"\b(?:"
    r"[A-Za-z]{1,4}-?\d{3,}(?:-\d+)*(?:-?[A-Za-z])?"  # MV-2026-448120, SLK8842D
    r"|[A-Za-z]{1,4} ?\d{3,} ?[A-Za-z]"  # SLK 8842 D — spaced only with the plate's trailing letter
    r"|\d{5,}(?:-\d+)*"  # 20260312-7
    r")\b"
)

# Hand-written and parameterised, per rule 1. Two ranked arms, each straight against the table so
# the HNSW and GIN indexes are used, each with the status and pack predicates the dense stopgap
# used so a disabled pack stays invisible; joined on chunk id so a chunk found by both carries both
# ranks. Cosine similarity is then computed for every surviving row, whichever arm found it,
# because it is the score the graph reads.
HYBRID_SEARCH = """
WITH dense AS (
    SELECT c.id, row_number() OVER (ORDER BY c.embedding <=> %(query)s::vector) AS rank
      FROM chunks c
      JOIN documents d ON d.id = c.document_id
     WHERE d.status = 'indexed'
       AND c.embedding IS NOT NULL
       AND (%(packs)s::text[] IS NULL
            OR d.pack_id IS NULL
            OR d.pack_id = ANY(%(packs)s::text[]))
     ORDER BY c.embedding <=> %(query)s::vector
     LIMIT %(limit)s
),
lexical AS (
    SELECT c.id,
           row_number() OVER (
               ORDER BY ts_rank_cd(c.tsv, websearch_to_tsquery('english', %(terms)s)) DESC, c.id
           ) AS rank
      FROM chunks c
      JOIN documents d ON d.id = c.document_id
     WHERE d.status = 'indexed'
       AND c.embedding IS NOT NULL
       AND c.tsv @@ websearch_to_tsquery('english', %(terms)s)
       AND (%(packs)s::text[] IS NULL
            OR d.pack_id IS NULL
            OR d.pack_id = ANY(%(packs)s::text[]))
     ORDER BY ts_rank_cd(c.tsv, websearch_to_tsquery('english', %(terms)s)) DESC, c.id
     LIMIT %(limit)s
),
found AS (
    SELECT COALESCE(dense.id, lexical.id) AS id,
           dense.rank   AS dense_rank,
           lexical.rank AS lexical_rank,
           COALESCE(1.0 / (%(k)s + dense.rank), 0)
             + COALESCE(1.0 / (%(k)s + lexical.rank), 0) AS rrf
      FROM dense
      FULL OUTER JOIN lexical ON lexical.id = dense.id
)
SELECT c.id,
       c.document_id,
       c.page,
       c.text,
       c.context_prefix,
       d.original_name,
       d.pack_id,
       1.0 - (c.embedding <=> %(query)s::vector) AS similarity,
       found.dense_rank,
       found.lexical_rank,
       found.rrf,
       d.doc_type
  FROM found
  JOIN chunks c ON c.id = found.id
  JOIN documents d ON d.id = c.document_id
 ORDER BY found.rrf DESC, similarity DESC, c.id
 LIMIT %(limit)s
"""


def identifiers(question: str) -> list[str]:
    """The tokens in a question that look like something printed rather than said: a policy
    number, a registration plate, a claim reference. A year on its own is not one — every
    schedule prints a year, and a boost on "2027" would lift the whole vault over the floor."""
    return list(dict.fromkeys(match.group(0) for match in IDENTIFIER.finditer(question)))


def prints(text: str, token: str) -> bool:
    """Whether the chunk prints the identifier, ignoring case and the spacing inside it: the
    schedule says `SLK 8842 D`, a person may type `SLK8842D`."""
    squeeze = re.compile(r"[\s-]+")
    return squeeze.sub("", token).casefold() in squeeze.sub("", text).casefold()


def hybrid_score(similarity: float, *, exact: bool) -> float:
    """The cosine similarity, lifted to `IDENTIFIER_HIT` when the chunk prints an identifier the
    question named. Never lowered: a passage that is close stays close."""
    return max(similarity, IDENTIFIER_HIT) if exact else similarity


@dataclass(frozen=True, slots=True)
class HybridRetriever:
    """Implements `core.graph.ports.Retriever`. Built where the connection is, like the dense
    stopgap it replaces, with the same enabled-pack filter."""

    conn: Any
    client: Ollama
    packs: tuple[str, ...] | None = None  # the enabled pack ids; None means do not filter
    k: int = RRF_K

    def search(self, question: str, *, candidates: int) -> list[Passage]:
        # The query prompt must match the one chunks were embedded with. See `QUERY_PROMPT`.
        vector = self.client.embed_query(question)
        literal = "[" + ",".join(f"{value:.6f}" for value in vector) + "]"
        allowed = sorted(self.packs) if self.packs is not None else None
        with self.conn.cursor() as cur:
            cur.execute(
                HYBRID_SEARCH,
                {
                    "query": literal,
                    "terms": question,
                    "limit": candidates,
                    "packs": allowed,
                    "k": self.k,
                },
            )
            rows = cur.fetchall()
        named = identifiers(question)
        return [
            Passage(
                chunk_id=row[0],
                document_id=row[1],
                page=row[2],
                text=row[3],
                score=hybrid_score(
                    float(row[7]),
                    exact=any(prints(row[3], token) for token in named),
                ),
                document_name=row[5],
                context_prefix=row[4] or "",
                pack_id=row[6] or "",
                doc_type=row[11] or "",
            )
            for row in rows
        ]
