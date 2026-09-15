# Household canon

Every document in the corpus must agree with this page. It was written before any document
existed, and nothing may contradict it. The household's own insurers and employers below are
the canon's and are used consistently; a document may also name real hospitals, schemes and
agencies where a real document would (`corpus/README.md`). There is no footer requirement.

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

## The family tree, and why three of them are not called Lim

Singapore Chinese convention: a woman who marries into a family keeps her own surname, and
the children take their father's. So the household holds three surnames and is still one
household.

| Person | Surname | Relation to the owner | Why the surname |
|---|---|---|---|
| Marcus Lim Jun Wei | Lim | **the owner** | — |
| Rachel Ng Hui Shan | **Ng** | wife | married in, kept her own surname |
| Lucas Lim Kai En | Lim | son | takes his father's |
| Lim Ah Kow | Lim | father | — |
| Tan Mei Ling | **Tan** | mother | married in, kept her own surname |

Two consequences, and both of them decide membership:

- **A different surname does not mean a different household.** Rachel Ng and Tan Mei Ling are
  Lim household members.
- **The same surname does not mean the same household.** Membership is decided by what a
  document says about relationships and addresses, never by the name alone.

**This is the only household in the corpus.** `corpus/batches/batch0-personas/` previously
held 22 persona sketches spanning three households — the Lims in Tampines, a Tan household at
Blk 123B Bishan St 12 (Sarah Tan Li Ling, David Tan Wei Ming, Emma Tan Jia Xin, Ethan Tan Jia
Le) and Priya Singh at Cecil Street. The folder was deleted in full, because the canon holds one
household. **Those people are not in the canon and must not be
reintroduced.** `Tan Mei Ling` is Marcus's mother; `Sarah Tan Li Ling` was a different
persona family and is gone.

**Rachel Ng Hui Shan has no identity document in the corpus, deliberately.** She is evidenced
by six register rows (`b1-0011`, `b1-0018`, `b1-0020`, `b1-0023`, `b1-0027`, `b1-0029`), which
is what the household roster needs: she arrives off a document, as ADR 0011 requires, rather
than off a persona sketch that never ingests.

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
| PH-2022-604188 | private hospital and surgical, on Marcus | Meridian Assurance | 2022-03-01 | yes |
| CI-2019-215736 | critical illness, on Marcus | Lionhead Life Assurance | 2019-09-01 | yes |
| LF-2024-883192 | term life, on Rachel | Lionhead Life Assurance | 2024-10-01 | yes |
| PH-2024-912404 | private hospital and surgical, on Rachel | Meridian Assurance | 2024-03-01 | yes |
| ES-2020-119284 | long-term care / ElderShield supplement, on Tan Mei Ling | Lionhead Life Assurance | 2020-04-10 | yes |
| CH-2024-339102 | junior health and surgical, on Lucas | Meridian Assurance | 2024-08-01 | yes |

A policy number is written identically everywhere it appears, and carries the same insurer
and the same insured on every document. The validator enforces this.

### The three policies on Marcus are three different products

Deliberately, because a household that holds life cover, hospital cover and critical illness
cover at once is the normal case and the three are easy to conflate:

| | `LF-2015-330277` | `PH-2022-604188` | `CI-2019-215736` |
|---|---|---|---|
| Product | whole life | private hospital and surgical | critical illness |
| Insurer | Lionhead Life Assurance | Meridian Assurance | Lionhead Life Assurance |
| Pays on | death, or surrender | hospitalisation and surgery, as incurred | diagnosis of a listed condition |
| Sum | 300,000.00 | 1,000,000.00 annual limit | 200,000.00 |
| Annual premium | 3,600.00 | 1,860.00 | 2,040.00 |
| Period | whole of life | 2026-03-01 → 2027-02-28, annually renewable | 2019-09-01 → 2049-08-31 |

`PH-2022-604188` sits with **Meridian** and carries a `PH-` prefix specifically so it cannot
be confused with `HS-2023-771904`, which is **Lim Ah Kow's** hospital income plan with
Lionhead. Two hospital-shaped policies, two different people, two different insurers, two
different prefixes. The 40 per cent premium jump at the 2027 renewal belongs to
`HS-2023-771904` and to Lim Ah Kow, and nothing about Marcus's plan may touch it.

### Whole life has no expiry, and now uses a separate `maturity_date`

A whole life policy has no fixed expiry. The insurance pack now makes `expiry_date` optional
on `policy_schedule` and carries a separate optional `maturity_date` field. For
`LF-2015-330277`, Marcus was born 1987-05-08 and the policy matures at age 100, so the register
stores `maturity_date 2087-05-07` and leaves `expiry_date` blank. This avoids creating a
false `policy_expiry` obligation for a whole-life policy.

## Issuers for the documents that have no `insurer` field

These never appear as a register column, so they live here instead. They are the canon's, so
every document of that type uses the same name.

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
