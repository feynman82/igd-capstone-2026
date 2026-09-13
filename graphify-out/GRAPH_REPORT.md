# Graph Report - igd-capstone-2026  (2026-09-13)

## Corpus Check
- 233 files · ~571,102 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2732 nodes · 5244 edges · 203 communities (156 shown, 47 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 322 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c9075c6c`
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
- PackManifest
- ingest.py
- Contributing
- FolderCapture
- worker.py
- base.py
- dispatch.py
- Ollama
- Intake
- _payload_for
- 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack
- Siew — Lane C · Governance and assurance
- Cursor
- retry_quarantine
- NNNN · The decision, as a statement not a question
- 6 · Use it
- __init__.py
- test_the_reminder_cron_is_read_from_its_manifest_not_written_twice
- test_alert_is_swept_nightly_even_though_its_manifest_says_fact_write
- __init__.py
- SentenceScanner
- __init__.py
- Household canon
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
- classify
- page.tsx
- 4. Local setup can run before the household assistant is ready
- reindex.py
- page.tsx
- date
- power-menu.tsx
- bytes_for
- README.md
- igd-capstone-2026
- FakeCursor
- Desmond — Lane E · Corpus and adversarial testing
- Ollama
- enabled_pack_ids
- Siew — Lane C · Governance and assurance
- Parser
- Desmond — task list
- date
- next.config.ts
- postcss.config.mjs
- test_the_real_packs_declare_metrics_that_exist
- Desmond — Lane E · Corpus and adversarial testing
- Working agreement for coding agents
- github.md
- ask.py
- 6 · Use it
- FIRST-RUN.md
- FakeCursor
- page.tsx
- page.tsx
- UnknownModule
- build
- test_a_failure_after_the_stream_started_arrives_as_an_event
- ask.py
- load_corpus.py
- The team
- Send
- 0002_household.sql
- Architecture decision records
- Exception
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- quiet_engine
- BaseModel
- Chunk
- Ollama
- Ollama
- ParsedPage
- Protocol
- Ollama
- ParsedDocument
- Ollama
- ParsedDocument
- Client
- date
- Exception
- Generated
- InstalledPack
- Person
- Popen
- TestClient
- ParsedPage
- TodayItem
- VaultDocument

## God Nodes (most connected - your core abstractions)
1. `Ollama` - 70 edges
2. `FakeConn` - 66 edges
3. `ModelUnavailable` - 50 edges
4. `rows_for()` - 49 edges
5. `client_for()` - 48 edges
6. `settings()` - 47 edges
7. `Settings` - 41 edges
8. `FakeOllama` - 34 edges
9. `FolderAdapter` - 31 edges
10. `extract()` - 30 edges

## Surprising Connections (you probably didn't know these)
- `test_a_claim_citing_the_same_document_twice_says_it_once()` --calls--> `Claim`  [INFERRED]
  tests/test_answer_graph.py → api/models.py
- `test_a_grounded_claim_renders_its_document_and_page()` --calls--> `Claim`  [INFERRED]
  tests/test_answer_graph.py → api/models.py
- `test_a_sentence_citing_a_passage_that_was_never_retrieved_is_dropped()` --calls--> `Claim`  [INFERRED]
  tests/test_answer_graph.py → api/models.py
- `test_a_sentence_with_no_supporting_passage_is_dropped()` --calls--> `Claim`  [INFERRED]
  tests/test_answer_graph.py → api/models.py
- `test_no_passages_at_all_abstains()` --calls--> `Claim`  [INFERRED]
  tests/test_answer_graph.py → api/models.py

## Import Cycles
- None detected.

## Communities (203 total, 47 thin omitted)

### Community 0 - "contracts.py"
Cohesion: 0.13
Nodes (21): Chunk, What is actually embedded: the prefix plus the text, matching the tsvector colum, Dispatcher, Protocol, What happens to a document between "these bytes are registered" and "this docume, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Send (+13 more)

### Community 1 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.15
Nodes (9): metadata, PacksPage(), Toggle(), EmptyState(), SHAPES, ModuleSummary, packs(), PackSummary (+1 more)

### Community 2 - "README.md"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.10
Nodes (41): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+33 more)

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
Cohesion: 0.07
Nodes (52): boot(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory(), createExternalModules() (+44 more)

### Community 10 - "Desmond — task list"
Cohesion: 0.17
Nodes (11): Desmond — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 11 - "Siew — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

### Community 12 - "Yew Mun — task list"
Cohesion: 0.10
Nodes (18): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation, W10 — due 2026-11-10 (+10 more)

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

### Community 17 - "igd-capstone-2026"
Cohesion: 0.09
Nodes (33): Inline, Any, Queued, Run the pipeline here and now, and report what it decided., Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker.      Celery is imported here ra, Intake, What every capture channel hands a document to.  An adapter's job ends at "these (+25 more)

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
Nodes (9): Graphify — the shared knowledge graph, Keeping it fresh, Merge conflicts, solved properly, Setup, once per clone, The hook leaves your tree dirty. Amend it into the commit you just made., Two kinds of extraction, and which needs what, Using it, What is committed, and what is not (+1 more)

### Community 29 - "`web/` — the interface"
Cohesion: 0.13
Nodes (17): Any, Who is asking, and whose documents may answer.  Two halves, deliberately split, `empty_for_owner` must never fire on a question that was never scoped — otherwis, The sentence that makes a wrong model guess cost a tap instead of a wrong answer, A second document must never silently move a name from one member to another., A daughter takes over her father's paperwork. The install follows., A fresh install is not broken. It answers about the household, as it always did., "What is Rachel's premium on my policy" is a question about Rachel.      A rel (+9 more)

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

### Community 51 - "Siew — task list"
Cohesion: 0.21
Nodes (13): FieldSpec, Grounding, Guardrails, ModuleTrigger, Persona, BaseModel, The two contracts the whole platform is built on.  Nothing else in the reposit, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer. (+5 more)

### Community 52 - "`docs/report/` — the final report"
Cohesion: 0.10
Nodes (19): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model (+11 more)

### Community 53 - "Passage"
Cohesion: 0.23
Nodes (11): check(), check_one(), Claim, precheck(), The grounding gate.  Rule 3 in AGENTS.md: no claim without a citation. This mo, Never raises, never rewrites a claim. It keeps, drops, or abstains.      The w, Is this evidence worth answering from at all? The reason to abstain, or `None`., Why this one sentence cannot be kept, or `None` if it can.      Depends on not (+3 more)

### Community 54 - "test_modules.py"
Cohesion: 0.18
Nodes (21): AlertConfig, FakeConn, FakePack, obligation_row(), date, datetime, Reminder and Alert: what fires, once, and with what behind it.  Both modules a, A sweep for a date in the future must record that date, or it repeats itself. (+13 more)

### Community 55 - "Settings"
Cohesion: 0.14
Nodes (26): AsyncClient, capture_check(), Check, collect_checks(), database_check(), interface_check(), model_check(), Read-only dependency diagnostics; installation is never treated as inference val (+18 more)

### Community 56 - "Registrar"
Cohesion: 0.09
Nodes (30): Client, _attachment(), Any, Client, datetime, RuntimeError, The Telegram capture adapter.  Same interface as the folder: `receive(payload,, Confirm the token works before anything else is attempted. (+22 more)

### Community 57 - "retrieve.py"
Cohesion: 0.18
Nodes (11): Classification, classification_sample(), classify(), _prompt(), Ollama, ParsedPage, Decide which pack's document type a captured document is, or decline to.  The, The text the classifier reads: the opening pages, labelled, within a fixed budge (+3 more)

### Community 58 - "cli.py"
Cohesion: 0.18
Nodes (19): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+11 more)

### Community 59 - "register_document"
Cohesion: 0.11
Nodes (22): CaptureAdapter, datetime, Protocol, The one interface every capture channel satisfies.      receive(payload, mime, s, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256` i, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sha256(), Capture adapters.  Every channel a document can arrive through satisfies one int (+14 more)

### Community 60 - "FolderCapture"
Cohesion: 0.09
Nodes (56): client_for(), conn(), FakeConn, filed_document(), inbox(), open_obligation(), pack_row(), Path (+48 more)

### Community 61 - "InstalledPack"
Cohesion: 0.10
Nodes (34): page_count(), PageUnavailable, _pdfium(), Any, LookupError, RuntimeError, One page of one document, as an image.  Two callers want the same thing for oppo, Safe to show a person: there is no such page, or this file cannot be drawn. (+26 more)

### Community 62 - "extract"
Cohesion: 0.11
Nodes (38): extract(), InstalledPack, Never raises. A failure is a reason, and a reason routes the document to quarant, FakeOllama, insurance(), iras(), _page_of_examples(), Any (+30 more)

### Community 63 - "pipeline.py"
Cohesion: 0.08
Nodes (34): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+26 more)

### Community 64 - "FolderAdapter"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 65 - "FolderCapture"
Cohesion: 0.10
Nodes (21): Block, DoclingParser, _kind(), _pages_from(), Parser, PlainTextParser, Turn captured bytes into pages of text, or say why it could not be done.  Every, Docling, held at arm's length: imported on first use, and never at module import (+13 more)

### Community 66 - "pipeline.py"
Cohesion: 0.38
Nodes (6): install(), install_best_effort(), Installed, What `install` did, so a startup line can say it in one sentence., Write every pack and module on disk into its table. Idempotent; never re-enables, Install at startup without being able to stop startup.      Both processes that

### Community 67 - "TelegramAdapter"
Cohesion: 0.22
Nodes (7): DocumentTypeSpec, One kind of document this pack recognises., document_types(), InstalledPack, _load_one(), Path, `"<pack>.<doc_type>"` -> (pack_id, spec). The classifier's whole candidate list.

### Community 68 - "ParsedPage"
Cohesion: 0.19
Nodes (16): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders somewhe, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, RuntimeError, Load the installed capability modules at runtime.  The mirror of `core/packs.py` (+8 more)

### Community 69 - "Ollama"
Cohesion: 0.07
Nodes (61): blocked_reasons(), forget(), page_images(), Any, Path, QuarantinedDocument, queue(), The second stage of quarantine: the page image, read by the vision-language mode (+53 more)

### Community 71 - "ingest.py"
Cohesion: 0.17
Nodes (19): Alert, _citations(), cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, Any (+11 more)

### Community 72 - "obligations.py"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 73 - "extract.py"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (16): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+8 more)

### Community 75 - "RUNNING.md"
Cohesion: 0.11
Nodes (34): Answer, Citation, Cited, Finished, _numbered(), _pack_for(), Event, InstalledPack (+26 more)

### Community 76 - "DoclingParser"
Cohesion: 0.14
Nodes (28): FolderAdapter, FolderSettings, Satisfies `CaptureAdapter`. Holds no database handle — it is given a `Registrar`, FolderCapture, A daemon thread that polls the watched folder until `stop()` or process exit., Begin watching. Returns False, with a logged reason, when it cannot., _loop(), main() (+20 more)

### Community 77 - "Notion"
Cohesion: 0.25
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "start_parrot.py"
Cohesion: 0.32
Nodes (7): main(), Path, Local-only startup preflight, using the standard library so setup can be diagnos, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file conte, report_hardware(), startup_gaps()

### Community 79 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.14
Nodes (14): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+6 more)

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (7): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 83 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 85 - "test_startup.py"
Cohesion: 0.13
Nodes (19): prepare_checkout(), Path, Startup tests do not ingest documents or need the corpus: they check process bou, npm is a wrapper around node. Killing only the wrapper orphans the port., The worker starts its nightly schedule as a process of its own. Terminating only, Stopping it signals its process group. Without a session of its own that group i, A developer's own `npm run dev` is used rather than fought for the port., `npm run dev` against an empty web/ fails slowly and cryptically. Say so instead (+11 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.14
Nodes (24): Load the generator and the embedder before the first question, and record the ou, warm_models(), Popen, _kill_tree(), main(), parse_args(), port_answers(), Any (+16 more)

### Community 89 - "Christian — Lane A · Integration and product owner"
Cohesion: 0.05
Nodes (83): AbstentionEvent, AskRequest, AskResponse, CloseRequest, ConfirmNameRequest, CorrectionRequest, CorrectionResponse, EnabledRequest (+75 more)

### Community 90 - "The team"
Cohesion: 0.09
Nodes (37): GET(), grant(), POST(), lastQuestion(), ParrotEvent, parseRecord(), POST(), readEvents() (+29 more)

### Community 91 - "1. Record architecture decisions"
Cohesion: 0.26
Nodes (12): Namespace, _beat_needs_its_own_process(), celery_argv(), main(), Any, Popen, Run the ingestion worker, and optionally the nightly schedule with it.      uv, The arguments the Celery command-line would have been given. Built here so a tes (+4 more)

### Community 92 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.14
Nodes (23): PackManifest, A domain pack, authored as one YAML file., _class_name(), _docstring(), _field_line(), load(), main(), Path (+15 more)

### Community 93 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 94 - "IngestJob"
Cohesion: 0.08
Nodes (32): _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact, _normalise(), _prepare(), printed_date() (+24 more)

### Community 102 - "schedule.py"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "PackManifest"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 104 - "ingest.py"
Cohesion: 0.08
Nodes (25): The page a person sees while Parrot starts, served by the engine itself.  **Why, The whole page. `screens_url` is escaped into a data attribute, never into scrip, render(), Safe to show. Forgetting a document whose file is still there would not last., StillInInbox, broker_available(), Run the folder capture loop in a background thread, beside the local server.  Th, Whether Redis answers. Not whether a worker is listening — `core/runtime/checks. (+17 more)

### Community 105 - "Contributing"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 106 - "FolderCapture"
Cohesion: 0.23
Nodes (11): HouseholdScope, What `AnswerGraph` is handed so it can scope without holding a connection., enabled_pack_ids(), enabled_packs(), The packs left switched on, or `None` when nothing has been installed yet., The installed packs a person has left switched on, as loaded pack objects., _ask(), main() (+3 more)

### Community 107 - "worker.py"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 109 - "dispatch.py"
Cohesion: 0.11
Nodes (31): create_app(), Settings, ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one t, _ollama_answering(), Any, MonkeyPatch, Path (+23 more)

### Community 110 - "Ollama"
Cohesion: 0.07
Nodes (42): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+34 more)

### Community 111 - "Intake"
Cohesion: 0.04
Nodes (45): ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes, postcss (+37 more)

### Community 112 - "_payload_for"
Cohesion: 0.06
Nodes (56): Claim, One sentence and the passages it was traced to. Never emitted without `citations, Abstained, AnswerGraph, Any, Passage, What the graph carries. It ends at the evidence; the answer is streamed, not sta, Built once, asked many times. Holds no connection: retrieval does. (+48 more)

### Community 113 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.16
Nodes (13): IngestJob, Magic bytes first, filename suffix second, `application/octet-stream` last., What a capture returns: a registered document, and whether we had seen it before, sniff_mime(), _Pending, datetime, Path, The watched-folder capture adapter.  A person drops a scan into a folder and i (+5 more)

### Community 114 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.10
Nodes (38): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+30 more)

### Community 115 - "Cursor"
Cohesion: 0.15
Nodes (22): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a, ndarray, load_matrix(), pack(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.  Des, Return (N x D matrix of normalised embeddings, chunk ids)., stats() (+14 more)

### Community 117 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 118 - "6 · Use it"
Cohesion: 0.15
Nodes (24): Lifecycle, What the person asked for, once. The first request wins; later ones change nothi, _client(), _eventually(), _launcher(), Path, TestClient, Restart and shut down: the engine asks its supervisor, and nothing else can ask (+16 more)

### Community 120 - "test_the_reminder_cron_is_read_from_its_manifest_not_written_twice"
Cohesion: 0.20
Nodes (8): archivo, figtree, jetbrains, metadata, outfit, spectral, viewport, ThemeProvider()

### Community 121 - "test_alert_is_swept_nightly_even_though_its_manifest_says_fact_write"
Cohesion: 0.24
Nodes (7): The answer graph.  Router, retrieve, rerank, grounding gate, then answer or abst, Protocol, What the graph needs from retrieval, stated as a contract rather than an import., Implemented by `core/retrieve/` when Lane B's hybrid search lands.      `candi, A cross-encoder, scoring question against passage. Returns the best `keep`, reor, Reranker, Retriever

### Community 122 - "__init__.py"
Cohesion: 0.27
Nodes (10): countdown(), detail(), figure(), ItemRow(), longDate(), sentence(), TONE, WORD (+2 more)

### Community 123 - "SentenceScanner"
Cohesion: 0.10
Nodes (28): Any, Pulling finished sentences out of a JSON reply that is still being written.  The, What document would have answered this, if the model said. Read once, at the end, Feed it deltas; it returns whichever sentences became complete because of them., Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes on, Find `"sentences": [` once. Everything before it is of no interest.          Sea, SentenceScanner (+20 more)

### Community 124 - "__init__.py"
Cohesion: 0.09
Nodes (27): already_said(), close(), current_lead(), Due, next_window(), Overdue, Any, date (+19 more)

### Community 125 - "Household canon"
Cohesion: 0.08
Nodes (23): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, Policies, The family tree, and why three of them are not called Lim (+15 more)

### Community 126 - "Finished"
Cohesion: 0.12
Nodes (13): metadata, Abstention(), Part, sentence(), textOf(), ADR-0011, Turn(), Conversation() (+5 more)

### Community 127 - "page.tsx"
Cohesion: 0.09
Nodes (12): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+4 more)

