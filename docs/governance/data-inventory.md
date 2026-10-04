# Data inventory and flow map

Status: draft · Owner: Siew · Reviewer: Christian · First entry (identity data, dates of birth
and loans) by Christian, 2026-09-17, kept below and corrected where the code has since moved

> Every claim points at a file. Anything that could not be traced is marked **unverified**.
> Statements about Singapore law are marked **to check against the instrument** until
> checked against its text. Where personal data rests, and what a delete reaches, is worked
> through in [`retention-and-erasure.md`](retention-and-erasure.md); this document does not
> repeat that trace.

## Whose data

| Whose | Who they are | Evidence |
|---|---|---|
| **The owner** | The one person marked `is_owner`. Every first-person answer is scoped to them | `db/migrations/0002_household.sql` (`people_one_owner`); ADR 0011 |
| **Other household members** | Partner, children, parents. They arrive off a document, not off a form | `0002_household.sql` (`relation`); ADR 0011 |
| **A child** | In the corpus, Lucas (born 2019): birth certificate, child policy, benefit illustration | `corpus/canon.md`; `corpus/register/batch2.csv` (`b2-0006`, `b2-0016`) |
| **Third parties named on a document** | Kept as `external` people so they stop raising questions: an ex-landlord, a former employer, another driver | `0002_household.sql` (`external` column comment) |

Organisations (insurers, employers, charities, lenders) are named on documents too. They are
not personal data, but an employer name next to a salary identifies the employee.

## The inventory

One row per kind of personal data. "Fields" are the `facts.key` values declared in
`core/documents.yaml`. Every value is also in `chunks.text`, because the whole page is chunked
and embedded, including values no field names.

