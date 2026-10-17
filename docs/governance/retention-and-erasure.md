# Retention and erasure policy

> **Status: Siew's decisions complete (2026-10-02); ready for Christian's technical review.**
> Owner: Siew.
> Started 2026-10-02 and checked against the code on `main` at `fc035bd` plus this branch.
>
> Part A is policy: how long each kind of data is kept and what erasing it means. Part B is
> what the code does today. Part C is what has to be built for Part A to be true. Every claim
> about the code points at a file.

**The short version.** Today PARROT keeps everything until someone deletes it by hand. The
only deletion it offers is for a document that failed to be read. **"Reset Workspace" does not
exist.** This policy says what it must do, and the policy cannot be met until it is built.

---

## Basis

- **Why the PDPA is used here.** A household's own use is outside the PDPA (domestic
  capacity). PARROT is designed to its standards anyway, and the team is bound in full for its
  own work (`data-inventory.md` §1, "two capacities", Siew, 2026-10-05).
- **No general right to erasure.** As the team understands it, the PDPA has no general right to
  erasure comparable to GDPR Article 17 (from the 2026-10-04 draft on `main`, **to confirm**).
  So this policy does not claim to "satisfy PDPA erasure". It says it **meets the Retention
  Limitation Obligation, and gives the household a working erase-on-request** (A3–A5), as the
  standard PARROT holds itself to.
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
| Documents, and everything read from them: the original file, page text and embeddings, facts, and reminders derived from them | D1–D10 | **Kept until the User erases the document, or resets the workspace.** A document stays useful for as long as it is on file. A policy that has lapsed still answers "what was I covered for", so lapsing is not a reason to delete. | **Decided** (Siew, 2026-10-02) |
| Household roster and the names each person goes by | S1, S2 | Kept until the person is erased, or the workspace is reset. | **Decided** (Siew, 2026-10-02) |
| Telegram chat → person mapping | S3 | Kept until the person is erased, the chat is removed from `TELEGRAM_CHAT_IDS`, or the workspace is reset. | **Decided** (Siew, 2026-10-02) |
| Advice consent (granted and withdrawn) | S4 | Kept for as long as any advice record that relies on it is kept. Without it, an advice record cannot show it was lawful. | **Decided** (Siew, 2026-10-02) |
| Advice records | S5 | **Erased with the document and the person it was about.** An advice record is erased in full, within the same 72 hours (A4), when any document it relied on is erased or the person it was about is erased. No skeleton or audit copy is kept. *Exception: the incident hold (A6).* | **Decided** (Siew, 2026-10-02; option (a)) |
| Correction, ingest and alert traces | S6, S7 | Erased with the document they concern (correction traces carry the old and new value). Traces with no document are kept until reset. *Exception: the incident hold (A6).* | **Decided** (Siew, 2026-10-02) |
| The conversation | S8 | Not retained. It is held in process memory and lost when the API restarts (`MemorySaver`). **If the Postgres checkpointer is ever adopted, this rule must be decided again before it ships.** | Holds today |
| Process log lines | S9 | Not retained by PARROT. No log file is written. | Holds today, `unverified` for every launcher |
| Screen-lock verifier | S10 | Kept until the household changes or clears the passphrase. | **Decided** (Siew, 2026-10-02) |
| The 40-document real holdout (team members) | — | Governed by `consent-and-redaction.md` §8: proposed deletion within 7 days of the final report's submission. | **Proposed** (protocol drafted 2026-10-17) |

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
| **Erase a document** | One document and everything derived from it (A2). Any document, not only a quarantined one. | **Decided (A4).** Not built: today only quarantined documents can be erased. |
| **Erase a person** | A household member or third party, their aliases and chat mapping, their advice consents and advice records. Their documents are erased too, if the User chooses. | **Decided (A5).** Not possible today. |
| **Reset Workspace** | Everything in Part A1 at once. PARROT is returned to its state before first use. | **Decided (A5).** Not built. |

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

