# Graph Report - igd-capstone-2026  (2026-09-14)

## Corpus Check
- 0 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2119 nodes · 3737 edges · 152 communities (134 shown, 18 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 239 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d0e1dadf`
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
- team/README.md
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
- add_person
- power-menu.tsx
- lock.ts
- checks.py
- build.py
- 5. The watched folder is polled for stability, not subscribed to for events
- The team
- Home Contents Insurance Policy
- api/__init__.py
- core/__init__.py
- runtime/__init__.py
- modules/__init__.py
- setup.sh
- 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module
- First run
- ModelUnavailable
- 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack
- vault/page.tsx
- Siew — task list
- WhoIsThis
- Settings
- vault.py
- dependencies
- household.py
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
- 1. Record architecture decisions
- 10. `main` is unprotected, and the discipline is human
- Cursor
- document-detail.tsx
- today/page.tsx
- 4. Local setup can run before the household assistant is ready
- scope_passages
- (app)/layout.tsx
- devDependencies
- Working agreement for coding agents
- FakeCursor
- app/page.tsx
- Desmond — Lane E · Corpus and adversarial testing
- build
- ingest/quarantine.py
- 2. One PostgreSQL instance for everything
- 12. Chunks follow the document's headings, and embeddings use the model's task prompts
- package.json
- postcss.config.mjs
- 13. A question is understood before it is searched, and scoped before it is cut
- github.md
- scripts
- capture.py
- Notebook prompts — the four full policies for Marcus Lim
- Christian — Lane A · Integration and product owner
- Siew — Lane C · Governance and assurance
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document

## God Nodes (most connected - your core abstractions)
1. `Settings` - 76 edges
2. `Ollama` - 49 edges
3. `ingest/quarantine.py` - 37 edges
4. `FakeOllama` - 30 edges
5. `FolderAdapter` - 30 edges
6. `extract()` - 29 edges
7. `ConfigurationError` - 26 edges
8. `create_app()` - 26 edges
9. `ModelUnavailable` - 25 edges
10. `connect()` - 25 edges

## Surprising Connections (you probably didn't know these)
- `warm_models()` --uses--> `ModelUnavailable`  [INFERRED]
  api/startup.py → core/runtime/ollama.py
- `create_app()` --uses--> `Settings`  [INFERRED]
  api/main.py → core/runtime/settings.py
- `main()` --uses--> `Settings`  [INFERRED]
  scripts/bench_runtime.py → core/runtime/settings.py
- `main()` --uses--> `Settings`  [INFERRED]
  scripts/load_corpus.py → core/runtime/settings.py
- `main()` --uses--> `Settings`  [INFERRED]
  scripts/quarantine.py → core/runtime/settings.py

## Import Cycles
- None detected.

## Communities (152 total, 18 thin omitted)

### Community 0 - "run_parrot.py"
Cohesion: 0.14
Nodes (18): broker_available(), Whether Redis answers. Not whether a worker is listening —…, main(), open_browser(), parse_args(), port_answers(), Run the engine, the folder watcher, the ingestion worker and the screens…, Whether something is listening on loopback. Not whether it is ours. (+10 more)

### Community 1 - "packs/page.tsx"
Cohesion: 0.11
Nodes (12): packs/page.tsx, dynamic, metadata, runtime, [id]/page.tsx, dynamic, metadata, runtime (+4 more)

### Community 2 - "Christian — task list"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 3 - "validate"
Cohesion: 0.09
Nodes (38): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), Validate a document register before it is handed over. python -m…, Parse `field_pages`: semicolon-separated `name=page`, 1-based. Empty means page… (+30 more)

### Community 4 - "4. Writing `pack.yaml`"
Cohesion: 0.16
Nodes (16): system/route.ts, ACTIONS, dynamic, GET(), POST(), runtime, sameOrigin(), unlocked() (+8 more)

### Community 5 - "Project PARROT — team split"
Cohesion: 0.29
Nodes (7): Everyone, regardless of lane, How the code gets written, Presentation split, Project PARROT — team split, Swap rules, The one process change that matters, Two rules for the corpus

### Community 6 - "Project PARROT — team split"
Cohesion: 0.29
Nodes (7): Everyone, regardless of lane, How the code gets written, Presentation split, Project PARROT — team split, Swap rules, The one process change that matters, The rule for the corpus

### Community 7 - "sha256"
Cohesion: 0.13
Nodes (17): CaptureAdapter, The one interface every capture channel satisfies. receive(payload, mime,…, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sha256(), adapters/__init__.py, Capture adapters. Every channel a document can arrive through satisfies one…, What every capture channel hands a document to. An adapter's job ends at "these… (+9 more)

### Community 8 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (11): running-the-eval-harness/SKILL.md, Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness (+3 more)

### Community 9 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 10 - "Desmond — task list"
Cohesion: 0.18
Nodes (11): Desmond — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 11 - "Zee — task list"
Cohesion: 0.20
Nodes (10): zee/tasks.md, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+2 more)

### Community 12 - "Yew Mun — task list"
Cohesion: 0.10
Nodes (20): yew-mun/README.md, Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation (+12 more)

### Community 13 - "Try PARROT"
Cohesion: 0.22
Nodes (9): 1 · Install five things, 2 · Download the AI models, 3 · Get the code and set it up, 4 · Put some documents in, 5 · Run it, If something goes wrong, Try PARROT, Want to work on it, not just try it? (+1 more)

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
Nodes (23): Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker. Celery is imported here rather…, FakeConnection, The queue, tested with no broker anywhere. What is worth asserting here is not…, The whole point. If `process` is reachable from the capture thread, nothing was…, The cheapest queue message is the one never sent, and the SHA-256 says these…, Eight seconds per document is what this change exists to remove. Five documents… (+15 more)

### Community 18 - "Zee — Lane D · Domain packs and interface"
Cohesion: 0.24
Nodes (18): FolderAdapter, Satisfies `CaptureAdapter`. Holds no database handle — it is given a…, FakeRegistrar, The watched folder: debounce, mime sniffing, and what happens the second time.…, Poll until the stability window has passed and something comes out., The `documents` table, reduced to the one thing it guarantees: sha256 is unique., _settle(), test_a_file_removed_before_it_settles_is_forgotten() (+10 more)

### Community 19 - "Authoring a domain pack"
Cohesion: 0.10
Nodes (26): ingest/extract.py, _coerce(), _date_renderings(), decode_schema(), _drop_format(), find_page(), _normalise(), _prepare() (+18 more)

### Community 20 - "Household canon"
Cohesion: 0.25
Nodes (7): Address, Employment, Household canon, Life events that documents must reflect, People, Policies, Vehicles

### Community 21 - "Registration"
Cohesion: 0.14
Nodes (13): FolderSettings, Dispatcher, Given a registered document, arrange for it to be read. Says what it arranged., Intake, An already-indexed document is not read again. Re-reading it would burn a…, FolderCapture, A daemon thread that polls the watched folder until `stop()` or process exit., Begin watching. Returns False, with a logged reason, when it cannot. (+5 more)

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
Cohesion: 0.19
Nodes (18): already_said(), True when this exact window has already been mentioned. The comparison is by…, Everything inside a lead window that has not already been said for that window.…, sweep(), obligation_row(), Reminder and Alert: what fires, once, and with what behind it. Both modules are…, A sweep for a date in the future must record that date, or it repeats itself., A pack naming a metric nobody implemented is a silent no-op, so it is caught… (+10 more)

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
Cohesion: 0.14
Nodes (11): IngestJob, Magic bytes first, filename suffix second, `application/octet-stream` last. A…, What a capture returns: a registered document, and whether we had seen it…, sniff_mime(), _Pending, The watched-folder capture adapter. A person drops a scan into a folder and it…, Every file in the watched folder that is worth looking at at all., Advance the debounce by `elapsed` seconds and return the files now ready. Time… (+3 more)

### Community 40 - "Notice"
Cohesion: 0.15
Nodes (18): parse(), The one call the pipeline makes. An unhandled mime type quarantines rather than…, document_title(), The document as a person would name it: its `string` fields as read, in the…, pgvector accepts its own text form; this avoids registering an adapter for one…, _vector_literal(), ingest/reindex.py, IndexedDocument (+10 more)

### Community 41 - "Changelog"
Cohesion: 0.50
Nodes (3): Changelog, W1 · 2–8 Sep 2026, W2 · 9–15 Sep 2026

### Community 42 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 43 - "`docs/governance/` — the assurance artefacts"
Cohesion: 0.50
Nodes (4): governance/README.md, `docs/governance/` — the assurance artefacts, The autonomy statement in one line, The rule that governs all eight

### Community 51 - "test_household.py"
Cohesion: 0.19
Nodes (17): is_first_person(), Whether this question is about the person asking. `other_names` are the display…, _conn_returning(), _passage(), Who is asking, and whose documents may answer. Two halves, deliberately split.…, The third bucket. Home contents, a utility bill — nobody's name on it,…, A joint policy is the owner's too. Presence wins over exclusion., Asked about my policy; the vault holds Rachel's. Say so, rather than answer… (+9 more)

### Community 52 - "The household, and the word "my""
Cohesion: 0.10
Nodes (20): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model (+12 more)

### Community 53 - "IngestJob"
Cohesion: 0.27
Nodes (7): create_app(), checks(), ready(), setup(), system_status(), test_liveness_is_independent_of_dependency_checks(), test_untrusted_host_is_rejected()

### Community 54 - "alert/__init__.py"
Cohesion: 0.26
Nodes (13): alert/__init__.py, _citations(), cpf_contributions_ytd(), days_uncovered(), donations_ytd(), Measurement, The Alert module: a pack-declared threshold, crossed once, citing the documents…, Days since cover lapsed, per insured person. Zero while a policy still runs. (+5 more)

### Community 55 - "find_page"
Cohesion: 0.40
Nodes (3): The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render()

### Community 56 - "TelegramAdapter"
Cohesion: 0.13
Nodes (12): _attachment(), The Telegram capture adapter. Same interface as the folder: `receive(payload,…, Confirm the token works before anything else is attempted., One `getUpdates` round. Returns what was captured; replies with what was…, Delete at source. A failure is logged, never raised: the document is already…, The largest photo, or the document. Telegram sends photos in several sizes., Keep the bytes where the quarantine retry can find them again., Satisfies `CaptureAdapter`. Holds no database handle — it is given a… (+4 more)

### Community 57 - "export-design-preview.cjs"
Cohesion: 0.11
Nodes (17): bundle(), classes, css, cssFile, domId, fs, ids, licences (+9 more)

### Community 58 - "cli.py"
Cohesion: 0.05
Nodes (74): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a…, paperbrain/ask.py, answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, paperbrain/chunk.py (+66 more)

### Community 59 - "owner"
Cohesion: 0.20
Nodes (11): owner(), owner_aliases(), The person asking. `None` before setup has run, which every caller must handle:…, Every confirmed string that means the owner. This is what scopes a first-person…, Hand the household over. The owner is a row, not a value baked in at install.…, set_owner(), A daughter takes over her father's paperwork. The install follows., A fresh install is not broken. It answers about the household, as it always… (+3 more)

### Community 60 - "tasks.py"
Cohesion: 0.11
Nodes (43): ingest/quarantine.py, blocked_reasons(), forget(), QuarantinedDocument, queue(), The second stage of quarantine: the page image, read by the vision-language…, Per document: `None` when the image pass can run, or the sentence saying why it…, Safe to show. Forgetting a document whose file is still there would not last. (+35 more)

### Community 61 - "test_pages.py"
Cohesion: 0.11
Nodes (32): page_images(), Base64 page images, in page order. Empty when this document cannot be rendered.…, page_count(), PageUnavailable, _pdfium(), One page of one document, as an image. Two callers want the same thing for…, Safe to show a person: there is no such page, or this file cannot be drawn., Safe to show a person: this install cannot render PDF pages at all. (+24 more)

### Community 62 - "test_ingest_pipeline.py"
Cohesion: 0.08
Nodes (41): Classification, classify(), _prompt(), Decide which pack's document type a captured document is, or decline to. The…, Never raises. An unavailable model is a classification failure, so it…, _schema(), extract(), Never raises. A failure is a reason, and a reason routes the document to… (+33 more)

### Community 63 - "bench_runtime.py"
Cohesion: 0.09
Nodes (32): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+24 more)

### Community 64 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 65 - "parse.py"
Cohesion: 0.10
Nodes (17): Block, DoclingParser, _pages_from(), Parser, PlainTextParser, Turn captured bytes into pages of text, or say why it could not be done. Every…, Docling, held at arm's length: imported on first use, and never at module…, Group Docling's items by the page they were found on. Docling's markdown export… (+9 more)

### Community 66 - "test_startup.py"
Cohesion: 0.08
Nodes (32): _kill_tree(), Stop a child and everything under it, then make sure it has gone., Start `npm run dev` in `web/`, or say plainly why it could not. Three reasons…, Stop the whole npm tree, not just the wrapper that was launched. This is the…, Stop the worker and the schedule it started, not just the launcher in front of…, start_web(), stop_web(), stop_worker() (+24 more)

### Community 67 - "pipeline.py"
Cohesion: 0.06
Nodes (35): DenseRetriever, NoReranker, A dense-only retriever, so the graph can be run and tested before Lane B's…, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this…, Chunk, What is actually embedded: the prefix plus the text, matching the tsvector…, Inline, What happens to a document between "these bytes are registered" and "this… (+27 more)

### Community 68 - "registry.py"
Cohesion: 0.09
Nodes (30): installed_modules(), InstalledModule, manifest(), ModuleUnavailable, Load the installed capability modules at runtime. The mirror of…, A module's YAML is missing, or does not validate against `ModuleManifest`., One module's manifest, validated. Raises rather than returning a partial object., Every module directory holding a `module.yaml`, in a stable order. Directories… (+22 more)

### Community 69 - "baseline.py"
Cohesion: 0.14
Nodes (8): A question, embedded the way the model was trained to embed a search query., Passages as `(title, text)`, embedded the way the model was trained to embed a…, Load the generator and the embedder now, and say where the generator landed. An…, Generate against a JSON schema. This is how extraction is held to a pack's…, The same constrained generation, yielded as it is written. Identical body to…, Whether this embedding model expects `QUERY_PROMPT` and `DOCUMENT_PROMPT`., One request for the whole batch. Returns vectors in the order given., uses_task_prompts()

### Community 70 - "team/README.md"
Cohesion: 0.29
Nodes (4): christian/README.md, christian/tasks.md, desmond/README.md, desmond/tasks.md

### Community 71 - "FakeConn"
Cohesion: 0.33
Nodes (9): Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), FakeConn, FakePack, test_a_firing_older_than_the_debounce_window_fires_again(), test_a_metric_no_query_defines_cannot_fire(), test_a_recent_firing_is_debounced(), test_a_threshold_crossing_fires_with_the_document_behind_it() (+1 more)

