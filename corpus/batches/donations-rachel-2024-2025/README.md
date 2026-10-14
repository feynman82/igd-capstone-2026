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

**Deliberately unregistered.** `tests/test_modules.py` asserts that no tax-deductible donation is
on file for 2025 (`donations_ytd` on 20 Dec 2025 is empty, because Marcus's only 2025 receipt,
`b1-0021`, is not deductible). Registering the 15 Nov 2025 receipt would change that story, so
it needs a decision before it gets a row.
