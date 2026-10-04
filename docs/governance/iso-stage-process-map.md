# ISO/IEC 22989 stages against ISO/IEC 5338 processes

Status: draft · Owner: Siew · Reviewer: Christian

> Every "what we do" cell points at a file in this repository. Stage names, process numbers
> and process titles are marked **to check against the standard** until they have been read
> in ISO/IEC 22989:2022 and ISO/IEC 5338:2023 themselves. This draft was written from the
> repository's own references (`packs/README.md`, `team/siew/README.md`), not from either
> standard's text.

## The distinction this map rests on

- **ISO/IEC 22989** defines the AI system *life cycle*: the stages a system passes through.
- **ISO/IEC 5338** defines AI system life cycle *processes*: the work that is done. It does
  not prescribe a life cycle. Where it shows stage names, it borrows them from 22989 as an
  illustration.

So the map has stages as rows and processes as the work done in each. A process can recur
across stages. Continuous validation, for one, runs from verification through operation.

## The map

Stage names follow 22989's life-cycle figure, **to check against the standard**.

| 22989 stage | 5338 process(es) we perform | What we actually do | Evidence |
|---|---|---|---|
| **Inception** | Stakeholder needs and requirements definition (**to check**: process number) | Problem framing, the household personas and the scope boundary: v1 advises and never acts | `docs/artefacts/PARROT_Revised_Proposal_v3.docx`; user stories (Zee, task "Write the user stories", Done); `core/contracts.py` `never_acts: Literal[True]` |
| **Design and development** | Architecture definition; **6.4.7 knowledge acquisition**; **6.4.8 AI data engineering** | Architecture decided and recorded as ADRs. Regulator and government sources indexed per pack with provenance. A synthetic corpus built register-first: ground truth written before any document is generated | `docs/adr/0001`–`0019`; `packs/*/grounding/*/sources.yaml` (publisher, URL, `review_by`); `corpus/canon.md`, `corpus/register/batch1.csv`, `batch2.csv`, `corpus/validate.py` |
| **Verification and validation** | Verification; **6.4.14 continuous validation** (first runs) | Every push runs the generated-file checks, lint, types and tests. Golden sets A (answerable), B (hard negatives) and C (adversarial) are scored against the register | `.github/workflows/ci.yml`; `tests/`; `eval/sets/`; `eval/results/2026-09-29-baseline-dense-only.md` (run 1), `2026-09-30-run2-hybrid-plus-reranker.md` (run 2) |
| **Deployment** | Transition (**to check**) | Installed on one household computer. Every service URL is loopback, and anything else is rejected at startup | `infra/docker-compose.yml` (ports bound to `127.0.0.1`); `infra/.env.example`; `core/runtime/settings.py`; `docs/RUNNING.md`; `START.cmd` |
| **Operation and monitoring** | Operation; maintenance (**to check**) | Each ingest and correction is traced. Documents that fail to parse are quarantined and given a second pass on the page image. Reminders and alerts run over obligations | `traces` table (`db/migrations/0001_init.sql`); `core/ingest/quarantine.py` (the "recovery rate"); `modules/reminder/`, `modules/alert/`; `eval/results/w7-module-metrics.md` |
| **Continuous validation** | **6.4.14 continuous validation** | Evaluation is scheduled weekly and runs are committed append-only, so a regression shows as a trend. A person's correction to a fact is recorded as a labelled example | `.github/workflows/eval.yml` (`cron: "0 18 * * 5"`); `eval/results/README.md` ("Append-only"); `core/corrections.py`; `facts.verified_by_user` |
| **Re-evaluation** | Decision management (**to check**) | A change to retrieval or a guardrail is measured before and after, and the decision is recorded. A grounding source carries a review date after which calculators will not use it | `eval/results/2026-09-30-floor-*-relevance.md`; ADRs 0018 and 0019; `sources.yaml` `review_by`, enforced in SQL per ADR 0016 |
| **Retirement** | Disposal (**to check**) | A pack can be disabled, which hides its documents. A quarantined document can be forgotten. **Full erasure of a household's data is not built** | `core/vault.py` (disabled packs hidden); `core/ingest/quarantine.py` `forget`; `docs/governance/retention-and-erasure.md` (no Reset Workspace) |

## The three AI-specific processes, in detail

**6.4.7 Knowledge acquisition.** Published guidance a pack calculates with lives in
`packs/<pack>/grounding/<corpus_id>/`, kept separate from the household's own documents.
Every source records its publisher, URL, retrieval date and review-by date
(`packs/README.md`, "Grounding"). Values are extracted from verbatim passages and stay
`pending` until a person approves them (`db/migrations/0003_advice.sql`, `grounding_values`
`status`; ADR 0016). Two corpora exist: `insurance_agent/grounding/sg_protection_guidance`
and `iras_tax/grounding/iras_tax_ya2025_ya2027`.

**6.4.8 AI data engineering.** The evaluation corpus is generated, not collected
(`docs/governance/synthetic-data-case.md`). It is built register-first: Desmond writes the
expected value of every field in `corpus/register/` before the document exists, and
`corpus/validate.py` checks a batch against it. Every document agrees with
`corpus/canon.md`. Field names are defined once in `core/documents.yaml` and generated
everywhere else (`python -m packs.build`). The real-document holdout comes later, under a
consent and redaction protocol that does not yet exist (see open questions).

**6.4.14 Continuous validation.** There are three golden sets: A answerable, B hard
negatives, C adversarial (`eval/sets/README.md`). They are scored by code where possible and
by a local judge model where not (`eval/score.py`). Every run is committed with a paragraph
saying what changed and whether the movement was expected (`eval/results/README.md`). Run 2
reports run 1's configuration on run 2's corpus as a separate column, so document growth and
retriever change are not confused (`eval/results/2026-09-30-run2-hybrid-plus-reranker.md`).

## What we consciously do not do

| Not performed | Why | Evidence |
|---|---|---|
| **Model training, fine-tuning or retraining** | We use Qwen-SEA-LION-v4-4B-VL as published, quantised, through Ollama. Corrections are kept as labelled examples, not trained on | `AGENTS.md` (stack); `infra/.env.example` `PARROT_GEN_MODEL`; `core/corrections.py` |
| **Collecting training data** | There is no training, so no training set. The corpus exists to evaluate | `docs/governance/synthetic-data-case.md` |
| **Online or production monitoring across users** | v1 is one household on one computer, with no telemetry and no network mode | `core/runtime/settings.py` (loopback only) |
| **Autonomous action** | v1 advises and never acts. The Actions module is specified, not built | `core/contracts.py` `never_acts: Literal[True]` |

**To check against the standard:** the process numbers and titles for these, so the table
can name the 5338 process each row declines.

## Open questions

1. For Siew: read both standards (SMU library or Singapore Standards eShop). Confirm the
   22989 stage names, and the titles and numbers of 5338 processes 6.4.7, 6.4.8 and 6.4.14.
   Fill in the processes marked **to check**. Record the edition read.
2. For Christian: is `.github/workflows/eval.yml`'s weekly schedule actually running? It
   targets a `[self-hosted, gpu]` runner. If that runner is not registered and online, the
   schedule never fires. Continuous validation is then the manual runs in `eval/results/`,
   and the Continuous validation row should say so. **Unverified.**
3. For Siew with Desmond: the consent and redaction protocol is a precondition of 6.4.8 for
   the holdout. It is not in `docs/governance/` yet.
4. For Christian: Retirement depends on the Reset Workspace question raised in
   [feynman82/igd-capstone-2026#45](https://github.com/feynman82/igd-capstone-2026/pull/45).
