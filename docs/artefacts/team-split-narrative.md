# Project PARROT — team split

Five people, nine weeks, three builders. Ownership is by **directory**, not by task, so the
split is enforced by `CODEOWNERS` rather than by memory.

---

## The five lanes

### A · Integration and product owner — **Christian** *(builder)*

The person who owns the contracts owns the platform. Deliberately the lane with the least
new feature code: an integrator who is also mid-feature stops integrating.

| | |
|---|---|
| **Owns** | `core/contracts.py`, `db/migrations/`, `core/graph/`, `core/adapters/`, `core/ingest/` (orchestration), `modules/`, the repo, the merge queue |
| **Ships** | Both manifests (week 1) · folder watchdog and Telegram bot · ingestion worker with idempotency · router, grounding gate, answer node · Reminder and Alert modules · the demo |
| **Presents** | The problem, the expansion model, the live demonstration |
| **Also** | Domain reviewer for the Insurance pack. Nineteen years of wholesale banking is an unusual advantage for reading policy schedules — use it as review, not as a second build lane |

### B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*

The most rubric-relevant workstream in the project, and the one that needs someone
comfortable being told by a number that their intuition was wrong.

| | |
|---|---|
| **Owns** | `core/retrieve/`, parsing and chunking config, embeddings, the reranker, the abstain floor, `eval/` and every committed result |
| **Ships** | Docling configuration · contextualised chunking · hybrid retrieval with RRF · cross-encoder reranking · the Ragas harness · three evaluation runs (W3, W5, W8) · the before-and-after table that goes in the report |
| **Presents** | Retrieval design and the evaluation results |
| **Seam** | Owns the *measurement* of extraction quality; Christian owns the extraction engine. The person who built a thing should not be the only person scoring it |

### C · Governance and assurance — **Siew**, the data governance officer

Not a documentation role. Six artefacts, each of which is a chapter of the report, plus the
protocol that makes the holdout corpus lawful to collect.

| | |
|---|---|
| **Owns** | `docs/governance/`, the consent and redaction protocol, the PDPA position |
| **Ships** | Data inventory · retention and erasure policy · model card · ISO/IEC 22989-to-5338 stage-and-process map · IMDA GenAI nine-dimension mapping · autonomy statement under IMDA's Agentic AI framework · the 15-item adversarial Set C |
| **Presents** | Governance, the regulatory mapping, the autonomy boundary |

### D · Domain packs and interface — **Zee**, the commercial member *(builder)*

Both halves are content-shaped work that AI coding tools handle well: a pack is mostly YAML,
a schema and a grounding corpus; the interface is generated against a finished design pack.

| | |
|---|---|
| **Owns** | `packs/iras_tax/`, `packs/insurance_agent/`, `web/` |
| **Ships** | Both pack manifests, extraction schemas, grounding corpora, guardrails and disclaimers · the four surfaces (Today, Ask, Vault, Packs) · the pack catalogue of nine deferred packs · the commercialisation roadmap page |
| **Presents** | The interface and the two domain packs |

### E · Corpus and adversarial testing — **Desmond**, the police officer

The corpus is the input to every other lane, so it starts in week 1 and never blocks. The
second half of this lane is investigative: work out how to make the system misbehave.

| | |
|---|---|
| **Owns** | The household canon, the document register, all document templates, every corpus batch, the quarantine review |
| **Ships** | ~360 synthetic documents across 12 types · 30 phone-photographed and 30 scanned documents · ~60 deliberately hard documents · the 40-document redacted holdout · the adversarial run and its findings |
| **Presents** | How the corpus was built and what the adversarial testing found |
| **Why this pairing** | Both halves are the same instinct — knowing what a real document looks like, and knowing how someone would try to get around a control |

---

## The one process change that matters

You said the corpus owner will produce **finished documents using an AI tool**. That works,
but done in the obvious order it throws away the single most valuable by-product: the labels.

**Do not generate documents and then work out what is in them.** Fill the register first.

