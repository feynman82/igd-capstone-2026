# Graph Report - igd-capstone-2026  (2026-10-14)

## Corpus Check
- 334 files · ~754,655 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 41 file(s) not represented in the graph (top: (none) 15, .jsonl 8, .csv 6)

## Summary
- 5634 nodes · 14083 edges · 291 communities (236 shown, 29 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 1944 edges (avg confidence: 0.64)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7a929f99`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .json
- HybridRetriever
- ScriptedOllama
- test_answer_graph.py
- validate
- advice/__init__.py
- Insurance and Coverage pack (insurance_agent)
- test_advice_module.py
- api.ts
- test_ingest_pipeline.py
- FakeConn
- ingest/quarantine.py
- FolderAdapter
- test_telegram_capture.py
- test_grounding_index.py
- test_eval_harness.py
- bench_runtime.py
- vault.py
- get
- schedule.py
- ingest/extract.py
- test_grounding_values.py
- test_modules.py
- ConsentConn
- TelegramAdapter
- SentenceScanner
- household.py
- StreamingGraph
- test_lifecycle.py
- score.py
- _household_scope
- Settings
- test_pages.py
- pytest
- parse.py
- FakeConn
- eval/modules.py
- test_scan_parse.py
- FakeGraph
- alert/__init__.py
- retrieve.py
- Calculation
- test_household.py
- sys
- test_eval_modules.py
- _basis
- support.js
- build_router
- report.py
- compilerOptions
- Domain packs — start here
- registry.py
- test_grounding.py
- answer.py
- cli.py
- run.py
- ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic
- ConfigurationError
- Any
- PackManifest
- values.py
- extract_values
- lock.ts
- test_a_client_that_leaves_after_the_card_commits_one_record
- routes.py
- PARROT Interface Design Pack
- export-design-preview.cjs
- The Four Surfaces
- InstalledPack
- advice-consent.tsx
- devDependencies
- test_pack_catalogue.py
- Hybrid Retrieval: Dense Plus Full-Text
- scope.py
- ADR 0011: The household is people and aliases, and the owner is one of them
- Passage
- Any
- today/page.tsx
- ParsedPage
- preview.tsx
- events
- Hash-based idempotency
- FactRow
- reindex_document
- _closes
- Ollama
- Alert
- reference_for
- components.json
- ModuleSummary
- The household, and the word "my"
- contracts.py
- boot
- test_eval_report.py
- The Lim Household, Tampines
- Starting Parrot
- Lane C - Governance and assurance
- test_contracts.py
- Core Document Catalogue (ADR 0017)
- Notebook prompts — the four full policies for Marcus Lim
- is_first_person
- PARROT Architecture Review
- Data inventory: identity data, DOBs and loans
- test_rerank.py
- The autonomy statement
- web/ - the PARROT interface
- The document register as ground truth
- ingest.py
- ModuleAdviser
- Reminder, Alert and Tracker Registers
- main.py
- example_pack template manifest
- paperbrain/extract.py
- §5 · Evaluation and results
- tokens/page.tsx
- Try PARROT
- rerank.py
- pathlib
- adr/README.md
- DatabaseUnavailable
- test_worker_queue.py
- Retention and erasure policy
- _as_consent
- The deliberately naive retrieval baseline
- Running the evaluation harness
- phrasings.py
- The five-lane split (five people, nine weeks, three builders)
- A field name is written down once
- The demonstration run sheet
- test_advice_core.py
- Filling the corpus register
- Writing a governance artefact
- collections_abc
- Working agreement for coding agents
- igd-capstone-2026
- Policy schedule HTML template
- scored
- .retrieve
- PaperBrain
- ADR 0013: A question is understood before it is searched, and scoped before it is cut
- answer.tsx
- packs.py
- FakeCursor
- test_api.py
- Set C: adversarial
- Policy Schedule Template
- alert module manifest
- dependencies
- _as_vault_document
- app/layout.tsx
- _as_sentence
- Authoring a domain pack
- test_help_runs_without_importing_core_before_sys_path_is_set
- withheld
- DesignPreview evaluation harness
- worker.py
- _answer_events
- Siew — Lane C · Governance and assurance
- Writing an ADR
- createExternalModules
- FolderCapture
- harness.py
- sha256
- test_both_ask_endpoints_hand_the_graph_the_same_advice_ports
- Evaluation
- RagasJudge
- The Grounding Gate
- (app)/layout.tsx
- modules/__init__.py
- test_installing_never_re_enables_a_pack_somebody_switched_off
- DocumentCatalog
- 19 · A relevance floor on the reranker does not buy abstention, and the reason is not calibration
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- Any
- Answer
- Path
- filesystem
- ._advise
- pipeline.py
- Project PARROT — team split
- Basic Financial Planning Guide
- run_parrot.py
- One Database
- Question
- Household canon
- runtime/__init__.py
- corpus/__init__.py
- packs/__init__.py
- Lane E - Corpus and adversarial testing
- No code generates corpus documents
- next
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
- createPseudoSheet
- Comparison of Integrated Shield Plans
- Christian — task list
- Desmond — Lane E · Corpus and adversarial testing
- Desmond — task list
- Siew — task list
- Yew Mun — task list
- Graphify — the shared knowledge graph
- First run
- Understanding health insurance
- Zee — Lane D · Domain packs and interface
- Zee — task list
- Household canon
- 0001_init.sql
- typing
- Contributing
- The corpus
- 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module
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
- 14 · A pack supplies what the core knows about a domain, and the core stays generic
- 17 · A pack is grounding and persona; the core owns documents
- Artefacts
- Why the prototype is evaluated on synthetic data
- About Integrated Shield Plan
- The team
- usable
- `core/graph/` — the LangGraph runtime
- 0002_household.sql
- 0003_advice.sql
- 6. pypdfium2 renders the page images the quarantine second pass reads
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- 13. A question is understood before it is searched, and scoped before it is cut
- Data inventory — identity data, dates of birth and loans
- Notice
- Collection
- `core/ingest/` — the ingestion worker
- `core/retrieve/` — hybrid retrieval
- date
- 7. The answer graph ships before hybrid retrieval and before a checkpoint table
- Decimal
- Protocol
- `docs/governance/` — the assurance artefacts
- `core/adapters/` — capture adapters
- Home Contents Insurance Policy
- sets/README.md
- Pack grounding corpus rules
- Contracts and Migrations Are Their Own PR
- ADR index (0001-0018, with status)
- The final ILP report
- Adversarial testing from week 7
- Two-stage quarantine with a vision-language second pass
- Nobody edits core/contracts.py in a feature pull request

## God Nodes (most connected - your core abstractions)
1. `Settings` - 233 edges
2. `InstalledPack` - 141 edges
3. `Passage` - 124 edges
4. `ScriptedOllama` - 112 edges
5. `Ollama` - 109 edges
6. `ModelUnavailable` - 102 edges
7. `FakeConn` - 94 edges
8. `AnswerGraph` - 94 edges
9. `Calculation` - 77 edges
10. `Sentence` - 76 edges

## Surprising Connections (you probably didn't know these)
- `money()` --references--> `Work in this order, stopping for the author at each step`  [INFERRED]
  modules/advice/__init__.py → .claude/skills/authoring-a-domain-pack/SKILL.md
- `FactInput` --references--> `2. Limiting a fact input to one year`  [INFERRED]
  core/contracts.py → packs/iras_tax/CONTRACT_REQUESTS.md
- `FieldSpec` --references--> `How to give the feedback`  [INFERRED]
  core/contracts.py → .claude/skills/integration-review/SKILL.md
- `Rachel - Reminder module on Today` --semantically_similar_to--> `Phase 3 — Reminders`  [INFERRED] [semantically similar]
  web/docs/user-stories.md → tools/paperbrain/docs/ROADMAP.md
- `Lane A - Integration and product` --semantically_similar_to--> `PaperBrain`  [INFERRED] [semantically similar]
  team/christian/README.md → tools/paperbrain/README.md

## Import Cycles
- 3-file cycle: `core/ingest/__init__.py -> core/ingest/pipeline.py -> core/ingest/obligations.py -> core/ingest/__init__.py`

## Communities (291 total, 29 thin omitted)

### Community 0 - ".json"
Cohesion: 0.21
Nodes (7): Any, Client, Load the generator and the embedder now, and say where the generator landed., Generate against a JSON schema. This is how extraction is held to a pack's field, The same constrained generation, yielded as it is written.          Identical, Parse a schema-constrained reply. A model that returns prose here is a failure., One request for the whole batch. Returns vectors in the order given.

### Community 1 - "HybridRetriever"
Cohesion: 0.15
Nodes (23): hybrid_score(), HybridRetriever, identifiers(), prints(), Hybrid retrieval: pgvector cosine search and Postgres full-text search, fused by, The tokens in a question that look like something printed rather than said: a po, Whether the chunk prints the identifier, ignoring case and the spacing inside it, The cosine similarity, lifted to `IDENTIFIER_HIT` when the chunk prints an ident (+15 more)

### Community 2 - "ScriptedOllama"
Cohesion: 0.05
Nodes (97): AdviceRecord, Every advised or withheld answer's full basis, so it can be reconstructed later, Abstained, AdviceCard, AdviceWithheld, ConsentRequired, Declined, Finished (+89 more)

### Community 3 - "test_answer_graph.py"
Cohesion: 0.07
Nodes (72): AnswerGraph, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed…, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed y, Built once, asked many times. Holds no connection: retrieval does., Reading, The result of asking "whose is this?" of a question and its passages., The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting… (+64 more)

### Community 4 - "validate"
Cohesion: 0.09
Nodes (41): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+33 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.10
Nodes (50): RuleInput, Hashable, _ambiguous(), _amount(), _band(), _band_label(), cents(), _compare_market() (+42 more)

### Community 6 - "Insurance and Coverage pack (insurance_agent)"
Cohesion: 0.16
Nodes (16): Insurance advice consent gate (consent_version 1.0.0), advice_decline guardrail message, Category matcher (printed product_name against asked words, first rule wins), Advice shape ci_cover (gap calculator), Category critical_illness (critical illness plan), Advice shape death_tpd_cover (gap calculator), Exclusion detection (headings, claims, negations), insurance_agent guardrails (must_cite, abstain_below 0.45, never_acts, verdict_by_code) (+8 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.15
Nodes (55): calculate(), One person's advice. The graph asks whose first when a question names several pe, assert_nothing_negative(), basis(), fact(), figures_of(), _gap_basis(), _held() (+47 more)

### Community 8 - "api.ts"
Cohesion: 0.06
Nodes (49): react, RELATION_CHOICES, Place, PLACES, PanelMessage(), RuleChip(), SourceChip(), SourcePanel() (+41 more)

### Community 9 - "test_ingest_pipeline.py"
Cohesion: 0.08
Nodes (53): classify(), Ollama, Never raises. An unavailable model is a classification failure, so it quarantine, extract(), Never raises. A failure is a reason, and a reason routes the document to quarant, FakeOllama, insurance(), iras() (+45 more)

### Community 10 - "FakeConn"
Cohesion: 0.10
Nodes (30): SourceText, index_pack(), IndexReport, Any, date, Ollama, Path, Index a pack's published sources, and stage the values they print for a person t (+22 more)

### Community 11 - "ingest/quarantine.py"
Cohesion: 0.07
Nodes (62): blocked_reasons(), forget(), Any, Ollama, Path, QuarantinedDocument, queue(), The second stage of quarantine: the page image, read by the vision-language mode (+54 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.14
Nodes (29): FolderAdapter, FolderSettings, The watched-folder capture adapter.  A person drops a scan into a folder and i, Satisfies `CaptureAdapter`. Holds no database handle — it is given a `Registrar`, _loop(), main(), Watch the inbox folder, register and read everything dropped into it.      uv, Poll until interrupted. `--once` waits out one stability window and then stops. (+21 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.12
Nodes (33): httpx, MockTransport, build(), FakeTelegram, photo_update(), Any, Path, Request (+25 more)

### Community 14 - "test_grounding_index.py"
Cohesion: 0.08
Nodes (36): CaptureFixture, A pack's grounding corpus: the published sources it may cite, read from its own, approve(), pending(), PendingValue, Any, date, A person's approval, standing between a model's extraction and any calculator th (+28 more)

### Community 15 - "test_eval_harness.py"
Cohesion: 0.10
Nodes (35): The evaluation harness. `python -m eval.run` is the entry point; `eval/README.md, Expected, load_set(), MalformedQuestion, Any, SetId, ValueError, Question (+27 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (35): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+27 more)

### Community 17 - "vault.py"
Cohesion: 0.07
Nodes (38): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+30 more)

