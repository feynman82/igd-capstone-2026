# Retention and erasure policy

Status: draft · Owner: Siew · Reviewer: Christian (technical accuracy)

> Every claim below points at a file. Anything that could not be traced is marked
> **unverified** and repeated in [Open questions](#open-questions). Statements about the
> PDPA are marked **to check against the statute** until they have been checked against the
> text on Singapore Statutes Online; this draft does not quote the Act.

## The finding to read first

**No "Reset Workspace" exists in the code at 2026-10-04 (`main` at `bac3afa`).** Searching
`api/`, `core/`, `scripts/` and `web/` finds no endpoint, script or button by that name. The
only deletion path for a document is narrower:

- `DELETE /quarantine/{document_id}` (`api/routes.py`), which calls `quarantine.forget`
  (`core/ingest/quarantine.py`), which runs `DELETE_QUARANTINED` (`core/ingest/sql.py`).
- That statement deletes only a row with `status = 'quarantined'`. Its comment says this is
  deliberate: an indexed document is evidence that answers and reminders cite.
- It is refused with a 409 while the file is still in the inbox, because capture would
  register the file again within a minute.

So at present **an indexed document cannot be erased through the product.** That is the
central gap in this policy. It is a code change, not a governance one, and it belongs to
Lane A (see [What has to be built](#what-has-to-be-built)). The rest of this document is
written so that it is true today and says what would make it true for a full reset.

## Scope and legal frame

v1 is a single-household assistant on one computer. Every service URL must be loopback,
and `core/runtime/settings.py` rejects anything else (`infra/.env.example`). Nothing in
this policy depends on a network mode, because there is none.

**To check against the statute:**

- *Domestic exclusion.* As we understand it, the PDPA 2012 does not place its data
  protection obligations on an individual acting in a personal or domestic capacity. On
  that reading, a household running Parrot for itself may fall outside the Act. If so, this
  policy is the standard we hold ourselves to, not a compliance claim. **Check the exact
  section before stating this in the report.**
- *Retention Limitation Obligation.* Stop keeping personal data, or remove the means of
  associating it with an individual, once the purpose is no longer served and there is no
  legal or business need to keep it.
- *Protection Obligation.* Make reasonable security arrangements for personal data in
  one's possession or under one's control.
- *There is no general right to erasure in the PDPA* comparable to GDPR Article 17, as we
  understand it. The task wording ("satisfies PDPA erasure") should therefore read:
  "satisfies the Retention Limitation Obligation, and gives the household a working
  erase-on-request". **Confirm before the report uses either phrase.**

Our position: the household is the data subject and the user. The purpose of retention is
"answering this household's questions about its own documents". When the household asks
to stop, that purpose ends and everything derived from its documents should go.

## Where personal data rests

| # | Store | What it holds | Personal data? | Evidence |
|---|---|---|---|---|
| 1 | Watched folder (`./inbox` by default) | The original files. The **only** copy: nothing is copied into the database | Yes: the documents themselves | `infra/.env.example`, `WATCH_FOLDER` |
| 2 | `documents` | Hash, original filename, MIME type, page count, doc type, status, quarantine reason | Yes: filenames often carry names | `db/migrations/0001_init.sql` |
| 3 | `chunks` | Page text and its embedding | Yes | `0001_init.sql` |
| 4 | `facts` | Extracted values (amounts, dates, ID numbers) and `subject`, the name as printed | Yes | `0001_init.sql`; ID types per ADR 0017 |
| 5 | `obligations` | Due dates and labels derived from facts | Yes, indirectly | `0001_init.sql` |
| 6 | `people`, `person_aliases`, `telegram_identities`, `document_attribution` | Household members, the names documents printed for them, Telegram chat ids | Yes | `db/migrations/0002_household.sql` |
| 7 | `advice_consents`, `advice_records` | Consent decisions; every advice answer with its `basis` snapshot and `answer_text` | Yes | `db/migrations/0003_advice.sql`, `core/advice_records.py` |
| 8 | `traces` | One line per ingest or correction. Correction traces keep `subject`, `was` and `now`; ingest traces keep `unplaced` field labels | Yes, for corrections. **Unverified** for ingest: depends on whether `unplaced` labels carry values | `core/corrections.py`, `core/ingest/pipeline.py`, `core/ingest/extract.py` |
| 9 | Redis (Celery broker and result backend) | Task kwargs: document id, digest, MIME type, **original filename**. No file bytes. Results expire after 3600 s | Filenames only | `core/worker/tasks.py`, `core/worker/app.py` (`result_expires=3600`) |
| 10 | LangGraph checkpointer | Conversation state in process memory (`MemorySaver`); gone on restart | Yes, but transient | `core/graph/answer.py` |
| 11 | Telegram | Media is downloaded into the inbox, then deleted from the chat | Transient on Telegram's servers | `core/adapters/telegram.py` docstring. **Unverified**: that deletion succeeds on every path, including a failed download |
| 12 | Postgres volume `pgdata` | Everything in rows 2–8, on the host disk | Yes | `infra/docker-compose.yml` |
| 13 | Process logs | stdout via `logging.basicConfig`; no file handler found | Possibly filenames and ids | `scripts/*.py`. **Unverified**: whether a launcher redirects stdout to a file |

Not personal data: `packs`, `modules`, `grounding_sources`, `grounding_values` (published
regulator figures), and `obligations` with `fact_id IS NULL` (pack-level deadlines such as
a filing date).

## Retention periods

| Data | Kept for | Why |
|---|---|---|
| Original file in the inbox | Until the household removes it | The inbox is the document store; Parrot never deletes a file (no code path found that unlinks one) |
| `documents` and everything derived from it (rows 2–5, `document_attribution`) | Until the document is erased | Needed to answer and to cite the page |
| Derived rows on re-ingest | Replaced, not accumulated | `DELETE_CHUNKS`, `DELETE_FACTS` in `core/ingest/sql.py`. The document row and its id survive, so citations stay valid |
| Household roster and aliases | Until the person is removed | Scopes every first-person answer (ADR 0011) |
| `advice_consents`, `advice_records` | Indefinitely, today | The record of what was advised and under which consent (ADR 0016). **A period needs deciding**: see open questions |
| `traces` | Indefinitely, today | Evaluation dataset and audit trail (`0001_init.sql` comment). **A period needs deciding** |
| Redis task results | 1 hour | `result_expires=3600` |
| Conversation state | The life of the process | `MemorySaver` |
| Synthetic corpus | Not personal data | `documents.synthetic`; `docs/governance/synthetic-data-case.md` |
| Real-document holdout | Governed by the consent and redaction protocol, not by this policy | The protocol is not yet written. It must exist before collection |

## The erasure path: what `DELETE FROM documents` reaches

Read from the foreign keys in `db/migrations/`. Deleting one `documents` row:

| Table | Effect | Why |
|---|---|---|
| `chunks` | **Deleted** | `document_id … ON DELETE CASCADE` (0001) |
| `facts` | **Deleted** | `document_id … ON DELETE CASCADE` (0001) |
| `obligations` | **Deleted** where derived from those facts | `fact_id … ON DELETE CASCADE` (0001) |
| `document_attribution` | **Deleted** | `document_id … ON DELETE CASCADE` (0002) |
| `person_aliases` | **Kept**; `document_id` set to NULL. The alias and its answer remain | `ON DELETE SET NULL` (0002) |
| `traces` | **Kept**. `thread_id` is the document id as text, with no foreign key | `core/ingest/pipeline.py`, `core/corrections.py` |
| `advice_records` | **Kept**. `basis` and `answer_text` may quote the deleted facts | No foreign key to `documents` (0003) |
| The file in the inbox | **Kept**. And while it is there, capture registers it again | `core/ingest/quarantine.py`, `StillInInbox` |
| The HNSW and GIN indexes | Entries removed with the rows. Dead tuples persist on disk until vacuum | Postgres behaviour. **Unverified** for this deployment |

Deleting a `people` row cascades to `person_aliases`, `telegram_identities`,
`document_attribution` and `advice_consents`. But `advice_records.consent_id` references
`advice_consents(id)` with no `ON DELETE` clause. **So deleting a person who has received
advice will fail**, unless their `advice_records` are deleted first (0003). That is
correct for an audit trail and wrong for an erasure request. It needs a decision.

## Policy

1. **Erase a document.** Remove the file from the inbox, then delete the `documents` row.
   Chunks, facts, derived obligations and attribution go with it. Today this is possible
   only for a quarantined document.
2. **Reset the workspace.** Remove every file from the inbox and delete every row in the
   tables in rows 2–8 above, including `traces` and `advice_records`, then restart the
   worker and the server. This empties Redis results and in-memory conversation state.
   Packs, modules and grounding values stay. **Not implemented**: see below.
3. **Forget a person.** Delete their `advice_records`, then their `people` row. Facts whose
   `subject` prints their name are *not* touched, because `subject` is the string the page
   printed. Erasing a person fully means erasing the documents about them.
4. **Corrections.** A correction overwrites the fact. The before-and-after values stay in
   `traces`, so they fall under rule 2, not rule 1.
5. **Backups.** None are taken by the stack (`infra/docker-compose.yml` defines one volume
   and no backup service). If a household takes one, it is outside this policy's reach. The
   policy should say so to them in plain words.

## What has to be built

Code changes. This artefact does not make them; they go to Lane A as a request.

| Need | Why | Touches |
|---|---|---|
| A Reset Workspace endpoint and button | Rule 2 has no implementation | `api/routes.py`, `core/ingest/sql.py`, `web/` |
| Erase an *indexed* document | Rule 1 works only for quarantined documents | `core/ingest/sql.py` (a new hand-written statement, rule 1 of AGENTS.md) |
| Erase traces and advice records for a document or a person | They outlive the document today | Statements by `thread_id` and `subject_person_ids`. No schema change needed |
| A decision on `advice_records.consent_id` | Blocks forgetting a person | A migration if the answer is `ON DELETE CASCADE`, so a separate reviewed PR (CLAUDE.md) |

## Open questions

For Christian unless marked otherwise.

1. Is a Reset Workspace planned for v1, or should the policy describe the manual SQL path
   instead? The task assumes it exists.
2. Do ingest-trace `unplaced` labels contain extracted values, or only field names?
   (`core/ingest/extract.py` lines 383–415 append `item.label`.)
3. Does the Telegram adapter delete the chat message on every path, including a failed
   download?
4. Does any launcher (`START.cmd`, `scripts/run_parrot.py`) write logs to a file?
5. Retention periods for `traces` and `advice_records`: indefinite, or a fixed period? For
   Siew and Yew Mun, because traces are also the evaluation dataset.
6. Should forgetting a person delete their advice records, or keep them anonymised?
7. For Siew: confirm the PDPA domestic-capacity exclusion and the wording of the Retention
   Limitation and Protection Obligations against the statute. Record the section numbers
   and the version date read.
