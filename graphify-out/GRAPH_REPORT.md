# Graph Report - igd-wt-agent  (2026-09-17)

## Corpus Check
- 269 files · ~649,160 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3866 nodes · 9622 edges · 228 communities (208 shown, 20 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 1210 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `40f90489`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_parrot.py
- page.tsx
- Christian — task list
- validate
- isUnlocked
- Project PARROT — team split
- Project PARROT — team split
- IngestJob
- Running the evaluation harness
- support.js
- Desmond — task list
- Zee — task list
- Yew Mun — task list
- answer.tsx
- Filling the corpus register
- Writing a governance artefact
- Claude Code — read this first
- test_worker_queue.py
- test_household.py
- extract.py
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
- README.md
- Project skills
- Evaluation
- pull_request_template.md
- ModelUnavailable
- routes.py
- Changelog
- filesystem
- `docs/governance/` — the assurance artefacts
- __init__.py
- __init__.py
- parrot
- Ollama
- 0011-the-household-is-people-and-aliases-and-the-owner-is-one-of-them.md
- extract.py
- __init__.py
- ingest.py
- _household_scope
- __init__.py
- cli.py
- settings
- State
- test_pages.py
- FakeOllama
- bench_runtime.py
- compilerOptions
- parse.py
- test_startup.py
- pipeline.py
- registry.py
- Ollama
- test_advice_module.py
- test_grounding_index.py
- preview.tsx
- api.ts
- Starting Parrot
- Any
- DenseRetriever
- Notion
- test_answer_graph.py
- The demonstration run sheet
- PaperBrain
- Contributing
- route.ts
- components.json
- Passage
- page.tsx
- Architecture
- Roadmap
- pack
- power-menu.tsx
- lock.ts
- Settings
- build.py
- InstalledPack
- Registration
- Home Contents Insurance Policy
- __init__.py
- __init__.py
- __init__.py
- __init__.py
- setup.sh
- 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module
- rows_for
- _Answering
- 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack
- test_telegram_capture.py
- Siew — task list
- page.tsx
- .load
- PackUnavailable
- dependencies
- Claim
- test_grounding_values.py
- household.py
- SourceText
- TelegramAdapter
- HouseholdInventory
- test_lifecycle.py
- __init__.py
- layout.tsx
- Answer
- test_contracts.py
- SentenceScanner
- __init__.py
- Household canon
- route.ts
- page.tsx
- FolderAdapter
- ScriptedClient
- Any
- _answer_events
- 10. `main` is unprotected, and the discipline is human
- scope.py
- document-detail.tsx
- item-row.tsx
- values.py
- test_api.py
- ModuleAdviser
- test_advice_core.py
- FakeConn
- PackManifest
- layout.tsx
- devDependencies
- Working agreement for coding agents
- review_grounding_values.py
- Domain packs — start here
- Desmond — Lane E · Corpus and adversarial testing
- schedule.py
- test_ingest_pipeline.py
- Any
- 2. One PostgreSQL instance for everything
- README.md
- obligation
- _today_items
- postcss.config.mjs
- 4. Writing `pack.yaml`
- 13. A question is understood before it is searched, and scoped before it is cut
- Try PARROT
- github.md
- walk
- obligations.py
- gate.py
- Notebook prompts — the four full policies for Marcus Lim
- application
- check_content
- classify.py
- First run
- igd-capstone-2026
- FakeCursor
- boot
- Zee — Lane D · Domain packs and interface
- Authoring a domain pack
- Christian — Lane A · Integration and product owner
- Siew — Lane C · Governance and assurance
- 0001_init.sql
- createRuntime
- start_parrot.py
- FactRow
- advice_consent.py
- corrections.py
- Yew Mun — Lane B · Retrieval and evaluation
- .json
- contracts.py
- 14 · A pack supplies what the core knows about a domain, and the core stays generic
- 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent
- page.tsx
- The team
- gate.py
- 0002_household.sql
- 0003_advice.sql
- test_a_client_that_leaves_after_the_card_commits_one_record
- test_a_document_still_in_the_inbox_is_not_forgotten
- Notice
- Registration
- 7. The answer graph ships before hybrid retrieval and before a checkpoint table
- test_advice_core.py
- ScriptedOllama
- eslint.config.mjs
- __init__.py
- README.md
- FakeCursor
- chunk.py
- The household, and the word "my"
- test_an_advice_card_carries_a_rules_publisher_on_the_wire
- next.config.ts
- FakeCursor
- is_first_person
- installed_packs
- find_browser_executable
- ClosingSpy
- HouseholdAdviceLog
- _Value
- 6. pypdfium2 renders the page images the quarantine second pass reads
- NNNN · The decision, as a statement not a question
- 12. Chunks follow the document's headings, and embeddings use the model's task prompts
- page.tsx
- 17 · A pack is grounding and persona; the core owns documents
- 5. The watched folder is polled for stability, not subscribed to for events
- 1. Record architecture decisions
- 4. Local setup can run before the household assistant is ready
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- 15. A name scopes a question, and a grandparent is not a parent
- test_a_grounding_corpus_travels_inside_its_pack
- test_the_debounce_key_separates_two_policies_of_one_person

## God Nodes (most connected - your core abstractions)
1. `InstalledPack` - 135 edges
2. `ScriptedOllama` - 108 edges
3. `Passage` - 95 edges
4. `FakeConn` - 94 edges
5. `Settings` - 87 edges
6. `AnswerGraph` - 80 edges
7. `ModelUnavailable` - 78 edges
8. `Ollama` - 78 edges
9. `Sentence` - 73 edges
10. `settings()` - 73 edges

## Surprising Connections (you probably didn't know these)
- `_settings()` --indirect_call--> `settings()`  [INFERRED]
  api/routes.py → tests/test_api.py
- `_Answering` --uses--> `HouseholdAdviceLog`  [INFERRED]
  api/routes.py → core/advice_records.py
- `_Answering` --uses--> `Answer`  [INFERRED]
  api/routes.py → core/graph/answer.py
- `_Answering` --uses--> `AnswerGraph`  [INFERRED]
  api/routes.py → core/graph/answer.py
- `_Answering` --uses--> `DenseRetriever`  [INFERRED]
  api/routes.py → core/graph/baseline.py

## Import Cycles
- None detected.

## Communities (228 total, 20 thin omitted)

### Community 0 - "run_parrot.py"
Cohesion: 0.15
Nodes (22): _kill_tree(), main(), parse_args(), port_answers(), Any, Namespace, Popen, Run the engine, the folder watcher, the ingestion worker and the screens togethe (+14 more)

### Community 1 - "page.tsx"
Cohesion: 0.13
Nodes (15): createRegistry(), HouseholdPage(), AppLayout(), isUrgent(), metadata, summary(), TodayPage(), VaultPage() (+7 more)

### Community 2 - "Christian — task list"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.10
Nodes (41): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+33 more)

