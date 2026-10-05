# Graph Report - igd-capstone-2026  (2026-10-05)

## Corpus Check
- 323 files · ~742,498 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 37 file(s) not represented in the graph (top: (none) 11, .jsonl 8, .csv 6)

## Summary
- 5554 nodes · 13163 edges · 332 communities (248 shown, 84 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 1457 edges (avg confidence: 0.72)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5a49824a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ModelUnavailable
- HybridRetriever
- ScriptedOllama
- AnswerGraph
- validate
- advice/__init__.py
- Insurance and Coverage pack (insurance_agent)
- test_advice_module.py
- api.ts
- FakeOllama
- InstalledPack
- Ollama
- FolderAdapter
- test_telegram_capture.py
- ModuleAdviser
- answer.py
- bench_runtime.py
- vault.py
- get
- schedule.py
- ingest/extract.py
- test_grounding_values.py
- Overdue
- HouseholdAdviceLog
- TelegramAdapter
- pytest
- household.py
- ParsedPage
- test_startup.py
- score.py
- _household_scope
- .load
- test_pages.py
- parse.py
- test_eval_generate.py
- test_modules.py
- eval/modules.py
- extract_values
- test_api.py
- alert/__init__.py
- retrieve.py
- StreamingGraph
- test_household.py
- sha256
- test_eval_modules.py
- test_tax_pack.py
- support.js
- build_router
- test_ingest_pipeline.py
- compilerOptions
- Domain packs — start here
- registry.py
- test_grounding.py
- date
- cli.py
- run.py
- ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic
- packs.py
- Any
- values.py
- advice-card.tsx
- lock.ts
- score_alerts
- routes.py
- PARROT Interface Design Pack
- export-design-preview.cjs
- The Four Surfaces
- pack
- advice-consent.tsx
- devDependencies
- test_advice_core.py
- AdviceRecord
- scope.py
- ADR 0011: The household is people and aliases, and the owner is one of them
- test_gate.py
- Any
- today/page.tsx
- ingest/reindex.py
- preview.tsx
- Hash-based idempotency
- test_eval_harness.py
- Ollama
- PARROT mid-term: talking script
- datetime
- Any
- test_advice_is_a_module
- components.json
- _as_module_summary
- 18 · The reranker runs in-process, because Ollama cannot serve a cross-encoder
- Passage
- boot
- report.py
- The Lim Household, Tampines
- Starting Parrot
- Lane C - Governance and assurance
- test_contracts.py
- Core Document Catalogue (ADR 0017)
- Notebook prompts — the four full policies for Marcus Lim
- is_first_person
- The five-lane split (five people, nine weeks, three builders)
- Data inventory: identity data, DOBs and loans
- ConfigurationError
- The autonomy statement
- web/ - the PARROT interface
- The document register as ground truth
- ingest.py
- Tax and Reliefs — contract changes this pack needs
- Reminder, Alert and Tracker Registers
- checks.py
- example_pack template manifest
- paperbrain/extract.py
- §5 · Evaluation and results
- tokens/page.tsx
- Try PARROT
- Integration review
- typing
- adr/README.md
- test_worker_queue.py
- Part A. Policy
- Terms of use
- The deliberately naive retrieval baseline
- Running the evaluation harness
- Project PARROT — team split
- A field name is written down once
- The demonstration run sheet
- run_parrot.py
- Filling the corpus register
- Writing a governance artefact
- Missing
- Working agreement for coding agents
- igd-capstone-2026
- Policy schedule HTML template
- PaperBrain
- ADR 0013: A question is understood before it is searched, and scoped before it is cut
- answer.tsx
- corrections.py
- Settings
- Set C: adversarial
- Policy Schedule Template
- alert module manifest
- dependencies
- FakeCursor
- app/layout.tsx
- Policies
- Authoring a domain pack
- validate.py
- test_lifecycle.py
- DesignPreview evaluation harness
- DatabaseUnavailable
- _answer_events
- Siew — Lane C · Governance and assurance
- Writing an ADR
- Every Fact Row Cites Its Source
- HouseholdScope
- base.py
- worker.py
- Evaluation
- .__post_init__
- advice_consent.py
- Registration
- Financial advisory process
- Household canon
- DocumentCatalog
- 19 · A relevance floor on the reranker does not buy abstention, and the reason is not calibration
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- _today_items
- test_a_client_that_leaves_after_the_card_commits_one_record
- gate.py
- filesystem
- test_answer_graph.py
- pipeline.py
- Project PARROT — team split
- Basic Financial Planning Guide
- phrasings.py
- pathlib
- One Database
- check_content
- Screens
- createExternalModules
- Lane E - Corpus and adversarial testing
- packs/page.tsx
- Provenance register for corpus sg_protection_guidance
- setup.sh
- session-start.sh
- package.json
- Tax and Reliefs pack (iras_tax)
- postcss.config.mjs
- Lane C - Governance and assurance
- parrot
- paperbrain/ollama.py
- stop
- Yew Mun — task list
- Comparison of Integrated Shield Plans
- Christian — task list
- Desmond — Lane E · Corpus and adversarial testing
- Desmond — task list
- Siew — task list
- IMDA frameworks: what applies to PARROT
- Graphify — the shared knowledge graph
- First run
- Understanding health insurance
- installed_packs
- build_team_tasks.py
- The household, and the word "my"
- Incident and data breach procedure
- Zee — Lane D · Domain packs and interface
- Zee — task list
- Household canon
- 0001_init.sql
- What to ask before buying life insurance
- FakeCursor
- RecordingConn
- FakeCursor
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
- .embed
- Architecture
- advice_consents
- Claude Code — read this first
- 2. One PostgreSQL instance for everything
- 10. `main` is unprotected, and the discipline is human
- 12. Chunks follow the document's headings, and embeddings use the model's task prompts
- 14 · A pack supplies what the core knows about a domain, and the core stays generic
- 17 · A pack is grounding and persona; the core owns documents
- Artefacts
- Why the prototype is evaluated on synthetic data
- `docs/report/` — the final report
- About Integrated Shield Plan
- Lifecycle
- The team
- usable
- `core/graph/` — the LangGraph runtime
- 0002_household.sql
- 0003_advice.sql
- 1. Record architecture decisions
- 4. Local setup can run before the household assistant is ready
- 6. pypdfium2 renders the page images the quarantine second pass reads
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- 13. A question is understood before it is searched, and scoped before it is cut
- Data inventory — identity data, dates of birth and loans
- Notice
- cron_expressions
- `core/ingest/` — the ingestion worker
- `core/retrieve/` — hybrid retrieval
- quarantine.tsx
- 7. The answer graph ships before hybrid retrieval and before a checkpoint table
- 15. A name scopes a question, and a grandparent is not a parent
- scope_to
- `docs/governance/` — the assurance artefacts
- resolve_names
- `core/adapters/` — capture adapters
- Home Contents Insurance Policy
- createPseudoSheet
- Incident log
- Due
- quiet_engine
- sets/README.md
- Pack grounding corpus rules
- test_help_runs_without_importing_core_before_sys_path_is_set
- The Grounding Gate
- _dual_cited_calculation
- _meets_calculation
- _shared_value_calculation
- ADR index (0001-0018, with status)
- The final ILP report
- Adversarial testing from week 7
- Two-stage quarantine with a vision-language second pass
- Nobody edits core/contracts.py in a feature pull request

## God Nodes (most connected - your core abstractions)
1. `Settings` - 207 edges
2. `ScriptedOllama` - 96 edges
3. `FakeConn` - 94 edges
4. `Ollama` - 90 edges
5. `InstalledPack` - 89 edges
6. `AnswerGraph` - 78 edges
7. `settings()` - 75 edges
8. `client_for()` - 74 edges
9. `build_router()` - 73 edges
10. `Passage` - 71 edges

## Surprising Connections (you probably didn't know these)
- `3. Implement technical controls and processes (§2.3, pp 33–45)` --references--> `ModuleManifest`  [INFERRED]
  docs/governance/imda-what-applies.md → core/contracts.py
- `GenAI framework: nine dimensions` --references--> `GroundingDocument`  [INFERRED]
  docs/governance/imda-what-applies.md → core/contracts.py
- `2. Make humans meaningfully accountable (§2.2, pp 25–32)` --references--> `_advice_basis()`  [INFERRED]
  docs/governance/imda-what-applies.md → core/graph/answer.py
- `_chat_ids()` --references--> `Containment, by kind`  [INFERRED]
  core/runtime/settings.py → docs/governance/incident-and-breach-procedure.md
- `1. Assess and bound the risks upfront (§2.1, pp 15–24)` --references--> `Guardrails`  [INFERRED]
  docs/governance/imda-what-applies.md → core/contracts.py

## Import Cycles
- None detected.

## Communities (332 total, 84 thin omitted)

### Community 0 - "ModelUnavailable"
Cohesion: 0.15
Nodes (3): ModelUnavailable, extract(), down()

### Community 1 - "HybridRetriever"
Cohesion: 0.10
Nodes (16): hybrid_score(), HybridRetriever, identifiers(), prints(), FakeConn, FakeCursor, FakeOllama, _row() (+8 more)

### Community 2 - "ScriptedOllama"
Cohesion: 0.07
Nodes (44): AdviceCard, _closes(), Finished, Subject, advised_pack(), build(), Consents, Household (+36 more)

### Community 3 - "AnswerGraph"
Cohesion: 0.09
Nodes (35): AnswerGraph, Sentence, Scoped, test_advice_is_declined_when_the_graph_was_given_no_adviser(), FakeInventory, FixedRetriever, holding(), insurance() (+27 more)

### Community 4 - "validate"
Cohesion: 0.17
Nodes (16): validate(), test_a_batch_mixes_packs_in_one_register(), test_a_header_without_field_pages_is_caught(), test_a_row_with_no_fields_carries_no_ground_truth(), test_an_unparseable_page_is_caught(), test_duplicate_ids_are_caught(), test_expiry_before_start_is_caught(), test_field_pages_naming_a_field_the_row_does_not_fill_is_caught() (+8 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.08
Nodes (44): RuleInput, Figure, Input, _Value, _ambiguous(), _amount(), _band(), _band_label() (+36 more)

### Community 6 - "Insurance and Coverage pack (insurance_agent)"
Cohesion: 0.16
Nodes (16): Insurance advice consent gate (consent_version 1.0.0), advice_decline guardrail message, Category matcher (printed product_name against asked words, first rule wins), Advice shape ci_cover (gap calculator), Category critical_illness (critical illness plan), Advice shape death_tpd_cover (gap calculator), Exclusion detection (headings, claims, negations), insurance_agent guardrails (must_cite, abstain_below 0.45, never_acts, verdict_by_code) (+8 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.14
Nodes (49): Calculation, calculate(), assert_nothing_negative(), basis(), fact(), _facts_tuple(), figures_of(), _gap_basis() (+41 more)

### Community 8 - "api.ts"
Cohesion: 0.08
Nodes (31): RELATION_CHOICES, Place, PLACES, SourcePanel(), DocumentDetail(), when(), Field(), format() (+23 more)

### Community 9 - "FakeOllama"
Cohesion: 0.11
Nodes (23): extract(), FakeOllama, _page_of_examples(), _reply_of_examples(), test_a_date_that_cannot_be_read_still_quarantines(), test_a_donation_receipt_stores_donation_amount_and_never_amount(), test_a_fact_is_stored_under_the_name_the_catalogue_declares(), test_a_long_document_whose_front_is_enough_is_read_once() (+15 more)

### Community 10 - "InstalledPack"
Cohesion: 0.08
Nodes (29): GroundingDocument, SourceText, index_pack(), IndexReport, _upsert_source(), ExtractedValue, InstalledPack, main() (+21 more)

### Community 11 - "Ollama"
Cohesion: 0.07
Nodes (28): blocked_reasons(), forget(), page_images(), QuarantinedDocument, queue(), Recovery, recovery_rate(), retry() (+20 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.21
Nodes (15): FolderAdapter, FolderSettings, FakeRegistrar, _settle(), test_a_file_removed_before_it_settles_is_forgotten(), test_a_file_still_being_written_is_not_registered(), test_a_file_too_large_for_a_household_document_is_skipped(), test_a_registered_file_is_not_registered_again_on_every_poll() (+7 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.10
Nodes (24): build(), FakeTelegram, photo_update(), test_a_chat_outside_the_allow_list_is_ignored(), test_a_conflict_names_the_webhook_rather_than_saying_nothing(), test_a_document_keeps_the_name_it_was_sent_under(), test_a_malformed_allow_list_is_a_configuration_error_not_an_empty_one(), test_a_photograph_becomes_a_document_on_the_telegram_channel() (+16 more)

### Community 14 - "ModuleAdviser"
Cohesion: 0.12
Nodes (13): Advice, Categories, FactInput, fact_row(), FactRow, facts_for(), in_category(), _is_an_adviser() (+5 more)

### Community 15 - "answer.py"
Cohesion: 0.05
Nodes (20): kind_of(), _advice_prompt(), answer_system(), _as_sentence(), _asked(), _citations(), _conversation(), _distinct() (+12 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (20): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+12 more)

### Community 17 - "vault.py"
Cohesion: 0.20
Nodes (8): _as_document(), declared_type(), document(), documents(), Fact, _facts_for(), VaultDocument, VaultPage

### Community 18 - "get"
Cohesion: 0.24
Nodes (23): bundledBlob(), getDC(), Dispatcher(), getError(), load(), createHelmetManager(), applyCanvasBg(), compile() (+15 more)

### Community 19 - "schedule.py"
Cohesion: 0.23
Nodes (4): build(), beat_schedule(), crontab_from(), test_both_sweeps_are_scheduled_and_named_after_registered_tasks()

### Community 20 - "ingest/extract.py"
Cohesion: 0.10
Nodes (13): ReminderConfig, _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact, Extraction, _normalise() (+5 more)

### Community 21 - "test_grounding_values.py"
Cohesion: 0.14
Nodes (30): number_tokens(), parse_value(), _dropped(), _log_values(), _run(), test_a_money_value_with_a_currency_marker_is_kept(), test_a_multiple_is_kept_in_the_forms_it_is_written(), test_a_number_is_kept_when_one_of_its_occurrences_fits_the_unit() (+22 more)

### Community 22 - "Overdue"
Cohesion: 0.16
Nodes (5): close(), next_window(), Overdue, snooze(), UnknownObligation

### Community 23 - "HouseholdAdviceLog"
Cohesion: 0.09
Nodes (12): HouseholdConsents, HouseholdAdviceLog, DenseRetriever, Reranker, Retriever, Asks, build(), Recorder (+4 more)

### Community 24 - "TelegramAdapter"
Cohesion: 0.13
Nodes (6): _attachment(), _pixels(), _status_reason(), TelegramAdapter, _write_local_copy(), B3. Things erasure has to reach beyond the database

### Community 25 - "pytest"
Cohesion: 0.06
Nodes (19): SentenceScanner, _as_printed(), page_pixels(), photographed(), _register_row(), scanned(), test_a_scan_keeps_the_schedule_table_and_its_page(), drip() (+11 more)

### Community 26 - "household.py"
Cohesion: 0.10
Nodes (19): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+11 more)

### Community 27 - "ParsedPage"
Cohesion: 0.11
Nodes (17): Chunk, chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), classification_sample(), ParsedPage (+9 more)

### Community 28 - "test_startup.py"
Cohesion: 0.19
Nodes (10): start_web(), prepare_checkout(), test_check_only_never_launches_even_when_ready(), test_incomplete_checkout_never_launches_a_process(), test_launch_preserves_paths_and_loopback_and_exit_code(), test_screens_are_not_started_twice_when_something_already_holds_the_port(), test_screens_are_not_started_without_dependencies(), test_screens_are_not_started_without_npm() (+2 more)

### Community 29 - "score.py"
Cohesion: 0.06
Nodes (33): Trace, _as_date(), _as_number(), cites(), _contains(), declined_in_prose(), doc_stem(), grade() (+25 more)

### Community 30 - "_household_scope"
Cohesion: 0.09
Nodes (19): _household_scope(), test_a_grandparent_nobody_holds_is_an_unknown_relation_not_the_fathers_policy(), test_a_grandparent_recorded_under_that_name_is_who_the_question_means(), test_a_person_nobody_has_confirmed_is_not_named(), test_a_question_naming_one_other_member_is_scoped_to_them(), test_the_owner_asking_about_themselves_by_name_is_scoped_to_the_owner(), test_whose_asks_whose_when_a_member_is_named_without_a_possessive(), test_whose_gives_a_person_named_outright() (+11 more)

### Community 31 - ".load"
Cohesion: 0.08
Nodes (30): create_app(), checks(), ready(), setup(), system_status(), ModelWarmth, warm_models(), _folder() (+22 more)

### Community 32 - "test_pages.py"
Cohesion: 0.08
Nodes (20): document_page(), page_count(), PageUnavailable, _pdfium(), render_page(), RendererUnavailable, _size(), test_a_damaged_pdf_is_a_sentence_not_a_traceback() (+12 more)

### Community 33 - "parse.py"
Cohesion: 0.09
Nodes (13): Block, DoclingParser, _kind(), _pages_from(), Parser, PlainTextParser, _table_text(), _cell() (+5 more)

### Community 34 - "test_eval_generate.py"
Cohesion: 0.08
Nodes (23): _ambiguous(), choose(), Generated, hand_written(), main(), on_file(), pool(), write_lane() (+15 more)

### Community 35 - "test_modules.py"
Cohesion: 0.11
Nodes (23): already_said(), current_lead(), sweep(), FakeConn, obligation_row(), srs_row(), test_a_dry_run_records_nothing(), test_a_firing_older_than_the_debounce_window_fires_again() (+15 more)

### Community 36 - "eval/modules.py"
Cohesion: 0.15
Nodes (13): _day(), main(), measure(), Measured, _number(), obligations(), obligations_possible(), _paragraph() (+5 more)

### Community 37 - "extract_values"
Cohesion: 0.17
Nodes (12): extract_values(), _long_text(), _reply(), ScriptedClient, _source(), test_a_json_reply_with_no_usable_values_is_no_values_for_that_section_only(), test_a_long_text_is_sent_in_more_than_one_call(), test_a_model_that_is_down_raises() (+4 more)

### Community 39 - "test_api.py"
Cohesion: 0.07
Nodes (32): Answer, Cited, advising(), conn(), FakeGraph, graph(), inbox(), _padded() (+24 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.11
Nodes (14): AlertConfig, Alert, days_uncovered(), _debounced(), Measurement, _per_subject(), srs_contributions_ytd(), sweep() (+6 more)

### Community 41 - "retrieve.py"
Cohesion: 0.17
Nodes (9): load_matrix(), pack(), unpack(), _fts_query(), fuse(), hydrate(), keyword_search(), search() (+1 more)

### Community 42 - "StreamingGraph"
Cohesion: 0.11
Nodes (18): Citation, Reading, Refused, a_citation(), advice_card(), rule_citation(), sse(), StreamingGraph (+10 more)

### Community 43 - "test_household.py"
Cohesion: 0.11
Nodes (16): conn(), _conn_returning(), _passage(), test_a_document_naming_the_owner_and_somebody_else_is_kept(), test_a_document_with_no_subject_belongs_to_everybody(), test_a_household_with_no_owner_scopes_nothing(), test_a_member_can_be_placed_but_the_owner_cannot(), test_an_unconfirmed_alias_resolves_to_nobody() (+8 more)

### Community 44 - "sha256"
Cohesion: 0.24
Nodes (9): sha256(), register_document(), conn(), database_url(), test_a_document_must_arrive_with_a_name(), test_a_new_document_is_inserted(), test_an_empty_payload_is_refused(), test_different_bytes_are_different_documents() (+1 more)

### Community 45 - "test_eval_modules.py"
Cohesion: 0.09
Nodes (20): _mark(), ModuleMetrics, Obligation, obligation_precision(), render(), _same_person(), score_obligations(), Verdict (+12 more)

### Community 46 - "test_tax_pack.py"
Cohesion: 0.20
Nodes (11): _basis(), _latest(), _matched(), _published(), _register(), _shape(), test_a_tax_question_reaches_the_tax_shape_and_insurance_keeps_its_own(), test_no_saving_is_estimated_without_a_notice_of_assessment() (+3 more)

### Community 47 - "support.js"
Cohesion: 0.12
Nodes (28): collectProps(), compileAttr(), compileTemplate(), contentKey(), cssToObj(), encodeCamelAttrs(), encodeCase(), evalDcLogic() (+20 more)

### Community 48 - "build_router"
Cohesion: 0.08
Nodes (29): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, QuarantinedDocument, QuarantineResponse, _as_person() (+21 more)

### Community 49 - "test_ingest_pipeline.py"
Cohesion: 0.11
Nodes (18): find_page(), printed_date(), parse(), insurance(), iras(), test_a_date_of_birth_printed_day_first_with_dashes_is_found(), test_a_date_on_no_page_still_has_no_page(), test_a_date_printed_in_other_common_notations_is_also_found() (+10 more)

### Community 50 - "compilerOptions"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 51 - "Domain packs — start here"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 52 - "registry.py"
Cohesion: 0.11
Nodes (17): ModuleManifest, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, enabled_module_ids(), _module_row(), modules() (+9 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.18
Nodes (12): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), _document(), _installed(), test_a_missing_recorded_file_is_refused(), test_a_pack_with_no_corpus_gives_none_and_empty() (+4 more)

### Community 54 - "date"
Cohesion: 0.16
Nodes (12): document_row(), fact_row(), filed_document(), obligation(), overdue_row(), test_a_core_document_stays_enabled_when_every_pack_is_off(), test_a_disabled_pack_does_not_reach_the_nightly_sweep(), test_one_document_is_shown_even_when_its_pack_is_off() (+4 more)

### Community 55 - "cli.py"
Cohesion: 0.19
Nodes (15): build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest(), cmd_init() (+7 more)

### Community 56 - "run.py"
Cohesion: 0.13
Nodes (17): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), _indexed(), main() (+9 more)

### Community 57 - "ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.09
Nodes (35): Code-written absence sentence: 'None of the N policies on file is a dental plan.', ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic, The advise route intent returns the pack's advice_decline, answering.categories: ordered whole-word rules over one printed field, Category filter applied before the keep-6 cut, answering.exclusions: headings under which a cover claim is not believed, Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration) (+27 more)

### Community 58 - "packs.py"
Cohesion: 0.09
Nodes (15): DocumentTypeSpec, Classification, classify(), _prompt(), _schema(), Catalog, document_types(), _load_one() (+7 more)

### Community 59 - "Any"
Cohesion: 0.13
Nodes (15): names_for(), advised_pack(), db(), _document(), FakeConn, FakeCursor, _source(), _sum_insured() (+7 more)

### Community 61 - "values.py"
Cohesion: 0.08
Nodes (20): ValueKey, _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), _pack(), printed_as() (+12 more)

### Community 62 - "advice-card.tsx"
Cohesion: 0.11
Nodes (22): Advice, AdviceCard(), AdviceWithheld(), capitalise(), sentence(), TONES, ADR-0016, VERDICT_TONE (+14 more)

### Community 63 - "lock.ts"
Cohesion: 0.08
Nodes (45): dynamic, GET(), grant(), POST(), runtime, ALLOWED, Context, DELETE() (+37 more)

### Community 64 - "score_alerts"
Cohesion: 0.19
Nodes (7): alert_fpr(), score_alerts(), Fired, test_a_metric_with_no_register_equivalent_is_not_guessed_at(), test_an_alert_the_register_agrees_with_is_not_counted_against_the_module(), test_an_alert_the_register_contradicts_is_a_false_positive(), test_nothing_fired_is_unmeasured_rather_than_zero()

### Community 65 - "routes.py"
Cohesion: 0.09
Nodes (36): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, AskRequest, AskResponse, Claim, CloseRequest (+28 more)

### Community 66 - "PARROT Interface Design Pack"
Cohesion: 0.08
Nodes (23): Citation chips are the trust surface, Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Suggestions come from this week's ingest, Civic Register: order, clarity and institutional confidence, Kitchen Table: a little less household admin, a little more breathing room, The Reading Desk: understand it, open the source, see for yourself (+15 more)

### Community 67 - "export-design-preview.cjs"
Cohesion: 0.08
Nodes (20): @eslint/eslintrc, compat, eslintConfig, bundle(), classes, css, cssFile, domId (+12 more)

### Community 68 - "The Four Surfaces"
Cohesion: 0.11
Nodes (17): `api/` — the FastAPI application, The FastAPI Application, Five properties worth knowing before you change anything, Rules, The surface, apply, Auto-Redirect to Today Once Ready, check (+9 more)

### Community 69 - "pack"
Cohesion: 0.11
Nodes (23): Asked, categories_asked(), categorise(), glossary(), mentions(), _pattern(), reworded(), _vocabulary() (+15 more)

### Community 70 - "advice-consent.tsx"
Cohesion: 0.15
Nodes (19): AdviceNote(), Consent, ConsentPrompt(), agree(), settle(), State, ADR-0016, AdviceConsentSection() (+11 more)

### Community 71 - "devDependencies"
Cohesion: 0.10
Nodes (21): eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node, @types/react (+13 more)

### Community 72 - "test_advice_core.py"
Cohesion: 0.23
Nodes (14): current(), FakeConn, _no_owner(), _owned(), test_a_withdrawal_after_a_grant_gives_none(), test_an_older_version_gives_status_outdated(), test_current_is_none_when_the_latest_grant_is_a_different_version(), test_current_queries_the_latest_row_by_person_and_pack() (+6 more)

### Community 73 - "AdviceRecord"
Cohesion: 0.09
Nodes (6): AdviceLog, AdviceRecord, ConsentBook, _advice_basis(), Part C. What must be built (for Christian), Log

### Community 74 - "scope.py"
Cohesion: 0.20
Nodes (7): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words()

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.17
Nodes (11): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), Telegram chat_id maps to a person, Possessive relations scope the question, before the cut to six, Naming exactly one person scopes to them (whole name, or a 3+ letter possessive unique to them) (+3 more)

### Community 76 - "test_gate.py"
Cohesion: 0.13
Nodes (25): check_advice(), check_one(), Claim, test_a_sentence_citing_a_passage_that_was_never_retrieved_is_dropped(), test_a_sentence_with_no_supporting_passage_is_dropped(), test_a_number_copied_from_the_passage_is_kept_however_it_is_formatted(), test_a_number_no_cited_passage_printed_is_dropped(), test_a_page_and_a_document_on_file_with_the_same_id_are_different_citations() (+17 more)

### Community 77 - "Any"
Cohesion: 0.16
Nodes (10): by_subject(), db(), FakeCursor, load_register(), test_a_deductible_receipt_counts_in_its_own_year_only(), test_a_lapsed_policy_is_not_masked_by_another_that_still_runs(), test_cpf_is_this_years_payslips_per_employee(), test_donations_are_this_years_deductible_receipts_per_donor() (+2 more)

### Community 78 - "today/page.tsx"
Cohesion: 0.06
Nodes (38): next, dynamic, HouseholdPage(), metadata, runtime, AppLayout(), dynamic, isUrgent() (+30 more)

### Community 79 - "ingest/reindex.py"
Cohesion: 0.12
Nodes (5): indexed(), IndexedDocument, reindex_document(), ReindexFailed, test_reindexing_replaces_chunks_and_leaves_facts_alone()

### Community 80 - "preview.tsx"
Cohesion: 0.10
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 82 - "Hash-based idempotency"
Cohesion: 0.25
Nodes (3): PaperBrain handled failure modes, The pb command line, PaperBrain dependency set

### Community 83 - "test_eval_harness.py"
Cohesion: 0.12
Nodes (21): reference_for(), Expected, load_set(), MalformedQuestion, Question, _answered(), FakeGraph, FakeRetriever (+13 more)

### Community 85 - "PARROT mid-term: talking script"
Cohesion: 0.10
Nodes (20): 01 · Christian, 02 · Christian, 03 · Christian, 04 · Christian, 05 · Christian, 06 · Christian, 07 · Zee, 08 · Zee (+12 more)

### Community 86 - "datetime"
Cohesion: 0.15
Nodes (11): approve(), pending(), PendingValue, reject(), _block(), main(), test_list_block_shows_id_pack_key_value_source_and_an_indented_passage(), test_review_cli_approve_and_reject_together_is_a_parser_error() (+3 more)

### Community 87 - "Any"
Cohesion: 0.18
Nodes (17): _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact(), _field_not_on_every_doc_type(), _held_per_month() (+9 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "_as_module_summary"
Cohesion: 0.29
Nodes (5): _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack()

### Community 91 - "18 · The reranker runs in-process, because Ollama cannot serve a cross-encoder"
Cohesion: 0.14
Nodes (10): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 18 · The reranker runs in-process, because Ollama cannot serve a cross-encoder, Alternatives considered, Consequences, Context (+2 more)

### Community 92 - "Passage"
Cohesion: 0.07
Nodes (21): Answering, Category, Exclusions, ExplainStep, FieldSpec, Grounding, Guardrails, ModuleTrigger (+13 more)

### Community 93 - "boot"
Cohesion: 0.20
Nodes (10): boot(), dcNameFromPath(), getReactDOM(), parseDataProps(), parseDcDocument(), parseDcText(), rootNameForDocument(), safeDecode() (+2 more)

### Community 94 - "report.py"
Cohesion: 0.07
Nodes (31): _cell(), collect(), main(), _overall(), _paragraph(), Provenance, render(), _row() (+23 more)

### Community 95 - "The Lim Household, Tampines"
Cohesion: 0.16
Nodes (9): loan_agreement Document Type, payslip Document Type, The Lim Household, Tampines, Rule of 78 Rebate and the 20 Per Cent Early Settlement Penalty, Motor Vehicle Hire Purchase Agreement Template, Republic of Xinkapow, the Invented Jurisdiction, Residential Housing Loan Facility Letter Template, 36-Month Lock-In, Prepayment Penalty and Subsidy Clawback (+1 more)

### Community 96 - "Starting Parrot"
Cohesion: 0.11
Nodes (21): ADR 0005 - The watched folder is polled, not subscribed to, Stability debounce with injected time, ADR 0008 - Ingestion runs on a Celery worker, Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Local validation notes, 2026-09-11 (+13 more)

### Community 97 - "Lane C - Governance and assurance"
Cohesion: 0.10
Nodes (13): The 40-document redacted holdout, Consent and redaction protocol, ISO/IEC 22989 to 5338 stage-to-process map, Lane C - Governance and assurance, Model card, Retention and erasure policy, Task: write the PDPA position on using synthetic data, Siew's generated task list (+5 more)

### Community 98 - "test_contracts.py"
Cohesion: 0.09
Nodes (28): PackManifest, _advised(), _checked(), _insurance(), _tax(), test_a_grounding_corpus_is_named_by_id_not_by_path(), test_a_grounding_corpus_travels_inside_its_pack(), test_a_market_comparison_may_compare_a_field_only_its_sources_publish() (+20 more)

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.15
Nodes (11): Generated files, benefit_illustration Document Type, birth_certificate Document Type, claim_letter Document Type, cpf_statement Document Type, Core Document Catalogue (ADR 0017), donation_receipt Document Type, identity_card Document Type (+3 more)

### Community 100 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 101 - "is_first_person"
Cohesion: 0.20
Nodes (7): is_first_person(), relation_asked(), test_a_name_that_is_not_exactly_one_person_scopes_nothing(), test_a_named_household_member_wins_over_the_pronoun(), test_a_possessive_relation_names_whose_documents_are_asked_about(), test_first_person_questions_are_recognised(), test_questions_about_other_people_are_not_scoped()

### Community 102 - "The five-lane split (five people, nine weeks, three builders)"
Cohesion: 0.09
Nodes (17): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The domain pack manifest, The expansion model: two axes, not one list, The golden set: answerable, hard negatives, adversarial, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build (+9 more)

### Community 103 - "Data inventory: identity data, DOBs and loans"
Cohesion: 0.27
Nodes (5): Data inventory: identity data, DOBs and loans, Telegram capture route and delete-at-source, What crosses a boundary, db service (pgvector/pgvector:pg17), redis service (redis:7-alpine)

### Community 104 - "ConfigurationError"
Cohesion: 0.06
Nodes (26): CrossEncoderReranker, passage_text(), relevance(), _chat_ids(), ConfigurationError, _flag(), local_url(), _port() (+18 more)

### Community 105 - "The autonomy statement"
Cohesion: 0.18
Nodes (11): IMDA mappings and autonomy statement artefact, The autonomy statement, The facts table as an extension point, The reminders table as an extension point, Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders (+3 more)

### Community 106 - "web/ - the PARROT interface"
Cohesion: 0.22
Nodes (7): Task: complete the Insurance Agent pack, The four surfaces: Today, Ask, Vault, Packs, Lane D - Domain packs and interface, Zee's generated task list, Task: write the user stories with acceptance criteria, Packs surface, web/ - the PARROT interface

### Community 107 - "The document register as ground truth"
Cohesion: 0.18
Nodes (5): python -m corpus.validate, The document register as ground truth, The household canon (the Lims of Tampines), Task: spot-check 20 register rows against the extractor, Golden Set A - answerable (60)

### Community 108 - "ingest.py"
Cohesion: 0.18
Nodes (10): Chunk, chunk_pages(), clean(), _split_page(), discover(), guess_date(), guess_type(), ingest_file() (+2 more)

### Community 109 - "Tax and Reliefs — contract changes this pack needs"
Cohesion: 0.40
Nodes (4): 1. A deduction multiplier on `estimate_saving`, 2. Limiting a fact input to one year, Not a contract change: parent relief, Tax and Reliefs — contract changes this pack needs

### Community 110 - "Reminder, Alert and Tracker Registers"
Cohesion: 0.18
Nodes (12): filing_deadline Reminder, passport Document Type, passport_expiry Reminder, policy_expiry Reminder, policy_schedule Document Type, Reminder, Alert and Tracker Registers, renewal_notice Document Type, srs_contribution_cutoff Reminder (+4 more)

### Community 111 - "checks.py"
Cohesion: 0.10
Nodes (18): device_name(), load(), score_pairs(), _warn_once(), broker_available(), capture_check(), Check, collect_checks() (+10 more)

### Community 112 - "example_pack template manifest"
Cohesion: 0.19
Nodes (10): Autonomy statement, abstention_rate, Set B, hard negatives, advice module manifest, example_pack template manifest, example_room advice shape, Pack advice block, The closed list of calculators (+2 more)

### Community 113 - "paperbrain/extract.py"
Cohesion: 0.41
Nodes (9): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+1 more)

### Community 114 - "§5 · Evaluation and results"
Cohesion: 0.17
Nodes (12): 5.10 What run 3 must add, 5.1 The claim, 5.2 What was measured, 5.3 The three-run spine, 5.4 Retrieval: what the two changes bought, 5.5 Abstention: the finding, 5.6 Extraction, by document type, 5.7 The two module metrics, and the lesson in them (+4 more)

### Community 115 - "tokens/page.tsx"
Cohesion: 0.05
Nodes (34): lucide-react, react, dynamic, runtime, Motion(), ROWS, INKS, metadata (+26 more)

### Community 116 - "Try PARROT"
Cohesion: 0.13
Nodes (15): 1 · Install five things, 2 · Download the AI models, 3 · Get the code and set it up, 4 · Put some documents in, 5 · Run it, 6 · Use it, Ask — a question about your own documents, If something goes wrong (+7 more)

### Community 117 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 119 - "adr/README.md"
Cohesion: 0.19
Nodes (7): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision, Architecture decision records, Index, Writing one

### Community 121 - "test_worker_queue.py"
Cohesion: 0.10
Nodes (19): Queued, bytes_for(), index_folder(), SourceMissing, FakeConnection, RecordingSend, registration(), test_a_document_whose_file_has_gone_is_reported_not_guessed() (+11 more)

### Community 122 - "Part A. Policy"
Cohesion: 0.18
Nodes (10): A1. Retention rules, A2. What erasure means, A3. Three ways to erase, A4. Deleting a document: only on instruction, confirmed, and complete within 72 hours, A5. Erasing a person, and resetting the workspace, A6. Incident hold, Basis, Decisions for Siew (+2 more)

### Community 123 - "Terms of use"
Cohesion: 0.22
Nodes (8): Clause A. Authority and Consent for Submissions on Behalf of Another Adult, Clause B. Purpose of Collection, Use and Retention, Clause C. Personal Data of Third Parties, Clause D. AI-Generated Answers and Helpdesk, Definitions, For review, Not yet written, Terms of use

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.14
Nodes (11): Task: benchmark the workstation and publish the numbers, Task: build the answer graph with the grounding gate, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, Task: contextualised chunking and the reranker, Task: hybrid retrieval with reciprocal rank fusion, Yew Mun's generated task list, Roadmap phase 1 - retrieval (+3 more)

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 127 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 129 - "The demonstration run sheet"
Cohesion: 0.05
Nodes (40): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+32 more)

