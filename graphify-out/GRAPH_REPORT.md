# Graph Report - igd-capstone-2026  (2026-09-29)

## Corpus Check
- 306 files · ~700,700 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 33 file(s) not represented in the graph (top: (none) 15, .csv 5, .jsonl 3)

## Summary
- 4505 nodes · 11137 edges · 198 communities (168 shown, 24 thin omitted)
- Extraction: 90% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 1050 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2c4abcb9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- typing
- pytest
- ScriptedOllama
- AnswerGraph
- validate
- advice/__init__.py
- Provenance register for corpus sg_protection_guidance
- test_advice_module.py
- run.py
- test_ingest_pipeline.py
- test_grounding_index.py
- test_worker_queue.py
- FolderAdapter
- test_telegram_capture.py
- Ollama
- ParsedPage
- bench_runtime.py
- vault.py
- support.js
- checks.py
- ingest/extract.py
- test_grounding_values.py
- Settings
- registry.py
- answer.py
- SentenceScanner
- household.py
- pipeline.py
- test_lifecycle.py
- score.py
- test_household.py
- .load
- test_pages.py
- extract_values
- sets_io.py
- TelegramAdapter
- test_eval_harness.py
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
- packs.py
- cli.py
- worker.py
- ADR index (0001-0018, with status)
- build.py
- Any
- source-chip.tsx
- values.py
- ConfigurationError
- lock.ts
- dependencies
- routes.py
- PARROT Interface Design Pack
- export-design-preview.cjs
- The Four Surfaces
- pack
- advice-consent.tsx
- devDependencies
- base.py
- Hybrid Retrieval: Dense Plus Full-Text
- scope.py
- ADR 0011: The household is people and aliases, and the owner is one of them
- FakeConn
- test_modules.py
- today/page.tsx
- test_the_code_scored_metrics_come_out_as_arithmetic_says
- preview.tsx
- reference_for
- Two-stage quarantine with a vision-language second pass
- Any
- Ollama
- F1
- main
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- test_a_document_still_in_the_inbox_is_not_forgotten
- components.json
- _as_module_summary
- test_tax_pack.py
- contracts.py
- Passage
- InstalledPack
- The Lim Household, Tampines
- ADR 0007 - The graph ships before retrieval and before a checkpoint table
- Lane C - Governance and assurance
- test_contracts.py
- Core Document Catalogue (ADR 0017)
- generate_lim_documents.py
- _ordered
- The five-lane split (five people, nine weeks, three builders)
- Data inventory: identity data, DOBs and loans
- test_rerank.py
- Roadmap phase 3 - reminders
- web/ - the PARROT interface
- The document register as ground truth
- ingest.py
- Tax and Reliefs — contract changes this pack needs
- Reminder, Alert and Tracker Registers
- FakeCursor
- example_pack template manifest
- paperbrain/extract.py
- _closes
- tokens/page.tsx
- _answer_events
- Integration review
- usable
- test_registration.py
- api/__init__.py
- capture.py
- packs/page.tsx
- ADR 0002 - One PostgreSQL instance for everything
- The deliberately naive retrieval baseline
- Running the evaluation harness
- grounding/__init__.py
- create_app
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
- ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts
- answer.tsx
- modules/__init__.py
- scripts
- test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them
- schedule.py
- PrivateCare Policy Wording Template
- alert module manifest
- test_reindexing_replaces_chunks_and_leaves_facts_alone
- test_the_catalogue_declares_metrics_that_exist
- app/layout.tsx
- The Grounding Gate
- Authoring a domain pack
- ADR 0008 - Ingestion runs on a Celery worker
- Cursor
- DesignPreview evaluation harness
- pathlib
- main
- Adversarial testing from week 7
- Writing an ADR
- Every Fact Row Cites Its Source
- HouseholdAdviceLog
- PARROT evaluation harness
- RagasJudge
- The autonomy statement
- test_the_inventory_always_reads_core_documents
- Calculation
- Page one as plain Label: value lines
- Project skills
- pull_request_template.md
- _as_consent
- The synthetic-to-real gap
- filesystem
- Due
- quiet_engine
- eslint.config.mjs
- One Database
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

## Communities (198 total, 24 thin omitted)

