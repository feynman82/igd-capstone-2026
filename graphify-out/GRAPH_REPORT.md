# Graph Report - .  (2026-09-20)

## Corpus Check
- 324 files · ~682,544 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4147 nodes · 10705 edges · 211 communities (187 shown, 24 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 1601 edges (avg confidence: 0.58)
- Token cost: 1,061,503 input · 0 output

## Community Hubs (Navigation)
- The Answer Graph
- Evaluation Harness
- Advice Graph Tests
- Answer Graph Tests
- Register Validation
- Advice Calculators
- Insurance Pack And Grounding
- Advice Module Tests
- Eval Harness Tests
- Ingestion Pipeline Tests
- Grounding Index Tests
- Celery Worker Queue
- Watched Folder Capture
- Telegram Capture Tests
- Worker Tasks And Reindex
- Parrot Launcher
- Runtime Benchmark
- Vault And Corrections
- Design Canvas Runtime
- Readiness Checks
- Schema-Constrained Extraction
- Grounding Value Tests
- API Consent Tests
- Pack And Module Registry
- Answer Streaming And Claims
- Sentence Scanner
- Household People And Aliases
- Ingest Pipeline
- Lifecycle Tests
- Eval Scoring
- Household Scope Tests
- Runtime Settings Tests
- Page Rendering Tests
- Hybrid Retrieval Tests
- Golden Set Generator
- Telegram Adapter
- Capture Dispatch
- Module Loading Tests
- Reminder Module
- API Streaming Tests
- Alert Module
- Paperbrain Retrieval
- API Answer Streaming
- Web API And Consent
- Ollama Client
- Grounding Value Extraction
- Grounding Gate Tests
- Docling Parsing
- API Models
- Household Scoping Tests
- Web TypeScript Config
- Today Surface Tests
- Contract Tests
- Grounding Corpus
- Evaluation Runner
- Paperbrain CLI
- Two-Stage Quarantine
- Chunking And Retrieval ADRs
- Chunking And Classification
- Advice Fact Reading Tests
- Ask Surface Components
- Grounding Value Parsing
- Settings And Configuration
- App Lock
- Web Runtime Dependencies
- API Event Serialisation
- Interface Design Pack
- Startup Tests
- Startup Screen
- Question Vocabulary
- Pack Knowledge ADR
- Web Lint Tooling
- Grounding Value Bands
- Retrieval And Answer Path
- Name Scoping
- Household Identity ADRs
- Advice Query Tests
- Module Sweep Tests
- Today Surface
- Design Tokens
- Design Preview
- API Routes
- Paperbrain Architecture
- Field Correction Tests
- Paperbrain Ollama
- Empty And Error States
- Grounding Value Review
- Advice And Pack Role ADRs
- Design Canvas Walker
- Web Component Config
- Today Rows And Citations
- Advice Consent
- Core Contracts
- Grounding Gate
- Module Adviser
- Household Canon
- Running Parrot
- Lane C Governance
- Advice Contract Tests
- Core Document Catalogue
- API Request Models
- Pack Manifest Tests
- Team Split Narrative
- Data Inventory
- Scan And OCR Tests
- User Stories
- Lane D Packs And Interface
- Lane E Corpus
- Paperbrain Ingest
- Inventory Tests
- Core Documents
- Artefacts Architecture Review
- Packs Readme
- Paperbrain Extract
- Household Who Is This
- Components System Screens
- Api Routes
- Ingest Classify
- Scripts Worker
- Tests Test Registration
- Core Registry
- Runtime Capture
- Packs Page
- Docs Notion
- Yew Mun Readme
- Ingest Obligations
- Tests Test Advice Core
- Tests Test Insurance Pack
- Governance Synthetic Data Case
- Docs Pack Authoring
- Tests Test Api
- Components Nav
- Ask Advice Card
- Adapters Readme
- Agents
- Docs Graphify
- Insurance Notebook Prompts Full
- Docs Household And Identity
- Eval Score
- Christian Readme
- Tests Test Advice Core
- Chat Route
- Vault Field
- Web Package
- Readme
- Worker Schedule
- Docs Synthetic Generation Guide
- Eval Readme
- Tests Test Api
- Tests Test Worker Queue
- App Layout
- Grounding Index
- Migrations 0001
- Docs Running
- Startup And Power Main
- Uploads Parrot Design Evaluation
- Scripts Build Team Tasks
- Scripts Start Parrot
- Desmond Readme
- Tests Test Api
- [ Path] Route
- Ingest Readme
- Api Models
- Adapters Base
- Graph Gate
- Eval Readme
- Eval Score
- Siew Readme
- Tests Test Api
- System Route
- Components Wordmark
- Agents
- Tests Test Household
- Packs Readme
- Notebooks Generate Lim Documents
- Scripts Load Corpus
- Api Models
- Migrations 0002 Household
- Migrations 0003 Advice
- Desmond Readme
- Api Routes
- Graph Answer
- Parrot Uiux Refinement Support
- Tests Test Contracts
- Graph Inventory
- Tests Test Rerank
- Web Eslint Config
- Agents
- Api
- Api Models
- Grounding
- Core
- Runtime
- Worker
- Corpus
- Eval
- Modules
- Packs
- Desmond Readme
- Desmond Readme
- Tests Test Contracts
- Tests Test Modules
- Scripts Setup
- Web Next Config
- Web Postcss Config
- Docs Team
- Pyproject
- Christian Readme
- Desmond Readme

## God Nodes (most connected - your core abstractions)
1. `InstalledPack` - 139 edges
2. `Passage` - 125 edges
3. `ScriptedOllama` - 112 edges
4. `Settings` - 102 edges
5. `Ollama` - 95 edges
6. `FakeConn` - 94 edges
7. `AnswerGraph` - 89 edges
8. `ModelUnavailable` - 86 edges
9. `Sentence` - 75 edges
10. `Answer` - 75 edges

## Surprising Connections (you probably didn't know these)
- `The Corpus Is Synthetic and Committed` --semantically_similar_to--> `Corpus Batches Are Not in Git`  [AMBIGUOUS] [semantically similar]
  NOTICE.md → FIRST-RUN.md
- `Domain Packs` --conceptually_related_to--> `Core Document Catalogue (ADR 0017)`  [AMBIGUOUS]
  README.md → core/documents.yaml
- `One cell, one field` --semantically_similar_to--> `A field name is three things at once`  [INFERRED] [semantically similar]
  corpus/templates/policy_schedule.html → docs/PACK_AUTHORING.md
- `next dev binds every interface, not loopback` --semantically_similar_to--> `Ports published on 127.0.0.1 only`  [INFERRED] [semantically similar]
  docs/governance/data-inventory.md → infra/docker-compose.yml
- `Explicitly not doing: cloud, hosted vectors, autonomous spending` --semantically_similar_to--> `The autonomy statement`  [INFERRED] [semantically similar]
  tools/paperbrain/docs/ROADMAP.md → team/siew/README.md

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

## Communities (211 total, 24 thin omitted)

### Community 0 - "The Answer Graph"
Cohesion: 0.05
Nodes (91): The record of every advised or withheld answer (ADR 0016).  `advice_records` k, AdviceShape, One kind of advice question, and everything its calculator needs to answer it., AdviceLog, AdviceRecord, Adviser, Calculation, ConsentBook (+83 more)

### Community 1 - "Evaluation Harness"
Cohesion: 0.05
Nodes (70): HouseholdConsents, `core.graph.advice.ConsentBook` over a live connection, for the graph to ask wit, HouseholdAdviceLog, `core.graph.advice.AdviceLog` over a live connection.      `basis` is dumped w, DenseRetriever, NoReranker, A dense-only retriever, so the graph can be run and tested before Lane B's hybri, Keeps the top `keep` in the order retrieval gave them. Lane B replaces this with (+62 more)

### Community 2 - "Advice Graph Tests"
Cohesion: 0.05
Nodes (75): _closes(), Which kinds of cover close a short shape's gap, written by code.      The pack, advised_pack(), build(), date, The advise branch: code calculates under consent, the model explains, and the an, Fix 1: a consumer that stops reading after the card and one sentence — a `Genera, C5 fix round 2. Before this fix, `yield AdviceCard(...)` sat *before* the explan (+67 more)

### Community 3 - "Answer Graph Tests"
Cohesion: 0.09
Nodes (69): AnswerGraph, _either(), Finished, The documents on file, narrowed to the same people the passages were., "None of the 5 policies on file is a dental plan." Written by code, never by the, Evidence gathered, floor cleared, the model is now writing. Nothing is claimed y, One sentence that has passed the gate, with the citations it passed on.      I, Everything that is only knowable once the last sentence is in.      `quarantin (+61 more)

### Community 4 - "Register Validation"
Cohesion: 0.05
Nodes (67): DocumentCatalog, The core's documents: every type, its fields, the registers and core answering (, (document_type, field_name) -> FieldSpec. Used by the extractor and the scorer., Why the catalogue cannot supply `field` from every one of `doc_types`, or None., Whether any document type in the catalogue declares `field`., Every core document type, field and category this pack names exists, or ValueErr, A compared field no document type of the shape declares can never be printed., _as_date() (+59 more)

### Community 5 - "Advice Calculators"
Cohesion: 0.09
Nodes (63): Advice, FactInput, A printed fact a calculator reads, named by where it is printed rather than what, What a pack that advises must say, once and in its own words, before it may., RuleInput, Figure, One number a calculator produced, and the words a sentence must use to state it., _amount() (+55 more)

### Community 6 - "Insurance Pack And Grounding"
Cohesion: 0.05
Nodes (65): CareShield Life (CPF Board), CareShield Life monthly payouts on severe disability and the ADL claim criteria, Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, MediShield Life (CPF Board), Critical illness protection gap (74%, S$579 billion, PGS 2022), LIA Media Release: Protection Gap Study 2022 (+57 more)

### Community 7 - "Advice Module Tests"
Cohesion: 0.13
Nodes (58): Missing, What a calculator returns when a fact or a rule value it needed was not there to, FactRow, One person's advice. The graph asks whose first when a question names several pe, assert_nothing_negative(), basis(), fact(), _facts_tuple() (+50 more)

### Community 8 - "Eval Harness Tests"
Cohesion: 0.07
Nodes (46): Answer, Cited, One sentence and the passages it was traced to. What rule 3 looks like as data., Answered. Asking for consent and naming what is missing are endings, not answers, Judge, Protocol, Ragas with a local model, or a fake. One call per (metric, question)., Expected (+38 more)

### Community 9 - "Ingestion Pipeline Tests"
Cohesion: 0.08
Nodes (52): extract(), find_page(), _normalise(), The first page whose text contains this value. None means no page supports it., Never raises. A failure is a reason, and a reason routes the document to quarant, FakeOllama, insurance(), iras() (+44 more)

### Community 10 - "Grounding Index Tests"
Cohesion: 0.09
Nodes (30): CaptureFixture, _Connected, _extracted(), FakeConn, FakeCursor, _installed(), Any, FakeConn (+22 more)

### Community 11 - "Celery Worker Queue"
Cohesion: 0.09
Nodes (40): The one interface every capture channel satisfies.      receive(payload, mime, s, The idempotency key for the whole platform. Bytes, not hex: `documents.sha256` i, sha256(), Any, Queued, Hand the document to the worker and go back to watching the folder., A `Queued` bound to this configuration's broker.      Celery is imported here ra, Intake (+32 more)

### Community 12 - "Watched Folder Capture"
Cohesion: 0.10
Nodes (36): Magic bytes first, filename suffix second, `application/octet-stream` last., sniff_mime(), FolderAdapter, FolderSettings, _Pending, datetime, Path, The watched-folder capture adapter.  A person drops a scan into a folder and i (+28 more)

### Community 13 - "Telegram Capture Tests"
Cohesion: 0.10
Nodes (39): RuntimeError, Safe to show: never contains the token., TelegramSettings, TelegramUnavailable, MockTransport, build(), FakeRegistrar, FakeTelegram (+31 more)

### Community 14 - "Worker Tasks And Reindex"
Cohesion: 0.10
Nodes (42): The reportable line. Deliberately a rate and a count, because a rate over three, recovery_rate(), bytes_for(), digest_of_document(), Any, The payload for `digest`, found by hashing what is in the watched folder., connect(), Any (+34 more)

### Community 15 - "Parrot Launcher"
Cohesion: 0.07
Nodes (34): broker_available(), dispatcher_for(), FolderCapture, Run the capture loops in background threads, beside the local server.  This is, Begin watching. Returns False, with a logged reason, when it cannot., A daemon thread that long-polls the Telegram bot until `stop()` or process exit., Begin polling. Returns False, with a logged reason, when it cannot or should not, Whether Redis answers. Not whether a worker is listening — `core/runtime/checks. (+26 more)

### Community 16 - "Runtime Benchmark"
Cohesion: 0.08
Nodes (34): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+26 more)