### Community 130 - "run_parrot.py"
Cohesion: 0.14
Nodes (8): main(), open_browser(), parse_args(), port_answers(), spawn_child(), start_worker(), supervise(), test_runner_rejects_lan_bind_before_starting()

### Community 131 - "Filling the corpus register"
Cohesion: 0.20
Nodes (9): Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one, The rule that cannot bend (+1 more)

### Community 132 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (9): Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six, Where governance touches the code (+1 more)

### Community 133 - "Missing"
Cohesion: 0.18
Nodes (6): AdviceShape, Adviser, Missing, Adviser, _keep_shape(), shape()

### Community 134 - "Working agreement for coding agents"
Cohesion: 0.12
Nodes (8): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents, Slash Commands: orient, check, handover, weekly

### Community 135 - "igd-capstone-2026"
Cohesion: 0.09
Nodes (23): Working Agreement for Coding Agents, The Five Lanes and Their Owners, Before your first commit, Contributing, Decisions, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure (+15 more)

### Community 136 - "Policy schedule HTML template"
Cohesion: 0.24
Nodes (8): b1-0001 Private Car Insurance Policy Schedule, b1-0002 HomeShelter Contents Policy Schedule, b1-0003 Hospital Income Protection Plan Schedule, Full-length insurance policy notebook prompt, Four full-policy notebook prompts, Shared policy-drafting preamble, Guaranteed surrender value table (b1-0031), Policy schedule HTML template

