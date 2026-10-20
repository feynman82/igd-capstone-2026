# Graph Report - igd-capstone-2026  (2026-10-20)

## Corpus Check
- 379 files · ~849,893 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 44 file(s) not represented in the graph (top: (none) 15, .jsonl 10, .csv 7)

## Summary
- 6473 nodes · 15120 edges · 367 communities (297 shown, 43 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 1161 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f9cf6bb4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- bands.py
- test_ingest_pipeline.py
- ScriptedOllama
- test_api.py
- validate
- advice/__init__.py
- Insurance and Coverage pack (insurance_agent)
- test_advice_module.py
- api.ts
- FakeOllama
- test_grounding_index.py
- test_grounding_values.py
- FolderAdapter
- test_telegram_capture.py
- test_corpus_files_match_the_register.py
- registry.py
- bench_runtime.py
- vault.py
- contracts.py
- schedule.py
- base.py
- scope.py
- reminder/__init__.py
- .load
- values.py
- SentenceScanner
- household.py
- test_answer_graph.py
- test_calendar.py
- headline.py
- test_household.py
- score_obligations
- test_pages.py
- FakeConn
- test_hybrid.py
- modules/__init__.py
- test_reindexing_replaces_chunks_and_leaves_facts_alone
- HouseholdScope
- tasks.py
- alert/__init__.py
- retrieve.py
- eval/modules.py
- extract_values
- answer.tsx
- main
- test_eval_headline.py
- support.js
- build_router
- main
- compilerOptions
- Domain packs — start here
- checks.py
- test_grounding.py
- _calendar
- cli.py
- .constrained
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- Any
- Any
- test_tax_pack.py
- review_grounding_values.py
- PARROT mid-term: talking script
- lock.ts
- test_eval_modules.py
- routes.py
- PARROT Interface Design Pack
- export-design-preview.cjs
- The Four Surfaces
- answer.py
- advice-consent.tsx
- HouseholdCalendar
- test_graph_labels.py
- Policies
- .__init__
- ADR 0011: The household is people and aliases, and the owner is one of them
- test_gate.py
- sse
- today/page.tsx
- test_lifecycle.py
- preview.tsx
- User stories and acceptance criteria
- Hash-based idempotency
- entry-dialog.tsx
- pytest
- tokens/page.tsx
- Ollama
- core/calendar.py
- advice-card.tsx
- components.json
- ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic
- Settings
- FakeCursor
- Domain pack
- report.py
- The Lim Household, Tampines
- Starting Parrot
- Lane C - Governance and assurance
- Period
- Core Document Catalogue (ADR 0017)
- Notebook prompts — the four full policies for Marcus Lim
- 2. One PostgreSQL instance for everything
- PARROT Architecture Review
- Data inventory: identity data, DOBs and loans
- TelegramCapture
- The autonomy statement
- web/ - the PARROT interface
- The document register as ground truth
- ingest.py
- _as_module_summary
- Reminder, Alert and Tracker Registers
- Banded Abstention Evaluation Implementation Plan
- example_pack template manifest
- paperbrain/extract.py
- §5 · Evaluation and results
- Financial advisory process
- Try PARROT
- test_eval_holdout.py
- api/__init__.py
- AdviceShape
- Any
- test_worker_queue.py
- Retention and erasure policy
- corpus_files
- The deliberately naive retrieval baseline
- Running the evaluation harness
- test_contracts.py
- The five-lane split (five people, nine weeks, three builders)
- A field name is written down once
- The demonstration run sheet
- CalendarEventIn
- Filling the corpus register
- Writing a governance artefact
- ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts
- Working agreement for coding agents
- igd-capstone-2026
- Policy schedule HTML template
- test_startup.py
- household/page.tsx
- PaperBrain
- ADR 0013: A question is understood before it is searched, and scoped before it is cut
- test_rerank.py
- _as_consent
- Model card — PARROT v1
- 7. The answer graph ships before hybrid retrieval and before a checkpoint table
- Set C: adversarial
- Policy Schedule Template
- alert module manifest
- Aim Headline Metrics Implementation Plan
- ConfigurationError
- Consent and redaction protocol: the real-document holdout
- Household canon
- Authoring a domain pack
- test_modules.py
- Every Fact Row Cites Its Source
- DesignPreview evaluation harness
- main
- score.py
- Siew — Lane C · Governance and assurance
- Writing an ADR
- dependencies
- test_eval_ranked.py
- typing
- test_eval_harness.py
- ._claim
- Evaluation
- .__post_init__
- _git_sha
- lucide-react
- Banded abstention: an evaluation model beside the fixed floor
- build.py
- 19 · A relevance floor on the reranker does not buy abstention, and the reason is not calibration
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- pipeline.py
- reading_order
- _pages_from
- filesystem
- draft
- advice_consent.py
- Project PARROT — team split
- Basic Financial Planning Guide
- no_weights
- answer
- One Database
- What to ask before buying life insurance
- ._handle
- 2. Amended Gemini Prompts Bank (Xinkapow Yellow/Orange Cards with KFC Mascot)
- runtime/__init__.py
- corpus/__init__.py
- packs/__init__.py
- Lane E - Corpus and adversarial testing
- No code generates corpus documents
- §4.3–4.4 · Packs and the interface, with the expansion model
- Provenance register for corpus sg_protection_guidance
- setup.sh
- session-start.sh
- package.json
- Tax and Reliefs pack (iras_tax)
- postcss.config.mjs
- Lane C - Governance and assurance
- parrot
- Vertical slices, not layers
- Real organisations may be named
- ModuleManifest
- _read
- FakeConn
- Comparison of Integrated Shield Plans
- Christian — task list
- Desmond — Lane E · Corpus and adversarial testing
- Desmond — task list
- Siew — task list
- Yew Mun — task list
- Graphify — the shared knowledge graph
- First run
- Understanding health insurance
- test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them
- 20 · The household calendar lives in Postgres, answers by code, and Parrot only ever drafts an entry
- RecordingConn
- Zee — Lane D · Domain packs and interface
- Zee — task list
- build_team_tasks.py
- PrivateCare Policy Wording Template
- FakeCursor
- Integration review
- Contributing
- The corpus
- AdviceRecord
- 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack
- 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent
- NNNN · The decision, as a statement not a question
- Notion
- Premium and Subsidy Tables
- Understanding integrated shield plans
- Christian — Lane A · Integration and product owner
- Yew Mun — Lane B · Retrieval and evaluation
- Architecture
- Claude Code — read this first
- 10. `main` is unprotected, and the discipline is human
- Third-party material the system indexes, and on what basis
- 14 · A pack supplies what the core knows about a domain, and the core stays generic
- 17 · A pack is grounding and persona; the core owns documents
- Artefacts
- Why the prototype is evaluated on synthetic data
- About Integrated Shield Plan
- The team
- freeze.py
- `core/graph/` — the LangGraph runtime
- Headline metrics that measure the aims, not the targets
- _page_of_examples
- 6. pypdfium2 renders the page images the quarantine second pass reads
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- adr/README.md
- Data inventory — identity data, dates of birth and loans
- Notice
- telegram.py
- `core/ingest/` — the ingestion worker
- `core/retrieve/` — hybrid retrieval
- START.cmd launcher
- The nine, one at a time
- Getting Parrot ready (startup readiness screen)
- Authoring a domain pack
- 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module
- `docs/governance/` — the assurance artefacts
- InstalledPack
- `core/adapters/` — capture adapters
- Home Contents Insurance Policy
- The pack catalogue
- Tax and Reliefs — contract changes this pack needs
- HouseholdInventory
- IMDA frameworks: what applies to PARROT
- sets/README.md
- Pack grounding corpus rules
- phrasings.py
- Contracts and Migrations Are Their Own PR
- ADR 0002 - One PostgreSQL instance for everything
- ._categories_read_a_declared_field
- test_eval_generate.py
- Scoped
- TelegramSettings
- Autonomy statement — PARROT v1
- eval/__init__.py
- §7.4 · Commercialisation roadmap
- Terms of use
- The five lanes
- Incident and data breach procedure
- `docs/report/` — the final report
- gate.py
- classify
- ISO/IEC 22989 stages and ISO/IEC 5338 processes: what PARROT actually does
- test_eval_freeze.py
- 13. A question is understood before it is searched, and scoped before it is cut
- 1. Record architecture decisions
- 4. Local setup can run before the household assistant is ready
- FakeCursor
- test_advice_core.py
- grounding/__init__.py
- core/__init__.py
- worker/__init__.py
- Incident log
- 5. The watched folder is polled for stability, not subscribed to for events
- is_first_person
- redis
- redis_exceptions
- .feed
- Alert
- PackUnavailable
- 15. A name scopes a question, and a grandparent is not a parent
- generate_lim_documents.py
- test_a_core_document_stays_enabled_when_every_pack_is_off
- .observe
- installed_packs
- main
- pathlib
- DoclingParser
- test_a_household_that_cannot_be_true_is_refused
- AnswerGraph
- .ask
- Asks
- usable
- Quarantine and the vision second pass
- conn
- Due
- quiet_engine
- .days
- _dual_cited_calculation
- _meets_calculation
- _shared_value_calculation
- test_an_unscoped_result_is_not_empty_for_the_owner
- test_the_catalogue_declares_metrics_that_exist
- date
- Decimal
- Exception
- fixture
- Generated
- parametrize
- The final ILP report
- Adversarial testing from week 7
- Two-stage quarantine with a vision-language second pass
- Nobody edits core/contracts.py in a feature pull request

## God Nodes (most connected - your core abstractions)
1. `Settings` - 203 edges
2. `Passage` - 103 edges
3. `ScriptedOllama` - 99 edges
4. `InstalledPack` - 92 edges
5. `AnswerGraph` - 87 edges
6. `build_router()` - 82 edges
7. `FakeConn` - 75 edges
8. `Ollama` - 75 edges
9. `settings()` - 75 edges
10. `client_for()` - 74 edges

## Surprising Connections (you probably didn't know these)
- `Phase 3 — Reminders` --semantically_similar_to--> `Rachel - Reminder module on Today`  [INFERRED] [semantically similar]
  tools/paperbrain/docs/ROADMAP.md → web/docs/user-stories.md
- `PaperBrain` --semantically_similar_to--> `Lane A - Integration and product`  [INFERRED] [semantically similar]
  tools/paperbrain/README.md → team/christian/README.md
- `Ingestion worker with idempotent upsert` --semantically_similar_to--> `Hash-based idempotency`  [INFERRED] [semantically similar]
  team/christian/README.md → tools/paperbrain/docs/ARCHITECTURE.md
- `Two-stage quarantine with a vision-language second pass` --semantically_similar_to--> `OCR is per page, not per file`  [INFERRED] [semantically similar]
  team/christian/README.md → tools/paperbrain/docs/ARCHITECTURE.md
- `next dev binds every interface, not loopback` --semantically_similar_to--> `Ports published on 127.0.0.1 only`  [INFERRED] [semantically similar]
  docs/governance/data-inventory.md → infra/docker-compose.yml

## Import Cycles
- 3-file cycle: `eval/bands.py -> eval/run.py -> eval/headline.py -> eval/bands.py`

## Communities (367 total, 43 thin omitted)

### Community 0 - "bands.py"
Cohesion: 0.05
Nodes (109): Axis, Band, EdgesFor, as_json(), axis_summary(), banded(), by_pack(), _cell() (+101 more)

### Community 1 - "test_ingest_pipeline.py"
Cohesion: 0.08
Nodes (31): _date_renderings(), find_page(), The first page whose text contains this value. None means no page supports it.…, Every common way a household document prints this date, given it as YYYY-MM-DD.…, fixture, parametrize, insurance(), iras() (+23 more)

### Community 2 - "ScriptedOllama"
Cohesion: 0.06
Nodes (69): AdviceCard, AdviceWithheld, ConsentRequired, Finished, Everything that is only knowable once the last sentence is in. `quarantined`…, Advice was asked for and the owner has not agreed to this pack's current…, Advice could not be worked out, and `missing` says what it needs, in the pack's…, A worked result, every word of it written by code, given before the model says… (+61 more)

### Community 3 - "test_api.py"
Cohesion: 0.07
Nodes (44): advising(), client(), conn(), FakeGraph, graph(), _padded(), fixture, MonkeyPatch (+36 more)

### Community 4 - "validate"
Cohesion: 0.09
Nodes (40): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+32 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.08
Nodes (72): Figure, Input, One fact or rule value a calculation was built on, carrying its own citation.…, One number a calculator produced, and the words a sentence must use to state…, _Value, Hashable, _ambiguous(), _amount() (+64 more)

### Community 6 - "Insurance and Coverage pack (insurance_agent)"
Cohesion: 0.16
Nodes (16): Insurance advice consent gate (consent_version 1.0.0), advice_decline guardrail message, Category matcher (printed product_name against asked words, first rule wins), Advice shape ci_cover (gap calculator), Category critical_illness (critical illness plan), Advice shape death_tpd_cover (gap calculator), Exclusion detection (headings, claims, negations), insurance_agent guardrails (must_cite, abstain_below 0.45, never_acts, verdict_by_code) (+8 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.14
Nodes (55): Calculation, Missing, What a calculator returns when every fact and rule it needed was on file and…, What a calculator returns when a fact or a rule value it needed was not there…, calculate(), assert_nothing_negative(), basis(), fact() (+47 more)

### Community 8 - "api.ts"
Cohesion: 0.04
Nodes (65): ADR-0017, react, dynamic, metadata, PacksPage(), runtime, DocumentPage(), dynamic (+57 more)

### Community 9 - "FakeOllama"
Cohesion: 0.10
Nodes (39): Catalog, extract(), Never raises. A failure is a reason, and a reason routes the document to…, Exception, Generated, Ollama, FakeOllama, Any (+31 more)

### Community 10 - "test_grounding_index.py"
Cohesion: 0.09
Nodes (43): GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records…, SourceText, index_pack(), IndexReport, Any, date, Path (+35 more)

### Community 11 - "test_grounding_values.py"
Cohesion: 0.18
Nodes (31): _dropped(), _log_values(), fixture, LogCaptureFixture, parametrize, Published values: the model reads a source, and code keeps only what the…, Assert a value was dropped, and logged with this reason., _run() (+23 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.15
Nodes (25): FolderAdapter, FolderSettings, Satisfies `CaptureAdapter`. Holds no database handle — it is given a…, FolderCapture, Begin watching. Returns False, with a logged reason, when it cannot., A daemon thread that polls the watched folder until `stop()` or process exit., FakeRegistrar, datetime (+17 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.12
Nodes (35): MockTransport, build(), FakeTelegram, photo_update(), Any, LogCaptureFixture, Path, Telegram capture: what arrives, what is answered, and what is written where. No… (+27 more)

### Community 14 - "test_corpus_files_match_the_register.py"
Cohesion: 0.29
Nodes (9): Path, A document file promises something by its name. This checks the promise is…, Committed document files under the folders a corpus document lives in., The promise rule 2 makes. A file called `b2-0021.pdf` says "I am register row…, Specimens named for what they are. A choice, not a defect — but a silent one,…, _register_ids(), test_a_file_named_like_a_register_row_has_one(), test_documents_that_claim_no_register_row_are_counted_not_hidden() (+1 more)

### Community 15 - "registry.py"
Cohesion: 0.13
Nodes (26): installed_modules(), Every module directory holding a `module.yaml`, in a stable order. Directories…, enabled_module_ids(), install(), Installed, _module_row(), modules(), _pack_row() (+18 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (36): platform, BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib() (+28 more)

### Community 17 - "vault.py"
Cohesion: 0.06
Nodes (39): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+31 more)

### Community 18 - "contracts.py"
Cohesion: 0.07
Nodes (41): Advice, AlertConfig, Answering, DocumentTypeSpec, ExplainStep, FieldSpec, Grounding, Guardrails (+33 more)

### Community 19 - "schedule.py"
Cohesion: 0.15
Nodes (17): build(), Any, The one Celery application, built from `Settings`. Every setting here is a…, Construct the Celery application. Imported lazily by callers so that nothing…, beat_schedule(), cron_expressions(), crontab_from(), manifest() (+9 more)

### Community 20 - "base.py"
Cohesion: 0.11
Nodes (22): CaptureAdapter, IngestJob, datetime, Protocol, The one interface every capture channel satisfies. receive(payload, mime,…, The body of every adapter's `receive`: register the bytes, and say what that…, Magic bytes first, filename suffix second, `application/octet-stream` last. A…, What a capture returns: a registered document, and whether we had seen it… (+14 more)

### Community 21 - "scope.py"
Cohesion: 0.18
Nodes (21): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Any (+13 more)

### Community 22 - "reminder/__init__.py"
Cohesion: 0.11
Nodes (24): already_said(), close(), current_lead(), next_window(), Overdue, Any, date, datetime (+16 more)

### Community 23 - ".load"
Cohesion: 0.09
Nodes (39): create_app(), checks(), lifespan(), ready(), setup(), system_status(), ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one… (+31 more)

### Community 24 - "values.py"
Cohesion: 0.07
Nodes (34): _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), number_tokens(), _pack(), parse_value() (+26 more)

### Community 25 - "SentenceScanner"
Cohesion: 0.14
Nodes (24): What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, SentenceScanner, drip(), parametrize, The scanner that decides when a streamed sentence is finished. Everything the…, A model that stops halfway has still said the sentences it finished, and they…, Feed `text` in `size`-character pieces, the way a model actually arrives. (+16 more)

### Community 26 - "household.py"
Cohesion: 0.08
Nodes (45): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+37 more)

### Community 27 - "test_answer_graph.py"
Cohesion: 0.04
Nodes (68): Abstained, _numbered(), _pack_for(), The implementation. Yields each sentence once it has passed the gate, never…, The pack that speaks for the best-scoring passage's document type, or None for…, "Who is Sarah Tan Li Ling?" A name that is nobody in the household, though it…, One wording for "who is your son?", shared by explaining and advising so they…, Refused (+60 more)

### Community 28 - "test_calendar.py"
Cohesion: 0.12
Nodes (32): wants_entry(), fastapi_testclient, api(), db(), event(), Any, date, fixture (+24 more)

### Community 29 - "headline.py"
Cohesion: 0.08
Nodes (45): delta(), The movement, in questions first. One question is the set's step, so it is a…, all_questions(), as_json(), _cell(), change(), Claim, claims_in() (+37 more)

### Community 30 - "test_household.py"
Cohesion: 0.09
Nodes (44): _household_scope(), MonkeyPatch, Person, Who is asking, and whose documents may answer. Two halves, deliberately split.…, `HouseholdScope` over a roster held in memory, with every document resolved by…, The roster has no grandparent relation, so the household says it the only way…, 13 September: "what is Marcus's premium?" has no "my", so nothing was scoped…, 19 October, Set C c-c08: "my brother's car insurance" was a someone-else word… (+36 more)

### Community 31 - "score_obligations"
Cohesion: 0.11
Nodes (24): Obligation, obligation_precision(), A passport prints RACHEL NG HUI SHAN and the register writes Rachel Ng Hui…, One verdict per obligation. `declared` is the catalogue's `registers.reminder`…, Metric 7, over the obligations a document produced. A calendar deadline is…, One `obligations` row, with the fact and document it was created from., What the register says about one obligation. `verdict` is the bucket it counts…, _same_person() (+16 more)

### Community 32 - "test_pages.py"
Cohesion: 0.09
Nodes (37): base64, page_count(), PageUnavailable, _pdfium(), Any, LookupError, RuntimeError, One page of one document, as an image. Two callers want the same thing for… (+29 more)

### Community 33 - "FakeConn"
Cohesion: 0.10
Nodes (41): FakeConn, obligation(), open_obligation(), overdue_row(), date, Snooze means 'not until this gets more urgent', so it can name the day it does., No new column: `already_said` is what makes the row quiet, and it reads this…, One row of `reminder.OVERDUE`, in its column order. (+33 more)

### Community 34 - "test_hybrid.py"
Cohesion: 0.11
Nodes (21): hybrid_score(), identifiers(), prints(), The tokens in a question that look like something printed rather than said: a…, Whether the chunk prints the identifier, ignoring case and the spacing inside…, The cosine similarity, lifted to `IDENTIFIER_HIT` when the chunk prints an…, FakeConn, FakeCursor (+13 more)

### Community 37 - "HouseholdScope"
Cohesion: 0.18
Nodes (16): HouseholdScope, Keep the passages of these people and of the household; set aside everybody…, What `AnswerGraph` is handed so it can scope without holding a connection.…, scope_to(), _conn_returning(), _passage(), The third bucket. Home contents, a utility bill — nobody's name on it,…, A joint policy is the owner's too. Presence wins over exclusion. (+8 more)

### Community 39 - "tasks.py"
Cohesion: 0.06
Nodes (69): blocked_reasons(), forget(), page_images(), Any, Path, ValueError, QuarantinedDocument, queue() (+61 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.18
Nodes (19): days_uncovered(), _debounced(), Measurement, _per_subject(), Any, date, datetime, Decimal (+11 more)

### Community 41 - "retrieve.py"
Cohesion: 0.18
Nodes (18): ndarray, numpy, sqlite3, load_matrix(), pack(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.…, Return (N x D matrix of normalised embeddings, chunk ids)., unpack() (+10 more)

### Community 42 - "eval/modules.py"
Cohesion: 0.13
Nodes (30): _day(), main(), measure(), Measured, _number(), obligations(), obligations_possible(), _paragraph() (+22 more)

### Community 43 - "extract_values"
Cohesion: 0.17
Nodes (20): extract_values(), _prompt(), Every value the source prints for these keys, kept only when its passage prints…, _long_text(), Any, Exception, Generated, Returns the replies the test wrote, in order, then an empty list of values. A… (+12 more)

### Community 44 - "answer.tsx"
Cohesion: 0.07
Nodes (30): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+22 more)

### Community 45 - "main"
Cohesion: 0.24
Nodes (11): _beat_needs_its_own_process(), celery_argv(), main(), Any, Namespace, Popen, The arguments the Celery command-line would have been given. Built here so a…, Celery refuses `worker --beat` on Windows — "-B option does not work on… (+3 more)

### Community 46 - "test_eval_headline.py"
Cohesion: 0.13
Nodes (47): Count, A rate that remembers its question count, because on sets this small one…, Expected, _adversarial(), _compute(), _fact(), _hard(), _line() (+39 more)

### Community 47 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 48 - "build_router"
Cohesion: 0.07
Nodes (43): CorrectionResponse, DeletedEvent, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, QuarantinedDocument, QuarantineResponse (+35 more)

### Community 49 - "main"
Cohesion: 0.05
Nodes (53): What the vault now holds, checked against the manifest and the committed…, verify(), _chosen(), _counts(), _facts(), _fixture_guards(), _floor_fields(), _indexed() (+45 more)

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 51 - "Domain packs — start here"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 52 - "checks.py"
Cohesion: 0.08
Nodes (38): The local API. Liveness is intentionally separate from assistant readiness.…, AsyncClient, asyncio, contextlib, device_name(), load(), Any, The tokenizer, the model and the device it sits on, loaded once per process.… (+30 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.18
Nodes (24): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError, Read and validate a pack's grounding corpus from its own folder on disk. A…, A pack's grounding corpus on disk does not match what its `sources.yaml`… (+16 more)

### Community 54 - "_calendar"
Cohesion: 0.12
Nodes (24): A document and a page, as a person would cite it — or, for published guidance,…, Source, _answer_events(), get_calendar(), today(), _calendar(), _cite(), connection() (+16 more)

### Community 55 - "cli.py"
Cohesion: 0.17
Nodes (22): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+14 more)

### Community 56 - ".constrained"
Cohesion: 0.11
Nodes (12): Any, Client, A question, embedded the way the model was trained to embed a search query., Passages as `(title, text)`, embedded the way the model was trained to embed a…, Load the generator and the embedder now, and say where the generator landed. An…, Generate against a JSON schema. This is how extraction is held to a pack's…, The one request body both constrained calls send. See `constrained_stream`., The same constrained generation, yielded as it is written. The same body as… (+4 more)

### Community 57 - "ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.16
Nodes (20): ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, The adult rule: advice is withheld for a person under 21 or a child with no date of birth on file, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel), Advice graph flow: shape match, subject resolution, consent, AdviceCard, explain, advice_records keeps each answer's full basis, PackManifest.advice shapes (gap, remaining_room, keep_or_surrender, compare_own, compare_market, estimate_saving), Advice.review: one question runs every shape at once (+12 more)

### Community 58 - "Any"
Cohesion: 0.12
Nodes (7): ConsentCursor, Fails, FakeCursor, Any, The parameters of the one statement containing `needle`. Fails loudly if it…, Yields `before`, then raises. `ask` raises at once., Remembers what `grant` or `withdraw` inserted, so the next read of the latest…

### Community 59 - "Any"
Cohesion: 0.11
Nodes (22): advised_pack(), _document(), _facts_tuple(), FakeConn, FakeCursor, Any, date, datetime (+14 more)

### Community 60 - "test_tax_pack.py"
Cohesion: 0.20
Nodes (16): _basis(), _latest(), _matched(), _published(), FactRow, parametrize, The tax pack's advice, run on batch 1's own SRS statements and Notices of…, The shape id the answer graph picks for a question with both packs enabled,… (+8 more)

### Community 61 - "review_grounding_values.py"
Cohesion: 0.15
Nodes (21): approve(), pending(), PendingValue, Any, date, A person's approval, standing between a model's extraction and any calculator…, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it. (+13 more)

### Community 62 - "PARROT mid-term: talking script"
Cohesion: 0.10
Nodes (20): 01 · Christian, 02 · Christian, 03 · Christian, 04 · Christian, 05 · Christian, 06 · Christian, 07 · Zee, 08 · Zee (+12 more)

### Community 63 - "lock.ts"
Cohesion: 0.07
Nodes (48): ref_node_crypto, dynamic, GET(), grant(), POST(), runtime, ALLOWED, Context (+40 more)

### Community 64 - "test_eval_modules.py"
Cohesion: 0.10
Nodes (26): alert_fpr(), AlertVerdict, _mark(), ModuleMetrics, One verdict per fired alert: whether the register, recomputed, crosses the same…, Metric 8. `None` when nothing fired: a rate over zero alerts is not 0.0, it is…, What `eval.run` puts in a result file, and what the W7 report prints., The detail that goes beside the two numbers, so a run file explains its own… (+18 more)

### Community 65 - "routes.py"
Cohesion: 0.07
Nodes (67): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, AskRequest, AskResponse, CalendarEntry, CalendarPerson (+59 more)

### Community 66 - "PARROT Interface Design Pack"
Cohesion: 0.12
Nodes (21): Capture is where the user already is, Citation chips are the trust surface, Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Nothing moves without a reason (motion specification), Suggestions come from this week's ingest, The home screen is not a text box, Civic Register: order, clarity and institutional confidence (+13 more)

### Community 67 - "export-design-preview.cjs"
Cohesion: 0.08
Nodes (23): @eslint/eslintrc, ref_node_fs, ref_node_path, ref_node_url, compat, eslintConfig, bundle(), classes (+15 more)

### Community 68 - "The Four Surfaces"
Cohesion: 0.10
Nodes (20): Packs and Modules May Not Import web/ or api/, `api/` — the FastAPI application, The FastAPI Application, Five properties worth knowing before you change anything, Rules, The surface, GET /api/today Never Marks Anything Notified, apply (+12 more)

### Community 69 - "answer.py"
Cohesion: 0.05
Nodes (66): Categories, Category, A kind of document a household holds, recognised by words printed in its name.…, kind_of(), `"fact:12"` -> `"fact"`, `"rule:7"` -> `"rule"`. Anything else is a calculator…, _asked(), _calendar_citation(), _conversation() (+58 more)

### Community 70 - "advice-consent.tsx"
Cohesion: 0.15
Nodes (19): AdviceNote(), Consent, ConsentPrompt(), agree(), settle(), State, ADR-0016, AdviceConsentSection() (+11 more)

### Community 71 - "HouseholdCalendar"
Cohesion: 0.18
Nodes (10): ask(), ask_stream(), _graph_for(), _history(), The conversation so far, as the graph reads it. Empty for a first question., HouseholdAdviceLog, `core.graph.advice.AdviceLog` over a live connection. `basis` is dumped with…, HouseholdCalendar (+2 more)

### Community 72 - "test_graph_labels.py"
Cohesion: 0.15
Nodes (21): labelled_lines(), The `label: value` lines, from the document passages a sentence cites, whose…, Generated, Failing, Judge, _page(), Any, Generated (+13 more)

### Community 73 - "Policies"
Cohesion: 0.10
Nodes (22): never_acts: True in Every Pack Manifest, No New Runtime Dependency Without an ADR, Never Generate SQL at Runtime, The Core Answering Layer, The Answer Path: route, retrieve, rerank, ground, answer or abstain, baseline.py Is Disposable and Never a Measurement, The Grounding Gate, ports.py, the Seam With Lane B (+14 more)

### Community 74 - ".__init__"
Cohesion: 0.20
Nodes (9): ConsentBook, Implemented by `HouseholdConsents` in `core/advice_consent.py`., The granting row's id, or `None` when the owner has not granted this exact…, The answer graph. Router, retrieve, rerank, grounding gate, then answer or…, Protocol, Implemented by `core/retrieve/` when Lane B's hybrid search lands. `candidates`…, A cross-encoder, scoring question against passage. Returns the best `keep`,…, Reranker (+1 more)

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.16
Nodes (20): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), The owner is a row, not a config value baked at install, people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), A resolved person is shown as a chip, like a citation, The roster is derived from documents, then confirmed (+12 more)

### Community 76 - "test_gate.py"
Cohesion: 0.13
Nodes (33): check_advice(), check_one(), Claim, Why an advice explanation cannot be kept, or `None`. Asked of a claim built…, Why this one sentence cannot be kept, or `None` if it can. Depends on nothing…, test_a_sentence_citing_a_passage_that_was_never_retrieved_is_dropped(), test_a_sentence_with_no_supporting_passage_is_dropped(), What the gate checks beyond "is there a citation". A cited sentence can still… (+25 more)

### Community 77 - "sse"
Cohesion: 0.09
Nodes (33): Citation, A passage, named the way a person cites it and identified the way a link needs.…, a_citation(), advice_card(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive…, No `reading` before it: the floor is checked before the model is asked anything. (+25 more)

### Community 78 - "today/page.tsx"
Cohesion: 0.11
Nodes (31): CalendarPage(), dynamic, metadata, runtime, ADR-0020, dynamic, isUrgent(), metadata (+23 more)

### Community 79 - "test_lifecycle.py"
Cohesion: 0.14
Nodes (25): Lifecycle, What the person asked for, once. The first request wins; later ones change…, _client(), _eventually(), _launcher(), parametrize, Path, TestClient (+17 more)

### Community 80 - "preview.tsx"
Cohesion: 0.10
Nodes (17): metadata, answers, DesignPreview(), Direction, directions, Item, items, web_app_design_preview_preview_module (+9 more)

### Community 81 - "User stories and acceptance criteria"
Cohesion: 0.14
Nodes (12): 1. How to read a criterion, 2. Rachel · Reminder module · Today, 3. Marcus · retrieval core · Ask, 4. Marcus and Rachel · capture · Vault, 5. Marcus · Alert module · Today, 6. The household ledger · Tracker · specification only, 7. Open questions for review, 8. The criteria as a checklist (+4 more)

### Community 82 - "Hash-based idempotency"
Cohesion: 0.25
Nodes (8): PaperBrain handled failure modes, Hash-based idempotency, OCR is per page, not per file, SQLite for everything, Vectors as BLOBs, scored in numpy, Exhaustive cosine instead of an ANN index, The pb command line, PaperBrain dependency set

### Community 83 - "entry-dialog.tsx"
Cohesion: 0.16
Nodes (17): DraftCard(), add(), change(), ADR-0020, EntryDialog(), remove(), save(), EntryDraft (+9 more)

### Community 84 - "pytest"
Cohesion: 0.14
Nodes (17): FixtureRequest, Image, needs_ocr, pytest, _as_printed(), page_pixels(), photographed(), fixture (+9 more)

### Community 85 - "tokens/page.tsx"
Cohesion: 0.11
Nodes (10): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+2 more)

### Community 86 - "Ollama"
Cohesion: 0.17
Nodes (10): answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, Ollama, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.…, Batch embeddings. Falls back to the legacy endpoint on old servers., Hit (+2 more)

### Community 87 - "core/calendar.py"
Cohesion: 0.15
Nodes (27): between(), clock(), create(), delete(), Event, EventFields, events_between(), expand() (+19 more)

### Community 88 - "advice-card.tsx"
Cohesion: 0.09
Nodes (24): Advice, AdviceCard(), AdviceWithheld(), capitalise(), sentence(), TONES, ADR-0016, VERDICT_TONE (+16 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.16
Nodes (19): Code-written absence sentence: 'None of the N policies on file is a dental plan.', ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic, The advise route intent returns the pack's advice_decline, answering.categories: ordered whole-word rules over one printed field, Category filter applied before the keep-6 cut, answering.exclusions: headings under which a cover claim is not believed, Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration) (+11 more)

### Community 91 - "Settings"
Cohesion: 0.09
Nodes (50): Whether Telegram capture should start. An unset token means "not this…, Settings, client_for(), consent(), ConsentConn, filed_document(), inbox(), pack_row() (+42 more)

### Community 92 - "FakeCursor"
Cohesion: 0.18
Nodes (3): FakeCursor, Any, FakeConn

### Community 93 - "Domain pack"
Cohesion: 0.15
Nodes (17): Step 8 - switch a pack off, Step 7 - the refusal to act, Exactly one owner, enforced by the database, facts.subject is never normalised, people and person_aliases, 4. Writing `pack.yaml`, Descriptions are prompts, Document types (+9 more)

### Community 94 - "report.py"
Cohesion: 0.06
Nodes (63): Any, Extraction against the holdout's own register, in the holdout's own vault., score(), _cell(), collect(), main(), _overall(), _paragraph() (+55 more)

### Community 95 - "The Lim Household, Tampines"
Cohesion: 0.11
Nodes (20): loan_agreement Document Type, The Lim Household, Tampines, One Household Only; the Persona Sketches Are Gone, Address, Employment, Household canon, Life events that documents must reflect, People (+12 more)

### Community 96 - "Starting Parrot"
Cohesion: 0.14
Nodes (14): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass, Reading a document (+6 more)

### Community 97 - "Lane C - Governance and assurance"
Cohesion: 0.10
Nodes (22): The evaluation is the gate, The 40-document redacted holdout, The synthetic-to-real gap, Consent and redaction protocol, ISO/IEC 22989 to 5338 stage-to-process map, Lane C - Governance and assurance, Model card, Retention and erasure policy (+14 more)

### Community 98 - "Period"
Cohesion: 0.11
Nodes (30): Any, The span of time each document's printed dates cover; None for one that prints…, asked_period(), document_period(), _month(), outside(), Period, date (+22 more)

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.13
Nodes (16): benefit_illustration Document Type, birth_certificate Document Type, claim_letter Document Type, cpf_statement Document Type, Core Document Catalogue (ADR 0017), donation_receipt Document Type, identity_card Document Type, Identity Documents Are Household Data (+8 more)

### Community 100 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 101 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 102 - "PARROT Architecture Review"
Cohesion: 0.17
Nodes (15): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), The domain pack manifest, The expansion model: two axes, not one list, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build, The VRAM budget, with headroom, Risk register: what will actually go wrong (+7 more)

### Community 103 - "Data inventory: identity data, DOBs and loans"
Cohesion: 0.27
Nodes (10): Data inventory: identity data, DOBs and loans, The lock is a screen lock, not encryption, next dev binds every interface, not loopback, Telegram capture route and delete-at-source, What crosses a boundary, Local Ollama judge model, db service (pgvector/pgvector:pg17), Compose reads .env from infra/, not the repo root (+2 more)

### Community 104 - "TelegramCapture"
Cohesion: 0.19
Nodes (7): attribution(), Any, A daemon thread that long-polls the Telegram bot until `stop()` or process…, Begin polling. Returns False, with a logged reason, when it cannot or should…, One long poll. A failure waits rather than hammering the API with the same…, Whose phone this arrived on, recorded before anything is read off it. See ADR…, TelegramCapture

### Community 105 - "The autonomy statement"
Cohesion: 0.18
Nodes (13): Governance claims traced to enforcement points, IMDA mappings and autonomy statement artefact, The autonomy statement, The facts table as an extension point, Constraint: fully offline, The reminders table as an extension point, Explicitly not doing, Phase 1 — Retrieval (done) (+5 more)

### Community 106 - "web/ - the PARROT interface"
Cohesion: 0.22
Nodes (10): Task: complete the Insurance Agent pack, ADR 0017 - a pack is grounding and persona, The four surfaces: Today, Ask, Vault, Packs, Lane D - Domain packs and interface, The platform argument: one core, two domains, Zee's generated task list, Task: write the user stories with acceptance criteria, Every criterion binds to a register row and a supplied date (+2 more)

### Community 107 - "The document register as ground truth"
Cohesion: 0.18
Nodes (15): batch0-personas is deleted and must not be recreated, python -m corpus.validate, The document register as ground truth, The whole-life expiry_date mismatch, Register column headings are generated, not chosen, The household canon (the Lims of Tampines), Register first, documents second, Task: spot-check 20 register rows against the extractor (+7 more)

### Community 108 - "ingest.py"
Cohesion: 0.16
Nodes (17): itertools, Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks. Paperwork is short and…, _split_page(), discover(), embed_chunks() (+9 more)

### Community 109 - "_as_module_summary"
Cohesion: 0.25
Nodes (8): PacksResponse, _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack(), ModuleSummary, PackSummary

### Community 110 - "Reminder, Alert and Tracker Registers"
Cohesion: 0.19
Nodes (14): Passport Uses date_of_expiry So policy_expiry Does Not Fire, filing_deadline Reminder, maturity_date Is Not expiry_date, passport Document Type, passport_expiry Reminder, policy_expiry Reminder, policy_schedule Document Type, Reminder, Alert and Tracker Registers (+6 more)

### Community 111 - "Banded Abstention Evaluation Implementation Plan"
Cohesion: 0.12
Nodes (15): After this plan, Banded Abstention Evaluation Implementation Plan, Banded replay, Deviations from the spec, decided while planning, File structure, Global Constraints, Pull requests, Task 0: Worktree environment (+7 more)

### Community 112 - "example_pack template manifest"
Cohesion: 0.19
Nodes (13): I explain the renewal notice, I do not renew policies, Autonomy statement, never_acts as a machine-checked flag, abstention_rate, Set B, hard negatives, advice module manifest, example_pack template manifest, example_room advice shape (+5 more)

### Community 113 - "paperbrain/extract.py"
Cohesion: 0.41
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 114 - "§5 · Evaluation and results"
Cohesion: 0.15
Nodes (12): 5.10 What run 3 must add, 5.1 The claim, 5.2 What was measured, 5.3 The three-run spine, 5.4 Retrieval: what the two changes bought, 5.5 Abstention: the finding, 5.6 Extraction, by document type, 5.7 The two module metrics, and the lesson in them (+4 more)

### Community 115 - "Financial advisory process"
Cohesion: 0.12
Nodes (15): After the meeting, Before the meeting, During the meeting, Financial advisory process, For an overview on the financial advisory process in Singapore, For insurance products:, For investment products:, Frequently asked questions (FAQ) (+7 more)

### Community 116 - "Try PARROT"
Cohesion: 0.13
Nodes (15): 1 · Install five things, 2 · Download the AI models, 3 · Get the code and set it up, 4 · Put some documents in, 5 · Run it, 6 · Use it, Ask — a question about your own documents, If something goes wrong (+7 more)

### Community 117 - "test_eval_holdout.py"
Cohesion: 0.12
Nodes (30): apply_schema(), check_outside_the_repository(), documents_in(), HoldoutRefused, main(), migrations(), Path, RuntimeError (+22 more)

### Community 119 - "AdviceShape"
Cohesion: 0.09
Nodes (31): AdviceShape, FactInput, A printed fact a calculator reads, named by where it is printed rather than…, One kind of advice question, and everything its calculator needs to answer it., Adviser, date, Implemented by `modules/advice/`. `core/` calls this; it never computes a…, Every shape the pack's review lists, for one person, as one calculation (ADR… (+23 more)

### Community 120 - "Any"
Cohesion: 0.14
Nodes (17): Measurement, by_subject(), db(), FakeCursor, load_register(), Any, date, fixture (+9 more)

### Community 121 - "test_worker_queue.py"
Cohesion: 0.06
Nodes (53): The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, sha256(), Dispatcher, Inline, Any, Queued, Given a registered document, arrange for it to be read. Says what it arranged., Run the pipeline here and now, and report what it decided. (+45 more)

### Community 122 - "Retention and erasure policy"
Cohesion: 0.12
Nodes (16): A1. Retention rules, A2. What erasure means, A3. Three ways to erase, A4. Deleting a document: only on instruction, confirmed, and complete within 72 hours, A5. Erasing a person, and resetting the workspace, A6. Incident hold, B1. The only erasure paths that exist, B2. What deleting a `documents` row cascades to, and what it leaves (+8 more)

### Community 123 - "corpus_files"
Cohesion: 0.23
Nodes (16): blob(), corpus_files(), _git(), Path, The batch registers as committed at `commit`, templates excluded. The register…, The full commit id: a branch name or a short id moves, and a frozen run must…, Every document under `corpus/batches/` at `commit`, hashed from the commit's…, register_rows() (+8 more)

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.14
Nodes (15): Task: benchmark the workstation and publish the numbers, Task: build the answer graph with the grounding gate, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, The deliberately naive retrieval baseline, Committed runs are never deleted, Task: contextualised chunking and the reranker, Task: hybrid retrieval with reciprocal rank fusion (+7 more)

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 126 - "test_contracts.py"
Cohesion: 0.07
Nodes (62): copy, PackManifest, A domain pack, authored as one YAML file: grounding, persona, answering and…, _advised(), _checked(), _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held() (+54 more)

### Community 127 - "The five-lane split (five people, nine weeks, three builders)"
Cohesion: 0.13
Nodes (17): The golden set: answerable, hard negatives, adversarial, Contracts before code, Everyone, regardless of lane, Fill the register first, then mail-merge the documents, The five-lane split (five people, nine weeks, three builders), How the code gets written, Invented organisations only, Lane B - Retrieval and evaluation (Yew Mun) (+9 more)

### Community 128 - "A field name is written down once"
Cohesion: 0.33
Nodes (6): Qwen-SEA-LION-v4-4B-VL extraction ceiling, Register first, then generate, Ground truth for free, extraction_f1, A field name is written down once, Never hand-edit a generated file

### Community 129 - "The demonstration run sheet"
Cohesion: 0.11
Nodes (19): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+11 more)

