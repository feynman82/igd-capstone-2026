# Marcus tax advice — demonstration readiness gate

**Status: NOT YET LIVE-VERIFIED.** GitHub CI passing does not verify the presenter's local Vault, ingestion worker, tax grounding approval, consent state or calculator outputs.

## Supported evidence already on main

The batch1 register includes Marcus NOAs YA2025 (`b1-0030`) and YA2026 (`b1-0028`), CPF 2024 (`b1-0024`) and 2025 (`b1-0022`), SRS 2024 (`b1-0026`) and 2025 (`b1-0025`). Check the **actual document and page citations** against these source PDFs.

The extra YA2023/YA2024 NOA and 2026 SRS worksheets in `corpus/batches/demo-tax-review/` are **unverified fictional drafts**, not approved evidence. Do **not** ingest them into the live Vault or treat a hypothetical zero SRS contribution as a real 2026 amount. Their browser-printable copies are under `web/public/demo/`.

## Presenter machine: mandatory rehearsal

- [ ] Start database, worker, Ollama, backend and web app following `docs/demo-run-sheet.md`.
- [ ] Load **approved** batch1 corpus using `make corpus-load BATCH=batch1` (if not already loaded). Confirm ingest worker completed and Vault shows the six Marcus records above.
- [ ] Check both domain packs enabled; check approved IRAS SRS cap and resident tax-rate values are available for the calculation. Do not infer approval from a markdown grounding file merely existing.
- [ ] In Vault, open Marcus YA2026 NOA and 2025 SRS; confirm extracted fields and source-page citations. Verify the 2025 SRS value is **not** silently represented as a 2026 contribution.
- [ ] Ask **“Give me some tax advice”**. Verify consent prompt if required, then the tax relief check card. Record whether SRS room and estimated saving calculate or display specific missing evidence.
- [ ] Ask **“How much tax does SRS save?”** and **“How much can I contribute to SRS?”**. Confirm calculator-derived estimates are qualified, have correct year context and source citations. If missing a current-year statement, the safe result is to abstain, **not** to guess.
- [ ] Ask **“What does my latest Notice of Assessment say?”** and verify the response cites Marcus's YA2026 NOA and correctly distinguishes assessable income from tax payable.
- [ ] Run the core demo's abstention prompt **“What is my electricity bill for March?”**. Verify it does not invent a figure.
- [ ] Capture dated screenshots of the Vault, advice card, consent, source citation and any missing-data card. Log observed pass/fail and environment; no claim of end-to-end success without this evidence.

## Decision rule

**GO for a limited demo** only when existing registered records are present and cited, and the tax pack either gives correct estimates or explicitly identifies what it cannot calculate. State that PARROT provides guidance, not an official IRAS assessment.

**NO-GO for a complete personalised tax optimisation claim** until the current-year SRS evidence is verified, the relevant IRAS values are approved, calculations are tested and the three draft documents are either validated/replaced or excluded.

Do not modify the frozen Run 3 baseline. The existing 7m50s general demonstration in `docs/demo-run-sheet.md` remains unchanged.