### Community 139 - "PaperBrain"
Cohesion: 0.22
Nodes (7): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 140 - "ADR 0013: A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.16
Nodes (12): ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts, chunks.tsv built from context_prefix || text, Context prefix: title - type - heading - page, rag_probe2 before/after similarity table (six policies, 13 September), scripts/reindex.py rebuilds chunks and vectors, Chunks follow the document's structure (Docling heading labels), Task prompts: embed_query and embed_documents, ADR 0013: A question is understood before it is searched, and scoped before it is cut (+4 more)

### Community 141 - "answer.tsx"
Cohesion: 0.07
Nodes (28): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+20 more)

### Community 143 - "corrections.py"
Cohesion: 0.15
Nodes (5): _columns(), correct(), Corrected, CorrectionRejected, UnknownFact

### Community 144 - "Settings"
Cohesion: 0.08
Nodes (60): Settings, client(), client_for(), consent(), ConsentConn, FakeConn, open_obligation(), rows_for() (+52 more)

### Community 145 - "Set C: adversarial"
Cohesion: 0.32
Nodes (7): refused(), Assumptions to recheck before the run, How it is scored, Planted documents (for Desmond), Set C: adversarial, The line format, act()

### Community 146 - "Policy Schedule Template"
Cohesion: 0.11
Nodes (17): Policy Schedule Template, PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Renewal Notice Template, Graphify shared knowledge graph (+9 more)

