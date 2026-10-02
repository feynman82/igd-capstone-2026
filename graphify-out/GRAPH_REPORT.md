# Graph Report - igd-capstone-2026  (2026-10-02)

## Corpus Check
- 316 files · ~727,509 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 34 file(s) not represented in the graph (top: (none) 11, .jsonl 7, .csv 5)

## Summary
- 4744 nodes · 11674 edges · 229 communities (181 shown, 48 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1086 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b71717e4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Ollama
- test_hybrid.py
- ScriptedOllama
- test_answer_graph.py
- test_register_validation.py
- advice/__init__.py
- Provenance register for corpus sg_protection_guidance
- test_advice_module.py
- api.ts
- FakeOllama
- main
- test_worker_queue.py
- FolderAdapter
- TelegramAdapter
- date
- .stream
- bench_runtime.py
- vault.py
- support.js
- values.py
- test_ingest_pipeline.py
- test_registration.py
- report.py
- pathlib
- ingest/quarantine.py
- SentenceScanner
- household.py
- packs.py
- test_lifecycle.py
- score.py
- test_household.py
- .load
- test_pages.py
- _pages_from
- test_eval_generate.py
- FakeConn
- ModuleManifest
- Any
- Overdue
- test_api.py
- alert/__init__.py
- retrieve.py
- sse
- Any
- test_startup.py
- score_obligations
- Passage
- pipeline.py
- build_router
- scope.py
- compilerOptions
- InstalledPack
- installed_packs
- test_grounding.py
- harness.py
- cli.py
- eval/modules.py
- ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic
- build.py
- test_grounding_index.py
- test_telegram_capture.py
- test_grounding_values.py
- create_app
- lock.ts
- ModuleAdviser
- routes.py
- PARROT Interface Design Pack
- export-design-preview.cjs
- The Four Surfaces
- typing
- advice-consent.tsx
- devDependencies
- ScriptedClient
- Hybrid Retrieval: Dense Plus Full-Text
- worker.py
- ADR 0011: The household is people and aliases, and the owner is one of them
- test_advice_core.py
- test_modules.py
- Calculation
- test_eval_harness.py
- preview.tsx
- generate.py
- Two-stage quarantine with a vision-language second pass
- Any
- Ollama
- packs/page.tsx
- test_contracts.py
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- Any
- components.json
- test_eval_modules.py
- validate
- advice-card.tsx
- test_eval_report.py
- The Lim Household, Tampines
- ADR 0007 - The graph ships before retrieval and before a checkpoint table
- Lane C - Governance and assurance
- Measured
- Core Document Catalogue (ADR 0017)
- main
- _kind
- The five-lane split (five people, nine weeks, three builders)
- Data inventory: identity data, DOBs and loans
- test_rerank.py
- Roadmap phase 3 - reminders
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
- HouseholdScope
- Integration review
- _today_items
- phrasings.py
- TelegramCapture
- Generated
- Terms of use
- The deliberately naive retrieval baseline
- Running the evaluation harness
- vault/page.tsx
- The case for synthetic evaluation data
- Domain pack
- Filling the corpus register
- Writing a governance artefact
- Two-Stage Quarantine With a Vision Second Pass
- Fill the Register Before Generating Documents
- Where Things Live
- Policy schedule HTML template
- PaperBrain
- ADR 0013: A question is understood before it is searched, and scoped before it is cut
- answer.tsx
- mentions
- Settings
- schedule.py
- PrivateCare Policy Wording Template
- alert module manifest
- dependencies
- test_the_inventory_always_reads_core_documents
- app/layout.tsx
- The Grounding Gate
- Authoring a domain pack
- ADR 0008 - Ingestion runs on a Celery worker
- classify
- DesignPreview evaluation harness
- test_an_unscoped_result_is_not_empty_for_the_owner
- build_team_tasks.py
- Adversarial testing from week 7
- Writing an ADR
- Every Fact Row Cites Its Source
- _graph_for
- Cursor
- eslint.config.mjs
- PARROT evaluation harness
- Any
- The autonomy statement
- scripts
- ModuleMetrics
- _as_module_summary
- Due
- ADR index (0001-0018, with status)
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- _answer_events
- test_both_ask_endpoints_hand_the_graph_the_same_advice_ports
- The synthetic-to-real gap
- filesystem
- FakeConn
- answer.py
- Part A. Policy
- Scoped
- correct
- _page_of_examples
- One Database
- _columns
- FakeTelegram
- FakeCursor
- Lane E - Corpus and adversarial testing
- advice_consents
- Alert
- setup.sh
- session-start.sh
- package.json
- Any
- postcss.config.mjs
- Lane C - Governance and assurance
- parrot
- State
- main
- contracts.py
- FakeCursor
- paperbrain/chunk.py
- sweep
- test_reindexing_replaces_chunks_and_leaves_facts_alone
- _ordered
- IMDA frameworks: what applies to PARROT
- quiet_engine
- printed_date
- Send
- resolve_names
- Obligation
- Config
- insurance

## God Nodes (most connected - your core abstractions)
1. `Settings` - 189 edges
2. `Passage` - 95 edges
3. `ScriptedOllama` - 87 edges
4. `InstalledPack` - 84 edges
5. `AnswerGraph` - 77 edges
6. `FakeConn` - 75 edges
7. `settings()` - 75 edges
8. `client_for()` - 74 edges
9. `build_router()` - 73 edges
10. `Ollama` - 70 edges

## Surprising Connections (you probably didn't know these)
- `GenAI framework: nine dimensions` --references--> `GroundingDocument`  [INFERRED]
  docs/governance/imda-what-applies.md → core/contracts.py
- `Agentic AI framework: four dimensions` --references--> `Guardrails`  [INFERRED]
  docs/governance/imda-what-applies.md → core/contracts.py
- `Agentic AI framework: four dimensions` --references--> `check_one()`  [INFERRED]
  docs/governance/imda-what-applies.md → core/graph/gate.py
- `Agentic AI framework: four dimensions` --references--> `local_url()`  [INFERRED]
  docs/governance/imda-what-applies.md → core/runtime/settings.py
- `B1. The only erasure paths that exist` --references--> `documents()`  [INFERRED]
  docs/governance/retention-and-erasure.md → core/vault.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The four code-scored metrics that need no judge** — eval_readme_abstention_rate, eval_readme_extraction_f1, eval_readme_obligation_precision, eval_readme_alert_fpr, eval_readme_evaluation [EXTRACTED 1.00]
- **One field name, one place: pack.yaml to register to extractor to score** — team_zee_readme_pack_yaml_is_the_only_authored_file, team_desmond_readme_generated_column_headings, team_desmond_readme_document_register, team_desmond_readme_corpus_validate, team_yew_mun_readme_golden_set_a, team_desmond_readme_expiry_date_stopgap [EXTRACTED 1.00]
- **The five-lane ownership split of the repository** — team_christian_readme_lane_a_integration, team_yew_mun_readme_lane_b_retrieval, team_siew_readme_lane_c_governance, team_zee_readme_lane_d_packs_and_interface, team_desmond_readme_lane_e_corpus [EXTRACTED 1.00]
- **Insurance coverage review: shapes, guideline keys and held categories answered in one pass** — packs_insurance_agent_pack_review, packs_insurance_agent_pack_death_tpd_cover, packs_insurance_agent_pack_ci_cover, packs_insurance_agent_pack_death_tpd_income_multiple, packs_insurance_agent_pack_ci_income_multiple, packs_insurance_agent_pack_hospital_expense, packs_insurance_agent_pack_long_term_care, packs_insurance_agent_pack_advice_consent [EXTRACTED 1.00]
- **The pack contract, revised across three ADRs** — docs_adr_0014_a_pack_supplies_knowledge_and_the_core_stays_generic_packmanifest_answering, docs_adr_0014_a_pack_supplies_knowledge_and_the_core_stays_generic_advice_decline_route, docs_adr_0016_a_pack_advises_code_calculates_under_recorded_consent_advice_shapes, docs_adr_0016_a_pack_advises_code_calculates_under_recorded_consent_verdict_by_code, docs_adr_0017_a_pack_is_grounding_and_persona_the_core_owns_documents_a_pack_is_knowledge_and_voice, docs_adr_0017_a_pack_is_grounding_and_persona_the_core_owns_documents_core_documents_yaml, docs_adr_0017_a_pack_is_grounding_and_persona_the_core_owns_documents_two_answering_layers [EXTRACTED 1.00]
- **Pack-first pipeline: a pack's field names gate the register, the corpus, evaluation and governance** — team_readme_pack_to_register_dependency, team_readme_lane_d_zee, team_readme_lane_e_desmond, team_readme_lane_b_yew_mun, team_readme_lane_c_siew, packs_iras_tax_pack_iras_tax [EXTRACTED 1.00]
- **Startup and power: the five lifecycle screens** — docs_artefacts_parrot_uiux_refinement_startup_and_power_main_dc_getting_parrot_ready, docs_artefacts_parrot_uiux_refinement_startup_and_power_powermenu_dc_power_menu, docs_artefacts_parrot_uiux_refinement_startup_and_power_restarting_dc_restarting_parrot, docs_artefacts_parrot_uiux_refinement_startup_and_power_shutdown_dc_parrot_is_off, docs_artefacts_parrot_uiux_refinement_startup_and_power_startupblocked_dc_waiting_for_its_database [EXTRACTED 1.00]
- **The five lanes of Project PARROT** — docs_team_lane_a_integration_and_product, docs_team_lane_b_retrieval_and_evaluation, docs_team_lane_c_governance_and_assurance, docs_team_lane_d_domain_packs_and_interface, docs_team_lane_e_corpus_and_adversarial_testing [EXTRACTED 1.00]
- **The Answer Path, End to End** — core_graph_readme_answer_path, core_retrieve_readme_hybrid_search, core_retrieve_readme_rrf_fusion, core_retrieve_readme_cross_encoder_reranker, core_graph_readme_grounding_gate, core_retrieve_readme_score_floor, api_readme_the_surface [EXTRACTED 1.00]
- **The Hard Rules of the Working Agreement** — agents_no_runtime_sql_generation, agents_every_fact_cites_its_source, agents_no_claim_without_a_citation, agents_contracts_are_a_separate_pr, agents_no_new_runtime_dependency_without_an_adr, agents_generated_files_have_one_source_of_truth, agents_packs_may_not_import_the_interface, agents_never_acts, agents_amend_the_graph_refresh_into_the_commit [EXTRACTED 1.00]
- **The three PARROT interface directions evaluated side by side** — docs_artefacts_parrot_uiux_refinement_uploads_parrot_design_evaluation_designpreview, docs_artefacts_parrot_uiux_refinement_uploads_parrot_design_evaluation_civic_register, docs_artefacts_parrot_uiux_refinement_uploads_parrot_design_evaluation_kitchen_table, docs_artefacts_parrot_uiux_refinement_uploads_parrot_design_evaluation_the_reading_desk [EXTRACTED 1.00]
- **The Ground-Truth Chain: Catalogue, Canon, Register, Templates, Validator** — core_documents_document_types, corpus_canon_lim_household, corpus_readme_register_first_order, corpus_templates_payslip_payslip_template, corpus_templates_hospital_income_policy_wording_policy_contract, corpus_readme_field_pages_second_pass, corpus_readme_handover_gate [INFERRED 0.85]
- **The grounded-refusal flow: gate, abstention screen, hard negatives, adversarial probe** — team_christian_readme_answer_graph, web_docs_user_stories_abstention_is_a_designed_screen, team_yew_mun_readme_golden_set_b, team_siew_readme_adversarial_set_c, team_siew_readme_autonomy_statement, team_desmond_readme_scope_attack [INFERRED 0.85]
- **Household scoping: from a printed name to a scoped answer** — docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_people, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_person_aliases, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_facts_subject, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_three_buckets, docs_adr_0013_a_question_is_understood_before_it_is_searched_possessive_relations_scope, docs_adr_0015_a_name_scopes_and_a_grandparent_is_not_a_parent_a_question_naming_exactly_one_person_is_theirs, docs_adr_0015_a_name_scopes_and_a_grandparent_is_not_a_parent_grandparent_is_a_relation_nobody_can_hold, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_resolved_person_chip [INFERRED 0.85]
- **The boundary: it abstains, it cites, and it never acts** — docs_pack_authoring_guardrails, docs_demo_run_sheet_the_abstention, docs_demo_run_sheet_the_refusal_to_act, docs_demo_run_sheet_the_source_chip, docs_adr_0007_the_graph_ships_before_retrieval_and_before_a_checkpoint_table_adr_0007 [INFERRED 0.85]
- **Capture to indexed document, and what happens when it fails** — docs_running_start_cmd, docs_running_watched_inbox_folder, docs_running_ingestion_worker, docs_running_quarantine_second_pass, docs_adr_0005_polling_the_watched_folder_adr_0005, docs_adr_0008_ingestion_runs_on_a_celery_worker_adr_0008, docs_adr_0006_pypdfium2_for_the_quarantine_image_pass_adr_0006 [INFERRED 0.95]
- **Module manifests sharing the reads/writes/runs/surfaces contract** — modules__template_module_module_template, modules_advice_module_advice, modules_alert_module_alert, modules_reminder_module_reminder [INFERRED 0.95]
- **The 9x/4x protection rule of thumb and the published sources a person approved it from** — packs_insurance_agent_grounding_sg_protection_guidance_moneysense_bfpg_faq_protection_rule_of_thumb, packs_insurance_agent_grounding_sg_protection_guidance_moneysense_bfpg_faq_consumer_faqs, packs_insurance_agent_grounding_sg_protection_guidance_moneysense_bfpg_starting_a_family_starting_a_family_guide, packs_insurance_agent_grounding_sg_protection_guidance_moneysense_basic_financial_planning_basic_financial_planning_guide, packs_insurance_agent_grounding_sg_protection_guidance_lia_protection_gap_study_protection_gap_study_2022, packs_insurance_agent_pack_death_tpd_income_multiple, packs_insurance_agent_pack_ci_income_multiple [INFERRED 0.95]

## Communities (229 total, 48 thin omitted)

### Community 0 - "Ollama"
Cohesion: 0.08
Nodes (19): digest_of_document(), connect(), Ollama, uses_task_prompts(), build(), application(), ingest(), register() (+11 more)

### Community 1 - "test_hybrid.py"
Cohesion: 0.14
Nodes (13): hybrid_score(), identifiers(), prints(), FakeConn, FakeOllama, _row(), test_a_chunk_prints_an_identifier_however_it_is_spaced(), test_a_paraphrase_keeps_every_score_where_cosine_put_it() (+5 more)

### Community 2 - "ScriptedOllama"
Cohesion: 0.07
Nodes (43): AdviceCard, AdviceWithheld, answer_system(), ConsentRequired, Finished, _unknown_relation(), Subject, advised_pack() (+35 more)

### Community 3 - "test_answer_graph.py"
Cohesion: 0.07
Nodes (58): Abstained, AnswerGraph, Declined, Refused, Sentence, ModelUnavailable, test_advice_is_declined_when_the_graph_was_given_no_adviser(), build() (+50 more)

### Community 4 - "test_register_validation.py"
Cohesion: 0.14
Nodes (15): test_a_batch_mixes_packs_in_one_register(), test_a_header_without_field_pages_is_caught(), test_a_row_with_no_fields_carries_no_ground_truth(), test_an_unparseable_page_is_caught(), test_duplicate_ids_are_caught(), test_expiry_before_start_is_caught(), test_field_pages_naming_a_field_the_row_does_not_fill_is_caught(), test_field_pages_records_the_page_a_value_is_printed_on() (+7 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.09
Nodes (41): Figure, Input, _ambiguous(), _amount(), _band(), _band_label(), Basis, _calculation() (+33 more)

### Community 6 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.05
Nodes (59): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, MediShield Life (CPF Board), Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022 (+51 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.15
Nodes (46): Missing, calculate(), basis(), fact(), figures_of(), _gap_basis(), _held(), _held_ward() (+38 more)

### Community 8 - "api.ts"
Cohesion: 0.05
Nodes (46): dynamic, HouseholdPage(), metadata, runtime, AppLayout(), dynamic, isUrgent(), metadata (+38 more)

### Community 9 - "FakeOllama"
Cohesion: 0.16
Nodes (18): extract(), FakeOllama, test_a_date_that_cannot_be_read_still_quarantines(), test_a_long_document_whose_front_is_enough_is_read_once(), test_a_long_document_whose_front_is_not_enough_is_read_in_full(), test_a_model_that_does_not_answer_is_not_asked_a_longer_question(), test_a_null_shaped_string_in_a_required_field_is_still_a_failure(), test_a_null_shaped_string_is_an_absent_field_not_a_bad_number() (+10 more)

### Community 10 - "main"
Cohesion: 0.12
Nodes (14): approve(), pending(), PendingValue, reject(), _block(), main(), test_approve_passes_only_the_ids_and_the_pending_condition(), test_list_block_shows_id_pack_key_value_source_and_an_indented_passage() (+6 more)

### Community 11 - "test_worker_queue.py"
Cohesion: 0.07
Nodes (23): sha256(), Inline, Queued, Intake, Registration, bytes_for(), index_folder(), SourceMissing (+15 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.09
Nodes (19): CaptureAdapter, IngestJob, FolderAdapter, _Pending, _Registered, FakeRegistrar, _settle(), test_a_file_removed_before_it_settles_is_forgotten() (+11 more)

### Community 13 - "TelegramAdapter"
Cohesion: 0.13
Nodes (6): _attachment(), _pixels(), _status_reason(), TelegramAdapter, _write_local_copy(), B3. Things erasure has to reach beyond the database

### Community 14 - "date"
Cohesion: 0.23
Nodes (9): document_row(), fact_row(), test_a_citation_that_resolves_to_nothing_still_says_what_it_said(), test_a_core_document_stays_enabled_when_every_pack_is_off(), test_an_alerts_citation_carries_the_document_it_opens(), test_one_document_is_shown_even_when_its_pack_is_off(), test_today_is_ordered_overdue_then_alerts_then_reminders(), test_vault_lists_documents_with_their_facts() (+1 more)

### Community 15 - ".stream"
Cohesion: 0.10
Nodes (7): _as_sentence(), _citations(), _max_sentences(), _numbered(), _pack_for(), Holding, test_a_type_no_pack_speaks_for_is_governed_by_the_core()

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (20): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+12 more)

### Community 17 - "vault.py"
Cohesion: 0.20
Nodes (8): _as_document(), declared_type(), document(), documents(), Fact, _facts_for(), VaultDocument, VaultPage

### Community 18 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 19 - "values.py"
Cohesion: 0.08
Nodes (22): _check(), collapse(), _cuts_a_number(), extract_values(), _groups(), _is_heading(), number_tokens(), _pack() (+14 more)

### Community 20 - "test_ingest_pipeline.py"
Cohesion: 0.11
Nodes (18): _date_renderings(), find_page(), _normalise(), Block, _policy_page(), test_a_chunk_never_starts_or_ends_inside_a_word(), test_a_date_of_birth_printed_day_first_with_dashes_is_found(), test_a_date_on_no_page_still_has_no_page() (+10 more)

### Community 21 - "test_registration.py"
Cohesion: 0.29
Nodes (8): register_document(), conn(), database_url(), test_a_document_must_arrive_with_a_name(), test_a_new_document_is_inserted(), test_an_empty_payload_is_refused(), test_different_bytes_are_different_documents(), test_the_same_bytes_update_in_place_and_do_not_insert_a_second_row()

### Community 22 - "report.py"
Cohesion: 0.14
Nodes (11): _cell(), collect(), main(), _overall(), _paragraph(), _row(), _statuses(), _summary() (+3 more)

### Community 23 - "pathlib"
Cohesion: 0.05
Nodes (19): FolderSettings, Dispatcher, install_best_effort(), broker_available(), dispatcher_for(), FolderCapture, DatabaseUnavailable, _chat_ids() (+11 more)

### Community 24 - "ingest/quarantine.py"
Cohesion: 0.08
Nodes (23): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), classification_sample(), ParsedPage, blocked_reasons() (+15 more)

### Community 25 - "SentenceScanner"
Cohesion: 0.05
Nodes (20): SentenceScanner, DoclingParser, _as_printed(), page_pixels(), photographed(), _register_row(), scanned(), test_a_scan_keeps_the_schedule_table_and_its_page() (+12 more)

### Community 26 - "household.py"
Cohesion: 0.09
Nodes (21): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+13 more)

### Community 27 - "packs.py"
Cohesion: 0.09
Nodes (13): DocumentTypeSpec, _prompt(), _coerce(), decode_schema(), _drop_format(), ExtractedFact, Extraction, _prepare() (+5 more)

### Community 28 - "test_lifecycle.py"
Cohesion: 0.13
Nodes (19): Lifecycle, _client(), _eventually(), _launcher(), Screens, _supervise(), test_a_browser_cannot_reach_the_engine_directly_even_with_the_header(), test_a_request_without_the_intent_header_is_refused() (+11 more)

### Community 29 - "score.py"
Cohesion: 0.09
Nodes (23): Trace, cites(), declined_in_prose(), doc_stem(), grade(), held_back(), inventory_only(), Judge (+15 more)

### Community 30 - "test_household.py"
Cohesion: 0.08
Nodes (25): is_first_person(), relation_asked(), _household_scope(), test_a_grandparent_nobody_holds_is_an_unknown_relation_not_the_fathers_policy(), test_a_grandparent_recorded_under_that_name_is_who_the_question_means(), test_a_name_that_is_not_exactly_one_person_scopes_nothing(), test_a_named_household_member_wins_over_the_pronoun(), test_a_person_nobody_has_confirmed_is_not_named() (+17 more)

### Community 31 - ".load"
Cohesion: 0.11
Nodes (23): ModelWarmth, warm_models(), _folder(), _ollama_answering(), test_a_database_that_does_not_answer_fails_in_seconds(), test_a_model_that_cannot_load_is_recorded_rather_than_raised(), test_an_embedding_model_without_task_prompts_is_sent_the_text_alone(), test_an_explicit_url_still_wins_over_the_port_variable() (+15 more)

### Community 32 - "test_pages.py"
Cohesion: 0.08
Nodes (20): page_images(), page_count(), PageUnavailable, _pdfium(), render_page(), RendererUnavailable, _size(), test_a_damaged_pdf_is_a_sentence_not_a_traceback() (+12 more)

### Community 33 - "_pages_from"
Cohesion: 0.27
Nodes (9): _pages_from(), _table_text(), _cell(), _on_page(), test_a_document_is_titled_by_the_string_fields_its_pack_declares(), test_a_table_is_kept_as_label_and_value_lines_in_reading_order(), test_a_wider_table_keeps_every_column_and_a_spanned_cell_once(), test_an_item_with_neither_text_nor_cells_is_still_skipped() (+1 more)

### Community 34 - "test_eval_generate.py"
Cohesion: 0.11
Nodes (15): hand_written(), main(), on_file(), lane_of(), read_register(), read_registers(), _asked(), test_a_question_a_person_already_wrote_is_not_generated_again() (+7 more)

### Community 35 - "FakeConn"
Cohesion: 0.06
Nodes (33): client(), conn(), FakeConn, filed_document(), inbox(), next_kind(), obligation(), overdue_row() (+25 more)

### Community 36 - "ModuleManifest"
Cohesion: 0.10
Nodes (14): ModuleManifest, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, enabled_module_ids(), install(), Installed (+6 more)

### Community 37 - "Any"
Cohesion: 0.14
Nodes (10): by_subject(), db(), FakeCursor, load_register(), test_a_deductible_receipt_counts_in_its_own_year_only(), test_a_lapsed_policy_is_not_masked_by_another_that_still_runs(), test_cpf_is_this_years_payslips_per_employee(), test_donations_are_this_years_deductible_receipts_per_donor() (+2 more)

### Community 38 - "Overdue"
Cohesion: 0.12
Nodes (7): close(), current_lead(), next_window(), Overdue, snooze(), UnknownObligation, test_the_tightest_entered_window_is_the_current_one()

### Community 39 - "test_api.py"
Cohesion: 0.08
Nodes (27): Answer, Cited, Asks, outcome_of(), FakeGraph, graph(), test_a_turn_can_only_be_the_person_or_parrot(), test_an_ask_citation_needs_no_lookup_to_be_openable() (+19 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.19
Nodes (10): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), srs_contributions_ytd(), _totals() (+2 more)

### Community 41 - "retrieve.py"
Cohesion: 0.18
Nodes (10): Connection, load_matrix(), pack(), unpack(), _fts_query(), fuse(), hydrate(), keyword_search() (+2 more)

### Community 42 - "sse"
Cohesion: 0.10
Nodes (22): Citation, Reading, a_citation(), advice_card(), rule_citation(), sse(), StreamingGraph, test_a_citation_says_whether_it_is_a_page_or_a_document_on_file() (+14 more)

### Community 43 - "Any"
Cohesion: 0.10
Nodes (17): advised_pack(), db(), _document(), _facts_tuple(), FakeConn, FakeCursor, _source(), _sum_insured() (+9 more)

### Community 44 - "test_startup.py"
Cohesion: 0.13
Nodes (13): start_web(), main(), report_hardware(), startup_gaps(), prepare_checkout(), test_check_only_never_launches_even_when_ready(), test_incomplete_checkout_never_launches_a_process(), test_launch_preserves_paths_and_loopback_and_exit_code() (+5 more)

### Community 45 - "score_obligations"
Cohesion: 0.15
Nodes (12): obligation_precision(), _same_person(), score_obligations(), Verdict, _obligation(), test_a_calendar_deadline_is_checked_against_the_catalogue_and_counted_apart(), test_a_date_the_document_does_not_print_is_a_false_obligation(), test_an_obligation_for_a_document_the_register_does_not_have() (+4 more)

### Community 46 - "Passage"
Cohesion: 0.05
Nodes (43): check(), check_advice(), check_content(), check_one(), Claim, _normal(), precheck(), _says() (+35 more)

### Community 47 - "pipeline.py"
Cohesion: 0.06
Nodes (19): Chunk, fixed(), from_facts(), _label(), parse(), ParsedDocument, Parser, PlainTextParser (+11 more)

### Community 48 - "build_router"
Cohesion: 0.10
Nodes (24): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, RetryAccepted, build_router(), add_person() (+16 more)

### Community 49 - "scope.py"
Cohesion: 0.21
Nodes (8): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Person

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 51 - "InstalledPack"
Cohesion: 0.06
Nodes (34): Categories, Category, _review_asked(), holdings(), Inventory, Asked, categories_asked(), categorise() (+26 more)

### Community 52 - "installed_packs"
Cohesion: 0.14
Nodes (10): installed_packs(), _pack_row(), packs(), RegisteredPack, set_pack_enabled(), UnknownModule, UnknownPack, test_every_installed_pack_still_loads() (+2 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.18
Nodes (12): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), _document(), _installed(), test_a_missing_recorded_file_is_refused(), test_a_pack_with_no_corpus_gives_none_and_empty() (+4 more)

### Community 54 - "harness.py"
Cohesion: 0.07
Nodes (14): HouseholdAdviceLog, DenseRetriever, NoReranker, HouseholdInventory, enabled_pack_ids(), enabled_packs(), HybridRetriever, build() (+6 more)

### Community 55 - "cli.py"
Cohesion: 0.17
Nodes (13): build_parser(), _client(), cmd_add(), cmd_docs(), cmd_doctor(), cmd_init(), cmd_search(), cmd_stats() (+5 more)

### Community 56 - "eval/modules.py"
Cohesion: 0.10
Nodes (20): main(), measure(), obligations(), obligations_possible(), _paragraph(), score_alerts(), _chosen(), _corpus_sha() (+12 more)

### Community 57 - "ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.15
Nodes (17): Code-written absence sentence: 'None of the N policies on file is a dental plan.', ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic, The advise route intent returns the pack's advice_decline, answering.categories: ordered whole-word rules over one printed field, Category filter applied before the keep-6 cut, answering.exclusions: headings under which a cover claim is not believed, Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration) (+9 more)

### Community 58 - "build.py"
Cohesion: 0.09
Nodes (13): DocumentCatalog, _class_name(), _docstring(), _field_line(), _header(), load(), load_catalog(), main() (+5 more)

### Community 59 - "test_grounding_index.py"
Cohesion: 0.11
Nodes (24): GroundingDocument, SourceText, index_pack(), IndexReport, _upsert_source(), ExtractedValue, _extracted(), _installed() (+16 more)

### Community 60 - "test_telegram_capture.py"
Cohesion: 0.20
Nodes (18): build(), photo_update(), test_a_chat_outside_the_allow_list_is_ignored(), test_a_conflict_names_the_webhook_rather_than_saying_nothing(), test_a_document_keeps_the_name_it_was_sent_under(), test_a_malformed_allow_list_is_a_configuration_error_not_an_empty_one(), test_a_photograph_becomes_a_document_on_the_telegram_channel(), test_a_rejected_token_says_which_setting_is_wrong() (+10 more)

### Community 61 - "test_grounding_values.py"
Cohesion: 0.16
Nodes (27): _dropped(), _log_values(), _run(), test_a_money_value_with_a_currency_marker_is_kept(), test_a_multiple_is_kept_in_the_forms_it_is_written(), test_a_number_is_kept_when_one_of_its_occurrences_fits_the_unit(), test_a_number_matches_its_printed_decimal_form(), test_a_number_not_in_its_passage_is_dropped() (+19 more)

### Community 62 - "create_app"
Cohesion: 0.27
Nodes (6): create_app(), checks(), lifespan(), ready(), setup(), system_status()

### Community 63 - "lock.ts"
Cohesion: 0.07
Nodes (45): dynamic, GET(), grant(), POST(), runtime, ALLOWED, Context, DELETE() (+37 more)

### Community 64 - "ModuleAdviser"
Cohesion: 0.10
Nodes (13): FactInput, fact_row(), FactRow, facts_for(), in_category(), _is_an_adviser(), ModuleAdviser, names_for() (+5 more)

### Community 65 - "routes.py"
Cohesion: 0.08
Nodes (33): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, AskRequest, CloseRequest, ConfirmNameRequest, ConsentRequest (+25 more)

### Community 66 - "PARROT Interface Design Pack"
Cohesion: 0.09
Nodes (21): Citation chips are the trust surface, Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Suggestions come from this week's ingest, Civic Register: order, clarity and institutional confidence, Kitchen Table: a little less household admin, a little more breathing room, The Reading Desk: understand it, open the source, see for yourself (+13 more)

### Community 67 - "export-design-preview.cjs"
Cohesion: 0.10
Nodes (17): bundle(), classes, css, cssFile, domId, fs, ids, licences (+9 more)

### Community 68 - "The Four Surfaces"
Cohesion: 0.13
Nodes (14): The FastAPI Application, The API Surface, apply, Auto-Redirect to Today Once Ready, check, draw, Five Readiness Rows in Plain Words, poll (+6 more)

### Community 69 - "typing"
Cohesion: 0.07
Nodes (3): render(), sniff_mime(), Registrar

### Community 70 - "advice-consent.tsx"
Cohesion: 0.17
Nodes (17): Consent, ConsentPrompt(), agree(), settle(), State, ADR-0016, AdviceConsentSection(), fetchConsents() (+9 more)

### Community 71 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 72 - "ScriptedClient"
Cohesion: 0.16
Nodes (12): _long_text(), _reply(), ScriptedClient, _source(), test_a_json_reply_with_no_usable_values_is_no_values_for_that_section_only(), test_a_long_text_is_sent_in_more_than_one_call(), test_a_model_that_is_down_raises(), test_a_reply_that_is_not_a_json_object_raises_as_an_outage() (+4 more)

### Community 73 - "Hybrid Retrieval: Dense Plus Full-Text"
Cohesion: 0.18
Nodes (5): bge-reranker-v2-m3 Cross-Encoder, 40 Down to 6, Hybrid Retrieval: Dense Plus Full-Text, Reciprocal Rank Fusion, k=60, The Household's Eleven Policies, The Validator Is the Handover Gate

### Community 74 - "worker.py"
Cohesion: 0.14
Nodes (8): find_browser_executable(), generate_documents(), _beat_needs_its_own_process(), celery_argv(), main(), _run(), _start_beat(), _stop_beat()

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.17
Nodes (11): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), Telegram chat_id maps to a person, Possessive relations scope the question, before the cut to six, Naming exactly one person scopes to them (whole name, or a 3+ letter possessive unique to them) (+3 more)

