---
description: Run the full gate — generated files in sync, lint, types, tests
---

Run the repository's definition of done and report what failed, in plain language.

```bash
make check
```

That runs, in order: `packs.build --check` (pack manifests vs their generated files),
`scripts/build_team_tasks.py --check` (task lists vs the master CSV), `ruff check`,
`ruff format --check`, `mypy core modules corpus`, and `pytest -q`.

For each failure, say which gate failed and what the fix is. The two staleness gates are
almost always fixed by running the generator and committing the result — never by editing
a generated file. Do not fix lint by widening a type or adding an ignore comment without
saying so explicitly.