### Community 130 - "CalendarEventIn"
Cohesion: 0.20
Nodes (11): CalendarEvent, CalendarEventIn, model_validator, What a person sets on an entry. The same shape creates and replaces one: an…, One stored entry, every date of it. Occurrences are `CalendarEntry` rows., _as_calendar_event(), create_event(), replace_event() (+3 more)

### Community 131 - "Filling the corpus register"
Cohesion: 0.20
Nodes (9): Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one, The rule that cannot bend (+1 more)

### Community 132 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (9): Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six, Where governance touches the code (+1 more)

### Community 133 - "ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.20
Nodes (14): Not finding you is an answer (first-person abstention), guardrails.abstain_below was calibrated on un-prompted scores, ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts, chunks.tsv built from context_prefix || text, Context prefix: title - type - heading - page, rag_probe2 before/after similarity table (six policies, 13 September), scripts/reindex.py rebuilds chunks and vectors, Chunks follow the document's structure (Docling heading labels) (+6 more)

### Community 134 - "Working agreement for coding agents"
Cohesion: 0.22
Nodes (9): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents, Slash Commands: orient, check, handover, weekly (+1 more)

### Community 135 - "igd-capstone-2026"
Cohesion: 0.13
Nodes (15): Working Agreement for Coding Agents, The Five Lanes and Their Owners, Setting Up a Second Machine, PARROT Is an Internal Working Name, Authoring a pack, igd-capstone-2026, `main` is not protected, PARROT, a Local-First Household RAG Platform (+7 more)

