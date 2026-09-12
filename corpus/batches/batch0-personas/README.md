# batch0-personas — NOT an evaluation batch

These 22 files are household persona sketches, not corpus documents. They have **no
register**, and they cannot have one:

- Not one of them is a `doc_type` any installed pack declares. The ten are
  `policy_schedule, renewal_notice, claim_letter, benefit_illustration,
  policy_anniversary_statement, payslip, donation_receipt, cpf_statement,
  srs_statement, notice_of_assessment`. These are NRIC records, birth certificates,
  medical histories, a caregiver schedule, school reminders and free-text summaries.
- They name real organisations on their face, which `corpus/README.md` rule 1 forbids.
- Their identifiers are masked (`GE-XXXX-X12G`, `S91XXXX15A`), so they carry no value an
  extractor could be scored against.

Do not run `make corpus-load BATCH=batch0-personas`. Every document would land in
quarantine and contribute nothing to `facts`.

What they are good for: character and household colour when writing golden-set questions,
and as screen dressing for the demo. Treat them as a mood board, not as data.

The real batches are register-first — see `corpus/README.md`.
