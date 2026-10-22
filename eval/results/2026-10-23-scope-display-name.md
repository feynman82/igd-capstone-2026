# scope-display-name — 2026-10-22

Sets A, B; retrieval hybrid, reranker cross-encoder `BAAI/bge-reranker-v2-m3`; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `28f88830362c4ed2`; code `44a9f5e`.

What changed, what moved, and whether that was expected:

A document now belongs to a household member when its subject is their own display name, as well as by confirmed alias (`44a9f5e`), on `parrot_since_run3`, against [`2026-10-22-since-run3`](2026-10-22-since-run3.md), whose household is correctly named. Expected: no change, because the fix matters only where the alias table is wrong. Moved: **nothing**. Every headline number is identical and no question changed outcome; 108 of 118 answers are word-for-word the same. Code-scored, no judge. The case it fixes is on the development vault, where a mis-confirmed alias had answered "What did I donate?" from Rachel's receipt; see the pull request.
