# label-check-on — 2026-10-19

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `8f7e6c432f1f7497`; code `5282c36-dirty`.

What changed, what moved, and whether that was expected:

ADR 0021's label check **on**, against
[`2026-10-19-label-check-off`](2026-10-19-label-check-off.md): same vault, same code, run straight
after it. The switch is the only variable.

| Condition for turning it on (ADR 0021) | off | on | met? |
|---|---|---|---|
| Unsupported claims fall | 15/76 | **11/76** | yes |
| Right and cited moves at most one question | 42/51 | 41/51 | yes (−1) |
| Over-caution moves at most one question | 4/51 | **7/51** | **no (+3)** |
| Median latency rises at most one second | 3.13 s | 3.48 s | yes (+0.34 s; p90 5.08 → 5.64 s) |

**By its own conditions, it stays off.** Seven answers changed:

- **What it was built for.** `b-b14`, "When is the road tax on SLK 8842 D due?", is no longer answered
  with `Period of Insurance From: 12 April 2026`. `a-gen-b2-0003-expiry_date`, a *wrong* Set A answer
  that gave the renewal notice's date, is now withheld. That leaves the unsupported claims but
  counts as one of the three over-caution, although withholding a wrong answer is the aim.
- **A false drop, from a design flaw.** `a-gen-b2-0011-lender` gave the right answer, "The lender on
  facility HP-2021-448190 is Crescent Bank Limited", and lost it. The value the check found was
  the facility number, which the sentence repeats *from the question* as a reference, not as its
  answer, so `Agreement No:` was judged against a claim about the lender. A value the question
  itself names should not be checked.
- **A lost answer, from a robustness gap.** `a-b08` lost a right answer when a model call failed
  mid-answer ("did not answer"), and the failure ended the whole answer. A check that cannot run
  should leave its sentence unchecked, not end the answer.
- **Missed, by the judge.** `b-b06` is unchanged. The lookup found `Name of Insured: Marcus Lim Jun
  Wei`, and the 4B judge then said that label supports "the named driver". This is the risk ADR
  0021 named, and it is not something to tune the prompt against, because `b-b06` is a test item.
- `a-gen-b2-0010-principal`, `a-gen-b2-0011-principal` and `b-d01` were already held back. They
  changed only in wording, and the two principals stop counting as claims.

**What a second measurement should change.** Skip values the question names, and leave a sentence
unchecked if its check fails. Both are code, not prompt. With them, the over-caution count would
fall back by the two defects, and the trade would be one wrong Set A answer withheld and one Set B
claim removed, against a third of a second of latency. Whether a judge that passes `b-b06` is
worth that is ADR 0021's decision.
