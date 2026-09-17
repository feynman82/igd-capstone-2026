# Graph Report - igd-wt-agent  (2026-09-17)

## Corpus Check
- 287 files · ~677,669 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3947 nodes · 9694 edges · 232 communities (210 shown, 22 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 1210 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `826dccb6`
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
- 5. The watched folder is polled for stability, not subscribed to for events
- NoReranker
- queries.py

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

## Communities (232 total, 22 thin omitted)

### Community 0 - "run_parrot.py"
Cohesion: 0.12
Nodes (27): Ollama, Load the generator and the embedder before the first question, and record the ou, warm_models(), broker_available(), Whether Redis answers. Not whether a worker is listening — `core/runtime/checks., _kill_tree(), main(), parse_args() (+19 more)

### Community 1 - "page.tsx"
Cohesion: 0.13
Nodes (14): isUrgent(), metadata, summary(), TodayPage(), countdown(), detail(), figure(), ItemRow() (+6 more)

### Community 2 - "Christian — task list"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.10
Nodes (41): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+33 more)

### Community 4 - "isUnlocked"
Cohesion: 0.60
Nodes (5): ACTIONS, GET(), POST(), sameOrigin(), unlocked()

### Community 5 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 6 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 7 - "IngestJob"
Cohesion: 0.07
Nodes (37): CaptureAdapter, datetime, Protocol, The one interface every capture channel satisfies.      receive(payload, mime,, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256` i, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sha256(), Capture adapters.  Every channel a document can arrive through satisfies one i (+29 more)

### Community 8 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 9 - "support.js"
Cohesion: 0.10
Nodes (14): cdnScriptFor(), compileTemplate(), contentKey(), createPseudoSheet(), encodeCamelAttrs(), encodeCase(), evalDcLogic(), importantify() (+6 more)

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
Cohesion: 0.07
Nodes (37): Inline, Any, Queued, What happens to a document between "these bytes are registered" and "this docume, Run the pipeline here and now, and report what it decided., Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker.      Celery is imported here, Intake (+29 more)

### Community 18 - "test_household.py"
Cohesion: 0.13
Nodes (28): Keep the owner's passages and the household's; set aside everybody else's., scope_passages(), conn(), _conn_returning(), _passage(), Any, Who is asking, and whose documents may answer.  Two halves, deliberately split, The third bucket. Home contents, a utility bill — nobody's name on it, everybody (+20 more)

### Community 19 - "extract.py"
Cohesion: 0.14
Nodes (22): FieldSpec, One extractable field. Its `name` is the column header in Desmond's register and, _coerce(), _date_renderings(), decode_schema(), _drop_format(), _prepare(), printed_date() (+14 more)

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
Cohesion: 0.08
Nodes (27): Answer, _as_sentence(), Citation, Cited, _distinct(), _input_citation(), Every event, collected. `scripts/ask.py` and the screen ask the same question of, A passage, named the way a person cites it and identified the way a link needs. (+19 more)

### Community 40 - "routes.py"
Cohesion: 0.14
Nodes (21): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, ConsentRequiredEvent, DeclinedEvent, FinishedEvent, Evidence gathered and good enough to answer from. Nothing has been claimed yet. (+13 more)

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
Cohesion: 0.10
Nodes (19): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model (+11 more)

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
Cohesion: 0.08
Nodes (72): FactInput, A printed fact a calculator reads, named by where it is printed rather than what, RuleInput, Figure, One number a calculator produced, and the words a sentence must use to state it., Hashable, _ambiguous(), _amount() (+64 more)

### Community 58 - "cli.py"
Cohesion: 0.18
Nodes (19): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+11 more)