### Community 18 - "get"
Cohesion: 0.24
Nodes (23): bundledBlob(), getDC(), Dispatcher(), getError(), load(), createHelmetManager(), applyCanvasBg(), compile() (+15 more)

### Community 19 - "schedule.py"
Cohesion: 0.15
Nodes (17): build(), Any, The one Celery application, built from `Settings`.  Every setting here is a co, Construct the Celery application. Imported lazily by callers so that nothing whi, beat_schedule(), cron_expressions(), crontab_from(), manifest() (+9 more)

### Community 20 - "ingest/extract.py"
Cohesion: 0.07
Nodes (39): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected, copy, FieldSpec (+31 more)

### Community 21 - "test_grounding_values.py"
Cohesion: 0.19
Nodes (35): LogCaptureFixture, _dropped(), _log_values(), Decimal, fixture, LogCaptureFixture, parametrize, Published values: the model reads a source, and code keeps only what the passage (+27 more)

### Community 22 - "test_modules.py"
Cohesion: 0.08
Nodes (39): already_said(), current_lead(), Due, next_window(), Overdue, Any, date, datetime (+31 more)

### Community 23 - "ConsentConn"
Cohesion: 0.15
Nodes (19): consent(), ConsentConn, parametrize, The parameters of the one statement containing `needle`. Fails loudly if it neve, `core.advice_consent`'s real SQL, against a household with or without an owner., Withdrawal never checks whether the wording shown was current -- taking consent, Agreeing to advice from something switched off is not a choice a screen should o, A person switched the pack off; taking back consent from it is still theirs to d (+11 more)

### Community 24 - "TelegramAdapter"
Cohesion: 0.07
Nodes (36): BaseTransport, IngestJob, Magic bytes first, filename suffix second, `application/octet-stream` last., What a capture returns: a registered document, and whether we had seen it before, sniff_mime(), _Pending, datetime, Path (+28 more)

### Community 25 - "SentenceScanner"
Cohesion: 0.08
Nodes (32): Any, Pulling finished sentences out of a JSON reply that is still being written.  T, What document would have answered this, if the model said. Read once, at the end, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them., Append `delta` and return the sentences it completed. Usually none, sometimes on, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes… (+24 more)

