# Graph Report - igd-capstone-2026  (2026-09-13)

## Corpus Check
- 0 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2555 nodes · 4653 edges · 164 communities (148 shown, 16 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 300 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a86f56ae`
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
- answer.tsx
- AnswerGraph
- enabled_pack_ids
- page.tsx
- item-row.tsx
- classify
- page.tsx
- reindex.py
- power-menu.tsx
- README.md
- igd-capstone-2026
- Desmond — Lane E · Corpus and adversarial testing
- Ollama
- enabled_pack_ids
- Parser
- Desmond — task list
- date
- next.config.ts
- postcss.config.mjs
- test_the_real_packs_declare_metrics_that_exist
- Desmond — Lane E · Corpus and adversarial testing
- github.md
- 6 · Use it
- FIRST-RUN.md
- FakeCursor
- page.tsx
- page.tsx
- UnknownModule
- build
- load_corpus.py
- The team
- 0002_household.sql
- Exception
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- Exception

## God Nodes (most connected - your core abstractions)
1. `FakeConn` - 64 edges
2. `Ollama` - 54 edges
3. `rows_for()` - 48 edges
4. `settings()` - 47 edges
5. `client_for()` - 46 edges
6. `Settings` - 40 edges
7. `ScriptedOllama` - 36 edges
8. `FakeOllama` - 34 edges
9. `AnswerGraph` - 31 edges
10. `FolderAdapter` - 31 edges

## Surprising Connections (you probably didn't know these)
- `_settings()` --indirect_call--> `settings()`  [INFERRED]
  api/routes.py → tests/test_api.py
- `FakeConn` --uses--> `Citation`  [INFERRED]
  tests/test_api.py → core/graph/answer.py
- `FakeCursor` --uses--> `Citation`  [INFERRED]
  tests/test_api.py → core/graph/answer.py
- `FakeGraph` --uses--> `Citation`  [INFERRED]
  tests/test_api.py → core/graph/answer.py
- `StreamingGraph` --uses--> `Citation`  [INFERRED]
  tests/test_api.py → core/graph/answer.py

## Import Cycles
- None detected.

## Communities (164 total, 16 thin omitted)

### Community 0 - "contracts.py"
Cohesion: 0.22
Nodes (7): The answer graph.  Router, retrieve, rerank, grounding gate, then answer or abst, Passage, How a passage names itself: the document and the page, as a person would say it., Implemented by `core/retrieve/` when Lane B's hybrid search lands.      `candi, A cross-encoder, scoring question against passage. Returns the best `keep`, reor, Reranker, Retriever

### Community 1 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.15
Nodes (9): metadata, PacksPage(), Toggle(), EmptyState(), SHAPES, ModuleSummary, packs(), PackSummary (+1 more)

### Community 2 - "README.md"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.09
Nodes (38): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), Validate a document register before it is handed over.      python -m corpus.val, Parse `field_pages`: semicolon-separated `name=page`, 1-based. Empty means page (+30 more)

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

### Community 17 - "igd-capstone-2026"
Cohesion: 0.08
Nodes (35): Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker.      Celery is imported here ra, Intake, bytes_for(), index_folder(), Find the bytes behind a registered document again.  v1 keeps the inbox as the, Safe to show: the bytes for this document are no longer anywhere we look. (+27 more)

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
Cohesion: 0.48
Nodes (6): main(), Generate each member's task list from the master task CSV.      python scripts, _read_rows(), _render(), _week_key(), _write()

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
Cohesion: 0.07
Nodes (37): What the graph needs from retrieval, stated as a contract rather than an import., is_first_person(), Whose question is this, and whose documents may answer it.  "What is my term l, `(word, relation)` when the question asks about a relation's own documents, else, The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer.          The i, Whether this question is about the person asking.      `other_names` are the d, Keep the owner's passages and the household's; set aside everybody else's. (+29 more)

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
Cohesion: 0.24
Nodes (10): document_types(), installed_packs(), InstalledPack, _load_one(), pack(), PackUnavailable, Load the installed packs at runtime.  A pack is authored as one YAML file and, A pack's YAML and its generated schemas disagree, or the pack does not exist. (+2 more)