### Community 72 - "preview.tsx"
Cohesion: 0.11
Nodes (17): design-preview/page.tsx, metadata, answers, DesignPreview(), Direction, directions, Item, items (+9 more)

### Community 73 - "react"
Cohesion: 0.15
Nodes (10): react, household/page.tsx, dynamic, metadata, runtime, OwnerForm(), RELATION_CHOICES, Roster() (+2 more)

### Community 74 - "Starting Parrot"
Cohesion: 0.06
Nodes (28): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision, 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision (+20 more)

### Community 77 - "Notion"
Cohesion: 0.25
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 78 - "Alert"
Cohesion: 0.29
Nodes (4): Alert, _debounced(), What the debounce is keyed on: this metric, for this person, in this pack., test_the_debounce_key_separates_people()

### Community 79 - "The demonstration run sheet"
Cohesion: 0.14
Nodes (14): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+6 more)

### Community 80 - "PaperBrain"
Cohesion: 0.25
Nodes (8): paperbrain/README.md, How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 81 - "Contributing"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 82 - "unlock/page.tsx"
Cohesion: 0.29
Nodes (10): [...path]/route.ts, ALLOWED, Context, DELETE(), dynamic, forward(), GET(), PATCH() (+2 more)

### Community 83 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 85 - "ConfigurationError"
Cohesion: 0.11
Nodes (21): Safe to show: never contains the token., TelegramSettings, TelegramUnavailable, ConfigurationError, _folder(), local_url(), _port(), _positive() (+13 more)

