# Graph Report - igd-capstone-2026  (2026-09-20)

## Corpus Check
- 0 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4209 nodes · 10086 edges · 236 communities (211 shown, 25 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 1661 edges (avg confidence: 0.69)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b32fb278`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- get
- packs/page.tsx
- Christian — task list
- validate
- build_router
- Project PARROT — team split
- Project PARROT — team split
- sha256
- Running the evaluation harness
- support.js
- Desmond — task list
- Zee — task list
- test_ingest_pipeline.py
- answer.tsx
- Filling the corpus register
- Writing a governance artefact
- Claude Code — read this first
- test_worker_queue.py
- Person
- ingest/extract.py
- Household canon
- install_best_effort
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
- InstalledPack
- HouseholdAdviceLog
- Changelog
- filesystem
- `docs/governance/` — the assurance artefacts
- corpus/__init__.py
- packs/__init__.py
- parrot
- _page_of_examples
- The household, and the word "my"
- RegisteredPack
- alert/__init__.py
- Basic Financial Planning Guide
- test_household.py
- advice/__init__.py
- cli.py
- client_for
- Ollama
- test_pages.py
- FakeOllama
- bench_runtime.py
- compilerOptions
- parse.py
- test_startup.py
- ParsedPage
- registry.py
- ModelUnavailable
- test_advice_module.py
- FakeCursor
- preview.tsx
- ConfigurationError
- Starting Parrot
- load_register
- obligations.py
- Notion
- Passage
- The demonstration run sheet
- PaperBrain
- Contributing
- [...path]/route.ts
- components.json
- .stream
- sweep
- Architecture
- Roadmap
- contracts.py
- tokens/page.tsx
- lock.ts
- document-detail.tsx
- DocumentCatalog
- .constrained_stream
- boot
- Home Contents Insurance Policy
- api/__init__.py
- core/__init__.py
- runtime/__init__.py
- modules/__init__.py
- setup.sh
- 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module
- FakeConn
- routes.py
- 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack
- test_telegram_capture.py
- Siew — task list
- ScriptedOllama
- Settings
- vault.py
- dependencies
- Claim
- test_grounding_values.py
- household.py
- GroundingCorpus
- TelegramAdapter
- _advised
- test_lifecycle.py
- worker/__init__.py
- app/layout.tsx
- ._build
- test_contracts.py
- SentenceScanner
- reminder/__init__.py
- Household canon
- item-row.tsx
- createExternalModules
- FolderAdapter
- test_grounding_index.py
- FakeConn
- connection
- 10. `main` is unprotected, and the discipline is human
- scope.py
- api.ts
- team/README.md
- today/page.tsx
- scope_passages
- test_api.py
- values.py
- FakeConn
- StreamingGraph
- PackManifest
- export-design-preview.cjs
- devDependencies
- Working agreement for coding agents
- Comparison of Integrated Shield Plans
- Domain packs — start here
- app/page.tsx
- Desmond — Lane E · Corpus and adversarial testing
- schedule.py
- ErrorEvent
- test_one_document_is_shown_even_when_its_pack_is_off
- 2. One PostgreSQL instance for everything
- adr/README.md
- test_an_empty_registry_shows_everything_rather_than_nothing
- package.json
- _today_items
- postcss.config.mjs
- 4. Writing `pack.yaml`
- 13. A question is understood before it is searched, and scoped before it is cut
- Try PARROT
- github.md
- .empty_for_owner
- send_retry
- Understanding health insurance
- Notebook prompts — the four full policies for Marcus Lim
- FakeCursor
- test_advice_core.py
- packs.py
- First run
- igd-capstone-2026
- FakeCursor
- gate.py
- Zee — Lane D · Domain packs and interface
- Authoring a domain pack
- Christian — Lane A · Integration and product owner
- Siew — Lane C · Governance and assurance
- 0001_init.sql
- Premium and Subsidy Tables
- HouseholdScope
- MediShield Life Benefits
- installed_packs
- Understanding integrated shield plans
- Yew Mun — Lane B · Retrieval and evaluation
- test_a_citation_that_resolves_to_nothing_still_says_what_it_said
- Alert
- 14 · A pack supplies what the core knows about a domain, and the core stays generic
- 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent
- test_reindexing_replaces_chunks_and_leaves_facts_alone
- The team
- scripts
- 0002_household.sql
- 0003_advice.sql
- test_a_client_that_leaves_after_the_card_commits_one_record
- quarantine.tsx
- Notice
- .retrieve
- 7. The answer graph ships before hybrid retrieval and before a checkpoint table
- .embed_documents
- 17 · A pack is grounding and persona; the core owns documents
- eslint.config.mjs
- grounding/__init__.py
- grounding/README.md
- About Integrated Shield Plan
- _as_response
- 1. Record architecture decisions
- test_an_advice_card_carries_a_rules_publisher_on_the_wire
- 4. Local setup can run before the household assistant is ready
- Data inventory — identity data, dates of birth and loans
- 6. pypdfium2 renders the page images the quarantine second pass reads
- createPseudoSheet
- generate_lim_documents.py
- CorrectionRequest
- .grounded
- _as_sentence
- .cite
- AdviceConsent
- .ref
- test_asking_whether_something_can_be_claimed_is_described_as_explain_to_the_router
- DenseRetriever
- test_advice_is_a_module
- test_help_runs_without_importing_core_before_sys_path_is_set
- test_an_unscoped_result_is_not_empty_for_the_owner
- test_each_policy_lapses_on_its_own
- .current

## God Nodes (most connected - your core abstractions)
1. `Settings` - 185 edges
2. `InstalledPack` - 154 edges
3. `ScriptedOllama` - 114 edges
4. `Passage` - 100 edges
5. `FakeConn` - 95 edges
6. `Ollama` - 92 edges
7. `ModelUnavailable` - 91 edges
8. `AnswerGraph` - 84 edges
9. `Sentence` - 76 edges
10. `settings()` - 75 edges

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

## Communities (236 total, 25 thin omitted)

### Community 0 - "get"
Cohesion: 0.24
Nodes (23): bundledBlob(), getDC(), Dispatcher(), getError(), load(), createHelmetManager(), applyCanvasBg(), compile() (+15 more)

### Community 1 - "packs/page.tsx"
Cohesion: 0.15
Nodes (10): ADR-0017, packs/page.tsx, dynamic, metadata, PacksPage(), runtime, Toggle(), ModuleSummary (+2 more)

### Community 2 - "Christian — task list"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.07
Nodes (45): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), Validate a document register before it is handed over. python -m…, Parse `field_pages`: semicolon-separated `name=page`, 1-based. Empty means page… (+37 more)

### Community 4 - "build_router"
Cohesion: 0.10
Nodes (30): CorrectionResponse, HouseholdResponse, ObligationChanged, PendingName, QuarantinedDocument, QuarantineResponse, What changed, in the words the screen confirms it with. `was` is returned…, The row is gone from Today. `speaks_again` is null when it will not come back.… (+22 more)

### Community 5 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 6 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 7 - "sha256"
Cohesion: 0.14
Nodes (13): The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, sha256(), Cursor, Insert or update the `documents` row for these bytes and say which happened.…, register_document(), cursor(), database_url(), The idempotent upsert, against the real unique index. `documents.sha256 UNIQUE`… (+5 more)

### Community 8 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (11): running-the-eval-harness/SKILL.md, Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness (+3 more)

### Community 9 - "support.js"
Cohesion: 0.12
Nodes (28): collectProps(), compileAttr(), compileTemplate(), contentKey(), cssToObj(), encodeCamelAttrs(), encodeCase(), evalDcLogic() (+20 more)

### Community 10 - "Desmond — task list"
Cohesion: 0.18
Nodes (11): Desmond — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 11 - "Zee — task list"
Cohesion: 0.22
Nodes (9): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20, W9 — due 2026-11-03 (+1 more)

### Community 12 - "test_ingest_pipeline.py"
Cohesion: 0.15
Nodes (18): printed_date(), A date as a document prints it, as YYYY-MM-DD, or None when it is not a date.…, parse(), The one call the pipeline makes. An unhandled mime type quarantines rather than…, _cell(), insurance(), iras(), _on_page() (+10 more)

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
Cohesion: 0.06
Nodes (45): Dispatcher, Inline, Queued, What happens to a document between "these bytes are registered" and "this…, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Hand the document to the worker and go back to watching the folder. (+37 more)

### Community 18 - "Person"
Cohesion: 0.15
Nodes (19): add_person(), owner(), owner_aliases(), Person, The person asking. `None` before setup has run, which every caller must handle:…, Every confirmed string that means the owner. This is what scopes a first-person…, The person a printed name means, or `None` if nobody has confirmed what it…, Add somebody, with the names they are known by on paper already confirmed.… (+11 more)

### Community 19 - "ingest/extract.py"
Cohesion: 0.10
Nodes (29): FieldSpec, One extractable field. Its `name` is the column header in Desmond's register…, One extractable field. Its `name` is the column header in Desmond's register and, ingest/extract.py, _coerce(), _date_renderings(), decode_schema(), _drop_format() (+21 more)

### Community 20 - "Household canon"
Cohesion: 0.25
Nodes (7): Address, Employment, Household canon, Life events that documents must reflect, People, Policies, Vehicles

### Community 21 - "install_best_effort"
Cohesion: 0.22
Nodes (13): lifespan(), install_best_effort(), Install at startup without being able to stop startup.      Both processes that, Install at startup without being able to stop startup. Both processes that own…, _beat_needs_its_own_process(), celery_argv(), main(), Run the ingestion worker, and optionally the nightly schedule with it. uv run… (+5 more)

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

### Community 29 - "test_modules.py"
Cohesion: 0.18
Nodes (21): already_said(), True when this exact window has already been mentioned. The comparison is by…, Everything inside a lead window that has not already been said for that window.…, sweep(), FakeConn, obligation_row(), Reminder and Alert: what fires, once, and with what behind it. Both modules are…, A sweep for a date in the future must record that date, or it repeats itself. (+13 more)

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

### Community 39 - "InstalledPack"
Cohesion: 0.05
Nodes (102): The record of every advised or withheld answer (ADR 0016). `advice_records`…, AdviceShape, One kind of advice question, and everything its calculator needs to answer it., One kind of advice question, and everything its calculator needs to answer it., AdviceLog, AdviceRecord, Adviser, Calculation (+94 more)

### Community 40 - "HouseholdAdviceLog"
Cohesion: 0.29
Nodes (6): HouseholdConsents, `core.graph.advice.ConsentBook` over a live connection, for the graph to ask…, HouseholdAdviceLog, `core.graph.advice.AdviceLog` over a live connection. `basis` is dumped with…, One construction for both. With any port missing the graph declines advice, so a, test_both_ask_endpoints_hand_the_graph_the_same_advice_ports()

### Community 41 - "Changelog"
Cohesion: 0.50
Nodes (3): Changelog, W1 · 2–8 Sep 2026, W2 · 9–15 Sep 2026

### Community 42 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 43 - "`docs/governance/` — the assurance artefacts"
Cohesion: 0.50
Nodes (4): governance/README.md, `docs/governance/` — the assurance artefacts, The autonomy statement in one line, The rule that governs all eight

### Community 51 - "_page_of_examples"
Cohesion: 0.18
Nodes (14): _page_of_examples(), One page printing every field's `example`, so each value is attributable to a…, `FieldSpec.name` is the `facts.key`. Nothing between the manifest and the row…, The named regression, spelled out so a future rename cannot quietly reintroduce…, One page printing every field's `example`, so each value is attributable to a pa, Each field's example as the model reports it; a repeating one as label and amoun, ADR 0017: several riders on one schedule, each a row pairing its label and its a, `FieldSpec.name` is the `facts.key`. Nothing between the manifest and the row re (+6 more)

### Community 52 - "The household, and the word "my""
Cohesion: 0.10
Nodes (20): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model (+12 more)

### Community 53 - "RegisteredPack"
Cohesion: 0.18
Nodes (13): _pack_row(), packs(), One row of `packs`, with the manifest validated back out of its jsonb column., No row in `packs` with that id., No row in `packs` with that id., Every installed pack. Documents and facts are the core's (ADR 0017), so none are, Every installed pack, with what it has extracted so far., Switch one pack on or off. Raises `UnknownPack` rather than silently doing nothi (+5 more)

### Community 54 - "alert/__init__.py"
Cohesion: 0.18
Nodes (18): alert/__init__.py, cpf_contributions_ytd(), days_uncovered(), donations_ytd(), Measurement, _per_subject(), The Alert module: a pack-declared threshold, crossed once, citing the documents…, Each holder's latest year-to-date total for this year: the largest, since it… (+10 more)

### Community 55 - "Basic Financial Planning Guide"
Cohesion: 0.15
Nodes (12): Basic Financial Planning Guide, Basic Financial Planning Guide, Basic Financial Planning Guide For Entrants To The Workforce, Basic Financial Planning Guide for those nearing retirement, Basic Financial Planning Guide For Those With Dependents, Emergency funds, For those approaching retirement, For those new to the workforce (+4 more)

### Community 56 - "test_household.py"
Cohesion: 0.05
Nodes (52): is_first_person(), Whether this question is about the person asking. `other_names` are the display…, Whether this question is about the person asking.      `other_names` are the d, _household_scope(), Who is asking, and whose documents may answer. Two halves, deliberately split.…, `HouseholdScope` over a roster held in memory, with every document resolved by…, `HouseholdScope` over a roster held in memory, with every document resolved by n, The roster has no grandparent relation, so the household says it the only way… (+44 more)

### Community 57 - "advice/__init__.py"
Cohesion: 0.04
Nodes (111): Advice, FactInput, A printed fact a calculator reads, named by where it is printed rather than…, A printed fact a calculator reads, named by where it is printed rather than what, What a pack that advises must say, once and in its own words, before it may., What a pack that advises must say, once and in its own words, before it may., RuleInput, Figure (+103 more)

### Community 58 - "cli.py"
Cohesion: 0.05
Nodes (74): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a…, paperbrain/ask.py, answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, paperbrain/chunk.py (+66 more)

### Community 59 - "client_for"
Cohesion: 0.10
Nodes (40): client(), client_for(), consent(), ConsentConn, open_obligation(), Snooze means 'not until this gets more urgent', so it can name the day it does., No new column: `already_said` is what makes the row quiet, and it reads this…, Snooze means 'not until this gets more urgent', so it can name the day it does. (+32 more)

### Community 60 - "Ollama"
Cohesion: 0.07
Nodes (67): ParsedDocument, ingest/quarantine.py, blocked_reasons(), forget(), page_images(), QuarantinedDocument, queue(), The second stage of quarantine: the page image, read by the vision-language… (+59 more)

### Community 61 - "test_pages.py"
Cohesion: 0.12
Nodes (28): page_count(), PageUnavailable, _pdfium(), One page of one document, as an image. Two callers want the same thing for…, Safe to show a person: there is no such page, or this file cannot be drawn., How many pages this file has, or 0 when it is not something with pages.…, `(bytes, media type)` for one page, one-based. An image document is returned…, render_page() (+20 more)

### Community 62 - "FakeOllama"
Cohesion: 0.12
Nodes (22): extract(), Never raises. A failure is a reason, and a reason routes the document to…, Never raises. A failure is a reason, and a reason routes the document to quarant, FakeOllama, Answers whatever the test told it to, and records what it was asked., Answers whatever the test told it to, and records what it was asked., test_a_date_that_cannot_be_read_still_quarantines(), test_a_long_document_whose_front_is_enough_is_read_once() (+14 more)

### Community 63 - "bench_runtime.py"
Cohesion: 0.09
Nodes (32): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+24 more)

### Community 64 - "compilerOptions"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 65 - "parse.py"
Cohesion: 0.11
Nodes (14): Block, DoclingParser, _kind(), _pages_from(), Parser, PlainTextParser, Turn captured bytes into pages of text, or say why it could not be done. Every…, Docling, held at arm's length: imported on first use, and never at module… (+6 more)

### Community 66 - "test_startup.py"
Cohesion: 0.08
Nodes (32): _kill_tree(), Stop a child and everything under it, then make sure it has gone., Start `npm run dev` in `web/`, or say plainly why it could not. Three reasons…, Stop the whole npm tree, not just the wrapper that was launched. This is the…, Stop the worker and the schedule it started, not just the launcher in front of…, start_web(), stop_web(), stop_worker() (+24 more)

### Community 67 - "ParsedPage"
Cohesion: 0.12
Nodes (25): ingest/chunk.py, Chunk, chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own… (+17 more)

### Community 68 - "registry.py"
Cohesion: 0.10
Nodes (28): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders…, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, Load the installed capability modules at runtime. The mirror of…, A module's YAML is missing, or does not validate against `ModuleManifest`. (+20 more)

### Community 69 - "ModelUnavailable"
Cohesion: 0.07
Nodes (40): commit_both_lanes(), document_title(), process(), _quarantine(), Parse, chunk, embed, extract, and commit both lanes in one transaction. The…, The document as a person would name it: its `string` fields as read, in declared, The document as a person would name it: its `string` fields as read, in the…, pgvector accepts its own text form; this avoids registering an adapter for one c (+32 more)

### Community 70 - "test_advice_module.py"
Cohesion: 0.07
Nodes (74): calculate(), names_for(), Drop rows a calculator cannot use, before deciding whether anything is missing.…, Drop rows a calculator cannot use, before deciding whether anything is missing., Each person's display name and confirmed aliases, trimmed and lower-cased the…, Each person's display name and confirmed aliases, trimmed and lower-cased the wa, One person's advice. The graph asks whose first when a question names several…, One person's advice. The graph asks whose first when a question names several pe (+66 more)

### Community 71 - "FakeCursor"
Cohesion: 0.10
Nodes (13): GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records…, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records, PendingValue, One value waiting for a person to sign off, with what they need to see to do it., _block(), One printed value, with everything a reviewer needs to sign off on it., _Connected (+5 more)

### Community 72 - "preview.tsx"
Cohesion: 0.11
Nodes (17): design-preview/page.tsx, metadata, answers, DesignPreview(), Direction, directions, Item, items (+9 more)

### Community 73 - "ConfigurationError"
Cohesion: 0.07
Nodes (47): approve(), pending(), A person's approval, standing between a model's extraction and any calculator…, Reject these ids with a note, ignoring any that are no longer `pending`., Every value still waiting for review, oldest first, optionally for one pack., Approve these ids, ignoring any that are no longer `pending`. Returns the count…, reject(), enabled_pack_ids() (+39 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (17): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+9 more)

### Community 75 - "load_register"
Cohesion: 0.18
Nodes (14): by_subject(), load_register(), Every batch1 row as the facts extraction would write, through the statement it u, Every batch1 row as the facts extraction would write, through the statement it…, One member's statement must never drive another member's 15,300 cap., One member's statement must never drive another member's 15,300 cap., On 10 February 2027 Marcus's home contents cover has lapsed, while his motor and, On 10 February 2027 Marcus's home contents cover has lapsed, while his motor… (+6 more)

### Community 76 - "obligations.py"
Cohesion: 0.24
Nodes (9): fixed(), from_facts(), _label(), Turn a dated fact into a commitment to do something about it. A fact is a…, What a person is shown. The key is the pack's word for it; the subject says…, Create the obligations the catalogue declares for these newly written facts., Create the obligations this pack declares for these newly written facts.…, Create the catalogue's calendar obligations — a filing deadline belongs to no do (+1 more)

### Community 77 - "Notion"
Cohesion: 0.29
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "Passage"
Cohesion: 0.06
Nodes (75): AnswerGraph, Built once, asked many times. Holds no connection: retrieval does., Built once, asked many times. Holds no connection: retrieval does., graph/__init__.py, The answer graph. Router, retrieve, rerank, grounding gate, then answer or…, Passage, What the graph needs from retrieval, stated as a contract rather than an…, The result of asking "whose is this?" of a question and its passages. (+67 more)

### Community 79 - "The demonstration run sheet"
Cohesion: 0.14
Nodes (14): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+6 more)

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (8): paperbrain/README.md, How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Contributing"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 82 - "[...path]/route.ts"
Cohesion: 0.16
Nodes (19): [...path]/route.ts, ALLOWED, Context, DELETE(), dynamic, forward(), GET(), PATCH() (+11 more)

### Community 83 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 84 - ".stream"
Cohesion: 0.04
Nodes (44): answer_system(), _asked(), _citations(), _either(), _max_sentences(), _numbered(), _pack_for(), The documents on file, narrowed to the same people the passages were. (+36 more)

### Community 85 - "sweep"
Cohesion: 0.29
Nodes (11): AlertConfig, Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), FakePack, One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order., One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order., srs_row(), test_a_firing_older_than_the_debounce_window_fires_again() (+3 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "contracts.py"
Cohesion: 0.05
Nodes (61): Answering, Categories, Category, Grounding, Guardrails, ModuleTrigger, Persona, The two contracts the whole platform is built on. Nothing else in the… (+53 more)

### Community 89 - "tokens/page.tsx"
Cohesion: 0.05
Nodes (36): lucide-react, react, (app)/layout.tsx, dynamic, runtime, Motion(), ROWS, tokens/page.tsx (+28 more)

### Community 90 - "lock.ts"
Cohesion: 0.13
Nodes (30): auth/route.ts, dynamic, GET(), grant(), POST(), runtime, unlock/page.tsx, dynamic (+22 more)

### Community 91 - "document-detail.tsx"
Cohesion: 0.24
Nodes (9): SourcePanel(), DocumentDetail(), when(), Field(), format(), isNumeric(), CorrectionResponse, pageImage() (+1 more)

### Community 92 - "DocumentCatalog"
Cohesion: 0.10
Nodes (28): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering (, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why the catalogue cannot supply `field` from every one of `doc_types`, or None., Whether any document type in the catalogue declares `field`., Every core document type, field and category this pack names exists, or ValueErr, _class_name(), _docstring() (+20 more)

### Community 94 - "boot"
Cohesion: 0.20
Nodes (10): boot(), dcNameFromPath(), getReactDOM(), parseDataProps(), parseDcDocument(), parseDcText(), rootNameForDocument(), safeDecode() (+2 more)

### Community 102 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "FakeConn"
Cohesion: 0.09
Nodes (33): conn(), FakeConn, pack_row(), The point of the endpoint. An UPDATE alone loses the example we are trying to…, The point of the endpoint. An UPDATE alone loses the example we are trying to co, The graph writes the record and never commits. The request that asked commits on, Starlette's own body iteration (`iterate_in_threadpool`) never calls `.close()`, The default database: two packs installed and enabled, and nothing else. (+25 more)

### Community 104 - "routes.py"
Cohesion: 0.08
Nodes (51): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, CloseRequest, ConfirmNameRequest, ConsentRequest, ConsentRequiredEvent (+43 more)

### Community 105 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 106 - "test_telegram_capture.py"
Cohesion: 0.07
Nodes (40): Safe to show: never contains the token., TelegramSettings, TelegramUnavailable, attribution(), A daemon thread that long-polls the Telegram bot until `stop()` or process…, One long poll. A failure waits rather than hammering the API with the same…, Whose phone this arrived on, recorded before anything is read off it. See ADR…, TelegramCapture (+32 more)

### Community 107 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 108 - "ScriptedOllama"
Cohesion: 0.06
Nodes (67): One sentence that has passed the gate, with the citations it passed on. It will…, One sentence that has passed the gate, with the citations it passed on.      I, Sentence, advised_pack(), build(), The advise branch: code calculates under consent, the model explains, and the…, Fix 1: a consumer that stops reading after the card and one sentence — a…, The `finally` that writes the advised record runs exactly once per stream,… (+59 more)

### Community 109 - "Settings"
Cohesion: 0.04
Nodes (82): create_app(), checks(), ready(), setup(), system_status(), The local API. Liveness is intentionally separate from assistant readiness.…, ModelWarmth, The page a person sees while Parrot starts, served by the engine itself. **Why… (+74 more)

### Community 110 - "vault.py"
Cohesion: 0.06
Nodes (42): _columns(), correct(), Corrected, CorrectionRejected, A person fixing a field the extractor got wrong. This is the one place in the…, `(value_text, value_num, value_date)` — exactly one of them set. The declared…, Store what a person says this field actually says, and keep what it used to…, Safe to show: there is no fact with that id. (+34 more)

### Community 111 - "dependencies"
Cohesion: 0.10
Nodes (20): ai, @ai-sdk/react, class-variance-authority, clsx, createComponentFactory(), lucide-react, next, next-themes (+12 more)

### Community 112 - "Claim"
Cohesion: 0.12
Nodes (33): check_advice(), check_one(), Claim, Why an advice explanation cannot be kept, or `None`. Asked of a claim built…, Why this one sentence cannot be kept, or `None` if it can. Depends on nothing…, test_a_claim_citing_the_same_document_twice_says_it_once(), test_a_grounded_claim_renders_its_document_and_page(), What the gate checks beyond "is there a citation". A cited sentence can still… (+25 more)

### Community 113 - "test_grounding_values.py"
Cohesion: 0.09
Nodes (45): number_tokens(), Every whole number the passage prints, thousands separators removed., _dropped(), _long_text(), Published values: the model reads a source, and code keeps only what the…, Assert a value was dropped, and logged with this reason., Returns the replies the test wrote, in order, then an empty list of values. A…, A truncated or non-JSON reply is an outage: the section was never actually… (+37 more)

### Community 114 - "household.py"
Cohesion: 0.09
Nodes (27): attribute(), classify_prompt(), confirm(), dismiss(), pending(), pending_count(), PendingAlias, person_for_chat() (+19 more)

### Community 115 - "GroundingCorpus"
Cohesion: 0.23
Nodes (18): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Read and validate a pack's grounding corpus from its own folder on disk. A…, A pack's grounding corpus on disk does not match what its `sources.yaml`…, Where this pack's grounding corpus lives on disk, or `None` if it declares none., Read, validate and hash every source this pack's corpus records. Raises… (+10 more)

### Community 116 - "TelegramAdapter"
Cohesion: 0.07
Nodes (33): CaptureAdapter, IngestJob, The one interface every capture channel satisfies. receive(payload, mime,…, Magic bytes first, filename suffix second, `application/octet-stream` last. A…, What a capture returns: a registered document, and whether we had seen it…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sniff_mime(), _Pending (+25 more)

### Community 117 - "_advised"
Cohesion: 0.11
Nodes (24): _advised(), _checked(), _market(), _market_compares_an_undeclared_field(), A market comparison of the held hospital plan, on `compare_fields`, ordered by…, A market comparison of the held hospital plan, on `compare_fields`, ordered by p, Only income is made annual, so only income may say how often its printed figure…, `annual_premium` is printed on no policy schedule; the market's sources publish… (+16 more)

### Community 118 - "test_lifecycle.py"
Cohesion: 0.11
Nodes (25): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor.…, What the person asked for, once. The first request wins; later ones change…, _client(), _eventually(), _launcher(), quiet_engine(), Restart and shut down: the engine asks its supervisor, and nothing else can ask… (+17 more)

### Community 120 - "app/layout.tsx"
Cohesion: 0.22
Nodes (8): next-themes, app/layout.tsx, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 122 - "test_contracts.py"
Cohesion: 0.10
Nodes (33): check_advice_links(), Every fact an advice shape reads from another pack is declared by an installed…, _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact() (+25 more)

### Community 123 - "SentenceScanner"
Cohesion: 0.10
Nodes (27): Pulling finished sentences out of a JSON reply that is still being written. The…, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner, drip() (+19 more)

### Community 124 - "reminder/__init__.py"
Cohesion: 0.11
Nodes (18): reminder/__init__.py, current_lead(), Due, next_window(), Overdue, The Reminder module: a nightly sweep of obligations, and nothing fires twice.…, Past their date and never closed. A different problem from a reminder, shown…, Safe to show: there is no obligation with that id, or it is already closed. (+10 more)

### Community 125 - "Household canon"
Cohesion: 0.04
Nodes (43): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, Policies, The family tree, and why three of them are not called Lim (+35 more)

### Community 126 - "item-row.tsx"
Cohesion: 0.16
Nodes (13): SourceChip(), stripTrailingPage(), ADR-0016, countdown(), detail(), figure(), ItemRow(), longDate() (+5 more)

### Community 127 - "createExternalModules"
Cohesion: 0.25
Nodes (11): cdnScriptFor(), createExternalModules(), ensureBabel(), resolve2(), resolveGlobal(), waitForGlobal(), isElementClass(), isRenderableType() (+3 more)

### Community 128 - "FolderAdapter"
Cohesion: 0.10
Nodes (29): FolderAdapter, FolderSettings, Every file in the watched folder that is worth looking at at all., Advance the debounce by `elapsed` seconds and return the files now ready. Time…, Satisfies `CaptureAdapter`. Holds no database handle — it is given a…, FolderCapture, Begin watching. Returns False, with a logged reason, when it cannot., Begin polling. Returns False, with a logged reason, when it cannot or should… (+21 more)

### Community 129 - "test_grounding_index.py"
Cohesion: 0.09
Nodes (40): SourceText, index_pack(), IndexReport, Index a pack's published sources, and stage the values they print for a person…, Upsert this pack's sources and stage the values a changed one prints. A pack…, Upsert this pack's sources and stage the values a changed one prints.      A p, Insert or refresh the source's row, and return its id., Insert or refresh the source's row, and return its id. (+32 more)

### Community 130 - "FakeConn"
Cohesion: 0.36
Nodes (8): advised_pack(), FakeConn, The insurance pack with a fixture advice block. The real wording is Zee's, revie, The insurance pack with a fixture advice block. The real wording is Zee's,…, test_a_price_goes_stale_sooner_than_a_rule(), test_advice_is_calculated_for_exactly_one_person(), test_an_unanswerable_shape_reads_nothing_more(), test_the_category_filter_leaves_a_hospital_cash_plan_out_of_critical_illness_cover()

### Community 131 - "connection"
Cohesion: 0.15
Nodes (12): ModuleSummary, PacksResponse, PackSummary, _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack() (+4 more)

### Community 132 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 133 - "scope.py"
Cohesion: 0.12
Nodes (23): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Whose question is this, and whose documents may answer it. "What is my term… (+15 more)

### Community 134 - "api.ts"
Cohesion: 0.06
Nodes (39): household/page.tsx, dynamic, metadata, runtime, AdviceConsentSection(), Load, STATUS, ADR-0016 (+31 more)

### Community 135 - "team/README.md"
Cohesion: 0.19
Nodes (11): packs/README.md, christian/README.md, christian/tasks.md, desmond/README.md, desmond/tasks.md, team/README.md, siew/README.md, siew/tasks.md (+3 more)

### Community 136 - "today/page.tsx"
Cohesion: 0.07
Nodes (35): next, HouseholdPage(), AppLayout(), today/page.tsx, dynamic, isUrgent(), metadata, runtime (+27 more)

### Community 137 - "scope_passages"
Cohesion: 0.19
Nodes (15): Keep the owner's passages and the household's; set aside everybody else's. A…, Keep the owner's passages and the household's; set aside everybody else's., scope_passages(), _conn_returning(), _passage(), The third bucket. Home contents, a utility bill — nobody's name on it,…, The third bucket. Home contents, a utility bill — nobody's name on it, everybody, A joint policy is the owner's too. Presence wins over exclusion. (+7 more)

### Community 138 - "test_api.py"
Cohesion: 0.06
Nodes (34): a_citation(), FakeGraph, graph(), inbox(), The five endpoints, against a fake database and the real queries. The…, Stands in for `AnswerGraph` at the seam `api/routes.py` owns., Stands in for `AnswerGraph` at the seam `api/routes.py` owns., What a retrieved passage hands over: the sentence a person reads, and the id a… (+26 more)

### Community 139 - "values.py"
Cohesion: 0.08
Nodes (35): A rule or table value a pack's sources publish. Extracted automatically,…, A rule or table value a pack's sources publish.      Extracted automatically,, ValueKey, _check(), collapse(), _cuts_a_number(), extract_values(), ExtractedValue (+27 more)

### Community 140 - "FakeConn"
Cohesion: 0.13
Nodes (28): current(), grant(), _latest(), NoOwner, The owner's consent to a pack's advice, append-only (ADR 0016). Consent is the…, Record the owner saying yes to `wording`, this pack's consent text at…, Record the owner taking it back. Append-only: the grant stays in the table,…, No owner is recorded yet, so there is nobody whose consent this could be (ADR… (+20 more)

### Community 141 - "StreamingGraph"
Cohesion: 0.09
Nodes (28): Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive…, No `reading` before it: the floor is checked before the model is asked anything., The promise the whole design rests on: a sentence and its chips arrive together,, By then the 200 has been sent. An exception that only logged would leave a… (+20 more)

### Community 142 - "PackManifest"
Cohesion: 0.10
Nodes (19): PackManifest, A domain pack, authored as one YAML file., (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why this pack cannot supply `field` from every one of `doc_types`, or None if…, An advice shape that names a missing role, field, category or key fails at load…, A domain pack, authored as one YAML file: grounding, persona, answering and advi, An advice shape that names a missing role or key fails at load time., A compared field no document type of the shape declares can never be printed.… (+11 more)

### Community 143 - "export-design-preview.cjs"
Cohesion: 0.11
Nodes (17): bundle(), classes, css, cssFile, domId, fs, ids, licences (+9 more)

### Community 144 - "devDependencies"
Cohesion: 0.10
Nodes (21): eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node, @types/react (+13 more)

### Community 145 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents

### Community 146 - "Comparison of Integrated Shield Plans"
Cohesion: 0.18
Nodes (10): Common reasons why insurers do not provide a Letter of Guarantee in specific cases, Common reasons why insurers may reject or not pay for claims, Comparison of Integrated Shield Plans, Comparison of lifetime premiums, Important Information, Letter of Guarantee, List of Integrated Shield Plans (IPs) and their targeted level of coverage, Medical Record Costs (+2 more)

### Community 147 - "Domain packs — start here"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 149 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 150 - "schedule.py"
Cohesion: 0.19
Nodes (13): The one Celery application, built from `Settings`. Every setting here is a…, beat_schedule(), cron_expressions(), crontab_from(), manifest(), When the nightly sweeps run, read from the modules' own manifests. A module…, A five-field cron expression as Celery understands it., The cron line for each swept module, by module id. Testable without Celery… (+5 more)

### Community 151 - "ErrorEvent"
Cohesion: 0.22
Nodes (10): ErrorEvent, The stream broke after it began. A client cannot read an HTTP status by then., The stream broke after it began. A client cannot read an HTTP status by then., _answer_events(), ask_stream(), events(), One event, in the wire format. `kind` is on the payload, so no `event:` line is…, One event, in the wire format. `kind` is on the payload, so no `event:` line is (+2 more)

### Community 152 - "test_one_document_is_shown_even_when_its_pack_is_off"
Cohesion: 0.16
Nodes (14): document_row(), fact_row(), filed_document(), ADR 0017: disabling insurance_agent switches off its voice, never a household's, v1 keeps the inbox as the document store, so this is a real state, not a fault., v1 keeps the inbox as the document store, so this is a real state, not a fault., Following a citation must never end in a blank screen because a pack was…, Following a citation must never end in a blank screen because a pack was switche (+6 more)

### Community 153 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "adr/README.md"
Cohesion: 0.06
Nodes (27): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision, 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision (+19 more)

### Community 155 - "test_an_empty_registry_shows_everything_rather_than_nothing"
Cohesion: 0.10
Nodes (21): obligation(), overdue_row(), One row of `reminder.OVERDUE`, in its column order., One row of `reminder.OVERDUE`, in its column order., The nightly sweep owns `last_notified_at`. A screen refresh must not burn a…, The nightly sweep owns `last_notified_at`. A screen refresh must not burn a wind, A registry that failed to install must fail loudly, not silently silence the…, A registry that failed to install must fail loudly, not silently silence the hou (+13 more)

### Community 156 - "package.json"
Cohesion: 0.11
Nodes (16): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+8 more)

### Community 157 - "_today_items"
Cohesion: 0.20
Nodes (12): A document and a page, as a person would cite it., Source, TodayItem, TodayResponse, today(), _cite(), _link(), Split a formatted citation back into its parts, keeping the text either way.… (+4 more)

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

### Community 164 - "send_retry"
Cohesion: 0.20
Nodes (10): ForgottenDocument, 202. The vision pass is slower than a page load, so it is queued and this is…, A quarantined document Parrot no longer remembers., A quarantined document Parrot no longer remembers., RetryAccepted, forget_one(), retry_one(), Put one quarantine retry on the queue and return its task id.      The vision pa (+2 more)

### Community 165 - "Understanding health insurance"
Cohesion: 0.20
Nodes (9): Assistance under MediFund, Basic health insurance coverage, Choosing your level of coverage, How MediSave fits in, If you have company health insurance, If you want more coverage, Types of health insurance plans, Understanding health insurance (+1 more)

### Community 166 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 168 - "test_advice_core.py"
Cohesion: 0.28
Nodes (14): _kind_of(), passages_for(), `"fact:12"` -> `"fact"`, `"rule:7"` -> `"rule"`. Anything else is a calculator…, Inputs as kind fact/rule passages (chunk_id from the ref), and the figures as…, check_content(), Why a cited sentence still cannot be kept, or `None`. Asked after `check_one`…, _calculation(), The types a calculator hands back, the owner's consent, and the record of an… (+6 more)

### Community 169 - "packs.py"
Cohesion: 0.10
Nodes (23): DocumentTypeSpec, One kind of document the core recognises., One kind of document this pack recognises., Classification, classify(), _prompt(), Decide which pack's document type a captured document is, or decline to. The…, Never raises. An unavailable model is a classification failure, so it… (+15 more)

### Community 170 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 171 - "igd-capstone-2026"
Cohesion: 0.20
Nodes (10): Authoring a pack, igd-capstone-2026, `main` is not protected, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live (+2 more)

### Community 173 - "gate.py"
Cohesion: 0.12
Nodes (18): Exclusions, A sentence claiming cover whose every citation sits under one of `headings` is…, A sentence claiming cover whose every citation sits under one of `headings` is d, check(), _normal(), The grounding gate. Rule 3 in AGENTS.md: no claim without a citation. This…, Never raises, never rewrites a claim. It keeps, drops, or abstains. The whole-…, "1,860.00", "1860" and "01" → "1860", "1860", "1": formatting is not a… (+10 more)

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

### Community 178 - "0001_init.sql"
Cohesion: 0.36
Nodes (7): chunks, documents, facts, modules, obligations, packs, traces

### Community 179 - "Premium and Subsidy Tables"
Cohesion: 0.33
Nodes (5): MediShield Life Premium Schedule for Singapore Citizens and Permanent Residents, Merdeka Generation Subsidy, Pioneer Generation Subsidy, Premium and Subsidy Tables, Premium Subsidy for the Lower- to Middle-Income

### Community 180 - "HouseholdScope"
Cohesion: 0.25
Nodes (8): HouseholdScope, What `AnswerGraph` is handed so it can scope without holding a connection.…, What `AnswerGraph` is handed so it can scope without holding a connection., A fresh install is not broken. It answers about the household, as it always…, A fresh install is not broken. It answers about the household, as it always did., test_a_household_with_no_owner_scopes_nothing(), test_my_dads_question_is_scoped_to_the_parent_and_an_unknown_relation_says_so(), test_whose_says_no_owner_when_nobody_has_claimed_the_household()

### Community 181 - "MediShield Life Benefits"
Cohesion: 0.33
Nodes (5): Exclusions under MediShield Life, Fertility Preservation Procedures in cases of potential iatrogenic infertility, List of Serious Pregnancy and Delivery-related Complications, MediShield Life Benefits, MediShield Life Benefits

### Community 182 - "installed_packs"
Cohesion: 0.20
Nodes (10): installed_packs(), _load_one(), Every pack directory holding a pack.yaml, in a stable order. Directories whose…, Every pack directory holding a pack.yaml, in a stable order.      Directories wh, test_every_installed_pack_still_loads(), test_every_pack_speaks_only_for_catalogue_types(), test_every_document_type_has_a_generated_model(), test_the_template_directory_is_not_an_installed_pack() (+2 more)

### Community 183 - "Understanding integrated shield plans"
Cohesion: 0.29
Nodes (6): Are you covered?, Should you upgrade to an IP?, The deductible is the fixed amount you pay each policy year – ranging from $1,500 to $3,500, depending on ward class – before any payout from your IP. The co-payment is 5% of the bill, capped at a minimum of $6,000 per year., Understanding integrated shield plans, Your budget, Your comfort level with the types of hospitals, wards and doctors

### Community 184 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

### Community 185 - "test_a_citation_that_resolves_to_nothing_still_says_what_it_said"
Cohesion: 0.29
Nodes (7): Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with…, Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with ev, A deleted document must not take the sentence down with it., A deleted document must not take the sentence down with it., test_a_citation_that_resolves_to_nothing_still_says_what_it_said(), test_an_alerts_citation_carries_the_document_it_opens(), uncovered_since()

### Community 186 - "Alert"
Cohesion: 0.20
Nodes (7): Alert, _debounced(), What the debounce is keyed on: this metric, for this person and thing, in this…, Two lapsed policies on one person are two alerts, and saying one must not silenc, Two lapsed policies on one person are two alerts, and saying one must not…, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

### Community 187 - "14 · A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.33
Nodes (6): 14 · A pack supplies what the core knows about a domain, and the core stays generic, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 188 - "16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.29
Nodes (7): 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent, Addendum, 17 September 2026: coverage review and the adult rule, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 190 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 191 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 192 - "0002_household.sql"
Cohesion: 0.70
Nodes (4): document_attribution, people, person_aliases, telegram_identities

### Community 193 - "0003_advice.sql"
Cohesion: 0.60
Nodes (4): advice_consents, advice_records, grounding_sources, grounding_values

### Community 194 - "test_a_client_that_leaves_after_the_card_commits_one_record"
Cohesion: 0.18
Nodes (12): next_kind(), The kind of the next event on the wire., Starlette never closes a body iterator a disconnected client stopped pulling. `_, The ruling's case as it happens on a socket: Starlette sends the card and at onc, What the API owns when a stream is closed with the graph still parked on the car, C5 fix round 2 closed the gap this test used to mark: `AdviceCard` is now yielde, The graph's own cleanup can fail -- for example the record insert raises -- and, test_a_client_that_leaves_after_the_card_commits_one_record() (+4 more)

### Community 195 - "quarantine.tsx"
Cohesion: 0.29
Nodes (4): GoneRow(), QuarantineQueue(), QuarantineRow(), QuarantinedDocument

### Community 196 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 197 - ".retrieve"
Cohesion: 0.33
Nodes (5): fuse(), Several searches as one list: each passage once, at the best score any phrasing…, Several searches as one list: each passage once, at the best score any phrasing, Every phrasing of the question, searched and fused. The person's own words…, Every phrasing of the question, searched and fused. The person's own words alway

### Community 198 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 199 - ".embed_documents"
Cohesion: 0.33
Nodes (4): A question, embedded the way the model was trained to embed a search query., Passages as `(title, text)`, embedded the way the model was trained to embed a…, Whether this embedding model expects `QUERY_PROMPT` and `DOCUMENT_PROMPT`., uses_task_prompts()

### Community 200 - "17 · A pack is grounding and persona; the core owns documents"
Cohesion: 0.33
Nodes (6): 17 · A pack is grounding and persona; the core owns documents, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 201 - "eslint.config.mjs"
Cohesion: 0.50
Nodes (3): @eslint/eslintrc, compat, eslintConfig

### Community 204 - "About Integrated Shield Plan"
Cohesion: 0.33
Nodes (5): About Integrated Shield Plan, How do I find out if I have an Integrated Shield Plan?, How do Integrated Shield Plan premiums and claims work?, Should I consider purchasing an Integrated Shield Plan?, What is an Integrated Shield Plan?

### Community 205 - "_as_response"
Cohesion: 0.18
Nodes (11): AskResponse, Claim, The whole answer, once. `text` is the consent wording when `kind` is `consent_re, One sentence and the passages it was traced to. Never emitted without…, One sentence and the passages it was traced to. Never emitted without `citations, _as_response(), _as_source(), One `Answer` to one of the shapes a client has to handle. (+3 more)

### Community 206 - "1. Record architecture decisions"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 207 - "test_an_advice_card_carries_a_rules_publisher_on_the_wire"
Cohesion: 0.33
Nodes (7): advice_card(), A published value's chip: no document and no page, only who published it and whe, A published number has no page to open. What makes it checkable is who published, Nothing shown, nothing recorded. Once advice is on the screen, a failure after i, rule_citation(), test_an_advice_card_carries_a_rules_publisher_on_the_wire(), test_an_answer_that_fails_before_any_advice_is_rolled_back_and_after_it_is_kept()

### Community 208 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 209 - "Data inventory — identity data, dates of birth and loans"
Cohesion: 0.40
Nodes (4): Data inventory — identity data, dates of birth and loans, Open questions for Siew, The inventory, What this entry covers

### Community 210 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 211 - "createPseudoSheet"
Cohesion: 0.67
Nodes (4): createPseudoSheet(), importantify(), scanUnquotedUrl(), stripComments()

### Community 212 - "generate_lim_documents.py"
Cohesion: 0.50
Nodes (4): find_browser_executable(), generate_documents(), Project Parrot - Synthetic Document Generator for Lim Household ===============, Find Microsoft Edge or Google Chrome executable on Windows.

### Community 213 - "CorrectionRequest"
Cohesion: 0.67
Nodes (3): CorrectionRequest, What the person typed. The pack decides what type it is; the caller does not…, What the person typed. The pack decides what type it is; the caller does not get

### Community 215 - "_as_sentence"
Cohesion: 0.67
Nodes (3): _as_sentence(), "which age band applies" -> "Which age band applies.": a pack's wording and a…, "which age band applies" -> "Which age band applies.": a pack's wording and a ca

### Community 217 - "AdviceConsent"
Cohesion: 0.50
Nodes (4): AdviceConsent, One advising pack, the wording a person is asked to agree to, and what the owner, _as_consent(), One advising pack's consent wording and the owner's standing answer to it.

### Community 221 - "test_asking_whether_something_can_be_claimed_is_described_as_explain_to_the_router"
Cohesion: 0.67
Nodes (3): 14 September: "warded for dengue 3 days, can claim?" was declined as advice…, 14 September: "warded for dengue 3 days, can claim?" was declined as advice beca, test_asking_whether_something_can_be_claimed_is_described_as_explain_to_the_router()

### Community 222 - "DenseRetriever"
Cohesion: 0.12
Nodes (14): AskRequest, ask(), _graph_for(), _history(), The conversation so far, as the graph reads it. Empty for a first question., The conversation so far, as the graph reads it. Empty for a first question., DenseRetriever, NoReranker (+6 more)

### Community 224 - "test_advice_is_a_module"
Cohesion: 0.67
Nodes (3): ADR 0016: calculators are a module, so `modules/advice/module.yaml` must load., ADR 0016: calculators are a module, so `modules/advice/module.yaml` must load., test_advice_is_a_module()

### Community 232 - "test_help_runs_without_importing_core_before_sys_path_is_set"
Cohesion: 0.67
Nodes (3): `--help` must work even though `core` is not on `sys.path` until the script…, `--help` must work even though `core` is not on `sys.path` until the script inse, test_help_runs_without_importing_core_before_sys_path_is_set()

### Community 233 - "test_an_unscoped_result_is_not_empty_for_the_owner"
Cohesion: 0.67
Nodes (3): `empty_for_owner` must never fire on a question that was never scoped —…, `empty_for_owner` must never fire on a question that was never scoped — otherwis, test_an_unscoped_result_is_not_empty_for_the_owner()

### Community 234 - "test_each_policy_lapses_on_its_own"
Cohesion: 0.67
Nodes (3): A live travel policy must not make a lapsed motor policy read as covered., A live travel policy must not make a lapsed motor policy read as covered., test_each_policy_lapses_on_its_own()

## Knowledge Gaps
- **736 isolated node(s):** `npx`, `@modelcontextprotocol/server-filesystem`, `api/__init__.py`, `core/__init__.py`, `grounding/__init__.py` (+731 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `FolderAdapter`, `FakeConn`, `connection`, `build_router`, `sha256`, `test_api.py`, `StreamingGraph`, `test_worker_queue.py`, `install_best_effort`, `schedule.py`, `test_one_document_is_shown_even_when_its_pack_is_off`, `test_an_empty_registry_shows_everything_rather_than_nothing`, `test_modules.py`, `send_retry`, `InstalledPack`, `FakeCursor`, `RegisteredPack`, `test_household.py`, `test_a_citation_that_resolves_to_nothing_still_says_what_it_said`, `client_for`, `Ollama`, `bench_runtime.py`, `test_startup.py`, `registry.py`, `ModelUnavailable`, `test_advice_module.py`, `ConfigurationError`, `Passage`, `FakeConn`, `routes.py`, `test_telegram_capture.py`, `test_lifecycle.py`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `InstalledPack` connect `InstalledPack` to `test_grounding_index.py`, `FakeConn`, `test_api.py`, `StreamingGraph`, `PackManifest`, `ingest/extract.py`, `packs.py`, `RegisteredPack`, `installed_packs`, `alert/__init__.py`, `advice/__init__.py`, `client_for`, `FakeOllama`, `registry.py`, `ModelUnavailable`, `test_advice_module.py`, `FakeCursor`, `ConfigurationError`, `obligations.py`, `Passage`, `.stream`, `sweep`, `contracts.py`, `AdviceConsent`, `DocumentCatalog`, `DenseRetriever`, `FakeConn`, `routes.py`, `ScriptedOllama`, `GroundingCorpus`, `test_contracts.py`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Why does `ModelUnavailable` connect `ModelUnavailable` to `test_grounding_index.py`, `InstalledPack`, `FakeCursor`, `packs.py`, `ConfigurationError`, `ScriptedOllama`, `Settings`, `Passage`, `test_ingest_pipeline.py`, `test_worker_queue.py`, `household.py`, `Person`, `ingest/extract.py`, `test_grounding_values.py`, `Ollama`, `FakeOllama`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 149 inferred relationships involving `Settings` (e.g. with `create_app()` and `_Answering`) actually correct?**
  _`Settings` has 149 INFERRED edges - model-reasoned connections that need verification._
- **Are the 84 inferred relationships involving `InstalledPack` (e.g. with `_Answering` and `DocumentCatalog`) actually correct?**
  _`InstalledPack` has 84 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `ScriptedOllama` (e.g. with `Abstained` and `AnswerGraph`) actually correct?**
  _`ScriptedOllama` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 57 inferred relationships involving `Passage` (e.g. with `AdviceLog` and `AdviceRecord`) actually correct?**
  _`Passage` has 57 INFERRED edges - model-reasoned connections that need verification._