"""Rebuild a document's chunks and vectors without reading it again for facts.

Chunking and embedding changed on 13 September — clause-aligned chunks, a document title in the
context prefix, and the embedding model's task prompts — and a vault embedded the old way cannot
be searched the new way: the query and the passages must be embedded alike. Re-ingesting would
also re-classify and re-extract, which on a processor-only machine is minutes of generation per
document to arrive at facts that did not change. So this does the retrieval lane only.

What it does not touch is the point: the document row, its facts, its obligations, and anything a
person corrected. Chunk ids change, which is harmless — a citation carries the document and the
page, and those do not.

A document is done in one transaction. Anything that fails leaves its old chunks exactly as they
were: a half-rebuilt document is worse than an old one, because it retrieves from neither.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from core.ingest import sql
from core.ingest.chunk import chunk_pages
from core.ingest.parse import parse
from core.ingest.pipeline import _vector_literal, document_title
from core.packs import PackUnavailable, pack
from core.runtime.ollama import ModelUnavailable

log = logging.getLogger(__name__)


class ReindexFailed(RuntimeError):
    """Safe to show: names what went wrong, never what the document says."""


@dataclass(frozen=True, slots=True)
class IndexedDocument:
    document_id: Any
    original_name: str
    mime: str
    doc_type: str | None
    pack_id: str | None


@dataclass(frozen=True, slots=True)
class _Value:
    key: str
    value_text: str | None


def indexed(conn: Any) -> list[IndexedDocument]:
    with conn.cursor() as cur:
        cur.execute(sql.SELECT_INDEXED)
        return [IndexedDocument(*row) for row in cur.fetchall()]


def reindex_document(conn: Any, client: Any, document: IndexedDocument, payload: bytes) -> int:
    """Parse, chunk and embed one document again, and replace its chunks. Returns how many."""
    parsed = parse(payload, document.mime, document.original_name)
    if not parsed.ok:
        raise ReindexFailed(parsed.reason or "the parser failed")

    with conn.cursor() as cur:
        cur.execute(sql.SELECT_FACT_VALUES, {"document_id": document.document_id})
        values = [_Value(key, value_text) for key, value_text in cur.fetchall()]
    title = document.original_name
    if document.pack_id and document.doc_type:
        try:
            installed = pack(document.pack_id)
        except PackUnavailable:
            installed = None
        if installed is not None:
            title = document_title(installed, document.doc_type, values, document.original_name)

    chunks = chunk_pages(
        parsed.pages, original_name=document.original_name, doc_type=document.doc_type, title=title
    )
    try:
        vectors = client.embed_documents([(chunk.title, chunk.embedding_input) for chunk in chunks])
    except ModelUnavailable as error:
        raise ReindexFailed(str(error)) from error

    try:
        with conn.cursor() as cur:
            cur.execute(sql.DELETE_CHUNKS, {"document_id": document.document_id})
            for chunk, vector in zip(chunks, vectors, strict=True):
                cur.execute(
                    sql.INSERT_CHUNK,
                    {
                        "document_id": document.document_id,
                        "page": chunk.page,
                        "ordinal": chunk.ordinal,
                        "context_prefix": chunk.context_prefix,
                        "text": chunk.text,
                        "embedding": _vector_literal(vector),
                    },
                )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    log.info("reindexed %s: %d chunk(s)", document.original_name, len(chunks))
    return len(chunks)