### Community 4 - "isUnlocked"
Cohesion: 0.52
Nodes (6): ACTIONS, GET(), POST(), sameOrigin(), unlocked(), isUnlocked()

### Community 5 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 6 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 7 - "IngestJob"
Cohesion: 0.09
Nodes (25): CaptureAdapter, datetime, Protocol, The one interface every capture channel satisfies.      receive(payload, mime,, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256` i, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sha256(), Capture adapters.  Every channel a document can arrive through satisfies one i (+17 more)

### Community 8 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 9 - "support.js"
Cohesion: 0.10
Nodes (12): cdnScriptFor(), compileTemplate(), contentKey(), dcNameFromPath(), encodeCamelAttrs(), encodeCase(), isElementClass(), isRenderableType() (+4 more)

### Community 10 - "Desmond — task list"
Cohesion: 0.18
Nodes (11): Desmond — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 11 - "Zee — task list"
Cohesion: 0.22
Nodes (9): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20, W9 — due 2026-11-03 (+1 more)

### Community 12 - "Yew Mun — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

### Community 13 - "answer.tsx"
Cohesion: 0.15
Nodes (15): Advice, AdviceCard(), AdviceNote(), AdviceWithheld(), capitalise(), sentence(), TONES, ADR-0016 (+7 more)

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
Cohesion: 0.09
Nodes (37): Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker.      Celery is imported here, bytes_for(), index_folder(), LookupError, Path (+29 more)

### Community 18 - "test_household.py"
Cohesion: 0.13
Nodes (28): Keep the owner's passages and the household's; set aside everybody else's., scope_passages(), conn(), _conn_returning(), _passage(), Any, Who is asking, and whose documents may answer.  Two halves, deliberately split, The third bucket. Home contents, a utility bill — nobody's name on it, everybody (+20 more)

### Community 19 - "extract.py"
Cohesion: 0.13
Nodes (21): _coerce(), _date_renderings(), decode_schema(), _drop_format(), _normalise(), _prepare(), printed_date(), Any (+13 more)

### Community 20 - "Household canon"
Cohesion: 0.25
Nodes (7): Address, Employment, Household canon, Life events that documents must reflect, People, Policies, Vehicles

### Community 21 - "retrieve.py"
Cohesion: 0.15
Nodes (22): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a, ndarray, load_matrix(), pack(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.  Des, Return (N x D matrix of normalised embeddings, chunk ids)., stats() (+14 more)

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

### Community 29 - "test_modules.py"
Cohesion: 0.15
Nodes (19): FakeConn, obligation_row(), datetime, A sweep for a date in the future must record that date, or it repeats itself., One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order., srs_row(), test_a_dry_run_records_nothing(), test_a_firing_older_than_the_debounce_window_fires_again() (+11 more)

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

### Community 39 - "ModelUnavailable"
Cohesion: 0.06
Nodes (70): The record of every advised or withheld answer (ADR 0016).  `advice_records` k, AdviceShape, One kind of advice question, and everything its calculator needs to answer it., AdviceLog, AdviceRecord, Adviser, Calculation, ConsentBook (+62 more)

### Community 40 - "routes.py"
Cohesion: 0.09
Nodes (26): AdviceConsent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, ConsentRequiredEvent, DeclinedEvent, ErrorEvent, Evidence gathered and good enough to answer from. Nothing has been claimed yet. (+18 more)

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
Cohesion: 0.24
Nodes (5): Ollama, OllamaUnavailable, RuntimeError, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.  Ta, Batch embeddings. Falls back to the legacy endpoint on old servers.

### Community 52 - "0011-the-household-is-people-and-aliases-and-the-owner-is-one-of-them.md"
Cohesion: 0.17
Nodes (10): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, `docs/report/` — the final report, Ownership, Source documents written for the report, The rule that keeps it honest (+2 more)

### Community 53 - "extract.py"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 54 - "__init__.py"
Cohesion: 0.15
Nodes (26): AlertConfig, Alert, cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject() (+18 more)

### Community 55 - "ingest.py"
Cohesion: 0.24
Nodes (13): Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks.  Paperwork is short and stru, _split_page(), discover(), guess_date(), guess_type() (+5 more)

### Community 56 - "_household_scope"
Cohesion: 0.09
Nodes (36): _household_scope(), MonkeyPatch, Person, `HouseholdScope` over a roster held in memory, with every document resolved by n, The roster has no grandparent relation, so the household says it the only way it, 13 September: "what is Marcus's premium?" has no "my", so nothing was scoped and, A model proposal is a question on Today, not a member yet — the same rule relati, Nothing named, nothing ruled out: the question is the owner's, same as `apply` w (+28 more)

### Community 57 - "__init__.py"
Cohesion: 0.09
Nodes (65): RuleInput, Figure, One number a calculator produced, and the words a sentence must use to state it., _ambiguous(), _amount(), _band(), _band_label(), Basis (+57 more)

### Community 58 - "cli.py"
Cohesion: 0.18
Nodes (19): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+11 more)

### Community 59 - "settings"
Cohesion: 0.14
Nodes (32): client_for(), consent(), ConsentConn, The point of the endpoint. An UPDATE alone loses the example we are trying to co, The parameters of the one statement containing `needle`. Fails loudly if it neve, A client whose database is `conn`.      `base_url` is loopback because `TrustedH, `core.advice_consent`'s real SQL, against a household with or without an owner., Withdrawal never checks whether the wording shown was current -- taking consent (+24 more)

### Community 60 - "State"
Cohesion: 0.05
Nodes (38): Abstained, _pack_for(), The pack that speaks for the best-scoring passage's document type, or None for t, Passage, How a passage names itself: the document and the page, as a person would say it., Unique across kinds: chunk ids, fact ids and guidance ids are three sequences., HouseholdScope, What `AnswerGraph` is handed so it can scope without holding a connection. (+30 more)

### Community 61 - "test_pages.py"
Cohesion: 0.10
Nodes (34): page_count(), PageUnavailable, _pdfium(), Any, LookupError, RuntimeError, One page of one document, as an image.  Two callers want the same thing for op, Safe to show a person: there is no such page, or this file cannot be drawn. (+26 more)

### Community 62 - "FakeOllama"
Cohesion: 0.13
Nodes (28): extract(), Never raises. A failure is a reason, and a reason routes the document to quarant, FakeOllama, _page_of_examples(), Any, Exception, Answers whatever the test told it to, and records what it was asked., One page printing every field's `example`, so each value is attributable to a pa (+20 more)

### Community 63 - "bench_runtime.py"
Cohesion: 0.08
Nodes (34): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+26 more)

