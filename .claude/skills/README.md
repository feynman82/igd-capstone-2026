# Project skills

Skills committed to this repository, so that a Claude Code session run by any of the five
of us behaves the same way. They encode this project's rules rather than general advice —
which is why they live here and not in anyone's personal setup.

| Skill | Whose lane | What it does |
|---|---|---|
| `authoring-a-domain-pack` | Zee | Walks a pack from proposal to committed YAML, stopping for your answer at each step. Written for a non-technical author. |
| `filling-the-corpus-register` | Desmond | Register-first discipline, the validator, the two rules that cannot bend, and the adversarial half of the lane. |
| `running-the-eval-harness` | Yew Mun | Running Ragas, the three golden sets, the targets, one-variable-per-run, and how to report a change. |
| `writing-a-governance-artefact` | Siew | The six deliverables, where each claim is enforced in code, and the 22989-vs-5338 distinction. |
| `writing-an-adr` | Anyone | The format, what earns one, and why you supersede rather than rewrite. |
| `integration-review` | Christian | Reviewing a PR against the contracts, and the weekly ninety-minute pass. |

## Slash commands

In `.claude/commands/`:

| Command | What it does |
|---|---|
| `/orient` | Reads `AGENTS.md` and your lane brief, then tells you what you may touch and what your next task is. Run this first in a new session. |
| `/check` | Runs `make check` and explains what failed in plain language. |
| `/handover` | Writes a handover note so the next session starts where this one stopped. |
| `/weekly` | The weekly integration pass across all five lanes. |

## Using them

A skill fires when the work matches its description, or you can name it: `/authoring-a-domain-pack`.

If you are new to the repository, start with `/orient`.

## Changing them

A skill is part of the repository's contract with its agents, in the same way `AGENTS.md`
is. Change one in its own pull request, with a sentence on what behaviour you are trying
to change — not bundled into a feature.
