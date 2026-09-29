# Graph Report - igd-capstone-2026  (2026-09-29)

## Corpus Check
- 304 files · ~700,291 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 37 file(s) not represented in the graph (top: (none) 15, .jsonl 7, .csv 5)

## Summary
- 4429 nodes · 10518 edges · 202 communities (171 shown, 25 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 1043 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a1953ef4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ScriptedOllama
- Passage
- test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them
- AnswerGraph
- DocumentCatalog
- advice/__init__.py
- Provenance register for corpus sg_protection_guidance
- test_advice_module.py
- test_eval_harness.py
- test_ingest_pipeline.py
- test_grounding_index.py
- test_worker_queue.py
- FolderAdapter
- test_telegram_capture.py
- connect
- run_parrot.py
- bench_runtime.py
- vault.py
- support.js
- checks.py
- ingest/extract.py
- test_grounding_values.py
- FakeConn
- registry.py
- answer.py
- SentenceScanner
- household.py
- ingest/reindex.py
- test_lifecycle.py
- score.py
- test_household.py
- .load
- ingest/quarantine.py
- test_hybrid.py
- test_eval_generate.py
- TelegramAdapter
- Registration
- Any
- reminder/__init__.py
- test_api.py
- alert/__init__.py
- Settings
- phrasings.py
- api.ts
- Ollama
- test_answer_graph.py
- test_gate.py
- _pages_from
- models.py
- HouseholdScope
- compilerOptions
- Any
- Any
- test_grounding.py
- main
- cli.py
- retry
- ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts
- ParsedPage
- Any
- answer.tsx
- values.py
- ConfigurationError
- lock.ts
- dependencies
- _as_event
- PARROT Interface Design Pack
- test_startup.py
- The Four Surfaces
- InstalledPack
- ADR index (0001-0018, with status)
- devDependencies
- sse
- Hybrid Retrieval: Dense Plus Full-Text
- scope.py
- ADR 0011: The household is people and aliases, and the owner is one of them
- FakeConn
- test_modules.py
- today/page.tsx
- tokens/page.tsx
- preview.tsx
- _as_module_summary
- Two-stage quarantine with a vision-language second pass
- pipeline.py
- build_router
- packs/page.tsx
- main
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- validate
- components.json
- item-row.tsx
- DatabaseUnavailable
- contracts.py
- ModelUnavailable
- ModuleAdviser
- The Lim Household, Tampines
- ADR 0007 - The graph ships before retrieval and before a checkpoint table
- Lane C - Governance and assurance
- test_contracts.py
- Core Document Catalogue (ADR 0017)
- export-design-preview.cjs
- ._categories_read_a_declared_field
- The five-lane split (five people, nine weeks, three builders)
- Data inventory: identity data, DOBs and loans
- test_scan_parse.py
- Roadmap phase 3 - reminders
- web/ - the PARROT interface
- The document register as ground truth
- validate.py
- .__init__
- Reminder, Alert and Tracker Registers
- Registrar
- example_pack template manifest
- FakeCursor
- find_page
- Running the evaluation harness
- _today_items
- HouseholdAdviceLog
- application
- register_document
- install_best_effort
- capture.py
- test_the_inventory_always_reads_core_documents
- ADR 0002 - One PostgreSQL instance for everything
- The deliberately naive retrieval baseline
- quiet_engine
- startup.py
- Filling the corpus register
- The case for synthetic evaluation data
- Writing a governance artefact
- routes.py
- The Grounding Gate
- advice-consent.tsx
- Two-Stage Quarantine With a Vision Second Pass
- Fill the Register Before Generating Documents
- Where Things Live
- Policy schedule HTML template
- Domain pack
- _graph_for
- PaperBrain
- Authoring a domain pack
- RagasJudge
- _as_consent
- scripts
- Integration review
- schedule.py
- PrivateCare Policy Wording Template
- alert module manifest
- Calculation
- Writing an ADR
- app/layout.tsx
- FakeCursor
- manifest
- START.cmd launcher
- send_retry
- DesignPreview evaluation harness
- build_team_tasks.py
- Project skills
- Adversarial testing from week 7
- pull_request_template.md
- ._compares_what_its_documents_declare
- Every Fact Row Cites Its Source
- base.py
- filesystem
- PARROT evaluation harness
- Due
- The autonomy statement
- sender
- test_the_batch_template_is_usable_exactly_as_generated
- test_an_unscoped_result_is_not_empty_for_the_owner
- test_the_catalogue_declares_metrics_that_exist
- Page one as plain Label: value lines
- find_browser_executable
- The synthetic-to-real gap
- test_rerank.py
- eslint.config.mjs
- One Database
- api/__init__.py
- grounding/__init__.py
- core/__init__.py
- runtime/__init__.py
- worker/__init__.py
- corpus/__init__.py
- eval/__init__.py
- modules/__init__.py
- packs/__init__.py
- Lane E - Corpus and adversarial testing
- No code generates corpus documents
- Alert
- setup.sh
- package.json
- postcss.config.mjs
- Lane C - Governance and assurance
- parrot
- Vertical slices, not layers
- Real organisations may be named

## God Nodes (most connected - your core abstractions)
1. `Settings` - 185 edges
2. `Passage` - 95 edges
3. `ScriptedOllama` - 87 edges
4. `InstalledPack` - 84 edges
5. `AnswerGraph` - 75 edges
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
- `The Corpus Is Synthetic and Committed` --semantically_similar_to--> `Corpus Batches Are Not in Git`  [AMBIGUOUS] [semantically similar]
  NOTICE.md → FIRST-RUN.md
- `One cell, one field` --semantically_similar_to--> `A field name is three things at once`  [INFERRED] [semantically similar]
  corpus/templates/policy_schedule.html → docs/PACK_AUTHORING.md

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

## Communities (202 total, 25 thin omitted)

### Community 0 - "ScriptedOllama"
Cohesion: 0.05
Nodes (80): AdviceCard, AdviceWithheld, _closes(), ConsentRequired, Finished, One sentence that has passed the gate, with the citations it passed on. It will…, Everything that is only knowable once the last sentence is in. `quarantined`…, Advice was asked for and the owner has not agreed to this pack's current… (+72 more)

### Community 1 - "Passage"
Cohesion: 0.07
Nodes (27): DenseRetriever, NoReranker, A dense-only retriever, so the graph can be run and tested before Lane B's…, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this…, Every number or identifier in a sentence that no cited passage prints. An…, unprinted_numbers(), The answer graph. Router, retrieve, rerank, grounding gate, then answer or…, Passage (+19 more)

### Community 2 - "test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them"
Cohesion: 0.25
Nodes (5): ClosingSpy, Wraps an event generator to record whether something called `.close()` on it,…, Starlette's own body iteration (`iterate_in_threadpool`) never calls `.close()`…, test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them(), spying()

### Community 3 - "AnswerGraph"
Cohesion: 0.10
Nodes (45): AnswerGraph, Declined, The pack's own decline, signed with its disclaimer, and a question it can…, A request for a recommendation or a judgement, declined before anything is…, Built once, asked many times. Holds no connection: retrieval does., The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting…, Scoped (+37 more)

### Community 4 - "DocumentCatalog"
Cohesion: 0.14
Nodes (23): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering…, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why the catalogue cannot supply `field` from every one of `doc_types`, or None., _class_name(), _docstring(), _field_line(), _header() (+15 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.07
Nodes (75): Figure, Input, One fact or rule value a calculation was built on, carrying its own citation.…, One number a calculator produced, and the words a sentence must use to state…, Hashable, _ambiguous(), _amount(), _band() (+67 more)

### Community 6 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.05
Nodes (65): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, MediShield Life (CPF Board), Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022 (+57 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.14
Nodes (53): FactRow, calculate(), assert_nothing_negative(), basis(), fact(), figures_of(), _gap_basis(), _held() (+45 more)

### Community 8 - "test_eval_harness.py"
Cohesion: 0.07
Nodes (43): Cited, One sentence and the passages it was traced to. What rule 3 looks like as data.…, Asks, Protocol, Ask PARROT the golden questions the way `scripts/ask.py` does, and keep what it…, The one method of `AnswerGraph` the harness uses. A test supplies a fake., The last question's contexts and candidate count, then a clean slate., Each question on its own thread, so no answer is a follow-up to the one before. (+35 more)

### Community 9 - "test_ingest_pipeline.py"
Cohesion: 0.10
Nodes (44): extract(), Never raises. A failure is a reason, and a reason routes the document to…, FakeOllama, insurance(), iras(), _page_of_examples(), Any, Exception (+36 more)

### Community 10 - "test_grounding_index.py"
Cohesion: 0.09
Nodes (41): CaptureFixture, GroundingCorpus, GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records…, Read and validate a pack's grounding corpus from its own folder on disk. A…, SourceText, index_pack(), IndexReport (+33 more)

### Community 11 - "test_worker_queue.py"
Cohesion: 0.10
Nodes (34): The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, sha256(), Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker. Celery is imported here rather…, Intake, What every capture channel hands a document to. An adapter's job ends at "these… (+26 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.15
Nodes (25): FolderAdapter, FolderSettings, Satisfies `CaptureAdapter`. Holds no database handle — it is given a…, FolderCapture, Begin watching. Returns False, with a logged reason, when it cannot., A daemon thread that polls the watched folder until `stop()` or process exit., FakeRegistrar, datetime (+17 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.12
Nodes (32): MockTransport, build(), FakeTelegram, photo_update(), Any, Path, Request, Response (+24 more)

### Community 14 - "connect"
Cohesion: 0.09
Nodes (46): queue(), The reportable line. Deliberately a rate and a count, because a rate over three…, What is waiting for a person's eyes, oldest first., Recovery, recovery_rate(), bytes_for(), digest_of_document(), Any (+38 more)

### Community 15 - "run_parrot.py"
Cohesion: 0.13
Nodes (24): _kill_tree(), main(), open_browser(), parse_args(), port_answers(), Any, Namespace, Popen (+16 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (34): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+26 more)

### Community 17 - "vault.py"
Cohesion: 0.07
Nodes (38): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+30 more)

### Community 18 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 19 - "checks.py"
Cohesion: 0.16
Nodes (21): The local API. Liveness is intentionally separate from assistant readiness.…, AsyncClient, asyncio, capture_check(), Check, collect_checks(), database_check(), interface_check() (+13 more)

### Community 20 - "ingest/extract.py"
Cohesion: 0.13
Nodes (23): DocumentTypeSpec, FieldSpec, One kind of document the core recognises., One extractable field. Its `name` is the column header in Desmond's register…, _coerce(), decode_schema(), _drop_format(), ExtractedFact (+15 more)

### Community 21 - "test_grounding_values.py"
Cohesion: 0.09
Nodes (56): extract_values(), parse_value(), The number a reported value states for its unit, or `None` when it states…, Every value the source prints for these keys, kept only when its passage prints…, Generated, The one client that talks to Ollama. Everything the platform infers goes…, LogCaptureFixture, _dropped() (+48 more)

### Community 22 - "FakeConn"
Cohesion: 0.08
Nodes (48): document_row(), fact_row(), FakeConn, obligation(), open_obligation(), overdue_row(), pack_row(), date (+40 more)

### Community 23 - "registry.py"
Cohesion: 0.10
Nodes (33): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders…, installed_modules(), InstalledModule, Load the installed capability modules at runtime. The mirror of…, Every module directory holding a `module.yaml`, in a stable order. Directories…, installed_packs(), Every pack directory holding a pack.yaml, in a stable order. Directories whose… (+25 more)

### Community 24 - "answer.py"
Cohesion: 0.04
Nodes (55): Claim, _advice_basis(), _advice_prompt(), answer_system(), _as_sentence(), _asked(), _citations(), _conversation() (+47 more)

### Community 25 - "SentenceScanner"
Cohesion: 0.09
Nodes (29): Any, Pulling finished sentences out of a JSON reply that is still being written. The…, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner (+21 more)

### Community 26 - "household.py"
Cohesion: 0.08
Nodes (47): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+39 more)

### Community 27 - "ingest/reindex.py"
Cohesion: 0.11
Nodes (14): pgvector accepts its own text form; this avoids registering an adapter for one…, _vector_literal(), indexed(), IndexedDocument, Any, RuntimeError, Rebuild a document's chunks and vectors without reading it again for facts.…, Safe to show: names what went wrong, never what the document says. (+6 more)

### Community 28 - "test_lifecycle.py"
Cohesion: 0.13
Nodes (26): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor.…, What the person asked for, once. The first request wins; later ones change…, _client(), _eventually(), _launcher(), parametrize, Path (+18 more)

### Community 29 - "score.py"
Cohesion: 0.06
Nodes (47): _as_date(), _as_number(), cites(), _contains(), doc_stem(), extraction_f1(), F1, FactRow (+39 more)

### Community 30 - "test_household.py"
Cohesion: 0.08
Nodes (46): is_first_person(), `(word, relation)` when the question asks about a relation's own documents,…, Whether this question is about the person asking. `other_names` are the display…, relation_asked(), _household_scope(), MonkeyPatch, parametrize, Person (+38 more)

### Community 31 - ".load"
Cohesion: 0.11
Nodes (33): create_app(), checks(), ready(), setup(), system_status(), _ollama_answering(), Any, MonkeyPatch (+25 more)

### Community 32 - "ingest/quarantine.py"
Cohesion: 0.09
Nodes (39): document_page(), page_images(), The second stage of quarantine: the page image, read by the vision-language…, Base64 page images, in page order. Empty when this document cannot be rendered.…, page_count(), PageUnavailable, _pdfium(), Any (+31 more)

### Community 33 - "test_hybrid.py"
Cohesion: 0.11
Nodes (22): hybrid_score(), identifiers(), prints(), Hybrid retrieval: pgvector cosine search and Postgres full-text search, fused…, The tokens in a question that look like something printed rather than said: a…, Whether the chunk prints the identifier, ignoring case and the spacing inside…, The cosine similarity, lifted to `IDENTIFIER_HIT` when the chunk prints an…, FakeConn (+14 more)

### Community 34 - "test_eval_generate.py"
Cohesion: 0.08
Nodes (43): _ambiguous(), choose(), Generated, hand_written(), main(), on_file(), pool(), Namespace (+35 more)

### Community 35 - "TelegramAdapter"
Cohesion: 0.14
Nodes (18): _attachment(), _pixels(), Any, Client, datetime, Response, The Telegram capture adapter. Same interface as the folder: `receive(payload,…, Confirm the token works before anything else is attempted. (+10 more)

### Community 36 - "Registration"
Cohesion: 0.12
Nodes (11): Dispatcher, Protocol, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Send, An already-indexed document is not read again. Re-reading it would burn a…, The row as it now stands, plus whether this call is the one that created it., Registration (+3 more)

### Community 37 - "Any"
Cohesion: 0.14
Nodes (17): Measurement, by_subject(), db(), FakeCursor, load_register(), Any, date, fixture (+9 more)

### Community 38 - "reminder/__init__.py"
Cohesion: 0.11
Nodes (24): already_said(), close(), current_lead(), next_window(), Overdue, Any, date, datetime (+16 more)

### Community 39 - "test_api.py"
Cohesion: 0.08
Nodes (44): Answer, Answered. Asking for consent and naming what is missing are endings, not…, advising(), client(), conn(), FakeGraph, graph(), _padded() (+36 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.19
Nodes (21): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), Any, date (+13 more)

### Community 41 - "Settings"
Cohesion: 0.10
Nodes (52): Whether Telegram capture should start. An unset token means "not this…, Settings, client_for(), consent(), ConsentConn, filed_document(), inbox(), parametrize (+44 more)

### Community 42 - "phrasings.py"
Cohesion: 0.20
Nodes (11): _keys(), LaneSpec, Row, How a question about a printed field is worded, per document type in…, One document type's wordings. `printed` and `spoken` each render the *thing* a…, Which register rows a lane's questions are drawn from. The task asks each…, A wording, or `None` when the row does not fill every field it needs., The spoken wording, or "Rachel's payslip" when the type has no product name of… (+3 more)

### Community 43 - "api.ts"
Cohesion: 0.08
Nodes (31): RELATION_CHOICES, Place, PLACES, SourcePanel(), DocumentDetail(), when(), Field(), format() (+23 more)

### Community 44 - "Ollama"
Cohesion: 0.11
Nodes (16): Ollama, Any, Client, A question, embedded the way the model was trained to embed a search query., Passages as `(title, text)`, embedded the way the model was trained to embed a…, Load the generator and the embedder now, and say where the generator landed. An…, Generate against a JSON schema. This is how extraction is held to a pack's…, The same constrained generation, yielded as it is written. Identical body to… (+8 more)

### Community 45 - "test_answer_graph.py"
Cohesion: 0.07
Nodes (44): Abstained, _either(), "a dental plan", or "a term life plan or a whole life plan". "An" only before…, build(), events(), passage(), Any, Exception (+36 more)

### Community 46 - "test_gate.py"
Cohesion: 0.07
Nodes (62): _kind_of(), passages_for(), `"fact:12"` -> `"fact"`, `"rule:7"` -> `"rule"`. Anything else is a calculator…, Inputs as kind fact/rule passages (chunk_id from the ref), and the figures as…, check(), check_advice(), check_content(), check_one() (+54 more)

### Community 47 - "_pages_from"
Cohesion: 0.24
Nodes (13): _kind(), _pages_from(), Group Docling's items by the page they were found on. Docling's markdown export…, Docling's label, reduced to the one distinction chunking needs: is this a…, A table as lines of text, one row per line: `label: value` when a row has two…, _table_text(), SimpleNamespace, _cell() (+5 more)

### Community 48 - "models.py"
Cohesion: 0.10
Nodes (31): AdviceCardEvent, CloseRequest, ConfirmNameRequest, ConsentRequest, CorrectionRequest, DeclinedEvent, EnabledRequest, ErrorEvent (+23 more)

### Community 49 - "HouseholdScope"
Cohesion: 0.14
Nodes (20): HouseholdScope, Any, Keep the owner's passages and the household's; set aside everybody else's. A…, Keep the passages of these people and of the household; set aside everybody…, What `AnswerGraph` is handed so it can scope without holding a connection.…, scope_passages(), scope_to(), _conn_returning() (+12 more)

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 51 - "Any"
Cohesion: 0.13
Nodes (7): ConsentCursor, Fails, FakeCursor, Any, The parameters of the one statement containing `needle`. Fails loudly if it…, Yields `before`, then raises. `ask` raises at once., Remembers what `grant` or `withdraw` inserted, so the next read of the latest…

### Community 52 - "Any"
Cohesion: 0.26
Nodes (15): _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact(), _field_not_on_every_doc_type(), _held_per_month() (+7 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.21
Nodes (21): corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError, A pack's grounding corpus on disk does not match what its `sources.yaml`…, Where this pack's grounding corpus lives on disk, or `None` if it declares none., Read, validate and hash every source this pack's corpus records. Raises… (+13 more)

### Community 54 - "main"
Cohesion: 0.13
Nodes (26): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), main(), _note() (+18 more)

### Community 55 - "cli.py"
Cohesion: 0.05
Nodes (75): ArgumentParser, Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a…, ndarray, answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The… (+67 more)

### Community 56 - "retry"
Cohesion: 0.16
Nodes (15): blocked_reasons(), forget(), Any, Path, ValueError, QuarantinedDocument, Per document: `None` when the image pass can run, or the sentence saying why it…, Safe to show. Forgetting a document whose file is still there would not last. (+7 more)

### Community 57 - "ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.33
Nodes (9): guardrails.abstain_below was calibrated on un-prompted scores, ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts, chunks.tsv built from context_prefix || text, Context prefix: title - type - heading - page, rag_probe2 before/after similarity table (six policies, 13 September), scripts/reindex.py rebuilds chunks and vectors, Chunks follow the document's structure (Docling heading labels), Task prompts: embed_query and embed_documents (+1 more)

### Community 58 - "ParsedPage"
Cohesion: 0.08
Nodes (28): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, One flat list of chunks, ordinal running across the whole document., The page as `(is_heading, line)`, from the parser's structure when it has any. (+20 more)

### Community 59 - "Any"
Cohesion: 0.10
Nodes (24): advised_pack(), db(), _document(), _facts_tuple(), FakeConn, FakeCursor, Any, date (+16 more)

### Community 60 - "answer.tsx"
Cohesion: 0.06
Nodes (36): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+28 more)

### Community 61 - "values.py"
Cohesion: 0.08
Nodes (31): _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), number_tokens(), _pack(), printed_as() (+23 more)

### Community 62 - "ConfigurationError"
Cohesion: 0.12
Nodes (22): _chat_ids(), ConfigurationError, _flag(), _folder(), local_url(), _port(), _positive(), Path (+14 more)

### Community 63 - "lock.ts"
Cohesion: 0.08
Nodes (45): dynamic, GET(), grant(), POST(), runtime, ALLOWED, Context, DELETE() (+37 more)

### Community 64 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 65 - "_as_event"
Cohesion: 0.15
Nodes (16): AbstentionEvent, AdviceFigure, AdviceWithheldEvent, ConsentRequiredEvent, FinishedEvent, Advice was asked for before the owner agreed to this pack's current consent…, Advice could not be worked out. `missing` names each fact or rule it needed, in…, One number a calculator produced, already printed the way the verdict prints it. (+8 more)

### Community 66 - "PARROT Interface Design Pack"
Cohesion: 0.09
Nodes (29): Not finding you is an answer (first-person abstention), Capture is where the user already is, Citation chips are the trust surface, Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Nothing moves without a reason (motion specification), Silence beats a guess (+21 more)

### Community 67 - "test_startup.py"
Cohesion: 0.10
Nodes (28): main(), Path, Local-only startup preflight, using the standard library so setup can be…, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file…, report_hardware(), startup_gaps(), prepare_checkout() (+20 more)

### Community 68 - "The Four Surfaces"
Cohesion: 0.13
Nodes (16): Packs and Modules May Not Import web/ or api/, The FastAPI Application, The API Surface, GET /api/today Never Marks Anything Notified, apply, Auto-Redirect to Today Once Ready, check, draw (+8 more)

### Community 69 - "InstalledPack"
Cohesion: 0.07
Nodes (53): Categories, holdings(), HouseholdInventory, Any, The documents on file, read from `facts` rather than searched for. "Do I have…, Handed to `AnswerGraph` by whoever holds a connection, as `HouseholdScope` is., Rows of `INVENTORY`, one holding per document that prints the field an enabled…, Asked (+45 more)

### Community 70 - "ADR index (0001-0018, with status)"
Cohesion: 0.09
Nodes (32): ADR 0006 - pypdfium2 renders the quarantine page images, ADR 0009 - next-themes and lucide-react are the only two web dependencies beyond the stack, Schedule-table questions remain weak (rank 2-4), ADR 0013: A question is understood before it is searched, and scoped before it is cut, The answer prompt carries today's date and names the scoped relation as who the question is about, AskRequest.history carries up to twelve earlier turns, A relevance-grading call and an 'answerable' schema flag were both dropped, Remaining failures are retrieval's to fix (cross-encoder plus lexical) (+24 more)

### Community 71 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 72 - "sse"
Cohesion: 0.10
Nodes (35): Citation, A passage, named the way a person cites it and identified the way a link needs.…, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed…, Reading, a_citation(), advice_card(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order. (+27 more)

### Community 73 - "Hybrid Retrieval: Dense Plus Full-Text"
Cohesion: 0.18
Nodes (11): No New Runtime Dependency Without an ADR, Never Generate SQL at Runtime, baseline.py Is Disposable and Never a Measurement, ports.py, the Seam With Lane B, bge-reranker-v2-m3 Cross-Encoder, 40 Down to 6, Hybrid Retrieval: Dense Plus Full-Text, Reciprocal Rank Fusion, k=60, The Household's Eleven Policies (+3 more)

### Community 74 - "scope.py"
Cohesion: 0.23
Nodes (16): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Whose question is this, and whose documents may answer it. "What is my term… (+8 more)

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.17
Nodes (19): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), The owner is a row, not a config value baked at install, people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), A resolved person is shown as a chip, like a citation, The roster is derived from documents, then confirmed (+11 more)

### Community 76 - "FakeConn"
Cohesion: 0.07
Nodes (35): Channel, current(), grant(), HouseholdConsents, _latest(), NoOwner, Any, RuntimeError (+27 more)

### Community 77 - "test_modules.py"
Cohesion: 0.15
Nodes (28): AlertConfig, Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), Everything inside a lead window that has not already been said for that window.…, sweep(), FakeConn, obligation_row(), datetime (+20 more)

### Community 78 - "today/page.tsx"
Cohesion: 0.08
Nodes (24): dynamic, HouseholdPage(), metadata, runtime, AppLayout(), dynamic, isUrgent(), metadata (+16 more)

### Community 79 - "tokens/page.tsx"
Cohesion: 0.05
Nodes (34): lucide-react, react, dynamic, runtime, Motion(), ROWS, INKS, metadata (+26 more)

### Community 80 - "preview.tsx"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 81 - "_as_module_summary"
Cohesion: 0.20
Nodes (10): ModuleSummary, PacksResponse, PackSummary, _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack() (+2 more)

### Community 82 - "Two-stage quarantine with a vision-language second pass"
Cohesion: 0.12
Nodes (19): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Two-stage quarantine with a vision-language second pass, Batch 4: the deliberately hard documents, A full policy wording registers as policy_schedule, Task: review every quarantined document and label the failure, Task: sign off the capture-to-database path against the data inventory, Measurement is owned separately from the engine (+11 more)

### Community 83 - "pipeline.py"
Cohesion: 0.09
Nodes (28): Chunk, What is actually embedded: the prefix plus the text, matching the tsvector…, What happens to a document between "these bytes are registered" and "this…, The ingestion worker. Capture registers a document; this package turns it into…, fixed(), from_facts(), _label(), Any (+20 more)

### Community 84 - "build_router"
Cohesion: 0.11
Nodes (29): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, What changed, in the words the screen confirms it with. `was` is returned…, The row is gone from Today. `speaks_again` is null when it will not come back.…, A name off a document that nobody has placed yet, and what the model thinks it… (+21 more)

### Community 85 - "packs/page.tsx"
Cohesion: 0.06
Nodes (29): ADR-0017, next, dynamic, metadata, PacksPage(), runtime, DocumentPage(), dynamic (+21 more)

### Community 86 - "main"
Cohesion: 0.12
Nodes (24): approve(), pending(), PendingValue, Any, date, A person's approval, standing between a model's extraction and any calculator…, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it. (+16 more)

### Community 87 - "ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.11
Nodes (27): Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration), Published guidance is a second evidence lane, never a second household, Every passage carries a kind: document, inventory or guidance, ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, The adult rule: advice is withheld for a person under 21 or a child with no date of birth on file, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel) (+19 more)

### Community 88 - "validate"
Cohesion: 0.20
Nodes (23): validate(), Path, The register is the evaluation ground truth. These are the checks that keep it…, A register in the old shape is full of ground truth, so "no fields" would be a…, Without it a golden-set question cannot say which page its answer is printed on., Otherwise the golden question cites a page for a value that is not in the…, Pages are 1-based because that is how a person reads a citation off a chip., The contract between `packs.build` and this validator, asserted rather than… (+15 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "item-row.tsx"
Cohesion: 0.16
Nodes (13): SourceChip(), stripTrailingPage(), ADR-0016, countdown(), detail(), figure(), ItemRow(), longDate() (+5 more)

### Community 91 - "DatabaseUnavailable"
Cohesion: 0.13
Nodes (19): enabled_pack_ids(), enabled_packs(), The packs left switched on, plus `core`, or `None` when nothing has been…, The installed packs a person has left switched on, as loaded pack objects. This…, HybridRetriever, Implements `core.graph.ports.Retriever`. Built where the connection is, like…, Lane B: hybrid retrieval. `HybridRetriever` implements…, DatabaseUnavailable (+11 more)

### Community 92 - "contracts.py"
Cohesion: 0.13
Nodes (23): Advice, Answering, Category, Exclusions, Grounding, Guardrails, ModuleTrigger, Persona (+15 more)

### Community 93 - "ModelUnavailable"
Cohesion: 0.10
Nodes (20): Classification, classify(), _prompt(), Never raises. An unavailable model is a classification failure, so it…, _schema(), document_types(), doc_type -> spec. The classifier's whole candidate list, from the catalogue…, ModelUnavailable (+12 more)

### Community 94 - "ModuleAdviser"
Cohesion: 0.11
Nodes (21): FactInput, A printed fact a calculator reads, named by where it is printed rather than…, _fact(), facts_for(), _is_an_adviser(), long_date(), ModuleAdviser, names_for() (+13 more)

### Community 95 - "The Lim Household, Tampines"
Cohesion: 0.15
Nodes (16): loan_agreement Document Type, payslip Document Type, The Lim Household, Tampines, One Household Only; the Persona Sketches Are Gone, Rachel Ng Arrives Off Documents, Not a Persona Sketch, Household Canon Template, Three Surnames, One Household, doc_id Is the Filename (+8 more)

### Community 96 - "ADR 0007 - The graph ships before retrieval and before a checkpoint table"
Cohesion: 0.16
Nodes (14): ADR 0004 - Local setup can run before the assistant is ready, ADR 0007 - The graph ships before retrieval and before a checkpoint table, Retrieval is a port, not an import, .graphifyignore excludes the corpus, Scoping happens after retrieval, and that has a ceiling, The redacted real-document holdout, Dense-only retrieval stopgap, Hardware qualification (+6 more)

### Community 97 - "Lane C - Governance and assurance"
Cohesion: 0.13
Nodes (16): The evaluation is the gate, Data inventory and flow map, ISO/IEC 22989 to 5338 stage-to-process map, Lane C - Governance and assurance, Model card, Retention and erasure policy, Say unverified rather than write a plausible sentence, Siew's generated task list (+8 more)

### Community 98 - "test_contracts.py"
Cohesion: 0.08
Nodes (48): PackManifest, A domain pack, authored as one YAML file: grounding, persona, answering and…, _advised(), _checked(), _insurance(), _market(), _market_compares_an_undeclared_field(), parametrize (+40 more)

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.10
Nodes (21): The Purely Additive Migration Exception, Contracts and Migrations Are Their Own PR, Sources of Truth Generate Their Outputs, Snooze Means Not Until This Gets More Urgent, The Three Things Agents Get Wrong Here, Generated Files Committed Alongside Their Source, benefit_illustration Document Type, birth_certificate Document Type (+13 more)

### Community 100 - "export-design-preview.cjs"
Cohesion: 0.11
Nodes (17): bundle(), classes, css, cssFile, domId, fs, ids, licences (+9 more)

### Community 101 - "._categories_read_a_declared_field"
Cohesion: 0.33
Nodes (3): Whether any document type in the catalogue declares `field`., An advice shape that names a missing role or key fails at load time. Caught…, model_validator

### Community 102 - "The five-lane split (five people, nine weeks, three builders)"
Cohesion: 0.09
Nodes (30): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The domain pack manifest, The expansion model: two axes, not one list, The golden set: answerable, hard negatives, adversarial, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build (+22 more)

### Community 103 - "Data inventory: identity data, DOBs and loans"
Cohesion: 0.17
Nodes (15): Data inventory: identity data, DOBs and loans, The lock is a screen lock, not encryption, next dev binds every interface, not loopback, Telegram capture route and delete-at-source, What crosses a boundary, Governance artefact set, Write unverified rather than assert, The final ILP report (+7 more)

### Community 104 - "test_scan_parse.py"
Cohesion: 0.12
Nodes (18): DoclingParser, Docling, held at arm's length: imported on first use, and never at module…, FixtureRequest, Image, needs_ocr, _as_printed(), page_pixels(), photographed() (+10 more)

### Community 105 - "Roadmap phase 3 - reminders"
Cohesion: 0.14
Nodes (15): The answer graph: router, retrieve, rerank, grounding gate, Capability modules: Reminder and Alert, Task: build the answer graph with the grounding gate, Contradiction attack, Task: contextualised chunking and the reranker, Task: hybrid retrieval with reciprocal rank fusion, The reminders table as an extension point, Roadmap phase 3 - reminders (+7 more)

### Community 106 - "web/ - the PARROT interface"
Cohesion: 0.14
Nodes (15): Task: complete the Insurance Agent pack, ADR 0017 - a pack is grounding and persona, Lock the design tokens before building any screen, The four surfaces: Today, Ask, Vault, Packs, Lane D - Domain packs and interface, The platform argument: one core, two domains, Task: define the pack catalogue - the nine deferred packs, Zee's generated task list (+7 more)

### Community 107 - "The document register as ground truth"
Cohesion: 0.18
Nodes (15): batch0-personas is deleted and must not be recreated, python -m corpus.validate, The document register as ground truth, The whole-life expiry_date mismatch, Register column headings are generated, not chosen, The household canon (the Lims of Tampines), Register first, documents second, Task: spot-check 20 register rows against the extractor (+7 more)

### Community 108 - "validate.py"
Cohesion: 0.12
Nodes (16): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+8 more)

### Community 109 - ".__init__"
Cohesion: 0.14
Nodes (9): AdviceLog, ConsentBook, Protocol, Implemented by `HouseholdConsents` in `core/advice_consent.py`., The granting row's id, or `None` when the owner has not granted this exact…, Implemented by `HouseholdAdviceLog` in `core/advice_records.py`., Routing and evidence. The answering is not a node — it yields, and a node…, Inventory (+1 more)

### Community 110 - "Reminder, Alert and Tracker Registers"
Cohesion: 0.18
Nodes (15): Passport Uses date_of_expiry So policy_expiry Does Not Fire, filing_deadline Reminder, maturity_date Is Not expiry_date, passport Document Type, passport_expiry Reminder, policy_expiry Reminder, policy_schedule Document Type, Reminder, Alert and Tracker Registers (+7 more)

### Community 111 - "Registrar"
Cohesion: 0.17
Nodes (7): Cursor, Any, Protocol, What a capture adapter is handed. It does not know psycopg exists., Registrar, cursor(), cursor()

### Community 112 - "example_pack template manifest"
Cohesion: 0.18
Nodes (14): I explain the renewal notice, I do not renew policies, Autonomy statement, ISO/IEC 22989 stages versus 5338 processes, never_acts as a machine-checked flag, Grounding corpora now live inside packs, advice module manifest, example_pack template manifest, example_room advice shape (+6 more)

### Community 113 - "FakeCursor"
Cohesion: 0.18
Nodes (3): FakeCursor, Any, FakeConn

### Community 114 - "find_page"
Cohesion: 0.17
Nodes (12): _date_renderings(), find_page(), _normalise(), The first page whose text contains this value. None means no page supports it.…, Every common way a household document prints this date, given it as YYYY-MM-DD.…, test_a_date_of_birth_printed_day_first_with_dashes_is_found(), test_a_date_on_no_page_still_has_no_page(), test_a_date_printed_in_other_common_notations_is_also_found() (+4 more)

### Community 115 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 116 - "_today_items"
Cohesion: 0.21
Nodes (13): A document and a page, as a person would cite it — or, for published guidance,…, Source, TodayItem, _as_source(), _cite(), _link(), date, Split a formatted citation back into its parts, keeping the text either way.… (+5 more)

### Community 117 - "HouseholdAdviceLog"
Cohesion: 0.25
Nodes (7): HouseholdAdviceLog, The record of every advised or withheld answer (ADR 0016). `advice_records`…, `core.graph.advice.AdviceLog` over a live connection. `basis` is dumped with…, AdviceRecord, Every advised or withheld answer's full basis, so it can be reconstructed later…, test_record_insert_includes_the_sha256_of_the_disclaimer(), Log

### Community 118 - "application"
Cohesion: 0.22
Nodes (14): application(), The configured application with its tasks registered. One per process., _beat_needs_its_own_process(), celery_argv(), main(), Any, Namespace, Popen (+6 more)

### Community 119 - "register_document"
Cohesion: 0.29
Nodes (12): Insert or update the `documents` row for these bytes and say which happened.…, register_document(), conn(), database_url(), Any, fixture, The idempotent upsert, against the real unique index. `documents.sha256 UNIQUE`…, test_a_document_must_arrive_with_a_name() (+4 more)

### Community 120 - "install_best_effort"
Cohesion: 0.33
Nodes (5): lifespan(), install_best_effort(), Installed, What `install` did, so a startup line can say it in one sentence., Install at startup without being able to stop startup. Both processes that own…

### Community 121 - "capture.py"
Cohesion: 0.08
Nodes (25): BaseTransport, RuntimeError, Safe to show: never contains the token., TelegramSettings, TelegramUnavailable, Inline, Run the pipeline here and now, and report what it decided., attribution() (+17 more)

### Community 122 - "test_the_inventory_always_reads_core_documents"
Cohesion: 0.22
Nodes (6): _Answering, The event stream one request is sending, held where the request's cleanup can…, Close the answer stream when the request ends, whatever ended it. Requires…, Conn, ADR 0017: a document is the core's, so the query includes `core` whatever is…, test_the_inventory_always_reads_core_documents()

### Community 123 - "ADR 0002 - One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (7): ADR 0001 - Record architecture decisions, ADR 0002 - One PostgreSQL instance for everything, Reciprocal rank fusion of dense and lexical, ADR 0003 - PaperBrain informs the pattern, not the module, PaperBrain prototype, Contracts before code, Lane A - Integration and product

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.17
Nodes (12): Task: benchmark the workstation and publish the numbers, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, The deliberately naive retrieval baseline, Committed runs are never deleted, Yew Mun's generated task list, Hybrid retrieval, not embeddings alone, Chunking respects paragraphs (+4 more)

### Community 125 - "quiet_engine"
Cohesion: 0.50
Nodes (4): fixture, MonkeyPatch, quiet_engine(), No real probes, no startup writes, no deliberate pause before exiting. The…

### Community 126 - "startup.py"
Cohesion: 0.22
Nodes (7): ModelWarmth, The page a person sees while Parrot starts, served by the engine itself. **Why…, Whether the generator has been loaded yet, and where it landed. Written by one…, Load the generator and the embedder before the first question, and record the…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), warm_models()

### Community 127 - "Filling the corpus register"
Cohesion: 0.20
Nodes (9): Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one, The rule that cannot bend (+1 more)

### Community 128 - "The case for synthetic evaluation data"
Cohesion: 0.18
Nodes (11): Qwen-SEA-LION-v4-4B-VL extraction ceiling, Register first, then generate, SYNTHETIC DOCUMENT footer, Ground truth for free, The 40-document holdout corpus, The case for synthetic evaluation data, Two withdrawn synthetic-data controls, extraction_f1 (+3 more)

### Community 129 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (9): Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six, Where governance touches the code (+1 more)

### Community 130 - "routes.py"
Cohesion: 0.19
Nodes (14): PersonModel, VaultDocument, VaultFact, VaultResponse, _as_person(), _as_vault_document(), vault_documents(), connection() (+6 more)

### Community 131 - "The Grounding Gate"
Cohesion: 0.29
Nodes (8): never_acts: True in Every Pack Manifest, The Core Answering Layer, The Answer Path: route, retrieve, rerank, ground, answer or abstain, The Grounding Gate, The Score Floor the Gate Reads, Kidney Stones: Inpatient Covered, Outpatient ESWL Excluded, Ask Screen, Try to Make It Lie: the Abstention Test

### Community 132 - "advice-consent.tsx"
Cohesion: 0.16
Nodes (18): AdviceNote(), Consent, ConsentPrompt(), agree(), settle(), State, ADR-0016, AdviceConsentSection() (+10 more)

### Community 133 - "Two-Stage Quarantine With a Vision Second Pass"
Cohesion: 0.15
Nodes (14): Amend the Graph Refresh Into the Commit, Qwen-SEA-LION-v4-4B-VL Generator, No CORS Middleware, Deliberately, Generation Model Swapped to Fit One 8 GB Card, Week 1 Entry, 2-8 Sep 2026, Week 2 Entry, 9-15 Sep 2026, Capture Channels Are Transports, receive(payload, mime, sender, ts, *, original_name) (+6 more)

### Community 134 - "Fill the Register Before Generating Documents"
Cohesion: 0.20
Nodes (10): Definition of Done, No Claim Without a Citation, Every Response That States Something Carries Its Source, Citation Names Resolved Once Per Response, Slash Commands: orient, check, handover, weekly, One Vertical Slice Per Pull Request, field_pages Is a Second Pass Over the Register, Fill the Register Before Generating Documents (+2 more)

### Community 135 - "Where Things Live"
Cohesion: 0.10
Nodes (25): Working Agreement for Coding Agents, The Five Lanes and Their Owners, The Contribution Loop, One cell, one field, Policy Schedule Template, Renewal Notice Template, ADR 0010 - main is unprotected, and the discipline is human, Amend the graph refresh into the commit (+17 more)

### Community 136 - "Policy schedule HTML template"
Cohesion: 0.24
Nodes (10): b1-0001 Private Car Insurance Policy Schedule, b1-0002 HomeShelter Contents Policy Schedule, b1-0003 Hospital Income Protection Plan Schedule, Full-length insurance policy notebook prompt, No Ref: line anywhere on the document, Cross-document corpus consistency, Four full-policy notebook prompts, Shared policy-drafting preamble (+2 more)

### Community 137 - "Domain pack"
Cohesion: 0.12
Nodes (21): The demonstration run sheet, Step 8 - switch a pack off, Step 6 - the abstention, Step 7 - the refusal to act, Step 2 - the source chip, Derive the roster, then confirm it, Exactly one owner, enforced by the database, facts.subject is never normalised (+13 more)

### Community 138 - "_graph_for"
Cohesion: 0.17
Nodes (13): AskRequest, AskResponse, Claim, The whole answer, once. `text` is the consent wording when `kind` is…, One sentence and the passages it was traced to. Never emitted without…, _as_response(), ask(), ask_stream() (+5 more)

### Community 139 - "PaperBrain"
Cohesion: 0.20
Nodes (10): The code pass of the knowledge graph, Nobody edits core/contracts.py in a feature pull request, Lane A - Integration and product, The semantic pass of the knowledge graph, Triage prompt: four buckets, no code written, Ninety protected minutes a week of integration, Christian's generated task list, PaperBrain (+2 more)

### Community 140 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 141 - "RagasJudge"
Cohesion: 0.32
Nodes (6): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts(), Ragas 0.4 metrics through Ollama's OpenAI-compatible endpoint. Imported lazily…

### Community 142 - "_as_consent"
Cohesion: 0.29
Nodes (7): AdviceConsent, AdviceConsent, One advising pack, the wording a person is asked to agree to, and what the…, _as_consent(), advice_consents(), record_consent(), One advising pack's consent wording and the owner's standing answer to it.

### Community 143 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 144 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 145 - "schedule.py"
Cohesion: 0.15
Nodes (17): build(), Any, The one Celery application, built from `Settings`. Every setting here is a…, Construct the Celery application. Imported lazily by callers so that nothing…, beat_schedule(), cron_expressions(), crontab_from(), manifest() (+9 more)

### Community 146 - "PrivateCare Policy Wording Template"
Cohesion: 0.31
Nodes (9): PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Gemini prompt bank for identity specimens, The Lim household canon, Republic of Xinkapow (+1 more)

### Community 147 - "alert module manifest"
Cohesion: 0.28
Nodes (9): Days without recorded cover tile, alert_fpr, obligation_precision, Module manifest template, Quoted "on" key in YAML 1.1, alert module manifest, Modules read typed rows, never chunks, reminder module manifest (+1 more)

### Community 148 - "Calculation"
Cohesion: 0.14
Nodes (18): AdviceShape, One kind of advice question, and everything its calculator needs to answer it., Adviser, Calculation, Missing, date, What a calculator returns, and what the graph needs to ask consent and keep a…, What a calculator returns when every fact and rule it needed was on file and… (+10 more)

### Community 149 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 150 - "app/layout.tsx"
Cohesion: 0.22
Nodes (7): next-themes, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 152 - "manifest"
Cohesion: 0.33
Nodes (6): manifest(), ModuleUnavailable, RuntimeError, A module's YAML is missing, or does not validate against `ModuleManifest`., One module's manifest, validated. Raises rather than returning a partial object., test_the_advice_module_manifest_loads()

### Community 153 - "START.cmd launcher"
Cohesion: 0.39
Nodes (8): ADR 0005 - The watched folder is polled, not subscribed to, Stability debounce with injected time, ADR 0008 - Ingestion runs on a Celery worker, The queue carries a digest, not the document, The ingestion worker, START.cmd launcher, Telegram capture, The watched inbox folder

### Community 154 - "send_retry"
Cohesion: 0.40
Nodes (5): 202. The vision pass is slower than a page load, so it is queued and this is…, RetryAccepted, retry_one(), Put one quarantine retry on the queue and return its task id. The vision pass…, send_retry()

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (8): parrot-sweep shimmer animation, Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, An answer with the page it came from, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "build_team_tasks.py"
Cohesion: 0.39
Nodes (7): main(), Path, Generate each member's task list from the master task CSV. python…, _read_rows(), _render(), _week_key(), _write()

### Community 157 - "Project skills"
Cohesion: 0.40
Nodes (4): Changing them, Project skills, Slash commands, Using them

### Community 158 - "Adversarial testing from week 7"
Cohesion: 0.25
Nodes (8): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Adversarial testing from week 7, Prompt injection carried inside a document, Scope attack: asking it to act, Task: run adversarial Set C and write up the findings, Adversarial Set C (15 questions that should not be answered), Golden Set C - adversarial (15)

### Community 159 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 161 - "Every Fact Row Cites Its Source"
Cohesion: 0.33
Nodes (7): Every Fact Row Cites Its Source, A Correction Cannot Invent a Row, Every Node Writes One Line to traces, The Ingestion Pipeline, The Pipeline Forks Into Retrieval and Facts Lanes, Numbers Come From Postgres, Never From the Model, macOS Worker Runs Celery Solo

### Community 163 - "base.py"
Cohesion: 0.10
Nodes (20): CaptureAdapter, IngestJob, datetime, Protocol, The one interface every capture channel satisfies. receive(payload, mime,…, Magic bytes first, filename suffix second, `application/octet-stream` last. A…, What a capture returns: a registered document, and whether we had seen it…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call. (+12 more)

### Community 164 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 165 - "PARROT evaluation harness"
Cohesion: 0.38
Nodes (7): abstention_rate, PARROT evaluation harness, Set A, answerable, Set B, hard negatives, Set C, adversarial, The golden question sets, must_cite_page from field_pages

### Community 167 - "The autonomy statement"
Cohesion: 0.29
Nodes (7): The autonomy statement, Governance claims traced to enforcement points, IMDA mappings and autonomy statement artefact, The facts table as an extension point, Constraint: fully offline, Explicitly not doing: cloud, hosted vectors, autonomous spending, Roadmap phase 2 - facts

### Community 173 - "Page one as plain Label: value lines"
Cohesion: 0.33
Nodes (6): Appendicitis entitlement demonstration, Page one as plain Label: value lines, Ward and hospital entitlement clause, Answering: vocabulary, categories, exclusions, The four tests every field must pass, policy_type was judged, not printed

### Community 174 - "find_browser_executable"
Cohesion: 0.47
Nodes (5): find_browser_executable(), generate_documents(), Path, Project Parrot - Synthetic Document Generator for Lim Household…, Find Microsoft Edge or Google Chrome executable on Windows.

### Community 179 - "The synthetic-to-real gap"
Cohesion: 0.40
Nodes (5): The 40-document redacted holdout, The synthetic-to-real gap, Consent and redaction protocol, Task: write the PDPA position on using synthetic data, Task: evaluation run 3 plus the holdout run

### Community 185 - "test_rerank.py"
Cohesion: 0.11
Nodes (24): CrossEncoderReranker, device_name(), load(), passage_text(), Any, The cross-encoder reranker: forty candidates read against the question, six…, What the reranker reads: the one-line context, when a chunk carries one, then…, Implements `core.graph.ports.Reranker`. Reorders by the cross-encoder's score… (+16 more)

### Community 186 - "eslint.config.mjs"
Cohesion: 0.50
Nodes (3): @eslint/eslintrc, compat, eslintConfig

### Community 201 - "Alert"
Cohesion: 0.25
Nodes (5): Alert, What the debounce is keyed on: this metric, for this person and thing, in this…, Two lapsed policies on one person are two alerts, and saying one must not…, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

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
- **356 isolated node(s):** `npx`, `@modelcontextprotocol/server-filesystem`, `_Formatter`, `parrot`, `setup.sh script` (+351 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1597 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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