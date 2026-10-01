# Graph Report - igd-capstone-2026  (2026-10-01)

## Corpus Check
- 313 files · ~714,054 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 38 file(s) not represented in the graph (top: (none) 15, .jsonl 7, .csv 5)

## Summary
- 4712 nodes · 11562 edges · 213 communities (170 shown, 37 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1042 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a4972d2c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Ollama
- test_hybrid.py
- InstalledPack
- test_answer_graph.py
- validate
- advice/__init__.py
- Provenance register for corpus sg_protection_guidance
- test_advice_module.py
- checks.py
- test_ingest_pipeline.py
- test_grounding_index.py
- test_worker_queue.py
- FolderAdapter
- test_telegram_capture.py
- tasks.py
- answer.py
- bench_runtime.py
- vault.py
- support.js
- worker.py
- ingest/extract.py
- test_grounding_values.py
- test_closing_the_graph_when_the_record_write_fails_rolls_back
- Passage
- .stream
- SentenceScanner
- household.py
- ParsedPage
- test_lifecycle.py
- score.py
- test_household.py
- .load
- test_pages.py
- _pages_from
- test_eval_generate.py
- TelegramAdapter
- phrasings.py
- Any
- reminder/__init__.py
- Answer
- alert/__init__.py
- retrieve.py
- Citation
- AdviceShape
- test_startup.py
- eval/modules.py
- test_gate.py
- pipeline.py
- build_router
- HouseholdScope
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
- item-row.tsx
- values.py
- FakeCursor
- lock.ts
- build
- routes.py
- PARROT Interface Design Pack
- export-design-preview.cjs
- The Four Surfaces
- pack
- advice-consent.tsx
- devDependencies
- typing
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
- paperbrain/ollama.py
- packs/page.tsx
- main
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- build_team_tasks.py
- components.json
- _as_module_summary
- test_tax_pack.py
- contracts.py
- TelegramCapture
- test_eval_report.py
- The Lim Household, Tampines
- ADR 0007 - The graph ships before retrieval and before a checkpoint table
- Lane C - Governance and assurance
- test_contracts.py
- Core Document Catalogue (ADR 0017)
- create_app
- dependencies
- The five-lane split (five people, nine weeks, three builders)
- Data inventory: identity data, DOBs and loans
- test_rerank.py
- Roadmap phase 3 - reminders
- web/ - the PARROT interface
- The document register as ground truth
- ingest.py
- Tax and Reliefs — contract changes this pack needs
- Reminder, Alert and Tracker Registers
- ConfigurationError
- example_pack template manifest
- paperbrain/extract.py
- ingest/quarantine.py
- react
- FakeCursor
- Integration review
- corrections.py
- FakeCursor
- api/__init__.py
- paperbrain/chunk.py
- _ordered
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
- schedule.py
- PrivateCare Policy Wording Template
- alert module manifest
- test_an_unscoped_result_is_not_empty_for_the_owner
- test_a_grounding_corpus_travels_inside_its_pack
- app/layout.tsx
- The Grounding Gate
- Authoring a domain pack
- ADR 0008 - Ingestion runs on a Celery worker
- .telegram_configured
- DesignPreview evaluation harness
- Registration
- run_parrot.py
- Adversarial testing from week 7
- Writing an ADR
- Every Fact Row Cites Its Source
- _graph_for
- advice/queries.py
- eslint.config.mjs
- PARROT evaluation harness
- RagasJudge
- The autonomy statement
- api.ts
- test_installing_never_re_enables_a_pack_somebody_switched_off
- config.py
- scripts
- ADR index (0001-0018, with status)
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- _answer_events
- ClosingSpy
- The synthetic-to-real gap
- filesystem
- _dual_cited_calculation
- ingest/reindex.py
- Due
- quiet_engine
- Namespace
- SetId
- One Database
- _shared_value_calculation
- Protocol
- test_the_catalogue_declares_metrics_that_exist
- runtime/__init__.py
- corpus/__init__.py
- packs/__init__.py
- Lane E - Corpus and adversarial testing
- No code generates corpus documents
- Answer
- Alert
- setup.sh
- session-start.sh
- package.json
- date
- postcss.config.mjs
- Lane C - Governance and assurance
- parrot
- Vertical slices, not layers
- Real organisations may be named
- Decimal
- parametrize

## God Nodes (most connected - your core abstractions)
1. `Settings` - 183 edges
2. `Passage` - 90 edges
3. `ScriptedOllama` - 87 edges
4. `InstalledPack` - 84 edges
5. `AnswerGraph` - 77 edges
6. `FakeConn` - 75 edges
7. `settings()` - 75 edges
8. `client_for()` - 74 edges
9. `build_router()` - 73 edges
10. `Ollama` - 68 edges

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

## Communities (213 total, 37 thin omitted)

### Community 0 - "Ollama"
Cohesion: 0.09
Nodes (24): The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), Index a pack's published sources, and stage the values they print for a person…, ModelUnavailable, Ollama, Any, Client (+16 more)

