# Monthly CPF statements, 2025 — unregistered

Twenty-four monthly contribution statements for Marcus Lim Jun Wei and Rachel Ng Hui Shan,
January to December 2025, rendered from `corpus/templates/cpf_monthly_statement.html` with
`merge-data.csv`. The annual statements for the same year are `batch1/b1-0022.pdf` and
`batch1/b1-0023.pdf`.

**These have no register rows, deliberately.** `cpf_statement` in `core/documents.yaml` has
only yearly fields (`statement_year`, `total_contributions`), so a monthly figure has no column
to be scored against. The files are named for what they are rather than for a row, so
`tests/test_corpus_files_match_the_register.py` counts them as unscoreable rather than failing.
To score them, add monthly fields to the document type (Lane A) and give each file a row.

## Inputs (consistent with `corpus/canon.md`)

| Member | Employer | Ordinary wages | Bonus |
|---|---|---|---|
| Marcus Lim Jun Wei | Meridian Systems Pte Ltd | 9,400 a month | none |
| Rachel Ng Hui Shan | Northlight Health Pte Ltd | 6,250 a month | none |

**Salary alone, so the CPF statements and the YA2026 notices agree** (issue #66). The first
render paid bonuses — Marcus 4,700 in June and 75,200 in December, Rachel 12,500 in December,
and Rachel on 5,200 until July — which contradicted both the canon (Rachel at 6,250 since
2018) and the notices, which assess 2025 income at exactly twelve months' salary: 112,800.00
for Marcus (`b1-0028`) and 75,000.00 for Rachel (`b1-0029`). "How much did Marcus earn in 2025"
now has one answer. Ordinary Account balances (`b1-0022` 148,200.00, `b1-0023` 96,400.00) are
unchanged: the statements print no opening balance, so nothing on any page contradicts them.

## Rules applied

CPF Board, contribution rates from 1 January 2025, age 55 and below: 37% total, 20% employee;
ordinary wage ceiling 7,400 a month; additional wage ceiling = 102,000 − ordinary wages subject
to CPF for the year; total rounded to the nearest dollar, employee share rounded down, employer
share is the difference.

| | Marcus | Rachel |
|---|---|---|
| Contribution a month | 2,738 (1,480 + 1,258) | 2,313 (1,250 + 1,063) |
| Additional wage ceiling | 13,200 | 27,000 |
| Employee share, year | 17,760 | 15,000 |
| Employer share, year | 15,096 | 12,756 |
| Total contributions, year | 32,856 | 27,756 |