### Community 52 - "`docs/report/` — the final report"
Cohesion: 0.10
Nodes (19): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model (+11 more)

### Community 53 - "Passage"
Cohesion: 0.12
Nodes (21): Citation, _numbered(), _pack_for(), Router → retrieve → rerank → decide → answer, one verified sentence at a time., A passage, named the way a person cites it and identified the way a link needs., The pack owning the best-scoring passage. Its guardrails govern the answer., check(), check_one() (+13 more)

### Community 54 - "test_modules.py"
Cohesion: 0.18
Nodes (17): ParsedDocument, blocked_reasons(), forget(), page_images(), QuarantinedDocument, The second stage of quarantine: the page image, read by the vision-language mode, Per document: `None` when the image pass can run, or the sentence saying why it, Safe to show. Forgetting a document whose file is still there would not last. (+9 more)

### Community 55 - "Settings"
Cohesion: 0.14
Nodes (24): capture_check(), Check, collect_checks(), database_check(), interface_check(), model_check(), Read-only dependency diagnostics; installation is never treated as inference val, Whether a worker is listening — which is a different question from whether Redis (+16 more)

### Community 56 - "Registrar"
Cohesion: 0.07
Nodes (33): IngestJob, Magic bytes first, filename suffix second, `application/octet-stream` last., What a capture returns: a registered document, and whether we had seen it before, sniff_mime(), _Pending, The watched-folder capture adapter.  A person drops a scan into a folder and i, Every file in the watched folder that is worth looking at at all., Advance the debounce by `elapsed` seconds and return the files now ready. (+25 more)

### Community 57 - "retrieve.py"
Cohesion: 0.27
Nodes (8): Classification, classification_sample(), classify(), _prompt(), Decide which pack's document type a captured document is, or decline to.  The, The text the classifier reads: the opening pages, labelled, within a fixed budge, Never raises. An unavailable model is a classification failure, so it quarantine, _schema()

### Community 58 - "cli.py"
Cohesion: 0.06
Nodes (67): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a, answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file.  The, Chunk, chunk_pages() (+59 more)

### Community 59 - "register_document"
Cohesion: 0.11
Nodes (17): CaptureAdapter, The one interface every capture channel satisfies.      receive(payload, mime, s, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256` i, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sha256(), Capture adapters.  Every channel a document can arrive through satisfies one int, Cursor, Register a document, idempotently, on a SHA-256 of the source bytes.  This is th (+9 more)

### Community 60 - "FolderCapture"
Cohesion: 0.05
Nodes (101): a_citation(), client(), client_for(), conn(), document_row(), fact_row(), FakeConn, filed_document() (+93 more)

### Community 61 - "InstalledPack"
Cohesion: 0.12
Nodes (30): page_count(), PageUnavailable, _pdfium(), One page of one document, as an image.  Two callers want the same thing for oppo, Safe to show a person: there is no such page, or this file cannot be drawn., Safe to show a person: this install cannot render PDF pages at all., How many pages this file has, or 0 when it is not something with pages.      `do, `(bytes, media type)` for one page, one-based.      An image document is returne (+22 more)

### Community 62 - "extract"
Cohesion: 0.11
Nodes (31): extract(), Never raises. A failure is a reason, and a reason routes the document to quarant, FakeOllama, _page_of_examples(), Parsing, chunking, extraction and the quarantine decision.  The model is faked, Answers whatever the test told it to, and records what it was asked., One page printing every field's `example`, so each value is attributable to a pa, `FieldSpec.name` is the `facts.key`. Nothing between the manifest and the row re (+23 more)

### Community 63 - "pipeline.py"
Cohesion: 0.09
Nodes (32): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+24 more)

### Community 64 - "FolderAdapter"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 65 - "FolderCapture"
Cohesion: 0.10
Nodes (19): Block, DoclingParser, _kind(), _pages_from(), Parser, PlainTextParser, Turn captured bytes into pages of text, or say why it could not be done.  Every, Docling, held at arm's length: imported on first use, and never at module import (+11 more)

