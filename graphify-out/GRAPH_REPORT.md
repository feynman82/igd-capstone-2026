# Graph Report - igd-capstone-2026  (2026-10-04)

## Corpus Check
- 318 files · ~725,133 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 35 file(s) not represented in the graph (top: (none) 11, .jsonl 8, .csv 5)

## Summary
- 5165 nodes · 11979 edges · 665 communities (221 shown, 444 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 1507 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5ca1e35b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ModelUnavailable
- HybridRetriever
- test_advice_graph.py
- ScriptedOllama
- validate
- advice/__init__.py
- Advice shape death_tpd_cover (gap calculator)
- test_advice_module.py
- api.ts
- test_ingest_pipeline.py
- test_grounding_index.py
- tasks.py
- FolderAdapter
- test_telegram_capture.py
- FakeConn
- InstalledPack
- bench_runtime.py
- vault.py
- support.js
- schedule.py
- ingest/extract.py
- test_grounding_values.py
- reminder/__init__.py
- Passage
- TelegramAdapter
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
- test_modules.py
- Measured
- extract_values
- test_api.py
- alert/__init__.py
- retrieve.py
- rows_for
- test_household.py
- pytest
- test_eval_modules.py
- test_tax_pack.py
- walk
- models.py
- report.py
- compilerOptions
- Domain packs — start here
- registry.py
- test_grounding.py
- Any
- cli.py
- run.py
- PARROT Interface Design Pack
- packs.py
- ModuleAdviser
- PackManifest
- values.py
- item-row.tsx
- lock.ts
- AlertConfig
- _as_event
- Getting Parrot ready (startup readiness screen)
- advice_consent.py
- `api/` — the FastAPI application
- pack
- value_forms
- devDependencies
- index_pack
- scope.py
- Citation chips are the trust surface
- Claim
- Any
- today/page.tsx
- RagasJudge
- preview.tsx
- ingest/quarantine.py
- PaperBrain dependency set
- Answer
- Ollama
- paperbrain/chunk.py
- review_grounding_values.py
- ADR 0016: A pack advises; code calculates from cited facts and reviewed rule values, under recorded consent
- ModuleManifest
- components.json
- routes.py
- 18 · The reranker runs in-process, because Ollama cannot serve a cross-encoder
- contracts.py
- boot
- test_eval_report.py
- The Lim Household, Tampines
- Starting Parrot
- test_contracts.py
- Core Document Catalogue (ADR 0017)
- Notebook prompts — the four full policies for Marcus Lim
- is_first_person
- PARROT Architecture Review
- db service (pgvector/pgvector:pg17)
- test_rerank.py
- Roadmap
- Task: complete the Insurance Agent pack
- ingest.py
- Tax and Reliefs — contract changes this pack needs
- Reminder, Alert and Tracker Registers
- Settings
- Module manifest template
- paperbrain/extract.py
- §5 · Evaluation and results
- tokens/page.tsx
- Try PARROT
- Integration review
- Ollama
- adr/README.md
- test_worker_queue.py
- Retention and erasure policy
- AdviceConsent
- Task: benchmark the workstation and publish the numbers
- Running the evaluation harness
- Project PARROT — team split
- 4. Writing `pack.yaml`
- Filling the corpus register
- Writing a governance artefact
- Changelog
- Working agreement for coding agents
- igd-capstone-2026
- Policy schedule HTML template
- PaperBrain
- Silence beats a guess
- answer.tsx
- _Answering
- settings
- Set C: adversarial
- PrivateCare Policy Wording Template
- alert_fpr
- dependencies
- FakeCursor
- app/layout.tsx
- Household canon
- Authoring a domain pack
- ADR 0005 - The watched folder is polled, not subscribed to
- eval/modules.py
- DesignPreview evaluation harness
- DatabaseUnavailable
- connection
- Siew — Lane C · Governance and assurance
- Writing an ADR
- AskResponse
- Cursor
- The demonstration run sheet
- Evaluation
- getReact
- (app)/layout.tsx
- .retrieve
- User stories and acceptance criteria
- DocumentCatalog
- 19 · A relevance floor on the reranker does not buy abstention, and the reason is not calibration
- Appendicitis entitlement demonstration
- Project skills
- pull_request_template.md
- _today_items
- test_a_client_that_leaves_after_the_card_commits_one_record
- The 40-document redacted holdout
- filesystem
- ._absence
- pipeline.py
- Project PARROT — team split
- Basic Financial Planning Guide
- ClosingSpy
- load_corpus.py
- open_obligation
- package.json
- 3. Comprehensive Document Suite: Policy Wordings & Loan Agreements
- Lane E - Corpus and adversarial testing
- packs/page.tsx
- Provenance register for corpus sg_protection_guidance
- setup.sh
- session-start.sh
- Insurance and Coverage pack (insurance_agent)
- postcss.config.mjs
- Lane C - Governance and assurance
- parrot
- paperbrain/ask.py
- AdviceWithheldEvent
- test_correcting_a_field_keeps_what_it_used_to_say
- Comparison of Integrated Shield Plans
- Christian — task list
- Desmond — Lane E · Corpus and adversarial testing
- Desmond — task list
- Siew — task list
- Yew Mun — task list
- Graphify — the shared knowledge graph
- First run
- Understanding health insurance
- Kitchen Table, resolved - for implementation
- The household, and the word "my"
- 2. Amended Gemini Prompts Bank (Xinkapow Yellow/Orange Cards with KFC Mascot)
- Zee — Lane D · Domain packs and interface
- Zee — task list
- Household canon
- 0001_init.sql
- [...path]/route.ts
- Contributing
- The corpus
- 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module
- 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack
- 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent
- NNNN · The decision, as a statement not a question
- Notion
- Premium and Subsidy Tables
- Understanding integrated shield plans
- Christian — Lane A · Integration and product owner
- Yew Mun — Lane B · Retrieval and evaluation
- test_an_advice_card_carries_a_rules_publisher_on_the_wire
- Architecture
- system/route.ts
- Claude Code — read this first
- 2. One PostgreSQL instance for everything
- 10. `main` is unprotected, and the discipline is human
- 12. Chunks follow the document's headings, and embeddings use the model's task prompts
- 14 · A pack supplies what the core knows about a domain, and the core stays generic
- 17 · A pack is grounding and persona; the core owns documents
- Artefacts
- Why the prototype is evaluated on synthetic data
- `docs/report/` — the final report
- About Integrated Shield Plan
- MediShield Life Benefits
- The team
- Basis
- `core/graph/` — the LangGraph runtime
- 0002_household.sql
- 0003_advice.sql
- 1. Record architecture decisions
- 4. Local setup can run before the household assistant is ready
- 6. pypdfium2 renders the page images the quarantine second pass reads
- 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document
- 13. A question is understood before it is searched, and scoped before it is cut
- Data inventory — identity data, dates of birth and loans
- Notice
- `core/ingest/` — the ingestion worker
- `core/retrieve/` — hybrid retrieval
- 7. The answer graph ships before hybrid retrieval and before a checkpoint table
- 15. A name scopes a question, and a grandparent is not a parent
- github.md
- test_the_debounce_key_separates_two_policies_of_one_person
- `docs/governance/` — the assurance artefacts
- Category hospital_expense (hospital and surgical plan)
- `core/adapters/` — capture adapters
- Home Contents Insurance Policy
- The FastAPI Application
- sets/README.md
- grounding/README.md
- next.config.ts
- Qwen-SEA-LION-v4-4B-VL Generator
- Working Agreement for Coding Agents
- The Five Lanes and Their Owners
- Slash Commands: orient, check, handover, weekly
- receive(payload, mime, sender, ts, *, original_name)
- The Grounding Gate
- Idempotent Upsert on a SHA-256 of the Source Bytes
- The Ingestion Pipeline
- bge-reranker-v2-m3 Cross-Encoder, 40 Down to 6
- Hybrid Retrieval: Dense Plus Full-Text
- Reciprocal Rank Fusion, k=60
- The Score Floor the Gate Reads
- The 40 Per Cent Hospital Premium Jump at the 2027 Renewal
- Life Events the Documents Must Reflect
- The Validator Is the Handover Gate
- ADR 0001 - Record architecture decisions
- ADR 0002 - One PostgreSQL instance for everything
- Reciprocal rank fusion of dense and lexical
- ADR 0003 - PaperBrain informs the pattern, not the module
- PaperBrain prototype
- ADR 0004 - Local setup can run before the assistant is ready
- Stability debounce with injected time
- ADR 0006 - pypdfium2 renders the quarantine page images
- ADR 0007 - The graph ships before retrieval and before a checkpoint table
- ADR 0008 - Ingestion runs on a Celery worker
- ADR 0009 - next-themes and lucide-react are the only two web dependencies beyond the stack
- ADR 0010 - main is unprotected, and the discipline is human
- ADR 0011: The household is people and aliases, and the owner is one of them
- facts.subject keeps the unnormalised printed string
- db/migrations/0002_household.sql (additive, four CREATE TABLEs)
- people table (display name, relation, is_owner)
- person_aliases (every printed string resolving to a person)
- Telegram chat_id maps to a person
- ADR 0012: Chunks follow the document's headings, and embeddings use the model's task prompts
- chunks.tsv built from context_prefix || text
- Context prefix: title - type - heading - page
- rag_probe2 before/after similarity table (six policies, 13 September)
- scripts/reindex.py rebuilds chunks and vectors
- Task prompts: embed_query and embed_documents
- ADR 0013: A question is understood before it is searched, and scoped before it is cut
- The answer prompt carries today's date and names the scoped relation as who the question is about
- AskRequest.history carries up to twelve earlier turns
- Possessive relations scope the question, before the cut to six
- Understand, then search (one model call writes the whole question plus 2-3 document-worded queries)
- Code-written absence sentence: 'None of the N policies on file is a dental plan.'
- ADR 0014: A pack supplies what the core knows about a domain, and the core stays generic
- answering.categories: ordered whole-word rules over one printed field
- Category filter applied before the keep-6 cut
- answering.exclusions: headings under which a cover claim is not believed
- grounding_sources and grounding_chunks (create-only migration)
- Inventory: documents on file read from facts with one hand-written query
- Every passage carries a kind: document, inventory or guidance
- persona.system is placed before the core's rules, which come last
- answering.vocabulary: what a household says to what the paper prints
- Naming exactly one person scopes to them (whole name, or a 3+ letter possessive unique to them)
- ADR 0015: A name scopes a question, and a grandparent is not a parent
- Only confirmed names name anybody
- Name scoping reuses scope_to, so the three buckets hold
- modules/advice/ calculators returning a Calculation or a Missing
- advice_consents, append-only (granted or withdrawn, version, wording hash, channel)
- Advice graph flow: shape match, subject resolution, consent, AdviceCard, explain
- advice_records keeps each answer's full basis
- PackManifest.advice shapes (gap, remaining_room, keep_or_surrender, compare_own, compare_market, estimate_saving)
- Advice.review: one question runs every shape at once
- Explanation gate: every number equals a printed input, no verdict word, no never_say phrase
- A grounding corpus lives at packs/<pack>/grounding/<corpus_id>/
- A rider is its own fact, categorised by its own printed name
- Rule and market values are typed rows, extracted automatically and approved by a person
- Guardrails.verdict_by_code: a verdict is chosen by code, never written by the model
- A pack holds grounding, persona, guardrails, its own answering and advice - nothing else
- ADR 0017: A pack is grounding and persona; the core owns documents
- core/documents.yaml, the single document catalogue
- DocumentCatalog contract
- FactInput.pack is removed; doc_types and field are catalogue names
- Facts are written with pack_id = 'core', and core is always enabled
- FieldType labelled_money with FieldSpec.repeats
- Two answering layers: core answering always applies, an enabled pack adds to it
- ADR 0018: The reranker runs in-process, because Ollama cannot serve a cross-encoder
- BAAI/bge-reranker-v2-m3 loaded in-process with transformers and torch
- PARROT_RERANK_MODEL now holds a Hugging Face model id
- ADR index (0001-0018, with status)
- AGENTS.md requires an ADR for any new runtime dependency
- ADR template (Status, Context, Decision, Alternatives, Consequences, Revisit when)
- Full-length insurance policy notebook prompt
- Register first, then generate
- Four full-policy notebook prompts
- Shared policy-drafting preamble
- Guaranteed surrender value table (b1-0031)
- Artefacts index (proposal, deck, reviews, diagrams, source material)
- Qwen-SEA-LION-v4-4B-VL (AI Singapore, 4B, MIT, 256K context, vision-language)
- The five-lane split (five people, nine weeks, three builders)
- Lane A - Integration and product owner (Christian)
- Lane B - Retrieval and evaluation (Yew Mun)
- Lane C - Governance and assurance (Siew)
- Lane D - Domain packs and interface (Zee)
- Lane E - Corpus and adversarial testing (Desmond)
- Step 8 - switch a pack off
- Step 6 - the abstention
- Step 7 - the refusal to act
- Step 2 - the source chip
- Data inventory: identity data, DOBs and loans
- Telegram capture route and delete-at-source
- What crosses a boundary
- Autonomy statement
- Governance artefact set
- ISO/IEC 22989 stages versus 5338 processes
- The 40-document holdout corpus
- The case for synthetic evaluation data
- Graphify shared knowledge graph
- .graphifyignore excludes the corpus
- Two kinds of extraction
- people and person_aliases
- Three buckets, not two
- The correctly-cited wrong person
- One Notion workspace per Claude account
- team-tasks.csv is where the plan lives
- Domain pack
- Pack grounding corpus
- python -m packs.build
- The final ILP report
- The redacted real-document holdout
- Dense-only retrieval stopgap
- Quarantine and the vision second pass
- Rebuilding the vault's vectors
- START.cmd launcher
- Telegram capture
- The watched inbox folder
- Gemini prompt bank for identity specimens
- Ground truth Q&A test matrix
- The Lim household canon
- Synthetic specimen watermark
- Lane A - Integration and product
- Lane B - Retrieval and evaluation
- Lane D - Domain packs and interface
- Lane E - Corpus and adversarial testing
- abstention_rate
- extraction_f1
- obligation_precision
- Set A, answerable
- Set B, hard negatives
- Set C, adversarial
- The golden question sets
- must_cite_page from field_pages
- Setting Up a Second Machine
- PARROT Is an Internal Working Name
- Platform Workers have wider protection gaps than the economically active population
- IP deductible ($1,500-$3,500 by ward class) and 5% co-payment
- Answering: vocabulary, categories, exclusions
- Pack grounding corpus rules
- Capability Modules: Reminder, Alert, Tracker
- Domain Packs
- PARROT, a Local-First Household RAG Platform
- The Stack in One Table
- The answer graph: router, retrieve, rerank, grounding gate
- Capability modules: Reminder and Alert
- Capture adapters behind one receive() interface
- The code pass of the knowledge graph
- The demonstration run sheet and backup recording
- Ingestion worker with idempotent upsert
- Lane A - Integration and product
- The semantic pass of the knowledge graph
- Two-stage quarantine with a vision-language second pass
- Task: build the answer graph with the grounding gate
- Task: code freeze and tag v1.0-demo
- Christian's generated task list
- Adversarial testing from week 7
- Batch 4: the deliberately hard documents
- Contradiction attack
- python -m corpus.validate
- The document register as ground truth
- The household canon (the Lims of Tampines)
- Prompt injection carried inside a document
- Scope attack: asking it to act
- Task: review every quarantined document and label the failure
- Task: run adversarial Set C and write up the findings
- Task: spot-check 20 register rows against the extractor
- Desmond's generated task list
- Twelve golden-set questions per person by the end of week 3
- Lane B - Yew Mun, retrieval and evaluation
- Lane C - Siew, governance and assurance
- Lane D - Zee, domain packs and interface
- Lane E - Desmond, corpus and adversarial testing
- Ninety protected minutes a week for integration
- Consent and redaction protocol
- Data inventory and flow map
- IMDA mappings and autonomy statement artefact
- ISO/IEC 22989 to 5338 stage-to-process map
- Lane C - Governance and assurance
- Model card
- Retention and erasure policy
- Task: write the PDPA position on using synthetic data
- Task: sign off the capture-to-database path against the data inventory
- Siew's generated task list
- Golden Set A - answerable (60)
- Golden Set B - hard negatives (25)
- Golden Set C - adversarial (15)
- Week 1 hardware benchmark with run-to-run spread
- Lane B - Retrieval and evaluation
- The nine metrics and their targets
- Task: contextualised chunking and the reranker
- Task: evaluation run 3 plus the holdout run
- Task: hybrid retrieval with reciprocal rank fusion
- Yew Mun's generated task list
- The four surfaces: Today, Ask, Vault, Packs
- Lane D - Domain packs and interface
- Task: define the pack catalogue - the nine deferred packs
- Zee's generated task list
- Task: write the user stories with acceptance criteria
- The facts table as an extension point
- PaperBrain handled failure modes
- The reminders table as an extension point
- Roadmap phase 1 - retrieval
- PaperBrain hybrid retrieval (BM25 + dense, fused by RRF)
- The pb command line
- Sample home contents insurance policy
- Ask Screen
- The Four Surfaces
- Packs Screen
- If Something Goes Wrong
- Vault Screen
- The household ledger - specified, not built in v1
- Marcus - retrieval core on Ask
- Rachel - Reminder module on Today
- Marcus - Alert module on Today (SRS ceiling)
- Marcus and Rachel - capture into the Vault
- Ask surface
- Packs surface
- Today surface
- Vault surface
- web/ - the PARROT interface

## God Nodes (most connected - your core abstractions)
1. `InstalledPack` - 139 edges
2. `Passage` - 125 edges
3. `Settings` - 113 edges
4. `ScriptedOllama` - 112 edges
5. `Ollama` - 95 edges
6. `FakeConn` - 94 edges
7. `AnswerGraph` - 92 edges
8. `ModelUnavailable` - 86 edges
9. `Answer` - 82 edges
10. `Sentence` - 75 edges

## Surprising Connections (you probably didn't know these)
- `Provenance register for corpus sg_protection_guidance` --references--> `Lane A - Christian, integration and product`  [AMBIGUOUS]
  packs/insurance_agent/grounding/sg_protection_guidance/sources.yaml → team/README.md
- `Days without recorded cover tile` --semantically_similar_to--> `days_uncovered masks a lapsed motor policy`  [INFERRED] [semantically similar]
  docs/artefacts/Parrot UIUX refinement/uploads/parrot-design-evaluation.html → packs/README.md
- `One cell, one field` --semantically_similar_to--> `A field name is three things at once`  [INFERRED] [semantically similar]
  corpus/templates/policy_schedule.html → docs/PACK_AUTHORING.md
- `_Answering` --uses--> `HybridRetriever`  [INFERRED]
  api/routes.py → core/retrieve/hybrid.py
- `Asks` --uses--> `HybridRetriever`  [INFERRED]
  eval/harness.py → core/retrieve/hybrid.py

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
- **Household scoping: from a printed name to a scoped answer** — docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_people, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_person_aliases, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_facts_subject, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_three_buckets, docs_adr_0013_a_question_is_understood_before_it_is_searched_possessive_relations_scope, docs_adr_0015_a_name_scopes_and_a_grandparent_is_not_a_parent_a_question_naming_exactly_one_person_is_theirs, docs_adr_0015_a_name_scopes_and_a_grandparent_is_not_a_parent_grandparent_is_a_relation_nobody_can_hold, docs_adr_0011_the_household_is_people_and_aliases_and_the_owner_is_one_of_them_resolved_person_chip [INFERRED 0.85]
- **The boundary: it abstains, it cites, and it never acts** — docs_pack_authoring_guardrails, docs_demo_run_sheet_the_abstention, docs_demo_run_sheet_the_refusal_to_act, docs_demo_run_sheet_the_source_chip, docs_adr_0007_the_graph_ships_before_retrieval_and_before_a_checkpoint_table_adr_0007 [INFERRED 0.85]
- **Module manifests sharing the reads/writes/runs/surfaces contract** — modules__template_module_module_template, modules_advice_module_advice, modules_alert_module_alert, modules_reminder_module_reminder [INFERRED 0.95]
- **The 9x/4x protection rule of thumb and the published sources a person approved it from** — packs_insurance_agent_grounding_sg_protection_guidance_moneysense_bfpg_faq_protection_rule_of_thumb, packs_insurance_agent_grounding_sg_protection_guidance_moneysense_bfpg_faq_consumer_faqs, packs_insurance_agent_grounding_sg_protection_guidance_moneysense_bfpg_starting_a_family_starting_a_family_guide, packs_insurance_agent_grounding_sg_protection_guidance_moneysense_basic_financial_planning_basic_financial_planning_guide, packs_insurance_agent_grounding_sg_protection_guidance_lia_protection_gap_study_protection_gap_study_2022, packs_insurance_agent_pack_death_tpd_income_multiple, packs_insurance_agent_pack_ci_income_multiple [INFERRED 0.95]

## Communities (665 total, 444 thin omitted)

### Community 0 - "ModelUnavailable"
Cohesion: 0.11
Nodes (4): IndexReport, ModelUnavailable, uses_task_prompts(), test_a_model_that_dies_before_any_sentence_abstains()

### Community 1 - "HybridRetriever"
Cohesion: 0.10
Nodes (16): hybrid_score(), HybridRetriever, identifiers(), prints(), FakeConn, FakeCursor, FakeOllama, _row() (+8 more)

### Community 2 - "test_advice_graph.py"
Cohesion: 0.07
Nodes (39): AdviceCard, AdviceWithheld, _closes(), Subject, advised_pack(), build(), Consents, Household (+31 more)

### Community 3 - "ScriptedOllama"
Cohesion: 0.06
Nodes (62): AnswerGraph, Finished, Reading, Sentence, Holding, Scoped, Generated, test_a_mislabelled_figure_through_the_graph_is_dropped() (+54 more)

### Community 4 - "validate"
Cohesion: 0.09
Nodes (24): _as_date(), _fields(), _known_doc_types(), _known_fields(), main(), _pages(), validate(), _wide_format() (+16 more)

### Community 5 - "advice/__init__.py"
Cohesion: 0.07
Nodes (37): Advice, FactInput, RuleInput, _Value, _ambiguous(), _band(), _band_label(), _compare_market() (+29 more)

### Community 6 - "Advice shape death_tpd_cover (gap calculator)"
Cohesion: 0.13
Nodes (16): CareShield Life monthly payouts on severe disability and the ADL claim criteria, DPS sum assured $70,000 (age 21-60) and $55,000 (age 60-65) from 1 April 2021, Critical illness protection gap (74%, S$579 billion, PGS 2022), Mortality protection gap (21%, S$373 billion, PGS 2022), Insurance advice consent gate (consent_version 1.0.0), advice_decline guardrail message, Advice shape ci_cover (gap calculator), Grounding value key ci_income_multiple (+8 more)

### Community 7 - "test_advice_module.py"
Cohesion: 0.13
Nodes (46): assert_nothing_negative(), basis(), fact(), _facts_tuple(), figures_of(), _gap_basis(), _held(), _held_ward() (+38 more)

### Community 8 - "api.ts"
Cohesion: 0.06
Nodes (48): metadata, DocumentPage(), metadata, AdviceConsentSection(), Load, STATUS, ADR-0016, OwnerForm() (+40 more)

### Community 9 - "test_ingest_pipeline.py"
Cohesion: 0.09
Nodes (33): extract(), FakeOllama, insurance(), iras(), _page_of_examples(), _reply_of_examples(), test_a_date_that_cannot_be_read_still_quarantines(), test_a_document_is_titled_by_the_string_fields_its_pack_declares() (+25 more)

### Community 10 - "test_grounding_index.py"
Cohesion: 0.09
Nodes (21): _Connected, _extracted(), FakeConn, FakeCursor, _installed(), _review_env(), _script_env(), _source() (+13 more)

### Community 11 - "tasks.py"
Cohesion: 0.18
Nodes (12): digest_of_document(), ingest(), register(), retry_one(), retry_quarantine(), _run_alerts(), _run_ingest(), _run_reminders() (+4 more)

### Community 12 - "FolderAdapter"
Cohesion: 0.08
Nodes (22): CaptureAdapter, IngestJob, sniff_mime(), FolderAdapter, FolderSettings, _Pending, _Registered, FolderCapture (+14 more)

### Community 13 - "test_telegram_capture.py"
Cohesion: 0.09
Nodes (25): TelegramSettings, TelegramUnavailable, Registrar, build(), FakeRegistrar, FakeTelegram, photo_update(), test_a_chat_outside_the_allow_list_is_ignored() (+17 more)

### Community 14 - "FakeConn"
Cohesion: 0.09
Nodes (19): conn(), FakeConn, obligation(), overdue_row(), pack_row(), test_a_core_reminder_still_reaches_today_when_its_old_pack_is_off(), test_a_disabled_pack_does_not_reach_the_nightly_sweep(), test_a_disabled_pack_stops_its_reminders() (+11 more)

### Community 15 - "InstalledPack"
Cohesion: 0.04
Nodes (41): AdviceShape, AdviceLog, AdviceRecord, Adviser, Calculation, ConsentBook, Input, kind_of() (+33 more)

### Community 16 - "bench_runtime.py"
Cohesion: 0.08
Nodes (20): BenchmarkUnavailable, coresident_mib(), Device, digest(), filler(), generate(), gib(), idle_baseline() (+12 more)

### Community 17 - "vault.py"
Cohesion: 0.07
Nodes (15): _columns(), correct(), Corrected, CorrectionRejected, UnknownFact, _as_document(), declared_type(), document() (+7 more)

### Community 18 - "support.js"
Cohesion: 0.09
Nodes (22): cdnScriptFor(), compileTemplate(), createExternalModules(), createHelmetManager(), createPseudoSheet(), createRuntime(), createStreamTracker(), encodeCamelAttrs() (+14 more)

### Community 19 - "schedule.py"
Cohesion: 0.21
Nodes (5): build(), beat_schedule(), cron_expressions(), crontab_from(), manifest()

### Community 20 - "ingest/extract.py"
Cohesion: 0.08
Nodes (22): FieldSpec, _coerce(), _date_renderings(), decode_schema(), _drop_format(), ExtractedFact, Extraction, find_page() (+14 more)

### Community 21 - "test_grounding_values.py"
Cohesion: 0.14
Nodes (30): number_tokens(), parse_value(), _dropped(), _log_values(), _run(), test_a_money_value_with_a_currency_marker_is_kept(), test_a_multiple_is_kept_in_the_forms_it_is_written(), test_a_number_is_kept_when_one_of_its_occurrences_fits_the_unit() (+22 more)

### Community 22 - "reminder/__init__.py"
Cohesion: 0.09
Nodes (11): already_said(), close(), current_lead(), Due, next_window(), Overdue, snooze(), sweep() (+3 more)

### Community 23 - "Passage"
Cohesion: 0.06
Nodes (22): HouseholdConsents, HouseholdAdviceLog, _pack_for(), DenseRetriever, NoReranker, precheck(), holdings(), HouseholdInventory (+14 more)

### Community 24 - "TelegramAdapter"
Cohesion: 0.08
Nodes (7): _attachment(), _pixels(), _status_reason(), TelegramAdapter, _write_local_copy(), attribution(), TelegramCapture

### Community 25 - "SentenceScanner"
Cohesion: 0.10
Nodes (13): SentenceScanner, drip(), test_a_backslash_before_a_quote_is_handled(), test_a_brace_inside_a_sentence_does_not_end_it(), test_a_sentence_is_released_before_the_rest_has_been_written(), test_a_sentence_that_is_not_an_object_is_skipped_rather_than_crashing(), test_a_truncated_stream_keeps_the_sentences_that_did_arrive(), test_an_answer_with_no_sentences_yields_nothing_and_keeps_its_missing() (+5 more)

### Community 26 - "household.py"
Cohesion: 0.10
Nodes (19): add_person(), attribute(), classify_prompt(), confirm(), dismiss(), link_telegram(), owner(), owner_aliases() (+11 more)

### Community 27 - "ParsedPage"
Cohesion: 0.12
Nodes (16): chunk_pages(), _clean(), _lines(), _page_chunks(), _pieces(), classification_sample(), ParsedPage, PlainTextParser (+8 more)

### Community 28 - "test_lifecycle.py"
Cohesion: 0.06
Nodes (31): Lifecycle, _client(), _eventually(), _launcher(), quiet_engine(), Screens, _supervise(), test_a_browser_cannot_reach_the_engine_directly_even_with_the_header() (+23 more)

### Community 29 - "score.py"
Cohesion: 0.09
Nodes (22): cites(), _contains(), declined_in_prose(), doc_stem(), grade(), held_back(), inventory_only(), Judge (+14 more)

### Community 30 - "_household_scope"
Cohesion: 0.09
Nodes (20): _household_scope(), test_a_grandparent_nobody_holds_is_an_unknown_relation_not_the_fathers_policy(), test_a_grandparent_recorded_under_that_name_is_who_the_question_means(), test_a_name_that_is_not_exactly_one_person_scopes_nothing(), test_a_person_nobody_has_confirmed_is_not_named(), test_a_question_naming_one_other_member_is_scoped_to_them(), test_the_owner_asking_about_themselves_by_name_is_scoped_to_the_owner(), test_whose_asks_whose_when_a_member_is_named_without_a_possessive() (+12 more)

### Community 31 - ".load"
Cohesion: 0.05
Nodes (41): create_app(), ModelWarmth, warm_models(), _chat_ids(), ConfigurationError, _flag(), _folder(), local_url() (+33 more)

### Community 32 - "test_pages.py"
Cohesion: 0.09
Nodes (19): page_count(), PageUnavailable, _pdfium(), render_page(), RendererUnavailable, _size(), test_a_damaged_pdf_is_a_sentence_not_a_traceback(), test_a_file_that_is_not_a_document_says_which_kind_it_is() (+11 more)

### Community 33 - "parse.py"
Cohesion: 0.11
Nodes (12): Block, DoclingParser, _kind(), _pages_from(), Parser, _table_text(), _cell(), _on_page() (+4 more)

### Community 34 - "test_eval_generate.py"
Cohesion: 0.06
Nodes (26): _ambiguous(), choose(), Generated, hand_written(), main(), on_file(), pool(), write_lane() (+18 more)

### Community 35 - "test_modules.py"
Cohesion: 0.14
Nodes (19): FakeConn, obligation_row(), srs_row(), test_a_dry_run_records_nothing(), test_a_firing_older_than_the_debounce_window_fires_again(), test_a_metric_no_query_defines_cannot_fire(), test_a_recent_firing_is_debounced(), test_a_sum_is_per_person_and_cites_only_that_persons_receipts() (+11 more)

### Community 36 - "Measured"
Cohesion: 0.22
Nodes (8): _day(), Measured, _number(), register_cpf_contributions_ytd(), register_days_uncovered(), register_donations_ytd(), register_srs_contributions_ytd(), test_the_register_metrics_mirror_the_modules_queries()

### Community 37 - "extract_values"
Cohesion: 0.13
Nodes (18): ValueKey, SourceText, _check(), extract_values(), ExtractedValue, _prompt(), _schema(), _long_text() (+10 more)

### Community 39 - "test_api.py"
Cohesion: 0.11
Nodes (17): advising(), client(), graph(), _padded(), streaming(), test_a_turn_can_only_be_the_person_or_parrot(), test_an_advised_answer_is_committed_once(), test_ask_requires_a_question() (+9 more)

### Community 40 - "alert/__init__.py"
Cohesion: 0.16
Nodes (11): Alert, cpf_contributions_ytd(), days_uncovered(), _debounced(), donations_ytd(), Measurement, _per_subject(), srs_contributions_ytd() (+3 more)

### Community 41 - "retrieve.py"
Cohesion: 0.17
Nodes (10): Connection, load_matrix(), pack(), unpack(), _fts_query(), fuse(), hydrate(), keyword_search() (+2 more)

### Community 42 - "rows_for"
Cohesion: 0.12
Nodes (21): a_citation(), rows_for(), sse(), StreamingGraph, test_a_citation_says_whether_it_is_a_page_or_a_document_on_file(), test_a_declined_request_for_advice_is_the_whole_stream(), test_a_failure_after_the_stream_started_arrives_as_an_event(), test_a_finished_answer_says_on_the_wire_when_the_pages_did_not_answer_the_rest() (+13 more)

### Community 43 - "test_household.py"
Cohesion: 0.13
Nodes (17): scope_to(), conn(), _conn_returning(), _passage(), test_a_document_naming_the_owner_and_somebody_else_is_kept(), test_a_document_with_no_subject_belongs_to_everybody(), test_a_household_with_no_owner_scopes_nothing(), test_a_member_can_be_placed_but_the_owner_cannot() (+9 more)

### Community 44 - "pytest"
Cohesion: 0.10
Nodes (14): register_document(), conn(), database_url(), test_a_document_must_arrive_with_a_name(), test_a_new_document_is_inserted(), test_an_empty_payload_is_refused(), test_different_bytes_are_different_documents(), test_the_same_bytes_update_in_place_and_do_not_insert_a_second_row() (+6 more)

### Community 45 - "test_eval_modules.py"
Cohesion: 0.14
Nodes (14): Obligation, obligation_precision(), score_obligations(), Verdict, Config, _obligation(), test_a_calendar_deadline_is_checked_against_the_catalogue_and_counted_apart(), test_a_date_the_document_does_not_print_is_a_false_obligation() (+6 more)

### Community 46 - "test_tax_pack.py"
Cohesion: 0.18
Nodes (12): _basis(), _latest(), _matched(), _published(), _register(), _shape(), test_a_tax_question_reaches_the_tax_shape_and_insurance_keeps_its_own(), test_no_saving_is_estimated_without_a_notice_of_assessment() (+4 more)

### Community 47 - "walk"
Cohesion: 0.30
Nodes (15): collectProps(), compileAttr(), contentKey(), cssToObj(), hostPositionStyle(), isDeckMountTag(), kebabToCamel(), walk() (+7 more)

### Community 48 - "models.py"
Cohesion: 0.14
Nodes (18): CloseRequest, CorrectionResponse, EnabledRequest, ForgottenDocument, HouseholdResponse, ObligationChanged, PacksResponse, PendingName (+10 more)

### Community 49 - "report.py"
Cohesion: 0.15
Nodes (12): _cell(), collect(), main(), _overall(), _paragraph(), Provenance, render(), _row() (+4 more)

### Community 50 - "compilerOptions"
Cohesion: 0.07
Nodes (28): ./*, dom, dom.iterable, esnext, next-env.d.ts, .next/types/**/*.ts, node_modules, **/*.ts (+20 more)

### Community 51 - "Domain packs — start here"
Cohesion: 0.11
Nodes (18): 1. What we are building, in one paragraph, 2. What a domain pack actually is, 3. The one thing that matters most, 4. What you do, step by step, 5. How your output lets Desmond continue, 6. Persona and guardrails, 6b. Answering: words, categories, exclusions, 6c. Advice: when a pack answers "is it enough?" (+10 more)

### Community 52 - "registry.py"
Cohesion: 0.11
Nodes (19): installed_modules(), installed_packs(), enabled_module_ids(), install(), install_best_effort(), Installed, _module_row(), modules() (+11 more)

### Community 53 - "test_grounding.py"
Cohesion: 0.18
Nodes (12): GroundingCorpus, corpus_dir(), CorpusInvalid, load_corpus(), _document(), _installed(), test_a_missing_recorded_file_is_refused(), test_a_pack_with_no_corpus_gives_none_and_empty() (+4 more)

### Community 54 - "Any"
Cohesion: 0.11
Nodes (9): document_row(), fact_row(), test_a_citation_that_resolves_to_nothing_still_says_what_it_said(), test_a_core_document_stays_enabled_when_every_pack_is_off(), test_an_alerts_citation_carries_the_document_it_opens(), test_one_document_is_shown_even_when_its_pack_is_off(), test_today_is_ordered_overdue_then_alerts_then_reminders(), test_vault_lists_documents_with_their_facts() (+1 more)

### Community 55 - "cli.py"
Cohesion: 0.23
Nodes (11): build_parser(), _client(), cmd_add(), cmd_docs(), cmd_doctor(), cmd_init(), cmd_search(), cmd_stats() (+3 more)

### Community 56 - "run.py"
Cohesion: 0.12
Nodes (18): _chosen(), _corpus_sha(), _counts(), _facts(), _Formatter, _git_sha(), _indexed(), main() (+10 more)

### Community 57 - "PARROT Interface Design Pack"
Cohesion: 0.20
Nodes (5): Gate checks beyond citation: printed numbers, exclusion-only claims, sentence cap, Query flow and grounding, Information architecture: Today, Ask, Vault, Capture and Packs, PARROT Interface Design Pack, Suggestions come from this week's ingest

### Community 58 - "packs.py"
Cohesion: 0.14
Nodes (8): DocumentTypeSpec, Classification, classify(), _prompt(), _schema(), document_types(), _load_one(), PackUnavailable

### Community 59 - "ModuleAdviser"
Cohesion: 0.12
Nodes (16): _is_an_adviser(), ModuleAdviser, advised_pack(), db(), _document(), FakeConn, FakeCursor, _source() (+8 more)

### Community 60 - "PackManifest"
Cohesion: 0.14
Nodes (7): PackManifest, test_a_grounding_corpus_travels_inside_its_pack(), test_a_pack_cannot_opt_out_of_never_acts(), test_a_shape_closed_by_an_unknown_category_is_rejected(), test_advice_naming_an_undeclared_catalogue_field_is_rejected_against_the_catalogue(), test_every_grounding_corpus_declares_its_provenance(), test_template_pack_validates()

### Community 61 - "values.py"
Cohesion: 0.11
Nodes (16): collapse(), _cuts_a_number(), _groups(), _is_heading(), _pack(), printed_as(), printed_in(), split_sections() (+8 more)

### Community 62 - "item-row.tsx"
Cohesion: 0.16
Nodes (14): SourceChip(), SourcePanel(), stripTrailingPage(), ADR-0016, countdown(), detail(), figure(), ItemRow() (+6 more)

### Community 63 - "lock.ts"
Cohesion: 0.12
Nodes (24): GET(), grant(), POST(), metadata, UnlockPage(), compat, eslintConfig, Accepted (+16 more)

### Community 64 - "AlertConfig"
Cohesion: 0.15
Nodes (10): AlertConfig, alert_fpr(), AlertVerdict, score_alerts(), _triggered(), Fired, test_a_metric_with_no_register_equivalent_is_not_guessed_at(), test_an_alert_the_register_agrees_with_is_not_counted_against_the_module() (+2 more)

### Community 65 - "_as_event"
Cohesion: 0.10
Nodes (12): AbstentionEvent, AdviceCardEvent, AdviceFigure, ConsentRequiredEvent, DeclinedEvent, FinishedEvent, ReadingEvent, RefusalEvent (+4 more)

### Community 66 - "Getting Parrot ready (startup readiness screen)"
Cohesion: 0.22
Nodes (8): The VRAM budget, with headroom, Component states (nothing filed yet, could not read page 2, the local model is not running, nothing needs you today), Four readiness components: your documents, filing, screens, local model, Getting Parrot ready (startup readiness screen), Power menu: Lock, Restart Parrot, Shut down Parrot, Restarting Parrot (engine stops, a fresh engine starts, the page reconnects by itself), Parrot is off (terminal state page), Parrot is waiting for its database (Docker Desktop not running)

### Community 67 - "advice_consent.py"
Cohesion: 0.21
Nodes (7): current(), grant(), _latest(), NoOwner, _record(), status(), withdraw()

### Community 68 - "`api/` — the FastAPI application"
Cohesion: 0.17
Nodes (11): `api/` — the FastAPI application, Five properties worth knowing before you change anything, Rules, The surface, apply, Auto-Redirect to Today Once Ready, check, draw (+3 more)

### Community 69 - "pack"
Cohesion: 0.09
Nodes (26): Categories, Asked, categories_asked(), categorise(), glossary(), mentions(), _pattern(), reworded() (+18 more)

### Community 70 - "value_forms"
Cohesion: 0.22
Nodes (5): _as_date(), _as_number(), reference_for(), same_value(), value_forms()

### Community 71 - "devDependencies"
Cohesion: 0.10
Nodes (21): eslint, eslint-config-next, @eslint/eslintrc, postcss, tailwindcss, @tailwindcss/postcss, @types/node, @types/react (+13 more)

### Community 74 - "scope.py"
Cohesion: 0.18
Nodes (9): _decide(), _Decision, _name_word_owners(), named_in(), _names(), _names_a_member_impersonally(), _own_name_words(), relation_asked() (+1 more)

### Community 75 - "Citation chips are the trust surface"
Cohesion: 0.29
Nodes (5): Citation chips are the trust surface, Civic Register: order, clarity and institutional confidence, Kitchen Table: a little less household admin, a little more breathing room, The Reading Desk: understand it, open the source, see for yourself, PARROT - three interface directions (offline interactive evaluation, sample data only)

### Community 76 - "Claim"
Cohesion: 0.05
Nodes (56): Exclusions, check_advice(), check_content(), check_one(), Claim, _loose_numbers(), _normal(), _says() (+48 more)

### Community 77 - "Any"
Cohesion: 0.17
Nodes (10): by_subject(), db(), FakeCursor, load_register(), test_a_deductible_receipt_counts_in_its_own_year_only(), test_a_lapsed_policy_is_not_masked_by_another_that_still_runs(), test_cpf_is_this_years_payslips_per_employee(), test_donations_are_this_years_deductible_receipts_per_donor() (+2 more)

### Community 78 - "today/page.tsx"
Cohesion: 0.09
Nodes (20): createRegistry(), HouseholdPage(), AppLayout(), isUrgent(), metadata, summary(), TodayPage(), metadata (+12 more)

### Community 80 - "preview.tsx"
Cohesion: 0.11
Nodes (16): metadata, answers, DesignPreview(), Direction, directions, Item, items, Outcome (+8 more)

### Community 81 - "ingest/quarantine.py"
Cohesion: 0.11
Nodes (13): blocked_reasons(), forget(), page_images(), QuarantinedDocument, queue(), Recovery, recovery_rate(), retry() (+5 more)

### Community 83 - "Answer"
Cohesion: 0.07
Nodes (35): Answer, Cited, Expected, load_set(), MalformedQuestion, Question, Fails, FakeGraph (+27 more)

### Community 85 - "paperbrain/chunk.py"
Cohesion: 0.43
Nodes (4): Chunk, chunk_pages(), clean(), _split_page()

### Community 86 - "review_grounding_values.py"
Cohesion: 0.20
Nodes (7): approve(), pending(), PendingValue, reject(), _block(), main(), test_list_block_shows_id_pack_key_value_source_and_an_indented_passage()

### Community 88 - "ModuleManifest"
Cohesion: 0.16
Nodes (6): ModuleManifest, InstalledModule, manifest(), ModuleUnavailable, test_a_module_may_read_grounding_values(), test_advice_is_a_module()

### Community 89 - "components.json"
Cohesion: 0.11
Nodes (17): aliases, components, hooks, lib, ui, utils, iconLibrary, rsc (+9 more)

### Community 90 - "routes.py"
Cohesion: 0.13
Nodes (11): AskRequest, ModuleSummary, PackSummary, PersonModel, VaultFact, _as_module_summary(), _as_pack_summary(), _as_person() (+3 more)

### Community 91 - "18 · The reranker runs in-process, because Ollama cannot serve a cross-encoder"
Cohesion: 0.14
Nodes (10): 11. The household is people and aliases, and the owner is one of them, Consequences, Context, Decision, 18 · The reranker runs in-process, because Ollama cannot serve a cross-encoder, Alternatives considered, Consequences, Context (+2 more)

### Community 92 - "contracts.py"
Cohesion: 0.16
Nodes (12): Answering, Category, Grounding, GroundingDocument, Guardrails, ModuleTrigger, Persona, Registrations (+4 more)

### Community 93 - "boot"
Cohesion: 0.22
Nodes (10): boot(), dcNameFromPath(), getReactDOM(), parseDataProps(), parseDcDocument(), parseDcText(), rootNameForDocument(), safeDecode() (+2 more)

### Community 94 - "test_eval_report.py"
Cohesion: 0.13
Nodes (18): extraction_by_type(), extraction_f1(), FactRow, _outcomes(), _totals(), unjoined(), _rendered(), _scores() (+10 more)

### Community 95 - "The Lim Household, Tampines"
Cohesion: 0.22
Nodes (9): loan_agreement Document Type, payslip Document Type, The Lim Household, Tampines, Rule of 78 Rebate and the 20 Per Cent Early Settlement Penalty, Motor Vehicle Hire Purchase Agreement Template, Republic of Xinkapow, the Invented Jurisdiction, Residential Housing Loan Facility Letter Template, 36-Month Lock-In, Prepayment Penalty and Subsidy Clawback (+1 more)

### Community 96 - "Starting Parrot"
Cohesion: 0.12
Nodes (17): Access and privacy, Asking a question, Dropping a document in, First test machine: Christian's Legion, Hardware qualification, Local validation notes, 2026-09-11, Moving a corpus between machines, Quarantine, and the second pass (+9 more)

### Community 98 - "test_contracts.py"
Cohesion: 0.09
Nodes (36): _advised(), _checked(), _compare_without_an_ordering(), _compares_an_undeclared_field(), _drop_held(), _drop_rules(), _duplicate_shape(), _fact() (+28 more)

### Community 99 - "Core Document Catalogue (ADR 0017)"
Cohesion: 0.15
Nodes (13): The Core Answering Layer, benefit_illustration Document Type, birth_certificate Document Type, claim_letter Document Type, cpf_statement Document Type, Core Document Catalogue (ADR 0017), donation_receipt Document Type, identity_card Document Type (+5 more)

### Community 100 - "Notebook prompts — the four full policies for Marcus Lim"
Cohesion: 0.13
Nodes (13): After generating, Before you generate: the register row, Notebook prompt — a full-length insurance policy for Marcus Lim, Optional block — the appendicitis demonstration, The prompt, What this prompt cannot fix, After all four, Notebook prompts — the four full policies for Marcus Lim (+5 more)

### Community 101 - "is_first_person"
Cohesion: 0.33
Nodes (4): is_first_person(), test_a_named_household_member_wins_over_the_pronoun(), test_first_person_questions_are_recognised(), test_questions_about_other_people_are_not_scoped()

### Community 102 - "PARROT Architecture Review"
Cohesion: 0.18
Nodes (11): Chunks follow the document's structure (Docling heading labels), PackManifest.answering, PARROT Architecture Review, The capability module contract (Reminder, Alert, Tracker), Document pipeline, The domain pack manifest, The expansion model: two axes, not one list, The golden set: answerable, hard negatives, adversarial (+3 more)

### Community 104 - "test_rerank.py"
Cohesion: 0.08
Nodes (21): CrossEncoderReranker, device_name(), load(), passage_text(), relevance(), score_pairs(), _warn_once(), FakeEncoded (+13 more)

### Community 105 - "Roadmap"
Cohesion: 0.20
Nodes (8): Explicitly not doing, Phase 1 — Retrieval (done), Phase 2 — Facts, Phase 3 — Reminders, Phase 4 — Agent, Roadmap, Sample supermarket tax invoice, Sample school term notice

### Community 108 - "ingest.py"
Cohesion: 0.18
Nodes (9): cmd_ingest(), Config, discover(), embed_chunks(), guess_date(), guess_type(), ingest_file(), IngestResult (+1 more)

### Community 109 - "Tax and Reliefs — contract changes this pack needs"
Cohesion: 0.40
Nodes (4): 1. A deduction multiplier on `estimate_saving`, 2. Limiting a fact input to one year, Not a contract change: parent relief, Tax and Reliefs — contract changes this pack needs

### Community 110 - "Reminder, Alert and Tracker Registers"
Cohesion: 0.24
Nodes (8): filing_deadline Reminder, passport Document Type, passport_expiry Reminder, policy_expiry Reminder, policy_schedule Document Type, Reminder, Alert and Tracker Registers, renewal_notice Document Type, srs_contribution_cutoff Reminder

### Community 111 - "Settings"
Cohesion: 0.08
Nodes (21): capture_check(), Check, collect_checks(), database_check(), interface_check(), model_check(), redis_check(), reranker_check() (+13 more)

### Community 112 - "Module manifest template"
Cohesion: 0.14
Nodes (10): Days without recorded cover tile, Module manifest template, advice module manifest, alert module manifest, reminder module manifest, example_pack template manifest, example_room advice shape, Pack advice block (+2 more)

### Community 113 - "paperbrain/extract.py"
Cohesion: 0.36
Nodes (9): extract(), extract_docx(), extract_eml(), extract_image(), extract_pdf(), extract_text_file(), Extracted, _ocr_image() (+1 more)

### Community 114 - "§5 · Evaluation and results"
Cohesion: 0.17
Nodes (12): 5.10 What run 3 must add, 5.1 The claim, 5.2 What was measured, 5.3 The three-run spine, 5.4 Retrieval: what the two changes bought, 5.5 Abstention: the finding, 5.6 Extraction, by document type, 5.7 The two module metrics, and the lesson in them (+4 more)

### Community 115 - "tokens/page.tsx"
Cohesion: 0.09
Nodes (12): Motion(), ROWS, INKS, metadata, RADII, SCALE, SECTIONS, SPACE (+4 more)

### Community 116 - "Try PARROT"
Cohesion: 0.13
Nodes (15): 1 · Install five things, 2 · Download the AI models, 3 · Get the code and set it up, 4 · Put some documents in, 5 · Run it, 6 · Use it, Ask — a question about your own documents, If something goes wrong (+7 more)

### Community 117 - "Integration review"
Cohesion: 0.29
Nodes (6): How to give the feedback, Integration review, Never, Read first, Reviewing a pull request, The weekly pass — ninety minutes, protected

### Community 118 - "Ollama"
Cohesion: 0.06
Nodes (6): render(), Dispatcher, Send, broker_available(), dispatcher_for(), Ollama

### Community 119 - "adr/README.md"
Cohesion: 0.19
Nodes (7): 5. The watched folder is polled for stability, not subscribed to for events, Consequences, Context, Decision, Architecture decision records, Index, Writing one

### Community 121 - "test_worker_queue.py"
Cohesion: 0.06
Nodes (26): sha256(), Inline, Queued, Intake, Registration, bytes_for(), index_folder(), SourceMissing (+18 more)

### Community 122 - "Retention and erasure policy"
Cohesion: 0.20
Nodes (9): Open questions, Policy, Retention and erasure policy, Retention periods, Scope and legal frame, The erasure path: what `DELETE FROM documents` reaches, The finding to read first, What has to be built (+1 more)

### Community 125 - "Running the evaluation harness"
Cohesion: 0.18
Nodes (10): Commands, Done, Never overwrite a result, One variable per run, Read first, Reporting a change, Running the evaluation harness, Staying in lane (+2 more)

### Community 127 - "Project PARROT — team split"
Cohesion: 0.14
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 129 - "4. Writing `pack.yaml`"
Cohesion: 0.12
Nodes (15): 1. What a pack is, 2. The one thing to understand before you start, 3. The workflow, 4. Writing `pack.yaml`, 5. The grounding corpus, 6. Definition of done, 7. Where to ask, Authoring a domain pack (+7 more)

### Community 131 - "Filling the corpus register"
Cohesion: 0.20
Nodes (9): Batches, Column headings are not yours to choose, Done, per batch, Filling the corpus register, Read first, The adversarial half, from week 7, The order, which is not the obvious one, The rule that cannot bend (+1 more)

### Community 132 - "Writing a governance artefact"
Cohesion: 0.20
Nodes (9): Adversarial Set C, Done, per artefact, Never, Read first, The autonomy statement, The governing rule, The six, Where governance touches the code (+1 more)

### Community 133 - "Changelog"
Cohesion: 0.50
Nodes (3): Changelog, W1 · 2–8 Sep 2026, W2 · 9–15 Sep 2026

### Community 134 - "Working agreement for coding agents"
Cohesion: 0.29
Nodes (7): Before you read files at random, Definition of done, Hard rules, Stack — do not substitute, Style, What to do when you are unsure, Working agreement for coding agents

### Community 135 - "igd-capstone-2026"
Cohesion: 0.20
Nodes (10): Authoring a pack, igd-capstone-2026, `main` is not protected, Quick start, The stack, in one table, The three rules that matter, What it is, Where things live (+2 more)

### Community 136 - "Policy schedule HTML template"
Cohesion: 0.40
Nodes (5): b1-0001 Private Car Insurance Policy Schedule, b1-0002 HomeShelter Contents Policy Schedule, b1-0003 Hospital Income Protection Plan Schedule, Policy schedule HTML template, SYNTHETIC DOCUMENT footer

### Community 139 - "PaperBrain"
Cohesion: 0.25
Nodes (7): How retrieval works, Layout, PaperBrain, Privacy, Setup, Use, What it handles

### Community 141 - "answer.tsx"
Cohesion: 0.07
Nodes (38): lastQuestion(), ParrotEvent, parseRecord(), POST(), priorTurns(), readEvents(), ADR-0016, upstreamDetail() (+30 more)

### Community 143 - "_Answering"
Cohesion: 0.13
Nodes (7): ConfirmNameRequest, ConsentRequest, CorrectionRequest, ErrorEvent, OwnerRequest, PlaceRequest, _Answering

### Community 144 - "settings"
Cohesion: 0.11
Nodes (26): client_for(), consent(), ConsentConn, filed_document(), inbox(), settings(), test_a_document_still_in_the_inbox_is_not_forgotten(), test_a_document_whose_file_left_the_inbox_is_409_not_500() (+18 more)

### Community 145 - "Set C: adversarial"
Cohesion: 0.33
Nodes (5): Assumptions to recheck before the run, How it is scored, Planted documents (for Desmond), Set C: adversarial, The line format

### Community 146 - "PrivateCare Policy Wording Template"
Cohesion: 0.20
Nodes (8): Policy Schedule Template, PrivateCare Policy Wording Template, Synthetic document footer notice, Lionhead Life Assurance, ProtectPlus Life With Riders Template, Riders attached to this policy, Renewal Notice Template, Republic of Xinkapow

### Community 148 - "dependencies"
Cohesion: 0.12
Nodes (17): ai, @ai-sdk/react, class-variance-authority, clsx, lucide-react, next, next-themes, tailwind-merge (+9 more)

### Community 150 - "app/layout.tsx"
Cohesion: 0.25
Nodes (6): figtree, jetbrains, metadata, outfit, viewport, ThemeProvider()

### Community 151 - "Household canon"
Cohesion: 0.14
Nodes (14): Address, Employment, Household canon, Issuers for the documents that have no `insurer` field, Life events that documents must reflect, People, Policies, The family tree, and why three of them are not called Lim (+6 more)

### Community 152 - "Authoring a domain pack"
Cohesion: 0.25
Nodes (7): Authoring a domain pack, Before anything else, Done, Grounding, when the pack needs it, Never, The rule that governs everything, Work in this order, stopping for the author at each step

### Community 154 - "eval/modules.py"
Cohesion: 0.12
Nodes (11): main(), _mark(), measure(), ModuleMetrics, obligations(), obligations_possible(), _paragraph(), render() (+3 more)

### Community 155 - "DesignPreview evaluation harness"
Cohesion: 0.22
Nodes (7): Starting Parrot, 3 of 5 ready, Parrot Startup Skeleton Screen, Civic Register direction, DesignPreview evaluation harness, Kitchen Table direction, The Reading Desk direction, Pack guardrails (must_cite, abstain_below, never_acts)

### Community 156 - "DatabaseUnavailable"
Cohesion: 0.08
Nodes (17): enabled_pack_ids(), enabled_packs(), connect(), DatabaseUnavailable, _ask(), main(), main(), _read_rows() (+9 more)

### Community 158 - "Siew — Lane C · Governance and assurance"
Cohesion: 0.29
Nodes (7): Adversarial Set C, Done, per artefact, Siew — Lane C · Governance and assurance, Starter prompt for your coding agent, The autonomy statement, The six artefacts, Where governance touches the code

### Community 159 - "Writing an ADR"
Cohesion: 0.29
Nodes (6): Format, Read first, Rules, What does not, What earns an ADR, Writing an ADR

### Community 162 - "AskResponse"
Cohesion: 0.29
Nodes (3): AskResponse, Claim, _as_response()

### Community 164 - "The demonstration run sheet"
Cohesion: 0.14
Nodes (14): 1 · Today — 0:00, fifty seconds, 2 · The source chip — 0:50, forty seconds, 3 · Drop a document in — 1:30, seventy seconds, 4 · Ask, and get an answer — 2:40, eighty seconds, 5 · Vault — 4:00, fifty seconds, 6 · The abstention — 4:50, one minute, 7 · The refusal to act — 5:50, forty seconds, 8 · Switch a pack off — 6:30, one minute (+6 more)

### Community 165 - "Evaluation"
Cohesion: 0.17
Nodes (11): Evaluation, Extraction F1 by document type, Generating a lane's dozen, Ground truth comes free, How much of a delta is a delta, Metrics and targets, Running the harness, The honesty check (+3 more)

### Community 166 - "getReact"
Cohesion: 0.25
Nodes (8): createComponentFactory(), evalDcLogic(), getReact(), renderDeckKids(), walkText(), warnUnresolved(), react, react

### Community 168 - "(app)/layout.tsx"
Cohesion: 0.10
Nodes (18): LockButton(), SURFACES, TabBar(), Tabs(), Action, CONFIRM, ITEMS, PowerMenu() (+10 more)

### Community 170 - "User stories and acceptance criteria"
Cohesion: 0.14
Nodes (12): 1. How to read a criterion, 2. Rachel · Reminder module · Today, 3. Marcus · retrieval core · Ask, 4. Marcus and Rachel · capture · Vault, 5. Marcus · Alert module · Today, 6. The household ledger · Tracker · specification only, 7. Open questions for review, 8. The criteria as a checklist (+4 more)

### Community 171 - "DocumentCatalog"
Cohesion: 0.10
Nodes (13): DocumentCatalog, _class_name(), _docstring(), _field_line(), _header(), load(), load_catalog(), main() (+5 more)

### Community 172 - "19 · A relevance floor on the reranker does not buy abstention, and the reason is not calibration"
Cohesion: 0.22
Nodes (8): 19 · A relevance floor on the reranker does not buy abstention, and the reason is not calibration, Alternatives considered, Consequences, Context, Decision, Revisit when, The measurement, Why it is not a calibration problem

### Community 174 - "Project skills"
Cohesion: 0.40
Nodes (4): Changing them, Project skills, Slash commands, Using them

### Community 175 - "pull_request_template.md"
Cohesion: 0.40
Nodes (4): Checks, Evaluation, Lane, What this changes

### Community 176 - "_today_items"
Cohesion: 0.21
Nodes (6): Source, TodayItem, _as_source(), _cite(), _link(), _today_items()

### Community 177 - "test_a_client_that_leaves_after_the_card_commits_one_record"
Cohesion: 0.24
Nodes (5): next_kind(), test_a_client_that_leaves_after_the_card_commits_one_record(), test_a_client_that_leaves_mid_explanation_still_commits_what_it_was_shown(), test_a_stream_closed_exactly_at_the_card_is_still_committed_by_the_api(), test_closing_the_graph_when_the_record_write_fails_rolls_back()

### Community 180 - "filesystem"
Cohesion: 0.50
Nodes (3): npx, filesystem, @modelcontextprotocol/server-filesystem

### Community 182 - "pipeline.py"
Cohesion: 0.07
Nodes (19): Chunk, fixed(), from_facts(), _label(), parse(), ParsedDocument, commit_both_lanes(), document_title() (+11 more)

### Community 183 - "Project PARROT — team split"
Cohesion: 0.15
Nodes (13): A · Integration and product owner — **Christian** *(builder)*, B · Retrieval and evaluation — **Yew Mun**, the data scientist *(builder)*, C · Governance and assurance — **Siew**, the data governance officer, D · Domain packs and interface — **Zee**, the commercial member *(builder)*, E · Corpus and adversarial testing — **Desmond**, the police officer, Everyone, regardless of lane, How the code gets written, Presentation split (+5 more)

### Community 184 - "Basic Financial Planning Guide"
Cohesion: 0.15
Nodes (12): Basic Financial Planning Guide, Basic Financial Planning Guide, Basic Financial Planning Guide For Entrants To The Workforce, Basic Financial Planning Guide for those nearing retirement, Basic Financial Planning Guide For Those With Dependents, Emergency funds, For those approaching retirement, For those new to the workforce (+4 more)

### Community 186 - "load_corpus.py"
Cohesion: 0.11
Nodes (7): find_browser_executable(), generate_documents(), documents_in(), main(), main(), report_hardware(), startup_gaps()

### Community 188 - "open_obligation"
Cohesion: 0.25
Nodes (6): open_obligation(), test_an_obligation_can_be_closed_as_done_or_dismissed(), test_an_obligation_cannot_be_closed_into_an_invented_state(), test_snooze_says_the_day_it_will_speak_again(), test_snooze_stamps_the_column_the_sweep_already_reads(), test_snoozing_inside_the_last_window_admits_there_is_nothing_after_it()

### Community 189 - "package.json"
Cohesion: 0.20
Nodes (9): name, private, scripts, build, dev, lint, start, typecheck (+1 more)

### Community 190 - "3. Comprehensive Document Suite: Policy Wordings & Loan Agreements"
Cohesion: 0.17
Nodes (10): 1. Ground Truth Parameters (Canonical Lim Household & Xinkapow), 3.1 Marcus's PrivateCare Hospital & Surgical Plan (`b2-0008.pdf`), 3.2 Dad's Hospital Income Protection Plan (`b2-0009.pdf`), 3.3 Crescent Bank Residential Housing Loan Facility Letter (`b2-0010.pdf`), 3.4 Crescent Bank Motor Vehicle Hire Purchase Agreement (`b2-0011.pdf`), 3.5 Marcus's Life Policy Schedule with Riders (`b2-0019.pdf`), 3. Comprehensive Document Suite: Policy Wordings & Loan Agreements, 4. How to Generate and Drop into `inbox/` (+2 more)

### Community 200 - "packs/page.tsx"
Cohesion: 0.20
Nodes (7): ADR-0017, metadata, PacksPage(), Toggle(), ModuleSummary, packs(), PackSummary

### Community 201 - "Provenance register for corpus sg_protection_guidance"
Cohesion: 0.18
Nodes (12): CareShield Life (CPF Board), Dependants Protection Scheme (CPF Board), CPF news release: higher DPS sum assured and premium rates from 1 April 2021, LIA Media Release: Protection Gap Study 2022, LIA 2022 Protection Gap Study Key Findings, Comparison of Private Hospital IPs (MOH, Jun 2026), Standard Integrated Shield Plans targeted at Ward Class B1 (MOH, Jun 2026), Consumer FAQs on the Basic Financial Planning Guide (+4 more)

### Community 205 - "Insurance and Coverage pack (insurance_agent)"
Cohesion: 0.20
Nodes (11): Category matcher (printed product_name against asked words, first rule wins), Exclusion detection (headings, claims, negations), insurance_agent guardrails (must_cite, abstain_below 0.45, never_acts, verdict_by_code), Insurance and Coverage pack (insurance_agent), insurance_agent persona (the household's insurance specialist), insurance_agent grounding binding (corpus sg_protection_guidance, top_k 6), Colloquial vocabulary mapping (kena warded, claimable, a&e, maid), iras_tax guardrails (must_cite, abstain_below 0.42, never_acts) (+3 more)

### Community 211 - "paperbrain/ask.py"
Cohesion: 0.43
Nodes (5): answer(), build_context(), format_sources(), cmd_ask(), Hit

### Community 213 - "test_correcting_a_field_keeps_what_it_used_to_say"
Cohesion: 0.33
Nodes (5): stored_fact(), test_a_corrected_field_stops_being_flagged(), test_a_date_field_takes_an_iso_date_and_says_so_when_it_does_not(), test_a_premium_that_is_not_a_number_is_refused_rather_than_stored_as_text(), test_correcting_a_field_keeps_what_it_used_to_say()

### Community 214 - "Comparison of Integrated Shield Plans"
Cohesion: 0.18
Nodes (10): Common reasons why insurers do not provide a Letter of Guarantee in specific cases, Common reasons why insurers may reject or not pay for claims, Comparison of Integrated Shield Plans, Comparison of lifetime premiums, Important Information, Letter of Guarantee, List of Integrated Shield Plans (IPs) and their targeted level of coverage, Medical Record Costs (+2 more)

### Community 215 - "Christian — task list"
Cohesion: 0.18
Nodes (11): Christian — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 216 - "Desmond — Lane E · Corpus and adversarial testing"
Cohesion: 0.18
Nodes (11): Desmond — Lane E · Corpus and adversarial testing, Done, per batch, Generating more documents: template, then notebook, Starter prompt for your coding agent, The one rule that changes everything: register first, The rule you cannot bend, The second half: adversarial testing, Volumes (+3 more)

### Community 217 - "Desmond — task list"
Cohesion: 0.18
Nodes (11): Desmond — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 218 - "Siew — task list"
Cohesion: 0.18
Nodes (11): Siew — task list, W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13 (+3 more)

### Community 219 - "Yew Mun — task list"
Cohesion: 0.18
Nodes (11): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W4 — due 2026-09-29, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20 (+3 more)

### Community 220 - "Graphify — the shared knowledge graph"
Cohesion: 0.20
Nodes (9): Graphify — the shared knowledge graph, Keeping it fresh, Merge conflicts, solved properly, Setup, once per clone, The hook leaves your tree dirty. Amend it into the commit you just made., Two kinds of extraction, and which needs what, Using it, What is committed, and what is not (+1 more)

### Community 221 - "First run"
Cohesion: 0.20
Nodes (10): 1 · Collaborators, 2 · Branch protection — deliberately not configured, 3 · Actions permissions, 4 · Project board, 5 · The Notion hub, First run, Send these on day one, Setting up a second machine (+2 more)

### Community 222 - "Understanding health insurance"
Cohesion: 0.20
Nodes (9): Assistance under MediFund, Basic health insurance coverage, Choosing your level of coverage, How MediSave fits in, If you have company health insurance, If you want more coverage, Types of health insurance plans, Understanding health insurance (+1 more)

### Community 224 - "Kitchen Table, resolved - for implementation"
Cohesion: 0.22
Nodes (6): The advise route intent returns the pack's advice_decline, Ask - Parrot does not act, Kitchen Table, resolved - for implementation, Screen set 1a-1o (Today, Ask, Vault, Packs, Unlock, dark, hero anatomies, handoff), Terracotta #B4462A as the brand accent, Type system: Outfit for names and UI, Figtree for prose, JetBrains Mono for anything measured

### Community 225 - "The household, and the word "my""
Cohesion: 0.22
Nodes (9): 1 · The failure this fixes, 2 · What already existed, 3 · Why a roster is not a setup form, 4 · The data model, 5 · Resolving "my" — three buckets, not two, 6 · Two safeguards, 7 · What this cost, and what it did not, 8 · What it enables, for §5 and §8 (+1 more)

### Community 226 - "2. Amended Gemini Prompts Bank (Xinkapow Yellow/Orange Cards with KFC Mascot)"
Cohesion: 0.22
Nodes (9): 2.1 Marcus Lim Jun Wei — Xinkapow National Identity Card (Front), 2.2 Marcus Lim Jun Wei — Xinkapow National Identity Card (Back), 2.3 Rachel Ng Hui Shan — Xinkapow National Identity Card (Front), 2.4 Rachel Ng Hui Shan — Xinkapow National Identity Card (Back), 2.5 Lim Ah Kow (Father) — Xinkapow Senior Citizen Identity Card, 2.6 Tan Mei Ling (Mother) — Xinkapow Senior Citizen Identity Card, 2.7 Lucas Lim Kai En — Xinkapow Digital Birth Certificate, 2.8 Rachel Ng Hui Shan — Xinkapow Passport (Data Page) (+1 more)

### Community 227 - "Zee — Lane D · Domain packs and interface"
Cohesion: 0.22
Nodes (9): Half one — domain packs (weeks 1 to 7), Half two — the interface (weeks 4 to 8), Read this first, Rules that apply to you specifically, The two halves of this lane, What "done" looks like, What you present, Your Claude Code skills (+1 more)

### Community 228 - "Zee — task list"
Cohesion: 0.22
Nodes (9): W10 — due 2026-11-10, W1 — due 2026-09-08, W2 — due 2026-09-15, W3 — due 2026-09-22, W5 — due 2026-10-06, W6 — due 2026-10-13, W7 — due 2026-10-20, W9 — due 2026-11-03 (+1 more)

### Community 229 - "Household canon"
Cohesion: 0.25
Nodes (7): Address, Employment, Household canon, Life events that documents must reflect, People, Policies, Vehicles

### Community 230 - "0001_init.sql"
Cohesion: 0.36
Nodes (7): chunks, documents, facts, modules, obligations, packs, traces

### Community 233 - "[...path]/route.ts"
Cohesion: 0.43
Nodes (7): ALLOWED, Context, DELETE(), forward(), GET(), PATCH(), POST()

### Community 234 - "Contributing"
Cohesion: 0.29
Nodes (7): Before your first commit, Contributing, Decisions, Generated files, If it touches retrieval, extraction or the grounding gate, The loop, When you are unsure

### Community 235 - "The corpus"
Cohesion: 0.29
Nodes (6): Handing a batch over, One rule, The corpus, The order matters, Tiers, Validate before handing over

### Community 236 - "3. PaperBrain informs core/retrieve/'s pattern; it is not the core module"
Cohesion: 0.29
Nodes (6): 3. PaperBrain informs core/retrieve/'s pattern; it is not the core module, Consequences, Context, Decision, Rejected, Revisit when

### Community 237 - "9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack"
Cohesion: 0.29
Nodes (6): 9. `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 238 - "16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent"
Cohesion: 0.29
Nodes (7): 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent, Addendum, 17 September 2026: coverage review and the adult rule, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 239 - "NNNN · The decision, as a statement not a question"
Cohesion: 0.29
Nodes (6): Alternatives considered, Consequences, Context, Decision, NNNN · The decision, as a statement not a question, Revisit when

### Community 240 - "Notion"
Cohesion: 0.29
Nodes (7): Importing the task database, Keeping the two in sync, Notion, Option A — move the hub into Christian's workspace ✅ recommended, Option B — Christian switches his connector to Yew Mun's workspace, Option C — leave Notion as a human-only view, The access problem, and the one decision that fixes it

### Community 241 - "Premium and Subsidy Tables"
Cohesion: 0.29
Nodes (6): MediShield Life (CPF Board), MediShield Life Premium Schedule for Singapore Citizens and Permanent Residents, Merdeka Generation Subsidy, Pioneer Generation Subsidy, Premium and Subsidy Tables, Premium Subsidy for the Lower- to Middle-Income

### Community 242 - "Understanding integrated shield plans"
Cohesion: 0.29
Nodes (6): Are you covered?, Should you upgrade to an IP?, The deductible is the fixed amount you pay each policy year – ranging from $1,500 to $3,500, depending on ward class – before any payout from your IP. The co-payment is 5% of the bill, capped at a minimum of $6,000 per year., Understanding integrated shield plans, Your budget, Your comfort level with the types of hospitals, wards and doctors

### Community 243 - "Christian — Lane A · Integration and product owner"
Cohesion: 0.29
Nodes (7): Also yours, Christian — Lane A · Integration and product owner, Starter prompt for your coding agent, Starter prompt: what can I actually pick up?, The five things you ship, Week 1, in order, What integration actually means here

### Community 244 - "Yew Mun — Lane B · Retrieval and evaluation"
Cohesion: 0.29
Nodes (7): Done, Order of work, Starter prompt for your coding agent, Targets, The three golden sets, What you own, Yew Mun — Lane B · Retrieval and evaluation

### Community 245 - "test_an_advice_card_carries_a_rules_publisher_on_the_wire"
Cohesion: 0.33
Nodes (4): advice_card(), rule_citation(), test_an_advice_card_carries_a_rules_publisher_on_the_wire(), test_an_answer_that_fails_before_any_advice_is_rolled_back_and_after_it_is_kept()

### Community 246 - "Architecture"
Cohesion: 0.29
Nodes (6): Architecture, Constraints that drive everything, Data flow, Decisions, Extension points, Failure modes, handled

### Community 247 - "system/route.ts"
Cohesion: 0.60
Nodes (5): ACTIONS, GET(), POST(), sameOrigin(), unlocked()

### Community 248 - "Claude Code — read this first"
Cohesion: 0.33
Nodes (5): Before you say you are done, Claude Code — read this first, Finding your way around, Skills and commands, The three things agents get wrong here

### Community 249 - "2. One PostgreSQL instance for everything"
Cohesion: 0.33
Nodes (5): 2. One PostgreSQL instance for everything, Consequences, Context, Decision, Rejected

### Community 250 - "10. `main` is unprotected, and the discipline is human"
Cohesion: 0.33
Nodes (6): 10. `main` is unprotected, and the discipline is human, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 251 - "12. Chunks follow the document's headings, and embeddings use the model's task prompts"
Cohesion: 0.33
Nodes (5): 12. Chunks follow the document's headings, and embeddings use the model's task prompts, Consequences, Context, Decision, Evidence

### Community 252 - "14 · A pack supplies what the core knows about a domain, and the core stays generic"
Cohesion: 0.33
Nodes (6): 14 · A pack supplies what the core knows about a domain, and the core stays generic, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 253 - "17 · A pack is grounding and persona; the core owns documents"
Cohesion: 0.33
Nodes (6): 17 · A pack is grounding and persona; the core owns documents, Alternatives considered, Consequences, Context, Decision, Revisit when

### Community 254 - "Artefacts"
Cohesion: 0.33
Nodes (5): A note on the model, Artefacts, Current deliverables, Regenerating, Source material

### Community 255 - "Why the prototype is evaluated on synthetic data"
Cohesion: 0.33
Nodes (5): The decision, What synthetic data does not prove, What we do not do, Why, Why the prototype is evaluated on synthetic data

### Community 256 - "`docs/report/` — the final report"
Cohesion: 0.33
Nodes (6): `docs/report/` — the final report, Ownership, Source documents written for the report, The rule that keeps it honest, The thing to understand before you write a word, Three questions for the supervisors, at the 6 October mid-term

### Community 257 - "About Integrated Shield Plan"
Cohesion: 0.33
Nodes (5): About Integrated Shield Plan, How do I find out if I have an Integrated Shield Plan?, How do Integrated Shield Plan premiums and claims work?, Should I consider purchasing an Integrated Shield Plan?, What is an Integrated Shield Plan?

### Community 258 - "MediShield Life Benefits"
Cohesion: 0.33
Nodes (5): Exclusions under MediShield Life, Fertility Preservation Procedures in cases of potential iatrogenic infertility, List of Serious Pregnancy and Delivery-related Complications, MediShield Life Benefits, MediShield Life Benefits

### Community 259 - "The team"
Cohesion: 0.33
Nodes (6): Everyone, regardless of lane, The dependency that sets the order, The presentation split, The task lists are generated, The team, Why work does not live here

### Community 260 - "Basis"
Cohesion: 0.17
Nodes (18): Figure, _amount(), Basis, calculate(), _calculation(), _capital(), cents(), _estimate_saving() (+10 more)

### Community 261 - "`core/graph/` — the LangGraph runtime"
Cohesion: 0.40
Nodes (4): `core/graph/` — the LangGraph runtime, Rules, What belongs here, What does not

### Community 262 - "0002_household.sql"
Cohesion: 0.70
Nodes (4): document_attribution, people, person_aliases, telegram_identities

### Community 263 - "0003_advice.sql"
Cohesion: 0.60
Nodes (4): advice_consents, advice_records, grounding_sources, grounding_values

### Community 264 - "1. Record architecture decisions"
Cohesion: 0.40
Nodes (4): 1. Record architecture decisions, Consequences, Context, Decision

### Community 265 - "4. Local setup can run before the household assistant is ready"
Cohesion: 0.40
Nodes (4): 4. Local setup can run before the household assistant is ready, Consequences, Context, Decision

### Community 266 - "6. pypdfium2 renders the page images the quarantine second pass reads"
Cohesion: 0.40
Nodes (4): 6. pypdfium2 renders the page images the quarantine second pass reads, Consequences, Context, Decision

### Community 267 - "8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document"
Cohesion: 0.40
Nodes (4): 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document, Consequences, Context, Decision

### Community 268 - "13. A question is understood before it is searched, and scoped before it is cut"
Cohesion: 0.40
Nodes (5): 13. A question is understood before it is searched, and scoped before it is cut, Consequences, Context, Decision, Evidence

### Community 269 - "Data inventory — identity data, dates of birth and loans"
Cohesion: 0.40
Nodes (4): Data inventory — identity data, dates of birth and loans, Open questions for Siew, The inventory, What this entry covers

### Community 270 - "Notice"
Cohesion: 0.40
Nodes (4): Notice, Third-party components, This repository contains no personal data, Use

### Community 272 - "`core/ingest/` — the ingestion worker"
Cohesion: 0.50
Nodes (3): `core/ingest/` — the ingestion worker, Quarantine is two-stage, Rules

### Community 273 - "`core/retrieve/` — hybrid retrieval"
Cohesion: 0.50
Nodes (3): `core/retrieve/` — hybrid retrieval, Rules, What belongs here

### Community 275 - "7. The answer graph ships before hybrid retrieval and before a checkpoint table"
Cohesion: 0.50
Nodes (4): 7. The answer graph ships before hybrid retrieval and before a checkpoint table, Consequences, Context, Decision

### Community 276 - "15. A name scopes a question, and a grandparent is not a parent"
Cohesion: 0.50
Nodes (4): 15. A name scopes a question, and a grandparent is not a parent, Consequences, Context, Decision

### Community 277 - "github.md"
Cohesion: 0.50
Nodes (3): Last sync, Screen map, Updated in this project

### Community 279 - "`docs/governance/` — the assurance artefacts"
Cohesion: 0.50
Nodes (3): `docs/governance/` — the assurance artefacts, The autonomy statement in one line, The rule that governs all eight

### Community 280 - "Category hospital_expense (hospital and surgical plan)"
Cohesion: 0.50
Nodes (4): Integrated Shield Plan (MediShield Life component plus a private insurance component), MediShield Life annual premium schedule by age next birthday (including 9% GST), Category hospital_expense (hospital and surgical plan), Grounding value key medishield_life_premium (by age_band)

## Ambiguous Edges - Review These
- `Provenance register for corpus sg_protection_guidance` → `Lane A - Christian, integration and product`  [AMBIGUOUS]
  packs/insurance_agent/grounding/sg_protection_guidance/sources.yaml · relation: references
- `LIA 2022 Protection Gap Study Key Findings` → `Protection rule of thumb: 9x annual income for death and TPD, 4x for critical illness`  [AMBIGUOUS]
  packs/insurance_agent/grounding/sg_protection_guidance/sources.yaml · relation: cites
- `The Lim Household, Tampines` → `Republic of Xinkapow, the Invented Jurisdiction`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to
- `Republic of Xinkapow, the Invented Jurisdiction` → `Real Organisations May Be Named`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to
- `Motor Vehicle Hire Purchase Agreement Template` → `Fill the Register Before Generating Documents`  [AMBIGUOUS]
  corpus/templates/car_loan_agreement.html · relation: conceptually_related_to

## Knowledge Gaps
- **1022 isolated node(s):** `The line format`, `How it is scored`, `Planted documents (for Desmond)`, `Assumptions to recheck before the run`, `After generating` (+1017 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 2453 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **444 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Provenance register for corpus sg_protection_guidance` and `Lane A - Christian, integration and product`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Settings` connect `Settings` to `ModelUnavailable`, `HybridRetriever`, `ScriptedOllama`, `test_advice_module.py`, `tasks.py`, `FolderAdapter`, `test_telegram_capture.py`, `FakeConn`, `_Answering`, `bench_runtime.py`, `settings`, `schedule.py`, `FakeCursor`, `Passage`, `TelegramAdapter`, `eval/modules.py`, `DatabaseUnavailable`, `test_lifecycle.py`, `.load`, `test_modules.py`, `Measured`, `test_api.py`, `rows_for`, `test_household.py`, `pytest`, `test_eval_modules.py`, `report.py`, `registry.py`, `run.py`, `ClosingSpy`, `load_corpus.py`, `ModuleAdviser`, `AlertConfig`, `Any`, `Answer`, `review_grounding_values.py`, `routes.py`, `test_rerank.py`, `Ollama`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 64 inferred relationships involving `InstalledPack` (e.g. with `_Answering` and `AdviceLog`) actually correct?**
  _`InstalledPack` has 64 INFERRED edges - model-reasoned connections that need verification._
- **What connects `The line format`, `How it is scored`, `Planted documents (for Desmond)` to the rest of the system?**
  _1022 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ModelUnavailable` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._
- **What is the exact relationship between `LIA 2022 Protection Gap Study Key Findings` and `Protection rule of thumb: 9x annual income for death and TPD, 4x for critical illness`?**
  _Edge tagged AMBIGUOUS (relation: cites) - confidence is low._
- **Why does `InstalledPack` connect `InstalledPack` to `ModelUnavailable`, `test_advice_graph.py`, `ScriptedOllama`, `Basis`, `advice/__init__.py`, `test_advice_module.py`, `test_grounding_index.py`, `FakeConn`, `_Answering`, `settings`, `FakeCursor`, `Passage`, `DatabaseUnavailable`, `extract_values`, `test_api.py`, `rows_for`, `DocumentCatalog`, `registry.py`, `._absence`, `test_grounding.py`, `ClosingSpy`, `packs.py`, `ModuleAdviser`, `PackManifest`, `pack`, `index_pack`, `Answer`, `routes.py`, `Ollama`, `AdviceConsent`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._