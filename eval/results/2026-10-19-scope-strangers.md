# scope-strangers — 2026-10-19

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `8f7e6c432f1f7497`; code `b55a4c2`.

What changed, what moved, and whether that was expected:

Sets A and B with #103's scope fix (`b55a4c2`), against
[`2026-10-19-label-check-off-2`](2026-10-19-label-check-off-2.md) on the same vault. The commits in
between (#101's extraction date fix, and #100 and #102's evaluation tooling) change ingestion and
evaluation, not answers. **All 76 answers are identical:** right and cited 42/51, unsupported claims
15/76, over-caution 4/51.

So the new abstentions take nothing from the questions that should be answered. Every Set A
question naming a member by a full possessive name (Rachel Ng Hui Shan's, Lim Ah Kow's, Tan Mei
Ling's, Lucas Lim Kai En's) still reaches that member.