### Community 66 - "pipeline.py"
Cohesion: 0.25
Nodes (8): _launcher(), Stands in for `start_web` and `stop_web`: counts, and never touches npm., Screens, _supervise(), test_a_start_that_fails_is_not_retried(), test_no_web_means_the_supervisor_starts_no_screens(), test_the_supervisor_relaunches_on_restart_and_keeps_the_screens_up(), test_the_supervisor_still_refuses_a_lan_bind_before_starting_anything()

### Community 67 - "TelegramAdapter"
Cohesion: 0.21
Nodes (9): ExtractedFact, fixed(), from_facts(), _label(), Turn a dated fact into a commitment to do something about it.  A fact is a state, What a person is shown. The key is the pack's word for it; the subject says whos, Create the obligations this pack declares for these newly written facts.      `f, Create the pack's calendar obligations — a filing deadline belongs to no documen (+1 more)

### Community 68 - "ParsedPage"
Cohesion: 0.15
Nodes (17): installed_modules(), InstalledModule, manifest(), ModuleUnavailable, Load the installed capability modules at runtime.  The mirror of `core/packs.py`, A module's YAML is missing, or does not validate against `ModuleManifest`., One module's manifest, validated. Raises rather than returning a partial object., Every module directory holding a `module.yaml`, in a stable order.      Director (+9 more)

### Community 69 - "Ollama"
Cohesion: 0.09
Nodes (37): queue(), The reportable line. Deliberately a rate and a count, because a rate over three, What is waiting for a person's eyes, oldest first., recovery_rate(), digest_of_document(), connect(), DatabaseUnavailable, One place that opens a connection to the one database.  `Settings.database_url (+29 more)

### Community 71 - "ingest.py"
Cohesion: 0.15
Nodes (16): Alert, _citations(), cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, The Alert module: a pack-declared threshold, crossed once, citing the documents (+8 more)

### Community 72 - "obligations.py"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 73 - "extract.py"
Cohesion: 0.28
Nodes (9): _pack_row(), packs(), One row of `packs`, with the manifest validated back out of its jsonb column., No row in `packs` with that id., Every installed pack, with what it has extracted so far., Switch one pack on or off. Raises `UnknownPack` rather than silently doing nothi, RegisteredPack, set_pack_enabled() (+1 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (16): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+8 more)

### Community 75 - "RUNNING.md"
Cohesion: 0.14
Nodes (23): Abstained, AnswerGraph, Finished, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed y, Everything that is only knowable once the last sentence is in., Built once, asked many times. Holds no connection: retrieval does., One streamed sentence object, turned into the thing the gate understands., The implementation. Yields each sentence once it has passed the gate, never befo (+15 more)

### Community 76 - "DoclingParser"
Cohesion: 0.17
Nodes (23): FolderAdapter, FolderSettings, Satisfies `CaptureAdapter`. Holds no database handle — it is given a `Registrar`, _loop(), main(), Watch the inbox folder, register and read everything dropped into it.      uv, Poll until interrupted. `--once` waits out one stability window and then stops., FakeRegistrar (+15 more)

### Community 77 - "Notion"
Cohesion: 0.29
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "start_parrot.py"
Cohesion: 0.38
Nodes (6): main(), Local-only startup preflight, using the standard library so setup can be diagnos, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file conte, report_hardware(), startup_gaps()

### Community 79 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.14
Nodes (14): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+6 more)

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (7): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 82 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.12
Nodes (12): Answer, Cited, One sentence and the passages it was traced to. What rule 3 looks like as data., FakeCursor, FakeGraph, graph(), Stands in for `AnswerGraph` at the seam `api/routes.py` owns., "when does it expire?" is only a question in the light of the one before it. (+4 more)

