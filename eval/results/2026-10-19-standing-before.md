# standing-before — 2026-10-19

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `8f7e6c432f1f7497`; code `517de21`.

What changed, what moved, and whether that was expected:

The baseline for #97: Sets A and B on main at `517de21`, run on the day so that the comparison
has one variable. Older runs differ from it in two ways. The question sets changed in #88: `b-b13`
moved to Set A as `a-b23`, and `b-b19` was retired. And the two loans were re-ingested on 19 October,
so the vault now holds their agreement dates. Against
[`2026-10-17-time-scoped-claims`](2026-10-17-time-scoped-claims.md), then: right and cited 41/50 →
42/51 (`a-b23` is new and right), unsupported claims 18/77 → 15/76 (`b-b13` and `b-b19` were two
of them; read the drop as two wrong questions removed, not the system improving), and filed
correctly 0.976 → 0.985 (the loans' re-extraction). Compared in
[`2026-10-19-standing-after`](2026-10-19-standing-after.md).
