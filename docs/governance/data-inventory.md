# Data inventory — identity data, dates of birth and loans

> **Draft — for Siew's review.** First entry only: the data ADR 0017 decision 6 makes
> household data. It is not yet the whole inventory. Every claim points at a file; anything
> that could not be traced is marked `unverified`.

## What this entry covers

`core/documents.yaml` declares four new document types and one new field (ADR 0017):

| Datum | Document type · `facts.key` | Example (synthetic, `docs/synthetic-generation-guide.md` §1) |
|---|---|---|
| NRIC / FIN number | `identity_card` · `id_number` | `S8714289B` |
| Passport number | `passport` · `passport_no`, `date_of_expiry` | §2.8 |
| Birth registration number | `birth_certificate` · `registration_no` | `T1942088J` |
| Full name | `identity_card`/`passport` · `full_name`; `birth_certificate` · `child_name` | `MARCUS LIM JUN WEI` |
| Date of birth | `date_of_birth` on the three identity types, and optional on `policy_schedule` | `1987-05-08` |
| Loan figures | `loan_agreement` · `lender`, `facility_no`, `borrower`, `principal`, `monthly_repayment`, `agreement_date` | `HL-2021-994182`, SGD 540,000.00 |

The full page text of each document is also chunked and embedded, so every value printed on
it rests in `chunks.text` as well as in `facts` — including values no field names (the address
on the back of an identity card, parents' ID numbers on a birth certificate).

## The inventory

| Question | Answer | Evidence |
|---|---|---|
| **Where it enters** | The watched folder (`inbox/`), or a photograph sent to the household's Telegram bot, which writes a copy into the same folder. | `core/adapters/telegram.py` (`_write_local_copy`); `core/runtime/settings.py` (`_folder`) |
| **Where it rests** | 1. The original file in the watched folder. 2. Postgres: `documents` (file name, type, status), `chunks` (page text and its embedding), `facts` (one row per value, with `document_id` and `page`), `person_aliases` (names as printed). 3. Answers that quote it: `advice_records.answer_text`, `traces.payload` and LangGraph's checkpoint tables — whether an identity value is written there depends on the question asked, `unverified`. | `db/migrations/0001_init.sql`, `0002_household.sql`, `0003_advice.sql`; `core/advice_records.py` |
| **Encrypted at rest** | No. Not by the application. | `web/lib/lock.ts` docstring: the lock "does not encrypt anything" |
| **Who can see it** | Through the interface: only a browser holding an in-date session cookie from the local passphrase. Every page under `web/app/(app)/` redirects to `/unlock` without one, and the browser's only routes to the API — `/api/parrot/*`, `/api/chat` — return 401 without one. **Not** through the interface: anyone with a terminal on this computer. The API answers any loopback request with no authentication, and Postgres and the folder are readable directly. | `web/app/(app)/layout.tsx`; `web/app/api/parrot/[...path]/route.ts`; `web/app/api/chat/route.ts`; `web/lib/lock.ts`; `api/main.py` (`TrustedHostMiddleware`, loopback hosts) |
| **What crosses a boundary** | **At inference and at rest: nothing.** Ollama, Postgres and Redis URLs are refused at start-up unless they are loopback, the API binds only `127.0.0.1`, and Docker publishes Postgres and Redis on `127.0.0.1` only. **At capture by Telegram: the document image does.** A photograph sent to the bot passes through Telegram's servers, and is deleted from the chat after it is filed (`TELEGRAM_DELETE_AT_SOURCE`, default on). What Telegram retains after deletion is `unverified`. The bot's replies carry only a filing acknowledgement and the file name, never an answer. The folder route crosses nothing. **The screens may be reachable from the local network.** `scripts/run_parrot.py` starts `npm run dev`, which is `next dev` with no `-H`, and Next.js then listens on every interface, not only loopback. A device on the same network still meets the passphrase, but after unlocking, pages travel over plain HTTP. Whether that is intended is `unverified`. | `core/runtime/settings.py` (`local_url`); `scripts/run_parrot.py` (`--bind-address` choices `127.0.0.1`; `start_web`); `web/package.json`; `infra/docker-compose.yml`; `core/adapters/telegram.py` (`_say`, `_delete`) |
| **Purpose** | A household assistant: answering identity questions the owner needs for bookings and forms ("What is Rachel's passport number?", "When was Marcus born?"), with the page cited; loans for "what do I owe" and penalty questions; dates of birth for age in insurance advice, only under the owner's recorded consent. | ADR 0017 decision 6; ADR 0016; `advice_consents` in `db/migrations/0003_advice.sql` |
| **Retention and erasure** | `unverified`. `retention-and-erasure.md` is not yet written. What is known: `chunks` and `facts` are `ON DELETE CASCADE` from `documents`; the file in the folder is not removed by a database delete. | `db/migrations/0001_init.sql`; `docs/governance/README.md` |

## Open questions for Siew

1. Telegram as a capture route for identity documents: acceptable with delete-at-source, or
   should identity documents be folder-only?
2. Identity values quoted in `traces`, checkpoints and `advice_records` — redact, or keep as the
   audit trail and cover them in the retention policy?
3. The lock is a screen lock, not encryption (`web/lib/lock.ts` says so). Is that sufficient
   for identity numbers, which ADR 0017 calls the most sensitive data in the vault?
4. Should the screens bind to loopback only (`next dev -H 127.0.0.1`), as the API does?
