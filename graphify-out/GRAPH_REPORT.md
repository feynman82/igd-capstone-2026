# Graph Report - igd-capstone-2026  (2026-09-15)

## Corpus Check
- 0 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3437 nodes · 8140 edges · 215 communities (187 shown, 28 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 1049 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `29fce05b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_parrot.py
- packs/page.tsx
- Christian — task list
- validate
- 4. Writing `pack.yaml`
- Project PARROT — team split
- Project PARROT — team split
- sha256
- Running the evaluation harness
- support.js
- Desmond — task list
- Zee — task list
- Yew Mun — task list
- Try PARROT
- Filling the corpus register
- Writing a governance artefact
- Claude Code — read this first
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
- Grounding corpora
- Notice
- Changelog
- filesystem
- `docs/governance/` — the assurance artefacts
- corpus/__init__.py
- packs/__init__.py
- parrot
- test_household.py
- The household, and the word "my"
- IngestJob
- alert/__init__.py
- find_page
- TelegramAdapter
- export-design-preview.cjs
- cli.py
- owner
- tasks.py
- test_pages.py
- test_ingest_pipeline.py
- bench_runtime.py
- compilerOptions
- parse.py
- test_startup.py
- pipeline.py
- registry.py
- baseline.py
- test_advice_module.py
- FakeConn
- preview.tsx
- react
- Starting Parrot
- FakeCursor
- FolderAdapter
- Notion
- Alert
- The demonstration run sheet
- PaperBrain
- Contributing
- unlock/page.tsx
- components.json
- Due
- ConfigurationError
- Architecture
- Roadmap
- contracts.py
- power-menu.tsx
- lock.ts
- checks.py
- build.py
- test_answer_graph.py
- Registration
- Home Contents Insurance Policy
- api/__init__.py
- core/__init__.py
- runtime/__init__.py
- modules/__init__.py
- setup.sh
- 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module
- rows_for
- models.py
- 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack
- vault/page.tsx
- Siew — task list
- WhoIsThis
- Settings
- vault.py
- dependencies
- Claim
- test_grounding_values.py
- household.py
- GroundingCorpus
- TelegramAdapter
- NNNN · The decision, as a statement not a question
- test_lifecycle.py
- worker/__init__.py
- app/layout.tsx
- graph/__init__.py
- item-row.tsx
- SentenceScanner
- reminder/__init__.py
- Household canon
- next
- tokens/page.tsx
- FolderAdapter
- 1. Record architecture decisions
- Any
- routes.py
- 10. `main` is unprotected, and the discipline is human
- Cursor
- document-detail.tsx
- today/page.tsx
- values.py
- 4. Local setup can run before the household assistant is ready
- FactRow
- FakeConn
- StreamingGraph
- PackManifest
- (app)/layout.tsx
- devDependencies
- Working agreement for coding agents
- review_grounding_values.py
- FakeCursor
- Desmond — Lane E · Corpus and adversarial testing
- build
- ingest/quarantine.py
- Any
- 2. One PostgreSQL instance for everything
- 12. Chunks follow the document's headings, and embeddings use the model's task prompts
- date
- _today_items
- postcss.config.mjs
- 4. Writing `pack.yaml`
- 13. A question is understood before it is searched, and scoped before it is cut
- Try PARROT
- github.md
- scripts
- main.py
- gate.py
- Notebook prompts — the four full policies for Marcus Lim
- worker.py
- test_advice_core.py
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
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- start_parrot.py
- _Value
- installed_packs
- Installed
- Yew Mun — Lane B · Retrieval and evaluation
- ask.py
- .embed_documents
- 14 · A pack supplies what the core knows about a domain, and the core stays generic
- 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent
- resolve
- The team
- _as_response
- 0002_household.sql
- 0003_advice.sql
- 5. The watched folder is polled for stability, not subscribed to for events
- getReact
- Notice
- connection
- 7. The answer graph ships before hybrid retrieval and before a checkpoint table
- test_a_grounding_corpus_travels_inside_its_pack
- VaultFact
- eslint.config.mjs
- __init__.py
- README.md
- queries.py
- test_generated_files_are_in_sync
- test_advice_is_a_module
- _meets_calculation
- next.config.ts
- test_a_citation_that_resolves_to_nothing_still_says_what_it_said
- CorrectionRequest
- PlaceRequest
- _gap_shared_value_calculation
- test_an_unconfirmed_alias_resolves_to_nobody
- test_the_debounce_key_separates_two_policies_of_one_person

## God Nodes (most connected - your core abstractions)
1. `InstalledPack` - 125 edges
2. `Passage` - 93 edges
3. `ScriptedOllama` - 89 edges
4. `Settings` - 83 edges
5. `AnswerGraph` - 79 edges
6. `ModelUnavailable` - 77 edges
7. `Ollama` - 77 edges
8. `FakeConn` - 72 edges
9. `Sentence` - 67 edges
10. `Calculation` - 65 edges

## Surprising Connections (you probably didn't know these)
- `_settings()` --indirect_call--> `settings()`  [INFERRED]
  api/routes.py → tests/test_api.py
- `ModelWarmth` --uses--> `ModelUnavailable`  [INFERRED]
  api/startup.py → core/runtime/ollama.py
- `ModelWarmth` --uses--> `Ollama`  [INFERRED]
  api/startup.py → core/runtime/ollama.py
- `FakeRegistrar` --uses--> `TelegramSettings`  [INFERRED]
  tests/test_telegram_capture.py → core/adapters/telegram.py
- `FakeTelegram` --uses--> `TelegramSettings`  [INFERRED]
  tests/test_telegram_capture.py → core/adapters/telegram.py

## Import Cycles
- None detected.

## Communities (215 total, 28 thin omitted)

### Community 0 - "run_parrot.py"
Cohesion: 0.13
Nodes (23): Load the generator and the embedder before the first question, and record the ou, warm_models(), broker_available(), Whether Redis answers. Not whether a worker is listening — `core/runtime/checks., _kill_tree(), main(), parse_args(), port_answers() (+15 more)

### Community 1 - "packs/page.tsx"
Cohesion: 0.13
Nodes (11): DocumentPage(), metadata, metadata, EmptyState(), ProblemState(), SHAPES, QuarantineQueue(), document() (+3 more)

### Community 2 - "Christian — task list"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.09
Nodes (39): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), Validate a document register before it is handed over.      python -m corpus.v, Parse `field_pages`: semicolon-separated `name=page`, 1-based. Empty means page (+31 more)

