# SRS statements, 2020–2025 — mostly unregistered

Annual SRS statements for Marcus Lim Jun Wei (`SRS-7741-20883`) and Rachel Ng Hui Shan
(`SRS-7741-31204`), rendered from `corpus/templates/srs_annual_statement.html` with
`merge-data.csv`. Issuer is the canon's Crescent Bank (Singapore) Limited.

| Year | Marcus | Rachel |
|---|---|---|
| 2020–2023 | here, unregistered | here, unregistered |
| 2024 | `batch1/b1-0026.pdf` | here, unregistered |
| 2025 | `batch1/b1-0025.pdf` | here — the source for register row `b1-0027`, which is **photo tier**: print it and photograph it on a phone, then save the photo as `b1-0027` |

The ten files here have no register rows, so
`tests/test_corpus_files_match_the_register.py` counts them as unscoreable rather than failing.

## Inputs

- **12,300.00 contributed each year**, in one cash contribution in December. That is within the
  15,300 annual cap for Singapore Citizens and PRs, which has applied since 1 January 2016
  (Ministry of Finance, Supplementary Retirement Scheme).
- Cash only: no investments, no withdrawals. Interest at 0.05% a year, credited 31 December on the
  opening balance plus the contribution for the days it was held, rounded to the cent.
- The 2020 statements, mailed in January 2021, go to the Hougang address; every later year goes to
  Tampines (`corpus/canon.md`: the move was on 2021-03-06).

| | Marcus | Rachel |
|---|---|---|
| Contributions, 2020–2025 | 73,800.00 | 73,800.00 |
| Closing balance, 31 Dec 2025 | 73,893.76 | 73,893.84 |