### Community 64 - "compilerOptions"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 65 - "parse.py"
Cohesion: 0.09
Nodes (22): Block, DoclingParser, _kind(), _pages_from(), Parser, PlainTextParser, Protocol, Turn captured bytes into pages of text, or say why it could not be done.  Ever (+14 more)

### Community 66 - "test_startup.py"
Cohesion: 0.13
Nodes (19): prepare_checkout(), Path, Startup tests do not ingest documents or need the corpus: they check process bou, npm is a wrapper around node. Killing only the wrapper orphans the port., The worker starts its nightly schedule as a process of its own. Terminating only, Stopping it signals its process group. Without a session of its own that group i, A developer's own `npm run dev` is used rather than fought for the port., `npm run dev` against an empty web/ fails slowly and cryptically. Say so instead (+11 more)

### Community 67 - "pipeline.py"
Cohesion: 0.15
Nodes (18): Chunk, Chunk, What is actually embedded: the prefix plus the text, matching the tsvector colum, Extraction, ParsedDocument, commit_both_lanes(), document_title(), Outcome (+10 more)

### Community 68 - "registry.py"
Cohesion: 0.10
Nodes (35): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders somewhe, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, RuntimeError, Load the installed capability modules at runtime.  The mirror of `core/packs.p (+27 more)

### Community 69 - "Ollama"
Cohesion: 0.11
Nodes (30): blocked_reasons(), forget(), page_images(), Any, Ollama, Path, ValueError, QuarantinedDocument (+22 more)

### Community 70 - "test_advice_module.py"
Cohesion: 0.13
Nodes (55): Missing, What a calculator returns when a fact or a rule value it needed was not there to, One person's advice. The graph asks whose first when a question names several pe, assert_nothing_negative(), basis(), fact(), _facts_tuple(), figures_of() (+47 more)

### Community 71 - "test_grounding_index.py"
Cohesion: 0.09
Nodes (33): CaptureFixture, PendingValue, One value waiting for a person to sign off, with what they need to see to do it., _Connected, _extracted(), FakeConn, FakeCursor, _installed() (+25 more)

### Community 72 - "preview.tsx"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 73 - "api.ts"
Cohesion: 0.10
Nodes (22): Load, STATUS, ADR-0016, RowSkeleton(), AdviceConsent, AdviceFigure, AskResponse, Claim (+14 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (17): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+9 more)

### Community 75 - "Any"
Cohesion: 0.14
Nodes (22): Measurement, by_subject(), db(), FakeCursor, load_register(), Any, date, Reminder and Alert: what fires, once, and with what behind it.  Both modules are (+14 more)

### Community 76 - "DenseRetriever"
Cohesion: 0.29
Nodes (4): DenseRetriever, NoReranker, A dense-only retriever, so the graph can be run and tested before Lane B's hybri, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this with

### Community 77 - "Notion"
Cohesion: 0.29
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "test_answer_graph.py"
Cohesion: 0.11
Nodes (56): AnswerGraph, Finished, "On file for Marcus Lim: MERIDIAN ASSURANCE, Private Car Insurance Policy (polic, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed y, One sentence that has passed the gate, with the citations it passed on.      It, Everything that is only knowable once the last sentence is in.      `quarantined, Built once, asked many times. Holds no connection: retrieval does., The documents on file, narrowed to the same people the passages were. (+48 more)

### Community 79 - "The demonstration run sheet"
Cohesion: 0.14
Nodes (14): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+6 more)

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (7): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Contributing"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 82 - "route.ts"
Cohesion: 0.43
Nodes (7): ALLOWED, Context, DELETE(), forward(), GET(), PATCH(), POST()

