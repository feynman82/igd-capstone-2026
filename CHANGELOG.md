# Changelog

One entry per week, written at the integration session. This is not release notes — it is
the raw material for the report's "what we built and when" section, and it is much easier
to write on the day than in November.

Format: what landed, what moved the numbers, what we decided, what slipped.

## W2 · 9–15 Sep 2026

**Landed**
- Repository framework: per-member briefs and generated task lists under `team/`
- Six project skills and four slash commands in `.claude/`, so every session behaves the same
- Contributing guide, ADR index and template, issue templates
- Knowledge graph built and committed; union merge driver wired so graph.json does not
  conflict between committers

**Decided**
- Member folders hold briefs and task lists only; work stays in the functional
  directories so the generated-file chain and `CODEOWNERS` keep working
- Task lists are generated from `docs/team-tasks.csv`, the same file imported into Notion

**Slipped**
- Semantic (markdown) pass over the graph still to run — the committed graph is the
  free code pass plus community labels.

## W1 · 2–8 Sep 2026

**Landed**
- Initial scaffold: `core/contracts.py`, the migration, corpus tooling, both pack manifests
- Pack codegen: one authored `pack.yaml` per pack, everything else generated and CI-gated

**Decided**
- Generation model swapped to `Qwen-SEA-LION-v4-4B-VL` — the whole stack now fits on one
  8 GB card, so the demo machine and the machine the product claims to run on are the same
  machine. Being vision-language also makes the quarantine queue a second pass rather than
  a dead end.

**Slipped**
- Week-1 hardware benchmark not yet run. Every VRAM figure in the proposal is still a
  planning estimate.
