# IMDA frameworks: what applies to PARROT

> **Status: W1 extract, 2026-10-05. Owner: Siew. For Christian's review.**
>
> **The Agentic AI framework has been read for this version.** The source is the copy Siew
> supplied: *Model AI Governance Framework for Agentic AI*, **Version 1.5, published 20 May 2026
> (updated 5 June 2026)**. Its terminology is used throughout the Agentic section, with page
> numbers. Page numbers are the framework's own printed numbers.
>
> **The GenAI framework has still not been read.** Its dimension names come from the team's
> architecture review (`docs/artefacts/architecture-review.html`, §10), and what each dimension
> asks is not paraphrased. The W6 task (`imda-genai-nine-dimensions.md`) turns that section into
> the full mapping.

## The two instruments

| Instrument | Version and date | Dimensions | Source of the wording used here |
|---|---|---|---|
| IMDA, *Model AI Governance Framework for Generative AI* | May 2024 | Nine | Architecture review §10. Ninth dimension decided by Siew, see below. **Not read.** |
| IMDA, *Model AI Governance Framework for Agentic AI* ("MGF for Agentic AI") | **v1.5, published 20 May 2026, updated 5 June 2026.** v1.0 was launched on 22 January 2026 (architecture review). | Four | **The framework itself** |

**The ninth GenAI dimension: decided (Siew, 2026-10-04).** The ninth GenAI dimension is
**human oversight**, as the architecture review lists it. The nine are accountability, data
governance, trusted development, incident reporting, testing and assurance, content provenance,
safety and alignment, cybersecurity, and human oversight.
*Note kept for the record:* the drafting author recalled the published ninth dimension as "AI
for Public Good". The GenAI framework's text has not been read, so a check of the names against
it remains worthwhile before the chapter cites them.

---

## Agentic AI framework: four dimensions (MGF for Agentic AI v1.5)

### The framework's terms, and ours

| Framework term | Meaning in the framework | PARROT's term | Note |
|---|---|---|---|
| **Agent** | An AI system that can "take actions, adapt to new information, and interact with other agents and systems to complete tasks on behalf of humans" (p 3) | The **System** (`terms-of-use.md`) | PARROT has agentic components: routing, a retrieval tool, memory and scheduled jobs. It **takes no action on the outside world.** The framework itself notes that "not all use cases are suitable for agents, and some may be better served by deterministic workflows" (p 15). PARROT's verdicts are made by such a workflow. |
| **Model developer** | First link in the "simplified agentic AI value chain" (p 25) | AI Singapore (SEA-LION) | Open weights, run locally (AGENTS.md, stack) |
| **System provider / app developer** | Builds the agentic system (p 25) | **System Developer** = the PARROT team | `terms-of-use.md`, Definitions |
| **Deployer** | The organisation that deploys the agent, and remains accountable for it (p 25) | **System Deployer** = the PARROT team | `terms-of-use.md`, Definitions |
| **End user**: a user who "interacts with" agents, or who "integrates" them into work (p 46) | The person relying on the agent | **User** (household member) | A household member *interacts with* PARROT, so §2.4.2 applies. §2.4.3 is mainly for employees. |
| **Human-in-the-loop / significant checkpoints** | Points that need human approval, especially high-stakes or irreversible actions (p 29) | Confirmation before deletion; owner-only erase and reset | `retention-and-erasure.md` A4, A5 |
| **Structural, rule-based controls** vs **prompt-layer controls** | System-level safeguards "through predefined logic", preferred over instructions to the model (p 33) | Typed guardrails, the citation gate, consent checks | See dimension 3 |

### The four dimensions

The framework's names are used exactly. The "What's new" table (p 5) calls dimension 2 "Enable
meaningful human accountability". The section heading (p 25), the contents page and the
four-dimensions figure (p 13) all say **"Make humans meaningfully accountable"**, so that is
used here.

Each practice is marked **Meets**, **Partly** or **Gap**, and points at the file that shows it.

