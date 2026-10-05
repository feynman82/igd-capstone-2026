# rebaseline-dense-only-26-docs — 2026-09-30

Sets A, B, C; retrieval dense, reranker none; generator
`hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `qwen2.5:7b-instruct`; corpus
`210231c041def426`; code `7d3a48c`.

## Why this run exists

Run 1 measured a vault of six insurance policy schedules. The shared specimen drop has since been
ingested and the vault holds twenty-six documents across seven types, so run 1's numbers describe
a corpus that no longer exists. Comparing run 2 against it directly would credit the retriever
with whatever the corpus did.

This is the same configuration as run 1 — dense, no reranking, nothing tuned — on today's vault.
Against run 1 it says **what arrived**. Against run 2 it says **what changed**. It is not a
second baseline: run 1 remains the committed baseline, because that is what the task named.

| Metric | Run 1 (6 docs) | This run (26 docs) | Δ |
|---|---|---|---|
| Context recall | 0.895 | 0.821 | −0.074 |
| Context precision | 0.868 | 0.767 | −0.101 |
| Faithfulness | 0.819 | 0.810 | −0.009 |
| Answer relevancy | 0.765 | 0.776 | +0.010 |
| Abstention rate, Set B | 0.760 | 0.560 | **−0.200** |
| Field extraction F1 | 0.898 | 0.903 | +0.005 |

Set A went from 19 runnable questions to 39; 33 still await a document. Set B is unchanged at 25,
because a hard negative needs no document.

## What arriving documents did

**Retrieval got harder, by exactly as much as run 1 predicted it would.** Recall −0.074 and
precision −0.101: six documents of one type was a haystack with almost no hay, and four times as
many gives the dense arm real competition. Run 1's paragraph said to read its retrieval figures
as a ceiling rather than a result, and that was right.

**Abstention fell by a fifth, and that is the finding.** Claims the documents cannot support went
from 6 of 25 to 11 of 25. Nothing about the model or the gate changed between these two runs —
only the number of plausible-looking near misses in front of it. A vault with a payslip, a loan
agreement and four identity cards in it offers a confident-sounding wrong answer to "what is the
no-claim discount" in a way a vault of six motor policies does not. **The system's honesty
degrades as its corpus grows**, which is the opposite of the direction it needs to go, and it is
not something a retrieval change can fix.

**Extraction F1 is flat and now means something.** 0.903 against 0.898, but run 1 scored one
document type and this scores seven: identity_card, passport, birth_certificate, payslip and
renewal_notice all at 1.000, policy_schedule 0.881, loan_agreement 0.762. The number stayed still
while the thing it measures got four times wider, which is the more useful reading of it.

## Was that expected?

The direction, yes; the size of the abstention drop, no. Losing a fifth of the headline metric to
documents arriving was not in any prediction I wrote, and it reframes what run 3 has to show: not
just that retrieval improved, but that honesty survived the corpus.