### Community 136 - "Policy schedule HTML template"
Cohesion: 0.24
Nodes (10): b1-0001 Private Car Insurance Policy Schedule, b1-0002 HomeShelter Contents Policy Schedule, b1-0003 Hospital Income Protection Plan Schedule, Full-length insurance policy notebook prompt, No Ref: line anywhere on the document, Cross-document corpus consistency, Four full-policy notebook prompts, Shared policy-drafting preamble (+2 more)

### Community 137 - "test_startup.py"
Cohesion: 0.09
Nodes (35): _kill_tree(), Popen, Stop a child and everything under it, then make sure it has gone., Start `npm run dev` in `web/`, or say plainly why it could not. Three reasons…, Stop a child the launcher started -- the worker or the screens -- and…, start_web(), stop(), main() (+27 more)

### Community 138 - "household/page.tsx"
Cohesion: 0.15
Nodes (12): dynamic, HouseholdPage(), metadata, runtime, AppLayout(), OwnerForm(), Roster(), WhoIsThis() (+4 more)

### Community 139 - "PaperBrain"
Cohesion: 0.22
Nodes (8): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles, Login is a local passphrase

### Community 140 - "ADR 0013: A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.15
Nodes (17): Schedule-table questions remain weak (rank 2-4), ADR 0013: A question is understood before it is searched, and scoped before it is cut, The answer prompt carries today's date and names the scoped relation as who the question is about, AskRequest.history carries up to twelve earlier turns, A relevance-grading call and an 'answerable' schema flag were both dropped, Remaining failures are retrieval's to fix (cross-encoder plus lexical), The router is unchanged and separate from understanding, Understand, then search (one model call writes the whole question plus 2-3 document-worded queries) (+9 more)

