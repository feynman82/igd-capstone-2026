# Retention and erasure policy

> **Status: draft for Siew's decisions and Christian's technical review.** Owner: Siew.
> Started 2026-10-02 and checked against the code on `main` at `fc035bd` plus this branch.
>
> Part A is policy: how long each kind of data is kept and what erasing it means. Part B is
> what the code does today. Part C is what has to be built for Part A to be true. Every claim
> about the code points at a file. Rules marked **Proposed** are for Siew to decide.

**The short version.** Today PARROT keeps everything until someone deletes it by hand. The
only deletion it offers is for a document that failed to be read. **"Reset Workspace" does not
exist.** This policy says what it must do, and the policy cannot be met until it is built.

---

## Basis

- **PDPA 2012, Part 6, section 25 (retention limitation).** The Part and section numbers are
  still to be confirmed. The section has *not* yet been quoted from the Act for this document,
  so it is not paraphrased here. The quote and the revised-edition
  date are to be added from Singapore Statutes Online, which this environment cannot reach.
- **Purpose.** The purpose the data is kept for is Clause B of `terms-of-use.md` (approved by
  Siew, 2026-10-02): to help the User's household understand and keep track of its own
  documents. A retention rule below is justified by that purpose or by an audit need, and by
  nothing else.
- **What is held.** The categories (D1 to D10, S1 to S10) and where each rests are defined in
  `data-inventory.md` §2. They are referred to here by those codes.

---

## Part A. Policy

### A1. Retention rules

| Data | Codes | Rule | Status |
|---|---|---|---|
| Documents, and everything read from them: the original file, page text and embeddings, facts, and reminders derived from them | D1–D10 | **Kept until the User erases the document, or resets the workspace.** A document stays useful for as long as it is on file. A policy that has lapsed still answers "what was I covered for", so lapsing is not a reason to delete. | **Proposed** |
| Household roster and the names each person goes by | S1, S2 | Kept until the person is erased, or the workspace is reset. | **Proposed** |
| Telegram chat → person mapping | S3 | Kept until the person is erased, the chat is removed from `TELEGRAM_CHAT_IDS`, or the workspace is reset. | **Proposed** |
| Advice consent (granted and withdrawn) | S4 | Kept for as long as any advice record that relies on it is kept. Without it, an advice record cannot show it was lawful. | **Proposed** |
| Advice records | S5 | **Erased with the document and the person it was about.** An advice record is erased in full, within the same 72 hours (A4), when any document it relied on is erased or the person it was about is erased. No skeleton or audit copy is kept. | **Decided** (Siew, 2026-10-02; option (a)) |
| Correction, ingest and alert traces | S6, S7 | Erased with the document they concern (correction traces carry the old and new value). Traces with no document are kept until reset. | **Proposed** |
| The conversation | S8 | Not retained. It is held in process memory and lost when the API restarts (`MemorySaver`). **If the Postgres checkpointer is ever adopted, this rule must be decided again before it ships.** | Holds today |
| Process log lines | S9 | Not retained by PARROT. No log file is written. | Holds today, `unverified` for every launcher |
| Screen-lock verifier | S10 | Kept until the household changes or clears the passphrase. | **Proposed** |
| The 40-document real holdout (team members) | — | Governed by `consent-and-redaction.md`, **which does not exist yet**. Not covered here. | **Open** |

### A2. What erasure means

Erasure must remove the data from **everything PARROT controls**:

- the database, including every copy of a value held outside `facts`;
- the file in the watched folder;
- any queue or cache the system keeps.

Erasure **cannot** remove data from places PARROT does not control. These must be **stated to
the User, not implied away**:

- Telegram's servers, for anything captured by Telegram (`data-inventory.md` §3);
- a git history the file was committed to;
- a backup the household took of its own computer.

### A3. Three ways to erase