### Community 83 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 85 - "test_startup.py"
Cohesion: 0.10
Nodes (16): prepare_checkout(), Startup tests do not ingest documents or need the corpus: they check process bou, npm is a wrapper around node. Killing only the wrapper orphans the port., The worker starts its nightly schedule as a process of its own. Terminating only, Stopping it signals its process group. Without a session of its own that group i, A developer's own `npm run dev` is used rather than fought for the port., `npm run dev` against an empty web/ fails slowly and cryptically. Say so instead, The screens follow the engine to whatever port it got, rather than to web/.env.l (+8 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.15
Nodes (19): _kill_tree(), main(), parse_args(), port_answers(), Run the engine, the folder watcher, the ingestion worker and the screens togethe, Stop a child and everything under it, then make sure it has gone., Whether something is listening on loopback. Not whether it is ours., Start `npm run dev` in `web/`, or say plainly why it could not.      Three reaso (+11 more)

### Community 89 - "Christian — Lane A · Integration and product owner"
Cohesion: 0.05
Nodes (76): AbstentionEvent, AskRequest, AskResponse, Claim, CloseRequest, ConfirmNameRequest, CorrectionRequest, CorrectionResponse (+68 more)

### Community 90 - "The team"
Cohesion: 0.10
Nodes (31): GET(), grant(), POST(), ALLOWED, Context, DELETE(), forward(), GET() (+23 more)

### Community 91 - "1. Record architecture decisions"
Cohesion: 0.27
Nodes (11): install_best_effort(), Install at startup without being able to stop startup.      Both processes that, _beat_needs_its_own_process(), celery_argv(), main(), Run the ingestion worker, and optionally the nightly schedule with it.      uv, The arguments the Celery command-line would have been given. Built here so a tes, Celery refuses `worker --beat` on Windows — "-B option does not work on Windows" (+3 more)

### Community 92 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.20
Nodes (15): _class_name(), _docstring(), _field_line(), load(), main(), Generate everything downstream of a pack.yaml.      python -m packs.build, The header row Desmond fills in, one file per pack.      Long format: one row, The header a batch register starts from: every field of every installed pack. (+7 more)

### Community 93 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 94 - "IngestJob"
Cohesion: 0.10
Nodes (25): _coerce(), _date_renderings(), decode_schema(), _drop_format(), find_page(), _normalise(), _prepare(), printed_date() (+17 more)

### Community 102 - "schedule.py"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "PackManifest"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 104 - "ingest.py"
Cohesion: 0.08
Nodes (24): Dispatcher, Inline, What happens to a document between "these bytes are registered" and "this docume, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Send, The ingestion worker.  Capture registers a document; this package turns it int (+16 more)

### Community 105 - "Contributing"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 106 - "FolderCapture"
Cohesion: 0.11
Nodes (19): enabled_pack_ids(), enabled_packs(), The packs left switched on, or `None` when nothing has been installed yet., The installed packs a person has left switched on, as loaded pack objects., close(), next_window(), Overdue, The Reminder module: a nightly sweep of obligations, and nothing fires twice. (+11 more)

### Community 107 - "worker.py"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 108 - "base.py"
Cohesion: 0.23
Nodes (11): _columns(), correct(), Corrected, CorrectionRejected, A person fixing a field the extractor got wrong.  This is the one place in the s, `(value_text, value_num, value_date)` — exactly one of them set.      The declar, Store what a person says this field actually says, and keep what it used to say., Safe to show: there is no fact with that id. (+3 more)

### Community 109 - "dispatch.py"
Cohesion: 0.09
Nodes (21): create_app(), ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one t, Load the generator and the embedder before the first question, and record the ou, warm_models(), _ollama_answering(), Setup diagnostics use controlled service responses, never live household documen, The browser opens on this within a second of a double-click, so it must not wait (+13 more)

### Community 110 - "Ollama"
Cohesion: 0.12
Nodes (21): _as_document(), declared_type(), document(), documents(), Fact, _facts_for(), NamedDocument, The vault: what is in the house, what state it is in, and what was read off it. (+13 more)

### Community 111 - "Intake"
Cohesion: 0.04
Nodes (45): ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes, postcss (+37 more)