| Data | Document types · fields | Whose | Purpose | Sensitivity | Retained |
|---|---|---|---|---|---|
| **National identity numbers** | `identity_card` · `id_number`; `passport` · `passport_no`; `birth_certificate` · `registration_no` | Every member, including a child | Forms and bookings ("What is Rachel's passport number?") | Highest. See [Identity data](#identity-data-dates-of-birth-and-loans) | Until the document is erased |
| **Names and dates of birth** | `full_name`, `child_name`, `date_of_birth` on identity types; `insured`, `life_assured`, `employee`, `taxpayer`, `member`, `donor`, `student`, `borrower` on the rest; `date_of_birth` optional on `policy_schedule` | Every member | Whose document this is; age for insurance advice under consent | Identifying | Until the document is erased |
| **Address** | No field. Printed on identity cards and letters, so in `chunks.text` only | Every member | None of its own. It arrives with the page | Identifying | With the document |
| **Income and employment** | `payslip` · `employer`, `gross_salary`, `cpf_employee`, `net_pay` | Earning adults | "What did I earn?"; tax-relief calculations | Financial | Until the document is erased |
| **Tax** | `notice_of_assessment` · `assessable_income`, `tax_payable` | Earning adults | Tax questions; SRS relief room (ADR 0016) | Financial | Until the document is erased |
| **Retirement savings** | `cpf_statement` · `ordinary_account_balance`, `total_contributions`; `srs_statement` · `account_no`, `contributions_ytd`; `cpf_topup_receipt` | Adults, and a parent receiving a top-up | Balances; relief room | Financial; `account_no` identifies an account | Until the document is erased |
| **Debt** | `loan_agreement` · `facility_no`, `principal`, `monthly_repayment` | Borrower | "What do I owe?" | Financial | Until the document is erased |
| **Insurance cover** | `policy_schedule`, `renewal_notice`, `benefit_illustration`, `policy_anniversary_statement` · policy numbers, premiums, sums assured, surrender value | Insured or life assured, including a child and the parents | Renewal reminders, cover questions, cover-gap advice under consent | Financial; reveals health through what is covered | Until the document is erased |
| **Health** | No field names a diagnosis. `claim_letter` · `incident_date`, `settled_amount`; the page text of a claim letter or hospital plan may | Claimant | Claim questions | Health. **Unverified** whether the corpus's claim letters print a diagnosis; the canon gives the parents named conditions | Until the document is erased |
| **Donations** | `donation_receipt` · `charity`, `donation_amount` | Donor | Tax-deduction questions | Can reveal beliefs or affiliations through the charity | Until the document is erased |
| **Education** | `course_fee_receipt` · `provider`, `course_title`, `fee_amount` | Student | Relief questions | Low | Until the document is erased |
| **Household relationships** | `people` (`display_name`, `relation`), `person_aliases` (every name a document printed) | Every member and named third parties | Scoping answers to the right person | Identifying | Until the person is removed |
| **Messaging identity** | `telegram_identities.chat_id` | Members who use the bot | Attributing a photographed document to its sender | Identifying | Until the person is removed |
| **Consent and advice** | `advice_consents` (granted or withdrawn, wording hash); `advice_records` (`basis`, `answer_text`) | The person advised | The record of what was advised under which consent (ADR 0016) | Financial; may quote any of the above | Indefinitely, today. See the retention policy |
| **Corrections and traces** | `traces.payload`. A correction keeps `subject`, `was` and `now` | Whoever the fact is about | Audit trail and evaluation data | May quote any of the above | Indefinitely, today. See the retention policy |
| **File names** | `documents.original_name`; Celery task arguments in Redis | Whoever the file is about | Showing and re-reading the document | Often carries a name | With the document; Redis results expire in 1 hour |

**To check against the instrument:** the PDPC's *Advisory Guidelines on the PDPA for NRIC and
other National Identification Numbers*. As we understand them, they restrict organisations
collecting NRIC numbers. Whether they apply to a household's own copy depends on the
domestic-capacity question raised in the retention policy.

## Flow map

```
 capture                      registration          reading (all on this computer)         at rest
 ───────                      ────────────          ──────────────────────────────         ───────
 file saved to inbox/  ─┐
                        ├──▶ hash, row in      ──▶ Celery task  ──▶ parse, OCR ──▶ extract ──▶ Postgres
 photo to Telegram bot ─┘    documents             (Redis:         (Docling,      (Ollama,     documents, chunks,
   │  passes through                               id, digest,      RapidOCR)      127.0.0.1)   facts, obligations,
   │  Telegram's servers,                          file name)                                   people, traces …
   │  copy written to inbox/,                                                                      │
   │  message deleted                                                                              ▼
   ▼                                                                            question ──▶ retrieve, rerank,
 [crosses a boundary]                                                           (screens on    answer, gate
                                                                                 127.0.0.1)   (Ollama, in-process
                                                                                              reranker)
```

| Step | What crosses a network boundary | Evidence |
|---|---|---|
| Capture by folder | Nothing | `core/adapters/folder.py` |
| Capture by Telegram | **The document image**, through Telegram's servers. The chat message is deleted after filing, unless `TELEGRAM_DELETE_AT_SOURCE` is turned off; it is on by default. Long polling, so nothing listens publicly | `core/adapters/telegram.py` (module docstring, `_write_local_copy`); `core/runtime/settings.py` line 204 |
| Queue | Nothing. Redis is published on `127.0.0.1` only, and tasks carry an id, digest, MIME type and file name, never file bytes | `infra/docker-compose.yml`; `core/worker/tasks.py` (`sender`) |
| Parsing, extraction, answering | Nothing. Every Ollama, Postgres and Redis URL must be loopback or start-up refuses it. The reranker runs in-process | `core/runtime/settings.py` (lines 21, 34); ADR 0018 |
| Screens | Nothing. `next dev -H 127.0.0.1` binds loopback only | `web/package.json` (`"dev"`) |
| Evaluation judge | Nothing. Local judge model | `eval/results/2026-09-30-run2-hybrid-plus-reranker.md` (judge `qwen2.5:7b-instruct`) |
| Model download | No personal data. Models are pulled once from Ollama's registry and Hugging Face | `infra/.env.example` (`ollama pull …`, "Fetched once into the HF cache") |

## Identity data, dates of birth and loans

*Christian's first entry, 2026-09-17. Corrections since are marked "Corrected".*

`core/documents.yaml` declares four document types and one field for this data (ADR 0017):

| Datum | Document type · `facts.key` | Example (synthetic, `docs/synthetic-generation-guide.md` §1) |
|---|---|---|
| NRIC / FIN number | `identity_card` · `id_number` | `S8714289B` |
| Passport number | `passport` · `passport_no`, `date_of_expiry` | §2.8 |
| Birth registration number | `birth_certificate` · `registration_no` | `T1942088J` |
| Full name | `identity_card`/`passport` · `full_name`; `birth_certificate` · `child_name` | `MARCUS LIM JUN WEI` |
| Date of birth | `date_of_birth` on the three identity types, and optional on `policy_schedule` | `1987-05-08` |
| Loan figures | `loan_agreement` · `lender`, `facility_no`, `borrower`, `principal`, `monthly_repayment`, `agreement_date` | `HL-2021-994182`, SGD 540,000.00 |

Values no field names also rest in `chunks.text`: the address on the back of an identity
card, and parents' ID numbers on a birth certificate.

| Question | Answer | Evidence |
|---|---|---|
| **Where it enters** | The watched folder, or a photograph sent to the Telegram bot, which writes a copy into the same folder | `core/adapters/telegram.py` (`_write_local_copy`); `core/runtime/settings.py` |
| **Where it rests** | The original file in the watched folder; `documents`, `chunks`, `facts`, `person_aliases`; and in answers that quote it, `advice_records.answer_text` and `traces.payload`. Whether an identity value lands there depends on the question asked: **unverified**. **Corrected:** there are no LangGraph checkpoint tables. The checkpointer is `MemorySaver`, in process memory only | `db/migrations/0001`–`0003`; `core/advice_records.py`; `core/graph/answer.py` (module docstring) |
| **Encrypted at rest** | No, not by the application | `web/lib/lock.ts` docstring: the lock "does not encrypt anything" |
| **Who can see it** | Through the interface: only a browser with an in-date session cookie from the local passphrase. Pages redirect to `/unlock`, and `/api/parrot/*` and `/api/chat` return 401 without one. Not through the interface: anyone with a terminal on this computer. The API answers any loopback request without authentication, and Postgres and the folder are readable directly | `web/app/(app)/layout.tsx`; `web/app/api/parrot/[...path]/route.ts`; `web/app/api/chat/route.ts`; `web/lib/lock.ts`; `api/main.py` |
| **What crosses a boundary** | As in the flow map. **Corrected:** the screens now bind to loopback (`next dev -H 127.0.0.1`), so the earlier concern about the local network no longer holds. What Telegram retains after a message is deleted is **unverified** | `web/package.json`; `core/adapters/telegram.py` |
| **Purpose** | Identity questions for bookings and forms, with the page cited; loans for "what do I owe"; dates of birth for age in insurance advice, only under recorded consent | ADR 0017 decision 6; ADR 0016; `advice_consents` |
| **Retention and erasure** | **Corrected:** now covered by [`retention-and-erasure.md`](retention-and-erasure.md). Chunks and facts cascade from `documents`. The file in the folder is not removed by a database delete. An indexed document cannot yet be erased through the product | `db/migrations/0001_init.sql`; `core/ingest/sql.py` (`DELETE_QUARANTINED`) |

## What this inventory supports

The architecture diagram's trust boundary says household data does not leave the machine at
inference. The flow map above is the evidence for that claim. It has one exception, Telegram
capture, which the claim should name rather than leave out.

## Open questions

1. ~~**Telegram for identity documents** (Christian's question 1). Acceptable with
   delete-at-source, or should identity documents be folder-only?~~ **Decided, Siew,
   2026-10-04: identity documents may be accepted through Telegram.** The image crosses
   Telegram's servers, as the flow map records. Delete-at-source is on by default
   (`TELEGRAM_DELETE_AT_SOURCE`, `core/runtime/settings.py`), and what Telegram keeps after
   deletion remains question 7.
2. **Values quoted in `traces` and `advice_records`** (Christian's question 2). Redact them,
   or keep them as the audit trail? Now an open question in the retention policy.
3. **Screen lock, not encryption** (Christian's question 3). Is a passphrase lock enough for
   identity numbers, which ADR 0017 calls the most sensitive data in the vault? For Siew.
4. ~~Should the screens bind to loopback only?~~ Done: `web/package.json`.
5. **Health data.** Do the corpus's claim letters print a diagnosis? If they do, health
   data is held in `chunks.text`. Check `b1-0007` to `b1-0009`. For Desmond.
6. **NRIC guidelines.** Read the PDPC advisory guidelines on NRIC numbers and record whether
   they bear on a household's own copy. For Siew.
7. **What Telegram keeps** after a bot deletes a message. Check Telegram's published privacy
   policy and cite it with its date. For Siew.