### Community 83 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 84 - "Passage"
Cohesion: 0.15
Nodes (28): build(), Any, Construct the Celery application. Imported lazily by callers so that nothing whi, application(), ingest(), Any, date, Ollama (+20 more)

### Community 85 - "page.tsx"
Cohesion: 0.17
Nodes (11): metadata, AdviceConsentSection(), OwnerForm(), RELATION_CHOICES, Roster(), Place, PLACES, WhoIsThis() (+3 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "pack"
Cohesion: 0.08
Nodes (44): Conn, Categories, Category, A kind of document a household holds, recognised by words printed in its name., HouseholdInventory, Handed to `AnswerGraph` by whoever holds a connection, as `HouseholdScope` is., Asked, categories_asked() (+36 more)

### Community 89 - "power-menu.tsx"
Cohesion: 0.19
Nodes (10): Action, CONFIRM, ITEMS, Stage, DependencyCheck, Phase, RestartingScreen(), ShutDownScreen() (+2 more)

### Community 90 - "lock.ts"
Cohesion: 0.18
Nodes (20): GET(), grant(), POST(), UnlockPage(), Accepted, clearFailures(), derive(), failures (+12 more)

### Community 91 - "Settings"
Cohesion: 0.14
Nodes (21): The local API. Liveness is intentionally separate from assistant readiness.  L, AsyncClient, capture_check(), Check, collect_checks(), database_check(), interface_check(), model_check() (+13 more)

### Community 92 - "build.py"
Cohesion: 0.12
Nodes (25): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering (, Why the catalogue cannot supply `field` from every one of `doc_types`, or None., Whether any document type in the catalogue declares `field`., Every core document type, field and category this pack names exists, or ValueErr, A compared field no document type of the shape declares can never be printed., _class_name(), _docstring() (+17 more)

### Community 93 - "InstalledPack"
Cohesion: 0.05
Nodes (37): Claim, _advice_basis(), _asked(), _citations(), _conversation(), _either(), fuse(), _max_sentences() (+29 more)

### Community 94 - "Registration"
Cohesion: 0.07
Nodes (40): FolderSettings, Dispatcher, Inline, Protocol, What happens to a document between "these bytes are registered" and "this docume, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided. (+32 more)

### Community 102 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "rows_for"
Cohesion: 0.15
Nodes (16): parse(), The one call the pipeline makes. An unhandled mime type quarantines rather than, indexed(), IndexedDocument, Any, RuntimeError, Rebuild a document's chunks and vectors without reading it again for facts.  Chu, Safe to show: names what went wrong, never what the document says. (+8 more)

### Community 104 - "_Answering"
Cohesion: 0.09
Nodes (50): AbstentionEvent, AdviceConsent, AskResponse, CloseRequest, ConfirmNameRequest, ConsentRequest, CorrectionRequest, CorrectionResponse (+42 more)

### Community 105 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 106 - "test_telegram_capture.py"
Cohesion: 0.10
Nodes (36): TelegramSettings, MockTransport, build(), FakeRegistrar, FakeTelegram, photo_update(), Any, Path (+28 more)

### Community 107 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 108 - "page.tsx"
Cohesion: 0.10
Nodes (23): _chat_ids(), ConfigurationError, _flag(), _folder(), local_url(), _port(), _positive(), Path (+15 more)

### Community 109 - ".load"
Cohesion: 0.11
Nodes (34): create_app(), ModelWarmth, Ollama, The page a person sees while Parrot starts, served by the engine itself.  **Wh, Whether the generator has been loaded yet, and where it landed. Written by one t, Load the generator and the embedder before the first question, and record the ou, The whole page. `screens_url` is escaped into a data attribute, never into scrip, render() (+26 more)

### Community 110 - "PackUnavailable"
Cohesion: 0.17
Nodes (16): _advised(), _checked(), Only income is made annual, so only income may say how often its printed figure, `annual_premium` is printed on no policy schedule; the market's sources publish, Two household documents can only be compared on what a household document prints, ADR 0017: `FactInput.pack` is gone; a payslip's gross salary is a core fact., Validated as a manifest, then against the core catalogue, as `core.packs` loads, The insurance pack plus one rule key, a critical illness gap and a hospital plan (+8 more)

### Community 111 - "dependencies"
Cohesion: 0.12
Nodes (17): ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes, tailwind-merge (+9 more)

### Community 112 - "Claim"
Cohesion: 0.14
Nodes (28): check_advice(), Claim, Why an advice explanation cannot be kept, or `None`. Asked of a claim built over, test_a_claim_citing_the_same_document_twice_says_it_once(), test_a_grounded_claim_renders_its_document_and_page(), What the gate checks beyond "is there a citation".  A cited sentence can still, `target` and `gap` both print SGD 500,000.00 (`_gap` with `held` at zero). Namin, The defect this fixes: naming `gap`, the *second* figure in `figures` order to p (+20 more)

### Community 113 - "test_grounding_values.py"
Cohesion: 0.10
Nodes (53): extract_values(), ExtractedValue, Ollama, Every value the source prints for these keys, kept only when its passage prints, LogCaptureFixture, _dropped(), _log_values(), _long_text() (+45 more)

### Community 114 - "household.py"
Cohesion: 0.10
Nodes (36): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+28 more)

### Community 115 - "SourceText"
Cohesion: 0.12
Nodes (34): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError, Read and validate a pack's grounding corpus from its own folder on disk.  A pa, A pack's grounding corpus on disk does not match what its `sources.yaml` records (+26 more)

### Community 116 - "TelegramAdapter"
Cohesion: 0.11
Nodes (24): BaseTransport, IngestJob, What a capture returns: a registered document, and whether we had seen it before, _attachment(), _pixels(), Any, Client, datetime (+16 more)

### Community 117 - "HouseholdInventory"
Cohesion: 0.13
Nodes (22): digest_of_document(), Any, enabled_pack_ids(), enabled_packs(), The packs left switched on, plus `core`, or `None` when nothing has been install, The installed packs a person has left switched on, as loaded pack objects., connect(), DatabaseUnavailable (+14 more)

### Community 118 - "test_lifecycle.py"
Cohesion: 0.12
Nodes (28): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor., What the person asked for, once. The first request wins; later ones change nothi, _client(), _eventually(), _launcher(), MonkeyPatch, Path (+20 more)

### Community 120 - "layout.tsx"
Cohesion: 0.25
Nodes (6): figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 121 - "Answer"
Cohesion: 0.12
Nodes (15): metadata, Abstention(), Part, sentence(), textOf(), ADR-0011, ADR-0016, Turn() (+7 more)

### Community 122 - "test_contracts.py"
Cohesion: 0.15
Nodes (27): _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact(), _field_not_on_every_doc_type(), _held_per_month() (+19 more)

### Community 123 - "SentenceScanner"
Cohesion: 0.10
Nodes (28): Any, Pulling finished sentences out of a JSON reply that is still being written.  T, What document would have answered this, if the model said. Read once, at the end, Feed it deltas; it returns whichever sentences became complete because of them., Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes on, Find `"sentences": [` once. Everything before it is of no interest.          S, SentenceScanner (+20 more)

### Community 124 - "__init__.py"
Cohesion: 0.09
Nodes (27): already_said(), close(), current_lead(), Due, next_window(), Overdue, Any, date (+19 more)

### Community 125 - "Household canon"
Cohesion: 0.05
Nodes (40): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, Policies, The family tree, and why three of them are not called Lim (+32 more)

### Community 126 - "route.ts"
Cohesion: 0.33
Nodes (9): lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns(), readEvents(), ADR-0016, upstreamDetail() (+1 more)

### Community 127 - "page.tsx"
Cohesion: 0.11
Nodes (10): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+2 more)