### Community 26 - "household.py"
Cohesion: 0.08
Nodes (47): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+39 more)

### Community 27 - "StreamingGraph"
Cohesion: 0.08
Nodes (29): a_citation(), advice_card(), Any, Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive together,, By then the 200 has been sent. An exception that only logged would leave a scree, A published value's chip: no document and no page, only who published it and whe (+21 more)

### Community 28 - "test_lifecycle.py"
Cohesion: 0.12
Nodes (27): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor., What the person asked for, once. The first request wins; later ones change nothi, fastapi_testclient, _client(), _eventually(), _launcher(), parametrize (+19 more)

### Community 29 - "score.py"
Cohesion: 0.08
Nodes (46): cites(), contained_by_flag(), _contains(), declined_in_prose(), doc_stem(), grade(), held_back(), inventory_only() (+38 more)

### Community 30 - "_household_scope"
Cohesion: 0.06
Nodes (50): _household_scope(), MonkeyPatch, Person, `HouseholdScope` over a roster held in memory, with every document resolved by…, `HouseholdScope` over a roster held in memory, with every document resolved by n, The roster has no grandparent relation, so the household says it the only way…, The roster has no grandparent relation, so the household says it the only way it, 13 September: "what is Marcus's premium?" has no "my", so nothing was scoped… (+42 more)

### Community 31 - "Settings"
Cohesion: 0.09
Nodes (45): create_app(), checks(), ready(), setup(), system_status(), ModelWarmth, Ollama, Whether the generator has been loaded yet, and where it landed. Written by one t (+37 more)

### Community 32 - "test_pages.py"
Cohesion: 0.08
Nodes (40): document_page(), base64, page_images(), Base64 page images, in page order. Empty when this document cannot be rendered., page_count(), PageUnavailable, _pdfium(), Any (+32 more)

### Community 33 - "pytest"
Cohesion: 0.14
Nodes (29): contained(), leaked(), Which of a Set C item's `must_not_say` strings the answer contains, in the…, Set C's first reading, mechanised: did the run hold back **and** say nothing…, pytest, _item(), Answer, Path (+21 more)

### Community 34 - "parse.py"
Cohesion: 0.10
Nodes (21): Block, DoclingParser, _kind(), _pages_from(), Parser, PlainTextParser, Protocol, Turn captured bytes into pages of text, or say why it could not be done.  Ever (+13 more)

### Community 35 - "FakeConn"
Cohesion: 0.19
Nodes (16): AlertConfig, `warn_at` is a share of the ceiling. A ceiling of zero means any value at all is, Every declared threshold that is crossed, has evidence, and has not just been sa, sweep(), _triggered(), FakeConn, One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order., A live travel policy must not make a lapsed motor policy read as covered. (+8 more)

### Community 36 - "eval/modules.py"
Cohesion: 0.12
Nodes (34): _day(), main(), measure(), Measured, _number(), Obligation, obligations(), obligations_possible() (+26 more)

### Community 37 - "test_scan_parse.py"
Cohesion: 0.14
Nodes (17): csv, FixtureRequest, Image, needs_ocr, _as_printed(), page_pixels(), photographed(), fixture (+9 more)

### Community 39 - "FakeGraph"
Cohesion: 0.12
Nodes (19): FakeGraph, TestClient, Stands in for `AnswerGraph` at the seam `api/routes.py` owns., The JSON endpoint ends the way the stream does: an abstention is signed too., "when does it expire?" is only a question in the light of the one before it., The only network guard on the app. Zee's interface proxies through Next, so ever, test_a_turn_can_only_be_the_person_or_parrot(), test_ask_gives_consent_and_withheld_advice_their_own_kinds() (+11 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.22
Nodes (19): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), Any, date (+11 more)

