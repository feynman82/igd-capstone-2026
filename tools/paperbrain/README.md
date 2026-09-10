# PaperBrain

A fully local, private brain for your personal paperwork — receipts, insurance
policies, tax notices, school letters. Nothing leaves your Mac: SQLite on disk,
Ollama for embeddings and generation, no API keys, no cloud, no telemetry.

Phase 1 (this repo) is the retrieval layer: get every document in, and be able
to ask it anything. Tracking, reminders and scheduling build on top of it — the
`facts` and `reminders` tables are already in the schema for that.

## Setup

```bash
cd ~/Documents/paperbrain

# 1. Ollama (once)
brew install ollama tesseract poppler
ollama serve &                      # or launch the Ollama.app
ollama pull nomic-embed-text        # ~275 MB, the embedder
ollama pull qwen2.5:14b-instruct    # ~9 GB, the answerer

# 2. Python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Check everything is wired up
./pb init
```

`pb doctor` tells you exactly what's missing if a step didn't take.

## Use

```bash
./pb add ~/Documents/Paperwork        # register a folder (repeatable)
./pb ingest                           # extract, chunk, embed — idempotent
./pb docs                             # what's in the library

./pb search "water damage"            # excerpts only, no model, instant
./pb ask "when does my home policy renew and what does it cost?"
./pb ask "how much GST did I pay at supermarkets in March?"
```

Re-run `./pb ingest` any time — files whose contents haven't changed are
skipped by hash, so it's a cheap cron job.

## What it handles

| Input | How |
|---|---|
| PDFs with a text layer | pypdf, exact |
| Scanned PDFs | auto-detected per page, rasterised and OCR'd |
| Receipt photos, `.HEIC` | Tesseract OCR |
| `.docx`, `.txt`, `.md`, `.csv`, `.eml` | direct |

## How retrieval works

Every question runs two searches and fuses them:

- **BM25** over SQLite FTS5 — catches literal tokens: `AIA-HC-7741928`, `$66.60`,
  a vendor name.
- **Dense vectors** — 768-dim `nomic-embed-text`, cosine over a normalised
  matrix in numpy. Catches paraphrase: "flooding from a pipe" → "water damage".

They're combined with Reciprocal Rank Fusion, so neither needs a calibrated
score. The top excerpts go to the chat model under a strict prompt: answer only
from the excerpts, cite `[n]`, and say so when the answer isn't there.

Exhaustive cosine over the whole corpus sounds naive and isn't — a few tens of
thousands of chunks scores in milliseconds on this machine, and it avoids a
native ANN extension that would complicate every future `pip install`.

## Layout

```
pb                    entry point (no install needed)
paperbrain/
  config.py           paths, models, chunking + retrieval knobs
  db.py               schema, FTS5 triggers, vector (de)serialisation
  extract.py          file -> text, with OCR fallback per page
  chunk.py            paragraph-aware chunking with overlap
  ollama.py           stdlib-only Ollama client
  ingest.py           walk, hash, extract, chunk, embed
  retrieve.py         BM25 + vectors + RRF
  ask.py              grounded prompt and citations
  cli.py              the `pb` commands
docs/ARCHITECTURE.md  design decisions and why
docs/ROADMAP.md       phases 2-4: facts, reminders, agent
```

## Privacy

- The only network call is to `127.0.0.1:11434`.
- The database lives at `~/.paperbrain/paperbrain.db`; delete it to forget
  everything. Your original files are never modified or moved.
- `.gitignore` excludes `*.db` — don't commit your paperwork index.
