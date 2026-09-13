# Graph Report - igd-capstone-2026  (2026-09-13)

## Corpus Check
- 0 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2644 nodes · 5237 edges · 178 communities (160 shown, 18 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 378 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `247d1e26`
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
- page.tsx
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
- ConfigurationError
- FakeCursor
- vault/page.tsx
- household/page.tsx
- [...path]/route.ts
- test_a_failure_after_the_stream_started_arrives_as_an_event
- test_one_document_is_shown_even_when_its_pack_is_off
- The team
- system/route.ts
- Christian — Lane A · Integration and product owner
- Siew — Lane C · Governance and assurance
- Exception
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- models.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 132 edges
2. `build_router()` - 65 edges
3. `Ollama` - 57 edges
4. `FakeConn` - 56 edges
5. `client_for()` - 49 edges
6. `settings()` - 49 edges
7. `rows_for()` - 48 edges
8. `Passage` - 46 edges
9. `ingest/quarantine.py` - 41 edges
10. `ModelUnavailable` - 35 edges

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

## Communities (178 total, 18 thin omitted)

### Community 0 - "ingest/quarantine.py"
Cohesion: 0.12
Nodes (20): Chunk, What is actually embedded: the prefix plus the text, matching the tsvector…, ExtractedFact, Extraction, fixed(), from_facts(), _label(), Turn a dated fact into a commitment to do something about it. A fact is a… (+12 more)

### Community 1 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.20
Nodes (8): packs/page.tsx, dynamic, metadata, PacksPage(), runtime, ModuleSummary, packs(), PackSummary

### Community 2 - "README.md"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.09
Nodes (38): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), Validate a document register before it is handed over. python -m…, Parse `field_pages`: semicolon-separated `name=page`, 1-based. Empty means page… (+30 more)

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
Cohesion: 0.23
Nodes (13): document_title(), The document as a person would name it: its `string` fields as read, in the…, ingest/quarantine.py, The second stage of quarantine: the page image, read by the vision-language…, Ask the vision-language model to read the pages. One request per page, so a…, Send the pages as images and try the whole pack pipeline again on what comes…, The reportable line. Deliberately a rate and a count, because a rate over three…, Recovery (+5 more)

### Community 8 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (11): running-the-eval-harness/SKILL.md, Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness (+3 more)

### Community 9 - "Christian — task list"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 10 - "Desmond — task list"
Cohesion: 0.18
Nodes (11): Desmond — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 11 - "Siew — task list"
Cohesion: 0.20
Nodes (10): zee/tasks.md, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+2 more)

### Community 12 - "Yew Mun — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

### Community 13 - "Zee — task list"
Cohesion: 0.13
Nodes (15): 1 · Install five things, 2 · Download the AI models, 3 · Get the code and set it up, 4 · Put some documents in, 5 · Run it, 6 · Use it, Ask — a question about your own documents, If something goes wrong (+7 more)

### Community 14 - "Filling the corpus register"
Cohesion: 0.20
Nodes (10): filling-the-corpus-register/SKILL.md, Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one (+2 more)

### Community 15 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (10): writing-a-governance-artefact/SKILL.md, Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six (+2 more)

### Community 16 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.33
Nodes (5): Before you say you are done, Claude Code — read this first, Finding your way around, Skills and commands, The three things agents get wrong here