### Community 17 - "Vault And Corrections"
Cohesion: 0.07
Nodes (38): _columns(), correct(), Corrected, CorrectionRejected, Any, date, Decimal, LookupError (+30 more)

### Community 18 - "Design Canvas Runtime"
Cohesion: 0.08
Nodes (29): boot(), cdnScriptFor(), compileTemplate(), contentKey(), createExternalModules(), createHelmetManager(), createRegistry(), createRuntime() (+21 more)

### Community 19 - "Readiness Checks"
Cohesion: 0.10
Nodes (33): The local API. Liveness is intentionally separate from assistant readiness.  Loo, AsyncClient, device_name(), load(), Any, The tokenizer, the model and the device it sits on, loaded once per process., One relevance logit per text, higher is better. Batched so forty passages is a h, score_pairs() (+25 more)

### Community 20 - "Schema-Constrained Extraction"
Cohesion: 0.09
Nodes (35): DocumentTypeSpec, FieldSpec, One kind of document the core recognises., One extractable field. Its `name` is the column header in Desmond's register and, _coerce(), _date_renderings(), decode_schema(), _drop_format() (+27 more)

### Community 21 - "Grounding Value Tests"
Cohesion: 0.14
Nodes (38): number_tokens(), parse_value(), Decimal, Every whole number the passage prints, thousands separators removed., The number a reported value states for its unit, or `None` when it states someth, LogCaptureFixture, _dropped(), _log_values() (+30 more)

