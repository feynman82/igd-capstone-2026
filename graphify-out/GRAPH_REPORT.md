# Graph Report - igd-capstone-2026  (2026-09-11)

## Corpus Check
- 155 files · ~103,165 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1565 nodes · 2804 edges · 123 communities (101 shown, 22 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 146 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c4992526`
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

## God Nodes (most connected - your core abstractions)
1. `FakeConn` - 28 edges
2. `FolderAdapter` - 24 edges
3. `AnswerGraph` - 20 edges
4. `IngestJob` - 20 edges
5. `ModelUnavailable` - 20 edges
6. `rows_for()` - 19 edges
7. `Intake` - 19 edges
8. `Passage` - 19 edges
9. `build_router()` - 18 edges
10. `client_for()` - 18 edges

## Surprising Connections (you probably didn't know these)
- `_settings()` --indirect_call--> `settings()`  [INFERRED]
  api/routes.py → tests/test_api.py
- `FakeConn` --uses--> `DenseRetriever`  [INFERRED]
  tests/test_api.py → core/graph/baseline.py
- `FakeCursor` --uses--> `DenseRetriever`  [INFERRED]
  tests/test_api.py → core/graph/baseline.py
- `FakeGraph` --uses--> `DenseRetriever`  [INFERRED]
  tests/test_api.py → core/graph/baseline.py
- `install_best_effort()` --indirect_call--> `conn()`  [INFERRED]
  core/registry.py → tests/test_api.py

## Import Cycles
- None detected.

## Communities (123 total, 22 thin omitted)

### Community 0 - "contracts.py"
Cohesion: 0.21
Nodes (16): PackManifest, A domain pack, authored as one YAML file., _class_name(), _docstring(), _field_line(), load(), main(), Path (+8 more)

### Community 1 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 2 - "README.md"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.22
Nodes (18): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), date, Validate a document register before it is handed over.      python -m corpus.val, Derived from the pack manifests, never hardcoded.      A register row can only n (+10 more)

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
Cohesion: 0.18
Nodes (11): Desmond — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 11 - "Siew — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

### Community 12 - "Yew Mun — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

### Community 13 - "Zee — task list"
Cohesion: 0.12
Nodes (14): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure, 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document (+6 more)

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
Nodes (19): Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker.      Celery is imported here ra, MonkeyPatch, FakeConnection, The whole point. If `process` is reachable from the capture thread, nothing was, The cheapest queue message is the one never sent, and the SHA-256 says these byt (+11 more)

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

### Community 53 - "Passage"
Cohesion: 0.06
Nodes (51): AnswerGraph, _numbered(), _pack_for(), Any, InstalledPack, Ollama, Passage, Router → retrieve → rerank → grounding gate → answer or abstain.  A LangGraph (+43 more)

### Community 54 - "test_modules.py"
Cohesion: 0.07
Nodes (43): AlertConfig, Decimal, already_said(), current_lead(), Due, overdue(), Any, date (+35 more)

### Community 55 - "Settings"
Cohesion: 0.08
Nodes (46): create_app(), Settings, The local API. Liveness is intentionally separate from assistant readiness.  Loo, AsyncClient, capture_check(), Check, collect_checks(), database_check() (+38 more)

### Community 56 - "Registrar"
Cohesion: 0.24
Nodes (21): FolderAdapter, FolderSettings, Satisfies `CaptureAdapter`. Holds no database handle — it is given a `Registrar`, FakeRegistrar, datetime, Path, The watched folder: debounce, mime sniffing, and what happens the second time., Poll until the stability window has passed and something comes out. (+13 more)

### Community 57 - "retrieve.py"
Cohesion: 0.21
Nodes (12): DocumentTypeSpec, One kind of document this pack recognises., document_types(), installed_packs(), _load_one(), PackUnavailable, Path, RuntimeError (+4 more)

### Community 58 - "cli.py"
Cohesion: 0.06
Nodes (65): ArgumentParser, Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a, ndarray, answer(), build_context(), format_sources(), Ollama (+57 more)

### Community 59 - "register_document"
Cohesion: 0.15
Nodes (18): The one interface every capture channel satisfies.      receive(payload, mime, s, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256` i, sha256(), Register a document, idempotently, on a SHA-256 of the source bytes.  This is th, The row as it now stands, plus whether this call is the one that created it., Insert or update the `documents` row for these bytes and say which happened., register_document(), Registration (+10 more)

### Community 60 - "FolderCapture"
Cohesion: 0.07
Nodes (59): Answer, Cited, One sentence and the passages it was traced to. What rule 3 looks like as data., datetime, TestClient, client(), client_for(), document_row() (+51 more)

### Community 62 - "extract"
Cohesion: 0.09
Nodes (25): Exception, Generated, ParsedPage, FakeOllama, iras(), _page_of_examples(), Any, Parsing, chunking, extraction and the quarantine decision.  The model is faked. (+17 more)

### Community 65 - "FolderCapture"
Cohesion: 0.13
Nodes (16): broker_available(), FolderCapture, FolderAdapter, Settings, Whether Redis answers. Not whether a worker is listening — `core/runtime/checks., A daemon thread that polls the watched folder until `stop()` or process exit., Begin watching. Returns False, with a logged reason, when it cannot., Queue the work when there is somewhere to queue it; otherwise say what we are do (+8 more)

### Community 66 - "pipeline.py"
Cohesion: 0.11
Nodes (25): Chunk, Chunk, chunk_pages(), _pack(), _paragraphs(), Split parsed pages into retrieval-sized chunks that still know their page number, What is actually embedded: the prefix plus the text, matching the tsvector colum, Greedily fill chunks up to the target, then carry a little tail into the next on (+17 more)

### Community 67 - "TelegramAdapter"
Cohesion: 0.12
Nodes (20): _attachment(), Any, Client, datetime, RuntimeError, The Telegram capture adapter.  Same interface as the folder: `receive(payload,, Confirm the token works before anything else is attempted., One `getUpdates` round. Returns what was captured; replies with what was receive (+12 more)

### Community 68 - "ParsedPage"
Cohesion: 0.11
Nodes (21): _coerce(), extract(), Extraction, find_page(), _normalise(), _prepare(), Any, date (+13 more)

### Community 69 - "Ollama"
Cohesion: 0.07
Nodes (56): blocked_reasons(), page_images(), Any, Ollama, Path, QuarantinedDocument, queue(), The second stage of quarantine: the page image, read by the vision-language mode (+48 more)

### Community 71 - "ingest.py"
Cohesion: 0.15
Nodes (20): AlertConfig, Any, InstalledPack, Alert, _citations(), cpf_contributions_ytd(), days_uncovered(), _debounced() (+12 more)

### Community 72 - "obligations.py"
Cohesion: 0.16
Nodes (13): ReminderConfig, ExtractedFact, fixed(), from_facts(), _label(), Any, date, Turn a dated fact into a commitment to do something about it.  A fact is a state (+5 more)

### Community 73 - "extract.py"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.08
Nodes (22): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Quarantine, and the second pass, Reading a document (+14 more)

### Community 75 - "RUNNING.md"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

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
Cohesion: 0.29
Nodes (7): Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The autonomy statement, The six artefacts, Where governance touches the code

### Community 84 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

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
Cohesion: 0.08
Nodes (48): AskRequest, AskResponse, Claim, EnabledRequest, ModuleSummary, PacksResponse, PackSummary, QuarantinedDocument (+40 more)

### Community 90 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 91 - "1. Record architecture decisions"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 92 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 93 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 94 - "IngestJob"
Cohesion: 0.16
Nodes (13): IngestJob, Magic bytes first, filename suffix second, `application/octet-stream` last., What a capture returns: a registered document, and whether we had seen it before, sniff_mime(), _Pending, datetime, Path, The watched-folder capture adapter.  A person drops a scan into a folder and i (+5 more)

### Community 102 - "schedule.py"
Cohesion: 0.19
Nodes (13): build(), Any, Settings, The one Celery application, built from `Settings`.  Every setting here is a cons, Construct the Celery application. Imported lazily by callers so that nothing whi, beat_schedule(), cron_expressions(), crontab_from() (+5 more)

### Community 104 - "ingest.py"
Cohesion: 0.14
Nodes (16): Classification, classify(), _prompt(), Ollama, Decide which pack's document type a captured document is, or decline to.  The, Never raises. An unavailable model is a classification failure, so it quarantine, _schema(), ModelUnavailable (+8 more)

### Community 105 - "Inline"
Cohesion: 0.22
Nodes (8): Inline, Registration, Run the pipeline here and now, and report what it decided., Outcome, _loop(), main(), Path, Run the Telegram capture adapter.      uv run python scripts/telegram_bot.py --c

### Community 106 - "bytes_for"
Cohesion: 0.15
Nodes (19): bytes_for(), index_folder(), Path, Find the bytes behind a registered document again.  v1 keeps the inbox as the, Safe to show: the bytes for this document are no longer anywhere we look., SHA-256 of every file sitting in the watched folder. The document row holds the, The payload for `digest`, found by hashing what is in the watched folder., SourceMissing (+11 more)

### Community 107 - "worker.py"
Cohesion: 0.06
Nodes (49): installed_modules(), InstalledModule, manifest(), ModuleUnavailable, Load the installed capability modules at runtime.  The mirror of `core/packs.py`, A module's YAML is missing, or does not validate against `ModuleManifest`., One module's manifest, validated. Raises rather than returning a partial object., Every module directory holding a `module.yaml`, in a stable order.      Director (+41 more)

### Community 108 - "base.py"
Cohesion: 0.29
Nodes (5): CaptureAdapter, datetime, Protocol, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., Capture adapters.  Every channel a document can arrive through satisfies one int

### Community 109 - "dispatch.py"
Cohesion: 0.23
Nodes (8): Dispatcher, What happens to a document between "these bytes are registered" and "this docume, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Send, What every capture channel hands a document to.  An adapter's job ends at "these, Run the folder capture loop in a background thread, beside the local server.  Th, Protocol

### Community 110 - "Ollama"
Cohesion: 0.17
Nodes (13): _declared_type(), documents(), Fact, _facts_for(), Any, The vault: what is in the house, what state it is in, and what was read off it., The one value this fact has. JSON-ready: a date becomes its ISO string., The pack's own name for the type when it is knowable, else the column it sits in (+5 more)

### Community 111 - "Intake"
Cohesion: 0.27
Nodes (8): Intake, Registration, An already-indexed document is not read again. Re-reading it would burn a minute, _loop(), main(), FolderAdapter, Watch the inbox folder, register and read everything dropped into it.      uv, Poll until interrupted. `--once` waits out one stability window and then stops.

### Community 112 - "_payload_for"
Cohesion: 0.31
Nodes (8): digest_of_document(), Any, main(), _payload_for(), Any, Path, Show the quarantine queue, and run the vision second pass over it.      uv run, The document's bytes, found by digest. `core/ingest/source.py` is the one implem

### Community 114 - "extract.py"
Cohesion: 0.21
Nodes (13): FieldSpec, Grounding, Guardrails, ModuleManifest, ModuleTrigger, Persona, The two contracts the whole platform is built on.  Nothing else in the reposit, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer. (+5 more)

### Community 115 - "Cursor"
Cohesion: 0.29
Nodes (3): Cursor, Any, Protocol

### Community 116 - "retry_quarantine"
Cohesion: 0.33
Nodes (6): Also yours, Christian — Lane A · Integration and product owner, Starter prompt for your coding agent, The five things you ship, Week 1, in order, What integration actually means here

### Community 117 - "ask.py"
Cohesion: 0.33
Nodes (3): The contracts are the platform. If these break, something important changed., The register headers and the extraction models are generated from pack.yaml., test_generated_files_are_in_sync()

### Community 118 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.40
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

## Knowledge Gaps
- **338 isolated node(s):** `What it is`, `Where to start`, `Quick start`, `Where things live`, `The stack, in one table` (+333 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Connection` connect `cli.py` to `Cursor`, `register_document`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `ingest_file()` connect `cli.py` to `extract.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `AnswerGraph` connect `Passage` to `Christian — Lane A · Integration and product owner`, `FolderCapture`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `FakeConn` (e.g. with `Answer` and `Cited`) actually correct?**
  _`FakeConn` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `FolderAdapter` (e.g. with `IngestJob` and `Registrar`) actually correct?**
  _`FolderAdapter` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `AnswerGraph` (e.g. with `FixedRetriever` and `PassThroughReranker`) actually correct?**
  _`AnswerGraph` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `IngestJob` (e.g. with `FolderAdapter` and `FolderSettings`) actually correct?**
  _`IngestJob` has 7 INFERRED edges - model-reasoned connections that need verification._