### Community 147 - "alert module manifest"
Cohesion: 0.28
Nodes (6): Days without recorded cover tile, alert_fpr, obligation_precision, Module manifest template, alert module manifest, reminder module manifest

### Community 148 - "dependencies"
Cohesion: 0.10
Nodes (20): ai, @ai-sdk/react, class-variance-authority, clsx, createComponentFactory(), lucide-react, next, next-themes (+12 more)

### Community 149 - "FakeCursor"
Cohesion: 0.09
Nodes (10): Abstained, AdviceWithheld, ConsentRequired, Declined, ClosingSpy, ConsentCursor, Fails, FakeCursor (+2 more)

### Community 150 - "app/layout.tsx"
Cohesion: 0.20
Nodes (7): next-themes, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 151 - "Policies"
Cohesion: 0.15
Nodes (7): bge-reranker-v2-m3 Cross-Encoder, 40 Down to 6, Hybrid Retrieval: Dense Plus Full-Text, Reciprocal Rank Fusion, k=60, Policies, The three policies on Marcus are three different products, Whole life has no expiry, and now uses a separate `maturity_date`, The Validator Is the Handover Gate

### Community 152 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 153 - "validate.py"
Cohesion: 0.12
Nodes (8): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), _wide_format(), _without_guide()

### Community 154 - "test_lifecycle.py"
Cohesion: 0.24
Nodes (9): _client(), _eventually(), test_a_browser_cannot_reach_the_engine_directly_even_with_the_header(), test_a_request_without_the_intent_header_is_refused(), test_an_accepted_request_answers_first_and_then_asks_the_server_to_stop(), test_an_engine_nobody_supervises_says_so_instead_of_pretending(), test_an_unknown_action_is_not_found(), test_status_says_whether_this_engine_can_restart_itself() (+1 more)

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (6): Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "DatabaseUnavailable"
Cohesion: 0.07
Nodes (16): TelegramSettings, TelegramUnavailable, Dispatcher, Inline, Send, Intake, attribution(), dispatcher_for() (+8 more)