### Community 1 - "test_hybrid.py"
Cohesion: 0.09
Nodes (28): hybrid_score(), HybridRetriever, identifiers(), prints(), Hybrid retrieval: pgvector cosine search and Postgres full-text search, fused…, The tokens in a question that look like something printed rather than said: a…, Whether the chunk prints the identifier, ignoring case and the spacing inside…, The cosine similarity, lifted to `IDENTIFIER_HIT` when the chunk prints an… (+20 more)

### Community 2 - "InstalledPack"
Cohesion: 0.04
Nodes (80): AdviceCard, AdviceWithheld, answer_system(), _closes(), ConsentRequired, Finished, _max_sentences(), The pack's own decline, signed with its disclaimer, and a question it can… (+72 more)

### Community 3 - "test_answer_graph.py"
Cohesion: 0.06
Nodes (93): Abstained, AnswerGraph, Declined, _pack_for(), One sentence that has passed the gate, with the citations it passed on. It will…, A request for a recommendation or a judgement, declined before anything is…, The pack that speaks for the best-scoring passage's document type, or None for…, Built once, asked many times. Holds no connection: retrieval does. (+85 more)

### Community 4 - "validate"
Cohesion: 0.09
Nodes (40): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+32 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.08
Nodes (69): Figure, Input, One fact or rule value a calculation was built on, carrying its own citation.…, One number a calculator produced, and the words a sentence must use to state…, _ambiguous(), _amount(), _band(), _band_label() (+61 more)