### Community 128 - "Ollama"
Cohesion: 0.24
Nodes (5): Ollama, OllamaUnavailable, RuntimeError, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.  Ta, Batch embeddings. Falls back to the legacy endpoint on old servers.

### Community 129 - "answer.tsx"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 131 - "ingest.py"
Cohesion: 0.24
Nodes (13): Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks.  Paperwork is short and stru, _split_page(), discover(), guess_date(), guess_type() (+5 more)

### Community 132 - "enabled_pack_ids"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 134 - "page.tsx"
Cohesion: 0.13
Nodes (19): ALWAYS_EXISTS, AskResponse, Claim, get(), HouseholdResponse, PacksResponse, PendingName, Person (+11 more)

### Community 135 - "api.ts"
Cohesion: 0.13
Nodes (22): DenseRetriever, client(), graph(), MonkeyPatch, TestClient, The five endpoints, against a fake database and the real queries.  The connect, Read as a statement: the upsert must not touch `enabled` on conflict., The setup page exists to say the database is missing. It cannot say it if it did (+14 more)

### Community 136 - "item-row.tsx"
Cohesion: 0.16
Nodes (7): isUrgent(), metadata, summary(), TodayPage(), Place, PLACES, WhoIsThis()

### Community 137 - "classify"
Cohesion: 0.47
Nodes (5): Field(), format(), isNumeric(), CorrectionResponse, VaultFact

