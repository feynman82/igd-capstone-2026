# Alignment with the IMDA Model AI Governance Framework for Agentic AI

Status: draft · Owner: Siew · Reviewer: Christian

**Instrument:** Infocomm Media Development Authority (IMDA), *Model AI Governance Framework
for Agentic AI*, Version 1.5. Published 20 May 2026, updated 5 June 2026. Copy read: the PDF
release supplied by Siew on 2026-10-05 (file `Mgf_for_Agentic_AI_atx_Release_July_2026.pdf`, 53
pages). Section numbers below are the framework's own.

> This supersedes the repository's references to "the Agentic AI framework published
> 22 January 2026". That was version 1.0. Version 1.5 keeps the four dimensions and adds,
> among others: controls and logging as core agent components; structural versus prompt-layer
> controls; change management; and automation-bias measures ("What's new in this version",
> p. 5).
>
> Every claim about Parrot points at a file. A gap is named as a gap, with an owner.

## 1. Where Parrot sits

The framework defines an agent by "some degree of independent planning, decision-making, and
action-taking … over multiple steps" (§1.1). It describes what an agent can do on two axes
(§1.1.3):
- **action-space:** the tools it can use;
- **autonomy:** how far it decides its own steps.

| Axis | Parrot v1 | Evidence |
|---|---|---|
| **Action-space** | **The smallest the framework describes.** Parrot reads the household's own documents. It writes only to its own database: facts, obligations, a person's corrections. It has no tool that touches an outside system on the model's initiative: it cannot pay, renew, book, file, send or sign | `core/contracts.py:249` (`never_acts: Literal[True]`); `AGENTS.md` ("Retrieval is one tool call we wrote ourselves") |
| **Autonomy** | **Low.** A fixed graph routes the question, gathers evidence and answers. The model does not choose its own steps. Verdicts for advice are chosen by code | `core/graph/answer.py` (module docstring: "The graph declares the part that is a pipeline"); `core/contracts.py:250` (`verdict_by_code`) |
| **Human involvement** (§1.1.3 levels) | Below "agent proposes, human operates". Parrot proposes no actions; it answers and advises, and the person acts | `web/components/ask/answer.tsx` ("Parrot does not act") |
| **Multi-agent** (§1.1.2, §1.2.3) | No. One sequential pipeline | `core/graph/answer.py` |

**So most of the framework's agent-specific risks do not arise in v1.** That is the design
decision, not an accident. The framework itself says "not all use cases are suitable for
agents, and some may be better served by deterministic workflows" (§2.1.1). This document
still walks all four dimensions, for two reasons:
- The specified-but-unbuilt **Actions module** would move Parrot up both axes. The framework
  says what must be true first (section 6).
- Several of the framework's practices apply to Parrot already, and the evidence is in the
  code.

## 2. Dimension 1: Assess and bound the risks upfront (§2.1)

### Risk factors (§2.1.1)

| Factor | Parrot v1 | Level | Evidence |
|---|---|---|---|
| *Impact:* domain and use case | Household finance, insurance and tax. Low tolerance for error | **High** | `packs/insurance_agent/`, `packs/iras_tax/` |
| *Impact:* access to sensitive data | Yes: identity numbers, income, health-related cover, a child's records. Held in persistent storage, which the framework names as raising the risk | **High** | `docs/governance/data-inventory.md` |
| *Impact:* access to external systems | None at inference. Telegram is used for capture only, and its replies and deletions are fixed code, not model-chosen | Low | `core/runtime/settings.py` (loopback only); `core/adapters/telegram.py` |
| *Impact:* scope of actions | Read-only over documents. Writes only to its own tables | Low | `core/ingest/sql.py`; `core/corrections.py` |
| *Impact:* reversibility | No external action exists to reverse | Low | `core/contracts.py:249` |
| *Likelihood:* autonomy | Fixed pipeline | Low | `core/graph/answer.py` |
| *Likelihood:* task complexity | Moderate: find evidence across documents, scope to the right person, decide whether to answer | Medium | `core/graph/scope.py`; `core/graph/gate.py` |
| *Likelihood:* exposure to external systems | Documents are untrusted input, and a document can carry a prompt injection | **Medium** | `eval/sets/adversarial/` (c-c04 to c-c06) |
| *Likelihood:* third-party components | Model weights from AI Singapore, quantised by a third party (`mradermacher`). Reranker from BAAI. All run locally, so no vendor sees the data | Medium | `docs/governance/model-card.md` §1 |
| *Likelihood:* system complexity | Single agent, sequential | Low | `core/graph/answer.py` |

