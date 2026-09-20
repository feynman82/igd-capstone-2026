# Graph Report - igd-capstone-2026  (2026-09-20)

## Corpus Check
- 0 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3843 nodes · 8034 edges · 239 communities (211 shown, 28 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 777 edges (avg confidence: 0.74)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c15d3959`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- pack
- packs/page.tsx
- Christian — task list
- validate
- Ollama
- Project PARROT — team split
- Project PARROT — team split
- sha256
- Running the evaluation harness
- support.js
- Desmond — task list
- Zee — task list
- test_api.py
- answer.tsx
- Filling the corpus register
- Writing a governance artefact
- Claude Code — read this first
- test_worker_queue.py
- test_grounding_index.py
- obligation
- Household canon
- get
- build_team_tasks.py
- `core/graph/` — the LangGraph runtime
- `core/ingest/` — the ingestion worker
- Integration review
- Writing an ADR
- test_startup.py
- Graphify — the shared knowledge graph
- test_modules.py
- `api/` — the FastAPI application
- The corpus
- Artefacts
- Why the prototype is evaluated on synthetic data
- `core/adapters/` — capture adapters
- sets/README.md
- Project skills
- ValueRow
- pull_request_template.md
- InstalledPack
- HouseholdConsents
- Changelog
- filesystem
- `docs/governance/` — the assurance artefacts
- corpus/__init__.py
- packs/__init__.py
- events
- add_person
- The household, and the word "my"
- owner
- alert/__init__.py
- Basic Financial Planning Guide
- test_household.py
- advice/__init__.py
- cli.py
- client_for
- load_corpus.py
- test_pages.py
- test_ingest_pipeline.py
- bench_runtime.py
- compilerOptions
- export-design-preview.cjs
- run_parrot.py
- ModelUnavailable
- registry.py
- Generated
- test_advice_module.py
- FakeCursor
- preview.tsx
- scope.py
- Starting Parrot
- load_register
- Screens
- Notion
- test_answer_graph.py
- The demonstration run sheet
- PaperBrain
- Contributing
- ingest/extract.py
- components.json
- .understand
- [...path]/route.ts
- Architecture
- Roadmap
- document-detail.tsx
- tokens/page.tsx
- lock.ts
- create_app
- FakeConn
- ._build
- FolderCapture
- Home Contents Insurance Policy
- api/__init__.py
- core/__init__.py
- runtime/__init__.py
- modules/__init__.py
- setup.sh
- 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module
- FakeConn
- ForgottenDocument
- DocumentCatalog
- test_telegram_capture.py
- Siew — task list
- ScriptedOllama
- test_runtime.py
- vault.py
- Registration
- Claim
- test_grounding_values.py
- household.py
- GroundingCorpus
- TelegramAdapter
- scope_passages
- test_lifecycle.py
- worker/__init__.py
- app/layout.tsx
- boot
- PackManifest
- SentenceScanner
- reminder/__init__.py
- Household canon
- item-row.tsx
- ErrorEvent
- FolderAdapter
- ._compares_what_its_documents_declare
- FakeConn
- createExternalModules
- 10. `main` is unprotected, and the discipline is human
- Passage
- api.ts
- team/README.md
- today/page.tsx
- values.py
- Answer
- FactRow
- test_reindexing_replaces_chunks_and_leaves_facts_alone
- StreamingGraph
- packs.py
- ingest/quarantine.py
- devDependencies
- Comparison of Integrated Shield Plans
- main
- Domain packs — start here
- app/page.tsx
- Desmond — Lane E · Corpus and adversarial testing
- schedule.py
- FakeConn
- test_one_document_is_shown_even_when_its_pack_is_off
- 2. One PostgreSQL instance for everything
- NNNN · The decision, as a statement not a question
- .retrieve
- package.json
- Source
- postcss.config.mjs
- 4. Writing `pack.yaml`
- 12. Chunks follow the document's headings, and embeddings use the model's task prompts
- Try PARROT
- github.md
- Understanding health insurance
- ParsedPage
- Notebook prompts — the four full policies for Marcus Lim
- install_best_effort
- _Value
- test_advice_core.py
- First run
- igd-capstone-2026
- 0001_init.sql
- quarantine.tsx
- Zee — Lane D · Domain packs and interface
- Authoring a domain pack
- Christian — Lane A · Integration and product owner
- Siew — Lane C · Governance and assurance
- dependencies
- Alert
- MediShield Life Benefits
- contracts.py
- Understanding integrated shield plans
- Yew Mun — Lane B · Retrieval and evaluation
- test_a_citation_that_resolves_to_nothing_still_says_what_it_said
- About Integrated Shield Plan
- Premium and Subsidy Tables
- 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent
- ReadingEvent
- 0002_household.sql
- 0003_advice.sql
- 1. Record architecture decisions
- Notice
- 6. pypdfium2 renders the page images the quarantine second pass reads
- installed_packs
- models.py
- grounding/__init__.py
- grounding/README.md
- Claim
- 4. Local setup can run before the household assistant is ready
- scripts
- Data inventory — identity data, dates of birth and loans
- eslint.config.mjs
- 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack
- generate_lim_documents.py
- usable
- 5. The watched folder is polled for stability, not subscribed to for events
- AdviceConsent
- _meets_calculation
- test_asking_whether_something_can_be_claimed_is_described_as_explain_to_the_router
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- createPseudoSheet
- test_help_runs_without_importing_core_before_sys_path_is_set
- test_an_unscoped_result_is_not_empty_for_the_owner
- test_each_policy_lapses_on_its_own
- ConfirmNameRequest
- CorrectionRequest
- CorrectionResponse
- DeclinedEvent
- ObligationChanged
- OwnerRequest
- PendingName
- PlaceRequest
- Turn
- AdviceCardEvent
- AdviceFigure
- AdviceWithheldEvent
- AskResponse
- ConsentRequest
- ConsentRequiredEvent

## God Nodes (most connected - your core abstractions)
1. `InstalledPack` - 113 edges
2. `FakeConn` - 81 edges
3. `Passage` - 74 edges
4. `client_for()` - 74 edges
5. `ScriptedOllama` - 72 edges
6. `settings()` - 72 edges
7. `advice/__init__.py` - 71 edges
8. `ModelUnavailable` - 69 edges
9. `rows_for()` - 69 edges
10. `Ollama` - 66 edges

## Surprising Connections (you probably didn't know these)
- `ModuleManifest` --uses--> `test_a_module_may_read_grounding_values()`  [INFERRED]
  core/contracts.py → tests/test_contracts.py
- `GroundingCorpus` --uses--> `test_every_grounding_corpus_declares_its_provenance()`  [INFERRED]
  core/contracts.py → tests/test_contracts.py
- `PackManifest` --uses--> `test_a_pack_cannot_opt_out_of_never_acts()`  [INFERRED]
  core/contracts.py → tests/test_contracts.py
- `PackManifest` --uses--> `test_template_pack_validates()`  [INFERRED]
  core/contracts.py → tests/test_contracts.py
- `create_app()` --uses--> `Lifecycle`  [INFERRED]
  api/main.py → core/runtime/lifecycle.py

## Import Cycles
- None detected.

## Communities (239 total, 28 thin omitted)

### Community 0 - "pack"
Cohesion: 0.08
Nodes (40): holdings(), HouseholdInventory, The documents on file, read from `facts` rather than searched for. "Do I have…, Handed to `AnswerGraph` by whoever holds a connection, as `HouseholdScope` is., Handed to `AnswerGraph` by whoever holds a connection, as `HouseholdScope` is., Rows of `INVENTORY`, one holding per document that prints the field its pack's…, Rows of `INVENTORY`, one holding per document that prints the field an enabled p, Asked (+32 more)

### Community 1 - "packs/page.tsx"
Cohesion: 0.15
Nodes (10): ADR-0017, packs/page.tsx, dynamic, metadata, PacksPage(), runtime, Toggle(), ModuleSummary (+2 more)

### Community 2 - "Christian — task list"
Cohesion: 0.17
Nodes (18): GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records…, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records, _long_text(), Returns the replies the test wrote, in order, then an empty list of values. A…, A truncated or non-JSON reply is an outage: the section was never actually…, Unlike a garbled reply, valid JSON with the wrong shape means the model…, _reply() (+10 more)

### Community 3 - "validate"
Cohesion: 0.07
Nodes (45): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), Validate a document register before it is handed over. python -m…, Parse `field_pages`: semicolon-separated `name=page`, 1-based. Empty means page… (+37 more)

### Community 4 - "Ollama"
Cohesion: 0.08
Nodes (54): queue(), Send the pages as images and try the whole pack pipeline again on what comes…, The reportable line. Deliberately a rate and a count, because a rate over three, The reportable line. Deliberately a rate and a count, because a rate over three…, What is waiting for a person's eyes, oldest first., Recovery, recovery_rate(), retry() (+46 more)

### Community 5 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 6 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 7 - "sha256"
Cohesion: 0.09
Nodes (22): CaptureAdapter, The one interface every capture channel satisfies. receive(payload, mime,…, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sha256(), adapters/__init__.py, Capture adapters. Every channel a document can arrive through satisfies one…, Cursor (+14 more)

### Community 8 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (11): running-the-eval-harness/SKILL.md, Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness (+3 more)

### Community 9 - "support.js"
Cohesion: 0.12
Nodes (28): collectProps(), compileAttr(), compileTemplate(), contentKey(), cssToObj(), encodeCamelAttrs(), encodeCase(), evalDcLogic() (+20 more)

### Community 10 - "Desmond — task list"
Cohesion: 0.12
Nodes (17): The result of asking "whose is this?" of a question and its passages., The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting…, A first-person question that nothing of the owner's can answer.          The i, Scoped, 13 September: "how much is my son's life insurance?" came back as the owner's…, 13 September: "how much is my son's life insurance?" came back as the owner's ow, 13 September: "is my dad's hospital cover still active?" was scoped to Lim Ah… (+9 more)

### Community 11 - "Zee — task list"
Cohesion: 0.18
Nodes (16): ParsedDocument, ingest/quarantine.py, blocked_reasons(), forget(), page_images(), QuarantinedDocument, The second stage of quarantine: the page image, read by the vision-language…, Per document: `None` when the image pass can run, or the sentence saying why it… (+8 more)

### Community 12 - "test_api.py"
Cohesion: 0.40
Nodes (5): The only network guard on the app. Zee's interface proxies through Next, so…, `hides its facts` reaches an answer through retrieval, not through the API., `hides its facts` reaches an answer through retrieval, not through the API., test_the_api_is_loopback_only(), test_the_retriever_filters_by_enabled_pack()

### Community 13 - "answer.tsx"
Cohesion: 0.06
Nodes (44): ai, @ai-sdk/react, chat/route.ts, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST() (+36 more)

### Community 14 - "Filling the corpus register"
Cohesion: 0.20
Nodes (10): filling-the-corpus-register/SKILL.md, Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one (+2 more)

### Community 15 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (10): writing-a-governance-artefact/SKILL.md, Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six (+2 more)

### Community 16 - "Claude Code — read this first"
Cohesion: 0.33
Nodes (5): Before you say you are done, Claude Code — read this first, Finding your way around, Skills and commands, The three things agents get wrong here

### Community 17 - "test_worker_queue.py"
Cohesion: 0.12
Nodes (22): Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker. Celery is imported here rather…, Intake, FakeConnection, FakeCursor, The queue, tested with no broker anywhere. What is worth asserting here is not…, The whole point. If `process` is reachable from the capture thread, nothing was… (+14 more)

### Community 18 - "test_grounding_index.py"
Cohesion: 0.10
Nodes (36): index_pack(), IndexReport, Upsert this pack's sources and stage the values a changed one prints. A pack…, Upsert this pack's sources and stage the values a changed one prints.      A p, What one call to `index_pack` did, so a script can say it in a line per pack., What one call to `index_pack` did, so a script can say it in a line per pack., main(), _Connected (+28 more)

### Community 19 - "obligation"
Cohesion: 0.05
Nodes (41): FakeGraph, graph(), obligation(), overdue_row(), The five endpoints, against a fake database and the real queries. The…, One row of `reminder.OVERDUE`, in its column order., One row of `reminder.OVERDUE`, in its column order., The nightly sweep owns `last_notified_at`. A screen refresh must not burn a… (+33 more)

### Community 20 - "Household canon"
Cohesion: 0.25
Nodes (7): Address, Employment, Household canon, Life events that documents must reflect, People, Policies, Vehicles

### Community 21 - "get"
Cohesion: 0.24
Nodes (23): bundledBlob(), getDC(), Dispatcher(), getError(), load(), createHelmetManager(), applyCanvasBg(), compile() (+15 more)

### Community 22 - "build_team_tasks.py"
Cohesion: 0.48
Nodes (6): main(), Generate each member's task list from the master task CSV. python…, _read_rows(), _render(), _week_key(), _write()

### Community 23 - "`core/graph/` — the LangGraph runtime"
Cohesion: 0.40
Nodes (5): graph/README.md, `core/graph/` — the LangGraph runtime, Rules, What belongs here, What does not

### Community 24 - "`core/ingest/` — the ingestion worker"
Cohesion: 0.50
Nodes (4): ingest/README.md, `core/ingest/` — the ingestion worker, Quarantine is two-stage, Rules

### Community 25 - "Integration review"
Cohesion: 0.29
Nodes (7): integration-review/SKILL.md, How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 26 - "Writing an ADR"
Cohesion: 0.29
Nodes (7): writing-an-adr/SKILL.md, Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 27 - "test_startup.py"
Cohesion: 0.11
Nodes (24): Start `npm run dev` in `web/`, or say plainly why it could not. Three reasons…, start_web(), main(), Local-only startup preflight, using the standard library so setup can be…, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file…, report_hardware(), startup_gaps() (+16 more)

### Community 28 - "Graphify — the shared knowledge graph"
Cohesion: 0.20
Nodes (9): Graphify — the shared knowledge graph, Keeping it fresh, Merge conflicts, solved properly, Setup, once per clone, The hook leaves your tree dirty. Amend it into the commit you just made., Two kinds of extraction, and which needs what, Using it, What is committed, and what is not (+1 more)

### Community 29 - "test_modules.py"
Cohesion: 0.16
Nodes (27): already_said(), True when this exact window has already been mentioned. The comparison is by…, Everything inside a lead window that has not already been said for that window.…, sweep(), FakeConn, FakePack, obligation_row(), Reminder and Alert: what fires, once, and with what behind it. Both modules are… (+19 more)

### Community 30 - "`api/` — the FastAPI application"
Cohesion: 0.40
Nodes (5): api/README.md, `api/` — the FastAPI application, Five properties worth knowing before you change anything, Rules, The surface

### Community 31 - "The corpus"
Cohesion: 0.29
Nodes (7): corpus/README.md, Handing a batch over, One rule, The corpus, The order matters, Tiers, Validate before handing over

### Community 32 - "Artefacts"
Cohesion: 0.33
Nodes (6): artefacts/README.md, A note on the model, Artefacts, Current deliverables, Regenerating, Source material

### Community 33 - "Why the prototype is evaluated on synthetic data"
Cohesion: 0.33
Nodes (5): The decision, What synthetic data does not prove, What we do not do, Why, Why the prototype is evaluated on synthetic data

### Community 34 - "`core/adapters/` — capture adapters"
Cohesion: 0.67
Nodes (3): adapters/README.md, `core/adapters/` — capture adapters, Rules

### Community 36 - "Project skills"
Cohesion: 0.40
Nodes (5): skills/README.md, Changing them, Project skills, Slash commands, Using them

### Community 37 - "ValueRow"
Cohesion: 0.13
Nodes (19): _ambiguous(), _band(), _in_band(), _product_name(), _qualified(), _qualifier(), One row of `queries.VALUES_FOR`: an approved value and the reviewed source it…, One row of `queries.VALUES_FOR`: an approved value and the reviewed source it ca (+11 more)

### Community 38 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 39 - "InstalledPack"
Cohesion: 0.07
Nodes (18): HouseholdConsents, `core.graph.advice.ConsentBook` over a live connection, for the graph to ask…, HouseholdAdviceLog, The record of every advised or withheld answer (ADR 0016). `advice_records`…, `core.graph.advice.AdviceLog` over a live connection. `basis` is dumped with…, AdviceLog, AdviceRecord, Implemented by `HouseholdAdviceLog` in `core/advice_records.py`. (+10 more)

### Community 40 - "HouseholdConsents"
Cohesion: 0.18
Nodes (7): attribute(), Say whose a captured document is, before anything has been read off it., attribution(), A daemon thread that long-polls the Telegram bot until `stop()` or process…, One long poll. A failure waits rather than hammering the API with the same…, Whose phone this arrived on, recorded before anything is read off it. See ADR…, TelegramCapture

### Community 41 - "Changelog"
Cohesion: 0.50
Nodes (3): Changelog, W1 · 2–8 Sep 2026, W2 · 9–15 Sep 2026

### Community 42 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 43 - "`docs/governance/` — the assurance artefacts"
Cohesion: 0.50
Nodes (4): governance/README.md, `docs/governance/` — the assurance artefacts, The autonomy statement in one line, The rule that governs all eight

### Community 50 - "events"
Cohesion: 0.50
Nodes (4): A sentence that passed the gate was true when it passed. Losing the connection…, A sentence that passed the gate was true when it passed. Losing the connection a, test_a_model_that_dies_mid_answer_keeps_what_it_already_proved(), constrained_stream()

### Community 51 - "add_person"
Cohesion: 0.20
Nodes (9): graph/__init__.py, The answer graph. Router, retrieve, rerank, grounding gate, then answer or…, What the graph needs from retrieval, stated as a contract rather than an…, Implemented by `core/retrieve/` when Lane B's hybrid search lands. `candidates`…, Implemented by `core/retrieve/` when Lane B's hybrid search lands.      `candida, A cross-encoder, scoring question against passage. Returns the best `keep`,…, A cross-encoder, scoring question against passage. Returns the best `keep`, reor, Reranker (+1 more)

### Community 52 - "The household, and the word "my""
Cohesion: 0.06
Nodes (29): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 13. A question is understood before it is searched, and scoped before it is cut, Consequences, Context, Decision (+21 more)

### Community 53 - "owner"
Cohesion: 0.18
Nodes (10): HouseholdScope, Keep the passages of these people and of the household; set aside everybody…, Keep the passages of these people and of the household; set aside everybody else, What `AnswerGraph` is handed so it can scope without holding a connection.…, What `AnswerGraph` is handed so it can scope without holding a connection., scope_to(), A fresh install is not broken. It answers about the household, as it always…, A fresh install is not broken. It answers about the household, as it always did. (+2 more)

### Community 54 - "alert/__init__.py"
Cohesion: 0.17
Nodes (19): AlertConfig, alert/__init__.py, cpf_contributions_ytd(), days_uncovered(), donations_ytd(), Measurement, _per_subject(), The Alert module: a pack-declared threshold, crossed once, citing the documents… (+11 more)

### Community 55 - "Basic Financial Planning Guide"
Cohesion: 0.15
Nodes (12): Basic Financial Planning Guide, Basic Financial Planning Guide, Basic Financial Planning Guide For Entrants To The Workforce, Basic Financial Planning Guide for those nearing retirement, Basic Financial Planning Guide For Those With Dependents, Emergency funds, For those approaching retirement, For those new to the workforce (+4 more)

### Community 56 - "test_household.py"
Cohesion: 0.05
Nodes (52): is_first_person(), Whether this question is about the person asking. `other_names` are the display…, Whether this question is about the person asking.      `other_names` are the d, _household_scope(), Who is asking, and whose documents may answer. Two halves, deliberately split.…, `HouseholdScope` over a roster held in memory, with every document resolved by…, `HouseholdScope` over a roster held in memory, with every document resolved by n, The roster has no grandparent relation, so the household says it the only way… (+44 more)

### Community 57 - "advice/__init__.py"
Cohesion: 0.08
Nodes (69): RuleInput, Figure, Input, One fact or rule value a calculation was built on, carrying its own citation.…, One number a calculator produced, and the words a sentence must use to state…, advice/__init__.py, _amount(), _band_label() (+61 more)

### Community 58 - "cli.py"
Cohesion: 0.05
Nodes (74): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a…, paperbrain/ask.py, answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, paperbrain/chunk.py (+66 more)

### Community 59 - "client_for"
Cohesion: 0.11
Nodes (31): InstalledPack, advising(), consent(), ConsentConn, inbox(), _padded(), The parameters of the one statement containing `needle`. Fails loudly if it…, The parameters of the one statement containing `needle`. Fails loudly if it neve (+23 more)

### Community 60 - "load_corpus.py"
Cohesion: 0.50
Nodes (4): documents_in(), main(), Load a handed-over corpus batch into this computer's database. uv run python…, Every document in the batch, in a stable order, recursing into tier subfolders.

### Community 61 - "test_pages.py"
Cohesion: 0.12
Nodes (28): page_count(), PageUnavailable, _pdfium(), One page of one document, as an image. Two callers want the same thing for…, Safe to show a person: there is no such page, or this file cannot be drawn., How many pages this file has, or 0 when it is not something with pages.…, `(bytes, media type)` for one page, one-based. An image document is returned…, render_page() (+20 more)

### Community 62 - "test_ingest_pipeline.py"
Cohesion: 0.06
Nodes (62): classify(), Never raises. An unavailable model is a classification failure, so it…, extract(), find_page(), _normalise(), printed_date(), The first page whose text contains this value. None means no page supports it.…, A date as a document prints it, as YYYY-MM-DD, or None when it is not a date.… (+54 more)

### Community 63 - "bench_runtime.py"
Cohesion: 0.09
Nodes (32): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+24 more)

