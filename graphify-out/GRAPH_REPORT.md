# Graph Report - igd-capstone-2026  (2026-10-04)

## Corpus Check
- 317 files · ~728,876 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 34 file(s) not represented in the graph (top: (none) 11, .jsonl 7, .csv 5)

## Summary
- 4753 nodes · 11684 edges · 237 communities (189 shown, 48 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1088 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b8c821af`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Ollama
- test_hybrid.py
- ScriptedOllama
- test_answer_graph.py
- validate
- advice/__init__.py
- Provenance register for corpus sg_protection_guidance
- test_advice_module.py
- today/page.tsx
- extract
- main
- test_worker_queue.py
- FolderAdapter
- TelegramAdapter
- date
- ._advise
- bench_runtime.py
- vault.py
- support.js
- values.py
- test_ingest_pipeline.py
- sha256
- report.py
- .load
- _page_chunks
- SentenceScanner
- household.py
- _coerce
- test_lifecycle.py
- score.py
- _household_scope
- test_runtime.py
- test_pages.py
- _pages_from
- test_eval_generate.py
- FakeConn
- ModuleManifest
- Any
- reminder/__init__.py
- test_api.py
- alert/__init__.py
- retrieve.py
- sse
- Any
- test_startup.py
- _obligation
- test_gate.py
- typing
- build_router
- scope.py
- compilerOptions
- pack
- packs.py
- test_grounding.py
- run.py
- cli.py
- main
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
- api.ts
- advice-consent.tsx
- devDependencies
- extract_values
- Hybrid Retrieval: Dense Plus Full-Text
- worker.py
- ADR 0011: The household is people and aliases, and the owner is one of them
- FakeConn
- test_modules.py
- test_tax_pack.py
- test_eval_harness.py
- preview.tsx
- test_scan_parse.py
- Two-stage quarantine with a vision-language second pass
- Any
- Ollama
- InstalledPack
- test_contracts.py
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- Answer
- components.json
- test_eval_modules.py
- HouseholdAdviceLog
- build
- item-row.tsx
- test_eval_report.py
- The Lim Household, Tampines
- ADR 0007 - The graph ships before retrieval and before a checkpoint table
- Lane C - Governance and assurance
- eval/modules.py
- Core Document Catalogue (ADR 0017)
- Registration
- Fact
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
- test_household.py
- Integration review
- _answer_events
- test_advice_core.py
- pathlib
- ModelUnavailable
- Terms of use
- The deliberately naive retrieval baseline
- Running the evaluation harness
- packs/page.tsx
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
- same_value
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
- FakeOllama
- DesignPreview evaluation harness
- IngestJob
- collections_abc
- Adversarial testing from week 7
- Writing an ADR
- Every Fact Row Cites Its Source
- HouseholdInventory
- Registrar
- eslint.config.mjs
- PARROT evaluation harness
- RagasJudge
- The autonomy statement
- scripts
- ModuleMetrics
- _as_module_summary
- Due
- ADR index (0001-0018, with status)
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- _as_consent
- test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them
- The synthetic-to-real gap
- filesystem
- FakeCursor
- Passage
- Part A. Policy
- Scoped
- correct
- _page_of_examples
- One Database
- _columns
- gate.py
- _closes
- Lane E - Corpus and adversarial testing
- advice_consents
- Alert
- setup.sh
- session-start.sh
- package.json
- rerank.py
- postcss.config.mjs
- Lane C - Governance and assurance
- parrot
- State
- FakeCursor
- contracts.py
- FakeCursor
- is_first_person
- test_a_client_that_leaves_after_the_card_commits_one_record
- test_reindexing_replaces_chunks_and_leaves_facts_alone
- scripts/reindex.py
- IMDA frameworks: what applies to PARROT
- quiet_engine
- [...path]/route.ts
- check
- resolve_names
- score_obligations
- .embed
- Incident and data breach procedure
- main
- PackUnavailable
- app.py
- test_a_grounding_corpus_travels_inside_its_pack
- Verdict
- _input_citation
- test_generated_files_are_in_sync
- _meets_calculation
- _shared_value_calculation
- test_the_catalogue_declares_metrics_that_exist

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
- `Containment, by kind` --references--> `_chat_ids()`  [INFERRED]
  docs/governance/incident-and-breach-procedure.md → core/runtime/settings.py
- `Agentic AI framework: four dimensions` --references--> `Guardrails`  [INFERRED]
  docs/governance/imda-what-applies.md → core/contracts.py
- `Agentic AI framework: four dimensions` --references--> `check_one()`  [INFERRED]
  docs/governance/imda-what-applies.md → core/graph/gate.py
- `Agentic AI framework: four dimensions` --references--> `local_url()`  [INFERRED]
  docs/governance/imda-what-applies.md → core/runtime/settings.py

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

## Communities (237 total, 48 thin omitted)

### Community 0 - "Ollama"
Cohesion: 0.07
Nodes (32): blocked_reasons(), forget(), QuarantinedDocument, queue(), Recovery, recovery_rate(), retry(), _still_quarantined() (+24 more)

### Community 1 - "test_hybrid.py"
Cohesion: 0.09
Nodes (15): hybrid_score(), identifiers(), prints(), FakeConn, FakeCursor, FakeOllama, _row(), test_a_chunk_prints_an_identifier_however_it_is_spaced() (+7 more)

### Community 2 - "ScriptedOllama"
Cohesion: 0.07
Nodes (40): AdviceCard, AdviceWithheld, ConsentRequired, Finished, Subject, advised_pack(), build(), Consents (+32 more)

### Community 3 - "test_answer_graph.py"
Cohesion: 0.11
Nodes (37): AnswerGraph, Declined, Sentence, test_advice_is_declined_when_the_graph_was_given_no_adviser(), events(), FakeInventory, FixedRetriever, holding() (+29 more)

### Community 4 - "validate"
Cohesion: 0.09
Nodes (24): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), validate(), _wide_format() (+16 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.08
Nodes (43): Figure, Input, _ambiguous(), _amount(), _band(), _band_label(), Basis, _calculation() (+35 more)

### Community 6 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.05
Nodes (59): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, MediShield Life (CPF Board), Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022 (+51 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.13
Nodes (47): calculate(), assert_nothing_negative(), basis(), fact(), figures_of(), _gap_basis(), _held(), _held_ward() (+39 more)

### Community 8 - "today/page.tsx"
Cohesion: 0.08
Nodes (24): dynamic, HouseholdPage(), metadata, runtime, AppLayout(), dynamic, isUrgent(), metadata (+16 more)

### Community 9 - "extract"
Cohesion: 0.17
Nodes (18): extract(), insurance(), iras(), test_a_date_that_cannot_be_read_still_quarantines(), test_a_long_document_whose_front_is_enough_is_read_once(), test_a_long_document_whose_front_is_not_enough_is_read_in_full(), test_a_model_that_does_not_answer_is_not_asked_a_longer_question(), test_a_null_shaped_string_in_a_required_field_is_still_a_failure() (+10 more)

### Community 10 - "main"
Cohesion: 0.12
Nodes (14): approve(), pending(), PendingValue, reject(), _block(), main(), test_approve_passes_only_the_ids_and_the_pending_condition(), test_list_block_shows_id_pack_key_value_source_and_an_indented_passage() (+6 more)

### Community 11 - "test_worker_queue.py"
Cohesion: 0.12
Nodes (15): Queued, FakeConnection, RecordingSend, registration(), test_an_already_indexed_document_is_not_queued_again(), test_handing_over_is_fast_enough_that_the_watcher_never_stalls(), test_ingest_says_so_rather_than_failing_when_the_file_is_gone(), test_inline_keeps_a_failed_parse_from_killing_the_watcher() (+7 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.17
Nodes (16): sniff_mime(), FolderAdapter, FakeRegistrar, _settle(), test_a_file_removed_before_it_settles_is_forgotten(), test_a_file_still_being_written_is_not_registered(), test_a_file_too_large_for_a_household_document_is_skipped(), test_a_registered_file_is_not_registered_again_on_every_poll() (+8 more)

### Community 13 - "TelegramAdapter"
Cohesion: 0.11
Nodes (7): _attachment(), _pixels(), _status_reason(), TelegramAdapter, TelegramUnavailable, _write_local_copy(), B3. Things erasure has to reach beyond the database

### Community 14 - "date"
Cohesion: 0.18
Nodes (11): document_row(), fact_row(), overdue_row(), test_a_citation_that_resolves_to_nothing_still_says_what_it_said(), test_a_core_document_stays_enabled_when_every_pack_is_off(), test_an_alerts_citation_carries_the_document_it_opens(), test_one_document_is_shown_even_when_its_pack_is_off(), test_overdue_is_filtered_by_the_same_set() (+3 more)

### Community 15 - "._advise"
Cohesion: 0.07
Nodes (13): Abstained, _advice_basis(), answer_system(), _as_sentence(), _distinct(), _max_sentences(), _pack_for(), Refused (+5 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (20): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+12 more)

### Community 17 - "vault.py"
Cohesion: 0.26
Nodes (7): _as_document(), declared_type(), document(), documents(), _facts_for(), VaultDocument, VaultPage

### Community 18 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 19 - "values.py"
Cohesion: 0.07
Nodes (22): _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), number_tokens(), _pack(), parse_value() (+14 more)

### Community 20 - "test_ingest_pipeline.py"
Cohesion: 0.11
Nodes (23): chunk_pages(), classification_sample(), _date_renderings(), find_page(), _normalise(), _read(), Block, ParsedPage (+15 more)

### Community 21 - "sha256"
Cohesion: 0.13
Nodes (10): CaptureAdapter, sha256(), register_document(), conn(), database_url(), test_a_document_must_arrive_with_a_name(), test_a_new_document_is_inserted(), test_an_empty_payload_is_refused() (+2 more)

### Community 22 - "report.py"
Cohesion: 0.12
Nodes (14): _cell(), collect(), main(), _overall(), _paragraph(), Provenance, render(), _row() (+6 more)

### Community 23 - ".load"
Cohesion: 0.07
Nodes (19): warm_models(), _chat_ids(), ConfigurationError, _flag(), _folder(), local_url(), _port(), _positive() (+11 more)

### Community 24 - "_page_chunks"
Cohesion: 0.25
Nodes (4): _clean(), _lines(), _page_chunks(), _pieces()

### Community 25 - "SentenceScanner"
Cohesion: 0.10
Nodes (13): SentenceScanner, drip(), test_a_backslash_before_a_quote_is_handled(), test_a_brace_inside_a_sentence_does_not_end_it(), test_a_sentence_is_released_before_the_rest_has_been_written(), test_a_sentence_that_is_not_an_object_is_skipped_rather_than_crashing(), test_a_truncated_stream_keeps_the_sentences_that_did_arrive(), test_an_answer_with_no_sentences_yields_nothing_and_keeps_its_missing() (+5 more)

### Community 26 - "household.py"
Cohesion: 0.09
Nodes (21): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+13 more)

### Community 27 - "_coerce"
Cohesion: 0.15
Nodes (8): _coerce(), decode_schema(), _drop_format(), _prepare(), printed_date(), test_a_null_shaped_string_is_an_absent_field_not_a_bad_number(), test_a_printed_date_becomes_iso_in_code_not_in_the_model(), test_something_that_is_not_a_date_is_not_turned_into_one()

### Community 28 - "test_lifecycle.py"
Cohesion: 0.14
Nodes (19): Lifecycle, _client(), _eventually(), _launcher(), Screens, _supervise(), test_a_browser_cannot_reach_the_engine_directly_even_with_the_header(), test_a_request_without_the_intent_header_is_refused() (+11 more)

### Community 29 - "score.py"
Cohesion: 0.08
Nodes (26): Trace, cites(), _contains(), declined_in_prose(), doc_stem(), grade(), held_back(), inventory_only() (+18 more)

### Community 30 - "_household_scope"
Cohesion: 0.09
Nodes (19): _household_scope(), test_a_grandparent_nobody_holds_is_an_unknown_relation_not_the_fathers_policy(), test_a_grandparent_recorded_under_that_name_is_who_the_question_means(), test_a_person_nobody_has_confirmed_is_not_named(), test_a_question_naming_one_other_member_is_scoped_to_them(), test_the_owner_asking_about_themselves_by_name_is_scoped_to_the_owner(), test_whose_asks_whose_when_a_member_is_named_without_a_possessive(), test_whose_gives_a_person_named_outright() (+11 more)

### Community 31 - "test_runtime.py"
Cohesion: 0.09
Nodes (23): ModelWarmth, _ollama_answering(), test_a_database_that_does_not_answer_fails_in_seconds(), test_a_model_that_cannot_load_is_recorded_rather_than_raised(), test_an_embedding_model_without_task_prompts_is_sent_the_text_alone(), test_an_explicit_url_still_wins_over_the_port_variable(), test_busy_port_does_not_open_browser(), test_database_version_extension_and_tables_are_required() (+15 more)

### Community 32 - "test_pages.py"
Cohesion: 0.08
Nodes (21): document_page(), page_images(), page_count(), PageUnavailable, _pdfium(), render_page(), RendererUnavailable, _size() (+13 more)

### Community 33 - "_pages_from"
Cohesion: 0.22
Nodes (10): _kind(), _pages_from(), _table_text(), _cell(), _on_page(), test_a_document_is_titled_by_the_string_fields_its_pack_declares(), test_a_table_is_kept_as_label_and_value_lines_in_reading_order(), test_a_wider_table_keeps_every_column_and_a_spanned_cell_once() (+2 more)

### Community 34 - "test_eval_generate.py"
Cohesion: 0.06
Nodes (27): _ambiguous(), choose(), Generated, hand_written(), main(), on_file(), pool(), write_lane() (+19 more)

### Community 35 - "FakeConn"
Cohesion: 0.09
Nodes (45): client_for(), FakeConn, filed_document(), inbox(), obligation(), open_obligation(), pack_row(), rows_for() (+37 more)

### Community 36 - "ModuleManifest"
Cohesion: 0.08
Nodes (19): ModuleManifest, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, enabled_module_ids(), _module_row(), modules() (+11 more)

### Community 37 - "Any"
Cohesion: 0.14
Nodes (10): by_subject(), db(), FakeCursor, load_register(), test_a_deductible_receipt_counts_in_its_own_year_only(), test_a_lapsed_policy_is_not_masked_by_another_that_still_runs(), test_cpf_is_this_years_payslips_per_employee(), test_donations_are_this_years_deductible_receipts_per_donor() (+2 more)

### Community 38 - "reminder/__init__.py"
Cohesion: 0.10
Nodes (9): already_said(), close(), current_lead(), next_window(), Overdue, snooze(), UnknownObligation, test_never_notified_is_never_said() (+1 more)

### Community 39 - "test_api.py"
Cohesion: 0.07
Nodes (28): advising(), client(), conn(), FakeGraph, graph(), _padded(), streaming(), test_a_turn_can_only_be_the_person_or_parrot() (+20 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.19
Nodes (10): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), srs_contributions_ytd(), _totals() (+2 more)

### Community 41 - "retrieve.py"
Cohesion: 0.14
Nodes (12): Connection, load_matrix(), pack(), stats(), unpack(), embed_chunks(), _fts_query(), fuse() (+4 more)

### Community 42 - "sse"
Cohesion: 0.10
Nodes (22): Citation, Reading, a_citation(), advice_card(), rule_citation(), sse(), StreamingGraph, test_a_citation_says_whether_it_is_a_page_or_a_document_on_file() (+14 more)

### Community 43 - "Any"
Cohesion: 0.10
Nodes (17): advised_pack(), db(), _document(), _facts_tuple(), FakeConn, FakeCursor, _source(), _sum_insured() (+9 more)

### Community 44 - "test_startup.py"
Cohesion: 0.08
Nodes (20): _kill_tree(), start_web(), stop_web(), stop_worker(), main(), report_hardware(), startup_gaps(), prepare_checkout() (+12 more)

### Community 45 - "_obligation"
Cohesion: 0.15
Nodes (10): obligation_precision(), Config, _obligation(), test_a_calendar_deadline_is_checked_against_the_catalogue_and_counted_apart(), test_a_date_the_document_does_not_print_is_a_false_obligation(), test_an_obligation_for_a_document_the_register_does_not_have(), test_an_obligation_whose_date_the_document_prints_is_correct(), test_case_is_not_a_disagreement_about_who_someone_is() (+2 more)

### Community 46 - "test_gate.py"
Cohesion: 0.11
Nodes (26): check_advice(), check_one(), Claim, test_a_claim_citing_the_same_document_twice_says_it_once(), test_a_grounded_claim_renders_its_document_and_page(), _dual_cited_calculation(), test_a_number_copied_from_the_passage_is_kept_however_it_is_formatted(), test_a_number_no_cited_passage_printed_is_dropped() (+18 more)

### Community 47 - "typing"
Cohesion: 0.06
Nodes (19): Chunk, ExtractedFact, Extraction, fixed(), from_facts(), _label(), parse(), ParsedDocument (+11 more)

### Community 48 - "build_router"
Cohesion: 0.08
Nodes (27): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, RetryAccepted, _as_person(), _as_vault_document() (+19 more)

### Community 49 - "scope.py"
Cohesion: 0.19
Nodes (9): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Person (+1 more)

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 51 - "pack"
Cohesion: 0.09
Nodes (27): Categories, holdings(), Asked, categories_asked(), categorise(), glossary(), _make_replacer(), mentions() (+19 more)

### Community 52 - "packs.py"
Cohesion: 0.20
Nodes (5): installed_packs(), _load_one(), test_every_installed_pack_still_loads(), test_every_pack_speaks_only_for_catalogue_types(), test_the_template_directory_is_not_an_installed_pack()

### Community 53 - "test_grounding.py"
Cohesion: 0.17
Nodes (12): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), _document(), _installed(), test_a_missing_recorded_file_is_refused(), test_a_pack_with_no_corpus_gives_none_and_empty() (+4 more)

### Community 54 - "run.py"
Cohesion: 0.08
Nodes (11): enabled_pack_ids(), enabled_packs(), HybridRetriever, DatabaseUnavailable, _Formatter, find_browser_executable(), generate_documents(), _ask() (+3 more)

### Community 55 - "cli.py"
Cohesion: 0.20
Nodes (14): build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest(), cmd_init() (+6 more)

### Community 56 - "main"
Cohesion: 0.14
Nodes (12): _chosen(), _counts(), _facts(), main(), _note(), _page_text(), _partition(), _progress() (+4 more)

### Community 57 - "ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.15
Nodes (17): Code-written absence sentence: 'None of the N policies on file is a dental plan.', ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic, The advise route intent returns the pack's advice_decline, answering.categories: ordered whole-word rules over one printed field, Category filter applied before the keep-6 cut, answering.exclusions: headings under which a cover claim is not believed, Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration) (+9 more)

### Community 58 - "build.py"
Cohesion: 0.09
Nodes (13): DocumentCatalog, _class_name(), _docstring(), _field_line(), _header(), load(), load_catalog(), main() (+5 more)

### Community 59 - "test_grounding_index.py"
Cohesion: 0.10
Nodes (24): GroundingDocument, SourceText, index_pack(), IndexReport, _upsert_source(), ExtractedValue, _Connected, _extracted() (+16 more)

### Community 60 - "test_telegram_capture.py"
Cohesion: 0.11
Nodes (22): TelegramSettings, build(), FakeTelegram, photo_update(), test_a_chat_outside_the_allow_list_is_ignored(), test_a_conflict_names_the_webhook_rather_than_saying_nothing(), test_a_document_keeps_the_name_it_was_sent_under(), test_a_malformed_allow_list_is_a_configuration_error_not_an_empty_one() (+14 more)

### Community 61 - "test_grounding_values.py"
Cohesion: 0.16
Nodes (27): _dropped(), _log_values(), _run(), test_a_money_value_with_a_currency_marker_is_kept(), test_a_multiple_is_kept_in_the_forms_it_is_written(), test_a_number_is_kept_when_one_of_its_occurrences_fits_the_unit(), test_a_number_matches_its_printed_decimal_form(), test_a_number_not_in_its_passage_is_dropped() (+19 more)

### Community 62 - "create_app"
Cohesion: 0.27
Nodes (6): create_app(), checks(), lifespan(), ready(), setup(), system_status()

### Community 63 - "lock.ts"
Cohesion: 0.10
Nodes (35): dynamic, GET(), grant(), POST(), runtime, ACTIONS, dynamic, GET() (+27 more)

### Community 64 - "ModuleAdviser"
Cohesion: 0.11
Nodes (12): FactInput, fact_row(), FactRow, facts_for(), in_category(), _is_an_adviser(), _latest_per_document(), ModuleAdviser (+4 more)

### Community 65 - "routes.py"
Cohesion: 0.08
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

### Community 69 - "api.ts"
Cohesion: 0.08
Nodes (31): RELATION_CHOICES, Place, PLACES, DocumentDetail(), when(), Field(), format(), isNumeric() (+23 more)

### Community 70 - "advice-consent.tsx"
Cohesion: 0.17
Nodes (17): Consent, ConsentPrompt(), agree(), settle(), State, ADR-0016, AdviceConsentSection(), fetchConsents() (+9 more)

### Community 71 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 72 - "extract_values"
Cohesion: 0.18
Nodes (12): extract_values(), _long_text(), _reply(), ScriptedClient, _source(), test_a_json_reply_with_no_usable_values_is_no_values_for_that_section_only(), test_a_long_text_is_sent_in_more_than_one_call(), test_a_model_that_is_down_raises() (+4 more)

### Community 73 - "Hybrid Retrieval: Dense Plus Full-Text"
Cohesion: 0.18
Nodes (5): bge-reranker-v2-m3 Cross-Encoder, 40 Down to 6, Hybrid Retrieval: Dense Plus Full-Text, Reciprocal Rank Fusion, k=60, The Household's Eleven Policies, The Validator Is the Handover Gate

### Community 74 - "worker.py"
Cohesion: 0.15
Nodes (9): install(), install_best_effort(), Installed, _beat_needs_its_own_process(), celery_argv(), main(), _run(), _start_beat() (+1 more)

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.17
Nodes (11): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), Telegram chat_id maps to a person, Possessive relations scope the question, before the cut to six, Naming exactly one person scopes to them (whole name, or a 3+ letter possessive unique to them) (+3 more)

### Community 76 - "FakeConn"
Cohesion: 0.10
Nodes (20): current(), grant(), HouseholdConsents, _latest(), NoOwner, _record(), status(), withdraw() (+12 more)

### Community 77 - "test_modules.py"
Cohesion: 0.15
Nodes (21): AlertConfig, sweep(), sweep(), FakeConn, obligation_row(), srs_row(), test_a_dry_run_records_nothing(), test_a_firing_older_than_the_debounce_window_fires_again() (+13 more)

### Community 78 - "test_tax_pack.py"
Cohesion: 0.18
Nodes (11): _basis(), _latest(), _matched(), _published(), _register(), _shape(), test_a_tax_question_reaches_the_tax_shape_and_insurance_keeps_its_own(), test_no_saving_is_estimated_without_a_notice_of_assessment() (+3 more)

### Community 79 - "test_eval_harness.py"
Cohesion: 0.12
Nodes (19): Cited, reference_for(), Expected, load_set(), MalformedQuestion, Question, subset(), _question() (+11 more)

### Community 80 - "preview.tsx"
Cohesion: 0.10
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 81 - "test_scan_parse.py"
Cohesion: 0.10
Nodes (7): DoclingParser, _as_printed(), page_pixels(), photographed(), _register_row(), scanned(), test_a_scan_keeps_the_schedule_table_and_its_page()

### Community 82 - "Two-stage quarantine with a vision-language second pass"
Cohesion: 0.12
Nodes (11): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Two-stage quarantine with a vision-language second pass, Batch 4: the deliberately hard documents, Task: review every quarantined document and label the failure, Task: sign off the capture-to-database path against the data inventory, PaperBrain handled failure modes, The pb command line (+3 more)

### Community 83 - "Any"
Cohesion: 0.11
Nodes (3): ConsentCursor, Fails, FakeCursor

### Community 84 - "Ollama"
Cohesion: 0.17
Nodes (5): answer(), build_context(), format_sources(), Ollama, Hit

### Community 85 - "InstalledPack"
Cohesion: 0.19
Nodes (6): AdviceShape, Adviser, Calculation, Missing, InstalledPack, Adviser

### Community 86 - "test_contracts.py"
Cohesion: 0.08
Nodes (40): PackManifest, _advised(), _checked(), _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape() (+32 more)

### Community 87 - "ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.16
Nodes (18): ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel), Advice graph flow: shape match, subject resolution, consent, AdviceCard, explain, advice_records keeps each answer's full basis, PackManifest.advice shapes (gap, remaining_room, keep_or_surrender, compare_own, compare_market, estimate_saving), Advice.review: one question runs every shape at once, A grounding corpus lives at packs/<pack>/grounding/<corpus_id>/ (+10 more)

### Community 88 - "Answer"
Cohesion: 0.14
Nodes (9): Answer, Asks, ask(), _answered(), FakeGraph, FakeRetriever, KeepAll, _passage() (+1 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "test_eval_modules.py"
Cohesion: 0.19
Nodes (8): alert_fpr(), AlertVerdict, score_alerts(), Fired, test_a_metric_with_no_register_equivalent_is_not_guessed_at(), test_an_alert_the_register_agrees_with_is_not_counted_against_the_module(), test_an_alert_the_register_contradicts_is_a_false_positive(), test_nothing_fired_is_unmeasured_rather_than_zero()

### Community 91 - "HouseholdAdviceLog"
Cohesion: 0.14
Nodes (6): HouseholdAdviceLog, AdviceLog, AdviceRecord, ConsentBook, test_record_insert_includes_the_sha256_of_the_disclaimer(), Log

### Community 92 - "build"
Cohesion: 0.07
Nodes (16): _without_one_round_of_passage_numbers(), _without_passage_numbers(), build(), passage(), test_a_grounded_question_is_answered_with_its_source(), test_a_model_that_is_not_running_abstains_rather_than_inventing(), test_a_passage_number_outside_the_evidence_is_ignored(), test_a_payslip_is_governed_by_the_tax_pack_not_the_strictest() (+8 more)

### Community 93 - "item-row.tsx"
Cohesion: 0.15
Nodes (14): SourceChip(), SourcePanel(), stripTrailingPage(), ADR-0016, countdown(), detail(), figure(), ItemRow() (+6 more)

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

### Community 98 - "eval/modules.py"
Cohesion: 0.21
Nodes (8): _day(), Measured, _number(), register_cpf_contributions_ytd(), register_days_uncovered(), register_donations_ytd(), register_srs_contributions_ytd(), test_the_register_metrics_mirror_the_modules_queries()

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.10
Nodes (11): Generated Files Committed Alongside Their Source, benefit_illustration Document Type, birth_certificate Document Type, claim_letter Document Type, cpf_statement Document Type, Core Document Catalogue (ADR 0017), donation_receipt Document Type, identity_card Document Type (+3 more)

### Community 100 - "Registration"
Cohesion: 0.18
Nodes (3): Registration, FakeRegistrar, explode_once()

### Community 102 - "The five-lane split (five people, nine weeks, three builders)"
Cohesion: 0.09
Nodes (18): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The domain pack manifest, The expansion model: two axes, not one list, The golden set: answerable, hard negatives, adversarial, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build (+10 more)

### Community 103 - "Data inventory: identity data, DOBs and loans"
Cohesion: 0.17
Nodes (7): Data inventory: identity data, DOBs and loans, Telegram capture route and delete-at-source, What crosses a boundary, Governance artefact set, The final ILP report, db service (pgvector/pgvector:pg17), redis service (redis:7-alpine)

### Community 104 - "test_rerank.py"
Cohesion: 0.09
Nodes (17): CrossEncoderReranker, passage_text(), relevance(), FakeEncoded, FakeModel, FakeTokenizer, no_weights(), _passage() (+9 more)

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

### Community 111 - "checks.py"
Cohesion: 0.15
Nodes (10): capture_check(), Check, collect_checks(), database_check(), interface_check(), model_check(), redis_check(), telegram_check() (+2 more)

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

### Community 116 - "test_household.py"
Cohesion: 0.15
Nodes (13): scope_passages(), conn(), _conn_returning(), _passage(), test_a_document_naming_the_owner_and_somebody_else_is_kept(), test_a_document_with_no_subject_belongs_to_everybody(), test_a_household_with_no_owner_scopes_nothing(), test_an_unscoped_result_is_not_empty_for_the_owner() (+5 more)

### Community 117 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 118 - "_answer_events"
Cohesion: 0.11
Nodes (10): Source, _answer_events(), _as_source(), today(), _cite(), connection(), _link(), _settings() (+2 more)

### Community 119 - "test_advice_core.py"
Cohesion: 0.25
Nodes (10): _kind_of(), passages_for(), check_content(), _calculation(), test_check_content_keeps_a_sentence_stating_a_facts_value(), test_check_content_keeps_a_sentence_stating_a_figure(), test_check_content_keeps_a_sentence_stating_a_rules_value(), test_check_content_still_drops_a_sentence_stating_an_unprinted_number() (+2 more)

### Community 121 - "pathlib"
Cohesion: 0.07
Nodes (14): FolderSettings, Dispatcher, Inline, Send, Intake, attribution(), broker_available(), dispatcher_for() (+6 more)

### Community 122 - "ModelUnavailable"
Cohesion: 0.13
Nodes (7): Generated, ModelUnavailable, test_a_model_that_dies_before_any_sentence_abstains(), constrained_stream(), constrained_stream(), extract(), down()

### Community 123 - "Terms of use"
Cohesion: 0.25
Nodes (7): Clause A. Authority and Consent for Submissions on Behalf of Another Adult, Clause B. Purpose of Collection, Use and Retention, Clause C. Personal Data of Third Parties, Definitions, For review, Not yet written, Terms of use

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.17
Nodes (8): Task: benchmark the workstation and publish the numbers, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, Yew Mun's generated task list, Roadmap phase 1 - retrieval, PaperBrain hybrid retrieval (BM25 + dense, fused by RRF), Sample home contents insurance policy, Sample supermarket tax invoice

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 127 - "packs/page.tsx"
Cohesion: 0.06
Nodes (28): ADR-0017, next, dynamic, metadata, PacksPage(), runtime, DocumentPage(), dynamic (+20 more)

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
Nodes (36): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+28 more)

### Community 143 - "same_value"
Cohesion: 0.25
Nodes (5): _as_date(), _as_number(), same_value(), value_forms(), test_same_value_normalises_dates_numbers_and_text()

### Community 144 - "Settings"
Cohesion: 0.14
Nodes (13): Settings, consent(), ConsentConn, test_a_grant_to_an_older_wording_is_listed_as_outdated(), test_consent_to_a_wording_that_is_no_longer_current_is_409(), test_consent_to_an_unknown_pack_or_one_that_does_not_advise_is_400(), test_consent_without_an_owner_is_422(), test_consents_list_each_advising_pack_and_what_the_owner_last_said() (+5 more)

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

### Community 154 - "FakeOllama"
Cohesion: 0.10
Nodes (13): DocumentTypeSpec, Classification, classify(), _prompt(), _schema(), document_types(), FakeOllama, test_a_document_no_pack_recognises_is_not_forced_into_one() (+5 more)

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (6): Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "IngestJob"
Cohesion: 0.19
Nodes (3): IngestJob, _Pending, _Registered

### Community 157 - "collections_abc"
Cohesion: 0.09
Nodes (6): render(), main(), _read_rows(), _render(), _week_key(), _write()

### Community 158 - "Adversarial testing from week 7"
Cohesion: 0.25
Nodes (8): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Adversarial testing from week 7, Prompt injection carried inside a document, Scope attack: asking it to act, Task: run adversarial Set C and write up the findings, Adversarial Set C (15 questions that should not be answered), Golden Set C - adversarial (15)

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 162 - "HouseholdInventory"
Cohesion: 0.15
Nodes (7): AskResponse, _as_response(), ask(), ask_stream(), _graph_for(), _history(), HouseholdInventory

### Community 163 - "Registrar"
Cohesion: 0.15
Nodes (4): Cursor, Registrar, cursor(), cursor()

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

### Community 169 - "ModuleMetrics"
Cohesion: 0.22
Nodes (5): _mark(), ModuleMetrics, render(), test_the_report_marks_both_metrics_against_their_target(), test_the_report_says_nothing_fired_rather_than_printing_a_rate()

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

### Community 176 - "_as_consent"
Cohesion: 0.33
Nodes (3): AdviceConsent, _as_consent(), record_consent()

### Community 177 - "test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them"
Cohesion: 0.22
Nodes (3): ClosingSpy, test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them(), spying()

### Community 179 - "The synthetic-to-real gap"
Cohesion: 0.40
Nodes (4): The 40-document redacted holdout, Consent and redaction protocol, Task: write the PDPA position on using synthetic data, Task: evaluation run 3 plus the holdout run

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 182 - "Passage"
Cohesion: 0.05
Nodes (19): _advice_prompt(), _citations(), fuse(), _minor(), _numbered(), DenseRetriever, NoReranker, precheck() (+11 more)

### Community 183 - "Part A. Policy"
Cohesion: 0.20
Nodes (9): A1. Retention rules, A2. What erasure means, A3. Three ways to erase, A4. Deleting a document: only on instruction, confirmed, and complete within 72 hours, A5. Erasing a person, and resetting the workspace, Basis, Decisions for Siew, Part A. Policy (+1 more)

### Community 184 - "Scoped"
Cohesion: 0.15
Nodes (8): scope_to(), Scoped, test_a_question_about_a_parent_names_them_as_who_it_is_about_and_carries_todays_date(), apply(), test_a_question_about_a_relation_nobody_holds_is_not_answered_from_the_owners_documents(), apply(), test_a_question_naming_another_member_does_not_call_them_the_asker(), apply()

### Community 185 - "correct"
Cohesion: 0.25
Nodes (3): correct(), Corrected, UnknownFact

### Community 186 - "_page_of_examples"
Cohesion: 0.24
Nodes (5): _page_of_examples(), _reply_of_examples(), test_a_donation_receipt_stores_donation_amount_and_never_amount(), test_a_fact_is_stored_under_the_name_the_catalogue_declares(), test_each_rider_is_its_own_fact_with_its_name_and_sum_assured()

### Community 189 - "gate.py"
Cohesion: 0.16
Nodes (8): Exclusions, _normal(), _says(), states_a_printed_value(), unprinted_numbers(), test_a_date_on_file_may_be_written_the_way_a_person_says_it(), test_a_leading_zero_does_not_make_a_printed_date_unprinted(), test_a_policy_number_is_kept_only_when_it_is_printed_whole()

### Community 190 - "_closes"
Cohesion: 0.21
Nodes (8): _closes(), _either(), _shape(), test_a_gap_closed_by_two_kinds_names_the_one_held_and_the_one_not(), test_a_gap_in_cover_already_held_asks_for_more_of_it_not_for_a_first_policy(), test_a_gap_with_nothing_on_file_says_none_is_on_file(), test_a_shape_that_names_no_cover_adds_no_sentence(), test_an_is_written_only_before_a_e_i_or_o()

### Community 200 - "advice_consents"
Cohesion: 0.33
Nodes (7): advice_consents(), 1. What counts, B1. The only erasure paths that exist, B2. What deleting a `documents` row cascades to, and what it leaves, B4. Does today's system meet Part A?, Part B. What the code does today, Status against the code

### Community 201 - "Alert"
Cohesion: 0.25
Nodes (3): Alert, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

### Community 204 - "package.json"
Cohesion: 0.11
Nodes (16): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+8 more)

### Community 205 - "rerank.py"
Cohesion: 0.23
Nodes (5): device_name(), load(), score_pairs(), _warn_once(), reranker_check()

### Community 211 - "State"
Cohesion: 0.13
Nodes (4): _asked(), _conversation(), _review_asked(), State

### Community 213 - "contracts.py"
Cohesion: 0.12
Nodes (15): Advice, Answering, Category, FieldSpec, Grounding, Guardrails, ModuleTrigger, Persona (+7 more)

### Community 215 - "is_first_person"
Cohesion: 0.20
Nodes (7): is_first_person(), relation_asked(), test_a_name_that_is_not_exactly_one_person_scopes_nothing(), test_a_named_household_member_wins_over_the_pronoun(), test_a_possessive_relation_names_whose_documents_are_asked_about(), test_first_person_questions_are_recognised(), test_questions_about_other_people_are_not_scoped()

### Community 216 - "test_a_client_that_leaves_after_the_card_commits_one_record"
Cohesion: 0.18
Nodes (5): next_kind(), test_a_client_that_leaves_after_the_card_commits_one_record(), test_a_client_that_leaves_mid_explanation_still_commits_what_it_was_shown(), test_a_stream_closed_exactly_at_the_card_is_still_committed_by_the_api(), test_closing_the_graph_when_the_record_write_fails_rolls_back()

### Community 218 - "scripts/reindex.py"
Cohesion: 0.23
Nodes (6): indexed(), IndexedDocument, reindex_document(), ReindexFailed, _Value, main()

### Community 219 - "IMDA frameworks: what applies to PARROT"
Cohesion: 0.25
Nodes (7): Agentic AI framework: four dimensions, Findings from this pass, For Siew, GenAI framework: nine dimensions, IMDA frameworks: what applies to PARROT, The two instruments, AdviceNote()

### Community 221 - "[...path]/route.ts"
Cohesion: 0.25
Nodes (10): ALLOWED, Context, DELETE(), dynamic, forward(), GET(), PATCH(), POST() (+2 more)

### Community 222 - "check"
Cohesion: 0.25
Nodes (6): check(), Verdict, test_a_sentence_citing_a_passage_that_was_never_retrieved_is_dropped(), test_a_sentence_with_no_supporting_passage_is_dropped(), test_no_passages_at_all_abstains(), test_weak_evidence_abstains_before_anything_is_written()

### Community 224 - "score_obligations"
Cohesion: 0.17
Nodes (7): measure(), Obligation, obligations(), obligations_possible(), _same_person(), score_obligations(), test_what_the_register_supports_is_reported_beside_the_precision()

### Community 226 - "Incident and data breach procedure"
Cohesion: 0.25
Nodes (7): 2. The six steps, 3. Is it a notifiable breach?, 4. The incident log, 5. Who is responsible on a household's own computer, Containment, by kind, Decisions for Siew, Incident and data breach procedure

### Community 227 - "main"
Cohesion: 0.33
Nodes (4): main(), _paragraph(), _corpus_sha(), _git_sha()

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
- **400 isolated node(s):** `The two instruments`, `Findings from this pass`, `For Siew`, `3. Is it a notifiable breach?`, `4. The incident log` (+395 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1735 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
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