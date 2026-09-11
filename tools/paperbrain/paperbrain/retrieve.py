"""Hybrid retrieval: BM25 keyword search fused with dense vector search.

Why hybrid: paperwork queries are half semantic ("what does my home policy say
about water damage") and half literal ("policy AIA-882401", "$1,248.90").
Embeddings are weak on exact tokens like policy numbers and amounts; BM25 is
weak on paraphrase. Reciprocal Rank Fusion combines the two rankings without
needing calibrated scores from either.
"""

from __future__ import annotations

import contextlib
import re
import sqlite3
from dataclasses import dataclass

import numpy as np

from .db import load_matrix, pack
from .ollama import Ollama

_FTS_SAFE = re.compile(r'[^\w\s"$.\-/]')


@dataclass
class Hit:
    chunk_id: int
    document_id: int
    path: str
    filename: str
    page: int | None
    text: str
    score: float
    doc_date: str | None = None
    doc_type: str | None = None


def _fts_query(question: str) -> str:
    """Turn free text into a safe FTS5 OR-query with prefix matching."""
    cleaned = _FTS_SAFE.sub(" ", question)
    terms = [t for t in cleaned.split() if len(t) > 1]
    if not terms:
        return ""
    return " OR ".join(f'"{t}"*' if t.isalnum() else f'"{t}"' for t in terms)


def keyword_search(conn: sqlite3.Connection, question: str, limit: int) -> list[int]:
    query = _fts_query(question)
    if not query:
        return []
    try:
        rows = conn.execute(
            """
            SELECT c.id AS id
            FROM chunks_fts f
            JOIN chunks c ON c.id = f.rowid
            WHERE chunks_fts MATCH ?
            ORDER BY bm25(chunks_fts)
            LIMIT ?
            """,
            (query, limit),
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    return [r["id"] for r in rows]


def vector_search(
    conn: sqlite3.Connection, client: Ollama, model: str, question: str, limit: int
) -> list[int]:
    matrix, ids = load_matrix(conn)
    if not ids:
        return []
    qvec = np.frombuffer(pack(client.embed(model, [question])[0]), dtype=np.float32)
    if qvec.shape[0] != matrix.shape[1]:
        # Embedding model changed since ingest — keyword search still works.
        return []
    scores = matrix @ qvec  # both sides are L2-normalised => cosine
    top = np.argsort(-scores)[:limit]
    return [ids[i] for i in top]


def fuse(rankings: list[list[int]], k: int = 60) -> list[tuple[int, float]]:
    """Reciprocal Rank Fusion over several ranked id lists."""
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, chunk_id in enumerate(ranking):
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.items(), key=lambda kv: -kv[1])


def hydrate(conn: sqlite3.Connection, scored: list[tuple[int, float]]) -> list[Hit]:
    if not scored:
        return []
    ids = [cid for cid, _ in scored]
    placeholders = ",".join("?" * len(ids))
    rows = conn.execute(
        f"""
        SELECT c.id, c.document_id, c.page, c.text,
               d.path, d.filename, d.doc_date, d.doc_type
        FROM chunks c JOIN documents d ON d.id = c.document_id
        WHERE c.id IN ({placeholders})
        """,
        ids,
    ).fetchall()
    by_id = {r["id"]: r for r in rows}
    hits = []
    for chunk_id, score in scored:
        r = by_id.get(chunk_id)
        if not r:
            continue
        hits.append(
            Hit(
                chunk_id=r["id"],
                document_id=r["document_id"],
                path=r["path"],
                filename=r["filename"],
                page=r["page"],
                text=r["text"],
                score=score,
                doc_date=r["doc_date"],
                doc_type=r["doc_type"],
            )
        )
    return hits


def search(
    conn: sqlite3.Connection,
    client: Ollama,
    cfg,
    question: str,
    top_k: int | None = None,
) -> list[Hit]:
    top_k = top_k or cfg.top_k
    rankings = [keyword_search(conn, question, cfg.candidates)]
    with contextlib.suppress(Exception):  # keyword-only is a fine degraded mode
        rankings.append(vector_search(conn, client, cfg.embed_model, question, cfg.candidates))
    return hydrate(conn, fuse(rankings, cfg.rrf_k)[:top_k])
