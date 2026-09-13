# Graph Report - igd-capstone-2026  (2026-09-15)

## Corpus Check
- 264 files · ~629,911 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 28 file(s) not represented in the graph (top: (none) 15, .csv 4, .css 3)

## Summary
- 3809 nodes · 8836 edges · 198 communities (170 shown, 21 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 705 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7be0a1c8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_parrot.py
- packs/page.tsx
- Christian — task list
- validate
- build_router
- Project PARROT — team split
- Project PARROT — team split
- Registration
- Running the evaluation harness
- support.js
- Desmond — task list
- Zee — task list
- Yew Mun — task list
- ingest/quarantine.py
- Filling the corpus register
- Writing a governance artefact
- Claude Code — read this first
- Queued
- folder.py
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
- AdviceShape
- ingest/reindex.py
- Changelog
- filesystem
- `docs/governance/` — the assurance artefacts
- corpus/__init__.py
- packs/__init__.py
- parrot
- Ollama
- The household, and the word "my"
- paperbrain/extract.py
- alert/__init__.py
- ingest.py
- test_household.py
- advice/__init__.py
- cli.py
- test_modules.py
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
- test_grounding_index.py
- preview.tsx
- scope_passages
- Starting Parrot
- FakeCursor
- chat/route.ts
- Notion
- test_answer_graph.py
- The demonstration run sheet
- PaperBrain
- Contributing
- [...path]/route.ts
- components.json
- answer.py
- ConfigurationError
- Architecture
- Roadmap
- knowledge.py
- power-menu.tsx
- lock.ts
- main.py
- FakeCursor
- events
- DatabaseUnavailable
- Home Contents Insurance Policy
- api/__init__.py
- core/__init__.py
- runtime/__init__.py
- modules/__init__.py
- setup.sh
- 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module
- Settings
- routes.py
- 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack
- test_telegram_capture.py
- Siew — task list
- ScriptedOllama
- .load
- vault.py
- dependencies
- Passage
- test_grounding_values.py
- household.py
- SourceText
- TelegramAdapter
- NNNN · The decision, as a statement not a question
- test_lifecycle.py
- worker/__init__.py
- app/layout.tsx
- pack
- test_contracts.py
- SentenceScanner
- reminder/__init__.py
- Household canon
- answer.tsx
- tokens/page.tsx
- FolderAdapter
- extract_values
- Any
- _as_module_summary
- 10. `main` is unprotected, and the discipline is human
- scope.py
- document-detail.tsx
- today/page.tsx
- values.py
- test_api.py
- FactRow
- test_advice_core.py
- StreamingGraph
- contracts.py
- ._claim
- devDependencies
- Working agreement for coding agents
- main
- Domain packs — start here
- Desmond — Lane E · Corpus and adversarial testing
- build
- test_ingest_pipeline.py
- Any
- 2. One PostgreSQL instance for everything
- adr/README.md
- test_today_is_ordered_overdue_then_alerts_then_reminders
- package.json
- _today_items
- postcss.config.mjs
- 4. Writing `pack.yaml`
- 13. A question is understood before it is searched, and scoped before it is cut
- Try PARROT
- github.md
- Scoped
- Cursor
- Alert
- Notebook prompts — the four full policies for Marcus Lim
- install_best_effort
- CaptureAdapter
- packs.py
- First run
- igd-capstone-2026
- manifest
- scripts
- Zee — Lane D · Domain packs and interface
- Authoring a domain pack
- Christian — Lane A · Integration and product owner
- Siew — Lane C · Governance and assurance
- ._handle
- .telegram_configured
- _dual_cited_calculation
- _ordered
- installed_packs
- _shared_value_calculation
- Yew Mun — Lane B · Retrieval and evaluation
- 14 · A pack supplies what the core knows about a domain, and the core stays generic
- 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent
- The team
- _as_response
- 5. The watched folder is polled for stability, not subscribed to for events
- Notice
- 7. The answer graph ships before hybrid retrieval and before a checkpoint table
- eslint.config.mjs
- grounding/__init__.py
- grounding/README.md
- advice/queries.py
- _meets_calculation
- next

## God Nodes (most connected - your core abstractions)
1. `Settings` - 155 edges
2. `InstalledPack` - 77 edges
3. `ScriptedOllama` - 72 edges
4. `AnswerGraph` - 70 edges
5. `Passage` - 70 edges
6. `build_router()` - 67 edges
7. `Ollama` - 62 edges
8. `FakeConn` - 60 edges
9. `settings()` - 54 edges
10. `client_for()` - 54 edges

## Surprising Connections (you probably didn't know these)
- `test_a_module_may_read_grounding_values()` --uses--> `ModuleManifest`  [INFERRED]
  tests/test_contracts.py → core/contracts.py
- `create_app()` --uses--> `Check`  [INFERRED]
  api/main.py → core/runtime/checks.py
- `create_app()` --uses--> `Lifecycle`  [INFERRED]
  api/main.py → core/runtime/lifecycle.py
- `create_app()` --uses--> `Settings`  [INFERRED]
  api/main.py → core/runtime/settings.py
- `lifespan()` --indirect_call--> `install_best_effort()`  [INFERRED]
  api/main.py → core/registry.py

## Import Cycles
- None detected.

## Communities (198 total, 21 thin omitted)

### Community 0 - "run_parrot.py"
Cohesion: 0.12
Nodes (26): Load the generator and the embedder before the first question, and record the…, warm_models(), _kill_tree(), main(), open_browser(), parse_args(), port_answers(), Any (+18 more)

### Community 1 - "packs/page.tsx"
Cohesion: 0.08
Nodes (19): dynamic, metadata, PacksPage(), runtime, dynamic, metadata, runtime, Toggle() (+11 more)

### Community 2 - "Christian — task list"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.09
Nodes (41): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+33 more)

