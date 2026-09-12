# Graph Report - igd-capstone-2026  (2026-09-12)

## Corpus Check
- 202 files · ~137,395 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2085 nodes · 4277 edges · 154 communities (137 shown, 17 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 363 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1bb59034`
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
- Passage
- test_modules.py
- Settings
- Registrar
- retrieve.py
- cli.py
- register_document
- FolderCapture
- InstalledPack
- extract
- pipeline.py
- FolderAdapter
- FolderCapture
- pipeline.py
- TelegramAdapter
- ParsedPage
- Ollama
- README.md
- ingest.py
- obligations.py
- extract.py
- Starting Parrot
- RUNNING.md
- DoclingParser
- Notion
- start_parrot.py
- Desmond — Lane E · Corpus and adversarial testing
- PaperBrain
- Working agreement for coding agents
- NNNN · The decision, as a statement not a question
- Siew — Lane C · Governance and assurance
- Yew Mun — Lane B · Retrieval and evaluation
- test_startup.py
- Architecture
- Roadmap
- 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module
- Christian — Lane A · Integration and product owner
- The team
- 1. Record architecture decisions
- 4. Local setup can run before the household assistant is ready
- 6. pypdfium2 renders the page images the quarantine second pass reads
- IngestJob
- Home Contents Insurance Policy
- __init__.py
- __init__.py
- __init__.py
- __init__.py
- setup.sh
- schedule.py
- tasks.py
- ingest.py
- Inline
- bytes_for
- worker.py
- base.py
- dispatch.py
- Ollama
- Intake
- _payload_for
- FakeCursor
- extract.py
- Cursor
- retry_quarantine
- ask.py
- 7. The answer graph ships before hybrid retrieval and before a checkpoint table
- __init__.py
- test_the_reminder_cron_is_read_from_its_manifest_not_written_twice
- test_alert_is_swept_nightly_even_though_its_manifest_says_fact_write
- __init__.py
- SentenceScanner
- __init__.py
- register.py
- Finished
- page.tsx
- Ollama
- answer.tsx
- AnswerGraph
- ingest.py
- enabled_pack_ids
- ports.py
- page.tsx
- api.ts
- item-row.tsx
- worker.py
- page.tsx
- modules.py
- Any
- page.tsx
- page.tsx
- FakeCursor
- DoclingParser
- Parser
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- InstalledPack
- Ollama
- Client
- next.config.ts
- postcss.config.mjs

## God Nodes (most connected - your core abstractions)
1. `FakeConn` - 62 edges
2. `Ollama` - 53 edges
3. `Settings` - 50 edges
4. `rows_for()` - 44 edges
5. `Passage` - 43 edges
6. `settings()` - 43 edges
7. `client_for()` - 43 edges
8. `ModelUnavailable` - 40 edges
9. `InstalledPack` - 39 edges
10. `SentenceScanner` - 34 edges

## Surprising Connections (you probably didn't know these)
- `_settings()` --indirect_call--> `settings()`  [INFERRED]
  api/routes.py → tests/test_api.py
- `Alert` --uses--> `AlertConfig`  [INFERRED]
  modules/alert/__init__.py → core/contracts.py
- `Measurement` --uses--> `AlertConfig`  [INFERRED]
  modules/alert/__init__.py → core/contracts.py
- `FakeCursor` --uses--> `AlertConfig`  [INFERRED]
  tests/test_modules.py → core/contracts.py
- `FakeConn` --uses--> `Citation`  [INFERRED]
  tests/test_api.py → core/graph/answer.py

## Import Cycles
- None detected.

## Communities (154 total, 17 thin omitted)

### Community 0 - "contracts.py"
Cohesion: 0.22
Nodes (14): _class_name(), _docstring(), _field_line(), load(), main(), Path, Generate everything downstream of a pack.yaml.      python -m packs.build, The header row Desmond fills in, one file per pack.      Long format: one row (+6 more)

### Community 1 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 2 - "README.md"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.22
Nodes (18): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), date, Path, Validate a document register before it is handed over.      python -m corpus.val (+10 more)

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
Cohesion: 0.15
Nodes (16): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+8 more)

### Community 10 - "Desmond — task list"
Cohesion: 0.18
Nodes (11): Desmond — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 11 - "Siew — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

### Community 12 - "Yew Mun — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

### Community 13 - "Zee — task list"
Cohesion: 0.29
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
Cohesion: 0.16
Nodes (20): Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker.      Celery is imported here ra, Intake, FakeConnection, MonkeyPatch, The whole point. If `process` is reachable from the capture thread, nothing was (+12 more)

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

### Community 30 - "`api/` — the FastAPI application"
Cohesion: 0.40
Nodes (4): `api/` — the FastAPI application, Five properties worth knowing before you change anything, Rules, The surface

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

### Community 53 - "Passage"
Cohesion: 0.18
Nodes (16): Router → retrieve → rerank → decide → answer, one verified sentence at a time., check(), check_one(), Claim, precheck(), The grounding gate.  Rule 3 in AGENTS.md: no claim without a citation. This mo, Never raises, never rewrites a claim. It keeps, drops, or abstains.      The w, Is this evidence worth answering from at all? The reason to abstain, or `None`. (+8 more)

### Community 54 - "test_modules.py"
Cohesion: 0.18
Nodes (21): AlertConfig, FakeConn, FakePack, obligation_row(), date, datetime, Reminder and Alert: what fires, once, and with what behind it.  Both modules a, A sweep for a date in the future must record that date, or it repeats itself. (+13 more)

### Community 55 - "Settings"
Cohesion: 0.14
Nodes (22): AsyncClient, capture_check(), Check, collect_checks(), database_check(), model_check(), Read-only dependency diagnostics; installation is never treated as inference val, Whether a worker is listening — which is a different question from whether Redis (+14 more)

### Community 56 - "Registrar"
Cohesion: 0.16
Nodes (16): TelegramSettings, ConfigurationError, _folder(), local_url(), _positive(), Path, ValueError, Small, literal .env reader with environment overrides and loopback-only endpoint (+8 more)

### Community 57 - "retrieve.py"
Cohesion: 0.13
Nodes (17): DocumentTypeSpec, One kind of document this pack recognises., Classification, _prompt(), Decide which pack's document type a captured document is, or decline to.  The, _schema(), document_types(), installed_packs() (+9 more)

### Community 58 - "cli.py"
Cohesion: 0.18
Nodes (19): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+11 more)

### Community 59 - "register_document"
Cohesion: 0.13
Nodes (19): The one interface every capture channel satisfies.      receive(payload, mime, s, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256` i, sha256(), The ingestion worker.  Capture registers a document; this package turns it int, Cursor, Any, Protocol, Register a document, idempotently, on a SHA-256 of the source bytes.  This is th (+11 more)

### Community 60 - "FolderCapture"
Cohesion: 0.05
Nodes (109): Answer, TestClient, a_citation(), client(), client_for(), conn(), document_row(), fact_row() (+101 more)

### Community 61 - "InstalledPack"
Cohesion: 0.09
Nodes (36): page_images(), Base64 page images, in page order. Empty when this document cannot be rendered., page_count(), PageUnavailable, _pdfium(), Any, LookupError, RuntimeError (+28 more)

### Community 62 - "extract"
Cohesion: 0.13
Nodes (28): classify(), Ollama, Never raises. An unavailable model is a classification failure, so it quarantine, extract(), Ollama, Never raises. A failure is a reason, and a reason routes the document to quarant, FakeOllama, iras() (+20 more)

### Community 63 - "pipeline.py"
Cohesion: 0.13
Nodes (25): blocked_reasons(), Any, Ollama, Path, QuarantinedDocument, queue(), The second stage of quarantine: the page image, read by the vision-language mode, Per document: `None` when the image pass can run, or the sentence saying why it (+17 more)

### Community 64 - "FolderAdapter"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 65 - "FolderCapture"
Cohesion: 0.32
Nodes (7): broker_available(), Whether Redis answers. Not whether a worker is listening — `core/runtime/checks., Popen, Run the local diagnostic server, the folder watcher and the ingestion worker tog, Start `scripts/worker.py --beat` beside us, or say plainly why it could not., start_worker(), stop_worker()

### Community 66 - "pipeline.py"
Cohesion: 0.14
Nodes (15): Chunk, chunk_pages(), _pack(), _paragraphs(), Split parsed pages into retrieval-sized chunks that still know their page number, What is actually embedded: the prefix plus the text, matching the tsvector colum, Greedily fill chunks up to the target, then carry a little tail into the next on, One flat list of chunks, ordinal running across the whole document. (+7 more)

### Community 67 - "TelegramAdapter"
Cohesion: 0.06
Nodes (57): IngestJob, Magic bytes first, filename suffix second, `application/octet-stream` last., What a capture returns: a registered document, and whether we had seen it before, sniff_mime(), FolderAdapter, FolderSettings, _Pending, datetime (+49 more)

### Community 68 - "ParsedPage"
Cohesion: 0.27
Nodes (11): FieldSpec, Grounding, Guardrails, ModuleTrigger, Persona, BaseModel, The two contracts the whole platform is built on.  Nothing else in the reposit, One extractable field. Its `name` is the column header in Desmond's register and (+3 more)

### Community 69 - "Ollama"
Cohesion: 0.17
Nodes (25): connect(), Any, One place that opens a connection to the one database.  `Settings.database_url`, Yield an open psycopg connection with autocommit off. The caller commits., ingest(), Any, date, Ollama (+17 more)

### Community 70 - "README.md"
Cohesion: 0.15
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 71 - "ingest.py"
Cohesion: 0.17
Nodes (19): Alert, _citations(), cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, Any (+11 more)

### Community 72 - "obligations.py"
Cohesion: 0.12
Nodes (21): Chunk, ReminderConfig, ExtractedFact, Extraction, fixed(), from_facts(), _label(), Any (+13 more)

### Community 73 - "extract.py"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.04
Nodes (44): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+36 more)

### Community 75 - "RUNNING.md"
Cohesion: 0.14
Nodes (17): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders somewhe, InstalledModule, manifest(), ModuleUnavailable, RuntimeError, Load the installed capability modules at runtime.  The mirror of `core/packs.py`, A module's YAML is missing, or does not validate against `ModuleManifest`. (+9 more)

### Community 76 - "DoclingParser"
Cohesion: 0.23
Nodes (15): create_app(), The local API. Liveness is intentionally separate from assistant readiness.  Loo, FastAPI, main(), Settings, Path, Setup diagnostics use controlled service responses, never live household documen, test_busy_port_does_not_open_browser() (+7 more)

### Community 77 - "Notion"
Cohesion: 0.25
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "start_parrot.py"
Cohesion: 0.32
Nodes (7): main(), Path, Local-only startup preflight, using the standard library so setup can be diagnos, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file conte, report_hardware(), startup_gaps()

### Community 79 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.25
Nodes (8): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Starter prompt for your coding agent, The one rule that changes everything: register first, The second half: adversarial testing, Two rules you cannot bend, Volumes, Where the column headings come from

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (7): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents

### Community 82 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 83 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 84 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.25
Nodes (7): AppLayout(), LockButton(), Rail(), SURFACES, TabBar(), CHOICES, ThemeToggle()

### Community 85 - "test_startup.py"
Cohesion: 0.52
Nodes (6): prepare_checkout(), Path, Startup tests do not ingest documents or need the corpus: they check process bou, test_check_only_never_launches_even_when_ready(), test_incomplete_checkout_never_launches_a_process(), test_launch_preserves_paths_and_loopback_and_exit_code()

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 89 - "Christian — Lane A · Integration and product owner"
Cohesion: 0.05
Nodes (80): AbstentionEvent, AskRequest, AskResponse, Claim, CloseRequest, CorrectionRequest, CorrectionResponse, EnabledRequest (+72 more)

### Community 90 - "The team"
Cohesion: 0.19
Nodes (19): GET(), grant(), POST(), Accepted, clearFailures(), derive(), failures, isConfigured() (+11 more)

### Community 91 - "1. Record architecture decisions"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 92 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 93 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 94 - "IngestJob"
Cohesion: 0.18
Nodes (11): Citation, Cited, A passage, named the way a person cites it and identified the way a link needs., One sentence and the passages it was traced to. What rule 3 looks like as data., The answer graph.  Router, retrieve, rerank, grounding gate, then answer or abst, Protocol, What the graph needs from retrieval, stated as a contract rather than an import., Implemented by `core/retrieve/` when Lane B's hybrid search lands.      `candi (+3 more)

### Community 102 - "schedule.py"
Cohesion: 0.24
Nodes (8): PackManifest, A domain pack, authored as one YAML file., (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., The contracts are the platform. If these break, something important changed., The register headers and the extraction models are generated from pack.yaml., test_a_pack_cannot_opt_out_of_never_acts(), test_generated_files_are_in_sync(), test_template_pack_validates()

### Community 103 - "tasks.py"
Cohesion: 0.29
Nodes (8): No row in `packs` with that id., No row in `modules` with that id., UnknownModule, UnknownPack, DatabaseUnavailable, RuntimeError, Safe to show: the message never carries the connection string., KeyError

### Community 104 - "ingest.py"
Cohesion: 0.20
Nodes (10): Generated, ModelUnavailable, Any, Client, RuntimeError, Generate against a JSON schema. This is how extraction is held to a pack's field, The same constrained generation, yielded as it is written.          Identical, Safe to show: names what could not be done, never the document it was doing it t (+2 more)

### Community 105 - "Inline"
Cohesion: 0.22
Nodes (7): DoclingParser, parse(), The one call the pipeline makes. An unhandled mime type quarantines rather than, Docling, held at arm's length: imported on first use, and never at module import, test_an_empty_text_file_does_not_parse(), test_an_unhandled_type_quarantines_rather_than_raising(), test_text_is_parsed_as_one_page()

### Community 106 - "bytes_for"
Cohesion: 0.15
Nodes (19): bytes_for(), index_folder(), LookupError, Path, Find the bytes behind a registered document again.  v1 keeps the inbox as the, Safe to show: the bytes for this document are no longer anywhere we look., SHA-256 of every file sitting in the watched folder. The document row holds the, The payload for `digest`, found by hashing what is in the watched folder. (+11 more)

### Community 107 - "worker.py"
Cohesion: 0.23
Nodes (17): installed_modules(), Every module directory holding a `module.yaml`, in a stable order.      Director, enabled_module_ids(), _module_row(), modules(), _pack_row(), packs(), Any (+9 more)

### Community 109 - "dispatch.py"
Cohesion: 0.09
Nodes (22): Dispatcher, Inline, Protocol, What happens to a document between "these bytes are registered" and "this docume, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Send (+14 more)

### Community 110 - "Ollama"
Cohesion: 0.11
Nodes (26): pack(), PackUnavailable, RuntimeError, A pack's YAML and its generated schemas disagree, or the pack does not exist., _as_document(), declared_type(), document(), documents() (+18 more)

### Community 111 - "Intake"
Cohesion: 0.04
Nodes (45): ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes, postcss (+37 more)

### Community 112 - "_payload_for"
Cohesion: 0.12
Nodes (32): Abstained, build(), events(), passage(), Any, Exception, The grounding gate, and the graph's two ways of not answering.  Rule 3 says no, The promise the Ask surface is built on. Two sentences, two separate events, in (+24 more)

### Community 114 - "extract.py"
Cohesion: 0.29
Nodes (5): CaptureAdapter, datetime, Protocol, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., Capture adapters.  Every channel a document can arrive through satisfies one int

### Community 115 - "Cursor"
Cohesion: 0.15
Nodes (22): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a, ndarray, load_matrix(), pack(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.  Des, Return (N x D matrix of normalised embeddings, chunk ids)., stats() (+14 more)

### Community 116 - "retry_quarantine"
Cohesion: 0.33
Nodes (6): Also yours, Christian — Lane A · Integration and product owner, Starter prompt for your coding agent, The five things you ship, Week 1, in order, What integration actually means here

### Community 117 - "ask.py"
Cohesion: 0.29
Nodes (7): Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The autonomy statement, The six artefacts, Where governance touches the code

### Community 118 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.38
Nodes (6): install(), install_best_effort(), Installed, What `install` did, so a startup line can say it in one sentence., Write every pack and module on disk into its table. Idempotent; never re-enables, Install at startup without being able to stop startup.      Both processes that

### Community 120 - "test_the_reminder_cron_is_read_from_its_manifest_not_written_twice"
Cohesion: 0.25
Nodes (6): archivo, jetbrains, metadata, spectral, viewport, ThemeProvider()

### Community 121 - "test_alert_is_swept_nightly_even_though_its_manifest_says_fact_write"
Cohesion: 0.43
Nodes (7): ALLOWED, Context, DELETE(), forward(), GET(), PATCH(), POST()

### Community 122 - "__init__.py"
Cohesion: 0.36
Nodes (5): metadata, UnlockPage(), UnlockForm(), Wordmark(), isUnlocked()

### Community 123 - "SentenceScanner"
Cohesion: 0.10
Nodes (28): Any, Pulling finished sentences out of a JSON reply that is still being written.  The, What document would have answered this, if the model said. Read once, at the end, Feed it deltas; it returns whichever sentences became complete because of them., Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes on, Find `"sentences": [` once. Everything before it is of no interest.          Sea, SentenceScanner (+20 more)

### Community 124 - "__init__.py"
Cohesion: 0.09
Nodes (27): already_said(), close(), current_lead(), Due, next_window(), Overdue, Any, date (+19 more)

### Community 125 - "register.py"
Cohesion: 0.43
Nodes (6): enabled_pack_ids(), enabled_packs(), The packs left switched on, or `None` when nothing has been installed yet., The installed packs a person has left switched on, as loaded pack objects., main(), Today: what the two capability modules have to say, ordered by urgency.      u

### Community 126 - "Finished"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

### Community 127 - "page.tsx"
Cohesion: 0.11
Nodes (10): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+2 more)

### Community 128 - "Ollama"
Cohesion: 0.24
Nodes (5): Ollama, OllamaUnavailable, RuntimeError, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.  Ta, Batch embeddings. Falls back to the legacy endpoint on old servers.

### Community 129 - "answer.tsx"
Cohesion: 0.12
Nodes (12): metadata, Abstention(), Part, sentence(), textOf(), Turn(), Conversation(), SUGGESTIONS (+4 more)

### Community 130 - "AnswerGraph"
Cohesion: 0.17
Nodes (10): Claim, AnswerGraph, Any, Ollama, What the graph carries. It ends at the evidence; the answer is streamed, not sta, Built once, asked many times. Holds no connection: retrieval does., One streamed sentence object, turned into the thing the gate understands., Routing and evidence. The answering is not a node — it yields, and a node return (+2 more)

### Community 131 - "ingest.py"
Cohesion: 0.24
Nodes (13): Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks.  Paperwork is short and stru, _split_page(), discover(), guess_date(), guess_type() (+5 more)

### Community 132 - "enabled_pack_ids"
Cohesion: 0.13
Nodes (20): Finished, _numbered(), _pack_for(), Event, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed y, One sentence that has passed the gate, with the citations it passed on.      I, Everything that is only knowable once the last sentence is in., The pack owning the best-scoring passage. Its guardrails govern the answer. (+12 more)

### Community 133 - "ports.py"
Cohesion: 0.47
Nodes (5): Path, documents_in(), main(), Load a handed-over corpus batch into this computer's database.      uv run pytho, Every document in the batch, in a stable order, recursing into tier subfolders.

### Community 134 - "page.tsx"
Cohesion: 0.31
Nodes (8): DocumentDetail(), when(), Field(), format(), isNumeric(), CorrectionResponse, pageImage(), VaultFact

### Community 135 - "api.ts"
Cohesion: 0.14
Nodes (16): metadata, VaultPage(), QuarantineQueue(), ALWAYS_EXISTS, AskResponse, Claim, get(), PacksResponse (+8 more)

### Community 136 - "item-row.tsx"
Cohesion: 0.29
Nodes (9): countdown(), detail(), ItemRow(), longDate(), sentence(), TONE, WORD, ObligationChanged (+1 more)

### Community 137 - "worker.py"
Cohesion: 0.26
Nodes (12): Namespace, _beat_needs_its_own_process(), celery_argv(), main(), Any, Popen, Run the ingestion worker, and optionally the nightly schedule with it.      uv, The arguments the Celery command-line would have been given. Built here so a tes (+4 more)

### Community 138 - "page.tsx"
Cohesion: 0.24
Nodes (7): DocumentPage(), metadata, EmptyState(), ProblemState(), SHAPES, document(), Problem

### Community 139 - "modules.py"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 140 - "Any"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 141 - "page.tsx"
Cohesion: 0.22
Nodes (6): metadata, PacksPage(), Toggle(), ModuleSummary, packs(), PackSummary

### Community 142 - "page.tsx"
Cohesion: 0.25
Nodes (6): isUrgent(), metadata, summary(), TodayPage(), quarantine(), today()

### Community 143 - "FakeCursor"
Cohesion: 0.50
Nodes (3): Architecture decision records, Index, Writing one

### Community 144 - "DoclingParser"
Cohesion: 0.40
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 146 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

### Community 149 - "InstalledPack"
Cohesion: 0.48
Nodes (6): answer(), build_context(), format_sources(), Ollama, Answer a question from retrieved chunks, with citations back to the file.  The, Hit

### Community 150 - "Ollama"
Cohesion: 0.48
Nodes (6): lastQuestion(), ParrotEvent, parseRecord(), POST(), readEvents(), upstreamDetail()

### Community 151 - "Client"
Cohesion: 0.16
Nodes (14): _coerce(), find_page(), _normalise(), _prepare(), Any, date, Decimal, Extract a pack's declared fields, and attribute every one of them to a page. (+6 more)

## Knowledge Gaps
- **459 isolated node(s):** `1 · Collaborators`, `2 · Branch protection`, `3 · Actions permissions`, `4 · Project board`, `5 · The Notion hub` (+454 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `FolderCapture`, `TelegramAdapter`, `Ollama`, `tasks.py`, `ingest.py`, `worker.py`, `worker.py`, `DoclingParser`, `dispatch.py`, `7. The answer graph ships before hybrid retrieval and before a checkpoint table`, `Registrar`, `Christian — Lane A · Integration and product owner`, `register_document`, `FolderCapture`, `register.py`, `pipeline.py`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `Connection` connect `Cursor` to `cli.py`, `register_document`, `ingest.py`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `Ollama` connect `Christian — Lane A · Integration and product owner` to `AnswerGraph`, `TelegramAdapter`, `enabled_pack_ids`, `Ollama`, `obligations.py`, `ingest.py`, `dispatch.py`, `_payload_for`, `igd-capstone-2026`, `Passage`, `Settings`, `Client`, `Registrar`, `retrieve.py`, `FolderCapture`, `IngestJob`, `pipeline.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `FakeConn` (e.g. with `Abstained` and `Answer`) actually correct?**
  _`FakeConn` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Ollama` (e.g. with `Abstained` and `Answer`) actually correct?**
  _`Ollama` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Settings` (e.g. with `Installed` and `RegisteredModule`) actually correct?**
  _`Settings` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Passage` (e.g. with `Abstained` and `Answer`) actually correct?**
  _`Passage` has 17 INFERRED edges - model-reasoned connections that need verification._