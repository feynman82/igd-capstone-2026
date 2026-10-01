# Data inventory and flow map

> **Status: draft for Christian's technical review.** Owner: Siew. Last checked against the code
> on 2026-10-01 (`main` at `fc035bd`).
>
> Every claim points at a file. Anything that could not be traced is marked **`unverified`** and
> is listed under "Open questions" rather than written as a plausible sentence. This inventory
> describes what the code does today, not what a policy intends.

## What this document answers

For every kind of personal data PARROT handles: **whose** it is, **why** it is held, **where** it
enters, **where** it rests, whether it **crosses a network boundary**, and **what deletes it**.
The retention period asked for in the W1 task is answered in the last column. For most rows the
answer is that **nothing deletes it today**. `retention-and-erasure.md` has to close that gap.
This document records it.

---

## 1. Whose data

| Data subject | How they appear | Evidence |
|---|---|---|
| **The owner** | The one person with `people.is_owner = true`, and the database allows only one. Every first-person answer is scoped to them. | `db/migrations/0002_household.sql` (`people_one_owner`) |
| **Household members** | Rows in `people` with `relation` of `partner`, `child`, `parent` or `other`, created by the owner. Children are explicitly in scope: `birth_certificate` is a document type. | `0002_household.sql`; `core/documents.yaml` (`birth_certificate.child_name`) |
| **Third parties named on a document** | Employers, lenders, insurers, charities and training providers are named by organisation. Some are **natural persons the household never agreed to hold**, for example "the ex-landlord on a tenancy agreement, a former employer, the other driver in a claim". These are kept with `external = true` "rather than discarded". | `0002_household.sql` (comment on `people.external`) |
| **People printed on a page but in no field** | Whatever the page says is chunked and embedded, including values no field names. Examples are the parents' ID numbers on a birth certificate and the address on the back of an identity card. | `core/ingest/chunk.py` → `chunks.text` in `0001_init.sql` |
| **Team members (holdout only)** | The 40-document real holdout. It is kept out of git by `.gitignore` (`corpus/holdout/`). The consent protocol that must govern it, `consent-and-redaction.md`, **does not exist yet**. | `.gitignore`; `docs/governance/README.md` |

### Lawful basis: deemed consent

> **Decision (Siew, 2026-10-01).** The exclusion for individuals acting in a personal or
> domestic capacity is not relied on, so PARROT is treated as within the PDPA. The basis for
> holding a household member's data is **deemed consent**: *Personal Data Protection Act 2012,
> Part 4 (Collection, Use and Disclosure of Personal Data), section 15 (Deemed consent)*. When a
> member submits their own documents and information, they are deemed to consent to it being
> held for the purpose they submitted it for.
>
> *Still to do:* quote the operative subsection verbatim from Singapore Statutes Online, with
> the revised-edition date. It is not paraphrased here because it has not yet been read from
> the source.

Advice is the one place the system asks for more than deemed consent. An advice answer needs
an **explicit, recorded** grant in `advice_consents` (S4), checked in the same transaction as
the answer (`core/advice_records.py`; ADR 0016).

Deemed consent rests on knowing **who submitted** a document. Here is what the code holds as
evidence of that:

| Route | Submitter recorded? | Evidence |
|---|---|---|
| Telegram, from a chat mapped to a person | **Yes.** The chat id → person mapping is stamped on the document as `document_attribution.source = 'telegram'`. | `core/adapters/telegram.py` (`_capture`, `self._attribute`); `0002_household.sql` |
| Telegram, from an unmapped chat | No. The document is filed with no attribution. | `core/adapters/telegram.py` ("attribution is a nicety; capture is not") |
| Folder | **No.** The sender passed in is the folder path, and `documents` has no sender column. Only `source_channel = 'folder'` is kept. | `core/adapters/folder.py` (`receive(..., str(self._settings.root), ...)`); `core/ingest/register.py` (`INSERT INTO documents`) |
| A person attributes it on a screen | Yes, as `document_attribution.source = 'user'`. This records who the document is *about*, not who submitted it. | `0002_household.sql` |

The cases deemed consent does not obviously reach are listed in §6, questions 5a to 5d.

Everything committed under `corpus/batches/` and `inbox/` is synthetic and is marked as such
(`.gitignore` comments; `documents.synthetic` in `0001_init.sql`). This inventory is about the data
a household would put into the running system.