### Community 157 - "_answer_events"
Cohesion: 0.14
Nodes (7): AdviceConsent, _answer_events(), _as_consent(), record_consent(), connection(), _settings(), _sse()

### Community 158 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.20
Nodes (10): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Task: run adversarial Set C and write up the findings, Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The six artefacts (+2 more)

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 162 - "HouseholdScope"
Cohesion: 0.10
Nodes (8): _as_response(), ask(), ask_stream(), _graph_for(), _history(), HouseholdInventory, HouseholdScope, test_the_inventory_always_reads_core_documents()

### Community 163 - "base.py"
Cohesion: 0.08
Nodes (8): CaptureAdapter, IngestJob, receive_via(), sniff_mime(), _Pending, _Registered, Registrar, test_mime_is_sniffed_from_the_bytes_first()

### Community 164 - "worker.py"
Cohesion: 0.20
Nodes (8): lifespan(), install_best_effort(), _beat_needs_its_own_process(), celery_argv(), main(), _run(), _start_beat(), _stop_beat()

### Community 165 - "Evaluation"
Cohesion: 0.15
Nodes (14): Evaluation, Extraction F1 by document type, Generating a lane's dozen, Ground truth comes free, How much of a delta is a delta, Metrics and targets, Running the harness, Set A, answerable (+6 more)