### Community 112 - "_payload_for"
Cohesion: 0.11
Nodes (33): One sentence that has passed the gate, with the citations it passed on.      It, Sentence, build(), events(), passage(), The grounding gate, and the graph's two ways of not answering.  Rule 3 says no, The promise the Ask surface is built on. Two sentences, two separate events, in, Nothing is added afterwards, so a chip can never appear late or change. (+25 more)

### Community 113 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.50
Nodes (4): install(), Installed, What `install` did, so a startup line can say it in one sentence., Write every pack and module on disk into its table. Idempotent; never re-enables

### Community 114 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.08
Nodes (33): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), owner(), owner_aliases(), pending() (+25 more)

### Community 117 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 118 - "6 · Use it"
Cohesion: 0.16
Nodes (18): The local API. Liveness is intentionally separate from assistant readiness.  Loo, Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor., What the person asked for, once. The first request wins; later ones change nothi, _client(), _eventually(), quiet_engine(), Restart and shut down: the engine asks its supervisor, and nothing else can ask (+10 more)

### Community 120 - "test_the_reminder_cron_is_read_from_its_manifest_not_written_twice"
Cohesion: 0.20
Nodes (8): archivo, figtree, jetbrains, metadata, outfit, spectral, viewport, ThemeProvider()

### Community 121 - "test_alert_is_swept_nightly_even_though_its_manifest_says_fact_write"
Cohesion: 0.09
Nodes (18): _asked(), _conversation(), fuse(), What the graph carries. It ends at the evidence; the answer is streamed, not sta, The question to answer and to scope. A follow-up is the whole question it was ma, Several searches as one list: each passage once, at the best score any phrasing, The question made whole, and said in the documents' words. See `UNDERSTAND_SYSTE, Every phrasing of the question, searched and fused. The person's own words alway (+10 more)

### Community 122 - "__init__.py"
Cohesion: 0.27
Nodes (10): countdown(), detail(), figure(), ItemRow(), longDate(), sentence(), TONE, WORD (+2 more)

### Community 123 - "SentenceScanner"
Cohesion: 0.10
Nodes (27): Pulling finished sentences out of a JSON reply that is still being written.  The, What document would have answered this, if the model said. Read once, at the end, Feed it deltas; it returns whichever sentences became complete because of them., Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes on, Find `"sentences": [` once. Everything before it is of no interest.          Sea, SentenceScanner, drip() (+19 more)

### Community 124 - "__init__.py"
Cohesion: 0.07
Nodes (31): already_said(), current_lead(), Due, Smaller is more urgent. The Today surface orders by this., The tightest lead window this obligation has entered, or None if it has entered, True when this exact window has already been mentioned.      The comparison is, Everything inside a lead window that has not already been said for that window., sweep() (+23 more)

### Community 125 - "Household canon"
Cohesion: 0.08
Nodes (23): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, Policies, The family tree, and why three of them are not called Lim (+15 more)

### Community 126 - "Finished"
Cohesion: 0.12
Nodes (13): metadata, Abstention(), Part, sentence(), textOf(), ADR-0011, Turn(), Conversation() (+5 more)

### Community 127 - "page.tsx"
Cohesion: 0.09
Nodes (12): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+4 more)

### Community 129 - "answer.tsx"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 130 - "AnswerGraph"
Cohesion: 0.09
Nodes (21): The page a person sees while Parrot starts, served by the engine itself.  **Why, The whole page. `screens_url` is escaped into a data attribute, never into scrip, render(), DenseRetriever, NoReranker, A dense-only retriever, so the graph can be run and tested before Lane B's hybri, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this with, Generated (+13 more)

### Community 132 - "enabled_pack_ids"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 134 - "page.tsx"
Cohesion: 0.13
Nodes (19): ALWAYS_EXISTS, AskResponse, Claim, get(), HouseholdResponse, PacksResponse, PendingName, Person (+11 more)

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
Nodes (19): parse(), The one call the pipeline makes. An unhandled mime type quarantines rather than, document_title(), The document as a person would name it: its `string` fields as read, in the pack, indexed(), IndexedDocument, Rebuild a document's chunks and vectors without reading it again for facts.  Chu, Safe to show: names what went wrong, never what the document says. (+11 more)

