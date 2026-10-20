# lexical-any-word-setc — 2026-10-20

Sets C; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `28f88830362c4ed2`; code `74f195c`.

What changed, what moved, and whether that was expected:

Set C on the lexical change (`74f195c`), on a clone of `parrot_run3` with the planted documents
from `d45f12d`, dropped afterwards. **15 of 15 contained, nothing leaked**, every category 3/3,
the same as Run 3's Set C ([`2026-10-20-run3-setc`](2026-10-20-run3-setc.md)); 14 of 15 with the
expected outcome, as in Run 3. The module metrics here read the frozen vault's facts, extracted
before the title fix (#120), so they are not part of this comparison.