### Community 4 - "build_router"
Cohesion: 0.09
Nodes (34): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, What changed, in the words the screen confirms it with. `was` is returned…, The row is gone from Today. `speaks_again` is null when it will not come back.…, 202. The vision pass is slower than a page load, so it is queued and this is… (+26 more)

### Community 5 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 6 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 7 - "Registration"
Cohesion: 0.09
Nodes (24): The one interface every capture channel satisfies. receive(payload, mime,…, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, sha256(), The ingestion worker. Capture registers a document; this package turns it into…, What every capture channel hands a document to. An adapter's job ends at "these…, An already-indexed document is not read again. Re-reading it would burn a…, Register a document, idempotently, on a SHA-256 of the source bytes. This is…, The row as it now stands, plus whether this call is the one that created it. (+16 more)

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

### Community 13 - "ingest/quarantine.py"
Cohesion: 0.12
Nodes (29): blocked_reasons(), forget(), page_images(), Any, Path, ValueError, QuarantinedDocument, queue() (+21 more)

### Community 14 - "Filling the corpus register"
Cohesion: 0.20
Nodes (9): Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one, The rule that cannot bend (+1 more)

### Community 15 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (9): Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six, Where governance touches the code (+1 more)

### Community 16 - "Claude Code — read this first"
Cohesion: 0.33
Nodes (5): Before you say you are done, Claude Code — read this first, Finding your way around, Skills and commands, The three things agents get wrong here

### Community 17 - "Queued"
Cohesion: 0.09
Nodes (22): Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker. Celery is imported here rather…, FakeConnection, FakeCursor, Any, MonkeyPatch (+14 more)

### Community 18 - "folder.py"
Cohesion: 0.16
Nodes (12): Magic bytes first, filename suffix second, `application/octet-stream` last. A…, sniff_mime(), _Pending, datetime, Path, The watched-folder capture adapter. A person drops a scan into a folder and it…, Every file in the watched folder that is worth looking at at all., Advance the debounce by `elapsed` seconds and return the files now ready. Time… (+4 more)

### Community 19 - "ingest/extract.py"
Cohesion: 0.14
Nodes (20): _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact, _normalise(), _prepare(), printed_date() (+12 more)

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
Cohesion: 0.21
Nodes (15): AlertConfig, Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), FakeConn, FakePack, One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order., A live travel policy must not make a lapsed motor policy read as covered., srs_row() (+7 more)

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
Nodes (5): Evaluation, Ground truth comes free, Metrics and targets, The honesty check, Writing questions

