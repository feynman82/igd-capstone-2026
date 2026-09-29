# Graph Report - igd-capstone-2026  (2026-09-29)

## Corpus Check
- 305 files · ~700,061 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 29 file(s) not represented in the graph (top: (none) 11, .csv 5, .jsonl 3)

## Summary
- 4472 nodes · 11163 edges · 209 communities (180 shown, 29 thin omitted)
- Extraction: 90% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1059 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `532a8d48`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- advice.py
- typing
- ScriptedOllama
- AnswerGraph
- validate
- advice/__init__.py
- Provenance register for corpus sg_protection_guidance
- test_advice_module.py
- test_eval_harness.py
- test_ingest_pipeline.py
- test_grounding_index.py
- test_worker_queue.py
- FolderAdapter
- test_telegram_capture.py
- tasks.py
- run_parrot.py
- bench_runtime.py
- vault.py
- support.js
- checks.py
- ingest/extract.py
- test_grounding_values.py
- settings
- registry.py
- answer.py
- pytest
- household.py
- pipeline.py
- test_lifecycle.py
- score.py
- test_household.py
- Settings
- test_pages.py
- FakeCursor
- sets_io.py
- TelegramAdapter
- Registration
- Any
- Overdue
- test_api.py
- alert/__init__.py
- retrieve.py
- sse
- api.ts
- ModelUnavailable
- test_answer_graph.py
- test_gate.py
- ParsedPage
- build_router
- HouseholdScope
- compilerOptions
- FakeConn
- Any
- test_grounding.py
- run.py
- cli.py
- ingest/quarantine.py
- ADR index (0001-0018, with status)
- build.py
- Any
- answer.tsx
- values.py
- ConfigurationError
- lock.ts
- dependencies
- models.py
- PARROT Interface Design Pack
- export-design-preview.cjs
- The Four Surfaces
- pack
- advice-consent.tsx
- devDependencies
- folder.py
- Hybrid Retrieval: Dense Plus Full-Text
- scope.py
- ADR 0011: The household is people and aliases, and the owner is one of them
- test_advice_core.py
- test_modules.py
- today/page.tsx
- tokens/page.tsx
- preview.tsx
- routes.py
- Two-stage quarantine with a vision-language second pass
- Any
- Ollama
- test_the_code_scored_metrics_come_out_as_arithmetic_says
- main
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- test_both_ask_endpoints_hand_the_graph_the_same_advice_ports
- components.json
- item-row.tsx
- test_tax_pack.py
- contracts.py
- Scoped
- InstalledPack
- The Lim Household, Tampines
- ADR 0007 - The graph ships before retrieval and before a checkpoint table
- Lane C - Governance and assurance
- test_contracts.py
- Core Document Catalogue (ADR 0017)
- _Answering
- ._categories_read_a_declared_field
- The five-lane split (five people, nine weeks, three builders)
- Data inventory: identity data, DOBs and loans
- test_rerank.py
- Roadmap phase 3 - reminders
- web/ - the PARROT interface
- The document register as ground truth
- ingest.py
- inventory.py
- Reminder, Alert and Tracker Registers
- FakeCursor
- example_pack template manifest
- paperbrain/extract.py
- _closes
- next
- _answer_events
- FieldSpec
- worker.py
- sha256
- installed_packs
- capture.py
- packs/page.tsx
- ADR 0002 - One PostgreSQL instance for everything
- The deliberately naive retrieval baseline
- Running the evaluation harness
- test_a_document_still_in_the_inbox_is_not_forgotten
- knowledge.py
- The case for synthetic evaluation data
- Domain pack
- test_a_client_that_leaves_after_the_card_commits_one_record
- Filling the corpus register
- Writing a governance artefact
- Two-Stage Quarantine With a Vision Second Pass
- Fill the Register Before Generating Documents
- Where Things Live
- Policy schedule HTML template
- sweep
- F1
- PaperBrain
- ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts
- chat/route.ts
- same_value
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
- pathlib
- Adversarial testing from week 7
- Writing an ADR
- AdviceRecord
- Every Fact Row Cites Its Source
- _as_response
- generic
- Passage
- PARROT evaluation harness
- RagasJudge
- The autonomy statement
- _market
- test_the_inventory_always_reads_core_documents
- Missing
- current_lead
- _on_page
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- _as_consent
- ._compares_what_its_documents_declare
- The synthetic-to-real gap
- filesystem
- usable
- Due
- _make_replacer
- ._handle
- scored
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
- test_advice_is_a_module
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
5. `AnswerGraph` - 77 edges
6. `FakeConn` - 75 edges
7. `settings()` - 75 edges
8. `client_for()` - 74 edges
9. `build_router()` - 73 edges
10. `Ollama` - 70 edges

## Surprising Connections (you probably didn't know these)
- `Work in this order, stopping for the author at each step` --references--> `money()`  [INFERRED]
  .claude/skills/authoring-a-domain-pack/SKILL.md → modules/advice/__init__.py
- `How to give the feedback` --references--> `FieldSpec`  [INFERRED]
  .claude/skills/integration-review/SKILL.md → core/contracts.py
- `2. Limiting a fact input to one year` --references--> `FactInput`  [INFERRED]
  packs/iras_tax/CONTRACT_REQUESTS.md → core/contracts.py
- `The Corpus Is Synthetic and Committed` --semantically_similar_to--> `Corpus Batches Are Not in Git`  [AMBIGUOUS] [semantically similar]
  NOTICE.md → FIRST-RUN.md