### Community 6 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.05
Nodes (64): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, MediShield Life (CPF Board), Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022 (+56 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.13
Nodes (59): Calculation, Missing, What a calculator returns when every fact and rule it needed was on file and…, What a calculator returns when a fact or a rule value it needed was not there…, calculate(), Adviser, date, assert_nothing_negative() (+51 more)

### Community 8 - "checks.py"
Cohesion: 0.10
Nodes (29): The local API. Liveness is intentionally separate from assistant readiness.…, AsyncClient, asyncio, contextlib, capture_check(), Check, collect_checks(), database_check() (+21 more)

### Community 9 - "test_ingest_pipeline.py"
Cohesion: 0.08
Nodes (53): classify(), Never raises. An unavailable model is a classification failure, so it…, extract(), Never raises. A failure is a reason, and a reason routes the document to…, Generated, FakeOllama, insurance(), iras() (+45 more)

### Community 10 - "test_grounding_index.py"
Cohesion: 0.12
Nodes (36): CaptureFixture, index_pack(), IndexReport, Any, date, Path, Upsert this pack's sources and stage the values a changed one prints. A pack…, Insert or refresh the source's row, and return its id. (+28 more)

### Community 11 - "test_worker_queue.py"
Cohesion: 0.08
Nodes (45): The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, sha256(), Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker. Celery is imported here rather…, Intake, bytes_for() (+37 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.09
Nodes (35): FolderAdapter, FolderSettings, _Pending, datetime, Path, Every file in the watched folder that is worth looking at at all., Advance the debounce by `elapsed` seconds and return the files now ready. Time…, One debounce tick, then register whatever it declared ready. (+27 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.10
Nodes (37): TelegramSettings, MockTransport, build(), FakeRegistrar, FakeTelegram, photo_update(), Any, Path (+29 more)

### Community 14 - "tasks.py"
Cohesion: 0.10
Nodes (37): queue(), The reportable line. Deliberately a rate and a count, because a rate over three…, What is waiting for a person's eyes, oldest first., Recovery, recovery_rate(), connect(), Any, Yield an open psycopg connection with autocommit off. The caller commits. (+29 more)

### Community 15 - "answer.py"
Cohesion: 0.06
Nodes (35): Claim, AdviceLog, Adviser, ConsentBook, _kind_of(), Protocol, What a calculator returns, and what the graph needs to ask consent and keep a…, Implemented by `HouseholdConsents` in `core/advice_consent.py`. (+27 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.06
Nodes (43): jinja2, find_browser_executable(), generate_documents(), Path, Project Parrot - Synthetic Document Generator for Lim Household…, Find Microsoft Edge or Google Chrome executable on Windows., platform, BenchmarkUnavailable (+35 more)

### Community 17 - "vault.py"
Cohesion: 0.09
Nodes (30): correct(), Corrected, Any, LookupError, Store what a person says this field actually says, and keep what it used to…, Safe to show: there is no fact with that id., What changed, in the words the screen will use to confirm it., UnknownFact (+22 more)

### Community 18 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 19 - "worker.py"
Cohesion: 0.16
Nodes (17): lifespan(), install_best_effort(), Installed, What `install` did, so a startup line can say it in one sentence., Install at startup without being able to stop startup. Both processes that own…, _beat_needs_its_own_process(), celery_argv(), main() (+9 more)

### Community 20 - "ingest/extract.py"
Cohesion: 0.09
Nodes (30): _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact, Extraction, find_page(), _normalise() (+22 more)

### Community 21 - "test_grounding_values.py"
Cohesion: 0.15
Nodes (35): _dropped(), _log_values(), Decimal, fixture, LogCaptureFixture, parametrize, Published values: the model reads a source, and code keeps only what the…, Assert a value was dropped, and logged with this reason. (+27 more)

### Community 22 - "test_closing_the_graph_when_the_record_write_fails_rolls_back"
Cohesion: 0.22
Nodes (8): next_kind(), The kind of the next event on the wire., Starlette never closes a body iterator a disconnected client stopped pulling.…, What the API owns when a stream is closed with the graph still parked on the…, The graph's own cleanup can fail -- for example the record insert raises -- and…, test_a_client_that_leaves_mid_explanation_still_commits_what_it_was_shown(), test_a_stream_closed_exactly_at_the_card_is_still_committed_by_the_api(), test_closing_the_graph_when_the_record_write_fails_rolls_back()

### Community 23 - "Passage"
Cohesion: 0.06
Nodes (31): DenseRetriever, NoReranker, A dense-only retriever, so the graph can be run and tested before Lane B's…, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this…, The answer graph. Router, retrieve, rerank, grounding gate, then answer or…, Passage, Protocol, What the graph needs from retrieval, stated as a contract rather than an… (+23 more)

### Community 24 - ".stream"
Cohesion: 0.08
Nodes (23): _asked(), _citations(), _either(), Event, The documents on file, narrowed to the same people the passages were., "None of the 5 policies on file is a dental plan." Written by code, never by…, "On file for Marcus Lim: MERIDIAN ASSURANCE, Private Car Insurance Policy…, The implementation. Yields each sentence once it has passed the gate, never… (+15 more)

### Community 25 - "SentenceScanner"
Cohesion: 0.06
Nodes (46): Any, Pulling finished sentences out of a JSON reply that is still being written. The…, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner (+38 more)

### Community 26 - "household.py"
Cohesion: 0.08
Nodes (47): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+39 more)

### Community 27 - "ParsedPage"
Cohesion: 0.14
Nodes (21): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, One flat list of chunks, ordinal running across the whole document., The page as `(is_heading, line)`, from the parser's structure when it has any. (+13 more)

### Community 28 - "test_lifecycle.py"
Cohesion: 0.12
Nodes (28): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor.…, What the person asked for, once. The first request wins; later ones change…, fastapi_testclient, _client(), _eventually(), _launcher(), parametrize (+20 more)

### Community 29 - "score.py"
Cohesion: 0.06
Nodes (57): _as_date(), _as_number(), cites(), _contains(), declined_in_prose(), doc_stem(), grade(), held_back() (+49 more)

### Community 30 - "test_household.py"
Cohesion: 0.08
Nodes (46): is_first_person(), `(word, relation)` when the question asks about a relation's own documents,…, Whether this question is about the person asking. `other_names` are the display…, relation_asked(), _household_scope(), MonkeyPatch, parametrize, Person (+38 more)

### Community 31 - ".load"
Cohesion: 0.12
Nodes (31): ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one…, db(), fixture, _ollama_answering(), Any, MonkeyPatch, parametrize (+23 more)

### Community 32 - "test_pages.py"
Cohesion: 0.08
Nodes (40): document_page(), base64, page_images(), Base64 page images, in page order. Empty when this document cannot be rendered.…, page_count(), PageUnavailable, _pdfium(), Any (+32 more)

### Community 33 - "_pages_from"
Cohesion: 0.14
Nodes (17): Block, DoclingParser, _kind(), _pages_from(), Docling, held at arm's length: imported on first use, and never at module…, Group Docling's items by the page they were found on. Docling's markdown export…, Docling's label, reduced to the one distinction chunking needs: is this a…, A table as lines of text, one row per line: `label: value` when a row has two… (+9 more)

### Community 34 - "test_eval_generate.py"
Cohesion: 0.08
Nodes (43): _ambiguous(), choose(), Generated, hand_written(), main(), on_file(), pool(), Namespace (+35 more)

### Community 35 - "TelegramAdapter"
Cohesion: 0.07
Nodes (36): BaseTransport, CaptureAdapter, IngestJob, datetime, Protocol, The one interface every capture channel satisfies. receive(payload, mime,…, Magic bytes first, filename suffix second, `application/octet-stream` last. A…, What a capture returns: a registered document, and whether we had seen it… (+28 more)

### Community 36 - "phrasings.py"
Cohesion: 0.20
Nodes (11): _keys(), LaneSpec, Row, How a question about a printed field is worded, per document type in…, One document type's wordings. `printed` and `spoken` each render the *thing* a…, Which register rows a lane's questions are drawn from. The task asks each…, A wording, or `None` when the row does not fill every field it needs., The spoken wording, or "Rachel's payslip" when the type has no product name of… (+3 more)

### Community 37 - "Any"
Cohesion: 0.16
Nodes (15): Measurement, by_subject(), FakeCursor, load_register(), Any, date, Every batch1 row as the facts extraction would write, through the statement it…, One member's statement must never drive another member's 15,300 cap. (+7 more)

### Community 38 - "reminder/__init__.py"
Cohesion: 0.11
Nodes (22): already_said(), current_lead(), next_window(), Overdue, Any, date, datetime, LookupError (+14 more)

### Community 39 - "Answer"
Cohesion: 0.08
Nodes (32): Answer, Cited, Every event, collected. `scripts/ask.py` and the screen ask the same question…, One sentence and the passages it was traced to. What rule 3 looks like as data.…, Answered. Asking for consent and naming what is missing are endings, not…, a_citation(), FakeGraph, TestClient (+24 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.19
Nodes (21): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), Any, date (+13 more)

### Community 41 - "retrieve.py"
Cohesion: 0.16
Nodes (19): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a…, ndarray, numpy, sqlite3, load_matrix(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.…, Return (N x D matrix of normalised embeddings, chunk ids). (+11 more)

### Community 42 - "Citation"
Cohesion: 0.25
Nodes (8): Citation, _distinct(), _input_citation(), A passage, named the way a person cites it and identified the way a link needs.…, A chip built from the `Input` itself, never from `Passage.cite()`.…, Each chip once, first use first: a sentence citing one input twice shows it…, A published value's chip: no document and no page, only who published it and…, rule_citation()

### Community 43 - "AdviceShape"
Cohesion: 0.09
Nodes (32): AdviceShape, One kind of advice question, and everything its calculator needs to answer it., date, fact_row(), FactRow, facts_for(), in_category(), _is_an_adviser() (+24 more)

### Community 44 - "test_startup.py"
Cohesion: 0.08
Nodes (37): _kill_tree(), Popen, Stop a child and everything under it, then make sure it has gone., Start `npm run dev` in `web/`, or say plainly why it could not. Three reasons…, Stop the whole npm tree, not just the wrapper that was launched. This is the…, Stop the worker and the schedule it started, not just the launcher in front of…, start_web(), stop_web() (+29 more)

### Community 45 - "eval/modules.py"
Cohesion: 0.05
Nodes (78): alert_fpr(), AlertVerdict, _day(), main(), _mark(), measure(), Measured, ModuleMetrics (+70 more)

### Community 46 - "test_gate.py"
Cohesion: 0.06
Nodes (65): passages_for(), Inputs as kind fact/rule passages (chunk_id from the ref), and the figures as…, check(), check_advice(), check_content(), check_one(), Claim, _normal() (+57 more)

### Community 47 - "pipeline.py"
Cohesion: 0.07
Nodes (33): Chunk, What is actually embedded: the prefix plus the text, matching the tsvector…, The ingestion worker. Capture registers a document; this package turns it into…, fixed(), from_facts(), _label(), Any, date (+25 more)

### Community 48 - "build_router"
Cohesion: 0.10
Nodes (31): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, What changed, in the words the screen confirms it with. `was` is returned…, The row is gone from Today. `speaks_again` is null when it will not come back.…, 202. The vision pass is slower than a page load, so it is queued and this is… (+23 more)

### Community 49 - "HouseholdScope"
Cohesion: 0.14
Nodes (20): HouseholdScope, Any, Keep the owner's passages and the household's; set aside everybody else's. A…, Keep the passages of these people and of the household; set aside everybody…, What `AnswerGraph` is handed so it can scope without holding a connection.…, scope_passages(), scope_to(), _conn_returning() (+12 more)

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 51 - "report.py"
Cohesion: 0.13
Nodes (24): _cell(), collect(), main(), _overall(), _paragraph(), Provenance, Any, Path (+16 more)

### Community 52 - "registry.py"
Cohesion: 0.08
Nodes (42): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders…, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, RuntimeError, Load the installed capability modules at runtime. The mirror of… (+34 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.15
Nodes (29): GroundingCorpus, GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records…, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError (+21 more)

### Community 54 - "packs.py"
Cohesion: 0.15
Nodes (16): DocumentTypeSpec, One kind of document the core recognises., Classification, _prompt(), Decide which of the core catalogue's document types a captured document is, or…, _schema(), Catalog, document_types() (+8 more)

### Community 55 - "cli.py"
Cohesion: 0.21
Nodes (20): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+12 more)

### Community 56 - "run.py"
Cohesion: 0.13
Nodes (26): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), _indexed(), main() (+18 more)

### Community 57 - "ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.15
Nodes (20): Code-written absence sentence: 'None of the N policies on file is a dental plan.', ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic, The advise route intent returns the pack's advice_decline, answering.categories: ordered whole-word rules over one printed field, Category filter applied before the keep-6 cut, answering.exclusions: headings under which a cover claim is not believed, Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration) (+12 more)

### Community 58 - "build.py"
Cohesion: 0.09
Nodes (29): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering…, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why the catalogue cannot supply `field` from every one of `doc_types`, or None., Whether any document type in the catalogue declares `field`., An advice shape that names a missing role or key fails at load time. Caught…, Every core document type, field and category this pack names exists, or…, A compared field no document type of the shape declares can never be printed.… (+21 more)

### Community 59 - "Any"
Cohesion: 0.13
Nodes (16): db(), _document(), _facts_tuple(), FakeCursor, Any, date, datetime, fixture (+8 more)

### Community 60 - "item-row.tsx"
Cohesion: 0.16
Nodes (13): SourceChip(), stripTrailingPage(), ADR-0016, countdown(), detail(), figure(), ItemRow(), longDate() (+5 more)

### Community 61 - "values.py"
Cohesion: 0.08
Nodes (31): _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), number_tokens(), _pack(), parse_value() (+23 more)

### Community 62 - "FakeCursor"
Cohesion: 0.12
Nodes (6): _Connected, FakeConn, FakeCursor, Any, FakeConn, A recording fake in the house style (see `tests/test_api.py`'s `FakeConn`):…

### Community 63 - "lock.ts"
Cohesion: 0.07
Nodes (46): ref_node_crypto, dynamic, GET(), grant(), POST(), runtime, ALLOWED, Context (+38 more)

### Community 64 - "build"
Cohesion: 0.11
Nodes (22): HouseholdConsents, `core.graph.advice.ConsentBook` over a live connection, for the graph to ask…, HouseholdAdviceLog, The record of every advised or withheld answer (ADR 0016). `advice_records`…, `core.graph.advice.AdviceLog` over a live connection. `basis` is dumped with…, AdviceRecord, Every advised or withheld answer's full basis, so it can be reconstructed later…, HouseholdInventory (+14 more)

### Community 65 - "routes.py"
Cohesion: 0.08
Nodes (54): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, AskRequest, AskResponse, CloseRequest, ConfirmNameRequest (+46 more)

### Community 66 - "PARROT Interface Design Pack"
Cohesion: 0.09
Nodes (30): Not finding you is an answer (first-person abstention), The readiness check verifies the model the way it will be used (one pair scored), Capture is where the user already is, Citation chips are the trust surface, Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Nothing moves without a reason (motion specification) (+22 more)

### Community 67 - "export-design-preview.cjs"
Cohesion: 0.11
Nodes (18): ref_node_fs, bundle(), classes, css, cssFile, domId, fs, ids (+10 more)

### Community 68 - "The Four Surfaces"
Cohesion: 0.13
Nodes (16): Packs and Modules May Not Import web/ or api/, The FastAPI Application, The API Surface, GET /api/today Never Marks Anything Notified, apply, Auto-Redirect to Today Once Ready, check, draw (+8 more)

### Community 69 - "pack"
Cohesion: 0.05
Nodes (54): _Answering, The event stream one request is sending, held where the request's cleanup can…, Close the answer stream when the request ends, whatever ended it. Requires…, Conn, Categories, _conversation(), The question made whole, and said in the documents' words. See…, holdings() (+46 more)

### Community 70 - "advice-consent.tsx"
Cohesion: 0.24
Nodes (13): ConsentPrompt(), agree(), settle(), AdviceConsentSection(), fetchConsents(), withdraw(), Load, STATUS (+5 more)

### Community 71 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 72 - "typing"
Cohesion: 0.11
Nodes (28): argparse, collections_abc, The watched-folder capture adapter. A person drops a scan into a folder and it…, A person's approval, standing between a model's extraction and any calculator…, Run the capture loops in background threads, beside the local server. This is…, DatabaseUnavailable, RuntimeError, One place that opens a connection to the one database. `Settings.database_url`… (+20 more)

### Community 73 - "Hybrid Retrieval: Dense Plus Full-Text"
Cohesion: 0.18
Nodes (11): No New Runtime Dependency Without an ADR, Never Generate SQL at Runtime, baseline.py Is Disposable and Never a Measurement, ports.py, the Seam With Lane B, bge-reranker-v2-m3 Cross-Encoder, 40 Down to 6, Hybrid Retrieval: Dense Plus Full-Text, Reciprocal Rank Fusion, k=60, The Household's Eleven Policies (+3 more)

### Community 74 - "scope.py"
Cohesion: 0.23
Nodes (16): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Whose question is this, and whose documents may answer it. "What is my term… (+8 more)

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.17
Nodes (19): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), The owner is a row, not a config value baked at install, people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), A resolved person is shown as a chip, like a citation, The roster is derived from documents, then confirmed (+11 more)

### Community 76 - "test_advice_core.py"
Cohesion: 0.12
Nodes (32): Channel, current(), grant(), _latest(), NoOwner, Any, RuntimeError, The owner's consent to a pack's advice, append-only (ADR 0016). Consent is the… (+24 more)

### Community 77 - "test_modules.py"
Cohesion: 0.17
Nodes (26): AlertConfig, Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), Everything inside a lead window that has not already been said for that window.…, sweep(), FakeConn, obligation_row(), datetime (+18 more)

### Community 78 - "today/page.tsx"
Cohesion: 0.05
Nodes (46): dynamic, HouseholdPage(), metadata, runtime, AppLayout(), dynamic, isUrgent(), metadata (+38 more)

### Community 79 - "test_eval_harness.py"
Cohesion: 0.09
Nodes (35): The reference answer Ragas judges recall and precision against. A fact…, reference_for(), Expected, load_set(), MalformedQuestion, Any, SetId, ValueError (+27 more)

### Community 80 - "preview.tsx"
Cohesion: 0.10
Nodes (17): metadata, answers, DesignPreview(), Direction, directions, Item, items, web_app_design_preview_preview_module (+9 more)

### Community 81 - "extract_values"
Cohesion: 0.15
Nodes (18): extract_values(), _prompt(), Every value the source prints for these keys, kept only when its passage prints…, _long_text(), Any, Exception, Generated, Returns the replies the test wrote, in order, then an empty list of values. A… (+10 more)

### Community 82 - "Two-stage quarantine with a vision-language second pass"
Cohesion: 0.12
Nodes (19): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Two-stage quarantine with a vision-language second pass, Batch 4: the deliberately hard documents, A full policy wording registers as policy_schedule, Task: review every quarantined document and label the failure, Task: sign off the capture-to-database path against the data inventory, Measurement is owned separately from the engine (+11 more)

### Community 83 - "Any"
Cohesion: 0.11
Nodes (8): advice_card(), ConsentCursor, Fails, FakeCursor, Any, The parameters of the one statement containing `needle`. Fails loudly if it…, Yields `before`, then raises. `ask` raises at once., Remembers what `grant` or `withdraw` inserted, so the next read of the latest…

### Community 84 - "paperbrain/ollama.py"
Cohesion: 0.17
Nodes (10): answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, Ollama, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.…, Batch embeddings. Falls back to the legacy endpoint on old servers., Hit (+2 more)

### Community 85 - "packs/page.tsx"
Cohesion: 0.06
Nodes (29): ADR-0017, next, dynamic, metadata, PacksPage(), runtime, DocumentPage(), dynamic (+21 more)

### Community 86 - "main"
Cohesion: 0.12
Nodes (21): approve(), pending(), PendingValue, Any, date, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it., Every value still waiting for review, oldest first, optionally for one pack. (+13 more)

### Community 87 - "ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.16
Nodes (20): ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, The adult rule: advice is withheld for a person under 21 or a child with no date of birth on file, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel), Advice graph flow: shape match, subject resolution, consent, AdviceCard, explain, advice_records keeps each answer's full basis, PackManifest.advice shapes (gap, remaining_room, keep_or_surrender, compare_own, compare_market, estimate_saving), Advice.review: one question runs every shape at once (+12 more)

