# floor-002-relevance — 2026-09-30

Hybrid retrieval, cross-encoder reranker, **relevance floor 0.02**; generator
`hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `qwen2.5:7b-instruct`; corpus
`210231c041def426`.

One of the two measured points behind **ADR 0019**, which rejects the idea. Kept because the
decision rests on these numbers and a rejected experiment is only trustworthy if its evidence is
committed.

| Metric | Run 2 (no floor) | This run (0.02) | Δ |
|---|---|---|---|
| Abstention rate, Set B | 0.520 | **0.640** | **+0.120** |
| Faithfulness | 0.967 ✓ | 0.809 ✗ | −0.158 |
| Context recall | 0.897 ✓ | 0.821 ✗ | −0.077 |
| Context precision | 0.854 | 0.827 | −0.027 |
| Answer relevancy | 0.779 | 0.801 ✓ | +0.023 |
| Field extraction F1 | 0.903 | 0.903 | 0.000 |
| Answered rate, Set A | 0.974 | 0.872 | −0.103 |
| Abstention precision | 0.929 | 0.762 | −0.167 |

**+0.12 on the headline metric costs two targets that had just been cleared for the first time.**
Faithfulness falls below 0.90 and recall below 0.85, because the floor removes passages that
answerable questions were being answered from: `a-b04` and `a-b09` lose their evidence entirely and
come back as inventory lines only, and `a-b01` answers from the wrong page.

Abstention precision −0.167 is the measure that names what happened: the extra abstentions are not
free, they come with false ones.

The floor was chosen at 0.02 from a sweep over one phrasing straight off the retriever, where Set
A's least relevant winning passage scored 0.0248. The sweep did not reproduce the pipeline — the
graph fuses several phrasings, scopes by person and filters by category before reranking — so the
distribution it calibrated against was not the one the reranker sees. ADR 0019 records that, and
records why fixing it does not rescue the idea.
