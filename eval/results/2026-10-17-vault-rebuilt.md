# vault-rebuilt — 2026-10-16

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `8f7e6c432f1f7497`; code `5d6fa72`.

What changed, what moved, and whether that was expected:

The development vault rebuilt on main: the 13 policy schedules re-extracted in place and the five
current payslips ingested (both on 16 October, with #77 and #80), then every document's chunks
rebuilt with #79's reading order. Compared with
[`2026-10-15-absence-needs-every-kind`](2026-10-15-absence-needs-every-kind.md), the last
Set A/B run on the old vault. **This is not one variable.** It measures the vault, which is several
merged changes at once, so the movements below are explained one question at a time.

| Headline | before | after |
|---|---|---|
| Filed correctly (extraction F1) | 0.875 | **0.976** |
| Right and cited (Set A) | 40/50 | 41/50 |
| Unsupported claims (all sets) | 20/77 | 19/77 |
| Over-caution (Set A) | 4/50 | 4/50 |
| Casual-phrasing gap | 0.125 | 0.150 |

**The filing fixes landed.** Extraction rose by 0.10: policy schedules reach 0.985, with every expiry
date and excess present, and payslips reach 1.00. Every policy now has its expiry reminder (14
pending, up from 9). `b1-0001` is now filed as "Private Car Insurance Policy" and categorised as a
motor policy.

**Four answers gained.** `a-gen-b1-0001-product_name` (the product name is now right),
`a-b15` (states the 750 excess), `a-d10`, and `a-gen-b1-0031-premium_payable` are right and
cited. `b-b05`, `b-b25` and `b-d01` no longer claim. `b-b05` ("last month's gross salary") now
abstains against the current payslips: 0.416 < 0.42.

**Three lost, and two new claims. Read one at a time:**

- **`b-b12` and `b-b15` are car hard negatives, and both are now answered.** "Who is my insurance
  agent for the car policy?" and "What was the premium on the car policy last year?" both abstained
  at 0.42. They now clear the 0.45 floor at 0.48 and 0.454. The rebuilt page-1 chunk of `b1-0001`
  opens with its title, "Private Car Insurance Policy", so it matches every car question better,
  including the ones the vault cannot answer. That is ADR 0019's finding again: better retrieval
  brings plausible evidence to unanswerable questions too. Both answers are unsupported. One says
  "your insurance agent is from MERIDIAN ASSURANCE"; the other gives this year's premium as last
  year's.
- **`a-b14` and `a-gen-b2-0003-expiry_date` look like generation variance.** The right document is
  still ranked first: `b2-0003` sits at the same 0.566. But `a-b14` wrote nothing past the code's
  "On file" line, and `a-gen-b2-0003` cited the renewal notice `b2-0007` and gave its date.
- **`a-gen-b2-0011-lender` gives the right value and cites page 2.** Page 2 also prints "Crescent
  Bank Limited", and its chunk now ranks first because the agreement number moved to the top of the
  page. The question requires page 1, so this is the scorer's page rule, not a wrong answer.

Still not right: the two loan principals and the two identity-card dates of birth (right document
first, wrong value; unchanged since 14 October), `a-b21` and `a-b22`.
