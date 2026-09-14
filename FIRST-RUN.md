# First run

Where the repository stands, and what is left to switch on.

**Done:** the repository is on GitHub at `feynman82/igd-capstone-2026` (private), the
local checkout on `sunshine` mirrors it, the knowledge graph is built and committed, the
graphify hooks are installed on that machine, and the setup items below are settled —
collaborators, the Actions permission, and the project board. The Notion hub (item 5) is a
decision, not a setup step, and it has been made: see below.

**`main` is not protected, and will not be.** This repo stays on Christian's personal
GitHub account rather than moving to a Team org, and GitHub does not enforce branch
rulesets on a private repo under a personal account regardless of how they are configured.
A saved-but-inert ruleset is worse than none: it reads like a guardrail on the settings
page while merges land unchecked, so we do not keep one. See
[ADR 0010](docs/adr/0010-main-is-unprotected-by-convention.md).

**What replaces it** is convention, and the convention has to carry the weight alone:
branch per lane, one PR per vertical slice, and the review named in
[`CODEOWNERS`](.github/CODEOWNERS) requested and given before merge. `CODEOWNERS` still
does useful work — it auto-requests the right reviewer — it simply cannot *block* anyone.
The weekly integration pass is where drift gets caught instead.

---

## 1 · Collaborators

**Settings → Collaborators and teams → Add people.**

| Person | GitHub | Role | Status |
|---|---|---|---|
| Yew Mun | `Yewhoo` | Write | Collaborator (accepted) |
| Zee | `fjzeetr-smuigd` | Write | Collaborator (accepted) |
| Siew | `nsiewsiew` | Write | Invite sent, pending |
| Desmond | `strawberries2026` | Write | Invite not yet sent |

`.github/CODEOWNERS` now carries all five real logins — `@feynman82`, `@Yewhoo`,
`@nsiewsiew`, `@fjzeetr-smuigd`, and `@strawberries2026`. No placeholders remain.

## 2 · Branch protection — deliberately not configured

Nothing to switch on here. See the note at the top: rulesets do not enforce on a private
repo under a personal account, so we do not save one. `main` is unprotected and the
discipline is human.

If the repository ever moves to a Team org or goes public, this is the ten-minute change
that becomes worth making — **Settings → Rules → Rulesets → New branch ruleset** on `main`,
requiring a pull request with 1 approval, review from Code Owners, the `check` and `web`
status checks, branches up to date, and force pushes blocked. Until then, do not configure
it: an inert ruleset misleads the next person who reads the settings page.

## 3 · Actions permissions

**Settings → Actions → General → Workflow permissions → Read and write.**
The evaluation workflow commits its results back, and fails silently without this.

## 4 · Project board

**Projects → New project → Board.** Group by **Owner** for standups, by **Week** for the
plan view. The 80 tasks are in `docs/team-tasks.csv`.

Optional — the repository already generates per-member task lists at `team/<name>/tasks.md`,
so the board is a convenience rather than the record. See `docs/NOTION.md` for which
system is the source of truth and why.

## 5 · The Notion hub

**Decided: the PARROT page stays in Yew Mun's workspace.** Christian's Claude connector
stays authenticated to his own (Dy L's Space), so Claude cannot read or write the Notion
page directly. `docs/team-tasks.csv` remains the system of record; Notion is the
human-facing view, updated by hand each week to match the CSV (see "Keeping the two in
sync" in `docs/NOTION.md`). `docs/NOTION.md` still writes up Option A (moving the page) as
the recommended path from before this decision — that section is now historical context,
not the plan.

---

## Setting up a second machine

For everyone who is not Christian:

Only trying PARROT rather than building on it? [`TRY-PARROT.md`](TRY-PARROT.md) is the
shorter path and assumes nothing.

```bash
git clone https://github.com/feynman82/igd-capstone-2026.git
cd igd-capstone-2026

docker compose -f infra/docker-compose.yml up -d     # postgres+pgvector, redis
uv sync --python 3.12 --extra dev

# The database in Docker runs the migration, so no local psql is needed.
docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot \
  < db/migrations/0001_init.sql
docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot \
  < db/migrations/0002_household.sql
docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot \
  < db/migrations/0003_advice.sql

# All three models are required: generation and the image pass, embedding, reranking.
ollama pull hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M
ollama pull embeddinggemma:300m
ollama pull hf.co/gpustack/bge-reranker-v2-m3-GGUF:latest

# knowledge graph
uv tool install graphifyy
graphify install --platform claude     # writes to ~/.claude/, not into this repo
make graph-setup                       # registers the union merge driver
graphify hook install

make check                             # know what green looks like before you change anything
```

No `.env` is required — every default already matches `infra/docker-compose.yml`. Copy
`infra/.env.example` to `.env` only to change a port, a model or the watched folder.

Corpus batches are **not in git** (`corpus/batches/` is gitignored, deliberately). A batch is
handed over by Lane E out of band; drop it in and load it with `make corpus-load BATCH=batch1`.
See "Moving a corpus between machines" in [`docs/RUNNING.md`](docs/RUNNING.md) for why the
database is rebuilt on each machine rather than shared.

Then open Claude Code in the repository and run **`/orient`**.

---

## What is already here

| Path | What it is |
|---|---|
| `AGENTS.md` | The working agreement every coding agent reads first. Eight hard rules. |
| `CLAUDE.md` | What a Claude Code session reads first; points at `AGENTS.md` and the lane briefs. |
| `team/` | One folder per person: their brief, and a task list generated from `docs/team-tasks.csv`. |
| `.claude/skills/` | Six project skills, so a session run by any of the five behaves the same way. |
| `.claude/commands/` | `/orient` `/check` `/handover` `/weekly`. |
| `core/contracts.py` | The pack and module manifests. `never_acts` cannot be set false — the guardrail is enforced by the type, not by review. |
| `db/migrations/0001_init.sql` | The schema. `facts.document_id` and `facts.page` are `NOT NULL`, so no fact can exist without provenance. |
| `db/migrations/0002_household.sql` | Who lives here, what they are called on paper, and which one is you. |
| `db/migrations/0003_advice.sql` | The values a pack calculates with, the owner's consent, and the record of every advice answer. |
| `packs/README.md` | The domain-pack guide written for a non-technical author. This is the file to send Zee. |
| `corpus/` | Desmond's lane: the canon template, the register template, and the validator that gates a handover. No document generation. |
| `docs/GRAPHIFY.md` | The knowledge graph: setup, the merge driver, and what leaves the machine. |
| `docs/NOTION.md` | The workspace decision, the CSV import mapping, and the weekly sync loop. |
| `docs/artefacts/` | Proposal v3, the deck, the architecture review, the interface pack, 13 diagrams, and the original source material. |
| `docs/adr/` | Two decision records and a template. Add one per non-obvious choice. |
| `docs/governance/` | Siew's eight artefacts, with due weeks. |

---

## The first three commits that matter

1. **Confirm `core/contracts.py` and merge it.** Nothing else starts until the contracts
   are on `main`.
2. **Apply the migrations and confirm them.**
   `psql "$DATABASE_URL" -f db/migrations/0001_init.sql`, then `0002_household.sql`, then
   `0003_advice.sql`
3. **Benchmark the workstation** and paste the table into `eval/results/w1-hardware.md`.
   Every VRAM figure in the proposal is currently a planning estimate.

## Send these on day one

- Zee → `team/zee/README.md`, then `packs/README.md`
- Desmond → `team/desmond/README.md`
- Yew Mun → `team/yew-mun/README.md`
- Siew → `team/siew/README.md`

Each sits beside a `tasks.md` containing only their tasks.
