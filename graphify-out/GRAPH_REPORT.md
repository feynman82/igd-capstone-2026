# Graph Report - igd-capstone-2026  (2026-09-11)

## Corpus Check
- 140 files · ~87,829 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1210 nodes · 2224 edges · 102 communities (89 shown, 13 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 160 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `aeeb6ec8`
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
- IngestJob
- Ollama
- test_ingest_pipeline.py
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
- Parser
- Home Contents Insurance Policy
- __init__.py
- __init__.py
- __init__.py
- __init__.py
- setup.sh

## God Nodes (most connected - your core abstractions)
1. `Ollama` - 36 edges
2. `FolderAdapter` - 31 edges
3. `Passage` - 30 edges
4. `ModelUnavailable` - 30 edges
5. `Settings` - 29 edges
6. `AnswerGraph` - 26 edges
7. `InstalledPack` - 25 edges
8. `IngestJob` - 20 edges
9. `extract()` - 20 edges
10. `Claim` - 19 edges

## Surprising Connections (you probably didn't know these)
- `main()` --indirect_call--> `sha256()`  [INFERRED]
  scripts/quarantine.py → core/adapters/base.py
- `FakeRegistrar` --uses--> `FolderSettings`  [INFERRED]
  tests/test_folder_capture.py → core/adapters/folder.py
- `FakeOllama` --uses--> `ParsedPage`  [INFERRED]
  tests/test_ingest_pipeline.py → core/ingest/parse.py
- `FakeRegistrar` --uses--> `Registration`  [INFERRED]
  tests/test_folder_capture.py → core/ingest/register.py
- `Alert` --uses--> `InstalledPack`  [INFERRED]
  modules/alert/__init__.py → core/packs.py

## Import Cycles
- None detected.

## Communities (102 total, 13 thin omitted)

### Community 0 - "contracts.py"
Cohesion: 0.07
Nodes (40): BaseModel, FieldSpec, Grounding, Guardrails, ModuleManifest, ModuleTrigger, PackManifest, Persona (+32 more)

### Community 1 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.18
Nodes (8): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected, Architecture decision records, Index, Writing one

### Community 2 - "README.md"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.22
Nodes (18): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), date, Path, Validate a document register before it is handed over.      python -m corpus.v (+10 more)

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
Cohesion: 0.22
Nodes (9): Authoring a pack, igd-capstone-2026, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live, Where to start (+1 more)

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
Cohesion: 0.05
Nodes (63): Answer, AnswerGraph, _numbered(), _pack_for(), Any, Ollama, Router → retrieve → rerank → grounding gate → answer or abstain.  A LangGraph, Whichever pack owns the most of the evidence. Its guardrails govern the answer. (+55 more)

### Community 54 - "test_modules.py"
Cohesion: 0.05
Nodes (63): AlertConfig, Decimal, Alert, _citations(), cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd() (+55 more)

### Community 55 - "Settings"
Cohesion: 0.06
Nodes (61): create_app(), Diagnostic API. Liveness is intentionally separate from assistant readiness., AsyncClient, queue(), The reportable line. Deliberately a rate and a count, because a rate over three, What is waiting for a person's eyes, oldest first., recovery_rate(), capture_check() (+53 more)

### Community 56 - "Registrar"
Cohesion: 0.12
Nodes (20): _attachment(), Any, Client, datetime, RuntimeError, The Telegram capture adapter.  Same interface as the folder: `receive(payload,, Confirm the token works before anything else is attempted., One `getUpdates` round. Returns what was captured; replies with what was receive (+12 more)

### Community 57 - "retrieve.py"
Cohesion: 0.11
Nodes (24): Connection, Cursor, Any, Protocol, Just enough of `psycopg.Connection` to register a document and to be faked in a, ndarray, load_matrix(), pack() (+16 more)

### Community 58 - "cli.py"
Cohesion: 0.18
Nodes (20): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+12 more)

### Community 59 - "register_document"
Cohesion: 0.14
Nodes (21): CaptureAdapter, datetime, Protocol, The one interface every capture channel satisfies.      receive(payload, mime, s, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256` i, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sha256(), Capture adapters.  Every channel a document can arrive through satisfies one int (+13 more)

### Community 60 - "FolderCapture"
Cohesion: 0.12
Nodes (13): FolderSettings, Intake, An already-indexed document is not re-parsed. Re-parsing it would burn a minute, The row as it now stands, plus whether this call is the one that created it., Registration, FolderCapture, Run the folder capture loop in a background thread, beside the local server., A daemon thread that polls the watched folder until `stop()` or process exit. (+5 more)

### Community 61 - "InstalledPack"
Cohesion: 0.13
Nodes (18): DocumentTypeSpec, One kind of document this pack recognises., Classification, _prompt(), Decide which pack's document type a captured document is, or decline to.  The, document_types(), installed_packs(), InstalledPack (+10 more)

### Community 62 - "extract"
Cohesion: 0.14
Nodes (20): classify(), Ollama, Never raises. An unavailable model is a classification failure, so it quarantine, _schema(), extract(), Ollama, Never raises. A failure is a reason, and a reason routes the document to quarant, FakeOllama (+12 more)

