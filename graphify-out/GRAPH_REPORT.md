# Graph Report - igd-capstone-2026  (2026-09-15)

## Corpus Check
- 270 files · ~635,455 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 30 file(s) not represented in the graph (top: (none) 15, .csv 4, .css 3)

## Summary
- 3964 nodes · 9230 edges · 215 communities (188 shown, 20 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 738 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `06d913a8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_parrot.py
- packs/page.tsx
- Christian — task list
- validate
- ingest/quarantine.py
- Project PARROT — team split
- Project PARROT — team split
- sha256
- Running the evaluation harness
- support.js
- Desmond — task list
- Zee — task list
- Yew Mun — task list
- score.py
- Filling the corpus register
- Writing a governance artefact
- Claude Code — read this first
- test_worker_queue.py
- index_pack
- ingest/extract.py
- Household canon
- retrieve.py
- build_team_tasks.py
- `core/graph/` — the LangGraph runtime
- `core/ingest/` — the ingestion worker
- Integration review
- Writing an ADR
- `core/retrieve/` — hybrid retrieval
- Graphify — the shared knowledge graph
- sweep
- `api/` — the FastAPI application
- The corpus
- Artefacts
- Why the prototype is evaluated on synthetic data
- `core/adapters/` — capture adapters
- sets/README.md
- Project skills
- Evaluation
- pull_request_template.md
- .__init__
- pack
- Changelog
- filesystem
- `docs/governance/` — the assurance artefacts
- corpus/__init__.py
- packs/__init__.py
- parrot
- Ollama
- The household, and the word "my"
- IngestJob
- alert/__init__.py
- ingest.py
- test_household.py
- advice/__init__.py
- cli.py
- harness.py
- Ollama
- test_pages.py
- extract
- bench_runtime.py
- compilerOptions
- export-design-preview.cjs
- test_startup.py
- pipeline.py
- registry.py
- ModelUnavailable
- test_advice_module.py
- FakeConn
- preview.tsx
- Scoped
- Starting Parrot
- test_modules.py
- main
- Notion
- Passage
- The demonstration run sheet
- PaperBrain
- Contributing
- [...path]/route.ts
- components.json
- ._advise
- load_set
- Architecture
- Roadmap
- answer.py
- (app)/layout.tsx
- lock.ts
- main.py
- FakeConn
- test_answer_graph.py
- TelegramCapture
- Home Contents Insurance Policy
- api/__init__.py
- core/__init__.py
- runtime/__init__.py
- modules/__init__.py
- setup.sh
- 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module
- Settings
- build_router
- 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack
- test_telegram_capture.py
- Siew — task list
- ScriptedOllama
- .load
- vault.py
- dependencies
- test_gate.py
- test_grounding_values.py
- household.py
- test_grounding.py
- TelegramAdapter
- scope_passages
- test_lifecycle.py
- worker/__init__.py
- app/layout.tsx
- build.py
- test_contracts.py
- SentenceScanner
- reminder/__init__.py
- Household canon
- answer.tsx
- tokens/page.tsx
- FolderAdapter
- extract_values
- Any
- chat/route.ts
- 10. `main` is unprotected, and the discipline is human
- scope.py
- api.ts
- today/page.tsx
- values.py
- test_api.py
- ModuleAdviser
- grade
- StreamingGraph
- sweep
- create_app
- devDependencies
- Working agreement for coding agents
- test_grounding_index.py
- FakeCursor
- Desmond — Lane E · Corpus and adversarial testing
- schedule.py
- test_ingest_pipeline.py
- Any
- 2. One PostgreSQL instance for everything
- adr/README.md
- date
- package.json
- _today_items
- postcss.config.mjs
- 4. Writing `pack.yaml`
- 13. A question is understood before it is searched, and scoped before it is cut
- Try PARROT
- github.md
- Cursor
- test_eval_harness.py
- gate.py
- Notebook prompts — the four full policies for Marcus Lim
- install_best_effort
- test_advice_core.py
- classify.py
- First run
- igd-capstone-2026
- FakeCursor
- FakeCursor
- Zee — Lane D · Domain packs and interface
- Authoring a domain pack
- Christian — Lane A · Integration and product owner
- Siew — Lane C · Governance and assurance
- FakeCursor
- ._advice_reads_what_the_pack_declares
- Alert
- _Value
- contracts.py
- Any
- Yew Mun — Lane B · Retrieval and evaluation
- Registration
- reference_for
- 14 · A pack supplies what the core knows about a domain, and the core stays generic
- 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent
- is_first_person
- The team
- _as_response
- installed_packs
- NNNN · The decision, as a statement not a question
- main
- scripts
- Notice
- 5. The watched folder is polled for stability, not subscribed to for events
- 7. The answer graph ships before hybrid retrieval and before a checkpoint table
- extraction_f1
- routes.py
- eslint.config.mjs
- __init__.py
- README.md
- usable
- sets_io.py
- RagasJudge
- Figure
- next
- quiet_engine
- unprinted_numbers
- test_generated_files_are_in_sync
- Calculation
- send_retry
- eval/__init__.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 159 edges
2. `Passage` - 84 edges
3. `InstalledPack` - 77 edges
4. `AnswerGraph` - 72 edges
5. `ScriptedOllama` - 72 edges
6. `build_router()` - 67 edges
7. `Ollama` - 66 edges
8. `FakeConn` - 60 edges
9. `settings()` - 54 edges
10. `client_for()` - 54 edges

## Surprising Connections (you probably didn't know these)
- `lifespan()` --indirect_call--> `install_best_effort()`  [INFERRED]
  api/main.py → core/registry.py
- `test_a_module_may_read_grounding_values()` --uses--> `ModuleManifest`  [INFERRED]
  tests/test_contracts.py → core/contracts.py
- `create_app()` --uses--> `Check`  [INFERRED]
  api/main.py → core/runtime/checks.py
- `create_app()` --uses--> `Lifecycle`  [INFERRED]
  api/main.py → core/runtime/lifecycle.py
- `create_app()` --uses--> `Settings`  [INFERRED]
  api/main.py → core/runtime/settings.py

## Import Cycles
- None detected.

## Communities (215 total, 20 thin omitted)

### Community 0 - "run_parrot.py"
Cohesion: 0.10
Nodes (28): Load the generator and the embedder before the first question, and record the…, warm_models(), broker_available(), Whether Redis answers. Not whether a worker is listening —…, _kill_tree(), main(), open_browser(), parse_args() (+20 more)

### Community 1 - "packs/page.tsx"
Cohesion: 0.08
Nodes (19): dynamic, metadata, PacksPage(), runtime, dynamic, metadata, runtime, Toggle() (+11 more)

### Community 2 - "Christian — task list"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.09
Nodes (41): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+33 more)

### Community 4 - "ingest/quarantine.py"
Cohesion: 0.07
Nodes (57): blocked_reasons(), forget(), Any, Path, ValueError, QuarantinedDocument, queue(), The second stage of quarantine: the page image, read by the vision-language… (+49 more)

### Community 5 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 6 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 7 - "sha256"
Cohesion: 0.14
Nodes (21): CaptureAdapter, datetime, Protocol, The one interface every capture channel satisfies. receive(payload, mime,…, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sha256(), Capture adapters. Every channel a document can arrive through satisfies one… (+13 more)

### Community 8 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 9 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 10 - "Desmond — task list"
Cohesion: 0.18
Nodes (11): Desmond — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 11 - "Zee — task list"
Cohesion: 0.22
Nodes (9): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20, W9 — due 2026-11-03 (+1 more)

### Community 12 - "Yew Mun — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

### Community 13 - "score.py"
Cohesion: 0.12
Nodes (20): F1, held_back(), Judge, judge_all(), judge_sync(), mean(), _median(), Any (+12 more)

### Community 14 - "Filling the corpus register"
Cohesion: 0.20
Nodes (9): Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one, The rule that cannot bend (+1 more)

### Community 15 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (9): Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six, Where governance touches the code (+1 more)

### Community 16 - "Claude Code — read this first"
Cohesion: 0.33
Nodes (5): Before you say you are done, Claude Code — read this first, Finding your way around, Skills and commands, The three things agents get wrong here

### Community 17 - "test_worker_queue.py"
Cohesion: 0.12
Nodes (26): Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker. Celery is imported here rather…, FakeConnection, MonkeyPatch, Path, The queue, tested with no broker anywhere. What is worth asserting here is not… (+18 more)

### Community 18 - "index_pack"
Cohesion: 0.12
Nodes (31): CaptureFixture, GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records…, SourceText, index_pack(), IndexReport, Any, date (+23 more)

### Community 19 - "ingest/extract.py"
Cohesion: 0.13
Nodes (22): _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact, Extraction, _normalise(), _prepare() (+14 more)

### Community 20 - "Household canon"
Cohesion: 0.25
Nodes (7): Address, Employment, Household canon, Life events that documents must reflect, People, Policies, Vehicles

### Community 21 - "retrieve.py"
Cohesion: 0.15
Nodes (20): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a…, ndarray, load_matrix(), pack(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.…, Return (N x D matrix of normalised embeddings, chunk ids)., stats() (+12 more)

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

### Community 29 - "sweep"
Cohesion: 0.16
Nodes (15): Due, Smaller is more urgent. The Today surface orders by this., Everything inside a lead window that has not already been said for that window.…, sweep(), obligation_row(), datetime, A sweep for a date in the future must record that date, or it repeats itself., test_a_dry_run_records_nothing() (+7 more)

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
Cohesion: 0.33
Nodes (5): Evaluation, Ground truth comes free, Running the harness, The honesty check, Writing questions

### Community 38 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 39 - ".__init__"
Cohesion: 0.13
Nodes (13): AdviceLog, Adviser, ConsentBook, Protocol, Implemented by `HouseholdConsents` in `core/advice_consent.py`., The granting row's id, or `None` when the owner has not granted this exact…, Implemented by `HouseholdAdviceLog` in `core/advice_records.py`., Implemented by `modules/advice/`. `core/` calls this; it never computes a… (+5 more)

### Community 40 - "pack"
Cohesion: 0.07
Nodes (30): holdings(), Any, Rows of `INVENTORY`, one holding per document that prints the field its pack's…, indexed(), IndexedDocument, Any, RuntimeError, Rebuild a document's chunks and vectors without reading it again for facts.… (+22 more)

### Community 41 - "Changelog"
Cohesion: 0.50
Nodes (3): Changelog, W1 · 2–8 Sep 2026, W2 · 9–15 Sep 2026

### Community 42 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 43 - "`docs/governance/` — the assurance artefacts"
Cohesion: 0.50
Nodes (3): `docs/governance/` — the assurance artefacts, The autonomy statement in one line, The rule that governs all eight

### Community 51 - "Ollama"
Cohesion: 0.20
Nodes (8): answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, Ollama, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.…, Batch embeddings. Falls back to the legacy endpoint on old servers., Hit

### Community 52 - "The household, and the word "my""
Cohesion: 0.10
Nodes (19): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model (+11 more)

### Community 53 - "IngestJob"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 54 - "alert/__init__.py"
Cohesion: 0.19
Nodes (21): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), Any, date (+13 more)

### Community 55 - "ingest.py"
Cohesion: 0.22
Nodes (13): Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks. Paperwork is short and…, _split_page(), discover(), guess_date(), guess_type() (+5 more)

### Community 56 - "test_household.py"
Cohesion: 0.11
Nodes (33): _household_scope(), MonkeyPatch, Person, Who is asking, and whose documents may answer. Two halves, deliberately split.…, `empty_for_owner` must never fire on a question that was never scoped —…, `HouseholdScope` over a roster held in memory, with every document resolved by…, The roster has no grandparent relation, so the household says it the only way…, 13 September: "what is Marcus's premium?" has no "my", so nothing was scoped… (+25 more)

### Community 57 - "advice/__init__.py"
Cohesion: 0.09
Nodes (60): Input, One fact or rule value a calculation was built on, carrying its own citation.…, _ambiguous(), _amount(), _band(), _band_label(), Basis, _calculation() (+52 more)

### Community 58 - "cli.py"
Cohesion: 0.16
Nodes (22): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+14 more)

### Community 59 - "harness.py"
Cohesion: 0.08
Nodes (30): _graph_for(), HouseholdConsents, `core.graph.advice.ConsentBook` over a live connection, for the graph to ask…, HouseholdAdviceLog, The record of every advised or withheld answer (ADR 0016). `advice_records`…, `core.graph.advice.AdviceLog` over a live connection. `basis` is dumped with…, AdviceRecord, Every advised or withheld answer's full basis, so it can be reconstructed later… (+22 more)

### Community 60 - "Ollama"
Cohesion: 0.06
Nodes (56): A dense-only retriever, so the graph can be run and tested before Lane B's…, Dispatcher, Inline, Protocol, What happens to a document between "these bytes are registered" and "this…, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided. (+48 more)

### Community 61 - "test_pages.py"
Cohesion: 0.09
Nodes (37): page_images(), Base64 page images, in page order. Empty when this document cannot be rendered.…, page_count(), PageUnavailable, _pdfium(), Any, LookupError, RuntimeError (+29 more)

### Community 62 - "extract"
Cohesion: 0.12
Nodes (30): extract(), Never raises. A failure is a reason, and a reason routes the document to…, Generated, FakeOllama, _page_of_examples(), Any, Exception, parametrize (+22 more)

### Community 63 - "bench_runtime.py"
Cohesion: 0.08
Nodes (34): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+26 more)

### Community 64 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 65 - "export-design-preview.cjs"
Cohesion: 0.11
Nodes (17): bundle(), classes, css, cssFile, domId, fs, ids, licences (+9 more)

### Community 66 - "test_startup.py"
Cohesion: 0.11
Nodes (28): Start `npm run dev` in `web/`, or say plainly why it could not. Three reasons…, start_web(), main(), Path, Local-only startup preflight, using the standard library so setup can be…, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file…, report_hardware() (+20 more)

### Community 67 - "pipeline.py"
Cohesion: 0.09
Nodes (26): Chunk, What is actually embedded: the prefix plus the text, matching the tsvector…, The ingestion worker. Capture registers a document; this package turns it into…, fixed(), from_facts(), _label(), Any, date (+18 more)

### Community 68 - "registry.py"
Cohesion: 0.13
Nodes (26): installed_modules(), Every module directory holding a `module.yaml`, in a stable order. Directories…, enabled_module_ids(), install(), Installed, _module_row(), modules(), _pack_row() (+18 more)

### Community 69 - "ModelUnavailable"
Cohesion: 0.08
Nodes (20): The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), ModelUnavailable, Any, Client, RuntimeError, A question, embedded the way the model was trained to embed a search query. (+12 more)

### Community 70 - "test_advice_module.py"
Cohesion: 0.14
Nodes (53): FactRow, calculate(), assert_nothing_negative(), basis(), fact(), figures_of(), _gap_basis(), _held() (+45 more)

### Community 71 - "FakeConn"
Cohesion: 0.12
Nodes (6): _Connected, FakeConn, FakeCursor, Any, FakeConn, A recording fake in the house style (see `tests/test_api.py`'s `FakeConn`):…

### Community 72 - "preview.tsx"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 73 - "Scoped"
Cohesion: 0.15
Nodes (14): The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting…, Keep the passages of these people and of the household; set aside everybody…, scope_to(), Scoped, 13 September: "how much is my son's life insurance?" came back as the owner's…, 13 September: "is my dad's hospital cover still active?" was scoped to Lim Ah…, "When does Rachel's policy renew?" is scoped to Rachel by name, with no… (+6 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (17): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+9 more)

### Community 75 - "test_modules.py"
Cohesion: 0.21
Nodes (20): Measurement, by_subject(), db(), load_register(), Any, date, fixture, Reminder and Alert: what fires, once, and with what behind it. Both modules are… (+12 more)

### Community 76 - "main"
Cohesion: 0.16
Nodes (21): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), main(), _note() (+13 more)

### Community 77 - "Notion"
Cohesion: 0.29
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "Passage"
Cohesion: 0.11
Nodes (40): AnswerGraph, Declined, The pack's own decline, signed with its disclaimer, and a question it can…, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed…, One sentence that has passed the gate, with the citations it passed on. It will…, A request for a recommendation or a judgement, declined before anything is…, Built once, asked many times. Holds no connection: retrieval does., Reading (+32 more)

### Community 79 - "The demonstration run sheet"
Cohesion: 0.14
Nodes (14): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+6 more)

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (7): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Contributing"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 82 - "[...path]/route.ts"
Cohesion: 0.15
Nodes (17): ALLOWED, Context, DELETE(), dynamic, forward(), GET(), PATCH(), POST() (+9 more)

### Community 83 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 84 - "._advise"
Cohesion: 0.09
Nodes (20): Claim, _advice_basis(), _advice_prompt(), ConsentRequired, _distinct(), _input_citation(), Any, date (+12 more)

### Community 85 - "load_set"
Cohesion: 0.29
Nodes (12): load_set(), MalformedQuestion, SetId, ValueError, A line the harness cannot grade. The message names the file and the line., Every question in `eval/sets/<folder>/*.jsonl`, in file order, validated. An…, Path, test_a_fact_question_needs_a_value_and_a_page() (+4 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "answer.py"
Cohesion: 0.05
Nodes (58): Category, A kind of document a household holds, recognised by words printed in its name.…, _as_sentence(), _asked(), _citations(), _conversation(), fuse(), _numbered() (+50 more)

### Community 89 - "(app)/layout.tsx"
Cohesion: 0.08
Nodes (24): lucide-react, react, dynamic, runtime, LockButton(), SURFACES, TabBar(), Tabs() (+16 more)

### Community 90 - "lock.ts"
Cohesion: 0.13
Nodes (28): dynamic, GET(), grant(), POST(), runtime, dynamic, metadata, runtime (+20 more)

### Community 91 - "main.py"
Cohesion: 0.17
Nodes (19): The local API. Liveness is intentionally separate from assistant readiness.…, AsyncClient, asyncio, capture_check(), Check, collect_checks(), database_check(), interface_check() (+11 more)

### Community 92 - "FakeConn"
Cohesion: 0.10
Nodes (32): Channel, ConsentStatus, current(), grant(), _latest(), NoOwner, Any, RuntimeError (+24 more)

### Community 93 - "test_answer_graph.py"
Cohesion: 0.07
Nodes (43): Abstained, _either(), "a dental plan", or "a term life plan or a whole life plan". "An" only before…, Refused, build(), events(), passage(), Any (+35 more)

### Community 94 - "TelegramCapture"
Cohesion: 0.12
Nodes (16): RuntimeError, Safe to show: never contains the token., TelegramSettings, TelegramUnavailable, attribution(), Any, A daemon thread that long-polls the Telegram bot until `stop()` or process…, Begin polling. Returns False, with a logged reason, when it cannot or should… (+8 more)

### Community 102 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "Settings"
Cohesion: 0.11
Nodes (54): Whether Telegram capture should start. An unset token means "not this…, Settings, client_for(), FakeConn, filed_document(), inbox(), open_obligation(), pack_row() (+46 more)

### Community 104 - "build_router"
Cohesion: 0.09
Nodes (35): CorrectionResponse, ForgottenDocument, HouseholdResponse, ModuleSummary, ObligationChanged, PacksResponse, PackSummary, What changed, in the words the screen confirms it with. `was` is returned… (+27 more)

### Community 105 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 106 - "test_telegram_capture.py"
Cohesion: 0.12
Nodes (32): MockTransport, build(), FakeTelegram, photo_update(), Any, Path, Request, Response (+24 more)

### Community 107 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 108 - "ScriptedOllama"
Cohesion: 0.08
Nodes (48): AdviceCard, AdviceWithheld, answer_system(), Finished, The pack's voice first, the core's rules last: a persona cannot loosen what…, Everything that is only knowable once the last sentence is in. `quarantined`…, Advice could not be worked out, and `missing` says what it needs, in the pack's…, A worked result, every word of it written by code, given before the model says… (+40 more)

### Community 109 - ".load"
Cohesion: 0.12
Nodes (32): ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one…, _folder(), Path, The watched folder, absolute, so a check and a worker never disagree about…, _ollama_answering(), Any, MonkeyPatch (+24 more)

### Community 110 - "vault.py"
Cohesion: 0.07
Nodes (38): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+30 more)

### Community 111 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 112 - "test_gate.py"
Cohesion: 0.14
Nodes (29): check_advice(), Claim, Why an advice explanation cannot be kept, or `None`. Asked of a claim built…, test_a_claim_citing_the_same_document_twice_says_it_once(), test_a_grounded_claim_renders_its_document_and_page(), What the gate checks beyond "is there a citation". A cited sentence can still…, `target` and `gap` both print SGD 500,000.00 (`_gap` with `held` at zero).…, The defect this fixes: naming `gap`, the *second* figure in `figures` order to… (+21 more)

### Community 113 - "test_grounding_values.py"
Cohesion: 0.16
Nodes (33): LogCaptureFixture, _dropped(), _log_values(), Decimal, fixture, parametrize, Published values: the model reads a source, and code keeps only what the…, Assert a value was dropped, and logged with this reason. (+25 more)

### Community 114 - "household.py"
Cohesion: 0.11
Nodes (32): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner_aliases(), pending() (+24 more)

### Community 115 - "test_grounding.py"
Cohesion: 0.19
Nodes (22): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError, Read and validate a pack's grounding corpus from its own folder on disk. A…, A pack's grounding corpus on disk does not match what its `sources.yaml`… (+14 more)

### Community 116 - "TelegramAdapter"
Cohesion: 0.11
Nodes (23): BaseTransport, IngestJob, What a capture returns: a registered document, and whether we had seen it…, _attachment(), _pixels(), Any, Client, datetime (+15 more)

### Community 117 - "scope_passages"
Cohesion: 0.23
Nodes (13): Any, Keep the owner's passages and the household's; set aside everybody else's. A…, scope_passages(), _conn_returning(), _passage(), The third bucket. Home contents, a utility bill — nobody's name on it,…, A joint policy is the owner's too. Presence wins over exclusion., Asked about my policy; the vault holds Rachel's. Say so, rather than answer… (+5 more)

### Community 118 - "test_lifecycle.py"
Cohesion: 0.13
Nodes (26): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor.…, What the person asked for, once. The first request wins; later ones change…, _client(), _eventually(), _launcher(), parametrize, Path (+18 more)

### Community 120 - "app/layout.tsx"
Cohesion: 0.22
Nodes (7): next-themes, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 121 - "build.py"
Cohesion: 0.19
Nodes (16): _class_name(), _docstring(), _field_line(), load(), main(), Path, Generate everything downstream of a pack.yaml. python -m packs.build #…, The header row Desmond fills in, one file per pack. Long format: one row per… (+8 more)

### Community 122 - "test_contracts.py"
Cohesion: 0.09
Nodes (51): PackManifest, A domain pack, authored as one YAML file., check_advice_links(), Every fact an advice shape reads from another pack is declared by an installed…, _advised(), _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held() (+43 more)

### Community 123 - "SentenceScanner"
Cohesion: 0.09
Nodes (29): Any, Pulling finished sentences out of a JSON reply that is still being written. The…, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner (+21 more)

### Community 124 - "reminder/__init__.py"
Cohesion: 0.11
Nodes (24): already_said(), close(), current_lead(), next_window(), Overdue, Any, date, datetime (+16 more)

### Community 125 - "Household canon"
Cohesion: 0.08
Nodes (23): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, Policies, The family tree, and why three of them are not called Lim (+15 more)

### Community 126 - "answer.tsx"
Cohesion: 0.10
Nodes (18): Abstention(), Part, sentence(), textOf(), ADR-0011, Turn(), SourceChip(), SourcePanel() (+10 more)

### Community 127 - "tokens/page.tsx"
Cohesion: 0.11
Nodes (10): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+2 more)

### Community 128 - "FolderAdapter"
Cohesion: 0.09
Nodes (37): Magic bytes first, filename suffix second, `application/octet-stream` last. A…, sniff_mime(), FolderAdapter, FolderSettings, _Pending, datetime, Path, The watched-folder capture adapter. A person drops a scan into a folder and it… (+29 more)

### Community 129 - "extract_values"
Cohesion: 0.19
Nodes (18): extract_values(), Every value the source prints for these keys, kept only when its passage prints…, _long_text(), Any, Exception, Returns the replies the test wrote, in order, then an empty list of values. A…, A truncated or non-JSON reply is an outage: the section was never actually…, Unlike a garbled reply, valid JSON with the wrong shape means the model… (+10 more)

### Community 130 - "Any"
Cohesion: 0.11
Nodes (21): advised_pack(), db(), _document(), _facts_tuple(), FakeConn, FakeCursor, Any, date (+13 more)

### Community 131 - "chat/route.ts"
Cohesion: 0.23
Nodes (12): ai, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns(), readEvents() (+4 more)

### Community 132 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 133 - "scope.py"
Cohesion: 0.23
Nodes (14): _decide(), _Decision, named_in(), _names(), Whose question is this, and whose documents may answer it. "What is my term…, `(word, relation)` when the question asks about a relation's own documents,…, Everybody in `people` the question names. A person is named by a whole display…, Who a question is about, decided once and read differently by `apply` and… (+6 more)

### Community 134 - "api.ts"
Cohesion: 0.08
Nodes (29): DocumentPage(), dynamic, metadata, runtime, RELATION_CHOICES, Place, PLACES, DocumentDetail() (+21 more)

### Community 136 - "today/page.tsx"
Cohesion: 0.08
Nodes (25): dynamic, HouseholdPage(), metadata, runtime, AppLayout(), dynamic, isUrgent(), metadata (+17 more)

### Community 137 - "values.py"
Cohesion: 0.07
Nodes (36): A rule or table value a pack's sources publish. Extracted automatically,…, ValueKey, _check(), collapse(), _cuts_a_number(), ExtractedValue, _groups(), _is_heading() (+28 more)

### Community 138 - "test_api.py"
Cohesion: 0.08
Nodes (42): Answer, Answered. Asking for consent and naming what is missing are endings, not…, Asks, Protocol, The one method of `AnswerGraph` the harness uses. A test supplies a fake., client(), conn(), FakeGraph (+34 more)

### Community 139 - "ModuleAdviser"
Cohesion: 0.13
Nodes (24): FactInput, A printed fact a calculator reads, named by where it is printed rather than…, fact_row(), FactRow, facts_for(), in_category(), _is_an_adviser(), _latest_per_document() (+16 more)

### Community 140 - "grade"
Cohesion: 0.17
Nodes (13): cites(), _contains(), doc_stem(), grade(), mentions(), `b1-0001.pdf` is register row `b1-0001`. The register's id is the file name's…, Whether any sentence of the answer is cited to the document and page the…, Whether the page the answer should come from was among the passages the model… (+5 more)

### Community 141 - "StreamingGraph"
Cohesion: 0.12
Nodes (22): Citation, A passage, named the way a person cites it and identified the way a link needs.…, a_citation(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive…, No `reading` before it: the floor is checked before the model is asked anything., By then the 200 has been sent. An exception that only logged would leave a… (+14 more)

### Community 142 - "sweep"
Cohesion: 0.33
Nodes (11): Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), FakeConn, FakePack, One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order., srs_row(), test_a_firing_older_than_the_debounce_window_fires_again(), test_a_metric_no_query_defines_cannot_fire() (+3 more)

### Community 143 - "create_app"
Cohesion: 0.27
Nodes (7): create_app(), checks(), lifespan(), ready(), setup(), system_status(), FastAPI

### Community 144 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 145 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents

### Community 146 - "test_grounding_index.py"
Cohesion: 0.11
Nodes (30): approve(), pending(), PendingValue, Any, date, A person's approval, standing between a model's extraction and any calculator…, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it. (+22 more)

### Community 147 - "FakeCursor"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 149 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 150 - "schedule.py"
Cohesion: 0.15
Nodes (17): build(), Any, The one Celery application, built from `Settings`. Every setting here is a…, Construct the Celery application. Imported lazily by callers so that nothing…, beat_schedule(), cron_expressions(), crontab_from(), manifest() (+9 more)

### Community 151 - "test_ingest_pipeline.py"
Cohesion: 0.06
Nodes (55): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, One flat list of chunks, ordinal running across the whole document., The page as `(is_heading, line)`, from the parser's structure when it has any. (+47 more)

### Community 152 - "Any"
Cohesion: 0.19
Nodes (3): FakeCursor, Any, The parameters of the one statement containing `needle`. Fails loudly if it…

### Community 153 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "adr/README.md"
Cohesion: 0.06
Nodes (28): 1. Record architecture decisions, Consequences, Context, Decision, 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision (+20 more)

### Community 155 - "date"
Cohesion: 0.13
Nodes (22): document_row(), fact_row(), obligation(), overdue_row(), date, One row of `reminder.OVERDUE`, in its column order., Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with…, The Celery beat never goes through the API, so the filter cannot live there. (+14 more)

### Community 156 - "package.json"
Cohesion: 0.11
Nodes (16): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+8 more)

### Community 157 - "_today_items"
Cohesion: 0.13
Nodes (20): A document and a page, as a person would cite it., Source, TodayItem, TodayResponse, today(), _cite(), connection(), _link() (+12 more)

### Community 159 - "4. Writing `pack.yaml`"
Cohesion: 0.12
Nodes (15): 1. What a pack is, 2. The one thing to understand before you start, 3. The workflow, 4. Writing `pack.yaml`, 5. The grounding corpus, 6. Definition of done, 7. Where to ask, Authoring a domain pack (+7 more)

### Community 160 - "13. A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.40
Nodes (5): 13. A question is understood before it is searched, and scoped before it is cut, Consequences, Context, Decision, Evidence

### Community 161 - "Try PARROT"
Cohesion: 0.12
Nodes (16): 1 · Install five things, 2 · Download the AI models, 3 · Get the code and set it up, 4 · Put some documents in, 5 · Run it, 6 · Use it, Ask — a question about your own documents, If something goes wrong (+8 more)

### Community 162 - "github.md"
Cohesion: 0.50
Nodes (3): Last sync, Screen map, Updated in this project

### Community 163 - "Cursor"
Cohesion: 0.25
Nodes (4): Cursor, Any, Protocol, cursor()

### Community 164 - "test_eval_harness.py"
Cohesion: 0.15
Nodes (20): Cited, One sentence and the passages it was traced to. What rule 3 looks like as data.…, Each question on its own thread, so no answer is a follow-up to the one before., Trace, trace_all(), _table(), Expected, Any (+12 more)

### Community 165 - "gate.py"
Cohesion: 0.16
Nodes (12): check(), check_one(), The grounding gate. Rule 3 in AGENTS.md: no claim without a citation. This…, Never raises, never rewrites a claim. It keeps, drops, or abstains. The whole-…, Why this one sentence cannot be kept, or `None` if it can. Depends on nothing…, _says(), Verdict, test_a_sentence_citing_a_passage_that_was_never_retrieved_is_dropped() (+4 more)

### Community 166 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 167 - "install_best_effort"
Cohesion: 0.22
Nodes (14): install_best_effort(), Install at startup without being able to stop startup. Both processes that own…, _beat_needs_its_own_process(), celery_argv(), main(), Any, Namespace, Popen (+6 more)

### Community 168 - "test_advice_core.py"
Cohesion: 0.36
Nodes (10): check_content(), Why a cited sentence still cannot be kept, or `None`. Asked after `check_one`…, _calculation(), The types a calculator hands back, the owner's consent, and the record of an…, test_check_content_keeps_a_sentence_stating_a_facts_value(), test_check_content_keeps_a_sentence_stating_a_figure(), test_check_content_keeps_a_sentence_stating_a_rules_value(), test_check_content_still_drops_a_sentence_stating_an_unprinted_number() (+2 more)

### Community 169 - "classify.py"
Cohesion: 0.16
Nodes (14): DocumentTypeSpec, One kind of document this pack recognises., Classification, classify(), _prompt(), Decide which pack's document type a captured document is, or decline to. The…, Never raises. An unavailable model is a classification failure, so it…, _schema() (+6 more)

### Community 170 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 171 - "igd-capstone-2026"
Cohesion: 0.20
Nodes (10): Authoring a pack, igd-capstone-2026, `main` is not protected, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live (+2 more)

### Community 172 - "FakeCursor"
Cohesion: 0.20
Nodes (3): FakeCursor, Any, FakeConn

### Community 174 - "Zee — Lane D · Domain packs and interface"
Cohesion: 0.22
Nodes (9): Half one — domain packs (weeks 1 to 7), Half two — the interface (weeks 4 to 8), Read this first, Rules that apply to you specifically, The two halves of this lane, What "done" looks like, What you present, Your Claude Code skills (+1 more)

### Community 175 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 176 - "Christian — Lane A · Integration and product owner"
Cohesion: 0.29
Nodes (7): Also yours, Christian — Lane A · Integration and product owner, Starter prompt for your coding agent, Starter prompt: what can I actually pick up?, The five things you ship, Week 1, in order, What integration actually means here

### Community 177 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.29
Nodes (7): Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The autonomy statement, The six artefacts, Where governance touches the code

### Community 179 - "._advice_reads_what_the_pack_declares"
Cohesion: 0.25
Nodes (4): Why this pack cannot supply `field` from every one of `doc_types`, or None if…, An advice shape that names a missing role, field, category or key fails at load…, A compared field no document type of the shape declares can never be printed.…, model_validator

### Community 180 - "Alert"
Cohesion: 0.25
Nodes (5): Alert, What the debounce is keyed on: this metric, for this person and thing, in this…, Two lapsed policies on one person are two alerts, and saying one must not…, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

### Community 181 - "_Value"
Cohesion: 0.33
Nodes (6): _Value, Hashable, _order_key(), _ordered(), One sortable key for a number, a date or a word, so a ranking never compares…, Keys ranked by value in the stated order, ties broken by name so a ranking is…

### Community 182 - "contracts.py"
Cohesion: 0.06
Nodes (39): Advice, AlertConfig, Answering, Categories, Exclusions, FieldSpec, Grounding, Guardrails (+31 more)

### Community 183 - "Any"
Cohesion: 0.15
Nodes (15): The person a printed name means, or `None` if nobody has confirmed what it…, Hand the household over. The owner is a row, not a value baked in at install.…, resolve(), set_owner(), conn(), Any, fixture, A second document must never silently move a name from one member to another. (+7 more)

### Community 184 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

### Community 185 - "Registration"
Cohesion: 0.15
Nodes (8): Intake, An already-indexed document is not read again. Re-reading it would burn a…, The row as it now stands, plus whether this call is the one that created it., Registration, Outcome, FakeRegistrar, The `documents` table, reduced to the one thing it guarantees: sha256 is unique., explode_once()

### Community 186 - "reference_for"
Cohesion: 0.20
Nodes (11): _as_date(), _as_number(), date, Decimal, The register's text against an extracted value, each normalised the way the…, The reference answer Ragas judges recall and precision against. A fact…, The ways a register value is printed. `2027-04-11` appears on a schedule as "11…, reference_for() (+3 more)

### Community 187 - "14 · A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.33
Nodes (6): 14 · A pack supplies what the core knows about a domain, and the core stays generic, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 188 - "16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.33
Nodes (6): 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 189 - "is_first_person"
Cohesion: 0.33
Nodes (7): is_first_person(), Whether this question is about the person asking. `other_names` are the display…, parametrize, "What is Rachel's premium on my policy" is a question about Rachel. A…, test_a_named_household_member_wins_over_the_pronoun(), test_first_person_questions_are_recognised(), test_questions_about_other_people_are_not_scoped()

### Community 190 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 191 - "_as_response"
Cohesion: 0.14
Nodes (14): AskRequest, AskResponse, Claim, ErrorEvent, The stream broke after it began. A client cannot read an HTTP status by then., One sentence and the passages it was traced to. Never emitted without…, _as_response(), ask() (+6 more)

### Community 192 - "installed_packs"
Cohesion: 0.29
Nodes (7): installed_packs(), Every pack directory holding a pack.yaml, in a stable order. Directories whose…, test_every_installed_pack_still_loads(), test_every_document_type_has_a_generated_model(), test_the_template_directory_is_not_an_installed_pack(), A pack naming a metric nobody implemented is a silent no-op, so it is caught…, test_the_real_packs_declare_metrics_that_exist()

### Community 193 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 194 - "main"
Cohesion: 0.47
Nodes (5): documents_in(), main(), Path, Load a handed-over corpus batch into this computer's database. uv run python…, Every document in the batch, in a stable order, recursing into tier subfolders.

### Community 195 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 196 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 197 - "5. The watched folder is polled for stability, not subscribed to for events"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 198 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 199 - "extraction_f1"
Cohesion: 0.50
Nodes (5): extraction_f1(), FactRow, One row of the `facts` table, as the harness reads it: which document, which…, Field extraction scored against the register, overall and by document type. The…, test_extraction_f1_scores_only_indexed_documents_against_the_register()

### Community 200 - "routes.py"
Cohesion: 0.09
Nodes (45): AbstentionEvent, CloseRequest, ConfirmNameRequest, CorrectionRequest, DeclinedEvent, EnabledRequest, FinishedEvent, OwnerRequest (+37 more)

### Community 201 - "eslint.config.mjs"
Cohesion: 0.50
Nodes (3): @eslint/eslintrc, compat, eslintConfig

### Community 205 - "sets_io.py"
Cohesion: 0.28
Nodes (8): field_page(), Path, The golden sets on disk, and the register they were written from. A question…, Desmond's register as rows. Comment lines are skipped; the header is the…, Every batch register, skipping the templates the pack build writes beside them., Which page a value is printed on. `field_pages` names only the fields that are…, read_register(), read_registers()

### Community 206 - "RagasJudge"
Cohesion: 0.32
Nodes (6): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts(), Ragas 0.4 metrics through Ollama's OpenAI-compatible endpoint. Imported lazily…

### Community 207 - "Figure"
Cohesion: 0.29
Nodes (7): Figure, One number a calculator produced, and the words a sentence must use to state…, _advice_calculation(), _gap_shared_value_calculation(), _meets_calculation(), A `meets` outcome: the gap figure is negative, and only its printed text…, `_gap`'s real figure construction order — target, held, gap — with `held` at…

### Community 208 - "next"
Cohesion: 0.18
Nodes (6): @ai-sdk/react, next, metadata, Conversation(), SUGGESTIONS, nextConfig

### Community 209 - "quiet_engine"
Cohesion: 0.50
Nodes (4): fixture, MonkeyPatch, quiet_engine(), No real probes, no startup writes, no deliberate pause before exiting. The…

### Community 210 - "unprinted_numbers"
Cohesion: 0.29
Nodes (7): _normal(), "1,860.00", "1860" and "01" → "1860", "1860", "1": formatting is not a…, Every number or identifier in a sentence that no cited passage prints. An…, unprinted_numbers(), test_a_date_on_file_may_be_written_the_way_a_person_says_it(), test_a_leading_zero_does_not_make_a_printed_date_unprinted(), test_a_policy_number_is_kept_only_when_it_is_printed_whole()

### Community 215 - "Calculation"
Cohesion: 0.13
Nodes (19): AdviceShape, One kind of advice question, and everything its calculator needs to answer it., Calculation, _kind_of(), Missing, passages_for(), date, What a calculator returns, and what the graph needs to ask consent and keep a… (+11 more)

### Community 219 - "send_retry"
Cohesion: 0.40
Nodes (5): 202. The vision pass is slower than a page load, so it is queued and this is…, RetryAccepted, retry_one(), Put one quarantine retry on the queue and return its task id. The vision pass…, send_retry()

## Knowledge Gaps
- **630 isolated node(s):** `npx`, `@modelcontextprotocol/server-filesystem`, `_Formatter`, `parrot`, `setup.sh script` (+625 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1682 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `run_parrot.py`, `FolderAdapter`, `Any`, `ingest/quarantine.py`, `sha256`, `test_api.py`, `StreamingGraph`, `create_app`, `test_grounding_index.py`, `schedule.py`, `date`, `_today_items`, `install_best_effort`, `Any`, `test_household.py`, `harness.py`, `Ollama`, `bench_runtime.py`, `main`, `test_startup.py`, `registry.py`, `test_advice_module.py`, `routes.py`, `test_modules.py`, `main`, `send_retry`, `main.py`, `TelegramCapture`, `build_router`, `test_telegram_capture.py`, `.load`, `test_lifecycle.py`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Why does `Connection` connect `retrieve.py` to `cli.py`, `Cursor`, `ingest.py`, `sha256`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `Ollama` connect `Ollama` to `run_parrot.py`, `extract_values`, `ingest/quarantine.py`, `values.py`, `index_pack`, `ingest/extract.py`, `.__init__`, `classify.py`, `harness.py`, `extract`, `pipeline.py`, `ModelUnavailable`, `routes.py`, `main`, `Passage`, `answer.py`, `TelegramCapture`, `Settings`, `build_router`, `.load`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 121 inferred relationships involving `Settings` (e.g. with `create_app()` and `build_router()`) actually correct?**
  _`Settings` has 121 INFERRED edges - model-reasoned connections that need verification._
- **Are the 37 inferred relationships involving `Passage` (e.g. with `_advice_prompt()` and `AnswerGraph`) actually correct?**
  _`Passage` has 37 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `InstalledPack` (e.g. with `Adviser` and `answer_system()`) actually correct?**
  _`InstalledPack` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `AnswerGraph` (e.g. with `AdviceShape` and `AdviceLog`) actually correct?**
  _`AnswerGraph` has 19 INFERRED edges - model-reasoned connections that need verification._