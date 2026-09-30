# baseline-dense-only — 2026-09-29

Sets A, B, C; retrieval dense, reranker none; generator
`hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `qwen2.5:7b-instruct`; corpus
`85125383437d5222`; code `3a3b417`.

| Metric | Run 1 | Target |
|---|---|---|
| Context recall | 0.895 | ≥ 0.85 ✓ |
| Context precision | 0.868 | ≥ 0.70 ✓ |
| Faithfulness | 0.819 | ≥ 0.90 ✗ |
| Answer relevancy | 0.765 | ≥ 0.80 ✗ |
| Abstention rate, Set B | 0.760 | ≥ 0.95 ✗ |
| Field extraction F1 | 0.898 | ≥ 0.90 ✗ |
| Obligation precision, alert FPR | not measured | W7 |
| Decode, peak VRAM | 130 tok/s, 7.4 GB | measured (W1 workstation, not this Mac) |

## What this is

The baseline: dense-only pgvector search, no fusion, no reranking, nothing tuned. Every later
run is compared against this one, so it is deliberately the naive configuration rather than the
one we can already beat — the hybrid retriever and the cross-encoder both exist and are switched
off here.

## What it ran against, and what it did not

Forty-four questions of a hundred and seventeen. Set A is 72 and 53 were skipped because their
document has not been mail-merged yet: the register has 50 rows and six have a PDF. Set C is
empty — Siew's fifteen adversarial questions are still to come. So this is nineteen answerable
questions about six insurance policy schedules, plus the twenty-five hard negatives, which need
no document. It is a real measurement of a small corpus, not a small measurement of the real
corpus. The skipped ids are in the result file so run 2 can tell what changed from what merely
arrived.

## Abstention, the number this lane leads with

**0.76 against a target of 0.95**, and every question falls in exactly one row:

| | n | |
|---|---|---|
| Abstained at the gate | 9 | the floor or the scope refused before the model wrote |
| Said nothing of its own | 8 | only the inventory's own lines: "None of the 6 policies on file is a travel policy" |
| Declined in prose | 2 | the model's words: "the chassis number is not listed in the provided passages" |
| **Made a claim** | **6** | **the failures** |

The six: a named driver the schedule does not print; a deductible reported as fully used; a
renewal that has not happened; Marcus's question answered from Lim Ah Kow's policy; and two
where the inventory's line is followed by a paragraph of facts about a policy that does not
answer what was asked. Every one of them carried a citation to a page that exists, and the gate
passed them for that reason. **A citation is not a warrant**, and this is the run that shows it.

`abstention_rate_by_flag` in the result file reads **0.56** — what this metric said before it
was fixed. It trusted `Answer.unanswered`, which one path through the graph forgets to set
(issue #16), so eight correct declines were counted as claims. A number that would have risen by
0.20 the moment somebody fixed a flag is bookkeeping, not a finding, so `held_back` now decides
from what the answer says. Both readings are in the file; when #16 lands they converge, and that
convergence is the check that the fix worked.

## What else moved, and why

**The retrieval numbers are a ceiling, not a result.** Recall 0.89 and precision 0.87 clear
their targets on the first attempt and every answered question cited the right page
(`citation_hit` 1.00, `page_shown` 1.00). Six documents of one type is a haystack with almost no
hay. Expect both to fall when forty-four more arrive.

**The generation numbers miss because the model contradicts its own citation.** Twice it wrote
"None of the 6 policies on file is a car or motor policy" while citing `b1-0001.pdf`, which is
the Private Car Insurance Policy: the inventory's category filter does not recognise its own
motor schedule. Once it answered "Comprehensive Cover" where the register says "Private Car
Insurance Policy" — the coverage type printed on the page, not the product name.

**Extraction F1 0.898 misses by a hair**: 44 hits, 3 false claims, 7 misses, all on policy
schedules. One false claim is issue #19 — the register calls `b1-0031` the "Heritage Whole Life
Plan" while the document prints "Participating Whole Life Insurance", so the extractor is
penalised for being right.

## How much of a delta is a delta

This configuration was run twice, an hour apart, while the metric was being corrected. Retrieval
and extraction came back **identical** — context recall, context precision and extraction F1 to
four decimal places — because they depend on the database and the register, not on sampling.
The generation metrics moved on their own: faithfulness 0.773 → 0.819, relevancy 0.753 → 0.765,
and one Set A question flipped between answering and holding back.

So read run 2 accordingly: **a change under about 0.05 in faithfulness or relevancy is noise**,
and a change in recall, precision or extraction F1 is real. The figures above are the second
run; the first is not committed, because a baseline should be one measurement rather than the
better of two.

## Was that expected?

The retrieval numbers were higher than expected and mean less than they look. The abstention
number was expected to disappoint and did — the lane's pre-run guess was around 0.7, and 0.76
is close, but the guess was right for the wrong reason: I expected the model to invent more and
the metric to be sound, and it was the other way round. The honest summary is the one the task
asked for: **dense-only, no reranking, and it is worse than you would like — in the one place we
said mattered most.**

## What run 2 changes

Hybrid retrieval with RRF, the cross-encoder reranker, contextualised chunks — all merged and
switched off here. A 15 September comparison on the older set moved context precision 0.83 →
0.91 and fact accuracy 0.83 → 0.88 while faithfulness *fell* 0.76 → 0.73, so the reranker alone
will not fix abstention. Whatever does will be a change to the gate, not to retrieval: six
answers cited a real page and said something the page does not support.