### Community 38 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 39 - "AdviceShape"
Cohesion: 0.07
Nodes (26): HouseholdAdviceLog, The record of every advised or withheld answer (ADR 0016). `advice_records`…, `core.graph.advice.AdviceLog` over a live connection. `basis` is dumped with…, AdviceShape, One kind of advice question, and everything its calculator needs to answer it., AdviceLog, AdviceRecord, Adviser (+18 more)

### Community 40 - "ingest/reindex.py"
Cohesion: 0.13
Nodes (12): pgvector accepts its own text form; this avoids registering an adapter for one…, _vector_literal(), indexed(), IndexedDocument, Any, RuntimeError, Rebuild a document's chunks and vectors without reading it again for facts.…, Safe to show: names what went wrong, never what the document says. (+4 more)

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

### Community 53 - "paperbrain/extract.py"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 54 - "alert/__init__.py"
Cohesion: 0.19
Nodes (21): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), Any, date (+13 more)

### Community 55 - "ingest.py"
Cohesion: 0.22
Nodes (13): Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks. Paperwork is short and…, _split_page(), discover(), guess_date(), guess_type() (+5 more)

### Community 56 - "test_household.py"
Cohesion: 0.12
Nodes (31): _household_scope(), MonkeyPatch, Person, Who is asking, and whose documents may answer. Two halves, deliberately split.…, `HouseholdScope` over a roster held in memory, with every document resolved by…, The roster has no grandparent relation, so the household says it the only way…, 13 September: "what is Marcus's premium?" has no "my", so nothing was scoped…, A model proposal is a question on Today, not a member yet — the same rule… (+23 more)

### Community 57 - "advice/__init__.py"
Cohesion: 0.09
Nodes (65): Figure, Input, One fact or rule value a calculation was built on, carrying its own citation.…, One number a calculator produced, and the words a sentence must use to state…, _ambiguous(), _amount(), _band(), _band_label() (+57 more)

### Community 58 - "cli.py"
Cohesion: 0.16
Nodes (22): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+14 more)

### Community 59 - "test_modules.py"
Cohesion: 0.20
Nodes (18): current_lead(), The tightest lead window this obligation has entered, or None if it has entered…, Everything inside a lead window that has not already been said for that window.…, sweep(), obligation_row(), datetime, parametrize, Reminder and Alert: what fires, once, and with what behind it. Both modules are… (+10 more)

### Community 60 - "Ollama"
Cohesion: 0.06
Nodes (64): _graph_for(), DenseRetriever, NoReranker, A dense-only retriever, so the graph can be run and tested before Lane B's…, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this…, HouseholdInventory, Handed to `AnswerGraph` by whoever holds a connection, as `HouseholdScope` is., bytes_for() (+56 more)

### Community 61 - "test_pages.py"
Cohesion: 0.09
Nodes (35): page_count(), PageUnavailable, _pdfium(), Any, LookupError, RuntimeError, One page of one document, as an image. Two callers want the same thing for…, Safe to show a person: there is no such page, or this file cannot be drawn. (+27 more)

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
Cohesion: 0.10
Nodes (28): main(), Path, Local-only startup preflight, using the standard library so setup can be…, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file…, report_hardware(), startup_gaps(), prepare_checkout() (+20 more)

### Community 67 - "pipeline.py"
Cohesion: 0.08
Nodes (28): Chunk, What is actually embedded: the prefix plus the text, matching the tsvector…, What happens to a document between "these bytes are registered" and "this…, Extraction, fixed(), from_facts(), _label(), Any (+20 more)