- `Domain Packs` --conceptually_related_to--> `Core Document Catalogue (ADR 0017)`  [AMBIGUOUS]
  README.md → core/documents.yaml

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The Answer Path, End to End** — core_graph_readme_answer_path, core_retrieve_readme_hybrid_search, core_retrieve_readme_rrf_fusion, core_retrieve_readme_cross_encoder_reranker, core_graph_readme_grounding_gate, core_retrieve_readme_score_floor, api_readme_the_surface [EXTRACTED 1.00]
- **The Hard Rules of the Working Agreement** — agents_no_runtime_sql_generation, agents_every_fact_cites_its_source, agents_no_claim_without_a_citation, agents_contracts_are_a_separate_pr, agents_no_new_runtime_dependency_without_an_adr, agents_generated_files_have_one_source_of_truth, agents_packs_may_not_import_the_interface, agents_never_acts, agents_amend_the_graph_refresh_into_the_commit [EXTRACTED 1.00]
- **The Ground-Truth Chain: Catalogue, Canon, Register, Templates, Validator** — core_documents_document_types, corpus_canon_lim_household, corpus_readme_register_first_order, corpus_templates_payslip_payslip_template, corpus_templates_hospital_income_policy_wording_policy_contract, corpus_readme_field_pages_second_pass, corpus_readme_handover_gate [INFERRED 0.85]
- **The five lanes of Project PARROT** — docs_team_lane_a_integration_and_product, docs_team_lane_b_retrieval_and_evaluation, docs_team_lane_c_governance_and_assurance, docs_team_lane_d_domain_packs_and_interface, docs_team_lane_e_corpus_and_adversarial_testing [EXTRACTED 1.00]
- **The boundary: it abstains, it cites, and it never acts** — docs_pack_authoring_guardrails, docs_demo_run_sheet_the_abstention, docs_demo_run_sheet_the_refusal_to_act, docs_demo_run_sheet_the_source_chip, docs_adr_0007_the_graph_ships_before_retrieval_and_before_a_checkpoint_table_adr_0007 [INFERRED 0.85]
- **Capture to indexed document, and what happens when it fails** — docs_running_start_cmd, docs_running_watched_inbox_folder, docs_running_ingestion_worker, docs_running_quarantine_second_pass, docs_adr_0005_polling_the_watched_folder_adr_0005, docs_adr_0008_ingestion_runs_on_a_celery_worker_adr_0008, docs_adr_0006_pypdfium2_for_the_quarantine_image_pass_adr_0006 [INFERRED 0.95]
- **Household scoping: from a printed name to a scoped answer** — docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_people, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_person_aliases, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_facts_subject, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_three_buckets, docs_adr_0013_a_question_is_understood_before_it_is_searched_possessive_relations_scope, docs_adr_0015_a_name_scopes_and_a_grandparent_is_not_a_parent_a_question_naming_exactly_one_person_is_theirs, docs_adr_0015_a_name_scopes_and_a_grandparent_is_not_a_parent_grandparent_is_a_relation_nobody_can_hold, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_resolved_person_chip [INFERRED 0.85]
- **The pack contract, revised across three ADRs** — docs_adr_0014_a_pack_supplies_knowledge_and_the_core_stays_generic_packmanifest_answering, docs_adr_0014_a_pack_supplies_knowledge_and_the_core_stays_generic_advice_decline_route, docs_adr_0016_a_pack_advises_code_calculates_under_recorded_consent_advice_shapes, docs_adr_0016_a_pack_advises_code_calculates_under_recorded_consent_verdict_by_code, docs_adr_0017_a_pack_is_grounding_and_persona_the_core_owns_documents_a_pack_is_knowledge_and_voice, docs_adr_0017_a_pack_is_grounding_and_persona_the_core_owns_documents_core_documents_yaml, docs_adr_0017_a_pack_is_grounding_and_persona_the_core_owns_documents_two_answering_layers [EXTRACTED 1.00]
- **Startup and power: the five lifecycle screens** — docs_artefacts_parrot_uiux_refinement_startup_and_power_main_dc_getting_parrot_ready, docs_artefacts_parrot_uiux_refinement_startup_and_power_powermenu_dc_power_menu, docs_artefacts_parrot_uiux_refinement_startup_and_power_restarting_dc_restarting_parrot, docs_artefacts_parrot_uiux_refinement_startup_and_power_shutdown_dc_parrot_is_off, docs_artefacts_parrot_uiux_refinement_startup_and_power_startupblocked_dc_waiting_for_its_database [EXTRACTED 1.00]
- **The three PARROT interface directions evaluated side by side** — docs_artefacts_parrot_uiux_refinement_uploads_parrot_design_evaluation_designpreview, docs_artefacts_parrot_uiux_refinement_uploads_parrot_design_evaluation_civic_register, docs_artefacts_parrot_uiux_refinement_uploads_parrot_design_evaluation_kitchen_table, docs_artefacts_parrot_uiux_refinement_uploads_parrot_design_evaluation_the_reading_desk [EXTRACTED 1.00]
- **Module manifests sharing the reads/writes/runs/surfaces contract** — modules__template_module_module_template, modules_advice_module_advice, modules_alert_module_alert, modules_reminder_module_reminder [INFERRED 0.95]
- **The four code-scored metrics that need no judge** — eval_readme_abstention_rate, eval_readme_extraction_f1, eval_readme_obligation_precision, eval_readme_alert_fpr, eval_readme_evaluation [EXTRACTED 1.00]
- **Insurance coverage review: shapes, guideline keys and held categories answered in one pass** — packs_insurance_agent_pack_review, packs_insurance_agent_pack_death_tpd_cover, packs_insurance_agent_pack_ci_cover, packs_insurance_agent_pack_death_tpd_income_multiple, packs_insurance_agent_pack_ci_income_multiple, packs_insurance_agent_pack_hospital_expense, packs_insurance_agent_pack_long_term_care, packs_insurance_agent_pack_advice_consent [EXTRACTED 1.00]
- **The 9x/4x protection rule of thumb and the published sources a person approved it from** — packs_insurance_agent_grounding_sg_protection_guidance_moneysense_bfpg_faq_protection_rule_of_thumb, packs_insurance_agent_grounding_sg_protection_guidance_moneysense_bfpg_faq_consumer_faqs, packs_insurance_agent_grounding_sg_protection_guidance_moneysense_bfpg_starting_a_family_starting_a_family_guide, packs_insurance_agent_grounding_sg_protection_guidance_moneysense_basic_financial_planning_basic_financial_planning_guide, packs_insurance_agent_grounding_sg_protection_guidance_lia_protection_gap_study_protection_gap_study_2022, packs_insurance_agent_pack_death_tpd_income_multiple, packs_insurance_agent_pack_ci_income_multiple [INFERRED 0.95]
- **Pack-first pipeline: a pack's field names gate the register, the corpus, evaluation and governance** — team_readme_pack_to_register_dependency, team_readme_lane_d_zee, team_readme_lane_e_desmond, team_readme_lane_b_yew_mun, team_readme_lane_c_siew, packs_iras_tax_pack_iras_tax [EXTRACTED 1.00]
- **The five-lane ownership split of the repository** — team_christian_readme_lane_a_integration, team_yew_mun_readme_lane_b_retrieval, team_siew_readme_lane_c_governance, team_zee_readme_lane_d_packs_and_interface, team_desmond_readme_lane_e_corpus [EXTRACTED 1.00]
- **One field name, one place: pack.yaml to register to extractor to score** — team_zee_readme_pack_yaml_is_the_only_authored_file, team_desmond_readme_generated_column_headings, team_desmond_readme_document_register, team_desmond_readme_corpus_validate, team_yew_mun_readme_golden_set_a, team_desmond_readme_expiry_date_stopgap [EXTRACTED 1.00]
- **The grounded-refusal flow: gate, abstention screen, hard negatives, adversarial probe** — team_christian_readme_answer_graph, web_docs_user_stories_abstention_is_a_designed_screen, team_yew_mun_readme_golden_set_b, team_siew_readme_adversarial_set_c, team_siew_readme_autonomy_statement, team_desmond_readme_scope_attack [INFERRED 0.85]