### Community 22 - "API Consent Tests"
Cohesion: 0.11
Nodes (37): client_for(), consent(), ConsentConn, filed_document(), inbox(), Path, The parameters of the one statement containing `needle`. Fails loudly if it neve, A client whose database is `conn`.      `base_url` is loopback because `Truste (+29 more)

### Community 23 - "Pack And Module Registry"
Cohesion: 0.10
Nodes (33): ModuleManifest, A capability module. Reads typed rows, writes its own namespace, renders somewhe, installed_modules(), InstalledModule, manifest(), ModuleUnavailable, RuntimeError, Load the installed capability modules at runtime.  The mirror of `core/packs.py` (+25 more)

### Community 24 - "Answer Streaming And Claims"
Cohesion: 0.06
Nodes (29): Claim, answer_system(), _asked(), _citations(), _conversation(), _max_sentences(), _numbered(), _pack_for() (+21 more)

### Community 25 - "Sentence Scanner"
Cohesion: 0.10
Nodes (28): Any, Pulling finished sentences out of a JSON reply that is still being written.  The, What document would have answered this, if the model said. Read once, at the end, Feed it deltas; it returns whichever sentences became complete because of them., Everything received so far. Used once, at the end, to read `missing`., Append `delta` and return the sentences it completed. Usually none, sometimes on, Find `"sentences": [` once. Everything before it is of no interest.          Sea, SentenceScanner (+20 more)

### Community 26 - "Household People And Aliases"
Cohesion: 0.10
Nodes (36): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+28 more)

### Community 27 - "Ingest Pipeline"
Cohesion: 0.09
Nodes (30): Chunk, parse(), The one call the pipeline makes. An unhandled mime type quarantines rather than, commit_both_lanes(), document_title(), Outcome, process(), Any (+22 more)

### Community 28 - "Lifecycle Tests"
Cohesion: 0.12
Nodes (28): Lifecycle, Restart and shut down: asked for by the screens, carried out by the supervisor., What the person asked for, once. The first request wins; later ones change nothi, _client(), _eventually(), _launcher(), MonkeyPatch, Path (+20 more)

### Community 29 - "Eval Scoring"
Cohesion: 0.10
Nodes (34): _as_number(), cites(), _contains(), doc_stem(), grade(), held_back(), judge_all(), judge_sync() (+26 more)

### Community 30 - "Household Scope Tests"
Cohesion: 0.09
Nodes (36): _household_scope(), MonkeyPatch, Person, `HouseholdScope` over a roster held in memory, with every document resolved by n, The roster has no grandparent relation, so the household says it the only way it, 13 September: "what is Marcus's premium?" has no "my", so nothing was scoped and, A model proposal is a question on Today, not a member yet — the same rule relati, Nothing named, nothing ruled out: the question is the owner's, same as `apply` w (+28 more)

### Community 31 - "Runtime Settings Tests"
Cohesion: 0.14
Nodes (31): create_app(), ModelWarmth, Ollama, Whether the generator has been loaded yet, and where it landed. Written by one t, Load the generator and the embedder before the first question, and record the ou, warm_models(), _ollama_answering(), Any (+23 more)

### Community 32 - "Page Rendering Tests"
Cohesion: 0.10
Nodes (33): page_images(), Base64 page images, in page order. Empty when this document cannot be rendered., page_count(), PageUnavailable, _pdfium(), Any, LookupError, One page of one document, as an image.  Two callers want the same thing for oppo (+25 more)

### Community 33 - "Hybrid Retrieval Tests"
Cohesion: 0.10
Nodes (22): hybrid_score(), identifiers(), prints(), Hybrid retrieval: pgvector cosine search and Postgres full-text search, fused by, The tokens in a question that look like something printed rather than said: a po, Whether the chunk prints the identifier, ignoring case and the spacing inside it, The cosine similarity, lifted to `IDENTIFIER_HIT` when the chunk prints an ident, Lane B: hybrid retrieval. `HybridRetriever` implements `core.graph.ports.Retriev (+14 more)

### Community 34 - "Golden Set Generator"
Cohesion: 0.11
Nodes (31): choose(), Generated, generic(), main(), _named(), on_file(), pool(), Path (+23 more)

### Community 35 - "Telegram Adapter"
Cohesion: 0.12
Nodes (21): BaseTransport, IngestJob, What a capture returns: a registered document, and whether we had seen it before, _attachment(), _pixels(), Any, Client, datetime (+13 more)

### Community 36 - "Capture Dispatch"
Cohesion: 0.09
Nodes (17): Dispatcher, Inline, Protocol, What happens to a document between "these bytes are registered" and "this docume, Given a registered document, arrange for it to be read. Says what it arranged., Put one ingestion message on the queue and return its task id., Run the pipeline here and now, and report what it decided., Send (+9 more)

### Community 37 - "Module Loading Tests"
Cohesion: 0.14
Nodes (22): Measurement, by_subject(), db(), FakeCursor, load_register(), Any, date, Reminder and Alert: what fires, once, and with what behind it.  Both modules a (+14 more)

### Community 38 - "Reminder Module"
Cohesion: 0.09
Nodes (27): already_said(), close(), current_lead(), Due, next_window(), Overdue, Any, date (+19 more)

### Community 39 - "API Streaming Tests"
Cohesion: 0.10
Nodes (31): advising(), client(), graph(), pack_row(), _padded(), MonkeyPatch, TestClient, The five endpoints, against a fake database and the real queries.  The connect (+23 more)

### Community 40 - "Alert Module"
Cohesion: 0.15
Nodes (26): AlertConfig, Alert, cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject() (+18 more)

### Community 41 - "Paperbrain Retrieval"
Cohesion: 0.11
Nodes (24): Connection, Cursor, Any, Protocol, Just enough of `psycopg.Connection` to register a document and to be faked in a, ndarray, load_matrix(), pack() (+16 more)

### Community 42 - "API Answer Streaming"
Cohesion: 0.12
Nodes (31): a_citation(), Parse an `text/event-stream` body into the payloads it carried., Yields whatever events the test scripted, in order., The promise the whole design rests on: a sentence and its chips arrive together,, No `reading` before it: the floor is checked before the model is asked anything., By then the 200 has been sent. An exception that only logged would leave a scree, A line about a document on file is not the answer to "does it cover floods?"., Advice changed how a stream ends, not what an explain answer sends. Nothing on t (+23 more)

### Community 43 - "Web API And Consent"
Cohesion: 0.08
Nodes (28): Consent, ConsentPrompt(), State, ADR-0016, AdviceConsentSection(), Load, STATUS, ADR-0016 (+20 more)

### Community 44 - "Ollama Client"
Cohesion: 0.08
Nodes (18): The page a person sees while Parrot starts, served by the engine itself.  **Why, The whole page. `screens_url` is escaped into a data attribute, never into scrip, render(), IndexReport, Index a pack's published sources, and stage the values they print for a person t, What one call to `index_pack` did, so a script can say it in a line per pack., Any, Client (+10 more)

### Community 45 - "Grounding Value Extraction"
Cohesion: 0.13
Nodes (28): A rule or table value a pack's sources publish.      Extracted automatically,, ValueKey, SourceText, _check(), extract_values(), ExtractedValue, _prompt(), Any (+20 more)

### Community 46 - "Grounding Gate Tests"
Cohesion: 0.14
Nodes (28): check_advice(), Claim, Why an advice explanation cannot be kept, or `None`. Asked of a claim built over, test_a_claim_citing_the_same_document_twice_says_it_once(), test_a_grounded_claim_renders_its_document_and_page(), What the gate checks beyond "is there a citation".  A cited sentence can still, `target` and `gap` both print SGD 500,000.00 (`_gap` with `held` at zero). Namin, The defect this fixes: naming `gap`, the *second* figure in `figures` order to p (+20 more)

### Community 47 - "Docling Parsing"
Cohesion: 0.10
Nodes (21): Block, DoclingParser, _kind(), _pages_from(), Parser, PlainTextParser, Protocol, Turn captured bytes into pages of text, or say why it could not be done.  Every (+13 more)

### Community 48 - "API Models"
Cohesion: 0.14
Nodes (28): CloseRequest, CorrectionResponse, EnabledRequest, ForgottenDocument, HouseholdResponse, ObligationChanged, PacksResponse, PendingName (+20 more)

### Community 49 - "Household Scoping Tests"
Cohesion: 0.13
Nodes (28): Keep the owner's passages and the household's; set aside everybody else's., scope_passages(), conn(), _conn_returning(), _passage(), Any, Who is asking, and whose documents may answer.  Two halves, deliberately split, The third bucket. Home contents, a utility bill — nobody's name on it, everybody (+20 more)

### Community 50 - "Web TypeScript Config"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 51 - "Today Surface Tests"
Cohesion: 0.10
Nodes (19): document_row(), fact_row(), overdue_row(), Any, date, ADR 0017: disabling insurance_agent switches off its voice, never a household's, One row of `reminder.OVERDUE`, in its column order., Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with ev (+11 more)

### Community 52 - "Contract Tests"
Cohesion: 0.15
Nodes (27): _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact(), _field_not_on_every_doc_type(), _held_per_month() (+19 more)

### Community 53 - "Grounding Corpus"
Cohesion: 0.17
Nodes (25): GroundingCorpus, GroundingDocument, One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records, corpus_dir(), CorpusInvalid, load_corpus(), Path, RuntimeError (+17 more)

### Community 54 - "Evaluation Runner"
Cohesion: 0.14
Nodes (26): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), main(), _note() (+18 more)

### Community 55 - "Paperbrain CLI"
Cohesion: 0.18
Nodes (20): ArgumentParser, build_parser(), _client(), cmd_add(), cmd_ask(), cmd_docs(), cmd_doctor(), cmd_ingest() (+12 more)

