# Graph Report - igd-capstone-2026  (2026-09-15)

## Corpus Check
- 272 files · ~637,426 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: (none) 15, .csv 4, .jsonl 3)

## Summary
- 3999 nodes · 9305 edges · 215 communities (186 shown, 22 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 742 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9f321280`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- knowledge.py
- packs/page.tsx
- Christian — task list
- validate
- Ollama
- Project PARROT — team split
- Project PARROT — team split
- register.py
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
- test_grounding_index.py
- FakeConn
- Household canon
- retrieve.py
- build_team_tasks.py
- `core/graph/` — the LangGraph runtime
- `core/ingest/` — the ingestion worker
- Integration review
- Writing an ADR
- `core/retrieve/` — hybrid retrieval
- Graphify — the shared knowledge graph
- test_modules.py
- `api/` — the FastAPI application
- The corpus
- Artefacts
- Why the prototype is evaluated on synthetic data
- `core/adapters/` — capture adapters
- sets/README.md
- Project skills
- Evaluation
- pull_request_template.md
- harness.py
- tokens/page.tsx
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
- AdviceRecord
- ConfigurationError
- test_pages.py
- test_ingest_pipeline.py
- bench_runtime.py
- compilerOptions
- export-design-preview.cjs
- test_startup.py
- pipeline.py
- registry.py
- ModelUnavailable
- test_advice_module.py
- FakeCursor
- preview.tsx
- _decide
- Starting Parrot
- Any
- main
- Notion
- test_answer_graph.py
- The demonstration run sheet
- PaperBrain
- Contributing
- ingest/extract.py
- components.json
- run_parrot.py
- [...path]/route.ts
- Architecture
- Roadmap
- State
- (app)/layout.tsx
- lock.ts
- main.py
- FakeConn
- build
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
- HouseholdConsents
- test_gate.py
- test_grounding_values.py
- household.py
- SourceText
- TelegramAdapter
- HouseholdScope
- test_lifecycle.py
- worker/__init__.py
- app/layout.tsx
- chat/route.ts
- test_contracts.py
- SentenceScanner
- reminder/__init__.py
- Household canon
- answer.tsx
- scripts/ask.py
- FolderAdapter
- Scoped
- Any
- folder.py
- 10. `main` is unprotected, and the discipline is human
- date
- api.ts
- today/page.tsx
- values.py
- test_api.py
- InstalledPack
- sweep
- StreamingGraph
- gate.py
- ParsedPage
- devDependencies
- Working agreement for coding agents
- main
- FakeCursor
- Desmond — Lane E · Corpus and adversarial testing
- schedule.py
- next
- Any
- 2. One PostgreSQL instance for everything
- adr/README.md
- owner
- package.json
- _today_items
- postcss.config.mjs
- 4. Writing `pack.yaml`
- 13. A question is understood before it is searched, and scoped before it is cut
- Try PARROT
- github.md
- Cursor
- test_eval_harness.py
- packs.py
- Notebook prompts — the four full policies for Marcus Lim
- application
- test_advice_core.py
- FakeCursor
- First run
- igd-capstone-2026
- ports.py
- _as_module_summary
- Zee — Lane D · Domain packs and interface
- Authoring a domain pack
- Christian — Lane A · Integration and product owner
- Siew — Lane C · Governance and assurance
- FakeCursor
- dependencies
- Alert
- quiet_engine
- contracts.py
- create_app
- Yew Mun — Lane B · Retrieval and evaluation
- FakeTelegram
- Calculation
- 14 · A pack supplies what the core knows about a domain, and the core stays generic
- 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent
- F1
- The team
- ErrorEvent
- inventory.py
- 1. Record architecture decisions
- Figure
- FolderCapture
- Notice
- 6. pypdfium2 renders the page images the quarantine second pass reads
- 7. The answer graph ships before hybrid retrieval and before a checkpoint table
- installed_packs
- routes.py
- manifest
- __init__.py
- README.md
- .telegram_configured
- sets_io.py
- RagasJudge
- Due
- scripts
- usable
- eslint.config.mjs
- .cite
- .ref
- answer.py
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

## Communities (215 total, 22 thin omitted)

### Community 0 - "knowledge.py"
Cohesion: 0.12
Nodes (27): Categories, Asked, categories_asked(), categorise(), glossary(), _make_replacer(), mentions(), _pattern() (+19 more)

### Community 1 - "packs/page.tsx"
Cohesion: 0.08
Nodes (19): dynamic, metadata, PacksPage(), runtime, dynamic, metadata, runtime, Toggle() (+11 more)

### Community 2 - "Christian — task list"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.09
Nodes (41): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+33 more)

### Community 4 - "Ollama"
Cohesion: 0.06
Nodes (78): blocked_reasons(), forget(), Any, Path, ValueError, QuarantinedDocument, queue(), The second stage of quarantine: the page image, read by the vision-language… (+70 more)

### Community 5 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 6 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 7 - "register.py"
Cohesion: 0.14
Nodes (19): CaptureAdapter, datetime, Protocol, The one interface every capture channel satisfies. receive(payload, mime,…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., Capture adapters. Every channel a document can arrive through satisfies one…, Register a document, idempotently, on a SHA-256 of the source bytes. This is…, Insert or update the `documents` row for these bytes and say which happened.… (+11 more)

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
Cohesion: 0.08
Nodes (41): _as_date(), _as_number(), cites(), _contains(), doc_stem(), grade(), held_back(), Judge (+33 more)

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
Cohesion: 0.06
Nodes (53): The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, sha256(), Dispatcher, Inline, Any, Protocol, Queued, What happens to a document between "these bytes are registered" and "this… (+45 more)

### Community 18 - "test_grounding_index.py"
Cohesion: 0.10
Nodes (37): CaptureFixture, index_pack(), IndexReport, date, Path, Upsert this pack's sources and stage the values a changed one prints. A pack…, What one call to `index_pack` did, so a script can say it in a line per pack., ExtractedValue (+29 more)

### Community 19 - "FakeConn"
Cohesion: 0.12
Nodes (19): FakeConn, obligation(), overdue_row(), One row of `reminder.OVERDUE`, in its column order., The nightly sweep owns `last_notified_at`. A screen refresh must not burn a…, A registry that failed to install must fail loudly, not silently silence the…, `hides its facts` reaches an answer through retrieval, not through the API., The Celery beat never goes through the API, so the filter cannot live there. (+11 more)

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

### Community 29 - "test_modules.py"
Cohesion: 0.22
Nodes (18): Everything inside a lead window that has not already been said for that window.…, sweep(), FakeConn, obligation_row(), datetime, Reminder and Alert: what fires, once, and with what behind it. Both modules are…, A sweep for a date in the future must record that date, or it repeats itself., A live travel policy must not make a lapsed motor policy read as covered. (+10 more)

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

### Community 39 - "harness.py"
Cohesion: 0.09
Nodes (22): Asks, build(), Any, Protocol, Ask PARROT the golden questions the way `scripts/ask.py` does, and keep what it…, The graph `scripts/ask.py` builds, with the recorder in the seam. Kept in step…, The one method of `AnswerGraph` the harness uses. A test supplies a fake., Counts candidates. What the model read is recorded by the reranker, which runs… (+14 more)

### Community 40 - "tokens/page.tsx"
Cohesion: 0.11
Nodes (10): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+2 more)

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
Cohesion: 0.08
Nodes (70): Input, One fact or rule value a calculation was built on, carrying its own citation.…, _Value, Hashable, _ambiguous(), _amount(), _band(), _band_label() (+62 more)

### Community 58 - "cli.py"
Cohesion: 0.16
Nodes (22): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+14 more)

### Community 59 - "AdviceRecord"
Cohesion: 0.25
Nodes (7): HouseholdAdviceLog, The record of every advised or withheld answer (ADR 0016). `advice_records`…, `core.graph.advice.AdviceLog` over a live connection. `basis` is dumped with…, AdviceRecord, Every advised or withheld answer's full basis, so it can be reconstructed later…, test_record_insert_includes_the_sha256_of_the_disclaimer(), Log

### Community 60 - "ConfigurationError"
Cohesion: 0.11
Nodes (24): _chat_ids(), ConfigurationError, _flag(), _folder(), local_url(), _port(), _positive(), Path (+16 more)

### Community 61 - "test_pages.py"
Cohesion: 0.09
Nodes (37): page_images(), Base64 page images, in page order. Empty when this document cannot be rendered.…, page_count(), PageUnavailable, _pdfium(), Any, LookupError, RuntimeError (+29 more)

### Community 62 - "test_ingest_pipeline.py"
Cohesion: 0.10
Nodes (43): extract(), Never raises. A failure is a reason, and a reason routes the document to…, pack(), Generated, FakeOllama, insurance(), iras(), _page_of_examples() (+35 more)

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
Cohesion: 0.06
Nodes (40): Chunk, What is actually embedded: the prefix plus the text, matching the tsvector…, The ingestion worker. Capture registers a document; this package turns it into…, fixed(), from_facts(), _label(), Any, date (+32 more)

### Community 68 - "registry.py"
Cohesion: 0.11
Nodes (30): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders…, installed_modules(), InstalledModule, Load the installed capability modules at runtime. The mirror of…, Every module directory holding a `module.yaml`, in a stable order. Directories…, enabled_module_ids(), install() (+22 more)

### Community 69 - "ModelUnavailable"
Cohesion: 0.08
Nodes (19): The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), ModelUnavailable, Any, Client, RuntimeError, A question, embedded the way the model was trained to embed a search query. (+11 more)

### Community 70 - "test_advice_module.py"
Cohesion: 0.14
Nodes (55): Missing, What a calculator returns when a fact or a rule value it needed was not there…, FactRow, calculate(), assert_nothing_negative(), basis(), fact(), figures_of() (+47 more)

### Community 71 - "FakeCursor"
Cohesion: 0.18
Nodes (3): FakeCursor, Any, FakeConn

### Community 72 - "preview.tsx"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 73 - "_decide"
Cohesion: 0.12
Nodes (19): _decide(), _Decision, is_first_person(), named_in(), _names(), Any, `(word, relation)` when the question asks about a relation's own documents,…, Whether this question is about the person asking. `other_names` are the display… (+11 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (17): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+9 more)

### Community 75 - "Any"
Cohesion: 0.14
Nodes (17): Measurement, by_subject(), db(), FakeCursor, load_register(), Any, date, fixture (+9 more)

### Community 76 - "main"
Cohesion: 0.14
Nodes (24): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), main(), _note() (+16 more)

### Community 77 - "Notion"
Cohesion: 0.29
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "test_answer_graph.py"
Cohesion: 0.11
Nodes (52): AnswerGraph, Finished, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed…, One sentence that has passed the gate, with the citations it passed on. It will…, Everything that is only knowable once the last sentence is in. `quarantined`…, Built once, asked many times. Holds no connection: retrieval does., Reading, Sentence (+44 more)

### Community 79 - "The demonstration run sheet"
Cohesion: 0.14
Nodes (14): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+6 more)

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (7): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Contributing"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 82 - "ingest/extract.py"
Cohesion: 0.10
Nodes (29): _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact, Extraction, find_page(), _normalise() (+21 more)

### Community 83 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 84 - "run_parrot.py"
Cohesion: 0.11
Nodes (26): broker_available(), Whether Redis answers. Not whether a worker is listening —…, _kill_tree(), main(), open_browser(), parse_args(), port_answers(), Any (+18 more)

### Community 85 - "[...path]/route.ts"
Cohesion: 0.15
Nodes (17): ALLOWED, Context, DELETE(), dynamic, forward(), GET(), PATCH(), POST() (+9 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "State"
Cohesion: 0.14
Nodes (11): _asked(), _conversation(), fuse(), What the graph carries. It ends at the evidence; the answer is streamed, not…, The question to answer and to scope. A follow-up is the whole question it was…, Several searches as one list: each passage once, at the best score any phrasing…, The question made whole, and said in the documents' words. See…, Every phrasing of the question, searched and fused. The person's own words… (+3 more)

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
Cohesion: 0.11
Nodes (30): Channel, ConsentStatus, current(), grant(), _latest(), NoOwner, Any, RuntimeError (+22 more)

### Community 93 - "build"
Cohesion: 0.07
Nodes (30): build(), events(), passage(), Any, Exception, Generated, parametrize, The same scripted reply, in five-character pieces. Deliberately chopped: every… (+22 more)

### Community 94 - "TelegramCapture"
Cohesion: 0.18
Nodes (7): attribution(), Any, A daemon thread that long-polls the Telegram bot until `stop()` or process…, Begin polling. Returns False, with a logged reason, when it cannot or should…, One long poll. A failure waits rather than hammering the API with the same…, Whose phone this arrived on, recorded before anything is read off it. See ADR…, TelegramCapture

### Community 102 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "Settings"
Cohesion: 0.12
Nodes (45): Settings, client_for(), filed_document(), inbox(), open_obligation(), pack_row(), Path, The point of the endpoint. An UPDATE alone loses the example we are trying to… (+37 more)

### Community 104 - "build_router"
Cohesion: 0.09
Nodes (34): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, What changed, in the words the screen confirms it with. `was` is returned…, The row is gone from Today. `speaks_again` is null when it will not come back.…, 202. The vision pass is slower than a page load, so it is queued and this is… (+26 more)

### Community 105 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 106 - "test_telegram_capture.py"
Cohesion: 0.11
Nodes (35): RuntimeError, Safe to show: never contains the token., TelegramSettings, TelegramUnavailable, build(), FakeRegistrar, photo_update(), Any (+27 more)

### Community 107 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 108 - "ScriptedOllama"
Cohesion: 0.08
Nodes (48): AdviceCard, AdviceWithheld, Declined, A request for a recommendation or a judgement, declined before anything is…, Advice could not be worked out, and `missing` says what it needs, in the pack's…, A worked result, every word of it written by code, given before the model says…, Whose question is this, and whose documents may answer it. "What is my term…, Whose situation a piece of advice is about — `whose`'s answer, with no passages… (+40 more)

### Community 109 - ".load"
Cohesion: 0.10
Nodes (35): ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one…, Load the generator and the embedder before the first question, and record the…, warm_models(), db(), fixture, conn(), fixture (+27 more)

### Community 110 - "vault.py"
Cohesion: 0.07
Nodes (38): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+30 more)

### Community 111 - "HouseholdConsents"
Cohesion: 0.67
Nodes (3): HouseholdConsents, `core.graph.advice.ConsentBook` over a live connection, for the graph to ask…, test_household_consents_implements_the_consent_book_port()

### Community 112 - "test_gate.py"
Cohesion: 0.14
Nodes (29): check_advice(), Claim, Why an advice explanation cannot be kept, or `None`. Asked of a claim built…, test_a_claim_citing_the_same_document_twice_says_it_once(), test_a_grounded_claim_renders_its_document_and_page(), What the gate checks beyond "is there a citation". A cited sentence can still…, `target` and `gap` both print SGD 500,000.00 (`_gap` with `held` at zero).…, The defect this fixes: naming `gap`, the *second* figure in `figures` order to… (+21 more)

### Community 113 - "test_grounding_values.py"
Cohesion: 0.10
Nodes (53): extract_values(), Every value the source prints for these keys, kept only when its passage prints…, LogCaptureFixture, _dropped(), _log_values(), _long_text(), Any, Decimal (+45 more)

### Community 114 - "household.py"
Cohesion: 0.11
Nodes (35): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), pending(), pending_count() (+27 more)

### Community 115 - "SourceText"
Cohesion: 0.15
Nodes (27): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError, Read and validate a pack's grounding corpus from its own folder on disk. A…, A pack's grounding corpus on disk does not match what its `sources.yaml`… (+19 more)

### Community 116 - "TelegramAdapter"
Cohesion: 0.11
Nodes (23): BaseTransport, IngestJob, What a capture returns: a registered document, and whether we had seen it…, _attachment(), _pixels(), Any, Client, datetime (+15 more)

### Community 117 - "HouseholdScope"
Cohesion: 0.18
Nodes (17): HouseholdScope, Keep the owner's passages and the household's; set aside everybody else's. A…, What `AnswerGraph` is handed so it can scope without holding a connection.…, scope_passages(), _conn_returning(), _passage(), Any, The third bucket. Home contents, a utility bill — nobody's name on it,… (+9 more)

### Community 118 - "test_lifecycle.py"
Cohesion: 0.13
Nodes (26): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor.…, What the person asked for, once. The first request wins; later ones change…, _client(), _eventually(), _launcher(), parametrize, Path (+18 more)

### Community 120 - "app/layout.tsx"
Cohesion: 0.22
Nodes (7): next-themes, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 121 - "chat/route.ts"
Cohesion: 0.23
Nodes (12): ai, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns(), readEvents() (+4 more)

### Community 122 - "test_contracts.py"
Cohesion: 0.05
Nodes (76): PackManifest, A domain pack, authored as one YAML file., (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why this pack cannot supply `field` from every one of `doc_types`, or None if…, An advice shape that names a missing role, field, category or key fails at load…, A compared field no document type of the shape declares can never be printed.…, check_advice_links(), Every fact an advice shape reads from another pack is declared by an installed… (+68 more)

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

### Community 127 - "scripts/ask.py"
Cohesion: 0.16
Nodes (13): ask(), _graph_for(), DenseRetriever, NoReranker, A dense-only retriever, so the graph can be run and tested before Lane B's…, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this…, HouseholdInventory, Handed to `AnswerGraph` by whoever holds a connection, as `HouseholdScope` is. (+5 more)

### Community 128 - "FolderAdapter"
Cohesion: 0.22
Nodes (22): FolderAdapter, FolderSettings, Satisfies `CaptureAdapter`. Holds no database handle — it is given a…, FakeRegistrar, datetime, fixture, Path, The watched folder: debounce, mime sniffing, and what happens the second time.… (+14 more)

### Community 129 - "Scoped"
Cohesion: 0.17
Nodes (9): The documents on file, narrowed to the same people the passages were., The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting…, Keep the passages of these people and of the household; set aside everybody…, scope_to(), Scoped, apply(), apply() (+1 more)

### Community 130 - "Any"
Cohesion: 0.12
Nodes (19): advised_pack(), _document(), _facts_tuple(), FakeConn, FakeCursor, Any, date, datetime (+11 more)

### Community 131 - "folder.py"
Cohesion: 0.16
Nodes (12): Magic bytes first, filename suffix second, `application/octet-stream` last. A…, sniff_mime(), _Pending, datetime, Path, The watched-folder capture adapter. A person drops a scan into a folder and it…, Every file in the watched folder that is worth looking at at all., Advance the debounce by `elapsed` seconds and return the files now ready. Time… (+4 more)

### Community 132 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 133 - "date"
Cohesion: 0.23
Nodes (13): document_row(), fact_row(), date, Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with…, A deleted document must not take the sentence down with it., Following a citation must never end in a blank screen because a pack was…, test_a_citation_that_resolves_to_nothing_still_says_what_it_said(), test_a_date_field_takes_an_iso_date_and_says_so_when_it_does_not() (+5 more)

### Community 134 - "api.ts"
Cohesion: 0.08
Nodes (29): DocumentPage(), dynamic, metadata, runtime, RELATION_CHOICES, Place, PLACES, DocumentDetail() (+21 more)

### Community 136 - "today/page.tsx"
Cohesion: 0.08
Nodes (25): dynamic, HouseholdPage(), metadata, runtime, AppLayout(), dynamic, isUrgent(), metadata (+17 more)

### Community 137 - "values.py"
Cohesion: 0.08
Nodes (34): A rule or table value a pack's sources publish. Extracted automatically,…, ValueKey, _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), number_tokens() (+26 more)

### Community 138 - "test_api.py"
Cohesion: 0.08
Nodes (42): Answer, _as_sentence(), Cited, Every event, collected. `scripts/ask.py` and the screen ask the same question…, One sentence and the passages it was traced to. What rule 3 looks like as data.…, Answered. Asking for consent and naming what is missing are endings, not…, "which age band applies" -> "Which age band applies.": a pack's wording and a…, client() (+34 more)

### Community 139 - "InstalledPack"
Cohesion: 0.08
Nodes (32): AdviceShape, One kind of advice question, and everything its calculator needs to answer it., AdviceLog, Adviser, ConsentBook, date, Protocol, What a calculator returns, and what the graph needs to ask consent and keep a… (+24 more)

### Community 140 - "sweep"
Cohesion: 0.30
Nodes (11): AlertConfig, Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), FakePack, One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order., srs_row(), test_a_firing_older_than_the_debounce_window_fires_again(), test_a_metric_no_query_defines_cannot_fire() (+3 more)

### Community 141 - "StreamingGraph"
Cohesion: 0.13
Nodes (20): a_citation(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive…, No `reading` before it: the floor is checked before the model is asked anything., By then the 200 has been sent. An exception that only logged would leave a…, A line about a document on file is not the answer to "does it cover floods?"., What a retrieved passage hands over: the sentence a person reads, and the id a… (+12 more)

### Community 142 - "gate.py"
Cohesion: 0.09
Nodes (23): Exclusions, A sentence claiming cover whose every citation sits under one of `headings` is…, check(), check_one(), _normal(), The grounding gate. Rule 3 in AGENTS.md: no claim without a citation. This…, Never raises, never rewrites a claim. It keeps, drops, or abstains. The whole-…, "1,860.00", "1860" and "01" → "1860", "1860", "1": formatting is not a… (+15 more)

### Community 143 - "ParsedPage"
Cohesion: 0.06
Nodes (42): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, One flat list of chunks, ordinal running across the whole document., The page as `(is_heading, line)`, from the parser's structure when it has any. (+34 more)

### Community 144 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 145 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents

### Community 146 - "main"
Cohesion: 0.15
Nodes (21): approve(), pending(), PendingValue, Any, date, A person's approval, standing between a model's extraction and any calculator…, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it. (+13 more)

### Community 147 - "FakeCursor"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 149 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 150 - "schedule.py"
Cohesion: 0.15
Nodes (17): build(), Any, The one Celery application, built from `Settings`. Every setting here is a…, Construct the Celery application. Imported lazily by callers so that nothing…, beat_schedule(), cron_expressions(), crontab_from(), manifest() (+9 more)

### Community 151 - "next"
Cohesion: 0.18
Nodes (6): @ai-sdk/react, next, metadata, Conversation(), SUGGESTIONS, nextConfig

### Community 152 - "Any"
Cohesion: 0.19
Nodes (3): FakeCursor, Any, The parameters of the one statement containing `needle`. Fails loudly if it…

### Community 153 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "adr/README.md"
Cohesion: 0.05
Nodes (30): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision, 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision (+22 more)

### Community 155 - "owner"
Cohesion: 0.22
Nodes (10): owner(), owner_aliases(), The person asking. `None` before setup has run, which every caller must handle:…, Every confirmed string that means the owner. This is what scopes a first-person…, Hand the household over. The owner is a row, not a value baked in at install.…, set_owner(), A daughter takes over her father's paperwork. The install follows., test_handing_over_to_nobody_is_an_error() (+2 more)

### Community 156 - "package.json"
Cohesion: 0.11
Nodes (16): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+8 more)

### Community 157 - "_today_items"
Cohesion: 0.16
Nodes (17): A document and a page, as a person would cite it., Source, _as_source(), _cite(), connection(), _link(), Any, date (+9 more)

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
Cohesion: 0.17
Nodes (23): The reference answer Ragas judges recall and precision against. A fact…, reference_for(), Expected, load_set(), MalformedQuestion, Any, SetId, ValueError (+15 more)

### Community 165 - "packs.py"
Cohesion: 0.15
Nodes (16): DocumentTypeSpec, One kind of document this pack recognises., Classification, classify(), _prompt(), Decide which pack's document type a captured document is, or decline to. The…, Never raises. An unavailable model is a classification failure, so it…, _schema() (+8 more)

### Community 166 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 167 - "application"
Cohesion: 0.20
Nodes (15): lifespan(), install_best_effort(), Install at startup without being able to stop startup. Both processes that own…, _beat_needs_its_own_process(), celery_argv(), main(), Any, Namespace (+7 more)

### Community 168 - "test_advice_core.py"
Cohesion: 0.25
Nodes (15): _kind_of(), passages_for(), `"fact:12"` -> `"fact"`, `"rule:7"` -> `"rule"`. Anything else is a calculator…, Inputs as kind fact/rule passages (chunk_id from the ref), and the figures as…, check_content(), Why a cited sentence still cannot be kept, or `None`. Asked after `check_one`…, Kind, _calculation() (+7 more)

### Community 169 - "FakeCursor"
Cohesion: 0.20
Nodes (3): FakeCursor, Any, FakeConn

### Community 170 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 171 - "igd-capstone-2026"
Cohesion: 0.20
Nodes (10): Authoring a pack, igd-capstone-2026, `main` is not protected, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live (+2 more)

### Community 172 - "ports.py"
Cohesion: 0.24
Nodes (7): The answer graph. Router, retrieve, rerank, grounding gate, then answer or…, Protocol, What the graph needs from retrieval, stated as a contract rather than an…, Implemented by `core/retrieve/` when Lane B's hybrid search lands. `candidates`…, A cross-encoder, scoring question against passage. Returns the best `keep`,…, Reranker, Retriever

### Community 173 - "_as_module_summary"
Cohesion: 0.20
Nodes (10): ModuleSummary, PacksResponse, PackSummary, _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack() (+2 more)

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

### Community 179 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 180 - "Alert"
Cohesion: 0.25
Nodes (5): Alert, What the debounce is keyed on: this metric, for this person and thing, in this…, Two lapsed policies on one person are two alerts, and saying one must not…, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

### Community 181 - "quiet_engine"
Cohesion: 0.50
Nodes (4): fixture, MonkeyPatch, quiet_engine(), No real probes, no startup writes, no deliberate pause before exiting. The…

### Community 182 - "contracts.py"
Cohesion: 0.13
Nodes (23): Advice, Answering, Category, FactInput, FieldSpec, Grounding, GroundingDocument, Guardrails (+15 more)

### Community 183 - "create_app"
Cohesion: 0.31
Nodes (6): create_app(), checks(), ready(), setup(), system_status(), FastAPI

### Community 184 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

### Community 185 - "FakeTelegram"
Cohesion: 0.25
Nodes (5): MockTransport, FakeTelegram, Request, Response, The four Bot API calls this adapter makes, and a record of what it asked for.

### Community 186 - "Calculation"
Cohesion: 0.24
Nodes (8): Calculation, What a calculator returns when every fact and rule it needed was on file and…, Adviser, date, _dual_cited_calculation(), An input that happens to print the same value as a figure, so the role check…, An input, `fact:12`, that independently prints the same value as the `target`…, _shared_value_calculation()

### Community 187 - "14 · A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.33
Nodes (6): 14 · A pack supplies what the core knows about a domain, and the core stays generic, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 188 - "16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.33
Nodes (6): 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 189 - "F1"
Cohesion: 0.25
Nodes (6): extraction_f1(), F1, FactRow, One row of the `facts` table, as the harness reads it: which document, which…, Field extraction scored against the register, overall and by document type. The…, test_extraction_f1_scores_only_indexed_documents_against_the_register()

### Community 190 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 191 - "ErrorEvent"
Cohesion: 0.22
Nodes (9): AskRequest, ErrorEvent, The stream broke after it began. A client cannot read an HTTP status by then., ask_stream(), events(), _history(), The conversation so far, as the graph reads it. Empty for a first question., One event, in the wire format. `kind` is on the payload, so no `event:` line is… (+1 more)

### Community 192 - "inventory.py"
Cohesion: 0.24
Nodes (10): holdings(), Any, The documents on file, read from `facts` rather than searched for. "Do I have…, Rows of `INVENTORY`, one holding per document that prints the field its pack's…, UUID, Holdings come from `facts`, one per document that prints the name the…, row(), test_a_pack_that_declares_no_categories_holds_nothing() (+2 more)

### Community 193 - "1. Record architecture decisions"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 194 - "Figure"
Cohesion: 0.29
Nodes (7): Figure, One number a calculator produced, and the words a sentence must use to state…, _advice_calculation(), _gap_shared_value_calculation(), _meets_calculation(), A `meets` outcome: the gap figure is negative, and only its printed text…, `_gap`'s real figure construction order — target, held, gap — with `held` at…

### Community 195 - "FolderCapture"
Cohesion: 0.29
Nodes (3): FolderCapture, Begin watching. Returns False, with a logged reason, when it cannot., A daemon thread that polls the watched folder until `stop()` or process exit.

### Community 196 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 197 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 198 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 199 - "installed_packs"
Cohesion: 0.29
Nodes (7): installed_packs(), Every pack directory holding a pack.yaml, in a stable order. Directories whose…, test_every_installed_pack_still_loads(), test_every_document_type_has_a_generated_model(), test_the_template_directory_is_not_an_installed_pack(), A pack naming a metric nobody implemented is a silent no-op, so it is caught…, test_the_real_packs_declare_metrics_that_exist()

### Community 200 - "routes.py"
Cohesion: 0.09
Nodes (48): AbstentionEvent, AskResponse, Claim, CloseRequest, ConfirmNameRequest, CorrectionRequest, DeclinedEvent, EnabledRequest (+40 more)

### Community 201 - "manifest"
Cohesion: 0.33
Nodes (6): manifest(), ModuleUnavailable, RuntimeError, A module's YAML is missing, or does not validate against `ModuleManifest`., One module's manifest, validated. Raises rather than returning a partial object., test_the_advice_module_manifest_loads()

### Community 205 - "sets_io.py"
Cohesion: 0.10
Nodes (33): choose(), Generated, generic(), main(), _named(), phrase(), on_file(), pool() (+25 more)

### Community 206 - "RagasJudge"
Cohesion: 0.32
Nodes (6): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts(), Ragas 0.4 metrics through Ollama's OpenAI-compatible endpoint. Imported lazily…

### Community 208 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 210 - "eslint.config.mjs"
Cohesion: 0.50
Nodes (3): @eslint/eslintrc, compat, eslintConfig

### Community 215 - "answer.py"
Cohesion: 0.06
Nodes (42): Claim, Abstained, _advice_basis(), _advice_prompt(), answer_system(), Citation, _citations(), ConsentRequired (+34 more)

## Knowledge Gaps
- **630 isolated node(s):** `npx`, `@modelcontextprotocol/server-filesystem`, `_Formatter`, `parrot`, `setup.sh script` (+625 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1696 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `Ollama`, `date`, `register.py`, `test_api.py`, `StreamingGraph`, `test_worker_queue.py`, `main`, `FakeConn`, `schedule.py`, `_today_items`, `test_modules.py`, `application`, `harness.py`, `create_app`, `test_household.py`, `ConfigurationError`, `bench_runtime.py`, `test_startup.py`, `FolderCapture`, `registry.py`, `test_advice_module.py`, `routes.py`, `Any`, `.telegram_configured`, `main`, `run_parrot.py`, `main.py`, `TelegramCapture`, `build_router`, `test_telegram_capture.py`, `.load`, `test_lifecycle.py`, `scripts/ask.py`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `AnswerGraph` connect `test_answer_graph.py` to `Scoped`, `Ollama`, `test_api.py`, `InstalledPack`, `harness.py`, `ports.py`, `Calculation`, `AdviceRecord`, `ModelUnavailable`, `routes.py`, `answer.py`, `State`, `build`, `build_router`, `ScriptedOllama`, `test_gate.py`, `HouseholdScope`, `SentenceScanner`, `scripts/ask.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `Ollama` connect `Ollama` to `values.py`, `InstalledPack`, `test_worker_queue.py`, `test_grounding_index.py`, `packs.py`, `harness.py`, `test_ingest_pipeline.py`, `pipeline.py`, `ModelUnavailable`, `routes.py`, `main`, `test_answer_graph.py`, `ingest/extract.py`, `run_parrot.py`, `answer.py`, `Settings`, `build_router`, `.load`, `test_grounding_values.py`, `SourceText`, `scripts/ask.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 121 inferred relationships involving `Settings` (e.g. with `create_app()` and `build_router()`) actually correct?**
  _`Settings` has 121 INFERRED edges - model-reasoned connections that need verification._
- **Are the 37 inferred relationships involving `Passage` (e.g. with `_advice_prompt()` and `AnswerGraph`) actually correct?**
  _`Passage` has 37 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `InstalledPack` (e.g. with `Adviser` and `answer_system()`) actually correct?**
  _`InstalledPack` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `AnswerGraph` (e.g. with `AdviceShape` and `AdviceLog`) actually correct?**
  _`AnswerGraph` has 19 INFERRED edges - model-reasoned connections that need verification._