# `corpus/holdout/` — the real-document holdout

**Empty on purpose, and it stays that way.**

Forty real household documents, collected under the consent and redaction protocol in
`docs/governance/`, redacted before use. They exist on the integration machine only.
**They are never committed to this repository** — the directory is gitignored and
`.graphifyignore` excludes it from knowledge-graph extraction as a second lock.

## Why it exists

Synthetic documents are cleaner and more consistent than real ones, so a score measured
only on them overstates the system. Report both numbers and the gap. **The gap is a
finding, not a defect** — and it is the number that makes the rest of the evaluation
credible.
