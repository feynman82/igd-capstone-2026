# Graph Report - igd-capstone-2026  (2026-09-13)

## Corpus Check
- 234 files · ~575,630 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 28 file(s) not represented in the graph (top: (none) 15, .csv 4, .css 3)

## Summary
- 2846 nodes · 5901 edges · 177 communities (155 shown, 16 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 406 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2bf3f314`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ingest/quarantine.py
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
- test_worker_queue.py
- Zee — Lane D · Domain packs and interface
- Authoring a domain pack
- Household canon
- Registration
- build_team_tasks.py
- `core/graph/` — the LangGraph runtime
- `core/ingest/` — the ingestion worker
- Integration review
- Writing an ADR
- `core/retrieve/` — hybrid retrieval
- Graphify — the shared knowledge graph
- build_router
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
- contracts.py
- `docs/report/` — the final report
- Passage
- test_modules.py
- main.py
- IngestJob
- export-design-preview.cjs
- cli.py
- register_document
- Settings
- InstalledPack
- test_ingest_pipeline.py
- pipeline.py
- FolderAdapter
- parse.py
- install_best_effort
- installed_packs
- registry.py
- Ollama
- README.md
- ingest.py
- obligations.py
- extract.py
- Starting Parrot
- answer.py
- FolderAdapter
- Notion
- State
- Desmond — Lane E · Corpus and adversarial testing
- PaperBrain
- Working agreement for coding agents
- Any
- Siew — Lane C · Governance and assurance
- FakeConn
- test_startup.py
- Architecture
- Roadmap
- run_parrot.py
- routes.py
- lock.ts
- application
- build.py
- 6. pypdfium2 renders the page images the quarantine second pass reads
- ingest/extract.py
- Home Contents Insurance Policy
- __init__.py
- __init__.py
- __init__.py
- __init__.py
- setup.sh
- schedule.py
- PackManifest
- ._client
- Contributing
- AnswerGraph
- worker.py
- base.py
- .load
- Ollama
- Intake
- test_answer_graph.py
- PackManifest
- test_household.py
- Cursor
- _today_items
- NNNN · The decision, as a statement not a question
- 6 · Use it
- __init__.py
- app/layout.tsx
- ports.py
- item-row.tsx
- SentenceScanner
- __init__.py
- Household canon
- answer.tsx
- page.tsx
- Ollama
- answer.tsx
- blocked_reasons
- ingest.py
- enabled_pack_ids
- Cursor
- api.ts
- test_api.py
- today/page.tsx
- create_app
- page.tsx
- 4. Local setup can run before the household assistant is ready
- reindex_document
- Passage
- date
- (app)/layout.tsx
- devDependencies
- README.md
- igd-capstone-2026
- FakeCursor
- Desmond — Lane E · Corpus and adversarial testing
- Ollama
- ParsedPage
- _as_response
- Parser
- Desmond — task list
- date
- package.json
- Yew Mun — Lane B · Retrieval and evaluation
- postcss.config.mjs
- enabled_pack_ids
- 13. A question is understood before it is searched, and scoped before it is cut
- Alert
- github.md
- scripts
- startup.py
- ConfigurationError
- FakeCursor
- vault/page.tsx
- household/page.tsx
- Due
- test_a_failure_after_the_stream_started_arrives_as_an_event
- The team
- Exception
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- quiet_engine
- models.py
- _as_vault_document

## God Nodes (most connected - your core abstractions)
1. `Settings` - 132 edges
2. `build_router()` - 66 edges
3. `Ollama` - 57 edges
4. `FakeConn` - 56 edges
5. `client_for()` - 50 edges
6. `settings()` - 50 edges
7. `rows_for()` - 49 edges
8. `Passage` - 46 edges
9. `ModelUnavailable` - 36 edges
10. `AnswerGraph` - 33 edges

## Surprising Connections (you probably didn't know these)
- `warm_models()` --uses--> `ModelUnavailable`  [INFERRED]
  api/startup.py → core/runtime/ollama.py
- `constrained_stream()` --calls--> `ModelUnavailable`  [EXTRACTED]
  tests/test_answer_graph.py → core/runtime/ollama.py
- `constrained_stream()` --calls--> `ModelUnavailable`  [EXTRACTED]
  tests/test_answer_graph.py → core/runtime/ollama.py
- `PassThroughReranker` --uses--> `Passage`  [INFERRED]
  tests/test_answer_graph.py → core/graph/ports.py
- `PhrasingRetriever` --uses--> `Passage`  [INFERRED]
  tests/test_answer_graph.py → core/graph/ports.py

## Import Cycles
- None detected.

## Communities (177 total, 16 thin omitted)

### Community 0 - "ingest/quarantine.py"
Cohesion: 0.09
Nodes (38): fixed(), from_facts(), _label(), Any, date, What a person is shown. The key is the pack's word for it; the subject says…, Create the obligations this pack declares for these newly written facts.…, Create the pack's calendar obligations — a filing deadline belongs to no… (+30 more)

### Community 1 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.16
Nodes (8): dynamic, metadata, PacksPage(), runtime, Toggle(), ModuleSummary, packs(), PackSummary

### Community 2 - "README.md"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.09
Nodes (41): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+33 more)

### Community 4 - "4. Writing `pack.yaml`"
Cohesion: 0.12
Nodes (15): 1. What a pack is, 2. The one thing to understand before you start, 3. The workflow, 4. Writing `pack.yaml`, 5. The grounding corpus, 6. Definition of done, 7. Where to ask, Authoring a domain pack (+7 more)

### Community 5 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 6 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 7 - "Domain packs — start here"
Cohesion: 0.15
Nodes (13): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 7. Grounding — the optional second half, 8. Starter prompt for Claude Code (+5 more)

### Community 8 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 9 - "Christian — task list"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 10 - "Desmond — task list"
Cohesion: 0.18
Nodes (11): Desmond — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 11 - "Siew — task list"
Cohesion: 0.20
Nodes (9): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20, W9 — due 2026-11-03 (+1 more)

### Community 12 - "Yew Mun — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

### Community 13 - "Zee — task list"
Cohesion: 0.13
Nodes (15): 1 · Install five things, 2 · Download the AI models, 3 · Get the code and set it up, 4 · Put some documents in, 5 · Run it, 6 · Use it, Ask — a question about your own documents, If something goes wrong (+7 more)

### Community 14 - "Filling the corpus register"
Cohesion: 0.20
Nodes (9): Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one, The rule that cannot bend (+1 more)

### Community 15 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (9): Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six, Where governance touches the code (+1 more)

### Community 16 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.33
Nodes (5): Before you say you are done, Claude Code — read this first, Finding your way around, Skills and commands, The three things agents get wrong here

### Community 17 - "test_worker_queue.py"
Cohesion: 0.08
Nodes (38): CaptureAdapter, datetime, Protocol, The one interface every capture channel satisfies. receive(payload, mime,…, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sha256(), Capture adapters. Every channel a document can arrive through satisfies one… (+30 more)

### Community 18 - "Zee — Lane D · Domain packs and interface"
Cohesion: 0.22
Nodes (9): Half one — domain packs (weeks 1 to 7), Half two — the interface (weeks 4 to 8), Read this first, Rules that apply to you specifically, The two halves of this lane, What "done" looks like, What you present, Your Claude Code skills (+1 more)

### Community 19 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 20 - "Household canon"
Cohesion: 0.25
Nodes (7): Address, Employment, Household canon, Life events that documents must reflect, People, Policies, Vehicles

### Community 21 - "Registration"
Cohesion: 0.09
Nodes (21): Dispatcher, Inline, Protocol, What happens to a document between "these bytes are registered" and "this…, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Send (+13 more)

### Community 22 - "build_team_tasks.py"
Cohesion: 0.39
Nodes (7): main(), Path, Generate each member's task list from the master task CSV. python…, _read_rows(), _render(), _week_key(), _write()

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
Nodes (9): Graphify — the shared knowledge graph, Keeping it fresh, Merge conflicts, solved properly, Setup, once per clone, The hook leaves your tree dirty. Amend it into the commit you just made., Two kinds of extraction, and which needs what, Using it, What is committed, and what is not (+1 more)

### Community 29 - "build_router"
Cohesion: 0.10
Nodes (30): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, What changed, in the words the screen confirms it with. `was` is returned…, The row is gone from Today. `speaks_again` is null when it will not come back.…, 202. The vision pass is slower than a page load, so it is queued and this is… (+22 more)

### Community 30 - "`api/` — the FastAPI application"
Cohesion: 0.40
Nodes (4): `api/` — the FastAPI application, Five properties worth knowing before you change anything, Rules, The surface

### Community 31 - "The corpus"
Cohesion: 0.29
Nodes (6): Handing a batch over, One rule, The corpus, The order matters, Tiers, Validate before handing over

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

### Community 51 - "contracts.py"
Cohesion: 0.26
Nodes (12): FieldSpec, Grounding, Guardrails, ModuleTrigger, Persona, BaseModel, The two contracts the whole platform is built on. Nothing else in the…, One extractable field. Its `name` is the column header in Desmond's register… (+4 more)

### Community 52 - "`docs/report/` — the final report"
Cohesion: 0.10
Nodes (19): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model (+11 more)

### Community 53 - "Passage"
Cohesion: 0.23
Nodes (10): check(), Claim, Never raises, never rewrites a claim. It keeps, drops, or abstains. The whole-…, Verdict, test_a_claim_citing_the_same_document_twice_says_it_once(), test_a_grounded_claim_renders_its_document_and_page(), test_a_sentence_citing_a_passage_that_was_never_retrieved_is_dropped(), test_a_sentence_with_no_supporting_passage_is_dropped() (+2 more)

### Community 54 - "test_modules.py"
Cohesion: 0.19
Nodes (20): already_said(), True when this exact window has already been mentioned. The comparison is by…, Everything inside a lead window that has not already been said for that window.…, sweep(), obligation_row(), date, datetime, Reminder and Alert: what fires, once, and with what behind it. Both modules are… (+12 more)

### Community 55 - "main.py"
Cohesion: 0.18
Nodes (17): The local API. Liveness is intentionally separate from assistant readiness.…, AsyncClient, asyncio, capture_check(), Check, collect_checks(), database_check(), interface_check() (+9 more)

### Community 56 - "IngestJob"
Cohesion: 0.08
Nodes (31): IngestJob, Magic bytes first, filename suffix second, `application/octet-stream` last. A…, What a capture returns: a registered document, and whether we had seen it…, sniff_mime(), _Pending, datetime, Path, The watched-folder capture adapter. A person drops a scan into a folder and it… (+23 more)

### Community 57 - "export-design-preview.cjs"
Cohesion: 0.11
Nodes (17): bundle(), classes, css, cssFile, domId, fs, ids, licences (+9 more)

### Community 58 - "cli.py"
Cohesion: 0.16
Nodes (22): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+14 more)

### Community 59 - "register_document"
Cohesion: 0.29
Nodes (12): Insert or update the `documents` row for these bytes and say which happened.…, register_document(), conn(), database_url(), Any, fixture, The idempotent upsert, against the real unique index. `documents.sha256 UNIQUE`…, test_a_document_must_arrive_with_a_name() (+4 more)

### Community 60 - "Settings"
Cohesion: 0.12
Nodes (53): Settings, client_for(), FakeConn, filed_document(), open_obligation(), pack_row(), Path, The point of the endpoint. An UPDATE alone loses the example we are trying to… (+45 more)

### Community 61 - "InstalledPack"
Cohesion: 0.09
Nodes (37): page_images(), Base64 page images, in page order. Empty when this document cannot be rendered.…, page_count(), PageUnavailable, _pdfium(), Any, LookupError, RuntimeError (+29 more)

### Community 62 - "test_ingest_pipeline.py"
Cohesion: 0.11
Nodes (41): extract(), Never raises. A failure is a reason, and a reason routes the document to…, Generated, FakeOllama, insurance(), iras(), _page_of_examples(), Any (+33 more)

### Community 63 - "pipeline.py"
Cohesion: 0.08
Nodes (34): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+26 more)

### Community 64 - "FolderAdapter"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 65 - "parse.py"
Cohesion: 0.08
Nodes (26): Block, DoclingParser, _kind(), _pages_from(), parse(), Parser, PlainTextParser, Protocol (+18 more)

### Community 66 - "install_best_effort"
Cohesion: 0.33
Nodes (6): lifespan(), install_best_effort(), Install at startup without being able to stop startup. Both processes that own…, The setup page exists to say the database is missing. It cannot say it if it…, test_the_server_still_starts_when_the_database_is_not_running(), refuse()

### Community 67 - "installed_packs"
Cohesion: 0.13
Nodes (17): DocumentTypeSpec, One kind of document this pack recognises., Classification, classify(), _prompt(), Decide which pack's document type a captured document is, or decline to. The…, Never raises. An unavailable model is a classification failure, so it…, _schema() (+9 more)

### Community 68 - "registry.py"
Cohesion: 0.13
Nodes (22): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders…, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, RuntimeError, Load the installed capability modules at runtime. The mirror of… (+14 more)

### Community 69 - "Ollama"
Cohesion: 0.12
Nodes (38): queue(), The reportable line. Deliberately a rate and a count, because a rate over three…, What is waiting for a person's eyes, oldest first., Recovery, recovery_rate(), bytes_for(), LookupError, Safe to show: the bytes for this document are no longer anywhere we look. (+30 more)

### Community 70 - "README.md"
Cohesion: 0.16
Nodes (3): Architecture decision records, Index, Writing one

### Community 71 - "ingest.py"
Cohesion: 0.23
Nodes (17): _citations(), cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, Any, date (+9 more)

### Community 72 - "obligations.py"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 73 - "extract.py"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (16): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+8 more)

### Community 75 - "answer.py"
Cohesion: 0.10
Nodes (27): Abstained, _asked(), Citation, Finished, _numbered(), _pack_for(), Event, Router → retrieve → rerank → decide → answer, one verified sentence at a time.… (+19 more)

### Community 76 - "FolderAdapter"
Cohesion: 0.13
Nodes (27): FolderAdapter, FolderSettings, Satisfies `CaptureAdapter`. Holds no database handle — it is given a…, FolderCapture, A daemon thread that polls the watched folder until `stop()` or process exit., Begin watching. Returns False, with a logged reason, when it cannot., FakeRegistrar, datetime (+19 more)

### Community 77 - "Notion"
Cohesion: 0.25
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "State"
Cohesion: 0.15
Nodes (9): _conversation(), fuse(), What the graph carries. It ends at the evidence; the answer is streamed, not…, Several searches as one list: each passage once, at the best score any phrasing…, The question made whole, and said in the documents' words. See…, Every phrasing of the question, searched and fused. The person's own words…, Whose question is it, over every candidate, and then the few that are read.…, State (+1 more)

### Community 79 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.09
Nodes (21): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+13 more)

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (7): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 82 - "Any"
Cohesion: 0.14
Nodes (8): document_row(), fact_row(), FakeCursor, Any, The parameters of the one statement containing `needle`. Fails loudly if it…, Following a citation must never end in a blank screen because a pack was…, test_one_document_is_shown_even_when_its_pack_is_off(), test_vault_lists_documents_with_their_facts()

### Community 83 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 84 - "FakeConn"
Cohesion: 0.33
Nodes (8): AlertConfig, FakeConn, FakePack, test_a_firing_older_than_the_debounce_window_fires_again(), test_a_metric_no_query_defines_cannot_fire(), test_a_recent_firing_is_debounced(), test_a_threshold_crossing_fires_with_the_document_behind_it(), test_below_the_warning_share_nothing_fires()

### Community 85 - "test_startup.py"
Cohesion: 0.10
Nodes (28): main(), Path, Local-only startup preflight, using the standard library so setup can be…, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file…, report_hardware(), startup_gaps(), prepare_checkout() (+20 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "run_parrot.py"
Cohesion: 0.12
Nodes (26): broker_available(), Whether Redis answers. Not whether a worker is listening —…, _kill_tree(), main(), open_browser(), parse_args(), port_answers(), Any (+18 more)

### Community 89 - "routes.py"
Cohesion: 0.15
Nodes (18): AbstentionEvent, FinishedEvent, PersonModel, Evidence gathered and good enough to answer from. Nothing has been claimed yet., One sentence that has passed the gate, with the sources it passed on. It will…, ReadingEvent, RefusalEvent, SentenceEvent (+10 more)

### Community 90 - "lock.ts"
Cohesion: 0.06
Nodes (54): dynamic, GET(), grant(), POST(), runtime, dynamic, lastQuestion(), ParrotEvent (+46 more)

### Community 91 - "application"
Cohesion: 0.15
Nodes (18): application(), The configured application with its tasks registered. One per process., Return something that puts one ingestion message on the queue and yields its…, Put one quarantine retry on the queue and return its task id. The vision pass…, send_retry(), sender(), _beat_needs_its_own_process(), celery_argv() (+10 more)

### Community 92 - "build.py"
Cohesion: 0.19
Nodes (16): _class_name(), _docstring(), _field_line(), load(), main(), Path, Generate everything downstream of a pack.yaml. python -m packs.build #…, The header row Desmond fills in, one file per pack. Long format: one row per… (+8 more)

### Community 93 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.50
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 94 - "ingest/extract.py"
Cohesion: 0.10
Nodes (29): _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact, Extraction, find_page(), _normalise() (+21 more)

### Community 102 - "schedule.py"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "PackManifest"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 104 - "._client"
Cohesion: 0.12
Nodes (11): Any, Client, A question, embedded the way the model was trained to embed a search query., Passages as `(title, text)`, embedded the way the model was trained to embed a…, Load the generator and the embedder now, and say where the generator landed. An…, Generate against a JSON schema. This is how extraction is held to a pack's…, The same constrained generation, yielded as it is written. Identical body to…, Whether this embedding model expects `QUERY_PROMPT` and `DOCUMENT_PROMPT`. (+3 more)

### Community 105 - "Contributing"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 106 - "AnswerGraph"
Cohesion: 0.15
Nodes (17): _graph_for(), Claim, AnswerGraph, Any, date, Built once, asked many times. Holds no connection: retrieval does., One streamed sentence object, turned into the thing the gate understands. The…, Routing and evidence. The answering is not a node — it yields, and a node… (+9 more)

### Community 107 - "worker.py"
Cohesion: 0.10
Nodes (18): Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The autonomy statement, The six artefacts, Where governance touches the code, Siew — task list (+10 more)

### Community 109 - ".load"
Cohesion: 0.11
Nodes (34): ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one…, Load the generator and the embedder before the first question, and record the…, warm_models(), _folder(), Path, The watched folder, absolute, so a check and a worker never disagree about…, _ollama_answering() (+26 more)

### Community 110 - "Ollama"
Cohesion: 0.07
Nodes (38): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+30 more)

### Community 111 - "Intake"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 112 - "test_answer_graph.py"
Cohesion: 0.09
Nodes (40): build(), events(), passage(), PassThroughReranker, PhrasingRetriever, Any, Exception, parametrize (+32 more)

### Community 113 - "PackManifest"
Cohesion: 0.24
Nodes (8): PackManifest, A domain pack, authored as one YAML file., (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., The contracts are the platform. If these break, something important changed., The register headers and the extraction models are generated from pack.yaml. If…, test_a_pack_cannot_opt_out_of_never_acts(), test_generated_files_are_in_sync(), test_template_pack_validates()

### Community 114 - "test_household.py"
Cohesion: 0.05
Nodes (73): is_first_person(), `(word, relation)` when the question asks about a relation's own documents,…, Whether this question is about the person asking. `other_names` are the display…, relation_asked(), add_person(), attribute(), classify_prompt(), confirm() (+65 more)

### Community 115 - "Cursor"
Cohesion: 0.15
Nodes (20): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a…, ndarray, load_matrix(), pack(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.…, Return (N x D matrix of normalised embeddings, chunk ids)., stats() (+12 more)

### Community 116 - "_today_items"
Cohesion: 0.14
Nodes (18): A document and a page, as a person would cite it., Source, TodayItem, TodayResponse, _as_source(), today(), _cite(), _link() (+10 more)

### Community 117 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 118 - "6 · Use it"
Cohesion: 0.13
Nodes (26): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor.…, What the person asked for, once. The first request wins; later ones change…, _client(), _eventually(), _launcher(), parametrize, Path (+18 more)

### Community 120 - "app/layout.tsx"
Cohesion: 0.22
Nodes (7): next-themes, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 121 - "ports.py"
Cohesion: 0.24
Nodes (7): The answer graph. Router, retrieve, rerank, grounding gate, then answer or…, Protocol, What the graph needs from retrieval, stated as a contract rather than an…, Implemented by `core/retrieve/` when Lane B's hybrid search lands. `candidates`…, A cross-encoder, scoring question against passage. Returns the best `keep`,…, Reranker, Retriever

### Community 122 - "item-row.tsx"
Cohesion: 0.27
Nodes (9): countdown(), detail(), figure(), ItemRow(), longDate(), sentence(), TONE, WORD (+1 more)

### Community 123 - "SentenceScanner"
Cohesion: 0.09
Nodes (29): Any, Pulling finished sentences out of a JSON reply that is still being written. The…, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner (+21 more)

### Community 124 - "__init__.py"
Cohesion: 0.12
Nodes (21): close(), current_lead(), next_window(), Overdue, Any, date, datetime, LookupError (+13 more)

### Community 125 - "Household canon"
Cohesion: 0.08
Nodes (23): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, Policies, The family tree, and why three of them are not called Lim (+15 more)

### Community 126 - "answer.tsx"
Cohesion: 0.10
Nodes (16): ai, @ai-sdk/react, metadata, Abstention(), Part, sentence(), textOf(), ADR-0011 (+8 more)

### Community 127 - "page.tsx"
Cohesion: 0.11
Nodes (10): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+2 more)

### Community 128 - "Ollama"
Cohesion: 0.20
Nodes (8): answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, Ollama, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.…, Batch embeddings. Falls back to the legacy endpoint on old servers., Hit

### Community 129 - "answer.tsx"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 130 - "blocked_reasons"
Cohesion: 0.24
Nodes (10): blocked_reasons(), forget(), Any, Path, ValueError, QuarantinedDocument, Per document: `None` when the image pass can run, or the sentence saying why it…, Safe to show. Forgetting a document whose file is still there would not last. (+2 more)

### Community 131 - "ingest.py"
Cohesion: 0.22
Nodes (13): Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks. Paperwork is short and…, _split_page(), discover(), guess_date(), guess_type() (+5 more)

### Community 132 - "enabled_pack_ids"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 133 - "Cursor"
Cohesion: 0.25
Nodes (4): Cursor, Any, Protocol, cursor()

### Community 134 - "api.ts"
Cohesion: 0.09
Nodes (24): RELATION_CHOICES, Place, PLACES, DocumentDetail(), when(), Field(), format(), isNumeric() (+16 more)

### Community 135 - "test_api.py"
Cohesion: 0.09
Nodes (35): Answer, Cited, One sentence and the passages it was traced to. What rule 3 looks like as data.…, Every event, collected. `scripts/ask.py` and the screen ask the same question…, client(), conn(), FakeGraph, graph() (+27 more)

### Community 136 - "today/page.tsx"
Cohesion: 0.13
Nodes (16): HouseholdPage(), AppLayout(), dynamic, isUrgent(), metadata, runtime, summary(), TodayPage() (+8 more)

### Community 137 - "create_app"
Cohesion: 0.36
Nodes (5): create_app(), checks(), ready(), setup(), system_status()

### Community 138 - "page.tsx"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 139 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.20
Nodes (10): ModuleSummary, PacksResponse, PackSummary, _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack() (+2 more)

### Community 140 - "reindex_document"
Cohesion: 0.13
Nodes (14): indexed(), IndexedDocument, Any, RuntimeError, Safe to show: names what went wrong, never what the document says., Parse, chunk and embed one document again, and replace its chunks. Returns how…, reindex_document(), ReindexFailed (+6 more)

### Community 141 - "Passage"
Cohesion: 0.12
Nodes (18): Passage, How a passage names itself: the document and the page, as a person would say it., Any, Whose question is this, and whose documents may answer it. "What is my term…, The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting…, Keep the owner's passages and the household's; set aside everybody else's. A…, Keep the passages of these people and of the household; set aside everybody… (+10 more)

### Community 142 - "date"
Cohesion: 0.19
Nodes (15): obligation(), overdue_row(), date, One row of `reminder.OVERDUE`, in its column order., Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with…, The Celery beat never goes through the API, so the filter cannot live there., A deleted document must not take the sentence down with it., test_a_citation_that_resolves_to_nothing_still_says_what_it_said() (+7 more)

### Community 143 - "(app)/layout.tsx"
Cohesion: 0.08
Nodes (24): lucide-react, react, dynamic, runtime, LockButton(), SURFACES, TabBar(), Tabs() (+16 more)

### Community 144 - "devDependencies"
Cohesion: 0.25
Nodes (8): devDependencies, postcss, tailwindcss, @tailwindcss/postcss, @types/node, @types/react, @types/react-dom, typescript

### Community 145 - "README.md"
Cohesion: 0.29
Nodes (7): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents

### Community 146 - "igd-capstone-2026"
Cohesion: 0.20
Nodes (10): Authoring a pack, igd-capstone-2026, `main` is not protected, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live (+2 more)

### Community 149 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 150 - "Ollama"
Cohesion: 0.15
Nodes (17): build(), Any, The one Celery application, built from `Settings`. Every setting here is a…, Construct the Celery application. Imported lazily by callers so that nothing…, beat_schedule(), cron_expressions(), crontab_from(), manifest() (+9 more)

### Community 151 - "ParsedPage"
Cohesion: 0.12
Nodes (23): Chunk, chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, One flat list of chunks, ordinal running across the whole document. (+15 more)

### Community 152 - "_as_response"
Cohesion: 0.14
Nodes (14): AskRequest, AskResponse, Claim, ErrorEvent, The stream broke after it began. A client cannot read an HTTP status by then., One sentence and the passages it was traced to. Never emitted without…, _as_response(), ask() (+6 more)

### Community 153 - "Parser"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "Desmond — task list"
Cohesion: 0.33
Nodes (5): 12. Chunks follow the document's headings, and embeddings use the model's task prompts, Consequences, Context, Decision, Evidence

### Community 155 - "date"
Cohesion: 0.50
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 156 - "package.json"
Cohesion: 0.12
Nodes (14): class-variance-authority, clsx, postcss, react-dom, tailwind-merge, tailwindcss, @tailwindcss/postcss, @types/node (+6 more)

### Community 157 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

### Community 159 - "enabled_pack_ids"
Cohesion: 0.15
Nodes (17): enabled_module_ids(), enabled_pack_ids(), enabled_packs(), _pack_row(), packs(), Any, One row of `packs`, with the manifest validated back out of its jsonb column., No row in `packs` with that id. (+9 more)

### Community 160 - "13. A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.33
Nodes (5): 13. A question is understood before it is searched, and scoped before it is cut, Consequences, Context, Decision, Evidence

### Community 161 - "Alert"
Cohesion: 0.33
Nodes (3): Alert, What the debounce is keyed on: this metric, for this person, in this pack., test_the_debounce_key_separates_people()

### Community 162 - "github.md"
Cohesion: 0.50
Nodes (3): Last sync, Screen map, Updated in this project

### Community 163 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 164 - "startup.py"
Cohesion: 0.40
Nodes (3): The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render()

### Community 165 - "ConfigurationError"
Cohesion: 0.09
Nodes (30): TelegramSettings, Run the folder capture loop in a background thread, beside the local server.…, connect(), DatabaseUnavailable, Any, RuntimeError, One place that opens a connection to the one database. `Settings.database_url`…, Safe to show: the message never carries the connection string. (+22 more)

### Community 166 - "FakeCursor"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 167 - "vault/page.tsx"
Cohesion: 0.09
Nodes (18): next, DocumentPage(), dynamic, metadata, runtime, dynamic, metadata, runtime (+10 more)

### Community 168 - "household/page.tsx"
Cohesion: 0.18
Nodes (9): dynamic, metadata, runtime, OwnerForm(), Roster(), WhoIsThis(), answer(), notOneOfUs() (+1 more)

### Community 171 - "test_a_failure_after_the_stream_started_arrives_as_an_event"
Cohesion: 0.17
Nodes (14): a_citation(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive…, No `reading` before it: the floor is checked before the model is asked anything., By then the 200 has been sent. An exception that only logged would leave a…, What a retrieved passage hands over: the sentence a person reads, and the id a…, sse() (+6 more)

### Community 174 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 178 - "Exception"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 179 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

### Community 180 - "quiet_engine"
Cohesion: 0.50
Nodes (4): fixture, MonkeyPatch, quiet_engine(), No real probes, no startup writes, no deliberate pause before exiting. The…

### Community 182 - "models.py"
Cohesion: 0.16
Nodes (19): CloseRequest, ConfirmNameRequest, CorrectionRequest, EnabledRequest, OwnerRequest, PersonRequest, PlaceRequest, BaseModel (+11 more)

### Community 202 - "_as_vault_document"
Cohesion: 0.29
Nodes (7): VaultDocument, VaultFact, VaultResponse, _as_vault_document(), one_document(), vault_documents(), VaultDocument

## Knowledge Gaps
- **605 isolated node(s):** `1 · Install five things`, `2 · Download the AI models`, `3 · Get the code and set it up`, `4 · Put some documents in`, `5 · Run it` (+600 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1330 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `ingest/quarantine.py`, `test_api.py`, `create_app`, `reindex_document`, `date`, `Registration`, `Ollama`, `build_router`, `ConfigurationError`, `test_a_failure_after_the_stream_started_arrives_as_an_event`, `main.py`, `register_document`, `pipeline.py`, `install_best_effort`, `registry.py`, `Ollama`, `FolderAdapter`, `Any`, `test_startup.py`, `run_parrot.py`, `routes.py`, `application`, `AnswerGraph`, `.load`, `test_household.py`, `6 · Use it`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `Connection` connect `Cursor` to `ingest.py`, `Cursor`, `Registration`, `cli.py`, `register_document`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `Ollama` connect `Ollama` to `ingest/quarantine.py`, `installed_packs`, `startup.py`, `ConfigurationError`, `._client`, `AnswerGraph`, `answer.py`, `FolderAdapter`, `.load`, `reindex_document`, `Registration`, `test_ingest_pipeline.py`, `routes.py`, `run_parrot.py`, `Settings`, `build_router`, `ingest/extract.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 103 inferred relationships involving `Settings` (e.g. with `create_app()` and `build_router()`) actually correct?**
  _`Settings` has 103 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `build_router()` (e.g. with `AskRequest` and `AskResponse`) actually correct?**
  _`build_router()` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Ollama` (e.g. with `warm_models()` and `AnswerGraph`) actually correct?**
  _`Ollama` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `client_for()` (e.g. with `Settings` and `fake_connection()`) actually correct?**
  _`client_for()` has 2 INFERRED edges - model-reasoned connections that need verification._