#### 1. Assess and bound the risks upfront (§2.1, pp 15–24)

| Framework practice | PARROT | Status | Evidence |
|---|---|---|---|
| **Determine suitable use cases** using the risk factors (§2.1.1, pp 15–17). **Impact:** domain, access to sensitive data, access to external systems, scope of actions, reversibility. **Likelihood:** autonomy, task complexity, external exposure, third-party agents, system complexity. | **Sensitive data: high.** It holds NRIC, salary, loans and possibly health data, with persistent memory (`data-inventory.md` §2). **External systems: none at inference**, since every model endpoint must be loopback. **Scope: reads documents and answers; cannot act.** **Reversibility:** no actions to reverse. **Autonomy and complexity: low.** A fixed pipeline, and verdicts by code. **Third-party:** open-weight models run locally. | **Partly.** The factors are answered here, but no written risk assessment exists. | `core/runtime/settings.py` (`local_url`); `core/contracts.py` (`verdict_by_code`) |
| **Bound risks through design: agent limits** on tools, autonomy and area of impact (§2.1.2, p 19). "Prefer deterministic rather than non-deterministic limits, and bound by design" (p 19). | **Bound by design, not by prompt.** `never_acts: Literal[True]`: a pack cannot enable action. `PrimitiveId` admits no `actions` module. Advice uses a closed list of six calculators. Retrieval is a single tool the team wrote. | **Meets** | `core/contracts.py` (`Guardrails`, `PrimitiveId`, `AdviceCalculator`) |
| **Agent identity and authorisation**: unique identity, least privilege, bounded by the authorising human (pp 23–24) | A single local system with no sub-agents. Delegation is bounded by person: only the owner may erase a person or reset, and the owner-only check is not yet built. | **Partly** (mostly not applicable) | `retention-and-erasure.md` A5 point 6, Part C item 4 |
| **Evaluate the residual risks** (p 24) | Not written down. | **Gap** | — |
| *OpenClaw case study (p 14)*, a Telegram-based personal assistant: "restrict messaging channel access" | An empty `TELEGRAM_CHAT_IDS` accepts **any chat**. This is the same risk the case study names. | **Gap** | `core/runtime/settings.py` (`_chat_ids`); `data-inventory.md` §5 gap 4 |
| *OCBC case study (p 20)*: "task-level autonomy only", "no self-initiation of actions", "no decision authority … outputs are advisory" | **The closest published analogue to PARROT.** It extracts from household financial documents and advises, and a person decides. One difference: reminders and alerts run on a schedule (Clause B 2(b), (c)), but they only inform. | **Meets** | `modules/reminder/module.yaml`; `terms-of-use.md` Clause B 3 |

#### 2. Make humans meaningfully accountable (§2.2, pp 25–32)

| Framework practice | PARROT | Status | Evidence |
|---|---|---|---|
| **Clear allocation of responsibilities within the organisation** (§2.2.1, pp 25–27): key decision makers, product teams, cybersecurity teams, users | Five lanes with named owners, enforced by CODEOWNERS. There is no named cybersecurity role, so red teaming falls to adversarial Set C (Siew) and the corpus attacks (Desmond). | **Partly** | `team/README.md`; `.github/CODEOWNERS` |
| **Outside the organisation**: "clarify distribution of obligations in any terms and conditions" (p 28) | Terms of use, Clauses A–C, allocate responsibility between the User and the team. | **Meets** (drafted; not yet presented to users) | `terms-of-use.md` |
| **Significant checkpoints needing human approval**, including "irreversible actions e.g. permanently deleting data" (§2.2.2, p 29) | Every deletion is confirmed. Erasing a person or resetting is owner-only, and reset requires typing `RESET`. The system makes no other irreversible action. | **Meets as policy**; **not built** | `retention-and-erasure.md` A4, A5 |
| **Keep approval requests contextual and digestible** (p 29) | The approved confirmation wording names what is erased, the 72 hours, and what PARROT cannot reach. | **Meets as policy** | `retention-and-erasure.md` A4, A5 |
| **Audit the effectiveness of human oversight**, e.g. the "human override rate" (p 30) | Corrections are recorded (`facts.verified_by_user`, correction traces), so an override rate *could* be measured, but it is not. | **Gap** (data exists) | `core/corrections.py`; `db/migrations/0001_init.sql` |
| **"Denying action by default when approval infrastructures fail"** (p 30) | No action exists to deny. When the model is unavailable, the advice card stands without the explanation. | **Meets** | `core/graph/answer.py` (`_advice_basis`, "model_unavailable") |
| Human decision where a guess would otherwise decide | Rule values are approved by a person before they are cited. A model-proposed name scopes nothing until a person confirms it. | **Meets** | `db/migrations/0003_advice.sql`; `0002_household.sql` |

