# Rachel's donation receipts, 2024–2025 — unregistered

Rendered from `corpus/templates/donation_receipt.html` with `merge-data.csv`. All three are
tax-deductible outright cash donations by Rachel Ng Hui Shan.

| Date | Charity | Receipt no. | Amount |
|---|---|---|---|
| 29 Feb 2024 | Good Luck VWO | GLV-2024-00229 | 500.00 |
| 15 Jun 2024 | LionsBefriender | LBF-2024-01873 | 1,000.00 |
| 15 Nov 2025 | GiveSG | GSG-2025-11506 | 300.00 |

The two 2024 receipts are the donations deducted at 250% on Rachel's YA2025 notice
(`../noa-ya2025/`).

**Deliberately unregistered for scoring.** `tests/test_modules.py` asserts that
`donations_ytd` on 20 Dec 2025 is empty for the **registered** corpus: Marcus's
registered 2025 receipt (`b1-0021`) is not deductible. This is **not** a claim
that Rachel made no deductible donation in 2025: the 15 Nov 2025 GiveSG receipt
above exists as an unregistered source fixture. Ingesting all files from this
folder into the same household vault would make the empty household-wide
assertion invalid. Keep these PDFs out of the registered-only evaluation slice
until the test and registration policy are explicitly reconciled.