### Community 4 - "4. Writing `pack.yaml`"
Cohesion: 0.52
Nodes (6): ACTIONS, GET(), POST(), sameOrigin(), unlocked(), isUnlocked()

### Community 5 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 6 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 7 - "sha256"
Cohesion: 0.17
Nodes (10): Cursor, Insert or update the `documents` row for these bytes and say which happened., register_document(), database_url(), The idempotent upsert, against the real unique index.  `documents.sha256 UNIQU, test_a_document_must_arrive_with_a_name(), test_a_new_document_is_inserted(), test_an_empty_payload_is_refused() (+2 more)

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

### Community 13 - "Try PARROT"
Cohesion: 0.18
Nodes (26): Figure, One number a calculator produced, and the words a sentence must use to state it., _amount(), Basis, calculate(), _calculation(), _capital(), cents() (+18 more)

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
Cohesion: 0.08
Nodes (39): The one interface every capture channel satisfies.      receive(payload, mime,, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256` i, sha256(), Queued, What happens to a document between "these bytes are registered" and "this docume, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker.      Celery is imported here, What every capture channel hands a document to.  An adapter's job ends at "the (+31 more)

### Community 18 - "Zee — Lane D · Domain packs and interface"
Cohesion: 0.40
Nodes (3): CaptureAdapter, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., Capture adapters.  Every channel a document can arrive through satisfies one i

### Community 19 - "Authoring a domain pack"
Cohesion: 0.15
Nodes (19): FieldSpec, One extractable field. Its `name` is the column header in Desmond's register and, _coerce(), _date_renderings(), decode_schema(), _drop_format(), Extraction, _prepare() (+11 more)

### Community 20 - "Household canon"
Cohesion: 0.25
Nodes (7): Address, Employment, Household canon, Life events that documents must reflect, People, Policies, Vehicles

### Community 21 - "Registration"
Cohesion: 0.14
Nodes (16): HouseholdConsents, `core.graph.advice.ConsentBook` over a live connection, for the graph to ask wit, HouseholdAdviceLog, `core.graph.advice.AdviceLog` over a live connection.      `basis` is dumped w, DenseRetriever, HouseholdInventory, Handed to `AnswerGraph` by whoever holds a connection, as `HouseholdScope` is., enabled_pack_ids() (+8 more)

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

### Community 29 - "test_modules.py"
Cohesion: 0.18
Nodes (21): FakeConn, FakePack, obligation_row(), Reminder and Alert: what fires, once, and with what behind it.  Both modules a, A sweep for a date in the future must record that date, or it repeats itself., One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order., A live travel policy must not make a lapsed motor policy read as covered., srs_row() (+13 more)

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
Cohesion: 0.07
Nodes (72): The record of every advised or withheld answer (ADR 0016).  `advice_records` k, AdviceShape, One kind of advice question, and everything its calculator needs to answer it., AdviceLog, AdviceRecord, Adviser, Calculation, ConsentBook (+64 more)

### Community 40 - "Notice"
Cohesion: 0.18
Nodes (16): document_title(), The document as a person would name it: its `string` fields as read, in the pack, pgvector accepts its own text form; this avoids registering an adapter for one c, _vector_literal(), indexed(), IndexedDocument, Rebuild a document's chunks and vectors without reading it again for facts.  C, Safe to show: names what went wrong, never what the document says. (+8 more)

### Community 41 - "Changelog"
Cohesion: 0.50
Nodes (3): Changelog, W1 · 2–8 Sep 2026, W2 · 9–15 Sep 2026

### Community 42 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 43 - "`docs/governance/` — the assurance artefacts"
Cohesion: 0.50
Nodes (3): `docs/governance/` — the assurance artefacts, The autonomy statement in one line, The rule that governs all eight

### Community 51 - "test_household.py"
Cohesion: 0.11
Nodes (8): Inline, Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Send, An already-indexed document is not read again. Re-reading it would burn a minute, The row as it now stands, plus whether this call is the one that created it., Registration, FakeCursor

### Community 52 - "The household, and the word "my""
Cohesion: 0.10
Nodes (19): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model (+11 more)

### Community 53 - "IngestJob"
Cohesion: 0.17
Nodes (18): Advice, Answering, Category, FactInput, Grounding, GroundingDocument, Guardrails, ModuleTrigger (+10 more)