**Confirmation wording** (approved by Siew, 2026-10-02; incident line added 2026-10-05; the screen is Zee's):

> **Delete "{file name}"?**
> This document and everything PARROT has read from it will be completely erased from PARROT
> within 72 hours (3 days). It cannot be recovered.
> PARROT cannot erase copies held outside it: a photo sent through Telegram, or a backup of
> this computer.
> If this document is part of an open incident investigation, its records will be erased when
> the investigation closes.
> **[Cancel]  [Delete]**

The last sentence of the wording is there because of A2. "Completely erased from PARROT" is
true only if the User is also told what PARROT cannot reach.

4. **Withdrawn at once.** *(Decided, Siew, 2026-10-02.)* As soon as the User confirms, the
   document stops being used in answers, reminders, alerts and advice. The 72 hours is only
   the time allowed to finish erasing it.

### A5. Erasing a person, and resetting the workspace

> **Decided (Siew, 2026-10-02).**

1. **Same three rules as A4.** A person is erased, and the workspace is reset, **only on the
   User's instruction**, **after confirmation**, and **completely within 72 hours**. What is
   erased is **withdrawn from use as soon as the User confirms**.
2. **A person's documents are an explicit choice.** The confirmation lists the documents the
   person appears on. The User chooses either to erase them too, or to keep them, and is told
   that the person's details will remain in them. Erasing a person while keeping their
   documents does not erase their details from those documents' page text (`chunks.text`).
   The confirmation must not imply otherwise.
3. **Shared documents are marked.** A document that is also about another household member
   is marked as shared in that list. It is not erased unless the User selects it.
4. **The owner is erased only by Reset Workspace.** The database allows exactly one owner
   (`db/migrations/0002_household.sql`, `people_one_owner`), and every first-person answer is
   scoped to them. Erasing the owner alone is not offered.
5. **Reset needs a stronger confirmation.** The User types `RESET` to confirm, because a reset
   is wider than any other action and cannot be undone.
6. **Only the owner.** *(Decided, Siew, 2026-10-02.)* Only the owner may erase a person or
   reset the workspace. Any User may still delete a document (A4). A household member who
   wants to be removed must ask the owner.

**Confirmation wording** (approved by Siew, 2026-10-02; incident line added 2026-10-05; the screens are Zee's):

> **Remove Rachel from PARROT?**
> Her names, chat link, advice consents and advice records will be completely erased from
> PARROT within 72 hours (3 days).
> **She appears on 6 documents.** [Erase them too] [Keep them — her details will remain in
> those documents]
> If any of this is part of an open incident investigation, those records will be erased when
> the investigation closes.
> **[Cancel]  [Remove]**

> **Reset PARROT?**
> Every document, everyone in your household, and everything PARROT has learned will be
> completely erased from PARROT within 72 hours (3 days). This cannot be undone.
> PARROT cannot erase copies held outside it: photos sent through Telegram, files committed to
> git, or backups of this computer.
> If any of this is part of an open incident investigation, those records will be erased when
> the investigation closes.
> **Type RESET to confirm.**  **[Cancel]  [Reset]**

### A6. Incident hold

> **Decided (Siew, 2026-10-05).** This reconciles the erasure rules with the MGF for Agentic
> AI's "ensure log immutability" (v1.5, p 44). See `imda-what-applies.md`, finding 5.

1. **Evidence is kept only while an incident is open.** When an incident is recorded under
   `incident-and-breach-procedure.md`, the records that are its evidence are **held**: the
   traces, advice records and attribution rows that show what happened. They are not erased
   while the incident is open.
2. **Otherwise, erase as this policy says.** When the incident is closed, held records are
   erased under A1, A4 and A5. Any erasure the User confirmed during the hold is completed then.
   Records that are not evidence of an open incident are never held.
3. **What a hold does not change.** A held document is still **withdrawn from use at once**
   when the User confirms deletion (A4 point 4). Only its evidence is kept, and only for the
   incident. The incident log never contains personal data, so it is not itself held data.

**The 72-hour promise under a hold: decided (Siew, 2026-10-05).** Option 1 was adopted: each
confirmation now says that records forming part of an open incident investigation are erased
when the investigation closes (A4, A5). The promise of erasure within 72 hours therefore holds
in every case. The line is on the person and reset screens as well as the document screen,
because both can erase held records.

---

## Part B. What the code does today

### B1. The only erasure paths that exist

| Path | Reaches | Limits | Evidence |
|---|---|---|---|
| **Forget a quarantined document**: `DELETE /quarantine/{document_id}` (`api/routes.py`, `forget_one`) | One `documents` row, and by cascade its `chunks`, `facts`, `obligations` and `document_attribution` | **Quarantined documents only:** "an indexed document is evidence that answers and reminders already cite". Refused **with a 409** while the file is still in the inbox, because the folder watcher would re-register it within a minute. **It deletes no file.** | `core/ingest/quarantine.py` (`forget`); `core/ingest/sql.py` (`DELETE_QUARANTINED`) |
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
| The job queue (Redis) | Per job: the document id, digest, MIME type and **original file name**. Never the file itself. **Task results expire after 1 hour** (`result_expires=3600`). Whether Redis writes a snapshot to disk is **`unverified`**. The compose file mounts no volume for Redis, so its data lasts as long as the container. | `core/worker/tasks.py` (`send`); `core/worker/app.py` (`result_expires`); `infra/docker-compose.yml` |
| Backups | **None are taken by the stack.** `infra/docker-compose.yml` defines one volume and no backup service. A backup the household takes itself is outside PARROT's reach (A2), and the reset confirmation says so. | `infra/docker-compose.yml` |
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
2. **Erase a person (A5)**, on confirmed instruction, complete within 72 hours, withdrawn
   from use at once. It must list the person's documents with shared ones marked, and erase
   only those the User selects. It must refuse the owner. This needs
   `advice_records.consent_id` to allow deletion (today it has no `ON DELETE`, so the
   database would refuse). That is an `ALTER`, which needs its own migration PR (rule 4).
   Which documents a person "appears on" has to be decided in code: through `facts.subject`
   resolved by their aliases, `document_attribution`, or both.
3. **Reset Workspace (A5)**, confirmed by typing `RESET`, complete within 72 hours.
   **Owner only**, like erasing a person (A5 point 6). Every table
   in A1, every file in the watched folder, the queue, and the lock verifier. Then a check that
   the database is empty, which Siew's sign-off can cite.
4. **Owner-only check (A5 point 6).** PARROT cannot tell today who is at the screen. There
   is one passphrase per household (`web/lib/lock.ts`), and the API answers any loopback
   request without authentication (`data-inventory.md` §3). Erasing a person and resetting
   therefore need a way to confirm the owner is the one acting, such as an owner-only
   passphrase asked for at that moment. The check has to sit in the API as well as on the
   screen, or calling the API directly gets round it. This is for Christian and Zee to design.
5. **A test for each**, using corpus fixtures with known ground truth (AGENTS.md, definition of
   done). Without a test, this policy can only point at intent.
6. **The confirmation screens (A4, A5).** Document, person and reset, each with the 72 hours,
   what is out of reach, and A5's document choice and typed `RESET`. The reset screen must also
   name git history (A2). Screens are Zee's work in `web/`.
7. **No automatic deletion (A4, A5).** No scheduled job may delete a document, erase a person
   or reset. This is a rule for any future module, and worth a test.
8. **Incident hold (A6).** A way to mark records as held for an open incident, so that
   erasure skips them until the hold is released, and then completes. Held records need no new
   copy: the hold only defers their erasure.

---

## Decisions for Siew

1. ~~**Advice records (S5):** erased with the document and person, or kept for a fixed audit
   period?~~ **Decided 2026-10-02:** option (a). They are erased in full with the document or
   person (A1).
2. ~~**The proposed rules in A1.**~~ **Confirmed 2026-10-02:** kept until erased or reset, as
   stated in A1.
3. ~~**Lapsed documents:** keep until erased, or erase automatically?~~ **Decided
   2026-10-02 (A4):** never deleted automatically.
4. **Section 25:** quote the operative wording into "Basis" once it can be read from the Act.
5. ~~**During the 72 hours:** does the document stop being used at once?~~ **Decided
   2026-10-02 (A4 point 4):** yes, as soon as the User confirms.
6. ~~**Persons and Reset Workspace:** do the same rules apply?~~ **Decided 2026-10-02 (A5):**
   yes, with the four additions.
7. ~~**Advice records and the 72 hours.**~~ Settled by Decision 1, option (a): nothing is
   kept, so nothing needs redacting.
8. ~~**Who may instruct erasing a person, or a reset?**~~ **Decided 2026-10-02 (A5 point 6):**
   only the owner.
9. ~~**Approve the wording** in A4 and A5.~~ **Approved 2026-10-02.**