### Community 88 - "build_team_tasks.py"
Cohesion: 0.25
Nodes (10): collections, csv, difflib, main(), Path, Generate each member's task list from the master task CSV. python…, _read_rows(), _render() (+2 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "_as_module_summary"
Cohesion: 0.25
Nodes (8): PacksResponse, _as_module_summary(), _as_pack_summary(), packs(), set_module(), set_pack(), ModuleSummary, PackSummary

### Community 91 - "test_tax_pack.py"
Cohesion: 0.20
Nodes (16): _basis(), _latest(), _matched(), _published(), FactRow, parametrize, The tax pack's advice, run on batch 1's own SRS statements and Notices of…, The shape id the answer graph picks for a question with both packs enabled,… (+8 more)

### Community 92 - "contracts.py"
Cohesion: 0.11
Nodes (27): Advice, Answering, Category, Exclusions, FactInput, FieldSpec, Grounding, Guardrails (+19 more)

### Community 93 - "TelegramCapture"
Cohesion: 0.13
Nodes (13): RuntimeError, Safe to show: never contains the token., TelegramUnavailable, attribution(), Any, A daemon thread that long-polls the Telegram bot until `stop()` or process…, Begin polling. Returns False, with a logged reason, when it cannot or should…, One long poll. A failure waits rather than hammering the API with the same… (+5 more)