### Community 17 - "test_worker_queue.py"
Cohesion: 0.11
Nodes (28): The one interface every capture channel satisfies. receive(payload, mime,…, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, sha256(), Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker. Celery is imported here rather…, index_folder(), Find the bytes behind a registered document again. v1 keeps the inbox as the… (+20 more)

### Community 18 - "Zee — Lane D · Domain packs and interface"
Cohesion: 0.22
Nodes (9): Half one — domain packs (weeks 1 to 7), Half two — the interface (weeks 4 to 8), Read this first, Rules that apply to you specifically, The two halves of this lane, What "done" looks like, What you present, Your Claude Code skills (+1 more)

### Community 19 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (8): authoring-a-domain-pack/SKILL.md, Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 20 - "Household canon"
Cohesion: 0.25
Nodes (7): Address, Employment, Household canon, Life events that documents must reflect, People, Policies, Vehicles

### Community 21 - "Registration"
Cohesion: 0.08
Nodes (20): What happens to a document between "these bytes are registered" and "this…, Put one ingestion message on the queue and return its task id., Send, ingest/__init__.py, The ingestion worker. Capture registers a document; this package turns it into…, What every capture channel hands a document to. An adapter's job ends at "these…, An already-indexed document is not read again. Re-reading it would burn a…, Outcome (+12 more)

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

### Community 27 - "`core/retrieve/` — hybrid retrieval"
Cohesion: 0.50
Nodes (4): retrieve/README.md, `core/retrieve/` — hybrid retrieval, Rules, What belongs here

### Community 28 - "Graphify — the shared knowledge graph"
Cohesion: 0.20
Nodes (9): Graphify — the shared knowledge graph, Keeping it fresh, Merge conflicts, solved properly, Setup, once per clone, The hook leaves your tree dirty. Amend it into the commit you just made., Two kinds of extraction, and which needs what, Using it, What is committed, and what is not (+1 more)

### Community 29 - "build_router"
Cohesion: 0.10
Nodes (32): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, QuarantinedDocument, QuarantineResponse, What changed, in the words the screen confirms it with. `was` is returned… (+24 more)

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

### Community 37 - "Evaluation"
Cohesion: 0.40
Nodes (5): eval/README.md, Evaluation, Ground truth comes free, The honesty check, Writing questions

### Community 38 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 39 - "Grounding corpora"
Cohesion: 0.40
Nodes (5): grounding/README.md, Grounding corpora, Owner, Rules, Structure

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
Nodes (4): governance/README.md, `docs/governance/` — the assurance artefacts, The autonomy statement in one line, The rule that governs all eight

### Community 51 - "contracts.py"
Cohesion: 0.11
Nodes (25): What the graph needs from retrieval, stated as a contract rather than an…, is_first_person(), Whose question is this, and whose documents may answer it. "What is my term…, `(word, relation)` when the question asks about a relation's own documents,…, Whether this question is about the person asking. `other_names` are the display…, relation_asked(), _conn_returning(), _passage() (+17 more)

### Community 52 - "`docs/report/` — the final report"
Cohesion: 0.10
Nodes (20): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model (+12 more)

### Community 53 - "Passage"
Cohesion: 0.16
Nodes (14): One streamed sentence object, turned into the thing the gate understands. The…, check(), check_one(), Claim, The grounding gate. Rule 3 in AGENTS.md: no claim without a citation. This…, Never raises, never rewrites a claim. It keeps, drops, or abstains. The whole-…, Why this one sentence cannot be kept, or `None` if it can. Depends on nothing…, Verdict (+6 more)

### Community 54 - "test_modules.py"
Cohesion: 0.19
Nodes (18): already_said(), True when this exact window has already been mentioned. The comparison is by…, Everything inside a lead window that has not already been said for that window.…, sweep(), obligation_row(), Reminder and Alert: what fires, once, and with what behind it. Both modules are…, A sweep for a date in the future must record that date, or it repeats itself., A pack naming a metric nobody implemented is a silent no-op, so it is caught… (+10 more)

### Community 55 - "main.py"
Cohesion: 0.14
Nodes (18): The local API. Liveness is intentionally separate from assistant readiness.…, The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), capture_check(), Check, collect_checks(), database_check() (+10 more)