### Community 166 - ".__post_init__"
Cohesion: 0.60
Nodes (4): aembed_text(), aembed_texts(), embed_text(), embed_texts()

### Community 167 - "advice_consent.py"
Cohesion: 0.21
Nodes (6): grant(), _latest(), NoOwner, _record(), status(), withdraw()

### Community 169 - "Financial advisory process"
Cohesion: 0.12
Nodes (15): After the meeting, Before the meeting, During the meeting, Financial advisory process, For an overview on the financial advisory process in Singapore, For insurance products:, For investment products:, Frequently asked questions (FAQ) (+7 more)

### Community 170 - "Household canon"
Cohesion: 0.05
Nodes (39): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, The family tree, and why three of them are not called Lim, Vehicles (+31 more)

### Community 171 - "DocumentCatalog"
Cohesion: 0.13
Nodes (13): DocumentCatalog, _class_name(), _docstring(), _field_line(), _header(), load(), load_catalog(), main() (+5 more)

### Community 172 - "19 · A relevance floor on the reranker does not buy abstention, and the reason is not calibration"
Cohesion: 0.22
Nodes (8): 19 · A relevance floor on the reranker does not buy abstention, and the reason is not calibration, Alternatives considered, Consequences, Context, Decision, Revisit when, The measurement, Why it is not a calibration problem