## Communities (209 total, 29 thin omitted)

### Community 0 - "advice.py"
Cohesion: 0.12
Nodes (14): AdviceLog, Adviser, ConsentBook, Protocol, What a calculator returns, and what the graph needs to ask consent and keep a…, Implemented by `HouseholdConsents` in `core/advice_consent.py`., The granting row's id, or `None` when the owner has not granted this exact…, Implemented by `HouseholdAdviceLog` in `core/advice_records.py`. (+6 more)

### Community 1 - "typing"
Cohesion: 0.04
Nodes (67): _graph_for(), The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), HouseholdAdviceLog, The record of every advised or withheld answer (ADR 0016). `advice_records`…, `core.graph.advice.AdviceLog` over a live connection. `basis` is dumped with…, DenseRetriever (+59 more)

### Community 2 - "ScriptedOllama"
Cohesion: 0.07
Nodes (61): AdviceCard, AdviceWithheld, ConsentRequired, Declined, Finished, A request for a recommendation or a judgement, declined before anything is…, Everything that is only knowable once the last sentence is in. `quarantined`…, Advice was asked for and the owner has not agreed to this pack's current… (+53 more)

### Community 3 - "AnswerGraph"
Cohesion: 0.13
Nodes (36): AnswerGraph, _citations(), The documents on file, narrowed to the same people the passages were., "None of the 5 policies on file is a dental plan." Written by code, never by…, "On file for Marcus Lim: MERIDIAN ASSURANCE, Private Car Insurance Policy…, One sentence that has passed the gate, with the citations it passed on. It will…, Built once, asked many times. Holds no connection: retrieval does., Sentence (+28 more)

### Community 4 - "validate"
Cohesion: 0.09
Nodes (40): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+32 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.08
Nodes (70): Figure, Input, One fact or rule value a calculation was built on, carrying its own citation.…, One number a calculator produced, and the words a sentence must use to state…, Hashable, _ambiguous(), _amount(), _band() (+62 more)