### Community 94 - "test_eval_report.py"
Cohesion: 0.13
Nodes (28): extraction_by_type(), extraction_f1(), FactRow, _outcomes(), Collection, One row of the `facts` table, as the harness reads it: which document, which…, `(doc_id, doc_type, field, (tp, fp, fn))` for every register cell that was…, Metric 6, micro-averaged over every scored field: `all`, then one entry per… (+20 more)

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
Nodes (59): copy, PackManifest, A domain pack, authored as one YAML file: grounding, persona, answering and…, pydantic, _advised(), _checked(), _compare_without_an_ordering(), _compares_an_undeclared_field() (+51 more)

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.10
Nodes (21): The Purely Additive Migration Exception, Contracts and Migrations Are Their Own PR, Sources of Truth Generate Their Outputs, Snooze Means Not Until This Gets More Urgent, The Three Things Agents Get Wrong Here, Generated Files Committed Alongside Their Source, benefit_illustration Document Type, birth_certificate Document Type (+13 more)

### Community 100 - "create_app"
Cohesion: 0.36
Nodes (5): create_app(), checks(), ready(), setup(), system_status()

### Community 101 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 102 - "The five-lane split (five people, nine weeks, three builders)"
Cohesion: 0.09
Nodes (30): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The domain pack manifest, The expansion model: two axes, not one list, The golden set: answerable, hard negatives, adversarial, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build (+22 more)