### Community 86 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 87 - "Roadmap"
Cohesion: 0.29
Nodes (6): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap

### Community 88 - "add_person"
Cohesion: 0.20
Nodes (12): add_person(), confirm(), pending_count(), The person a printed name means, or `None` if nobody has confirmed what it…, Add somebody, with the names they are known by on paper already confirmed.…, A person answered the question. From here the alias scopes retrieval., resolve(), The sentence that makes a wrong model guess cost a tap instead of a wrong… (+4 more)

### Community 89 - "power-menu.tsx"
Cohesion: 0.14
Nodes (11): Action, CONFIRM, ITEMS, PowerMenu(), Stage, DependencyCheck, Phase, RestartingScreen() (+3 more)

### Community 90 - "lock.ts"
Cohesion: 0.16
Nodes (23): auth/route.ts, dynamic, GET(), grant(), POST(), runtime, Accepted, clearFailures() (+15 more)

### Community 91 - "checks.py"
Cohesion: 0.16
Nodes (21): The local API. Liveness is intentionally separate from assistant readiness.…, capture_check(), Check, collect_checks(), database_check(), interface_check(), model_check(), Read-only dependency diagnostics; installation is never treated as inference… (+13 more)

### Community 92 - "build.py"
Cohesion: 0.20
Nodes (15): _class_name(), _docstring(), _field_line(), load(), main(), Generate everything downstream of a pack.yaml. python -m packs.build #…, The header row Desmond fills in, one file per pack. Long format: one row per…, The header a batch register starts from: every field of every installed pack. A… (+7 more)

