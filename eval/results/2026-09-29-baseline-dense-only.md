# baseline-dense-only — 2026-09-29

Sets A, B, C; retrieval dense, reranker none; generator
`hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `qwen2.5:7b-instruct`; corpus
`85125383437d5222`; code `14eec2f`.

| Metric | Run 1 | Target |
|---|---|---|
| Context recall | 0.895 | ≥ 0.85 ✓ |
| Context precision | 0.868 | ≥ 0.70 ✓ |
| Faithfulness | 0.773 | ≥ 0.90 ✗ |
| Answer relevancy | 0.753 | ≥ 0.80 ✗ |
| Abstention rate, Set B | 0.560 | ≥ 0.95 ✗ |
| Field extraction F1 | 0.898 | ≥ 0.90 ✗ |
| Obligation precision, alert FPR | not measured | W7 |
| Decode, peak VRAM | 130 tok/s, 7.4 GB | measured (W1 workstation, not this Mac) |

## What this is

The baseline: dense-only pgvector search, no fusion, no reranking, nothing tuned. Every later
run is compared against this one, so it is deliberately the naive configuration rather than the
one we can already beat — the hybrid retriever and the cross-encoder both exist and are switched
off here.

## What it ran against, and what it did not

Forty-four questions of a hundred and seventeen. Set A is 72 questions and 53 of them were
skipped because their document has not been mail-merged yet: the register has 50 rows and six
of them have a PDF. Set C is empty — Siew's fifteen adversarial questions are still to come.
So this run is nineteen answerable questions about six insurance policy schedules, plus the
twenty-five hard negatives, which need no document. It is a real measurement of a small corpus,
not a small measurement of the real corpus, and the number that moves most when the batch lands
will be extraction F1, which today is scored on one document type.

## What moved and why

**Retrieval is already good enough to be uninteresting.** Recall 0.89 and precision 0.87 clear
their targets on the first try, and every answered question cited the right page (`citation_hit`
1.00, `page_shown` 1.00). That is not the retriever being clever: six documents of one type is a
haystack with almost no hay. Expect both to fall when forty-four more documents arrive, and
treat today's numbers as a ceiling rather than a result.

**The two failures are the generator's, not retrieval's.** Faithfulness 0.77 and relevancy 0.75
say the model is writing sentences the retrieved page does not support. Twice it answered
"None of the 6 policies on file is a car or motor policy" while citing `b1-0001.pdf`, which is
the Private Car Insurance Policy — the inventory's category filter does not recognise its own
motor schedule, and the model then contradicts its own citation. Once it answered "Comprehensive
Cover" where the register says "Private Car Insurance Policy": the coverage type printed on the
page, not the product name.

**Abstention is the headline and it is bad.** 0.56 against a target of 0.95, on the metric the
lane said it would lead with. Of the twenty-five hard negatives, fourteen were held back, five
declined honestly in prose ("the chassis number is not listed in the provided documents"), and
**six made a claim the documents cannot support** — a named driver the schedule does not print,
a deductible reported as fully used, a renewal that has not happened, and Lim Ah Kow's hospital
plan answering a question about Marcus's. Some of that is issue #16 (an absence-only answer is
reported as answered rather than unanswered), but not all of it: b-b24 and b-b25 are the model
inventing, and the gate let them through because every sentence carried a citation to a page
that exists. A citation is not a warrant, and this is the run that shows it.

**Extraction F1 0.898 misses its target by a hair** — 44 hits, 3 false claims, 7 misses, all on
policy schedules. One of the three false claims is issue #19: the register calls `b1-0031` the
"Heritage Whole Life Plan" and the document prints "Participating Whole Life Insurance", so the
extractor is penalised for being right.

## Was that expected?

The retrieval numbers were higher than expected and mean less than they look. The abstention
number was expected to disappoint, and it did, by more than the lane's own worst guess — the
pre-run estimate was around 0.7. The honest summary is the one the task asked for: **dense-only,
no reranking, and it is worse than you would like — in the one place we said mattered most.**

## What run 2 changes

Hybrid retrieval with RRF, the cross-encoder reranker, contextualised chunks — all already
merged and switched off here. A 15 September comparison on the older set moved context precision
0.83 → 0.91 and fact accuracy 0.83 → 0.88 while faithfulness fell 0.76 → 0.73, so the reranker
alone will not fix abstention. If #16 lands before run 2, the abstention delta will be partly
bookkeeping and the paragraph must say which part.