### Community 54 - "alert/__init__.py"
Cohesion: 0.12
Nodes (22): AlertConfig, Alert, cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject() (+14 more)

### Community 55 - "find_page"
Cohesion: 0.20
Nodes (13): current(), grant(), _latest(), NoOwner, The owner's consent to a pack's advice, append-only (ADR 0016).  Consent is th, Record the owner saying yes to `wording`, this pack's consent text at `version`., Record the owner taking it back. Append-only: the grant stays in the table, supe, No owner is recorded yet, so there is nobody whose consent this could be (ADR 00 (+5 more)

### Community 56 - "TelegramAdapter"
Cohesion: 0.07
Nodes (36): conn(), _household_scope(), Who is asking, and whose documents may answer.  Two halves, deliberately split, `empty_for_owner` must never fire on a question that was never scoped — otherwis, A second document must never silently move a name from one member to another., A daughter takes over her father's paperwork. The install follows., `HouseholdScope` over a roster held in memory, with every document resolved by n, The roster has no grandparent relation, so the household says it the only way it (+28 more)

### Community 57 - "export-design-preview.cjs"
Cohesion: 0.09
Nodes (44): RuleInput, _ambiguous(), _band(), _band_label(), _compare_market(), _compare_own(), fact_input(), _in_band() (+36 more)

### Community 58 - "cli.py"
Cohesion: 0.06
Nodes (67): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a, answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file.  The, Chunk, chunk_pages() (+59 more)

### Community 59 - "owner"
Cohesion: 0.14
Nodes (13): client(), conn(), FakeConn, The parameters of the one statement containing `needle`. Fails loudly if it neve, Capture would register it again within a minute, so the button would only appear, 13 September: the only answer was "someone else here", and the screen said, `hides its facts` reaches an answer through retrieval, not through the API., test_a_document_still_in_the_inbox_is_not_forgotten() (+5 more)

### Community 60 - "tasks.py"
Cohesion: 0.11
Nodes (32): queue(), Ask the vision-language model to read the pages. One request per page, so a page, Send the pages as images and try the whole pack pipeline again on what comes bac, The reportable line. Deliberately a rate and a count, because a rate over three, What is waiting for a person's eyes, oldest first., Recovery, recovery_rate(), retry() (+24 more)

### Community 61 - "test_pages.py"
Cohesion: 0.09
Nodes (40): blocked_reasons(), forget(), page_images(), QuarantinedDocument, The second stage of quarantine: the page image, read by the vision-language mode, Per document: `None` when the image pass can run, or the sentence saying why it, Safe to show. Forgetting a document whose file is still there would not last., Remove a quarantined document from Parrot's memory. Its name, or `None` if there (+32 more)

### Community 62 - "test_ingest_pipeline.py"
Cohesion: 0.09
Nodes (40): extract(), find_page(), _normalise(), The first page whose text contains this value. None means no page supports it., Never raises. A failure is a reason, and a reason routes the document to quarant, FakeOllama, _page_of_examples(), Parsing, chunking, extraction and the quarantine decision.  The model is faked (+32 more)

### Community 63 - "bench_runtime.py"
Cohesion: 0.09
Nodes (32): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+24 more)

### Community 64 - "compilerOptions"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 65 - "parse.py"
Cohesion: 0.14
Nodes (14): DoclingParser, _kind(), _pages_from(), Docling, held at arm's length: imported on first use, and never at module import, Group Docling's items by the page they were found on.      Docling's markdown, Docling's label, reduced to the one distinction chunking needs: is this a headin, A table as lines of text, one row per line: `label: value` when a row has two ce, _table_text() (+6 more)

### Community 66 - "test_startup.py"
Cohesion: 0.10
Nodes (16): prepare_checkout(), Startup tests do not ingest documents or need the corpus: they check process bou, npm is a wrapper around node. Killing only the wrapper orphans the port., The worker starts its nightly schedule as a process of its own. Terminating only, Stopping it signals its process group. Without a session of its own that group i, A developer's own `npm run dev` is used rather than fought for the port., `npm run dev` against an empty web/ fails slowly and cryptically. Say so instead, The screens follow the engine to whatever port it got, rather than to web/.env.l (+8 more)

### Community 67 - "pipeline.py"
Cohesion: 0.08
Nodes (27): ReminderConfig, Chunk, What is actually embedded: the prefix plus the text, matching the tsvector colum, ExtractedFact, The ingestion worker.  Capture registers a document; this package turns it int, fixed(), from_facts(), _label() (+19 more)

