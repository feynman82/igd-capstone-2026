# fixtures-in-vault — 2026-10-15

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `79d610547eaca546`; code `b8300ec`.

What changed, what moved, and whether that was expected:

The baseline for removing Set C's planted documents from the development vault, measured with all three still in it. The run's own guard fired — `run.fixtures_in_vault` names `b3-0001`, `b3-0002` and `b3-0003` — which is the first time a run has said so rather than a person finding it afterwards. Compared in [`2026-10-15-fixtures-removed`](2026-10-15-fixtures-removed.md).