### Community 56 - "Two-Stage Quarantine"
Cohesion: 0.14
Nodes (24): ParsedDocument, blocked_reasons(), forget(), Any, Ollama, Path, ValueError, QuarantinedDocument (+16 more)

### Community 57 - "Chunking And Retrieval ADRs"
Cohesion: 0.11
Nodes (26): guardrails.abstain_below was calibrated on un-prompted scores, ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts, chunks.tsv built from context_prefix || text, Context prefix: title - type - heading - page, rag_probe2 before/after similarity table (six policies, 13 September), scripts/reindex.py rebuilds chunks and vectors, Schedule-table questions remain weak (rank 2-4), Chunks follow the document's structure (Docling heading labels) (+18 more)

### Community 58 - "Chunking And Classification"
Cohesion: 0.13
Nodes (23): Chunk, chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), Split parsed pages into retrieval-sized chunks that follow the document's own st, One flat list of chunks, ordinal running across the whole document. (+15 more)

### Community 59 - "Advice Fact Reading Tests"
Cohesion: 0.16
Nodes (17): advised_pack(), db(), _document(), FakeConn, FakeCursor, Any, date, datetime (+9 more)

### Community 60 - "Ask Surface Components"
Cohesion: 0.12
Nodes (14): metadata, Abstention(), Part, sentence(), textOf(), ADR-0011, ADR-0016, Turn() (+6 more)

### Community 61 - "Grounding Value Parsing"
Cohesion: 0.11
Nodes (22): collapse(), _cuts_a_number(), _groups(), _is_heading(), _pack(), printed_as(), printed_in(), Extract the values a pack's published sources print, and keep only what the text (+14 more)

### Community 62 - "Settings And Configuration"
Cohesion: 0.11
Nodes (21): _chat_ids(), ConfigurationError, _flag(), _folder(), local_url(), _port(), _positive(), Path (+13 more)

### Community 63 - "App Lock"
Cohesion: 0.18
Nodes (20): GET(), grant(), POST(), UnlockPage(), Accepted, clearFailures(), derive(), failures (+12 more)

### Community 64 - "Web Runtime Dependencies"
Cohesion: 0.09
Nodes (22): ai, @ai-sdk/react, class-variance-authority, clsx, createComponentFactory(), lucide-react, next, next-themes (+14 more)

### Community 65 - "API Event Serialisation"
Cohesion: 0.10
Nodes (22): AbstentionEvent, AdviceCardEvent, AdviceFigure, ConsentRequiredEvent, DeclinedEvent, FinishedEvent, Evidence gathered and good enough to answer from. Nothing has been claimed yet., One sentence that has passed the gate, with the sources it passed on.      It (+14 more)

### Community 66 - "Interface Design Pack"
Cohesion: 0.13
Nodes (22): Not finding you is an answer (first-person abstention), Capture is where the user already is, Citation chips are the trust surface, Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Nothing moves without a reason (motion specification), Silence beats a guess, Suggestions come from this week's ingest (+14 more)

### Community 67 - "Startup Tests"
Cohesion: 0.13
Nodes (19): prepare_checkout(), Path, Startup tests do not ingest documents or need the corpus: they check process bou, npm is a wrapper around node. Killing only the wrapper orphans the port., The worker starts its nightly schedule as a process of its own. Terminating only, Stopping it signals its process group. Without a session of its own that group i, A developer's own `npm run dev` is used rather than fought for the port., `npm run dev` against an empty web/ fails slowly and cryptically. Say so instead (+11 more)

### Community 68 - "Startup Screen"
Cohesion: 0.10
Nodes (21): Packs and Modules May Not Import web/ or api/, Qwen-SEA-LION-v4-4B-VL Generator, The FastAPI Application, The API Surface, GET /api/today Never Marks Anything Notified, apply, Auto-Redirect to Today Once Ready, check (+13 more)

### Community 69 - "Question Vocabulary"
Cohesion: 0.18
Nodes (19): Asked, categories_asked(), glossary(), _make_replacer(), mentions(), _pattern(), What the core and the enabled packs know about how people ask, applied without a, The catalogue's words and every enabled pack's, unioned; a pack's wording wins a (+11 more)

### Community 70 - "Pack Knowledge ADR"
Cohesion: 0.14
Nodes (21): Code-written absence sentence: 'None of the N policies on file is a dental plan.', ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic, The advise route intent returns the pack's advice_decline, answering.categories: ordered whole-word rules over one printed field, Category filter applied before the keep-6 cut, answering.exclusions: headings under which a cover claim is not believed, Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, grounding_sources and grounding_chunks (create-only migration) (+13 more)

### Community 71 - "Web Lint Tooling"
Cohesion: 0.10
Nodes (21): eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node, @types/react (+13 more)

### Community 72 - "Grounding Value Bands"
Cohesion: 0.15
Nodes (20): Hashable, _ambiguous(), _band(), _band_label(), _in_band(), _order_key(), _ordered(), date (+12 more)

### Community 73 - "Retrieval And Answer Path"
Cohesion: 0.11
Nodes (20): never_acts: True in Every Pack Manifest, No New Runtime Dependency Without an ADR, Never Generate SQL at Runtime, The Core Answering Layer, The Answer Path: route, retrieve, rerank, ground, answer or abstain, baseline.py Is Disposable and Never a Measurement, The Grounding Gate, ports.py, the Seam With Lane B (+12 more)

### Community 74 - "Name Scoping"
Cohesion: 0.18
Nodes (19): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), Any (+11 more)

### Community 75 - "Household Identity ADRs"
Cohesion: 0.16
Nodes (20): ADR 0011: The household is people and aliases, and the owner is one of them, facts.subject keeps the unnormalised printed string, db/migrations/0002_household.sql (additive, four CREATE TABLEs), The owner is a row, not a config value baked at install, people table (display name, relation, is_owner), person_aliases (every printed string resolving to a person), A resolved person is shown as a chip, like a citation, The roster is derived from documents, then confirmed (+12 more)

### Community 76 - "Advice Query Tests"
Cohesion: 0.23
Nodes (15): FakeConn, _no_owner(), _owned(), A recording fake in the house style (see `tests/test_grounding_index.py`'s `Fake, Script the owner household.owner reads: one person, `is_owner`., test_a_withdrawal_after_a_grant_gives_none(), test_an_older_version_gives_status_outdated(), test_current_is_none_when_the_latest_grant_is_a_different_version() (+7 more)

### Community 77 - "Module Sweep Tests"
Cohesion: 0.15
Nodes (19): FakeConn, obligation_row(), datetime, A sweep for a date in the future must record that date, or it repeats itself., One row of `queries.SRS_CONTRIBUTIONS_YTD`, in its column order., srs_row(), test_a_dry_run_records_nothing(), test_a_firing_older_than_the_debounce_window_fires_again() (+11 more)

### Community 78 - "Today Surface"
Cohesion: 0.15
Nodes (13): HouseholdPage(), isUrgent(), metadata, summary(), TodayPage(), VaultPage(), ALWAYS_EXISTS, get() (+5 more)

### Community 79 - "Design Tokens"
Cohesion: 0.11
Nodes (10): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+2 more)

### Community 80 - "Design Preview"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 81 - "API Routes"
Cohesion: 0.13
Nodes (18): AskRequest, ModuleSummary, PackSummary, PersonModel, VaultFact, _as_module_summary(), _as_pack_summary(), _as_person() (+10 more)

### Community 82 - "Paperbrain Architecture"
Cohesion: 0.12
Nodes (19): Capture adapters behind one receive() interface, Ingestion worker with idempotent upsert, Two-stage quarantine with a vision-language second pass, Batch 4: the deliberately hard documents, A full policy wording registers as policy_schedule, Task: review every quarantined document and label the failure, Task: sign off the capture-to-database path against the data inventory, Measurement is owned separately from the engine (+11 more)

