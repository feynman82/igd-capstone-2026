# IMDA GenAI framework — the nine dimensions, answered

Status: draft · Owner: Siew · Reviewer: Christian (technical accuracy) · Framework: IMDA and AI
Verify Foundation, *Model AI Governance Framework for Generative AI*; dimension names and
descriptions from the published annex (see [Sources](#sources)) · Evidence
read on `main` at `eb9fc20` (2026-10-17), with the governance drafts of
[feynman82/igd-capstone-2026#51](https://github.com/feynman82/igd-capstone-2026/pull/51) merged in

This is the full mapping that the W1 extract (`imda-what-applies.md`, GenAI section) said the W6
task would produce. Where the two disagree, this page is the later reading.

> The rule for this page (`docs/team-tasks.csv`): every dimension is answered with **an artefact
> or a measured result, never a description of intent**. Where neither exists, the row says
> **gap** and does not fill the space with a sentence. Anything that could not be traced is
> marked **unverified** and repeated in [Open questions](#open-questions).
>
> Each dimension's name and its italic one-line description are quoted verbatim from the annex.

## Summary

| # | Dimension | Answered with | Status |
|---|---|---|---|
| 1 | Accountability | Lane ownership in `CODEOWNERS`, a named reviewer on every task, and ADRs that record who decided | Evidenced |
| 2 | Data | The data inventory, provenance enforced as `NOT NULL`, and reviewed grounding sources | Evidenced, with known gaps |
| 3 | Trusted development and deployment | The model card, and evaluation runs stamped with the code commit | Partial: what the user is told is unverified |
| 4 | Incident reporting | An approved incident procedure and incident log; a helpdesk in the terms of use; the `traces` audit table | Partly: procedure not yet exercised, PDPA steps to confirm; helpdesk not yet in the interface |
| 5 | Testing and assurance | Sets A, B and C, with measured results in `eval/results/` | Partly: all testing is internal; there is no third-party testing |
| 6 | Security | Loopback-only endpoints refused at start-up, screens bound to `127.0.0.1`, and the injection items in Set C | Evidenced, with known gaps |
| 7 | Content provenance | Every sentence cites a passage, and every fact a document and page | Evidenced |
| 8 | Safety and alignment R&D | No R&D is done. The developer states the generator is not safety-aligned, and our controls compensate | Out of scope, stated |
| 9 | AI for Public Good | Runs on one consumer GPU, measured | Partial |

## The nine, one at a time

### 1. Accountability

*"Putting in place the right incentive structure for different players in the AI system
development life cycle to be responsible to end-users."*

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

*"Ensuring data quality and addressing potentially contentious training data in a pragmatic
way, as data is core to model development."*

PARROT trains no model (`model-card.md` §6), so the training-data half belongs to the model
developers. What PARROT controls is the quality and lawful use of the data it reads and cites.

| Claim | Evidence |
|---|---|
| What personal data is held, whose, on what basis, where it rests, and what crosses a boundary | `docs/governance/data-inventory.md` §§1–3 |
| What the household is told the data is for, and how long it is kept | `docs/governance/terms-of-use.md` Clause B; `docs/governance/retention-and-erasure.md` |
| No fact without a source | `facts.document_id` and `facts.page` are `NOT NULL` (`db/migrations/0001_init.sql`) |
| Development uses no real person's documents | The corpus is generated register-first (`docs/governance/synthetic-data-case.md`, `corpus/register/`) |
| Pack grounding comes from named publishers and is signed off before it is cited | `GroundingDocument` requires `publisher_kind` in {regulator, government, industry_association}, a `https://` URL, a `retrieved` date and a `review_by` date; the comment on `reviewed_on` says "nothing is cited until a person has signed it off" (`core/contracts.py`, `GroundingDocument`) |
| Extraction quality, measured | Filed correctly (extraction F1) **0.976** (`eval/results/2026-10-17-vault-rebuilt.md`) |
| What erasure reaches | `docs/governance/retention-and-erasure.md` |

**Known gaps.** `consent-and-redaction.md`, which governs the real-document holdout, does not
exist yet. Data is not encrypted at rest: the lock is a screen lock, not encryption
(`web/lib/lock.ts`; `data-inventory.md` §6, question 3).

### 3. Trusted development and deployment

*"Enhancing transparency around baseline safety and hygiene measures based on industry best
practices in development, evaluation and disclosure."*

| Claim | Evidence |
|---|---|
| The models, licences, intended use, out-of-scope use and failure modes are published | `docs/governance/model-card.md` |
| Every evaluation result names the generator tag, corpus hash and code commit it ran on | The header of every `eval/results/*.md`, e.g. `code 5d6fa72` on `2026-10-17-vault-rebuilt.md` |
| The terms of use tell the user that answers are generated by AI and must be checked against the cited source | `terms-of-use.md` Clause D 1–2 (approved by Siew, 2026-10-05) |
| A pack shows its disclaimer, and a declined or withheld answer carries it | `guardrails.disclaimer` in each `packs/*/pack.yaml`; `web/components/ask/advice-card.tsx`; `web/app/api/chat/route.ts` |
| Non-obvious choices are recorded with their alternatives | `docs/adr/` (20 records) |

**Not built:** the Ask screen does not yet say that answers are generated by AI. The terms say
it, but not at the point of interaction. Raised as
[feynman82/igd-capstone-2026#90](https://github.com/feynman82/igd-capstone-2026/issues/90), with
Clause D's wording.

### 4. Incident reporting

*"Implementing an incident management system for timely notification, remediation and
continuous improvements, as no AI system is foolproof."*

Read, as decided on 2026-10-04 (`imda-what-applies.md`), as the team's internal handling.
Notifying the PDPC is a PDPA duty, covered by the same procedure.

| What exists | Evidence |
|---|---|
| A procedure: report, contain, record, assess, notify, learn | `docs/governance/incident-and-breach-procedure.md` (approved by Siew, 2026-10-17; PDPA steps still to confirm) |
| An incident log that never holds personal data | `docs/governance/incidents.md` (approved 2026-10-05; no incidents recorded) |
| A contact point for the user | `terms-of-use.md` Clause D 3: the PARROT helpdesk at +65 9123 4567. The number is still to be confirmed as a staffed line (`terms-of-use.md`, "Status against the code"). |
| Every graph node writes a row to `traces`: node, latency, model, and a payload with the retrieved ids and the gate's decision | `db/migrations/0001_init.sql` (`traces`); `core/graph/README.md` ("Rules") |
| Failures found in evaluation become tracked issues, fixed and re-measured | e.g. [feynman82/igd-capstone-2026#48](https://github.com/feynman82/igd-capstone-2026/issues/48), re-measured in `eval/results/2026-10-14-setc-injection-planted.md` |

**Partly.** The procedure is approved but not yet exercised, and its PDPA notification steps
are still to confirm from the Act. The helpdesk appears only in the
terms of use, not in the interface, and the user cannot reach it from a screen. A helpdesk
contact in the interface is raised as
[feynman82/igd-capstone-2026#91](https://github.com/feynman82/igd-capstone-2026/issues/91).

### 5. Testing and assurance

*"Providing external validation and added trust through third-party testing, and developing
common AI testing standards for consistency."*

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

**What this does not show.**
- **No external validation.** The annex's emphasis is *external* validation and *third-party*
  testing. Every result above was produced by the team, on the team's own sets, scored by the
  team's own harness. Nothing has been tested by a third party, and that is the gap to state.
- **All of it is synthetic.** Performance on real documents waits for the holdout.
- **English only.** No question is in another language (model card §3).

### 6. Security

*"Addressing new threat vectors that arise through generative AI models."*

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

**Known gaps** (from `data-inventory.md` §§3 and 5):
- The API answers any loopback request without authentication.
- **An empty `TELEGRAM_CHAT_IDS` accepts documents from any chat.** That is the risk IMDA's
  OpenClaw case study names: *"restrict messaging channel access"* (MGF for Agentic AI v1.5,
  p 14).

The screens no longer listen on every interface: `web/package.json` runs `next dev -H 127.0.0.1`.

### 7. Content provenance

*"Transparency about where content comes from as useful signals for end-users."*

| Claim | Evidence |
|---|---|
| A sentence with no supporting passage is dropped, and so is a citation to a passage that was not retrieved | `core/graph/gate.py`; `core/graph/README.md` |
| Every stored fact carries its document and page | `db/migrations/0001_init.sql` |
| A calendar line cites the calendar day, and a deadline cites its document's page | ADR 0020 decision 5 (`Citation.kind = "calendar"`) |
| A sentence about "last year" must cite a document whose dates reach last year | `core/graph/period.py`; measured in `2026-10-17-time-scoped-claims.md` (one unsupported claim removed, nothing else moved) |

Every answer sentence shows the user the document and page it came from: the *"useful
signal for end-users"* the annex describes. The user opens the cited page from a source chip
(`web/components/source-chip.tsx`).

**Stated limit.** A citation shows where a value came from, not that it answers the question.
Unsupported claims still stand at 18 of 77 (dimension 5). Telling the user that the answer
itself is AI-generated is dimension 3's open item
([feynman82/igd-capstone-2026#90](https://github.com/feynman82/igd-capstone-2026/issues/90)).

### 8. Safety and alignment R&D

*"Accelerating R&D through global cooperation among AI Safety Institutes to improve model
alignment with human intention and values."*

This is addressed to AI Safety Institutes, not to a deployer.

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

*"Responsible AI includes harnessing AI to benefit the public by democratising access,
improving public sector adoption, upskilling workers and developing AI systems sustainably."*

| Claim | Evidence |
|---|---|
| The whole stack runs on one consumer GPU, with no cloud cost per question | RTX 3080 10 GB: 130 tok/s, 7.4 GB peak VRAM at 16K context (`eval/results/w1-hardware.md`) |
| A household's data stays in the household | `data-inventory.md`, "What crosses a boundary" |
| A Singapore-developed model for Singapore documents | Model card §1 |

**Partial.** The regional-language claim is the developer's and is untested here. No energy or
carbon figure is measured. A *minimum* hardware specification is a roadmap condition, not a
result (`docs/report/07-commercialisation-roadmap.md`).

## Open questions

1. **The ninth dimension is AI for Public Good: settled against the annex.** Siew's decision of
   2026-10-04 chose **human oversight**, following the architecture review, before either
   framework had been read. The annex lists **AI for Public Good** as dimension 9 and has no
   "human oversight" dimension. The decision is superseded (`imda-what-applies.md` updated).
   Human oversight is still evidenced, under the Agentic framework's dimension 2
   (`imda-what-applies.md`; `autonomy-statement.md`). **Still open:** the architecture review
   (`docs/artefacts/architecture-review.html`, §10, Christian's) lists the wrong nine, with
   "cybersecurity" and "human oversight", and needs correcting.
2. **The model card's dimension numbers: corrected.** It said *"IMDA GenAI dimension 5
   (transparency)"*. In the annex, disclosure is part of dimension 3 (*"… in development,
   evaluation and disclosure"*) and dimension 5 is testing and assurance. `model-card.md` and
   `README.md` now say dimensions 3 and 5.
3. **The model card quotes run 2 (30 September).** This page quotes the 15–17 October runs,
   which use different headline measures (judge `none`). The two need one set of figures before
   finalisation (W8).
4. **The Ask screen does not tell the user they are talking to an AI.** Clause D says it, but no
   disclosure was found in `web/`. First requested of Zee on #51 (2026-10-05); raised with
   Christian as [feynman82/igd-capstone-2026#90](https://github.com/feynman82/igd-capstone-2026/issues/90). (Dimensions 3 and 7.)
5. **Incident reporting.** `incident-and-breach-procedure.md` is approved (2026-10-17). Confirm the helpdesk in
   Clause D 3 is a real, staffed line. A helpdesk email in the interface is raised as
   [feynman82/igd-capstone-2026#91](https://github.com/feynman82/igd-capstone-2026/issues/91), and
   the interface and Clause D 3 should name the same contact.

## Sources

- AI Verify Foundation and IMDA, *Annex: Nine dimensions of the proposed Model AI Governance
  Framework*, from the copy Siew supplied. It is one page: the nine names and a one-line
  description of each, quoted above.
- **Edition.** The annex is titled for the *proposed* framework, issued for consultation in
  January 2024. The framework was finalised on 30 May 2024. Secondary sources give the same
  nine names for the final text
  ([OECD.AI catalogue](https://oecd.ai/en/catalogue/tools/model-ai-governance-framework-for-generative-ai),
  [Baker McKenzie](https://insightplus.bakermckenzie.com/bm/technology-media-telecommunications_1/singapore-new-model-ai-governance-framework-for-generative-ai-launched-by-imda-and-ai-verify-foundation)).
  If the chapter quotes anything beyond the names and these one-line descriptions, read it
  from the final 30 May 2024 text.
- AI Singapore, *Qwen-SEA-LION-v4-4B-VL* model card, read 2026-10-14 (via `model-card.md`).