---

## 2. The inventory

Abbreviations: **DB** = the one Postgres database (`infra/docker-compose.yml`, volume `pgdata`).
"Cascades" means `ON DELETE CASCADE` from `documents` in the migrations.

### 2a. What the documents carry

The document types and fields are declared once, in `core/documents.yaml`, as ADR 0017 requires.

| # | Category | Whose | Fields (`facts.key`) and document types | Purpose | Rests in | What deletes it today |
|---|---|---|---|---|---|---|
| D1 | **Original file**: the image or PDF itself | Any of §1 | Every type | Re-reading, citation thumbnails (`core/pages.py`), the quarantine image pass | The watched folder `inbox/` (`core/runtime/settings.py` `_folder`), as written by a person or by the Telegram adapter (`core/adapters/telegram.py` `_write_local_copy`) | **Nothing in PARROT.** A database delete never removes the file. The file has to be deleted by hand. |
| D2 | **National identifiers**: NRIC/FIN, passport number, birth registration number | Owner, members, children | `identity_card.id_number`, `passport.passport_no`, `birth_certificate.registration_no` | Identity questions asked when filling in forms or making bookings ("What is Rachel's passport number?"), answered with the page cited (ADR 0017 decision 6) | `facts.value_text`, `chunks.text` and its embedding, plus D1 | Cascades with the document. See §4 for what survives it. |
| D3 | **Names** | All of §1 | Every `person` field: `insured`, `claimant`, `life_assured`, `employee`, `donor`, `member`, `recipient`, `account_holder`, `taxpayer`, `student`, `full_name`, `child_name`, `borrower` | Scoping each answer to the right person (ADR 0011, ADR 0015) | `facts.value_text` and `facts.subject`, `chunks.text`, **and `person_aliases.alias`** | `facts` and `chunks` cascade. **The alias outlives the document.** `person_aliases.document_id` is `ON DELETE SET NULL`, so only the pointer back to the document is lost. |
| D4 | **Dates of birth** | Owner, members, children | `date_of_birth` on `identity_card`, `passport` and `birth_certificate`, and optionally on `policy_schedule` | Age, used in insurance advice only under recorded consent (ADR 0016, ADR 0017) | `facts.value_date`, `chunks` | Cascades with the document |
| D5 | **Income and employment** | Employees in the household | `payslip`: `employer`, `pay_period`, `gross_salary`, `cpf_employee`, `net_pay` | Tax-relief and protection-gap calculations (`packs/iras_tax`, `packs/insurance_agent`) | `facts`, `chunks` | Cascades with the document |
| D6 | **Tax and retirement** | Taxpayers and CPF/SRS members | `notice_of_assessment` (`assessable_income`, `tax_payable`), `cpf_statement`, `srs_statement` (`account_no`), `cpf_topup_receipt` (`member`, `recipient`), `donation_receipt`, `course_fee_receipt` | Relief room, reminders and explanation (`packs/iras_tax`) | `facts`, `chunks`, plus derived `obligations` | Cascades. `obligations.fact_id` cascades from `facts`. |
| D7 | **Insurance**: policy numbers, cover, premiums, claims | Insured persons, claimants, lives assured | `policy_schedule`, `renewal_notice`, `claim_letter` (`claim_no`, `incident_date`, `settled_amount`), `benefit_illustration`, `policy_anniversary_statement` | Renewal reminders, coverage questions, advice under consent | `facts`, `chunks`, `obligations` | Cascades with the document |
| D8 | **Health information** | Insured persons, claimants | **No field captures it.** A claim letter or a hospital-plan schedule may still *print* a diagnosis or an admission, and that text is chunked. **`unverified`**: whether the synthetic corpus contains any, and how often real ones would. | Not a purpose of the system. It arrives only because it is printed on a page. | `chunks.text` only, plus D1 | Cascades with the document |
| D9 | **Debt** | Borrowers | `loan_agreement`: `lender`, `facility_no`, `borrower`, `principal`, `monthly_repayment`, `agreement_date` | Questions like "what do I owe" and questions about penalties (ADR 0017) | `facts`, `chunks` | Cascades with the document |
| D10 | **Document metadata** | Inferred from the file | `documents.original_name`. The file name often names the person, as in `Marcus_Lim_Donation_Receipt_2023_001.pdf`. Telegram photos are renamed `telegram-photo-<unix time>.jpg`. | Display, de-duplication by `sha256` | `documents` | Only `DELETE_QUARANTINED`, and only for quarantined documents. See §4. |

