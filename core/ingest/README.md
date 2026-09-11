# `core/ingest/` — the ingestion worker

**Owner: Christian.** FastAPI + Celery + Redis.

Docling parse and OCR → contextualise chunk → embed → extract typed fields →
idempotent upsert on a SHA-256 of the source bytes.

Capture does not run any of that. It registers the document, puts a message on Redis and goes
back to watching the folder; `core/worker/` reads the message and calls `pipeline.process`.
Five scans dropped at once are five filed lines at once, and the queue is what survives a
restart. See `docs/adr/0008-ingestion-runs-on-a-celery-worker.md`.

The pipeline **forks**, and both lanes commit in one transaction so a reminder can never
disagree with a search result:

- **Retrieval lane** → `chunks` (vector + tsvector)
- **Facts lane** → `facts`, `obligations` (typed rows, each citing a document and page)

## Quarantine is two-stage

Parse failure, OCR confidence below threshold, or schema validation failure routes to the
quarantine queue — surfaced in the interface as "needs your eyes", never silently dropped.

Because the generator is a **vision-language** model, quarantine gets a second pass: the
page *image* goes to the model, which reads pixels rather than the text a parser managed
to recover. Docling is not replaced — it stays faster, cheaper and better on digital PDFs.
Instrument the recovery rate; it is a reportable finding.

## Rules

`facts.document_id` and `facts.page` are `NOT NULL`. There is no code path that writes a
fact without provenance, and adding one is the kind of change that invalidates the
governance chapter.
