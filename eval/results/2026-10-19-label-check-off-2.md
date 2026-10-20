# label-check-off-2 — 2026-10-19

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `8f7e6c432f1f7497`; code `bc8eee8`.

What changed, what moved, and whether that was expected:

The baseline for the second measurement of ADR 0021: the label check with its two fixes
(`bc8eee8`), switch **off**, immediately before
[`2026-10-19-label-check-on-2`](2026-10-19-label-check-on-2.md). This time the code was committed
first, so the run is not marked `-dirty`. Its 76 answers are identical, word for word, to
[`2026-10-19-label-check-off`](2026-10-19-label-check-off.md): with the switch off, the fixes
change nothing.
