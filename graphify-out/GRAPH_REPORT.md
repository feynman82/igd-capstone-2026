# Graph Report - igd-capstone-2026  (2026-10-01)

## Corpus Check
- 314 files · ~723,001 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 34 file(s) not represented in the graph (top: (none) 11, .jsonl 7, .csv 5)

## Summary
- 4720 nodes · 11636 edges · 199 communities (165 shown, 34 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1070 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b00ed608`
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
- test_ingest_pipeline.py
- test_grounding_index.py
- test_worker_queue.py
- FolderAdapter
- test_telegram_capture.py
- FakeConn
- answer.py
- bench_runtime.py
- vault.py
- support.js
- worker.py
- _read
- test_grounding_values.py
- report.py
- pathlib
- State
- SentenceScanner
- household.py
- ParsedPage
- test_lifecycle.py
- score.py
- _household_scope
- .load
- test_pages.py
- _pages_from
- test_eval_generate.py
- TelegramAdapter
- pytest
- Any
- test_modules.py
- test_api.py
- alert/__init__.py
- retrieve.py
- sse
- base.py
- run_parrot.py
- test_eval_modules.py
- test_gate.py
- pipeline.py
- build_router
- test_household.py
- compilerOptions
- InstalledPack
- registry.py
- test_grounding.py
- classify.py
- cli.py
- run.py
- ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic
- build.py
- eval/modules.py
- ingest/reindex.py
- values.py
- ingest/quarantine.py
- lock.ts
- _advised
- models.py
- PARROT Interface Design Pack
- export-design-preview.cjs
- The Four Surfaces
- test_advice_core.py
- advice-consent.tsx
- devDependencies
- gate.py
- Hybrid Retrieval: Dense Plus Full-Text
- scope.py
- ADR 0011: The household is people and aliases, and the owner is one of them
- FakeConn
- sweep
- date
- test_eval_harness.py
- preview.tsx
- extract_values
- Two-stage quarantine with a vision-language second pass
- Any
- Ollama
- api.ts
- validate.py
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- test_contracts.py
- components.json
- test_registration.py
- test_tax_pack.py
- contracts.py
- _answer_events
- test_eval_report.py
- The Lim Household, Tampines
- ADR 0007 - The graph ships before retrieval and before a checkpoint table
- Lane C - Governance and assurance
- PackManifest
- Core Document Catalogue (ADR 0017)
- find_page
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
- checks.py
- example_pack template manifest
- paperbrain/extract.py
- §5 · Evaluation and results
- tokens/page.tsx
- test_a_grounding_corpus_travels_inside_its_pack
- Integration review
- core/modules.py
- FakeCursor
- TelegramCapture
- ModelUnavailable
- _as_consent
- The deliberately naive retrieval baseline
- Running the evaluation harness
- FakeCursor
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
- install_best_effort
- Settings
- schedule.py
- PrivateCare Policy Wording Template
- alert module manifest
- is_first_person
- same_value
- next
- The Grounding Gate
- Authoring a domain pack
- ADR 0008 - Ingestion runs on a Celery worker
- unprinted_numbers
- DesignPreview evaluation harness
- typing
- Adversarial testing from week 7
- Writing an ADR
- Every Fact Row Cites Its Source
- _as_response
- Cursor
- send_retry
- PARROT evaluation harness
- RagasJudge
- The autonomy statement
- PackUnavailable
- test_both_ask_endpoints_hand_the_graph_the_same_advice_ports
- routes.py
- ADR index (0001-0018, with status)
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- _today_items
- test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them
- The synthetic-to-real gap
- filesystem
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

## Communities (199 total, 34 thin omitted)

### Community 0 - "Ollama"
Cohesion: 0.07
Nodes (26): Recovery, recovery_rate(), retry(), _still_quarantined(), bytes_for(), digest_of_document(), SourceMissing, Ollama (+18 more)

### Community 1 - "test_hybrid.py"
Cohesion: 0.09
Nodes (16): hybrid_score(), HybridRetriever, identifiers(), prints(), FakeConn, FakeCursor, FakeOllama, _row() (+8 more)

### Community 2 - "ScriptedOllama"
Cohesion: 0.06
Nodes (49): AdviceCard, AdviceWithheld, _closes(), ConsentRequired, Sentence, Subject, advised_pack(), build() (+41 more)

### Community 3 - "test_answer_graph.py"
Cohesion: 0.05
Nodes (65): Abstained, AnswerGraph, Declined, Finished, _pack_for(), Refused, Holding, Passage (+57 more)

### Community 4 - "validate"
Cohesion: 0.09
Nodes (24): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), validate(), _wide_format() (+16 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.05
Nodes (60): AdviceShape, Adviser, Calculation, Figure, Input, Missing, _ambiguous(), _amount() (+52 more)

### Community 6 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.05
Nodes (59): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, MediShield Life (CPF Board), Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022 (+51 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.07
Nodes (64): calculate(), advised_pack(), assert_nothing_negative(), basis(), db(), _document(), fact(), _facts_tuple() (+56 more)

### Community 8 - "today/page.tsx"
Cohesion: 0.07
Nodes (29): dynamic, HouseholdPage(), metadata, runtime, AppLayout(), dynamic, isUrgent(), metadata (+21 more)

### Community 9 - "test_ingest_pipeline.py"
Cohesion: 0.08
Nodes (35): extract(), printed_date(), FakeOllama, insurance(), iras(), _page_of_examples(), _reply_of_examples(), test_a_date_that_cannot_be_read_still_quarantines() (+27 more)

### Community 10 - "test_grounding_index.py"
Cohesion: 0.05
Nodes (38): index_pack(), IndexReport, _upsert_source(), approve(), pending(), PendingValue, reject(), _block() (+30 more)

### Community 11 - "test_worker_queue.py"
Cohesion: 0.08
Nodes (21): sha256(), Inline, Queued, Intake, Registration, index_folder(), FakeConnection, RecordingSend (+13 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.12
Nodes (18): FolderAdapter, FolderSettings, FolderCapture, _loop(), main(), FakeRegistrar, _settle(), test_a_file_removed_before_it_settles_is_forgotten() (+10 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.08
Nodes (27): TelegramSettings, TelegramUnavailable, _loop(), main(), build(), FakeRegistrar, FakeTelegram, photo_update() (+19 more)

### Community 14 - "FakeConn"
Cohesion: 0.07
Nodes (34): conn(), FakeConn, next_kind(), obligation(), open_obligation(), overdue_row(), pack_row(), rows_for() (+26 more)

### Community 15 - "answer.py"
Cohesion: 0.04
Nodes (24): AdviceLog, AdviceRecord, ConsentBook, _advice_basis(), _advice_prompt(), answer_system(), _as_sentence(), _citations() (+16 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (20): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+12 more)

### Community 17 - "vault.py"
Cohesion: 0.09
Nodes (13): correct(), Corrected, UnknownFact, _as_document(), declared_type(), document(), documents(), Fact (+5 more)

### Community 18 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 19 - "worker.py"
Cohesion: 0.14
Nodes (8): find_browser_executable(), generate_documents(), _beat_needs_its_own_process(), celery_argv(), main(), _run(), _start_beat(), _stop_beat()

### Community 20 - "_read"
Cohesion: 0.21
Nodes (5): _coerce(), decode_schema(), _drop_format(), _prepare(), _read()

### Community 21 - "test_grounding_values.py"
Cohesion: 0.16
Nodes (28): ExtractedValue, _dropped(), _log_values(), _run(), test_a_money_value_with_a_currency_marker_is_kept(), test_a_multiple_is_kept_in_the_forms_it_is_written(), test_a_number_is_kept_when_one_of_its_occurrences_fits_the_unit(), test_a_number_matches_its_printed_decimal_form() (+20 more)

### Community 22 - "report.py"
Cohesion: 0.14
Nodes (12): _cell(), collect(), main(), _overall(), _paragraph(), Provenance, render(), _row() (+4 more)

### Community 23 - "pathlib"
Cohesion: 0.05
Nodes (27): _graph_for(), HouseholdConsents, HouseholdAdviceLog, DenseRetriever, NoReranker, HouseholdInventory, HouseholdScope, enabled_pack_ids() (+19 more)

### Community 24 - "State"
Cohesion: 0.15
Nodes (4): _asked(), _conversation(), fuse(), State

### Community 25 - "SentenceScanner"
Cohesion: 0.09
Nodes (13): SentenceScanner, drip(), test_a_backslash_before_a_quote_is_handled(), test_a_brace_inside_a_sentence_does_not_end_it(), test_a_sentence_is_released_before_the_rest_has_been_written(), test_a_sentence_that_is_not_an_object_is_skipped_rather_than_crashing(), test_a_truncated_stream_keeps_the_sentences_that_did_arrive(), test_an_answer_with_no_sentences_yields_nothing_and_keeps_its_missing() (+5 more)

### Community 26 - "household.py"
Cohesion: 0.09
Nodes (21): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+13 more)

### Community 27 - "ParsedPage"
Cohesion: 0.12
Nodes (16): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), classification_sample(), ParsedPage, PlainTextParser (+8 more)

### Community 28 - "test_lifecycle.py"
Cohesion: 0.12
Nodes (19): Lifecycle, _client(), _eventually(), _launcher(), Screens, _supervise(), test_a_browser_cannot_reach_the_engine_directly_even_with_the_header(), test_a_request_without_the_intent_header_is_refused() (+11 more)

### Community 29 - "score.py"
Cohesion: 0.06
Nodes (34): Answer, Asks, Trace, cites(), _contains(), declined_in_prose(), doc_stem(), grade() (+26 more)

### Community 30 - "_household_scope"
Cohesion: 0.09
Nodes (19): _household_scope(), test_a_grandparent_nobody_holds_is_an_unknown_relation_not_the_fathers_policy(), test_a_grandparent_recorded_under_that_name_is_who_the_question_means(), test_a_person_nobody_has_confirmed_is_not_named(), test_a_question_naming_one_other_member_is_scoped_to_them(), test_the_owner_asking_about_themselves_by_name_is_scoped_to_the_owner(), test_whose_asks_whose_when_a_member_is_named_without_a_possessive(), test_whose_gives_a_person_named_outright() (+11 more)

### Community 31 - ".load"
Cohesion: 0.07
Nodes (35): create_app(), checks(), ready(), setup(), system_status(), ModelWarmth, warm_models(), _chat_ids() (+27 more)

### Community 32 - "test_pages.py"
Cohesion: 0.08
Nodes (21): document_page(), page_images(), page_count(), PageUnavailable, _pdfium(), render_page(), RendererUnavailable, _size() (+13 more)

### Community 33 - "_pages_from"
Cohesion: 0.20
Nodes (10): Block, _kind(), _pages_from(), _table_text(), _cell(), _on_page(), test_a_table_is_kept_as_label_and_value_lines_in_reading_order(), test_a_wider_table_keeps_every_column_and_a_spanned_cell_once() (+2 more)

### Community 34 - "test_eval_generate.py"
Cohesion: 0.08
Nodes (23): _ambiguous(), choose(), Generated, hand_written(), main(), on_file(), pool(), write_lane() (+15 more)

### Community 35 - "TelegramAdapter"
Cohesion: 0.11
Nodes (6): _attachment(), _pixels(), _status_reason(), TelegramAdapter, _write_local_copy(), Registrar

### Community 36 - "pytest"
Cohesion: 0.09
Nodes (8): DoclingParser, Parser, _as_printed(), page_pixels(), photographed(), _register_row(), scanned(), test_a_scan_keeps_the_schedule_table_and_its_page()

### Community 37 - "Any"
Cohesion: 0.14
Nodes (10): by_subject(), db(), FakeCursor, load_register(), test_a_deductible_receipt_counts_in_its_own_year_only(), test_a_lapsed_policy_is_not_masked_by_another_that_still_runs(), test_cpf_is_this_years_payslips_per_employee(), test_donations_are_this_years_deductible_receipts_per_donor() (+2 more)

### Community 38 - "test_modules.py"
Cohesion: 0.08
Nodes (20): already_said(), current_lead(), Due, next_window(), Overdue, snooze(), sweep(), UnknownObligation (+12 more)

### Community 39 - "test_api.py"
Cohesion: 0.11
Nodes (21): FakeGraph, graph(), streaming(), test_a_turn_can_only_be_the_person_or_parrot(), test_an_ask_citation_needs_no_lookup_to_be_openable(), test_ask_gives_consent_and_withheld_advice_their_own_kinds(), test_ask_refuses_a_request_to_act(), test_ask_requires_a_question() (+13 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.21
Nodes (9): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), srs_contributions_ytd(), _totals() (+1 more)

### Community 41 - "retrieve.py"
Cohesion: 0.14
Nodes (12): Connection, load_matrix(), pack(), stats(), unpack(), embed_chunks(), _fts_query(), fuse() (+4 more)

### Community 42 - "sse"
Cohesion: 0.10
Nodes (22): Citation, Reading, a_citation(), advice_card(), rule_citation(), sse(), StreamingGraph, test_a_citation_says_whether_it_is_a_page_or_a_document_on_file() (+14 more)

### Community 43 - "base.py"
Cohesion: 0.09
Nodes (6): CaptureAdapter, IngestJob, sniff_mime(), _Pending, _Registered, test_mime_is_sniffed_from_the_bytes_first()

### Community 44 - "run_parrot.py"
Cohesion: 0.05
Nodes (28): _kill_tree(), main(), open_browser(), parse_args(), port_answers(), spawn_child(), start_web(), start_worker() (+20 more)

### Community 45 - "test_eval_modules.py"
Cohesion: 0.07
Nodes (26): alert_fpr(), AlertVerdict, _mark(), ModuleMetrics, Obligation, obligation_precision(), render(), score_alerts() (+18 more)

### Community 46 - "test_gate.py"
Cohesion: 0.14
Nodes (23): check_advice(), Claim, test_a_claim_citing_the_same_document_twice_says_it_once(), test_a_grounded_claim_renders_its_document_and_page(), test_a_number_copied_from_the_passage_is_kept_however_it_is_formatted(), test_a_number_no_cited_passage_printed_is_dropped(), test_a_page_and_a_document_on_file_with_the_same_id_are_different_citations(), test_an_exclusion_quoted_as_an_exclusion_is_kept() (+15 more)

### Community 47 - "pipeline.py"
Cohesion: 0.09
Nodes (15): Chunk, Extraction, fixed(), from_facts(), _label(), parse(), ParsedDocument, commit_both_lanes() (+7 more)

### Community 48 - "build_router"
Cohesion: 0.11
Nodes (24): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, QuarantinedDocument, QuarantineResponse, build_router() (+16 more)

### Community 49 - "test_household.py"
Cohesion: 0.15
Nodes (13): scope_passages(), conn(), _conn_returning(), _passage(), test_a_document_naming_the_owner_and_somebody_else_is_kept(), test_a_document_with_no_subject_belongs_to_everybody(), test_a_household_with_no_owner_scopes_nothing(), test_an_unscoped_result_is_not_empty_for_the_owner() (+5 more)

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 51 - "InstalledPack"
Cohesion: 0.05
Nodes (35): _Answering, Categories, _review_asked(), holdings(), Inventory, Asked, categories_asked(), categorise() (+27 more)

### Community 52 - "registry.py"
Cohesion: 0.11
Nodes (19): ModuleManifest, installed_modules(), installed_packs(), enabled_module_ids(), install(), _module_row(), modules(), _pack_row() (+11 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.18
Nodes (13): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), SourceText, _document(), _installed(), test_a_missing_recorded_file_is_refused() (+5 more)

### Community 54 - "classify.py"
Cohesion: 0.29
Nodes (5): Classification, classify(), _prompt(), _schema(), document_types()

### Community 55 - "cli.py"
Cohesion: 0.18
Nodes (14): build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest(), cmd_init() (+6 more)

### Community 56 - "run.py"
Cohesion: 0.13
Nodes (16): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), _indexed(), main() (+8 more)

### Community 57 - "ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.15
Nodes (17): Code-written absence sentence: 'None of the N policies on file is a dental plan.', ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic, The advise route intent returns the pack's advice_decline, answering.categories: ordered whole-word rules over one printed field, Category filter applied before the keep-6 cut, answering.exclusions: headings under which a cover claim is not believed, Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration) (+9 more)

### Community 58 - "build.py"
Cohesion: 0.09
Nodes (13): DocumentCatalog, _class_name(), _docstring(), _field_line(), _header(), load(), load_catalog(), main() (+5 more)

### Community 59 - "eval/modules.py"
Cohesion: 0.12
Nodes (13): _day(), measure(), Measured, _number(), obligations(), obligations_possible(), register_cpf_contributions_ytd(), register_days_uncovered() (+5 more)

### Community 60 - "ingest/reindex.py"
Cohesion: 0.12
Nodes (7): _vector_literal(), indexed(), IndexedDocument, reindex_document(), ReindexFailed, _Value, test_reindexing_replaces_chunks_and_leaves_facts_alone()

### Community 61 - "values.py"
Cohesion: 0.07
Nodes (22): _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), number_tokens(), _pack(), parse_value() (+14 more)

### Community 62 - "ingest/quarantine.py"
Cohesion: 0.18
Nodes (6): blocked_reasons(), forget(), QuarantinedDocument, queue(), StillInInbox, transcribe()

### Community 63 - "lock.ts"
Cohesion: 0.07
Nodes (45): dynamic, GET(), grant(), POST(), runtime, ALLOWED, Context, DELETE() (+37 more)

### Community 64 - "_advised"
Cohesion: 0.15
Nodes (11): _advised(), _checked(), test_a_market_comparison_may_compare_a_field_only_its_sources_publish(), test_a_review_names_only_declared_shapes_and_categories(), test_advice_naming_an_unknown_category_is_rejected_against_the_catalogue(), test_advice_reading_a_payslip_field_needs_no_second_pack(), test_an_inconsistent_advice_block_is_rejected_by_name(), test_an_insurance_manifest_with_advice_validates() (+3 more)

### Community 65 - "models.py"
Cohesion: 0.10
Nodes (21): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, CloseRequest, ConfirmNameRequest, ConsentRequest, ConsentRequiredEvent (+13 more)

### Community 66 - "PARROT Interface Design Pack"
Cohesion: 0.09
Nodes (21): Citation chips are the trust surface, Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Suggestions come from this week's ingest, Civic Register: order, clarity and institutional confidence, Kitchen Table: a little less household admin, a little more breathing room, The Reading Desk: understand it, open the source, see for yourself (+13 more)

### Community 67 - "export-design-preview.cjs"
Cohesion: 0.08
Nodes (20): @eslint/eslintrc, compat, eslintConfig, bundle(), classes, css, cssFile, domId (+12 more)

### Community 68 - "The Four Surfaces"
Cohesion: 0.13
Nodes (14): The FastAPI Application, The API Surface, apply, Auto-Redirect to Today Once Ready, check, draw, Five Readiness Rows in Plain Words, poll (+6 more)

### Community 69 - "test_advice_core.py"
Cohesion: 0.25
Nodes (10): _kind_of(), passages_for(), check_content(), _calculation(), test_check_content_keeps_a_sentence_stating_a_facts_value(), test_check_content_keeps_a_sentence_stating_a_figure(), test_check_content_keeps_a_sentence_stating_a_rules_value(), test_check_content_still_drops_a_sentence_stating_an_unprinted_number() (+2 more)

### Community 70 - "advice-consent.tsx"
Cohesion: 0.16
Nodes (18): AdviceNote(), Consent, ConsentPrompt(), agree(), settle(), State, ADR-0016, AdviceConsentSection() (+10 more)

### Community 71 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 72 - "gate.py"
Cohesion: 0.15
Nodes (9): check(), check_one(), precheck(), _says(), Verdict, test_a_sentence_citing_a_passage_that_was_never_retrieved_is_dropped(), test_a_sentence_with_no_supporting_passage_is_dropped(), test_no_passages_at_all_abstains() (+1 more)

### Community 73 - "Hybrid Retrieval: Dense Plus Full-Text"
Cohesion: 0.18
Nodes (5): bge-reranker-v2-m3 Cross-Encoder, 40 Down to 6, Hybrid Retrieval: Dense Plus Full-Text, Reciprocal Rank Fusion, k=60, The Household's Eleven Policies, The Validator Is the Handover Gate

### Community 74 - "scope.py"
Cohesion: 0.19
Nodes (9): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Person (+1 more)

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.17
Nodes (11): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), Telegram chat_id maps to a person, Possessive relations scope the question, before the cut to six, Naming exactly one person scopes to them (whole name, or a 3+ letter possessive unique to them) (+3 more)

### Community 76 - "FakeConn"
Cohesion: 0.11
Nodes (20): current(), grant(), _latest(), NoOwner, _record(), status(), withdraw(), FakeConn (+12 more)

### Community 77 - "sweep"
Cohesion: 0.18
Nodes (12): AlertConfig, sweep(), _triggered(), FakeConn, srs_row(), test_a_firing_older_than_the_debounce_window_fires_again(), test_a_metric_no_query_defines_cannot_fire(), test_a_recent_firing_is_debounced() (+4 more)

### Community 78 - "date"
Cohesion: 0.23
Nodes (9): document_row(), fact_row(), test_a_citation_that_resolves_to_nothing_still_says_what_it_said(), test_a_core_document_stays_enabled_when_every_pack_is_off(), test_an_alerts_citation_carries_the_document_it_opens(), test_one_document_is_shown_even_when_its_pack_is_off(), test_today_is_ordered_overdue_then_alerts_then_reminders(), test_vault_lists_documents_with_their_facts() (+1 more)

### Community 79 - "test_eval_harness.py"
Cohesion: 0.12
Nodes (20): Cited, reference_for(), Expected, load_set(), MalformedQuestion, Question, subset(), _answered() (+12 more)

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

### Community 85 - "api.ts"
Cohesion: 0.04
Nodes (62): ADR-0017, dynamic, metadata, PacksPage(), runtime, DocumentPage(), dynamic, metadata (+54 more)

### Community 86 - "validate.py"
Cohesion: 0.22
Nodes (5): main(), _read_rows(), _render(), _week_key(), _write()

### Community 87 - "ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.16
Nodes (18): ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel), Advice graph flow: shape match, subject resolution, consent, AdviceCard, explain, advice_records keeps each answer's full basis, PackManifest.advice shapes (gap, remaining_room, keep_or_surrender, compare_own, compare_market, estimate_saving), Advice.review: one question runs every shape at once, A grounding corpus lives at packs/<pack>/grounding/<corpus_id>/ (+10 more)

### Community 88 - "test_contracts.py"
Cohesion: 0.14
Nodes (23): _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact(), _field_not_on_every_doc_type(), _held_per_month() (+15 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "test_registration.py"
Cohesion: 0.29
Nodes (8): register_document(), conn(), database_url(), test_a_document_must_arrive_with_a_name(), test_a_new_document_is_inserted(), test_an_empty_payload_is_refused(), test_different_bytes_are_different_documents(), test_the_same_bytes_update_in_place_and_do_not_insert_a_second_row()

### Community 91 - "test_tax_pack.py"
Cohesion: 0.18
Nodes (12): _basis(), _latest(), _matched(), _published(), _register(), _shape(), test_a_tax_question_reaches_the_tax_shape_and_insurance_keeps_its_own(), test_no_saving_is_estimated_without_a_notice_of_assessment() (+4 more)

### Community 92 - "contracts.py"
Cohesion: 0.09
Nodes (19): Advice, Answering, Category, DocumentTypeSpec, Exclusions, FactInput, FieldSpec, Grounding (+11 more)

### Community 93 - "_answer_events"
Cohesion: 0.20
Nodes (5): ErrorEvent, _answer_events(), connection(), _settings(), _sse()

### Community 94 - "test_eval_report.py"
Cohesion: 0.12
Nodes (19): extraction_by_type(), extraction_f1(), FactRow, _outcomes(), _totals(), unjoined(), test_extraction_f1_scores_only_indexed_documents_against_the_register(), _rendered() (+11 more)

### Community 95 - "The Lim Household, Tampines"
Cohesion: 0.15
Nodes (10): loan_agreement Document Type, payslip Document Type, The Lim Household, Tampines, Household Canon Template, Rule of 78 Rebate and the 20 Per Cent Early Settlement Penalty, Motor Vehicle Hire Purchase Agreement Template, Republic of Xinkapow, the Invented Jurisdiction, Residential Housing Loan Facility Letter Template (+2 more)

### Community 96 - "ADR 0007 - The graph ships before retrieval and before a checkpoint table"
Cohesion: 0.22
Nodes (7): ADR 0007 - The graph ships before retrieval and before a checkpoint table, .graphifyignore excludes the corpus, The redacted real-document holdout, Dense-only retrieval stopgap, Hardware qualification, Rebuilding the vault's vectors, Lane B - Retrieval and evaluation

### Community 97 - "Lane C - Governance and assurance"
Cohesion: 0.13
Nodes (9): Data inventory and flow map, ISO/IEC 22989 to 5338 stage-to-process map, Lane C - Governance and assurance, Model card, Retention and erasure policy, Siew's generated task list, Golden Set B - hard negatives (25), The nine metrics and their targets (+1 more)

### Community 98 - "PackManifest"
Cohesion: 0.21
Nodes (8): PackManifest, _insurance(), test_a_grounding_corpus_is_named_by_id_not_by_path(), test_a_pack_cannot_opt_out_of_verdict_by_code(), test_a_pack_declaring_document_types_is_rejected(), test_a_shape_closed_by_an_unknown_category_is_rejected(), test_advice_naming_an_undeclared_catalogue_field_is_rejected_against_the_catalogue(), test_categories_reading_a_declared_field_validate()

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.10
Nodes (11): Generated Files Committed Alongside Their Source, benefit_illustration Document Type, birth_certificate Document Type, claim_letter Document Type, cpf_statement Document Type, Core Document Catalogue (ADR 0017), donation_receipt Document Type, identity_card Document Type (+3 more)

### Community 100 - "find_page"
Cohesion: 0.17
Nodes (10): _date_renderings(), find_page(), _normalise(), test_a_date_of_birth_printed_day_first_with_dashes_is_found(), test_a_date_on_no_page_still_has_no_page(), test_a_date_printed_in_other_common_notations_is_also_found(), test_a_value_is_attributed_to_the_page_it_is_printed_on(), test_a_value_on_no_page_has_no_page() (+2 more)

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
Cohesion: 0.06
Nodes (23): CrossEncoderReranker, device_name(), load(), passage_text(), relevance(), score_pairs(), _warn_once(), reranker_check() (+15 more)

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
Cohesion: 0.09
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

### Community 117 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 118 - "core/modules.py"
Cohesion: 0.18
Nodes (4): InstalledModule, manifest(), ModuleUnavailable, test_the_advice_module_manifest_loads()

### Community 121 - "TelegramCapture"
Cohesion: 0.13
Nodes (4): attribution(), broker_available(), dispatcher_for(), TelegramCapture

### Community 122 - "ModelUnavailable"
Cohesion: 0.13
Nodes (4): Generated, ModelUnavailable, constrained_stream(), constrained_stream()

### Community 123 - "_as_consent"
Cohesion: 0.13
Nodes (11): AdviceConsent, _as_consent(), advice_consents(), record_consent(), Clause A. Authority and Consent for Submissions on Behalf of Another Adult, Clause B. Purpose, Definitions, For review (+3 more)

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.17
Nodes (8): Task: benchmark the workstation and publish the numbers, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, Yew Mun's generated task list, Roadmap phase 1 - retrieval, PaperBrain hybrid retrieval (BM25 + dense, fused by RRF), Sample home contents insurance policy, Sample supermarket tax invoice

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

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
Nodes (40): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+32 more)

### Community 143 - "install_best_effort"
Cohesion: 0.33
Nodes (3): lifespan(), install_best_effort(), Installed

### Community 144 - "Settings"
Cohesion: 0.10
Nodes (34): Settings, client(), client_for(), consent(), ConsentConn, filed_document(), inbox(), settings() (+26 more)

### Community 145 - "schedule.py"
Cohesion: 0.18
Nodes (7): beat_schedule(), cron_expressions(), crontab_from(), manifest(), test_alert_is_swept_nightly_even_though_its_manifest_says_fact_write(), test_both_sweeps_are_scheduled_and_named_after_registered_tasks(), test_the_reminder_cron_is_read_from_its_manifest_not_written_twice()

### Community 146 - "PrivateCare Policy Wording Template"
Cohesion: 0.31
Nodes (9): PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Gemini prompt bank for identity specimens, The Lim household canon, Republic of Xinkapow (+1 more)

### Community 147 - "alert module manifest"
Cohesion: 0.28
Nodes (6): Days without recorded cover tile, alert_fpr, obligation_precision, Module manifest template, alert module manifest, reminder module manifest

### Community 148 - "is_first_person"
Cohesion: 0.20
Nodes (7): is_first_person(), relation_asked(), test_a_name_that_is_not_exactly_one_person_scopes_nothing(), test_a_named_household_member_wins_over_the_pronoun(), test_a_possessive_relation_names_whose_documents_are_asked_about(), test_first_person_questions_are_recognised(), test_questions_about_other_people_are_not_scoped()

### Community 149 - "same_value"
Cohesion: 0.25
Nodes (5): _as_date(), _as_number(), same_value(), value_forms(), test_same_value_normalises_dates_numbers_and_text()

### Community 150 - "next"
Cohesion: 0.15
Nodes (9): next, next-themes, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider() (+1 more)

### Community 151 - "The Grounding Gate"
Cohesion: 0.29
Nodes (7): The Core Answering Layer, The Answer Path: route, retrieve, rerank, ground, answer or abstain, The Grounding Gate, The Score Floor the Gate Reads, Kidney Stones: Inpatient Covered, Outpatient ESWL Excluded, Ask Screen, Try to Make It Lie: the Abstention Test

### Community 152 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 153 - "ADR 0008 - Ingestion runs on a Celery worker"
Cohesion: 0.39
Nodes (7): ADR 0005 - The watched folder is polled, not subscribed to, Stability debounce with injected time, ADR 0008 - Ingestion runs on a Celery worker, The ingestion worker, START.cmd launcher, Telegram capture, The watched inbox folder

### Community 154 - "unprinted_numbers"
Cohesion: 0.29
Nodes (5): _normal(), unprinted_numbers(), test_a_date_on_file_may_be_written_the_way_a_person_says_it(), test_a_leading_zero_does_not_make_a_printed_date_unprinted(), test_a_policy_number_is_kept_only_when_it_is_printed_whole()

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (6): Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "typing"
Cohesion: 0.07
Nodes (6): render(), _columns(), CorrectionRejected, Dispatcher, Send, ExtractedFact

### Community 158 - "Adversarial testing from week 7"
Cohesion: 0.25
Nodes (8): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Adversarial testing from week 7, Prompt injection carried inside a document, Scope attack: asking it to act, Task: run adversarial Set C and write up the findings, Adversarial Set C (15 questions that should not be answered), Golden Set C - adversarial (15)

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 162 - "_as_response"
Cohesion: 0.17
Nodes (7): AskRequest, AskResponse, Claim, _as_response(), ask(), ask_stream(), _history()

### Community 163 - "Cursor"
Cohesion: 0.25
Nodes (3): Cursor, cursor(), cursor()

### Community 164 - "send_retry"
Cohesion: 0.40
Nodes (3): RetryAccepted, retry_one(), send_retry()

### Community 165 - "PARROT evaluation harness"
Cohesion: 0.38
Nodes (7): abstention_rate, PARROT evaluation harness, Set A, answerable, Set B, hard negatives, Set C, adversarial, The golden question sets, must_cite_page from field_pages

### Community 166 - "RagasJudge"
Cohesion: 0.32
Nodes (5): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts()

### Community 167 - "The autonomy statement"
Cohesion: 0.29
Nodes (3): IMDA mappings and autonomy statement artefact, The facts table as an extension point, Roadmap phase 2 - facts

### Community 170 - "routes.py"
Cohesion: 0.13
Nodes (15): ModuleSummary, PacksResponse, PackSummary, PersonModel, VaultDocument, VaultFact, VaultResponse, _as_module_summary() (+7 more)

### Community 172 - "ADR index (0001-0018, with status)"
Cohesion: 0.09
Nodes (25): ADR 0001 - Record architecture decisions, ADR 0002 - One PostgreSQL instance for everything, Reciprocal rank fusion of dense and lexical, ADR 0003 - PaperBrain informs the pattern, not the module, PaperBrain prototype, ADR 0004 - Local setup can run before the assistant is ready, ADR 0006 - pypdfium2 renders the quarantine page images, ADR 0009 - next-themes and lucide-react are the only two web dependencies beyond the stack (+17 more)

### Community 174 - "Project skills"
Cohesion: 0.40
Nodes (4): Changing them, Project skills, Slash commands, Using them

### Community 175 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 176 - "_today_items"
Cohesion: 0.17
Nodes (8): Source, TodayItem, TodayResponse, _as_source(), today(), _cite(), _link(), _today_items()

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
Cohesion: 0.06
Nodes (33): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+25 more)

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
- **384 isolated node(s):** `Definitions`, `Clause A. Authority and Consent for Submissions on Behalf of Another Adult`, `Clause B. Purpose`, `Not yet written`, `For review` (+379 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1716 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **34 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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