# Notion

Notion is where the team looks at the plan. `docs/team-tasks.csv` is where the plan
*lives*. That direction matters: the CSV also generates every `team/<name>/tasks.md`, so
if the two disagree the CSV wins and Notion gets re-imported.

---

## The access problem, and the one decision that fixes it

The PARROT page sits in **Yew Mun's** Notion workspace. Christian's Claude connector is
authenticated to **Dy L's Space**, so Claude gets a 404 on the page and cannot read or
write the task database.

**Claude supports one Notion workspace per account.** Connecting a second is an open
feature request, not a setting — the only way to change workspaces today is to disconnect
in *Settings → Connectors* and reconnect, and that disconnection applies to every session.
So this is not a permissions problem that sharing the page will solve. It is a question of
which single workspace Christian's Claude should be pointed at.

### Option A — move the hub into Christian's workspace ✅ recommended

Christian is the integration lead and the one orchestrating with Claude, so the project
hub belongs where his tooling already is. Dy L's Space also holds his other active work,
which he would otherwise lose Claude access to under Option B.

**Yew Mun does this:**

1. Open the **IGD Project PARROT** page.
2. `•••` (top right) → **Add connections** is not the step — skip it. Instead: `•••` →
   **Move to** → and if Christian's workspace is not in the dropdown, first invite him:
   **Settings → People → Add members** → `deyao.liao@gmail.com`. A guest invite on the
   single page is enough; he does not need to join the whole workspace.
3. Once Christian appears as a member or guest, `•••` → **Move to** → choose
   **Dy L's Space** → **I understand, duplicate**.

**Then Christian:** re-share the page back to the team — `Share` → invite Yew Mun, Siew,
Zee and Desmond as guests with **Can edit**.

> **Do this now rather than in October.** Notion warns that a cross-workspace move can
> break links, database relations, permissions and page history. Right now the page holds
> almost nothing, so the move costs nothing. In week 8, with a populated task database and
> six weeks of meeting notes, it will not be free.

### Option B — Christian switches his connector to Yew Mun's workspace

*Settings → Connectors → Notion → Disconnect → Connect →* choose Yew Mun's workspace
during the Notion authorisation. He must be a member of it first.

The cost is real: Claude loses access to Dy L's Space, which carries his other live
projects. Only worth it if the team is firmly committed to Yew Mun's workspace as the
system of record.

### Option C — leave Notion as a human-only view

Import the CSV, keep Claude out of Notion entirely, and let the repository be the record.
Zero setup, and honestly not a bad outcome: the report is written from the repository, not
from Notion. This is the fallback if A and B both stall.

---

## Importing the task database

Once the hub is somewhere workable:

1. On the PARROT page: **/database** → **Import** → **CSV**, and choose
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
   - **Timeline by Week**, grouped by Lane — the plan view
   - **Table filtered to `Status ≠ Done` and `Week ≤ current`** — what is actually late

---

## Keeping the two in sync

Once a week, at the integration session:

1. Update `Status` in `docs/team-tasks.csv` to match what Notion says
2. `python scripts/build_team_tasks.py` — regenerates every member's `tasks.md`
3. Commit both

That is the whole loop. Do not edit `team/*/tasks.md` by hand; CI fails on it, for the
same reason it fails on a hand-edited `schemas.py`.

New tasks that came up mid-week get added to the CSV, not only to Notion — otherwise the
repository's view of the plan quietly falls behind, and the report is written from the
wrong record.

Once Claude can see the workspace, step 1 becomes something Claude does rather than
something you do.