#### 3. Implement technical controls and processes (§2.3, pp 33–45)

| Framework practice | PARROT | Status | Evidence |
|---|---|---|---|
| **Structural, rule-based controls rather than prompt-layer controls**, "especially for higher-risk actions" (§2.3.1, p 33) | **PARROT's strongest point.** The citation rule is a gate in code that drops any sentence with no retrieved support. It is not an instruction to the model. The verdict is chosen by code (`verdict_by_code: Literal[True]`), and advice is refused in code without consent. | **Meets** | `core/graph/gate.py`; `core/contracts.py`; `core/advice_consent.py` |
| Tool controls: strict input formats, least privilege, no write access to sensitive tables unless needed (p 34) | The model writes no SQL. Every query is hand-written and parameterised (AGENTS.md rule 1). Modules read typed rows and never write to `facts`. | **Meets** | AGENTS.md rule 1; `core/contracts.py` (`ModuleManifest`) |
| **Before deploying, test agents** for task execution, policy compliance, robustness, repeatedly and across varied datasets (§2.3.2, p 38) | A Ragas harness over golden sets with targets, a register-first corpus with known ground truth, and `make check` on every change. Run 1: faithfulness 0.819 against a 0.90 target. **Policy compliance (refusals)** is to be tested by adversarial Set C: 15 items, drafted (`eval/sets/adversarial/lane-c.jsonl`), and not yet run. | **Partly** | `eval/`; `eval/results/2026-09-29-baseline-dense-only.md` |
| **Continuously monitor and test** after deployment (§2.3.3, pp 42–44) | Each ingest, correction and alert writes a trace. There are no alert thresholds and no scheduled re-evaluation. | **Partly** | `db/migrations/0001_init.sql` (`traces`) |
| **"Ensure log immutability"**: problematic trajectories "cannot be deleted" (p 44) | **Resolved by an incident hold (Siew, 2026-10-05).** The evidence of an *open incident* is kept until the incident is closed. Otherwise it is erased as the retention policy says. | **Meets as policy**, for problematic records only | `retention-and-erasure.md` A6; `incident-and-breach-procedure.md` |
| **Robust change management**: triggers for review, including "model updates" (p 45) | ADRs for every decision. Each fact carries the `pack_version` that extracted it. There is no defined trigger to re-run the evaluation when the model changes. | **Partly** | `docs/adr/`; `db/migrations/0001_init.sql` (`facts.pack_version`) |

#### 4. Enable end-user responsibility (§2.4, pp 46–49)

For users who **interact with** agents (§2.4.2, pp 46–47):