### Community 59 - "settings"
Cohesion: 0.14
Nodes (32): client_for(), consent(), ConsentConn, The point of the endpoint. An UPDATE alone loses the example we are trying to co, The parameters of the one statement containing `needle`. Fails loudly if it neve, A client whose database is `conn`.      `base_url` is loopback because `TrustedH, `core.advice_consent`'s real SQL, against a household with or without an owner., Withdrawal never checks whether the wording shown was current -- taking consent (+24 more)

### Community 60 - "State"
Cohesion: 0.08
Nodes (36): ModelUnavailable, RuntimeError, Safe to show: names what could not be done, never the document it was doing it t, build(), events(), passage(), Any, Exception (+28 more)

### Community 61 - "test_pages.py"
Cohesion: 0.09
Nodes (36): page_images(), Base64 page images, in page order. Empty when this document cannot be rendered., page_count(), PageUnavailable, _pdfium(), Any, LookupError, RuntimeError (+28 more)

### Community 62 - "FakeOllama"
Cohesion: 0.09
Nodes (47): extract(), find_page(), _normalise(), The first page whose text contains this value. None means no page supports it., Never raises. A failure is a reason, and a reason routes the document to quarant, FakeOllama, insurance(), iras() (+39 more)

### Community 63 - "bench_runtime.py"
Cohesion: 0.08
Nodes (34): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+26 more)

### Community 64 - "compilerOptions"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 65 - "parse.py"
Cohesion: 0.10
Nodes (21): Block, DoclingParser, _kind(), _pages_from(), Parser, PlainTextParser, Protocol, Turn captured bytes into pages of text, or say why it could not be done.  Ever (+13 more)

### Community 66 - "test_startup.py"
Cohesion: 0.13
Nodes (19): prepare_checkout(), Path, Startup tests do not ingest documents or need the corpus: they check process bou, npm is a wrapper around node. Killing only the wrapper orphans the port., The worker starts its nightly schedule as a process of its own. Terminating only, Stopping it signals its process group. Without a session of its own that group i, A developer's own `npm run dev` is used rather than fought for the port., `npm run dev` against an empty web/ fails slowly and cryptically. Say so instead (+11 more)

### Community 67 - "pipeline.py"
Cohesion: 0.11
Nodes (26): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering (, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why the catalogue cannot supply `field` from every one of `doc_types`, or None., Whether any document type in the catalogue declares `field`., Every core document type, field and category this pack names exists, or ValueErr, A compared field no document type of the shape declares can never be printed., _class_name() (+18 more)

### Community 68 - "registry.py"
Cohesion: 0.08
Nodes (42): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders somewhe, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, RuntimeError, Load the installed capability modules at runtime.  The mirror of `core/packs.p (+34 more)

### Community 69 - "Ollama"
Cohesion: 0.11
Nodes (30): blocked_reasons(), forget(), Any, Ollama, Path, ValueError, QuarantinedDocument, queue() (+22 more)

### Community 70 - "test_advice_module.py"
Cohesion: 0.12
Nodes (60): Calculation, Missing, passages_for(), Inputs as kind fact/rule passages (chunk_id from the ref), and the figures as on, What a calculator returns when every fact and rule it needed was on file and app, What a calculator returns when a fact or a rule value it needed was not there to, One person's advice. The graph asks whose first when a question names several pe, date (+52 more)

### Community 71 - "test_grounding_index.py"
Cohesion: 0.07
Nodes (46): CaptureFixture, approve(), pending(), PendingValue, Any, date, A person's approval, standing between a model's extraction and any calculator th, Reject these ids with a note, ignoring any that are no longer `pending`. (+38 more)

### Community 72 - "preview.tsx"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 73 - "api.ts"
Cohesion: 0.14
Nodes (19): Categories, Category, A kind of document a household holds, recognised by words printed in its name., holdings(), Any, The documents on file, read from `facts` rather than searched for.  "Do I have c, Rows of `INVENTORY`, one holding per document that prints the field an enabled p, Asked (+11 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (17): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+9 more)

### Community 75 - "Any"
Cohesion: 0.14
Nodes (22): Measurement, by_subject(), db(), FakeCursor, load_register(), Any, date, Reminder and Alert: what fires, once, and with what behind it.  Both modules are (+14 more)

### Community 76 - "DenseRetriever"
Cohesion: 0.13
Nodes (19): DocumentTypeSpec, One kind of document the core recognises., Classification, classify(), _prompt(), Ollama, Decide which of the core catalogue's document types a captured document is, or d, Never raises. An unavailable model is a classification failure, so it quarantine (+11 more)

### Community 77 - "Notion"
Cohesion: 0.29
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "test_answer_graph.py"
Cohesion: 0.12
Nodes (51): AnswerGraph, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed y, One sentence that has passed the gate, with the citations it passed on.      I, Built once, asked many times. Holds no connection: retrieval does., The documents on file, narrowed to the same people the passages were., Reading, Sentence, Holding (+43 more)

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
Cohesion: 0.13
Nodes (17): AdviceConsent, AdviceConsent, ErrorEvent, The stream broke after it began. A client cannot read an HTTP status by then., One advising pack, the wording a person is asked to agree to, and what the owner, _answer_events(), _as_consent(), connection() (+9 more)