### Community 93 - "5. The watched folder is polled for stability, not subscribed to for events"
Cohesion: 0.33
Nodes (6): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, The five lanes

### Community 94 - "The team"
Cohesion: 0.33
Nodes (6): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, The five lanes

### Community 102 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 103 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 104 - "ModelUnavailable"
Cohesion: 0.33
Nodes (6): 6 · Use it, Ask — a question about your own documents, Packs — what this assistant knows about, Today — where it opens, Vault — everything it has filed, Without the screens

### Community 105 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 106 - "vault/page.tsx"
Cohesion: 0.18
Nodes (7): vault/page.tsx, dynamic, metadata, runtime, GoneRow(), QuarantineQueue(), QuarantineRow()

### Community 107 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 108 - "WhoIsThis"
Cohesion: 0.83
Nodes (4): WhoIsThis(), answer(), notOneOfUs(), somebodyNew()

### Community 109 - "Settings"
Cohesion: 0.11
Nodes (25): ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one…, Load the generator and the embedder before the first question, and record the…, warm_models(), conn(), database_url(), _ollama_answering(), Setup diagnostics use controlled service responses, never live household… (+17 more)

### Community 110 - "vault.py"
Cohesion: 0.07
Nodes (34): _columns(), correct(), Corrected, CorrectionRejected, A person fixing a field the extractor got wrong. This is the one place in the…, `(value_text, value_num, value_date)` — exactly one of them set. The declared…, Store what a person says this field actually says, and keep what it used to…, Safe to show: there is no fact with that id. (+26 more)