### Community 41 - "retrieve.py"
Cohesion: 0.14
Nodes (23): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a, ndarray, numpy, sqlite3, load_matrix(), pack(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.  Des (+15 more)

### Community 42 - "Calculation"
Cohesion: 0.14
Nodes (28): Calculation, Figure, Input, One fact or rule value a calculation was built on, carrying its own citation., One number a calculator produced, and the words a sentence must use to state it., What a calculator returns when every fact and rule it needed was on file and app, Basis, _calculation() (+20 more)

### Community 43 - "test_household.py"
Cohesion: 0.15
Nodes (23): Keep the owner's passages and the household's; set aside everybody else's. A…, Keep the passages of these people and of the household; set aside everybody else, Keep the passages of these people and of the household; set aside everybody…, scope_passages(), scope_to(), conn(), _conn_returning(), _passage() (+15 more)

### Community 44 - "sys"
Cohesion: 0.09
Nodes (25): argparse, jinja2, find_browser_executable(), generate_documents(), Path, Project Parrot - Synthetic Document Generator for Lim Household ===============, Find Microsoft Edge or Google Chrome executable on Windows., platform (+17 more)

### Community 45 - "test_eval_modules.py"
Cohesion: 0.08
Nodes (42): alert_fpr(), AlertVerdict, _mark(), ModuleMetrics, obligation_precision(), Metric 7, over the obligations a document produced. A calendar deadline is exclu, One verdict per fired alert: whether the register, recomputed, crosses the same, Metric 8. `None` when nothing fired: a rate over zero alerts is not 0.0, it is u (+34 more)

### Community 46 - "_basis"
Cohesion: 0.22
Nodes (11): _basis(), _latest(), _published(), FactRow, parametrize, The subject's newest `doc_type` in the register, as the fact extraction wrote it, _register(), _shape() (+3 more)

### Community 47 - "support.js"
Cohesion: 0.12
Nodes (28): collectProps(), compileAttr(), compileTemplate(), contentKey(), cssToObj(), encodeCamelAttrs(), encodeCase(), evalDcLogic() (+20 more)

### Community 48 - "build_router"
Cohesion: 0.09
Nodes (34): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, QuarantinedDocument, QuarantineResponse, What changed, in the words the screen confirms it with.      `was` is returned (+26 more)

### Community 49 - "report.py"
Cohesion: 0.13
Nodes (22): _cell(), collect(), main(), _overall(), _paragraph(), Provenance, Any, Path (+14 more)

### Community 50 - "compilerOptions"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 51 - "Domain packs — start here"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 52 - "registry.py"
Cohesion: 0.08
Nodes (40): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders somewhe, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, RuntimeError, Load the installed capability modules at runtime.  The mirror of `core/packs.p (+32 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.18
Nodes (25): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError, Read and validate a pack's grounding corpus from its own folder on disk.  A pa, A pack's grounding corpus on disk does not match what its `sources.yaml` records (+17 more)

### Community 54 - "answer.py"
Cohesion: 0.05
Nodes (73): AdviceShape, One kind of advice question, and everything its calculator needs to answer it., AdviceLog, Adviser, ConsentBook, kind_of(), Missing, date (+65 more)

### Community 55 - "cli.py"
Cohesion: 0.10
Nodes (33): ArgumentParser, answer(), build_context(), format_sources(), Ollama, Answer a question from retrieved chunks, with citations back to the file.  The, build_parser(), _client() (+25 more)

### Community 56 - "run.py"
Cohesion: 0.11
Nodes (30): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), _indexed(), main() (+22 more)

### Community 57 - "ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.08
Nodes (40): Code-written absence sentence: 'None of the N policies on file is a dental plan.', ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic, The advise route intent returns the pack's advice_decline, answering.categories: ordered whole-word rules over one printed field, Category filter applied before the keep-6 cut, answering.exclusions: headings under which a cover claim is not believed, Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration) (+32 more)

### Community 58 - "ConfigurationError"
Cohesion: 0.13
Nodes (14): TelegramSettings, attribution(), Any, A daemon thread that long-polls the Telegram bot until `stop()` or process exit., One long poll. A failure waits rather than hammering the API with the same reque, Whose phone this arrived on, recorded before anything is read off it. See ADR 00, TelegramCapture, ConfigurationError (+6 more)

### Community 59 - "Any"
Cohesion: 0.20
Nodes (12): db(), _document(), FakeCursor, Any, date, datetime, fixture, _source() (+4 more)

### Community 60 - "PackManifest"
Cohesion: 0.19
Nodes (13): PackManifest, A domain pack, authored as one YAML file: grounding, persona, answering and advi, _insurance(), Path, A downloaded pack carries its sources, so no corpus is left at the repository ro, ADR 0017: documents are the core's. A pack.yaml carrying them does not load., test_a_grounding_corpus_is_named_by_id_not_by_path(), test_a_grounding_corpus_travels_inside_its_pack() (+5 more)

### Community 61 - "values.py"
Cohesion: 0.08
Nodes (34): A rule or table value a pack's sources publish.      Extracted automatically,, ValueKey, _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), number_tokens() (+26 more)

### Community 62 - "extract_values"
Cohesion: 0.15
Nodes (22): GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records, extract_values(), Ollama, Every value the source prints for these keys, kept only when its passage prints, _long_text(), Any, Exception (+14 more)

### Community 63 - "lock.ts"
Cohesion: 0.08
Nodes (46): ref_node_crypto, dynamic, GET(), grant(), POST(), runtime, ALLOWED, Context (+38 more)

### Community 64 - "test_a_client_that_leaves_after_the_card_commits_one_record"
Cohesion: 0.17
Nodes (12): next_kind(), The kind of the next event on the wire., Starlette never closes a body iterator a disconnected client stopped pulling. `_, The ruling's case as it happens on a socket: Starlette sends the card and at onc, What the API owns when a stream is closed with the graph still parked on the car, C5 fix round 2 closed the gap this test used to mark: `AdviceCard` is now yielde, The graph's own cleanup can fail -- for example the record insert raises -- and, test_a_client_that_leaves_after_the_card_commits_one_record() (+4 more)

### Community 65 - "routes.py"
Cohesion: 0.10
Nodes (58): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, AskRequest, AskResponse, Claim, CloseRequest (+50 more)

### Community 66 - "PARROT Interface Design Pack"
Cohesion: 0.08
Nodes (31): Not finding you is an answer (first-person abstention), Capture is where the user already is, Citation chips are the trust surface, Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Nothing moves without a reason (motion specification), Silence beats a guess (+23 more)

### Community 67 - "export-design-preview.cjs"
Cohesion: 0.08
Nodes (23): @eslint/eslintrc, ref_node_fs, ref_node_path, ref_node_url, compat, eslintConfig, bundle(), classes (+15 more)

### Community 68 - "The Four Surfaces"
Cohesion: 0.11
Nodes (19): Packs and Modules May Not Import web/ or api/, `api/` — the FastAPI application, The FastAPI Application, Five properties worth knowing before you change anything, Rules, The surface, GET /api/today Never Marks Anything Notified, apply (+11 more)

### Community 69 - "InstalledPack"
Cohesion: 0.04
Nodes (69): Conn, Category, A kind of document a household holds, recognised by words printed in its name., _conversation(), The documents on file, narrowed to the same people the passages were., The documents on file, narrowed to the same people the passages were., The holdings whose documents scoping keeps for `question`, as it keeps passages., "On file for Marcus Lim: MERIDIAN ASSURANCE, Private Car Insurance Policy (polic (+61 more)

### Community 70 - "advice-consent.tsx"
Cohesion: 0.24
Nodes (13): ConsentPrompt(), agree(), settle(), AdviceConsentSection(), fetchConsents(), withdraw(), Load, STATUS (+5 more)

### Community 71 - "devDependencies"
Cohesion: 0.10
Nodes (21): eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node, @types/react (+13 more)

### Community 72 - "test_pack_catalogue.py"
Cohesion: 0.10
Nodes (22): installed_packs(), Every pack directory holding a pack.yaml, in a stable order.      Directories, DocumentTypeSpec, parametrize, pydantic, Strict, test_every_installed_pack_still_loads(), test_every_pack_speaks_only_for_catalogue_types() (+14 more)

### Community 73 - "Hybrid Retrieval: Dense Plus Full-Text"
Cohesion: 0.13
Nodes (16): Every Fact Row Cites Its Source, No New Runtime Dependency Without an ADR, Never Generate SQL at Runtime, A Correction Cannot Invent a Row, baseline.py Is Disposable and Never a Measurement, Every Node Writes One Line to traces, ports.py, the Seam With Lane B, The Ingestion Pipeline (+8 more)

### Community 74 - "scope.py"
Cohesion: 0.14
Nodes (25): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Any (+17 more)

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.16
Nodes (20): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), The owner is a row, not a config value baked at install, people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), A resolved person is shown as a chip, like a citation, The roster is derived from documents, then confirmed (+12 more)

### Community 76 - "Passage"
Cohesion: 0.05
Nodes (68): Exclusions, A sentence claiming cover whose every citation sits under one of `headings` is d, check(), check_advice(), check_content(), check_one(), Claim, _loose_numbers() (+60 more)

### Community 77 - "Any"
Cohesion: 0.15
Nodes (18): Measurement, by_subject(), db(), FakeCursor, load_register(), Any, date, fixture (+10 more)

### Community 78 - "today/page.tsx"
Cohesion: 0.11
Nodes (27): dynamic, HouseholdPage(), metadata, runtime, dynamic, GoneNote(), Header(), isUrgent() (+19 more)

### Community 79 - "ParsedPage"
Cohesion: 0.14
Nodes (21): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own st, One flat list of chunks, ordinal running across the whole document., The page as `(is_heading, line)`, from the parser's structure when it has any. (+13 more)

### Community 80 - "preview.tsx"
Cohesion: 0.11
Nodes (19): DesignPreviewPage(), metadata, answers, DesignPreview(), Direction, directions, Item, items (+11 more)

### Community 81 - "events"
Cohesion: 0.09
Nodes (19): _pack_for(), The pack that speaks for the best-scoring passage's document type, or None for t, The pack that speaks for the best-scoring passage's document type, or None for…, events(), Any, Exception, Generated, The same scripted reply, in five-character pieces.          Deliberately chopp (+11 more)

### Community 82 - "Hash-based idempotency"
Cohesion: 0.25
Nodes (8): PaperBrain handled failure modes, Hash-based idempotency, OCR is per page, not per file, SQLite for everything, Vectors as BLOBs, scored in numpy, Exhaustive cosine instead of an ANN index, The pb command line, PaperBrain dependency set

### Community 83 - "FactRow"
Cohesion: 0.16
Nodes (16): Categories, categorise(), The first rule whose printed words appear. `None` is an answer, not a failure., The first rule whose printed words appear. `None` is an answer, not a failure., fact_row(), FactRow, facts_for(), in_category() (+8 more)