### Community 83 - "Field Correction Tests"
Cohesion: 0.12
Nodes (16): conn(), FakeConn, The point of the endpoint. An UPDATE alone loses the example we are trying to co, b1-0032.pdf on 13 September: deleted from the inbox, and still asking for attent, `hides its facts` reaches an answer through retrieval, not through the API., A date that has passed is the one somebody most wants to check against the paper, stored_fact(), test_a_corrected_field_stops_being_flagged() (+8 more)

### Community 84 - "Paperbrain Ollama"
Cohesion: 0.17
Nodes (11): answer(), build_context(), format_sources(), Ollama, Answer a question from retrieved chunks, with citations back to the file.  The, Ollama, OllamaUnavailable, RuntimeError (+3 more)

### Community 85 - "Empty And Error States"
Cohesion: 0.13
Nodes (12): DocumentPage(), metadata, metadata, EmptyState(), ProblemState(), RowSkeleton(), SHAPES, QuarantineQueue() (+4 more)

### Community 86 - "Grounding Value Review"
Cohesion: 0.20
Nodes (16): approve(), pending(), PendingValue, Any, date, A person's approval, standing between a model's extraction and any calculator th, Reject these ids with a note, ignoring any that are no longer `pending`., One value waiting for a person to sign off, with what they need to see to do it. (+8 more)

### Community 87 - "Advice And Pack Role ADRs"
Cohesion: 0.18
Nodes (18): ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent, The adult rule: advice is withheld for a person under 21 or a child with no date of birth on file, modules/advice/ calculators returning a Calculation or a Missing, advice_consents, append-only (granted or withdrawn, version, wording hash, channel), Advice graph flow: shape match, subject resolution, consent, AdviceCard, explain, advice_records keeps each answer's full basis, PackManifest.advice shapes (gap, remaining_room, keep_or_surrender, compare_own, compare_market, estimate_saving), Advice.review: one question runs every shape at once (+10 more)

### Community 88 - "Design Canvas Walker"
Cohesion: 0.25
Nodes (18): collectProps(), compileAttr(), cssToObj(), getReact(), hostPositionStyle(), isDeckMountTag(), kebabToCamel(), renderDeckKids() (+10 more)

### Community 89 - "Web Component Config"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "Today Rows And Citations"
Cohesion: 0.16
Nodes (14): SourceChip(), SourcePanel(), stripTrailingPage(), ADR-0016, countdown(), detail(), figure(), ItemRow() (+6 more)

### Community 91 - "Advice Consent"
Cohesion: 0.21
Nodes (16): Channel, current(), grant(), _latest(), NoOwner, Any, RuntimeError, The owner's consent to a pack's advice, append-only (ADR 0016).  Consent is th (+8 more)

### Community 92 - "Core Contracts"
Cohesion: 0.19
Nodes (16): Answering, Categories, Category, Grounding, Guardrails, ModuleTrigger, Persona, BaseModel (+8 more)

### Community 93 - "Grounding Gate"
Cohesion: 0.14
Nodes (15): Exclusions, A sentence claiming cover whose every citation sits under one of `headings` is d, check(), check_one(), The grounding gate.  Rule 3 in AGENTS.md: no claim without a citation. This mo, Never raises, never rewrites a claim. It keeps, drops, or abstains.      The w, Why this one sentence cannot be kept, or `None` if it can.      Depends on not, _says() (+7 more)

### Community 94 - "Module Adviser"
Cohesion: 0.18
Nodes (13): fact_row(), facts_for(), in_category(), _is_an_adviser(), ModuleAdviser, names_for(), product_names(), Adviser (+5 more)

### Community 95 - "Household Canon"
Cohesion: 0.15
Nodes (16): loan_agreement Document Type, payslip Document Type, The Lim Household, Tampines, One Household Only; the Persona Sketches Are Gone, Rachel Ng Arrives Off Documents, Not a Persona Sketch, Household Canon Template, Three Surnames, One Household, doc_id Is the Filename (+8 more)

### Community 96 - "Running Parrot"
Cohesion: 0.15
Nodes (16): ADR 0004 - Local setup can run before the assistant is ready, ADR 0006 - pypdfium2 renders the quarantine page images, ADR 0007 - The graph ships before retrieval and before a checkpoint table, Retrieval is a port, not an import, ADR 0009 - next-themes and lucide-react are the only two web dependencies beyond the stack, .graphifyignore excludes the corpus, Scoping happens after retrieval, and that has a ceiling, The redacted real-document holdout (+8 more)

### Community 97 - "Lane C Governance"
Cohesion: 0.13
Nodes (16): The evaluation is the gate, Data inventory and flow map, ISO/IEC 22989 to 5338 stage-to-process map, Lane C - Governance and assurance, Model card, Retention and erasure policy, Say unverified rather than write a plausible sentence, Siew's generated task list (+8 more)

### Community 98 - "Advice Contract Tests"
Cohesion: 0.16
Nodes (16): _advised(), _checked(), Only income is made annual, so only income may say how often its printed figure, `annual_premium` is printed on no policy schedule; the market's sources publish, `closed_by` names kinds of cover, so a typo would silently print nothing on a sh, ADR 0017: `FactInput.pack` is gone; a payslip's gross salary is a core fact., Validated as a manifest, then against the core catalogue, as `core.packs` loads, The insurance pack plus one rule key, a critical illness gap and a hospital plan (+8 more)

### Community 99 - "Core Document Catalogue"
Cohesion: 0.15
Nodes (15): Sources of Truth Generate Their Outputs, Generated Files Committed Alongside Their Source, benefit_illustration Document Type, birth_certificate Document Type, claim_letter Document Type, cpf_statement Document Type, Core Document Catalogue (ADR 0017), donation_receipt Document Type (+7 more)

### Community 100 - "API Request Models"
Cohesion: 0.13
Nodes (15): ConfirmNameRequest, ConsentRequest, CorrectionRequest, ErrorEvent, OwnerRequest, PlaceRequest, The stream broke after it began. A client cannot read an HTTP status by then., What the person typed. The pack decides what type it is; the caller does not get (+7 more)

### Community 101 - "Pack Manifest Tests"
Cohesion: 0.16
Nodes (14): PackManifest, A domain pack, authored as one YAML file: grounding, persona, answering and advi, An advice shape that names a missing role or key fails at load time., _insurance(), The manifest alone cannot know the catalogue, so it validates; `check_against` n, ADR 0017: documents are the core's. A pack.yaml carrying them does not load., test_a_grounding_corpus_is_named_by_id_not_by_path(), test_a_pack_cannot_opt_out_of_never_acts() (+6 more)

### Community 102 - "Team Split Narrative"
Cohesion: 0.15
Nodes (15): The domain pack manifest, The golden set: answerable, hard negatives, adversarial, Contracts before code, Fill the register first, then mail-merge the documents, The five-lane split (five people, nine weeks, three builders), Invented organisations only, Lane B - Retrieval and evaluation (Yew Mun), Lane C - Governance and assurance (Siew) (+7 more)

### Community 103 - "Data Inventory"
Cohesion: 0.17
Nodes (15): Data inventory: identity data, DOBs and loans, The lock is a screen lock, not encryption, next dev binds every interface, not loopback, Telegram capture route and delete-at-source, What crosses a boundary, Governance artefact set, Write unverified rather than assert, The final ILP report (+7 more)

### Community 104 - "Scan And OCR Tests"
Cohesion: 0.17
Nodes (13): FixtureRequest, Image, _as_printed(), page_pixels(), photographed(), A scanned or photographed document parses to pages with its tables preserved., The register stores typed values; the page prints them the way a person would., Page 1 of the digital schedule, drawn at 200 dpi — the resolution of a desk scan (+5 more)

### Community 105 - "User Stories"
Cohesion: 0.14
Nodes (15): The answer graph: router, retrieve, rerank, grounding gate, Capability modules: Reminder and Alert, Task: build the answer graph with the grounding gate, Contradiction attack, Task: contextualised chunking and the reranker, Task: hybrid retrieval with reciprocal rank fusion, The reminders table as an extension point, Roadmap phase 3 - reminders (+7 more)

