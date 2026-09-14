# User stories and acceptance criteria

**Owner: Zee (Lane D).** Reviewed by Siew. One story per persona, each with a criterion
that can be run rather than argued about.

The design pack, [`docs/artefacts/interface-design-pack.html`](../../docs/artefacts/interface-design-pack.html),
is where these five stories were first written. This file is the buildable version of
them: every criterion below names the fixture it is tested against, the route it is
tested on, and what a failure looks like. A criterion that cannot be run is not a
criterion, so where the system cannot yet satisfy a story, that is written down in
[§7 Open questions](#7-open-questions-for-review) instead of being quietly softened.

**Every fixture claim below was verified against `corpus/register/batch1.csv` on 14 September
2026**, at 33 rows — doc ids, tiers, subjects, dates and amounts read out of the register rather
than remembered. Three claims in the first draft of this file had already gone stale, because
the batch grew from 30 rows to 33 the night after it was written. The register is Lane E's and
moves; when it does, re-read it before trusting a number here.

## 1. How to read a criterion

Three rules, because the obvious reading is wrong more often than it is right.

**PARROT holds exactly one household.** This is an invariant, not a convention. A vault
containing two families has two people called "my father", two sets of policy numbers and
no correct answer to a question about either — the tool is corrupted rather than merely
untidy. The household is the **Lims of Tampines**, described in
[`corpus/canon.md`](../../corpus/canon.md): Marcus Lim Jun Wei, Rachel Ng Hui Shan, their
son Lucas, and Marcus's resident parents Lim Ah Kow and Tan Mei Ling. Every name in this
file is one of those five.

**A persona is a role inside that household, not a separate customer.** The design pack
was written before the corpus existed and casts five outsiders — Sarah, Priya, Jason and a
couple called Daniel and Rachel. Those names cannot appear here without breaking the rule
above, so each story below is recast onto the Lim who actually holds the documents it
needs. Marcus carries three of the five because he holds twenty-two of the thirty-three
documents in batch1; that is what being the household's document-holder means, and it is more honest
than inventing people to spread the stories evenly.

**Every criterion binds to a document in `corpus/register/batch1.csv`, and dates are
supplied rather than waited for.** A criterion that says "an answer with a citation" is
untestable; one that says "names Lionhead Life Assurance and cites `b1-0008`" is a test.
`/today` takes `?as_of=YYYY-MM-DD`, which moves the whole reminder sweep rather than just
the heading, so each Today criterion names the date it runs at — as of today not one lead
window in either pack is open, and the nearest is 2026-12-15. This is also how the
demonstration shows a lead window opening without anybody editing a database.

## 2. Rachel · Reminder module · Today

> **As the parent who keeps getting surprised**, **I want** to be told what is coming
> before it arrives, **so that** I stop discovering a renewal the morning it is due.

**Accepts when**

1. `/today?as_of=2026-12-15` shows a reminder for policy `HS-2023-771904` — her
   father-in-law's hospital cover — under **Needs you now**, reading 30 days left against
   an expiry of 2027-01-14. It comes from `registers.reminder.policy_expiry` in
   `packs/insurance_agent/pack.yaml`, whose `lead_days` are `[60, 30, 14, 1]`.
2. At `?as_of=2026-11-15` the same item appears under **Coming up**, not **Needs you
   now**. The line between the two is `URGENT_WITHIN_DAYS = 30` in the page, and it is the
   only ordering decision the screen makes: `urgency` arrives from `/api/today` already
   sorted.
3. The row carries a source chip naming the document and page. Clicking it opens that page
   as an image with the row still behind it. A chip that renders `[3]` fails this.
4. Loading the page twice does not consume a lead window: `/api/today` is a GET and sweeps
   with `mark=False`, so a second load is identical. Only the nightly Celery pass writes
   `last_notified_at`.
5. Past the due date the item's `kind` is `overdue` and it stays at the top.
6. With no items in window the screen renders `EmptyState`, with a sentence saying nothing
   needs attention — not a blank column and not a spinner that never resolves.
7. `/today?as_of=2026-09-15` shows a reminder for Marcus's Notice of Assessment, `b1-0028`,
   reading 30 days left against a payment due date of 2026-10-15. It comes from
   `registers.reminder.tax_payment_due` in `packs/iras_tax/pack.yaml`, whose `from_field` is
   `payment_due_date` and whose `lead_days` are `[30, 7, 1]`. This is the obligation
   `corpus/canon.md` calls the nearest live one, and until the registration was added no
   reminder fired for it at all. The two packs' reminders appear on one screen, sorted
   together, which is the platform argument in a single view.

**Fixtures** `b1-0003` (policy schedule, Lim Ah Kow, expiry 2027-01-14, clean tier) and
`b1-0005` (its renewal notice). **Not done if** the screen sorts, computes a due date, or
writes anything on a page load.

## 3. Marcus · retrieval core · Ask

> **As the person managing my father's care**, **I want** to ask which insurer covered his
> last hospital admission and get an answer I can check, **so that** I can make a claim
> without opening six folders.

**Accepts when**

1. Asking *"who covered my father's last hospital claim and what did they settle?"* returns
   `kind: "answer"` naming **Lionhead Life Assurance**, claim **CLM-2026-00412** and
   **5,620.00**, from `b1-0008` — the March 2026 claim, not the November 2025 one
   (`b1-0009`).
2. Every claim in the answer carries at least one citation. A claim whose `chunk_ids` is
   empty is not rendered at all. This is hard rule 3 and it is the product: an uncited
   sentence reaching the screen is a defect, not a formatting problem.
3. Asking *"how much is the surrender value on my whole life policy now?"* cites `b1-0013`
   (June 2026) and not `b1-0014` or `b1-0015`. The same policy is described three times in
   the corpus specifically to catch a system that answers from whichever document it found
   first.
4. Asking something no document covers — *"what is my father's blood type?"* — returns
   `kind: "abstention"`, rendered in its own visually distinct state, showing `missing`
   rather than a hedged guess. Abstention is a designed screen.
5. Asking the pack to act or advise — *"should I switch insurers?"* — returns
   `kind: "refusal"` with the pack disclaimer. `never_acts` is `Literal[True]` in
   `core/contracts.py`; the interface shows the boundary, it does not enforce it.
6. Every answer renders the disclaimer of the pack that answered.

**Fixtures** `b1-0008`, `b1-0009`, `b1-0013`–`b1-0015`. **Not done if** a citation chip
opens the wrong page, or the abstention state is styled as an error.

## 4. Marcus and Rachel · capture · Vault

> **As a couple with two jobs, a child and two resident parents**, **we want** to
> photograph a document and have it filed and understood, **so that** filing costs fifteen
> seconds instead of an evening.

**Accepts when**

1. A photographed document appears in `/vault` within 60 seconds of capture, with its
   `doc_type` identified and its extracted fields populated.
2. The same file captured twice leaves **one** row in the vault. The content key is a
   SHA-256 of the source bytes, so a second capture under a different filename reports
   already filed.
3. A document that fails to parse, or extracts below confidence, appears in the vault's
   **Needs your eyes** queue with a `quarantine_reason`. Nothing disappears silently.
4. A wrong field is corrected from where the mistake is visible, in one click, and the
   correction persists — `verified_by_user` becomes true and the value survives a reload.
5. Both photo-tier documents in batch1 survive the round trip, because a phone photograph
   of a scanned page is the realistic worst case rather than the exception.

**Fixtures** `b1-0009` and `b1-0027`, the two `photo` tier rows; the six `scanned` rows
are `b1-0008`, `b1-0010`, `b1-0015`, `b1-0021`, `b1-0024` and `b1-0030`.
**Depends on** the Telegram adapter, which is Lane A's and in progress — criterion 1 is
blocked on it, criteria 2 to 5 are testable today through the watched folder. **Not done
if** a quarantined document is reachable only from a log.

## 5. Marcus · Alert module · Today

> **As the one contributing to SRS**, **I want** to be warned as I reach the relief
> ceiling, **so that** I stop losing money to a limit I did not notice.

**Accepts when**

1. With `b1-0025` ingested — Marcus, contributions of **15,300.00** for 2025 — a single
   alert appears on Today. The registration is `registers.alert` in
   `packs/iras_tax/pack.yaml`: metric `srs_contributions_ytd`, ceiling `15300`,
   `warn_at: 0.9`.
2. The alert states both numbers, the figure reached and the ceiling. "You are near your
   SRS limit" fails this; the reader has to be told where they stand.
3. It cites the document the figure was computed from, chip and page, like every other
   claim.
4. It does not repeat daily. The alert module debounces at 168 hours — a threshold
   crossing is news once a week.
5. Rachel's own statement, `b1-0027` at 8,000.00 — 52 per cent of the ceiling — raises
   **no** alert, and the two are not summed. The ceiling is per person, and a household
   tool that adds two people's contributions together would warn them both wrongly.

**Fixtures** `b1-0025` (fires), `b1-0026` (prior year), `b1-0027` (must not fire).
**Not done if** the alert carries no citation, or a second load of Today raises it again.

## 6. The household ledger · Tracker · specification only

> **As a household whose tax paperwork arrives in pieces all year**, **we want** a running
> view of what has been contributed and given, **so that** we reach filing season with the
> numbers already added up.

**This story is specified and not built in v1**, and saying so here is the point of
writing it down. `packs/iras_tax/pack.yaml` registers
`registers.tracker.metrics: [donations_ytd, cpf_contributions_ytd, srs_contributions_ytd]`
and `PackSummary.tracker` is already on the Packs surface, but `modules/` holds only
`reminder` and `alert`. There is no tracker module to compute a figure, so there is
nothing for the interface to render.

**Would accept when** each figure is computed in SQL from typed rows rather than generated
prose (hard rule 1 — the query would be hand-written in `modules/tracker/queries.py`), the
receipts behind it are one click away, anything uncategorised is shown rather than silently
dropped, and the totals are per person rather than per household for the same reason as
criterion 5.5. Batch1 already carries the rows it would read: `b1-0019`–`b1-0021` for
donations, `b1-0022`–`b1-0024` for CPF, `b1-0025`–`b1-0027` for SRS.

**Building it is Lane A's**, needs a module manifest against `core.contracts:TrackerConfig`,
and should be an ADR before it is a pull request. Until then it belongs in the pack
catalogue as a named capability, which is the W3 task.

## 7. Open questions for review

Four things surfaced while binding these stories to what is actually in the repository.
Three of the four sit outside Lane D, so none is fixed here.

**The design pack still describes outsiders.** Half of this is now resolved:
`corpus/batches/batch0-personas/` — which held NRIC records, birth certificates and medical
histories for a Tan family and for Priya Singh alongside the Lims — has been deleted in full,
and `corpus/canon.md` records that those people are not in the canon and must not be
reintroduced. `corpus/batches/` now holds `batch1` and nothing else. What remains is the design
pack, `docs/artefacts/interface-design-pack.html`, whose five personas are still outsiders in
prose; §1 above is the recast, and the two read differently. → **the design pack is
Christian's, and it needs a decision at the weekly session.**

**Snooze and dismiss are in the design pack and not in the contract.** The original story
accepts when an item "can be dismissed or snoozed without leaving the screen". `TodayItem`
has no field for that state, and `/api/today` deliberately sweeps with `mark=False` so that
reading the screen never writes. Making it real is a `core/contracts.py` change and
therefore its own reviewed pull request. Criterion 2.1 above is written without it. →
**Christian.**

**The tax due date now fires a reminder — resolved.** `corpus/canon.md` calls the 2026-10-15
payment due date on `b1-0028` "the Reminder module's story and the nearest live obligation",
and `packs/iras_tax/pack.yaml` registered only `filing_deadline` (fixed at 2027-04-18) and
`srs_contribution_cutoff` (2026-12-31), so the notice of assessment produced no reminder at
all. The pack now registers `tax_payment_due`, `from_field: payment_due_date`, with windows
`[30, 7, 1]`. The insurance pack gained the same treatment for the renewal notice's pay-by
date (`renewal_payment_due`, `[14, 3]`). → **done, in `pack.yaml`, which is mine.**

**The premium jump is not an alert.** Canon calls `b1-0003` → `b1-0005` — 2,140.00 rising
to 2,996.00, up 40 per cent — "the Alert module's story". `packs/insurance_agent/pack.yaml`
registers one alert metric, `days_uncovered`, ceiling 0. There is no premium-increase
metric in either pack, so nothing fires. As things stand this is an excellent *Ask* story
spanning two documents, and it should either be described that way or get a metric. →
**Desmond and Christian.**

## 8. The criteria as a checklist

| # | Who | Surface | Testable today | Fixture |
|---|---|---|---|---|
| 2.1–2.6 | Rachel | Today | yes, at `?as_of=2026-12-15` | `b1-0003`, `b1-0005` |
| 2.7 | Marcus | Today | yes, at `?as_of=2026-09-15` | `b1-0028` |
| 3.1–3.6 | Marcus | Ask | yes | `b1-0008`, `b1-0013`–`b1-0015` |
| 4.1 | Marcus and Rachel | capture | blocked on the Telegram adapter | `b1-0009`, `b1-0027` |
| 4.2–4.5 | Marcus and Rachel | Vault | yes, via the watched folder | `b1-0009`, `b1-0027` |
| 5.1–5.5 | Marcus | Today | yes | `b1-0025`, `b1-0027` |
| 6 | the household | — | no: no tracker module exists | `b1-0019`–`b1-0027` |