### Community 138 - "page.tsx"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 140 - "reindex.py"
Cohesion: 0.15
Nodes (19): parse(), The one call the pipeline makes. An unhandled mime type quarantines rather than, pgvector accepts its own text form; this avoids registering an adapter for one c, _vector_literal(), indexed(), IndexedDocument, Any, RuntimeError (+11 more)

### Community 141 - "page.tsx"
Cohesion: 0.19
Nodes (10): is_first_person(), Any, Passage, Whose question is this, and whose documents may answer it.  "What is my term lif, Keep the owner's passages and the household's; set aside everybody else's., The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer.          The int, Whether this question is about the person asking.      `other_names` are the dis (+2 more)

### Community 142 - "date"
Cohesion: 0.14
Nodes (21): Decimal, document_row(), fact_row(), obligation(), overdue_row(), date, One row of `reminder.OVERDUE`, in its column order., Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with ev (+13 more)

### Community 143 - "power-menu.tsx"
Cohesion: 0.16
Nodes (11): Action, CONFIRM, ITEMS, PowerMenu(), Stage, DependencyCheck, Phase, RestartingScreen() (+3 more)

### Community 144 - "bytes_for"
Cohesion: 0.21
Nodes (13): bytes_for(), index_folder(), LookupError, Path, Find the bytes behind a registered document again.  v1 keeps the inbox as the, Safe to show: the bytes for this document are no longer anywhere we look., SHA-256 of every file sitting in the watched folder. The document row holds the, The payload for `digest`, found by hashing what is in the watched folder. (+5 more)

