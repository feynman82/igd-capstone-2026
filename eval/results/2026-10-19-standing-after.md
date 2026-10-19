# standing-after — 2026-10-19

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `8f7e6c432f1f7497`; code `838d074`.

What changed, what moved, and whether that was expected:

One change against [`2026-10-19-standing-before`](2026-10-19-standing-before.md), with the same
vault, corpus and question sets, run one after the other: a `loan_agreement` now spans from its
agreement date onwards, not a single day (#97). **Nothing moved.** All 76 answers are identical
word for word, and every headline number is unchanged: right and cited 42/51, unsupported claims
15/76, over-caution 4/51, filed correctly 0.985. That is the expected result. The time check runs
only on a question that names "last year" or "last month", and no question in Sets A or B asks one
about a loan. What #97 changes, answering such a question from a loan signed before the period,
is shown by its tests, not by this run; an answerable loan question has been asked of Lane A.
