# SRS statements, 2020–2025 — mostly unregistered

Annual SRS statements for Marcus Lim Jun Wei (`SRS-7741-20883`) and Rachel Ng Hui Shan
(`SRS-7741-31204`), rendered from `corpus/templates/srs_annual_statement.html` with
`merge-data.csv`. Issuer is the canon's Crescent Bank (Singapore) Limited.

| Year | Marcus | Rachel |
|---|---|---|
| 2020–2023 | 12,300 a year — here, unregistered | 12,300 a year — here, unregistered |
| 2024 | 15,300 — `batch1/b1-0026.pdf` | 12,300 — here, unregistered |
| 2025 | 15,300 — `batch1/b1-0025.pdf` | 8,000 — here; the source for register row `b1-0027` |

Where the register already fixes a year, the statement prints the register's figure; the
SRS alert and the tax pack's SRS advice are tested against those (`tests/test_modules.py`,
`tests/test_tax_pack.py`). `b1-0027` is **photo tier**: print `srs-2025-rachel-ng.pdf`,
photograph it on a phone, and save the photo as `b1-0027`.

The ten files here have no register rows, so
`tests/test_corpus_files_match_the_register.py` counts them as unscoreable rather than failing.

## Inputs

- One cash contribution in December each year, within the 15,300 annual cap for Singapore
  Citizens and PRs in force since 1 January 2016 (Ministry of Finance, Supplementary
  Retirement Scheme).
- Cash only: no investments, no withdrawals. Interest at 0.05% a year, credited 31 December on
  the opening balance plus the contribution for the days it was held, rounded to the cent.
- The 2020 statements, mailed in January 2021, go to the Hougang address; later years go to
  Tampines (`corpus/canon.md`: the move was on 2021-03-06).

| | Marcus | Rachel |
|---|---|---|
| Contributions, 2020–2025 | 79,800.00 | 69,500.00 |
| Closing balance, 31 Dec 2025 | 79,895.39 | 69,593.79 |