### Community 145 - "README.md"
Cohesion: 0.29
Nodes (7): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents

### Community 146 - "igd-capstone-2026"
Cohesion: 0.20
Nodes (10): Authoring a pack, igd-capstone-2026, `main` is not protected, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live (+2 more)

### Community 149 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.17
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 150 - "Ollama"
Cohesion: 0.21
Nodes (12): build(), Any, The one Celery application, built from `Settings`.  Every setting here is a cons, Construct the Celery application. Imported lazily by callers so that nothing whi, beat_schedule(), cron_expressions(), crontab_from(), manifest() (+4 more)

### Community 151 - "enabled_pack_ids"
Cohesion: 0.10
Nodes (27): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own st, One flat list of chunks, ordinal running across the whole document., The page as `(is_heading, line)`, from the parser's structure when it has any. (+19 more)

### Community 153 - "Parser"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "Desmond — task list"
Cohesion: 0.20
Nodes (8): 12. Chunks follow the document's headings, and embeddings use the model's task prompts, Consequences, Context, Decision, Evidence, Architecture decision records, Index, Writing one

### Community 155 - "date"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 159 - "test_the_real_packs_declare_metrics_that_exist"
Cohesion: 0.20
Nodes (14): installed_packs(), Every pack directory holding a pack.yaml, in a stable order.      Directories, enabled_module_ids(), _pack_row(), packs(), Any, One row of `packs`, with the manifest validated back out of its jsonb column., The modules left switched on, or `None` when nothing has been installed yet. (+6 more)