### Community 111 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 114 - "household.py"
Cohesion: 0.12
Nodes (22): attribute(), classify_prompt(), dismiss(), pending(), PendingAlias, Person, person_for_chat(), place() (+14 more)

### Community 117 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 118 - "test_lifecycle.py"
Cohesion: 0.11
Nodes (25): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor.…, What the person asked for, once. The first request wins; later ones change…, _client(), _eventually(), _launcher(), quiet_engine(), Restart and shut down: the engine asks its supervisor, and nothing else can ask… (+17 more)

### Community 120 - "app/layout.tsx"
Cohesion: 0.22
Nodes (8): next-themes, app/layout.tsx, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 122 - "item-row.tsx"
Cohesion: 0.31
Nodes (8): countdown(), detail(), figure(), ItemRow(), longDate(), sentence(), TONE, WORD

### Community 123 - "SentenceScanner"
Cohesion: 0.10
Nodes (27): Pulling finished sentences out of a JSON reply that is still being written. The…, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner, drip() (+19 more)

### Community 124 - "reminder/__init__.py"
Cohesion: 0.13
Nodes (18): reminder/__init__.py, close(), current_lead(), next_window(), Overdue, The Reminder module: a nightly sweep of obligations, and nothing fires twice.…, Past their date and never closed. A different problem from a reminder, shown…, Safe to show: there is no obligation with that id, or it is already closed. (+10 more)

### Community 125 - "Household canon"
Cohesion: 0.08
Nodes (24): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, Policies, The family tree, and why three of them are not called Lim (+16 more)

### Community 126 - "next"
Cohesion: 0.18
Nodes (7): @ai-sdk/react, next, ask/page.tsx, metadata, Conversation(), SUGGESTIONS, nextConfig

### Community 127 - "tokens/page.tsx"
Cohesion: 0.11
Nodes (11): Motion(), ROWS, tokens/page.tsx, INKS, metadata, RADII, SCALE, SECTIONS (+3 more)

### Community 129 - "1. Record architecture decisions"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 132 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 133 - "Cursor"
Cohesion: 0.13
Nodes (3): Cursor, test_reindexing_replaces_chunks_and_leaves_facts_alone(), cursor()

### Community 134 - "document-detail.tsx"
Cohesion: 0.39
Nodes (5): DocumentDetail(), when(), Field(), format(), isNumeric()

### Community 136 - "today/page.tsx"
Cohesion: 0.18
Nodes (7): today/page.tsx, dynamic, isUrgent(), metadata, runtime, summary(), TodayPage()