### Community 68 - "registry.py"
Cohesion: 0.11
Nodes (27): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders somewhe, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, Load the installed capability modules at runtime.  The mirror of `core/packs.p, A module's YAML is missing, or does not validate against `ModuleManifest`. (+19 more)

### Community 69 - "baseline.py"
Cohesion: 0.13
Nodes (11): Generated, Ollama, A question, embedded the way the model was trained to embed a search query., Passages as `(title, text)`, embedded the way the model was trained to embed a d, Load the generator and the embedder now, and say where the generator landed., Generate against a JSON schema. This is how extraction is held to a pack's field, The same constrained generation, yielded as it is written.          Identical, Whether this embedding model expects `QUERY_PROMPT` and `DOCUMENT_PROMPT`. (+3 more)

### Community 70 - "test_advice_module.py"
Cohesion: 0.14
Nodes (51): Missing, What a calculator returns when a fact or a rule value it needed was not there to, One person's advice. The graph asks whose first when a question names several pe, assert_nothing_negative(), basis(), fact(), figures_of(), _gap_basis() (+43 more)

### Community 71 - "FakeConn"
Cohesion: 0.11
Nodes (26): _Connected, _extracted(), FakeConn, _installed(), Indexing a pack's sources into pending values, and a reviewer approving or rejec, A recording fake in the house style (see `tests/test_api.py`'s `FakeConn`): ever, Patch the settings, database and pack lookups `scripts/index_grounding.py` impor, Patch the settings and database `scripts/review_grounding_values.py` imports. (+18 more)

### Community 72 - "preview.tsx"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 73 - "react"
Cohesion: 0.17
Nodes (11): HouseholdPage(), metadata, OwnerForm(), RELATION_CHOICES, Roster(), Place, PLACES, WhoIsThis() (+3 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.12
Nodes (17): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+9 more)

### Community 75 - "FakeCursor"
Cohesion: 0.13
Nodes (13): by_subject(), db(), FakeCursor, load_register(), Every batch1 row as the facts extraction would write, through the statement it u, One member's statement must never drive another member's 15,300 cap., On 10 February 2027 Marcus's home contents cover has lapsed, while his motor and, test_a_deductible_receipt_counts_in_its_own_year_only() (+5 more)

### Community 76 - "FolderAdapter"
Cohesion: 0.21
Nodes (12): _conn_returning(), _passage(), The third bucket. Home contents, a utility bill — nobody's name on it, everybody, A joint policy is the owner's too. Presence wins over exclusion., Asked about my policy; the vault holds Rachel's. Say so, rather than answer hers, A fresh install is not broken. It answers about the household, as it always did., test_a_document_naming_the_owner_and_somebody_else_is_kept(), test_a_document_with_no_subject_belongs_to_everybody() (+4 more)

### Community 77 - "Notion"
Cohesion: 0.29
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "Alert"
Cohesion: 0.08
Nodes (66): Abstained, AnswerGraph, Built once, asked many times. Holds no connection: retrieval does., The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer.          The i, Scoped, ModelUnavailable, Safe to show: names what could not be done, never the document it was doing it t (+58 more)

### Community 79 - "The demonstration run sheet"
Cohesion: 0.14
Nodes (14): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+6 more)

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (7): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Contributing"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 82 - "unlock/page.tsx"
Cohesion: 0.43
Nodes (7): ALLOWED, Context, DELETE(), forward(), GET(), PATCH(), POST()

### Community 83 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 84 - "Due"
Cohesion: 0.06
Nodes (32): _advice_basis(), _advice_prompt(), answer_system(), _citations(), _conversation(), _either(), _numbered(), The shape a question asks for, matched from the pack's own phrases without a mod (+24 more)

### Community 85 - "ConfigurationError"
Cohesion: 0.10
Nodes (29): _chat_ids(), ConfigurationError, _flag(), _folder(), local_url(), _port(), _positive(), Small, literal .env reader with environment overrides and loopback-only endpoint (+21 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "contracts.py"
Cohesion: 0.08
Nodes (39): DocumentTypeSpec, One kind of document this pack recognises., glossary(), _make_replacer(), mentions(), _pattern(), What a pack knows about how people ask, applied without a model.  Three things, The question with each declared phrase replaced by what the documents print, lon (+31 more)

### Community 89 - "power-menu.tsx"
Cohesion: 0.19
Nodes (10): Action, CONFIRM, ITEMS, Stage, DependencyCheck, Phase, RestartingScreen(), ShutDownScreen() (+2 more)

### Community 90 - "lock.ts"
Cohesion: 0.18
Nodes (20): GET(), grant(), POST(), UnlockPage(), Accepted, clearFailures(), derive(), failures (+12 more)

### Community 91 - "checks.py"
Cohesion: 0.13
Nodes (28): create_app(), The local API. Liveness is intentionally separate from assistant readiness.  L, capture_check(), Check, collect_checks(), database_check(), interface_check(), model_check() (+20 more)

### Community 92 - "build.py"
Cohesion: 0.10
Nodes (25): PackManifest, A domain pack, authored as one YAML file., (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why this pack cannot supply `field` from every one of `doc_types`, or None if it, An advice shape that names a missing role, field, category or key fails at load, A compared field no document type of the shape declares can never be printed., _class_name(), _docstring() (+17 more)

### Community 93 - "test_answer_graph.py"
Cohesion: 0.22
Nodes (6): metadata, PacksPage(), Toggle(), ModuleSummary, packs(), PackSummary

### Community 94 - "Registration"
Cohesion: 0.09
Nodes (28): TelegramSettings, Dispatcher, Given a registered document, arrange for it to be read. Says what it arranged., Intake, attribution(), dispatcher_for(), FolderCapture, Run the capture loops in background threads, beside the local server.  This is (+20 more)

### Community 102 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "rows_for"
Cohesion: 0.15
Nodes (26): client_for(), open_obligation(), pack_row(), The point of the endpoint. An UPDATE alone loses the example we are trying to co, Snooze means 'not until this gets more urgent', so it can name the day it does., No new column: `already_said` is what makes the row quiet, and it reads this one, A client whose database is `conn`.      `base_url` is loopback because `Truste, b1-0032.pdf on 13 September: deleted from the inbox, and still asking for attent (+18 more)

