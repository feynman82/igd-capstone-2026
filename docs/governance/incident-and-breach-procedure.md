# Incident and data breach procedure

> **Status: draft for Siew's approval and Christian's technical review.** Owner: Siew. Started
> 2026-10-04.
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

**To confirm from the Act (PDPA 2012, Part 6A).** The structure below is for Siew to check
against the text. The figures commonly cited for these rules are an assessment within 30 days
of suspecting a breach, notification to the PDPC within 3 calendar days of assessing it as
notifiable, and a breach being notifiable if it is likely to cause significant harm to an
affected individual or involves 500 or more individuals. They are **unverified** here and must
not be used until quoted from the Act.

A breach of **NRIC or passport numbers, dates of birth, salary, loan or health information**
should be assumed serious until assessed. These are the categories the data inventory (D2, D4,
D5, D8, D9) identifies as most sensitive.

## 4. The incident log

**Proposed:** `docs/governance/incidents.md`, one entry per incident, committed like every other
governance file. **It never contains personal data.** Documents are named by their id and
people by their role.

```
### INC-<yyyy-mm-dd>-<n>: <one-line title>
- Noticed:   <date and time>, by <role>, through <how>
- Kind:      <one of section 1>
- Data:      <categories, by inventory code, e.g. D2, D5>; <number of people affected>
- Contained: <what was done, when>
- Assessed:  breach yes/no; notifiable yes/no; why
- Notified:  <PDPC / individuals / supervisors, and when>, or "not required, because ..."
- Cause:     <root cause>
- Fixed:     <commit, test or Set C item, ADR>
- Closed:    <date>
```

## 5. Who is responsible on a household's own computer

PARROT runs on the household's computer, and the System Developer and Deployer is the PARROT
team (`terms-of-use.md`, Definitions). For incidents in **the team's own work** (the
repository, the holdout, the demonstration machine) the team follows this procedure in full.
For incidents on **a household's copy**, it is **for Siew to decide** whether the household or
the team carries the duties in section 3. The team never receives a household's data
(`data-inventory.md` §3), which bears on that.

## Decisions for Siew

1. Approve the procedure, and the proposed "same day" times in section 2.
2. Confirm the PDPA Part 6A steps and time limits from the Act (section 3).
3. Decide section 5: who carries the PDPA duties for an incident on a household's own copy.
4. Approve `docs/governance/incidents.md` as the incident log.
