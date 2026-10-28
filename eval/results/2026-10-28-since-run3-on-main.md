# since-run3-on-main — 2026-10-28

Sets A, B; retrieval hybrid, reranker cross-encoder `BAAI/bge-reranker-v2-m3`; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `28f88830362c4ed2`; code `f0d337a`.

What changed, what moved, and whether that was expected:

**Does PARROT behave the way the five-number headline describes?** The frozen since-Run-3 vault
(`parrot_since_run3`, Run 3's corpus with the fixes it found), scored with `main` at `f0d337a` and no
judge, to check the headline that the chapter and deck now lead with. Against
[`2026-10-22-since-run3`](2026-10-22-since-run3.md), the same vault and questions:
- **unsupported claims 22 → 21**/118: 10 Set B questions answered with nothing on file, 7 wrong
  values, 4 false "not on file";
- right and cited 76 → **77**/93; over-caution 5 → 4; casual 8/10 against formal 69/83;
- extraction 0.961, unchanged; abstention 0.56 → 0.60 as a diagnostic.

Two questions changed, both towards the aims. `b-b04`, a hard negative asking for the no-claim
discount, no longer states one; it gives only the code-written "on file" line. `a-d02` is now
answered right. The only answering code that changed since `b2b5066` is `core/graph/scope.py` (#136,
a document belongs to a person who matches by display name); `modules/reminder/queries.py` (#140)
changes what Today surfaces, not answers. Set C on a clone: nothing leaked
([`2026-10-28-since-run3-on-main-setc`](2026-10-28-since-run3-on-main-setc.md)).