### Community 6 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.05
Nodes (64): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, MediShield Life (CPF Board), Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022 (+56 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.10
Nodes (68): Calculation, What a calculator returns when every fact and rule it needed was on file and…, calculate(), advised_pack(), assert_nothing_negative(), basis(), fact(), _facts_tuple() (+60 more)

### Community 8 - "test_eval_harness.py"
Cohesion: 0.10
Nodes (33): Cited, One sentence and the passages it was traced to. What rule 3 looks like as data.…, The evaluation harness. `python -m eval.run` is the entry point;…, Decode rate and peak VRAM from the newest benchmark file…, _runtime_numbers(), The reference answer Ragas judges recall and precision against. A fact…, reference_for(), Expected (+25 more)

### Community 9 - "test_ingest_pipeline.py"
Cohesion: 0.09
Nodes (48): extract(), Never raises. A failure is a reason, and a reason routes the document to…, FakeOllama, insurance(), iras(), _page_of_examples(), Any, Exception (+40 more)

### Community 10 - "test_grounding_index.py"
Cohesion: 0.09
Nodes (41): CaptureFixture, GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records…, SourceText, index_pack(), IndexReport, Any, date (+33 more)

### Community 11 - "test_worker_queue.py"
Cohesion: 0.10
Nodes (32): Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker. Celery is imported here rather…, bytes_for(), index_folder(), Path, SHA-256 of every file sitting in the watched folder. The document row holds the… (+24 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.19
Nodes (23): FolderAdapter, Satisfies `CaptureAdapter`. Holds no database handle — it is given a…, FakeRegistrar, datetime, fixture, parametrize, Path, The watched folder: debounce, mime sniffing, and what happens the second time.… (+15 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.10
Nodes (36): RuntimeError, Safe to show: never contains the token., TelegramSettings, TelegramUnavailable, MockTransport, build(), FakeRegistrar, FakeTelegram (+28 more)

### Community 14 - "tasks.py"
Cohesion: 0.10
Nodes (31): digest_of_document(), Any, enabled_pack_ids(), The packs left switched on, plus `core`, or `None` when nothing has been…, connect(), Any, Yield an open psycopg connection with autocommit off. The caller commits., Any (+23 more)

### Community 15 - "run_parrot.py"
Cohesion: 0.07
Nodes (49): _kill_tree(), main(), open_browser(), parse_args(), port_answers(), Any, Namespace, Popen (+41 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (35): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+27 more)

### Community 17 - "vault.py"
Cohesion: 0.07
Nodes (38): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+30 more)

### Community 18 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 19 - "checks.py"
Cohesion: 0.09
Nodes (33): AsyncClient, asyncio, device_name(), load(), Any, The tokenizer, the model and the device it sits on, loaded once per process.…, One relevance logit per text, higher is better. Batched so forty passages is a…, score_pairs() (+25 more)

### Community 20 - "ingest/extract.py"
Cohesion: 0.07
Nodes (39): copy, _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact, Extraction, find_page() (+31 more)

### Community 21 - "test_grounding_values.py"
Cohesion: 0.11
Nodes (48): LogCaptureFixture, _dropped(), _log_values(), _long_text(), Any, Exception, fixture, parametrize (+40 more)

### Community 22 - "settings"
Cohesion: 0.10
Nodes (40): client_for(), consent(), ConsentConn, open_obligation(), pack_row(), parametrize, Snooze means 'not until this gets more urgent', so it can name the day it does., No new column: `already_said` is what makes the row quiet, and it reads this… (+32 more)

### Community 23 - "registry.py"
Cohesion: 0.10
Nodes (30): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders…, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, RuntimeError, Load the installed capability modules at runtime. The mirror of… (+22 more)

### Community 24 - "answer.py"
Cohesion: 0.05
Nodes (47): _advice_basis(), _advice_prompt(), answer_system(), _as_sentence(), _asked(), _conversation(), _distinct(), fuse() (+39 more)

### Community 25 - "pytest"
Cohesion: 0.06
Nodes (46): Any, Pulling finished sentences out of a JSON reply that is still being written. The…, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner (+38 more)

### Community 26 - "household.py"
Cohesion: 0.08
Nodes (45): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+37 more)

### Community 27 - "pipeline.py"
Cohesion: 0.10
Nodes (29): Chunk, What is actually embedded: the prefix plus the text, matching the tsvector…, parse(), ParsedDocument, The one call the pipeline makes. An unhandled mime type quarantines rather than…, commit_both_lanes(), document_title(), process() (+21 more)

### Community 28 - "test_lifecycle.py"
Cohesion: 0.10
Nodes (31): Parrot's local HTTP interface., Lifecycle, What the person asked for, once. The first request wins; later ones change…, fastapi_testclient, _client(), _eventually(), _launcher(), fixture (+23 more)

### Community 29 - "score.py"
Cohesion: 0.10
Nodes (34): Trace, cites(), _contains(), doc_stem(), grade(), held_back(), Judge, judge_all() (+26 more)

### Community 30 - "test_household.py"
Cohesion: 0.08
Nodes (48): is_first_person(), `(word, relation)` when the question asks about a relation's own documents,…, Whether this question is about the person asking. `other_names` are the display…, relation_asked(), _household_scope(), MonkeyPatch, parametrize, Person (+40 more)

### Community 31 - "Settings"
Cohesion: 0.08
Nodes (50): create_app(), checks(), ready(), setup(), system_status(), ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one…, Load the generator and the embedder before the first question, and record the… (+42 more)

### Community 32 - "test_pages.py"
Cohesion: 0.09
Nodes (37): base64, page_count(), PageUnavailable, _pdfium(), Any, LookupError, RuntimeError, One page of one document, as an image. Two callers want the same thing for… (+29 more)

### Community 34 - "sets_io.py"
Cohesion: 0.11
Nodes (31): collections, csv, choose(), Generated, main(), on_file(), pool(), Path (+23 more)

### Community 35 - "TelegramAdapter"
Cohesion: 0.10
Nodes (24): BaseTransport, Magic bytes first, filename suffix second, `application/octet-stream` last. A…, sniff_mime(), _attachment(), _pixels(), Any, Client, datetime (+16 more)

### Community 36 - "Registration"
Cohesion: 0.15
Nodes (5): An already-indexed document is not read again. Re-reading it would burn a…, Outcome, One line for the Parrot window. A person should be able to read what happened., The row as it now stands, plus whether this call is the one that created it., Registration

### Community 37 - "Any"
Cohesion: 0.17
Nodes (13): Measurement, by_subject(), FakeCursor, load_register(), Any, Every batch1 row as the facts extraction would write, through the statement it…, One member's statement must never drive another member's 15,300 cap., On 10 February 2027 Marcus's home contents cover has lapsed, while his motor… (+5 more)

### Community 38 - "Overdue"
Cohesion: 0.16
Nodes (14): close(), next_window(), Overdue, Any, date, LookupError, Past their date and never closed. A different problem from a reminder, shown…, Safe to show: there is no obligation with that id, or it is already closed. (+6 more)

### Community 39 - "test_api.py"
Cohesion: 0.10
Nodes (33): Answer, Answered. Asking for consent and naming what is missing are endings, not…, Asks, Protocol, The one method of `AnswerGraph` the harness uses. A test supplies a fake., client(), FakeGraph, TestClient (+25 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.19
Nodes (21): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), Any, date (+13 more)

### Community 41 - "retrieve.py"
Cohesion: 0.16
Nodes (19): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a…, ndarray, numpy, sqlite3, load_matrix(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.…, Return (N x D matrix of normalised embeddings, chunk ids). (+11 more)

### Community 42 - "sse"
Cohesion: 0.10
Nodes (35): Citation, A passage, named the way a person cites it and identified the way a link needs.…, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed…, Reading, a_citation(), advice_card(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order. (+27 more)

### Community 43 - "api.ts"
Cohesion: 0.06
Nodes (39): DocumentPage(), dynamic, metadata, runtime, RELATION_CHOICES, Place, PLACES, DocumentDetail() (+31 more)

### Community 44 - "ModelUnavailable"
Cohesion: 0.07
Nodes (31): DocumentTypeSpec, One kind of document the core recognises., Classification, classify(), _prompt(), Decide which of the core catalogue's document types a captured document is, or…, Never raises. An unavailable model is a classification failure, so it…, _schema() (+23 more)

### Community 45 - "test_answer_graph.py"
Cohesion: 0.07
Nodes (46): Abstained, _pack_for(), The pack that speaks for the best-scoring passage's document type, or None for…, Generated, build(), events(), passage(), Any (+38 more)

### Community 46 - "test_gate.py"
Cohesion: 0.10
Nodes (44): check(), check_advice(), check_content(), check_one(), Claim, _normal(), The grounding gate. Rule 3 in AGENTS.md: no claim without a citation. This…, Never raises, never rewrites a claim. It keeps, drops, or abstains. The whole-… (+36 more)

### Community 47 - "ParsedPage"
Cohesion: 0.06
Nodes (36): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, One flat list of chunks, ordinal running across the whole document., The page as `(is_heading, line)`, from the parser's structure when it has any. (+28 more)

### Community 48 - "build_router"
Cohesion: 0.09
Nodes (34): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, What changed, in the words the screen confirms it with. `was` is returned…, The row is gone from Today. `speaks_again` is null when it will not come back.…, 202. The vision pass is slower than a page load, so it is queued and this is… (+26 more)

### Community 49 - "HouseholdScope"
Cohesion: 0.14
Nodes (20): HouseholdScope, Any, Keep the owner's passages and the household's; set aside everybody else's. A…, Keep the passages of these people and of the household; set aside everybody…, What `AnswerGraph` is handed so it can scope without holding a connection.…, scope_passages(), scope_to(), _conn_returning() (+12 more)

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 51 - "FakeConn"
Cohesion: 0.08
Nodes (45): document_row(), fact_row(), FakeConn, obligation(), overdue_row(), date, ADR 0017: disabling insurance_agent switches off its voice, never a household's…, The point of the endpoint. An UPDATE alone loses the example we are trying to… (+37 more)

### Community 52 - "Any"
Cohesion: 0.26
Nodes (15): _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact(), _field_not_on_every_doc_type(), _held_per_month() (+7 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.17
Nodes (24): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError, Read and validate a pack's grounding corpus from its own folder on disk. A…, A pack's grounding corpus on disk does not match what its `sources.yaml`… (+16 more)

### Community 54 - "run.py"
Cohesion: 0.20
Nodes (17): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), main(), _note() (+9 more)

### Community 55 - "cli.py"
Cohesion: 0.22
Nodes (19): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+11 more)

### Community 56 - "ingest/quarantine.py"
Cohesion: 0.10
Nodes (33): blocked_reasons(), forget(), page_images(), Any, Path, ValueError, QuarantinedDocument, queue() (+25 more)

### Community 57 - "ADR index (0001-0018, with status)"
Cohesion: 0.09
Nodes (32): ADR 0006 - pypdfium2 renders the quarantine page images, ADR 0009 - next-themes and lucide-react are the only two web dependencies beyond the stack, Schedule-table questions remain weak (rank 2-4), ADR 0013: A question is understood before it is searched, and scoped before it is cut, The answer prompt carries today's date and names the scoped relation as who the question is about, AskRequest.history carries up to twelve earlier turns, A relevance-grading call and an 'answerable' schema flag were both dropped, Remaining failures are retrieval's to fix (cross-encoder plus lexical) (+24 more)

### Community 58 - "build.py"
Cohesion: 0.15
Nodes (23): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering…, Why the catalogue cannot supply `field` from every one of `doc_types`, or None., _class_name(), _docstring(), _field_line(), _header(), load() (+15 more)

### Community 59 - "Any"
Cohesion: 0.18
Nodes (10): _document(), FakeCursor, Any, date, datetime, _source(), _sum_insured(), test_facts_are_read_only_under_a_persons_confirmed_names() (+2 more)

### Community 60 - "answer.tsx"
Cohesion: 0.12
Nodes (28): Advice, AdviceCard(), AdviceNote(), AdviceWithheld(), capitalise(), sentence(), TONES, ADR-0016 (+20 more)

### Community 61 - "values.py"
Cohesion: 0.07
Nodes (36): _check(), collapse(), _cuts_a_number(), extract_values(), _groups(), _is_heading(), number_tokens(), _pack() (+28 more)

### Community 62 - "ConfigurationError"
Cohesion: 0.08
Nodes (28): The local API. Liveness is intentionally separate from assistant readiness.…, collections_abc, contextlib, One place that opens a connection to the one database. `Settings.database_url`…, Restart and shut down: asked for by the screens, carried out by the supervisor.…, _chat_ids(), ConfigurationError, _flag() (+20 more)

### Community 63 - "lock.ts"
Cohesion: 0.07
Nodes (46): ref_node_crypto, dynamic, GET(), grant(), POST(), runtime, ALLOWED, Context (+38 more)

### Community 64 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 65 - "models.py"
Cohesion: 0.09
Nodes (39): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, CloseRequest, ConfirmNameRequest, ConsentRequest, ConsentRequiredEvent (+31 more)

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
Cohesion: 0.16
Nodes (18): glossary(), The catalogue's words and every enabled pack's, unioned; a pack's wording wins…, The question with each declared phrase replaced by what the documents print,…, Only the lines the question used, so the prompt grows by what it needs and no…, reworded(), _vocabulary(), pack(), A shortfall nobody can act on is half an answer. `closed_by` is what makes the… (+10 more)

### Community 70 - "advice-consent.tsx"
Cohesion: 0.17
Nodes (17): Consent, ConsentPrompt(), agree(), settle(), State, ADR-0016, AdviceConsentSection(), fetchConsents() (+9 more)

### Community 71 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 72 - "folder.py"
Cohesion: 0.18
Nodes (10): IngestJob, What a capture returns: a registered document, and whether we had seen it…, _Pending, datetime, Path, The watched-folder capture adapter. A person drops a scan into a folder and it…, Every file in the watched folder that is worth looking at at all., Advance the debounce by `elapsed` seconds and return the files now ready. Time… (+2 more)

### Community 73 - "Hybrid Retrieval: Dense Plus Full-Text"
Cohesion: 0.18
Nodes (11): No New Runtime Dependency Without an ADR, Never Generate SQL at Runtime, baseline.py Is Disposable and Never a Measurement, ports.py, the Seam With Lane B, bge-reranker-v2-m3 Cross-Encoder, 40 Down to 6, Hybrid Retrieval: Dense Plus Full-Text, Reciprocal Rank Fusion, k=60, The Household's Eleven Policies (+3 more)

### Community 74 - "scope.py"
Cohesion: 0.22
Nodes (16): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Whose question is this, and whose documents may answer it. "What is my term… (+8 more)

### Community 75 - "ADR 0011: The household is people and aliases, and the owner is one of them"
Cohesion: 0.17
Nodes (19): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), The owner is a row, not a config value baked at install, people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), A resolved person is shown as a chip, like a citation, The roster is derived from documents, then confirmed (+11 more)