### Community 63 - "pipeline.py"
Cohesion: 0.16
Nodes (17): Chunk, Extraction, The ingestion worker.  Capture registers a document; this package turns it int, What every capture channel hands a document to.  An adapter's job ends at "these, commit_both_lanes(), Outcome, process(), Any (+9 more)

### Community 64 - "FolderAdapter"
Cohesion: 0.26
Nodes (20): FolderAdapter, Satisfies `CaptureAdapter`. Holds no database handle — it is given a `Registrar`, FakeRegistrar, datetime, Path, The watched folder: debounce, mime sniffing, and what happens the second time., Poll until the stability window has passed and something comes out., The `documents` table, reduced to the one thing it guarantees: sha256 is unique. (+12 more)

### Community 65 - "IngestJob"
Cohesion: 0.16
Nodes (13): IngestJob, Magic bytes first, filename suffix second, `application/octet-stream` last., What a capture returns: a registered document, and whether we had seen it before, sniff_mime(), _Pending, datetime, Path, The watched-folder capture adapter.  A person drops a scan into a folder and i (+5 more)

### Community 66 - "Ollama"
Cohesion: 0.17
Nodes (11): answer(), build_context(), format_sources(), Ollama, Answer a question from retrieved chunks, with citations back to the file.  The, Ollama, OllamaUnavailable, RuntimeError (+3 more)

### Community 67 - "test_ingest_pipeline.py"
Cohesion: 0.19
Nodes (14): find_page(), _normalise(), Extract a pack's declared fields, and attribute every one of them to a page., The first page whose text contains this value. None means no page supports it., parse(), Turn captured bytes into pages of text, or say why it could not be done.  Every, The one call the pipeline makes. An unhandled mime type quarantines rather than, Parsing, chunking, extraction and the quarantine decision.  The model is faked. (+6 more)

### Community 68 - "ParsedPage"
Cohesion: 0.17
Nodes (12): Chunk, chunk_pages(), _pack(), _paragraphs(), Split parsed pages into retrieval-sized chunks that still know their page number, What is actually embedded: the prefix plus the text, matching the tsvector colum, Greedily fill chunks up to the target, then carry a little tail into the next on, One flat list of chunks, ordinal running across the whole document. (+4 more)

### Community 69 - "Ollama"
Cohesion: 0.23
Nodes (14): ParsedDocument, page_images(), Any, Ollama, QuarantinedDocument, The second stage of quarantine: the page image, read by the vision-language mode, Base64 page images, in page order. Empty when this document cannot be rendered., Ask the vision-language model to read the pages. One request per page, so a page (+6 more)

### Community 71 - "ingest.py"
Cohesion: 0.24
Nodes (13): Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks.  Paperwork is short and stru, _split_page(), discover(), guess_date(), guess_type() (+5 more)

### Community 72 - "obligations.py"
Cohesion: 0.19
Nodes (11): ExtractedFact, fixed(), from_facts(), _label(), Any, date, Turn a dated fact into a commitment to do something about it.  A fact is a state, What a person is shown. The key is the pack's word for it; the subject says whos (+3 more)

### Community 73 - "extract.py"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.17
Nodes (12): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Quarantine, and the second pass, Reading a document (+4 more)

### Community 75 - "RUNNING.md"
Cohesion: 0.18
Nodes (8): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision, 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 76 - "DoclingParser"
Cohesion: 0.29
Nodes (4): DoclingParser, _pages_from(), Group Docling's items by the page they were found on.      Docling's markdown ex, Docling, held at arm's length: imported on first use, and never at module import

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
Cohesion: 0.33
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 89 - "Christian — Lane A · Integration and product owner"
Cohesion: 0.33
Nodes (6): Also yours, Christian — Lane A · Integration and product owner, Starter prompt for your coding agent, The five things you ship, Week 1, in order, What integration actually means here

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

## Knowledge Gaps
- **334 isolated node(s):** `npx`, `@modelcontextprotocol/server-filesystem`, `packs`, `modules`, `traces` (+329 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Connection` connect `retrieve.py` to `cli.py`, `register_document`, `ingest.py`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `Ollama` connect `Ollama` to `test_ingest_pipeline.py`, `obligations.py`, `Passage`, `Settings`, `FolderCapture`, `InstalledPack`, `pipeline.py`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `register_document()` connect `register_document` to `retrieve.py`, `FolderCapture`, `pipeline.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Ollama` (e.g. with `Answer` and `AnswerGraph`) actually correct?**
  _`Ollama` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `FolderAdapter` (e.g. with `IngestJob` and `Registrar`) actually correct?**
  _`FolderAdapter` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Passage` (e.g. with `Answer` and `AnswerGraph`) actually correct?**
  _`Passage` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ModelUnavailable` (e.g. with `Answer` and `AnswerGraph`) actually correct?**
  _`ModelUnavailable` has 14 INFERRED edges - model-reasoned connections that need verification._