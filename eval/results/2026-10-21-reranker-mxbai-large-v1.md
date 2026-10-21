# reranker-mxbai-large-v1 — 2026-10-21

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `28f88830362c4ed2`; code `3b564a2`.

What changed, what moved, and whether that was expected:

**Rejected.** The reranker swapped for `mixedbread-ai/mxbai-rerank-large-v1` with
`PARROT_RERANK_MODEL`, with no code change, on `parrot_lexab`, against
[`2026-10-20-lexical-any-word`](2026-10-20-lexical-any-word.md) (`bge-reranker-v2-m3`). This file's
header says only "cross-encoder", because `eval/run.py` did not yet record the model. That it ran is
shown by the passages read: median relevance 0.174, against 0.408 for the default.

It was chosen by a screen of four rerankers on each question's real 40 candidates
([`2026-10-21-reranker-screen`](2026-10-21-reranker-screen.md)), where it ranked the right document
first 76 times out of 93 against 66. Moved:
- right and cited 74 → **71**/93;
- over-caution 5 → **9**;
- casual 8 → **6**/10;
- unsupported claims 24 → **22**/118;
- abstention 0.52 → **0.60**.

Four answers became right and seven were lost, five of them to holding back. It is ADR 0019's trade
again: declining more of Set B costs answerable questions.