### Community 76 - "test_advice_core.py"
Cohesion: 0.06
Nodes (30): current(), grant(), HouseholdConsents, _latest(), NoOwner, _record(), status(), withdraw() (+22 more)

### Community 77 - "test_modules.py"
Cohesion: 0.15
Nodes (18): AlertConfig, already_said(), sweep(), FakeConn, obligation_row(), test_a_dry_run_records_nothing(), test_a_metric_no_query_defines_cannot_fire(), test_a_sum_is_per_person_and_cites_only_that_persons_receipts() (+10 more)

### Community 78 - "Calculation"
Cohesion: 0.11
Nodes (16): Calculation, assert_nothing_negative(), _dual_cited_calculation(), _meets_calculation(), _shared_value_calculation(), _basis(), _latest(), _matched() (+8 more)

### Community 79 - "test_eval_harness.py"
Cohesion: 0.10
Nodes (21): Recorder, trace_all(), _runtime_numbers(), reference_for(), Expected, load_set(), MalformedQuestion, Question (+13 more)

### Community 80 - "preview.tsx"
Cohesion: 0.10
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 81 - "generate.py"
Cohesion: 0.18
Nodes (8): _ambiguous(), choose(), Generated, pool(), write_lane(), field_page(), test_choose_alternates_the_two_wordings_and_is_stable(), test_the_line_is_gradeable_by_construction()

