# lexical-any-word — 2026-10-20

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `28f88830362c4ed2`; code `74f195c`.

What changed, what moved, and whether that was expected:

The lexical arm needs any word of the question rather than every word, and ranks a chunk by how
many different words it shares before how often (`74f195c`), against
[`2026-10-20-lexical-all-words`](2026-10-20-lexical-all-words.md) on the same vault copy. Expected:
chunks that print most of a question but not one of its words reach the reranker. Moved:
- right and cited 72 → **74**/93;
- unsupported claims 25 → **24**/118;
- over-caution 6 → **5**/93;
- retrieval misses 2 → **1**;
- abstention unchanged at 0.52.

The two gains are `a-b23` (the chassis number, now found on the hire-purchase agreement it was
never retrieved from) and `a-gen-b1-0007-policy_no-spoken`. No question's outcome got worse; 106 of
118 answers are word-for-word identical. The two loan-principal misses are unchanged: their passages
now reach the reranker, but the answer still says "not stated" (see the issue on stored facts).