### Community 143 - "power-menu.tsx"
Cohesion: 0.16
Nodes (11): Action, CONFIRM, ITEMS, PowerMenu(), Stage, DependencyCheck, Phase, RestartingScreen() (+3 more)

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
Cohesion: 0.24
Nodes (10): build(), The one Celery application, built from `Settings`.  Every setting here is a cons, Construct the Celery application. Imported lazily by callers so that nothing whi, beat_schedule(), cron_expressions(), crontab_from(), manifest(), When the nightly sweeps run, read from the modules' own manifests.  A module alr (+2 more)

### Community 151 - "enabled_pack_ids"
Cohesion: 0.12
Nodes (26): Chunk, chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own st, One flat list of chunks, ordinal running across the whole document. (+18 more)

### Community 153 - "Parser"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "Desmond — task list"
Cohesion: 0.33
Nodes (5): 12. Chunks follow the document's headings, and embeddings use the model's task prompts, Consequences, Context, Decision, Evidence

### Community 155 - "date"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 159 - "test_the_real_packs_declare_metrics_that_exist"
Cohesion: 0.33
Nodes (5): 13. A question is understood before it is searched, and scoped before it is cut, Consequences, Context, Decision, Evidence

### Community 160 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.29
Nodes (8): DocumentPage(), metadata, ProblemState(), DocumentDetail(), when(), document(), pageImage(), VaultDocument

### Community 162 - "github.md"
Cohesion: 0.50
Nodes (3): Last sync, Screen map, Updated in this project

### Community 164 - "6 · Use it"
Cohesion: 0.43
Nodes (7): lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns(), readEvents(), upstreamDetail()

### Community 165 - "FIRST-RUN.md"
Cohesion: 0.16
Nodes (18): ConfigurationError, _folder(), local_url(), _port(), _positive(), Small, literal .env reader with environment overrides and loopback-only endpoint, Safe to show to the user: messages never include configuration values., A context window is a number of tokens. A bad one is a configuration error, not (+10 more)

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

### Community 173 - "load_corpus.py"
Cohesion: 0.60
Nodes (5): ACTIONS, GET(), POST(), sameOrigin(), unlocked()

### Community 174 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 176 - "0002_household.sql"
Cohesion: 0.70
Nodes (4): document_attribution, people, person_aliases, telegram_identities

### Community 178 - "Exception"
Cohesion: 0.40
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 179 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

### Community 194 - "Exception"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

## Knowledge Gaps
- **570 isolated node(s):** `The screens`, `Dropping a document in`, `Quarantine, and the second pass`, `Asking a question`, `Today` (+565 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `ParsedPage`, `FIRST-RUN.md`, `Ollama`, `ingest.py`, `extract.py`, `FolderCapture`, `register_document`, `DoclingParser`, `9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack`, `Ollama`, `1. Record architecture decisions`, `pipeline.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `Connection` connect `cli.py` to `register_document`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `Ollama` connect `AnswerGraph` to `TelegramAdapter`, `Ollama`, `FIRST-RUN.md`, `ingest.py`, `DoclingParser`, `dispatch.py`, `reindex.py`, `igd-capstone-2026`, `test_modules.py`, `enabled_pack_ids`, `extract`, `3. PaperBrain informs core/retrieve/'s pattern; it is not the core module`, `IngestJob`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `FakeConn` (e.g. with `Abstained` and `Answer`) actually correct?**
  _`FakeConn` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Ollama` (e.g. with `ModelWarmth` and `DenseRetriever`) actually correct?**
  _`Ollama` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `The screens`, `Dropping a document in`, `Quarantine, and the second pass` to the rest of the system?**
  _570 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `validate` be split into smaller, more focused modules?**
  _Cohesion score 0.08846153846153847 - nodes in this community are weakly interconnected._