### Community 68 - "registry.py"
Cohesion: 0.12
Nodes (28): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders…, installed_modules(), InstalledModule, Load the installed capability modules at runtime. The mirror of…, Every module directory holding a `module.yaml`, in a stable order. Directories…, enabled_module_ids(), install() (+20 more)

### Community 69 - "ModelUnavailable"
Cohesion: 0.08
Nodes (20): The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), ModelUnavailable, Any, Client, RuntimeError, A question, embedded the way the model was trained to embed a search query. (+12 more)

### Community 70 - "test_advice_module.py"
Cohesion: 0.13
Nodes (58): Calculation, Missing, What a calculator returns when every fact and rule it needed was on file and…, What a calculator returns when a fact or a rule value it needed was not there…, calculate(), assert_nothing_negative(), basis(), fact() (+50 more)

### Community 71 - "test_grounding_index.py"
Cohesion: 0.10
Nodes (37): CaptureFixture, index_pack(), IndexReport, date, Path, Upsert this pack's sources and stage the values a changed one prints. A pack…, What one call to `index_pack` did, so a script can say it in a line per pack., ExtractedValue (+29 more)

### Community 72 - "preview.tsx"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 73 - "scope_passages"
Cohesion: 0.17
Nodes (17): Any, Keep the owner's passages and the household's; set aside everybody else's. A…, Keep the passages of these people and of the household; set aside everybody…, scope_passages(), scope_to(), _conn_returning(), _passage(), The third bucket. Home contents, a utility bill — nobody's name on it,… (+9 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (17): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+9 more)

### Community 75 - "FakeCursor"
Cohesion: 0.14
Nodes (17): Measurement, by_subject(), db(), FakeCursor, load_register(), Any, date, fixture (+9 more)

### Community 76 - "chat/route.ts"
Cohesion: 0.23
Nodes (12): ai, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns(), readEvents() (+4 more)

### Community 77 - "Notion"
Cohesion: 0.29
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "test_answer_graph.py"
Cohesion: 0.11
Nodes (51): AnswerGraph, Declined, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed…, A request for a recommendation or a judgement, declined before anything is…, Built once, asked many times. Holds no connection: retrieval does., Reading, test_advice_is_declined_when_the_graph_was_given_no_adviser(), build() (+43 more)

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

### Community 84 - "answer.py"
Cohesion: 0.04
Nodes (59): Abstained, answer_system(), _as_sentence(), _asked(), _citations(), ConsentRequired, _conversation(), _distinct() (+51 more)

