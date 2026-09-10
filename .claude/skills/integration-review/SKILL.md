---
name: integration-review
description: Review a pull request against this repository's contracts, or run the weekly integration pass across lanes. Use when reviewing someone's PR, before merging to main, at the weekly integration session, or when checking whether the lanes have drifted apart.
---

# Integration review

The failure mode of five people and their agents on one repository is not slow progress.
It is five plausible-looking implementations of the same idea, discovered in week 8.

This skill is the pass that prevents that.

## Read first

`AGENTS.md`, `core/contracts.py`, `.github/CODEOWNERS`, `team/README.md`.

## Reviewing a pull request

Work through these in order and stop at the first one that fails — a PR that widens a
contract does not need its test coverage reviewed yet.

**1 · Does it stay in its lane?** Compare the changed paths against `CODEOWNERS`. A PR
touching another lane's directory needs that owner's review, or it needs splitting.

**2 · Does it change a contract?** Any diff to `core/contracts.py` or `db/migrations/`
must be its **own** PR, reviewed before anything depends on it. The most common way a
multi-agent repository degrades is a contract quietly widened to make one feature easier.
If the diff mixes a contract change with a feature, send it back to be split — every time,
including when the change is obviously fine.

**3 · Are generated files in sync?** `python -m packs.build --check` and
`python scripts/build_team_tasks.py --check`. CI runs both, but knowing which gate failed
saves a round trip. A `pack.yaml` committed without its generated files is the usual
cause.

**4 · The eight hard rules.** Read them in `AGENTS.md`; the four an agent will
cheerfully break:
- runtime-generated SQL (module queries are hand-written and parameterised)
- a fact written without `document_id` and `page`
- a new runtime dependency without an ADR
- an import from `web/` or `api/` inside `packs/` or `modules/`

**5 · Is it a vertical slice?** A PR should let somebody do something new. A PR that adds
a layer is hard to review and impossible to demo.

**6 · If it touches retrieval, extraction or the gate:** are the numbers in the body,
with one sentence on why they moved? Numbers absent means not reviewed yet.

**7 · Does the test use corpus fixtures?** Tests use the register in `corpus/register/`
with known ground truth, never live documents.

## The weekly pass — ninety minutes, protected

Not a review of a diff; a review of the repository.

- **Duplicate helpers.** Three agents wrote three date parsers this week. Find them, keep
  one, delete two. This is most of the value of the session.
- **Drift between the pack manifests and the corpus.** `packs.build --check` plus a look
  at whether the register columns still read sensibly.
- **Contract creep.** `git log -p core/contracts.py` since last week. Every change should
  map to an ADR or a decision someone remembers making.
- **Stale task lists.** `python scripts/build_team_tasks.py --check`, and whether the
  statuses in `docs/team-tasks.csv` match reality.
- **The graph.** Regenerate `graphify-out/` and commit it — alone, in its own commit.
  Nobody else commits it; see `docs/GRAPHIFY.md`.
- **What is blocked.** Walk the dependency chain in `team/README.md`. If Zee has not
  committed a pack, Desmond cannot start, and that is this week's only real problem.

## How to give the feedback

Say which rule, point at the file, propose the fix. "This widens `FieldSpec` to make the
insurance pack easier — split the contract change into its own PR and I will review it
first" lands better than "please don't do this", and it tells the agent on the other side
exactly what to do.

Be willing to merge something imperfect that is in its lane and passes the gates. The
gates exist so that judgement can be spent on the things they do not catch.

## Never

- Merge a contract change bundled with a feature
- Merge with `make check` red
- Fix someone's PR yourself instead of telling them what is wrong — it removes the
  feedback loop that makes the next PR better
