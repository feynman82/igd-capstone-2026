# reranker-screen — 2026-10-21

Four cross-encoders, scored offline on the passages `AnswerGraph.rerank` is actually handed: each Set A
question understood, retrieved and scoped on `parrot_lexab` (a copy of the frozen Run 3 vault,
`d45f12d`) at `3b564a2`, then reranked by each model in turn. No answers were generated. Of the 93
questions, 93 had their cited document among the candidates.

| Reranker | Size | Answering page in the 6 read | Cited document first | `a-b21` payslip | `a-b23` chassis chunk | Seconds per question (M-series GPU) |
|---|---|---|---|---|---|---|
| `BAAI/bge-reranker-v2-m3` (in use) | 568M | 90/93 | 66/93 | #21 | #5 | 0.25 |
| `Alibaba-NLP/gte-reranker-modernbert-base` | 149M | 89/93 | 66/93 | #21 | #4 | 0.25 |
| `mixedbread-ai/mxbai-rerank-large-v1` | 435M | 89/93 | **76/93** | **#2** | #10 | 1.17 |
| `tomaarsen/Qwen3-Reranker-0.6B-seq-cls` | 0.6B | 90/93 | 65/93 | **#3** | #6 | 1.09 |

Qwen3 was given its instruction template, which PARROT's reranker does not apply; the others read
the question and passage as PARROT gives them. All are Apache-2.0.

**The reranker in use is already at the ceiling of this measure:** the answering page is among the
six read for 90 of 93. So the candidates differ in ordering. Only mxbai showed a real gain there, and
it was the one taken to a full run
([`2026-10-21-reranker-mxbai-large-v1`](2026-10-21-reranker-mxbai-large-v1.md)), where it answered
fewer questions correctly. The reranker is unchanged.