### Community 160 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.29
Nodes (8): DocumentPage(), metadata, ProblemState(), DocumentDetail(), when(), document(), pageImage(), VaultDocument

### Community 162 - "github.md"
Cohesion: 0.50
Nodes (3): Last sync, Screen map, Updated in this project

### Community 163 - "ask.py"
Cohesion: 0.31
Nodes (9): _conn_returning(), _passage(), The third bucket. Home contents, a utility bill — nobody's name on it, everybody, A joint policy is the owner's too. Presence wins over exclusion., Asked about my policy; the vault holds Rachel's. Say so, rather than answer hers, test_a_document_naming_the_owner_and_somebody_else_is_kept(), test_a_document_with_no_subject_belongs_to_everybody(), test_another_persons_documents_are_set_aside() (+1 more)

### Community 164 - "6 · Use it"
Cohesion: 0.29
Nodes (8): No row in `packs` with that id., No row in `modules` with that id., UnknownModule, UnknownPack, DatabaseUnavailable, RuntimeError, Safe to show: the message never carries the connection string., KeyError

### Community 165 - "FIRST-RUN.md"
Cohesion: 0.12
Nodes (23): TelegramSettings, ConfigurationError, _folder(), local_url(), _port(), _positive(), Path, Small, literal .env reader with environment overrides and loopback-only endpoint (+15 more)

