# Marcus tax demo — review-only corpus staging

**DO NOT INGEST THESE HTML WORKSHEETS INTO THE LIVE PARROT VAULT.**

These are illustrative, fictional, not source-verified tax documents. They are staged by type to make review and eventual replacement with approved PDF fixtures straightforward:

| Folder | Document | Blocker |
| --- | --- | --- |
| `noa-ya2023/` | Marcus YA2023 draft | Income assumption unverified; tax payable absent |
| `noa-ya2024/` | Marcus YA2024 draft | Income assumption unverified; tax payable absent |
| `srs-2026/` | Marcus 2026 SRS draft | Contribution total is hypothetical, not evidence |

The HTML files are printable via browser **Print / Save as PDF**; there are also downloadable copies under `web/public/demo/`. This folder is not registered or included in Run 3 freeze. Do not run `make corpus-load` on it.

## Approval steps
1. Corpus owner verifies historical payslips and assessment assumptions against `corpus/canon.md` and registered records.
2. Produce fully verified synthetic PDF fixtures with required fields, and a matching register row for each.
3. Validate corpus/register and extraction tests, then review a PR.
4. Load approved documents to the **demo machine's** vault and verify Ask citations and advice behaviour.

Already registered: Marcus YA2025 `b1-0030`, YA2026 `b1-0028`, CPF 2024 `b1-0024`, CPF 2025 `b1-0022`, SRS 2024 `b1-0026`, SRS 2025 `b1-0025`.
