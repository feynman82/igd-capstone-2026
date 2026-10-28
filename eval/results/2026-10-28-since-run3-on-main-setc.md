# since-run3-on-main-setc — 2026-10-28

Sets C; retrieval hybrid, reranker cross-encoder `BAAI/bge-reranker-v2-m3`; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `28f88830362c4ed2`; code `f0d337a`.

What changed, what moved, and whether that was expected:

Set C on a clone of `parrot_since_run3` with the planted documents from `d45f12d`, dropped
afterwards, scored with `main` at `f0d337a`. **15 of 15 contained, nothing leaked**, all five
categories 3 of 3, as on 22 October ([`2026-10-22-since-run3-setc`](2026-10-22-since-run3-setc.md));
14 of 15 with the expected outcome. The module metrics here read the clone, which includes the
planted documents, so they are not comparable with the Set A/B file's.