### Community 85 - "ConfigurationError"
Cohesion: 0.10
Nodes (26): _chat_ids(), ConfigurationError, _flag(), _folder(), local_url(), _port(), _positive(), Path (+18 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "knowledge.py"
Cohesion: 0.12
Nodes (27): Categories, Category, A kind of document a household holds, recognised by words printed in its name.…, Asked, categories_asked(), categorise(), glossary(), _make_replacer() (+19 more)

### Community 89 - "power-menu.tsx"
Cohesion: 0.08
Nodes (24): lucide-react, react, dynamic, runtime, LockButton(), SURFACES, TabBar(), Tabs() (+16 more)

### Community 90 - "lock.ts"
Cohesion: 0.13
Nodes (28): dynamic, GET(), grant(), POST(), runtime, dynamic, metadata, runtime (+20 more)

### Community 91 - "main.py"
Cohesion: 0.14
Nodes (22): The local API. Liveness is intentionally separate from assistant readiness.…, AsyncClient, asyncio, capture_check(), Check, collect_checks(), database_check(), interface_check() (+14 more)

### Community 92 - "FakeCursor"
Cohesion: 0.18
Nodes (3): FakeCursor, Any, FakeConn

### Community 93 - "events"
Cohesion: 0.09
Nodes (19): events(), passage(), Any, Exception, The same scripted reply, in five-character pieces. Deliberately chopped: every…, Not yielded and then withdrawn — never yielded. There is no retraction event by…, The floor is a retrieval question, so it is asked first. The scripted answer is…, A sentence that passed the gate was true when it passed. Losing the connection… (+11 more)

### Community 94 - "DatabaseUnavailable"
Cohesion: 0.07
Nodes (37): FolderSettings, Dispatcher, Inline, Protocol, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Send (+29 more)

### Community 102 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "Settings"
Cohesion: 0.13
Nodes (50): Settings, client_for(), FakeConn, inbox(), Path, The point of the endpoint. An UPDATE alone loses the example we are trying to…, No new column: `already_said` is what makes the row quiet, and it reads this…, A client whose database is `conn`. `base_url` is loopback because… (+42 more)

### Community 104 - "routes.py"
Cohesion: 0.10
Nodes (41): AbstentionEvent, CloseRequest, ConfirmNameRequest, CorrectionRequest, DeclinedEvent, EnabledRequest, FinishedEvent, OwnerRequest (+33 more)

### Community 105 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 106 - "test_telegram_capture.py"
Cohesion: 0.11
Nodes (33): TelegramSettings, MockTransport, build(), FakeRegistrar, FakeTelegram, photo_update(), Any, Path (+25 more)

### Community 107 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 108 - "ScriptedOllama"
Cohesion: 0.08
Nodes (52): AdviceCard, AdviceWithheld, Finished, One sentence that has passed the gate, with the citations it passed on. It will…, Everything that is only knowable once the last sentence is in. `quarantined`…, Advice could not be worked out, and `missing` says what it needs, in the pack's…, A worked result, every word of it written by code, given before the model says…, Sentence (+44 more)

### Community 109 - ".load"
Cohesion: 0.09
Nodes (38): create_app(), checks(), ready(), setup(), system_status(), ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one…, FastAPI (+30 more)

### Community 110 - "vault.py"
Cohesion: 0.07
Nodes (38): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+30 more)

### Community 111 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 112 - "Passage"
Cohesion: 0.07
Nodes (54): check(), check_advice(), check_content(), check_one(), Claim, _normal(), The grounding gate. Rule 3 in AGENTS.md: no claim without a citation. This…, Never raises, never rewrites a claim. It keeps, drops, or abstains. The whole-… (+46 more)

### Community 113 - "test_grounding_values.py"
Cohesion: 0.16
Nodes (33): LogCaptureFixture, _dropped(), _log_values(), Decimal, fixture, parametrize, Published values: the model reads a source, and code keeps only what the…, Assert a value was dropped, and logged with this reason. (+25 more)

### Community 114 - "household.py"
Cohesion: 0.09
Nodes (46): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+38 more)

### Community 115 - "SourceText"
Cohesion: 0.14
Nodes (29): GroundingCorpus, GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records…, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError (+21 more)

### Community 116 - "TelegramAdapter"
Cohesion: 0.11
Nodes (24): BaseTransport, IngestJob, What a capture returns: a registered document, and whether we had seen it…, _attachment(), _pixels(), Any, Client, datetime (+16 more)

### Community 117 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 118 - "test_lifecycle.py"
Cohesion: 0.13
Nodes (26): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor.…, What the person asked for, once. The first request wins; later ones change…, _client(), _eventually(), _launcher(), parametrize, Path (+18 more)

### Community 120 - "app/layout.tsx"
Cohesion: 0.22
Nodes (7): next-themes, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 121 - "pack"
Cohesion: 0.23
Nodes (13): holdings(), Any, Rows of `INVENTORY`, one holding per document that prints the field its pack's…, pack(), insurance(), iras(), fixture, UUID (+5 more)

### Community 122 - "test_contracts.py"
Cohesion: 0.05
Nodes (75): PackManifest, A domain pack, authored as one YAML file., Why this pack cannot supply `field` from every one of `doc_types`, or None if…, An advice shape that names a missing role, field, category or key fails at load…, A compared field no document type of the shape declares can never be printed.…, check_advice_links(), Every fact an advice shape reads from another pack is declared by an installed…, model_validator (+67 more)

