# run2-hybrid-plus-reranker — 2026-09-30

Sets A, B, C; retrieval **hybrid** (dense + full-text, RRF k=60), reranker **bge-reranker-v2-m3**
(40 candidates to 6); generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge
`qwen2.5:7b-instruct`; corpus `210231c041def426`; code `7d3a48c`.

## The delta table

Three columns, because two would lie. Run 1 measured six documents; the corpus grew to
twenty-six before run 2. The middle column is run 1's configuration on run 2's vault, so the two
deltas separate cleanly: **arrived** is what the documents did, **changed** is what the retriever
did.

| Metric | Run 1 (6 docs, dense) | Re-baseline (26 docs, dense) | **Run 2 (26 docs, hybrid + reranker)** | arrived | changed | Target |
|---|---|---|---|---|---|---|
| Context recall | 0.895 | 0.821 | **0.897** | −0.074 | **+0.077** | ≥ 0.85 ✓ |
| Context precision | 0.868 | 0.767 | **0.854** | −0.101 | **+0.087** | ≥ 0.70 ✓ |
| Faithfulness | 0.819 | 0.810 | **0.967** | −0.009 | **+0.158** | ≥ 0.90 ✓ |
| Answer relevancy | 0.765 | 0.776 | 0.779 | +0.010 | +0.003 | ≥ 0.80 ✗ |
| Abstention rate, Set B | 0.760 | 0.560 | 0.520 | −0.200 | −0.040 | ≥ 0.95 ✗ |
| Field extraction F1 | 0.898 | 0.903 | 0.903 | +0.005 | 0.000 | ≥ 0.90 ✓ |

**Four of six targets met, three of them for the first time.** 64 questions scored (39 Set A, 25
Set B); 33 Set A questions await a document.

## One sentence per metric

**Context recall +0.077 — the lexical arm finds what the embedding missed.** Hybrid recovers the
entire loss from a four-times-larger corpus and lands marginally above run 1's six-document
figure. The mechanism is visible per question: three questions that *abstained* under dense-only
now answer correctly, all three asking for a printed identifier — `b2-0013` and `b2-0015`'s
identity card numbers, and `b2-0010`'s principal. A dense embedding of `S8923156F` is an embedding
of "an NRIC number"; the full-text arm matches the characters, and the identifier lift carries it
over the pack's floor.

**Context precision +0.087 — the reranker is doing the cutting.** Both arms widen the candidate
set and the cross-encoder narrows it by reading each passage against the question, so what reaches
the model is more relevant than what retrieval ranked first.

**Faithfulness +0.158, 0.810 → 0.967 — by far the largest movement, and the one that clears a
target we have never cleared.** Three times run 1's measured noise floor of ~0.05, so it is real.
It is the reranker: the model contradicted its own citation in earlier runs because it was handed
six passages ranked by vector distance, some of which had nothing to do with the question. Given
six passages that were *read* first, it stops arguing with them. `a-b01` and `a-b11` both flip
from wrong to right on exactly that.

**Answer relevancy +0.003 — nothing.** Inside the noise floor, and still short of 0.80. Relevancy
scores the answer against the *question*, and better evidence does not make a 4B model phrase an
answer more to the point. This one needs the generation prompt, not retrieval.

**Abstention −0.040 — the reranker made honesty slightly worse, and that is the finding of this
run.** Claims went from 11 of 25 to 12, and prose declines from 2 to 0. The mechanism is
uncomfortable and worth stating plainly: better evidence makes the model *more* willing to answer.
`b-b14` is the clean case — "when is the road tax on SLK 8842 D due?" abstained under dense-only
and now answers "12 April 2026", which is the vehicle's first-registration date read off a policy
schedule. The plate is a real identifier, hybrid's lift puts the schedule over the floor, the
reranker ranks it first because it genuinely is the most relevant passage, and the model then
answers a question the page does not answer. Every step behaved correctly and the answer is
wrong.

**Extraction F1 unchanged, exactly 0.903 — the sanity check.** Extraction runs at ingestion and
cannot be touched by a retrieval change. A movement here would have meant the harness was
measuring something other than what it claims.

## What this says about where the work goes

Retrieval is close to done. Recall, precision and faithfulness all clear their targets, and the
two that miss are not retrieval's to fix:

- **Abstention 0.52 against 0.95** is the gate. Twelve answers cited a real page and said
  something the page does not support. Improving retrieval moved this the *wrong way*, twice in a
  row, and no further retrieval work will fix it. The floor is a cosine similarity compared
  against the best passage; what `b-b14` needs is a check that the passage answers *this*
  question, which is what the cross-encoder score could provide and currently does not — the
  reranker reorders and cuts but `Passage.score` stays the cosine (ADR 0014 left moving the floor
  to reranker scores as Lane B's call, with the golden set in hand). That is now the single
  highest-value change available, and it is measurable: this run is its baseline.
- **Relevancy 0.78 against 0.80** is the generation prompt, Lane A's.

## Costs and small regressions, for honesty

- **Median latency 2839 ms → 3368 ms (+19%)**, the cross-encoder's forty forward passes. Cheap
  for +0.158 faithfulness.
- **`page_shown` 1.000 → 0.974.** The reranker cut the must-cite page for one question, `a-b11` —
  which still answered correctly from another page. The 40→6 cut can drop a page the register
  names, and at `keep=6` on a 26-document vault that has now happened once.
- **`a-gen-b1-0031-premium_payable-spoken` went from correct to unanswered** — the whole-life
  policy's premium, where the reranker preferred the surrender-value table to the schedule line.
- Two Set B questions improved (`b-b03`, `b-b11`) while two got worse (`b-b13`, `b-b14`): the net
  −0.04 is four questions moving, not a trend, and only `b-b14` has a diagnosable mechanism.

## Was that expected?

Partly. Hybrid recovering the corpus loss was expected and the size was about right. Faithfulness
moving 0.16 was not — the 15 September comparison had it *falling* 0.76 → 0.73, which I now read
as noise on a 37-question set rather than a real effect. Abstention getting worse as retrieval
improves was not expected either time, and two runs in a row have now shown it. That is the
finding to take to the mid-term: **this system's weakest number is not a retrieval problem, and
the last two months of retrieval work have proved it by improving everything except that.**
