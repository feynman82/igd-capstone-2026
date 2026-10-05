# `docs/governance/` — the assurance artefacts

**Owner: Siew.** Each file here is a deliverable in its own right *and* a chapter of the
report. They are produced as artefacts along the way, not written up as prose in November.

| File | Framework | Owner | Due |
|---|---|---|---|
| `data-inventory.md` | PDPA — what enters, where it rests, what crosses a boundary | Siew | W2 |
| `consent-and-redaction.md` | PDPA — governs the real-document holdout; must exist **before** collection | Siew with Desmond | W2 |
| `retention-and-erasure.md` | PDPA — including what "Reset Workspace" and `DELETE FROM documents` actually cascade to | Siew | W4 |
| `model-card.md` | IMDA GenAI, dimensions 1 and 5 | Siew with Yew Mun | W6 |
| `iso-stage-process-map.md` | ISO/IEC 22989 stages against ISO/IEC 5338 processes | Siew | W7 |
| `imda-genai-nine-dimensions.md` | IMDA GenAI (2024) | Siew | W8 |
| `imda-agentic-alignment.md` | IMDA Agentic AI v1.5 (May 2026), all four dimensions | Siew | W8 |
| `autonomy-statement.md` | IMDA Agentic AI v1.5 (May 2026), dimensions 1 and 2 | Siew with Christian | W8 |
| `synthetic-data-case.md` | Why synthetic data, what it proves and what it does not | Siew with Desmond | W6 |

## The autonomy statement in one line

Version 1 observes, retrieves and advises. It does not pay, book or file. The Actions
module is specified and deliberately not built, and every pack manifest enforces the
boundary with `never_acts: true` — a machine-checked flag, not a sentence in a policy
document.

## The rule that governs all eight

Ground every claim in a file in this repository or in a cited instrument. Where the
evidence cannot be found, write `unverified` and raise it — an artefact that asserts
something the code does not do is worse than one with a gap in it.

Use the **`writing-a-governance-artefact`** skill. It lists where each of the four
strongest claims is enforced in code, and it carries the 22989-versus-5338 distinction
that is easy to get wrong: 5338 supplies processes and explicitly does not prescribe a
life cycle; the stage names commonly attributed to it are 22989's.