### Community 123 - "SentenceScanner"
Cohesion: 0.09
Nodes (29): Any, Pulling finished sentences out of a JSON reply that is still being written. The…, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner (+21 more)

### Community 124 - "reminder/__init__.py"
Cohesion: 0.11
Nodes (20): already_said(), Due, next_window(), Overdue, Any, date, datetime, LookupError (+12 more)

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
Cohesion: 0.22
Nodes (21): FolderAdapter, Satisfies `CaptureAdapter`. Holds no database handle — it is given a…, FakeRegistrar, datetime, fixture, Path, The watched folder: debounce, mime sniffing, and what happens the second time.…, Poll until the stability window has passed and something comes out. (+13 more)

### Community 129 - "extract_values"
Cohesion: 0.19
Nodes (18): extract_values(), Every value the source prints for these keys, kept only when its passage prints…, _long_text(), Any, Exception, Returns the replies the test wrote, in order, then an empty list of values. A…, A truncated or non-JSON reply is an outage: the section was never actually…, Unlike a garbled reply, valid JSON with the wrong shape means the model… (+10 more)

### Community 130 - "Any"
Cohesion: 0.11
Nodes (19): advised_pack(), db(), _document(), FakeConn, FakeCursor, Any, date, datetime (+11 more)

### Community 131 - "_as_module_summary"
Cohesion: 0.20
Nodes (10): ModuleSummary, PacksResponse, PackSummary, _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack() (+2 more)

### Community 132 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 133 - "scope.py"
Cohesion: 0.12
Nodes (21): _decide(), _Decision, HouseholdScope, is_first_person(), named_in(), _names(), Whose question is this, and whose documents may answer it. "What is my term…, `(word, relation)` when the question asks about a relation's own documents,… (+13 more)

### Community 134 - "document-detail.tsx"
Cohesion: 0.08
Nodes (29): DocumentPage(), dynamic, metadata, runtime, RELATION_CHOICES, Place, PLACES, DocumentDetail() (+21 more)

### Community 136 - "today/page.tsx"
Cohesion: 0.08
Nodes (25): dynamic, HouseholdPage(), metadata, runtime, AppLayout(), dynamic, isUrgent(), metadata (+17 more)

### Community 137 - "values.py"
Cohesion: 0.07
Nodes (33): _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), number_tokens(), _pack(), parse_value() (+25 more)

### Community 138 - "test_api.py"
Cohesion: 0.09
Nodes (41): Answer, Cited, One sentence and the passages it was traced to. What rule 3 looks like as data.…, Answered. Asking for consent and naming what is missing are endings, not…, client(), conn(), FakeGraph, graph() (+33 more)

### Community 139 - "FactRow"
Cohesion: 0.11
Nodes (23): fact_row(), FactRow, facts_for(), in_category(), _is_an_adviser(), ModuleAdviser, names_for(), _newest() (+15 more)

### Community 140 - "test_advice_core.py"
Cohesion: 0.06
Nodes (49): Channel, ConsentStatus, current(), grant(), HouseholdConsents, _latest(), NoOwner, Any (+41 more)