### Community 141 - "test_rerank.py"
Cohesion: 0.14
Nodes (24): CrossEncoderReranker, passage_text(), One relevance logit per text, higher is better. Batched so forty passages is a…, Say it, once per process. A passage cut at the cap is scored on its first part…, What the reranker reads: the one-line context, when a chunk carries one, then…, The cross-encoder's score as a probability. The model emits a logit; a floor is…, Implements `core.graph.ports.Reranker`. Reorders by the cross-encoder's score,…, relevance() (+16 more)

### Community 142 - "_as_consent"
Cohesion: 0.29
Nodes (7): AdviceConsent, AdviceConsent, One advising pack, the wording a person is asked to agree to, and what the…, _as_consent(), advice_consents(), record_consent(), One advising pack's consent wording and the owner's standing answer to it.

### Community 143 - "Model card — PARROT v1"
Cohesion: 0.15
Nodes (12): 1. What the system is, 2. Intended use, 3. Out of scope, 4. Measured performance, 5. Known failure modes, 6. Data, 7. What a user is told, Model card — PARROT v1 (+4 more)

### Community 144 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 145 - "Set C: adversarial"
Cohesion: 0.33
Nodes (5): Assumptions to recheck before the run, How it is scored, Planted documents (for Desmond), Set C: adversarial, The line format