### Community 174 - "Project skills"
Cohesion: 0.40
Nodes (4): Changing them, Project skills, Slash commands, Using them

### Community 175 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 176 - "_today_items"
Cohesion: 0.22
Nodes (6): Source, _as_source(), today(), _cite(), _link(), _today_items()

### Community 177 - "test_a_client_that_leaves_after_the_card_commits_one_record"
Cohesion: 0.16
Nodes (6): next_kind(), test_a_client_that_leaves_after_the_card_commits_one_record(), test_a_client_that_leaves_mid_explanation_still_commits_what_it_was_shown(), test_a_graph_stream_closed_exactly_at_the_card_still_records_it(), test_a_stream_closed_exactly_at_the_card_is_still_committed_by_the_api(), test_closing_the_graph_when_the_record_write_fails_rolls_back()

### Community 179 - "gate.py"
Cohesion: 0.17
Nodes (8): _loose_numbers(), _normal(), _says(), states_a_printed_value(), unprinted_numbers(), test_a_date_on_file_may_be_written_the_way_a_person_says_it(), test_a_leading_zero_does_not_make_a_printed_date_unprinted(), test_a_policy_number_is_kept_only_when_it_is_printed_whole()

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 181 - "test_answer_graph.py"
Cohesion: 0.06
Nodes (33): _either(), precheck(), Generated, build(), events(), passage(), test_a_grounded_question_is_answered_with_its_source(), test_a_model_that_dies_before_any_sentence_abstains() (+25 more)

### Community 182 - "pipeline.py"
Cohesion: 0.11
Nodes (11): ParsedDocument, commit_both_lanes(), document_title(), Outcome, process(), _quarantine(), read_and_commit(), write_chunks() (+3 more)

### Community 183 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 184 - "Basic Financial Planning Guide"
Cohesion: 0.15
Nodes (12): Basic Financial Planning Guide, Basic Financial Planning Guide, Basic Financial Planning Guide For Entrants To The Workforce, Basic Financial Planning Guide for those nearing retirement, Basic Financial Planning Guide For Those With Dependents, Emergency funds, For those approaching retirement, For those new to the workforce (+4 more)

### Community 185 - "phrasings.py"
Cohesion: 0.20
Nodes (4): _keys(), LaneSpec, _spec(), TypeSpec

### Community 186 - "pathlib"
Cohesion: 0.08
Nodes (12): enabled_pack_ids(), enabled_packs(), find_browser_executable(), generate_documents(), _ask(), main(), documents_in(), main() (+4 more)

### Community 188 - "check_content"
Cohesion: 0.29
Nodes (9): passages_for(), check_content(), _calculation(), test_check_content_keeps_a_sentence_stating_a_facts_value(), test_check_content_keeps_a_sentence_stating_a_figure(), test_check_content_keeps_a_sentence_stating_a_rules_value(), test_check_content_still_drops_a_sentence_stating_an_unprinted_number(), test_passages_for_gives_fact_rule_and_calculation_refs() (+1 more)

### Community 189 - "Screens"
Cohesion: 0.23
Nodes (7): _launcher(), Screens, _supervise(), test_a_start_that_fails_is_not_retried(), test_no_web_means_the_supervisor_starts_no_screens(), test_the_supervisor_relaunches_on_restart_and_keeps_the_screens_up(), test_the_supervisor_still_refuses_a_lan_bind_before_starting_anything()

### Community 190 - "createExternalModules"
Cohesion: 0.25
Nodes (11): cdnScriptFor(), createExternalModules(), ensureBabel(), resolve2(), resolveGlobal(), waitForGlobal(), isElementClass(), isRenderableType() (+3 more)

### Community 200 - "packs/page.tsx"
Cohesion: 0.15
Nodes (9): ADR-0017, dynamic, metadata, PacksPage(), runtime, Toggle(), ModuleSummary, packs() (+1 more)

### Community 201 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.20
Nodes (15): Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022, Platform Workers have wider protection gaps than the economically active population, Mortality protection gap (21%, S$373 billion, PGS 2022), LIA 2022 Protection Gap Study Key Findings (+7 more)

### Community 204 - "package.json"
Cohesion: 0.08
Nodes (22): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+14 more)