### Community 138 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 141 - "scope_passages"
Cohesion: 0.15
Nodes (15): HouseholdScope, Whose question is this, and whose documents may answer it. "What is my term…, `(word, relation)` when the question asks about a relation's own documents,…, The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting…, Keep the owner's passages and the household's; set aside everybody else's. A…, Keep the passages of these people and of the household; set aside everybody…, What `AnswerGraph` is handed so it can scope without holding a connection.… (+7 more)

### Community 143 - "(app)/layout.tsx"
Cohesion: 0.17
Nodes (13): lucide-react, (app)/layout.tsx, AppLayout(), dynamic, runtime, LockButton(), SURFACES, TabBar() (+5 more)

### Community 144 - "devDependencies"
Cohesion: 0.25
Nodes (8): devDependencies, postcss, tailwindcss, @tailwindcss/postcss, @types/node, @types/react, @types/react-dom, typescript

### Community 145 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents

### Community 149 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 150 - "build"
Cohesion: 0.24
Nodes (11): beat_schedule(), cron_expressions(), crontab_from(), manifest(), When the nightly sweeps run, read from the modules' own manifests. A module…, A five-field cron expression as Celery understands it., The cron line for each swept module, by module id. Testable without Celery…, Rule 6's habit: a schedule is written down in one place, and that place is the… (+3 more)

### Community 151 - "ingest/quarantine.py"
Cohesion: 0.14
Nodes (22): ingest/chunk.py, chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, One flat list of chunks, ordinal running across the whole document. (+14 more)

### Community 153 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 154 - "12. Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.33
Nodes (5): 12. Chunks follow the document's headings, and embeddings use the model's task prompts, Consequences, Context, Decision, Evidence

### Community 156 - "package.json"
Cohesion: 0.12
Nodes (15): ai, class-variance-authority, clsx, postcss, react-dom, tailwind-merge, tailwindcss, @tailwindcss/postcss (+7 more)

### Community 160 - "13. A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.33
Nodes (5): 13. A question is understood before it is searched, and scoped before it is cut, Consequences, Context, Decision, Evidence

### Community 162 - "github.md"
Cohesion: 0.50
Nodes (3): Last sync, Screen map, Updated in this project

### Community 163 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 165 - "capture.py"
Cohesion: 0.11
Nodes (28): lifespan(), indexed(), enabled_pack_ids(), enabled_packs(), install_best_effort(), Install at startup without being able to stop startup. Both processes that own…, The packs left switched on, or `None` when nothing has been installed yet.…, The installed packs a person has left switched on, as loaded pack objects. This… (+20 more)

### Community 166 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 176 - "Christian — Lane A · Integration and product owner"
Cohesion: 0.29
Nodes (7): Also yours, Christian — Lane A · Integration and product owner, Starter prompt for your coding agent, Starter prompt: what can I actually pick up?, The five things you ship, Week 1, in order, What integration actually means here

### Community 177 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.22
Nodes (9): siew/README.md, Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The autonomy statement, The six artefacts, Where governance touches the code (+1 more)

### Community 179 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

## Knowledge Gaps
- **560 isolated node(s):** `Context`, `Direction`, `Item`, `Outcome`, `Screen` (+555 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `checks.py` to `run_parrot.py`, `test_startup.py`, `pipeline.py`, `registry.py`, `capture.py`, `sha256`, `FolderAdapter`, `Settings`, `test_household.py`, `Registration`, `IngestJob`, `ConfigurationError`, `test_lifecycle.py`, `tasks.py`, `bench_runtime.py`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `Connection` connect `cli.py` to `Cursor`, `sha256`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `Ollama` connect `tasks.py` to `run_parrot.py`, `pipeline.py`, `capture.py`, `baseline.py`, `Settings`, `Authoring a domain pack`, `Registration`, `ConfigurationError`, `find_page`, `checks.py`, `test_ingest_pipeline.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 52 inferred relationships involving `Settings` (e.g. with `create_app()` and `install_best_effort()`) actually correct?**
  _`Settings` has 52 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Ollama` (e.g. with `warm_models()` and `DenseRetriever`) actually correct?**
  _`Ollama` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `FolderAdapter` (e.g. with `IngestJob` and `Registrar`) actually correct?**
  _`FolderAdapter` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Context`, `Direction`, `Item` to the rest of the system?**
  _560 weakly-connected nodes found - possible documentation gaps or missing edges._