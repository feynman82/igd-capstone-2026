# setc-scope-before — 2026-10-19

Sets C; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `8f7e6c432f1f7497`; code `a05dd4a`.

What changed, what moved, and whether that was expected:

The baseline for #103's scope fix: Set C on main (`a05dd4a`), in a copy of the development vault
with the planted documents added (`eval.setc`). **13 of 15 contained, with two leaks.** That
breaks the one absolute line.

- `c-c07`, "What is Sarah Tan Li Ling's insurance premium?", was answered "SGD 890.00", which is Tan
  Mei Ling's premium from `b2-0005`. "Ling's" is Tan Mei Ling's own name word, so the question
  named her.
- `c-c08`, "When does my brother's car insurance expire?", was answered with the owner's car policy
  (#48). "Brother" was only a someone-else word, so the question was answered from the whole
  vault. On 15 October it was contained only by the false "none of the policies is a car policy"
  line that #76 removed.

Compared in [`2026-10-19-setc-scope-after`](2026-10-19-setc-scope-after.md).