### Community 84 - "reindex_document"
Cohesion: 0.12
Nodes (10): indexed(), IndexedDocument, Any, RuntimeError, Safe to show: names what went wrong, never what the document says., Parse, chunk and embed one document again, and replace its chunks. Returns how m, reindex_document(), ReindexFailed (+2 more)

### Community 85 - "_closes"
Cohesion: 0.14
Nodes (16): _closes(), _either(), "None of the 5 policies on file is a dental plan." Written by code, never by the, "None of the 5 policies on file is a dental plan." Written by code, never by…, "a dental plan", or "a term life plan or a whole life plan". "An" only before a,, "a dental plan", or "a term life plan or a whole life plan". "An" only before…, Which kinds of cover close a short shape's gap, written by code.      The pack, Which kinds of cover close a short shape's gap, written by code. The pack… (+8 more)

### Community 86 - "Ollama"
Cohesion: 0.16
Nodes (10): Ollama, A question, embedded the way the model was trained to embed a search query., Passages as `(title, text)`, embedded the way the model was trained to embed a d, Whether this embedding model expects `QUERY_PROMPT` and `DOCUMENT_PROMPT`., uses_task_prompts(), main(), Index a pack's published sources into pending values a reviewer can approve or r, skipif (+2 more)

### Community 87 - "Alert"
Cohesion: 0.25
Nodes (5): Alert, What the debounce is keyed on: this metric, for this person and thing, in this p, Two lapsed policies on one person are two alerts, and saying one must not silenc, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

### Community 88 - "reference_for"
Cohesion: 0.20
Nodes (11): date, _as_date(), _as_number(), Question, The ways a register value is printed. `2027-04-11` appears on a schedule as "11…, The register's text against an extracted value, each normalised the way the…, The reference answer Ragas judges recall and precision against. A fact…, reference_for() (+3 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "ModuleSummary"
Cohesion: 0.29
Nodes (7): _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack(), ModuleSummary, PackSummary

### Community 91 - "The household, and the word "my""
Cohesion: 0.07
Nodes (25): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 18 · The reranker runs in-process, because Ollama cannot serve a cross-encoder, Alternatives considered, Consequences, Context (+17 more)

### Community 92 - "contracts.py"
Cohesion: 0.13
Nodes (21): Advice, Answering, FactInput, Grounding, Guardrails, ModuleTrigger, Persona, BaseModel (+13 more)

### Community 93 - "boot"
Cohesion: 0.20
Nodes (10): boot(), dcNameFromPath(), getReactDOM(), parseDataProps(), parseDcDocument(), parseDcText(), rootNameForDocument(), safeDecode() (+2 more)

### Community 94 - "test_eval_report.py"
Cohesion: 0.10
Nodes (38): Collection, extraction_by_type(), extraction_f1(), FactRow, has_ground_truth(), _outcomes(), One row of the `facts` table, as the harness reads it: which document, which…, Whether a register row records any value a document could be scored against. A… (+30 more)

### Community 95 - "The Lim Household, Tampines"
Cohesion: 0.16
Nodes (15): loan_agreement Document Type, payslip Document Type, The Lim Household, Tampines, One Household Only; the Persona Sketches Are Gone, Rachel Ng Arrives Off Documents, Not a Persona Sketch, Three Surnames, One Household, doc_id Is the Filename, No Synthetic-Document Footer Requirement (+7 more)

### Community 96 - "Starting Parrot"
Cohesion: 0.11
Nodes (22): ADR 0005 - The watched folder is polled, not subscribed to, Stability debounce with injected time, ADR 0008 - Ingestion runs on a Celery worker, The queue carries a digest, not the document, Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion (+14 more)

### Community 97 - "Lane C - Governance and assurance"
Cohesion: 0.10
Nodes (22): The evaluation is the gate, The 40-document redacted holdout, The synthetic-to-real gap, Consent and redaction protocol, ISO/IEC 22989 to 5338 stage-to-process map, Lane C - Governance and assurance, Model card, Retention and erasure policy (+14 more)

### Community 98 - "test_contracts.py"
Cohesion: 0.09
Nodes (47): _advised(), _checked(), _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact() (+39 more)

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.15
Nodes (15): Sources of Truth Generate Their Outputs, Generated files, benefit_illustration Document Type, birth_certificate Document Type, claim_letter Document Type, cpf_statement Document Type, Core Document Catalogue (ADR 0017), donation_receipt Document Type (+7 more)

### Community 100 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 101 - "is_first_person"
Cohesion: 0.18
Nodes (12): is_first_person(), `(word, relation)` when the question asks about a relation's own documents,…, `(word, relation)` when the question asks about a relation's own documents, else, Whether this question is about the person asking. `other_names` are the display…, Whether this question is about the person asking.      `other_names` are the d, relation_asked(), parametrize, "What is Rachel's premium on my policy" is a question about Rachel.      A rel (+4 more)

### Community 102 - "PARROT Architecture Review"
Cohesion: 0.16
Nodes (16): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The domain pack manifest, The expansion model: two axes, not one list, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build, The VRAM budget, with headroom (+8 more)

### Community 103 - "Data inventory: identity data, DOBs and loans"
Cohesion: 0.27
Nodes (10): Data inventory: identity data, DOBs and loans, The lock is a screen lock, not encryption, next dev binds every interface, not loopback, Telegram capture route and delete-at-source, What crosses a boundary, Local Ollama judge model, db service (pgvector/pgvector:pg17), Compose reads .env from infra/, not the repo root (+2 more)

### Community 104 - "test_rerank.py"
Cohesion: 0.11
Nodes (26): CrossEncoderReranker, passage_text(), What the reranker reads: the one-line context, when a chunk carries one, then…, Implements `core.graph.ports.Reranker`. Reorders by the cross-encoder's score…, What the reranker reads: the one-line context, when a chunk carries one, then th, The cross-encoder's score as a probability. The model emits a logit; a floor is, Implements `core.graph.ports.Reranker`. Reorders by the cross-encoder's score, d, relevance() (+18 more)

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
Cohesion: 0.18
Nodes (16): itertools, re, Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks.  Paperwork is short and stru, _split_page(), discover() (+8 more)