### Community 82 - "Two-stage quarantine with a vision-language second pass"
Cohesion: 0.12
Nodes (11): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Two-stage quarantine with a vision-language second pass, Batch 4: the deliberately hard documents, Task: review every quarantined document and label the failure, Task: sign off the capture-to-database path against the data inventory, PaperBrain handled failure modes, The pb command line (+3 more)

### Community 83 - "Any"
Cohesion: 0.11
Nodes (3): ConsentCursor, Fails, FakeCursor

### Community 84 - "Ollama"
Cohesion: 0.16
Nodes (6): answer(), build_context(), format_sources(), cmd_ask(), Ollama, Hit

### Community 85 - "packs/page.tsx"
Cohesion: 0.15
Nodes (9): ADR-0017, dynamic, metadata, PacksPage(), runtime, Toggle(), ModuleSummary, packs() (+1 more)

### Community 86 - "test_contracts.py"
Cohesion: 0.08
Nodes (30): PackManifest, _advised(), _checked(), _insurance(), _market(), _market_compares_an_undeclared_field(), _tax(), test_a_grounding_corpus_is_named_by_id_not_by_path() (+22 more)

### Community 87 - "ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.16
Nodes (18): ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel), Advice graph flow: shape match, subject resolution, consent, AdviceCard, explain, advice_records keeps each answer's full basis, PackManifest.advice shapes (gap, remaining_room, keep_or_surrender, compare_own, compare_market, estimate_saving), Advice.review: one question runs every shape at once, A grounding corpus lives at packs/<pack>/grounding/<corpus_id>/ (+10 more)