### Community 104 - "models.py"
Cohesion: 0.10
Nodes (27): CloseRequest, CorrectionResponse, EnabledRequest, ErrorEvent, ForgottenDocument, HouseholdResponse, ObligationChanged, PacksResponse (+19 more)

### Community 105 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 106 - "vault/page.tsx"
Cohesion: 0.10
Nodes (30): Safe to show: never contains the token., TelegramUnavailable, build(), FakeRegistrar, FakeTelegram, photo_update(), Telegram capture: what arrives, what is answered, and what is written where., A photograph as Telegram actually sends one: the same image in several sizes. (+22 more)

### Community 107 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 108 - "WhoIsThis"
Cohesion: 0.08
Nodes (54): AdviceCard, Finished, One sentence that has passed the gate, with the citations it passed on.      I, Everything that is only knowable once the last sentence is in.      `quarantin, A worked result, every word of it written by code, given before the model says a, Sentence, Whose situation a piece of advice is about — `whose`'s answer, with no passages, Whose situation a piece of advice is about — the judgement `apply` makes, withou (+46 more)

### Community 109 - "Settings"
Cohesion: 0.27
Nodes (10): countdown(), detail(), figure(), ItemRow(), longDate(), sentence(), TONE, WORD (+2 more)

### Community 110 - "vault.py"
Cohesion: 0.08
Nodes (32): _columns(), correct(), Corrected, CorrectionRejected, A person fixing a field the extractor got wrong.  This is the one place in the, `(value_text, value_num, value_date)` — exactly one of them set.      The decl, Store what a person says this field actually says, and keep what it used to say., Safe to show: there is no fact with that id. (+24 more)

### Community 111 - "dependencies"
Cohesion: 0.12
Nodes (17): ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes, tailwind-merge (+9 more)

### Community 112 - "Claim"
Cohesion: 0.10
Nodes (38): check(), check_advice(), check_one(), Claim, Never raises, never rewrites a claim. It keeps, drops, or abstains.      The w, Why an advice explanation cannot be kept, or `None`. Asked of a claim built over, Why this one sentence cannot be kept, or `None` if it can.      Depends on not, test_a_claim_citing_the_same_document_twice_says_it_once() (+30 more)

### Community 113 - "test_grounding_values.py"
Cohesion: 0.14
Nodes (30): number_tokens(), Every whole number the passage prints, thousands separators removed., _dropped(), Published values: the model reads a source, and code keeps only what the passage, Assert a value was dropped, and logged with this reason., _run(), test_a_money_value_with_a_currency_marker_is_kept(), test_a_multiple_is_kept_in_the_forms_it_is_written() (+22 more)

### Community 114 - "household.py"
Cohesion: 0.09
Nodes (26): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), pending(), PendingAlias, person_for_chat() (+18 more)

### Community 115 - "GroundingCorpus"
Cohesion: 0.13
Nodes (28): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Read and validate a pack's grounding corpus from its own folder on disk.  A pa, A pack's grounding corpus on disk does not match what its `sources.yaml` records, Where this pack's grounding corpus lives on disk, or `None` if it declares none., Read, validate and hash every source this pack's corpus records.      Raises ` (+20 more)

