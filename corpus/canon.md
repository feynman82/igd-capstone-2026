# Household canon

Every document in the corpus must agree with this page. It was written before any document
existed, and nothing may contradict it. **Every organisation named here is invented** —
`corpus/README.md` rule 1 — and every rendered page carries a visible
`SYNTHETIC DOCUMENT — NOT A REAL RECORD` footer.

The household is the **Lim household, Tampines**: a sandwich-generation family supporting a
young child and two resident grandparents. That is what makes the paperwork interesting —
parent relief, elderly hospital cover and a child's policy all sit in one register.

## People
| Name | Role | Date of birth | Notes |
|---|---|---|---|
| Marcus Lim Jun Wei | adult | 1987-05-08 | primary earner, IT Manager; supports both parents |
| Rachel Ng Hui Shan | adult | 1989-02-17 | Senior Physiotherapist |
| Lucas Lim Kai En | child | 2019-06-14 | son |
| Lim Ah Kow | parent | 1958-10-12 | Marcus's father, retiree; hypertension and diabetes; lives with the household from 2021 |
| Tan Mei Ling | parent | 1961-04-25 | Marcus's mother, retiree; osteoporosis; lives with the household from 2021 |

## Address
Current: Blk 45B Tampines Ave 8 #07-21 Singapore 521045 (from 2021-03-06)
Previous: Blk 210 Hougang Ave 1 #05-14 Singapore 530210 (until 2021-03-05)

## Employment
| Person | Employer (invented) | From | To | Monthly gross |
|---|---|---|---|---|
| Marcus Lim Jun Wei | Meridian Systems Pte Ltd | 2019-02-01 | — | 9400.00 |
| Rachel Ng Hui Shan | Northlight Health Pte Ltd | 2018-08-01 | — | 6250.00 |

## Vehicles
| Plate | Make and model | Registered | Sold |
|---|---|---|---|
| SLK 8842 D | seven-seat MPV, 1.8 | 2021-04-12 | — |

## Policies
| Policy number | Type | Insurer (invented) | First taken out | Still active? |
|---|---|---|---|---|
| MV-2026-448120 | private car | Meridian Assurance | 2021-04-12 | yes |
| HM-2024-559013 | home contents | Meridian Assurance | 2024-02-01 | yes |
| HS-2023-771904 | hospital income, on Lim Ah Kow | Lionhead Life Assurance | 2023-01-15 | yes |
| LF-2015-330277 | whole life, on Marcus | Lionhead Life Assurance | 2015-06-01 | yes |

A policy number is written identically everywhere it appears, and carries the same insurer
and the same insured on every document. The validator enforces this.

## Invented issuers for the documents that have no `insurer` field

These never appear as a register column, so they live here instead — the templates must use
these names and not their real-world counterparts.

| Document | Issuer on the letterhead (invented) |
|---|---|
| `cpf_statement` | Central Savings Board |
| `notice_of_assessment` | National Revenue Board |
| `srs_statement` | Crescent Bank (Singapore) Limited |
| `donation_receipt` | Riverbend Community Trust; Harbourlight Education Fund |
| `payslip` | the employer above |

## Life events that documents must reflect

- **The hospital premium jumps at the 2027 renewal.** HS-2023-771904 is 2140.00 for the
  period from 2026-01-15; the renewal notice issued 2026-08-28 asks 2996.00 — up 40 per cent.
  This is the Alert module's story, and it spans two documents.
- **A motor claim in May 2026.** Incident 2026-05-14 on MV-2026-448120, settled 3480.00 in
  June. The car policy renewed anyway at 1284.00.
- **Two hospital claims on Lim Ah Kow**, November 2025 and March 2026, against HS-2023-771904.
- **Tax is due 2026-10-15** for both adults, assessed 2026-08-05. This is the Reminder
  module's story and the nearest live obligation.
- **Marcus's whole life policy has three anniversary statements** (2024, 2025, 2026) with a
  rising surrender value — the same policy described three times, which is what catches a
  system that answers from one document when the question spans several.
