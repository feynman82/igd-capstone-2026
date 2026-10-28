# Module metrics — 2026-10-22

Metrics 7 and 8 of `eval/README.md`, reported apart from the RAG metrics because an alert module can be perfect on a system that retrieves badly, and the reverse. Scored against `corpus/register/` by `python -m eval.modules`; corpus `28f88830362c4ed2`, code `8a0c8f6`. Both sweeps ran with `mark=False`, so measuring consumed no lead window and no debounce.

| metric | target | measured |
|---|---|---|
| Obligation precision | ≥ 0.95 | 0.812 ✗ |
| Alert false-positive rate | ≤ 0.05 | — |

## Obligations — 16 from a document, 2 from the calendar

Precision is over the 16 a document produced. The register supports 16 of them, so this is a precision, not a count of what was found: an obligation can only be created from a fact the extractor wrote, and the gap between 16 and 16 is extraction recall, not reminder logic.

| due | obligation | from | verdict | the register says |
|---|---|---|---|---|
| 2026-01-31 | policy expiry — Marcus Lim Jun Wei | `b1-0006`.`expiry_date` | a later document renews it ✗ | 2027-01-31 |
| 2026-02-28 | policy expiry — Rachel Ng Hui Shan | `b2-0007`.`expiry_date` | a later document renews it ✗ | 2027-02-28 |
| 2026-04-11 | policy expiry — Marcus Lim Jun Wei | `b1-0004`.`expiry_date` | a later document renews it ✗ | 2027-04-11 |
| 2026-12-31 | srs contribution cutoff | _the catalogue_ | declared in the catalogue | core/documents.yaml |
| 2027-01-14 | policy expiry — Lim Ah Kow | `b1-0003`.`expiry_date` | matches the register | 2027-01-14 |
| 2027-01-14 | policy expiry — Lim Ah Kow | `b1-0005`.`expiry_date` | matches the register | 2027-01-14 |
| 2027-01-14 | policy expiry — Lim Ah Kow | `b2-0009`.`expiry_date` | matches the register | 2027-01-14 |
| 2027-01-31 | policy expiry — Marcus Lim Jun Wei | `b1-0002`.`expiry_date` | matches the register | 2027-01-31 |
| 2027-02-28 | policy expiry — Marcus Lim Jun Wei | `b1-0032`.`expiry_date` | matches the register | 2027-02-28 |
| 2027-02-28 | policy expiry — Rachel Ng Hui Shan | `b2-0004`.`expiry_date` | matches the register | 2027-02-28 |
| 2027-02-28 | policy expiry — Marcus Lim Jun Wei | `b2-0008`.`expiry_date` | matches the register | 2027-02-28 |
| 2027-04-11 | policy expiry — Marcus Lim Jun Wei | `b1-0001`.`expiry_date` | matches the register | 2027-04-11 |
| 2027-04-18 | filing deadline | _the catalogue_ | declared in the catalogue | core/documents.yaml |
| 2031-04-09 | policy expiry — Tan Mei Ling | `b2-0005`.`expiry_date` | matches the register | 2031-04-09 |
| 2033-02-28 | passport expiry — RACHEL NG HUI SHAN | `b2-0020`.`date_of_expiry` | matches the register | 2033-02-28 |
| 2045-07-31 | policy expiry — Lucas Lim Kai En | `b2-0006`.`expiry_date` | matches the register | 2045-07-31 |
| 2049-08-31 | policy expiry — Marcus Lim Jun Wei | `b1-0033`.`expiry_date` | matches the register | 2049-08-31 |
| 2054-09-30 | policy expiry — Rachel Ng Hui Shan | `b2-0003`.`expiry_date` | matches the register | 2054-09-30 |

On 2026-10-22 the reminder sweep had 0 obligation(s) inside a lead window and 3 overdue. Those counts move with the date; the precision above does not, which is why it is the number in the table.

## Alerts

Nothing fired, so the rate is unmeasured rather than 0.00 — a module that never fires would otherwise claim the target. The declared thresholds are in `core/documents.yaml` under `registers.alert`.

## How to read it

The since-Run-3 vault had reported obligation precision 1.0. Re-scored with the check added in `8a0c8f6`, it is 0.8125, and all three misses are the same kind: a renewal notice whose policy the next schedule renewed (`b1-0006` by `b1-0002`, `b2-0007` by `b2-0004`, `b1-0004` by `b1-0001`). They are also the three overdue items on 22 October. The title fix (#120) and the expiry fix (#133) made these reminders exact; they did not make them right, so the rise from 0.875 to 1.0 was three stale reminders becoming exact, and the precision measured on the same terms is 0.8125 before and after. The reminder module needs the latest-expiry rule the alert module already has (issue #137).