### 2b. What the system creates about people

| # | Category | Whose | Purpose | Rests in | What deletes it today |
|---|---|---|---|---|---|
| S1 | **Household roster**: display name and relation to the owner | Owner, members, external people | Scoping answers. Some pack rules depend on relation, for example parent relief. | `people` (`0002_household.sql`, written by `core/household.py`) | **No delete statement exists for `people`.** `grep` finds `DELETE_ALIAS` and nothing else in `core/household.py`. |
| S2 | **Aliases**: every name string a document printed, mapped to a person, with the model's confidence | As S1 | Name resolution (ADR 0011) | `person_aliases` | `DELETE_ALIAS` removes one alias at a time (`core/household.py`). Deleting a person would cascade, but no code path deletes a person. |
| S3 | **Telegram chat identity**: chat id → person | Members who send documents from their phone | Attributing a document at capture, before it is parsed | `telegram_identities`; `document_attribution` | `document_attribution` cascades with the document. `telegram_identities` cascades only when the person is deleted, and nothing deletes a person (S1). |
| S4 | **Advice consent**: granted or withdrawn, the version, a hash of the wording, the channel and the time | The person who consented | Evidence that advice was given under recorded consent (ADR 0016) | `advice_consents` (`core/advice_consent.py`) | Cascades from `people` only, which nothing deletes. Withdrawing consent inserts a row and deletes none, by design. |
| S5 | **Advice record**: subject, person ids, verdict, the `basis` (the facts read and the figures computed) and the full `answer_text` | The advised person | Audit trail for every advised or withheld answer (ADR 0016) | `advice_records` (`core/advice_records.py`) | **Nothing.** It has no foreign key to `documents`, so it survives document deletion holding copies of the values. `consent_id` references `advice_consents` with no `ON DELETE`. That means deleting a person who has an advice record would be **refused** by the database, an inference from `0003_advice.sql` that is **`unverified`** by test. |
| S6 | **Correction trace**: `subject`, `key`, page, and the value before (`was`) and after (`now`) | Whoever the corrected fact was about | A labelled example for evaluation, and an audit of the human edit | `traces` (`core/corrections.py`) | **Nothing.** `traces` has no foreign key. The old and new values survive document deletion. |
| S7 | **Ingest and alert traces** | Indirectly | Evaluation and audit (`0001_init.sql` comment on `traces`) | `traces` (`core/ingest/pipeline.py`, `modules/alert/__init__.py`) | Nothing. The ingest payload holds counts and the names of unplaced fields, not values. The alert payload holds the metric's value, for example relief used. |
| S8 | **Conversation**: the questions asked and the answers given | The asker and anyone asked about | Answering within a thread | **In process memory only.** The checkpointer is `MemorySaver`, not `PostgresSaver` (`core/graph/answer.py` docstring and line ~1487). In the browser it lives in React state through `useChat`, and `grep` finds no `localStorage`/`sessionStorage` use in `web/`. | A restart of the API process clears the server copy, and closing the tab clears the browser copy. This changes when the Postgres checkpointer lands, which the docstring calls "the swap is one line". |
| S9 | **Process log lines** | Anyone named in an answer | Debugging | The console of the process. The answer gate logs the first 80 characters of every sentence it drops (`core/graph/answer.py`, `log.info("gate dropped ...")`), and a dropped sentence can contain a fact value. Whether any launcher writes these lines to a file is **`unverified`**. `grep` finds no `FileHandler` in `core/`, `api/` or `scripts/`. | Not retained by PARROT unless redirected. |
| S10 | **Screen passphrase verifier** (PBKDF2, not the passphrase) | The household | Locking the screens | `.parrot/lock.json` beside `web/` (`web/lib/lock.ts`, `PARROT_LOCK_FILE`) | Deleted by hand. The file's docstring describes doing that as the "forgot it" path. |

### 2c. Not personal data, listed so it is not mistaken for some

The following hold no household data:

- `grounding_sources` and `grounding_values` (published regulator pages)
- `packs` and `modules` (manifests)
- the evaluation sets under `eval/sets/` (questions over synthetic data)

---

## 3. Flow map: where data crosses a boundary