### Community 146 - "Policy Schedule Template"
Cohesion: 0.16
Nodes (15): One cell, one field, Policy Schedule Template, Renewal Notice Template, ADR 0010 - main is unprotected, and the discipline is human, Amend the graph refresh into the commit, Graphify shared knowledge graph, Two kinds of extraction, Union merge driver for graph.json (+7 more)

### Community 147 - "alert module manifest"
Cohesion: 0.28
Nodes (9): Days without recorded cover tile, alert_fpr, obligation_precision, Module manifest template, Quoted "on" key in YAML 1.1, alert module manifest, Modules read typed rows, never chunks, reminder module manifest (+1 more)

### Community 148 - "Aim Headline Metrics Implementation Plan"
Cohesion: 0.15
Nodes (12): Aim Headline Metrics Implementation Plan, Deviations from the spec, decided while planning, File structure, Global Constraints, Pull request, Task 0: Starting state (controller, before any dispatch), Task 1: The `phrasing` field, Task 2: `eval/headline.py` — the five numbers (+4 more)

### Community 149 - "ConfigurationError"
Cohesion: 0.11
Nodes (24): _chat_ids(), ConfigurationError, _flag(), _folder(), local_url(), _port(), _positive(), Path (+16 more)

### Community 150 - "Consent and redaction protocol: the real-document holdout"
Cohesion: 0.10
Nodes (20): 10. PDPA obligations this protocol answers, 1. What the holdout is, and why it needs this, 2. Rules at a glance, 3. What may be contributed, 4.1 Who asks, and how, 4.2 The consent record, 4.3 Withdrawal, 4. Consent (+12 more)

### Community 151 - "Household canon"
Cohesion: 0.20
Nodes (8): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, The family tree, and why three of them are not called Lim, Vehicles

### Community 152 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 153 - "test_modules.py"
Cohesion: 0.16
Nodes (27): Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), Everything inside a lead window that has not already been said for that window.…, sweep(), FakeConn, obligation_row(), datetime, Reminder and Alert: what fires, once, and with what behind it. Both modules are… (+19 more)

### Community 154 - "Every Fact Row Cites Its Source"
Cohesion: 0.20
Nodes (11): Every Fact Row Cites Its Source, No Claim Without a Citation, A Correction Cannot Invent a Row, Every Response That States Something Carries Its Source, Citation Names Resolved Once Per Response, Every Node Writes One Line to traces, The Ingestion Pipeline, The Pipeline Forks Into Retrieval and Facts Lanes (+3 more)

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (8): parrot-sweep shimmer animation, Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, An answer with the page it came from, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "main"
Cohesion: 0.22
Nodes (10): main(), open_browser(), parse_args(), port_answers(), Any, Namespace, Whether something is listening on loopback. Not whether it is ours., Keep Parrot running across restarts, and own the screens so they outlive them.… (+2 more)

### Community 157 - "score.py"
Cohesion: 0.05
Nodes (88): Answer, Cited, One sentence and the passages it was traced to. What rule 3 looks like as data.…, Answered. Asking for consent and naming what is missing are endings, not…, Trace, cites(), contained(), contained_by_flag() (+80 more)

### Community 158 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.20
Nodes (10): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Task: run adversarial Set C and write up the findings, Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The six artefacts (+2 more)

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 160 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 161 - "test_eval_ranked.py"
Cohesion: 0.16
Nodes (19): capped(), documents(), governing(), Any, The pack whose floor decides, and that floor. `core` when no pack speaks for…, Every distinct document among the passages read, in the order the reranker put…, The four fields `eval/bands.py` replays from, for one question. `packs` are the…, The questions a floor-off run still held back: core evidence under the core… (+11 more)

### Community 162 - "typing"
Cohesion: 0.06
Nodes (47): The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), collections_abc, The record of every advised or withheld answer (ADR 0016). `advice_records`…, A person fixing a field the extractor got wrong. This is the one place in the…, What a calculator returns, and what the graph needs to ask consent and keep a…, A dense-only retriever, so the graph can be run and tested before Lane B's… (+39 more)

### Community 163 - "test_eval_harness.py"
Cohesion: 0.06
Nodes (58): The last question's contexts and candidate count, then a clean slate., Each question on its own thread, so no answer is a follow-up to the one before., Recorder, trace_all(), _judge_missing(), _provenance(), Path, Decode rate and peak VRAM from the newest benchmark file… (+50 more)

### Community 164 - "._claim"
Cohesion: 0.18
Nodes (9): Claim, _advice_basis(), Any, One streamed sentence object, turned into the thing the gate understands. The…, Routing and evidence. The answering is not a node — it yields, and a node…, Every removable passage mention, removed. One removal can expose the next — in…, Everything an advised answer rested on, so it can be reconstructed from its…, _without_one_round_of_passage_numbers() (+1 more)

### Community 165 - "Evaluation"
Cohesion: 0.16
Nodes (14): Evaluation, Extraction F1 by document type, Generating a lane's dozen, Ground truth comes free, How much of a delta is a delta, Metrics and targets, Running the harness, Set A, answerable (+6 more)

### Community 166 - ".__post_init__"
Cohesion: 0.60
Nodes (4): aembed_text(), aembed_texts(), embed_text(), embed_texts()

### Community 167 - "_git_sha"
Cohesion: 0.10
Nodes (22): _dirty(), _git(), _git_sha(), The commit, with "-dirty" when the code a run executes has uncommitted changes…, Tracked changes in `git status --porcelain` output; an untracked file never ran., _as_date(), _as_number(), _contains() (+14 more)

### Community 168 - "lucide-react"
Cohesion: 0.08
Nodes (24): lucide-react, dynamic, runtime, LockButton(), SURFACES, TabBar(), Tabs(), ADR-0020 (+16 more)

### Community 169 - "Banded abstention: an evaluation model beside the fixed floor"
Cohesion: 0.18
Nodes (10): 1. What one run records, 2. Replay and banding — `eval/bands.py`, 3. The report, 4. Testing, Approach: record once, replay many, Banded abstention: an evaluation model beside the fixed floor, Pull requests, Scope (+2 more)

### Community 171 - "build.py"
Cohesion: 0.11
Nodes (26): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering…, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why the catalogue cannot supply `field` from every one of `doc_types`, or None., Every core document type, field and category this pack names exists, or…, A compared field no document type of the shape declares can never be printed.…, _class_name(), _docstring() (+18 more)

### Community 172 - "19 · A relevance floor on the reranker does not buy abstention, and the reason is not calibration"
Cohesion: 0.22
Nodes (8): 19 · A relevance floor on the reranker does not buy abstention, and the reason is not calibration, Alternatives considered, Consequences, Context, Decision, Revisit when, The measurement, Why it is not a calibration problem

### Community 173 - "Page one as plain Label: value lines"
Cohesion: 0.33
Nodes (6): Appendicitis entitlement demonstration, Page one as plain Label: value lines, Ward and hospital entitlement clause, Answering: vocabulary, categories, exclusions, The four tests every field must pass, policy_type was judged, not printed

### Community 174 - "Project skills"
Cohesion: 0.40
Nodes (4): Changing them, Project skills, Slash commands, Using them

### Community 175 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 176 - "pipeline.py"
Cohesion: 0.05
Nodes (60): Chunk, chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, One flat list of chunks, ordinal running across the whole document. (+52 more)

### Community 177 - "reading_order"
Cohesion: 0.29
Nodes (8): Block, _box(), Where Docling found the item, measured from the top of the page, or None if…, Docling's order, with any block it put after something printed below it moved…, `lower` starts at or under the line where `upper` ends, and they share some…, One thing the parser found on a page, and what kind of thing it is., reading_order(), _under()