| Framework practice | PARROT | Status | Evidence |
|---|---|---|---|
| **User's responsibilities**, "such as asking the user to double-check all information" | Every answer carries a source chip that opens the cited page. Advice cards carry the pack's disclaimer. | **Meets** | `web/components/source-chip.tsx`; `web/components/ask/advice-card.tsx` |
| **Interaction**: "declare upfront in the user interface that the users are interacting with agents" | **Terms of use, Clause D** (approved 2026-10-05) says that answers are AI-generated and must be verified. But the framework asks for this **in the interface, "rather than writing it only in separate documentation"**. The screens still say only "this assistant" or "household assistant". | **Partly**: in the terms; a screen line is still needed (Zee) | `web/app/unlock/page.tsx`; `web/app/(app)/packs/page.tsx` |
| **Agents' range of actions and decisions** | Clause B states the four uses, and that the System makes no payment, booking, renewal or filing. | **Meets** (drafted) | `terms-of-use.md` Clause B |
| **Data**: how it is collected, stored and used, with "explicit consent" where necessary | The data inventory and Clause B. Explicit, recorded consent before advice. | **Meets** | `data-inventory.md`; `core/advice_consent.py` |
| **Human accountability and escalation**: "human contact points … whom the users can alert if the agents malfunction" | **Terms of use, Clause D 3:** the PARROT helpdesk at +65 9123 4567 (number to confirm). The incident procedure handles what the helpdesk receives. | **Meets** (Clause D approved; number to confirm) | `incident-and-breach-procedure.md` |

---

## GenAI framework: nine dimensions

**Applies** means PARROT has something to show. **Partly** means it has some of it, and the
gap is named. **Little** means the dimension is mainly addressed to model developers or to
government, and PARROT, as a deployer, has only a small part to play.

| Dimension | Applies? | What in PARROT answers it | Evidence |
|---|---|---|---|
| **Accountability** | Applies | The `never_acts` and `verdict_by_code` types. Ownership by lane through CODEOWNERS. An advice record for every advised or withheld answer. Terms that allocate responsibility. | `core/contracts.py`; `.github/CODEOWNERS`; `core/advice_records.py`; `terms-of-use.md` |
| **Data (governance)** | Applies | **The strongest dimension.** A data inventory, a retention and erasure policy, a deemed-consent basis, and a synthetic corpus built register-first. Data stays on the household's computer at inference and at rest. | `data-inventory.md`; `retention-and-erasure.md`; `synthetic-data-case.md`; `corpus/register/` |
| **Trusted development and deployment** | Partly | ADRs for every non-obvious decision. Published sources carry publisher, URL, retrieval date and a review-by date, and none is cited until a person signs it off. **Gap:** the model card is not written yet (W4, overdue). | `docs/adr/`; `core/contracts.py` (`GroundingDocument`); `db/migrations/0003_advice.sql` |
| **Incident reporting** | Applies | **Read as internal handling only (Siew, 2026-10-04).** A procedure is drafted: report, contain, record, assess, learn, with an incident log that holds no personal data. `traces` and `advice_records` are the evidence. Outward notification to the PDPC is a PDPA duty, not part of this dimension. It is covered by the same procedure (§3), with its steps still to confirm from the Act. **Not yet:** approved, or exercised. | `incident-and-breach-procedure.md`; `db/migrations/0001_init.sql` (`traces`) |
| **Testing and assurance** | Applies | The evaluation harness (Ragas) with targets. Run 1, on 2026-09-29: context recall 0.895, context precision 0.868, **faithfulness 0.819 against a 0.90 target**, answer relevancy 0.765 against 0.80. Adversarial Set C is drafted, with 15 items in five categories, and not yet run (`eval/sets/adversarial/`). `make check` gates every change. | `eval/`; `eval/results/2026-09-29-baseline-dense-only.md`; `Makefile` |
| **Security** (the review: "cybersecurity") | Partly | Loopback-only services. Screens bound to `127.0.0.1`. The API refuses non-loopback hosts. **Gaps:** the screen lock does not encrypt, the API has no authentication for local callers, and an empty Telegram allow list accepts any chat. Prompt injection is covered by Set C's `injection` items (`eval/sets/adversarial/lane-c.jsonl`), drafted and not yet run. | `data-inventory.md` §3 and §5; `web/lib/lock.ts`; `api/main.py` |
| **Content provenance** | Applies | **Read as showing where information came from (Siew, 2026-10-04).** One of PARROT's strongest dimensions. Every fact cites a document and a page (`NOT NULL`), so no fact can be written without its source. Every answer sentence must cite a retrieved passage, or the gate drops it. The user opens the cited page from a source chip. Every published source carries its publisher, URL, retrieval date and review-by date, and is cited only after a person signs it off. | `db/migrations/0001_init.sql` (`facts`); `core/graph/gate.py`; `web/components/source-chip.tsx`; `core/pages.py`; `db/migrations/0003_advice.sql` (`grounding_sources`) |
| **Safety and alignment (R&D)** | Little | Mainly addressed to model developers. What PARROT does as a deployer: the model only explains, and code chooses the verdict. A pack can forbid phrases (`never_say`), and the gate refuses unsupported claims. | `core/contracts.py` (`verdict_by_code`, `AdviceShape.never_say`) |
| **Human oversight** | Applies | The same evidence as Agentic dimension 2: people approve published rule values, confirm names before they scope answers, and correct facts. Only the owner may erase a person or reset. | See Agentic dimension 2 |

