# Incident and data breach procedure

> **Status: approved by Siew, 2026-10-17, including the "same day" times in section 2.** For
> Christian's technical review. Owner: Siew. Started 2026-10-04. Approval does not confirm the
> statutory steps: everything marked **to confirm** below still is.
>
> This procedure answers the IMDA GenAI dimension "incident reporting", which until now had
> nothing behind it (`imda-what-applies.md`). It also covers a personal data breach under the
> PDPA.
>
> **The PDPA's breach notification rules (Part 6A) have not been read for this draft.** The
> environment it was written in cannot reach the Act. Every statutory step below is marked
> **to confirm**. Its wording and time limits must be quoted from the Act before the procedure
> is relied on.

## 1. What counts

An **incident** is any event in which PARROT, or the people running it, did something that put
a person's data, or a person relying on an answer, at risk. A **data breach** is an incident in
which personal data was, or may have been, accessed, copied, changed or lost without
authority. **When in doubt, treat it as an incident and record it.** Recording one that turns
out to be nothing costs a few minutes.

Incidents this system can realistically have:

| Kind | Example | Where it would show | Breach? |
|---|---|---|---|
| **Wrong person's data** | An alias resolves to the wrong household member, so one adult is shown another's salary or policy | `person_aliases`, `traces` | **Possibly**, if shown to someone not entitled to it |
| **Unauthorised capture** | A stranger sends a document to the household's Telegram bot while `TELEGRAM_CHAT_IDS` is empty, which accepts any chat | `documents.source_channel = 'telegram'`, inbox | Possibly. The bot may also have replied to the stranger. |
| **Data published** | A real document dropped into `inbox/` is committed and pushed to GitHub (`inbox/` is tracked, `.gitignore`) | git history | **Yes** |
| **Device lost or stolen** | The household's computer, holding unencrypted documents and database (`web/lib/lock.ts`: the lock "does not encrypt anything") | — | **Yes** |
| **Holdout exposure** | One of the team's 40 real holdout documents leaves the machine it is kept on, or is committed | git history, file shares | **Yes** |
| **Erasure not completed** | A confirmed deletion is not complete within 72 hours (`retention-and-erasure.md` A4) | the erasure record (Part C, not yet built) | Possibly |
| **Advice without consent** | An advice answer given for a person with no current consent | `advice_records` against `advice_consents` | No, but a serious incident |
| **Unsupported claim** | A factual sentence reaches the user with no supporting passage, past the gate (`core/graph/gate.py`) | `traces`; the user's report | No |
| **Prompt injection followed** | Text inside a filed document makes the assistant do or say something it should refuse (adversarial Set C) | `traces`; Set C results | Depends on what it did |

## 2. The six steps

**Within the team, the clock starts when anyone first suspects an incident**, not when it is
confirmed.

| Step | What to do | Who | When (proposed) |
|---|---|---|---|
| **1. Report** | Tell Siew and Christian. Say what happened, when, and how you noticed. **Do not paste personal data into the report**: name the document by its id, not its contents. | Whoever notices | **Same day** |
| **2. Contain** | Stop it getting worse. See the containment table below. | Christian, with whoever has access | **Same day** |
| **3. Record** | Write an entry in the incident log (section 4). | Siew | Within 1 day |
| **4. Assess** | Was personal data involved? Whose? How many people? Could it cause them harm? Decide whether it is a notifiable breach (section 3). | Siew, with Christian | **To confirm**: PDPA time limit for assessment |
| **5. Notify** | If notifiable: the PDPC, and the affected individuals, as the Act requires (section 3). In every case: the course supervisors, if the incident involves the holdout or a real person's data. | Siew | **To confirm**: PDPA time limit for notification |
| **6. Learn** | Fix the cause. Add a test or a Set C item that would have caught it. Write an ADR if a decision changes. Close the log entry with what changed. | Owning lane | Before the next weekly integration session |

### Containment, by kind