### Community 103 - "Data inventory: identity data, DOBs and loans"
Cohesion: 0.17
Nodes (15): Data inventory: identity data, DOBs and loans, The lock is a screen lock, not encryption, next dev binds every interface, not loopback, Telegram capture route and delete-at-source, What crosses a boundary, Governance artefact set, Write unverified rather than assert, The final ILP report (+7 more)

### Community 104 - "test_rerank.py"
Cohesion: 0.07
Nodes (43): CrossEncoderReranker, device_name(), load(), passage_text(), Any, The cross-encoder reranker: forty candidates read against the question, six…, One relevance logit per text, higher is better. Batched so forty passages is a…, Say it, once per process. A passage cut at the cap is scored on its first part… (+35 more)

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
Cohesion: 0.27
Nodes (11): pack(), discover(), embed_chunks(), guess_date(), guess_type(), ingest_file(), IngestResult, Path (+3 more)

### Community 109 - "Tax and Reliefs — contract changes this pack needs"
Cohesion: 0.40
Nodes (4): 1. A deduction multiplier on `estimate_saving`, 2. Limiting a fact input to one year, Not a contract change: parent relief, Tax and Reliefs — contract changes this pack needs

### Community 110 - "Reminder, Alert and Tracker Registers"
Cohesion: 0.18
Nodes (15): Passport Uses date_of_expiry So policy_expiry Does Not Fire, filing_deadline Reminder, maturity_date Is Not expiry_date, passport Document Type, passport_expiry Reminder, policy_expiry Reminder, policy_schedule Document Type, Reminder, Alert and Tracker Registers (+7 more)