### Community 166 - "FakeCursor"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 168 - "page.tsx"
Cohesion: 0.31
Nodes (6): HouseholdPage(), metadata, OwnerForm(), RELATION_CHOICES, Roster(), household()

### Community 169 - "UnknownModule"
Cohesion: 0.29
Nodes (7): Also yours, Christian — Lane A · Integration and product owner, Starter prompt for your coding agent, Starter prompt: what can I actually pick up?, The five things you ship, Week 1, in order, What integration actually means here

### Community 170 - "build"
Cohesion: 0.29
Nodes (7): Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The autonomy statement, The six artefacts, Where governance touches the code

### Community 171 - "test_a_failure_after_the_stream_started_arrives_as_an_event"
Cohesion: 0.29
Nodes (7): Parse an `text/event-stream` body into the payloads it carried., No `reading` before it: the floor is checked before the model is asked anything., By then the 200 has been sent. An exception that only logged would leave a scree, sse(), test_a_failure_after_the_stream_started_arrives_as_an_event(), test_a_refusal_is_the_whole_stream(), test_an_abstention_is_the_whole_stream()

### Community 172 - "ask.py"
Cohesion: 0.48
Nodes (6): answer(), build_context(), format_sources(), Ollama, Answer a question from retrieved chunks, with citations back to the file.  The, Hit