### Community 106 - "Lane D Packs And Interface"
Cohesion: 0.14
Nodes (15): Task: complete the Insurance Agent pack, ADR 0017 - a pack is grounding and persona, Lock the design tokens before building any screen, The four surfaces: Today, Ask, Vault, Packs, Lane D - Domain packs and interface, The platform argument: one core, two domains, Task: define the pack catalogue - the nine deferred packs, Zee's generated task list (+7 more)

### Community 107 - "Lane E Corpus"
Cohesion: 0.18
Nodes (15): batch0-personas is deleted and must not be recreated, python -m corpus.validate, The document register as ground truth, The whole-life expiry_date mismatch, Register column headings are generated, not chosen, The household canon (the Lims of Tampines), Register first, documents second, Task: spot-check 20 register rows against the extractor (+7 more)

### Community 108 - "Paperbrain Ingest"
Cohesion: 0.24
Nodes (13): Chunk, chunk_pages(), clean(), Split extracted text into retrieval-sized chunks.  Paperwork is short and stru, _split_page(), discover(), guess_date(), guess_type() (+5 more)

### Community 109 - "Inventory Tests"
Cohesion: 0.23
Nodes (12): Conn, pack(), MonkeyPatch, test_with_no_pack_in_play_the_sentence_limit_is_the_catalogue_s(), UUID, Holdings come from `facts`, one per document that prints the name the categories, ADR 0017: a document is the core's, so the query includes `core` whatever is ena, row() (+4 more)

### Community 110 - "Core Documents"
Cohesion: 0.19
Nodes (14): Passport Uses date_of_expiry So policy_expiry Does Not Fire, filing_deadline Reminder, maturity_date Is Not expiry_date, passport Document Type, passport_expiry Reminder, policy_expiry Reminder, policy_schedule Document Type, Reminder, Alert and Tracker Registers (+6 more)

### Community 111 - "Artefacts Architecture Review"
Cohesion: 0.19
Nodes (14): PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The expansion model: two axes, not one list, Governance: ISO/IEC 22989 stages and ISO/IEC 5338 processes side by side, The pack catalogue, and why Tax and Insurance are the two to build, The VRAM budget, with headroom, Risk register: what will actually go wrong (+6 more)

### Community 112 - "Packs Readme"
Cohesion: 0.18
Nodes (14): I explain the renewal notice, I do not renew policies, Autonomy statement, ISO/IEC 22989 stages versus 5338 processes, never_acts as a machine-checked flag, Grounding corpora now live inside packs, advice module manifest, example_pack template manifest, example_room advice shape (+6 more)

### Community 113 - "Paperbrain Extract"
Cohesion: 0.36
Nodes (12): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+4 more)

### Community 114 - "Household Who Is This"
Cohesion: 0.19
Nodes (10): metadata, OwnerForm(), RELATION_CHOICES, Roster(), Place, PLACES, WhoIsThis(), PendingName (+2 more)

### Community 115 - "Components System Screens"
Cohesion: 0.18
Nodes (11): Action, CONFIRM, ITEMS, PowerMenu(), Stage, DependencyCheck, Phase, RestartingScreen() (+3 more)

### Community 116 - "Api Routes"
Cohesion: 0.21
Nodes (13): A document and a page, as a person would cite it — or, for published guidance, w, Source, TodayItem, _as_source(), _cite(), _link(), date, Split a formatted citation back into its parts, keeping the text either way. (+5 more)

### Community 117 - "Ingest Classify"
Cohesion: 0.19
Nodes (11): Classification, classify(), _prompt(), Ollama, Decide which of the core catalogue's document types a captured document is, or d, Never raises. An unavailable model is a classification failure, so it quarantine, _schema(), ADR 0017: candidates are the catalogue's types, unqualified, and every one is `c (+3 more)

### Community 118 - "Scripts Worker"
Cohesion: 0.26
Nodes (12): _beat_needs_its_own_process(), celery_argv(), main(), Any, Namespace, Popen, Run the ingestion worker, and optionally the nightly schedule with it.      uv, The arguments the Celery command-line would have been given. Built here so a tes (+4 more)

### Community 119 - "Tests Test Registration"
Cohesion: 0.32
Nodes (11): Insert or update the `documents` row for these bytes and say which happened., register_document(), conn(), database_url(), Any, The idempotent upsert, against the real unique index.  `documents.sha256 UNIQUE`, test_a_document_must_arrive_with_a_name(), test_a_new_document_is_inserted() (+3 more)

### Community 120 - "Core Registry"
Cohesion: 0.21
Nodes (12): installed_packs(), Every pack directory holding a pack.yaml, in a stable order.      Directories, _pack_row(), packs(), Every installed pack. Documents and facts are the core's (ADR 0017), so none are, Switch one pack on or off. Raises `UnknownPack` rather than silently doing nothi, One row of `packs`, with the manifest validated back out of its jsonb column., RegisteredPack (+4 more)

### Community 121 - "Runtime Capture"
Cohesion: 0.23
Nodes (8): attribution(), Any, One long poll. A failure waits rather than hammering the API with the same reque, Whose phone this arrived on, recorded before anything is read off it. See ADR 00, _loop(), main(), Path, Run the Telegram capture adapter on its own, and check that the token works.

### Community 122 - "Packs Page"
Cohesion: 0.20
Nodes (7): ADR-0017, metadata, PacksPage(), Toggle(), ModuleSummary, packs(), PackSummary

### Community 123 - "Docs Notion"
Cohesion: 0.18
Nodes (12): ADR 0001 - Record architecture decisions, ADR 0002 - One PostgreSQL instance for everything, Reciprocal rank fusion of dense and lexical, ADR 0003 - PaperBrain informs the pattern, not the module, PaperBrain prototype, ADR 0010 - main is unprotected, and the discipline is human, One Notion workspace per Claude account, Move the hub into the integrator's workspace (+4 more)

### Community 124 - "Yew Mun Readme"
Cohesion: 0.17
Nodes (12): Task: benchmark the workstation and publish the numbers, Week 1 hardware benchmark with run-to-run spread, Lane B - Retrieval and evaluation, The deliberately naive retrieval baseline, Committed runs are never deleted, Yew Mun's generated task list, Hybrid retrieval, not embeddings alone, Chunking respects paragraphs (+4 more)

### Community 125 - "Ingest Obligations"
Cohesion: 0.25
Nodes (10): ReminderConfig, fixed(), from_facts(), _label(), Any, date, Turn a dated fact into a commitment to do something about it.  A fact is a sta, What a person is shown. The key is the catalogue's word for it; the subject says (+2 more)

### Community 126 - "Tests Test Advice Core"
Cohesion: 0.36
Nodes (10): check_content(), Why a cited sentence still cannot be kept, or `None`. Asked after `check_one` pa, _calculation(), The types a calculator hands back, the owner's consent, and the record of an adv, test_check_content_keeps_a_sentence_stating_a_facts_value(), test_check_content_keeps_a_sentence_stating_a_figure(), test_check_content_keeps_a_sentence_stating_a_rules_value(), test_check_content_still_drops_a_sentence_stating_an_unprinted_number() (+2 more)

### Community 127 - "Tests Test Insurance Pack"
Cohesion: 0.22
Nodes (10): categorise(), The first rule whose printed words appear. `None` is an answer, not a failure., _categories(), The insurance pack's categories, against the product names that would misfile th, Asking what to get is asking what is missing, and the review is what answers it., A shortfall nobody can act on is half an answer. `closed_by` is what makes the r, test_a_printed_product_name_falls_in_exactly_the_category_a_person_would_file_it_under(), test_asking_what_to_get_reaches_the_coverage_review() (+2 more)

### Community 128 - "Governance Synthetic Data Case"
Cohesion: 0.18
Nodes (11): Qwen-SEA-LION-v4-4B-VL extraction ceiling, Register first, then generate, SYNTHETIC DOCUMENT footer, Ground truth for free, The 40-document holdout corpus, The case for synthetic evaluation data, Two withdrawn synthetic-data controls, extraction_f1 (+3 more)

### Community 129 - "Docs Pack Authoring"
Cohesion: 0.22
Nodes (11): The demonstration run sheet, Step 8 - switch a pack off, Step 6 - the abstention, Step 7 - the refusal to act, Domain pack, Five to eight fields per document type, Pack grounding corpus, Pack guardrails (+3 more)

### Community 130 - "Tests Test Api"
Cohesion: 0.24
Nodes (10): next_kind(), The kind of the next event on the wire., Starlette never closes a body iterator a disconnected client stopped pulling. `_, The ruling's case as it happens on a socket: Starlette sends the card and at onc, What the API owns when a stream is closed with the graph still parked on the car, The graph's own cleanup can fail -- for example the record insert raises -- and, test_a_client_that_leaves_after_the_card_commits_one_record(), test_a_client_that_leaves_mid_explanation_still_commits_what_it_was_shown() (+2 more)

