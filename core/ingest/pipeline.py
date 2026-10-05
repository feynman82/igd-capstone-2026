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
from core.packs import CORE, PackUnavailable, catalog
from core.runtime.db import vector_literal
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
    read = read_and_commit(conn, client, document_id=document_id, parsed=parsed, name=original_name)
    return _quarantine(conn, document_id, parsed, read) if isinstance(read, str) else read


def read_and_commit(
    conn: Any, client: Ollama, *, document_id: Any, parsed: ParsedDocument, name: str
) -> Outcome | str:
    """Pages of text to both lanes, committed: classify, extract, chunk, embed, write. Or the
    reason it stopped, for the caller to quarantine in its own words — the first pass and the
    image pass (`core/ingest/quarantine.py`) read a document the same way from here on.

    Extraction is judged before anything is embedded. The retrieval lane would succeed where the
    facts lane did not, and writing only half of a document is exactly the disagreement this
    pipeline exists to prevent, so a document that fails extraction waits for the second pass
    without costing an embedding call first.
    """
    classification = classify(client, classification_sample(parsed.pages))
    if not classification.recognised:
        return classification.reason or "not a known document type"
    assert classification.doc_type is not None

    try:
        documents = catalog()
    except PackUnavailable as error:
        return str(error)

    extraction = extract(
        client,
        documents,
        classification.doc_type,
        parsed.pages,
        confidence=classification.confidence,
    )
    if not extraction.ok:
        return extraction.reason or "extraction did not satisfy the type"

    chunks = chunk_pages(
        parsed.pages,
        original_name=name,
        doc_type=classification.doc_type,
        title=document_title(documents, classification.doc_type, extraction.facts, name),
    )
    try:
        vectors = client.embed_documents([(chunk.title, chunk.embedding_input) for chunk in chunks])
    except ModelUnavailable as error:
        return str(error)

    written = commit_both_lanes(
        conn,
        document_id=document_id,
        parsed=parsed,
        chunks=chunks,
        vectors=vectors,
        extraction=extraction,
        doc_type=classification.doc_type,
    )
    return Outcome(
        document_id=document_id,
        status="indexed",
        pages=parsed.page_count,
        doc_type=classification.doc_type,
        pack_id=CORE,
        chunks=len(chunks),
        facts=written,
        reason=None,
    )


def document_title(documents: Any, doc_type: str, facts: Any, original_name: str) -> str:
    """The document as a person would name it: its `string` fields as read, in declared order.

    For a policy schedule that is the insurer and the product name — "Meridian Assurance,
    PrivateCare Hospital and Surgical Plan" — which is what a chunk from clause 6 of a contract
    cannot say for itself, and what "do I have a hospitalisation plan?" is really asking about.
    Which fields name a document is read from the catalogue's declared types rather than written
    here, so no field name lives in this module. The filename when nothing was read.
    """
    spec = documents.documents.document_types.get(doc_type)
    named = [field.name for field in spec.fields if field.type == "string"] if spec else []
    values = {fact.key: fact.value_text for fact in facts if getattr(fact, "value_text", None)}
    parts = [str(values[name]).strip() for name in named if values.get(name)]
    return ", ".join(dict.fromkeys(parts))[:160] or original_name


def commit_both_lanes(
    conn: Any,
    *,
    document_id: Any,
    parsed: ParsedDocument,
    chunks: list[Chunk],
    vectors: list[list[float]],
    extraction: Extraction,
    doc_type: str,
) -> int:
    version = catalog().version  # which field list read these facts, so re-extraction is auditable
    with conn.cursor() as cur:
        write_chunks(cur, document_id, chunks, vectors)
        cur.execute(sql.DELETE_FACTS, {"document_id": document_id})
        written_facts = []
        for fact in extraction.facts:
            cur.execute(
                sql.INSERT_FACT,
                {
                    "document_id": document_id,
                    "page": fact.page,
                    "pack_id": CORE,
                    "pack_version": version,
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

        from_facts(cur, written_facts)
        fixed(cur)
        cur.execute(
            sql.MARK_INDEXED,
            {
                "document_id": document_id,
                "pages": parsed.page_count,
                "doc_type": doc_type,
                "pack_id": CORE,
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


def write_chunks(
    cur: Any, document_id: Any, chunks: list[Chunk], vectors: list[list[float]]
) -> None:
    """Replace a document's chunks. The first pass, the image pass and a reindex all write here."""
    cur.execute(sql.DELETE_CHUNKS, {"document_id": document_id})
    for chunk, vector in zip(chunks, vectors, strict=True):
        cur.execute(
            sql.INSERT_CHUNK,
            {
                "document_id": document_id,
                "page": chunk.page,
                "ordinal": chunk.ordinal,
                "context_prefix": chunk.context_prefix,
                "text": chunk.text,
                "embedding": vector_literal(vector),
            },
        )