---

## Findings from this pass

1. **`must_cite` is declared but never read.** Every pack manifest sets `must_cite: true`, but
   no code reads the flag (`grep` finds it only in `core/contracts.py` and the pack YAML). The
   citation rule is enforced, but unconditionally, by `core/graph/gate.py`. Setting
   `must_cite: false` would change nothing. The chapter should cite the gate as the evidence,
   not the flag.
   **Recommendation to Christian (Siew, 2026-10-04):** type `must_cite` as `Literal[True]`,
   like `never_acts` and `verdict_by_code`, so that a pack setting it to `false` fails to load.
   This is a change to `core/contracts.py`, so it needs its own reviewed PR (AGENTS.md rule 4).
   Once it lands, the chapter can say that three guardrails are fixed by type, and that the
   gate enforces citation.
2. **"The Actions module is specified and deliberately not built"**
   (`docs/governance/README.md`). The only "specification" found is a box in Fig 1 of the
   architecture review, "drawn deliberately as a boundary". There is no written specification.
   **The stronger evidence is in the contract:** `PrimitiveId` in `core/contracts.py` admits
   only `reminder`, `alert`, `tracker` and `advice`. A module called `actions` cannot even be
   declared without a reviewed change to the contract (rule 4). The autonomy statement (W7)
   should cite that alongside `never_acts`, and should say "not built" rather than
   "specified".
3. **Faithfulness is below target** (0.819 against 0.90). This is the measured number that
   testing-and-assurance, and the model card, must report as it is.
4. **Incident reporting had nothing behind it.** A procedure is now drafted in
   `incident-and-breach-procedure.md`, awaiting Siew's approval.
5. **Log immutability against erasure: decided (Siew, 2026-10-05).** The framework recommends
   that problematic agent trajectories "cannot be deleted" (p 44). The retention policy erases
   traces and advice records with the document and person. Siew's decision: **keep evidence
   only while an incident is open, and erase as the policy says otherwise.** This is recorded
   as `retention-and-erasure.md` A6. The "problematic trajectories" the framework means are
   exactly an open incident's evidence, so the framework is met for them. Every other record
   follows the erasure policy.
6. **Three gaps the framework names, all small:**
   - no screen says plainly that answers are written by AI (p 47; Zee). The terms now say it
     (Clause D), but the framework wants it in the interface too;
   - ~~no contact point is given to users~~: now in the terms of use, Clause D 3 (helpdesk);
   - the Telegram allow list is open when empty, the risk the OpenClaw case names (p 14;
     Christian).
7. **No written residual-risk evaluation** (p 24). It is a short paragraph, and could sit in
   the autonomy statement (W7).

## For Siew

1. **Agentic framework:** check the statuses above against your reading. **GenAI framework:**
   still to read, then confirm its dimension names and each "Applies?" judgement. *(The ninth
   dimension is decided: human oversight.)*
2. ~~Decide finding 5.~~ **Decided 2026-10-05:** an incident hold (`retention-and-erasure.md` A6).