### Community 88 - "Any"
Cohesion: 0.26
Nodes (14): _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact(), _field_not_on_every_doc_type(), _held_per_month() (+6 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "test_eval_modules.py"
Cohesion: 0.15
Nodes (8): alert_fpr(), AlertVerdict, Fired, test_a_metric_with_no_register_equivalent_is_not_guessed_at(), test_an_alert_the_register_agrees_with_is_not_counted_against_the_module(), test_an_alert_the_register_contradicts_is_a_false_positive(), test_nothing_fired_is_unmeasured_rather_than_zero(), test_what_the_register_supports_is_reported_beside_the_precision()

### Community 91 - "validate"
Cohesion: 0.18
Nodes (9): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), validate(), _wide_format() (+1 more)

### Community 93 - "advice-card.tsx"
Cohesion: 0.09
Nodes (24): Agentic AI framework: four dimensions, Advice, AdviceCard(), AdviceNote(), AdviceWithheld(), capitalise(), sentence(), TONES (+16 more)

### Community 94 - "test_eval_report.py"
Cohesion: 0.11
Nodes (21): Provenance, render(), extraction_by_type(), extraction_f1(), FactRow, _outcomes(), _totals(), unjoined() (+13 more)

### Community 95 - "The Lim Household, Tampines"
Cohesion: 0.15
Nodes (10): loan_agreement Document Type, payslip Document Type, The Lim Household, Tampines, Household Canon Template, Rule of 78 Rebate and the 20 Per Cent Early Settlement Penalty, Motor Vehicle Hire Purchase Agreement Template, Republic of Xinkapow, the Invented Jurisdiction, Residential Housing Loan Facility Letter Template (+2 more)

