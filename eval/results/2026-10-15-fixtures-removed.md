# fixtures-removed — 2026-10-15

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `79d610547eaca546`; code `b8300ec`.

What changed, what moved, and whether that was expected:

Set C's three planted documents were taken out of the development vault, and Sets A and B
re-scored. Everything else identical — same corpus, same code, same flags — against
[`2026-10-15-fixtures-in-vault`](2026-10-15-fixtures-in-vault.md), measured an hour earlier with
the fixtures still in. The fixtures are the only variable.

| Headline | with fixtures | without | |
|---|---|---|---|
| Right and cited (Set A) | 34/50 — 0.680 | **36/50 — 0.720** | better |
| Over-caution (Set A) | 6/50 | **4/50** | better |
| Unsupported claims (all sets) | 23/77 | **25/77** | worse |
| Retrieval misses (Set A) | 0/50 | 0/50 | — |
| Casual / formal phrasing | 4/10 · 30/40 | 5/10 · 31/40 | — |
| Filed correctly | 0.9028 | 0.9028 | — |

**Only four questions changed, and the result is that the measurement is now honest, not that
it improved.** The fixtures were distorting it in both directions:

| | with → without | |
|---|---|---|
| `a-b02` | abstained → **answered correctly** | the fixture `b3-0001` had been ranked first at 0.95 |
| `a-b21` | held back → **answered wrongly** | the fixture `b3-0002` had been ranked first; holding back hid a wrong answer |
| `a-b19` | held back → answered correctly | no fixture ranked first; possibly run-to-run noise |
| `b-b05` | **declined → claimed** | the fixture had *manufactured* a correct abstention |

`b-b05` is the one worth carrying forward. It asks "What was last month's gross salary?" — a hard
negative, because there is no September payslip. With the fixtures in, the nearest document was
the planted budget note, the model could trace no answer, and it declined: right, by accident.
Without them it finds real payslips and answers with salaries for the wrong months. **"Last month"
is not resolved against a document's date**, and the fixture had been hiding that.

**A correction to what was predicted.** Five Set A failures had a planted document ranked above
the right answer, and removing the fixtures was expected to recover them. Two changed. The other
three — `a-b01`, `a-b13` and `a-gen-b1-0001-product_name-printed` — fail for reasons the fixtures
did not cause. The product name one is the generation error recorded in
[`w6-extraction-by-doc-type.md`](w6-extraction-by-doc-type.md): the model writes the cover
description, "Comprehensive Cover", instead of the printed product name. Being ranked first is
not the same as being the cause.

Retrieval misses are still zero: every failing Set A question had its page among the passages
the model read. What remains is ranking and generation, not recall.

**From here, Sets A and B are scored in a vault that holds no fixtures, and `eval.run` warns in
red and in the result file (`run.fixtures_in_vault`) if it finds any.** Set C is scored in its own
vault by `eval.setc` — see [`2026-10-15-setc-isolated-vault`](2026-10-15-setc-isolated-vault.md).
