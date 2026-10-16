# time-scoped-claims — 2026-10-16

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `8f7e6c432f1f7497`; code `2147d81-dirty`.

What changed, what moved, and whether that was expected:

One change against [`2026-10-17-vault-rebuilt`](2026-10-17-vault-rebuilt.md), on the same vault,
corpus and question sets. When a question names a relative past period ("last year", "last
month"), the answer graph drops any sentence whose cited documents' printed dates do not reach
into that period. See `core/graph/period.py`.

| Headline | before | after |
|---|---|---|
| Right and cited (Set A) | 41/50 | 41/50 |
| Unsupported claims (all sets) | 19/77 | **18/77** |
| Over-caution (Set A) | 4/50 | 4/50 |
| Filed correctly | 0.9762 | 0.9762 |

**Exactly one question moved, the one predicted.** `b-b15`, "What was the premium on the car policy
last year?", had answered "The premium on the car policy last year was SGD 1,284.00". The number is
printed, but it is printed on the one car schedule on file, which covers 12 April 2026 to 11 April
2027. That sentence is now dropped, and the answer is the code's "On file" line alone, which is
held back. No Set A question changed, and no other answer changed in any way.

**What this does not show.** Relative periods appear only in Set B (six questions). So nothing
here tests the check against an answerable "last year" question, and that test still has to come.
`b-b05` ("last month's gross salary") already abstains on the floor; the check would now drop its
sentences too, because no payslip on file is for September 2026.