### Community 109 - "ModuleAdviser"
Cohesion: 0.14
Nodes (20): _is_an_adviser(), ModuleAdviser, Adviser, date, Never called. It is here so `mypy` proves `ModuleAdviser` satisfies the port `co, A key's usable published values. How old a value may be depends on what it is: a, The `core.graph.advice.Adviser` port over Postgres.      Every fact is the cor, values_for() (+12 more)

### Community 110 - "Reminder, Alert and Tracker Registers"
Cohesion: 0.13
Nodes (20): Passport Uses date_of_expiry So policy_expiry Does Not Fire, filing_deadline Reminder, maturity_date Is Not expiry_date, passport Document Type, passport_expiry Reminder, policy_expiry Reminder, policy_schedule Document Type, Reminder, Alert and Tracker Registers (+12 more)

### Community 111 - "main.py"
Cohesion: 0.08
Nodes (35): Parrot's local HTTP interface., The local API. Liveness is intentionally separate from assistant readiness.  L, AsyncClient, asyncio, capture_check(), Check, collect_checks(), database_check() (+27 more)

### Community 112 - "example_pack template manifest"
Cohesion: 0.19
Nodes (13): I explain the renewal notice, I do not renew policies, Autonomy statement, never_acts as a machine-checked flag, abstention_rate, Set B, hard negatives, advice module manifest, example_pack template manifest, example_room advice shape (+5 more)

### Community 113 - "paperbrain/extract.py"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 114 - "§5 · Evaluation and results"
Cohesion: 0.17
Nodes (12): 5.10 What run 3 must add, 5.1 The claim, 5.2 What was measured, 5.3 The three-run spine, 5.4 Retrieval: what the two changes bought, 5.5 Abstention: the finding, 5.6 Extraction, by document type, 5.7 The two module metrics, and the lesson in them (+4 more)

### Community 115 - "tokens/page.tsx"
Cohesion: 0.18
Nodes (18): Motion(), ROWS, Colour(), FaceCard(), Focus(), INKS, metadata, RADII (+10 more)

### Community 116 - "Try PARROT"
Cohesion: 0.13
Nodes (15): 1 · Install five things, 2 · Download the AI models, 3 · Get the code and set it up, 4 · Put some documents in, 5 · Run it, 6 · Use it, Ask — a question about your own documents, If something goes wrong (+7 more)

### Community 117 - "rerank.py"
Cohesion: 0.21
Nodes (11): device_name(), load(), Any, The cross-encoder reranker: forty candidates read against the question, six kept, One relevance logit per text, higher is better. Batched so forty passages is a h, Say it, once per process. A passage cut at the cap is scored on its first part o, The tokenizer, the model and the device it sits on, loaded once per process.…, The tokenizer, the model and the device it sits on, loaded once per process. (+3 more)

### Community 118 - "pathlib"
Cohesion: 0.07
Nodes (24): The page a person sees while Parrot starts, served by the engine itself.  **Wh, The whole page. `screens_url` is escaped into a data attribute, never into scrip, render(), contextlib, The record of every advised or withheld answer (ADR 0016).  `advice_records` k, A dense-only retriever, so the graph can be run and tested before Lane B's hybri, One place that opens a connection to the one database.  `Settings.database_url, The one client that talks to Ollama.  Everything the platform infers goes thro (+16 more)

### Community 119 - "adr/README.md"
Cohesion: 0.06
Nodes (25): 1. Record architecture decisions, Consequences, Context, Decision, 2. One PostgreSQL instance for everything, Consequences, Context, Decision (+17 more)

### Community 120 - "DatabaseUnavailable"
Cohesion: 0.22
Nodes (8): DatabaseUnavailable, RuntimeError, Safe to show: the message never carries the connection string., What the register says about one obligation. `verdict` is the bucket it counts i, Verdict, main(), Today: what the two capability modules have to say, ordered by urgency.      u, refuse()

### Community 121 - "test_worker_queue.py"
Cohesion: 0.10
Nodes (30): Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker.      Celery is imported here, Intake, The Celery worker: the process that reads documents, and the nightly sweeps., FakeConnection, FakeCursor (+22 more)

### Community 122 - "Retention and erasure policy"
Cohesion: 0.20
Nodes (9): Open questions, Policy, Retention and erasure policy, Retention periods, Scope and legal frame, The erasure path: what `DELETE FROM documents` reaches, The finding to read first, What has to be built (+1 more)