### Community 64 - "compilerOptions"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 65 - "export-design-preview.cjs"
Cohesion: 0.11
Nodes (17): bundle(), classes, css, cssFile, domId, fs, ids, licences (+9 more)

### Community 66 - "run_parrot.py"
Cohesion: 0.12
Nodes (22): _kill_tree(), main(), open_browser(), parse_args(), port_answers(), Run the engine, the folder watcher, the ingestion worker and the screens…, Stop a child and everything under it, then make sure it has gone., Whether something is listening on loopback. Not whether it is ours. (+14 more)

### Community 67 - "ModelUnavailable"
Cohesion: 0.06
Nodes (48): DocumentTypeSpec, One kind of document the core recognises., One kind of document this pack recognises., ingest/extract.py, _coerce(), _date_renderings(), decode_schema(), _drop_format() (+40 more)

### Community 68 - "registry.py"
Cohesion: 0.09
Nodes (35): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders…, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, Load the installed capability modules at runtime. The mirror of…, A module's YAML is missing, or does not validate against `ModuleManifest`. (+27 more)

### Community 69 - "Generated"
Cohesion: 0.09
Nodes (23): The page a person sees while Parrot starts, served by the engine itself. **Why…, Load the generator and the embedder before the first question, and record the…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), warm_models(), Classification, _prompt(), Decide which pack's document type a captured document is, or decline to. The… (+15 more)