### Community 85 - "page.tsx"
Cohesion: 0.19
Nodes (10): metadata, OwnerForm(), RELATION_CHOICES, Roster(), Place, PLACES, WhoIsThis(), PendingName (+2 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "pack"
Cohesion: 0.16
Nodes (21): categories_asked(), glossary(), _make_replacer(), mentions(), _pattern(), The catalogue's words and every enabled pack's, unioned; a pack's wording wins a, The question with each declared phrase replaced by what the documents print, lon, Only the lines the question used, so the prompt grows by what it needs and no mo (+13 more)

### Community 89 - "power-menu.tsx"
Cohesion: 0.18
Nodes (11): Action, CONFIRM, ITEMS, PowerMenu(), Stage, DependencyCheck, Phase, RestartingScreen() (+3 more)

### Community 90 - "lock.ts"
Cohesion: 0.17
Nodes (22): GET(), grant(), POST(), metadata, UnlockPage(), Accepted, clearFailures(), derive() (+14 more)

### Community 91 - "Settings"
Cohesion: 0.12
Nodes (25): The local API. Liveness is intentionally separate from assistant readiness.  L, AsyncClient, capture_check(), Check, collect_checks(), database_check(), interface_check(), model_check() (+17 more)

### Community 92 - "build.py"
Cohesion: 0.20
Nodes (21): ingest(), Any, date, Ollama, Path, The work the queue carries: read a document, retry quarantine, sweep the two mod, The second pass over exactly one document, which is what a person clicking Retry, One document, by id. The interface's Retry button lands here through the broker. (+13 more)

### Community 93 - "InstalledPack"
Cohesion: 0.04
Nodes (56): Claim, _advice_basis(), _advice_prompt(), _asked(), _citations(), _conversation(), _either(), fuse() (+48 more)

### Community 94 - "Registration"
Cohesion: 0.14
Nodes (15): Exclusions, A sentence claiming cover whose every citation sits under one of `headings` is d, check(), check_one(), The grounding gate.  Rule 3 in AGENTS.md: no claim without a citation. This mo, Never raises, never rewrites a claim. It keeps, drops, or abstains.      The w, Why this one sentence cannot be kept, or `None` if it can.      Depends on not, _says() (+7 more)

### Community 102 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "rows_for"
Cohesion: 0.08
Nodes (36): Chunk, Extraction, The ingestion worker.  Capture registers a document; this package turns it int, parse(), ParsedDocument, The one call the pipeline makes. An unhandled mime type quarantines rather than, commit_both_lanes(), document_title() (+28 more)

### Community 104 - "_Answering"
Cohesion: 0.09
Nodes (38): CloseRequest, ConfirmNameRequest, ConsentRequest, CorrectionRequest, CorrectionResponse, EnabledRequest, ForgottenDocument, HouseholdResponse (+30 more)

### Community 105 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 106 - "test_telegram_capture.py"
Cohesion: 0.12
Nodes (33): TelegramSettings, MockTransport, build(), FakeTelegram, photo_update(), Any, Path, Request (+25 more)

### Community 107 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 108 - "page.tsx"
Cohesion: 0.12
Nodes (22): _chat_ids(), ConfigurationError, _flag(), _folder(), local_url(), _port(), _positive(), Path (+14 more)

### Community 109 - ".load"
Cohesion: 0.16
Nodes (28): create_app(), ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one t, _ollama_answering(), Any, MonkeyPatch, Path, Setup diagnostics use controlled service responses, never live household documen (+20 more)

### Community 110 - "PackUnavailable"
Cohesion: 0.08
Nodes (45): PackManifest, A domain pack, authored as one YAML file: grounding, persona, answering and advi, An advice shape that names a missing role or key fails at load time.          Ca, _advised(), _checked(), _insurance(), _market(), _market_compares_an_undeclared_field() (+37 more)

### Community 111 - "dependencies"
Cohesion: 0.10
Nodes (20): ai, @ai-sdk/react, class-variance-authority, clsx, createComponentFactory(), lucide-react, next, next-themes (+12 more)

### Community 112 - "Claim"
Cohesion: 0.14
Nodes (29): check_advice(), Claim, Why an advice explanation cannot be kept, or `None`. Asked of a claim built over, test_a_claim_citing_the_same_document_twice_says_it_once(), test_a_grounded_claim_renders_its_document_and_page(), _advice_calculation(), What the gate checks beyond "is there a citation".  A cited sentence can still, `target` and `gap` both print SGD 500,000.00 (`_gap` with `held` at zero). Namin (+21 more)

### Community 113 - "test_grounding_values.py"
Cohesion: 0.06
Nodes (87): A rule or table value a pack's sources publish.      Extracted automatically, ap, ValueKey, SourceText, _check(), collapse(), _cuts_a_number(), extract_values(), ExtractedValue (+79 more)

### Community 114 - "household.py"
Cohesion: 0.10
Nodes (36): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+28 more)