### Community 179 - "_pages_from"
Cohesion: 0.19
Nodes (21): _pages_from(), Group Docling's items by the page they were found on. Docling's markdown export…, A table as lines of text, one row per line: `label: value` when a row has two…, _table_text(), SimpleNamespace, _at(), _cell(), _on_page() (+13 more)

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 181 - "draft"
Cohesion: 0.13
Nodes (19): period(), The dates a question names, as whole calendar units (SDRR ADR 0018): "next…, Reply, _clock(), _dates(), draft(), _iso(), _person_in() (+11 more)

### Community 182 - "advice_consent.py"
Cohesion: 0.19
Nodes (18): Channel, current(), grant(), _latest(), NoOwner, Any, RuntimeError, The owner's consent to a pack's advice, append-only (ADR 0016). Consent is the… (+10 more)

### Community 183 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 184 - "Basic Financial Planning Guide"
Cohesion: 0.15
Nodes (12): Basic Financial Planning Guide, Basic Financial Planning Guide, Basic Financial Planning Guide For Entrants To The Workforce, Basic Financial Planning Guide for those nearing retirement, Basic Financial Planning Guide For Those With Dependents, Emergency funds, For those approaching retirement, For those new to the workforce (+4 more)

### Community 185 - "no_weights"
Cohesion: 0.12
Nodes (15): FakeEncoded, FakeModel, FakeTokenizer, no_weights(), Any, fixture, LogCaptureFixture, MonkeyPatch (+7 more)

### Community 186 - "answer"
Cohesion: 0.19
Nodes (17): answer(), day_name(), Deadline, _deadline_line(), deadlines(), describe(), digest(), Line (+9 more)

### Community 188 - "What to ask before buying life insurance"
Cohesion: 0.20
Nodes (9): Are verbal representations provided in line with what's in the insurance policy documents?, Ask your FA representative, Ask yourself, Has the FA representative recommended a suitable product?, Is the information in the insurance policy correct?, Is there any benefit to switching insurance or investment products?, Take your time, What to ask before buying life insurance (+1 more)

### Community 190 - "2. Amended Gemini Prompts Bank (Xinkapow Yellow/Orange Cards with KFC Mascot)"
Cohesion: 0.11
Nodes (19): 1. Ground Truth Parameters (Canonical Lim Household & Xinkapow), 2.1 Marcus Lim Jun Wei — Xinkapow National Identity Card (Front), 2.2 Marcus Lim Jun Wei — Xinkapow National Identity Card (Back), 2.3 Rachel Ng Hui Shan — Xinkapow National Identity Card (Front), 2.4 Rachel Ng Hui Shan — Xinkapow National Identity Card (Back), 2.5 Lim Ah Kow (Father) — Xinkapow Senior Citizen Identity Card, 2.6 Tan Mei Ling (Mother) — Xinkapow Senior Citizen Identity Card, 2.7 Lucas Lim Kai En — Xinkapow Digital Birth Certificate (+11 more)

### Community 200 - "§4.3–4.4 · Packs and the interface, with the expansion model"
Cohesion: 0.20
Nodes (9): 1 · The expansion model (feeds §3.3), 2 · What a pack is, and what it stopped being (ADR 0017), 3 · Enforced, not agreed (feeds §4.3), §4.3–4.4 · Packs and the interface, with the expansion model, 4 · The two built packs, 5 · The catalogue as the expansion model's evidence, 6 · The interface (feeds §4.4), The argument (+1 more)

### Community 201 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.20
Nodes (17): Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022, Platform Workers have wider protection gaps than the economically active population, Mortality protection gap (21%, S$373 billion, PGS 2022), LIA 2022 Protection Gap Study Key Findings (+9 more)

### Community 204 - "package.json"
Cohesion: 0.05
Nodes (40): class-variance-authority, clsx, eslint, eslint-config-next, next, next-themes, postcss, react-dom (+32 more)