**Threat modelling and taint tracing** (§2.1.1) are recommended: tracing how untrusted data
moves through the system. The untrusted path is page text → `chunks` → retrieved passages →
the generation prompt. **Gap G1:** no written threat model exists. Set C tests the path; it
does not map it.

### Bounding the risks by design (§2.1.2)

The framework's rule: "prefer deterministic rather than non-deterministic limits, and bound by
design" (§2.1.2). Parrot's limits, by type:

| Limit | Structural (code) or prompt-layer | Evidence |
|---|---|---|
| Cannot act | **Structural.** No action tool exists, and a pack that sets `never_acts` otherwise fails to load | `core/contracts.py:249` |
| Verdicts chosen by code, not the model | **Structural** | `core/contracts.py:250`; ADR 0016 |
| Every fact has a source page | **Structural.** Database constraint | `db/migrations/0001_init.sql` (`facts.document_id`, `facts.page` `NOT NULL`) |
| No SQL written at runtime | **Structural.** Every statement is hand-written | `AGENTS.md` rule 1; `core/ingest/sql.py` |
| Nothing leaves the machine | **Structural.** Non-loopback URLs are refused at start-up | `core/runtime/settings.py` lines 21, 34 |
| Advice only on approved, in-date rule values | **Structural.** Enforced in SQL | ADR 0016; `db/migrations/0003_advice.sql` (`grounding_values.status`) |
| Requests to act are refused | **Prompt-layer.** The model classifies intent. The structural backstop is that no action tool exists | `core/graph/answer.py` (`ROUTE_SYSTEM`, `_ROUTE_SCHEMA`) |
| Answers stay within the evidence | **Both.** The answer prompt, then a code gate that checks claims against cited passages | `core/graph/gate.py` |

**Agent identity** (§2.1.2) is designed for agents that act across organisational
boundaries. Parrot is one local agent acting for one household, so a cryptographic agent
identity has nothing to attach to. The equivalent controls are:
- the local passphrase (`web/lib/lock.ts`);
- Telegram's chat allow list (`core/adapters/telegram.py`);
- the household roster (`db/migrations/0002_household.sql`).

**Gap G2:** the Telegram allow list is enforced only when it is non-empty. With no chat ids
configured, a message from any chat is accepted (`core/adapters/telegram.py` lines 144–146:
`if self._settings.allowed_chat_ids and chat_id not in …`). The framework asks for
least-privilege, deny-by-default access (§2.1.2, §2.2.2). This is a code change: Christian.

**Residual risk** (§2.1.2): "organisations should evaluate and determine if the residual risk …
is of a tolerable level and can be accepted". Parrot's measured residual risk is that it
answers when it should abstain: 0.52 against a 0.95 target in run 2
(`eval/results/2026-09-30-run2-hybrid-plus-reranker.md`). **Open question Q1:** is that
acceptable for a system that advises and never acts? Siew to decide, with Yew Mun.

## 3. Dimension 2: Make humans meaningfully accountable (§2.2)

### Responsibility along the value chain (§2.2.1)

| Framework role | Who, for Parrot | Evidence |
|---|---|---|
| Model developers | AI Singapore (generator), on Alibaba's Qwen3-VL base; BAAI (reranker); Google (`embeddinggemma`) | `docs/governance/model-card.md` |
| Platform providers | Ollama, LangGraph, PostgreSQL with pgvector | `AGENTS.md`; `infra/docker-compose.yml` |
| System provider / app developer | The five-person team, by lane | `CLAUDE.md`; `.github/CODEOWNERS` |
| Pack authors (a third party in future) | ADR 0016 calls a pack "a developer-built add-on a household downloads" | ADR 0016 |
| Deployer and end user | The household, which is both | `README.md` |