### Community 123 - "_as_consent"
Cohesion: 0.29
Nodes (7): AdviceConsent, AdviceConsent, One advising pack, the wording a person is asked to agree to, and what the owner, _as_consent(), advice_consents(), record_consent(), One advising pack's consent wording and the owner's standing answer to it.

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.14
Nodes (15): Task: benchmark the workstation and publish the numbers, Task: build the answer graph with the grounding gate, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, The deliberately naive retrieval baseline, Committed runs are never deleted, Task: contextualised chunking and the reranker, Task: hybrid retrieval with reciprocal rank fusion (+7 more)

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 126 - "phrasings.py"
Cohesion: 0.20
Nodes (11): _keys(), LaneSpec, Row, How a question about a printed field is worded, per document type in `core/docum, One document type's wordings.      `printed` and `spoken` each render the *thi, Which register rows a lane's questions are drawn from.      The task asks each, A wording, or `None` when the row does not fill every field it needs., The spoken wording, or "Rachel's payslip" when the type has no product name of i (+3 more)

### Community 127 - "The five-lane split (five people, nine weeks, three builders)"
Cohesion: 0.09
Nodes (25): The golden set: answerable, hard negatives, adversarial, A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, Contracts before code, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane (+17 more)

### Community 128 - "A field name is written down once"
Cohesion: 0.33
Nodes (6): Qwen-SEA-LION-v4-4B-VL extraction ceiling, Register first, then generate, Ground truth for free, extraction_f1, A field name is written down once, Never hand-edit a generated file

### Community 129 - "The demonstration run sheet"
Cohesion: 0.05
Nodes (45): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+37 more)

### Community 130 - "test_advice_core.py"
Cohesion: 0.08
Nodes (45): Channel, current(), grant(), _latest(), NoOwner, Any, RuntimeError, The owner's consent to a pack's advice, append-only (ADR 0016).  Consent is th (+37 more)

### Community 131 - "Filling the corpus register"
Cohesion: 0.20
Nodes (9): Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one, The rule that cannot bend (+1 more)

### Community 132 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (9): Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six, Where governance touches the code (+1 more)

### Community 133 - "collections_abc"
Cohesion: 0.06
Nodes (64): collections, collections_abc, _ambiguous(), choose(), Generated, generic(), hand_written(), main() (+56 more)

### Community 134 - "Working agreement for coding agents"
Cohesion: 0.12
Nodes (16): Before you read files at random, Definition of done, Hard rules, No Claim Without a Citation, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents (+8 more)

### Community 135 - "igd-capstone-2026"
Cohesion: 0.13
Nodes (19): Working Agreement for Coding Agents, The Five Lanes and Their Owners, ADR 0010 - main is unprotected, and the discipline is human, Contracts before code, Lane A - Integration and product, Setting Up a Second Machine, PARROT Is an Internal Working Name, Authoring a pack (+11 more)

### Community 136 - "Policy schedule HTML template"
Cohesion: 0.24
Nodes (10): b1-0001 Private Car Insurance Policy Schedule, b1-0002 HomeShelter Contents Policy Schedule, b1-0003 Hospital Income Protection Plan Schedule, Full-length insurance policy notebook prompt, No Ref: line anywhere on the document, Cross-document corpus consistency, Four full-policy notebook prompts, Shared policy-drafting preamble (+2 more)

### Community 137 - "scored"
Cohesion: 0.20
Nodes (9): fixture, LogCaptureFixture, MonkeyPatch, A passage cut at the cap is scored on its first part only. That is how a quiet r, A scorer that ranks by the number the passage text ends with, and records what…, A scorer that ranks by the number the passage text ends with, and records what i, scored(), test_a_passage_within_the_limit_says_nothing() (+1 more)

### Community 138 - ".retrieve"
Cohesion: 0.33
Nodes (5): fuse(), Several searches as one list: each passage once, at the best score any phrasing…, Several searches as one list: each passage once, at the best score any phrasing, Every phrasing of the question, searched and fused. The person's own words alway, Every phrasing of the question, searched and fused. The person's own words…

### Community 139 - "PaperBrain"
Cohesion: 0.22
Nodes (8): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles, Login is a local passphrase

### Community 140 - "ADR 0013: A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.12
Nodes (23): guardrails.abstain_below was calibrated on un-prompted scores, ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts, chunks.tsv built from context_prefix || text, Context prefix: title - type - heading - page, rag_probe2 before/after similarity table (six policies, 13 September), scripts/reindex.py rebuilds chunks and vectors, Schedule-table questions remain weak (rank 2-4), Chunks follow the document's structure (Docling heading labels) (+15 more)

### Community 141 - "answer.tsx"
Cohesion: 0.06
Nodes (47): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+39 more)

### Community 142 - "packs.py"
Cohesion: 0.10
Nodes (24): DocumentTypeSpec, One kind of document the core recognises., Classification, _prompt(), Decide which of the core catalogue's document types a captured document is, or d, _schema(), ValueError, Safe to show. Forgetting a document whose file is still there would not last. (+16 more)

### Community 144 - "test_api.py"
Cohesion: 0.08
Nodes (87): client_for(), document_row(), fact_row(), FakeConn, filed_document(), inbox(), obligation(), open_obligation() (+79 more)

### Community 145 - "Set C: adversarial"
Cohesion: 0.33
Nodes (5): Assumptions to recheck before the run, How it is scored, Planted documents (for Desmond), Set C: adversarial, The line format

### Community 146 - "Policy Schedule Template"
Cohesion: 0.11
Nodes (23): One cell, one field, Policy Schedule Template, PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Renewal Notice Template (+15 more)

### Community 147 - "alert module manifest"
Cohesion: 0.28
Nodes (9): Days without recorded cover tile, alert_fpr, obligation_precision, Module manifest template, Quoted "on" key in YAML 1.1, alert module manifest, Modules read typed rows, never chunks, reminder module manifest (+1 more)

### Community 148 - "dependencies"
Cohesion: 0.10
Nodes (20): ai, @ai-sdk/react, class-variance-authority, clsx, createComponentFactory(), lucide-react, next, next-themes (+12 more)

### Community 149 - "_as_vault_document"
Cohesion: 0.50
Nodes (4): _as_vault_document(), one_document(), vault_documents(), VaultDocument

### Community 150 - "app/layout.tsx"
Cohesion: 0.22
Nodes (9): next-themes, web_app_globals, figtree, jetbrains, metadata, outfit, RootLayout(), viewport (+1 more)

### Community 151 - "_as_sentence"
Cohesion: 0.67
Nodes (3): _as_sentence(), "which age band applies" -> "Which age band applies.": a pack's wording and a ca, Built once, asked many times. Holds no connection: retrieval does.

### Community 152 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 153 - "test_help_runs_without_importing_core_before_sys_path_is_set"
Cohesion: 0.67
Nodes (3): parametrize, `--help` must work even though `core` is not on `sys.path` until the script inse, test_help_runs_without_importing_core_before_sys_path_is_set()

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (8): parrot-sweep shimmer animation, Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, An answer with the page it came from, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "worker.py"
Cohesion: 0.18
Nodes (17): lifespan(), install_best_effort(), Install at startup without being able to stop startup.      Both processes tha, application(), The configured application with its tasks registered. One per process., _beat_needs_its_own_process(), celery_argv(), main() (+9 more)

### Community 157 - "_answer_events"
Cohesion: 0.09
Nodes (30): A document and a page, as a person would cite it — or, for published guidance, w, Source, _answer_events(), _as_response(), _as_source(), ask(), ask_stream(), today() (+22 more)

### Community 158 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.20
Nodes (10): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Task: run adversarial Set C and write up the findings, Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The six artefacts (+2 more)

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 160 - "createExternalModules"
Cohesion: 0.25
Nodes (11): cdnScriptFor(), createExternalModules(), ensureBabel(), resolve2(), resolveGlobal(), waitForGlobal(), isElementClass(), isRenderableType() (+3 more)

### Community 161 - "FolderCapture"
Cohesion: 0.22
Nodes (4): FolderCapture, Begin watching. Returns False, with a logged reason, when it cannot., Begin polling. Returns False, with a logged reason, when it cannot or should not, A daemon thread that polls the watched folder until `stop()` or process exit.

### Community 162 - "harness.py"
Cohesion: 0.09
Nodes (36): _graph_for(), HouseholdConsents, `core.graph.advice.ConsentBook` over a live connection, for the graph to ask wit, HouseholdAdviceLog, `core.graph.advice.AdviceLog` over a live connection.      `basis` is dumped w, DenseRetriever, NoReranker, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this with (+28 more)

### Community 163 - "sha256"
Cohesion: 0.09
Nodes (27): CaptureAdapter, datetime, Protocol, The one interface every capture channel satisfies.      receive(payload, mime,, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256` i, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sha256(), Capture adapters.  Every channel a document can arrive through satisfies one i (+19 more)

### Community 164 - "test_both_ask_endpoints_hand_the_graph_the_same_advice_ports"
Cohesion: 0.12
Nodes (16): advising(), conn(), graph(), _padded(), fixture, MonkeyPatch, One construction for both. With any port missing the graph declines advice, so a, Starlette's own body iteration (`iterate_in_threadpool`) never calls `.close()` (+8 more)

### Community 165 - "Evaluation"
Cohesion: 0.15
Nodes (14): Evaluation, Extraction F1 by document type, Generating a lane's dozen, Ground truth comes free, How much of a delta is a delta, Metrics and targets, Running the harness, Set A, answerable (+6 more)

### Community 166 - "RagasJudge"
Cohesion: 0.32
Nodes (6): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts(), Ragas 0.4 metrics through Ollama's OpenAI-compatible endpoint. Imported lazily…

### Community 167 - "The Grounding Gate"
Cohesion: 0.33
Nodes (7): never_acts: True in Every Pack Manifest, The Core Answering Layer, The Answer Path: route, retrieve, rerank, ground, answer or abstain, The Grounding Gate, The Score Floor the Gate Reads, Ask Screen, Try to Make It Lie: the Abstention Test

### Community 168 - "(app)/layout.tsx"
Cohesion: 0.09
Nodes (25): lucide-react, AppLayout(), dynamic, runtime, LockButton(), SURFACES, TabBar(), Tabs() (+17 more)

### Community 171 - "DocumentCatalog"
Cohesion: 0.09
Nodes (30): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering (, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why the catalogue cannot supply `field` from every one of `doc_types`, or None., Whether any document type in the catalogue declares `field`., An advice shape that names a missing role or key fails at load time., Every core document type, field and category this pack names exists, or ValueErr, A compared field no document type of the shape declares can never be printed. (+22 more)

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

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 181 - "._advise"
Cohesion: 0.06
Nodes (35): Claim, _advice_basis(), answer_system(), _asked(), _max_sentences(), _numbered(), Any, Event (+27 more)

### Community 182 - "pipeline.py"
Cohesion: 0.08
Nodes (35): Chunk, ReminderConfig, Chunk, What is actually embedded: the prefix plus the text, matching the tsvector colum, The ingestion worker.  Capture registers a document; this package turns it int, fixed(), from_facts(), _label() (+27 more)

### Community 183 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 184 - "Basic Financial Planning Guide"
Cohesion: 0.15
Nodes (12): Basic Financial Planning Guide, Basic Financial Planning Guide, Basic Financial Planning Guide For Entrants To The Workforce, Basic Financial Planning Guide for those nearing retirement, Basic Financial Planning Guide For Those With Dependents, Emergency funds, For those approaching retirement, For those new to the workforce (+4 more)

### Community 186 - "run_parrot.py"
Cohesion: 0.06
Nodes (55): _kill_tree(), main(), open_browser(), parse_args(), port_answers(), Any, Namespace, Popen (+47 more)

### Community 190 - "Household canon"
Cohesion: 0.05
Nodes (39): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, The family tree, and why three of them are not called Lim, Vehicles (+31 more)

### Community 200 - "next"
Cohesion: 0.07
Nodes (33): ADR-0017, next, AlwaysOn(), dynamic, metadata, ModuleRow(), PackCard(), PacksPage() (+25 more)

### Community 201 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.20
Nodes (17): Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022, Platform Workers have wider protection gaps than the economically active population, Mortality protection gap (21%, S$373 billion, PGS 2022), LIA 2022 Protection Gap Study Key Findings (+9 more)

### Community 204 - "package.json"
Cohesion: 0.08
Nodes (22): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+14 more)

