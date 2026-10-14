# Notices of Assessment, YA2025 (income earned in 2024) — clean sources

Rendered from `corpus/templates/notice_of_assessment.html` with `merge-data.csv`. Issuer is the
canon's National Revenue Board; dated 6 Aug 2025, payable by 15 Oct 2025.

| File | Taxpayer | Register |
|---|---|---|
| `noa-ya2025-marcus-lim.pdf` | Marcus Lim Jun Wei | the clean source for row `b1-0030`, which is **scanned tier**: print and scan it, then save the scan as `b1-0030` |
| `noa-ya2025-rachel-ng.pdf` | Rachel Ng Hui Shan | no row |

Neither file is named for a row, so `tests/test_corpus_files_match_the_register.py` counts them
as unscoreable until the scan exists.

## Computation

Resident rates from YA2024; YA2025 Personal Income Tax Rebate of 60% capped at $200. CPF relief is
the employee's 20% of ordinary wages, capped at the 2024 ceiling of $6,800 a month. Approved
donations are deducted at 250% before assessable income.

| | Marcus | Rachel |
|---|---|---|
| Employment income (2024 salary × 12) | 112,800.00 | 62,400.00 |
| Approved donations at 250% | — | (3,750.00) — 1,500.00 given in 2024, `../donations-rachel-2024-2025/` |
| **Assessable income** | **112,800.00** | **58,650.00** |
| Earned Income Relief | 1,000.00 | 1,000.00 |
| CPF Relief | 16,320.00 | 12,480.00 |
| SRS Relief (2024 contributions, `../srs-2020-2025/`) | 15,300.00 | 12,300.00 |
| Parent Relief, two parents living with him | 18,000.00 | — |
| Qualifying Child Relief, Lucas | 4,000.00 | — |
| Working Mother's Child Relief, 15% of earned income | — | 9,360.00 |
| Chargeable income | 58,180.00 | 23,510.00 |
| Tax before rebate | 1,822.60 | 70.20 |
| Rebate | (200.00) | (42.12) |
| **Tax payable** | **1,622.60** | **28.08** |

Rachel's 2024 salary of 5,200 a month is the pre-increment figure used in the 2025 CPF statements.