**Within the team**, responsibility is allocated by directory and enforced by
`.github/CODEOWNERS`. Every task names a reviewer who is never its owner
(`docs/team-tasks.csv`). This matches the framework's call to allocate responsibility across
the lifecycle (§2.2.1, "Within the organisation").

**Gap G3:** the framework asks deployers to clarify obligations with third parties, and to
address third-party opacity (§2.2.1, "Outside the organisation"). Pack authors are the
foreseeable third party. Nothing yet says what a pack author is accountable for. This belongs
in the pack-authoring guide: Zee, with Siew.

### Meaningful human oversight (§2.2.2)

The framework asks for approval checkpoints before high-stakes or irreversible actions.
Parrot has no actions, but it already puts a person in front of every decision that changes
what it believes:

| Checkpoint | What a person must do first | Evidence |
|---|---|---|
| Advice | Give recorded consent, per person and per pack, with the wording hashed | `db/migrations/0003_advice.sql` (`advice_consents`); ADR 0016 |
| A rule value a calculator uses | Approve it, with name and date recorded | `0003_advice.sql` (`grounding_values` `CHECK`) |
| A name the model proposes for a person | Confirm it; until then it scopes nothing | `0002_household.sql` (`person_aliases.confirmed`) |
| A fact the extractor got wrong | Correct it; the correction is recorded | `core/corrections.py`; `facts.verified_by_user` |

**Deny by default when approval is missing** (§2.2.2): advice without consent returns
`consent_required`, and an unapproved rule value is never read (`core/graph/answer.py`; ADR
0016).

**Automation bias** (§2.2.2). The framework suggests tracking the human override rate.
Parrot's risk is a household trusting a cited answer. Run 1's finding was "a citation is not
a warrant": six wrong answers each cited a real page
(`eval/results/2026-09-29-baseline-dense-only.md`). **Gap G4:** the correction rate, which is
Parrot's equivalent of the override rate, is recorded in `traces` but not measured. Yew Mun.

## 4. Dimension 3: Implement technical controls and processes (§2.3)

### Controls (§2.3.1)

Structural controls are listed in section 2. Against the framework's sample controls:

| Framework control | Parrot | Evidence |
|---|---|---|
| Strict input formats for tools | Model outputs that drive control flow are schema-constrained | `core/graph/answer.py` (`_ROUTE_SCHEMA`) |
| Least-privilege tools | One retrieval tool; no write tool for the model | `AGENTS.md` |
| No write access to sensitive tables unless needed | The model writes nothing directly. Ingestion writes through fixed statements | `core/ingest/sql.py` |
| Sandbox code execution | No code execution exists | — |
| MCP whitelisting | No MCP | — |

### Testing before deployment (§2.3.2)

| Framework test | Parrot | Evidence |
|---|---|---|
| Overall task execution | Set A, answerable questions with known answers | `eval/sets/answerable/` |
| Policy compliance | Set C, 15 items that must be refused. Drafted, not yet run | `eval/sets/adversarial/` |
| Robustness to edge cases | Set B, 25 hard negatives that must be abstained on | `eval/sets/hard_negatives/` |
| Testing repeatedly | Run 1 run twice to measure the noise floor (~0.05) | run 1 write-up, "How much of a delta is a delta" |
| Deterministic plus LLM evaluation | Code-scored metrics, plus a local LLM judge | `eval/score.py` |
| Realistic environment | **Partly.** Synthetic corpus only, until the holdout run | `docs/governance/synthetic-data-case.md` |
| Tool-calling accuracy | Not applicable: no action tools | — |

### Monitoring and change management (§2.3.3)

| Framework practice | Parrot | Evidence |
|---|---|---|
| Log each step | One trace line per graph node | `db/migrations/0001_init.sql` (`traces`) |
| **Log immutability** | **Not met.** Traces are ordinary rows. Kept unredacted as the audit trail (Siew, 2026-10-04), but deletable | `docs/governance/data-inventory.md` Q2. **Gap G5** |
| Alert thresholds on agent behaviour | **None.** The Alert module watches household data, not the agent | `modules/alert/`. Proportionate for v1; revisit with Actions |
| Gradual rollout | One household. Synthetic corpus first, then a 40-document holdout under a consent protocol | `team/desmond/README.md` |
| Change triggers | Technical: an embedding change is a migration, its own reviewed PR. Regulatory: each grounding source carries a `review_by` date, after which calculators stop using it | `infra/.env.example`; `packs/*/grounding/*/sources.yaml` |
| Changes categorised by risk | Contracts and migrations are separate reviewed PRs. A dependency needs an ADR | `CLAUDE.md`; `AGENTS.md` rule 5 |
| Re-test after change | Evaluation runs committed append-only, with a weekly schedule | `eval/results/README.md`; `.github/workflows/eval.yml` (unverified that the runner is online) |