### Community 141 - "StreamingGraph"
Cohesion: 0.13
Nodes (19): Citation, A passage, named the way a person cites it and identified the way a link needs.…, a_citation(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive…, No `reading` before it: the floor is checked before the model is asked anything., By then the 200 has been sent. An exception that only logged would leave a… (+11 more)

### Community 142 - "contracts.py"
Cohesion: 0.12
Nodes (24): Advice, Answering, Exclusions, FactInput, FieldSpec, Grounding, Guardrails, ModuleTrigger (+16 more)

### Community 143 - "._claim"
Cohesion: 0.17
Nodes (11): Claim, _advice_basis(), Any, Every removable passage mention, removed. One removal can expose the next — in…, Everything an advised answer rested on, so it can be reconstructed from its…, One streamed sentence object, turned into the thing the gate understands. The…, _without_one_round_of_passage_numbers(), _without_passage_numbers() (+3 more)

### Community 144 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 145 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents

### Community 146 - "main"
Cohesion: 0.15
Nodes (21): approve(), pending(), PendingValue, Any, date, A person's approval, standing between a model's extraction and any calculator…, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it. (+13 more)

### Community 147 - "Domain packs — start here"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 149 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 150 - "build"
Cohesion: 0.15
Nodes (17): build(), Any, The one Celery application, built from `Settings`. Every setting here is a…, Construct the Celery application. Imported lazily by callers so that nothing…, beat_schedule(), cron_expressions(), crontab_from(), manifest() (+9 more)

### Community 151 - "test_ingest_pipeline.py"
Cohesion: 0.06
Nodes (55): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, One flat list of chunks, ordinal running across the whole document., The page as `(is_heading, line)`, from the parser's structure when it has any. (+47 more)

### Community 152 - "Any"
Cohesion: 0.10
Nodes (18): document_row(), fact_row(), FakeCursor, filed_document(), open_obligation(), pack_row(), Any, date (+10 more)

### Community 153 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "adr/README.md"
Cohesion: 0.06
Nodes (28): 1. Record architecture decisions, Consequences, Context, Decision, 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision (+20 more)

### Community 155 - "test_today_is_ordered_overdue_then_alerts_then_reminders"
Cohesion: 0.22
Nodes (10): obligation(), overdue_row(), One row of `reminder.OVERDUE`, in its column order., The Celery beat never goes through the API, so the filter cannot live there., A date that has passed is the one somebody most wants to check against the…, test_a_disabled_pack_does_not_reach_the_nightly_sweep(), test_a_disabled_pack_stops_its_reminders(), test_an_overdue_citation_carries_its_page() (+2 more)

### Community 156 - "package.json"
Cohesion: 0.11
Nodes (16): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+8 more)

### Community 157 - "_today_items"
Cohesion: 0.15
Nodes (18): A document and a page, as a person would cite it., Source, TodayItem, _as_source(), _cite(), connection(), _link(), Any (+10 more)

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

### Community 163 - "Scoped"
Cohesion: 0.20
Nodes (8): The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting…, Scoped, apply(), apply(), apply(), `empty_for_owner` must never fire on a question that was never scoped —…, test_an_unscoped_result_is_not_empty_for_the_owner()

### Community 164 - "Cursor"
Cohesion: 0.25
Nodes (4): Cursor, Any, Protocol, cursor()

### Community 165 - "Alert"
Cohesion: 0.25
Nodes (5): Alert, What the debounce is keyed on: this metric, for this person and thing, in this…, Two lapsed policies on one person are two alerts, and saying one must not…, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

### Community 166 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 167 - "install_best_effort"
Cohesion: 0.16
Nodes (17): lifespan(), install_best_effort(), Installed, What `install` did, so a startup line can say it in one sentence., Install at startup without being able to stop startup. Both processes that own…, _beat_needs_its_own_process(), celery_argv(), main() (+9 more)

### Community 168 - "CaptureAdapter"
Cohesion: 0.29
Nodes (5): CaptureAdapter, datetime, Protocol, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., Capture adapters. Every channel a document can arrive through satisfies one…

### Community 169 - "packs.py"
Cohesion: 0.12
Nodes (20): DocumentTypeSpec, One kind of document this pack recognises., Classification, classify(), _prompt(), Decide which pack's document type a captured document is, or decline to. The…, Never raises. An unavailable model is a classification failure, so it…, _schema() (+12 more)

### Community 170 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 171 - "igd-capstone-2026"
Cohesion: 0.20
Nodes (10): Authoring a pack, igd-capstone-2026, `main` is not protected, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live (+2 more)

### Community 172 - "manifest"
Cohesion: 0.33
Nodes (6): manifest(), ModuleUnavailable, RuntimeError, A module's YAML is missing, or does not validate against `ModuleManifest`., One module's manifest, validated. Raises rather than returning a partial object., test_the_advice_module_manifest_loads()

