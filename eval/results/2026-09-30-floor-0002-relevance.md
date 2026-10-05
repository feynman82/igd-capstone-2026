# floor-0002-relevance — 2026-09-30

Hybrid retrieval, cross-encoder reranker, **relevance floor 0.002**; generator
`hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `qwen2.5:7b-instruct`; corpus
`210231c041def426`.

The second measured point behind **ADR 0019**, and the one that settles it. 0.002 is *below Set B's
own tenth percentile*, so it should have been a pure junk filter — a floor that removes passages
nothing could be answered from and touches nothing else.

| Metric | Run 2 (no floor) | This run (0.002) | Δ |
|---|---|---|---|
| Abstention rate, Set B | 0.520 | 0.560 | +0.040 |
| Faithfulness | 0.967 ✓ | 0.936 ✓ | −0.031 |
| Context recall | 0.897 ✓ | 0.872 ✓ | −0.026 |
| Context precision | 0.854 | 0.847 | −0.007 |
| Answer relevancy | 0.779 | 0.775 | −0.004 |
| Field extraction F1 | 0.903 | 0.903 | 0.000 |
| Answered rate, Set A | 0.974 | 0.897 | −0.077 |
| Abstention precision | 0.929 | 0.778 | −0.151 |

It was not a pure junk filter. **One hard negative gained, two answerable questions damaged** —
`a-b01` answers wrongly and `a-b04` loses its evidence and returns only inventory lines. One Set B
question (`b-b03`) went the wrong way, from held back to answered, so the +0.04 is a net of
movements rather than a clean gain.

Both targets survive here, unlike at 0.02. That is the only thing to be said for it, and it is not
enough: abstention precision falls 0.151 for +0.040 of rate, which is paying in false abstentions
for a number that is meant to measure honesty.

Two points make a monotonic line and there is no operating point hiding between them. The reason is
in ADR 0019: the hard negatives that get answered are the ones where a genuinely relevant page
exists, so relevance is the wrong axis to separate them on.