### Community 96 - "ADR 0007 - The graph ships before retrieval and before a checkpoint table"
Cohesion: 0.22
Nodes (7): ADR 0007 - The graph ships before retrieval and before a checkpoint table, .graphifyignore excludes the corpus, The redacted real-document holdout, Dense-only retrieval stopgap, Hardware qualification, Rebuilding the vault's vectors, Lane B - Retrieval and evaluation

### Community 97 - "Lane C - Governance and assurance"
Cohesion: 0.13
Nodes (9): Data inventory and flow map, ISO/IEC 22989 to 5338 stage-to-process map, Lane C - Governance and assurance, Model card, Retention and erasure policy, Siew's generated task list, Golden Set B - hard negatives (25), The nine metrics and their targets (+1 more)

### Community 98 - "Measured"
Cohesion: 0.20
Nodes (8): _day(), Measured, _number(), register_cpf_contributions_ytd(), register_days_uncovered(), register_donations_ytd(), register_srs_contributions_ytd(), test_the_register_metrics_mirror_the_modules_queries()

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.10
Nodes (11): Generated Files Committed Alongside Their Source, benefit_illustration Document Type, birth_certificate Document Type, claim_letter Document Type, cpf_statement Document Type, Core Document Catalogue (ADR 0017), donation_receipt Document Type, identity_card Document Type (+3 more)