### Community 115 - "SourceText"
Cohesion: 0.19
Nodes (23): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError, Read and validate a pack's grounding corpus from its own folder on disk.  A pa, A pack's grounding corpus on disk does not match what its `sources.yaml` records (+15 more)

### Community 116 - "TelegramAdapter"
Cohesion: 0.11
Nodes (23): BaseTransport, _attachment(), _pixels(), Any, Client, datetime, Response, RuntimeError (+15 more)

### Community 117 - "HouseholdInventory"
Cohesion: 0.26
Nodes (15): _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact(), _field_not_on_every_doc_type(), _held_per_month() (+7 more)

### Community 118 - "test_lifecycle.py"
Cohesion: 0.12
Nodes (28): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor., What the person asked for, once. The first request wins; later ones change nothi, _client(), _eventually(), _launcher(), MonkeyPatch, Path (+20 more)

### Community 120 - "layout.tsx"
Cohesion: 0.25
Nodes (6): figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 121 - "Answer"
Cohesion: 0.09
Nodes (24): lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns(), readEvents(), ADR-0016, upstreamDetail() (+16 more)

### Community 122 - "test_contracts.py"
Cohesion: 0.21
Nodes (11): Conn, HouseholdInventory, Handed to `AnswerGraph` by whoever holds a connection, as `HouseholdScope` is., UUID, Holdings come from `facts`, one per document that prints the name the categories, ADR 0017: a document is the core's, so the query includes `core` whatever is ena, row(), test_a_pack_that_declares_no_categories_holds_nothing() (+3 more)

### Community 123 - "SentenceScanner"
Cohesion: 0.10
Nodes (28): Any, Pulling finished sentences out of a JSON reply that is still being written.  T, What document would have answered this, if the model said. Read once, at the end, Feed it deltas; it returns whichever sentences became complete because of them., Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes on, Find `"sentences": [` once. Everything before it is of no interest.          S, SentenceScanner (+20 more)

### Community 124 - "__init__.py"
Cohesion: 0.09
Nodes (27): already_said(), close(), current_lead(), Due, next_window(), Overdue, Any, date (+19 more)

### Community 125 - "Household canon"
Cohesion: 0.04
Nodes (42): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, Policies, The family tree, and why three of them are not called Lim (+34 more)

### Community 126 - "route.ts"
Cohesion: 0.22
Nodes (11): ReminderConfig, ExtractedFact, fixed(), from_facts(), _label(), Any, date, Turn a dated fact into a commitment to do something about it.  A fact is a state (+3 more)

### Community 127 - "page.tsx"
Cohesion: 0.09
Nodes (12): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+4 more)

### Community 128 - "FolderAdapter"
Cohesion: 0.09
Nodes (40): IngestJob, Magic bytes first, filename suffix second, `application/octet-stream` last., What a capture returns: a registered document, and whether we had seen it before, sniff_mime(), FolderAdapter, FolderSettings, _Pending, datetime (+32 more)

### Community 129 - "ScriptedClient"
Cohesion: 0.05
Nodes (46): ADR-0017, metadata, PacksPage(), DocumentPage(), metadata, metadata, VaultPage(), AdviceConsentSection() (+38 more)

### Community 130 - "Any"
Cohesion: 0.14
Nodes (19): names_for(), Each person's display name and confirmed aliases, trimmed and lower-cased the wa, advised_pack(), db(), _document(), FakeConn, FakeCursor, Any (+11 more)

### Community 131 - "_answer_events"
Cohesion: 0.13
Nodes (18): AskRequest, ModuleSummary, PackSummary, PersonModel, VaultFact, _as_module_summary(), _as_pack_summary(), _as_person() (+10 more)