```
  phone ──Telegram cloud──┐           (crosses: image, file name, chat id)
                          ▼
  person ──copies file──▶ inbox/ ──poll──▶ worker ──▶ Docling parse ──▶ Ollama 127.0.0.1
                                     │                                   (classify, extract,
                                     │                                    embed, image pass)
                                     ▼
                         Postgres 127.0.0.1  ◀──  API 127.0.0.1  ◀──  Next.js 127.0.0.1  ◀── browser
                         (documents, chunks,       (answer graph,       (screen lock,
                          facts, people, …)          MemorySaver)          useChat state)
```

| Hop | Crosses the machine? | What crosses | Evidence |
|---|---|---|---|
| Folder capture | No | — | `core/adapters/folder.py` |
| **Telegram capture** | **Yes** | **The document image or file** passes through Telegram's servers. So does its original file name, if it was sent as a file. The bot's reply carries the file name ("Filed: {name}") and never an answer. With `TELEGRAM_DELETE_AT_SOURCE` (default on) the bot deletes the message after filing. What Telegram retains after that deletion is **`unverified`**. | `core/adapters/telegram.py` (`_capture`, `_say`, `_delete`, `_attachment`); `core/runtime/settings.py` (`telegram_delete_at_source`) |
| Telegram allow list | — | **If `TELEGRAM_CHAT_IDS` is empty, the bot accepts documents from any chat.** Anyone who finds the bot can put a file into the household's inbox. | `core/runtime/settings.py` (`_chat_ids`: "Empty means any chat") |
| Inference: generation, embedding, extraction, quarantine image pass | No | — The Ollama, Postgres and Redis URLs are refused at start-up unless they point at a loopback address. | `core/runtime/settings.py` (`local_url`) |
| Reranker | Model weights only, inbound | The first load downloads the cross-encoder from Hugging Face by model name. No household data is sent. | `core/retrieve/rerank.py` (`from_pretrained`); ADR 0018 |
| Docling | Possibly model weights, inbound | Whether Docling fetches its layout models over the network on first parse is **`unverified`**. | `core/ingest/parse.py` |
| Database and queue | No | Postgres and Redis are published on `127.0.0.1` only. | `infra/docker-compose.yml` (`ports`) |
| API | No | It binds `127.0.0.1` and answers any loopback request **without authentication**. | `scripts/run_parrot.py` (`--bind-address`); `api/main.py` (`TrustedHostMiddleware`) |
| Screens | No | `next dev -H 127.0.0.1`, changed in commit `3a624c5` ("Screens listen on this computer only"). This closes open question 4 of the earlier draft. | `web/package.json` (`dev`) |
| **git** | **Possibly** | **`inbox/` is committed to the repository** so the team can share synthetic specimens (`.gitignore` comment). On a developer's machine, a real document dropped into the inbox is one `git add -A` away from GitHub. | `.gitignore` |

**The claim the architecture diagram can make:** at inference and at rest, nothing leaves the
machine. **The claim it cannot make without qualification:** capture by Telegram sends the
document image through a third party. A team member's working copy of the repository is one
careless `git add` away from publishing a real document.

---

## 4. What `DELETE FROM documents` reaches, and what it does not

This section is the evidence the retention and erasure policy will rest on.

**There is no "Reset Workspace" in the code.** `grep -ri "reset.?workspace"` finds it only in
the task list. The single in-product deletion of a document is `forget()`
(`core/ingest/quarantine.py`), which runs `DELETE_QUARANTINED` (`core/ingest/sql.py`). It is
restricted to `status = 'quarantined'` on purpose: "an indexed document is evidence that answers
and reminders already cite, and removing that is not this statement's job". It refuses to run
while the file is still in the inbox. **An indexed document cannot be erased through PARROT
today.**

If a document row is deleted, by `forget()` or by hand:

| Reached (cascade) | Not reached |
|---|---|
| `chunks`: page text and embeddings | **The original file** in `inbox/` (D1) |
| `facts`, and `obligations` through `facts` | **`person_aliases.alias`**: the printed name stays, with `document_id` set to NULL (D3, S2) |
| `document_attribution` | **`people`** and **`telegram_identities`** (S1, S3) |
| | **`advice_records.answer_text` and `basis`**: copies of values (S5) |
| | **`traces`**: correction `was`/`now` values, alert values (S6, S7) |
| | Postgres WAL and any backup of `pgdata`. Whether any backup exists is **`unverified`**. |
| | Git history, if the file was ever committed from `inbox/` |
| | Telegram's servers, if it was captured that way (§3) |