### Community 173 - "load_corpus.py"
Cohesion: 0.60
Nodes (5): ACTIONS, GET(), POST(), sameOrigin(), unlocked()

### Community 174 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 175 - "Send"
Cohesion: 0.40
Nodes (3): The local API. Liveness is intentionally separate from assistant readiness.  Loo, Restart and shut down: asked for by the screens, carried out by the supervisor., FastAPI

### Community 176 - "0002_household.sql"
Cohesion: 0.70
Nodes (4): document_attribution, people, person_aliases, telegram_identities

### Community 178 - "Exception"
Cohesion: 0.40
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 179 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

### Community 180 - "quiet_engine"
Cohesion: 0.67
Nodes (3): MonkeyPatch, quiet_engine(), No real probes, no startup writes, no deliberate pause before exiting.      The

## Knowledge Gaps
- **568 isolated node(s):** `Read first`, `The order, which is not the obvious one`, `Column headings are not yours to choose`, `Validate before handing over`, `The rule that cannot bend` (+563 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **47 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Ollama` connect `ingest.py` to `contracts.py`, `Ollama`, `FIRST-RUN.md`, `api.ts`, `FolderCapture`, `RUNNING.md`, `DoclingParser`, `dispatch.py`, `reindex.py`, `_payload_for`, `igd-capstone-2026`, `extract`, `3. PaperBrain informs core/retrieve/'s pattern; it is not the core module`, `Christian — Lane A · Integration and product owner`, `IngestJob`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `Connection` connect `Cursor` to `cli.py`, `register_document`, `ingest.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `Settings` connect `Settings` to `pipeline.py`, `6 · Use it`, `ParsedPage`, `FIRST-RUN.md`, `Ollama`, `ingest.py`, `register_document`, `FolderCapture`, `DoclingParser`, `Ollama`, `1. Record architecture decisions`, `pipeline.py`, `test_the_real_packs_declare_metrics_that_exist`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `Ollama` (e.g. with `ModelWarmth` and `Abstained`) actually correct?**
  _`Ollama` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `FakeConn` (e.g. with `Abstained` and `Answer`) actually correct?**
  _`FakeConn` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `ModelUnavailable` (e.g. with `ModelWarmth` and `Abstained`) actually correct?**
  _`ModelUnavailable` has 27 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Read first`, `The order, which is not the obvious one`, `Column headings are not yours to choose` to the rest of the system?**
  _568 weakly-connected nodes found - possible documentation gaps or missing edges._