### Community 76 - "test_advice_core.py"
Cohesion: 0.06
Nodes (50): Channel, current(), grant(), HouseholdConsents, _latest(), NoOwner, Any, RuntimeError (+42 more)

### Community 77 - "test_modules.py"
Cohesion: 0.13
Nodes (25): Capability modules. A module reads typed rows and writes its own namespace. It…, already_said(), datetime, True when this exact window has already been mentioned. The comparison is by…, Everything inside a lead window that has not already been said for that window.…, sweep(), FakeConn, obligation_row() (+17 more)

### Community 78 - "today/page.tsx"
Cohesion: 0.09
Nodes (38): dynamic, HouseholdPage(), metadata, runtime, dynamic, GoneNote(), Header(), isUrgent() (+30 more)

### Community 79 - "tokens/page.tsx"
Cohesion: 0.20
Nodes (17): Motion(), Colour(), FaceCard(), Focus(), INKS, metadata, RADII, Radius() (+9 more)

### Community 80 - "preview.tsx"
Cohesion: 0.11
Nodes (19): DesignPreviewPage(), metadata, answers, DesignPreview(), Direction, directions, Item, items (+11 more)

### Community 81 - "routes.py"
Cohesion: 0.12
Nodes (23): ModuleSummary, PacksResponse, PackSummary, PersonModel, VaultDocument, VaultFact, VaultResponse, _as_module_summary() (+15 more)

### Community 82 - "Two-stage quarantine with a vision-language second pass"
Cohesion: 0.12
Nodes (19): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Two-stage quarantine with a vision-language second pass, Batch 4: the deliberately hard documents, A full policy wording registers as policy_schedule, Task: review every quarantined document and label the failure, Task: sign off the capture-to-database path against the data inventory, Measurement is owned separately from the engine (+11 more)

### Community 83 - "Any"
Cohesion: 0.12
Nodes (7): ConsentCursor, Fails, FakeCursor, Any, The parameters of the one statement containing `needle`. Fails loudly if it…, Yields `before`, then raises. `ask` raises at once., Remembers what `grant` or `withdraw` inserted, so the next read of the latest…

### Community 84 - "Ollama"
Cohesion: 0.17
Nodes (10): answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, Ollama, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.…, Batch embeddings. Falls back to the legacy endpoint on old servers., Hit (+2 more)

### Community 85 - "test_the_code_scored_metrics_come_out_as_arithmetic_says"
Cohesion: 0.15
Nodes (11): The last question's contexts and candidate count, then a clean slate., Each question on its own thread, so no answer is a follow-up to the one before., Recorder, trace_all(), _table(), FakeGraph, FakeRetriever, KeepAll (+3 more)

### Community 86 - "main"
Cohesion: 0.12
Nodes (21): approve(), pending(), PendingValue, Any, date, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it., Every value still waiting for review, oldest first, optionally for one pack. (+13 more)

