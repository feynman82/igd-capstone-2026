# First run

Where the repository stands, and what is left to switch on.

**Done:** the repository is on GitHub at `feynman82/igd-capstone-2026` (private), the
local checkout on `sunshine` mirrors it, the knowledge graph is built and committed, and
the graphify hooks are installed on that machine.

**Not done:** collaborators, branch protection, the Actions permission, the project board,
and the Notion hub. Those are the five things below, and all but the last are three
minutes each in GitHub settings.

---

## 1 · Collaborators

**Settings → Collaborators and teams → Add people.**

| Person | GitHub | Role |
|---|---|---|
| Yew Mun | `Yewhoo` | Write |
| Siew | *handle needed* | Write |
| Zee | *handle needed* | Write |
| Desmond | *handle needed* | Write |

`.github/CODEOWNERS` already carries `@feynman82` and `@Yewhoo`. The other three are still
the placeholders `@siew`, `@zee`, `@desmond` — **a pull request touching their paths cannot
request a review until those are real logins**, so replace each one as its handle arrives.
It is a one-line commit:

```bash
sed -i 's/@zee/@theirRealHandle/g' .github/CODEOWNERS
git commit -am "CODEOWNERS: Zee's real handle" && git push
```

## 2 · Branch protection

**Settings → Rules → Rulesets → New branch ruleset**, targeting `main`:

- Require a pull request before merging — **1 approval**
- Require review from **Code Owners**
- Require status checks to pass — add `check` and `web` once CI has run once
- Require branches to be up to date before merging
- Block force pushes

Do this while the repository is still young. Doing it in week 6 feels like an accusation;
doing it now is just how the repository works.

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

The PARROT page is in Yew Mun's workspace; Christian's Claude connector is authenticated
to his own. Claude allows one Notion workspace per account, so this needs a decision
rather than a permission change.

**`docs/NOTION.md` has the three options and the exact steps.** The short version: have
Yew Mun move the page into Christian's workspace while it is still nearly empty, because
a cross-workspace move breaks relations and page history and that cost only grows.

---

## Setting up a second machine

For everyone who is not Christian:

```bash
git clone https://github.com/feynman82/igd-capstone-2026.git
cd igd-capstone-2026

cp infra/.env.example .env
docker compose -f infra/docker-compose.yml up -d     # postgres+pgvector, redis
uv sync
psql "$DATABASE_URL" -f db/migrations/0001_init.sql
ollama pull hf.co/aisingapore/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M

# knowledge graph
uv tool install graphifyy
graphify install --platform claude     # writes to ~/.claude/, not into this repo
make graph-setup                       # registers the union merge driver
graphify hook install

make check                             # know what green looks like before you change anything
```

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
2. **Apply the migration and confirm it.**
   `psql "$DATABASE_URL" -f db/migrations/0001_init.sql`
3. **Benchmark the workstation** and paste the table into `eval/results/w1-hardware.md`.
   Every VRAM figure in the proposal is currently a planning estimate.

## Send these on day one

- Zee → `team/zee/README.md`, then `packs/README.md`
- Desmond → `team/desmond/README.md`
- Yew Mun → `team/yew-mun/README.md`
- Siew → `team/siew/README.md`

Each sits beside a `tasks.md` containing only their tasks.
