# ISO/IEC 22989 stages and ISO/IEC 5338 processes: what PARROT actually does

Status: draft · Owner: Siew · Reviewer: Christian (technical accuracy) · Evidence read on `main`
at `eb9fc20` (2026-10-17), with the governance drafts of
[feynman82/igd-capstone-2026#92](https://github.com/feynman82/igd-capstone-2026/pull/92)

> Every claim points at a file in this repository. Anything that could not be traced is marked
> **unverified**, and anything planned but not built is marked **not built**.
>
> **To confirm against the standards.** Neither standard has been read for this draft:
> ISO/IEC 22989:2022 and ISO/IEC 5338:2023 are sold, not published. The stage names, the
> 5338 process names and the clause numbers 6.4.7, 6.4.8 and 6.4.14 come from the team's
> architecture review (`docs/artefacts/architecture-review.html`, §10) and the
> `writing-a-governance-artefact` skill. Check each against the text before the chapter cites
> it.

## Two standards, two jobs

- **ISO/IEC 22989** names the AI system life cycle's **stages**.
- **ISO/IEC 5338** supplies the **processes** an organisation carries out. It builds on the
  software and systems life cycle processes of ISO/IEC/IEEE 12207 and 15288, and adds three
  that are specific to AI:
  - **6.4.7 knowledge acquisition**
  - **6.4.8 AI data engineering**
  - **6.4.14 continuous validation**

5338 **does not prescribe a life cycle.** The stage names often attributed to it are 22989's,
and appear in 5338 only as an illustrative figure (`writing-a-governance-artefact` skill;
architecture review §10). This map therefore keeps the two apart. Each row is a 22989 stage;
the second column names the 5338 processes the team performed in it; the third column says
what was actually done, with the file that shows it.

## The map

| 22989 stage | 5338 processes engaged | What PARROT actually does | Evidence | When |
|---|---|---|---|---|
| **Inception** | Project planning; stakeholder needs and requirements definition | Five personas framed the problem. The scope was frozen and split into five lanes, each owning a set of directories. The MVP is two packs and two modules. Every task is in one register, with a reviewer who is never its author. | `README.md` (MVP scope); `team/README.md`; `.github/CODEOWNERS`; `docs/team-tasks.csv` ("Freeze scope and confirm the lane split", W1) | W1 |
| **Design and development** | Architecture definition; design definition; **knowledge acquisition (6.4.7)** | The pack and module contracts are typed, and a pack cannot declare that it acts. 20 ADRs record each non-obvious choice with its alternatives. **6.4.7:** each pack's grounding corpus is assembled from named public sources. Each source records its publisher, publisher kind, URL, retrieval date and review-by date, and is cited only after a person signs it off. | `core/contracts.py` (`PackManifest`, `ModuleManifest`, `GroundingDocument`); `docs/adr/`; `packs/insurance_agent/grounding/sg_protection_guidance/sources.yaml`; `packs/iras_tax/grounding/iras_tax_ya2025_ya2027/sources.yaml`; `core/grounding/corpus.py` | W1–W7 |
| **Verification and validation** | Implementation; integration; verification; **AI data engineering (6.4.8)** | **6.4.8:** the corpus is built register-first. Ground truth is written before any document is generated, then validated (`corpus.validate`). Every field is declared once and the extraction schemas are generated from it. Ingestion parses, chunks, embeds and extracts, and a document that fails goes to quarantine for a second pass that reads the page image. **Verification:** `make check` gates every change, and CI runs it on every pull request. **Validation:** golden Sets A and B and adversarial Set C, with 31 committed result write-ups. | `corpus/README.md`; `corpus/register/`; `core/documents.yaml` → `core/document_schemas.py`; `core/ingest/`; ADR 0006, ADR 0012; `Makefile` (`check`); `eval/`; `eval/results/` | W2–W8 |
| **Deployment** | Transition; validation; configuration management | The stack runs locally from one launcher, with Postgres and Redis published on `127.0.0.1` only. Configuration management is git, with generated files checked for drift. Code freeze is planned for 28 October (`main` tagged). The demonstration has a written run sheet. | `infra/docker-compose.yml`; `scripts/run_parrot.py`; `START.cmd`; `FIRST-RUN.md`; `docs/RUNNING.md`; `docs/team-tasks.csv` ("Code freeze", W9); `docs/demo-run-sheet.md` | W8–W9 |
| **Operation and monitoring** | Operation; **continuous validation (6.4.14)**, in part | Every graph node writes to the `traces` table, which serves as both the audit trail and the evaluation data. A person's correction to a fact is kept beside the model's original value, as a labelled example. Reminder and Alert sweeps run on a schedule. | `db/migrations/0001_init.sql` (`traces`, `facts.verified_by_user`); `core/corrections.py`; `core/worker/schedule.py`; `modules/reminder/`, `modules/alert/` | W8 onward |
| **Continuous validation** | **Continuous validation (6.4.14)** | **During development, performed:** the harness was re-run after every retrieval, extraction or vault change, and each result file names the generator, corpus hash and code commit it ran on. Set C runs in a vault of its own. **After the MVP, not built:** nothing triggers a re-run when the model or a pack version changes. | `eval/results/*.md` headers, 29 Sep–17 Oct; `eval/results/2026-10-15-setc-isolated-vault.md`; `imda-what-applies.md` (Agentic dimension 3, "Robust change management": Partly) | W4–W8 |
| **Re-evaluation** | Measurement; validation | The real-document holdout measures the gap between synthetic and real extraction, once, in a vault of its own. It is never used for tuning. | `eval/holdout.py`; `docs/governance/consent-and-redaction.md`; `docs/team-tasks.csv` ("Evaluation run 3 plus the holdout run", W8) | W8 |
| **Retirement** | Disposal | **Designed, mostly not built.** Erasure is specified: a document is deleted only on instruction, and completely within 72 hours; erasing a person or resetting is owner-only. In code today, only a quarantined document can be deleted. There is no Reset Workspace, and switching a pack off does not remove its facts. The holdout is deleted by **31 December 2026, the end of the MVP**. | `retention-and-erasure.md` Parts A and B; `core/registry.py` (`enabled`); `consent-and-redaction.md` §8 | Post-MVP |

## The three AI-specific processes, plainly

| 5338 process | Performed? | The strongest evidence | What is missing |
|---|---|---|---|
| **6.4.7 Knowledge acquisition** | **Yes** | Each grounding source is typed with publisher, publisher kind, URL, retrieval date and review-by date, and *"nothing is cited until a person has signed it off"* (`core/contracts.py`, `GroundingDocument.reviewed_on`) | The sign-off is recorded per source, not audited |
| **6.4.8 AI data engineering** | **Yes** | Ground truth exists before the document does (register-first), and one source of truth generates the schemas, the register columns and the field dictionary (`AGENTS.md` rule 6; `python -m packs.build`) | The corpus is synthetic. Real-data engineering is the holdout, still to be collected (`consent-and-redaction.md`) |
| **6.4.14 Continuous validation** | **Partly** | 31 result write-ups, each stamped with its code commit, across 29 Sep–17 Oct (`eval/results/`) | No post-deployment trigger: nothing re-runs the harness when the model or a pack changes |

## Processes consciously not performed

**To confirm against the standards.** These process names are those of ISO/IEC/IEEE 12207, on
which 5338 builds. They are listed so the chapter can say what was left out on purpose, and why.

| Process | Why not, for a capstone MVP |
|---|---|
| **Acquisition and supply** (agreement processes) | No acquirer or supplier contract exists. The models are open-weight releases used under their licences (`model-card.md` §1), not procured. |
| **Maintenance** | There is no service after the MVP to maintain. Post-MVP items are named (`core/adapters/README.md`, "Post-MVP"), not scheduled. |
| **Portfolio management, human resource management, infrastructure management** (organisational processes) | The team is five students on one project, with no organisation above it. |
| **Quality management**, as a separate function | Quality is held by `make check`, CODEOWNERS review and the evaluation harness, not by a quality function. `main` is unprotected by convention (ADR 0010). |
| **Continuous validation after deployment** | Not built (row above). A household's own copy would need it before any release beyond the MVP. |

## What the architecture review planned, corrected against the code

The review's §10 table is the plan this map was drawn from. Four of its cells do not match the
code:

| The review says | The code shows |
|---|---|
| Operation and monitoring: "the JSONL trace log" | Traces are a Postgres table, `traces` (`db/migrations/0001_init.sql`), not a JSONL file |
| Retirement: "Pack uninstall removes its facts and jobs" | No uninstall was found. A pack is switched off with a flag (`SET_PACK_ENABLED`, `core/registry.py`), and its facts stay. **No job is removed**: the scheduled sweeps belong to modules, not packs, and keep running. The Reminder sweep and the morning digest skip a disabled pack's obligations (`core/worker/tasks.py`, `enabled_pack_ids`). The Alert sweep does not filter by pack at all, because alert thresholds belong to the core catalogue, "so no pack being switched off silences them" (`modules/alert/__init__.py`, `sweep`; ADR 0017). |
| Retirement: "Reset Workspace purges indexes and embeddings" | No Reset Workspace exists in the code (`retention-and-erasure.md` Part B) |
| Deployment: "Docker Compose stack" | True for Postgres and Redis (`infra/docker-compose.yml`). **The application does not run inside Compose.** The compose file defines only `db` and `redis`, and says Ollama runs on the host. The API, worker and screens are started on the host by `scripts/run_parrot.py` (`make dev`, or `START.cmd` through `scripts/start_parrot.py`). |

## Open questions

1. **Siew:** read the three clause numbers (6.4.7, 6.4.8, 6.4.14) and the stage names against the
   standards before the chapter cites them. The team has only the review's summary.
2. **Christian:** confirm the code freeze date. *(The deployment row is settled: the launcher, not
   Compose, verified 2026-10-19.)*
3. **Christian:** correct the four cells of the architecture review listed above, or note them as
   superseded by this map.
4. **Yew Mun:** is a re-run trigger for model or pack changes in scope before W8? If not, the 6.4.14
   row stays "Partly", and says so.
