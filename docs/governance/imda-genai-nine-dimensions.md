# IMDA GenAI framework — the nine dimensions, answered

Status: draft · Owner: Siew · Reviewer: Christian (technical accuracy) · Framework: IMDA and AI
Verify Foundation, *Model AI Governance Framework for Generative AI*, 30 May 2024 · Evidence
read on `main` at `eb9fc20` (2026-10-17)

> The rule for this page (`docs/team-tasks.csv`): every dimension is answered with **an artefact
> or a measured result, never a description of intent**. Where neither exists, the row says
> **gap** and does not fill the space with a sentence. Anything that could not be traced is
> marked **unverified** and repeated in [Open questions](#open-questions).
>
> **To check against the primary text.** The IMDA and AI Verify Foundation sites are blocked
> from the environment this was drafted in. The dimension names and one-line summaries in the
> first column come from secondary sources, listed under [Sources](#sources). Confirm them
> verbatim before this enters the report.

## Summary

| # | Dimension | Answered with | Status |
|---|---|---|---|
| 1 | Accountability | Lane ownership in `CODEOWNERS`, a named reviewer on every task, and ADRs that record who decided | Evidenced |
| 2 | Data | The data inventory, provenance enforced as `NOT NULL`, and reviewed grounding sources | Evidenced, with known gaps |
| 3 | Trusted development and deployment | The model card, and evaluation runs stamped with the code commit | Partial: what the user is told is unverified |
| 4 | Incident reporting | The `traces` audit table, and failures tracked as GitHub issues | **Gap**: no reporting route for a user |
| 5 | Testing and assurance | Sets A, B and C, with measured results in `eval/results/` | Evidenced |
| 6 | Security | Loopback-only endpoints refused at start-up, a Telegram allow list, and the injection items in Set C | Evidenced, with known gaps |
| 7 | Content provenance | Every sentence cites a passage, and every fact a document and page | Evidenced for sources; unverified for labelling output as AI-generated |
| 8 | Safety and alignment R&D | No R&D is done. The developer states the generator is not safety-aligned, and our controls compensate | Out of scope, stated |
| 9 | AI for Public Good | Runs on one consumer GPU, measured | Partial |

## The nine, one at a time

### 1. Accountability

*Responsibility is allocated along the development chain according to who controls what.*

| Link in the chain | Who | Evidence |
|---|---|---|
| Model developer | AI Singapore (generator); BAAI, Google (reranker, embedding) | `docs/governance/model-card.md` §1, with licences |
| Deployer and integrator | The five lanes, each owning a set of directories | `.github/CODEOWNERS`; `team/*/README.md` |
| Decisions | Each ADR names its decider and reviewers | `docs/adr/`, e.g. ADR 0020: decider Christian, reviewers Zee and Siew |
| Every deliverable | Reviewed by the lane that uses it, never by its author | `docs/team-tasks.csv`, `Reviewer` column |

**Stated limit.** `CODEOWNERS` *requests* review but does not enforce it: `main` is unprotected
(`docs/adr/0010-main-is-unprotected-by-convention.md`). The household is the operator, and v1
cannot act on its behalf (`docs/governance/autonomy-statement.md`). So accountability for any
decision stays with the person who reads the answer.

### 2. Data

*The quality and lawful use of the data the system is built and run on.*

| Claim | Evidence |
|---|---|
| What personal data is held, where it rests, and what crosses a boundary | `docs/governance/data-inventory.md` |
| No fact without a source | `facts.document_id` and `facts.page` are `NOT NULL` (`db/migrations/0001_init.sql`) |
| Development uses no real person's documents | The corpus is generated register-first (`docs/governance/synthetic-data-case.md`, `corpus/register/`) |
| Pack grounding comes from named publishers and is signed off before it is cited | `GroundingDocument` requires `publisher_kind` in {regulator, government, industry_association}, a `https://` URL, a `retrieved` date and a `review_by` date; the comment on `reviewed_on` says "nothing is cited until a person has signed it off" (`core/contracts.py`, `GroundingDocument`) |
| Extraction quality, measured | Filed correctly (extraction F1) **0.976** (`eval/results/2026-10-17-vault-rebuilt.md`) |
| What erasure reaches | `docs/governance/retention-and-erasure.md` |

**Known gaps.** The data inventory covers only one entry so far. `consent-and-redaction.md`,
which governs the real-document holdout, does not exist yet. Data is not encrypted at rest
(`data-inventory.md`, "Encrypted at rest").

### 3. Trusted development and deployment

*Transparency about how the model was developed and tested, and what users are told.*

| Claim | Evidence |
|---|---|
| The models, licences, intended use, out-of-scope use and failure modes are published | `docs/governance/model-card.md` |
| Every evaluation result names the generator tag, corpus hash and code commit it ran on | The header of every `eval/results/*.md`, e.g. `code 5d6fa72` on `2026-10-17-vault-rebuilt.md` |
| A pack shows its disclaimer, and a declined or withheld answer carries it | `guardrails.disclaimer` in each `packs/*/pack.yaml`; `web/components/ask/advice-card.tsx`; `web/app/api/chat/route.ts` |
| Non-obvious choices are recorded with their alternatives | `docs/adr/` (20 records) |

**unverified:** whether the Ask screen tells the user, on an ordinary answer, that it was
generated by a model and may be wrong, and which model. This is carried from model card open
question 5 (for Zee).

### 4. Incident reporting

*A way to report, and learn from, an incident after deployment.*

| What exists | Evidence |
|---|---|
| Every graph node writes a row to `traces`: node, latency, model, and a payload with the retrieved ids and the gate's decision. It is the audit trail of what was answered and why. | `db/migrations/0001_init.sql` (`traces`); `core/graph/README.md` ("Rules") |
| Failures found in evaluation become tracked issues | e.g. the household-identity failure [feynman82/igd-capstone-2026#48](https://github.com/feynman82/igd-capstone-2026/issues/48), fixed and re-measured in `eval/results/2026-10-14-setc-injection-planted.md` |

**Gap.** A household has no route to report a wrong answer. There is no incident log, no
severity scale, and no named person who receives a report. v1 is a single-household prototype
on synthetic data, so the gap can be argued, but it must be stated and not covered with a
sentence.

### 5. Testing and assurance

*Testing before and after deployment, against stated targets.*

Latest runs, synthetic corpus, generator `Qwen-SEA-LION-v4-4B-VL` Q4_K_M:

| Measure | Result | Source |
|---|---|---|
| Right and cited, Set A (answerable) | **41 / 50** | `eval/results/2026-10-17-time-scoped-claims.md` |
| Unsupported claims, all sets | **18 / 77** | same |
| Over-caution, Set A | 4 / 50 | same |
| Adversarial Set C, held back by behaviour | **15 / 15** (12 / 15 by flag; [feynman82/igd-capstone-2026#16](https://github.com/feynman82/igd-capstone-2026/issues/16)) | `eval/results/2026-10-15-setc-isolated-vault.md` |
| Set C by category: act, injection, not on file, advice, out of date | 3/3 each | same |
| Extraction F1 | 0.976 | `eval/results/2026-10-17-vault-rebuilt.md` |

Set C is run in a vault of its own, so its planted documents never distort Sets A and B
(`2026-10-15-setc-isolated-vault.md`).

**What this does not show.** All of it is synthetic. Performance on real documents waits for
the holdout. No question is in a language other than English (model card §3).

### 6. Security

*New threat vectors that generative AI brings, prompt injection among them.*

| Claim | Evidence |
|---|---|
| Nothing leaves the machine at inference: Ollama, Postgres and Redis URLs are refused at start-up unless they are loopback | `core/runtime/settings.py` (`local_url`, lines 21 and 34) |
| Only allow-listed Telegram chats are spoken to, and an empty list speaks to nobody | `core/adapters/telegram.py` (`send`) |
| An instruction planted in a document is not obeyed: 3 of 3 injection items held | `eval/results/2026-10-14-setc-injection-planted.md` |
| The system cannot be made to act, because there is nothing to act with | `docs/governance/autonomy-statement.md` |

**Stated limit.** The injection result itself says that two of the three were held by rules that
would have fired anyway, *"not by anything that inspects a document for instructions. The honest
claim is that the instructions were not obeyed, not that an injection defence exists"*
(`2026-10-14-setc-injection-planted.md`).

**Known gaps** (from `data-inventory.md`): the API answers any loopback request without
authentication, and the web screens may listen on every interface over plain HTTP.

### 7. Content provenance

*Transparency about where content came from, and whether it was generated.*

| Claim | Evidence |
|---|---|
| A sentence with no supporting passage is dropped, and so is a citation to a passage that was not retrieved | `core/graph/gate.py`; `core/graph/README.md` |
| Every stored fact carries its document and page | `db/migrations/0001_init.sql` |
| A calendar line cites the calendar day, and a deadline cites its document's page | ADR 0020 decision 5 (`Citation.kind = "calendar"`) |
| A sentence about "last year" must cite a document whose dates reach last year | `core/graph/period.py`; measured in `2026-10-17-time-scoped-claims.md` (one unsupported claim removed, nothing else moved) |

**Stated limit.** A citation shows where a value came from, not that it answers the question.
Unsupported claims still stand at 18 of 77 (dimension 5). The framework's main concern here is
labelling generated content. PARROT answers that with sources, and whether output is also
labelled as AI-generated is the unverified item under dimension 3.

### 8. Safety and alignment R&D

*Research to align models with human intent. The framework addresses this to the research
community and safety institutes.*

PARROT does no model research, training or fine-tuning (`docs/governance/model-card.md` §6).
The developer's own model card lists these limits: the generator is not safety-aligned, has
not been tested against adversarial prompting, and can hallucinate (AI Singapore model card,
read 2026-10-14, as summarised in `model-card.md` §5). PARROT's response is to keep the model's freedom narrow, not to align it:
- **The gate:** an unsupported sentence is never shown.
- **`verdict_by_code: Literal[True]`:** the model explains a verdict but never chooses it
  (`core/contracts.py:250`).
- **No ability to act:** see the autonomy statement.
- **Set C:** tests all three.

### 9. AI for Public Good

*Access, adoption, and sustainable development.*

| Claim | Evidence |
|---|---|
| The whole stack runs on one consumer GPU, with no cloud cost per question | RTX 3080 10 GB: 130 tok/s, 7.4 GB peak VRAM at 16K context (`eval/results/w1-hardware.md`) |
| A household's data stays in the household | `data-inventory.md`, "What crosses a boundary" |
| A Singapore-developed model for Singapore documents | Model card §1 |

**Partial.** The regional-language claim is the developer's and is untested here. No energy or
carbon figure is measured. A *minimum* hardware specification is a roadmap condition, not a
result (`docs/report/07-commercialisation-roadmap.md`).

## Open questions

1. **The repository lists a different nine.** `docs/artefacts/architecture-review.html` names
   the dimensions as *"…cybersecurity · human oversight"*. It has "human oversight" and no "AI
   for Public Good". Secondary sources agree with this page's list. Confirm against the
   primary text, then correct the architecture review (Christian's) or this page.
2. **The model card numbers its dimensions differently.** It says *"IMDA GenAI dimension 5
   (transparency)"* (`model-card.md` §7, and its header says "dimensions 1 and 5"). On this
   page's list, dimension 5 is testing and assurance, and disclosure to users falls under 3.
   Siew to align the model card once item 1 is settled.
3. **The model card quotes run 2 (30 September).** This page quotes the 15–17 October runs,
   which use different headline measures (judge `none`). The two need one set of figures before
   finalisation (W8).
4. **Zee:** what does the Ask screen tell the user about the model on an ordinary answer?
   (Dimensions 3 and 7.)
5. **Incident reporting:** accept the gap as stated, or ask Christian for a minimal route, such
   as a "report this answer" control that writes to `traces`? That would be a code change.

## Sources

- IMDA and AI Verify Foundation, *Model AI Governance Framework for Generative AI*, 30 May 2024.
  Not read directly (blocked); confirm the dimension names against it.
- Secondary summaries used for the dimension names:
  [OECD.AI catalogue](https://oecd.ai/en/catalogue/tools/model-ai-governance-framework-for-generative-ai),
  [Baker McKenzie](https://insightplus.bakermckenzie.com/bm/technology-media-telecommunications_1/singapore-new-model-ai-governance-framework-for-generative-ai-launched-by-imda-and-ai-verify-foundation),
  [Allen & Gledhill](https://www.allenandgledhill.com/sg/publication/articles/27238/announces-proposed-model-ai-governance-framework-for-generative-ai)
- AI Singapore, *Qwen-SEA-LION-v4-4B-VL* model card, read 2026-10-14 (via `model-card.md`).