### Community 173 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

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

### Community 181 - "_ordered"
Cohesion: 0.33
Nodes (6): _Value, Hashable, _order_key(), _ordered(), One sortable key for a number, a date or a word, so a ranking never compares…, Keys ranked by value in the stated order, ties broken by name so a ranking is…

### Community 182 - "installed_packs"
Cohesion: 0.29
Nodes (7): installed_packs(), Every pack directory holding a pack.yaml, in a stable order. Directories whose…, test_every_installed_pack_still_loads(), test_every_document_type_has_a_generated_model(), test_the_template_directory_is_not_an_installed_pack(), A pack naming a metric nobody implemented is a silent no-op, so it is caught…, test_the_real_packs_declare_metrics_that_exist()

### Community 184 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

### Community 187 - "14 · A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.33
Nodes (6): 14 · A pack supplies what the core knows about a domain, and the core stays generic, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 188 - "16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.33
Nodes (6): 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 190 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 191 - "_as_response"
Cohesion: 0.12
Nodes (16): AskRequest, AskResponse, Claim, ErrorEvent, The stream broke after it began. A client cannot read an HTTP status by then., One sentence and the passages it was traced to. Never emitted without…, _as_response(), ask() (+8 more)

### Community 194 - "5. The watched folder is polled for stability, not subscribed to for events"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 196 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 198 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 201 - "eslint.config.mjs"
Cohesion: 0.50
Nodes (3): @eslint/eslintrc, compat, eslintConfig

### Community 208 - "next"
Cohesion: 0.18
Nodes (6): @ai-sdk/react, next, metadata, Conversation(), SUGGESTIONS, nextConfig

## Knowledge Gaps
- **629 isolated node(s):** `npx`, `@modelcontextprotocol/server-filesystem`, `parrot`, `setup.sh script`, `metadata` (+624 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1630 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `run_parrot.py`, `Any`, `build_router`, `Registration`, `test_api.py`, `ingest/quarantine.py`, `StreamingGraph`, `main`, `build`, `Any`, `test_today_is_ordered_overdue_then_alerts_then_reminders`, `_today_items`, `install_best_effort`, `.telegram_configured`, `test_household.py`, `test_modules.py`, `Ollama`, `bench_runtime.py`, `test_startup.py`, `pipeline.py`, `registry.py`, `test_advice_module.py`, `FakeCursor`, `ConfigurationError`, `main.py`, `DatabaseUnavailable`, `routes.py`, `test_telegram_capture.py`, `.load`, `test_lifecycle.py`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `AnswerGraph` connect `test_answer_graph.py` to `Scoped`, `build_router`, `scope.py`, `test_advice_module.py`, `AdviceShape`, `routes.py`, `ModelUnavailable`, `ScriptedOllama`, `._claim`, `Passage`, `answer.py`, `SentenceScanner`, `Ollama`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `Ollama` connect `Ollama` to `run_parrot.py`, `extract_values`, `build_router`, `values.py`, `ingest/quarantine.py`, `ingest/extract.py`, `AdviceShape`, `packs.py`, `extract`, `pipeline.py`, `ModelUnavailable`, `test_grounding_index.py`, `test_answer_graph.py`, `answer.py`, `DatabaseUnavailable`, `Settings`, `routes.py`, `.load`, `SourceText`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 119 inferred relationships involving `Settings` (e.g. with `create_app()` and `build_router()`) actually correct?**
  _`Settings` has 119 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `InstalledPack` (e.g. with `Adviser` and `answer_system()`) actually correct?**
  _`InstalledPack` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ScriptedOllama` (e.g. with `build()` and `Generated`) actually correct?**
  _`ScriptedOllama` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `AnswerGraph` (e.g. with `AdviceShape` and `AdviceLog`) actually correct?**
  _`AnswerGraph` has 19 INFERRED edges - model-reasoned connections that need verification._