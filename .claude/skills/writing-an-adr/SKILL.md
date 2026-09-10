---
name: writing-an-adr
description: Write an architecture decision record for this repository. Use when a non-obvious technical choice is made, when adding a runtime dependency (which AGENTS.md requires an ADR for), when a decision is being revisited, or when someone asks why something was built a particular way.
---

# Writing an ADR

An ADR records **why**, at the moment the reasoning is still in someone's head. Six weeks
later nobody remembers whether Postgres-only was a considered decision or an accident,
and the difference matters when a supervisor asks.

`AGENTS.md` requires one for any new runtime dependency.

## Read first

`docs/adr/0001-*.md` and `docs/adr/0002-one-postgres.md` — both are short, and both show
the tone. Then `AGENTS.md`.

## Format

`docs/adr/NNNN-short-slug.md`, four digits, next number in sequence.

```markdown
# NNNN · <The decision, as a statement not a question>

- **Status:** Proposed | Accepted | Superseded by [NNNN](NNNN-slug.md)
- **Date:** YYYY-MM-DD
- **Decider:** <name>

## Context

What forced a choice. The constraint, not the background. Two or three sentences.

## Decision

What we are doing, in the present tense and the active voice.

## Alternatives considered

| Option | Why not |
|---|---|
| ... | ... |

At least two, and each rejection needs a reason that would survive being read back.
"Too complex" is not a reason. "Adds a second datastore, so a household question spanning
chunks and facts loses ACID guarantees" is.

## Consequences

What this makes easy, and what it makes hard. **Both.** An ADR with only benefits is a
sales document.

## Revisit when

The condition under which this should be reopened. Not a date — a trigger.
```

## What earns an ADR

- A new runtime dependency (required by `AGENTS.md`)
- Choosing between two viable technologies
- A constraint that will look arbitrary later: the 16K context cap, the abstain floor,
  invented-issuers-only in the corpus
- A deliberate omission: why the Tracker module is specified and not built, why the
  Actions module is out of scope
- Anything a supervisor is likely to ask "why did you do it that way" about

## What does not

- Style choices covered by ruff
- Anything that only affects one function
- A decision with one option

## Rules

**Never rewrite an accepted ADR.** Supersede it: write a new one, set the old one's
status to `Superseded by NNNN`, and link both ways. The trail of superseded decisions is
itself evidence for the report — it shows the design was reasoned about rather than
assembled.

**Write the alternatives honestly.** An alternative listed only to be dismissed in four
words fools nobody, least of all a reviewer who has used the thing you dismissed.

**Keep it under a page.** If it needs more, the decision is really two decisions.
