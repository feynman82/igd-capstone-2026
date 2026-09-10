# First run

This directory is a git repository with its history already in place. The remote
`feynman82/igd-capstone-2026` exists and is empty.

## 1. Push

```bash
cd path/to/igd-capstone-2026
git remote add origin https://github.com/feynman82/igd-capstone-2026.git
git push -u origin main
```

If the remote already has a commit (a README created with the repository), rebase onto
it once rather than force-pushing:

```bash
git pull --rebase origin main
git push -u origin main
```

## 2. Turn on the guardrails, while the repo is still empty

Doing this in week 1 costs nothing. Doing it in week 6 feels like an accusation.

**Settings → Collaborators** — add Yew Mun, Siew, Zee and Desmond, then replace the four
placeholder handles in `.github/CODEOWNERS` with their real GitHub usernames and push.

**Settings → Branches → Add branch ruleset** for `main`:

- Require a pull request before merging — 1 approval
- Require review from Code Owners
- Require status checks to pass — add `check` and `web` once CI has run once
- Require branches to be up to date before merging
- Block force pushes

**Settings → Actions → General** — set workflow permissions to read and write, so the
evaluation workflow can commit its results.

**Projects → New project → Board** — one column per lane (Christian, Yew Mun, Siew, Zee,
Desmond). Group by owner for standups, by week for the plan view. The 80 tasks are in
`docs/team-tasks.csv`.

## 3. Install graphify

Only you do this, and only from a local checkout — it parses files on disk and installs
git hooks, so it cannot be started from the GitHub web interface or the API.

```bash
uv tool install graphifyy
graphify install     # then check `git diff AGENTS.md` and revert anything it overwrote
graphify .
graphify hook install
git add graphify-out/graph.json graphify-out/GRAPH_REPORT.md
git commit -m "Add knowledge graph"
```

Everyone else runs `graphify update .` locally and leaves the output uncommitted. Full
detail, including why only one person commits it, is in `docs/GRAPHIFY.md`.

## 4. The self-hosted runner, when you get to week 3

The golden set needs Ollama and a real model, so it cannot run on GitHub's runners.
Settings → Actions → Runners → New self-hosted runner, on the Legion, with the label `gpu`.
`.github/workflows/eval.yml` already targets `[self-hosted, gpu]`.

Until then, run `make eval` locally and commit the JSON under `eval/results/` — the workflow
supports both paths.

## What is already here

| Path | What it is |
|---|---|
| `AGENTS.md` | The working agreement every coding agent reads first. Read it before your first Antigravity session. |
| `core/contracts.py` | The pack and module manifests, as Pydantic. `never_acts` cannot be set to false — the guardrail is enforced by the type, not by review. |
| `db/migrations/0001_init.sql` | The schema. `facts.document_id` and `facts.page` are NOT NULL, so no fact can exist without provenance. |
| `corpus/` | Desmond's lane: the household canon template, the register template, and the validator that gates a handover. No document generation. |
| `docs/TEAM.md` | The five lanes, the presentation split, the swap rules. |
| `docs/team-tasks.csv` | 80 tasks, ready to import into Notion. |
| `docs/adr/` | Two decision records to start. Add one per non-obvious choice. |
| `team/` | One folder per person: their brief, and a task list generated from `docs/team-tasks.csv`. |
| `.claude/skills/`, `.claude/commands/` | Six project skills and four slash commands, so every session behaves the same. Start any session with `/orient`. |
| `packs/README.md` | Zee's lane, written for a non-technical author. This is the file to send her. |
| `docs/GRAPHIFY.md` | The shared knowledge graph: setup, the one-committer rule, what leaves the machine. |
| `docs/artefacts/` | The proposal, the deck, the architecture review, the interface pack, the diagrams and the original source material. |
| `CLAUDE.md` | What a Claude Code session reads first. Points at `AGENTS.md` and the lane files. |
| `.claude/settings.json` | Permission allowlist so agent sessions can run `make check` without prompting, and cannot push or commit. |
| `packs/_template/`, `modules/_template/` | Copy these to start a pack or a module. |

## First three commits, in order

1. **Fill in `core/contracts.py` if anything is missing, and merge it.** Nothing else starts
   until the contracts are on `main`.
2. **Apply the migration and confirm it.** `psql "$DATABASE_URL" -f db/migrations/0001_init.sql`
3. **Benchmark the workstation** and paste the table into an ADR. Every VRAM number in the
   proposal is currently an estimate. Pull the model first:
   `ollama pull hf.co/aisingapore/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`

## Send these three links on day one

- Zee → `team/zee/README.md`
- Desmond → `team/desmond/README.md`
- Yew Mun → `team/yew-mun/README.md`, Siew → `team/siew/README.md`

Each of those sits beside a `tasks.md` with only their tasks in it.
