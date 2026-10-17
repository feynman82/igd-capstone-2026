# `docs/governance/` — the assurance artefacts

**Owner: Siew.** Each file here is a deliverable in its own right *and* a chapter of the
report. They are produced as artefacts along the way, not written up as prose in November.

| File | Framework | Owner | Due |
|---|---|---|---|
| `data-inventory.md` | PDPA — what enters, where it rests, what crosses a boundary | Siew | W2 |
| `consent-and-redaction.md` | PDPA — governs the real-document holdout; must exist **before** collection | Siew with Desmond | W2 |
| `retention-and-erasure.md` | PDPA — including what "Reset Workspace" and `DELETE FROM documents` actually cascade to | Siew | W4 |
| `model-card.md` | IMDA GenAI, dimensions 3 and 5 | Siew with Yew Mun | W6 |
| `iso-stage-process-map.md` | ISO/IEC 22989 stages against ISO/IEC 5338 processes | Siew | W7 |
| `imda-genai-nine-dimensions.md` | IMDA GenAI (2024) | Siew | W8 |
| `autonomy-statement.md` | MGF for Agentic AI (v1.5, May 2026): *Assess and bound the risks upfront* and *Make humans meaningfully accountable* | Siew with Christian | W8 |
| `synthetic-data-case.md` | Why synthetic data, what it proves and what it does not | Siew with Desmond | W6 |
| `imda-what-applies.md` | IMDA GenAI (2024) and MGF for Agentic AI (v1.5, May 2026) — extract, mapped to code | Siew | W1 |
| `incident-and-breach-procedure.md` | IMDA GenAI incident reporting; PDPA Part 6A data breach notification | Siew with Christian | — |
| `incidents.md` | The incident log (PDPA Accountability Obligation); never holds personal data | Siew | — |
| `terms-of-use.md` | PDPA s 15 deemed consent — the contractual basis for one adult filing for another | Siew | — |

## The autonomy statement in one line

Version 1 observes, retrieves and advises. It does not act on the household's behalf: it
does not pay, book or file anything, and it contacts no one outside the household. The Actions
module is deliberately not built. No pack can declare that it acts (`never_acts: Literal[True]`)
and no kind of module can act (`PrimitiveId`, `core/contracts.py`), so the boundary is
machine-checked, not a sentence in a policy document.

## The rule that governs all of them

Ground every claim in a file in this repository or in a cited instrument. Where the
evidence cannot be found, write `unverified` and raise it — an artefact that asserts
something the code does not do is worse than one with a gap in it.

Use the **`writing-a-governance-artefact`** skill. It lists where each of the four
strongest claims is enforced in code, and it carries the 22989-versus-5338 distinction
that is easy to get wrong: 5338 supplies processes and explicitly does not prescribe a
life cycle; the stage names commonly attributed to it are 22989's.