### Community 205 - "Tax and Reliefs pack (iras_tax)"
Cohesion: 0.22
Nodes (10): iras_tax grounding binding (corpus iras_reliefs_ya2026, top_k 8), Tax and Reliefs pack (iras_tax), iras_tax persona (explains the user's documents against IRAS guidance, never estimates a liability), Twelve golden-set questions per person by the end of week 3, Lane A - Christian, integration and product, Lane B - Yew Mun, retrieval and evaluation, Lane C - Siew, governance and assurance, Lane D - Zee, domain packs and interface (+2 more)

### Community 211 - "paperbrain/ollama.py"
Cohesion: 0.25
Nodes (4): answer(), build_context(), format_sources(), Hit

### Community 212 - "stop"
Cohesion: 0.20
Nodes (6): _kill_tree(), stop(), test_a_worker_that_has_already_stopped_is_left_alone(), test_stopping_screens_that_were_never_started_does_nothing(), test_stopping_the_screens_kills_the_tree_not_the_wrapper(), test_stopping_the_worker_kills_the_tree_not_the_launcher()

### Community 213 - "Yew Mun — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

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

### Community 219 - "IMDA frameworks: what applies to PARROT"
Cohesion: 0.17
Nodes (11): 2. Make humans meaningfully accountable (§2.2, pp 25–32), 3. Implement technical controls and processes (§2.3, pp 33–45), 4. Enable end-user responsibility (§2.4, pp 46–49), Agentic AI framework: four dimensions (MGF for Agentic AI v1.5), Findings from this pass, For Siew, GenAI framework: nine dimensions, IMDA frameworks: what applies to PARROT (+3 more)

### Community 220 - "Graphify — the shared knowledge graph"
Cohesion: 0.20
Nodes (9): Graphify — the shared knowledge graph, Keeping it fresh, Merge conflicts, solved properly, Setup, once per clone, The hook leaves your tree dirty. Amend it into the commit you just made., Two kinds of extraction, and which needs what, Using it, What is committed, and what is not (+1 more)

### Community 221 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 222 - "Understanding health insurance"
Cohesion: 0.15
Nodes (12): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Assistance under MediFund, Basic health insurance coverage, Choosing your level of coverage, How MediSave fits in, If you have company health insurance, If you want more coverage (+4 more)

### Community 223 - "installed_packs"
Cohesion: 0.22
Nodes (6): installed_packs(), install(), Installed, test_every_installed_pack_still_loads(), test_every_pack_speaks_only_for_catalogue_types(), test_the_template_directory_is_not_an_installed_pack()

### Community 224 - "build_team_tasks.py"
Cohesion: 0.29
Nodes (5): main(), _read_rows(), _render(), _week_key(), _write()

### Community 225 - "The household, and the word "my""
Cohesion: 0.22
Nodes (9): 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model, 5 · Resolving "my" — three buckets, not two, 6 · Two safeguards, 7 · What this cost, and what it did not, 8 · What it enables, for §5 and §8 (+1 more)

### Community 226 - "Incident and data breach procedure"
Cohesion: 0.25
Nodes (7): 2. The six steps, 3. Is it a notifiable breach?, 4. The incident log, 5. Who is responsible on a household's own computer, Containment, by kind, Decisions for Siew, Incident and data breach procedure

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

### Community 231 - "What to ask before buying life insurance"
Cohesion: 0.20
Nodes (9): Are verbal representations provided in line with what's in the insurance policy documents?, Ask your FA representative, Ask yourself, Has the FA representative recommended a suitable product?, Is the information in the insurance policy correct?, Is there any benefit to switching insurance or investment products?, Take your time, What to ask before buying life insurance (+1 more)

### Community 235 - "The corpus"
Cohesion: 0.10
Nodes (13): Qwen-SEA-LION-v4-4B-VL Generator, Changelog, W1 · 2–8 Sep 2026, W2 · 9–15 Sep 2026, receive(payload, mime, sender, ts, *, original_name), Idempotent Upsert on a SHA-256 of the Source Bytes, Two-Stage Quarantine With a Vision Second Pass, Handing a batch over (+5 more)

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

### Community 247 - "advice_consents"
Cohesion: 0.33
Nodes (7): advice_consents(), 1. What counts, B1. The only erasure paths that exist, B2. What deleting a `documents` row cascades to, and what it leaves, B4. Does today's system meet Part A?, Part B. What the code does today, Status against the code

### Community 248 - "Claude Code — read this first"
Cohesion: 0.33
Nodes (5): Before you say you are done, Claude Code — read this first, Finding your way around, Skills and commands, The three things agents get wrong here

### Community 249 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 250 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 251 - "12. Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.33
Nodes (5): 12. Chunks follow the document's headings, and embeddings use the model's task prompts, Consequences, Context, Decision, Evidence

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

### Community 256 - "`docs/report/` — the final report"
Cohesion: 0.33
Nodes (6): `docs/report/` — the final report, Ownership, Source documents written for the report, The rule that keeps it honest, The thing to understand before you write a word, Three questions for the supervisors, at the 6 October mid-term

### Community 257 - "About Integrated Shield Plan"
Cohesion: 0.25
Nodes (8): About Integrated Shield Plan, How do I find out if I have an Integrated Shield Plan?, How do Integrated Shield Plan premiums and claims work?, Integrated Shield Plan (MediShield Life component plus a private insurance component), Should I consider purchasing an Integrated Shield Plan?, What is an Integrated Shield Plan?, Comparison of Private Hospital IPs (MOH, Jun 2026), Standard Integrated Shield Plans targeted at Ward Class B1 (MOH, Jun 2026)

### Community 258 - "Lifecycle"
Cohesion: 0.29
Nodes (3): Lifecycle, test_exit_codes_tell_the_supervisor_what_to_do(), test_the_first_request_wins_and_exit_is_asked_for_once()

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

### Community 264 - "1. Record architecture decisions"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 265 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 266 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 267 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

### Community 268 - "13. A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.40
Nodes (5): 13. A question is understood before it is searched, and scoped before it is cut, Consequences, Context, Decision, Evidence

### Community 269 - "Data inventory — identity data, dates of birth and loans"
Cohesion: 0.40
Nodes (4): Data inventory — identity data, dates of birth and loans, Open questions for Siew, The inventory, What this entry covers

### Community 270 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 271 - "cron_expressions"
Cohesion: 0.38
Nodes (4): cron_expressions(), manifest(), test_alert_is_swept_nightly_even_though_its_manifest_says_fact_write(), test_the_reminder_cron_is_read_from_its_manifest_not_written_twice()

### Community 272 - "`core/ingest/` — the ingestion worker"
Cohesion: 0.50
Nodes (3): `core/ingest/` — the ingestion worker, Quarantine is two-stage, Rules

### Community 273 - "`core/retrieve/` — hybrid retrieval"
Cohesion: 0.50
Nodes (3): `core/retrieve/` — hybrid retrieval, Rules, What belongs here

### Community 274 - "quarantine.tsx"
Cohesion: 0.29
Nodes (4): GoneRow(), QuarantineQueue(), QuarantineRow(), QuarantinedDocument

### Community 275 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 276 - "15. A name scopes a question, and a grandparent is not a parent"
Cohesion: 0.50
Nodes (4): 15. A name scopes a question, and a grandparent is not a parent, Consequences, Context, Decision

### Community 279 - "`docs/governance/` — the assurance artefacts"
Cohesion: 0.50
Nodes (3): `docs/governance/` — the assurance artefacts, The autonomy statement in one line, The rule that governs all eight

### Community 283 - "createPseudoSheet"
Cohesion: 0.67
Nodes (4): createPseudoSheet(), importantify(), scanUnquotedUrl(), stripComments()

### Community 284 - "Incident log"
Cohesion: 0.50
Nodes (3): Incident log, Incidents, Template

### Community 288 - "Pack grounding corpus rules"
Cohesion: 0.50
Nodes (3): ISO/IEC 22989 stages versus 5338 processes, Grounding corpora, Pack grounding corpus rules

### Community 294 - "The Grounding Gate"
Cohesion: 0.29
Nodes (7): The Core Answering Layer, The Answer Path: route, retrieve, rerank, ground, answer or abstain, The Grounding Gate, The Score Floor the Gate Reads, Kidney Stones: Inpatient Covered, Outpatient ESWL Excluded, Ask Screen, Try to Make It Lie: the Abstention Test

### Community 337 - "ADR index (0001-0018, with status)"
Cohesion: 0.09
Nodes (24): ADR 0001 - Record architecture decisions, ADR 0002 - One PostgreSQL instance for everything, Reciprocal rank fusion of dense and lexical, ADR 0003 - PaperBrain informs the pattern, not the module, PaperBrain prototype, ADR 0004 - Local setup can run before the assistant is ready, ADR 0006 - pypdfium2 renders the quarantine page images, ADR 0007 - The graph ships before retrieval and before a checkpoint table (+16 more)

### Community 459 - "The final ILP report"
Cohesion: 0.20
Nodes (6): SYNTHETIC DOCUMENT footer, Governance artefact set, The 40-document holdout corpus, The case for synthetic evaluation data, The final ILP report, The honesty check

### Community 550 - "Adversarial testing from week 7"
Cohesion: 0.20
Nodes (9): The answer graph: router, retrieve, rerank, grounding gate, Capability modules: Reminder and Alert, Adversarial testing from week 7, Contradiction attack, Prompt injection carried inside a document, Scope attack: asking it to act, Rachel - Reminder module on Today, Marcus - Alert module on Today (SRS ceiling) (+1 more)

### Community 552 - "Two-stage quarantine with a vision-language second pass"
Cohesion: 0.14
Nodes (11): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Lane A - Integration and product, Two-stage quarantine with a vision-language second pass, Christian's generated task list, Batch 4: the deliberately hard documents, Task: review every quarantined document and label the failure, Data inventory and flow map (+3 more)

### Community 553 - "Nobody edits core/contracts.py in a feature pull request"
Cohesion: 0.33
Nodes (4): The code pass of the knowledge graph, The semantic pass of the knowledge graph, Task: define the pack catalogue - the nine deferred packs, The household ledger - specified, not built in v1

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
- **885 isolated node(s):** `session-start.sh script`, `PATH`, `The two instruments`, `The framework's terms, and ours`, `4. Enable end-user responsibility (§2.4, pp 46–49)` (+880 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 2310 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **84 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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