# rerank-printed-words — 2026-10-20

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `28f88830362c4ed2`; code `54c246c`.

What changed, what moved, and whether that was expected:

**Rejected, not merged.** The reranker read the question with the household's vocabulary replaced by
what the documents print, and `core/documents.yaml` gained "take-home pay → net pay". Code `54c246c`
was on a local branch that was deleted, never pushed; the change was three lines in
`AnswerGraph.rerank`. It ran on `parrot_lexab`, a copy of the frozen Run 3 vault, against
[`2026-10-20-lexical-any-word`](2026-10-20-lexical-any-word.md). Expected: `a-b21`'s payslip, found
1st of 40 by search but scored 0.0001 by the reranker, is read. It was read (6th of 6), but the
answer was still held back: best cosine 0.416 against the tax pack's 0.42 floor. `a-d04` lost its
right answer when the reworded "warded" reordered the same documents. Net: right and cited 74 → 73,
over-caution 5 → 7. Issue #125 has the trace.