### Community 70 - "test_advice_module.py"
Cohesion: 0.14
Nodes (56): Missing, What a calculator returns when a fact or a rule value it needed was not there…, calculate(), One person's advice. The graph asks whose first when a question names several…, One person's advice. The graph asks whose first when a question names several pe, basis(), fact(), figures_of() (+48 more)

### Community 72 - "preview.tsx"
Cohesion: 0.11
Nodes (17): design-preview/page.tsx, metadata, answers, DesignPreview(), Direction, directions, Item, items (+9 more)

### Community 73 - "scope.py"
Cohesion: 0.11
Nodes (26): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Whose question is this, and whose documents may answer it. "What is my term… (+18 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (17): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+9 more)

### Community 75 - "load_register"
Cohesion: 0.14
Nodes (12): by_subject(), db(), FakeCursor, load_register(), Every batch1 row as the facts extraction would write, through the statement it u, Every batch1 row as the facts extraction would write, through the statement it…, One member's statement must never drive another member's 15,300 cap., One member's statement must never drive another member's 15,300 cap. (+4 more)

### Community 76 - "Screens"
Cohesion: 0.23
Nodes (8): _launcher(), Stands in for `start_web` and `stop_web`: counts, and never touches npm., Screens, _supervise(), test_a_start_that_fails_is_not_retried(), test_no_web_means_the_supervisor_starts_no_screens(), test_the_supervisor_relaunches_on_restart_and_keeps_the_screens_up(), test_the_supervisor_still_refuses_a_lan_bind_before_starting_anything()