### Community 56 - "IngestJob"
Cohesion: 0.09
Nodes (21): CaptureAdapter, IngestJob, What a capture returns: a registered document, and whether we had seen it…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., adapters/__init__.py, Capture adapters. Every channel a document can arrive through satisfies one…, _attachment(), The Telegram capture adapter. Same interface as the folder: `receive(payload,… (+13 more)

### Community 57 - "export-design-preview.cjs"
Cohesion: 0.11
Nodes (17): bundle(), classes, css, cssFile, domId, fs, ids, licences (+9 more)

### Community 58 - "cli.py"
Cohesion: 0.23
Nodes (19): build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest(), cmd_init() (+11 more)

### Community 59 - "register_document"
Cohesion: 0.26
Nodes (13): alert/__init__.py, _citations(), cpf_contributions_ytd(), days_uncovered(), donations_ytd(), Measurement, The Alert module: a pack-declared threshold, crossed once, citing the documents…, Days since cover lapsed, per insured person. Zero while a policy still runs. (+5 more)

### Community 60 - "Settings"
Cohesion: 0.11
Nodes (38): client(), client_for(), open_obligation(), pack_row(), The point of the endpoint. An UPDATE alone loses the example we are trying to…, Snooze means 'not until this gets more urgent', so it can name the day it does., No new column: `already_said` is what makes the row quiet, and it reads this…, A client whose database is `conn`. `base_url` is loopback because… (+30 more)

### Community 61 - "InstalledPack"
Cohesion: 0.11
Nodes (32): page_images(), Base64 page images, in page order. Empty when this document cannot be rendered.…, page_count(), PageUnavailable, _pdfium(), One page of one document, as an image. Two callers want the same thing for…, Safe to show a person: there is no such page, or this file cannot be drawn., Safe to show a person: this install cannot render PDF pages at all. (+24 more)

### Community 62 - "test_ingest_pipeline.py"
Cohesion: 0.16
Nodes (18): extract(), Never raises. A failure is a reason, and a reason routes the document to…, FakeOllama, Answers whatever the test told it to, and records what it was asked., test_a_date_that_cannot_be_read_still_quarantines(), test_a_long_document_whose_front_is_enough_is_read_once(), test_a_long_document_whose_front_is_not_enough_is_read_in_full(), test_a_null_shaped_string_in_a_required_field_is_still_a_failure() (+10 more)

### Community 63 - "pipeline.py"
Cohesion: 0.09
Nodes (32): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+24 more)

### Community 64 - "FolderAdapter"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 65 - "parse.py"
Cohesion: 0.10
Nodes (19): Block, DoclingParser, _kind(), _pages_from(), Parser, PlainTextParser, Turn captured bytes into pages of text, or say why it could not be done. Every…, Docling, held at arm's length: imported on first use, and never at module… (+11 more)

### Community 66 - "install_best_effort"
Cohesion: 0.33
Nodes (9): Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), FakeConn, FakePack, test_a_firing_older_than_the_debounce_window_fires_again(), test_a_metric_no_query_defines_cannot_fire(), test_a_recent_firing_is_debounced(), test_a_threshold_crossing_fires_with_the_document_behind_it() (+1 more)

### Community 67 - "installed_packs"
Cohesion: 0.13
Nodes (19): document_types(), installed_packs(), InstalledPack, _load_one(), pack(), PackUnavailable, Load the installed packs at runtime. A pack is authored as one YAML file and…, A pack's YAML and its generated schemas disagree, or the pack does not exist. (+11 more)

### Community 68 - "registry.py"
Cohesion: 0.09
Nodes (30): installed_modules(), InstalledModule, manifest(), ModuleUnavailable, Load the installed capability modules at runtime. The mirror of…, A module's YAML is missing, or does not validate against `ModuleManifest`., One module's manifest, validated. Raises rather than returning a partial object., Every module directory holding a `module.yaml`, in a stable order. Directories… (+22 more)

### Community 69 - "Ollama"
Cohesion: 0.12
Nodes (25): blocked_reasons(), forget(), QuarantinedDocument, queue(), Per document: `None` when the image pass can run, or the sentence saying why it…, Safe to show. Forgetting a document whose file is still there would not last., Remove a quarantined document from Parrot's memory. Its name, or `None` if…, What is waiting for a person's eyes, oldest first. (+17 more)

### Community 70 - "README.md"
Cohesion: 0.14
Nodes (16): christian/README.md, christian/tasks.md, desmond/README.md, desmond/tasks.md, team/README.md, Everyone, regardless of lane, The dependency that sets the order, The presentation split (+8 more)

### Community 71 - "ingest.py"
Cohesion: 0.24
Nodes (10): A document and a page, as a person would cite it., Source, TodayItem, TodayResponse, today(), _cite(), _link(), Split a formatted citation back into its parts, keeping the text either way.… (+2 more)

### Community 72 - "obligations.py"
Cohesion: 0.11
Nodes (17): design-preview/page.tsx, metadata, answers, DesignPreview(), Direction, directions, Item, items (+9 more)

### Community 73 - "extract.py"
Cohesion: 0.27
Nodes (13): Configuration for PaperBrain. Everything is local. Nothing in this file should…, paperbrain/extract.py, extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file() (+5 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (16): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+8 more)

### Community 75 - "answer.py"
Cohesion: 0.09
Nodes (25): _asked(), Citation, _conversation(), fuse(), _numbered(), _pack_for(), Router → retrieve → rerank → decide → answer, one verified sentence at a time.…, What the graph carries. It ends at the evidence; the answer is streamed, not… (+17 more)

### Community 76 - "FolderAdapter"
Cohesion: 0.12
Nodes (27): Magic bytes first, filename suffix second, `application/octet-stream` last. A…, sniff_mime(), FolderAdapter, _Pending, The watched-folder capture adapter. A person drops a scan into a folder and it…, Every file in the watched folder that is worth looking at at all., Advance the debounce by `elapsed` seconds and return the files now ready. Time…, One debounce tick, then register whatever it declared ready. (+19 more)

### Community 77 - "Notion"
Cohesion: 0.25
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "State"
Cohesion: 0.18
Nodes (17): enabled_pack_ids(), enabled_packs(), The packs left switched on, or `None` when nothing has been installed yet.…, The installed packs a person has left switched on, as loaded pack objects. This…, The work the queue carries: read a document, retry quarantine, sweep the two…, One document, by id. The interface's Retry button lands here through the broker., Attach the tasks to a Celery application and return it., register() (+9 more)

### Community 79 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.14
Nodes (14): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+6 more)

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (8): paperbrain/README.md, How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 83 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 84 - "FakeConn"
Cohesion: 0.11
Nodes (33): FolderSettings, Dispatcher, Inline, Given a registered document, arrange for it to be read. Says what it arranged., Run the pipeline here and now, and report what it decided., Intake, FolderCapture, Run the folder capture loop in a background thread, beside the local server.… (+25 more)

### Community 85 - "test_startup.py"
Cohesion: 0.06
Nodes (51): Load the generator and the embedder before the first question, and record the…, warm_models(), broker_available(), Whether Redis answers. Not whether a worker is listening —…, _kill_tree(), main(), open_browser(), parse_args() (+43 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "run_parrot.py"
Cohesion: 0.27
Nodes (9): ingest/chunk.py, _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, The page as `(is_heading, line)`, from the parser's structure when it has any., A line, in pieces no longer than the target, broken at sentences and then at… (+1 more)

### Community 89 - "routes.py"
Cohesion: 0.25
Nodes (8): next, [id]/page.tsx, DocumentPage(), dynamic, metadata, runtime, document(), nextConfig

### Community 90 - "lock.ts"
Cohesion: 0.16
Nodes (23): auth/route.ts, dynamic, GET(), grant(), POST(), runtime, Accepted, clearFailures() (+15 more)

### Community 91 - "application"
Cohesion: 0.12
Nodes (21): lifespan(), install_best_effort(), Install at startup without being able to stop startup. Both processes that own…, application(), The configured application with its tasks registered. One per process., Return something that puts one ingestion message on the queue and yields its…, Put one quarantine retry on the queue and return its task id. The vision pass…, send_retry() (+13 more)

### Community 92 - "build.py"
Cohesion: 0.20
Nodes (15): _class_name(), _docstring(), _field_line(), load(), main(), Generate everything downstream of a pack.yaml. python -m packs.build #…, The header row Desmond fills in, one file per pack. Long format: one row per…, The header a batch register starts from: every field of every installed pack. A… (+7 more)

### Community 93 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 94 - "ingest/extract.py"
Cohesion: 0.14
Nodes (18): ingest/extract.py, _coerce(), _date_renderings(), decode_schema(), _drop_format(), _normalise(), _prepare(), printed_date() (+10 more)

### Community 102 - "schedule.py"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "PackManifest"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 104 - "._client"
Cohesion: 0.10
Nodes (16): runtime/ollama.py, Generated, ModelUnavailable, The one client that talks to Ollama. Everything the platform infers goes…, A question, embedded the way the model was trained to embed a search query., Passages as `(title, text)`, embedded the way the model was trained to embed a…, Load the generator and the embedder now, and say where the generator landed. An…, Generate against a JSON schema. This is how extraction is held to a pack's… (+8 more)

### Community 105 - "Contributing"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 107 - "worker.py"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 108 - "base.py"
Cohesion: 0.14
Nodes (13): react, Toggle(), SourceChip(), SourcePanel(), DocumentDetail(), when(), Field(), format() (+5 more)

### Community 109 - ".load"
Cohesion: 0.10
Nodes (33): create_app(), checks(), ready(), setup(), system_status(), ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one…, Settings (+25 more)

### Community 110 - "Ollama"
Cohesion: 0.08
Nodes (32): _columns(), correct(), Corrected, CorrectionRejected, A person fixing a field the extractor got wrong. This is the one place in the…, `(value_text, value_num, value_date)` — exactly one of them set. The declared…, Store what a person says this field actually says, and keep what it used to…, Safe to show: there is no fact with that id. (+24 more)

### Community 111 - "Intake"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 112 - "test_answer_graph.py"
Cohesion: 0.11
Nodes (31): Abstained, build(), events(), passage(), The grounding gate, and the graph's two ways of not answering. Rule 3 says no…, The promise the Ask surface is built on. Two sentences, two separate events, in…, Nothing is added afterwards, so a chip can never appear late or change., Not yielded and then withdrawn — never yielded. There is no retraction event by… (+23 more)

### Community 113 - "PackManifest"
Cohesion: 0.14
Nodes (11): Action, CONFIRM, ITEMS, PowerMenu(), Stage, DependencyCheck, Phase, RestartingScreen() (+3 more)

### Community 114 - "test_household.py"
Cohesion: 0.07
Nodes (44): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), owner(), owner_aliases(), pending() (+36 more)

### Community 115 - "Cursor"
Cohesion: 0.16
Nodes (20): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a…, paperbrain/db.py, load_matrix(), pack(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.…, Return (N x D matrix of normalised embeddings, chunk ids)., stats() (+12 more)

### Community 116 - "_today_items"
Cohesion: 0.24
Nodes (9): Classification, classify(), _prompt(), Decide which pack's document type a captured document is, or decline to. The…, Never raises. An unavailable model is a classification failure, so it…, _schema(), test_a_document_no_pack_recognises_is_not_forced_into_one(), test_a_low_confidence_classification_is_refused() (+1 more)

### Community 117 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 118 - "6 · Use it"
Cohesion: 0.11
Nodes (25): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor.…, What the person asked for, once. The first request wins; later ones change…, _client(), _eventually(), _launcher(), quiet_engine(), Restart and shut down: the engine asks its supervisor, and nothing else can ask… (+17 more)

### Community 120 - "app/layout.tsx"
Cohesion: 0.22
Nodes (8): next-themes, app/layout.tsx, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 121 - "ports.py"
Cohesion: 0.16
Nodes (12): AnswerGraph, Built once, asked many times. Holds no connection: retrieval does., Routing and evidence. The answering is not a node — it yields, and a node…, Every event, collected. `scripts/ask.py` and the screen ask the same question…, graph/__init__.py, The answer graph. Router, retrieve, rerank, grounding gate, then answer or…, Implemented by `core/retrieve/` when Lane B's hybrid search lands. `candidates`…, A cross-encoder, scoring question against passage. Returns the best `keep`,… (+4 more)

### Community 122 - "item-row.tsx"
Cohesion: 0.24
Nodes (10): countdown(), detail(), figure(), ItemRow(), longDate(), sentence(), TONE, WORD (+2 more)

### Community 123 - "SentenceScanner"
Cohesion: 0.10
Nodes (27): Pulling finished sentences out of a JSON reply that is still being written. The…, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner, drip() (+19 more)

### Community 124 - "__init__.py"
Cohesion: 0.13
Nodes (18): reminder/__init__.py, close(), current_lead(), next_window(), Overdue, The Reminder module: a nightly sweep of obligations, and nothing fires twice.…, Past their date and never closed. A different problem from a reminder, shown…, Safe to show: there is no obligation with that id, or it is already closed. (+10 more)

### Community 125 - "Household canon"
Cohesion: 0.08
Nodes (24): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, Policies, The family tree, and why three of them are not called Lim (+16 more)

### Community 126 - "answer.tsx"
Cohesion: 0.13
Nodes (11): @ai-sdk/react, ask/page.tsx, metadata, Abstention(), Part, sentence(), textOf(), ADR-0011 (+3 more)

### Community 127 - "page.tsx"
Cohesion: 0.11
Nodes (11): Motion(), ROWS, tokens/page.tsx, INKS, metadata, RADII, SCALE, SECTIONS (+3 more)

### Community 128 - "Ollama"
Cohesion: 0.20
Nodes (10): paperbrain/ask.py, answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, paperbrain/ollama.py, Ollama, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.… (+2 more)

### Community 129 - "answer.tsx"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 130 - "blocked_reasons"
Cohesion: 0.23
Nodes (13): ai, chat/route.ts, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+5 more)

### Community 131 - "ingest.py"
Cohesion: 0.24
Nodes (12): paperbrain/chunk.py, Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks. Paperwork is short and…, _split_page(), guess_date(), guess_type() (+4 more)

### Community 132 - "enabled_pack_ids"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 134 - "api.ts"
Cohesion: 0.12
Nodes (17): RELATION_CHOICES, Place, PLACES, ALWAYS_EXISTS, AskResponse, Claim, HouseholdResponse, PacksResponse (+9 more)

### Community 135 - "test_api.py"
Cohesion: 0.10
Nodes (20): Answer, Cited, One sentence and the passages it was traced to. What rule 3 looks like as data.…, FakeGraph, graph(), inbox(), The five endpoints, against a fake database and the real queries. The…, Stands in for `AnswerGraph` at the seam `api/routes.py` owns. (+12 more)

### Community 136 - "today/page.tsx"
Cohesion: 0.11
Nodes (21): today/page.tsx, dynamic, isUrgent(), metadata, runtime, summary(), TodayPage(), vault/page.tsx (+13 more)

### Community 137 - "create_app"
Cohesion: 0.29
Nodes (4): Alert, _debounced(), What the debounce is keyed on: this metric, for this person, in this pack., test_the_debounce_key_separates_people()

### Community 138 - "page.tsx"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 139 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.25
Nodes (8): ModuleSummary, PacksResponse, PackSummary, _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack()

### Community 140 - "reindex_document"
Cohesion: 0.12
Nodes (15): parse(), The one call the pipeline makes. An unhandled mime type quarantines rather than…, ingest/reindex.py, indexed(), IndexedDocument, Rebuild a document's chunks and vectors without reading it again for facts.…, Safe to show: names what went wrong, never what the document says., Parse, chunk and embed one document again, and replace its chunks. Returns how… (+7 more)

### Community 141 - "Passage"
Cohesion: 0.15
Nodes (16): Passage, How a passage names itself: the document and the page, as a person would say it., The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting…, Keep the owner's passages and the household's; set aside everybody else's. A…, Keep the passages of these people and of the household; set aside everybody…, scope_passages(), scope_to() (+8 more)

### Community 142 - "date"
Cohesion: 0.09
Nodes (27): conn(), FakeConn, obligation(), overdue_row(), The parameters of the one statement containing `needle`. Fails loudly if it…, One row of `reminder.OVERDUE`, in its column order., Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with…, The nightly sweep owns `last_notified_at`. A screen refresh must not burn a… (+19 more)

### Community 143 - "(app)/layout.tsx"
Cohesion: 0.18
Nodes (12): lucide-react, (app)/layout.tsx, dynamic, runtime, LockButton(), SURFACES, TabBar(), Tabs() (+4 more)

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
Cohesion: 0.22
Nodes (12): beat_schedule(), cron_expressions(), crontab_from(), manifest(), When the nightly sweeps run, read from the modules' own manifests. A module…, A five-field cron expression as Celery understands it., The cron line for each swept module, by module id. Testable without Celery…, Rule 6's habit: a schedule is written down in one place, and that place is the… (+4 more)

### Community 151 - "ParsedPage"
Cohesion: 0.16
Nodes (24): chunk_pages(), One flat list of chunks, ordinal running across the whole document., classification_sample(), The text the classifier reads: the opening pages, labelled, within a fixed…, find_page(), The first page whose text contains this value. None means no page supports it.…, ParsedPage, _page_of_examples() (+16 more)

### Community 152 - "_as_response"
Cohesion: 0.12
Nodes (15): AskRequest, ErrorEvent, The stream broke after it began. A client cannot read an HTTP status by then., ask(), ask_stream(), events(), _graph_for(), _history() (+7 more)

### Community 153 - "Parser"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "Desmond — task list"
Cohesion: 0.33
Nodes (5): 12. Chunks follow the document's headings, and embeddings use the model's task prompts, Consequences, Context, Decision, Evidence

### Community 155 - "date"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 156 - "package.json"
Cohesion: 0.12
Nodes (14): class-variance-authority, clsx, postcss, react-dom, tailwind-merge, tailwindcss, @tailwindcss/postcss, @types/node (+6 more)

### Community 157 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

### Community 160 - "13. A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.33
Nodes (5): 13. A question is understood before it is searched, and scoped before it is cut, Consequences, Context, Decision, Evidence

### Community 161 - "Alert"
Cohesion: 0.17
Nodes (12): Finished, Everything that is only knowable once the last sentence is in., PassThroughReranker, PhrasingRetriever, Scores one passage differently depending on which phrasing found it., A sentence that passed the gate was true when it passed. Losing the connection…, test_a_follow_up_is_understood_from_the_conversation_and_answered_whole(), test_a_model_that_dies_mid_answer_keeps_what_it_already_proved() (+4 more)

### Community 162 - "github.md"
Cohesion: 0.50
Nodes (3): Last sync, Screen map, Updated in this project

### Community 163 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 165 - "ConfigurationError"
Cohesion: 0.12
Nodes (18): ConfigurationError, _folder(), local_url(), _port(), _positive(), Small, literal .env reader with environment overrides and loopback-only…, Safe to show to the user: messages never include configuration values., A context window is a number of tokens. A bad one is a configuration error, not… (+10 more)

### Community 166 - "FakeCursor"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 167 - "vault/page.tsx"
Cohesion: 0.29
Nodes (4): GoneRow(), QuarantineQueue(), QuarantineRow(), QuarantinedDocument

### Community 168 - "household/page.tsx"
Cohesion: 0.16
Nodes (11): household/page.tsx, dynamic, HouseholdPage(), metadata, runtime, OwnerForm(), Roster(), WhoIsThis() (+3 more)

### Community 170 - "[...path]/route.ts"
Cohesion: 0.29
Nodes (10): [...path]/route.ts, ALLOWED, Context, DELETE(), dynamic, forward(), GET(), PATCH() (+2 more)

### Community 171 - "test_a_failure_after_the_stream_started_arrives_as_an_event"
Cohesion: 0.15
Nodes (15): a_citation(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive…, No `reading` before it: the floor is checked before the model is asked anything., By then the 200 has been sent. An exception that only logged would leave a…, What a retrieved passage hands over: the sentence a person reads, and the id a…, sse() (+7 more)

### Community 172 - "test_one_document_is_shown_even_when_its_pack_is_off"
Cohesion: 0.22
Nodes (10): document_row(), fact_row(), filed_document(), v1 keeps the inbox as the document store, so this is a real state, not a fault., Following a citation must never end in a blank screen because a pack was…, test_a_document_whose_file_left_the_inbox_is_409_not_500(), test_a_page_comes_back_as_an_image(), test_a_page_that_does_not_exist_is_a_404_that_says_so() (+2 more)

### Community 174 - "The team"
Cohesion: 0.22
Nodes (9): AppLayout(), unlock/page.tsx, dynamic, metadata, runtime, UnlockPage(), UnlockForm(), isUnlocked() (+1 more)

### Community 175 - "system/route.ts"
Cohesion: 0.31
Nodes (9): system/route.ts, ACTIONS, dynamic, GET(), POST(), runtime, sameOrigin(), unlocked() (+1 more)

### Community 176 - "Christian — Lane A · Integration and product owner"
Cohesion: 0.29
Nodes (7): Also yours, Christian — Lane A · Integration and product owner, Starter prompt for your coding agent, Starter prompt: what can I actually pick up?, The five things you ship, Week 1, in order, What integration actually means here

### Community 177 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.29
Nodes (7): Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The autonomy statement, The six artefacts, Where governance touches the code

### Community 178 - "Exception"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 179 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

### Community 182 - "models.py"
Cohesion: 0.08
Nodes (42): AbstentionEvent, AskResponse, Claim, CloseRequest, ConfirmNameRequest, CorrectionRequest, EnabledRequest, FinishedEvent (+34 more)

## Knowledge Gaps
- **620 isolated node(s):** `Part`, `Place`, `AskResponse`, `Claim`, `HouseholdResponse` (+615 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `.load` to `test_api.py`, `date`, `Registration`, `build_router`, `ConfigurationError`, `test_a_failure_after_the_stream_started_arrives_as_an_event`, `test_one_document_is_shown_even_when_its_pack_is_off`, `contracts.py`, `models.py`, `main.py`, `Settings`, `pipeline.py`, `registry.py`, `Ollama`, `State`, `FakeConn`, `test_startup.py`, `application`, `._client`, `6 · Use it`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `Connection` connect `Cursor` to `cli.py`, `ingest.py`, `Registration`, `Cursor`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `SentenceScanner` connect `SentenceScanner` to `ports.py`, `answer.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 103 inferred relationships involving `Settings` (e.g. with `create_app()` and `build_router()`) actually correct?**
  _`Settings` has 103 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `build_router()` (e.g. with `AskRequest` and `AskResponse`) actually correct?**
  _`build_router()` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Ollama` (e.g. with `warm_models()` and `AnswerGraph`) actually correct?**
  _`Ollama` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `client_for()` (e.g. with `Settings` and `fake_connection()`) actually correct?**
  _`client_for()` has 2 INFERRED edges - model-reasoned connections that need verification._