### Community 128 - "FolderAdapter"
Cohesion: 0.24
Nodes (20): FolderAdapter, Satisfies `CaptureAdapter`. Holds no database handle — it is given a `Registrar`, FakeRegistrar, datetime, Path, The watched folder: debounce, mime sniffing, and what happens the second time., Poll until the stability window has passed and something comes out., The `documents` table, reduced to the one thing it guarantees: sha256 is unique. (+12 more)

### Community 129 - "ScriptedClient"
Cohesion: 0.10
Nodes (14): ADR-0017, metadata, PacksPage(), metadata, Toggle(), EmptyState(), ProblemState(), SHAPES (+6 more)

### Community 130 - "Any"
Cohesion: 0.12
Nodes (22): names_for(), date, Each person's display name and confirmed aliases, trimmed and lower-cased the wa, A key's usable published values. How old a value may be depends on what it is: a, values_for(), advised_pack(), db(), _document() (+14 more)

### Community 131 - "_answer_events"
Cohesion: 0.10
Nodes (22): AskRequest, PersonModel, VaultFact, _as_module_summary(), _as_pack_summary(), _as_person(), _as_vault_document(), connection() (+14 more)

### Community 132 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 133 - "scope.py"
Cohesion: 0.16
Nodes (21): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Any (+13 more)

### Community 134 - "document-detail.tsx"
Cohesion: 0.20
Nodes (12): DocumentPage(), metadata, DocumentDetail(), when(), Field(), format(), isNumeric(), CorrectionResponse (+4 more)

### Community 136 - "item-row.tsx"
Cohesion: 0.16
Nodes (14): SourceChip(), SourcePanel(), stripTrailingPage(), ADR-0016, countdown(), detail(), figure(), ItemRow() (+6 more)

### Community 137 - "values.py"
Cohesion: 0.09
Nodes (33): A rule or table value a pack's sources publish.      Extracted automatically, ap, ValueKey, _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), number_tokens() (+25 more)

### Community 138 - "test_api.py"
Cohesion: 0.07
Nodes (45): HouseholdConsents, `core.graph.advice.ConsentBook` over a live connection, for the graph to ask wit, advising(), client(), FakeGraph, graph(), _padded(), MonkeyPatch (+37 more)

### Community 139 - "ModuleAdviser"
Cohesion: 0.17
Nodes (16): FactInput, A printed fact a calculator reads, named by where it is printed rather than what, _fact(), fact_row(), FactRow, facts_for(), _is_an_adviser(), ModuleAdviser (+8 more)

### Community 140 - "test_advice_core.py"
Cohesion: 0.14
Nodes (13): Magic bytes first, filename suffix second, `application/octet-stream` last., sniff_mime(), _Pending, datetime, Path, The watched-folder capture adapter.  A person drops a scan into a folder and i, Every file in the watched folder that is worth looking at at all., Advance the debounce by `elapsed` seconds and return the files now ready. (+5 more)