### Community 87 - "ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.11
Nodes (27): Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration), Published guidance is a second evidence lane, never a second household, Every passage carries a kind: document, inventory or guidance, ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, The adult rule: advice is withheld for a person under 21 or a child with no date of birth on file, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel) (+19 more)

### Community 88 - "test_both_ask_endpoints_hand_the_graph_the_same_advice_ports"
Cohesion: 0.13
Nodes (14): advising(), conn(), graph(), _padded(), fixture, MonkeyPatch, One construction for both. With any port missing the graph declines advice, so…, The same pack, its consent wording and disclaimer surrounded by the whitespace… (+6 more)

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "item-row.tsx"
Cohesion: 0.24
Nodes (10): countdown(), detail(), figure(), ItemRow(), longDate(), sentence(), TONE, WORD (+2 more)

### Community 91 - "test_tax_pack.py"
Cohesion: 0.22
Nodes (15): _basis(), _latest(), _matched(), _published(), FactRow, parametrize, The tax pack's advice, run on batch 1's own SRS statements and Notices of…, The shape id the answer graph picks for a question with both packs enabled,… (+7 more)

### Community 92 - "contracts.py"
Cohesion: 0.15
Nodes (21): Advice, Answering, Exclusions, Grounding, Guardrails, ModuleTrigger, Persona, BaseModel (+13 more)

### Community 93 - "Scoped"
Cohesion: 0.18
Nodes (12): The result of asking "whose is this?" of a question and its passages., A first-person question that nothing of the owner's can answer. The interesting…, Scoped, 13 September: "how much is my son's life insurance?" came back as the owner's…, 13 September: "is my dad's hospital cover still active?" was scoped to Lim Ah…, "When does Rachel's policy renew?" is scoped to Rachel by name, with no…, test_a_question_about_a_parent_names_them_as_who_it_is_about_and_carries_todays_date(), apply() (+4 more)

### Community 94 - "InstalledPack"
Cohesion: 0.08
Nodes (34): AdviceShape, FactInput, A printed fact a calculator reads, named by where it is printed rather than…, One kind of advice question, and everything its calculator needs to answer it., date, The shape a question asks for, matched from the pack's own phrases without a…, The first advising pack whose review a question asks for, as a shape the advise…, _review_asked() (+26 more)

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
Cohesion: 0.09
Nodes (39): PackManifest, A domain pack, authored as one YAML file: grounding, persona, answering and…, _advised(), _checked(), _insurance(), parametrize, Path, The contracts are the platform. If these break, something important changed. (+31 more)

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.10
Nodes (21): The Purely Additive Migration Exception, Contracts and Migrations Are Their Own PR, Sources of Truth Generate Their Outputs, Snooze Means Not Until This Gets More Urgent, The Three Things Agents Get Wrong Here, Generated Files Committed Alongside Their Source, benefit_illustration Document Type, birth_certificate Document Type (+13 more)

### Community 100 - "_Answering"
Cohesion: 0.50
Nodes (4): _Answering, The event stream one request is sending, held where the request's cleanup can…, Close the answer stream when the request ends, whatever ended it. Requires…, Conn

### Community 101 - "._categories_read_a_declared_field"
Cohesion: 0.33
Nodes (3): Whether any document type in the catalogue declares `field`., An advice shape that names a missing role or key fails at load time. Caught…, model_validator

### Community 102 - "The five-lane split (five people, nine weeks, three builders)"
Cohesion: 0.09
Nodes (30): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The domain pack manifest, The expansion model: two axes, not one list, The golden set: answerable, hard negatives, adversarial, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build (+22 more)

### Community 103 - "Data inventory: identity data, DOBs and loans"
Cohesion: 0.17
Nodes (15): Data inventory: identity data, DOBs and loans, The lock is a screen lock, not encryption, next dev binds every interface, not loopback, Telegram capture route and delete-at-source, What crosses a boundary, Governance artefact set, Write unverified rather than assert, The final ILP report (+7 more)

### Community 104 - "test_rerank.py"
Cohesion: 0.27
Nodes (11): CrossEncoderReranker, passage_text(), What the reranker reads: the one-line context, when a chunk carries one, then…, Implements `core.graph.ports.Reranker`. Reorders by the cross-encoder's score…, _passage(), skipif, The cross-encoder reranker: what it does with scores, and that the scores are…, test_reorders_by_the_cross_encoder_and_keeps_retrievals_score() (+3 more)

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
Cohesion: 0.16
Nodes (18): itertools, re, Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks. Paperwork is short and…, _split_page(), pack() (+10 more)

### Community 109 - "inventory.py"
Cohesion: 0.24
Nodes (10): holdings(), Any, The documents on file, read from `facts` rather than searched for. "Do I have…, Rows of `INVENTORY`, one holding per document that prints the field an enabled…, UUID, Holdings come from `facts`, one per document that prints the name the…, row(), test_a_pack_that_declares_no_categories_holds_nothing() (+2 more)

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

### Community 115 - "next"
Cohesion: 0.08
Nodes (29): lucide-react, next, react, AppLayout(), dynamic, runtime, ROWS, LockButton() (+21 more)

### Community 116 - "_answer_events"
Cohesion: 0.15
Nodes (17): ErrorEvent, The stream broke after it began. A client cannot read an HTTP status by then., A document and a page, as a person would cite it — or, for published guidance,…, Source, TodayItem, _answer_events(), _cite(), _link() (+9 more)

### Community 117 - "FieldSpec"
Cohesion: 0.18
Nodes (9): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected, FieldSpec, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer. (+1 more)

### Community 118 - "worker.py"
Cohesion: 0.20
Nodes (15): lifespan(), install_best_effort(), Install at startup without being able to stop startup. Both processes that own…, _beat_needs_its_own_process(), celery_argv(), main(), Any, Namespace (+7 more)

