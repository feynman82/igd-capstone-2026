# Module metrics — 2026-10-01

Metrics 7 and 8 of `eval/README.md`, reported apart from the RAG metrics because an alert module can be perfect on a system that retrieves badly, and the reverse. Scored against `corpus/register/` by `python -m eval.modules`; corpus `210231c041def426`, code `f47e343`. Both sweeps ran with `mark=False`, so measuring consumed no lead window and no debounce.

| metric | target | measured |
|---|---|---|
| Obligation precision | ≥ 0.95 | 1.000 ✓ |
| Alert false-positive rate | ≤ 0.05 | 1.000 ✗ |

## Obligations — 7 from a document, 2 from the calendar

Precision is over the 7 a document produced. The register supports 16 of them, so this is a precision, not a count of what was found: an obligation can only be created from a fact the extractor wrote, and the gap between 7 and 16 is extraction recall, not reminder logic.

| due | obligation | from | verdict | the register says |
|---|---|---|---|---|
| 2026-02-28 | policy expiry — Rachel Ng Hui Shan | `b2-0007`.`expiry_date` | matches the register | 2026-02-28 |
| 2026-12-31 | srs contribution cutoff | _the catalogue_ | declared in the catalogue | core/documents.yaml |
| 2027-01-14 | policy expiry — Lim Ah Kow | `b1-0003`.`expiry_date` | matches the register | 2027-01-14 |
| 2027-01-31 | policy expiry — Marcus Lim Jun Wei | `b1-0002`.`expiry_date` | matches the register | 2027-01-31 |
| 2027-02-28 | policy expiry — Marcus Lim Jun Wei | `b1-0032`.`expiry_date` | matches the register | 2027-02-28 |
| 2027-04-11 | policy expiry — Marcus Lim Jun Wei | `b1-0001`.`expiry_date` | matches the register | 2027-04-11 |
| 2027-04-18 | filing deadline | _the catalogue_ | declared in the catalogue | core/documents.yaml |
| 2033-02-28 | passport expiry — RACHEL NG HUI SHAN | `b2-0020`.`date_of_expiry` | matches the register | 2033-02-28 |
| 2049-08-31 | policy expiry — Marcus Lim Jun Wei | `b1-0033`.`expiry_date` | matches the register | 2049-08-31 |

On 2026-10-01 the reminder sweep had 0 obligation(s) inside a lead window and 1 overdue. Those counts move with the date; the precision above does not, which is why it is the number in the table.

## Alerts

| metric | whose | item | fired at | the register says | verdict |
|---|---|---|---|---|---|
| `days_uncovered` | Rachel Ng Hui Shan | PH-2024-912404 | 215 | -150 | false positive ✗ |

`days_uncovered` counts days since cover lapsed, so a negative value in the register column is cover still to run rather than a gap.

- `days_uncovered` for Rachel Ng Hui Shan: the register does not reach the threshold — the register's latest expiry for it is 2027-02-28.

## How to read it

The two numbers point in opposite directions and both readings are the same finding.

**Obligation precision is 1.000 against a 0.95 target, and it is a smaller claim than it looks.**
Every one of the seven document-derived obligations names a date its own document prints, for the
person that document is about — including the passport, where the document prints
`RACHEL NG HUI SHAN` and the register writes it in title case, which is not a disagreement about
who someone is. The two calendar deadlines match declarations in `core/documents.yaml`. But the
register supports sixteen such obligations and only seven exist, because an obligation can only be
created from a fact the extractor wrote, and `expiry_date` is extracted on 5 of 11 policy
schedules ([#32](https://github.com/feynman82/igd-capstone-2026/issues/32)). Precision says
everything the reminder module raised was true. It does not say the reminders are complete, and on
this corpus they are not — fewer than half the policies the household owns can produce one.

**The alert false-positive rate is 1.000 against a ≤0.05 target, and the alert module is not at
fault.** One alert fired: `days_uncovered` for Rachel's PH-2024-912404, claiming 215 days
uncovered. The register says that policy runs to 2027-02-28 — 150 days of cover still to run. The
cause is the same extraction gap: the vault holds the 2026-02-28 expiry from the renewal notice
`b2-0007`, and does not hold the 2027-02-28 expiry from the policy schedule `b2-0004`, because
`b2-0004` prints its dates in ISO form and that is exactly the case the extractor misses. The
module then did the correct thing with what it had: it took the latest expiry it could see, found
it in the past, and said so with a citation.

That is the result worth carrying into the report. A module metric can fail entirely on a module
with no bug in it, because a module reads facts and a missing fact is indistinguishable from a
world in which the thing never happened. It is also the strongest argument yet for fixing #32:
one missing field produced a confident, cited, wrong alert about someone's insurance lapsing.

Two caveats on the apparatus. Both numbers are dated — a lead window and a lapse are gaps against
a day — so the run file records `modules_as_of`, and a sweep on a different day can legitimately
give a different rate. And the rate rests on a single fired alert: 1.000 and 0.000 are the only
values it could have taken, so treat it as a found defect rather than as a measured rate until
more alerts exist to divide by. `srs_contributions_ytd`, the other declared threshold, fired
nothing because the only SRS statements in the corpus are for 2024 and 2025 and the metric is
year-to-date for the year being swept.