### Community 100 - "main"
Cohesion: 0.15
Nodes (8): TelegramSettings, TelegramUnavailable, _loop(), main(), FakeRegistrar, test_an_adapter_without_a_token_refuses_to_be_built(), test_one_failing_update_does_not_take_the_rest_of_the_batch_with_it(), explode_once()

### Community 102 - "The five-lane split (five people, nine weeks, three builders)"
Cohesion: 0.09
Nodes (18): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The domain pack manifest, The expansion model: two axes, not one list, The golden set: answerable, hard negatives, adversarial, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build (+10 more)

### Community 103 - "Data inventory: identity data, DOBs and loans"
Cohesion: 0.17
Nodes (7): Data inventory: identity data, DOBs and loans, Telegram capture route and delete-at-source, What crosses a boundary, Governance artefact set, The final ILP report, db service (pgvector/pgvector:pg17), redis service (redis:7-alpine)

### Community 104 - "test_rerank.py"
Cohesion: 0.07
Nodes (22): CrossEncoderReranker, device_name(), load(), passage_text(), relevance(), score_pairs(), _warn_once(), reranker_check() (+14 more)

### Community 105 - "Roadmap phase 3 - reminders"
Cohesion: 0.14
Nodes (13): The answer graph: router, retrieve, rerank, grounding gate, Capability modules: Reminder and Alert, Task: build the answer graph with the grounding gate, Contradiction attack, Task: contextualised chunking and the reranker, Task: hybrid retrieval with reciprocal rank fusion, The reminders table as an extension point, Roadmap phase 3 - reminders (+5 more)

### Community 106 - "web/ - the PARROT interface"
Cohesion: 0.14
Nodes (10): Task: complete the Insurance Agent pack, The four surfaces: Today, Ask, Vault, Packs, Lane D - Domain packs and interface, Task: define the pack catalogue - the nine deferred packs, Zee's generated task list, Task: write the user stories with acceptance criteria, The household ledger - specified, not built in v1, Ask surface (+2 more)

### Community 107 - "The document register as ground truth"
Cohesion: 0.18
Nodes (5): python -m corpus.validate, The document register as ground truth, The household canon (the Lims of Tampines), Task: spot-check 20 register rows against the extractor, Golden Set A - answerable (60)

### Community 108 - "ingest.py"
Cohesion: 0.29
Nodes (8): cmd_ingest(), discover(), embed_chunks(), guess_date(), guess_type(), ingest_file(), IngestResult, sha256()

### Community 109 - "Tax and Reliefs — contract changes this pack needs"
Cohesion: 0.40
Nodes (4): 1. A deduction multiplier on `estimate_saving`, 2. Limiting a fact input to one year, Not a contract change: parent relief, Tax and Reliefs — contract changes this pack needs

### Community 110 - "Reminder, Alert and Tracker Registers"
Cohesion: 0.18
Nodes (12): filing_deadline Reminder, passport Document Type, passport_expiry Reminder, policy_expiry Reminder, policy_schedule Document Type, Reminder, Alert and Tracker Registers, renewal_notice Document Type, srs_contribution_cutoff Reminder (+4 more)

### Community 111 - "checks.py"
Cohesion: 0.14
Nodes (11): capture_check(), Check, collect_checks(), database_check(), interface_check(), model_check(), redis_check(), telegram_check() (+3 more)

### Community 112 - "example_pack template manifest"
Cohesion: 0.18
Nodes (11): Autonomy statement, ISO/IEC 22989 stages versus 5338 processes, Grounding corpora now live inside packs, advice module manifest, example_pack template manifest, example_room advice shape, Pack advice block, The closed list of calculators (+3 more)

### Community 113 - "paperbrain/extract.py"
Cohesion: 0.36
Nodes (9): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+1 more)

### Community 114 - "§5 · Evaluation and results"
Cohesion: 0.15
Nodes (12): 5.10 What run 3 must add, 5.1 The claim, 5.2 What was measured, 5.3 The three-run spine, 5.4 Retrieval: what the two changes bought, 5.5 Abstention: the finding, 5.6 Extraction, by document type, 5.7 The two module metrics, and the lesson in them (+4 more)