### Community 119 - "sha256"
Cohesion: 0.12
Nodes (24): CaptureAdapter, datetime, Protocol, The one interface every capture channel satisfies. receive(payload, mime,…, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., sha256(), Capture adapters. Every channel a document can arrive through satisfies one… (+16 more)

### Community 120 - "installed_packs"
Cohesion: 0.18
Nodes (14): installed_packs(), _load_one(), Path, Every pack directory holding a pack.yaml, in a stable order. Directories whose…, _pack_row(), packs(), Every installed pack. Documents and facts are the core's (ADR 0017), so none…, Switch one pack on or off. Raises `UnknownPack` rather than silently doing… (+6 more)

### Community 121 - "capture.py"
Cohesion: 0.06
Nodes (38): FolderSettings, Dispatcher, Inline, Protocol, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Send (+30 more)

### Community 122 - "packs/page.tsx"
Cohesion: 0.20
Nodes (12): ADR-0017, AlwaysOn(), dynamic, metadata, ModuleRow(), PackCard(), PacksPage(), runtime (+4 more)

### Community 123 - "ADR 0002 - One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (7): ADR 0001 - Record architecture decisions, ADR 0002 - One PostgreSQL instance for everything, Reciprocal rank fusion of dense and lexical, ADR 0003 - PaperBrain informs the pattern, not the module, PaperBrain prototype, Contracts before code, Lane A - Integration and product

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.17
Nodes (12): Task: benchmark the workstation and publish the numbers, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, The deliberately naive retrieval baseline, Committed runs are never deleted, Yew Mun's generated task list, Hybrid retrieval, not embeddings alone, Chunking respects paragraphs (+4 more)

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 126 - "test_a_document_still_in_the_inbox_is_not_forgotten"
Cohesion: 0.18
Nodes (11): filed_document(), inbox(), Path, Capture would register it again within a minute, so the button would only…, A watched folder holding one document, hashed the way the ingest registered it., v1 keeps the inbox as the document store, so this is a real state, not a fault., test_a_document_still_in_the_inbox_is_not_forgotten(), test_a_document_whose_file_left_the_inbox_is_409_not_500() (+3 more)

### Community 127 - "knowledge.py"
Cohesion: 0.22
Nodes (16): Categories, Category, A kind of document a household holds, recognised by words printed in its name.…, Asked, categories_asked(), categorise(), mentions(), _pattern() (+8 more)

### Community 128 - "The case for synthetic evaluation data"
Cohesion: 0.18
Nodes (11): Qwen-SEA-LION-v4-4B-VL extraction ceiling, Register first, then generate, SYNTHETIC DOCUMENT footer, Ground truth for free, The 40-document holdout corpus, The case for synthetic evaluation data, Two withdrawn synthetic-data controls, extraction_f1 (+3 more)

### Community 129 - "Domain pack"
Cohesion: 0.12
Nodes (21): The demonstration run sheet, Step 8 - switch a pack off, Step 6 - the abstention, Step 7 - the refusal to act, Step 2 - the source chip, Derive the roster, then confirm it, Exactly one owner, enforced by the database, facts.subject is never normalised (+13 more)

### Community 130 - "test_a_client_that_leaves_after_the_card_commits_one_record"
Cohesion: 0.18
Nodes (10): next_kind(), The kind of the next event on the wire., Starlette never closes a body iterator a disconnected client stopped pulling.…, The ruling's case as it happens on a socket: Starlette sends the card and at…, What the API owns when a stream is closed with the graph still parked on the…, The graph's own cleanup can fail -- for example the record insert raises -- and…, test_a_client_that_leaves_after_the_card_commits_one_record(), test_a_client_that_leaves_mid_explanation_still_commits_what_it_was_shown() (+2 more)

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
Cohesion: 0.29
Nodes (10): AlertConfig, Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order., srs_row(), test_a_firing_older_than_the_debounce_window_fires_again(), test_a_metric_no_query_defines_cannot_fire(), test_a_recent_firing_is_debounced() (+2 more)

### Community 138 - "F1"
Cohesion: 0.22
Nodes (6): extraction_f1(), F1, FactRow, One row of the `facts` table, as the harness reads it: which document, which…, Field extraction scored against the register, overall and by document type. The…, test_extraction_f1_scores_only_indexed_documents_against_the_register()

### Community 139 - "PaperBrain"
Cohesion: 0.20
Nodes (10): The code pass of the knowledge graph, Nobody edits core/contracts.py in a feature pull request, Lane A - Integration and product, The semantic pass of the knowledge graph, Triage prompt: four buckets, no code written, Ninety protected minutes a week of integration, Christian's generated task list, PaperBrain (+2 more)

### Community 140 - "ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.33
Nodes (9): guardrails.abstain_below was calibrated on un-prompted scores, ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts, chunks.tsv built from context_prefix || text, Context prefix: title - type - heading - page, rag_probe2 before/after similarity table (six policies, 13 September), scripts/reindex.py rebuilds chunks and vectors, Chunks follow the document's structure (Docling heading labels), Task prompts: embed_query and embed_documents (+1 more)

### Community 141 - "chat/route.ts"
Cohesion: 0.11
Nodes (22): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+14 more)

### Community 142 - "same_value"
Cohesion: 0.25
Nodes (9): _as_date(), _as_number(), date, Decimal, The register's text against an extracted value, each normalised the way the…, The ways a register value is printed. `2027-04-11` appears on a schedule as "11…, same_value(), value_forms() (+1 more)

### Community 143 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 144 - "test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them"
Cohesion: 0.22
Nodes (5): ClosingSpy, Wraps an event generator to record whether something called `.close()` on it,…, Starlette's own body iteration (`iterate_in_threadpool`) never calls `.close()`…, test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them(), spying()

### Community 145 - "schedule.py"
Cohesion: 0.21
Nodes (13): beat_schedule(), cron_expressions(), crontab_from(), manifest(), Any, When the nightly sweeps run, read from the modules' own manifests. A module…, A five-field cron expression as Celery understands it., The cron line for each swept module, by module id. Testable without Celery… (+5 more)

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
Cohesion: 0.29
Nodes (3): Cursor, Any, Protocol

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (8): parrot-sweep shimmer animation, Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, An answer with the page it came from, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "build_team_tasks.py"
Cohesion: 0.33
Nodes (8): difflib, main(), Path, Generate each member's task list from the master task CSV. python…, _read_rows(), _render(), _week_key(), _write()

### Community 157 - "pathlib"
Cohesion: 0.07
Nodes (32): argparse, A person's approval, standing between a model's extraction and any calculator…, enabled_packs(), The installed packs a person has left switched on, as loaded pack objects. This…, The one Celery application, built from `Settings`. Every setting here is a…, Validate a document register before it is handed over. python -m…, datetime, jinja2 (+24 more)

### Community 158 - "Adversarial testing from week 7"
Cohesion: 0.25
Nodes (8): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Adversarial testing from week 7, Prompt injection carried inside a document, Scope attack: asking it to act, Task: run adversarial Set C and write up the findings, Adversarial Set C (15 questions that should not be answered), Golden Set C - adversarial (15)

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 160 - "AdviceRecord"
Cohesion: 0.33
Nodes (4): AdviceRecord, Every advised or withheld answer's full basis, so it can be reconstructed later…, test_record_insert_includes_the_sha256_of_the_disclaimer(), Log

### Community 161 - "Every Fact Row Cites Its Source"
Cohesion: 0.33
Nodes (7): Every Fact Row Cites Its Source, A Correction Cannot Invent a Row, Every Node Writes One Line to traces, The Ingestion Pipeline, The Pipeline Forks Into Retrieval and Facts Lanes, Numbers Come From Postgres, Never From the Model, macOS Worker Runs Celery Solo