### Community 205 - "Tax and Reliefs pack (iras_tax)"
Cohesion: 0.22
Nodes (13): iras_tax grounding binding (corpus iras_reliefs_ya2026, top_k 8), Tax and Reliefs pack (iras_tax), iras_tax persona (explains the user's documents against IRAS guidance, never estimates a liability), Task lists are generated from docs/team-tasks.csv, Twelve golden-set questions per person by the end of week 3, Lane A - Christian, integration and product, Lane B - Yew Mun, retrieval and evaluation, Lane C - Siew, governance and assurance (+5 more)

### Community 213 - "createPseudoSheet"
Cohesion: 0.67
Nodes (4): createPseudoSheet(), importantify(), scanUnquotedUrl(), stripComments()

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

### Community 227 - "Zee — Lane D · Domain packs and interface"
Cohesion: 0.22
Nodes (9): Half one — domain packs (weeks 1 to 7), Half two — the interface (weeks 4 to 8), Read this first, Rules that apply to you specifically, The two halves of this lane, What "done" looks like, What you present, Your Claude Code skills (+1 more)

### Community 228 - "Zee — task list"
Cohesion: 0.22
Nodes (9): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20, W9 — due 2026-11-03 (+1 more)

### Community 229 - "Household canon"
Cohesion: 0.25
Nodes (7): Address, Employment, Household canon, Life events that documents must reflect, People, Policies, Vehicles

### Community 230 - "0001_init.sql"
Cohesion: 0.36
Nodes (7): chunks, documents, facts, modules, obligations, packs, traces

### Community 231 - "typing"
Cohesion: 0.08
Nodes (25): Dispatcher, Inline, Protocol, What happens to a document between "these bytes are registered" and "this docume, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Send (+17 more)

### Community 234 - "Contributing"
Cohesion: 0.25
Nodes (8): Before your first commit, Contributing, Decisions, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure, main Is Deliberately Unprotected, main Is Not Protected

### Community 235 - "The corpus"
Cohesion: 0.10
Nodes (20): Amend the Graph Refresh Into the Commit, Qwen-SEA-LION-v4-4B-VL Generator, No CORS Middleware, Deliberately, Changelog, Generation Model Swapped to Fit One 8 GB Card, W1 · 2–8 Sep 2026, W2 · 9–15 Sep 2026, Capture Channels Are Transports (+12 more)

### Community 236 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

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

### Community 261 - "`core/graph/` — the LangGraph runtime"
Cohesion: 0.40
Nodes (4): `core/graph/` — the LangGraph runtime, Rules, What belongs here, What does not

### Community 262 - "0002_household.sql"
Cohesion: 0.70
Nodes (4): document_attribution, people, person_aliases, telegram_identities

### Community 263 - "0003_advice.sql"
Cohesion: 0.60
Nodes (4): advice_consents, advice_records, grounding_sources, grounding_values

### Community 266 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 267 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

### Community 268 - "13. A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.18
Nodes (9): 13. A question is understood before it is searched, and scoped before it is cut, Consequences, Context, Decision, Evidence, 15. A name scopes a question, and a grandparent is not a parent, Consequences, Context (+1 more)

### Community 269 - "Data inventory — identity data, dates of birth and loans"
Cohesion: 0.40
Nodes (4): Data inventory — identity data, dates of birth and loans, Open questions for Siew, The inventory, What this entry covers

### Community 270 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 272 - "`core/ingest/` — the ingestion worker"
Cohesion: 0.50
Nodes (3): `core/ingest/` — the ingestion worker, Quarantine is two-stage, Rules

### Community 273 - "`core/retrieve/` — hybrid retrieval"
Cohesion: 0.50
Nodes (3): `core/retrieve/` — hybrid retrieval, Rules, What belongs here

### Community 275 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 279 - "`docs/governance/` — the assurance artefacts"
Cohesion: 0.50
Nodes (3): `docs/governance/` — the assurance artefacts, The autonomy statement in one line, The rule that governs all eight

### Community 288 - "Pack grounding corpus rules"
Cohesion: 0.50
Nodes (3): ISO/IEC 22989 stages versus 5338 processes, Grounding corpora, Pack grounding corpus rules

### Community 290 - "Contracts and Migrations Are Their Own PR"
Cohesion: 0.33
Nodes (6): The Purely Additive Migration Exception, Contracts and Migrations Are Their Own PR, Snooze Means Not Until This Gets More Urgent, The Three Things Agents Get Wrong Here, MemorySaver Until a Reviewed Migration, MemorySaver Checkpointer, Not PostgresSaver

### Community 337 - "ADR index (0001-0018, with status)"
Cohesion: 0.12
Nodes (23): ADR 0001 - Record architecture decisions, ADR 0002 - One PostgreSQL instance for everything, Reciprocal rank fusion of dense and lexical, ADR 0003 - PaperBrain informs the pattern, not the module, PaperBrain prototype, ADR 0004 - Local setup can run before the assistant is ready, ADR 0006 - pypdfium2 renders the quarantine page images, ADR 0007 - The graph ships before retrieval and before a checkpoint table (+15 more)

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
- `Fill the Register Before Generating Documents` → `Motor Vehicle Hire Purchase Agreement Template`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to
- `Corpus Batches Are Not in Git` → `The Corpus Is Synthetic and Committed`  [AMBIGUOUS]
  NOTICE.md · relation: semantically_similar_to
- `Domain Packs` → `Core Document Catalogue (ADR 0017)`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `The Lim Household, Tampines` → `Republic of Xinkapow, the Invented Jurisdiction`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to
- `Republic of Xinkapow, the Invented Jurisdiction` → `Real Organisations May Be Named`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to
- `Sources of Truth Generate Their Outputs` → `pack.yaml Is the Only Place a Field Name Is Written`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to

## Knowledge Gaps
- **825 isolated node(s):** `Advice`, `Withheld`, `Part`, `ParrotEvent`, `Action` (+820 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 2318 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Provenance register for corpus sg_protection_guidance` and `Lane A - Christian, integration and product`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Provenance register for corpus sg_protection_guidance` and `Lane D - Zee, domain packs and interface`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `LIA 2022 Protection Gap Study Key Findings` and `Protection rule of thumb: 9x annual income for death and TPD, 4x for critical illness`?**
  _Edge tagged AMBIGUOUS (relation: cites) - confidence is low._
- **What is the exact relationship between `Fill the Register Before Generating Documents` and `Motor Vehicle Hire Purchase Agreement Template`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Corpus Batches Are Not in Git` and `The Corpus Is Synthetic and Committed`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Domain Packs` and `Core Document Catalogue (ADR 0017)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `The Lim Household, Tampines` and `Republic of Xinkapow, the Invented Jurisdiction`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._