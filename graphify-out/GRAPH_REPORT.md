# Graph Report - igd-capstone-2026  (2026-10-03)

## Corpus Check
- 307 files · ~704,491 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 29 file(s) not represented in the graph (top: (none) 11, .csv 5, .jsonl 3)

## Summary
- 4476 nodes · 11165 edges · 215 communities (186 shown, 29 thin omitted)
- Extraction: 90% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1059 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `932ab332`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- answer.py
- test_hybrid.py
- ScriptedOllama
- AnswerGraph
- validate
- advice/__init__.py
- Provenance register for corpus sg_protection_guidance
- test_advice_module.py
- run.py
- extract
- test_grounding_index.py
- test_worker_queue.py
- FolderAdapter
- test_telegram_capture.py
- Ollama
- run_parrot.py
- bench_runtime.py
- vault.py
- support.js
- checks.py
- test_ingest_pipeline.py
- test_grounding_values.py
- Settings
- registry.py
- InstalledPack
- SentenceScanner
- household.py
- ModelUnavailable
- test_lifecycle.py
- score.py
- test_household.py
- .load
- test_pages.py
- extract_values
- test_eval_generate.py
- TelegramAdapter
- Registration
- Any
- reminder/__init__.py
- test_api.py
- alert/__init__.py
- retrieve.py
- sse
- api.ts
- ._client
- test_answer_graph.py
- test_gate.py
- _pages_from
- build_router
- HouseholdScope
- compilerOptions
- FakeConn
- State
- test_grounding.py
- FakeOllama
- cli.py
- blocked_reasons
- ADR index (0001-0018, with status)
- build.py
- Any
- answer.tsx
- _check
- settings.py
- lock.ts
- dependencies
- routes.py
- PARROT Interface Design Pack
- export-design-preview.cjs
- The Four Surfaces
- pack
- advice-consent.tsx
- devDependencies
- IngestJob
- Hybrid Retrieval: Dense Plus Full-Text
- scope.py
- ADR 0011: The household is people and aliases, and the owner is one of them
- FakeConn
- test_modules.py
- today/page.tsx
- tokens/page.tsx
- preview.tsx
- test_advice_core.py
- Two-stage quarantine with a vision-language second pass
- Any
- Ollama
- TelegramUnavailable
- main
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- test_both_ask_endpoints_hand_the_graph_the_same_advice_ports
- components.json
- item-row.tsx
- test_tax_pack.py
- contracts.py
- Passage
- AdviceShape
- The Lim Household, Tampines
- ADR 0007 - The graph ships before retrieval and before a checkpoint table
- Lane C - Governance and assurance
- test_contracts.py
- Core Document Catalogue (ADR 0017)
- _Answering
- split_sections
- The five-lane split (five people, nine weeks, three builders)
- Data inventory: identity data, DOBs and loans
- test_rerank.py
- Roadmap phase 3 - reminders
- web/ - the PARROT interface
- The document register as ground truth
- ingest.py
- pytest
- Reminder, Alert and Tracker Registers
- FakeCursor
- example_pack template manifest
- paperbrain/extract.py
- _closes
- react
- _answer_events
- Integration review
- FakeCursor
- test_registration.py
- main.py
- TelegramCapture
- next
- ADR 0002 - One PostgreSQL instance for everything
- The deliberately naive retrieval baseline
- Running the evaluation harness
- _page_of_examples
- create_app
- The case for synthetic evaluation data
- Domain pack
- Any
- Filling the corpus register
- Writing a governance artefact
- Two-Stage Quarantine With a Vision Second Pass
- Fill the Register Before Generating Documents
- Where Things Live
- Policy schedule HTML template
- sweep
- page_pixels
- PaperBrain
- ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts
- chat/route.ts
- test_a_core_document_stays_enabled_when_every_pack_is_off
- scripts
- test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them
- schedule.py
- PrivateCare Policy Wording Template
- alert module manifest
- test_reindexing_replaces_chunks_and_leaves_facts_alone
- FakeCursor
- app/layout.tsx
- The Grounding Gate
- Authoring a domain pack
- ADR 0008 - Ingestion runs on a Celery worker
- Cursor
- DesignPreview evaluation harness
- build_team_tasks.py
- test_startup.py
- Adversarial testing from week 7
- Writing an ADR
- AdviceRecord
- Every Fact Row Cites Its Source
- HouseholdAdviceLog
- check
- unprinted_numbers
- PARROT evaluation harness
- RagasJudge
- The autonomy statement
- FolderCapture
- test_the_inventory_always_reads_core_documents
- Missing
- printed_date
- DoclingParser
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- _as_consent
- page_count
- The synthetic-to-real gap
- filesystem
- .ask
- Due
- quiet_engine
- FakeTelegram
- test_an_install_without_the_renderer_says_so
- eslint.config.mjs
- One Database
- _dual_cited_calculation
- _meets_calculation
- _shared_value_calculation
- runtime/__init__.py
- corpus/__init__.py
- packs/__init__.py
- Lane E - Corpus and adversarial testing
- No code generates corpus documents
- test_page_numbers_are_the_ones_a_citation_says
- Alert
- setup.sh
- session-start.sh
- package.json
- three_pages
- postcss.config.mjs
- Lane C - Governance and assurance
- parrot
- Vertical slices, not layers
- Real organisations may be named
- advice/queries.py
- _gap_shared_value_calculation
- test_an_unscoped_result_is_not_empty_for_the_owner

## God Nodes (most connected - your core abstractions)
1. `Settings` - 185 edges
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
- `Work in this order, stopping for the author at each step` --references--> `money()`  [INFERRED]
  .claude/skills/authoring-a-domain-pack/SKILL.md → modules/advice/__init__.py
- `2. Limiting a fact input to one year` --references--> `FactInput`  [INFERRED]
  packs/iras_tax/CONTRACT_REQUESTS.md → core/contracts.py
- `How to give the feedback` --references--> `FieldSpec`  [INFERRED]
  .claude/skills/integration-review/SKILL.md → core/contracts.py
- `Explicitly not doing: cloud, hosted vectors, autonomous spending` --semantically_similar_to--> `The autonomy statement`  [INFERRED] [semantically similar]
  tools/paperbrain/docs/ROADMAP.md → team/siew/README.md
- `Task: hybrid retrieval with reciprocal rank fusion` --semantically_similar_to--> `Hybrid retrieval, not embeddings alone`  [INFERRED] [semantically similar]
  team/yew-mun/tasks.md → tools/paperbrain/docs/ARCHITECTURE.md

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