### Community 162 - "_as_response"
Cohesion: 0.15
Nodes (13): AskRequest, AskResponse, Claim, The whole answer, once. `text` is the consent wording when `kind` is…, One sentence and the passages it was traced to. Never emitted without…, _as_response(), _as_source(), ask() (+5 more)

### Community 163 - "generic"
Cohesion: 0.33
Nodes (6): generic(), _named(), phrase(), For a document type without hand-written phrasings: name the field and the…, A phrasing that needs every named key filled, or it does not apply to the row., Phrasing

### Community 164 - "Passage"
Cohesion: 0.08
Nodes (20): Every number or identifier in a sentence that no cited passage prints. An…, Does this sentence state a number or identifier, and is every one printed by…, states_a_printed_value(), unprinted_numbers(), The answer graph. Router, retrieve, rerank, grounding gate, then answer or…, Passage, Protocol, How a passage names itself: the document and the page, as a person would say it. (+12 more)

### Community 165 - "PARROT evaluation harness"
Cohesion: 0.38
Nodes (7): abstention_rate, PARROT evaluation harness, Set A, answerable, Set B, hard negatives, Set C, adversarial, The golden question sets, must_cite_page from field_pages

### Community 166 - "RagasJudge"
Cohesion: 0.32
Nodes (6): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts(), Ragas 0.4 metrics through Ollama's OpenAI-compatible endpoint. Imported lazily…

### Community 167 - "The autonomy statement"
Cohesion: 0.29
Nodes (7): The autonomy statement, Governance claims traced to enforcement points, IMDA mappings and autonomy statement artefact, The facts table as an extension point, Constraint: fully offline, Explicitly not doing: cloud, hosted vectors, autonomous spending, Roadmap phase 2 - facts

### Community 168 - "_market"
Cohesion: 0.29
Nodes (7): _market(), _market_compares_an_undeclared_field(), A market comparison of the held hospital plan, on `compare_fields`, ordered by…, `annual_premium` is printed on no policy schedule; the market's sources publish…, Two household documents can only be compared on what a household document…, test_a_market_comparison_may_compare_a_field_only_its_sources_publish(), test_an_own_comparison_may_not_compare_a_field_only_sources_publish()

### Community 169 - "test_the_inventory_always_reads_core_documents"
Cohesion: 0.29
Nodes (3): ADR 0017: a document is the core's, so the query includes `core` whatever is…, test_the_inventory_always_reads_core_documents(), cursor()

### Community 170 - "Missing"
Cohesion: 0.47
Nodes (4): Missing, What a calculator returns when a fact or a rule value it needed was not there…, Adviser, date

### Community 171 - "current_lead"
Cohesion: 0.33
Nodes (6): current_lead(), The tightest lead window this obligation has entered, or None if it has entered…, date, parametrize, test_every_firing_is_scoped_and_cites_a_page(), test_the_tightest_entered_window_is_the_current_one()

### Community 172 - "_on_page"
Cohesion: 0.47
Nodes (6): SimpleNamespace, _cell(), _on_page(), test_a_table_is_kept_as_label_and_value_lines_in_reading_order(), test_a_wider_table_keeps_every_column_and_a_spanned_cell_once(), test_an_item_with_neither_text_nor_cells_is_still_skipped()

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

### Community 179 - "The synthetic-to-real gap"
Cohesion: 0.40
Nodes (5): The 40-document redacted holdout, The synthetic-to-real gap, Consent and redaction protocol, Task: write the PDPA position on using synthetic data, Task: evaluation run 3 plus the holdout run

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 185 - "scored"
Cohesion: 0.40
Nodes (4): fixture, MonkeyPatch, A scorer that ranks by the number the passage text ends with, and records what…, scored()

### Community 186 - "eslint.config.mjs"
Cohesion: 0.33
Nodes (5): @eslint/eslintrc, ref_node_path, ref_node_url, compat, eslintConfig

### Community 201 - "Alert"
Cohesion: 0.25
Nodes (5): Alert, What the debounce is keyed on: this metric, for this person and thing, in this…, Two lapsed policies on one person are two alerts, and saying one must not…, test_the_debounce_key_separates_people(), test_the_debounce_key_separates_two_policies_of_one_person()

### Community 204 - "package.json"
Cohesion: 0.11
Nodes (16): class-variance-authority, clsx, eslint, eslint-config-next, postcss, react-dom, tailwind-merge, tailwindcss (+8 more)

## Ambiguous Edges - Review These
- `Sources of Truth Generate Their Outputs` → `pack.yaml Is the Only Place a Field Name Is Written`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `Corpus Batches Are Not in Git` → `The Corpus Is Synthetic and Committed`  [AMBIGUOUS]
  NOTICE.md · relation: semantically_similar_to
- `Domain Packs` → `Core Document Catalogue (ADR 0017)`  [AMBIGUOUS]
  README.md · relation: conceptually_related_to
- `Fill the Register Before Generating Documents` → `Motor Vehicle Hire Purchase Agreement Template`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to
- `Real Organisations May Be Named` → `Republic of Xinkapow, the Invented Jurisdiction`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to
- `The Lim Household, Tampines` → `Republic of Xinkapow, the Invented Jurisdiction`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to
- `Provenance register for corpus sg_protection_guidance` → `Lane A - Christian, integration and product`  [AMBIGUOUS]
  packs/insurance_agent/grounding/sg_protection_guidance/sources.yaml · relation: references
- `Provenance register for corpus sg_protection_guidance` → `Lane D - Zee, domain packs and interface`  [AMBIGUOUS]
  team/README.md · relation: conceptually_related_to
- `LIA 2022 Protection Gap Study Key Findings` → `Protection rule of thumb: 9x annual income for death and TPD, 4x for critical illness`  [AMBIGUOUS]
  packs/insurance_agent/grounding/sg_protection_guidance/sources.yaml · relation: cites

## Knowledge Gaps
- **354 isolated node(s):** `npx`, `@modelcontextprotocol/server-filesystem`, `_Formatter`, `parrot`, `setup.sh script` (+349 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1571 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Sources of Truth Generate Their Outputs` and `pack.yaml Is the Only Place a Field Name Is Written`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Corpus Batches Are Not in Git` and `The Corpus Is Synthetic and Committed`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Domain Packs` and `Core Document Catalogue (ADR 0017)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Fill the Register Before Generating Documents` and `Motor Vehicle Hire Purchase Agreement Template`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Real Organisations May Be Named` and `Republic of Xinkapow, the Invented Jurisdiction`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `The Lim Household, Tampines` and `Republic of Xinkapow, the Invented Jurisdiction`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Provenance register for corpus sg_protection_guidance` and `Lane A - Christian, integration and product`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._