### Community 111 - "ConfigurationError"
Cohesion: 0.11
Nodes (24): _chat_ids(), ConfigurationError, _flag(), _folder(), local_url(), _port(), _positive(), Path (+16 more)

### Community 112 - "example_pack template manifest"
Cohesion: 0.18
Nodes (14): I explain the renewal notice, I do not renew policies, Autonomy statement, ISO/IEC 22989 stages versus 5338 processes, never_acts as a machine-checked flag, Grounding corpora now live inside packs, advice module manifest, example_pack template manifest, example_room advice shape (+6 more)

### Community 113 - "paperbrain/extract.py"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 114 - "ingest/quarantine.py"
Cohesion: 0.18
Nodes (16): blocked_reasons(), forget(), Any, Path, ValueError, QuarantinedDocument, The second stage of quarantine: the page image, read by the vision-language…, Per document: `None` when the image pass can run, or the sentence saying why it… (+8 more)

### Community 115 - "react"
Cohesion: 0.05
Nodes (34): lucide-react, react, dynamic, runtime, Motion(), ROWS, INKS, metadata (+26 more)

### Community 116 - "FakeCursor"
Cohesion: 0.20
Nodes (3): FakeCursor, Any, FakeConn

### Community 117 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 118 - "corrections.py"
Cohesion: 0.28
Nodes (8): _columns(), CorrectionRejected, date, Decimal, ValueError, A person fixing a field the extractor got wrong. This is the one place in the…, `(value_text, value_num, value_date)` — exactly one of them set. The declared…, Safe to show: the value does not fit what this field is declared to be.

### Community 121 - "paperbrain/chunk.py"
Cohesion: 0.36
Nodes (6): itertools, Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks. Paperwork is short and…, _split_page()

### Community 122 - "_ordered"
Cohesion: 0.33
Nodes (6): _Value, Hashable, _order_key(), _ordered(), One sortable key for a number, a date or a word, so a ranking never compares…, Keys ranked by value in the stated order, ties broken by name so a ranking is…

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
Cohesion: 0.40
Nodes (5): VaultResponse, _as_vault_document(), one_document(), vault_documents(), VaultDocument

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
Nodes (41): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+33 more)

### Community 144 - "Settings"
Cohesion: 0.06
Nodes (140): Evidence gathered, floor cleared, the model is now writing. Nothing is claimed…, Reading, Settings, client(), client_for(), conn(), consent(), ConsentConn (+132 more)

### Community 145 - "schedule.py"
Cohesion: 0.15
Nodes (17): build(), Any, The one Celery application, built from `Settings`. Every setting here is a…, Construct the Celery application. Imported lazily by callers so that nothing…, beat_schedule(), cron_expressions(), crontab_from(), manifest() (+9 more)

### Community 146 - "PrivateCare Policy Wording Template"
Cohesion: 0.31
Nodes (9): PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Gemini prompt bank for identity specimens, The Lim household canon, Republic of Xinkapow (+1 more)