### Community 116 - "TelegramAdapter"
Cohesion: 0.14
Nodes (14): _attachment(), _pixels(), The Telegram capture adapter.  Same interface as the folder: `receive(payload,, Confirm the token works before anything else is attempted., One `getUpdates` round. Returns what was captured; replies with what was receive, Delete at source. A failure is logged, never raised: the document is already our, What an HTTP status from the Bot API means, in a sentence a person can act on., How big a `PhotoSize` is: area first, declared bytes as the tie-break.      So (+6 more)

### Community 117 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 118 - "test_lifecycle.py"
Cohesion: 0.12
Nodes (25): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor., What the person asked for, once. The first request wins; later ones change nothi, _client(), _eventually(), _launcher(), quiet_engine(), Restart and shut down: the engine asks its supervisor, and nothing else can ask (+17 more)

### Community 120 - "app/layout.tsx"
Cohesion: 0.25
Nodes (6): figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 121 - "graph/__init__.py"
Cohesion: 0.08
Nodes (15): _kind_of(), passages_for(), `"fact:12"` -> `"fact"`, `"rule:7"` -> `"rule"`. Anything else is a calculator b, Inputs as kind fact/rule passages (chunk_id from the ref), and the figures as on, fuse(), Several searches as one list: each passage once, at the best score any phrasing, Every phrasing of the question, searched and fused. The person's own words alway, Passage (+7 more)

### Community 122 - "item-row.tsx"
Cohesion: 0.10
Nodes (35): _advised(), _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact(), _field_not_on_every_doc_type() (+27 more)

### Community 123 - "SentenceScanner"
Cohesion: 0.10
Nodes (27): Pulling finished sentences out of a JSON reply that is still being written.  T, What document would have answered this, if the model said. Read once, at the end, Feed it deltas; it returns whichever sentences became complete because of them., Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes on, Find `"sentences": [` once. Everything before it is of no interest.          S, SentenceScanner, drip() (+19 more)

### Community 124 - "reminder/__init__.py"
Cohesion: 0.09
Nodes (23): already_said(), current_lead(), Due, next_window(), Overdue, The Reminder module: a nightly sweep of obligations, and nothing fires twice., Past their date and never closed. A different problem from a reminder, shown sep, Safe to show: there is no obligation with that id, or it is already closed. (+15 more)

### Community 125 - "Household canon"
Cohesion: 0.14
Nodes (12): 1. How to read a criterion, 2. Rachel · Reminder module · Today, 3. Marcus · retrieval core · Ask, 4. Marcus and Rachel · capture · Vault, 5. Marcus · Alert module · Today, 6. The household ledger · Tracker · specification only, 7. Open questions for review, 8. The criteria as a checklist (+4 more)

### Community 126 - "next"
Cohesion: 0.14
Nodes (10): metadata, Abstention(), Part, sentence(), textOf(), ADR-0011, Turn(), Conversation() (+2 more)

### Community 127 - "tokens/page.tsx"
Cohesion: 0.11
Nodes (10): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+2 more)

### Community 128 - "FolderAdapter"
Cohesion: 0.10
Nodes (32): IngestJob, Magic bytes first, filename suffix second, `application/octet-stream` last., What a capture returns: a registered document, and whether we had seen it before, sniff_mime(), FolderAdapter, FolderSettings, _Pending, The watched-folder capture adapter.  A person drops a scan into a folder and i (+24 more)

### Community 129 - "1. Record architecture decisions"
Cohesion: 0.17
Nodes (22): A rule or table value a pack's sources publish.      Extracted automatically,, ValueKey, extract_values(), ExtractedValue, _prompt(), Every value the source prints for these keys, kept only when its passage prints, _schema(), _long_text() (+14 more)

### Community 130 - "Any"
Cohesion: 0.12
Nodes (18): names_for(), Each person's display name and confirmed aliases, trimmed and lower-cased the wa, advised_pack(), db(), _document(), _facts_tuple(), FakeConn, FakeCursor (+10 more)

### Community 131 - "routes.py"
Cohesion: 0.10
Nodes (24): AskRequest, ConfirmNameRequest, ModuleSummary, OwnerRequest, PackSummary, PersonModel, First run: the name on your documents. One field, because the owner is the one p, The answer to "who is this?". Either an existing person, or a new one to create. (+16 more)

### Community 132 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 133 - "Cursor"
Cohesion: 0.23
Nodes (12): _decide(), _Decision, named_in(), _names(), Whose question is this, and whose documents may answer it.  "What is my term l, `(word, relation)` when the question asks about a relation's own documents, else, Everybody in `people` the question names.      A person is named by a whole di, Who a question is about, decided once and read differently by `apply` and `whose (+4 more)

### Community 134 - "document-detail.tsx"
Cohesion: 0.14
Nodes (16): Field(), format(), isNumeric(), ALWAYS_EXISTS, AskResponse, Claim, CorrectionResponse, HouseholdResponse (+8 more)

### Community 136 - "today/page.tsx"
Cohesion: 0.16
Nodes (12): createRegistry(), AppLayout(), isUrgent(), metadata, summary(), TodayPage(), VaultPage(), get() (+4 more)

### Community 137 - "values.py"
Cohesion: 0.10
Nodes (26): _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), _pack(), parse_value(), printed_as() (+18 more)

### Community 138 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.08
Nodes (25): a_citation(), FakeGraph, graph(), inbox(), The five endpoints, against a fake database and the real queries.  The connect, Stands in for `AnswerGraph` at the seam `api/routes.py` owns., What a retrieved passage hands over: the sentence a person reads, and the id a l, The JSON endpoint ends the way the stream does: an abstention is signed too. (+17 more)

### Community 139 - "FactRow"
Cohesion: 0.14
Nodes (17): Categories, categorise(), The first rule whose printed words appear. `None` is an answer, not a failure., _fact(), fact_row(), FactRow, facts_for(), in_category() (+9 more)