### Community 115 - "tokens/page.tsx"
Cohesion: 0.05
Nodes (34): lucide-react, react, dynamic, runtime, Motion(), ROWS, INKS, metadata (+26 more)

### Community 116 - "HouseholdScope"
Cohesion: 0.17
Nodes (11): HouseholdScope, scope_passages(), _conn_returning(), _passage(), test_a_document_naming_the_owner_and_somebody_else_is_kept(), test_a_document_with_no_subject_belongs_to_everybody(), test_a_household_with_no_owner_scopes_nothing(), test_another_persons_documents_are_set_aside() (+3 more)

### Community 117 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 118 - "_today_items"
Cohesion: 0.17
Nodes (8): Source, TodayItem, TodayResponse, _as_source(), today(), _cite(), _link(), _today_items()

### Community 119 - "phrasings.py"
Cohesion: 0.20
Nodes (4): _keys(), LaneSpec, _spec(), TypeSpec

### Community 123 - "Terms of use"
Cohesion: 0.25
Nodes (7): Clause A. Authority and Consent for Submissions on Behalf of Another Adult, Clause B. Purpose of Collection, Use and Retention, Clause C. Personal Data of Third Parties, Definitions, For review, Not yet written, Terms of use

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.17
Nodes (8): Task: benchmark the workstation and publish the numbers, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, Yew Mun's generated task list, Roadmap phase 1 - retrieval, PaperBrain hybrid retrieval (BM25 + dense, fused by RRF), Sample home contents insurance policy, Sample supermarket tax invoice

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 127 - "vault/page.tsx"
Cohesion: 0.07
Nodes (27): DocumentPage(), dynamic, metadata, runtime, dynamic, metadata, runtime, SourcePanel() (+19 more)

### Community 128 - "The case for synthetic evaluation data"
Cohesion: 0.18
Nodes (5): Register first, then generate, SYNTHETIC DOCUMENT footer, The 40-document holdout corpus, The case for synthetic evaluation data, extraction_f1

### Community 129 - "Domain pack"
Cohesion: 0.12
Nodes (16): The demonstration run sheet, Step 8 - switch a pack off, Step 6 - the abstention, Step 7 - the refusal to act, Step 2 - the source chip, people and person_aliases, Three buckets, not two, The correctly-cited wrong person (+8 more)

### Community 131 - "Filling the corpus register"
Cohesion: 0.20
Nodes (9): Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one, The rule that cannot bend (+1 more)

### Community 132 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (9): Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six, Where governance touches the code (+1 more)

### Community 133 - "Two-Stage Quarantine With a Vision Second Pass"
Cohesion: 0.15
Nodes (7): Qwen-SEA-LION-v4-4B-VL Generator, Week 1 Entry, 2-8 Sep 2026, Week 2 Entry, 9-15 Sep 2026, receive(payload, mime, sender, ts, *, original_name), Idempotent Upsert on a SHA-256 of the Source Bytes, Two-Stage Quarantine With a Vision Second Pass, Clean, Scanned and Photo Tiers

### Community 135 - "Where Things Live"
Cohesion: 0.10
Nodes (17): Working Agreement for Coding Agents, The Five Lanes and Their Owners, The Contribution Loop, Policy Schedule Template, Renewal Notice Template, ADR 0010 - main is unprotected, and the discipline is human, Graphify shared knowledge graph, Two kinds of extraction (+9 more)

### Community 136 - "Policy schedule HTML template"
Cohesion: 0.24
Nodes (8): b1-0001 Private Car Insurance Policy Schedule, b1-0002 HomeShelter Contents Policy Schedule, b1-0003 Hospital Income Protection Plan Schedule, Full-length insurance policy notebook prompt, Four full-policy notebook prompts, Shared policy-drafting preamble, Guaranteed surrender value table (b1-0031), Policy schedule HTML template

### Community 139 - "PaperBrain"
Cohesion: 0.20
Nodes (5): The code pass of the knowledge graph, Lane A - Integration and product, The semantic pass of the knowledge graph, Christian's generated task list, PaperBrain

### Community 140 - "ADR 0013: A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.16
Nodes (12): ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts, chunks.tsv built from context_prefix || text, Context prefix: title - type - heading - page, rag_probe2 before/after similarity table (six policies, 13 September), scripts/reindex.py rebuilds chunks and vectors, Chunks follow the document's structure (Docling heading labels), Task prompts: embed_query and embed_documents, ADR 0013: A question is understood before it is searched, and scoped before it is cut (+4 more)

### Community 141 - "answer.tsx"
Cohesion: 0.07
Nodes (29): ai, @ai-sdk/react, next, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST() (+21 more)

### Community 143 - "mentions"
Cohesion: 0.15
Nodes (8): _as_date(), _as_number(), _contains(), mentions(), same_value(), value_forms(), test_a_register_value_is_recognised_however_it_is_printed(), test_same_value_normalises_dates_numbers_and_text()

### Community 144 - "Settings"
Cohesion: 0.10
Nodes (36): Settings, client_for(), consent(), ConsentConn, open_obligation(), pack_row(), settings(), stored_fact() (+28 more)

### Community 145 - "schedule.py"
Cohesion: 0.21
Nodes (7): beat_schedule(), cron_expressions(), crontab_from(), manifest(), test_alert_is_swept_nightly_even_though_its_manifest_says_fact_write(), test_both_sweeps_are_scheduled_and_named_after_registered_tasks(), test_the_reminder_cron_is_read_from_its_manifest_not_written_twice()

### Community 146 - "PrivateCare Policy Wording Template"
Cohesion: 0.31
Nodes (9): PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Gemini prompt bank for identity specimens, The Lim household canon, Republic of Xinkapow (+1 more)

### Community 147 - "alert module manifest"
Cohesion: 0.28
Nodes (6): Days without recorded cover tile, alert_fpr, obligation_precision, Module manifest template, alert module manifest, reminder module manifest

### Community 148 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 150 - "app/layout.tsx"
Cohesion: 0.20
Nodes (7): next-themes, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 151 - "The Grounding Gate"
Cohesion: 0.29
Nodes (7): The Core Answering Layer, The Answer Path: route, retrieve, rerank, ground, answer or abstain, The Grounding Gate, The Score Floor the Gate Reads, Kidney Stones: Inpatient Covered, Outpatient ESWL Excluded, Ask Screen, Try to Make It Lie: the Abstention Test

### Community 152 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 153 - "ADR 0008 - Ingestion runs on a Celery worker"
Cohesion: 0.39
Nodes (7): ADR 0005 - The watched folder is polled, not subscribed to, Stability debounce with injected time, ADR 0008 - Ingestion runs on a Celery worker, The ingestion worker, START.cmd launcher, Telegram capture, The watched inbox folder

### Community 154 - "classify"
Cohesion: 0.15
Nodes (9): Classification, classify(), _schema(), test_a_document_no_pack_recognises_is_not_forced_into_one(), test_a_low_confidence_classification_is_refused(), test_a_pack_qualified_type_is_not_a_candidate(), test_an_unavailable_model_is_a_classification_failure_not_a_crash(), test_identity_documents_and_loans_are_candidates() (+1 more)

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (6): Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 157 - "build_team_tasks.py"
Cohesion: 0.25
Nodes (5): main(), _read_rows(), _render(), _week_key(), _write()