### Community 147 - "alert module manifest"
Cohesion: 0.28
Nodes (9): Days without recorded cover tile, alert_fpr, obligation_precision, Module manifest template, Quoted "on" key in YAML 1.1, alert module manifest, Modules read typed rows, never chunks, reminder module manifest (+1 more)

### Community 149 - "test_a_grounding_corpus_travels_inside_its_pack"
Cohesion: 0.50
Nodes (4): Path, A downloaded pack carries its sources, so no corpus is left at the repository…, test_a_grounding_corpus_travels_inside_its_pack(), test_every_grounding_corpus_declares_its_provenance()

### Community 150 - "app/layout.tsx"
Cohesion: 0.20
Nodes (8): next-themes, web_app_globals, figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 151 - "The Grounding Gate"
Cohesion: 0.29
Nodes (8): never_acts: True in Every Pack Manifest, The Core Answering Layer, The Answer Path: route, retrieve, rerank, ground, answer or abstain, The Grounding Gate, The Score Floor the Gate Reads, Kidney Stones: Inpatient Covered, Outpatient ESWL Excluded, Ask Screen, Try to Make It Lie: the Abstention Test

### Community 152 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 153 - "ADR 0008 - Ingestion runs on a Celery worker"
Cohesion: 0.39
Nodes (8): ADR 0005 - The watched folder is polled, not subscribed to, Stability debounce with injected time, ADR 0008 - Ingestion runs on a Celery worker, The queue carries a digest, not the document, The ingestion worker, START.cmd launcher, Telegram capture, The watched inbox folder

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (8): parrot-sweep shimmer animation, Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, An answer with the page it came from, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "Registration"
Cohesion: 0.09
Nodes (28): Dispatcher, Inline, Protocol, What happens to a document between "these bytes are registered" and "this…, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Send (+20 more)

### Community 157 - "run_parrot.py"
Cohesion: 0.12
Nodes (21): Load the generator and the embedder before the first question, and record the…, warm_models(), broker_available(), Whether Redis answers. Not whether a worker is listening —…, main(), open_browser(), parse_args(), port_answers() (+13 more)

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
Cohesion: 0.22
Nodes (10): Claim, One sentence and the passages it was traced to. Never emitted without…, _as_response(), ask(), ask_stream(), _graph_for(), _history(), One `Answer` to one of the shapes a client has to handle. (+2 more)

### Community 164 - "eslint.config.mjs"
Cohesion: 0.33
Nodes (5): @eslint/eslintrc, ref_node_path, ref_node_url, compat, eslintConfig

### Community 165 - "PARROT evaluation harness"
Cohesion: 0.38
Nodes (7): abstention_rate, PARROT evaluation harness, Set A, answerable, Set B, hard negatives, Set C, adversarial, The golden question sets, must_cite_page from field_pages

### Community 166 - "RagasJudge"
Cohesion: 0.32
Nodes (6): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts(), Ragas 0.4 metrics through Ollama's OpenAI-compatible endpoint. Imported lazily…

### Community 167 - "The autonomy statement"
Cohesion: 0.29
Nodes (7): The autonomy statement, Governance claims traced to enforcement points, IMDA mappings and autonomy statement artefact, The facts table as an extension point, Constraint: fully offline, Explicitly not doing: cloud, hosted vectors, autonomous spending, Roadmap phase 2 - facts

### Community 168 - "api.ts"
Cohesion: 0.24
Nodes (9): SourcePanel(), DocumentDetail(), when(), Field(), format(), isNumeric(), CorrectionResponse, pageImage() (+1 more)

### Community 171 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

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
Cohesion: 0.11
Nodes (21): ErrorEvent, The stream broke after it began. A client cannot read an HTTP status by then., _answer_events(), today(), _cite(), connection(), _link(), Any (+13 more)

### Community 177 - "ClosingSpy"
Cohesion: 0.33
Nodes (3): ClosingSpy, Wraps an event generator to record whether something called `.close()` on it,…, spying()

### Community 179 - "The synthetic-to-real gap"
Cohesion: 0.40
Nodes (5): The 40-document redacted holdout, The synthetic-to-real gap, Consent and redaction protocol, Task: write the PDPA position on using synthetic data, Task: evaluation run 3 plus the holdout run

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 182 - "ingest/reindex.py"
Cohesion: 0.13
Nodes (11): indexed(), IndexedDocument, Any, RuntimeError, Rebuild a document's chunks and vectors without reading it again for facts.…, Safe to show: names what went wrong, never what the document says., Parse, chunk and embed one document again, and replace its chunks. Returns how…, reindex_document() (+3 more)

### Community 184 - "quiet_engine"
Cohesion: 0.50
Nodes (4): fixture, MonkeyPatch, quiet_engine(), No real probes, no startup writes, no deliberate pause before exiting. The…

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
- **369 isolated node(s):** `_Formatter`, `Action`, `Stage`, `DependencyCheck`, `Phase` (+364 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1709 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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