"""Parse, chunk, embed, extract, and commit both lanes in one transaction.

The fork is the point of this module. A document produces chunks for retrieval and facts for
the modules, and they are written in the **same** transaction, so a reminder can never disagree
with a search result: either both lanes see the document or neither does.

Anything that fails routes to quarantine with a reason, and quarantine is a queue rather than a
bin. `core/ingest/quarantine.py` runs the second pass over it.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

from core.ingest import sql
from core.ingest.chunk import Chunk, chunk_pages
from core.ingest.classify import classification_sample, classify
from core.ingest.extract import Extraction, extract
from core.ingest.obligations import fixed, from_facts
from core.ingest.parse import ParsedDocument, parse
from core.packs import PackUnavailable, pack
from core.runtime.ollama import ModelUnavailable, Ollama

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Outcome:
    document_id: Any
    status: str  # indexed | quarantined
    pages: int
    doc_type: str | None
    pack_id: str | None
    chunks: int
    facts: int
    reason: str | None = None

    @property
    def quarantined(self) -> bool:
        return self.status == "quarantined"

    def line(self) -> str:
        """One line for the Parrot window. A person should be able to read what happened."""
        if self.quarantined:
            return f"needs your eyes: {self.reason}"
        if self.status != "indexed":
            return f"{self.status}: {self.reason or self.status}"
        return (
            f"indexed as {self.pack_id}.{self.doc_type}: "
            f"{self.pages} page(s), {self.chunks} chunk(s), {self.facts} cited fact(s)"
        )


def process(
    conn: Any,
    client: Ollama,
    *,
    document_id: Any,
    payload: bytes,
    mime: str,
    original_name: str,
) -> Outcome:
    """The whole pipeline for one document. Commits on success, rolls back on failure."""
    parsed = parse(payload, mime, original_name)
    if not parsed.ok:
        return _quarantine(conn, document_id, parsed, parsed.reason or "the parser failed")

    classification = classify(client, classification_sample(parsed.pages))
    if not classification.recognised:
        return _quarantine(
            conn, document_id, parsed, classification.reason or "not recognised by any pack"
        )
    assert classification.pack_id is not None and classification.doc_type is not None

    try:
        installed = pack(classification.pack_id)
    except PackUnavailable as error:
        return _quarantine(conn, document_id, parsed, str(error))

    extraction = extract(
        client,
        installed,
        classification.doc_type,
        parsed.pages,
        confidence=classification.confidence,
    )

    chunks = chunk_pages(
        parsed.pages, original_name=original_name, doc_type=classification.doc_type
    )
    try:
        vectors = client.embed([chunk.embedding_input for chunk in chunks])
    except ModelUnavailable as error:
        return _quarantine(conn, document_id, parsed, str(error))

    if not extraction.ok:
        # The retrieval lane would succeed and the facts lane would not. Writing only half of it
        # is exactly the disagreement this pipeline exists to prevent, so the whole document
        # waits for the second pass.
        return _quarantine(
            conn, document_id, parsed, extraction.reason or "extraction did not satisfy the pack"
        )

    written = commit_both_lanes(
        conn,
        document_id=document_id,
        parsed=parsed,
        chunks=chunks,
        vectors=vectors,
        extraction=extraction,
        installed_id=installed.id,
        installed_version=installed.version,
        doc_type=classification.doc_type,
    )
    return Outcome(
        document_id=document_id,
        status="indexed",
        pages=parsed.page_count,
        doc_type=classification.doc_type,
        pack_id=installed.id,
        chunks=len(chunks),
        facts=written,
        reason=None,
    )


def commit_both_lanes(
    conn: Any,
    *,
    document_id: Any,
    parsed: ParsedDocument,
    chunks: list[Chunk],
    vectors: list[list[float]],
    extraction: Extraction,
    installed_id: str,
    installed_version: str,
    doc_type: str,
) -> int:
    with conn.cursor() as cur:
        cur.execute(sql.DELETE_CHUNKS, {"document_id": document_id})
        cur.execute(sql.DELETE_FACTS, {"document_id": document_id})
        for chunk, vector in zip(chunks, vectors, strict=True):
            cur.execute(
                sql.INSERT_CHUNK,
                {
                    "document_id": document_id,
                    "page": chunk.page,
                    "ordinal": chunk.ordinal,
                    "context_prefix": chunk.context_prefix,
                    "text": chunk.text,
                    "embedding": _vector_literal(vector),
                },
            )
        written_facts = []
        for fact in extraction.facts:
            cur.execute(
                sql.INSERT_FACT,
                {
                    "document_id": document_id,
                    "page": fact.page,
                    "pack_id": installed_id,
                    "pack_version": installed_version,
                    "key": fact.key,
                    "subject": fact.subject,
                    "value_text": fact.value_text,
                    "value_num": fact.value_num,
                    "value_date": fact.value_date,
                    "confidence": fact.confidence,
                },
            )
            row = cur.fetchone()
            if row is not None:
                written_facts.append((int(row[0]), fact))

        installed = pack(installed_id)
        from_facts(cur, installed, written_facts)
        fixed(cur, installed)
        cur.execute(
            sql.MARK_INDEXED,
            {
                "document_id": document_id,
                "pages": parsed.page_count,
                "doc_type": doc_type,
                "pack_id": installed_id,
            },
        )
        cur.execute(
            sql.INSERT_TRACE,
            {
                "thread_id": str(document_id),
                "node": "ingest",
                "latency_ms": extraction.latency_ms,
                "model": extraction.model,
                "payload": json.dumps(
                    {
                        "parser": parsed.parser,
                        "pages": parsed.page_count,
                        "chunks": len(chunks),
                        "facts": len(extraction.facts),
                        "unplaced": extraction.unplaced or [],
                    }
                ),
            },
        )
    conn.commit()
    return len(extraction.facts)


def _quarantine(conn: Any, document_id: Any, parsed: ParsedDocument, reason: str) -> Outcome:
    with conn.cursor() as cur:
        cur.execute(sql.DELETE_CHUNKS, {"document_id": document_id})
        cur.execute(sql.DELETE_FACTS, {"document_id": document_id})
        cur.execute(
            sql.MARK_QUARANTINED,
            {
                "document_id": document_id,
                "pages": parsed.page_count or None,
                "reason": reason[:500],
            },
        )
    conn.commit()
    log.info("quarantined %s: %s", document_id, reason)
    return Outcome(
        document_id=document_id,
        status="quarantined",
        pages=parsed.page_count,
        doc_type=None,
        pack_id=None,
        chunks=0,
        facts=0,
        reason=reason,
    )


def _vector_literal(vector: list[float]) -> str:
    """pgvector accepts its own text form; this avoids registering an adapter for one column."""
    return "[" + ",".join(f"{value:.6f}" for value in vector) + "]"