### Community 158 - "Adversarial testing from week 7"
Cohesion: 0.25
Nodes (8): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Adversarial testing from week 7, Prompt injection carried inside a document, Scope attack: asking it to act, Task: run adversarial Set C and write up the findings, Adversarial Set C (15 questions that should not be answered), Golden Set C - adversarial (15)

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 162 - "_graph_for"
Cohesion: 0.18
Nodes (7): AskResponse, Claim, _as_response(), ask(), ask_stream(), _graph_for(), _history()

### Community 163 - "Cursor"
Cohesion: 0.25
Nodes (3): Cursor, cursor(), cursor()

### Community 164 - "eslint.config.mjs"
Cohesion: 0.33
Nodes (3): @eslint/eslintrc, compat, eslintConfig

### Community 165 - "PARROT evaluation harness"
Cohesion: 0.38
Nodes (7): abstention_rate, PARROT evaluation harness, Set A, answerable, Set B, hard negatives, Set C, adversarial, The golden question sets, must_cite_page from field_pages

### Community 166 - "Any"
Cohesion: 0.22
Nodes (5): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts()

### Community 167 - "The autonomy statement"
Cohesion: 0.29
Nodes (3): IMDA mappings and autonomy statement artefact, The facts table as an extension point, Roadmap phase 2 - facts

### Community 168 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 169 - "ModuleMetrics"
Cohesion: 0.24
Nodes (5): _mark(), ModuleMetrics, render(), test_the_report_marks_both_metrics_against_their_target(), test_the_report_says_nothing_fired_rather_than_printing_a_rate()

### Community 170 - "_as_module_summary"
Cohesion: 0.20
Nodes (8): ModuleSummary, PacksResponse, PackSummary, _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack()

### Community 172 - "ADR index (0001-0018, with status)"
Cohesion: 0.09
Nodes (25): ADR 0001 - Record architecture decisions, ADR 0002 - One PostgreSQL instance for everything, Reciprocal rank fusion of dense and lexical, ADR 0003 - PaperBrain informs the pattern, not the module, PaperBrain prototype, ADR 0004 - Local setup can run before the assistant is ready, ADR 0006 - pypdfium2 renders the quarantine page images, ADR 0009 - next-themes and lucide-react are the only two web dependencies beyond the stack (+17 more)

### Community 174 - "Project skills"
Cohesion: 0.40
Nodes (4): Changing them, Project skills, Slash commands, Using them

### Community 175 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 176 - "_answer_events"
Cohesion: 0.12
Nodes (8): AdviceConsent, ErrorEvent, _answer_events(), _as_consent(), record_consent(), connection(), _settings(), _sse()

### Community 177 - "test_both_ask_endpoints_hand_the_graph_the_same_advice_ports"
Cohesion: 0.11
Nodes (8): ClosingSpy, streaming(), test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them(), spying(), test_both_ask_endpoints_hand_the_graph_the_same_advice_ports(), ask(), test_the_server_still_starts_when_the_database_is_not_running(), refuse()

### Community 179 - "The synthetic-to-real gap"
Cohesion: 0.40
Nodes (4): The 40-document redacted holdout, Consent and redaction protocol, Task: write the PDPA position on using synthetic data, Task: evaluation run 3 plus the holdout run

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 181 - "FakeConn"
Cohesion: 0.12
Nodes (3): _Connected, FakeConn, FakeCursor

### Community 182 - "answer.py"
Cohesion: 0.04
Nodes (24): AdviceShape, AdviceLog, AdviceRecord, Adviser, ConsentBook, _advice_basis(), _advice_prompt(), _closes() (+16 more)

### Community 183 - "Part A. Policy"
Cohesion: 0.18
Nodes (10): A1. Retention rules, A2. What erasure means, A3. Three ways to erase, A4. Deleting a document: only on instruction, confirmed, and complete within 72 hours, A5. Erasing a person, and resetting the workspace, Basis, Decisions for Siew, Part A. Policy (+2 more)

### Community 184 - "Scoped"
Cohesion: 0.15
Nodes (8): scope_to(), Scoped, test_a_question_about_a_parent_names_them_as_who_it_is_about_and_carries_todays_date(), apply(), test_a_question_about_a_relation_nobody_holds_is_not_answered_from_the_owners_documents(), apply(), test_a_question_naming_another_member_does_not_call_them_the_asker(), apply()

### Community 185 - "correct"
Cohesion: 0.25
Nodes (3): correct(), Corrected, UnknownFact

### Community 186 - "_page_of_examples"
Cohesion: 0.24
Nodes (5): _page_of_examples(), _reply_of_examples(), test_a_donation_receipt_stores_donation_amount_and_never_amount(), test_a_fact_is_stored_under_the_name_the_catalogue_declares(), test_each_rider_is_its_own_fact_with_its_name_and_sum_assured()

### Community 200 - "advice_consents"
Cohesion: 0.40
Nodes (6): advice_consents(), B1. The only erasure paths that exist, B2. What deleting a `documents` row cascades to, and what it leaves, B4. Does today's system meet Part A?, Part B. What the code does today, Status against the code

### Community 201 - "Alert"
Cohesion: 0.25
Nodes (3): Alert, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

### Community 204 - "package.json"
Cohesion: 0.11
Nodes (16): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+8 more)

### Community 205 - "Any"
Cohesion: 0.29
Nodes (4): resolve(), conn(), test_one_name_cannot_belong_to_two_people(), test_the_owner_is_found_by_any_of_their_names()

### Community 211 - "State"
Cohesion: 0.15
Nodes (4): _asked(), _conversation(), fuse(), State

### Community 212 - "main"
Cohesion: 0.10
Nodes (13): _kill_tree(), main(), open_browser(), parse_args(), port_answers(), stop_web(), stop_worker(), supervise() (+5 more)

### Community 213 - "contracts.py"
Cohesion: 0.12
Nodes (15): Advice, Answering, Exclusions, FieldSpec, Grounding, Guardrails, ModuleTrigger, Persona (+7 more)

### Community 215 - "paperbrain/chunk.py"
Cohesion: 0.36
Nodes (4): Chunk, chunk_pages(), clean(), _split_page()

### Community 216 - "sweep"
Cohesion: 0.36
Nodes (6): sweep(), srs_row(), test_a_firing_older_than_the_debounce_window_fires_again(), test_a_recent_firing_is_debounced(), test_a_threshold_crossing_fires_with_the_document_behind_it(), test_below_the_warning_share_nothing_fires()

### Community 218 - "_ordered"
Cohesion: 0.33
Nodes (3): _Value, _order_key(), _ordered()

### Community 219 - "IMDA frameworks: what applies to PARROT"
Cohesion: 0.33
Nodes (5): Findings from this pass, For Siew, GenAI framework: nine dimensions, IMDA frameworks: what applies to PARROT, The two instruments

### Community 221 - "printed_date"
Cohesion: 0.50
Nodes (3): printed_date(), test_a_printed_date_becomes_iso_in_code_not_in_the_model(), test_something_that_is_not_a_date_is_not_turned_into_one()

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
- **396 isolated node(s):** `The two instruments`, `Findings from this pass`, `For Siew`, `Action`, `Stage` (+391 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1730 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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