### Community 0 - "typing"
Cohesion: 0.05
Nodes (49): The page a person sees while Parrot starts, served by the engine itself. **Why…, The whole page. `screens_url` is escaped into a data attribute, never into…, render(), collections_abc, The Telegram capture adapter. Same interface as the folder: `receive(payload,…, The owner's consent to a pack's advice, append-only (ADR 0016). Consent is the…, The record of every advised or withheld answer (ADR 0016). `advice_records`…, _columns() (+41 more)

### Community 1 - "pytest"
Cohesion: 0.06
Nodes (45): hybrid_score(), HybridRetriever, identifiers(), prints(), The tokens in a question that look like something printed rather than said: a…, Whether the chunk prints the identifier, ignoring case and the spacing inside…, The cosine similarity, lifted to `IDENTIFIER_HIT` when the chunk prints an…, Implements `core.graph.ports.Retriever`. Built where the connection is, like… (+37 more)

### Community 2 - "ScriptedOllama"
Cohesion: 0.07
Nodes (65): AdviceCard, AdviceWithheld, ConsentRequired, Finished, One sentence that has passed the gate, with the citations it passed on. It will…, Everything that is only knowable once the last sentence is in. `quarantined`…, Advice was asked for and the owner has not agreed to this pack's current…, Advice could not be worked out, and `missing` says what it needs, in the pack's… (+57 more)

### Community 3 - "AnswerGraph"
Cohesion: 0.15
Nodes (33): AnswerGraph, Declined, The pack's own decline, signed with its disclaimer, and a question it can…, A request for a recommendation or a judgement, declined before anything is…, Built once, asked many times. Holds no connection: retrieval does., test_advice_is_declined_when_the_graph_was_given_no_adviser(), FakeInventory, FixedRetriever (+25 more)

### Community 4 - "validate"
Cohesion: 0.09
Nodes (40): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), date, Path (+32 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.07
Nodes (80): Figure, Input, One fact or rule value a calculation was built on, carrying its own citation.…, One number a calculator produced, and the words a sentence must use to state…, _ambiguous(), _amount(), _band(), _band_label() (+72 more)

### Community 6 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.05
Nodes (64): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, MediShield Life (CPF Board), Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022 (+56 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.14
Nodes (55): Missing, What a calculator returns when a fact or a rule value it needed was not there…, calculate(), assert_nothing_negative(), basis(), fact(), figures_of(), _gap_basis() (+47 more)

### Community 8 - "run.py"
Cohesion: 0.14
Nodes (24): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), main(), _note() (+16 more)

### Community 9 - "test_ingest_pipeline.py"
Cohesion: 0.08
Nodes (50): classify(), Never raises. An unavailable model is a classification failure, so it…, extract(), Never raises. A failure is a reason, and a reason routes the document to…, Generated, FakeOllama, insurance(), iras() (+42 more)

### Community 10 - "test_grounding_index.py"
Cohesion: 0.09
Nodes (41): CaptureFixture, index_pack(), IndexReport, Any, date, Path, Upsert this pack's sources and stage the values a changed one prints. A pack…, Insert or refresh the source's row, and return its id. (+33 more)

### Community 11 - "test_worker_queue.py"
Cohesion: 0.09
Nodes (33): The idempotency key for the whole platform. Bytes, not hex: `documents.sha256`…, sha256(), Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker. Celery is imported here rather…, index_folder(), Path (+25 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.15
Nodes (25): FolderAdapter, FolderSettings, Satisfies `CaptureAdapter`. Holds no database handle — it is given a…, FolderCapture, Begin watching. Returns False, with a logged reason, when it cannot., A daemon thread that polls the watched folder until `stop()` or process exit., FakeRegistrar, datetime (+17 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.08
Nodes (41): BaseTransport, RuntimeError, Safe to show: never contains the token., TelegramSettings, TelegramUnavailable, MockTransport, build(), FakeRegistrar (+33 more)

### Community 14 - "Ollama"
Cohesion: 0.08
Nodes (59): blocked_reasons(), forget(), Any, Path, ValueError, QuarantinedDocument, queue(), The second stage of quarantine: the page image, read by the vision-language… (+51 more)

### Community 15 - "ParsedPage"
Cohesion: 0.13
Nodes (22): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own…, One flat list of chunks, ordinal running across the whole document., The page as `(is_heading, line)`, from the parser's structure when it has any. (+14 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (35): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+27 more)

### Community 17 - "vault.py"
Cohesion: 0.09
Nodes (30): correct(), Corrected, Any, LookupError, Store what a person says this field actually says, and keep what it used to…, Safe to show: there is no fact with that id., What changed, in the words the screen will use to confirm it., UnknownFact (+22 more)

### Community 18 - "support.js"
Cohesion: 0.06
Nodes (75): boot(), bundledBlob(), cdnScriptFor(), collectProps(), compileAttr(), compileTemplate(), contentKey(), createComponentFactory() (+67 more)

### Community 19 - "checks.py"
Cohesion: 0.10
Nodes (30): AsyncClient, asyncio, device_name(), load(), Any, Say it, once per process. A passage cut at the cap is scored on its first part…, The tokenizer, the model and the device it sits on, loaded once per process.…, One relevance logit per text, higher is better. Batched so forty passages is a… (+22 more)

### Community 20 - "ingest/extract.py"
Cohesion: 0.09
Nodes (32): _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact, Extraction, find_page(), _normalise() (+24 more)

### Community 21 - "test_grounding_values.py"
Cohesion: 0.14
Nodes (36): parse_value(), The number a reported value states for its unit, or `None` when it states…, _dropped(), _log_values(), Any, Decimal, fixture, LogCaptureFixture (+28 more)

### Community 22 - "Settings"
Cohesion: 0.10
Nodes (52): Whether Telegram capture should start. An unset token means "not this…, Settings, client_for(), consent(), ConsentConn, pack_row(), parametrize, The point of the endpoint. An UPDATE alone loses the example we are trying to… (+44 more)

### Community 23 - "registry.py"
Cohesion: 0.08
Nodes (42): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders…, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, RuntimeError, Load the installed capability modules at runtime. The mirror of… (+34 more)

### Community 24 - "answer.py"
Cohesion: 0.06
Nodes (44): Claim, AdviceRecord, Every advised or withheld answer's full basis, so it can be reconstructed later…, Abstained, _advice_basis(), _advice_prompt(), answer_system(), _as_sentence() (+36 more)

### Community 25 - "SentenceScanner"
Cohesion: 0.10
Nodes (28): Any, What document would have answered this, if the model said. Read once, at the…, Feed it deltas; it returns whichever sentences became complete because of them.…, Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes…, Find `"sentences": [` once. Everything before it is of no interest. Searching…, SentenceScanner, drip() (+20 more)

### Community 26 - "household.py"
Cohesion: 0.08
Nodes (47): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+39 more)

### Community 27 - "pipeline.py"
Cohesion: 0.07
Nodes (40): Chunk, What is actually embedded: the prefix plus the text, matching the tsvector…, fixed(), from_facts(), _label(), Any, date, What a person is shown. The key is the catalogue's word for it; the subject… (+32 more)

### Community 28 - "test_lifecycle.py"
Cohesion: 0.12
Nodes (28): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor.…, What the person asked for, once. The first request wins; later ones change…, fastapi_testclient, _client(), _eventually(), _launcher(), parametrize (+20 more)

### Community 29 - "score.py"
Cohesion: 0.10
Nodes (33): Trace, cites(), _contains(), doc_stem(), grade(), held_back(), Judge, judge_all() (+25 more)

### Community 30 - "test_household.py"
Cohesion: 0.08
Nodes (46): is_first_person(), `(word, relation)` when the question asks about a relation's own documents,…, Whether this question is about the person asking. `other_names` are the display…, relation_asked(), _household_scope(), MonkeyPatch, parametrize, Person (+38 more)

### Community 31 - ".load"
Cohesion: 0.11
Nodes (32): ModelWarmth, Whether the generator has been loaded yet, and where it landed. Written by one…, Load the generator and the embedder before the first question, and record the…, warm_models(), _ollama_answering(), Any, MonkeyPatch, parametrize (+24 more)

### Community 32 - "test_pages.py"
Cohesion: 0.08
Nodes (38): document_page(), base64, page_images(), Base64 page images, in page order. Empty when this document cannot be rendered.…, page_count(), PageUnavailable, _pdfium(), Any (+30 more)

### Community 33 - "extract_values"
Cohesion: 0.18
Nodes (18): extract_values(), Every value the source prints for these keys, kept only when its passage prints…, _long_text(), Exception, Generated, Returns the replies the test wrote, in order, then an empty list of values. A…, A truncated or non-JSON reply is an outage: the section was never actually…, Unlike a garbled reply, valid JSON with the wrong shape means the model… (+10 more)

### Community 34 - "sets_io.py"
Cohesion: 0.09
Nodes (35): choose(), Generated, generic(), main(), _named(), phrase(), on_file(), pool() (+27 more)

### Community 35 - "TelegramAdapter"
Cohesion: 0.14
Nodes (17): _attachment(), _pixels(), Any, Client, datetime, Response, Confirm the token works before anything else is attempted., One `getUpdates` round. Returns what was captured; replies with what was… (+9 more)

### Community 36 - "test_eval_harness.py"
Cohesion: 0.18
Nodes (22): Expected, load_set(), MalformedQuestion, Any, SetId, ValueError, Question, A line the harness cannot grade. The message names the file and the line. (+14 more)

### Community 37 - "Any"
Cohesion: 0.14
Nodes (17): Measurement, by_subject(), db(), FakeCursor, load_register(), Any, date, fixture (+9 more)

### Community 38 - "reminder/__init__.py"
Cohesion: 0.11
Nodes (24): already_said(), close(), current_lead(), next_window(), Overdue, Any, date, datetime (+16 more)

### Community 39 - "test_api.py"
Cohesion: 0.07
Nodes (48): Answer, Cited, One sentence and the passages it was traced to. What rule 3 looks like as data.…, Answered. Asking for consent and naming what is missing are endings, not…, Asks, Protocol, The one method of `AnswerGraph` the harness uses. A test supplies a fake., advising() (+40 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.19
Nodes (21): cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), Any, date (+13 more)

### Community 41 - "retrieve.py"
Cohesion: 0.14
Nodes (22): Connection, Just enough of `psycopg.Connection` to register a document and to be faked in a…, ndarray, numpy, sqlite3, load_matrix(), pack(), SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.… (+14 more)

### Community 42 - "sse"
Cohesion: 0.10
Nodes (35): Citation, A passage, named the way a person cites it and identified the way a link needs.…, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed…, Reading, a_citation(), advice_card(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order. (+27 more)

### Community 43 - "api.ts"
Cohesion: 0.07
Nodes (31): dynamic, metadata, runtime, OwnerForm(), RELATION_CHOICES, Roster(), Place, PLACES (+23 more)

### Community 44 - "._client"
Cohesion: 0.12
Nodes (11): Any, Client, A question, embedded the way the model was trained to embed a search query., Passages as `(title, text)`, embedded the way the model was trained to embed a…, Load the generator and the embedder now, and say where the generator landed. An…, Generate against a JSON schema. This is how extraction is held to a pack's…, The same constrained generation, yielded as it is written. Identical body to…, Whether this embedding model expects `QUERY_PROMPT` and `DOCUMENT_PROMPT`. (+3 more)

### Community 45 - "test_answer_graph.py"
Cohesion: 0.06
Nodes (46): _either(), _pack_for(), "a dental plan", or "a term life plan or a whole life plan". "An" only before…, The pack that speaks for the best-scoring passage's document type, or None for…, build(), events(), passage(), Any (+38 more)

### Community 46 - "test_gate.py"
Cohesion: 0.07
Nodes (61): passages_for(), Inputs as kind fact/rule passages (chunk_id from the ref), and the figures as…, check(), check_advice(), check_content(), check_one(), Claim, _normal() (+53 more)

### Community 47 - "_pages_from"
Cohesion: 0.14
Nodes (17): Block, DoclingParser, _kind(), _pages_from(), Docling, held at arm's length: imported on first use, and never at module…, Group Docling's items by the page they were found on. Docling's markdown export…, Docling's label, reduced to the one distinction chunking needs: is this a…, A table as lines of text, one row per line: `label: value` when a row has two… (+9 more)

### Community 48 - "build_router"
Cohesion: 0.08
Nodes (38): CorrectionResponse, ForgottenDocument, HouseholdResponse, ObligationChanged, PendingName, What changed, in the words the screen confirms it with. `was` is returned…, The row is gone from Today. `speaks_again` is null when it will not come back.…, 202. The vision pass is slower than a page load, so it is queued and this is… (+30 more)

### Community 49 - "HouseholdScope"
Cohesion: 0.14
Nodes (20): HouseholdScope, Any, Keep the owner's passages and the household's; set aside everybody else's. A…, Keep the passages of these people and of the household; set aside everybody…, What `AnswerGraph` is handed so it can scope without holding a connection.…, scope_passages(), scope_to(), _conn_returning() (+12 more)

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 51 - "FakeConn"
Cohesion: 0.07
Nodes (49): document_row(), fact_row(), FakeConn, next_kind(), obligation(), open_obligation(), overdue_row(), date (+41 more)

### Community 52 - "State"
Cohesion: 0.15
Nodes (11): _asked(), _conversation(), fuse(), What the graph carries. It ends at the evidence; the answer is streamed, not…, The question to answer and to scope. A follow-up is the whole question it was…, Several searches as one list: each passage once, at the best score any phrasing…, The question made whole, and said in the documents' words. See…, Every phrasing of the question, searched and fused. The person's own words… (+3 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.17
Nodes (26): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError, Read and validate a pack's grounding corpus from its own folder on disk. A…, A pack's grounding corpus on disk does not match what its `sources.yaml`… (+18 more)

### Community 54 - "packs.py"
Cohesion: 0.15
Nodes (16): DocumentTypeSpec, One kind of document the core recognises., Classification, _prompt(), Decide which of the core catalogue's document types a captured document is, or…, _schema(), Catalog, document_types() (+8 more)

### Community 55 - "cli.py"
Cohesion: 0.21
Nodes (20): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+12 more)

### Community 56 - "worker.py"
Cohesion: 0.18
Nodes (17): lifespan(), install_best_effort(), Install at startup without being able to stop startup. Both processes that own…, application(), The configured application with its tasks registered. One per process., _beat_needs_its_own_process(), celery_argv(), main() (+9 more)

### Community 57 - "ADR index (0001-0018, with status)"
Cohesion: 0.09
Nodes (32): ADR 0006 - pypdfium2 renders the quarantine page images, ADR 0009 - next-themes and lucide-react are the only two web dependencies beyond the stack, Schedule-table questions remain weak (rank 2-4), ADR 0013: A question is understood before it is searched, and scoped before it is cut, The answer prompt carries today's date and names the scoped relation as who the question is about, AskRequest.history carries up to twelve earlier turns, A relevance-grading call and an 'answerable' schema flag were both dropped, Remaining failures are retrieval's to fix (cross-encoder plus lexical) (+24 more)

### Community 58 - "build.py"
Cohesion: 0.09
Nodes (28): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering…, Why the catalogue cannot supply `field` from every one of `doc_types`, or None., Whether any document type in the catalogue declares `field`., An advice shape that names a missing role or key fails at load time. Caught…, Every core document type, field and category this pack names exists, or…, A compared field no document type of the shape declares can never be printed.…, model_validator (+20 more)

### Community 59 - "Any"
Cohesion: 0.10
Nodes (24): advised_pack(), db(), _document(), _facts_tuple(), FakeConn, FakeCursor, Any, date (+16 more)

### Community 60 - "source-chip.tsx"
Cohesion: 0.15
Nodes (13): SourceChip(), SourcePanel(), stripTrailingPage(), ADR-0016, DocumentDetail(), when(), Field(), format() (+5 more)

### Community 61 - "values.py"
Cohesion: 0.08
Nodes (31): _check(), collapse(), _cuts_a_number(), _groups(), _is_heading(), number_tokens(), _pack(), printed_as() (+23 more)

### Community 62 - "ConfigurationError"
Cohesion: 0.09
Nodes (29): _chat_ids(), ConfigurationError, _flag(), _folder(), local_url(), _port(), _positive(), Path (+21 more)

### Community 63 - "lock.ts"
Cohesion: 0.07
Nodes (47): ref_node_crypto, ref_node_fs, dynamic, GET(), grant(), POST(), runtime, ALLOWED (+39 more)

### Community 64 - "dependencies"
Cohesion: 0.18
Nodes (11): dependencies, ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes (+3 more)

### Community 65 - "routes.py"
Cohesion: 0.08
Nodes (56): AbstentionEvent, AdviceCardEvent, AdviceFigure, AdviceWithheldEvent, AskRequest, AskResponse, CloseRequest, ConfirmNameRequest (+48 more)

### Community 66 - "PARROT Interface Design Pack"
Cohesion: 0.09
Nodes (29): Not finding you is an answer (first-person abstention), Capture is where the user already is, Citation chips are the trust surface, Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Nothing moves without a reason (motion specification), Silence beats a guess (+21 more)

### Community 67 - "export-design-preview.cjs"
Cohesion: 0.11
Nodes (17): bundle(), classes, css, cssFile, domId, fs, ids, licences (+9 more)

### Community 68 - "The Four Surfaces"
Cohesion: 0.13
Nodes (16): Packs and Modules May Not Import web/ or api/, The FastAPI Application, The API Surface, GET /api/today Never Marks Anything Notified, apply, Auto-Redirect to Today Once Ready, check, draw (+8 more)

### Community 69 - "pack"
Cohesion: 0.09
Nodes (42): Categories, holdings(), Any, Rows of `INVENTORY`, one holding per document that prints the field an enabled…, Asked, categories_asked(), categorise(), glossary() (+34 more)

### Community 70 - "advice-consent.tsx"
Cohesion: 0.16
Nodes (18): AdviceNote(), Consent, ConsentPrompt(), agree(), settle(), State, ADR-0016, AdviceConsentSection() (+10 more)

### Community 71 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node (+3 more)

### Community 72 - "base.py"
Cohesion: 0.08
Nodes (27): CaptureAdapter, IngestJob, datetime, Protocol, The one interface every capture channel satisfies. receive(payload, mime,…, Magic bytes first, filename suffix second, `application/octet-stream` last. A…, What a capture returns: a registered document, and whether we had seen it…, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call. (+19 more)

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
Nodes (34): Channel, current(), grant(), HouseholdConsents, _latest(), NoOwner, Any, RuntimeError (+26 more)

### Community 77 - "test_modules.py"
Cohesion: 0.15
Nodes (28): AlertConfig, Every declared threshold that is crossed, has evidence, and has not just been…, sweep(), Everything inside a lead window that has not already been said for that window.…, sweep(), FakeConn, obligation_row(), datetime (+20 more)

### Community 78 - "today/page.tsx"
Cohesion: 0.09
Nodes (24): HouseholdPage(), AppLayout(), dynamic, isUrgent(), metadata, runtime, summary(), TodayPage() (+16 more)

### Community 79 - "test_the_code_scored_metrics_come_out_as_arithmetic_says"
Cohesion: 0.17
Nodes (10): The last question's contexts and candidate count, then a clean slate., Each question on its own thread, so no answer is a follow-up to the one before., Recorder, trace_all(), FakeGraph, FakeRetriever, KeepAll, _passage() (+2 more)

### Community 80 - "preview.tsx"
Cohesion: 0.10
Nodes (17): metadata, answers, DesignPreview(), Direction, directions, Item, items, web_app_design_preview_preview_module (+9 more)

### Community 81 - "reference_for"
Cohesion: 0.20
Nodes (11): _as_date(), _as_number(), date, Decimal, The register's text against an extracted value, each normalised the way the…, The reference answer Ragas judges recall and precision against. A fact…, The ways a register value is printed. `2027-04-11` appears on a schedule as "11…, reference_for() (+3 more)

### Community 82 - "Two-stage quarantine with a vision-language second pass"
Cohesion: 0.12
Nodes (19): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Two-stage quarantine with a vision-language second pass, Batch 4: the deliberately hard documents, A full policy wording registers as policy_schedule, Task: review every quarantined document and label the failure, Task: sign off the capture-to-database path against the data inventory, Measurement is owned separately from the engine (+11 more)

### Community 83 - "Any"
Cohesion: 0.13
Nodes (7): ConsentCursor, Fails, FakeCursor, Any, The parameters of the one statement containing `needle`. Fails loudly if it…, Yields `before`, then raises. `ask` raises at once., Remembers what `grant` or `withdraw` inserted, so the next read of the latest…

### Community 84 - "Ollama"
Cohesion: 0.17
Nodes (10): answer(), build_context(), format_sources(), Answer a question from retrieved chunks, with citations back to the file. The…, Ollama, Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.…, Batch embeddings. Falls back to the legacy endpoint on old servers., Hit (+2 more)

### Community 85 - "F1"
Cohesion: 0.22
Nodes (6): extraction_f1(), F1, FactRow, One row of the `facts` table, as the harness reads it: which document, which…, Field extraction scored against the register, overall and by document type. The…, test_extraction_f1_scores_only_indexed_documents_against_the_register()

### Community 86 - "main"
Cohesion: 0.14
Nodes (18): approve(), pending(), PendingValue, Any, date, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it., Every value still waiting for review, oldest first, optionally for one pack. (+10 more)

### Community 87 - "ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.11
Nodes (27): Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration), Published guidance is a second evidence lane, never a second household, Every passage carries a kind: document, inventory or guidance, ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, The adult rule: advice is withheld for a person under 21 or a child with no date of birth on file, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel) (+19 more)

### Community 88 - "test_a_document_still_in_the_inbox_is_not_forgotten"
Cohesion: 0.22
Nodes (9): filed_document(), inbox(), Path, Capture would register it again within a minute, so the button would only…, A watched folder holding one document, hashed the way the ingest registered it., v1 keeps the inbox as the document store, so this is a real state, not a fault., test_a_document_still_in_the_inbox_is_not_forgotten(), test_a_document_whose_file_left_the_inbox_is_409_not_500() (+1 more)

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
Cohesion: 0.10
Nodes (28): Advice, Answering, Category, Exclusions, FieldSpec, Grounding, GroundingDocument, Guardrails (+20 more)

### Community 93 - "Passage"
Cohesion: 0.06
Nodes (27): The documents on file, narrowed to the same people the passages were., The answer graph. Router, retrieve, rerank, grounding gate, then answer or…, Holding, Passage, Protocol, How a passage names itself: the document and the page, as a person would say it., Unique across kinds: chunk ids, fact ids and guidance ids are three sequences., Implemented by `core/retrieve/` when Lane B's hybrid search lands. `candidates`… (+19 more)

### Community 94 - "InstalledPack"
Cohesion: 0.07
Nodes (32): AdviceShape, FactInput, A printed fact a calculator reads, named by where it is printed rather than…, One kind of advice question, and everything its calculator needs to answer it., AdviceLog, Adviser, ConsentBook, _kind_of() (+24 more)

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
Nodes (65): copy, PackManifest, A domain pack, authored as one YAML file: grounding, persona, answering and…, pydantic, _advised(), _checked(), _compare_without_an_ordering(), _compares_an_undeclared_field() (+57 more)

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.10
Nodes (21): The Purely Additive Migration Exception, Contracts and Migrations Are Their Own PR, Sources of Truth Generate Their Outputs, Snooze Means Not Until This Gets More Urgent, The Three Things Agents Get Wrong Here, Generated Files Committed Alongside Their Source, benefit_illustration Document Type, birth_certificate Document Type (+13 more)

### Community 100 - "generate_lim_documents.py"
Cohesion: 0.32
Nodes (7): jinja2, find_browser_executable(), generate_documents(), Path, Project Parrot - Synthetic Document Generator for Lim Household…, Find Microsoft Edge or Google Chrome executable on Windows., subprocess

### Community 101 - "_ordered"
Cohesion: 0.33
Nodes (6): _Value, Hashable, _order_key(), _ordered(), One sortable key for a number, a date or a word, so a ranking never compares…, Keys ranked by value in the stated order, ties broken by name so a ranking is…

### Community 102 - "The five-lane split (five people, nine weeks, three builders)"
Cohesion: 0.09
Nodes (30): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The domain pack manifest, The expansion model: two axes, not one list, The golden set: answerable, hard negatives, adversarial, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build (+22 more)

### Community 103 - "Data inventory: identity data, DOBs and loans"
Cohesion: 0.17
Nodes (15): Data inventory: identity data, DOBs and loans, The lock is a screen lock, not encryption, next dev binds every interface, not loopback, Telegram capture route and delete-at-source, What crosses a boundary, Governance artefact set, Write unverified rather than assert, The final ILP report (+7 more)

### Community 104 - "test_rerank.py"
Cohesion: 0.09
Nodes (28): CrossEncoderReranker, passage_text(), What the reranker reads: the one-line context, when a chunk carries one, then…, Implements `core.graph.ports.Reranker`. Reorders by the cross-encoder's score…, FakeEncoded, FakeModel, FakeTokenizer, no_weights() (+20 more)

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
Cohesion: 0.19
Nodes (15): itertools, re, Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks. Paperwork is short and…, _split_page(), discover() (+7 more)

### Community 109 - "Tax and Reliefs — contract changes this pack needs"
Cohesion: 0.40
Nodes (4): 1. A deduction multiplier on `estimate_saving`, 2. Limiting a fact input to one year, Not a contract change: parent relief, Tax and Reliefs — contract changes this pack needs

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
Cohesion: 0.31
Nodes (9): _closes(), Which kinds of cover close a short shape's gap, written by code. The pack…, Marcus held a critical illness plan on 20 September and was SGD 251,200.00…, `closed_by` is optional in the contract, and a shape without it stays as it was., _shape(), test_a_gap_closed_by_two_kinds_names_the_one_held_and_the_one_not(), test_a_gap_in_cover_already_held_asks_for_more_of_it_not_for_a_first_policy(), test_a_gap_with_nothing_on_file_says_none_is_on_file() (+1 more)

### Community 115 - "tokens/page.tsx"
Cohesion: 0.05
Nodes (34): lucide-react, react, dynamic, runtime, Motion(), ROWS, INKS, metadata (+26 more)

### Community 116 - "_answer_events"
Cohesion: 0.13
Nodes (19): _answer_events(), today(), _cite(), connection(), _link(), Any, date, Event (+11 more)

### Community 117 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 119 - "test_registration.py"
Cohesion: 0.29
Nodes (12): Insert or update the `documents` row for these bytes and say which happened.…, register_document(), conn(), database_url(), Any, fixture, The idempotent upsert, against the real unique index. `documents.sha256 UNIQUE`…, test_a_document_must_arrive_with_a_name() (+4 more)

### Community 121 - "capture.py"
Cohesion: 0.06
Nodes (30): Dispatcher, Inline, Protocol, What happens to a document between "these bytes are registered" and "this…, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Send (+22 more)

### Community 122 - "packs/page.tsx"
Cohesion: 0.06
Nodes (29): ADR-0017, next, dynamic, metadata, PacksPage(), runtime, DocumentPage(), dynamic (+21 more)

### Community 123 - "ADR 0002 - One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (7): ADR 0001 - Record architecture decisions, ADR 0002 - One PostgreSQL instance for everything, Reciprocal rank fusion of dense and lexical, ADR 0003 - PaperBrain informs the pattern, not the module, PaperBrain prototype, Contracts before code, Lane A - Integration and product

### Community 124 - "The deliberately naive retrieval baseline"
Cohesion: 0.17
Nodes (12): Task: benchmark the workstation and publish the numbers, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, The deliberately naive retrieval baseline, Committed runs are never deleted, Yew Mun's generated task list, Hybrid retrieval, not embeddings alone, Chunking respects paragraphs (+4 more)

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 127 - "create_app"
Cohesion: 0.16
Nodes (12): create_app(), checks(), ready(), setup(), system_status(), The local API. Liveness is intentionally separate from assistant readiness.…, contextlib, FastAPI (+4 more)

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

### Community 140 - "ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.33
Nodes (9): guardrails.abstain_below was calibrated on un-prompted scores, ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts, chunks.tsv built from context_prefix || text, Context prefix: title - type - heading - page, rag_probe2 before/after similarity table (six policies, 13 September), scripts/reindex.py rebuilds chunks and vectors, Chunks follow the document's structure (Docling heading labels), Task prompts: embed_query and embed_documents (+1 more)

### Community 141 - "answer.tsx"
Cohesion: 0.06
Nodes (36): ai, @ai-sdk/react, dynamic, lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns() (+28 more)

### Community 143 - "scripts"
Cohesion: 0.33
Nodes (6): scripts, build, dev, lint, start, typecheck

### Community 144 - "test_ask_stream_hands_its_events_to_answering_so_its_teardown_can_close_them"
Cohesion: 0.25
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

### Community 154 - "Cursor"
Cohesion: 0.25
Nodes (4): Cursor, Any, cursor(), cursor()

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.25
Nodes (8): parrot-sweep shimmer animation, Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, An answer with the page it came from, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "pathlib"
Cohesion: 0.06
Nodes (48): argparse, collections, enabled_pack_ids(), The packs left switched on, plus `core`, or `None` when nothing has been…, connect(), DatabaseUnavailable, Any, RuntimeError (+40 more)

### Community 157 - "main"
Cohesion: 0.07
Nodes (44): _kill_tree(), main(), open_browser(), port_answers(), Popen, Stop a child and everything under it, then make sure it has gone., Whether something is listening on loopback. Not whether it is ours., Start `npm run dev` in `web/`, or say plainly why it could not. Three reasons… (+36 more)

### Community 158 - "Adversarial testing from week 7"
Cohesion: 0.25
Nodes (8): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Adversarial testing from week 7, Prompt injection carried inside a document, Scope attack: asking it to act, Task: run adversarial Set C and write up the findings, Adversarial Set C (15 questions that should not be answered), Golden Set C - adversarial (15)

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 161 - "Every Fact Row Cites Its Source"
Cohesion: 0.33
Nodes (7): Every Fact Row Cites Its Source, A Correction Cannot Invent a Row, Every Node Writes One Line to traces, The Ingestion Pipeline, The Pipeline Forks Into Retrieval and Facts Lanes, Numbers Come From Postgres, Never From the Model, macOS Worker Runs Celery Solo

### Community 162 - "HouseholdAdviceLog"
Cohesion: 0.13
Nodes (14): Claim, One sentence and the passages it was traced to. Never emitted without…, _as_response(), ask(), ask_stream(), _graph_for(), _history(), One `Answer` to one of the shapes a client has to handle. (+6 more)

### Community 165 - "PARROT evaluation harness"
Cohesion: 0.38
Nodes (7): abstention_rate, PARROT evaluation harness, Set A, answerable, Set B, hard negatives, Set C, adversarial, The golden question sets, must_cite_page from field_pages

### Community 166 - "RagasJudge"
Cohesion: 0.32
Nodes (6): RagasJudge, aembed_text(), aembed_texts(), embed_text(), embed_texts(), Ragas 0.4 metrics through Ollama's OpenAI-compatible endpoint. Imported lazily…

### Community 167 - "The autonomy statement"
Cohesion: 0.29
Nodes (7): The autonomy statement, Governance claims traced to enforcement points, IMDA mappings and autonomy statement artefact, The facts table as an extension point, Constraint: fully offline, Explicitly not doing: cloud, hosted vectors, autonomous spending, Roadmap phase 2 - facts

### Community 169 - "test_the_inventory_always_reads_core_documents"
Cohesion: 0.22
Nodes (6): _Answering, The event stream one request is sending, held where the request's cleanup can…, Close the answer stream when the request ends, whatever ended it. Requires…, Conn, ADR 0017: a document is the core's, so the query includes `core` whatever is…, test_the_inventory_always_reads_core_documents()

### Community 170 - "Calculation"
Cohesion: 0.22
Nodes (9): Calculation, What a calculator returns when every fact and rule it needed was on file and…, Adviser, _dual_cited_calculation(), _meets_calculation(), An input that happens to print the same value as a figure, so the role check…, A `meets` outcome: the gap figure is negative, and only its printed text…, An input, `fact:12`, that independently prints the same value as the `target`… (+1 more)

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
Cohesion: 0.29
Nodes (7): AdviceConsent, AdviceConsent, One advising pack, the wording a person is asked to agree to, and what the…, _as_consent(), advice_consents(), record_consent(), One advising pack's consent wording and the owner's standing answer to it.

### Community 179 - "The synthetic-to-real gap"
Cohesion: 0.40
Nodes (5): The 40-document redacted holdout, The synthetic-to-real gap, Consent and redaction protocol, Task: write the PDPA position on using synthetic data, Task: evaluation run 3 plus the holdout run

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 183 - "quiet_engine"
Cohesion: 0.50
Nodes (4): fixture, MonkeyPatch, quiet_engine(), No real probes, no startup writes, no deliberate pause before exiting. The…

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
- **362 isolated node(s):** `session-start.sh script`, `PATH`, `npx`, `@modelcontextprotocol/server-filesystem`, `_Formatter` (+357 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1621 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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