| Erasure | What it removes | Status |
|---|---|---|
| **Erase a document** | One document and everything derived from it (A2). Any document, not only a quarantined one. | **Proposed.** Today only quarantined documents can be erased. |
| **Erase a person** | A household member or third party, their aliases and chat mapping, and the records about them. Their documents are erased too, if the User chooses. | **Proposed.** Not possible today. |
| **Reset Workspace** | Everything in Part A1 at once. PARROT is returned to its state before first use. | **Proposed.** Not built. |

### A4. Deleting a document: only on instruction, confirmed, and complete within 72 hours

> **Decided (Siew, 2026-10-02).**

1. **Only on the User's instruction.** PARROT never deletes a document unless the User has told
   it to. No document is deleted automatically: not on expiry, not on lapse, and not by any
   scheduled job.
2. **Confirmed before it happens.** When the User asks to delete a document, PARROT asks them
   to confirm before deleting anything. The confirmation tells them that the document will be
   completely erased from PARROT within **72 hours (3 days)**.
3. **Complete within 72 hours.** Within 72 hours of the User confirming, the document and
   everything derived from it is erased from everything PARROT controls (A2). That includes the
   file in the watched folder and the copies listed in B2.

**Suggested confirmation wording** (drafted for Siew to approve; the screen is Zee's):

> **Delete "{file name}"?**
> This document and everything PARROT has read from it will be completely erased from PARROT
> within 72 hours (3 days). It cannot be recovered.
> PARROT cannot erase copies held outside it: a photo sent through Telegram, or a backup of
> this computer.
> **[Cancel]  [Delete]**

The last sentence of the wording is there because of A2. "Completely erased from PARROT" is
true only if the User is also told what PARROT cannot reach.

4. **Withdrawn at once.** *(Decided, Siew, 2026-10-02.)* As soon as the User confirms, the
   document stops being used in answers, reminders, alerts and advice. The 72 hours is only
   the time allowed to finish erasing it.

---

## Part B. What the code does today

### B1. The only erasure paths that exist

| Path | Reaches | Limits | Evidence |
|---|---|---|---|
| **Forget a quarantined document** | One `documents` row, and by cascade its `chunks`, `facts`, `obligations` and `document_attribution` | **Quarantined documents only:** "an indexed document is evidence that answers and reminders already cite". Refused while the file is still in the inbox, because the folder watcher would re-register it within a minute. **It deletes no file.** | `core/ingest/quarantine.py` (`forget`); `core/ingest/sql.py` (`DELETE_QUARANTINED`) |
| **Remove one alias** | One `person_aliases` row | One name string at a time | `core/household.py` (`DELETE_ALIAS`) |
| **Re-read a document** | Replaces that document's `chunks` and `facts` | Not an erasure. The document row is kept on purpose, so citations survive. | `core/ingest/sql.py` (`DELETE_CHUNKS`, `DELETE_FACTS`); `core/ingest/pipeline.py` |

**No statement deletes from `people`, `telegram_identities`, `advice_consents`,
`advice_records` or `traces`.** `grep` of `core/`, `api/`, `modules/` and `scripts/` finds none.

### B2. What deleting a `documents` row cascades to, and what it leaves

From the foreign keys in `db/migrations/0001_init.sql`, `0002_household.sql` and
`0003_advice.sql`:

| Removed with the document | **Left behind** |
|---|---|
| `chunks` (page text and embeddings) | **The original file** in `inbox/` |
| `facts`, and through them `obligations` | **`person_aliases.alias`**: the name stays, and its `document_id` is set to NULL |
| `document_attribution` | **`advice_records`** (`answer_text`, `basis`): copies of the values, with no foreign key to the document |
| | **`traces`**: a correction's `was` and `now` values, and alert values; no foreign key |
| | `people`, `telegram_identities`, `advice_consents` |

### B3. Things erasure has to reach beyond the database

| Where | What is there | Evidence |
|---|---|---|
| The watched folder | The original file. Telegram captures are written here too. | `core/runtime/settings.py` (`_folder`); `core/adapters/telegram.py` (`_write_local_copy`) |
| The job queue (Redis) | Per job: the document id, digest, MIME type and **original file name**. Never the file itself. Whether Redis writes a snapshot to disk is **`unverified`**. The compose file mounts no volume for Redis, so its data lasts as long as the container. | `core/worker/tasks.py` (`send`); `infra/docker-compose.yml` |
| Postgres storage | A deleted row is not overwritten at once. It stays in the table files until Postgres reclaims the space, and in its write-ahead log. This is standard Postgres behaviour, **`unverified`** for this deployment. Whether erasure should force reclamation is a question for Christian. | `infra/docker-compose.yml` (`pgdata` volume) |
| The repository | `inbox/` is tracked by git (`.gitignore`). A real document committed there survives in history, whatever PARROT deletes. | `.gitignore` |

### B4. Does today's system meet Part A?

**No.** An indexed document cannot be erased, a person cannot be erased at all, there is no
reset, and even the one erasure that exists leaves the file and four kinds of copy behind.
The governance chapter must say so plainly. Claiming the PDPA erasure point on the strength of
`ON DELETE CASCADE` alone would assert something the code does not do.

---

## Part C. What must be built (for Christian)

Each item is code or schema, so none of it is Siew's to build. Rule 1 (hand-written SQL in
named statements) and rule 4 (migrations reviewed separately) apply.