### Community 140 - "FakeConn"
Cohesion: 0.23
Nodes (15): FakeConn, _no_owner(), _owned(), A recording fake in the house style (see `tests/test_grounding_index.py`'s `Fake, Script the owner household.owner reads: one person, `is_owner`., test_a_withdrawal_after_a_grant_gives_none(), test_an_older_version_gives_status_outdated(), test_current_is_none_when_the_latest_grant_is_a_different_version() (+7 more)

### Community 141 - "StreamingGraph"
Cohesion: 0.15
Nodes (17): Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive together,, No `reading` before it: the floor is checked before the model is asked anything., By then the 200 has been sent. An exception that only logged would leave a scree, A line about a document on file is not the answer to "does it cover floods?"., sse(), streaming() (+9 more)

### Community 142 - "PackManifest"
Cohesion: 0.20
Nodes (10): AbstentionEvent, DeclinedEvent, FinishedEvent, One sentence that has passed the gate, with the sources it passed on.      It, A request for a recommendation or a judgement, declined by a pack without advice, Evidence gathered and good enough to answer from. Nothing has been claimed yet., ReadingEvent, RefusalEvent (+2 more)

### Community 143 - "(app)/layout.tsx"
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
Nodes (13): approve(), pending(), PendingValue, A person's approval, standing between a model's extraction and any calculator th, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it., Every value still waiting for review, oldest first, optionally for one pack., Approve these ids, ignoring any that are no longer `pending`. Returns the count (+5 more)

### Community 147 - "FakeCursor"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 149 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 150 - "build"
Cohesion: 0.24
Nodes (10): build(), The one Celery application, built from `Settings`.  Every setting here is a co, Construct the Celery application. Imported lazily by callers so that nothing whi, beat_schedule(), cron_expressions(), crontab_from(), manifest(), When the nightly sweeps run, read from the modules' own manifests.  A module a (+2 more)

### Community 151 - "ingest/quarantine.py"
Cohesion: 0.09
Nodes (31): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own st, One flat list of chunks, ordinal running across the whole document., The page as `(is_heading, line)`, from the parser's structure when it has any. (+23 more)

### Community 153 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "12. Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.06
Nodes (28): 1. Record architecture decisions, Consequences, Context, Decision, 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision (+20 more)

### Community 155 - "date"
Cohesion: 0.13
Nodes (21): obligation(), overdue_row(), One row of `reminder.OVERDUE`, in its column order., The nightly sweep owns `last_notified_at`. A screen refresh must not burn a wind, A registry that failed to install must fail loudly, not silently silence the hou, The default database: two packs installed and enabled, and nothing else., The Celery beat never goes through the API, so the filter cannot live there., A date that has passed is the one somebody most wants to check against the paper (+13 more)

### Community 157 - "_today_items"
Cohesion: 0.29
Nodes (8): A document and a page, as a person would cite it., Source, TodayItem, _cite(), _link(), Split a formatted citation back into its parts, keeping the text either way., Fill in `document_id` on every source, in one query for the whole response., _today_items()

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

### Community 163 - "scripts"
Cohesion: 0.30
Nodes (15): collectProps(), compileAttr(), cssToObj(), hostPositionStyle(), isDeckMountTag(), kebabToCamel(), renderDeckKids(), walk() (+7 more)

### Community 164 - "main.py"
Cohesion: 0.14
Nodes (11): ModelWarmth, The page a person sees while Parrot starts, served by the engine itself.  **Wh, Whether the generator has been loaded yet, and where it landed. Written by one t, The whole page. `screens_url` is escaped into a data attribute, never into scrip, render(), _ollama_answering(), 13 September: size_vram was 0 on every model and nothing on screen said so., test_a_model_that_cannot_load_is_recorded_rather_than_raised() (+3 more)

### Community 165 - "gate.py"
Cohesion: 0.29
Nodes (7): _normal(), "1,860.00", "1860" and "01" → "1860", "1860", "1": formatting is not a different, Every number or identifier in a sentence that no cited passage prints. An identi, unprinted_numbers(), test_a_date_on_file_may_be_written_the_way_a_person_says_it(), test_a_leading_zero_does_not_make_a_printed_date_unprinted(), test_a_policy_number_is_kept_only_when_it_is_printed_whole()

### Community 166 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 167 - "worker.py"
Cohesion: 0.22
Nodes (13): application(), The configured application with its tasks registered. One per process., Return something that puts one ingestion message on the queue and yields its tas, sender(), _beat_needs_its_own_process(), celery_argv(), main(), Run the ingestion worker, and optionally the nightly schedule with it.      uv (+5 more)

### Community 168 - "test_advice_core.py"
Cohesion: 0.20
Nodes (15): Exclusions, A sentence claiming cover whose every citation sits under one of `headings` is d, check_content(), The grounding gate.  Rule 3 in AGENTS.md: no claim without a citation. This mo, Why a cited sentence still cannot be kept, or `None`. Asked after `check_one` pa, _says(), Verdict, _calculation() (+7 more)

### Community 169 - "classify.py"
Cohesion: 0.22
Nodes (10): document_row(), fact_row(), filed_document(), v1 keeps the inbox as the document store, so this is a real state, not a fault., Following a citation must never end in a blank screen because a pack was switche, test_a_document_whose_file_left_the_inbox_is_409_not_500(), test_a_page_comes_back_as_an_image(), test_a_page_that_does_not_exist_is_a_404_that_says_so() (+2 more)

### Community 170 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 171 - "igd-capstone-2026"
Cohesion: 0.20
Nodes (10): Authoring a pack, igd-capstone-2026, `main` is not protected, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live (+2 more)

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

### Community 179 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.29
Nodes (8): createExternalModules(), createHelmetManager(), createPseudoSheet(), createRuntime(), importantify(), Placeholder(), scanUnquotedUrl(), stripComments()

### Community 180 - "start_parrot.py"
Cohesion: 0.38
Nodes (6): main(), Local-only startup preflight, using the standard library so setup can be diagnos, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file conte, report_hardware(), startup_gaps()

### Community 181 - "_Value"
Cohesion: 0.31
Nodes (6): SourceChip(), SourcePanel(), DocumentDetail(), when(), pageImage(), Source

### Community 183 - "Installed"
Cohesion: 0.43
Nodes (7): lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns(), readEvents(), upstreamDetail()

### Community 184 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

### Community 185 - "ask.py"
Cohesion: 0.29
Nodes (4): NoReranker, A dense-only retriever, so the graph can be run and tested before Lane B's hybri, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this with, The one client that talks to Ollama.  Everything the platform infers goes thro

### Community 186 - ".embed_documents"
Cohesion: 0.38
Nodes (7): _pack_row(), packs(), One row of `packs`, with the manifest validated back out of its jsonb column., Every installed pack, with what it has extracted so far., Switch one pack on or off. Raises `UnknownPack` rather than silently doing nothi, RegisteredPack, set_pack_enabled()

### Community 187 - "14 · A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.33
Nodes (6): 14 · A pack supplies what the core knows about a domain, and the core stays generic, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 188 - "16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.33
Nodes (6): 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 189 - "resolve"
Cohesion: 0.33
Nodes (6): findTopLevelEquality(), parensWrapWhole(), resolve(), resolvePath(), walkText(), warnUnresolved()

### Community 190 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 191 - "_as_response"
Cohesion: 0.29
Nodes (7): AskResponse, Claim, One sentence and the passages it was traced to. Never emitted without `citations, _as_response(), _as_source(), A citation that never lost its document id, so the chip opens the page without a, One `Answer` to one of the shapes a client has to handle.

### Community 192 - "0002_household.sql"
Cohesion: 0.70
Nodes (4): document_attribution, people, person_aliases, telegram_identities

### Community 193 - "0003_advice.sql"
Cohesion: 0.60
Nodes (4): advice_consents, advice_records, grounding_sources, grounding_values

### Community 194 - "5. The watched folder is polled for stability, not subscribed to for events"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 195 - "getReact"
Cohesion: 0.40
Nodes (5): createComponentFactory(), evalDcLogic(), getReact(), react, react

### Community 196 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 197 - "connection"
Cohesion: 0.29
Nodes (7): _market(), _market_compares_an_undeclared_field(), A market comparison of the held hospital plan, on `compare_fields`, ordered by p, `annual_premium` is printed on no policy schedule; the market's sources publish, Two household documents can only be compared on what a household document prints, test_a_market_comparison_may_compare_a_field_only_its_sources_publish(), test_an_own_comparison_may_not_compare_a_field_only_sources_publish()

### Community 198 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 200 - "VaultFact"
Cohesion: 0.38
Nodes (4): metadata, UnlockForm(), Wordmark(), WordmarkLockup()

### Community 204 - "queries.py"
Cohesion: 0.33
Nodes (6): is_first_person(), Whether this question is about the person asking.      `other_names` are the d, "What is Rachel's premium on my policy" is a question about Rachel.      A rel, test_a_named_household_member_wins_over_the_pronoun(), test_first_person_questions_are_recognised(), test_questions_about_other_people_are_not_scoped()

### Community 205 - "test_generated_files_are_in_sync"
Cohesion: 0.33
Nodes (6): owner(), owner_aliases(), The person asking. `None` before setup has run, which every caller must handle:, Every confirmed string that means the owner. This is what scopes a first-person, Hand the household over. The owner is a row, not a value baked in at install., set_owner()

### Community 209 - "test_a_citation_that_resolves_to_nothing_still_says_what_it_said"
Cohesion: 0.40
Nodes (5): Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with ev, A deleted document must not take the sentence down with it., test_a_citation_that_resolves_to_nothing_still_says_what_it_said(), test_an_alerts_citation_carries_the_document_it_opens(), uncovered_since()

## Knowledge Gaps
- **576 isolated node(s):** `npx`, `@modelcontextprotocol/server-filesystem`, `packs`, `modules`, `traces` (+571 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `checks.py` to `run_parrot.py`, `Any`, `routes.py`, `sha256`, `4. Local setup can run before the household assistant is ready`, `StreamingGraph`, `review_grounding_values.py`, `Registration`, `build`, `Any`, `test_modules.py`, `worker.py`, `Notice`, `TelegramAdapter`, `ask.py`, `.embed_documents`, `owner`, `tasks.py`, `bench_runtime.py`, `test_startup.py`, `registry.py`, `baseline.py`, `test_advice_module.py`, `FakeCursor`, `Alert`, `ConfigurationError`, `Registration`, `vault/page.tsx`, `GroundingCorpus`, `test_lifecycle.py`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `Ollama` connect `baseline.py` to `run_parrot.py`, `1. Record architecture decisions`, `routes.py`, `values.py`, `test_worker_queue.py`, `Authoring a domain pack`, `Registration`, `ingest/quarantine.py`, `main.py`, `Grounding corpora`, `Notice`, `test_household.py`, `ask.py`, `tasks.py`, `test_pages.py`, `pipeline.py`, `Alert`, `ConfigurationError`, `checks.py`, `Registration`, `models.py`, `WhoIsThis`, `GroundingCorpus`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `InstalledPack` connect `Grounding corpora` to `Any`, `FactRow`, `Try PARROT`, `Authoring a domain pack`, `Registration`, `alert/__init__.py`, `export-design-preview.cjs`, `.embed_documents`, `test_ingest_pipeline.py`, `pipeline.py`, `registry.py`, `test_advice_module.py`, `FakeConn`, `test_a_grounding_corpus_travels_inside_its_pack`, `Alert`, `Due`, `contracts.py`, `build.py`, `WhoIsThis`, `GroundingCorpus`, `item-row.tsx`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `InstalledPack` (e.g. with `AdviceLog` and `AdviceRecord`) actually correct?**
  _`InstalledPack` has 58 INFERRED edges - model-reasoned connections that need verification._
- **Are the 38 inferred relationships involving `Passage` (e.g. with `AdviceLog` and `AdviceRecord`) actually correct?**
  _`Passage` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `ScriptedOllama` (e.g. with `Adviser` and `Consents`) actually correct?**
  _`ScriptedOllama` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `Settings` (e.g. with `Installed` and `RegisteredModule`) actually correct?**
  _`Settings` has 29 INFERRED edges - model-reasoned connections that need verification._