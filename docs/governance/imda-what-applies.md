# IMDA frameworks: what applies to PARROT

> **Status: first extract (W1 task), 2026-10-02. Owner: Siew. For Christian's review.**
>
> **Read this first.** Neither framework was read for this draft. IMDA's site cannot be reached
> from the environment this was written in. The dimension names come from the team's own
> architecture review (`docs/artefacts/architecture-review.html`, §10). What each dimension
> *asks* is **not** stated here, because the brief says not to paraphrase an obligation that
> has not been read. This document maps each dimension to **the parts of PARROT that would
> answer it**, each pointing at a file.
>
> **Before this is relied on,** Siew must read both frameworks and check every dimension name
> and its fit. The W6 task (`imda-genai-nine-dimensions.md`) turns this into the full mapping,
> with an artefact or a measured number for each dimension.

## The two instruments

| Instrument | Date | Dimensions | Source of the names used here |
|---|---|---|---|
| IMDA, *Model AI Governance Framework for Generative AI* | May 2024 | Nine | Architecture review §10. Ninth dimension decided by Siew, see below. |
| IMDA / MDDI, *Model AI Governance Framework for Agentic AI* | Launched 22 January 2026; the review notes an update in June 2026 | Four | Architecture review §10 |

**The ninth dimension: decided (Siew, 2026-10-04).** The ninth GenAI dimension is
**human oversight**, as the architecture review lists it. The nine are accountability, data
governance, trusted development, incident reporting, testing and assurance, content provenance,
safety and alignment, cybersecurity, and human oversight.
*Note kept for the record:* the drafting author recalled the published ninth dimension as "AI
for Public Good". The framework's own text has still not been read in this environment, so a
check of the dimension names against the published framework remains worthwhile before the
chapter cites them.

---

## Agentic AI framework: four dimensions

This framework is the one to lead with (`team/siew/README.md`). PARROT is an assistant with
retrieval, memory and scheduled jobs, and its strongest evidence is a boundary enforced in code.

| Dimension | What in PARROT answers it | Evidence |
|---|---|---|
| **1. Risk assessment and bounding** | **The system cannot act.** `never_acts` is typed `Literal[True]`, so a pack that sets anything else does not load. The module types are a closed list (`PrimitiveId`) with no `actions` in it. Advice uses a **closed list** of six calculators, and the verdict is chosen by code (`verdict_by_code: Literal[True]`). Retrieval is one tool call the team wrote. | `core/contracts.py` (`Guardrails`, `AdviceCalculator`); AGENTS.md (stack, rule 8) |
| **2. Human accountability** | People decide wherever a guess would otherwise decide. A published rule value is cited only after a person approves it. A name the model proposes scopes nothing until a person confirms it. A user's correction of a fact is recorded with its old and new value. Only the owner may erase a person or reset (policy; not yet built). | `db/migrations/0003_advice.sql` (`grounding_values.status`, `reviewed_by`); `0002_household.sql` (`person_aliases.confirmed`); `core/corrections.py`; `retention-and-erasure.md` A5 |
| **3. Technical controls** | **No claim without a citation:** the gate drops any sentence with no supporting passage, or one citing a passage that was not retrieved. **Abstention** below a relevance floor. **Advice only under recorded consent**, checked in the same transaction. **Nothing leaves the machine at inference:** every model endpoint must be loopback. **An audit trail** in `traces` and `advice_records`. | `core/graph/gate.py` (`check_one`); `core/graph/answer.py` (`abstain_below`); `core/advice_consent.py`; `core/runtime/settings.py` (`local_url`); `db/migrations/0001_init.sql` (`traces`) |
| **4. End-user responsibility** | The user can check every answer against the page it came from. Every advice card shows the pack's disclaimer, and a product disclosure when a product is named. A pack without advice declines to recommend. The terms say who answers for what is submitted. | `web/components/source-chip.tsx`; `core/pages.py`; `web/components/ask/advice-card.tsx` (`AdviceNote`); `core/contracts.py` (`advice_decline`); `terms-of-use.md` Clauses A–C |

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
| **Testing and assurance** | Applies | The evaluation harness (Ragas) with targets. Run 1, on 2026-09-29: context recall 0.895, context precision 0.868, **faithfulness 0.819 against a 0.90 target**, answer relevancy 0.765 against 0.80. Adversarial Set C is not written yet (W3, overdue). `make check` gates every change. | `eval/`; `eval/results/2026-09-29-baseline-dense-only.md`; `Makefile` |
| **Security** (the review: "cybersecurity") | Partly | Loopback-only services. Screens bound to `127.0.0.1`. The API refuses non-loopback hosts. **Gaps:** the screen lock does not encrypt, the API has no authentication for local callers, and an empty Telegram allow list accepts any chat. Prompt injection is to be tested by Set C. | `data-inventory.md` §3 and §5; `web/lib/lock.ts`; `api/main.py` |
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

## For Siew

1. Read both frameworks. Confirm the dimension names against the published text, and check
   each "Applies?" judgement. *(The ninth dimension is decided: human oversight.)*
2. Decide whether an incident and breach procedure becomes a governance artefact. It would be
   a short document, but at present there is nothing.