## Communities (215 total, 29 thin omitted)

### Community 0 - "answer.py"
Cohesion: 0.03
Nodes (86): collections, collections_abc, The one interface every capture channel satisfies. receive(payload, mime,…, Magic bytes first, filename suffix second, `application/octet-stream` last. A…, sniff_mime(), The watched-folder capture adapter. A person drops a scan into a folder and it…, The Telegram capture adapter. Same interface as the folder: `receive(payload,…, HouseholdConsents (+78 more)

### Community 1 - "test_hybrid.py"
Cohesion: 0.10
Nodes (27): hybrid_score(), HybridRetriever, identifiers(), prints(), The tokens in a question that look like something printed rather than said: a…, Whether the chunk prints the identifier, ignoring case and the spacing inside…, The cosine similarity, lifted to `IDENTIFIER_HIT` when the chunk prints an…, Implements `core.graph.ports.Retriever`. Built where the connection is, like… (+19 more)

### Community 2 - "ScriptedOllama"
Cohesion: 0.07
Nodes (61): AdviceCard, AdviceWithheld, ConsentRequired, Declined, Finished, A request for a recommendation or a judgement, declined before anything is…, Everything that is only knowable once the last sentence is in. `quarantined`…, Advice was asked for and the owner has not agreed to this pack's current… (+53 more)

### Community 3 - "AnswerGraph"
Cohesion: 0.17
Nodes (30): AnswerGraph, One sentence that has passed the gate, with the citations it passed on. It will…, Built once, asked many times. Holds no connection: retrieval does., Sentence, FakeInventory, FixedRetriever, holding(), insurance() (+22 more)

### Community 4 - "validate"
Cohesion: 0.09
Nodes (41): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+33 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.08
Nodes (72): Figure, Input, One fact or rule value a calculation was built on, carrying its own citation.…, One number a calculator produced, and the words a sentence must use to state…, _Value, Hashable, _ambiguous(), _amount() (+64 more)

### Community 6 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.05
Nodes (64): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, MediShield Life (CPF Board), Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022 (+56 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.14
Nodes (55): Calculation, What a calculator returns when every fact and rule it needed was on file and…, calculate(), assert_nothing_negative(), basis(), fact(), figures_of(), _gap_basis() (+47 more)

### Community 8 - "run.py"
Cohesion: 0.06
Nodes (60): Cited, One sentence and the passages it was traced to. What rule 3 looks like as data.…, The last question's contexts and candidate count, then a clean slate., Each question on its own thread, so no answer is a follow-up to the one before., Recorder, trace_all(), The evaluation harness. `python -m eval.run` is the entry point;…, _chosen() (+52 more)

### Community 9 - "extract"
Cohesion: 0.17
Nodes (20): extract(), Never raises. A failure is a reason, and a reason routes the document to…, insurance(), iras(), Any, fixture, test_a_date_that_cannot_be_read_still_quarantines(), test_a_document_is_titled_by_the_string_fields_its_pack_declares() (+12 more)

### Community 10 - "test_grounding_index.py"
Cohesion: 0.08
Nodes (44): CaptureFixture, GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records…, SourceText, index_pack(), IndexReport, Any, date (+36 more)

### Community 11 - "test_worker_queue.py"
Cohesion: 0.10
Nodes (32): The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, sha256(), Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker. Celery is imported here rather…, index_folder(), Path (+24 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.21
Nodes (23): FolderAdapter, Satisfies `CaptureAdapter`. Holds no database handle — it is given a…, FakeRegistrar, datetime, fixture, parametrize, Path, The watched folder: debounce, mime sniffing, and what happens the second time.… (+15 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.20
Nodes (24): build(), photo_update(), Path, Telegram capture: what arrives, what is answered, and what is written where. No…, A photograph as Telegram actually sends one: the same image in several sizes.…, The claim the queued dispatcher depends on. See `core/ingest/source.py`., 409 is the one poll failure that never clears by itself, so it must not read as…, Silently reading "everyone" out of a typo would be the opposite of what was… (+16 more)

### Community 14 - "Ollama"
Cohesion: 0.05
Nodes (99): argparse, FolderSettings, Dispatcher, Inline, Given a registered document, arrange for it to be read. Says what it arranged., Run the pipeline here and now, and report what it decided., queue(), Send the pages as images and try the whole pack pipeline again on what comes… (+91 more)

### Community 15 - "run_parrot.py"
Cohesion: 0.09
Nodes (32): Load the generator and the embedder before the first question, and record the…, warm_models(), broker_available(), Whether Redis answers. Not whether a worker is listening —…, _kill_tree(), main(), open_browser(), parse_args() (+24 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.05
Nodes (55): jinja2, find_browser_executable(), generate_documents(), Path, Project Parrot - Synthetic Document Generator for Lim Household…, Find Microsoft Edge or Google Chrome executable on Windows., platform, BenchmarkUnavailable (+47 more)

### Community 17 - "vault.py"
Cohesion: 0.06
Nodes (39): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+31 more)

### Community 18 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 19 - "checks.py"
Cohesion: 0.11
Nodes (29): AsyncClient, asyncio, device_name(), load(), Any, The tokenizer, the model and the device it sits on, loaded once per process.…, One relevance logit per text, higher is better. Batched so forty passages is a…, score_pairs() (+21 more)

### Community 20 - "test_ingest_pipeline.py"
Cohesion: 0.11
Nodes (25): _date_renderings(), find_page(), _normalise(), The first page whose text contains this value. None means no page supports it.…, Every common way a household document prints this date, given it as YYYY-MM-DD.…, Block, parse(), The one call the pipeline makes. An unhandled mime type quarantines rather than… (+17 more)

### Community 21 - "test_grounding_values.py"
Cohesion: 0.16
Nodes (33): LogCaptureFixture, _dropped(), _log_values(), Decimal, fixture, parametrize, Published values: the model reads a source, and code keeps only what the…, Assert a value was dropped, and logged with this reason. (+25 more)

### Community 22 - "Settings"
Cohesion: 0.10
Nodes (46): Whether Telegram capture should start. An unset token means "not this…, Settings, client_for(), consent(), ConsentConn, inbox(), pack_row(), parametrize (+38 more)

### Community 23 - "registry.py"
Cohesion: 0.07
Nodes (48): lifespan(), ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders…, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, RuntimeError (+40 more)

### Community 24 - "InstalledPack"
Cohesion: 0.07
Nodes (31): Abstained, _advice_basis(), answer_system(), _citations(), _input_citation(), _max_sentences(), _numbered(), Any (+23 more)

### Community 25 - "SentenceScanner"
Cohesion: 0.10
Nodes (28): Any, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner, drip() (+20 more)

### Community 26 - "household.py"
Cohesion: 0.09
Nodes (39): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+31 more)

### Community 27 - "ModelUnavailable"
Cohesion: 0.03
Nodes (102): A person fixing a field the extractor got wrong. This is the one place in the…, Chunk, chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own… (+94 more)

### Community 28 - "test_lifecycle.py"
Cohesion: 0.12
Nodes (27): Parrot's local HTTP interface., Lifecycle, What the person asked for, once. The first request wins; later ones change…, fastapi_testclient, _client(), _eventually(), _launcher(), parametrize (+19 more)

### Community 29 - "score.py"
Cohesion: 0.06
Nodes (48): Trace, _as_date(), _as_number(), cites(), _contains(), doc_stem(), extraction_f1(), F1 (+40 more)

### Community 30 - "test_household.py"
Cohesion: 0.08
Nodes (46): is_first_person(), `(word, relation)` when the question asks about a relation's own documents,…, Whether this question is about the person asking. `other_names` are the display…, relation_asked(), _household_scope(), MonkeyPatch, parametrize, Person (+38 more)

### Community 31 - ".load"
Cohesion: 0.13
Nodes (29): ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one…, _ollama_answering(), Any, MonkeyPatch, parametrize, Path, Setup diagnostics use controlled service responses, never live household… (+21 more)

### Community 32 - "test_pages.py"
Cohesion: 0.21
Nodes (16): document_page(), base64, PageUnavailable, LookupError, Safe to show a person: there is no such page, or this file cannot be drawn., `(bytes, media type)` for one page, one-based. An image document is returned…, render_page(), Drawing one page of one document. The thing worth protecting here is the page… (+8 more)

### Community 33 - "extract_values"
Cohesion: 0.18
Nodes (19): extract_values(), _prompt(), Every value the source prints for these keys, kept only when its passage prints…, _long_text(), Any, Exception, Returns the replies the test wrote, in order, then an empty list of values. A…, A truncated or non-JSON reply is an outage: the section was never actually… (+11 more)

### Community 34 - "test_eval_generate.py"
Cohesion: 0.09
Nodes (30): choose(), Generated, generic(), main(), _named(), phrase(), on_file(), pool() (+22 more)

### Community 35 - "TelegramAdapter"
Cohesion: 0.14
Nodes (17): _attachment(), _pixels(), Any, Client, datetime, Response, Confirm the token works before anything else is attempted., One `getUpdates` round. Returns what was captured; replies with what was… (+9 more)

### Community 36 - "Registration"
Cohesion: 0.27
Nodes (4): Intake, An already-indexed document is not read again. Re-reading it would burn a…, The row as it now stands, plus whether this call is the one that created it., Registration

### Community 37 - "Any"
Cohesion: 0.13
Nodes (17): Measurement, by_subject(), db(), FakeCursor, load_register(), Any, date, fixture (+9 more)

### Community 38 - "reminder/__init__.py"
Cohesion: 0.10
Nodes (24): already_said(), current_lead(), next_window(), Overdue, Any, date, datetime, LookupError (+16 more)

### Community 39 - "test_api.py"
Cohesion: 0.09
Nodes (35): Answer, Answered. Asking for consent and naming what is missing are endings, not…, Asks, Protocol, The one method of `AnswerGraph` the harness uses. A test supplies a fake., client(), FakeGraph, TestClient (+27 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.21
Nodes (19): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), Any, date (+11 more)

### Community 41 - "retrieve.py"
Cohesion: 0.14
Nodes (22): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a…, ndarray, numpy, sqlite3, load_matrix(), pack(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.… (+14 more)

### Community 42 - "sse"
Cohesion: 0.09
Nodes (37): Citation, _distinct(), A passage, named the way a person cites it and identified the way a link needs.…, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed…, Each chip once, first use first: a sentence citing one input twice shows it…, Reading, a_citation(), advice_card() (+29 more)

### Community 43 - "api.ts"
Cohesion: 0.07
Nodes (35): DocumentPage(), dynamic, metadata, runtime, RELATION_CHOICES, Place, PLACES, DocumentDetail() (+27 more)

### Community 44 - "._client"
Cohesion: 0.12
Nodes (11): Any, Client, A question, embedded the way the model was trained to embed a search query., Passages as `(title, text)`, embedded the way the model was trained to embed a…, Load the generator and the embedder now, and say where the generator landed. An…, Generate against a JSON schema. This is how extraction is held to a pack's…, The same constrained generation, yielded as it is written. Identical body to…, Whether this embedding model expects `QUERY_PROMPT` and `DOCUMENT_PROMPT`. (+3 more)

### Community 45 - "test_answer_graph.py"
Cohesion: 0.06
Nodes (49): _pack_for(), Every removable passage mention, removed. One removal can expose the next — in…, The pack that speaks for the best-scoring passage's document type, or None for…, Refused, _without_one_round_of_passage_numbers(), _without_passage_numbers(), build(), events() (+41 more)

### Community 46 - "test_gate.py"
Cohesion: 0.12
Nodes (33): check_advice(), check_one(), Claim, Why an advice explanation cannot be kept, or `None`. Asked of a claim built…, Why this one sentence cannot be kept, or `None` if it can. Depends on nothing…, test_a_claim_citing_the_same_document_twice_says_it_once(), test_a_grounded_claim_renders_its_document_and_page(), What the gate checks beyond "is there a citation". A cited sentence can still… (+25 more)

### Community 47 - "_pages_from"
Cohesion: 0.24
Nodes (11): _pages_from(), Group Docling's items by the page they were found on. Docling's markdown export…, A table as lines of text, one row per line: `label: value` when a row has two…, _table_text(), SimpleNamespace, _cell(), _on_page(), test_a_table_is_kept_as_label_and_value_lines_in_reading_order() (+3 more)

### Community 48 - "build_router"
Cohesion: 0.07
Nodes (41): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, What changed, in the words the screen confirms it with. `was` is returned…, The row is gone from Today. `speaks_again` is null when it will not come back.…, 202. The vision pass is slower than a page load, so it is queued and this is… (+33 more)

### Community 49 - "HouseholdScope"
Cohesion: 0.17
Nodes (17): HouseholdScope, Keep the owner's passages and the household's; set aside everybody else's. A…, What `AnswerGraph` is handed so it can scope without holding a connection.…, scope_passages(), _conn_returning(), _passage(), The third bucket. Home contents, a utility bill — nobody's name on it,…, A joint policy is the owner's too. Presence wins over exclusion. (+9 more)

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 51 - "FakeConn"
Cohesion: 0.06
Nodes (54): FakeConn, filed_document(), next_kind(), obligation(), open_obligation(), overdue_row(), Snooze means 'not until this gets more urgent', so it can name the day it does., No new column: `already_said` is what makes the row quiet, and it reads this… (+46 more)

### Community 52 - "State"
Cohesion: 0.12
Nodes (14): _asked(), _conversation(), fuse(), The shape a question asks for, matched from the pack's own phrases without a…, The first advising pack whose review a question asks for, as a shape the advise…, What the graph carries. It ends at the evidence; the answer is streamed, not…, The question to answer and to scope. A follow-up is the whole question it was…, Several searches as one list: each passage once, at the best score any phrasing… (+6 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.17
Nodes (24): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError, Read and validate a pack's grounding corpus from its own folder on disk. A…, A pack's grounding corpus on disk does not match what its `sources.yaml`… (+16 more)

### Community 54 - "FakeOllama"
Cohesion: 0.12
Nodes (14): Generated, FakeOllama, Exception, ADR 0017: candidates are the catalogue's types, unqualified, and every one is…, ADR 0017 decision 6: these were quarantined because no type fitted them., Answers whatever the test told it to, and records what it was asked., test_a_document_no_pack_recognises_is_not_forced_into_one(), test_a_low_confidence_classification_is_refused() (+6 more)

### Community 55 - "cli.py"
Cohesion: 0.20
Nodes (20): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+12 more)

### Community 56 - "blocked_reasons"
Cohesion: 0.22
Nodes (11): blocked_reasons(), forget(), Any, Path, ValueError, QuarantinedDocument, Per document: `None` when the image pass can run, or the sentence saying why it…, Safe to show. Forgetting a document whose file is still there would not last. (+3 more)

### Community 57 - "ADR index (0001-0018, with status)"
Cohesion: 0.09
Nodes (32): ADR 0006 - pypdfium2 renders the quarantine page images, ADR 0009 - next-themes and lucide-react are the only two web dependencies beyond the stack, Schedule-table questions remain weak (rank 2-4), ADR 0013: A question is understood before it is searched, and scoped before it is cut, The answer prompt carries today's date and names the scoped relation as who the question is about, AskRequest.history carries up to twelve earlier turns, A relevance-grading call and an 'answerable' schema flag were both dropped, Remaining failures are retrieval's to fix (cross-encoder plus lexical) (+24 more)

### Community 58 - "build.py"
Cohesion: 0.09
Nodes (29): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering…, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why the catalogue cannot supply `field` from every one of `doc_types`, or None., Whether any document type in the catalogue declares `field`., An advice shape that names a missing role or key fails at load time. Caught…, Every core document type, field and category this pack names exists, or…, A compared field no document type of the shape declares can never be printed.… (+21 more)

### Community 59 - "Any"
Cohesion: 0.10
Nodes (24): advised_pack(), db(), _document(), _facts_tuple(), FakeConn, FakeCursor, Any, date (+16 more)

### Community 60 - "answer.tsx"
Cohesion: 0.13
Nodes (27): Advice, AdviceCard(), AdviceNote(), AdviceWithheld(), capitalise(), sentence(), TONES, ADR-0016 (+19 more)

### Community 61 - "_check"
Cohesion: 0.10
Nodes (19): _check(), collapse(), _cuts_a_number(), number_tokens(), parse_value(), printed_as(), printed_in(), Any (+11 more)

### Community 62 - "settings.py"
Cohesion: 0.13
Nodes (15): _chat_ids(), _flag(), _folder(), local_url(), _port(), _positive(), Path, Small, literal .env reader with environment overrides and loopback-only… (+7 more)

### Community 63 - "lock.ts"
Cohesion: 0.07
Nodes (47): ref_node_crypto, dynamic, GET(), grant(), POST(), runtime, ALLOWED, Context (+39 more)

### Community 64 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 65 - "routes.py"
Cohesion: 0.08
Nodes (58): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, AskRequest, Claim, CloseRequest, ConfirmNameRequest (+50 more)

### Community 66 - "PARROT Interface Design Pack"
Cohesion: 0.09
Nodes (29): Not finding you is an answer (first-person abstention), Capture is where the user already is, Citation chips are the trust surface, Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Nothing moves without a reason (motion specification), Silence beats a guess (+21 more)

### Community 67 - "export-design-preview.cjs"
Cohesion: 0.10
Nodes (18): ref_node_fs, bundle(), classes, css, cssFile, domId, fs, ids (+10 more)

### Community 68 - "The Four Surfaces"
Cohesion: 0.13
Nodes (16): Packs and Modules May Not Import web/ or api/, The FastAPI Application, The API Surface, GET /api/today Never Marks Anything Notified, apply, Auto-Redirect to Today Once Ready, check, draw (+8 more)

### Community 69 - "pack"
Cohesion: 0.08
Nodes (45): Categories, Category, A kind of document a household holds, recognised by words printed in its name.…, holdings(), Any, Rows of `INVENTORY`, one holding per document that prints the field an enabled…, Asked, categories_asked() (+37 more)

### Community 70 - "advice-consent.tsx"
Cohesion: 0.17
Nodes (17): Consent, ConsentPrompt(), agree(), settle(), State, ADR-0016, AdviceConsentSection(), fetchConsents() (+9 more)

### Community 71 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 72 - "IngestJob"
Cohesion: 0.12
Nodes (14): CaptureAdapter, IngestJob, datetime, Protocol, What a capture returns: a registered document, and whether we had seen it…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., _Pending, datetime (+6 more)

### Community 73 - "Hybrid Retrieval: Dense Plus Full-Text"
Cohesion: 0.18
Nodes (11): No New Runtime Dependency Without an ADR, Never Generate SQL at Runtime, baseline.py Is Disposable and Never a Measurement, ports.py, the Seam With Lane B, bge-reranker-v2-m3 Cross-Encoder, 40 Down to 6, Hybrid Retrieval: Dense Plus Full-Text, Reciprocal Rank Fusion, k=60, The Household's Eleven Policies (+3 more)

### Community 74 - "scope.py"
Cohesion: 0.21
Nodes (17): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Any (+9 more)

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.17
Nodes (19): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), The owner is a row, not a config value baked at install, people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), A resolved person is shown as a chip, like a citation, The roster is derived from documents, then confirmed (+11 more)

### Community 76 - "FakeConn"
Cohesion: 0.12
Nodes (28): Channel, current(), grant(), _latest(), NoOwner, Any, RuntimeError, Record the owner saying yes to `wording`, this pack's consent text at… (+20 more)

### Community 77 - "test_modules.py"
Cohesion: 0.18
Nodes (19): Capability modules. A module reads typed rows and writes its own namespace. It…, Everything inside a lead window that has not already been said for that window.…, sweep(), FakeConn, obligation_row(), datetime, Reminder and Alert: what fires, once, and with what behind it. Both modules are…, A sweep for a date in the future must record that date, or it repeats itself. (+11 more)

### Community 78 - "today/page.tsx"
Cohesion: 0.09
Nodes (38): dynamic, HouseholdPage(), metadata, runtime, dynamic, GoneNote(), Header(), isUrgent() (+30 more)

### Community 79 - "tokens/page.tsx"
Cohesion: 0.18
Nodes (18): Motion(), ROWS, Colour(), FaceCard(), Focus(), INKS, metadata, RADII (+10 more)

### Community 80 - "preview.tsx"
Cohesion: 0.11
Nodes (19): DesignPreviewPage(), metadata, answers, DesignPreview(), Direction, directions, Item, items (+11 more)

### Community 81 - "test_advice_core.py"
Cohesion: 0.23
Nodes (16): _kind_of(), passages_for(), `"fact:12"` -> `"fact"`, `"rule:7"` -> `"rule"`. Anything else is a calculator…, Inputs as kind fact/rule passages (chunk_id from the ref), and the figures as…, check_content(), Why a cited sentence still cannot be kept, or `None`. Asked after `check_one`…, _says(), Kind (+8 more)

### Community 82 - "Two-stage quarantine with a vision-language second pass"
Cohesion: 0.12
Nodes (19): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Two-stage quarantine with a vision-language second pass, Batch 4: the deliberately hard documents, A full policy wording registers as policy_schedule, Task: review every quarantined document and label the failure, Task: sign off the capture-to-database path against the data inventory, Measurement is owned separately from the engine (+11 more)

### Community 83 - "Any"
Cohesion: 0.12
Nodes (7): ConsentCursor, Fails, FakeCursor, Any, The parameters of the one statement containing `needle`. Fails loudly if it…, Yields `before`, then raises. `ask` raises at once., Remembers what `grant` or `withdraw` inserted, so the next read of the latest…

### Community 84 - "Ollama"
Cohesion: 0.17
Nodes (10): answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, Ollama, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.…, Batch embeddings. Falls back to the legacy endpoint on old servers., Hit (+2 more)

### Community 85 - "TelegramUnavailable"
Cohesion: 0.15
Nodes (11): BaseTransport, RuntimeError, Safe to show: never contains the token., TelegramSettings, TelegramUnavailable, FakeRegistrar, The offset has already moved, so the survivors are all that is left to save., The `documents` table, reduced to the one thing it guarantees: sha256 is unique. (+3 more)

### Community 86 - "main"
Cohesion: 0.14
Nodes (19): approve(), pending(), PendingValue, Any, date, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it., Every value still waiting for review, oldest first, optionally for one pack. (+11 more)

### Community 87 - "ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.11
Nodes (27): Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration), Published guidance is a second evidence lane, never a second household, Every passage carries a kind: document, inventory or guidance, ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, The adult rule: advice is withheld for a person under 21 or a child with no date of birth on file, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel) (+19 more)

### Community 88 - "test_both_ask_endpoints_hand_the_graph_the_same_advice_ports"
Cohesion: 0.14
Nodes (13): advising(), conn(), graph(), _padded(), fixture, MonkeyPatch, One construction for both. With any port missing the graph declines advice, so…, The same pack, its consent wording and disclaimer surrounded by the whitespace… (+5 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "item-row.tsx"
Cohesion: 0.24
Nodes (10): countdown(), detail(), figure(), ItemRow(), longDate(), sentence(), TONE, WORD (+2 more)

### Community 91 - "test_tax_pack.py"
Cohesion: 0.20
Nodes (16): decimal, _basis(), _latest(), _matched(), _published(), FactRow, parametrize, The tax pack's advice, run on batch 1's own SRS statements and Notices of… (+8 more)

### Community 92 - "contracts.py"
Cohesion: 0.08
Nodes (34): How to give the feedback, Advice, Answering, DocumentTypeSpec, Exclusions, FactInput, FieldSpec, Grounding (+26 more)

### Community 93 - "Passage"
Cohesion: 0.08
Nodes (18): Passage, How a passage names itself: the document and the page, as a person would say it., Unique across kinds: chunk ids, fact ids and guidance ids are three sequences., The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting…, Keep the passages of these people and of the household; set aside everybody…, scope_to(), Scoped (+10 more)

### Community 94 - "AdviceShape"
Cohesion: 0.11
Nodes (22): AdviceShape, One kind of advice question, and everything its calculator needs to answer it., _fact(), fact_row(), facts_for(), in_category(), _is_an_adviser(), ModuleAdviser (+14 more)

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
Cohesion: 0.07
Nodes (61): copy, PackManifest, A domain pack, authored as one YAML file: grounding, persona, answering and…, _advised(), _checked(), _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held() (+53 more)

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.10
Nodes (21): The Purely Additive Migration Exception, Contracts and Migrations Are Their Own PR, Sources of Truth Generate Their Outputs, Snooze Means Not Until This Gets More Urgent, The Three Things Agents Get Wrong Here, Generated Files Committed Alongside Their Source, benefit_illustration Document Type, birth_certificate Document Type (+13 more)

### Community 100 - "_Answering"
Cohesion: 0.50
Nodes (4): _Answering, The event stream one request is sending, held where the request's cleanup can…, Close the answer stream when the request ends, whatever ended it. Requires…, Conn

### Community 101 - "split_sections"
Cohesion: 0.17
Nodes (12): _groups(), _is_heading(), _pack(), Consecutive pieces joined while they fit, so a page of short sections is one…, The text in consecutive sections of at most about `limit` characters. A line is…, split_sections(), _starts_paragraph(), test_a_paragraph_longer_than_a_section_is_split_at_line_boundaries() (+4 more)

### Community 102 - "The five-lane split (five people, nine weeks, three builders)"
Cohesion: 0.09
Nodes (30): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The domain pack manifest, The expansion model: two axes, not one list, The golden set: answerable, hard negatives, adversarial, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build (+22 more)

### Community 103 - "Data inventory: identity data, DOBs and loans"
Cohesion: 0.17
Nodes (15): Data inventory: identity data, DOBs and loans, The lock is a screen lock, not encryption, next dev binds every interface, not loopback, Telegram capture route and delete-at-source, What crosses a boundary, Governance artefact set, Write unverified rather than assert, The final ILP report (+7 more)

### Community 104 - "test_rerank.py"
Cohesion: 0.13
Nodes (18): Lane B: hybrid retrieval. `HybridRetriever` implements…, CrossEncoderReranker, passage_text(), What the reranker reads: the one-line context, when a chunk carries one, then…, Implements `core.graph.ports.Reranker`. Reorders by the cross-encoder's score…, _passage(), fixture, MonkeyPatch (+10 more)

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

### Community 109 - "pytest"
Cohesion: 0.20
Nodes (10): FixtureRequest, io, needs_ocr, pytest, _as_printed(), parametrize, A scanned or photographed document parses to pages with its tables preserved.…, The register stores typed values; the page prints them the way a person would. (+2 more)

### Community 110 - "Reminder, Alert and Tracker Registers"
Cohesion: 0.18
Nodes (15): Passport Uses date_of_expiry So policy_expiry Does Not Fire, filing_deadline Reminder, maturity_date Is Not expiry_date, passport Document Type, passport_expiry Reminder, policy_expiry Reminder, policy_schedule Document Type, Reminder, Alert and Tracker Registers (+7 more)

### Community 111 - "FakeCursor"
Cohesion: 0.18
Nodes (3): FakeCursor, Any, FakeConn

### Community 112 - "example_pack template manifest"
Cohesion: 0.18
Nodes (14): I explain the renewal notice, I do not renew policies, Autonomy statement, ISO/IEC 22989 stages versus 5338 processes, never_acts as a machine-checked flag, Grounding corpora now live inside packs, advice module manifest, example_pack template manifest, example_room advice shape (+6 more)

### Community 113 - "paperbrain/extract.py"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 114 - "_closes"
Cohesion: 0.21
Nodes (12): _closes(), _either(), "a dental plan", or "a term life plan or a whole life plan". "An" only before…, Which kinds of cover close a short shape's gap, written by code. The pack…, Marcus held a critical illness plan on 20 September and was SGD 251,200.00…, `closed_by` is optional in the contract, and a shape without it stays as it was., _shape(), test_a_gap_closed_by_two_kinds_names_the_one_held_and_the_one_not() (+4 more)

### Community 115 - "react"
Cohesion: 0.10
Nodes (25): lucide-react, react, AppLayout(), dynamic, runtime, LockButton(), SURFACES, TabBar() (+17 more)

### Community 116 - "_answer_events"
Cohesion: 0.13
Nodes (18): TodayResponse, _answer_events(), today(), _cite(), connection(), _link(), Any, date (+10 more)

### Community 117 - "Integration review"
Cohesion: 0.33
Nodes (5): Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 118 - "FakeCursor"
Cohesion: 0.20
Nodes (3): FakeCursor, Any, FakeConn

### Community 119 - "test_registration.py"
Cohesion: 0.29
Nodes (12): Insert or update the `documents` row for these bytes and say which happened.…, register_document(), conn(), database_url(), Any, fixture, The idempotent upsert, against the real unique index. `documents.sha256 UNIQUE`…, test_a_document_must_arrive_with_a_name() (+4 more)

### Community 120 - "main.py"
Cohesion: 0.20
Nodes (8): The local API. Liveness is intentionally separate from assistant readiness.…, The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), contextlib, html, secrets, starlette_middleware_trustedhost

### Community 121 - "TelegramCapture"
Cohesion: 0.18
Nodes (7): attribution(), Any, A daemon thread that long-polls the Telegram bot until `stop()` or process…, Begin polling. Returns False, with a logged reason, when it cannot or should…, One long poll. A failure waits rather than hammering the API with the same…, Whose phone this arrived on, recorded before anything is read off it. See ADR…, TelegramCapture

### Community 122 - "next"
Cohesion: 0.10
Nodes (18): ADR-0017, next, AlwaysOn(), dynamic, metadata, ModuleRow(), PackCard(), PacksPage() (+10 more)

### Community 123 - "ADR 0002 - One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (7): ADR 0001 - Record architecture decisions, ADR 0002 - One PostgreSQL instance for everything, Reciprocal rank fusion of dense and lexical, ADR 0003 - PaperBrain informs the pattern, not the module, PaperBrain prototype, Contracts before code, Lane A - Integration and product

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.17
Nodes (12): Task: benchmark the workstation and publish the numbers, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, The deliberately naive retrieval baseline, Committed runs are never deleted, Yew Mun's generated task list, Hybrid retrieval, not embeddings alone, Chunking respects paragraphs (+4 more)

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 126 - "_page_of_examples"
Cohesion: 0.24
Nodes (10): _page_of_examples(), One page printing every field's `example`, so each value is attributable to a…, Each field's example as the model reports it; a repeating one as label and…, ADR 0017: several riders on one schedule, each a row pairing its label and its…, `FieldSpec.name` is the `facts.key`. Nothing between the manifest and the row…, The named regression, spelled out so a future rename cannot quietly reintroduce…, _reply_of_examples(), test_a_donation_receipt_stores_donation_amount_and_never_amount() (+2 more)

### Community 127 - "create_app"
Cohesion: 0.31
Nodes (6): create_app(), checks(), ready(), setup(), system_status(), FastAPI

### Community 128 - "The case for synthetic evaluation data"
Cohesion: 0.18
Nodes (11): Qwen-SEA-LION-v4-4B-VL extraction ceiling, Register first, then generate, SYNTHETIC DOCUMENT footer, Ground truth for free, The 40-document holdout corpus, The case for synthetic evaluation data, Two withdrawn synthetic-data controls, extraction_f1 (+3 more)

### Community 129 - "Domain pack"
Cohesion: 0.12
Nodes (21): The demonstration run sheet, Step 8 - switch a pack off, Step 6 - the abstention, Step 7 - the refusal to act, Step 2 - the source chip, Derive the roster, then confirm it, Exactly one owner, enforced by the database, facts.subject is never normalised (+13 more)

### Community 130 - "Any"
Cohesion: 0.29
Nodes (8): The person a printed name means, or `None` if nobody has confirmed what it…, resolve(), conn(), Any, fixture, A second document must never silently move a name from one member to another., test_one_name_cannot_belong_to_two_people(), test_the_owner_is_found_by_any_of_their_names()

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

### Community 137 - "sweep"
Cohesion: 0.24
Nodes (12): AlertConfig, `warn_at` is a share of the ceiling. A ceiling of zero means any value at all…, Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), _triggered(), One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order., srs_row(), test_a_firing_older_than_the_debounce_window_fires_again() (+4 more)

### Community 138 - "page_pixels"
Cohesion: 0.32
Nodes (8): Image, page_pixels(), photographed(), fixture, Page 1 of the digital schedule, drawn at 200 dpi — the resolution of a desk…, The scanned tier: an image-only PDF. No text layer, so every character comes…, The photographed tier: lower resolution, a slight skew, a grey table showing at…, scanned()

### Community 139 - "PaperBrain"
Cohesion: 0.20
Nodes (10): The code pass of the knowledge graph, Nobody edits core/contracts.py in a feature pull request, Lane A - Integration and product, The semantic pass of the knowledge graph, Triage prompt: four buckets, no code written, Ninety protected minutes a week of integration, Christian's generated task list, PaperBrain (+2 more)

### Community 140 - "ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.33
Nodes (9): guardrails.abstain_below was calibrated on un-prompted scores, ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts, chunks.tsv built from context_prefix || text, Context prefix: title - type - heading - page, rag_probe2 before/after similarity table (six policies, 13 September), scripts/reindex.py rebuilds chunks and vectors, Chunks follow the document's structure (Docling heading labels), Task prompts: embed_query and embed_documents (+1 more)

### Community 141 - "chat/route.ts"
Cohesion: 0.11
Nodes (23): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+15 more)

### Community 142 - "test_a_core_document_stays_enabled_when_every_pack_is_off"
Cohesion: 0.32
Nodes (8): document_row(), fact_row(), date, ADR 0017: disabling insurance_agent switches off its voice, never a household's…, Following a citation must never end in a blank screen because a pack was…, test_a_core_document_stays_enabled_when_every_pack_is_off(), test_one_document_is_shown_even_when_its_pack_is_off(), test_vault_lists_documents_with_their_facts()

### Community 143 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 144 - "test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them"
Cohesion: 0.22
Nodes (5): ClosingSpy, Wraps an event generator to record whether something called `.close()` on it,…, Starlette's own body iteration (`iterate_in_threadpool`) never calls `.close()`…, test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them(), spying()

### Community 145 - "schedule.py"
Cohesion: 0.15
Nodes (17): build(), Any, The one Celery application, built from `Settings`. Every setting here is a…, Construct the Celery application. Imported lazily by callers so that nothing…, beat_schedule(), cron_expressions(), crontab_from(), manifest() (+9 more)

### Community 146 - "PrivateCare Policy Wording Template"
Cohesion: 0.31
Nodes (9): PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Gemini prompt bank for identity specimens, The Lim household canon, Republic of Xinkapow (+1 more)

### Community 147 - "alert module manifest"
Cohesion: 0.28
Nodes (9): Days without recorded cover tile, alert_fpr, obligation_precision, Module manifest template, Quoted "on" key in YAML 1.1, alert module manifest, Modules read typed rows, never chunks, reminder module manifest (+1 more)

### Community 150 - "app/layout.tsx"
Cohesion: 0.22
Nodes (9): next-themes, web_app_globals, figtree, jetbrains, metadata, outfit, RootLayout(), viewport (+1 more)

### Community 151 - "The Grounding Gate"
Cohesion: 0.29
Nodes (8): never_acts: True in Every Pack Manifest, The Core Answering Layer, The Answer Path: route, retrieve, rerank, ground, answer or abstain, The Grounding Gate, The Score Floor the Gate Reads, Kidney Stones: Inpatient Covered, Outpatient ESWL Excluded, Ask Screen, Try to Make It Lie: the Abstention Test

### Community 152 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 153 - "ADR 0008 - Ingestion runs on a Celery worker"
Cohesion: 0.39
Nodes (8): ADR 0005 - The watched folder is polled, not subscribed to, Stability debounce with injected time, ADR 0008 - Ingestion runs on a Celery worker, The queue carries a digest, not the document, The ingestion worker, START.cmd launcher, Telegram capture, The watched inbox folder

### Community 154 - "Cursor"
Cohesion: 0.25
Nodes (4): Cursor, Any, Protocol, cursor()

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (8): parrot-sweep shimmer animation, Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, An answer with the page it came from, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "build_team_tasks.py"
Cohesion: 0.29
Nodes (9): csv, difflib, main(), Path, Generate each member's task list from the master task CSV. python…, _read_rows(), _render(), _week_key() (+1 more)

### Community 157 - "test_startup.py"
Cohesion: 0.11
Nodes (26): main(), Path, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file…, report_hardware(), startup_gaps(), prepare_checkout(), Path (+18 more)

### Community 158 - "Adversarial testing from week 7"
Cohesion: 0.25
Nodes (8): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Adversarial testing from week 7, Prompt injection carried inside a document, Scope attack: asking it to act, Task: run adversarial Set C and write up the findings, Adversarial Set C (15 questions that should not be answered), Golden Set C - adversarial (15)

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 160 - "AdviceRecord"
Cohesion: 0.40
Nodes (3): AdviceRecord, Every advised or withheld answer's full basis, so it can be reconstructed later…, Log

### Community 161 - "Every Fact Row Cites Its Source"
Cohesion: 0.33
Nodes (7): Every Fact Row Cites Its Source, A Correction Cannot Invent a Row, Every Node Writes One Line to traces, The Ingestion Pipeline, The Pipeline Forks Into Retrieval and Facts Lanes, Numbers Come From Postgres, Never From the Model, macOS Worker Runs Celery Solo

### Community 162 - "HouseholdAdviceLog"
Cohesion: 0.13
Nodes (14): AskResponse, The whole answer, once. `text` is the consent wording when `kind` is…, _as_response(), ask(), ask_stream(), _graph_for(), _history(), One `Answer` to one of the shapes a client has to handle. (+6 more)

### Community 163 - "check"
Cohesion: 0.29
Nodes (6): check(), Never raises, never rewrites a claim. It keeps, drops, or abstains. The whole-…, Verdict, test_a_sentence_citing_a_passage_that_was_never_retrieved_is_dropped(), test_a_sentence_with_no_supporting_passage_is_dropped(), test_no_passages_at_all_abstains()

### Community 164 - "unprinted_numbers"
Cohesion: 0.29
Nodes (7): _normal(), "1,860.00", "1860" and "01" → "1860", "1860", "1": formatting is not a…, Every number or identifier in a sentence that no cited passage prints. An…, unprinted_numbers(), test_a_date_on_file_may_be_written_the_way_a_person_says_it(), test_a_leading_zero_does_not_make_a_printed_date_unprinted(), test_a_policy_number_is_kept_only_when_it_is_printed_whole()

### Community 165 - "PARROT evaluation harness"
Cohesion: 0.38
Nodes (7): abstention_rate, PARROT evaluation harness, Set A, answerable, Set B, hard negatives, Set C, adversarial, The golden question sets, must_cite_page from field_pages

### Community 166 - "RagasJudge"
Cohesion: 0.32
Nodes (6): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts(), Ragas 0.4 metrics through Ollama's OpenAI-compatible endpoint. Imported lazily…

### Community 167 - "The autonomy statement"
Cohesion: 0.29
Nodes (7): The autonomy statement, Governance claims traced to enforcement points, IMDA mappings and autonomy statement artefact, The facts table as an extension point, Constraint: fully offline, Explicitly not doing: cloud, hosted vectors, autonomous spending, Roadmap phase 2 - facts

### Community 168 - "FolderCapture"
Cohesion: 0.29
Nodes (3): FolderCapture, Begin watching. Returns False, with a logged reason, when it cannot., A daemon thread that polls the watched folder until `stop()` or process exit.

### Community 169 - "test_the_inventory_always_reads_core_documents"
Cohesion: 0.29
Nodes (3): ADR 0017: a document is the core's, so the query includes `core` whatever is…, test_the_inventory_always_reads_core_documents(), cursor()

### Community 170 - "Missing"
Cohesion: 0.24
Nodes (6): Missing, date, What a calculator returns when a fact or a rule value it needed was not there…, Every shape the pack's review lists, for one person, as one calculation (ADR…, Adviser, date

### Community 171 - "printed_date"
Cohesion: 0.40
Nodes (6): printed_date(), A date as a document prints it, as YYYY-MM-DD, or None when it is not a date.…, parametrize, test_a_null_shaped_string_is_an_absent_field_not_a_bad_number(), test_a_printed_date_becomes_iso_in_code_not_in_the_model(), test_something_that_is_not_a_date_is_not_turned_into_one()

### Community 173 - "Page one as plain Label: value lines"
Cohesion: 0.33
Nodes (6): Appendicitis entitlement demonstration, Page one as plain Label: value lines, Ward and hospital entitlement clause, Answering: vocabulary, categories, exclusions, The four tests every field must pass, policy_type was judged, not printed

### Community 174 - "Project skills"
Cohesion: 0.40
Nodes (4): Changing them, Project skills, Slash commands, Using them

### Community 175 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 176 - "_as_consent"
Cohesion: 0.33
Nodes (6): AdviceConsent, One advising pack, the wording a person is asked to agree to, and what the…, _as_consent(), advice_consents(), record_consent(), One advising pack's consent wording and the owner's standing answer to it.

### Community 177 - "page_count"
Cohesion: 0.40
Nodes (5): page_count(), How many pages this file has, or 0 when it is not something with pages.…, test_a_pdf_is_counted_by_the_file_not_by_what_the_parser_managed(), test_an_image_document_is_one_page(), test_something_with_no_pages_counts_zero()

### Community 179 - "The synthetic-to-real gap"
Cohesion: 0.40
Nodes (5): The 40-document redacted holdout, The synthetic-to-real gap, Consent and redaction protocol, Task: write the PDPA position on using synthetic data, Task: evaluation run 3 plus the holdout run

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 181 - ".ask"
Cohesion: 0.50
Nodes (3): _as_sentence(), Every event, collected. `scripts/ask.py` and the screen ask the same question…, "which age band applies" -> "Which age band applies.": a pack's wording and a…

### Community 183 - "quiet_engine"
Cohesion: 0.50
Nodes (4): fixture, MonkeyPatch, quiet_engine(), No real probes, no startup writes, no deliberate pause before exiting. The…

### Community 184 - "FakeTelegram"
Cohesion: 0.22
Nodes (6): MockTransport, FakeTelegram, Any, Request, Response, The four Bot API calls this adapter makes, and a record of what it asked for.

### Community 185 - "test_an_install_without_the_renderer_says_so"
Cohesion: 0.50
Nodes (3): MonkeyPatch, The interface has an error state for "this cannot be shown". It has none for a…, test_an_install_without_the_renderer_says_so()

### Community 186 - "eslint.config.mjs"
Cohesion: 0.33
Nodes (5): @eslint/eslintrc, ref_node_path, ref_node_url, compat, eslintConfig

### Community 200 - "test_page_numbers_are_the_ones_a_citation_says"
Cohesion: 0.50
Nodes (4): Width and height straight out of the PNG header, so the test needs no image…, Page 2 is the wide one. If the off-by-one ever returns, this is what catches it., _size(), test_page_numbers_are_the_ones_a_citation_says()

### Community 201 - "Alert"
Cohesion: 0.25
Nodes (5): Alert, What the debounce is keyed on: this metric, for this person and thing, in this…, Two lapsed policies on one person are two alerts, and saying one must not…, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

### Community 204 - "package.json"
Cohesion: 0.11
Nodes (16): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+8 more)

### Community 205 - "three_pages"
Cohesion: 0.67
Nodes (3): fixture, A three-page PDF, each page a different size so a render can be told from its…, three_pages()

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
- **356 isolated node(s):** `Action`, `Stage`, `DependencyCheck`, `Phase`, `Status` (+351 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1574 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
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