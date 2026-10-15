# 20 · The household calendar lives in Postgres, answers by code, and Parrot only ever drafts an entry

- **Status:** Accepted
- **Date:** 2026-10-15
- **Decider:** Christian (Lane A), on 15 October: a Calendar tab with create, edit and delete, a
  week on Today, events plus document deadlines, Google and iCloud sync designed for but not built
  (the demonstration's entries are synthetic and local), simple repeats, the Lim household seeded,
  and three features taken from OpenJarvis — a Telegram morning digest, "Ask drafts, you confirm",
  and "what's on" answered by code. Reviewers: Zee (`web/`), Siew (what Parrot may do unasked).
- **Models:** the owner's SDRR calendar (its ADRs 0028, 0029, 0030 and 0052) and
  [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) (`morning_digest`, `ApprovalStore`,
  the `gcalendar` and `apple_calendar` connectors).

## Context

Parrot knows the household's deadlines — a renewal, a tax due date — because they are printed on
documents and become `obligations`. It does not know what the household *has on*: Lucas's
swimming, Ah Kow's diabetes review, the trip to Penang. The five personas run their week from a
calendar, and Today, the screen Parrot opens on, showed the documents' dates with nothing around
them. Three constraints shaped what was built.

- **One database** (`AGENTS.md`). Entries cannot live in a second store, and a sync to Google or
  iCloud sends household data off the machine, which the footer on Today promises does not happen.
- **`never_acts`.** A request like "add Dad's polyclinic review on Friday" is a request to act. The
  router refuses acts. A calendar Parrot writes to by itself would be the first thing it does.
- **No claim without a citation** (rule 3). "What's on this week?" has to be answered with every
  line traceable, as a document answer is.

## Decision

1. **Entries are a table, `calendar_events`, in a purely additive migration** (`0004_calendar.sql`,
   CREATE only, rule 4's exception). A row is a series: title, first date, an optional last day,
   start and end times or all day, who it is for (a `people` id, or the whole household), where,
   notes, and a repeat of never, daily, weekly, monthly or yearly with an optional end. Repeats are
   expanded in Python between two dates (`core/calendar.py`); a monthly entry on the 31st skips
   the months without one, as iCalendar does.
2. **Deadlines are never copied in.** The calendar reads open `obligations` for its range and shows
   each with the page its date was read from. A date written down twice can disagree with itself.
   One label on one date is shown once, even when two packs wrote it.
3. **An edit or a delete is to the whole series** (SDRR's ADR 0052 decided the same). There is no
   "this date only", so there is no half-edited series.
4. **Sync is designed for and not built.** `source` (`local`, `google`, `icloud`) and `external_id`
   are on the table, with a unique index per provider id, so a Google or CalDAV adapter writes
   rows the screens already read. It would be an adapter behind the capture-adapter pattern, with
   its own ADR: credentials, a security review, and the off-machine claim on Today rewritten.
5. **Calendar questions are answered by code, before the graph runs** (SDRR ADR 0028 §9). A
   question naming the calendar or asking what is on gets every event and deadline in the period
   it names, a sentence each; "when is Lucas's next swim?" finds the series whose title and
   person hold two thirds of the question's words. An event cites the calendar on its date
   (`Citation.kind = "calendar"`, a link to that day); a deadline cites its document's page. No
   model is called, so no model can drop a line or name the wrong person.
6. **Parrot drafts; a person confirms** (OpenJarvis's approval queue at its one tier here, "always
   ask"). "Add …", "put … in the calendar" and "remind me to …" are caught by code before the
   router, the model reads the parts out of the sentence — handed a table of the next fourteen
   dates, so "Friday" is a lookup — and a `Drafted` event ends the answer. Nothing is written until
   the card's **Add to calendar** calls the API, which records `created_via = 'ask'`. `never_acts`
   holds: the entry is the person's, made with one press.
7. **A morning digest goes to the household's Telegram chats at 07:10**, after the Reminder and
   Alert sweeps: today's entries, then the rest of the week. It reads; it never marks a reminder
   as said. An empty week sends nothing, and an empty allow list speaks to nobody.
8. **The Calendar is the fifth tab**, and Today carries the next seven days under "Needs you now".

## Alternatives considered

| Option | Why not |
|---|---|
| Sync with Google or iCloud now, as SDRR does over CalDAV | Credentials, an external write path and a security review thirteen days before code freeze, for a demonstration whose household is synthetic. It also breaks the footer's promise, which needs its own decision. The table is ready for it (decision 4). |
| Store deadlines as calendar rows | The same date in two places. A corrected renewal date would leave a stale entry behind, and the calendar would stop being able to cite its page. |
| Let the model answer "what's on" from the rows, as retrieval does | On SDRR a 4B model handed the right events once named a person from another record and once picked a stale entry. The rows are the answer; paraphrasing them only adds ways to be wrong. |
| Let Parrot add an entry when asked, and tell the person afterwards | That is acting. It is also the shape of the agentic risk the MGF for Agentic AI asks a product to bound: an action on a person's behalf that they did not see first. |
| Edit one date of a series | Needs exception dates and a "this or all" choice on every edit. The household's repeats are lessons and clinic visits; moving one is rare and a one-off entry covers it. |

## Consequences

- A person can create, change and delete entries from the Calendar and from Ask's draft card,
  and see the week on Today. The digest needs Telegram configured and an allow list.
- `Citation.kind` gains `calendar`, so the API's `Source.kind`, the web `Source` type and the
  source chip each learn one more kind. A calendar chip links inside the app, never out.
- Calendar answers count as answered, cited sentences in an evaluation run. They are not
  retrieval and should be reported apart if a golden set grows calendar questions.
- "Remind me to …" now drafts an entry instead of being refused. A remind request with no date
  drafts one for today, which the card shows for the person to change.
- The digest reads the calendar at 07:10 in the worker's own time zone. The demonstration
  machine is in Singapore; a household elsewhere would need the beat timezone set.
- Nav holds five tabs. A sixth would need the "more" menu the design pack warned against.

## Revisit when

A household needs its phone's calendar in Parrot, or Parrot's in its phone: that is the sync
adapter in decision 4, and it reopens the off-machine promise with it.
