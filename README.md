# igd-capstone-2026

**Working name: PARROT.** A local-first household RAG platform. No commercial name yet —
`parrot` appears in module and variable names as an internal identifier only.

SMU Industry Graduate Diploma, *AI in the Digital Economy* — Integrated Learning Project,
September to November 2026. Supervisors: Prof. Venky Shankararaman, Prof. Gary Pan.

---

## What it is

A household's documents — payslips, policy schedules, renewal notices, receipts — are
photographed with a phone and filed automatically. The assistant answers questions about
them from the documents themselves, on the user's own machine, and shows which document
and which page every answer came from. When the evidence does not cover the question, it
says so rather than guessing.

**The RAG core is the platform.** Everything else is an expansion along one of two
orthogonal axes:

- **Capability modules** — Reminder, Alert, Tracker. They read typed rows and never see
  the interface.
- **Domain packs** — Tax and Reliefs, Insurance and Coverage, and nine more specified but
  deferred. A pack is a YAML file describing what a kind of document is and what is
  printed on it.

Two packs and two modules are built for the MVP, which is the smallest thing that
demonstrates both axes.

---

## Where to start

| You are | Read |
|---|---|
| Any agent working here | [`AGENTS.md`](AGENTS.md), then [`CLAUDE.md`](CLAUDE.md) — or just run `/orient` |
| New to the project | [`docs/artefacts/architecture-review.html`](docs/artefacts/architecture-review.html) — open it in a browser |
| Looking for your brief and tasks | [`team/`](team/README.md) |
| Zee | [`team/zee/README.md`](team/zee/README.md), then [`packs/README.md`](packs/README.md) |
| About to open a PR | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Wiring up Notion | [`docs/NOTION.md`](docs/NOTION.md) |
| Setting up a machine | [`FIRST-RUN.md`](FIRST-RUN.md) |

---

## Quick start

```bash
cp infra/.env.example .env
docker compose -f infra/docker-compose.yml up -d     # postgres+pgvector, redis
uv sync                                              # or: pip install -e ".[dev]"
psql "$DATABASE_URL" -f db/migrations/0001_init.sql
ollama pull hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M
python -m corpus.validate corpus/register/batch1.csv  # check a handed-over batch
make dev                                             # setup page on :8000, watcher and worker
```

`make dev` starts three things: the setup page, the folder watcher and the ingestion worker
with its nightly sweeps. To run the worker on its own — a second window, or a machine where
the server is already up:

```bash
uv run python scripts/worker.py --beat
```

---

## Where things live

| Path | What | Owner |
|---|---|---|
| `core/contracts.py` | The pack and module manifests. **Changing this needs its own reviewed PR.** | Christian |
| `core/graph/` | LangGraph runtime: router, grounding gate, answer node | Christian |
| `core/adapters/` | Capture adapters: watched folder, Telegram, (WhatsApp, Drive) | Christian |
| `core/ingest/` | Ingestion worker, extraction, two-stage quarantine, idempotency | Christian |
| `core/retrieve/` | Hybrid search, RRF fusion, reranking, score floor | Yew Mun |
| `modules/` | Capability modules: reminder, alert, (tracker) | Christian |
| `packs/` | Domain packs. One authored `pack.yaml` each; everything else generated | Zee |
| `grounding/` | Authoritative reference corpora, with provenance in `sources.yaml` | Zee, reviewed by Siew |
| `web/` | Next.js 15 interface | Zee |
| `corpus/` | The document register (ground truth) and its validator | Desmond |
| `eval/` | Golden sets, Ragas harness, committed results | Yew Mun |
| `docs/governance/` | PDPA, ISO, IMDA artefacts | Siew |
| `team/<name>/` | Each person's brief and their generated task list | — |
| `.claude/` | Project skills and slash commands every session loads | Christian |
| `scripts/` | Repository generators — currently the task-list builder | Christian |
| `docs/artefacts/` | Proposal, deck, diagrams, review, source material | Christian |
| `docs/adr/` | Architecture decision records — one per non-obvious choice | anyone |

---

## The stack, in one table

| Layer | Choice |
|---|---|
| Datastore | PostgreSQL 17 + pgvector. **One database.** Chunks, facts, obligations, agent state and the registry |
| Retrieval | pgvector HNSW + Postgres full-text, fused with reciprocal rank fusion |
| Reranking | `bge-reranker-v2-m3` |
| Embeddings | EmbeddingGemma-300M, 768 dimensions |
| Generation | `Qwen-SEA-LION-v4-4B-VL` — AI Singapore, MIT, vision-language, English plus seven SEA languages |
| Orchestration | LangGraph with a Postgres checkpointer |
| Parsing | Docling (MIT, CPU-capable), with a vision second pass on quarantine |
| Interface | Next.js 15, Tailwind, shadcn/ui |
| Evaluation | Ragas with a locally served judge |

The target is consumer hardware; fitting the full workflow on an 8 GB GPU remains a
planning estimate. The first demo target is Christian's onboard RTX 4060, without the
external development GPU. Minimum specifications will follow measured quality, latency
and memory use. See [`docs/RUNNING.md`](docs/RUNNING.md) for startup and qualification.

On Windows, double-click [`START.cmd`](START.cmd). It currently opens the local setup
page; document ingestion, questions and the product interface are still being built.

---

## Authoring a pack

Full guide for non-technical authors in [`packs/README.md`](packs/README.md); technical
detail in `docs/PACK_AUTHORING.md`. In short: edit one YAML, run `python -m packs.build`,
commit the source and the generated files together.

```bash
python -m packs.build                        # schemas, register headers, field dictionary
python scripts/build_team_tasks.py           # per-member task lists from the master CSV
make check                                   # both staleness gates, plus lint, types, tests
```

A field name written in `pack.yaml` becomes three things at once: the attribute on the
extraction model, the `facts.key` it is stored under, and **the column header in the
corpus register**. Generating that third one from the same file is what stops the pack
and the corpus drifting apart — a failure that otherwise surfaces as a silently zero
evaluation score in week 8.

---

## The three rules that matter

1. **Contracts before code.** A change to `core/contracts.py` or `db/migrations/` is its
   own PR, reviewed before any code depends on it.
2. **Numbers come from Postgres, never from the model.** Dates, amounts and policy
   numbers are read from typed columns. The model phrases the sentence around them.
3. **`pack.yaml` is the only place a field name is written down**, and
   `docs/team-tasks.csv` the only place a task is. Everything else is generated from them.

---

## Working with agents

Every session loads `AGENTS.md` and the skills in `.claude/skills/`, so a Claude Code
session run by any of the five of us behaves the same way. Start with `/orient`; finish
with `/check`. `docs/GRAPHIFY.md` sets up the shared knowledge graph that lets a session
find the relevant part of a five-person repository without reading all of it.
