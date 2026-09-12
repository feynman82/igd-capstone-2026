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
| **Just want to run it and try it** | [`TRY-PARROT.md`](TRY-PARROT.md) |
| Any agent working here | [`AGENTS.md`](AGENTS.md), then [`CLAUDE.md`](CLAUDE.md) — or just run `/orient` |
| New to the project | [`docs/artefacts/architecture-review.html`](docs/artefacts/architecture-review.html) — open it in a browser |
| Looking for your brief and tasks | [`team/`](team/README.md) |
| Zee | [`team/zee/README.md`](team/zee/README.md), then [`packs/README.md`](packs/README.md) |
| **Rehearsing the demonstration** | [`docs/demo-run-sheet.md`](docs/demo-run-sheet.md) |
| About to open a PR | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Wiring up Notion | [`docs/NOTION.md`](docs/NOTION.md) |
| Setting up a machine | [`FIRST-RUN.md`](FIRST-RUN.md) |

---

## Quick start

```bash
docker compose -f infra/docker-compose.yml up -d     # postgres+pgvector, redis
uv sync --python 3.12 --extra dev
docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot \
  < db/migrations/0001_init.sql                      # no local psql needed

ollama pull hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M   # generation + vision
ollama pull embeddinggemma:300m                                     # embedding
ollama pull hf.co/gpustack/bge-reranker-v2-m3-GGUF:latest           # reranker

uv run python -m corpus.validate corpus/register/batch1.csv   # check a handed-over batch
make corpus-load BATCH=batch1                         # load it into this machine's database
(cd web && npm ci)                                    # first time only
make dev                                              # everything: engine, watcher, worker, screens
```

No `.env` is needed: every default already matches `infra/docker-compose.yml`. Copy
`infra/.env.example` to `.env` only to change a port, a model or the watched folder. The
engine tells the screens which port it got, so those two cannot drift apart.

`make dev` — and `START.cmd`, which is the same thing with a preflight in front of it —
starts four things: the engine on `:8000`, the folder watcher, the ingestion worker with its
nightly sweeps, and the screens on `:3000`. Add `--no-web` to leave the screens to you.

To run the worker on its own — a second window, or a machine where the server is already up:

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
| `scripts/` | The command line: `ask`, `today`, `quarantine`, the watcher, the worker, the Telegram bot, the corpus loader, the benchmark, and the repository generators | Christian |
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
| Orchestration | LangGraph. The checkpointer is `MemorySaver` — see the note below |
| Parsing | Docling (MIT, CPU-capable), with a vision second pass on quarantine |
| Interface | Next.js 15, Tailwind, shadcn/ui |
| Evaluation | Ragas with a locally served judge |

**Two rows in that table are the choice, not yet the code.** Retrieval is dense-only
pgvector today — the RRF fusion and the reranker are Lane B's and are not built, so
`core/graph/baseline.py` stands in behind a port and answer *quality* is not a number
anybody should quote. And the checkpointer is `MemorySaver`, not `PostgresSaver`: the
Postgres one creates its own tables at runtime, which rule 4 forbids in a feature PR, so the
swap is owed to a separate reviewed migration. Both are recorded in
[ADR 0007](docs/adr/0007-the-graph-ships-before-retrieval-and-before-a-checkpoint-table.md).

The target is consumer hardware; fitting the full workflow on an 8 GB GPU remains a
planning estimate. The first demo target is Christian's onboard RTX 4060, without the
external development GPU. Minimum specifications will follow measured quality, latency
and memory use. Measured numbers, and the method, are in
[`eval/results/w1-hardware.md`](eval/results/w1-hardware.md); see
[`docs/RUNNING.md`](docs/RUNNING.md) for startup and qualification.

Two processes. On Windows, double-click [`START.cmd`](START.cmd) — or `make dev` — to start
the engine: the local API, the folder watcher and the ingestion worker, plus a setup page on
`:8000` reporting whether Docker, Ollama and the three models are present. Then `cd web && npm
run dev` and open <http://localhost:3000> for the screens: Today, Ask, Vault and Packs, behind
a local passphrase. Documents dropped into `inbox/` are read automatically.

Step-by-step, written for somebody who has not seen the code:
[`TRY-PARROT.md`](TRY-PARROT.md).

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

All three are conventions. None of them is enforced by GitHub.

---

## `main` is not protected

This repository is private under a personal account, and GitHub does not enforce branch
rulesets there. There is no ruleset, deliberately — a saved one would be inert and would
read like a gate that is not there. So **`git push` to `main` will succeed**, and that is
not the same as permission.

[`CODEOWNERS`](.github/CODEOWNERS) still auto-requests the right reviewer; it just cannot
block a merge. Branch per lane, one vertical slice per PR, get the review, and if you do
land something directly, say so in the team channel the same day. The weekly integration
pass is the only backstop. Reasoning in
[ADR 0010](docs/adr/0010-main-is-unprotected-by-convention.md); the loop itself is in
[`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Working with agents

Every session loads `AGENTS.md` and the skills in `.claude/skills/`, so a Claude Code
session run by any of the five of us behaves the same way. Start with `/orient`; finish
with `/check`. `docs/GRAPHIFY.md` sets up the shared knowledge graph that lets a session
find the relevant part of a five-person repository without reading all of it.