### Community 131 - "Components Nav"
Cohesion: 0.25
Nodes (7): AppLayout(), LockButton(), SURFACES, TabBar(), Tabs(), CHOICES, ThemeToggle()

### Community 132 - "Ask Advice Card"
Cohesion: 0.25
Nodes (10): Advice, AdviceCard(), AdviceNote(), AdviceWithheld(), capitalise(), sentence(), TONES, ADR-0016 (+2 more)

### Community 133 - "Adapters Readme"
Cohesion: 0.20
Nodes (10): Amend the Graph Refresh Into the Commit, No CORS Middleware, Deliberately, Week 2 Entry, 9-15 Sep 2026, Capture Channels Are Transports, receive(payload, mime, sender, ts, *, original_name), Idempotent Upsert on a SHA-256 of the Source Bytes, State What Synthetic Data Does Not Prove, Clean, Scanned and Photo Tiers (+2 more)

### Community 134 - "Agents"
Cohesion: 0.20
Nodes (10): Definition of Done, No Claim Without a Citation, Every Response That States Something Carries Its Source, Citation Names Resolved Once Per Response, Slash Commands: orient, check, handover, weekly, One Vertical Slice Per Pull Request, field_pages Is a Second Pass Over the Register, Fill the Register Before Generating Documents (+2 more)

### Community 135 - "Docs Graphify"
Cohesion: 0.24
Nodes (10): One cell, one field, Policy Schedule Template, Renewal Notice Template, Amend the graph refresh into the commit, Graphify shared knowledge graph, Two kinds of extraction, Union merge driver for graph.json, A field name is three things at once (+2 more)

### Community 136 - "Insurance Notebook Prompts Full"
Cohesion: 0.24
Nodes (10): b1-0001 Private Car Insurance Policy Schedule, b1-0002 HomeShelter Contents Policy Schedule, b1-0003 Hospital Income Protection Plan Schedule, Full-length insurance policy notebook prompt, No Ref: line anywhere on the document, Cross-document corpus consistency, Four full-policy notebook prompts, Shared policy-drafting preamble (+2 more)

### Community 137 - "Docs Household And Identity"
Cohesion: 0.22
Nodes (10): Step 2 - the source chip, Derive the roster, then confirm it, Exactly one owner, enforced by the database, facts.subject is never normalised, people and person_aliases, Three buckets, not two, The correctly-cited wrong person, The ten field types (+2 more)

### Community 138 - "Eval Score"
Cohesion: 0.20
Nodes (7): _as_date(), extraction_f1(), F1, date, The register's text against an extracted value, each normalised the way the pack, Field extraction scored against the register, overall and by document type., same_value()

### Community 139 - "Christian Readme"
Cohesion: 0.20
Nodes (10): The code pass of the knowledge graph, Nobody edits core/contracts.py in a feature pull request, Lane A - Integration and product, The semantic pass of the knowledge graph, Triage prompt: four buckets, no code written, Ninety protected minutes a week of integration, Christian's generated task list, PaperBrain (+2 more)

### Community 140 - "Tests Test Advice Core"
Cohesion: 0.24
Nodes (3): FakeCursor, Any, FakeConn

### Community 141 - "Chat Route"
Cohesion: 0.33
Nodes (9): lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns(), readEvents(), ADR-0016, upstreamDetail() (+1 more)

### Community 142 - "Vault Field"
Cohesion: 0.31
Nodes (8): DocumentDetail(), when(), Field(), format(), isNumeric(), CorrectionResponse, pageImage(), VaultFact

### Community 143 - "Web Package"
Cohesion: 0.20
Nodes (9): name, private, scripts, build, dev, lint, start, typecheck (+1 more)

### Community 144 - "Readme"
Cohesion: 0.22
Nodes (9): Working Agreement for Coding Agents, The Five Lanes and Their Owners, The Contribution Loop, main Is Deliberately Unprotected, Setting Up a Second Machine, PARROT Is an Internal Working Name, main Is Not Protected, PARROT, a Local-First Household RAG Platform (+1 more)

### Community 145 - "Worker Schedule"
Cohesion: 0.33
Nodes (8): beat_schedule(), cron_expressions(), crontab_from(), manifest(), Any, When the nightly sweeps run, read from the modules' own manifests.  A module alr, A five-field cron expression as Celery understands it., The cron line for each swept module, by module id. Testable without Celery insta

### Community 146 - "Docs Synthetic Generation Guide"
Cohesion: 0.31
Nodes (9): PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Gemini prompt bank for identity specimens, The Lim household canon, Republic of Xinkapow (+1 more)

### Community 147 - "Eval Readme"
Cohesion: 0.28
Nodes (9): Days without recorded cover tile, alert_fpr, obligation_precision, Module manifest template, Quoted "on" key in YAML 1.1, alert module manifest, Modules read typed rows, never chunks, reminder module manifest (+1 more)

### Community 148 - "Tests Test Api"
Cohesion: 0.22
Nodes (9): obligation(), The nightly sweep owns `last_notified_at`. A screen refresh must not burn a wind, A registry that failed to install must fail loudly, not silently silence the hou, The Celery beat never goes through the API, so the filter cannot live there., test_a_core_reminder_still_reaches_today_when_its_old_pack_is_off(), test_a_disabled_pack_does_not_reach_the_nightly_sweep(), test_an_empty_registry_shows_everything_rather_than_nothing(), test_every_today_item_names_its_source() (+1 more)

### Community 150 - "App Layout"
Cohesion: 0.25
Nodes (6): figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 151 - "Grounding Index"
Cohesion: 0.29
Nodes (8): index_pack(), Any, date, Ollama, Path, Upsert this pack's sources and stage the values a changed one prints.      A p, Insert or refresh the source's row, and return its id., _upsert_source()

### Community 152 - "Migrations 0001"
Cohesion: 0.36
Nodes (7): chunks, documents, facts, modules, obligations, packs, traces

### Community 153 - "Docs Running"
Cohesion: 0.39
Nodes (8): ADR 0005 - The watched folder is polled, not subscribed to, Stability debounce with injected time, ADR 0008 - Ingestion runs on a Celery worker, The queue carries a digest, not the document, The ingestion worker, START.cmd launcher, Telegram capture, The watched inbox folder

### Community 154 - "Startup And Power Main"
Cohesion: 0.29
Nodes (8): The readiness check verifies the model the way it will be used (one pair scored), Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Four readiness components: your documents, filing, screens, local model, Getting Parrot ready (startup readiness screen), Power menu: Lock, Restart Parrot, Shut down Parrot, Restarting Parrot (engine stops, a fresh engine starts, the page reconnects by itself), Parrot is off (terminal state page), Parrot is waiting for its database (Docker Desktop not running)

### Community 155 - "Uploads Parrot Design Evaluation"
Cohesion: 0.25
Nodes (8): parrot-sweep shimmer animation, Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, An answer with the page it came from, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction

### Community 156 - "Scripts Build Team Tasks"
Cohesion: 0.39
Nodes (7): main(), Path, Generate each member's task list from the master task CSV.      python scripts, _read_rows(), _render(), _week_key(), _write()

