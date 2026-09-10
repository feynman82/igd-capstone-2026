# Notion

Notion is where the team looks at the plan. `docs/team-tasks.csv` is where the plan
*lives*. That direction matters: the CSV also generates every `team/<name>/tasks.md`, so
if the two disagree, the CSV wins and Notion gets re-imported.

## Importing the task database

1. In the PARROT page: **/database** → **Import** → **CSV**, and choose
   `docs/team-tasks.csv`.
2. Set the property types — Notion guesses these badly on first import:

| Column | Notion type | Options |
|---|---|---|
| `Task` | Title | — |
| `Owner` | Select | Christian · Yew Mun · Siew · Zee · Desmond · All |
| `Lane` | Select | A. Integration · B. Retrieval and eval · C. Governance · D. Packs and interface · E. Corpus |
| `Week` | Select | W1 … W10 |
| `Due` | Date | — |
| `Type` | Select | Build · Milestone · Write · Review |
| `Done when` | Text | — |
| `Depends on` | Text | — |
| `Status` | Status | Not started · In progress · Done · Blocked |

3. Three views worth making immediately:
   - **Board by Owner** — the standup view
   - **Timeline by Week** — the plan view, grouped by Lane
   - **Table filtered to `Status ≠ Done` and `Week ≤ current`** — what is actually late

## Keeping the two in sync

Once a week, at the integration session:

1. Update `Status` in `docs/team-tasks.csv` to match what Notion says
2. `python scripts/build_team_tasks.py` — regenerates every member's `tasks.md`
3. Commit both

That is the whole loop. Do not edit `team/*/tasks.md` by hand; CI fails on it, for the
same reason it fails on a hand-edited `schemas.py`.

New tasks that came up mid-week get added to the CSV, not only to Notion — otherwise the
repository's view of the plan quietly falls behind and the report is written from the
wrong record.

## Claude's access to the Notion page

The Claude connector is authenticated to the workspace **Dy L's Space**. The PARROT page
sits in a different workspace — its page id begins `734b29c2`, while everything in Dy L's
Space begins `3b0de315`/`3bade315` — so Claude gets a 404 on it and cannot read or write
the database directly.

To change that, open the PARROT page in *its* workspace → **•••** → **Connections** →
add **Claude**, and connect that workspace in Claude's connector settings. Until then the
CSV import above is the path, and it is not a bad one: the repository stays the record,
which is what the report is written from.
