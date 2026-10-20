# lexical-all-words — 2026-10-20

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `28f88830362c4ed2`; code `92dba06`.

What changed, what moved, and whether that was expected:

The baseline for the lexical change: `main` (`92dba06`), Sets A and B, code-scored, on `parrot_lexab`,
a copy of the frozen Run 3 vault (`parrot_run3`, commit `d45f12d`, 93 documents), so the two arms
read the same vault. It reproduces Run 3's headline exactly: right and cited 72/93, unsupported claims
25/118, over-caution 6/93, abstention 0.52. On this vault the lexical arm, which joins the question's
words with AND, finds nothing at all for 60 of the 93 Set A questions and 22 of the 25 Set B ones.
