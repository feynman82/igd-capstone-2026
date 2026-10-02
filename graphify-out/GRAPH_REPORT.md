# Graph Report - igd-capstone-2026  (2026-10-02)

## Corpus Check
- 314 files · ~723,371 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 34 file(s) not represented in the graph (top: (none) 11, .jsonl 7, .csv 5)

## Summary
- 4721 nodes · 11637 edges · 204 communities (169 shown, 35 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1070 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `42641c9e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Ollama
- FakeCursor
- ScriptedOllama
- test_answer_graph.py
- test_register_validation.py
- advice/__init__.py
- Provenance register for corpus sg_protection_guidance
- test_advice_module.py
- api.ts
- FakeOllama
- test_grounding_index.py
- typing
- FolderAdapter
- test_telegram_capture.py
- FakeConn
- ._advise
- bench_runtime.py
- vault.py
- support.js
- worker.py
- ingest/extract.py
- test_grounding_values.py
- report.py
- pathlib
- State
- SentenceScanner
- household.py
- test_ingest_pipeline.py
- test_lifecycle.py
- score.py
- test_household.py
- .load
- test_pages.py
- _pages_from
- test_eval_generate.py
- logging
- test_scan_parse.py
- Any
- reminder/__init__.py
- test_api.py
- alert/__init__.py
- retrieve.py
- rows_for
- Any
- test_startup.py
- eval/modules.py
- test_gate.py
- pipeline.py
- build_router
- HouseholdScope
- compilerOptions
- packs.py
- registry.py
- datetime
- classify.py
- cli.py
- run.py
- ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic
- build.py
- index_pack
- ingest/reindex.py
- values.py
- ingest/quarantine.py
- lock.ts
- InstalledPack
- routes.py
- PARROT Interface Design Pack
- export-design-preview.cjs
- The Four Surfaces
- FakeConn
- advice-consent.tsx
- devDependencies
- test_inventory.py
- Hybrid Retrieval: Dense Plus Full-Text
- scope.py
- ADR 0011: The household is people and aliases, and the owner is one of them
- FakeConn
- test_modules.py
- Calculation
- test_eval_harness.py
- preview.tsx
- extract_values
- Two-stage quarantine with a vision-language second pass
- Any
- Ollama
- packs/page.tsx
- build_team_tasks.py
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- test_contracts.py
- components.json
- validate
- test_tax_pack.py
- contracts.py
- item-row.tsx
- test_eval_report.py
- The Lim Household, Tampines
- ADR 0007 - The graph ships before retrieval and before a checkpoint table
- Lane C - Governance and assurance
- HouseholdAdviceLog
- Core Document Catalogue (ADR 0017)
- stop_web
- phrasings.py
- The five-lane split (five people, nine weeks, three builders)
- Data inventory: identity data, DOBs and loans
- test_rerank.py
- Roadmap phase 3 - reminders
- web/ - the PARROT interface
- The document register as ground truth
- ingest.py
- Tax and Reliefs — contract changes this pack needs
- Reminder, Alert and Tracker Registers
- runtime/ollama.py
- example_pack template manifest
- paperbrain/extract.py
- §5 · Evaluation and results
- tokens/page.tsx
- Path
- Integration review
- _closes
- FakeCursor
- capture.py
- ModelUnavailable
- _as_consent
- The deliberately naive retrieval baseline
- Running the evaluation harness
- document-detail.tsx
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
- test_a_document_still_in_the_inbox_is_not_forgotten
- Settings
- schedule.py
- PrivateCare Policy Wording Template
- alert module manifest
- dependencies
- ingest/chunk.py
- app/layout.tsx
- The Grounding Gate
- Authoring a domain pack
- ADR 0008 - Ingestion runs on a Celery worker
- Passage
- DesignPreview evaluation harness
- _without_passage_numbers
- events
- Adversarial testing from week 7
- Writing an ADR
- Every Fact Row Cites Its Source
- HouseholdInventory
- Cursor
- eslint.config.mjs
- PARROT evaluation harness
- RagasJudge
- The autonomy statement
- scripts
- usable
- _as_module_summary
- Due
- ADR index (0001-0018, with status)
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- _answer_events
- test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them
- The synthetic-to-real gap
- filesystem
- quiet_engine
- startup_gaps
- test_the_batch_template_is_usable_exactly_as_generated
- test_an_unscoped_result_is_not_empty_for_the_owner
- One Database
- Lane E - Corpus and adversarial testing
- Alert
- setup.sh
- session-start.sh
- package.json
- postcss.config.mjs
- Lane C - Governance and assurance
- parrot

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
- `Explicitly not doing: cloud, hosted vectors, autonomous spending` --semantically_similar_to--> `The autonomy statement`  [INFERRED] [semantically similar]
  tools/paperbrain/docs/ROADMAP.md → team/siew/README.md
- `Task: hybrid retrieval with reciprocal rank fusion` --semantically_similar_to--> `Hybrid retrieval, not embeddings alone`  [INFERRED] [semantically similar]
  team/yew-mun/tasks.md → tools/paperbrain/docs/ARCHITECTURE.md
- `next dev binds every interface, not loopback` --semantically_similar_to--> `Ports published on 127.0.0.1 only`  [INFERRED] [semantically similar]
  docs/governance/data-inventory.md → infra/docker-compose.yml
- `One cell, one field` --semantically_similar_to--> `A field name is three things at once`  [INFERRED] [semantically similar]
  corpus/templates/policy_schedule.html → docs/PACK_AUTHORING.md
- `Domain Packs` --conceptually_related_to--> `Core Document Catalogue (ADR 0017)`  [AMBIGUOUS]
  README.md → core/documents.yaml

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

## Communities (204 total, 35 thin omitted)

### Community 0 - "Ollama"
Cohesion: 0.06
Nodes (27): Recovery, recovery_rate(), bytes_for(), digest_of_document(), index_folder(), SourceMissing, connect(), Ollama (+19 more)

### Community 1 - "FakeCursor"
Cohesion: 0.18
Nodes (8): FakeConn, FakeCursor, FakeOllama, _row(), test_a_paraphrase_keeps_every_score_where_cosine_put_it(), test_only_the_chunk_that_prints_the_number_is_lifted(), test_the_catalogue_type_reaches_the_graph(), test_the_query_is_asked_once_with_both_arms_and_the_pack_filter()

### Community 2 - "ScriptedOllama"
Cohesion: 0.06
Nodes (46): AdviceCard, AdviceWithheld, ConsentRequired, Finished, Sentence, Subject, advised_pack(), build() (+38 more)

### Community 3 - "test_answer_graph.py"
Cohesion: 0.07
Nodes (50): AnswerGraph, Declined, Refused, Holding, Scoped, test_advice_is_declined_when_the_graph_was_given_no_adviser(), build(), FakeInventory (+42 more)

### Community 4 - "test_register_validation.py"
Cohesion: 0.17
Nodes (14): test_a_batch_mixes_packs_in_one_register(), test_a_header_without_field_pages_is_caught(), test_a_row_with_no_fields_carries_no_ground_truth(), test_an_unparseable_page_is_caught(), test_duplicate_ids_are_caught(), test_expiry_before_start_is_caught(), test_field_pages_naming_a_field_the_row_does_not_fill_is_caught(), test_field_pages_records_the_page_a_value_is_printed_on() (+6 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.07
Nodes (45): Figure, Input, _ambiguous(), _amount(), _band(), _band_label(), Basis, _calculation() (+37 more)

### Community 6 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.05
Nodes (59): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, MediShield Life (CPF Board), Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022 (+51 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.14
Nodes (47): Missing, calculate(), assert_nothing_negative(), basis(), fact(), figures_of(), _gap_basis(), _held() (+39 more)

### Community 8 - "api.ts"
Cohesion: 0.05
Nodes (46): dynamic, HouseholdPage(), metadata, runtime, AppLayout(), dynamic, isUrgent(), metadata (+38 more)

### Community 9 - "FakeOllama"
Cohesion: 0.11
Nodes (23): extract(), FakeOllama, _page_of_examples(), _reply_of_examples(), test_a_date_that_cannot_be_read_still_quarantines(), test_a_donation_receipt_stores_donation_amount_and_never_amount(), test_a_fact_is_stored_under_the_name_the_catalogue_declares(), test_a_long_document_whose_front_is_enough_is_read_once() (+15 more)

### Community 10 - "test_grounding_index.py"
Cohesion: 0.11
Nodes (17): approve(), pending(), PendingValue, reject(), _block(), main(), _review_env(), test_approve_passes_only_the_ids_and_the_pending_condition() (+9 more)

### Community 11 - "typing"
Cohesion: 0.06
Nodes (29): sha256(), Dispatcher, Inline, Queued, Send, Intake, register_document(), Registration (+21 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.11
Nodes (19): FolderAdapter, FolderSettings, FolderCapture, _loop(), main(), FakeRegistrar, _settle(), test_a_file_removed_before_it_settles_is_forgotten() (+11 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.10
Nodes (24): TelegramSettings, build(), FakeRegistrar, FakeTelegram, photo_update(), test_a_chat_outside_the_allow_list_is_ignored(), test_a_conflict_names_the_webhook_rather_than_saying_nothing(), test_a_document_keeps_the_name_it_was_sent_under() (+16 more)

### Community 14 - "FakeConn"
Cohesion: 0.08
Nodes (26): document_row(), fact_row(), FakeConn, obligation(), open_obligation(), overdue_row(), test_a_citation_that_resolves_to_nothing_still_says_what_it_said(), test_a_core_document_stays_enabled_when_every_pack_is_off() (+18 more)

### Community 15 - "._advise"
Cohesion: 0.07
Nodes (13): Abstained, _advice_basis(), _advice_prompt(), answer_system(), _citations(), _distinct(), _input_citation(), _max_sentences() (+5 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (20): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+12 more)

### Community 17 - "vault.py"
Cohesion: 0.07
Nodes (15): _columns(), correct(), Corrected, CorrectionRejected, UnknownFact, _as_document(), declared_type(), document() (+7 more)

### Community 18 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 19 - "worker.py"
Cohesion: 0.18
Nodes (9): lifespan(), install_best_effort(), application(), _beat_needs_its_own_process(), celery_argv(), main(), _run(), _start_beat() (+1 more)

### Community 20 - "ingest/extract.py"
Cohesion: 0.11
Nodes (12): _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact, Extraction, _normalise(), _prepare() (+4 more)

### Community 21 - "test_grounding_values.py"
Cohesion: 0.16
Nodes (27): _dropped(), _log_values(), _run(), test_a_money_value_with_a_currency_marker_is_kept(), test_a_multiple_is_kept_in_the_forms_it_is_written(), test_a_number_is_kept_when_one_of_its_occurrences_fits_the_unit(), test_a_number_matches_its_printed_decimal_form(), test_a_number_not_in_its_passage_is_dropped() (+19 more)

### Community 22 - "report.py"
Cohesion: 0.13
Nodes (13): _cell(), collect(), main(), _overall(), _paragraph(), Provenance, render(), _row() (+5 more)

### Community 23 - "pathlib"
Cohesion: 0.08
Nodes (12): enabled_pack_ids(), enabled_packs(), DatabaseUnavailable, find_browser_executable(), generate_documents(), _ask(), main(), main() (+4 more)

### Community 24 - "State"
Cohesion: 0.12
Nodes (5): _asked(), _conversation(), fuse(), _review_asked(), State

### Community 25 - "SentenceScanner"
Cohesion: 0.09
Nodes (13): SentenceScanner, drip(), test_a_backslash_before_a_quote_is_handled(), test_a_brace_inside_a_sentence_does_not_end_it(), test_a_sentence_is_released_before_the_rest_has_been_written(), test_a_sentence_that_is_not_an_object_is_skipped_rather_than_crashing(), test_a_truncated_stream_keeps_the_sentences_that_did_arrive(), test_an_answer_with_no_sentences_yields_nothing_and_keeps_its_missing() (+5 more)

### Community 26 - "household.py"
Cohesion: 0.08
Nodes (25): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+17 more)

### Community 27 - "test_ingest_pipeline.py"
Cohesion: 0.12
Nodes (22): chunk_pages(), classification_sample(), find_page(), Block, ParsedPage, insurance(), iras(), _policy_page() (+14 more)

### Community 28 - "test_lifecycle.py"
Cohesion: 0.17
Nodes (12): Lifecycle, _client(), _eventually(), test_a_browser_cannot_reach_the_engine_directly_even_with_the_header(), test_a_request_without_the_intent_header_is_refused(), test_an_accepted_request_answers_first_and_then_asks_the_server_to_stop(), test_an_engine_nobody_supervises_says_so_instead_of_pretending(), test_an_unknown_action_is_not_found() (+4 more)

### Community 29 - "score.py"
Cohesion: 0.07
Nodes (28): _as_date(), _as_number(), cites(), _contains(), declined_in_prose(), doc_stem(), grade(), held_back() (+20 more)

### Community 30 - "test_household.py"
Cohesion: 0.08
Nodes (25): is_first_person(), relation_asked(), _household_scope(), test_a_grandparent_nobody_holds_is_an_unknown_relation_not_the_fathers_policy(), test_a_grandparent_recorded_under_that_name_is_who_the_question_means(), test_a_name_that_is_not_exactly_one_person_scopes_nothing(), test_a_named_household_member_wins_over_the_pronoun(), test_a_person_nobody_has_confirmed_is_not_named() (+17 more)

### Community 31 - ".load"
Cohesion: 0.05
Nodes (45): create_app(), checks(), ready(), setup(), system_status(), ModelWarmth, warm_models(), _chat_ids() (+37 more)

### Community 32 - "test_pages.py"
Cohesion: 0.08
Nodes (20): page_images(), page_count(), PageUnavailable, _pdfium(), render_page(), RendererUnavailable, _size(), test_a_damaged_pdf_is_a_sentence_not_a_traceback() (+12 more)

### Community 33 - "_pages_from"
Cohesion: 0.16
Nodes (10): DoclingParser, _kind(), _pages_from(), _table_text(), _cell(), _on_page(), test_a_table_is_kept_as_label_and_value_lines_in_reading_order(), test_a_wider_table_keeps_every_column_and_a_spanned_cell_once() (+2 more)

### Community 34 - "test_eval_generate.py"
Cohesion: 0.08
Nodes (23): _ambiguous(), choose(), Generated, hand_written(), main(), on_file(), pool(), write_lane() (+15 more)

### Community 35 - "logging"
Cohesion: 0.06
Nodes (11): CaptureAdapter, IngestJob, sniff_mime(), _Pending, _Registered, _attachment(), _pixels(), _status_reason() (+3 more)

### Community 36 - "test_scan_parse.py"
Cohesion: 0.14
Nodes (6): _as_printed(), page_pixels(), photographed(), _register_row(), scanned(), test_a_scan_keeps_the_schedule_table_and_its_page()

### Community 37 - "Any"
Cohesion: 0.14
Nodes (10): by_subject(), db(), FakeCursor, load_register(), test_a_deductible_receipt_counts_in_its_own_year_only(), test_a_lapsed_policy_is_not_masked_by_another_that_still_runs(), test_cpf_is_this_years_payslips_per_employee(), test_donations_are_this_years_deductible_receipts_per_donor() (+2 more)

### Community 38 - "reminder/__init__.py"
Cohesion: 0.11
Nodes (8): already_said(), current_lead(), next_window(), Overdue, snooze(), UnknownObligation, test_never_notified_is_never_said(), test_the_tightest_entered_window_is_the_current_one()

### Community 39 - "test_api.py"
Cohesion: 0.09
Nodes (25): advising(), client(), conn(), FakeGraph, graph(), _padded(), streaming(), test_a_client_that_leaves_after_the_card_commits_one_record() (+17 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.18
Nodes (11): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), srs_contributions_ytd(), sweep() (+3 more)

### Community 41 - "retrieve.py"
Cohesion: 0.14
Nodes (12): Connection, load_matrix(), pack(), stats(), unpack(), embed_chunks(), _fts_query(), fuse() (+4 more)

### Community 42 - "rows_for"
Cohesion: 0.10
Nodes (25): Citation, Reading, a_citation(), advice_card(), rows_for(), rule_citation(), sse(), StreamingGraph (+17 more)

### Community 43 - "Any"
Cohesion: 0.10
Nodes (17): advised_pack(), db(), _document(), _facts_tuple(), FakeConn, FakeCursor, _source(), _sum_insured() (+9 more)

### Community 44 - "test_startup.py"
Cohesion: 0.15
Nodes (12): start_web(), main(), report_hardware(), prepare_checkout(), test_check_only_never_launches_even_when_ready(), test_incomplete_checkout_never_launches_a_process(), test_launch_preserves_paths_and_loopback_and_exit_code(), test_screens_are_not_started_twice_when_something_already_holds_the_port() (+4 more)

### Community 45 - "eval/modules.py"
Cohesion: 0.05
Nodes (41): alert_fpr(), AlertVerdict, _day(), main(), _mark(), measure(), Measured, ModuleMetrics (+33 more)

### Community 46 - "test_gate.py"
Cohesion: 0.07
Nodes (42): _kind_of(), passages_for(), check(), check_advice(), check_content(), check_one(), Claim, _says() (+34 more)

### Community 47 - "pipeline.py"
Cohesion: 0.07
Nodes (16): Chunk, fixed(), from_facts(), _label(), parse(), ParsedDocument, Parser, PlainTextParser (+8 more)

### Community 48 - "build_router"
Cohesion: 0.08
Nodes (28): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, RetryAccepted, _as_person(), _as_vault_document() (+20 more)

### Community 49 - "HouseholdScope"
Cohesion: 0.14
Nodes (12): HouseholdScope, scope_passages(), scope_to(), _conn_returning(), _passage(), test_a_document_naming_the_owner_and_somebody_else_is_kept(), test_a_document_with_no_subject_belongs_to_everybody(), test_a_household_with_no_owner_scopes_nothing() (+4 more)

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 51 - "packs.py"
Cohesion: 0.11
Nodes (22): Categories, Asked, categories_asked(), categorise(), glossary(), _make_replacer(), mentions(), _pattern() (+14 more)

### Community 52 - "registry.py"
Cohesion: 0.07
Nodes (25): ModuleManifest, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, installed_packs(), _load_one(), enabled_module_ids() (+17 more)

### Community 53 - "datetime"
Cohesion: 0.15
Nodes (12): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), _document(), _installed(), test_a_missing_recorded_file_is_refused(), test_a_pack_with_no_corpus_gives_none_and_empty() (+4 more)

### Community 54 - "classify.py"
Cohesion: 0.11
Nodes (14): DocumentTypeSpec, Classification, classify(), _prompt(), _schema(), Catalog, document_types(), PackUnavailable (+6 more)

### Community 55 - "cli.py"
Cohesion: 0.18
Nodes (14): build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest(), cmd_init() (+6 more)

### Community 56 - "run.py"
Cohesion: 0.12
Nodes (18): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), _indexed(), main() (+10 more)

### Community 57 - "ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.15
Nodes (17): Code-written absence sentence: 'None of the N policies on file is a dental plan.', ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic, The advise route intent returns the pack's advice_decline, answering.categories: ordered whole-word rules over one printed field, Category filter applied before the keep-6 cut, answering.exclusions: headings under which a cover claim is not believed, Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration) (+9 more)

### Community 58 - "build.py"
Cohesion: 0.09
Nodes (13): DocumentCatalog, _class_name(), _docstring(), _field_line(), _header(), load(), load_catalog(), main() (+5 more)

### Community 59 - "index_pack"
Cohesion: 0.14
Nodes (18): GroundingDocument, SourceText, index_pack(), IndexReport, _upsert_source(), _extracted(), _installed(), _script_env() (+10 more)

### Community 60 - "ingest/reindex.py"
Cohesion: 0.10
Nodes (8): document_title(), indexed(), IndexedDocument, reindex_document(), ReindexFailed, _Value, test_a_document_is_titled_by_the_string_fields_its_pack_declares(), test_reindexing_replaces_chunks_and_leaves_facts_alone()

### Community 61 - "values.py"
Cohesion: 0.07
Nodes (24): ValueKey, _check(), collapse(), _cuts_a_number(), ExtractedValue, _groups(), _is_heading(), number_tokens() (+16 more)

### Community 62 - "ingest/quarantine.py"
Cohesion: 0.18
Nodes (8): blocked_reasons(), forget(), QuarantinedDocument, queue(), retry(), _still_quarantined(), StillInInbox, transcribe()

### Community 63 - "lock.ts"
Cohesion: 0.07
Nodes (45): dynamic, GET(), grant(), POST(), runtime, ALLOWED, Context, DELETE() (+37 more)

### Community 64 - "InstalledPack"
Cohesion: 0.15
Nodes (11): AdviceShape, InstalledPack, _fact(), fact_row(), facts_for(), _is_an_adviser(), ModuleAdviser, names_for() (+3 more)

### Community 65 - "routes.py"
Cohesion: 0.09
Nodes (36): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, AskRequest, Claim, CloseRequest, ConfirmNameRequest (+28 more)

### Community 66 - "PARROT Interface Design Pack"
Cohesion: 0.09
Nodes (21): Citation chips are the trust surface, Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Suggestions come from this week's ingest, Civic Register: order, clarity and institutional confidence, Kitchen Table: a little less household admin, a little more breathing room, The Reading Desk: understand it, open the source, see for yourself (+13 more)

### Community 67 - "export-design-preview.cjs"
Cohesion: 0.10
Nodes (17): bundle(), classes, css, cssFile, domId, fs, ids, licences (+9 more)

### Community 68 - "The Four Surfaces"
Cohesion: 0.13
Nodes (14): The FastAPI Application, The API Surface, apply, Auto-Redirect to Today Once Ready, check, draw, Five Readiness Rows in Plain Words, poll (+6 more)

### Community 69 - "FakeConn"
Cohesion: 0.12
Nodes (3): _Connected, FakeConn, FakeCursor

### Community 70 - "advice-consent.tsx"
Cohesion: 0.24
Nodes (13): ConsentPrompt(), agree(), settle(), AdviceConsentSection(), fetchConsents(), withdraw(), Load, STATUS (+5 more)

### Community 71 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 72 - "test_inventory.py"
Cohesion: 0.12
Nodes (7): _Answering, holdings(), row(), test_a_pack_that_declares_no_categories_holds_nothing(), test_a_policy_on_file_is_named_categorised_and_cited_to_the_page_its_name_is_on(), test_a_renewal_notice_is_not_counted_as_a_policy_on_file(), test_the_inventory_always_reads_core_documents()

### Community 73 - "Hybrid Retrieval: Dense Plus Full-Text"
Cohesion: 0.18
Nodes (5): bge-reranker-v2-m3 Cross-Encoder, 40 Down to 6, Hybrid Retrieval: Dense Plus Full-Text, Reciprocal Rank Fusion, k=60, The Household's Eleven Policies, The Validator Is the Handover Gate

### Community 74 - "scope.py"
Cohesion: 0.22
Nodes (8): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Person

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.17
Nodes (11): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), Telegram chat_id maps to a person, Possessive relations scope the question, before the cut to six, Naming exactly one person scopes to them (whole name, or a 3+ letter possessive unique to them) (+3 more)

### Community 76 - "FakeConn"
Cohesion: 0.07
Nodes (21): current(), grant(), HouseholdConsents, _latest(), NoOwner, _record(), status(), withdraw() (+13 more)

### Community 77 - "test_modules.py"
Cohesion: 0.15
Nodes (20): sweep(), FakeConn, obligation_row(), srs_row(), test_a_dry_run_records_nothing(), test_a_firing_older_than_the_debounce_window_fires_again(), test_a_metric_no_query_defines_cannot_fire(), test_a_recent_firing_is_debounced() (+12 more)

### Community 78 - "Calculation"
Cohesion: 0.13
Nodes (7): Calculation, Adviser, _dual_cited_calculation(), _meets_calculation(), _shared_value_calculation(), test_srs_room_is_the_cap_less_this_years_contributions(), test_the_srs_saving_is_an_estimate_at_the_band_the_assessed_income_falls_in()

### Community 79 - "test_eval_harness.py"
Cohesion: 0.07
Nodes (31): Answer, _as_sentence(), Cited, Asks, Trace, trace_all(), reference_for(), Expected (+23 more)

### Community 80 - "preview.tsx"
Cohesion: 0.10
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 81 - "extract_values"
Cohesion: 0.18
Nodes (12): extract_values(), _long_text(), _reply(), ScriptedClient, _source(), test_a_json_reply_with_no_usable_values_is_no_values_for_that_section_only(), test_a_long_text_is_sent_in_more_than_one_call(), test_a_model_that_is_down_raises() (+4 more)

### Community 82 - "Two-stage quarantine with a vision-language second pass"
Cohesion: 0.12
Nodes (11): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Two-stage quarantine with a vision-language second pass, Batch 4: the deliberately hard documents, Task: review every quarantined document and label the failure, Task: sign off the capture-to-database path against the data inventory, PaperBrain handled failure modes, The pb command line (+3 more)

### Community 83 - "Any"
Cohesion: 0.11
Nodes (3): ConsentCursor, Fails, FakeCursor

### Community 84 - "Ollama"
Cohesion: 0.17
Nodes (5): answer(), build_context(), format_sources(), Ollama, Hit

### Community 85 - "packs/page.tsx"
Cohesion: 0.06
Nodes (29): ADR-0017, next, dynamic, metadata, PacksPage(), runtime, DocumentPage(), dynamic (+21 more)

### Community 86 - "build_team_tasks.py"
Cohesion: 0.33
Nodes (5): main(), _read_rows(), _render(), _week_key(), _write()

### Community 87 - "ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.16
Nodes (18): ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel), Advice graph flow: shape match, subject resolution, consent, AdviceCard, explain, advice_records keeps each answer's full basis, PackManifest.advice shapes (gap, remaining_room, keep_or_surrender, compare_own, compare_market, estimate_saving), Advice.review: one question runs every shape at once, A grounding corpus lives at packs/<pack>/grounding/<corpus_id>/ (+10 more)

### Community 88 - "test_contracts.py"
Cohesion: 0.07
Nodes (44): PackManifest, _advised(), _checked(), _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape() (+36 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "validate"
Cohesion: 0.18
Nodes (9): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), validate(), _wide_format() (+1 more)

### Community 91 - "test_tax_pack.py"
Cohesion: 0.20
Nodes (9): _basis(), _latest(), _matched(), _published(), _register(), _shape(), test_a_tax_question_reaches_the_tax_shape_and_insurance_keeps_its_own(), test_no_saving_is_estimated_without_a_notice_of_assessment() (+1 more)

### Community 92 - "contracts.py"
Cohesion: 0.11
Nodes (17): Advice, AlertConfig, Answering, Category, Exclusions, FactInput, FieldSpec, Grounding (+9 more)

### Community 93 - "item-row.tsx"
Cohesion: 0.16
Nodes (13): SourceChip(), stripTrailingPage(), ADR-0016, countdown(), detail(), figure(), ItemRow(), longDate() (+5 more)

### Community 94 - "test_eval_report.py"
Cohesion: 0.13
Nodes (18): extraction_by_type(), extraction_f1(), FactRow, _outcomes(), _totals(), test_extraction_f1_scores_only_indexed_documents_against_the_register(), _rendered(), _scores() (+10 more)

### Community 95 - "The Lim Household, Tampines"
Cohesion: 0.15
Nodes (10): loan_agreement Document Type, payslip Document Type, The Lim Household, Tampines, Household Canon Template, Rule of 78 Rebate and the 20 Per Cent Early Settlement Penalty, Motor Vehicle Hire Purchase Agreement Template, Republic of Xinkapow, the Invented Jurisdiction, Residential Housing Loan Facility Letter Template (+2 more)

### Community 96 - "ADR 0007 - The graph ships before retrieval and before a checkpoint table"
Cohesion: 0.22
Nodes (7): ADR 0007 - The graph ships before retrieval and before a checkpoint table, .graphifyignore excludes the corpus, The redacted real-document holdout, Dense-only retrieval stopgap, Hardware qualification, Rebuilding the vault's vectors, Lane B - Retrieval and evaluation

### Community 97 - "Lane C - Governance and assurance"
Cohesion: 0.13
Nodes (9): Data inventory and flow map, ISO/IEC 22989 to 5338 stage-to-process map, Lane C - Governance and assurance, Model card, Retention and erasure policy, Siew's generated task list, Golden Set B - hard negatives (25), The nine metrics and their targets (+1 more)

### Community 98 - "HouseholdAdviceLog"
Cohesion: 0.21
Nodes (4): HouseholdAdviceLog, AdviceRecord, test_record_insert_includes_the_sha256_of_the_disclaimer(), Log

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.10
Nodes (11): Generated Files Committed Alongside Their Source, benefit_illustration Document Type, birth_certificate Document Type, claim_letter Document Type, cpf_statement Document Type, Core Document Catalogue (ADR 0017), donation_receipt Document Type, identity_card Document Type (+3 more)

### Community 100 - "stop_web"
Cohesion: 0.18
Nodes (7): _kill_tree(), stop_web(), stop_worker(), test_a_worker_that_has_already_stopped_is_left_alone(), test_stopping_screens_that_were_never_started_does_nothing(), test_stopping_the_screens_kills_the_tree_not_the_wrapper(), test_stopping_the_worker_kills_the_tree_not_the_launcher()

### Community 101 - "phrasings.py"
Cohesion: 0.20
Nodes (4): _keys(), LaneSpec, _spec(), TypeSpec

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
Cohesion: 0.20
Nodes (10): Chunk, chunk_pages(), clean(), _split_page(), discover(), guess_date(), guess_type(), ingest_file() (+2 more)

### Community 109 - "Tax and Reliefs — contract changes this pack needs"
Cohesion: 0.40
Nodes (4): 1. A deduction multiplier on `estimate_saving`, 2. Limiting a fact input to one year, Not a contract change: parent relief, Tax and Reliefs — contract changes this pack needs

### Community 110 - "Reminder, Alert and Tracker Registers"
Cohesion: 0.18
Nodes (12): filing_deadline Reminder, passport Document Type, passport_expiry Reminder, policy_expiry Reminder, policy_schedule Document Type, Reminder, Alert and Tracker Registers, renewal_notice Document Type, srs_contribution_cutoff Reminder (+4 more)

### Community 111 - "runtime/ollama.py"
Cohesion: 0.08
Nodes (11): render(), capture_check(), Check, collect_checks(), database_check(), interface_check(), model_check(), redis_check() (+3 more)

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

### Community 116 - "Path"
Cohesion: 0.26
Nodes (7): _launcher(), Screens, _supervise(), test_a_start_that_fails_is_not_retried(), test_no_web_means_the_supervisor_starts_no_screens(), test_the_supervisor_relaunches_on_restart_and_keeps_the_screens_up(), test_the_supervisor_still_refuses_a_lan_bind_before_starting_anything()

### Community 117 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 118 - "_closes"
Cohesion: 0.21
Nodes (8): _closes(), _either(), _shape(), test_a_gap_closed_by_two_kinds_names_the_one_held_and_the_one_not(), test_a_gap_in_cover_already_held_asks_for_more_of_it_not_for_a_first_policy(), test_a_gap_with_nothing_on_file_says_none_is_on_file(), test_a_shape_that_names_no_cover_adds_no_sentence(), test_an_is_written_only_before_a_e_i_or_o()

### Community 121 - "capture.py"
Cohesion: 0.09
Nodes (7): TelegramUnavailable, attribution(), broker_available(), dispatcher_for(), TelegramCapture, _loop(), main()

### Community 122 - "ModelUnavailable"
Cohesion: 0.13
Nodes (7): Generated, ModelUnavailable, test_a_model_that_dies_before_any_sentence_abstains(), constrained_stream(), constrained_stream(), extract(), down()

### Community 123 - "_as_consent"
Cohesion: 0.12
Nodes (12): AdviceConsent, _as_consent(), advice_consents(), record_consent(), Clause A. Authority and Consent for Submissions on Behalf of Another Adult, Clause B. Purpose of Collection, Use and Retention, Clause C. Personal Data of Third Parties, Definitions (+4 more)

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.17
Nodes (8): Task: benchmark the workstation and publish the numbers, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, Yew Mun's generated task list, Roadmap phase 1 - retrieval, PaperBrain hybrid retrieval (BM25 + dense, fused by RRF), Sample home contents insurance policy, Sample supermarket tax invoice

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 127 - "document-detail.tsx"
Cohesion: 0.24
Nodes (9): SourcePanel(), DocumentDetail(), when(), Field(), format(), isNumeric(), CorrectionResponse, pageImage() (+1 more)

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
Cohesion: 0.06
Nodes (41): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+33 more)

### Community 143 - "test_a_document_still_in_the_inbox_is_not_forgotten"
Cohesion: 0.18
Nodes (7): filed_document(), inbox(), test_a_document_still_in_the_inbox_is_not_forgotten(), test_a_document_whose_file_left_the_inbox_is_409_not_500(), test_a_page_comes_back_as_an_image(), test_a_page_that_does_not_exist_is_a_404_that_says_so(), test_quarantine_says_what_needs_eyes_and_why()

### Community 144 - "Settings"
Cohesion: 0.11
Nodes (36): Settings, client_for(), consent(), ConsentConn, pack_row(), settings(), stored_fact(), test_a_core_reminder_still_reaches_today_when_its_old_pack_is_off() (+28 more)

### Community 145 - "schedule.py"
Cohesion: 0.16
Nodes (8): build(), beat_schedule(), cron_expressions(), crontab_from(), manifest(), test_alert_is_swept_nightly_even_though_its_manifest_says_fact_write(), test_both_sweeps_are_scheduled_and_named_after_registered_tasks(), test_the_reminder_cron_is_read_from_its_manifest_not_written_twice()

### Community 146 - "PrivateCare Policy Wording Template"
Cohesion: 0.31
Nodes (9): PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Gemini prompt bank for identity specimens, The Lim household canon, Republic of Xinkapow (+1 more)

### Community 147 - "alert module manifest"
Cohesion: 0.28
Nodes (6): Days without recorded cover tile, alert_fpr, obligation_precision, Module manifest template, alert module manifest, reminder module manifest

### Community 148 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 149 - "ingest/chunk.py"
Cohesion: 0.27
Nodes (4): _clean(), _lines(), _page_chunks(), _pieces()

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

### Community 154 - "Passage"
Cohesion: 0.04
Nodes (26): AdviceLog, Adviser, ConsentBook, DenseRetriever, NoReranker, _normal(), precheck(), states_a_printed_value() (+18 more)

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (6): Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "_without_passage_numbers"
Cohesion: 0.33
Nodes (4): _without_one_round_of_passage_numbers(), _without_passage_numbers(), test_a_passage_number_outside_the_evidence_is_ignored(), test_a_printed_figure_in_brackets_is_not_taken_for_a_passage_number()

### Community 157 - "events"
Cohesion: 0.09
Nodes (9): _pack_for(), events(), test_a_model_that_dies_mid_answer_keeps_what_it_already_proved(), test_a_sentence_that_is_only_a_citation_is_not_an_answer(), test_a_sentence_the_gate_drops_is_never_yielded_at_all(), test_a_type_no_pack_speaks_for_is_governed_by_the_core(), test_every_sentence_arrives_with_its_citations_already_on_it(), test_the_floor_that_is_applied_belongs_to_the_passage_that_has_to_clear_it() (+1 more)

### Community 158 - "Adversarial testing from week 7"
Cohesion: 0.25
Nodes (8): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Adversarial testing from week 7, Prompt injection carried inside a document, Scope attack: asking it to act, Task: run adversarial Set C and write up the findings, Adversarial Set C (15 questions that should not be answered), Golden Set C - adversarial (15)

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 162 - "HouseholdInventory"
Cohesion: 0.15
Nodes (7): AskResponse, _as_response(), ask(), ask_stream(), _graph_for(), _history(), HouseholdInventory

### Community 163 - "Cursor"
Cohesion: 0.25
Nodes (3): Cursor, cursor(), cursor()

### Community 164 - "eslint.config.mjs"
Cohesion: 0.33
Nodes (3): @eslint/eslintrc, compat, eslintConfig

### Community 165 - "PARROT evaluation harness"
Cohesion: 0.38
Nodes (7): abstention_rate, PARROT evaluation harness, Set A, answerable, Set B, hard negatives, Set C, adversarial, The golden question sets, must_cite_page from field_pages

### Community 166 - "RagasJudge"
Cohesion: 0.32
Nodes (5): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts()

### Community 167 - "The autonomy statement"
Cohesion: 0.29
Nodes (3): IMDA mappings and autonomy statement artefact, The facts table as an extension point, Roadmap phase 2 - facts

### Community 168 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 170 - "_as_module_summary"
Cohesion: 0.29
Nodes (5): _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack()

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
Cohesion: 0.11
Nodes (10): Source, _answer_events(), _as_source(), today(), _cite(), connection(), _link(), _settings() (+2 more)

### Community 177 - "test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them"
Cohesion: 0.22
Nodes (3): ClosingSpy, test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them(), spying()

### Community 179 - "The synthetic-to-real gap"
Cohesion: 0.40
Nodes (4): The 40-document redacted holdout, Consent and redaction protocol, Task: write the PDPA position on using synthetic data, Task: evaluation run 3 plus the holdout run

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 201 - "Alert"
Cohesion: 0.25
Nodes (3): Alert, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

### Community 204 - "package.json"
Cohesion: 0.11
Nodes (16): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+8 more)

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
- **385 isolated node(s):** `Definitions`, `Clause A. Authority and Consent for Submissions on Behalf of Another Adult`, `Clause B. Purpose of Collection, Use and Retention`, `Clause C. Personal Data of Third Parties`, `Not yet written` (+380 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1717 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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