# Architecture

## Constraints that drive everything

1. **Fully offline.** Personal paperwork is the most sensitive data most people
   own. No embeddings API, no hosted vector store, no crash reporter.
2. **Runs on one MacBook Pro** (64 GB unified memory, 18-core CPU / 20-core
   GPU). Comfortable for a 14B chat model plus a small embedder resident at the
   same time.
3. **Survives neglect.** This is a tool used in bursts — a receipt drop here, a
   tax question in April. It must work after three months of not being touched,
   without a migration dance or a stale service.

Those rule out a lot: no Docker, no Postgres/pgvector, no Chroma server, no
LangChain layer to break on upgrade. What's left is a single SQLite file, a
handful of stdlib modules, numpy, and Ollama.

## Data flow

```
file ──extract──> pages[] ──chunk──> chunks[] ──embed──> SQLite
                                                            │
question ──┬─ BM25 (FTS5) ───────rank A──┐                  │
           └─ cosine (numpy) ────rank B──┴─ RRF ─> top-k ───┘
                                                    │
                                      grounded prompt -> Ollama chat -> answer + citations
```

## Decisions

**SQLite for everything.** Documents, chunks, the FTS5 index and the vectors
live in one file that can be copied, backed up by Time Machine, or deleted to
forget everything. FTS5 is compiled into the SQLite that ships with macOS and
with Python, so keyword search costs zero dependencies.

**Vectors as BLOBs, scored in numpy.** Embeddings are L2-normalised at write
time, so cosine similarity is a single matrix-vector product. At 20k chunks
that's a 20k×768 float32 matrix — 60 MB, scored in a few milliseconds. An ANN
index (sqlite-vec, faiss, hnswlib) only starts to pay off a couple of orders of
magnitude beyond a household's paperwork, and each one is a native wheel that
can break on an OS upgrade. Revisit if the corpus ever passes ~200k chunks.

**Hybrid retrieval, not embeddings alone.** Half of all paperwork questions hinge
on an exact string — a policy number, an amount, a vendor. Embedding models
smear those. BM25 nails them and is nearly free. RRF fuses the two rankings
without needing the two scores to be on the same scale.

**OCR is per page, not per file.** A 30-page policy usually has 29 text pages
and one scanned signature page. Rasterising the whole document to OCR it would
be slow and would *lose* quality on the pages that already have perfect text.
So each page is checked for a text layer and only the empty ones get OCR'd.

**Hash-based idempotency.** `pb ingest` is re-runnable and cheap: a file whose
sha256 matches what's stored is skipped before extraction. That makes it safe to
put on a schedule, and makes "re-index everything" a normal operation rather than
a scary one.

**Chunking respects paragraphs.** A receipt's line items and a policy's clause
must not be cut mid-item, or retrieval returns half an amount. Splits happen at
blank lines first, with a hard character cut only inside an unusually long
paragraph, plus a 200-char stitch from the previous chunk for context.

**The prompt refuses to guess.** For paperwork, a confidently invented renewal
date is worse than "I don't have that document". The system prompt forbids
outside knowledge, requires `[n]` citations, and requires verbatim figures.

## Failure modes, handled

| Situation | Behaviour |
|---|---|
| Ollama not running | `OllamaUnavailable` with the exact fix; ingest still stores text, embeds later |
| Tesseract/poppler missing | Text-layer PDFs still ingest; scanned pages reported per file |
| Embedding model swapped | Dimension mismatch detected; vector search skipped, BM25 carries the query |
| File modified after ingest | Hash differs, document and its chunks are replaced atomically |

## Extension points

- `documents.doc_type` / `doc_date` are heuristic today (regex). A `pb classify`
  pass can upgrade them with the local LLM without touching the schema.
- `facts` is where structured extraction lands (amounts, due dates, policy
  numbers), each row pointing back at the chunk it came from so nothing is
  unverifiable.
- `reminders` is what the scheduling layer reads. Keeping it in the same
  database means a reminder can always be traced to its source document.
