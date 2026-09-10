# 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module

Date: 2026-09-10 · Status: accepted

## Context
`tools/paperbrain/` is Yew Mun's working local-RAG prototype: SQLite + FTS5 + numpy
cosine, pypdf + Tesseract for parsing, `nomic-embed-text` / `qwen2.5:14b-instruct` for
models, no orchestration graph, built for a 64 GB unified-memory Mac. It works, and its
retrieval design is sound. Whether it becomes PARROT's core retrieval module or stays a
separate prototype was an open question raised tonight while evaluating it against the
Week 1 hardware benchmark.

## Decision
PaperBrain is not adopted as a module. `core/retrieve/` ports its retrieval *pattern* —
hybrid BM25 plus dense fused with reciprocal rank fusion (already ADR 0002's decision),
hash-based idempotent ingest, per-page OCR fallback, and a refuse-to-guess grounded prompt
with `[n]` citations — rebuilt against PostgreSQL 17 with `pgvector` (`tsvector` for the
lexical side, `pgvector` cosine for dense), Docling for parsing, and
`Qwen-SEA-LION-v4-4B-VL` / `embeddinggemma` for models, wired into the LangGraph
router → retrieve → rerank → grounding-gate graph. `tools/paperbrain/` stays where it is,
unmodified, as a working reference implementation.

## Rejected
- **Adopt `tools/paperbrain/` wholesale as `core/retrieve/`:** violates ADR 0002 (a second
  datastore, SQLite alongside Postgres), swaps in unpinned models, has no reranker and no
  orchestration graph, and pulls in a parallel dependency set (pypdf, pytesseract,
  pdf2image, Pillow, pillow-heif) not in `pyproject.toml`.
- **Ignore PaperBrain entirely and design retrieval from a blank page:** throws away a
  design that already answers real household-paperwork questions correctly, including the
  RRF fusion ADR 0002 already committed to.

## Consequences
Retrieval keeps the algorithm PaperBrain already validated instead of re-deriving it, and
picks up its idempotent-ingest and per-page-OCR habits, which the current ingestion worker
spec doesn't yet call out explicitly. It costs a rewrite of every I/O boundary (SQLite →
Postgres, pypdf/Tesseract → Docling, its models → SEA-LION/embeddinggemma) rather than a
straight port, and PaperBrain itself now needs someone to keep it from silently diverging
as a second, unmaintained implementation of the same idea.

## Revisit when
`core/retrieve/`'s hybrid fusion measurably underperforms PaperBrain's on the same
questions, or Docling's parse quality on the corpus turns out worse than pypdf/Tesseract's
— either would be a reason to pull more of PaperBrain's specific choices back in rather
than just its shape.
