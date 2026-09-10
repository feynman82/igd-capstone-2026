---
description: Run the weekly integration pass across all five lanes
---

Use the `integration-review` skill and run the weekly pass. Report findings; change
nothing without asking.

Work through:

- `git log --oneline --since="1 week ago"` — what actually landed
- Duplicate helpers written by different lanes this week
- `git log -p core/contracts.py --since="1 week ago"` — contract creep; every change
  should map to an ADR
- `python -m packs.build --check` and `python scripts/build_team_tasks.py --check`
- Whether `docs/team-tasks.csv` statuses match what the commits say happened
- The dependency chain in `team/README.md` — who is blocked on whom right now

End with **one** sentence naming the single thing most worth fixing this week, and a
reminder to regenerate `graphify-out/` in its own commit.