---

## 5. Gaps found, for Christian

These are statements about the code. Each one needs a decision, and none can be closed by
wording in a policy.

1. **No erasure path for an indexed document, and none for a person.** `retention-and-erasure.md`
   cannot claim PDPA-style erasure until one exists. The minimum is a hand-written statement set
   that also clears S5 and S6 for the same `document_id` or person. Rule 1 applies.
2. **`advice_records.consent_id` has no `ON DELETE`.** Erasing a person who has been advised
   would fail. Fixing it is an `ALTER` and therefore a separate migration PR under rule 4.
3. **`traces` and `advice_records` copy values out of `facts`.** They are the audit trail, and they
   are also the copies an erasure misses. That needs a decision: redact on erasure, or keep and
   justify.
4. **An empty `TELEGRAM_CHAT_IDS` means any chat.** The safe default for a household vault is the
   reverse.
5. **`inbox/` is tracked by git.** Separating the household's working inbox from the committed
   specimens would remove the risk of publishing a real document.
6. **Health information can enter through page text** with no field or purpose behind it (D8).
7. **Folder capture records no submitter** (§1, "Lawful basis"). Deemed consent is argued from
   who submitted a document. For the main capture route, the code keeps no evidence of that.

## 6. Open questions for Siew

These are carried from the first draft unless marked new.

1. Telegram as a capture route for identity documents: is it acceptable with delete-at-source,
   or should identity documents be folder-only?
2. Identity values quoted in `traces` and `advice_records`: redact them, or keep them as the
   audit trail and cover them in the retention policy? (Checkpoints are in memory today, see S8.)
3. The lock is a screen lock, not encryption, and `web/lib/lock.ts` says so. Is that sufficient
   for identity numbers, which ADR 0017 calls the most sensitive data in the vault?
4. ~~Should the screens bind to loopback only?~~ **Closed.** They do since `3a624c5`.
5. ~~Which law applies to a household using its own copy?~~ **Decided 2026-10-01:** the PDPA
   applies, and the lawful basis is deemed consent (§1). The decision leaves these cases open:
   - **5a.** A member who submits *another* member's document, for example the owner filing a
     partner's passport. The person who acted is not the data subject. Does deemed consent cover
     this, or does it need the subject's own act?
   - **5b.** Children (`birth_certificate`, `relation = 'child'`). **Decided (Siew,
     2026-10-01):** for a child **under 13**, consent is given by a parent or guardian. In
     PARROT that is the parent who files the child's document.
     *Source:* the PDPC's advisory guidelines on minors, confirmed by Siew on 2026-10-01. The
     13-year threshold is PDPC guidance, not the text of the Act, which sets no age. The
     chapter number and the guidelines' revision date are still to be added when the
     reference list is compiled.
     **Decided (Siew, 2026-10-01):** children aged **13 to 17** cannot consent for themselves
     in PARROT. A parent must file the document. So the rule is that **every child under 18
     needs a parent's filing.** This is a decision for PARROT. It may be stricter than the PDPC
     guidance requires for 13- to 17-year-olds. When the guidelines are cited, state that this
     is a deliberate choice, so it does not read as a misquotation of them.
     *Still open:* the evidence. Nothing records which parent filed a
     child's document, or that it was filed as a parent (gap 7, folder capture). The child's
     date of birth is held (`birth_certificate.date_of_birth`, D4), so the age at filing could
     be computed, but no code does it.
   - **5c.** Third parties printed on a document (§1, row 3), such as a landlord or the other
     driver in a claim. They submitted nothing, so deemed consent by their own conduct cannot
     apply. Is there another basis, or should their data be minimised?
   - **5d.** Purpose. Deemed consent covers the purpose the data was submitted for. Is
     "answering questions about the household's documents" one purpose, or are reminders,
     alerts and advice separate ones? Advice already has explicit consent (S4).
6. *(new)* **NRIC numbers.** The PDPC published advisory guidelines on NRIC and other national
   identification numbers in 2018. They have **not been read**. Check whether they bear on a
   household tool, or only on organisations collecting from customers.
7. *(new)* Is a third party's personal data that arrives on a household document (§1, row 3) in
   scope for the retention policy? `people.external` keeps it deliberately.