1. **Erase a document**, for any status, **only on the User's confirmed instruction (A4)**.
   One transaction that deletes the `documents` row (cascade does the rest), deletes that
   document's `traces`, deletes **every `advice_records` row that relied on it** (A1), and
   removes the file from the watched folder. Those advice rows can be found because each
   figure in `basis.inputs` carries the `document_id` it came from (`core/graph/answer.py`,
   `_advice_basis`). There is no foreign key to follow, so the statement has to match on that
   field. Removing the file is what stops the watcher reading it again.
   Today's refusal while the file is still in the inbox exists for exactly this reason.
   **Everything must be complete within 72 hours of the confirmation.** That includes
   whatever is needed for Postgres to stop holding the deleted rows (B3), if Christian
   confirms that it does. A record of when each erasure was confirmed and when it finished
   would let Siew's sign-off show the 72 hours being met. It must not record what the
   document contained. **From the moment of confirmation, the document must be excluded from
   retrieval, facts read by modules, reminders and alerts (A4 point 4)**, even if the physical
   erasure runs later.
2. **Erase a person.** This needs `advice_records.consent_id` to allow deletion (today it has
   no `ON DELETE`, so the database would refuse). That is an `ALTER`, which needs its own
   migration PR (rule 4).
3. **Reset Workspace.** Every table in A1, every file in the watched folder, the queue, and the
   lock verifier. Then a check that the database is empty, which Siew's sign-off can cite.
4. **A test for each**, using corpus fixtures with known ground truth (AGENTS.md, definition of
   done). Without a test, this policy can only point at intent.
5. **The confirmation screen (A4).** Ask before deleting, state the 72 hours, and name what
   is out of reach (Telegram, the household's own backups). The erase and reset screens must
   also name git history (A2). Screens are Zee's work in `web/`.
6. **No automatic deletion (A4).** No scheduled job may delete a document. This is a rule for
   any future module, and worth a test.

---

## Decisions for Siew

1. ~~**Advice records (S5):** erased with the document and person, or kept for a fixed audit
   period?~~ **Decided 2026-10-02:** option (a). They are erased in full with the document or
   person (A1).
2. **The proposed rules in A1:** confirm, change, or set fixed periods instead of "until
   erased or reset". *(For documents, settled by A4: kept until the User instructs deletion.)*
3. ~~**Lapsed documents:** keep until erased, or erase automatically?~~ **Decided
   2026-10-02 (A4):** never deleted automatically.
4. **Section 25:** quote the operative wording into "Basis" once it can be read from the Act.
5. ~~**During the 72 hours:** does the document stop being used at once?~~ **Decided
   2026-10-02 (A4 point 4):** yes, as soon as the User confirms.
6. **Persons and Reset Workspace:** do the same rules apply (confirmation, 72 hours, only on
   instruction)?
7. ~~**Advice records and the 72 hours.**~~ Settled by Decision 1, option (a): nothing is
   kept, so nothing needs redacting.
