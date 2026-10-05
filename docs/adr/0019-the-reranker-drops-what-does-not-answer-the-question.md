# 19 · A relevance floor on the reranker does not buy abstention, and the reason is not calibration

- **Status:** Rejected by measurement. The mechanism ships switched off; the finding is the decision.
- **Date:** 2026-09-30
- **Decider:** Yew Mun (Lane B), with golden Sets A and B. Reviewers: Christian (the gate), Siew (what an abstention claims)
- **Answers:** ADR 0014's note that moving the floor to reranker scores is Lane B's to decide. It is decided: not this way.

## Context

Abstention on Set B is 0.52 against a target of 0.95, and two evaluation runs moved it the **wrong
way** while improving every retrieval metric — arriving documents cost 0.20, hybrid search and the
reranker a further 0.04. Twelve of twenty-five hard negatives are answered with a claim the
documents cannot support, and every one cites a page that exists.

The structural reason is real. `gate.precheck` compares `Passage.score` against the pack's
`abstain_below`, and that score is a cosine similarity: it says how close the *wording* was, never
whether the passage answers the question. `b-b14` is the whole problem in one question — "when is
the road tax on SLK 8842 D due?". The plate is printed on the motor schedule, so hybrid search
finds it and the identifier lift puts it at 0.95, far above the 0.45 floor. The cross-encoder ranks
that schedule first, correctly: of everything retrieved it *is* the most relevant passage. The
model answers "12 April 2026", the vehicle's first registration date. Every stage behaved as
designed and the answer is invented.

The one component that asks "does this passage answer *this* question" is the cross-encoder, and
its score was being computed and thrown away. Putting it to work was the obvious next move.

## Decision

**A relevance floor on the cross-encoder's score is rejected.** It was built, calibrated, measured
at three settings on the full golden sets, and it trades away more than it buys at every one.

`CrossEncoderReranker.floor` stays, defaulting to `0.0`, which drops nothing. `eval.run
--rerank-floor` sets it and every result file records it. The mechanism is kept because it is the
apparatus for this question and the next attempt should not rebuild it, not because it is on.

## The measurement

Hybrid retrieval, this reranker, 39 answerable questions and 25 hard negatives, one variable:

| floor | abstention (B) | faithfulness | recall | answered (A) | abstention precision | fact accuracy |
|---|---|---|---|---|---|---|
| **0.0 (off)** | 0.52 | **0.967** ✓ | **0.897** ✓ | **0.974** | **0.929** | **0.846** |
| 0.002 | 0.56 | 0.936 ✓ | 0.872 ✓ | 0.897 | 0.778 | 0.795 |
| 0.02 | 0.64 | 0.809 ✗ | 0.821 ✗ | 0.872 | 0.762 | 0.769 |

At 0.02, +0.12 abstention costs **two targets that had just been cleared for the first time**.

At 0.002 — below Set B's own tenth percentile, which should have been a pure junk filter — it buys
**one** hard negative and damages **two** answerable questions: `a-b01` answers wrongly and `a-b04`
loses its evidence altogether. Abstention precision drops 0.15, which is the false-abstention
measure saying so directly.

## Why it is not a calibration problem

A first sweep, scoring one phrasing straight off the retriever, said 0.02 would keep 0.95 of Set A's
cited pages and empty none. It was wrong, because the graph fuses **several phrasings**, then scopes
by person and filters by category, and only then reranks — so the distribution reaching the
cross-encoder in the pipeline is not the one the sweep measured. That error is worth recording, but
fixing it does not rescue the idea.

The idea fails for a reason no threshold can fix. **The hard negatives that get answered are the ones
where a genuinely relevant page exists**, and a cross-encoder is built to score exactly those highly.
`b-b14`'s schedule really does print that plate; "what is the no-claim discount" really is about the
motor policy that really is on file. Set A's relevance distribution and Set B's overlap at the top
because the two sets are not separable by *relevance* — they are separable by whether the page
carries the field that was asked for, which is a different question and not one a similarity or a
relevance score can answer.

## Alternatives considered

| Option | Why not |
|---|---|
| Replace `Passage.score` with the cross-encoder score and let the existing floor read it | Same number in a different scale, so the same measurement applies — and it would change five packs' `abstain_below` and a contract to achieve it. ADR 0014 named that cost; the measurement now says there is nothing to buy with it. |
| A relative floor — drop passages far below the best one | Improves precision and cannot help abstention at all: the best passage, which is the one the wrong answer is built from, always survives. |
| Raise the pack's `abstain_below` | It is a similarity, so raising it rejects paraphrase — the thing hybrid search exists to serve — while leaving `b-b14` untouched at 0.95. Wrong axis. |
| Report the number a third time and do nothing | Two runs had shown it worsening. Trying the one component that measures relevance was the right next step; the result is that the answer lies elsewhere, which is worth more than another unexplained row. |

## Consequences

What this buys: the question is closed with numbers rather than opinion, and the next person does not
spend a week on it. `--rerank-floor` and the recorded `rerank_floor` remain for whoever wants to
re-test as the corpus grows. No behaviour changes today.

What it costs: the headline metric is still 0.52 against 0.95, and Lane B no longer has a retrieval
lever to pull at it. The residue needs something that reasons about **which field the question asks
for against which fields the page prints** — that is a pack's knowledge, so it is Zee's and Siew's
more than mine — or the model being asked to decline and believed, which is the generation prompt.
The report should also say plainly that 0.95 was set in week 1, before anything had been measured.

## Revisit when

A pack can say which fields a document type prints, so an answer can be refused for naming a field
the page does not carry; or Set A doubles and the distributions are worth re-measuring. Not before:
the curve above is monotonic and there is no operating point hiding in it.
