# Graph Report - igd-capstone-2026  (2026-09-10)

## Corpus Check
- 67 files · ~51,336 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 481 nodes · 493 edges · 53 communities (47 shown, 6 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fa22c956`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- contracts.py
- NNNN · The decision, as a statement not a question
- README.md
- validate
- 4. Writing `pack.yaml`
- Project PARROT — team split
- Project PARROT — team split
- Domain packs — start here
- Running the evaluation harness
- Christian — task list
- Desmond — task list
- Siew — task list
- Yew Mun — task list
- Zee — task list
- Filling the corpus register
- Writing a governance artefact
- Siew — Lane C · Governance and assurance
- igd-capstone-2026
- Zee — Lane D · Domain packs and interface
- Authoring a domain pack
- Household canon
- 0001_init.sql
- build_team_tasks.py
- `core/graph/` — the LangGraph runtime
- `core/ingest/` — the ingestion worker
- Integration review
- Writing an ADR
- `core/retrieve/` — hybrid retrieval
- Graphify — the shared knowledge graph
- `web/` — the interface
- `api/` — the FastAPI application
- The corpus
- Artefacts
- Why the prototype is evaluated on synthetic data
- `core/adapters/` — capture adapters
- README.md
- Project skills
- Evaluation
- pull_request_template.md
- Grounding corpora
- Notice
- Changelog
- filesystem
- Governance artefacts
- __init__.py
- __init__.py
- parrot
- Siew — task list
- `docs/report/` — the final report

## God Nodes (most connected - your core abstractions)
1. `Strict` - 14 edges
2. `validate()` - 13 edges
3. `PackManifest` - 11 edges
4. `Christian — task list` - 11 edges
5. `Desmond — task list` - 11 edges
6. `Siew — task list` - 11 edges
7. `Yew Mun — task list` - 11 edges
8. `Zee — task list` - 11 edges
9. `First run` - 10 edges
10. `Running the evaluation harness` - 10 edges

## Surprising Connections (you probably didn't know these)
- `load()` --references--> `PackManifest`  [EXTRACTED]
  packs/build.py → core/contracts.py
- `render_dictionary()` --references--> `PackManifest`  [EXTRACTED]
  packs/build.py → core/contracts.py
- `render_register_columns()` --references--> `PackManifest`  [EXTRACTED]
  packs/build.py → core/contracts.py
- `render_schemas()` --references--> `PackManifest`  [EXTRACTED]
  packs/build.py → core/contracts.py
- `test_a_row_with_no_fields_carries_no_ground_truth()` --calls--> `validate()`  [EXTRACTED]
  tests/test_register_validation.py → corpus/validate.py

## Import Cycles
- None detected.

## Communities (53 total, 6 thin omitted)

### Community 0 - "contracts.py"
Cohesion: 0.09
Nodes (33): BaseModel, AlertConfig, DocumentTypeSpec, FieldSpec, Grounding, Guardrails, ModuleManifest, ModuleTrigger (+25 more)

### Community 1 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.09
Nodes (18): 1. Record architecture decisions, Consequences, Context, Decision, 2. One PostgreSQL instance for everything, Consequences, Context, Decision (+10 more)

### Community 2 - "README.md"
Cohesion: 0.11
Nodes (17): Also yours, Christian — Lane A · Integration and product owner, Starter prompt for your coding agent, The five things you ship, Week 1, in order, What integration actually means here, Christian — task list, W10 — due 2026-11-10 (+9 more)

### Community 3 - "validate"
Cohesion: 0.22
Nodes (18): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), Path, Validate a document register before it is handed over.      python -m corpus.v, Derived from the pack manifests, never hardcoded.      A register row can only (+10 more)

### Community 4 - "4. Writing `pack.yaml`"
Cohesion: 0.12
Nodes (15): 1. What a pack is, 2. The one thing to understand before you start, 3. The workflow, 4. Writing `pack.yaml`, 5. The grounding corpus, 6. Definition of done, 7. Where to ask, Authoring a domain pack (+7 more)

### Community 5 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 6 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 7 - "Domain packs — start here"
Cohesion: 0.15
Nodes (13): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 7. Grounding — the optional second half, 8. Starter prompt for Claude Code (+5 more)

### Community 8 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 9 - "Christian — task list"
Cohesion: 0.18
Nodes (10): 1 · Collaborators, 2 · Branch protection, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 10 - "Desmond — task list"
Cohesion: 0.10
Nodes (19): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Starter prompt for your coding agent, The one rule that changes everything: register first, The second half: adversarial testing, Two rules you cannot bend, Volumes, Where the column headings come from (+11 more)

### Community 11 - "Siew — task list"
Cohesion: 0.06
Nodes (25): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents, Adversarial Set C (+17 more)

### Community 12 - "Yew Mun — task list"
Cohesion: 0.10
Nodes (18): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation, W10 — due 2026-11-10 (+10 more)

### Community 13 - "Zee — task list"
Cohesion: 0.25
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 14 - "Filling the corpus register"
Cohesion: 0.20
Nodes (9): Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one, Two rules that cannot bend (+1 more)

### Community 15 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (9): Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six, Where governance touches the code (+1 more)

### Community 16 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.33
Nodes (5): Before you say you are done, Claude Code — read this first, Finding your way around, Skills and commands, The three things agents get wrong here

### Community 17 - "igd-capstone-2026"
Cohesion: 0.08
Nodes (22): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it, Authoring a pack (+14 more)

### Community 18 - "Zee — Lane D · Domain packs and interface"
Cohesion: 0.22
Nodes (9): Half one — domain packs (weeks 1 to 7), Half two — the interface (weeks 4 to 8), Read this first, Rules that apply to you specifically, The two halves of this lane, What "done" looks like, What you present, Your Claude Code skills (+1 more)

### Community 19 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 20 - "Household canon"
Cohesion: 0.25
Nodes (7): Address, Employment, Household canon, Life events that documents must reflect, People, Policies, Vehicles

### Community 21 - "0001_init.sql"
Cohesion: 0.36
Nodes (7): chunks, documents, facts, modules, obligations, packs, traces

### Community 22 - "build_team_tasks.py"
Cohesion: 0.39
Nodes (7): main(), Path, Generate each member's task list from the master task CSV.      python scripts, _read_rows(), _render(), _week_key(), _write()

### Community 23 - "`core/graph/` — the LangGraph runtime"
Cohesion: 0.40
Nodes (4): `core/graph/` — the LangGraph runtime, Rules, What belongs here, What does not

### Community 24 - "`core/ingest/` — the ingestion worker"
Cohesion: 0.50
Nodes (3): `core/ingest/` — the ingestion worker, Quarantine is two-stage, Rules

### Community 25 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 26 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 27 - "`core/retrieve/` — hybrid retrieval"
Cohesion: 0.50
Nodes (3): `core/retrieve/` — hybrid retrieval, Rules, What belongs here

### Community 28 - "Graphify — the shared knowledge graph"
Cohesion: 0.20
Nodes (9): Graphify — the shared knowledge graph, Keeping it fresh, Merge conflicts, solved properly, Setup, once per clone, The hook leaves your tree dirty, and that is expected, Two kinds of extraction, and which needs what, Using it, What is committed, and what is not (+1 more)

### Community 29 - "`web/` — the interface"
Cohesion: 0.50
Nodes (3): Before building any screen, Rules, `web/` — the interface

### Community 31 - "The corpus"
Cohesion: 0.33
Nodes (5): The corpus, The order matters, Tiers, Two rules, Validate before handing over

### Community 32 - "Artefacts"
Cohesion: 0.33
Nodes (5): A note on the model, Artefacts, Current deliverables, Regenerating, Source material

### Community 33 - "Why the prototype is evaluated on synthetic data"
Cohesion: 0.33
Nodes (5): The decision, What synthetic data does not prove, What we do not do, Why, Why the prototype is evaluated on synthetic data

### Community 36 - "Project skills"
Cohesion: 0.40
Nodes (4): Changing them, Project skills, Slash commands, Using them

### Community 37 - "Evaluation"
Cohesion: 0.40
Nodes (4): Evaluation, Ground truth comes free, The honesty check, Writing questions

### Community 38 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 39 - "Grounding corpora"
Cohesion: 0.40
Nodes (4): Grounding corpora, Owner, Rules, Structure

### Community 40 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 41 - "Changelog"
Cohesion: 0.50
Nodes (3): Changelog, W1 · 2–8 Sep 2026, W2 · 9–15 Sep 2026

### Community 42 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 43 - "Governance artefacts"
Cohesion: 0.50
Nodes (3): `docs/governance/` — the assurance artefacts, The autonomy statement in one line, The rule that governs all eight

### Community 51 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 52 - "`docs/report/` — the final report"
Cohesion: 0.33
Nodes (5): `docs/report/` — the final report, Ownership, The rule that keeps it honest, The thing to understand before you write a word, Three questions for the supervisors, at the 6 October mid-term

## Knowledge Gaps
- **289 isolated node(s):** `The thing to understand before you write a word`, `Ownership`, `The rule that keeps it honest`, `Three questions for the supervisors, at the 6 October mid-term`, `1 · Collaborators` (+284 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Domain packs — start here` connect `Domain packs — start here` to `Siew — task list`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **What connects `The thing to understand before you write a word`, `Ownership`, `The rule that keeps it honest` to the rest of the system?**
  _289 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `contracts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08636977058029689 - nodes in this community are weakly interconnected._
- **Should `NNNN · The decision, as a statement not a question` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._
- **Should `README.md` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Should `4. Writing `pack.yaml`` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `Project PARROT — team split` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._