### Community 77 - "Notion"
Cohesion: 0.25
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "test_answer_graph.py"
Cohesion: 0.18
Nodes (22): Holding, Inventory, Passage, FakeInventory, FixedRetriever, holding(), insurance(), PassThroughReranker (+14 more)

### Community 79 - "The demonstration run sheet"
Cohesion: 0.14
Nodes (14): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+6 more)

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (8): paperbrain/README.md, How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Contributing"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 82 - "ingest/extract.py"
Cohesion: 0.22
Nodes (7): collapse(), _cuts_a_number(), printed_in(), Text with table pipes and every run of whitespace folded to one space. A model…, Whether the passage is printed in the text, without starting or ending inside a…, test_collapse_folds_whitespace_and_table_pipes(), test_printed_in_accepts_both_forms_of_a_table_row()

### Community 83 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 85 - "[...path]/route.ts"
Cohesion: 0.16
Nodes (19): [...path]/route.ts, ALLOWED, Context, DELETE(), dynamic, forward(), GET(), PATCH() (+11 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "document-detail.tsx"
Cohesion: 0.24
Nodes (9): SourcePanel(), DocumentDetail(), when(), Field(), format(), isNumeric(), CorrectionResponse, pageImage() (+1 more)

### Community 89 - "tokens/page.tsx"
Cohesion: 0.05
Nodes (36): lucide-react, react, (app)/layout.tsx, dynamic, runtime, Motion(), ROWS, tokens/page.tsx (+28 more)

### Community 90 - "lock.ts"
Cohesion: 0.13
Nodes (30): auth/route.ts, dynamic, GET(), grant(), POST(), runtime, unlock/page.tsx, dynamic (+22 more)

### Community 91 - "create_app"
Cohesion: 0.13
Nodes (15): create_app(), checks(), ready(), setup(), system_status(), The setup page exists to say the database is missing. It cannot say it if it…, The setup page exists to say the database is missing. It cannot say it if it did, test_the_server_still_starts_when_the_database_is_not_running() (+7 more)

### Community 92 - "FakeConn"
Cohesion: 0.10
Nodes (30): current(), grant(), _latest(), NoOwner, The owner's consent to a pack's advice, append-only (ADR 0016). Consent is the…, Record the owner saying yes to `wording`, this pack's consent text at…, Record the owner taking it back. Append-only: the grant stays in the table,…, No owner is recorded yet, so there is nobody whose consent this could be (ADR… (+22 more)

### Community 94 - "FolderCapture"
Cohesion: 0.22
Nodes (4): FolderCapture, Begin watching. Returns False, with a logged reason, when it cannot., Begin polling. Returns False, with a logged reason, when it cannot or should…, A daemon thread that polls the watched folder until `stop()` or process exit.

### Community 102 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "FakeConn"
Cohesion: 0.07
Nodes (56): client(), client_for(), conn(), FakeConn, filed_document(), open_obligation(), pack_row(), The point of the endpoint. An UPDATE alone loses the example we are trying to… (+48 more)

### Community 104 - "ForgottenDocument"
Cohesion: 0.40
Nodes (5): ForgottenDocument, 202. The vision pass is slower than a page load, so it is queued and this is…, A quarantined document Parrot no longer remembers., A quarantined document Parrot no longer remembers., RetryAccepted

### Community 105 - "DocumentCatalog"
Cohesion: 0.10
Nodes (27): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering (, Why the catalogue cannot supply `field` from every one of `doc_types`, or None., Whether any document type in the catalogue declares `field`., Every core document type, field and category this pack names exists, or ValueErr, _class_name(), _docstring(), _field_line() (+19 more)

### Community 106 - "test_telegram_capture.py"
Cohesion: 0.10
Nodes (26): build(), FakeRegistrar, FakeTelegram, photo_update(), Telegram capture: what arrives, what is answered, and what is written where. No…, A photograph as Telegram actually sends one: the same image in several sizes.…, The claim the queued dispatcher depends on. See `core/ingest/source.py`., The offset has already moved, so the survivors are all that is left to save. (+18 more)

### Community 107 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 108 - "ScriptedOllama"
Cohesion: 0.18
Nodes (12): next_kind(), The kind of the next event on the wire., Starlette never closes a body iterator a disconnected client stopped pulling. `_, The ruling's case as it happens on a socket: Starlette sends the card and at onc, What the API owns when a stream is closed with the graph still parked on the car, C5 fix round 2 closed the gap this test used to mark: `AdviceCard` is now yielde, The graph's own cleanup can fail -- for example the record insert raises -- and, test_a_client_that_leaves_after_the_card_commits_one_record() (+4 more)

### Community 109 - "test_runtime.py"
Cohesion: 0.09
Nodes (15): ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one…, _ollama_answering(), Setup diagnostics use controlled service responses, never live household…, 13 September: size_vram was 0 on every model and nothing on screen said so., test_a_database_that_does_not_answer_fails_in_seconds(), test_a_model_that_cannot_load_is_recorded_rather_than_raised(), test_an_embedding_model_without_task_prompts_is_sent_the_text_alone() (+7 more)

### Community 110 - "vault.py"
Cohesion: 0.06
Nodes (42): _columns(), correct(), Corrected, CorrectionRejected, A person fixing a field the extractor got wrong. This is the one place in the…, `(value_text, value_num, value_date)` — exactly one of them set. The declared…, Store what a person says this field actually says, and keep what it used to…, Safe to show: there is no fact with that id. (+34 more)

### Community 111 - "Registration"
Cohesion: 0.10
Nodes (19): Dispatcher, Inline, What happens to a document between "these bytes are registered" and "this…, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Send, What every capture channel hands a document to. An adapter's job ends at "these… (+11 more)

### Community 112 - "Claim"
Cohesion: 0.07
Nodes (58): Exclusions, A sentence claiming cover whose every citation sits under one of `headings` is…, A sentence claiming cover whose every citation sits under one of `headings` is d, check(), check_advice(), check_content(), check_one(), Claim (+50 more)

### Community 113 - "test_grounding_values.py"
Cohesion: 0.14
Nodes (30): number_tokens(), Every whole number the passage prints, thousands separators removed., _dropped(), Published values: the model reads a source, and code keeps only what the…, Assert a value was dropped, and logged with this reason., _run(), test_a_money_value_with_a_currency_marker_is_kept(), test_a_multiple_is_kept_in_the_forms_it_is_written() (+22 more)

### Community 114 - "household.py"
Cohesion: 0.07
Nodes (44): add_person(), classify_prompt(), confirm(), dismiss(), owner(), owner_aliases(), pending(), pending_count() (+36 more)

### Community 115 - "GroundingCorpus"
Cohesion: 0.23
Nodes (18): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Read and validate a pack's grounding corpus from its own folder on disk. A…, A pack's grounding corpus on disk does not match what its `sources.yaml`…, Where this pack's grounding corpus lives on disk, or `None` if it declares none., Read, validate and hash every source this pack's corpus records. Raises… (+10 more)

### Community 116 - "TelegramAdapter"
Cohesion: 0.09
Nodes (29): IngestJob, Magic bytes first, filename suffix second, `application/octet-stream` last. A…, What a capture returns: a registered document, and whether we had seen it…, sniff_mime(), _Registered, _attachment(), _pixels(), The Telegram capture adapter. Same interface as the folder: `receive(payload,… (+21 more)

### Community 117 - "scope_passages"
Cohesion: 0.17
Nodes (16): Keep the owner's passages and the household's; set aside everybody else's. A…, Keep the owner's passages and the household's; set aside everybody else's., scope_passages(), _conn_returning(), _passage(), The third bucket. Home contents, a utility bill — nobody's name on it,…, The third bucket. Home contents, a utility bill — nobody's name on it, everybody, A joint policy is the owner's too. Presence wins over exclusion. (+8 more)

### Community 118 - "test_lifecycle.py"
Cohesion: 0.16
Nodes (18): The local API. Liveness is intentionally separate from assistant readiness.…, Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor.…, What the person asked for, once. The first request wins; later ones change…, _client(), _eventually(), quiet_engine(), Restart and shut down: the engine asks its supervisor, and nothing else can ask… (+10 more)

### Community 120 - "app/layout.tsx"
Cohesion: 0.22
Nodes (8): next-themes, app/layout.tsx, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 121 - "boot"
Cohesion: 0.20
Nodes (10): boot(), dcNameFromPath(), getReactDOM(), parseDataProps(), parseDcDocument(), parseDcText(), rootNameForDocument(), safeDecode() (+2 more)

### Community 122 - "PackManifest"
Cohesion: 0.06
Nodes (60): check_advice_links(), Every fact an advice shape reads from another pack is declared by an installed…, _advised(), _checked(), _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules() (+52 more)

### Community 123 - "SentenceScanner"
Cohesion: 0.10
Nodes (27): Pulling finished sentences out of a JSON reply that is still being written. The…, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner, drip() (+19 more)

### Community 124 - "reminder/__init__.py"
Cohesion: 0.11
Nodes (20): reminder/__init__.py, close(), current_lead(), Due, next_window(), Overdue, The Reminder module: a nightly sweep of obligations, and nothing fires twice.…, Past their date and never closed. A different problem from a reminder, shown… (+12 more)

### Community 125 - "Household canon"
Cohesion: 0.04
Nodes (43): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, Policies, The family tree, and why three of them are not called Lim (+35 more)

### Community 126 - "item-row.tsx"
Cohesion: 0.16
Nodes (13): SourceChip(), stripTrailingPage(), ADR-0016, countdown(), detail(), figure(), ItemRow(), longDate() (+5 more)

### Community 127 - "ErrorEvent"
Cohesion: 0.67
Nodes (3): ErrorEvent, The stream broke after it began. A client cannot read an HTTP status by then., The stream broke after it began. A client cannot read an HTTP status by then.

### Community 128 - "FolderAdapter"
Cohesion: 0.12
Nodes (28): FolderAdapter, FolderSettings, _Pending, The watched-folder capture adapter. A person drops a scan into a folder and it…, Every file in the watched folder that is worth looking at at all., Advance the debounce by `elapsed` seconds and return the files now ready. Time…, One debounce tick, then register whatever it declared ready., Satisfies `CaptureAdapter`. Holds no database handle — it is given a… (+20 more)

### Community 129 - "._compares_what_its_documents_declare"
Cohesion: 0.11
Nodes (18): PackManifest, A domain pack, authored as one YAML file., Why this pack cannot supply `field` from every one of `doc_types`, or None if…, An advice shape that names a missing role, field, category or key fails at load…, A domain pack, authored as one YAML file: grounding, persona, answering and advi, An advice shape that names a missing role or key fails at load time., A compared field no document type of the shape declares can never be printed.…, A compared field no document type of the shape declares can never be printed. (+10 more)

### Community 130 - "FakeConn"
Cohesion: 0.15
Nodes (11): names_for(), Each person's display name and confirmed aliases, trimmed and lower-cased the…, Each person's display name and confirmed aliases, trimmed and lower-cased the wa, db(), _document(), FakeCursor, _source(), _sum_insured() (+3 more)

### Community 131 - "createExternalModules"
Cohesion: 0.25
Nodes (11): cdnScriptFor(), createExternalModules(), ensureBabel(), resolve2(), resolveGlobal(), waitForGlobal(), isElementClass(), isRenderableType() (+3 more)

### Community 132 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 133 - "Passage"
Cohesion: 0.07
Nodes (50): build(), events(), passage(), PhrasingRetriever, The grounding gate, and the graph's two ways of not answering. Rule 3 says no…, ADR 0017: every chunk is `core`'s, and the type a pack speaks for picks its guar, Scores one passage differently depending on which phrasing found it., Scores one passage differently depending on which phrasing found it. (+42 more)

### Community 134 - "api.ts"
Cohesion: 0.06
Nodes (39): household/page.tsx, dynamic, metadata, runtime, AdviceConsentSection(), Load, STATUS, ADR-0016 (+31 more)

### Community 135 - "team/README.md"
Cohesion: 0.18
Nodes (11): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision, packs/README.md, christian/README.md, desmond/README.md, team/README.md (+3 more)

### Community 136 - "today/page.tsx"
Cohesion: 0.07
Nodes (35): next, HouseholdPage(), AppLayout(), today/page.tsx, dynamic, isUrgent(), metadata, runtime (+27 more)

### Community 137 - "values.py"
Cohesion: 0.09
Nodes (33): A rule or table value a pack's sources publish. Extracted automatically,…, A rule or table value a pack's sources publish.      Extracted automatically,, ValueKey, SourceText, Index a pack's published sources, and stage the values they print for a person…, Insert or refresh the source's row, and return its id., Insert or refresh the source's row, and return its id., _upsert_source() (+25 more)

### Community 139 - "FactRow"
Cohesion: 0.20
Nodes (12): Categories, FactInput, A printed fact a calculator reads, named by where it is printed rather than…, A printed fact a calculator reads, named by where it is printed rather than what, fact_row(), FactRow, facts_for(), in_category() (+4 more)

### Community 140 - "test_reindexing_replaces_chunks_and_leaves_facts_alone"
Cohesion: 0.11
Nodes (19): document_title(), The document as a person would name it: its `string` fields as read, in declared, The document as a person would name it: its `string` fields as read, in the…, pgvector accepts its own text form; this avoids registering an adapter for one c, pgvector accepts its own text form; this avoids registering an adapter for one…, _vector_literal(), ingest/reindex.py, indexed() (+11 more)

### Community 141 - "StreamingGraph"
Cohesion: 0.07
Nodes (39): a_citation(), advice_card(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive…, No `reading` before it: the floor is checked before the model is asked anything. (+31 more)

### Community 143 - "ingest/quarantine.py"
Cohesion: 0.08
Nodes (24): Block, DoclingParser, _kind(), _pages_from(), parse(), Parser, PlainTextParser, Turn captured bytes into pages of text, or say why it could not be done. Every… (+16 more)

### Community 144 - "devDependencies"
Cohesion: 0.10
Nodes (21): eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node, @types/react (+13 more)

### Community 145 - "Comparison of Integrated Shield Plans"
Cohesion: 0.18
Nodes (10): Common reasons why insurers do not provide a Letter of Guarantee in specific cases, Common reasons why insurers may reject or not pay for claims, Comparison of Integrated Shield Plans, Comparison of lifetime premiums, Important Information, Letter of Guarantee, List of Integrated Shield Plans (IPs) and their targeted level of coverage, Medical Record Costs (+2 more)

### Community 146 - "main"
Cohesion: 0.16
Nodes (18): approve(), pending(), PendingValue, A person's approval, standing between a model's extraction and any calculator…, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it., Every value still waiting for review, oldest first, optionally for one pack., Approve these ids, ignoring any that are no longer `pending`. Returns the count… (+10 more)

### Community 147 - "Domain packs — start here"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 149 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 150 - "schedule.py"
Cohesion: 0.17
Nodes (15): build(), The one Celery application, built from `Settings`. Every setting here is a…, Construct the Celery application. Imported lazily by callers so that nothing…, beat_schedule(), cron_expressions(), crontab_from(), manifest(), When the nightly sweeps run, read from the modules' own manifests. A module… (+7 more)

### Community 151 - "FakeConn"
Cohesion: 0.67
Nodes (3): On 10 February 2027 Marcus's home contents cover has lapsed, while his motor and, On 10 February 2027 Marcus's home contents cover has lapsed, while his motor…, test_a_lapsed_policy_is_not_masked_by_another_that_still_runs()

### Community 152 - "test_one_document_is_shown_even_when_its_pack_is_off"
Cohesion: 0.32
Nodes (8): document_row(), fact_row(), ADR 0017: disabling insurance_agent switches off its voice, never a household's, Following a citation must never end in a blank screen because a pack was…, Following a citation must never end in a blank screen because a pack was switche, test_a_core_document_stays_enabled_when_every_pack_is_off(), test_one_document_is_shown_even_when_its_pack_is_off(), test_vault_lists_documents_with_their_facts()

### Community 153 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 156 - "package.json"
Cohesion: 0.11
Nodes (16): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+8 more)

### Community 159 - "4. Writing `pack.yaml`"
Cohesion: 0.12
Nodes (15): 1. What a pack is, 2. The one thing to understand before you start, 3. The workflow, 4. Writing `pack.yaml`, 5. The grounding corpus, 6. Definition of done, 7. Where to ask, Authoring a domain pack (+7 more)

### Community 160 - "12. Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.33
Nodes (5): 12. Chunks follow the document's headings, and embeddings use the model's task prompts, Consequences, Context, Decision, Evidence

### Community 161 - "Try PARROT"
Cohesion: 0.12
Nodes (16): 1 · Install five things, 2 · Download the AI models, 3 · Get the code and set it up, 4 · Put some documents in, 5 · Run it, 6 · Use it, Ask — a question about your own documents, If something goes wrong (+8 more)

### Community 162 - "github.md"
Cohesion: 0.50
Nodes (3): Last sync, Screen map, Updated in this project

### Community 163 - "Understanding health insurance"
Cohesion: 0.20
Nodes (9): Assistance under MediFund, Basic health insurance coverage, Choosing your level of coverage, How MediSave fits in, If you have company health insurance, If you want more coverage, Types of health insurance plans, Understanding health insurance (+1 more)

### Community 165 - "ParsedPage"
Cohesion: 0.12
Nodes (24): ingest/chunk.py, Chunk, chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own… (+16 more)

### Community 166 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 167 - "install_best_effort"
Cohesion: 0.10
Nodes (25): lifespan(), install(), install_best_effort(), Installed, What `install` did, so a startup line can say it in one sentence., What `install` did, so a startup line can say it in one sentence., Write every pack and module on disk into its table. Idempotent; never re-enables, Write every pack and module on disk into its table. Idempotent; never re-… (+17 more)

### Community 168 - "_Value"
Cohesion: 0.29
Nodes (7): _Value, _order_key(), _ordered(), One sortable key for a number, a date or a word, so a ranking never compares…, One sortable key for a number, a date or a word, so a ranking never compares acr, Keys ranked by value in the stated order, ties broken by name so a ranking is…, Keys ranked by value in the stated order, ties broken by name so a ranking is re

### Community 169 - "test_advice_core.py"
Cohesion: 0.27
Nodes (11): _kind_of(), passages_for(), `"fact:12"` -> `"fact"`, `"rule:7"` -> `"rule"`. Anything else is a calculator…, Inputs as kind fact/rule passages (chunk_id from the ref), and the figures as…, _calculation(), test_check_content_keeps_a_sentence_stating_a_facts_value(), test_check_content_keeps_a_sentence_stating_a_figure(), test_check_content_keeps_a_sentence_stating_a_rules_value() (+3 more)

### Community 170 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 171 - "igd-capstone-2026"
Cohesion: 0.20
Nodes (10): Authoring a pack, igd-capstone-2026, `main` is not protected, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live (+2 more)

### Community 172 - "0001_init.sql"
Cohesion: 0.36
Nodes (7): chunks, documents, facts, modules, obligations, packs, traces

### Community 173 - "quarantine.tsx"
Cohesion: 0.29
Nodes (4): GoneRow(), QuarantineQueue(), QuarantineRow(), QuarantinedDocument

### Community 174 - "Zee — Lane D · Domain packs and interface"
Cohesion: 0.22
Nodes (9): Half one — domain packs (weeks 1 to 7), Half two — the interface (weeks 4 to 8), Read this first, Rules that apply to you specifically, The two halves of this lane, What "done" looks like, What you present, Your Claude Code skills (+1 more)

### Community 175 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (8): authoring-a-domain-pack/SKILL.md, Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 176 - "Christian — Lane A · Integration and product owner"
Cohesion: 0.29
Nodes (7): Also yours, Christian — Lane A · Integration and product owner, Starter prompt for your coding agent, Starter prompt: what can I actually pick up?, The five things you ship, Week 1, in order, What integration actually means here

### Community 177 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.29
Nodes (7): Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The autonomy statement, The six artefacts, Where governance touches the code

### Community 179 - "dependencies"
Cohesion: 0.10
Nodes (20): ai, @ai-sdk/react, class-variance-authority, clsx, createComponentFactory(), lucide-react, next, next-themes (+12 more)

### Community 180 - "Alert"
Cohesion: 0.17
Nodes (10): Alert, _debounced(), Every declared threshold that is crossed, has evidence, and has not just been…, What the debounce is keyed on: this metric, for this person and thing, in this…, sweep(), Two lapsed policies on one person are two alerts, and saying one must not silenc, Two lapsed policies on one person are two alerts, and saying one must not…, test_every_firing_is_scoped_and_cites_a_page() (+2 more)

### Community 181 - "MediShield Life Benefits"
Cohesion: 0.33
Nodes (5): Exclusions under MediShield Life, Fertility Preservation Procedures in cases of potential iatrogenic infertility, List of Serious Pregnancy and Delivery-related Complications, MediShield Life Benefits, MediShield Life Benefits

### Community 182 - "contracts.py"
Cohesion: 0.10
Nodes (25): Advice, Answering, Category, FieldSpec, Grounding, Guardrails, ModuleTrigger, Persona (+17 more)

### Community 183 - "Understanding integrated shield plans"
Cohesion: 0.29
Nodes (6): Are you covered?, Should you upgrade to an IP?, The deductible is the fixed amount you pay each policy year – ranging from $1,500 to $3,500, depending on ward class – before any payout from your IP. The co-payment is 5% of the bill, capped at a minimum of $6,000 per year., Understanding integrated shield plans, Your budget, Your comfort level with the types of hospitals, wards and doctors

### Community 184 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.13
Nodes (14): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here, yew-mun/README.md, Done (+6 more)

### Community 185 - "test_a_citation_that_resolves_to_nothing_still_says_what_it_said"
Cohesion: 0.25
Nodes (8): Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with…, Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with ev, A deleted document must not take the sentence down with it., A deleted document must not take the sentence down with it., test_a_citation_that_resolves_to_nothing_still_says_what_it_said(), test_an_alerts_citation_carries_the_document_it_opens(), test_today_is_ordered_overdue_then_alerts_then_reminders(), uncovered_since()

### Community 186 - "About Integrated Shield Plan"
Cohesion: 0.33
Nodes (5): About Integrated Shield Plan, How do I find out if I have an Integrated Shield Plan?, How do Integrated Shield Plan premiums and claims work?, Should I consider purchasing an Integrated Shield Plan?, What is an Integrated Shield Plan?

### Community 187 - "Premium and Subsidy Tables"
Cohesion: 0.33
Nodes (5): MediShield Life Premium Schedule for Singapore Citizens and Permanent Residents, Merdeka Generation Subsidy, Pioneer Generation Subsidy, Premium and Subsidy Tables, Premium Subsidy for the Lower- to Middle-Income

### Community 188 - "16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.10
Nodes (19): 14 · A pack supplies what the core knows about a domain, and the core stays generic, Alternatives considered, Consequences, Context, Decision, Revisit when, 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent, Addendum, 17 September 2026: coverage review and the adult rule (+11 more)

### Community 189 - "ReadingEvent"
Cohesion: 0.40
Nodes (5): One sentence that has passed the gate, with the sources it passed on. It will…, One sentence that has passed the gate, with the sources it passed on.      It wi, Evidence gathered and good enough to answer from. Nothing has been claimed yet., ReadingEvent, SentenceEvent

### Community 192 - "0002_household.sql"
Cohesion: 0.70
Nodes (4): document_attribution, people, person_aliases, telegram_identities

### Community 194 - "0003_advice.sql"
Cohesion: 0.60
Nodes (4): advice_consents, advice_records, grounding_sources, grounding_values

### Community 195 - "1. Record architecture decisions"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 196 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 197 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 199 - "installed_packs"
Cohesion: 0.22
Nodes (9): installed_packs(), Every pack directory holding a pack.yaml, in a stable order. Directories whose…, Every pack directory holding a pack.yaml, in a stable order.      Directories wh, test_every_installed_pack_still_loads(), test_every_pack_speaks_only_for_catalogue_types(), test_every_document_type_has_a_generated_model(), test_the_template_directory_is_not_an_installed_pack(), A pack naming a metric nobody implemented is a silent no-op, so it is caught… (+1 more)

### Community 200 - "models.py"
Cohesion: 0.09
Nodes (21): AbstentionEvent, AskRequest, CloseRequest, EnabledRequest, FinishedEvent, HouseholdResponse, ModuleSummary, PacksResponse (+13 more)

### Community 205 - "Claim"
Cohesion: 0.67
Nodes (3): Claim, One sentence and the passages it was traced to. Never emitted without…, One sentence and the passages it was traced to. Never emitted without `citations

### Community 206 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 208 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 209 - "Data inventory — identity data, dates of birth and loans"
Cohesion: 0.40
Nodes (4): Data inventory — identity data, dates of birth and loans, Open questions for Siew, The inventory, What this entry covers

### Community 210 - "eslint.config.mjs"
Cohesion: 0.50
Nodes (3): @eslint/eslintrc, compat, eslintConfig

### Community 211 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 212 - "generate_lim_documents.py"
Cohesion: 0.50
Nodes (4): find_browser_executable(), generate_documents(), Project Parrot - Synthetic Document Generator for Lim Household ===============, Find Microsoft Edge or Google Chrome executable on Windows.

### Community 213 - "usable"
Cohesion: 0.40
Nodes (3): Drop rows a calculator cannot use, before deciding whether anything is missing.…, Drop rows a calculator cannot use, before deciding whether anything is missing., usable()

### Community 216 - "5. The watched folder is polled for stability, not subscribed to for events"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 218 - "_meets_calculation"
Cohesion: 0.07
Nodes (39): AdviceShape, One kind of advice question, and everything its calculator needs to answer it., One kind of advice question, and everything its calculator needs to answer it., Adviser, Calculation, ConsentBook, What a calculator returns, and what the graph needs to ask consent and keep a…, Implemented by `HouseholdConsents` in `core/advice_consent.py`. (+31 more)

### Community 221 - "test_asking_whether_something_can_be_claimed_is_described_as_explain_to_the_router"
Cohesion: 0.67
Nodes (3): 14 September: "warded for dengue 3 days, can claim?" was declined as advice…, 14 September: "warded for dengue 3 days, can claim?" was declined as advice beca, test_asking_whether_something_can_be_claimed_is_described_as_explain_to_the_router()

### Community 222 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

### Community 224 - "createPseudoSheet"
Cohesion: 0.67
Nodes (4): createPseudoSheet(), importantify(), scanUnquotedUrl(), stripComments()

### Community 232 - "test_help_runs_without_importing_core_before_sys_path_is_set"
Cohesion: 0.67
Nodes (3): `--help` must work even though `core` is not on `sys.path` until the script…, `--help` must work even though `core` is not on `sys.path` until the script inse, test_help_runs_without_importing_core_before_sys_path_is_set()

### Community 233 - "test_an_unscoped_result_is_not_empty_for_the_owner"
Cohesion: 0.67
Nodes (3): `empty_for_owner` must never fire on a question that was never scoped —…, `empty_for_owner` must never fire on a question that was never scoped — otherwis, test_an_unscoped_result_is_not_empty_for_the_owner()

### Community 234 - "test_each_policy_lapses_on_its_own"
Cohesion: 0.67
Nodes (3): A live travel policy must not make a lapsed motor policy read as covered., A live travel policy must not make a lapsed motor policy read as covered., test_each_policy_lapses_on_its_own()

### Community 236 - "ConfirmNameRequest"
Cohesion: 0.67
Nodes (3): ConfirmNameRequest, The answer to "who is this?". Either an existing person, or a new one to create., The answer to "who is this?". Either an existing person, or a new one to create.

### Community 237 - "CorrectionRequest"
Cohesion: 0.67
Nodes (3): CorrectionRequest, What the person typed. The pack decides what type it is; the caller does not…, What the person typed. The pack decides what type it is; the caller does not get

### Community 238 - "CorrectionResponse"
Cohesion: 0.67
Nodes (3): CorrectionResponse, What changed, in the words the screen confirms it with. `was` is returned…, What changed, in the words the screen confirms it with.      `was` is returned r

### Community 239 - "DeclinedEvent"
Cohesion: 0.67
Nodes (3): DeclinedEvent, A request for a recommendation or a judgement, declined by a pack without…, A request for a recommendation or a judgement, declined by a pack without advice

### Community 240 - "ObligationChanged"
Cohesion: 0.67
Nodes (3): ObligationChanged, The row is gone from Today. `speaks_again` is null when it will not come back.…, The row is gone from Today. `speaks_again` is null when it will not come back.

### Community 241 - "OwnerRequest"
Cohesion: 0.67
Nodes (3): OwnerRequest, First run: the name on your documents. One field, because the owner is the one…, First run: the name on your documents. One field, because the owner is the one p

### Community 242 - "PendingName"
Cohesion: 0.67
Nodes (3): PendingName, A name off a document that nobody has placed yet, and what the model thinks it…, A name off a document that nobody has placed yet, and what the model thinks it i

### Community 243 - "PlaceRequest"
Cohesion: 0.67
Nodes (3): PlaceRequest, How somebody already in the roster is related to the owner. The owner's own is…, How somebody already in the roster is related to the owner. The owner's own is `

### Community 244 - "Turn"
Cohesion: 0.67
Nodes (3): One earlier turn of the conversation. Read to make a follow-up whole; never…, One earlier turn of the conversation. Read to make a follow-up whole; never evid, Turn

## Knowledge Gaps
- **712 isolated node(s):** `npx`, `@modelcontextprotocol/server-filesystem`, `api/__init__.py`, `TodayItem`, `TodayResponse` (+707 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `InstalledPack` connect `client_for` to `pack`, `._compares_what_its_documents_declare`, `FakeConn`, `Ollama`, `Passage`, `values.py`, `FactRow`, `StreamingGraph`, `test_grounding_index.py`, `obligation`, `ValueRow`, `InstalledPack`, `install_best_effort`, `Alert`, `alert/__init__.py`, `advice/__init__.py`, `test_ingest_pipeline.py`, `ModelUnavailable`, `registry.py`, `test_advice_module.py`, `installed_packs`, `FakeCursor`, `test_answer_graph.py`, `_meets_calculation`, `FakeConn`, `DocumentCatalog`, `GroundingCorpus`, `PackManifest`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `Ollama` connect `Generated` to `FolderAdapter`, `run_parrot.py`, `ModelUnavailable`, `Ollama`, `HouseholdConsents`, `values.py`, `Zee — task list`, `test_reindexing_replaces_chunks_and_leaves_facts_alone`, `test_runtime.py`, `Registration`, `test_worker_queue.py`, `test_grounding_index.py`, `TelegramAdapter`, `FolderCapture`, `test_ingest_pipeline.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `ModelUnavailable` connect `Generated` to `Christian — task list`, `ModelUnavailable`, `Ollama`, `Passage`, `FakeCursor`, `_Value`, `values.py`, `Zee — task list`, `test_reindexing_replaces_chunks_and_leaves_facts_alone`, `test_runtime.py`, `test_answer_graph.py`, `test_grounding_values.py`, `test_grounding_index.py`, `household.py`, `events`, `test_ingest_pipeline.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 62 inferred relationships involving `InstalledPack` (e.g. with `DocumentCatalog` and `DocumentTypeSpec`) actually correct?**
  _`InstalledPack` has 62 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `FakeConn` (e.g. with `HouseholdConsents` and `HouseholdAdviceLog`) actually correct?**
  _`FakeConn` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 36 inferred relationships involving `Passage` (e.g. with `AdviceLog` and `AdviceRecord`) actually correct?**
  _`Passage` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `ScriptedOllama` (e.g. with `Claim` and `Holding`) actually correct?**
  _`ScriptedOllama` has 15 INFERRED edges - model-reasoned connections that need verification._