### Community 157 - "Scripts Start Parrot"
Cohesion: 0.32
Nodes (7): main(), Path, Local-only startup preflight, using the standard library so setup can be diagnos, Inspect startup files without importing the application or reading user data., Report categories only, without hostname, username, serial numbers or file conte, report_hardware(), startup_gaps()

### Community 158 - "Desmond Readme"
Cohesion: 0.25
Nodes (8): The demonstration run sheet and backup recording, Task: code freeze and tag v1.0-demo, Adversarial testing from week 7, Prompt injection carried inside a document, Scope attack: asking it to act, Task: run adversarial Set C and write up the findings, Adversarial Set C (15 questions that should not be answered), Golden Set C - adversarial (15)

### Community 159 - "Tests Test Api"
Cohesion: 0.25
Nodes (8): open_obligation(), Snooze means 'not until this gets more urgent', so it can name the day it does., No new column: `already_said` is what makes the row quiet, and it reads this one, test_an_obligation_can_be_closed_as_done_or_dismissed(), test_an_obligation_cannot_be_closed_into_an_invented_state(), test_snooze_says_the_day_it_will_speak_again(), test_snooze_stamps_the_column_the_sweep_already_reads(), test_snoozing_inside_the_last_window_admits_there_is_nothing_after_it()

### Community 160 - "[ Path] Route"
Cohesion: 0.43
Nodes (7): ALLOWED, Context, DELETE(), forward(), GET(), PATCH(), POST()

### Community 161 - "Ingest Readme"
Cohesion: 0.33
Nodes (7): Every Fact Row Cites Its Source, A Correction Cannot Invent a Row, Every Node Writes One Line to traces, The Ingestion Pipeline, The Pipeline Forks Into Retrieval and Facts Lanes, Numbers Come From Postgres, Never From the Model, macOS Worker Runs Celery Solo

### Community 162 - "Api Models"
Cohesion: 0.29
Nodes (7): AskResponse, Claim, The whole answer, once. `text` is the consent wording when `kind` is `consent_re, One sentence and the passages it was traced to. Never emitted without `citations, _as_response(), One `Answer` to one of the shapes a client has to handle., AskResponse

### Community 163 - "Adapters Base"
Cohesion: 0.29
Nodes (5): CaptureAdapter, datetime, Protocol, Folder, Telegram, and post-MVP WhatsApp and Drive, all reduced to one call., Capture adapters.  Every channel a document can arrive through satisfies one int

### Community 164 - "Graph Gate"
Cohesion: 0.29
Nodes (7): _normal(), "1,860.00", "1860" and "01" → "1860", "1860", "1": formatting is not a different, Every number or identifier in a sentence that no cited passage prints. An identi, unprinted_numbers(), test_a_date_on_file_may_be_written_the_way_a_person_says_it(), test_a_leading_zero_does_not_make_a_printed_date_unprinted(), test_a_policy_number_is_kept_only_when_it_is_printed_whole()

### Community 165 - "Eval Readme"
Cohesion: 0.38
Nodes (7): abstention_rate, PARROT evaluation harness, Set A, answerable, Set B, hard negatives, Set C, adversarial, The golden question sets, must_cite_page from field_pages

### Community 166 - "Eval Score"
Cohesion: 0.29
Nodes (3): Any, RagasJudge, Ragas 0.4 metrics through Ollama's OpenAI-compatible endpoint. Imported lazily s

### Community 167 - "Siew Readme"
Cohesion: 0.29
Nodes (7): The autonomy statement, Governance claims traced to enforcement points, IMDA mappings and autonomy statement artefact, The facts table as an extension point, Constraint: fully offline, Explicitly not doing: cloud, hosted vectors, autonomous spending, Roadmap phase 2 - facts

### Community 168 - "Tests Test Api"
Cohesion: 0.33
Nodes (7): advice_card(), A published value's chip: no document and no page, only who published it and whe, A published number has no page to open. What makes it checkable is who published, Nothing shown, nothing recorded. Once advice is on the screen, a failure after i, rule_citation(), test_an_advice_card_carries_a_rules_publisher_on_the_wire(), test_an_answer_that_fails_before_any_advice_is_rolled_back_and_after_it_is_kept()

### Community 169 - "System Route"
Cohesion: 0.52
Nodes (6): ACTIONS, GET(), POST(), sameOrigin(), unlocked(), isUnlocked()

### Community 170 - "Components Wordmark"
Cohesion: 0.38
Nodes (4): metadata, UnlockForm(), Wordmark(), WordmarkLockup()

### Community 171 - "Agents"
Cohesion: 0.33
Nodes (6): The Purely Additive Migration Exception, Contracts and Migrations Are Their Own PR, Snooze Means Not Until This Gets More Urgent, The Three Things Agents Get Wrong Here, MemorySaver Until a Reviewed Migration, MemorySaver Checkpointer, Not PostgresSaver

### Community 172 - "Tests Test Household"
Cohesion: 0.33
Nodes (6): is_first_person(), Whether this question is about the person asking.      `other_names` are the d, "What is Rachel's premium on my policy" is a question about Rachel.      A rel, test_a_named_household_member_wins_over_the_pronoun(), test_first_person_questions_are_recognised(), test_questions_about_other_people_are_not_scoped()

### Community 173 - "Packs Readme"
Cohesion: 0.33
Nodes (6): Appendicitis entitlement demonstration, Page one as plain Label: value lines, Ward and hospital entitlement clause, Answering: vocabulary, categories, exclusions, The four tests every field must pass, policy_type was judged, not printed

### Community 174 - "Notebooks Generate Lim Documents"
Cohesion: 0.47
Nodes (5): find_browser_executable(), generate_documents(), Path, Project Parrot - Synthetic Document Generator for Lim Household ===============, Find Microsoft Edge or Google Chrome executable on Windows.

### Community 175 - "Scripts Load Corpus"
Cohesion: 0.47
Nodes (5): documents_in(), main(), Path, Load a handed-over corpus batch into this computer's database.      uv run pytho, Every document in the batch, in a stable order, recursing into tier subfolders.

### Community 176 - "Api Models"
Cohesion: 0.40
Nodes (5): AdviceConsent, AdviceConsent, One advising pack, the wording a person is asked to agree to, and what the owner, _as_consent(), One advising pack's consent wording and the owner's standing answer to it.

### Community 177 - "Migrations 0002 Household"
Cohesion: 0.70
Nodes (4): document_attribution, people, person_aliases, telegram_identities

### Community 178 - "Migrations 0003 Advice"
Cohesion: 0.60
Nodes (4): advice_consents, advice_records, grounding_sources, grounding_values

### Community 179 - "Desmond Readme"
Cohesion: 0.40
Nodes (5): The 40-document redacted holdout, The synthetic-to-real gap, Consent and redaction protocol, Task: write the PDPA position on using synthetic data, Task: evaluation run 3 plus the holdout run

### Community 180 - "Api Routes"
Cohesion: 0.67
Nodes (4): connection(), Request, One connection per request, closed when it ends.      Handlers are declared `d, _settings()

### Community 181 - "Graph Answer"
Cohesion: 0.50
Nodes (3): fuse(), Several searches as one list: each passage once, at the best score any phrasing, Every phrasing of the question, searched and fused. The person's own words alway

### Community 182 - "Parrot Uiux Refinement Support"
Cohesion: 0.67
Nodes (4): createPseudoSheet(), importantify(), scanUnquotedUrl(), stripComments()

### Community 183 - "Tests Test Contracts"
Cohesion: 0.50
Nodes (4): Path, A downloaded pack carries its sources, so no corpus is left at the repository ro, test_a_grounding_corpus_travels_inside_its_pack(), test_every_grounding_corpus_declares_its_provenance()

### Community 184 - "Graph Inventory"
Cohesion: 0.67
Nodes (3): holdings(), Any, Rows of `INVENTORY`, one holding per document that prints the field an enabled p

### Community 185 - "Tests Test Rerank"
Cohesion: 0.67
Nodes (3): MonkeyPatch, A scorer that ranks by the number the passage text ends with, and records what i, scored()

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
- **264 isolated node(s):** `packs`, `modules`, `traces`, `parrot`, `setup.sh script` (+259 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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