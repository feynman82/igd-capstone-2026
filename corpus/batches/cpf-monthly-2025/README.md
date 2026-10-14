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
| Marcus Lim Jun Wei | Meridian Systems Pte Ltd | 9,400 a month | 0.5 month (4,700) in June; 8 months (75,200) in December |
| Rachel Ng Hui Shan | Northlight Health Pte Ltd | 5,200 Jan–Jun; 6,250 from July | 2 months (12,500) in December |

## Rules applied

CPF Board, contribution rates from 1 January 2025, age 55 and below: 37% total, 20% employee;
ordinary wage ceiling 7,400 a month; additional wage ceiling = 102,000 − ordinary wages subject
to CPF for the year; total rounded to the nearest dollar, employee share rounded down, employer
share is the difference.

| | Marcus | Rachel |
|---|---|---|
| Additional wage ceiling | 13,200 | 33,300 |
| Employee share, year | 20,400 | 16,240 |
| Employer share, year | 17,340 | 13,807 |
| Total contributions, year | 37,740 | 30,047 |
