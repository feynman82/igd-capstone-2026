# label-check-off — 2026-10-19

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `8f7e6c432f1f7497`; code `5282c36-dirty`.

What changed, what moved, and whether that was expected:

The baseline for ADR 0021's label check: Sets A and B with the switch built but **off**,
immediately before [`2026-10-19-label-check-on`](2026-10-19-label-check-on.md), on the same vault,
corpus and question sets. Its 76 answers are identical, word for word, to
[`2026-10-19-standing-after`](2026-10-19-standing-after.md), so the switch changes nothing while
it is off. The code is marked `-dirty` because it was measured before it was committed; the
commit that carries it changed no line.
