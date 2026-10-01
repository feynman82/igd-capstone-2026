# Graph Report - igd-capstone-2026  (2026-10-01)

## Corpus Check
- 311 files · ~709,256 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 38 file(s) not represented in the graph (top: (none) 15, .jsonl 7, .csv 5)

## Summary
- 4692 nodes · 11566 edges · 207 communities (176 shown, 25 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1063 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f47e3430`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ModelUnavailable
- test_hybrid.py
- ScriptedOllama
- test_answer_graph.py
- validate
- Input
- Provenance register for corpus sg_protection_guidance
- test_advice_module.py
- checks.py
- test_ingest_pipeline.py
- test_grounding_index.py
- test_worker_queue.py
- FolderAdapter
- test_telegram_capture.py
- Ollama
- answer.py
- bench_runtime.py
- vault.py
- support.js
- worker.py
- ingest/extract.py
- test_grounding_values.py
- FakeConn
- Passage
- rows_for
- SentenceScanner
- household.py
- ParsedPage
- test_lifecycle.py
- score.py
- _household_scope
- .load
- test_pages.py
- parse.py
- test_eval_generate.py
- TelegramAdapter
- phrasings.py
- Any
- reminder/__init__.py
- test_api.py
- alert/__init__.py
- retrieve.py
- sse
- advice/__init__.py
- main
- test_eval_modules.py
- test_gate.py
- pipeline.py
- build_router
- test_household.py
- compilerOptions
- report.py
- registry.py
- test_grounding.py
- packs.py
- cli.py
- run.py
- ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic
- build.py
- Any
- eval/modules.py
- values.py
- FakeCursor
- lock.ts
- HouseholdAdviceLog
- routes.py
- PARROT Interface Design Pack
- export-design-preview.cjs
- The Four Surfaces
- pack
- advice-consent.tsx
- devDependencies
- score_alerts
- Hybrid Retrieval: Dense Plus Full-Text
- scope.py
- ADR 0011: The household is people and aliases, and the owner is one of them
- test_advice_core.py
- test_modules.py
- today/page.tsx
- test_eval_harness.py
- preview.tsx
- extract_values
- Two-stage quarantine with a vision-language second pass
- Any
- Ollama
- api.ts
- main
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- test_scan_parse.py
- components.json
- _as_module_summary
- test_tax_pack.py
- contracts.py
- Measured
- test_eval_report.py
- The Lim Household, Tampines
- ADR 0007 - The graph ships before retrieval and before a checkpoint table
- Lane C - Governance and assurance
- test_contracts.py
- Core Document Catalogue (ADR 0017)
- _today_items
- Connection
- The five-lane split (five people, nine weeks, three builders)
- Data inventory: identity data, DOBs and loans
- test_rerank.py
- Roadmap phase 3 - reminders
- web/ - the PARROT interface
- The document register as ground truth
- ingest.py
- Tax and Reliefs — contract changes this pack needs
- Reminder, Alert and Tracker Registers
- typing
- example_pack template manifest
- paperbrain/extract.py
- ingest/quarantine.py
- react
- test_registration.py
- Integration review
- PackManifest
- FakeCursor
- api/__init__.py
- test_the_inventory_always_reads_core_documents
- ValueRow
- _as_consent
- The deliberately naive retrieval baseline
- Running the evaluation harness
- grounding/__init__.py
- _as_vault_document
- The case for synthetic evaluation data
- Domain pack
- core/__init__.py
- Filling the corpus register
- Writing a governance artefact
- Two-Stage Quarantine With a Vision Second Pass
- Fill the Register Before Generating Documents
- Where Things Live
- Policy schedule HTML template
- worker/__init__.py
- eval/__init__.py
- PaperBrain
- ADR 0013: A question is understood before it is searched, and scoped before it is cut
- answer.tsx
- modules/__init__.py
- test_each_policy_lapses_on_its_own
- Settings
- pathlib
- PrivateCare Policy Wording Template
- alert module manifest
- is_first_person
- test_a_grounding_corpus_travels_inside_its_pack
- next
- The Grounding Gate
- Authoring a domain pack
- ADR 0008 - Ingestion runs on a Celery worker
- paperbrain/db.py
- DesignPreview evaluation harness
- logging
- supervise
- Adversarial testing from week 7
- Writing an ADR
- Every Fact Row Cites Its Source
- _graph_for
- test_a_document_still_in_the_inbox_is_not_forgotten
- .embed
- PARROT evaluation harness
- RagasJudge
- The autonomy statement
- Any
- ._categories_read_a_declared_field
- obligation_precision
- send_retry
- ADR index (0001-0018, with status)
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- _answer_events
- test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them
- The synthetic-to-real gap
- filesystem
- installed_packs
- test_reindexing_replaces_chunks_and_leaves_facts_alone
- Due
- Asks
- obligations_possible
- test_both_ask_endpoints_hand_the_graph_the_same_advice_ports
- One Database
- Config
- runtime/__init__.py
- corpus/__init__.py
- packs/__init__.py
- Lane E - Corpus and adversarial testing
- No code generates corpus documents
- Alert
- setup.sh
- session-start.sh
- package.json
- postcss.config.mjs
- Lane C - Governance and assurance
- parrot
- Vertical slices, not layers
- Real organisations may be named

## God Nodes (most connected - your core abstractions)
1. `Settings` - 186 edges
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

## Communities (207 total, 25 thin omitted)

### Community 0 - "ModelUnavailable"
Cohesion: 0.12
Nodes (15): Generated, ModelUnavailable, Any, Client, RuntimeError, Load the generator and the embedder now, and say where the generator landed. An…, Generate against a JSON schema. This is how extraction is held to a pack's…, The same constrained generation, yielded as it is written. Identical body to… (+7 more)

### Community 1 - "test_hybrid.py"
Cohesion: 0.09
Nodes (27): hybrid_score(), HybridRetriever, identifiers(), prints(), The tokens in a question that look like something printed rather than said: a…, Whether the chunk prints the identifier, ignoring case and the spacing inside…, The cosine similarity, lifted to `IDENTIFIER_HIT` when the chunk prints an…, Implements `core.graph.ports.Retriever`. Built where the connection is, like… (+19 more)

### Community 2 - "ScriptedOllama"
Cohesion: 0.06
Nodes (71): AdviceCard, AdviceWithheld, _closes(), ConsentRequired, Declined, Finished, A request for a recommendation or a judgement, declined before anything is…, Everything that is only knowable once the last sentence is in. `quarantined`… (+63 more)

### Community 3 - "test_answer_graph.py"
Cohesion: 0.06
Nodes (84): AnswerGraph, _either(), One sentence that has passed the gate, with the citations it passed on. It will…, "a dental plan", or "a term life plan or a whole life plan". "An" only before…, Built once, asked many times. Holds no connection: retrieval does., Sentence, The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting… (+76 more)

### Community 4 - "validate"
Cohesion: 0.09
Nodes (40): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+32 more)

### Community 5 - "Input"
Cohesion: 0.09
Nodes (55): Figure, Input, One fact or rule value a calculation was built on, carrying its own citation.…, One number a calculator produced, and the words a sentence must use to state…, _amount(), Basis, _calculation(), _capital() (+47 more)

### Community 6 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.05
Nodes (64): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, MediShield Life (CPF Board), Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022 (+56 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.13
Nodes (59): Calculation, Missing, What a calculator returns when every fact and rule it needed was on file and…, What a calculator returns when a fact or a rule value it needed was not there…, calculate(), Adviser, assert_nothing_negative(), basis() (+51 more)

### Community 8 - "checks.py"
Cohesion: 0.14
Nodes (21): capture_check(), Check, collect_checks(), database_check(), interface_check(), Read-only dependency diagnostics; installation is never treated as inference…, Whether the screens are answering on their port. This used to be a sentence…, Whether a worker is listening — which is a different question from whether… (+13 more)

### Community 9 - "test_ingest_pipeline.py"
Cohesion: 0.10
Nodes (45): extract(), Never raises. A failure is a reason, and a reason routes the document to…, FakeOllama, insurance(), iras(), _page_of_examples(), Any, Exception (+37 more)

### Community 10 - "test_grounding_index.py"
Cohesion: 0.09
Nodes (39): CaptureFixture, GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records…, SourceText, index_pack(), IndexReport, Any, date (+31 more)

### Community 11 - "test_worker_queue.py"
Cohesion: 0.11
Nodes (32): The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, sha256(), Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker. Celery is imported here rather…, index_folder(), Path (+24 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.09
Nodes (37): Magic bytes first, filename suffix second, `application/octet-stream` last. A…, sniff_mime(), FolderAdapter, FolderSettings, _Pending, datetime, Path, The watched-folder capture adapter. A person drops a scan into a folder and it… (+29 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.10
Nodes (35): MockTransport, build(), FakeRegistrar, FakeTelegram, photo_update(), Any, Path, Request (+27 more)

### Community 14 - "Ollama"
Cohesion: 0.07
Nodes (68): Send the pages as images and try the whole pack pipeline again on what comes…, The reportable line. Deliberately a rate and a count, because a rate over three…, Recovery, recovery_rate(), retry(), _still_quarantined(), bytes_for(), digest_of_document() (+60 more)

### Community 15 - "answer.py"
Cohesion: 0.04
Nodes (66): Claim, AdviceLog, Adviser, ConsentBook, Protocol, Implemented by `HouseholdConsents` in `core/advice_consent.py`., The granting row's id, or `None` when the owner has not granted this exact…, Implemented by `HouseholdAdviceLog` in `core/advice_records.py`. (+58 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (35): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+27 more)

### Community 17 - "vault.py"
Cohesion: 0.07
Nodes (37): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+29 more)

### Community 18 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 19 - "worker.py"
Cohesion: 0.13
Nodes (21): install_best_effort(), Install at startup without being able to stop startup. Both processes that own…, jinja2, find_browser_executable(), generate_documents(), Path, Project Parrot - Synthetic Document Generator for Lim Household…, Find Microsoft Edge or Google Chrome executable on Windows. (+13 more)

### Community 20 - "ingest/extract.py"
Cohesion: 0.09
Nodes (32): copy, FieldSpec, One extractable field. Its `name` is the column header in Desmond's register…, _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact (+24 more)

### Community 21 - "test_grounding_values.py"
Cohesion: 0.16
Nodes (33): _dropped(), _log_values(), Decimal, fixture, LogCaptureFixture, parametrize, Published values: the model reads a source, and code keeps only what the…, Assert a value was dropped, and logged with this reason. (+25 more)

### Community 22 - "FakeConn"
Cohesion: 0.12
Nodes (17): FakeConn, next_kind(), pack_row(), The kind of the next event on the wire., Starlette never closes a body iterator a disconnected client stopped pulling.…, The ruling's case as it happens on a socket: Starlette sends the card and at…, What the API owns when a stream is closed with the graph still parked on the…, The graph's own cleanup can fail -- for example the record insert raises -- and… (+9 more)

### Community 23 - "Passage"
Cohesion: 0.06
Nodes (33): fuse(), Several searches as one list: each passage once, at the best score any phrasing…, Every phrasing of the question, searched and fused. The person's own words…, DenseRetriever, NoReranker, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this…, The answer graph. Router, retrieve, rerank, grounding gate, then answer or…, Passage (+25 more)

### Community 24 - "rows_for"
Cohesion: 0.09
Nodes (37): document_row(), fact_row(), obligation(), open_obligation(), overdue_row(), date, ADR 0017: disabling insurance_agent switches off its voice, never a household's…, Snooze means 'not until this gets more urgent', so it can name the day it does. (+29 more)

### Community 25 - "SentenceScanner"
Cohesion: 0.10
Nodes (28): Any, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner, drip() (+20 more)

### Community 26 - "household.py"
Cohesion: 0.09
Nodes (39): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+31 more)

### Community 27 - "ParsedPage"
Cohesion: 0.13
Nodes (22): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, One flat list of chunks, ordinal running across the whole document., The page as `(is_heading, line)`, from the parser's structure when it has any. (+14 more)

### Community 28 - "test_lifecycle.py"
Cohesion: 0.14
Nodes (25): Lifecycle, What the person asked for, once. The first request wins; later ones change…, _client(), _eventually(), _launcher(), parametrize, Path, TestClient (+17 more)

### Community 29 - "score.py"
Cohesion: 0.06
Nodes (62): Answer, Answered. Asking for consent and naming what is missing are endings, not…, Trace, _as_date(), _as_number(), cites(), _contains(), declined_in_prose() (+54 more)

### Community 30 - "_household_scope"
Cohesion: 0.09
Nodes (35): _household_scope(), MonkeyPatch, Person, `HouseholdScope` over a roster held in memory, with every document resolved by…, The roster has no grandparent relation, so the household says it the only way…, 13 September: "what is Marcus's premium?" has no "my", so nothing was scoped…, A model proposal is a question on Today, not a member yet — the same rule…, Nothing named, nothing ruled out: the question is the owner's, same as `apply`… (+27 more)

### Community 31 - ".load"
Cohesion: 0.07
Nodes (48): create_app(), checks(), lifespan(), ready(), setup(), system_status(), ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one… (+40 more)

### Community 32 - "test_pages.py"
Cohesion: 0.08
Nodes (39): document_page(), page_images(), Base64 page images, in page order. Empty when this document cannot be rendered.…, page_count(), PageUnavailable, _pdfium(), Any, LookupError (+31 more)

### Community 33 - "parse.py"
Cohesion: 0.10
Nodes (21): Block, DoclingParser, _kind(), _pages_from(), Parser, PlainTextParser, Protocol, Turn captured bytes into pages of text, or say why it could not be done. Every… (+13 more)

### Community 34 - "test_eval_generate.py"
Cohesion: 0.09
Nodes (40): _ambiguous(), choose(), Generated, hand_written(), main(), on_file(), pool(), Namespace (+32 more)

### Community 35 - "TelegramAdapter"
Cohesion: 0.08
Nodes (32): BaseTransport, CaptureAdapter, IngestJob, datetime, Protocol, The one interface every capture channel satisfies. receive(payload, mime,…, What a capture returns: a registered document, and whether we had seen it…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call. (+24 more)

### Community 36 - "phrasings.py"
Cohesion: 0.20
Nodes (11): _keys(), LaneSpec, Row, How a question about a printed field is worded, per document type in…, One document type's wordings. `printed` and `spoken` each render the *thing* a…, Which register rows a lane's questions are drawn from. The task asks each…, A wording, or `None` when the row does not fill every field it needs., The spoken wording, or "Rachel's payslip" when the type has no product name of… (+3 more)

### Community 37 - "Any"
Cohesion: 0.14
Nodes (17): Measurement, by_subject(), db(), FakeCursor, load_register(), Any, date, fixture (+9 more)

### Community 38 - "reminder/__init__.py"
Cohesion: 0.11
Nodes (22): already_said(), current_lead(), next_window(), Overdue, Any, date, datetime, LookupError (+14 more)

### Community 39 - "test_api.py"
Cohesion: 0.10
Nodes (37): advising(), client(), conn(), FakeGraph, graph(), _padded(), fixture, MonkeyPatch (+29 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.19
Nodes (21): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), Any, date (+13 more)

### Community 41 - "retrieve.py"
Cohesion: 0.21
Nodes (15): answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, pack(), _fts_query(), fuse(), Hit (+7 more)

### Community 42 - "sse"
Cohesion: 0.10
Nodes (35): Citation, A passage, named the way a person cites it and identified the way a link needs.…, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed…, Reading, a_citation(), advice_card(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order. (+27 more)

### Community 43 - "advice/__init__.py"
Cohesion: 0.10
Nodes (32): AdviceShape, FactInput, A printed fact a calculator reads, named by where it is printed rather than…, One kind of advice question, and everything its calculator needs to answer it., date, _fact(), fact_row(), FactRow (+24 more)

### Community 44 - "main"
Cohesion: 0.07
Nodes (45): platform, _kill_tree(), main(), open_browser(), port_answers(), Popen, Stop a child and everything under it, then make sure it has gone., Whether something is listening on loopback. Not whether it is ours. (+37 more)

### Community 45 - "test_eval_modules.py"
Cohesion: 0.19
Nodes (18): Obligation, One verdict per obligation. `declared` is the catalogue's `registers.reminder`…, One `obligations` row, with the fact and document it was created from., score_obligations(), _obligation(), Metrics 7 and 8: obligation precision and the alert false-positive rate. No…, The failure this metric exists for: a reminder for a date nobody printed., A passport prints RACHEL NG HUI SHAN; the register writes it in title case. (+10 more)

### Community 46 - "test_gate.py"
Cohesion: 0.08
Nodes (51): What a calculator returns, and what the graph needs to ask consent and keep a…, check(), check_advice(), check_content(), check_one(), Claim, _normal(), The grounding gate. Rule 3 in AGENTS.md: no claim without a citation. This… (+43 more)

### Community 47 - "pipeline.py"
Cohesion: 0.07
Nodes (41): Chunk, What is actually embedded: the prefix plus the text, matching the tsvector…, The ingestion worker. Capture registers a document; this package turns it into…, fixed(), from_facts(), _label(), Any, date (+33 more)

### Community 48 - "build_router"
Cohesion: 0.11
Nodes (29): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, QuarantinedDocument, QuarantineResponse, What changed, in the words the screen confirms it with. `was` is returned… (+21 more)

### Community 49 - "test_household.py"
Cohesion: 0.15
Nodes (23): Keep the owner's passages and the household's; set aside everybody else's. A…, scope_passages(), conn(), _conn_returning(), _passage(), Any, fixture, Who is asking, and whose documents may answer. Two halves, deliberately split.… (+15 more)

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 51 - "report.py"
Cohesion: 0.14
Nodes (22): _cell(), collect(), main(), _overall(), _paragraph(), Provenance, Any, Path (+14 more)

### Community 52 - "registry.py"
Cohesion: 0.13
Nodes (26): installed_modules(), Every module directory holding a `module.yaml`, in a stable order. Directories…, enabled_module_ids(), install(), Installed, _module_row(), modules(), _pack_row() (+18 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.18
Nodes (24): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError, Read and validate a pack's grounding corpus from its own folder on disk. A…, A pack's grounding corpus on disk does not match what its `sources.yaml`… (+16 more)

### Community 54 - "packs.py"
Cohesion: 0.11
Nodes (23): DocumentTypeSpec, One kind of document the core recognises., Classification, classify(), _prompt(), Decide which of the core catalogue's document types a captured document is, or…, Never raises. An unavailable model is a classification failure, so it…, _schema() (+15 more)

### Community 55 - "cli.py"
Cohesion: 0.21
Nodes (20): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+12 more)

### Community 56 - "run.py"
Cohesion: 0.12
Nodes (29): main(), _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), _indexed() (+21 more)

### Community 57 - "ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.15
Nodes (20): Code-written absence sentence: 'None of the N policies on file is a dental plan.', ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic, The advise route intent returns the pack's advice_decline, answering.categories: ordered whole-word rules over one printed field, Category filter applied before the keep-6 cut, answering.exclusions: headings under which a cover claim is not believed, Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration) (+12 more)

### Community 58 - "build.py"
Cohesion: 0.13
Nodes (24): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering…, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why the catalogue cannot supply `field` from every one of `doc_types`, or None., _class_name(), _docstring(), _field_line(), _header() (+16 more)

### Community 59 - "Any"
Cohesion: 0.10
Nodes (23): advised_pack(), db(), _document(), _facts_tuple(), FakeConn, FakeCursor, Any, date (+15 more)

### Community 60 - "eval/modules.py"
Cohesion: 0.15
Nodes (15): _mark(), measure(), ModuleMetrics, obligations(), _paragraph(), Metrics 7 and 8: obligation precision and the alert false-positive rate, scored…, A passport prints RACHEL NG HUI SHAN and the register writes Rachel Ng Hui…, What `eval.run` puts in a result file, and what the W7 report prints. (+7 more)

### Community 61 - "values.py"
Cohesion: 0.07
Nodes (33): _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), number_tokens(), _pack(), parse_value() (+25 more)

### Community 62 - "FakeCursor"
Cohesion: 0.22
Nodes (3): FakeCursor, Any, FakeConn

### Community 63 - "lock.ts"
Cohesion: 0.07
Nodes (46): ref_node_crypto, dynamic, GET(), grant(), POST(), runtime, ALLOWED, Context (+38 more)

### Community 64 - "HouseholdAdviceLog"
Cohesion: 0.31
Nodes (6): HouseholdAdviceLog, `core.graph.advice.AdviceLog` over a live connection. `basis` is dumped with…, AdviceRecord, Every advised or withheld answer's full basis, so it can be reconstructed later…, test_record_insert_includes_the_sha256_of_the_disclaimer(), Log

### Community 65 - "routes.py"
Cohesion: 0.10
Nodes (42): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, CloseRequest, ConfirmNameRequest, ConsentRequest, ConsentRequiredEvent (+34 more)

### Community 66 - "PARROT Interface Design Pack"
Cohesion: 0.09
Nodes (30): Not finding you is an answer (first-person abstention), The readiness check verifies the model the way it will be used (one pair scored), Capture is where the user already is, Citation chips are the trust surface, Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Nothing moves without a reason (motion specification) (+22 more)

### Community 67 - "export-design-preview.cjs"
Cohesion: 0.08
Nodes (23): @eslint/eslintrc, ref_node_fs, ref_node_path, ref_node_url, compat, eslintConfig, bundle(), classes (+15 more)

### Community 68 - "The Four Surfaces"
Cohesion: 0.13
Nodes (16): Packs and Modules May Not Import web/ or api/, The FastAPI Application, The API Surface, GET /api/today Never Marks Anything Notified, apply, Auto-Redirect to Today Once Ready, check, draw (+8 more)

### Community 69 - "pack"
Cohesion: 0.06
Nodes (54): Categories, _asked(), _conversation(), The shape a question asks for, matched from the pack's own phrases without a…, The first advising pack whose review a question asks for, as a shape the advise…, What the graph carries. It ends at the evidence; the answer is streamed, not…, The question to answer and to scope. A follow-up is the whole question it was…, The question made whole, and said in the documents' words. See… (+46 more)

### Community 70 - "advice-consent.tsx"
Cohesion: 0.16
Nodes (18): AdviceNote(), Consent, ConsentPrompt(), agree(), settle(), State, ADR-0016, AdviceConsentSection() (+10 more)

### Community 71 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 72 - "score_alerts"
Cohesion: 0.16
Nodes (13): alert_fpr(), AlertVerdict, One verdict per fired alert: whether the register, recomputed, crosses the same…, Metric 8. `None` when nothing fired: a rate over zero alerts is not 0.0, it is…, score_alerts(), Fired, A `modules.alert.Alert` as far as `score_alerts` reads one., The real case, as of this corpus: the vault extracted the renewal notice's 2026… (+5 more)

### Community 73 - "Hybrid Retrieval: Dense Plus Full-Text"
Cohesion: 0.18
Nodes (11): No New Runtime Dependency Without an ADR, Never Generate SQL at Runtime, baseline.py Is Disposable and Never a Measurement, ports.py, the Seam With Lane B, bge-reranker-v2-m3 Cross-Encoder, 40 Down to 6, Hybrid Retrieval: Dense Plus Full-Text, Reciprocal Rank Fusion, k=60, The Household's Eleven Policies (+3 more)

### Community 74 - "scope.py"
Cohesion: 0.20
Nodes (19): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Any (+11 more)

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.17
Nodes (19): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), The owner is a row, not a config value baked at install, people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), A resolved person is shown as a chip, like a citation, The roster is derived from documents, then confirmed (+11 more)

### Community 76 - "test_advice_core.py"
Cohesion: 0.06
Nodes (47): Channel, current(), grant(), HouseholdConsents, _latest(), NoOwner, Any, RuntimeError (+39 more)

### Community 77 - "test_modules.py"
Cohesion: 0.15
Nodes (28): AlertConfig, Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), Everything inside a lead window that has not already been said for that window.…, sweep(), FakeConn, obligation_row(), datetime (+20 more)

### Community 78 - "today/page.tsx"
Cohesion: 0.07
Nodes (29): dynamic, HouseholdPage(), metadata, runtime, AppLayout(), dynamic, isUrgent(), metadata (+21 more)

### Community 79 - "test_eval_harness.py"
Cohesion: 0.09
Nodes (35): Cited, One sentence and the passages it was traced to. What rule 3 looks like as data.…, The reference answer Ragas judges recall and precision against. A fact…, reference_for(), Expected, load_set(), MalformedQuestion, Any (+27 more)

### Community 80 - "preview.tsx"
Cohesion: 0.10
Nodes (17): metadata, answers, DesignPreview(), Direction, directions, Item, items, web_app_design_preview_preview_module (+9 more)

### Community 81 - "extract_values"
Cohesion: 0.18
Nodes (19): extract_values(), Every value the source prints for these keys, kept only when its passage prints…, _long_text(), Any, Exception, Generated, Returns the replies the test wrote, in order, then an empty list of values. A…, A truncated or non-JSON reply is an outage: the section was never actually… (+11 more)

### Community 82 - "Two-stage quarantine with a vision-language second pass"
Cohesion: 0.12
Nodes (19): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Two-stage quarantine with a vision-language second pass, Batch 4: the deliberately hard documents, A full policy wording registers as policy_schedule, Task: review every quarantined document and label the failure, Task: sign off the capture-to-database path against the data inventory, Measurement is owned separately from the engine (+11 more)

### Community 83 - "Any"
Cohesion: 0.12
Nodes (7): ConsentCursor, Fails, FakeCursor, Any, The parameters of the one statement containing `needle`. Fails loudly if it…, Yields `before`, then raises. `ask` raises at once., Remembers what `grant` or `withdraw` inserted, so the next read of the latest…

### Community 84 - "Ollama"
Cohesion: 0.21
Nodes (5): Ollama, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.…, Batch embeddings. Falls back to the legacy endpoint on old servers., urllib_error, urllib_request

### Community 85 - "api.ts"
Cohesion: 0.04
Nodes (62): ADR-0017, dynamic, metadata, PacksPage(), runtime, DocumentPage(), dynamic, metadata (+54 more)

### Community 86 - "main"
Cohesion: 0.12
Nodes (22): approve(), pending(), PendingValue, Any, date, A person's approval, standing between a model's extraction and any calculator…, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it. (+14 more)

### Community 87 - "ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.16
Nodes (20): ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, The adult rule: advice is withheld for a person under 21 or a child with no date of birth on file, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel), Advice graph flow: shape match, subject resolution, consent, AdviceCard, explain, advice_records keeps each answer's full basis, PackManifest.advice shapes (gap, remaining_room, keep_or_surrender, compare_own, compare_market, estimate_saving), Advice.review: one question runs every shape at once (+12 more)

### Community 88 - "test_scan_parse.py"
Cohesion: 0.14
Nodes (17): csv, FixtureRequest, Image, needs_ocr, _as_printed(), page_pixels(), photographed(), fixture (+9 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "_as_module_summary"
Cohesion: 0.20
Nodes (10): ModuleSummary, PacksResponse, PackSummary, _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack() (+2 more)

### Community 91 - "test_tax_pack.py"
Cohesion: 0.20
Nodes (16): pytest, _basis(), _latest(), _matched(), _published(), FactRow, parametrize, The tax pack's advice, run on batch 1's own SRS statements and Notices of… (+8 more)

### Community 92 - "contracts.py"
Cohesion: 0.08
Nodes (34): Advice, Answering, Category, Exclusions, Grounding, Guardrails, ModuleManifest, ModuleTrigger (+26 more)

### Community 93 - "Measured"
Cohesion: 0.20
Nodes (14): _day(), Measured, _number(), A metric recomputed from the register, for one person and one of their things.…, Days since cover lapsed, per person and per policy, from the register's own…, Each holder's largest year-to-date total for the year being swept. A statement…, Deductible donations this year, added up. A receipt that does not say it is…, Employee CPF on this year's payslips, added up. `pay_period` is text, as YYYY-… (+6 more)

### Community 94 - "test_eval_report.py"
Cohesion: 0.12
Nodes (30): extraction_by_type(), extraction_f1(), FactRow, _outcomes(), Collection, One row of the `facts` table, as the harness reads it: which document, which…, `(doc_id, doc_type, field, (tp, fp, fn))` for every register cell that was…, Metric 6, micro-averaged over every scored field: `all`, then one entry per… (+22 more)

### Community 95 - "The Lim Household, Tampines"
Cohesion: 0.15
Nodes (16): loan_agreement Document Type, payslip Document Type, The Lim Household, Tampines, One Household Only; the Persona Sketches Are Gone, Rachel Ng Arrives Off Documents, Not a Persona Sketch, Household Canon Template, Three Surnames, One Household, doc_id Is the Filename (+8 more)

### Community 96 - "ADR 0007 - The graph ships before retrieval and before a checkpoint table"
Cohesion: 0.22
Nodes (11): ADR 0007 - The graph ships before retrieval and before a checkpoint table, Retrieval is a port, not an import, .graphifyignore excludes the corpus, Scoping happens after retrieval, and that has a ceiling, The redacted real-document holdout, Dense-only retrieval stopgap, Hardware qualification, Rebuilding the vault's vectors (+3 more)

### Community 97 - "Lane C - Governance and assurance"
Cohesion: 0.13
Nodes (16): The evaluation is the gate, Data inventory and flow map, ISO/IEC 22989 to 5338 stage-to-process map, Lane C - Governance and assurance, Model card, Retention and erasure policy, Say unverified rather than write a plausible sentence, Siew's generated task list (+8 more)

### Community 98 - "test_contracts.py"
Cohesion: 0.08
Nodes (51): _advised(), _checked(), _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact() (+43 more)

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.10
Nodes (21): The Purely Additive Migration Exception, Contracts and Migrations Are Their Own PR, Sources of Truth Generate Their Outputs, Snooze Means Not Until This Gets More Urgent, The Three Things Agents Get Wrong Here, Generated Files Committed Alongside Their Source, benefit_illustration Document Type, birth_certificate Document Type (+13 more)

### Community 100 - "_today_items"
Cohesion: 0.19
Nodes (13): A document and a page, as a person would cite it — or, for published guidance,…, Source, TodayItem, TodayResponse, today(), _cite(), _link(), date (+5 more)

### Community 101 - "Connection"
Cohesion: 0.18
Nodes (8): Connection, Cursor, Any, Protocol, Just enough of `psycopg.Connection` to register a document and to be faked in a…, cursor(), embed_chunks(), Embed every chunk that doesn't have a vector yet.

### Community 102 - "The five-lane split (five people, nine weeks, three builders)"
Cohesion: 0.09
Nodes (30): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The domain pack manifest, The expansion model: two axes, not one list, The golden set: answerable, hard negatives, adversarial, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build (+22 more)

### Community 103 - "Data inventory: identity data, DOBs and loans"
Cohesion: 0.17
Nodes (15): Data inventory: identity data, DOBs and loans, The lock is a screen lock, not encryption, next dev binds every interface, not loopback, Telegram capture route and delete-at-source, What crosses a boundary, Governance artefact set, Write unverified rather than assert, The final ILP report (+7 more)

### Community 104 - "test_rerank.py"
Cohesion: 0.06
Nodes (45): CrossEncoderReranker, device_name(), load(), passage_text(), Any, The cross-encoder reranker: forty candidates read against the question, six…, One relevance logit per text, higher is better. Batched so forty passages is a…, Say it, once per process. A passage cut at the cap is scored on its first part… (+37 more)

### Community 105 - "Roadmap phase 3 - reminders"
Cohesion: 0.14
Nodes (15): The answer graph: router, retrieve, rerank, grounding gate, Capability modules: Reminder and Alert, Task: build the answer graph with the grounding gate, Contradiction attack, Task: contextualised chunking and the reranker, Task: hybrid retrieval with reciprocal rank fusion, The reminders table as an extension point, Roadmap phase 3 - reminders (+7 more)

### Community 106 - "web/ - the PARROT interface"
Cohesion: 0.14
Nodes (15): Task: complete the Insurance Agent pack, ADR 0017 - a pack is grounding and persona, Lock the design tokens before building any screen, The four surfaces: Today, Ask, Vault, Packs, Lane D - Domain packs and interface, The platform argument: one core, two domains, Task: define the pack catalogue - the nine deferred packs, Zee's generated task list (+7 more)

### Community 107 - "The document register as ground truth"
Cohesion: 0.18
Nodes (15): batch0-personas is deleted and must not be recreated, python -m corpus.validate, The document register as ground truth, The whole-life expiry_date mismatch, Register column headings are generated, not chosen, The household canon (the Lims of Tampines), Register first, documents second, Task: spot-check 20 register rows against the extractor (+7 more)

### Community 108 - "ingest.py"
Cohesion: 0.20
Nodes (14): itertools, Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks. Paperwork is short and…, _split_page(), discover(), guess_date() (+6 more)

### Community 109 - "Tax and Reliefs — contract changes this pack needs"
Cohesion: 0.40
Nodes (4): 1. A deduction multiplier on `estimate_saving`, 2. Limiting a fact input to one year, Not a contract change: parent relief, Tax and Reliefs — contract changes this pack needs

### Community 110 - "Reminder, Alert and Tracker Registers"
Cohesion: 0.18
Nodes (15): Passport Uses date_of_expiry So policy_expiry Does Not Fire, filing_deadline Reminder, maturity_date Is Not expiry_date, passport Document Type, passport_expiry Reminder, policy_expiry Reminder, policy_schedule Document Type, Reminder, Alert and Tracker Registers (+7 more)

### Community 111 - "typing"
Cohesion: 0.05
Nodes (46): The local API. Liveness is intentionally separate from assistant readiness.…, The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), collections_abc, contextlib, The owner's consent to a pack's advice, append-only (ADR 0016). Consent is the…, The record of every advised or withheld answer (ADR 0016). `advice_records`… (+38 more)

### Community 112 - "example_pack template manifest"
Cohesion: 0.18
Nodes (14): I explain the renewal notice, I do not renew policies, Autonomy statement, ISO/IEC 22989 stages versus 5338 processes, never_acts as a machine-checked flag, Grounding corpora now live inside packs, advice module manifest, example_pack template manifest, example_room advice shape (+6 more)

### Community 113 - "paperbrain/extract.py"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 114 - "ingest/quarantine.py"
Cohesion: 0.18
Nodes (16): base64, blocked_reasons(), forget(), Any, Path, ValueError, QuarantinedDocument, queue() (+8 more)

### Community 115 - "react"
Cohesion: 0.05
Nodes (34): lucide-react, react, dynamic, runtime, Motion(), ROWS, INKS, metadata (+26 more)

### Community 116 - "test_registration.py"
Cohesion: 0.29
Nodes (12): Insert or update the `documents` row for these bytes and say which happened.…, register_document(), conn(), database_url(), Any, fixture, The idempotent upsert, against the real unique index. `documents.sha256 UNIQUE`…, test_a_document_must_arrive_with_a_name() (+4 more)

### Community 117 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 118 - "PackManifest"
Cohesion: 0.23
Nodes (10): PackManifest, A domain pack, authored as one YAML file: grounding, persona, answering and…, Every core document type, field and category this pack names exists, or…, A compared field no document type of the shape declares can never be printed.…, _insurance(), ADR 0017: documents are the core's. A pack.yaml carrying them does not load., test_a_grounding_corpus_is_named_by_id_not_by_path(), test_a_pack_cannot_opt_out_of_verdict_by_code() (+2 more)

### Community 121 - "test_the_inventory_always_reads_core_documents"
Cohesion: 0.20
Nodes (7): _Answering, The event stream one request is sending, held where the request's cleanup can…, Close the answer stream when the request ends, whatever ended it. Requires…, Conn, ADR 0017: a document is the core's, so the query includes `core` whatever is…, test_the_inventory_always_reads_core_documents(), cursor()

### Community 122 - "ValueRow"
Cohesion: 0.15
Nodes (18): Hashable, _ambiguous(), _band(), _band_label(), _in_band(), _order_key(), _ordered(), _product_name() (+10 more)

### Community 123 - "_as_consent"
Cohesion: 0.29
Nodes (7): AdviceConsent, AdviceConsent, One advising pack, the wording a person is asked to agree to, and what the…, _as_consent(), advice_consents(), record_consent(), One advising pack's consent wording and the owner's standing answer to it.

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.17
Nodes (12): Task: benchmark the workstation and publish the numbers, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, The deliberately naive retrieval baseline, Committed runs are never deleted, Yew Mun's generated task list, Hybrid retrieval, not embeddings alone, Chunking respects paragraphs (+4 more)

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 127 - "_as_vault_document"
Cohesion: 0.29
Nodes (7): VaultDocument, VaultFact, VaultResponse, _as_vault_document(), one_document(), vault_documents(), VaultDocument

### Community 128 - "The case for synthetic evaluation data"
Cohesion: 0.18
Nodes (11): Qwen-SEA-LION-v4-4B-VL extraction ceiling, Register first, then generate, SYNTHETIC DOCUMENT footer, Ground truth for free, The 40-document holdout corpus, The case for synthetic evaluation data, Two withdrawn synthetic-data controls, extraction_f1 (+3 more)

### Community 129 - "Domain pack"
Cohesion: 0.12
Nodes (21): The demonstration run sheet, Step 8 - switch a pack off, Step 6 - the abstention, Step 7 - the refusal to act, Step 2 - the source chip, Derive the roster, then confirm it, Exactly one owner, enforced by the database, facts.subject is never normalised (+13 more)

### Community 131 - "Filling the corpus register"
Cohesion: 0.20
Nodes (9): Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one, The rule that cannot bend (+1 more)

### Community 132 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (9): Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six, Where governance touches the code (+1 more)

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

### Community 139 - "PaperBrain"
Cohesion: 0.20
Nodes (10): The code pass of the knowledge graph, Nobody edits core/contracts.py in a feature pull request, Lane A - Integration and product, The semantic pass of the knowledge graph, Triage prompt: four buckets, no code written, Ninety protected minutes a week of integration, Christian's generated task list, PaperBrain (+2 more)

### Community 140 - "ADR 0013: A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.16
Nodes (18): guardrails.abstain_below was calibrated on un-prompted scores, ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts, chunks.tsv built from context_prefix || text, Context prefix: title - type - heading - page, rag_probe2 before/after similarity table (six policies, 13 September), scripts/reindex.py rebuilds chunks and vectors, Schedule-table questions remain weak (rank 2-4), Chunks follow the document's structure (Docling heading labels) (+10 more)

### Community 141 - "answer.tsx"
Cohesion: 0.06
Nodes (40): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+32 more)

### Community 144 - "Settings"
Cohesion: 0.11
Nodes (46): Whether Telegram capture should start. An unset token means "not this…, Settings, client_for(), consent(), ConsentConn, parametrize, The point of the endpoint. An UPDATE alone loses the example we are trying to…, The graph writes the record and never commits. The request that asked commits… (+38 more)

### Community 145 - "pathlib"
Cohesion: 0.07
Nodes (37): argparse, collections, build(), Any, The one Celery application, built from `Settings`. Every setting here is a…, Construct the Celery application. Imported lazily by callers so that nothing…, beat_schedule(), cron_expressions() (+29 more)

### Community 146 - "PrivateCare Policy Wording Template"
Cohesion: 0.31
Nodes (9): PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Gemini prompt bank for identity specimens, The Lim household canon, Republic of Xinkapow (+1 more)

### Community 147 - "alert module manifest"
Cohesion: 0.28
Nodes (9): Days without recorded cover tile, alert_fpr, obligation_precision, Module manifest template, Quoted "on" key in YAML 1.1, alert module manifest, Modules read typed rows, never chunks, reminder module manifest (+1 more)

### Community 148 - "is_first_person"
Cohesion: 0.20
Nodes (11): is_first_person(), `(word, relation)` when the question asks about a relation's own documents,…, Whether this question is about the person asking. `other_names` are the display…, relation_asked(), parametrize, "What is Rachel's premium on my policy" is a question about Rachel. A…, test_a_name_that_is_not_exactly_one_person_scopes_nothing(), test_a_named_household_member_wins_over_the_pronoun() (+3 more)

### Community 149 - "test_a_grounding_corpus_travels_inside_its_pack"
Cohesion: 0.50
Nodes (4): Path, A downloaded pack carries its sources, so no corpus is left at the repository…, test_a_grounding_corpus_travels_inside_its_pack(), test_every_grounding_corpus_declares_its_provenance()

### Community 150 - "next"
Cohesion: 0.15
Nodes (10): next, next-themes, web_app_globals, figtree, jetbrains, metadata, outfit, viewport (+2 more)

### Community 151 - "The Grounding Gate"
Cohesion: 0.29
Nodes (8): never_acts: True in Every Pack Manifest, The Core Answering Layer, The Answer Path: route, retrieve, rerank, ground, answer or abstain, The Grounding Gate, The Score Floor the Gate Reads, Kidney Stones: Inpatient Covered, Outpatient ESWL Excluded, Ask Screen, Try to Make It Lie: the Abstention Test

### Community 152 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 153 - "ADR 0008 - Ingestion runs on a Celery worker"
Cohesion: 0.39
Nodes (8): ADR 0005 - The watched folder is polled, not subscribed to, Stability debounce with injected time, ADR 0008 - Ingestion runs on a Celery worker, The queue carries a digest, not the document, The ingestion worker, START.cmd launcher, Telegram capture, The watched inbox folder

### Community 154 - "paperbrain/db.py"
Cohesion: 0.24
Nodes (8): ndarray, numpy, sqlite3, load_matrix(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.…, Return (N x D matrix of normalised embeddings, chunk ids)., stats(), unpack()

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (8): parrot-sweep shimmer animation, Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, An answer with the page it came from, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "logging"
Cohesion: 0.06
Nodes (41): RuntimeError, Safe to show: never contains the token., TelegramSettings, TelegramUnavailable, Dispatcher, Inline, Protocol, What happens to a document between "these bytes are registered" and "this… (+33 more)

### Community 157 - "supervise"
Cohesion: 0.40
Nodes (5): parse_args(), Any, Namespace, Keep Parrot running across restarts, and own the screens so they outlive them.…, supervise()

### Community 158 - "Adversarial testing from week 7"
Cohesion: 0.25
Nodes (8): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Adversarial testing from week 7, Prompt injection carried inside a document, Scope attack: asking it to act, Task: run adversarial Set C and write up the findings, Adversarial Set C (15 questions that should not be answered), Golden Set C - adversarial (15)

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 161 - "Every Fact Row Cites Its Source"
Cohesion: 0.33
Nodes (7): Every Fact Row Cites Its Source, A Correction Cannot Invent a Row, Every Node Writes One Line to traces, The Ingestion Pipeline, The Pipeline Forks Into Retrieval and Facts Lanes, Numbers Come From Postgres, Never From the Model, macOS Worker Runs Celery Solo

### Community 162 - "_graph_for"
Cohesion: 0.17
Nodes (13): AskRequest, AskResponse, Claim, The whole answer, once. `text` is the consent wording when `kind` is…, One sentence and the passages it was traced to. Never emitted without…, _as_response(), ask(), ask_stream() (+5 more)

### Community 163 - "test_a_document_still_in_the_inbox_is_not_forgotten"
Cohesion: 0.20
Nodes (10): filed_document(), inbox(), Path, Capture would register it again within a minute, so the button would only…, A watched folder holding one document, hashed the way the ingest registered it., v1 keeps the inbox as the document store, so this is a real state, not a fault., test_a_document_still_in_the_inbox_is_not_forgotten(), test_a_document_whose_file_left_the_inbox_is_409_not_500() (+2 more)

### Community 164 - ".embed"
Cohesion: 0.29
Nodes (5): A question, embedded the way the model was trained to embed a search query., Passages as `(title, text)`, embedded the way the model was trained to embed a…, Whether this embedding model expects `QUERY_PROMPT` and `DOCUMENT_PROMPT`., One request for the whole batch. Returns vectors in the order given., uses_task_prompts()

### Community 165 - "PARROT evaluation harness"
Cohesion: 0.38
Nodes (7): abstention_rate, PARROT evaluation harness, Set A, answerable, Set B, hard negatives, Set C, adversarial, The golden question sets, must_cite_page from field_pages

### Community 166 - "RagasJudge"
Cohesion: 0.32
Nodes (6): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts(), Ragas 0.4 metrics through Ollama's OpenAI-compatible endpoint. Imported lazily…

### Community 167 - "The autonomy statement"
Cohesion: 0.29
Nodes (7): The autonomy statement, Governance claims traced to enforcement points, IMDA mappings and autonomy statement artefact, The facts table as an extension point, Constraint: fully offline, Explicitly not doing: cloud, hosted vectors, autonomous spending, Roadmap phase 2 - facts

### Community 168 - "Any"
Cohesion: 0.29
Nodes (4): Any, Exception, Generated, The same scripted reply, in five-character pieces. Deliberately chopped: every…

### Community 169 - "._categories_read_a_declared_field"
Cohesion: 0.33
Nodes (3): Whether any document type in the catalogue declares `field`., An advice shape that names a missing role or key fails at load time. Caught…, model_validator

### Community 170 - "obligation_precision"
Cohesion: 0.33
Nodes (4): obligation_precision(), Metric 7, over the obligations a document produced. A calendar deadline is…, What the register says about one obligation. `verdict` is the bucket it counts…, Verdict

### Community 171 - "send_retry"
Cohesion: 0.40
Nodes (5): 202. The vision pass is slower than a page load, so it is queued and this is…, RetryAccepted, retry_one(), Put one quarantine retry on the queue and return its task id. The vision pass…, send_retry()

### Community 172 - "ADR index (0001-0018, with status)"
Cohesion: 0.09
Nodes (27): ADR 0001 - Record architecture decisions, ADR 0002 - One PostgreSQL instance for everything, Reciprocal rank fusion of dense and lexical, ADR 0003 - PaperBrain informs the pattern, not the module, PaperBrain prototype, ADR 0004 - Local setup can run before the assistant is ready, ADR 0006 - pypdfium2 renders the quarantine page images, ADR 0009 - next-themes and lucide-react are the only two web dependencies beyond the stack (+19 more)

### Community 173 - "Page one as plain Label: value lines"
Cohesion: 0.33
Nodes (6): Appendicitis entitlement demonstration, Page one as plain Label: value lines, Ward and hospital entitlement clause, Answering: vocabulary, categories, exclusions, The four tests every field must pass, policy_type was judged, not printed

### Community 174 - "Project skills"
Cohesion: 0.40
Nodes (4): Changing them, Project skills, Slash commands, Using them

### Community 175 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 176 - "_answer_events"
Cohesion: 0.20
Nodes (12): ErrorEvent, The stream broke after it began. A client cannot read an HTTP status by then., _answer_events(), connection(), Any, Event, Request, One connection per request, closed when it ends. Handlers are declared `def`… (+4 more)

### Community 177 - "test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them"
Cohesion: 0.25
Nodes (5): ClosingSpy, Wraps an event generator to record whether something called `.close()` on it,…, Starlette's own body iteration (`iterate_in_threadpool`) never calls `.close()`…, test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them(), spying()

### Community 179 - "The synthetic-to-real gap"
Cohesion: 0.40
Nodes (5): The 40-document redacted holdout, The synthetic-to-real gap, Consent and redaction protocol, Task: write the PDPA position on using synthetic data, Task: evaluation run 3 plus the holdout run

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 181 - "installed_packs"
Cohesion: 0.40
Nodes (5): installed_packs(), Every pack directory holding a pack.yaml, in a stable order. Directories whose…, test_every_installed_pack_still_loads(), test_every_pack_speaks_only_for_catalogue_types(), test_the_template_directory_is_not_an_installed_pack()

### Community 184 - "Asks"
Cohesion: 0.50
Nodes (3): Asks, Protocol, The one method of `AnswerGraph` the harness uses. A test supplies a fake.

### Community 185 - "obligations_possible"
Cohesion: 0.50
Nodes (4): obligations_possible(), How many document-derived obligations the register supports — the denominator…, Precision over three rows is not a reminder system that found everything, so…, test_what_the_register_supports_is_reported_beside_the_precision()

### Community 201 - "Alert"
Cohesion: 0.25
Nodes (5): Alert, What the debounce is keyed on: this metric, for this person and thing, in this…, Two lapsed policies on one person are two alerts, and saying one must not…, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

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
- **369 isolated node(s):** `session-start.sh script`, `PATH`, `npx`, `@modelcontextprotocol/server-filesystem`, `_Formatter` (+364 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1700 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
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