| Kind | First action | Evidence |
|---|---|---|
| Unauthorised Telegram capture | Set `TELEGRAM_CHAT_IDS` to the household's chats only and restart. If the bot token may be known to others, revoke it with Telegram and set a new `TELEGRAM_BOT_TOKEN`. | `core/runtime/settings.py` (`_chat_ids`, `TELEGRAM_BOT_TOKEN`) |
| Data published to GitHub | Make the repository private at once. Then remove the file from history. Deleting it in a new commit is **not** enough: git keeps it (`.gitignore` comment on `corpus/holdout/`). Ask GitHub to clear cached views. | `.gitignore`; `NOTICE.md` |
| Wrong person's data | Unconfirm the alias that caused it (`DELETE_ALIAS`), so it scopes nothing until a person decides again. | `core/household.py` |
| Device lost | Nothing on the device can be reached remotely. Assess what was on it from the data inventory. | `data-inventory.md` §2 |
| Advice without consent | Stop the advice path for that pack until the cause is found. | `core/advice_consent.py` |
| Any incident on the running system | **Place an incident hold** on the records that are the incident's evidence (`traces`, `advice_records`, attribution rows). They are not erased while the incident is open. **Release the hold when the incident is closed**, and the retention policy then applies. | `retention-and-erasure.md` A6; `db/migrations/0001_init.sql` (`traces`) |

## 3. Is it a notifiable breach?

> **Source: Siew, 2026-10-05**, summarising *PDPA 2012, Part 6A* (Notification of Data
> Breaches), https://sso.agc.gov.sg/Act/PDPA2012?ProvIds=P16A-. That page could not be opened
> from the environment this was written in. The section numbers and the exact wording are to
> be quoted when the chapter cites them.

| Step | Rule | Where it sits in this procedure |
|---|---|---|
| **Assess** | When a data breach is suspected, carry out a **reasonable and expeditious assessment** of whether it is a **notifiable data breach**: one that causes or is likely to cause **significant harm** to individuals, or is of a **significant scale**. | Section 2, step 4 |
| **Notify the PDPC** | Once the breach is assessed as notifiable, notify the Personal Data Protection Commission **within 3 calendar days**. | Section 2, step 5 |
| **Data intermediary** | A data intermediary that processes data on behalf of another organisation, and has a breach, must notify that organisation **without undue delay**. | Applies only if a team member ever processes personal data for another organisation. The team never receives a household's data (`data-inventory.md` §3), so it is not a household's data intermediary. |

*Not in this summary, so still to confirm from the Act:*
- whether, and when, the **affected individuals** must also be notified;
- the threshold that defines "significant scale".

The earlier draft's "30 days to assess" and "500 or more individuals" were unverified, and are
**removed**. Neither appears in the Act's rule as summarised above, which says "expeditious".

A breach of **NRIC or passport numbers, dates of birth, salary, loan or health information**
should be assumed to risk **significant harm** until assessed. These are the categories the
data inventory (D2, D4, D5, D8, D9) identifies as most sensitive.

## 4. The incident log

> **Approved (Siew, 2026-10-05):** `docs/governance/incidents.md`.

The incident log is the evidence that the team meets the **Accountability Obligation**. The PDPC
expects an organisation to be able to *show* its data controls (Siew, 2026-10-05). So
**every** incident is logged, including ones assessed as minor or not notifiable. A logged
non-notifiable incident is the proof that the team monitors and assesses its risks. **The log
never contains personal data.** Documents are named by their id and people by their role.

Each entry records:
- the date, time and nature of the incident;
- **the assessment process used** to decide whether it was notifiable;
- the containment measures; and
- the long-term remedial actions taken to prevent a recurrence.

The template is in `incidents.md`.

## 5. Who is responsible on a household's own computer

> **Siew, 2026-10-05:** no one carries PDPA duties for a household's own copy. The PDPA excludes
> any individual acting in a personal or domestic capacity from the Data Protection Provisions
> (Siew's source: PDPC, *Advisory Guidelines on Key Concepts in the PDPA*, 1 October 2021).

So:
- **A household's own copy:** this procedure is offered to the household as **good
  practice**. It is not a statutory duty, and the team does not notify the PDPC for it.
- **The team's own work:** the repository, the 40-document holdout, and the demonstration
  machine. The team is an organisation holding personal data, so **this procedure applies in
  full, including section 3**.

This is consistent with `data-inventory.md` §1, "two capacities" (Siew, 2026-10-05).
PARROT is designed to PDPA standards as a choice, and the team is bound in full for its own
work.

## Decisions for Siew

1. ~~Approve the procedure, and the proposed "same day" times in section 2.~~ **Approved
   2026-10-17.**
2. ~~Confirm the PDPA Part 6A steps.~~ **Recorded 2026-10-05** (section 3). Still to confirm:
   whether affected individuals must be notified, and the "significant scale" threshold.
3. ~~Reconcile section 5 with the data inventory.~~ **Decided 2026-10-05:** option (a), two
   capacities (`data-inventory.md` §1).
4. ~~Approve the incident log.~~ **Approved 2026-10-05.**