### Community 132 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 133 - "scope.py"
Cohesion: 0.15
Nodes (22): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Any (+14 more)

### Community 134 - "document-detail.tsx"
Cohesion: 0.15
Nodes (14): SourceChip(), SourcePanel(), stripTrailingPage(), ADR-0016, DocumentDetail(), when(), Field(), format() (+6 more)

### Community 136 - "item-row.tsx"
Cohesion: 0.15
Nodes (12): Basic Financial Planning Guide, Basic Financial Planning Guide, Basic Financial Planning Guide For Entrants To The Workforce, Basic Financial Planning Guide for those nearing retirement, Basic Financial Planning Guide For Those With Dependents, Emergency funds, For those approaching retirement, For those new to the workforce (+4 more)

### Community 137 - "values.py"
Cohesion: 0.18
Nodes (10): Common reasons why insurers do not provide a Letter of Guarantee in specific cases, Common reasons why insurers may reject or not pay for claims, Comparison of Integrated Shield Plans, Comparison of lifetime premiums, Important Information, Letter of Guarantee, List of Integrated Shield Plans (IPs) and their targeted level of coverage, Medical Record Costs (+2 more)

### Community 138 - "test_api.py"
Cohesion: 0.07
Nodes (45): HouseholdConsents, `core.graph.advice.ConsentBook` over a live connection, for the graph to ask wit, advising(), client(), FakeGraph, graph(), _padded(), MonkeyPatch (+37 more)

### Community 139 - "ModuleAdviser"
Cohesion: 0.15
Nodes (17): fact_row(), FactRow, facts_for(), _is_an_adviser(), ModuleAdviser, _newest(), product_names(), Adviser (+9 more)

### Community 140 - "test_advice_core.py"
Cohesion: 0.20
Nodes (9): Assistance under MediFund, Basic health insurance coverage, Choosing your level of coverage, How MediSave fits in, If you have company health insurance, If you want more coverage, Types of health insurance plans, Understanding health insurance (+1 more)

