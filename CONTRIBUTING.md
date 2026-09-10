# Contributing

Five people and their coding agents on one repository, for ten weeks. These are the
rules that keep that from turning into five implementations of the same idea.

The full working agreement is [`AGENTS.md`](AGENTS.md) — every agent reads it, and so
should you. This file is the human-facing short version.

## Before your first commit

1. Read `AGENTS.md`.
2. Read your brief in [`team/`](team/README.md) and your task list beside it.
3. Run `make check` on a clean checkout, so you know what green looks like.
4. In a Claude Code session, run `/orient`.

## The loop

```bash
git switch -c <lane-letter>/<short-slug>     # e.g. d/insurance-pack-fields
# work
make check
git push -u origin HEAD
# open a PR, fill in the template
```

**One vertical slice per pull request.** A PR should let somebody do something new, not
add a layer. If you cannot describe it as "now you can X", it is probably two PRs or none.

**Stay in your directories.** [`CODEOWNERS`](.github/CODEOWNERS) maps each path to the
person who reviews it. A PR that touches another lane needs that owner's review.

**Contracts are their own PR.** A change to `core/contracts.py` or `db/migrations/` is
reviewed on its own, before anything depends on it. Never bundled with a feature — this
one is enforced by review every time, including when the change is obviously fine.

## Generated files

Three sets of files are generated and must be committed alongside their source:

| Generated | From | Command |
|---|---|---|
| `packs/*/schemas.py`, `corpus/register/*_columns.csv`, `docs/field-dictionary.md` | `packs/*/pack.yaml` | `python -m packs.build` |
| `team/*/tasks.md` | `docs/team-tasks.csv` | `python scripts/build_team_tasks.py` |

CI fails if either is stale. Never hand-edit a generated file — the fix is always to
change the source and regenerate.

## If it touches retrieval, extraction or the grounding gate

Run `make eval-quick` and paste the numbers into the PR body with **one sentence on why
they moved** — a mechanism, not a restatement of the delta. Change one variable at a
time; a run that changed three things has told you nothing about any of them.

## Decisions

A non-obvious choice gets an ADR in [`docs/adr/`](docs/adr/README.md). A new runtime
dependency requires one. Use the `writing-an-adr` skill.

## When you are unsure

Open an issue with the **Decision** template rather than inventing a second way of doing
something that already has one way. A question costs five minutes; a divergence
discovered in week 8 costs a weekend.