### Community 141 - "FakeConn"
Cohesion: 0.13
Nodes (23): a_citation(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive together,, No `reading` before it: the floor is checked before the model is asked anything., By then the 200 has been sent. An exception that only logged would leave a scree, A line about a document on file is not the answer to "does it cover floods?"., Advice changed how a stream ends, not what an explain answer sends. Nothing on t (+15 more)

### Community 142 - "PackManifest"
Cohesion: 0.18
Nodes (13): PackManifest, A domain pack, authored as one YAML file: grounding, persona, answering and advi, An advice shape that names a missing role or key fails at load time.          Ca, _insurance(), The manifest alone cannot know the catalogue, so it validates; `check_against` n, ADR 0017: documents are the core's. A pack.yaml carrying them does not load., test_a_grounding_corpus_is_named_by_id_not_by_path(), test_a_pack_cannot_opt_out_of_never_acts() (+5 more)

### Community 143 - "layout.tsx"
Cohesion: 0.25
Nodes (7): LockButton(), SURFACES, TabBar(), Tabs(), PowerMenu(), CHOICES, ThemeToggle()

### Community 144 - "devDependencies"
Cohesion: 0.06
Nodes (30): eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node, @types/react (+22 more)

### Community 145 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents

### Community 146 - "review_grounding_values.py"
Cohesion: 0.23
Nodes (13): approve(), pending(), Any, date, A person's approval, standing between a model's extraction and any calculator th, Reject these ids with a note, ignoring any that are no longer `pending`., Every value still waiting for review, oldest first, optionally for one pack., Approve these ids, ignoring any that are no longer `pending`. Returns the count (+5 more)

### Community 147 - "Domain packs — start here"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 149 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 150 - "schedule.py"
Cohesion: 0.33
Nodes (8): beat_schedule(), cron_expressions(), crontab_from(), manifest(), Any, When the nightly sweeps run, read from the modules' own manifests.  A module a, A five-field cron expression as Celery understands it., The cron line for each swept module, by module id. Testable without Celery insta

### Community 151 - "test_ingest_pipeline.py"
Cohesion: 0.14
Nodes (24): chunk_pages(), One flat list of chunks, ordinal running across the whole document., classification_sample(), The text the classifier reads: the opening pages, labelled, within a fixed budge, find_page(), The first page whose text contains this value. None means no page supports it., ParsedPage, insurance() (+16 more)

### Community 152 - "Any"
Cohesion: 0.11
Nodes (15): document_row(), fact_row(), Any, date, ADR 0017: disabling insurance_agent switches off its voice, never a household's, Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with ev, A deleted document must not take the sentence down with it., Following a citation must never end in a blank screen because a pack was switche (+7 more)

### Community 153 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "README.md"
Cohesion: 0.33
Nodes (3): Architecture decision records, Index, Writing one

### Community 155 - "obligation"
Cohesion: 0.09
Nodes (38): conn(), FakeConn, obligation(), open_obligation(), overdue_row(), pack_row(), Snooze means 'not until this gets more urgent', so it can name the day it does., No new column: `already_said` is what makes the row quiet, and it reads this one (+30 more)

### Community 157 - "_today_items"
Cohesion: 0.14
Nodes (18): Claim, A document and a page, as a person would cite it — or, for published guidance, w, One sentence and the passages it was traced to. Never emitted without `citations, Source, TodayItem, _as_response(), _as_source(), _cite() (+10 more)

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

### Community 163 - "walk"
Cohesion: 0.30
Nodes (15): collectProps(), compileAttr(), cssToObj(), hostPositionStyle(), isDeckMountTag(), kebabToCamel(), renderDeckKids(), walk() (+7 more)

### Community 164 - "obligations.py"
Cohesion: 0.48
Nodes (6): answer(), build_context(), format_sources(), Ollama, Answer a question from retrieved chunks, with citations back to the file.  The, Hit

### Community 165 - "gate.py"
Cohesion: 0.33
Nodes (6): findTopLevelEquality(), parensWrapWhole(), resolve(), resolvePath(), walkText(), warnUnresolved()

### Community 166 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 167 - "application"
Cohesion: 0.22
Nodes (14): install_best_effort(), Install at startup without being able to stop startup.      Both processes that, _beat_needs_its_own_process(), celery_argv(), main(), Any, Namespace, Popen (+6 more)

### Community 168 - "check_content"
Cohesion: 0.23
Nodes (15): FakeConn, _no_owner(), _owned(), A recording fake in the house style (see `tests/test_grounding_index.py`'s `Fake, Script the owner household.owner reads: one person, `is_owner`., test_a_withdrawal_after_a_grant_gives_none(), test_an_older_version_gives_status_outdated(), test_current_is_none_when_the_latest_grant_is_a_different_version() (+7 more)

### Community 169 - "classify.py"
Cohesion: 0.15
Nodes (17): DocumentTypeSpec, One kind of document the core recognises., Classification, classify(), _prompt(), Ollama, Decide which of the core catalogue's document types a captured document is, or d, Never raises. An unavailable model is a classification failure, so it quarantine (+9 more)

### Community 170 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 171 - "igd-capstone-2026"
Cohesion: 0.20
Nodes (10): Authoring a pack, igd-capstone-2026, `main` is not protected, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live (+2 more)

### Community 172 - "FakeCursor"
Cohesion: 0.13
Nodes (13): Adviser, Ollama, The answer graph.  Router, retrieve, rerank, grounding gate, then answer or ab, holdings(), Any, The documents on file, read from `facts` rather than searched for.  "Do I have c, Rows of `INVENTORY`, one holding per document that prints the field an enabled p, Protocol (+5 more)

### Community 173 - "boot"
Cohesion: 0.25
Nodes (9): boot(), createStreamTracker(), getReactDOM(), init(), parseDataProps(), parseDcDocument(), parseDcText(), react-dom (+1 more)

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

### Community 178 - "0001_init.sql"
Cohesion: 0.36
Nodes (7): chunks, documents, facts, modules, obligations, packs, traces

### Community 179 - "createRuntime"
Cohesion: 0.29
Nodes (8): createExternalModules(), createHelmetManager(), createPseudoSheet(), createRuntime(), importantify(), Placeholder(), scanUnquotedUrl(), stripComments()

### Community 180 - "start_parrot.py"
Cohesion: 0.32
Nodes (7): main(), Path, Local-only startup preflight, using the standard library so setup can be diagnos, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file conte, report_hardware(), startup_gaps()

### Community 181 - "FactRow"
Cohesion: 0.40
Nodes (5): createComponentFactory(), evalDcLogic(), getReact(), react, react

### Community 182 - "advice_consent.py"
Cohesion: 0.21
Nodes (16): Channel, current(), grant(), _latest(), NoOwner, Any, RuntimeError, The owner's consent to a pack's advice, append-only (ADR 0016).  Consent is th (+8 more)

### Community 183 - "corrections.py"
Cohesion: 0.07
Nodes (38): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+30 more)