### Community 141 - "FakeConn"
Cohesion: 0.13
Nodes (23): a_citation(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive together,, No `reading` before it: the floor is checked before the model is asked anything., By then the 200 has been sent. An exception that only logged would leave a scree, A line about a document on file is not the answer to "does it cover floods?"., Advice changed how a stream ends, not what an explain answer sends. Nothing on t (+15 more)

### Community 142 - "PackManifest"
Cohesion: 0.29
Nodes (7): AskResponse, Claim, The whole answer, once. `text` is the consent wording when `kind` is `consent_re, One sentence and the passages it was traced to. Never emitted without `citations, _as_response(), One `Answer` to one of the shapes a client has to handle., AskResponse

### Community 143 - "layout.tsx"
Cohesion: 0.19
Nodes (10): HouseholdPage(), AppLayout(), LockButton(), SURFACES, TabBar(), Tabs(), UnlockForm(), Wordmark() (+2 more)

### Community 144 - "devDependencies"
Cohesion: 0.06
Nodes (30): eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node, @types/react (+22 more)

### Community 145 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents

### Community 146 - "review_grounding_values.py"
Cohesion: 0.25
Nodes (8): Finished, Everything that is only knowable once the last sentence is in.      `quarantin, Fix 2(a). The sentence names the gap figure with its own word ("gap") and cites, Fix 2(c). SGD 451,200.00 is the *target*, not a gap: "short by" states it withou, test_a_mislabelled_figure_through_the_graph_is_dropped(), test_a_never_say_phrase_is_dropped_even_when_correctly_labelled(), test_a_verdict_in_the_explanation_is_dropped_and_the_figure_kept(), test_the_explanation_stops_at_three_sentences()

### Community 147 - "Domain packs — start here"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 149 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 150 - "schedule.py"
Cohesion: 0.21
Nodes (12): build(), Any, The one Celery application, built from `Settings`.  Every setting here is a co, Construct the Celery application. Imported lazily by callers so that nothing whi, beat_schedule(), cron_expressions(), crontab_from(), manifest() (+4 more)

### Community 151 - "test_ingest_pipeline.py"
Cohesion: 0.13
Nodes (23): Chunk, chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own st, One flat list of chunks, ordinal running across the whole document. (+15 more)

### Community 152 - "Any"
Cohesion: 0.11
Nodes (15): document_row(), fact_row(), Any, date, ADR 0017: disabling insurance_agent switches off its voice, never a household's, Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with ev, A deleted document must not take the sentence down with it., Following a citation must never end in a blank screen because a pack was switche (+7 more)

### Community 153 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "README.md"
Cohesion: 0.06
Nodes (27): 1. Record architecture decisions, Consequences, Context, Decision, 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision (+19 more)

### Community 155 - "obligation"
Cohesion: 0.09
Nodes (38): conn(), FakeConn, obligation(), open_obligation(), overdue_row(), pack_row(), Snooze means 'not until this gets more urgent', so it can name the day it does., No new column: `already_said` is what makes the row quiet, and it reads this one (+30 more)

### Community 157 - "_today_items"
Cohesion: 0.21
Nodes (13): A document and a page, as a person would cite it — or, for published guidance, w, Source, TodayItem, _as_source(), _cite(), _link(), date, Split a formatted citation back into its parts, keeping the text either way. (+5 more)

### Community 159 - "4. Writing `pack.yaml`"
Cohesion: 0.12
Nodes (15): 1. What a pack is, 2. The one thing to understand before you start, 3. The workflow, 4. Writing `pack.yaml`, 5. The grounding corpus, 6. Definition of done, 7. Where to ask, Authoring a domain pack (+7 more)

### Community 160 - "13. A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.18
Nodes (9): 13. A question is understood before it is searched, and scoped before it is cut, Consequences, Context, Decision, Evidence, 15. A name scopes a question, and a grandparent is not a parent, Consequences, Context (+1 more)

### Community 161 - "Try PARROT"
Cohesion: 0.12
Nodes (16): 1 · Install five things, 2 · Download the AI models, 3 · Get the code and set it up, 4 · Put some documents in, 5 · Run it, 6 · Use it, Ask — a question about your own documents, If something goes wrong (+8 more)

### Community 162 - "github.md"
Cohesion: 0.50
Nodes (3): Last sync, Screen map, Updated in this project

### Community 163 - "walk"
Cohesion: 0.25
Nodes (18): collectProps(), compileAttr(), cssToObj(), getReact(), hostPositionStyle(), isDeckMountTag(), kebabToCamel(), renderDeckKids() (+10 more)

### Community 164 - "obligations.py"
Cohesion: 0.48
Nodes (6): answer(), build_context(), format_sources(), Ollama, Answer a question from retrieved chunks, with citations back to the file.  The, Hit

### Community 165 - "gate.py"
Cohesion: 0.18
Nodes (11): createExternalModules(), createHelmetManager(), createRegistry(), createRuntime(), createStreamTracker(), findTopLevelEquality(), init(), parensWrapWhole() (+3 more)

### Community 166 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 167 - "application"
Cohesion: 0.26
Nodes (12): _beat_needs_its_own_process(), celery_argv(), main(), Any, Namespace, Popen, Run the ingestion worker, and optionally the nightly schedule with it.      uv, The arguments the Celery command-line would have been given. Built here so a tes (+4 more)

### Community 168 - "check_content"
Cohesion: 0.25
Nodes (16): FakeConn, _no_owner(), _owned(), The types a calculator hands back, the owner's consent, and the record of an adv, A recording fake in the house style (see `tests/test_grounding_index.py`'s `Fake, Script the owner household.owner reads: one person, `is_owner`., test_a_withdrawal_after_a_grant_gives_none(), test_an_older_version_gives_status_outdated() (+8 more)

### Community 169 - "classify.py"
Cohesion: 0.29
Nodes (6): Are you covered?, Should you upgrade to an IP?, The deductible is the fixed amount you pay each policy year – ranging from $1,500 to $3,500, depending on ward class – before any payout from your IP. The co-payment is 5% of the bill, capped at a minimum of $6,000 per year., Understanding integrated shield plans, Your budget, Your comfort level with the types of hospitals, wards and doctors

### Community 170 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 171 - "igd-capstone-2026"
Cohesion: 0.20
Nodes (10): Authoring a pack, igd-capstone-2026, `main` is not protected, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live (+2 more)

### Community 172 - "FakeCursor"
Cohesion: 0.33
Nodes (5): About Integrated Shield Plan, How do I find out if I have an Integrated Shield Plan?, How do Integrated Shield Plan premiums and claims work?, Should I consider purchasing an Integrated Shield Plan?, What is an Integrated Shield Plan?

### Community 173 - "boot"
Cohesion: 0.22
Nodes (10): boot(), dcNameFromPath(), getReactDOM(), parseDataProps(), parseDcDocument(), parseDcText(), rootNameForDocument(), safeDecode() (+2 more)

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
Cohesion: 0.33
Nodes (5): MediShield Life Premium Schedule for Singapore Citizens and Permanent Residents, Merdeka Generation Subsidy, Pioneer Generation Subsidy, Premium and Subsidy Tables, Premium Subsidy for the Lower- to Middle-Income

### Community 180 - "start_parrot.py"
Cohesion: 0.32
Nodes (7): main(), Path, Local-only startup preflight, using the standard library so setup can be diagnos, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file conte, report_hardware(), startup_gaps()

### Community 181 - "FactRow"
Cohesion: 0.33
Nodes (5): Exclusions under MediShield Life, Fertility Preservation Procedures in cases of potential iatrogenic infertility, List of Serious Pregnancy and Delivery-related Complications, MediShield Life Benefits, MediShield Life Benefits

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
Cohesion: 0.07
Nodes (35): enabled_pack_ids(), enabled_packs(), The packs left switched on, plus `core`, or `None` when nothing has been install, The installed packs a person has left switched on, as loaded pack objects., connect(), DatabaseUnavailable, Any, RuntimeError (+27 more)

### Community 186 - "contracts.py"
Cohesion: 0.20
Nodes (15): Advice, Answering, Grounding, GroundingDocument, Guardrails, ModuleTrigger, Persona, BaseModel (+7 more)

### Community 187 - "14 · A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.33
Nodes (6): 14 · A pack supplies what the core knows about a domain, and the core stays generic, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 188 - "16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.33
Nodes (6): 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 189 - "page.tsx"
Cohesion: 0.21
Nodes (11): index_pack(), IndexReport, Any, date, Ollama, Path, Index a pack's published sources, and stage the values they print for a person t, Upsert this pack's sources and stage the values a changed one prints.      A p (+3 more)

### Community 190 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 191 - "gate.py"
Cohesion: 0.29
Nodes (7): _normal(), "1,860.00", "1860" and "01" → "1860", "1860", "1": formatting is not a different, Every number or identifier in a sentence that no cited passage prints. An identi, unprinted_numbers(), test_a_date_on_file_may_be_written_the_way_a_person_says_it(), test_a_leading_zero_does_not_make_a_printed_date_unprinted(), test_a_policy_number_is_kept_only_when_it_is_printed_whole()

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
Cohesion: 0.09
Nodes (18): Dispatcher, Protocol, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Send, attribution(), dispatcher_for(), FolderCapture (+10 more)

### Community 198 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 199 - "test_advice_core.py"
Cohesion: 0.31
Nodes (9): check_content(), Why a cited sentence still cannot be kept, or `None`. Asked after `check_one` pa, _calculation(), test_check_content_keeps_a_sentence_stating_a_facts_value(), test_check_content_keeps_a_sentence_stating_a_figure(), test_check_content_keeps_a_sentence_stating_a_rules_value(), test_check_content_still_drops_a_sentence_stating_an_unprinted_number(), test_passages_for_gives_fact_rule_and_calculation_refs() (+1 more)

### Community 200 - "ScriptedOllama"
Cohesion: 0.07
Nodes (70): AdviceShape, One kind of advice question, and everything its calculator needs to answer it., AdviceLog, AdviceRecord, Adviser, ConsentBook, Input, date (+62 more)

### Community 204 - "FakeCursor"
Cohesion: 0.24
Nodes (3): FakeCursor, Any, FakeConn

### Community 205 - "chunk.py"
Cohesion: 0.40
Nodes (3): HouseholdAdviceLog, The record of every advised or withheld answer (ADR 0016).  `advice_records` k, `core.graph.advice.AdviceLog` over a live connection.      `basis` is dumped w

### Community 206 - "The household, and the word "my""
Cohesion: 0.40
Nodes (3): The page a person sees while Parrot starts, served by the engine itself.  **Wh, The whole page. `screens_url` is escaped into a data attribute, never into scrip, render()

### Community 207 - "test_an_advice_card_carries_a_rules_publisher_on_the_wire"
Cohesion: 0.33
Nodes (7): advice_card(), A published value's chip: no document and no page, only who published it and whe, A published number has no page to open. What makes it checkable is who published, Nothing shown, nothing recorded. Once advice is on the screen, a failure after i, rule_citation(), test_an_advice_card_carries_a_rules_publisher_on_the_wire(), test_an_answer_that_fails_before_any_advice_is_rolled_back_and_after_it_is_kept()

### Community 209 - "FakeCursor"
Cohesion: 0.40
Nodes (4): Data inventory — identity data, dates of birth and loans, Open questions for Siew, The inventory, What this entry covers

### Community 210 - "is_first_person"
Cohesion: 0.33
Nodes (6): is_first_person(), Whether this question is about the person asking.      `other_names` are the d, "What is Rachel's premium on my policy" is a question about Rachel.      A rel, test_a_named_household_member_wins_over_the_pronoun(), test_first_person_questions_are_recognised(), test_questions_about_other_people_are_not_scoped()

### Community 211 - "installed_packs"
Cohesion: 0.67
Nodes (3): _kind_of(), `"fact:12"` -> `"fact"`, `"rule:7"` -> `"rule"`. Anything else is a calculator b, Kind

### Community 212 - "find_browser_executable"
Cohesion: 0.47
Nodes (5): find_browser_executable(), generate_documents(), Path, Project Parrot - Synthetic Document Generator for Lim Household ===============, Find Microsoft Edge or Google Chrome executable on Windows.

### Community 216 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 218 - "12. Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.33
Nodes (5): 12. Chunks follow the document's headings, and embeddings use the model's task prompts, Consequences, Context, Decision, Evidence

### Community 221 - "5. The watched folder is polled for stability, not subscribed to for events"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 222 - "NoReranker"
Cohesion: 0.29
Nodes (4): DenseRetriever, NoReranker, A dense-only retriever, so the graph can be run and tested before Lane B's hybri, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this with

## Knowledge Gaps
- **669 isolated node(s):** `npx`, `@modelcontextprotocol/server-filesystem`, `packs`, `modules`, `traces` (+664 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `run_parrot.py`, `FolderAdapter`, `Any`, `_answer_events`, `IngestJob`, `test_api.py`, `FakeConn`, `test_worker_queue.py`, `test_household.py`, `schedule.py`, `obligation`, `test_modules.py`, `application`, `routes.py`, `ModelUnavailable`, `.json`, `settings`, `State`, `bench_runtime.py`, `test_startup.py`, `registry.py`, `Registration`, `Ollama`, `test_grounding_index.py`, `test_advice_module.py`, `Any`, `test_answer_graph.py`, `build.py`, `rows_for`, `test_telegram_capture.py`, `page.tsx`, `.load`, `test_lifecycle.py`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `ModelUnavailable` connect `State` to `Ollama`, `ModelUnavailable`, `ScriptedOllama`, `rows_for`, `test_grounding_index.py`, `DenseRetriever`, `.load`, `The household, and the word "my"`, `test_answer_graph.py`, `test_grounding_values.py`, `review_grounding_values.py`, `household.py`, `extract.py`, `FakeOllama`, `.json`, `Settings`, `InstalledPack`, `route.ts`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `InstalledPack` connect `ScriptedOllama` to `Any`, `_answer_events`, `test_api.py`, `ModuleAdviser`, `FakeConn`, `review_grounding_values.py`, `obligation`, `ModelUnavailable`, `routes.py`, `__init__.py`, `.json`, `settings`, `State`, `page.tsx`, `pipeline.py`, `registry.py`, `test_advice_module.py`, `test_grounding_index.py`, `api.ts`, `DenseRetriever`, `test_answer_graph.py`, `Passage`, `pack`, `InstalledPack`, `PackUnavailable`, `test_grounding_values.py`, `SourceText`, `test_contracts.py`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 64 inferred relationships involving `InstalledPack` (e.g. with `_Answering` and `AdviceLog`) actually correct?**
  _`InstalledPack` has 64 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `ScriptedOllama` (e.g. with `Adviser` and `Consents`) actually correct?**
  _`ScriptedOllama` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 38 inferred relationships involving `Passage` (e.g. with `AdviceLog` and `AdviceRecord`) actually correct?**
  _`Passage` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `FakeConn` (e.g. with `HouseholdConsents` and `HouseholdAdviceLog`) actually correct?**
  _`FakeConn` has 19 INFERRED edges - model-reasoned connections that need verification._