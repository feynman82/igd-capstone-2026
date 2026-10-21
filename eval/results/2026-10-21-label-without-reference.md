# label-without-reference — 2026-10-20

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `28f88830362c4ed2`; code `3b564a2`.

What changed, what moved, and whether that was expected:

The baseline for the reference-in-label experiment: `main` (`3b564a2`) on `parrot_refbase`, a copy of
`parrot_run3` re-chunked and re-embedded from the frozen commit's own files (`d45f12d`) with facts
untouched. Re-parsing produced 375 chunks where Run 3's load had fewer, so these numbers are not
Run 3's; they are the arm the candidate is compared with, and its chunk texts and facts are
identical to the candidate's.