### Community 184 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

### Community 185 - ".json"
Cohesion: 0.16
Nodes (12): ModelUnavailable, Any, Client, RuntimeError, Load the generator and the embedder now, and say where the generator landed., Generate against a JSON schema. This is how extraction is held to a pack's field, The same constrained generation, yielded as it is written.          Identical, Safe to show: names what could not be done, never the document it was doing it t (+4 more)

### Community 186 - "contracts.py"
Cohesion: 0.09
Nodes (29): Advice, Answering, FieldSpec, Grounding, GroundingDocument, Guardrails, ModuleTrigger, Persona (+21 more)

### Community 187 - "14 · A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.33
Nodes (6): 14 · A pack supplies what the core knows about a domain, and the core stays generic, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 188 - "16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.33
Nodes (6): 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 190 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 191 - "gate.py"
Cohesion: 0.14
Nodes (15): Exclusions, A sentence claiming cover whose every citation sits under one of `headings` is d, check(), check_one(), The grounding gate.  Rule 3 in AGENTS.md: no claim without a citation. This mo, Never raises, never rewrites a claim. It keeps, drops, or abstains.      The w, Why this one sentence cannot be kept, or `None` if it can.      Depends on not, _says() (+7 more)

### Community 192 - "0002_household.sql"
Cohesion: 0.70
Nodes (4): document_attribution, people, person_aliases, telegram_identities

### Community 193 - "0003_advice.sql"
Cohesion: 0.60
Nodes (4): advice_consents, advice_records, grounding_sources, grounding_values

