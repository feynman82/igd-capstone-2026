# Module metrics — 2026-10-20

Metrics 7 and 8 of `eval/README.md`, reported apart from the RAG metrics because an alert module can be perfect on a system that retrieves badly, and the reverse. Scored against `corpus/register/` by `python -m eval.modules`; corpus `28f88830362c4ed2`, code `8a0c8f6`. Both sweeps ran with `mark=False`, so measuring consumed no lead window and no debounce.

| metric | target | measured |
|---|---|---|
| Obligation precision | ≥ 0.95 | 0.812 ✗ |
| Alert false-positive rate | ≤ 0.05 | 1.000 ✗ |

## Obligations — 16 from a document, 2 from the calendar

Precision is over the 16 a document produced. The register supports 16 of them, so this is a precision, not a count of what was found: an obligation can only be created from a fact the extractor wrote, and the gap between 16 and 16 is extraction recall, not reminder logic.

| due | obligation | from | verdict | the register says |
|---|---|---|---|---|
| 2026-01-31 | policy expiry — Mr Marcus Lim Jun Wei | `b1-0006`.`expiry_date` | the wrong person ✗ | Marcus Lim Jun Wei |
| 2026-02-28 | policy expiry — Rachel Ng Hui Shan | `b2-0007`.`expiry_date` | a later document renews it ✗ | 2027-02-28 |
| 2026-03-01 | policy expiry — Mr Marcus Lim Jun Wei | `b1-0004`.`expiry_date` | a date the document does not print ✗ | 2026-04-11 |
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

On 2026-10-20 the reminder sweep had 0 obligation(s) inside a lead window and 3 overdue. Those counts move with the date; the precision above does not, which is why it is the number in the table.

## Alerts

| metric | whose | item | fired at | the register says | verdict |
|---|---|---|---|---|---|
| `days_uncovered` | Mr Marcus Lim Jun Wei | HM-2024-559013 | 262 | — | false positive ✗ |
| `days_uncovered` | Mr Marcus Lim Jun Wei | MV-2026-448120 | 233 | — | false positive ✗ |

`days_uncovered` counts days since cover lapsed, so a negative value in the register column is cover still to run rather than a gap.

- `days_uncovered` for Mr Marcus Lim Jun Wei: the register produces no value at all for this person and item.
- `days_uncovered` for Mr Marcus Lim Jun Wei: the register produces no value at all for this person and item.

## How to read it

Run 3's frozen vault, re-scored with the check added in `8a0c8f6`: an expiry that a later document extends for the same person and policy is no longer a correct obligation. Run 3 had reported 0.875; the one change is Rachel's renewal notice `b2-0007`, read exactly, but for a term `b2-0004` had already renewed, so 14 of 16 becomes 13. The other two renewal notices whose policies were renewed, `b1-0006` and `b1-0004`, were already scored wrong for other reasons (the title left in the name, fixed in #120, and the expiry date, fixed in #133). Those three are also the three overdue items on 20 October: every overdue reminder in Run 3 was for a policy already renewed. The alerts are unchanged, because the alert metric already took the latest expiry.