### Community 205 - "Tax and Reliefs pack (iras_tax)"
Cohesion: 0.22
Nodes (13): iras_tax grounding binding (corpus iras_reliefs_ya2026, top_k 8), Tax and Reliefs pack (iras_tax), iras_tax persona (explains the user's documents against IRAS guidance, never estimates a liability), Task lists are generated from docs/team-tasks.csv, Twelve golden-set questions per person by the end of week 3, Lane A - Christian, integration and product, Lane B - Yew Mun, retrieval and evaluation, Lane C - Siew, governance and assurance (+5 more)

### Community 211 - "ModuleManifest"
Cohesion: 0.14
Nodes (14): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders…, InstalledModule, manifest(), ModuleUnavailable, RuntimeError, Load the installed capability modules at runtime. The mirror of…, A module's YAML is missing, or does not validate against `ModuleManifest`. (+6 more)

### Community 212 - "_read"
Cohesion: 0.11
Nodes (28): _coerce(), decode_schema(), _drop_format(), field_lines(), _normalise(), _prepare(), printed_date(), Any (+20 more)

### Community 213 - "FakeConn"
Cohesion: 0.18
Nodes (13): FakeConn, _no_owner(), _owned(), A recording fake in the house style (see `tests/test_grounding_index.py`'s…, Script the owner household.owner reads: one person, `is_owner`., test_an_older_version_gives_status_outdated(), test_current_is_none_when_the_latest_grant_is_a_different_version(), test_current_queries_the_latest_row_by_person_and_pack() (+5 more)

### Community 214 - "Comparison of Integrated Shield Plans"
Cohesion: 0.18
Nodes (10): Common reasons why insurers do not provide a Letter of Guarantee in specific cases, Common reasons why insurers may reject or not pay for claims, Comparison of Integrated Shield Plans, Comparison of lifetime premiums, Important Information, Letter of Guarantee, List of Integrated Shield Plans (IPs) and their targeted level of coverage, Medical Record Costs (+2 more)

### Community 215 - "Christian — task list"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 216 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 217 - "Desmond — task list"
Cohesion: 0.18
Nodes (11): Desmond — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 218 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 219 - "Yew Mun — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

### Community 220 - "Graphify — the shared knowledge graph"
Cohesion: 0.20
Nodes (9): Graphify — the shared knowledge graph, Keeping it fresh, Merge conflicts, solved properly, Setup, once per clone, The hook leaves your tree dirty. Amend it into the commit you just made., Two kinds of extraction, and which needs what, Using it, What is committed, and what is not (+1 more)

### Community 221 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 222 - "Understanding health insurance"
Cohesion: 0.15
Nodes (12): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Assistance under MediFund, Basic health insurance coverage, Choosing your level of coverage, How MediSave fits in, If you have company health insurance, If you want more coverage (+4 more)

### Community 224 - "test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them"
Cohesion: 0.25
Nodes (5): ClosingSpy, Wraps an event generator to record whether something called `.close()` on it,…, Starlette's own body iteration (`iterate_in_threadpool`) never calls `.close()`…, test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them(), spying()

### Community 225 - "20 · The household calendar lives in Postgres, answers by code, and Parrot only ever drafts an entry"
Cohesion: 0.29
Nodes (6): 20 · The household calendar lives in Postgres, answers by code, and Parrot only ever drafts an entry, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 226 - "RecordingConn"
Cohesion: 0.15
Nodes (5): A connection and its cursor in one: records every statement, commits nothing…, Extraction is judged before embedding: a document bound for quarantine costs no…, RecordingConn, test_a_document_that_fails_extraction_is_neither_embedded_nor_written(), test_a_read_document_is_written_to_both_lanes_in_one_commit()

### Community 227 - "Zee — Lane D · Domain packs and interface"
Cohesion: 0.22
Nodes (9): Half one — domain packs (weeks 1 to 7), Half two — the interface (weeks 4 to 8), Read this first, Rules that apply to you specifically, The two halves of this lane, What "done" looks like, What you present, Your Claude Code skills (+1 more)

### Community 228 - "Zee — task list"
Cohesion: 0.22
Nodes (9): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20, W9 — due 2026-11-03 (+1 more)

### Community 229 - "build_team_tasks.py"
Cohesion: 0.29
Nodes (9): collections, difflib, main(), Path, Generate each member's task list from the master task CSV. python…, _read_rows(), _render(), _week_key() (+1 more)

### Community 230 - "PrivateCare Policy Wording Template"
Cohesion: 0.31
Nodes (9): PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Gemini prompt bank for identity specimens, The Lim household canon, Republic of Xinkapow (+1 more)

### Community 232 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 234 - "Contributing"
Cohesion: 0.17
Nodes (12): Sources of Truth Generate Their Outputs, Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure (+4 more)

### Community 235 - "The corpus"
Cohesion: 0.10
Nodes (20): Amend the Graph Refresh Into the Commit, Qwen-SEA-LION-v4-4B-VL Generator, No CORS Middleware, Deliberately, Changelog, Generation Model Swapped to Fit One 8 GB Card, W1 · 2–8 Sep 2026, W2 · 9–15 Sep 2026, Capture Channels Are Transports (+12 more)

### Community 236 - "AdviceRecord"
Cohesion: 0.25
Nodes (6): AdviceLog, AdviceRecord, Protocol, Implemented by `HouseholdAdviceLog` in `core/advice_records.py`., Every advised or withheld answer's full basis, so it can be reconstructed later…, Log

### Community 237 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 238 - "16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.29
Nodes (7): 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent, Addendum, 17 September 2026: coverage review and the adult rule, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 239 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 240 - "Notion"
Cohesion: 0.29
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 241 - "Premium and Subsidy Tables"
Cohesion: 0.12
Nodes (14): MediShield Life (CPF Board), Exclusions under MediShield Life, Fertility Preservation Procedures in cases of potential iatrogenic infertility, List of Serious Pregnancy and Delivery-related Complications, MediShield Life Benefits, MediShield Life Benefits, MediShield Life Premium Schedule for Singapore Citizens and Permanent Residents, Merdeka Generation Subsidy (+6 more)

### Community 242 - "Understanding integrated shield plans"
Cohesion: 0.25
Nodes (7): Are you covered?, IP deductible ($1,500-$3,500 by ward class) and 5% co-payment, Should you upgrade to an IP?, The deductible is the fixed amount you pay each policy year – ranging from $1,500 to $3,500, depending on ward class – before any payout from your IP. The co-payment is 5% of the bill, capped at a minimum of $6,000 per year., Understanding integrated shield plans, Your budget, Your comfort level with the types of hospitals, wards and doctors

### Community 243 - "Christian — Lane A · Integration and product owner"
Cohesion: 0.29
Nodes (7): Also yours, Christian — Lane A · Integration and product owner, Starter prompt for your coding agent, Starter prompt: what can I actually pick up?, The five things you ship, Week 1, in order, What integration actually means here

### Community 244 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

### Community 246 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 248 - "Claude Code — read this first"
Cohesion: 0.33
Nodes (5): Before you say you are done, Claude Code — read this first, Finding your way around, Skills and commands, The three things agents get wrong here

### Community 250 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 251 - "Third-party material the system indexes, and on what basis"
Cohesion: 0.25
Nodes (7): Open items, The basis: the computational data analysis exception, The e-Tax Guide, The obstacle, Third-party material the system indexes, and on what basis, What is indexed, Where the exception stops

### Community 252 - "14 · A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.33
Nodes (6): 14 · A pack supplies what the core knows about a domain, and the core stays generic, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 253 - "17 · A pack is grounding and persona; the core owns documents"
Cohesion: 0.33
Nodes (6): 17 · A pack is grounding and persona; the core owns documents, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 254 - "Artefacts"
Cohesion: 0.33
Nodes (5): A note on the model, Artefacts, Current deliverables, Regenerating, Source material

### Community 255 - "Why the prototype is evaluated on synthetic data"
Cohesion: 0.33
Nodes (5): The decision, What synthetic data does not prove, What we do not do, Why, Why the prototype is evaluated on synthetic data

### Community 257 - "About Integrated Shield Plan"
Cohesion: 0.25
Nodes (8): About Integrated Shield Plan, How do I find out if I have an Integrated Shield Plan?, How do Integrated Shield Plan premiums and claims work?, Integrated Shield Plan (MediShield Life component plus a private insurance component), Should I consider purchasing an Integrated Shield Plan?, What is an Integrated Shield Plan?, Comparison of Private Hospital IPs (MOH, Jun 2026), Standard Integrated Shield Plans targeted at Ward Class B1 (MOH, Jun 2026)

### Community 259 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 260 - "freeze.py"
Cohesion: 0.21
Nodes (14): apply_household(), Declared, FreezeRefused, household(), main(), RuntimeError, Load a frozen corpus commit into an isolated vault, verify it, and report — for…, A household declaration: `{"people": [{"name", "relation", "owner"?,… (+6 more)

### Community 261 - "`core/graph/` — the LangGraph runtime"
Cohesion: 0.40
Nodes (4): `core/graph/` — the LangGraph runtime, Rules, What belongs here, What does not

### Community 262 - "Headline metrics that measure the aims, not the targets"
Cohesion: 0.22
Nodes (8): 1. The five numbers, 2. Where it lives, 3. The README, the targets and DY, 4. Testing, Headline metrics that measure the aims, not the targets, Note for DY, What changes, Why

### Community 263 - "_page_of_examples"
Cohesion: 0.24
Nodes (10): _page_of_examples(), One page printing every field's `example`, so each value is attributable to a…, Each field's example as the model reports it; a repeating one as label and…, ADR 0017: several riders on one schedule, each a row pairing its label and its…, `FieldSpec.name` is the `facts.key`. Nothing between the manifest and the row…, The named regression, spelled out so a future rename cannot quietly reintroduce…, _reply_of_examples(), test_a_donation_receipt_stores_donation_amount_and_never_amount() (+2 more)

### Community 266 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 267 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

### Community 268 - "adr/README.md"
Cohesion: 0.07
Nodes (27): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 12. Chunks follow the document's headings, and embeddings use the model's task prompts, Consequences, Context, Decision (+19 more)

### Community 269 - "Data inventory — identity data, dates of birth and loans"
Cohesion: 0.40
Nodes (4): Data inventory — identity data, dates of birth and loans, Open questions for Siew, The inventory, What this entry covers

### Community 270 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 271 - "telegram.py"
Cohesion: 0.13
Nodes (20): _attachment(), _pixels(), Any, Client, datetime, Response, The Telegram capture adapter. Same interface as the folder: `receive(payload,…, Confirm the token works before anything else is attempted. (+12 more)

### Community 272 - "`core/ingest/` — the ingestion worker"
Cohesion: 0.50
Nodes (3): `core/ingest/` — the ingestion worker, Quarantine is two-stage, Rules

### Community 273 - "`core/retrieve/` — hybrid retrieval"
Cohesion: 0.50
Nodes (3): `core/retrieve/` — hybrid retrieval, Rules, What belongs here

### Community 274 - "START.cmd launcher"
Cohesion: 0.39
Nodes (8): ADR 0005 - The watched folder is polled, not subscribed to, Stability debounce with injected time, ADR 0008 - Ingestion runs on a Celery worker, The queue carries a digest, not the document, START.cmd launcher, Telegram capture, The ingestion worker, The watched inbox folder

### Community 275 - "The nine, one at a time"
Cohesion: 0.13
Nodes (14): 1. Accountability, 2. Data, 3. Trusted development and deployment, 4. Incident reporting, 5. Testing and assurance, 6. Security, 7. Content provenance, 8. Safety and alignment R&D (+6 more)

### Community 276 - "Getting Parrot ready (startup readiness screen)"
Cohesion: 0.29
Nodes (8): The readiness check verifies the model the way it will be used (one pair scored), Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Four readiness components: your documents, filing, screens, local model, Getting Parrot ready (startup readiness screen), Power menu: Lock, Restart Parrot, Shut down Parrot, Restarting Parrot (engine stops, a fresh engine starts, the page reconnects by itself), Parrot is off (terminal state page), Parrot is waiting for its database (Docker Desktop not running)

### Community 277 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): 1. What a pack is, 2. The one thing to understand before you start, 3. The workflow, 5. The grounding corpus, 6. Definition of done, 7. Where to ask, Authoring a domain pack

### Community 278 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 279 - "`docs/governance/` — the assurance artefacts"
Cohesion: 0.50
Nodes (3): `docs/governance/` — the assurance artefacts, The autonomy statement in one line, The rule that governs all eight

### Community 280 - "InstalledPack"
Cohesion: 0.05
Nodes (39): _advice_prompt(), answer_system(), _citations(), _closes(), _distinct(), _either(), _guidance(), _max_sentences() (+31 more)

### Community 283 - "The pack catalogue"
Cohesion: 0.33
Nodes (5): Open questions, The nine packs, The pack catalogue, What building one involves, What the catalogue shows

### Community 284 - "Tax and Reliefs — contract changes this pack needs"
Cohesion: 0.40
Nodes (4): 1. A deduction multiplier on `estimate_saving`, 2. Limiting a fact input to one year, Not a contract change: parent relief, Tax and Reliefs — contract changes this pack needs

### Community 285 - "HouseholdInventory"
Cohesion: 0.15
Nodes (8): _Answering, The event stream one request is sending, held where the request's cleanup can…, Close the answer stream when the request ends, whatever ended it. Requires…, Conn, HouseholdInventory, Handed to `AnswerGraph` by whoever holds a connection, as `HouseholdScope` is., ADR 0017: a document is the core's, so the query includes `core` whatever is…, test_the_inventory_always_reads_core_documents()

### Community 286 - "IMDA frameworks: what applies to PARROT"
Cohesion: 0.15
Nodes (12): 1. Assess and bound the risks upfront (§2.1, pp 15–24), 2. Make humans meaningfully accountable (§2.2, pp 25–32), 3. Implement technical controls and processes (§2.3, pp 33–45), 4. Enable end-user responsibility (§2.4, pp 46–49), Agentic AI framework: four dimensions (MGF for Agentic AI v1.5), Findings from this pass, For Siew, GenAI framework: nine dimensions (+4 more)

### Community 288 - "Pack grounding corpus rules"
Cohesion: 0.50
Nodes (3): ISO/IEC 22989 stages versus 5338 processes, Grounding corpora, Pack grounding corpus rules

### Community 289 - "phrasings.py"
Cohesion: 0.20
Nodes (11): _keys(), LaneSpec, Row, How a question about a printed field is worded, per document type in…, One document type's wordings. `printed` and `spoken` each render the *thing* a…, Which register rows a lane's questions are drawn from. The task asks each…, A wording, or `None` when the row does not fill every field it needs., The spoken wording, or "Rachel's payslip" when the type has no product name of… (+3 more)

### Community 290 - "Contracts and Migrations Are Their Own PR"
Cohesion: 0.33
Nodes (6): The Purely Additive Migration Exception, Contracts and Migrations Are Their Own PR, Snooze Means Not Until This Gets More Urgent, The Three Things Agents Get Wrong Here, MemorySaver Until a Reviewed Migration, MemorySaver Checkpointer, Not PostgresSaver

### Community 291 - "ADR 0002 - One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (7): ADR 0001 - Record architecture decisions, ADR 0002 - One PostgreSQL instance for everything, Reciprocal rank fusion of dense and lexical, ADR 0003 - PaperBrain informs the pattern, not the module, PaperBrain prototype, Contracts before code, Lane A - Integration and product

### Community 292 - "._categories_read_a_declared_field"
Cohesion: 0.33
Nodes (3): model_validator, Whether any document type in the catalogue declares `field`., An advice shape that names a missing role or key fails at load time. Caught…

### Community 293 - "test_eval_generate.py"
Cohesion: 0.09
Nodes (46): _ambiguous(), choose(), documents(), Generated, hand_written(), main(), on_file(), pool() (+38 more)

### Community 294 - "Scoped"
Cohesion: 0.18
Nodes (12): The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting…, Scoped, 13 September: "how much is my son's life insurance?" came back as the owner's…, 13 September: "is my dad's hospital cover still active?" was scoped to Lim Ah…, "When does Rachel's policy renew?" is scoped to Rachel by name, with no…, test_a_question_about_a_parent_names_them_as_who_it_is_about_and_carries_todays_date(), apply() (+4 more)

### Community 295 - "TelegramSettings"
Cohesion: 0.13
Nodes (12): BaseTransport, RuntimeError, Safe to show: never contains the token., TelegramSettings, TelegramUnavailable, test_the_digest_speaks_only_to_the_allow_list(), FakeRegistrar, The offset has already moved, so the survivors are all that is left to save. (+4 more)

### Community 296 - "Autonomy statement — PARROT v1"
Cohesion: 0.20
Nodes (9): Autonomy statement — PARROT v1, IMDA Agentic AI framework — where this sits, Open questions, Residual risk, Sources, The statement, What v1 does do without being asked, stated so the boundary is exact, What would have to be true to move the boundary (+1 more)

### Community 298 - "§7.4 · Commercialisation roadmap"
Cohesion: 0.33
Nodes (5): §7.4 · Commercialisation roadmap, Packs are the unit of sale, Roadmap, Segments, from the five personas, The two constraints we can defend

### Community 299 - "Terms of use"
Cohesion: 0.20
Nodes (9): Clause A. Authority and Consent for Submissions on Behalf of Another Adult, Clause B. Purpose of Collection, Use and Retention, Clause C. Personal Data of Third Parties, Clause D. AI-Generated Answers and Helpdesk, Definitions, For review, Not yet written, Status against the code (+1 more)

### Community 300 - "The five lanes"
Cohesion: 0.33
Nodes (6): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, The five lanes

### Community 301 - "Incident and data breach procedure"
Cohesion: 0.22
Nodes (8): 1. What counts, 2. The six steps, 3. Is it a notifiable breach?, 4. The incident log, 5. Who is responsible on a household's own computer, Containment, by kind, Decisions for Siew, Incident and data breach procedure

### Community 302 - "`docs/report/` — the final report"
Cohesion: 0.33
Nodes (6): `docs/report/` — the final report, Ownership, Source documents written for the report, The rule that keeps it honest, The thing to understand before you write a word, Three questions for the supervisors, at the 6 October mid-term

### Community 303 - "gate.py"
Cohesion: 0.13
Nodes (16): Exclusions, A sentence claiming cover whose every citation sits under one of `headings` is…, _loose_numbers(), _normal(), The grounding gate. Rule 3 in AGENTS.md: no claim without a citation. This…, Every number in `text` that is not part of an identifier: an identifier is…, Every number or identifier in a sentence that no cited passage prints. An…, "1,860.00", "1860" and "01" → "1860", "1860", "1": formatting is not a… (+8 more)

### Community 304 - "classify"
Cohesion: 0.14
Nodes (13): Classification, classify(), _prompt(), Never raises. An unavailable model is a classification failure, so it…, _schema(), ADR 0017: candidates are the catalogue's types, unqualified, and every one is…, ADR 0017 decision 6: these were quarantined because no type fitted them., test_a_document_no_pack_recognises_is_not_forced_into_one() (+5 more)

### Community 305 - "ISO/IEC 22989 stages and ISO/IEC 5338 processes: what PARROT actually does"
Cohesion: 0.25
Nodes (7): ISO/IEC 22989 stages and ISO/IEC 5338 processes: what PARROT actually does, Open questions, Processes consciously not performed, The map, The three AI-specific processes, plainly, Two standards, two jobs, What the architecture review planned, corrected against the code

### Community 306 - "test_eval_freeze.py"
Cohesion: 0.26
Nodes (12): differences(), Entry, manifest(), manifest_sha(), Any, One hash over every path and its content hash, independent of listing order., Every path added, removed or changed against a published manifest. Empty means…, role() (+4 more)

### Community 307 - "13. A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.40
Nodes (5): 13. A question is understood before it is searched, and scoped before it is cut, Consequences, Context, Decision, Evidence

### Community 308 - "1. Record architecture decisions"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 309 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 310 - "FakeCursor"
Cohesion: 0.20
Nodes (3): FakeCursor, Any, FakeConn

### Community 311 - "test_advice_core.py"
Cohesion: 0.35
Nodes (12): passages_for(), Inputs as kind fact/rule passages (chunk_id from the ref), and the figures as…, check_content(), Why a cited sentence still cannot be kept, or `None`. Asked after `check_one`…, _calculation(), The types a calculator hands back, the owner's consent, and the record of an…, test_check_content_keeps_a_sentence_stating_a_facts_value(), test_check_content_keeps_a_sentence_stating_a_figure() (+4 more)

### Community 315 - "Incident log"
Cohesion: 0.50
Nodes (3): Incident log, Incidents, Template

### Community 316 - "5. The watched folder is polled for stability, not subscribed to for events"
Cohesion: 0.40
Nodes (4): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision

### Community 317 - "is_first_person"
Cohesion: 0.29
Nodes (8): is_first_person(), Whether this question is about the person asking. `other_names` are the display…, parametrize, "What is Rachel's premium on my policy" is a question about Rachel. A…, test_a_named_household_member_wins_over_the_pronoun(), test_a_possessive_relation_names_whose_documents_are_asked_about(), test_first_person_questions_are_recognised(), test_questions_about_other_people_are_not_scoped()

### Community 321 - ".feed"
Cohesion: 0.38
Nodes (3): Any, Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…

### Community 322 - "Alert"
Cohesion: 0.25
Nodes (5): Alert, What the debounce is keyed on: this metric, for this person and thing, in this…, Two lapsed policies on one person are two alerts, and saying one must not…, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

### Community 323 - "PackUnavailable"
Cohesion: 0.38
Nodes (6): Catalog, _load_one(), PackUnavailable, Path, RuntimeError, A pack names what the catalogue does not declare, or the pack does not exist.

### Community 324 - "15. A name scopes a question, and a grandparent is not a parent"
Cohesion: 0.50
Nodes (4): 15. A name scopes a question, and a grandparent is not a parent, Consequences, Context, Decision

### Community 325 - "generate_lim_documents.py"
Cohesion: 0.38
Nodes (6): jinja2, find_browser_executable(), generate_documents(), Path, Project Parrot - Synthetic Document Generator for Lim Household…, Find Microsoft Edge or Google Chrome executable on Windows.

### Community 326 - "test_a_core_document_stays_enabled_when_every_pack_is_off"
Cohesion: 0.38
Nodes (7): document_row(), fact_row(), ADR 0017: disabling insurance_agent switches off its voice, never a household's…, Following a citation must never end in a blank screen because a pack was…, test_a_core_document_stays_enabled_when_every_pack_is_off(), test_one_document_is_shown_even_when_its_pack_is_off(), test_vault_lists_documents_with_their_facts()

### Community 327 - ".observe"
Cohesion: 0.40
Nodes (4): _Pending, Path, Advance the debounce by `elapsed` seconds and return the files now ready. Time…, Every file in the watched folder that is worth looking at at all.

### Community 328 - "installed_packs"
Cohesion: 0.33
Nodes (6): installed_packs(), Every pack directory holding a pack.yaml, in a stable order. Directories whose…, test_every_installed_pack_still_loads(), test_every_pack_speaks_only_for_catalogue_types(), test_the_template_directory_is_not_an_installed_pack(), test_the_catalogue_names_nine_packs_none_of_them_built()

### Community 329 - "main"
Cohesion: 0.33
Nodes (6): load(), _mime(), Register and read every document of `role` from the commit's bytes, one at a…, clone_vault(), main(), Copy the development vault into `target`. Nothing is written to `source`.…

### Community 330 - "pathlib"
Cohesion: 0.04
Nodes (86): argparse, HouseholdConsents, `core.graph.advice.ConsentBook` over a live connection, for the graph to ask…, DenseRetriever, NoReranker, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this…, enabled_pack_ids(), enabled_packs() (+78 more)

### Community 332 - "test_a_household_that_cannot_be_true_is_refused"
Cohesion: 0.50
Nodes (5): _declaration(), parametrize, Path, The development vault's own household fails the last case: 'Marcus Lim Jun Wei'…, test_a_household_that_cannot_be_true_is_refused()

### Community 333 - "AnswerGraph"
Cohesion: 0.11
Nodes (49): AnswerGraph, _calendar_events(), Declined, The pack's own decline, signed with its disclaimer, and a question it can…, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed…, One sentence that has passed the gate, with the citations it passed on. It will…, A request for a recommendation or a judgement, declined before anything is…, A calendar answer as the stream every other answer is: read, sentences,… (+41 more)

### Community 334 - ".ask"
Cohesion: 0.50
Nodes (3): _as_sentence(), Every event, collected. `scripts/ask.py` and the screen ask the same question…, "which age band applies" -> "Which age band applies.": a pack's wording and a…

### Community 335 - "Asks"
Cohesion: 0.50
Nodes (3): Asks, Protocol, The one method of `AnswerGraph` the harness uses. A test supplies a fake.

### Community 337 - "Quarantine and the vision second pass"
Cohesion: 0.13
Nodes (18): ADR 0004 - Local setup can run before the assistant is ready, ADR 0006 - pypdfium2 renders the quarantine page images, ADR 0007 - The graph ships before retrieval and before a checkpoint table, Retrieval is a port, not an import, ADR 0009 - next-themes and lucide-react are the only two web dependencies beyond the stack, .graphifyignore excludes the corpus, Derive the roster, then confirm it, Scoping happens after retrieval, and that has a ceiling (+10 more)

### Community 340 - "quiet_engine"
Cohesion: 0.50
Nodes (4): fixture, MonkeyPatch, quiet_engine(), No real probes, no startup writes, no deliberate pause before exiting. The…

### Community 459 - "The final ILP report"
Cohesion: 0.20
Nodes (10): SYNTHETIC DOCUMENT footer, Governance artefact set, Write unverified rather than assert, The 40-document holdout corpus, The case for synthetic evaluation data, Two withdrawn synthetic-data controls, The final ILP report, A debatable thesis statement (+2 more)

### Community 550 - "Adversarial testing from week 7"
Cohesion: 0.20
Nodes (11): The answer graph: router, retrieve, rerank, grounding gate, Capability modules: Reminder and Alert, Adversarial testing from week 7, Contradiction attack, Prompt injection carried inside a document, Scope attack: asking it to act, Open question: the premium jump is not an alert, Open question: snooze and dismiss are not in the contract (+3 more)

### Community 552 - "Two-stage quarantine with a vision-language second pass"
Cohesion: 0.14
Nodes (16): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Lane A - Integration and product, Triage prompt: four buckets, no code written, Two-stage quarantine with a vision-language second pass, Christian's generated task list, Batch 4: the deliberately hard documents, A full policy wording registers as policy_schedule (+8 more)

### Community 553 - "Nobody edits core/contracts.py in a feature pull request"
Cohesion: 0.33
Nodes (6): The code pass of the knowledge graph, Nobody edits core/contracts.py in a feature pull request, The semantic pass of the knowledge graph, Ninety protected minutes a week of integration, Task: define the pack catalogue - the nine deferred packs, The household ledger - specified, not built in v1

## Ambiguous Edges - Review These
- `Provenance register for corpus sg_protection_guidance` → `Lane A - Christian, integration and product`  [AMBIGUOUS]
  packs/insurance_agent/grounding/sg_protection_guidance/sources.yaml · relation: references
- `Provenance register for corpus sg_protection_guidance` → `Lane D - Zee, domain packs and interface`  [AMBIGUOUS]
  team/README.md · relation: conceptually_related_to
- `LIA 2022 Protection Gap Study Key Findings` → `Protection rule of thumb: 9x annual income for death and TPD, 4x for critical illness`  [AMBIGUOUS]
  packs/insurance_agent/grounding/sg_protection_guidance/sources.yaml · relation: cites
- `Sources of Truth Generate Their Outputs` → `pack.yaml Is the Only Place a Field Name Is Written`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `Domain Packs` → `Core Document Catalogue (ADR 0017)`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `The Lim Household, Tampines` → `Republic of Xinkapow, the Invented Jurisdiction`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to
- `Republic of Xinkapow, the Invented Jurisdiction` → `Real Organisations May Be Named`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to
- `Motor Vehicle Hire Purchase Agreement Template` → `Fill the Register Before Generating Documents`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to
- `Corpus Batches Are Not in Git` → `The Corpus Is Synthetic and Committed`  [AMBIGUOUS]
  NOTICE.md · relation: semantically_similar_to

## Knowledge Gaps
- **1025 isolated node(s):** `Action`, `Stage`, `DependencyCheck`, `Phase`, `Status` (+1020 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 2695 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Provenance register for corpus sg_protection_guidance` and `Lane A - Christian, integration and product`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Provenance register for corpus sg_protection_guidance` and `Lane D - Zee, domain packs and interface`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `LIA 2022 Protection Gap Study Key Findings` and `Protection rule of thumb: 9x annual income for death and TPD, 4x for critical illness`?**
  _Edge tagged AMBIGUOUS (relation: cites) - confidence is low._
- **What is the exact relationship between `Sources of Truth Generate Their Outputs` and `pack.yaml Is the Only Place a Field Name Is Written`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Domain Packs` and `Core Document Catalogue (ADR 0017)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `The Lim Household, Tampines` and `Republic of Xinkapow, the Invented Jurisdiction`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Republic of Xinkapow, the Invented Jurisdiction` and `Real Organisations May Be Named`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._