### Community 194 - "test_a_client_that_leaves_after_the_card_commits_one_record"
Cohesion: 0.24
Nodes (10): next_kind(), The kind of the next event on the wire., Starlette never closes a body iterator a disconnected client stopped pulling. `_, The ruling's case as it happens on a socket: Starlette sends the card and at onc, What the API owns when a stream is closed with the graph still parked on the car, The graph's own cleanup can fail -- for example the record insert raises -- and, test_a_client_that_leaves_after_the_card_commits_one_record(), test_a_client_that_leaves_mid_explanation_still_commits_what_it_was_shown() (+2 more)

### Community 195 - "test_a_document_still_in_the_inbox_is_not_forgotten"
Cohesion: 0.18
Nodes (11): filed_document(), inbox(), Path, Capture would register it again within a minute, so the button would only appear, A watched folder holding one document, hashed the way the ingest registered it., v1 keeps the inbox as the document store, so this is a real state, not a fault., test_a_document_still_in_the_inbox_is_not_forgotten(), test_a_document_whose_file_left_the_inbox_is_409_not_500() (+3 more)

### Community 196 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 197 - "Registration"
Cohesion: 0.20
Nodes (4): An already-indexed document is not read again. Re-reading it would burn a minute, The row as it now stands, plus whether this call is the one that created it., Registration, Outcome

### Community 198 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 199 - "test_advice_core.py"
Cohesion: 0.36
Nodes (10): check_content(), Why a cited sentence still cannot be kept, or `None`. Asked after `check_one` pa, _calculation(), The types a calculator hands back, the owner's consent, and the record of an adv, test_check_content_keeps_a_sentence_stating_a_facts_value(), test_check_content_keeps_a_sentence_stating_a_figure(), test_check_content_keeps_a_sentence_stating_a_rules_value(), test_check_content_still_drops_a_sentence_stating_an_unprinted_number() (+2 more)

### Community 200 - "ScriptedOllama"
Cohesion: 0.09
Nodes (46): AdviceCard, answer_system(), The pack's voice first, the core's rules last: a persona cannot loosen what foll, A worked result, every word of it written by code, given before the model says a, Whose situation a piece of advice is about — `whose`'s answer, with no passages, Subject, advised_pack(), build() (+38 more)

### Community 204 - "FakeCursor"
Cohesion: 0.24
Nodes (3): FakeCursor, Any, FakeConn

### Community 205 - "chunk.py"
Cohesion: 0.31
Nodes (8): _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own st, The page as `(is_heading, line)`, from the parser's structure when it has any., A line, in pieces no longer than the target, broken at sentences and then at spa, `(heading, text)` for each chunk on one page, and the heading still open at its

### Community 206 - "The household, and the word "my""
Cohesion: 0.22
Nodes (9): 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model, 5 · Resolving "my" — three buckets, not two, 6 · Two safeguards, 7 · What this cost, and what it did not, 8 · What it enables, for §5 and §8 (+1 more)

### Community 207 - "test_an_advice_card_carries_a_rules_publisher_on_the_wire"
Cohesion: 0.33
Nodes (7): advice_card(), A published value's chip: no document and no page, only who published it and whe, A published number has no page to open. What makes it checkable is who published, Nothing shown, nothing recorded. Once advice is on the screen, a failure after i, rule_citation(), test_an_advice_card_carries_a_rules_publisher_on_the_wire(), test_an_answer_that_fails_before_any_advice_is_rolled_back_and_after_it_is_kept()

### Community 210 - "is_first_person"
Cohesion: 0.33
Nodes (6): is_first_person(), Whether this question is about the person asking.      `other_names` are the d, "What is Rachel's premium on my policy" is a question about Rachel.      A rel, test_a_named_household_member_wins_over_the_pronoun(), test_first_person_questions_are_recognised(), test_questions_about_other_people_are_not_scoped()

### Community 211 - "installed_packs"
Cohesion: 0.19
Nodes (12): Catalog, installed_packs(), _load_one(), PackUnavailable, Path, RuntimeError, Load the core document catalogue and the installed packs at runtime.  The core o, A pack names what the catalogue does not declare, or the pack does not exist. (+4 more)

### Community 212 - "find_browser_executable"
Cohesion: 0.47
Nodes (5): find_browser_executable(), generate_documents(), Path, Project Parrot - Synthetic Document Generator for Lim Household ===============, Find Microsoft Edge or Google Chrome executable on Windows.

### Community 213 - "ClosingSpy"
Cohesion: 0.25
Nodes (4): ClosingSpy, C5 fix round 2 closed the gap this test used to mark: `AdviceCard` is now yielde, Wraps an event generator to record whether something called `.close()` on it, as, test_a_graph_stream_closed_exactly_at_the_card_still_records_it()

### Community 214 - "HouseholdAdviceLog"
Cohesion: 0.29
Nodes (7): _normal(), "1,860.00", "1860" and "01" → "1860", "1860", "1": formatting is not a different, Every number or identifier in a sentence that no cited passage prints. An identi, unprinted_numbers(), test_a_date_on_file_may_be_written_the_way_a_person_says_it(), test_a_leading_zero_does_not_make_a_printed_date_unprinted(), test_a_policy_number_is_kept_only_when_it_is_printed_whole()

### Community 215 - "_Value"
Cohesion: 0.33
Nodes (6): _Value, Hashable, _order_key(), _ordered(), One sortable key for a number, a date or a word, so a ranking never compares acr, Keys ranked by value in the stated order, ties broken by name so a ranking is re

### Community 216 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 217 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 218 - "12. Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.33
Nodes (5): 12. Chunks follow the document's headings, and embeddings use the model's task prompts, Consequences, Context, Decision, Evidence

### Community 219 - "page.tsx"
Cohesion: 0.38
Nodes (4): metadata, UnlockForm(), Wordmark(), WordmarkLockup()

### Community 220 - "17 · A pack is grounding and persona; the core owns documents"
Cohesion: 0.33
Nodes (6): 17 · A pack is grounding and persona; the core owns documents, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 221 - "5. The watched folder is polled for stability, not subscribed to for events"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 222 - "1. Record architecture decisions"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 223 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 224 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

### Community 225 - "15. A name scopes a question, and a grandparent is not a parent"
Cohesion: 0.50
Nodes (4): 15. A name scopes a question, and a grandparent is not a parent, Consequences, Context, Decision

### Community 226 - "test_a_grounding_corpus_travels_inside_its_pack"
Cohesion: 0.50
Nodes (4): Path, A downloaded pack carries its sources, so no corpus is left at the repository ro, test_a_grounding_corpus_travels_inside_its_pack(), test_every_grounding_corpus_declares_its_provenance()

## Knowledge Gaps
- **623 isolated node(s):** `npx`, `@modelcontextprotocol/server-filesystem`, `packs`, `modules`, `traces` (+618 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `run_parrot.py`, `Any`, `_answer_events`, `IngestJob`, `test_api.py`, `FakeConn`, `review_grounding_values.py`, `test_household.py`, `obligation`, `test_modules.py`, `application`, `ModelUnavailable`, `.json`, `settings`, `bench_runtime.py`, `test_startup.py`, `registry.py`, `Ollama`, `test_advice_module.py`, `Any`, `test_answer_graph.py`, `Passage`, `ClosingSpy`, `Registration`, `_Answering`, `test_telegram_capture.py`, `page.tsx`, `.load`, `HouseholdInventory`, `test_lifecycle.py`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `InstalledPack` connect `ModelUnavailable` to `Any`, `_answer_events`, `test_api.py`, `ModuleAdviser`, `FakeConn`, `PackManifest`, `obligation`, `routes.py`, `classify.py`, `FakeCursor`, `__init__.py`, `settings`, `State`, `registry.py`, `test_advice_module.py`, `test_grounding_index.py`, `ScriptedOllama`, `test_answer_graph.py`, `installed_packs`, `ClosingSpy`, `pack`, `build.py`, `InstalledPack`, `_Answering`, `SourceText`, `HouseholdInventory`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `ModelUnavailable` connect `.json` to `extract.py`, `test_ingest_pipeline.py`, `ModelUnavailable`, `classify.py`, `contracts.py`, `State`, `FakeOllama`, `pipeline.py`, `Ollama`, `test_grounding_index.py`, `ScriptedOllama`, `test_answer_graph.py`, `_Value`, `Settings`, `InstalledPack`, `Registration`, `rows_for`, `.load`, `test_grounding_values.py`, `household.py`, `HouseholdInventory`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 64 inferred relationships involving `InstalledPack` (e.g. with `_Answering` and `AdviceLog`) actually correct?**
  _`InstalledPack` has 64 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `ScriptedOllama` (e.g. with `Adviser` and `Consents`) actually correct?**
  _`ScriptedOllama` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 38 inferred relationships involving `Passage` (e.g. with `AdviceLog` and `AdviceRecord`) actually correct?**
  _`Passage` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `FakeConn` (e.g. with `HouseholdConsents` and `HouseholdAdviceLog`) actually correct?**
  _`FakeConn` has 19 INFERRED edges - model-reasoned connections that need verification._