```
1. Household canon        one page, the facts every document must agree with
2. Document register      a spreadsheet: one row per document, one column per field
                          ← THIS IS THE GROUND TRUTH
3. One template per type   made with an AI tool, with merge fields
4. Mail merge              register + template → hundreds of documents, no code
5. Print and photograph    a subset, on a phone. More realistic than any simulation
```

Filling the register first gives you, at no extra cost:

- **Extraction F1 measured directly** rather than by hand-labelling 400 documents in week 8
- **Most of golden Set A generated** rather than written by hand
- **Internal consistency** — a policy cannot expire before it starts, and the same policy
  number appears identically in the schedule, the renewal notice and the claim letter
- **Mass production without code** — mail merge turns 96 register rows into 96 payslips

Without the register, someone spends week 8 labelling documents by hand, and the evaluation
that carries the grade arrives late and thin.

### Two rules for the corpus

1. **Invented organisations only.** Never render a document bearing the name, logo or
   letterhead of a real insurer, bank or agency. A realistic fake notice from a real
   institution is a fabricated official record whatever the intent, and it would make the
   corpus unpublishable alongside the report. Every page carries a visible `SYNTHETIC
   DOCUMENT` footer.
2. **Say what synthetic data does not prove.** Generated documents are cleaner and more
   consistent than real ones, so a score measured only on them overstates the system. That
   is what the 40-document holdout is for. Report both numbers and the gap — that gap is a
   finding, not a defect.

---

## Presentation split

The presentation rubric scores each presenter individually; its top band requires that the
presenter "spoke and participated at a very high and balanced level". A team where one
person narrates 25 slides cannot reach it. Assign these in week 1.

| Segment | Owner |
|---|---|
| Problem, personas, expansion model, live demonstration | Christian |
| The interface and the two domain packs | Zee |
| The corpus, how it was built, and the adversarial findings | Desmond |
| Retrieval design and the evaluation results | Yew Mun |
| Governance, the regulatory mapping, the autonomy boundary | Siew |

---

## Everyone, regardless of lane

Each person writes **12 golden-set questions for their own area** by the end of week 3. It is
the highest-value work with the lowest barrier to entry, it is the one task that otherwise
bottlenecks on a single person, and it forces everybody to state what "correct" means for
the thing they built.

---

## How the code gets written

Three builders and their agents on one repository. The failure mode is not slow progress —
it is five plausible-looking implementations of the same idea.

1. **Contracts before code.** `core/contracts.py` and the database schema land in week 1, in
   their own reviewed pull requests, before any feature depends on them. An agent given a
   schema is consistent across sessions and across people; an agent given prose is not.
2. **One `AGENTS.md` at the repo root**, read by every agent. Stack, hard rules, definition
   of done. The hard rules are the ones an agent will otherwise cheerfully break: never
   generate SQL at runtime, never write a fact without a document id and page, no new
   runtime dependency without a decision record.
3. **Vertical slices, not layers.** A pull request should let someone do something new.
4. **The evaluation is the gate.** Any change to retrieval, extraction or the grounding gate
   pastes its numbers into the pull request with one line on why they moved.
5. **Nobody edits `core/contracts.py` in a feature pull request.** The most common way a
   multi-agent repository degrades is a contract quietly widened to make one feature easier.
6. **Ninety minutes a week for integration**, protected. Christian merges everything and deletes the
   duplicate helpers. Cheaper than discovering the divergence in week 8.

---

## Swap rules

- If **Zee** turns out not to want the frontend, split lane D at its
  natural seam: pack content (document taxonomies, the IRAS corpus, disclaimer wording, the
  catalogue) needs no code, and the interface is the single workstream best handed almost
  entirely to an agent under Christian's review.
- If **Desmond** finishes the corpus early, the next most valuable thing is more
  adversarial work: try to make the assistant contradict itself across two documents that
  disagree. That is a genuine finding and nobody else will have one.
- If **a week is lost**, cut the Insurance pack, not the Alert module. One module plus one
  pack still demonstrates both axes of expansion; two packs and no module demonstrates one.
