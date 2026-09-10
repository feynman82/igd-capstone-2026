# Roadmap

The goal isn't a search box. It's getting time back: paperwork that files
itself, remembers its own deadlines, and tells you before something lapses.

## Phase 1 — Retrieval (done)

Everything readable, everything askable, with citations.

- [x] Ingest PDF / scan / photo / docx / txt / eml, idempotent by hash
- [x] Paragraph-aware chunking, per-page OCR fallback
- [x] Hybrid BM25 + vector retrieval with RRF
- [x] Grounded answers with `[n]` citations
- [ ] `pb ingest --watch` — a LaunchAgent that indexes a drop folder on change
- [ ] Small eval set: ~30 real questions with expected source files, so
      retrieval changes can be measured instead of vibed

## Phase 2 — Facts

Turn documents into rows. Populate `facts` with the local LLM, using a strict
JSON schema per document type, every row pointing back at its source chunk.

- Extract: vendor, amount, currency, date, category (receipts); policy number,
  insurer, premium, renewal date, coverage limits (insurance); assessment year,
  amount payable, due date (tax); event name, date, deadline (school).
- Re-run `pb classify` to upgrade the regex `doc_type` / `doc_date` guesses.
- New commands: `pb spend --month 2026-03`, `pb policies`, `pb due --next 60`.
- Everything stays verifiable: no fact without a chunk id.

## Phase 3 — Reminders

The `reminders` table plus a scheduler.

- Derive reminders from facts (renewal dates, tax due dates, consent deadlines)
  with a per-type lead time.
- Surface via `pb agenda`, macOS notifications, and optional one-way export to a
  local `.ics` file the Calendar app subscribes to — still no cloud.
- Dismiss / snooze / done, so it stops nagging about handled things.

## Phase 4 — Agent

Only after facts and reminders are trustworthy.

- A tool-using loop over the local model: search documents, query facts, create
  reminders, draft the reply to the insurer.
- Multi-step questions: "did the renewal premium go up versus last year, and by
  how much" — needs two facts and a comparison, not one retrieval.
- A quiet weekly digest: what arrived, what's due, what looks wrong.

## Explicitly not doing

- Cloud sync or a mobile app. The threat model is the whole point.
- A hosted vector database. See ARCHITECTURE.md.
- Autonomous actions that spend money or send mail. It drafts; you send.
