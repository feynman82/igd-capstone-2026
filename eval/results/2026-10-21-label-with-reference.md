# label-with-reference — 2026-10-20

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `28f88830362c4ed2`; code `3895898`.

What changed, what moved, and whether that was expected:

**Rejected, not merged.** Every chunk's context prefix carried its document's first declared
`identifier` (title — type — reference — section — page). Code `3895898` was on a local branch that
was deleted, never pushed. It ran on `parrot_refcand`, re-chunked like
[`2026-10-21-label-without-reference`](2026-10-21-label-without-reference.md), with identical chunk
texts and facts, so the prefix was the only difference. Expected: a question naming an agreement
finds that agreement's financial schedule. Moved:
- both loan principals now right;
- right and cited 76 → 78;
- unsupported claims 23 → 20;
- abstention 0.52 → 0.56.

Rejected because `b-b02`, a near-miss policy number that does not exist, was answered with the real
policy's premium, the failure the identifier design exists to refuse. Also: three right answers
were lost; 62 of 118 answers changed wording, since the prefix feeds the embedding and the prompt;
and identity documents would carry full ID numbers in every label. Issue #125 has the detail.