## 5. Dimension 4: Enable end-user responsibility (§2.4)

The household is the framework's "user who interacts with agents" (§2.4.2). The framework
asks for transparency on five points:

| Framework asks the user be told | Parrot | Evidence |
|---|---|---|
| Their own responsibilities | Pack disclaimers tell the user to confirm before acting, e.g. "confirm reliefs and amounts on myTax Portal or with IRAS before you file" | `packs/iras_tax/pack.yaml` (`disclaimer`) |
| That they are dealing with an AI, at the point of interaction | **Unverified.** No on-screen statement found that answers are AI-generated. **Gap G6** | `web/`. Zee to confirm |
| The agent's range of actions | Shown: "Advises, never acts. This pack cannot pay, renew, book or file anything." | `web/app/(app)/packs/page.tsx`; `web/components/ask/answer.tsx` |
| How their data is used | Written in the data inventory; consent recorded for advice | `docs/governance/data-inventory.md`; `advice_consents` |
| Who to contact if it malfunctions | The household runs it, so there is no operator to escalate to. **Gap G7** for any future pack author | — |

**Tradecraft** (§2.4.3) is the framework's concern that people lose the skill an agent takes
over. Parrot cites the page for every answer, so the household can read the document itself.
The system points back to the source rather than replacing it (`facts.page NOT NULL`;
`web/components/ask/answer.tsx`).

## 6. What would have to be true before Parrot acts

The **Actions module** is specified and deliberately not built. If it were built, Parrot would
gain an action-space, and the framework then requires, as a minimum:

1. **A risk tier per action**, by severity and reversibility (§2.1.1, the Dayos case).
   Example: a calendar entry is reversible; a payment or an email to an insurer is not.
2. **Human approval before every irreversible action**, enforced in code, not in the prompt
   (§2.2.2; the OpenClaw case: "Enforce human approval through system-level controls where
   possible").
3. **Deny by default** when approval cannot be obtained (§2.2.2).
4. **Tests that disallowed actions fail**, before release (OpenClaw case: "attempt disallowed
   actions to ensure restrictions work").
5. **Immutable logs** of every action (§2.3.3), which closes G5.
6. **A narrower allow list** on any channel that can trigger an action, which closes G2.

Until all six exist, `never_acts` stays `Literal[True]`. This section is the core of the
autonomy statement (due 20 October).

## Gaps

| # | Gap | Framework | Owner |
|---|---|---|---|
| G1 | No written threat model or taint trace for documents as untrusted input | §2.1.1 | Siew, with Desmond |
| G2 | An empty Telegram allow list accepts every chat | §2.1.2, §2.2.2 | Christian (code) |
| G3 | Pack authors' obligations are undefined | §2.2.1 | Zee, with Siew |
| G4 | Correction rate (the override rate) is not measured | §2.2.2 | Yew Mun |
| G5 | Traces are not immutable | §2.3.3 | Christian. Decide with the retention policy |
| G6 | No confirmed on-screen statement that answers are AI-generated | §2.4.2 | Zee |
| G7 | No escalation contact for a downloaded pack | §2.4.2 | Zee |

## Open questions

1. **Q1, residual risk.** Is an abstention rate of 0.52 acceptable for v1, given it advises
   and never acts? It needs a stated decision (§2.1.2). Siew.
2. **Q2, the framework's URL.** Add IMDA's web address for version 1.5 to the instrument line.
   Siew.
3. **Q3, other repository references.** `team/siew/README.md` and `docs/governance/README.md`
   are updated in this change. `.claude/skills/writing-a-governance-artefact/SKILL.md` still
   says "22 January 2026", and it is Christian's file to correct.
