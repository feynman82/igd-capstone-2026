# Banded abstention: an evaluation model beside the fixed floor

**Lane B · Yew Mun · 2026-10-14 · design, not yet built**

## Why

The grounding gate decides whether PARROT answers with one number per pack:
`guardrails.abstain_below`, a cosine similarity (insurance 0.45, tax 0.42, the core 0.42 when no
pack speaks for the evidence). `precheck` in `core/graph/gate.py` compares the best passage
against it and either generates or abstains. There is nothing in between, so a question whose
right document scores 0.44 under insurance's floor returns nothing at all — the person is told
the vault does not cover it when it does.

One number cannot be tuned out of this, and run 2 says why. On the golden sets the floor is
already too *loose* — Set A answered at 0.974, but Set B declined at only 0.520 against a 0.95
target — while on colloquial questions it is too *strict* (`core/graph/answer.py`, the 13
September notes: "if i had a fall, and warded for 1 night" put the right clause first at 0.416 and
abstained). Lowering it was tried and let a 4B reader answer near-misses: "do i have travel
insurance?" at 0.38 came back "You have travel insurance".

The floor is not what stops hallucination. Checks 1 and 2 in the gate — every sentence cites a
passage, every cited passage was retrieved — and `unprinted_numbers` do that, on every answer,
whatever the floor. The floor decides only whether the model is asked to write at all. That is the
room this design uses.

## The product idea it evaluates

Instead of answer-or-nothing, PARROT shows a **ranked top 3**, each item labelled **High**,
**Medium** or **Low**:

- Item #1 gets a generated, cited answer **only if it is High**. That answer passes the gate
  exactly as today.
- Every visible item, #1 included, shows the **verbatim passage** it was found in, its document
  and page, and its band. A quote is copied, not written, so it cannot be invented.
- An item below a **hard edge** is hidden. If all three are below it, PARROT abstains as it does
  today and names the document that would have answered.

The person sees how much to trust each candidate and chooses. The model writes one answer, at
most, and only from evidence strong enough to have been answered from before.

## Scope

This spec builds the **evaluation** of that idea, beside the existing fixed floor, so the two can
be compared on the same run. It changes nothing a person talks to.

**In:** `eval/` — Lane B. `core/retrieve/` is read, not changed.

**Out, and later:** replacing `guardrails.abstain_below` with band edges (`core/contracts.py`, a
separate reviewed pull request), the banded gate in `core/graph/` (Christian), the top-3 screen in
`web/` (Zee), and any judgement on quotes from adversarial documents (Siew). Those are proposed
after this work lands, with its numbers.

## Approach: record once, replay many

One harness run with the floor switched off records, per question, everything any floor or band
scheme needs. A pure replay function then applies the fixed floor and any banded scheme to that one
file. One run gives the whole trade-off curve; no setting costs another hour with the judge.

Replay is exact because the floor decides only *whether* the model writes, never *what* it reads:
the passages, their order and the answer are the same at any floor. The one exception is below
under Replay check.

Rejected: a live banded gate behind a flag in `core/graph/` (a full run per setting, and a pull
request in another lane before there is evidence for it); hand-picked band edges (the fixed number
this replaces, three times over).

## 1. What one run records

**`eval/run.py --floor-off`.** `eval/harness.py`'s `build` hands `AnswerGraph` copies of the
enabled packs whose manifest has `guardrails.abstain_below = 0.0` (`model_copy(update=…)` on the
frozen manifest). The installed packs are not modified and nothing in `core/graph/` changes. The
result file records `run.floor: "off"`, so it cannot be read as a measurement of production.

**New fields per question in `per_question`:**

| Field | What |
|---|---|
| `best_score` | The best passage's cosine score — what `precheck` reads |
| `governing_pack` | The pack `_pack_for` would choose, or `core` |
| `floor_in_force` | That pack's production `abstain_below` — the floor today's PARROT would have applied |
| `ranked` | Up to three *distinct documents* from the reranker's kept passages, each `{doc, page, cosine, relevance, pack_id, quote}` from that document's best passage |

`relevance` is the cross-encoder's score as a probability. `Passage.score` stays a cosine (it is
what the graph's floor reads, and `core/retrieve/rerank.py` says why), so the harness computes
relevance itself with the two functions `rerank.py` already makes public — `score_pairs` and
`relevance` — for the kept passages only: six pairs, a few milliseconds. Using the reranker's own
functions rather than a copy is what keeps the recorded number the one the reranker filters on.

**Known limit.** When the best passage belongs to no pack, the graph applies a hard-coded 0.42
(`core/graph/answer.py`, in `AnswerGraph.stream`: `else 0.42`) that `eval/` cannot override. For those
questions, replay cannot test a High edge below 0.42. The run counts them in
`run.core_floor_capped`. Lifting the cap is a one-line pull request for Christian, raised only if
that count is large enough to matter.

**Cost.** One full run with the judge. Set B questions now receive generated answers they would
normally have abstained from. That is intended: it is what lets replay grade the answer path at
any edge.

## 2. Replay and banding — `eval/bands.py`

A pure function from a floor-off result file to outcomes. No database, no model, no judge.

**Two schemes, one interface** — each takes a recorded row and returns an outcome.

- **`Fixed`** — today's rule. `best_score >= floor_in_force` → *answered*, carrying over the
  recorded answer, correctness, citations and Ragas scores. Otherwise *held back*.
- **`Banded(high, medium, hard, axis)`** — edges per pack; `axis` is `cosine` or `relevance`.
  - Each item in `ranked` is **High** (`>= high`), **Medium** (`>= medium`), **Low** (`>= hard`)
    or hidden. A score exactly on an edge takes the higher band.
  - Items are listed in descending order of the axis score, so a label never rises as the list is
    read down.
  - Outcome: item #1 High → **answered**, with the recorded answer as written — read from all six
    passages as today, not from document #1 alone. No High item but at least one visible →
    **quotes only**. Nothing visible → **abstained**.

**Replay check.** `Fixed` at production floors, replayed from the floor-off run, must reproduce the
committed run's answered/held-back split question by question. The branch replay cannot see: a
below-floor question that today still answers from the documents-on-file list
(`core/graph/answer.py`, the `records = passages if refusal is None else []` path). Every question
that comes out differently is listed by id, not smoothed over. If the mismatches are more than the
one-question granularity of the set, replay is not trustworthy and the report says so first.

**Choosing edges is a person's job.** For each pack the module sweeps the edges from 0.30 to 0.60
in steps of 0.01 and prints the trade-off: Set A answered and top-3 hit rate against Set B
generated-answer abstention. It marks two reference points and picks neither:

- the edge that keeps today's Set A answered rate;
- the edge that meets Set B's 0.95 target.

**Two cautions, built in.**

- *Tuning on the test.* Edges chosen on Sets A and B are scored on the questions they were fitted
  to. The chosen edges are confirmed **once** on the holdout vault (`eval/holdout.py`), and that
  number is reported beside the fitted one. This step waits for `yew-mun/holdout-isolated-vault`
  to merge.
- *Granularity.* Set B has 25 questions: one question is 0.04. Two settings one Set B question
  apart are reported as **tied**, not ranked.

## 3. The report

```
uv run python -m eval.bands eval/results/<floor-off run>.json \
    --high 0.50 --medium 0.42 --hard 0.35 --axis cosine --label <what>
```

Edges may be given per pack (`--high insurance_agent=0.52,iras_tax=0.48`). Writes
`eval/results/<date>-bands-<label>.md` and its `.json`, append-only like every result file. It is
a companion report: the nine metrics in the source run are not touched, and nothing here is a
tenth metric.

1. **Header.** The source run file and its generator, judge, corpus sha and git sha — replay changes
   none of them, so it inherits them.
2. **Replay check.** `Fixed` against the committed run, and the ids that differ.
3. **Today against banded, side by side, overall and per pack.**
   - *Set A:* answered rate; **top-3 hit rate** (the `must_cite_doc` appears in any visible item);
     right document in High; nothing shown (still a false abstention); faithfulness and answer
     relevancy over answered questions.
   - *Set B:* generated-answer abstention (the headline, defined as today); nothing shown; the band
     distribution of what was shown — it should be mostly Low.
   - *Set C:* **`leaked_via_quote`.** A planted injection or forbidden string can now reach the
     screen inside a quote, even though no model reads it. Every visible quote is checked against
     the question's `must_not_say`. This exposure is new with the banded design, and it is Siew's to
     judge, so it is reported by question id and string.
4. **Are the labels honest?** For Set A, the fraction of High, Medium and Low items that are the
   right document. High must beat Medium and Medium must beat Low. If not, the labels mislead the
   person reading them, and the report says so before anything else.
5. **The sweep.** Per pack, a compact table every 0.02, the two reference points marked.
6. **Cosine against relevance.** Sections 4 and 5, summarised for each axis side by side.
7. **How to read it.** A paragraph a person writes. Kept when the report is regenerated, as
   `eval.report` keeps its own.

## 4. Testing

Test-first, on hand-built rows rather than a live vault, so `make check` stays fast and needs no
model.

**`tests/test_eval_bands.py`**

- A score exactly on an edge takes the higher band; 0.4499 against 0.45 is Medium.
- When cosine and reranker order disagree, items are listed by the banding axis and labels never
  rise down the list.
- Six passages from two documents give two items, each from its document's best passage.
- High #1 → answered; Medium only → quotes only; all below `hard` → abstained.
- A result file without `ranked` (any run before this change) is refused with an error naming it.
- `Fixed` at production floors reproduces `outcome` on a hand-built run; a planted mismatch is
  listed by id.
- A visible quote containing a `must_not_say` string is flagged; the same string in a hidden item
  is not.
- A hand-built case where Medium is right more often than High raises the label warning.
- Two settings one Set B question apart are reported as tied.

**`tests/test_eval_harness.py`** — `--floor-off` hands the graph pack copies at 0.0 and leaves the
installed packs unchanged; `ranked` is filled from the recorder, with `relevance` from a stubbed
`score_pairs`; `run.floor` is `"off"`.

**`tests/test_eval_report.py`** (or the bands equivalent) — regenerating keeps "How to read it".

**By hand, recorded in the pull request:** `make eval-quick` with `--floor-off` and `eval.bands`
on it, to check the pieces fit; one full floor-off run with the judge, committed; the bands report
at the edges chosen from the sweep; the holdout confirmation, once.

## Pull requests

One variable each, as the lane rules ask.

1. `eval/` — recording: `--floor-off`, `best_score`, `governing_pack`, `floor_in_force`, `ranked`.
2. `eval/bands.py` — replay, banding, sweep and report.
3. `eval/results/` — the floor-off run and the first bands report, with a paragraph on what moved.

Then, separately and with those numbers: the proposal to Christian, Siew and Zee for the contract,
the graph and the screen.

**Done** for each: `make check` passes, result files committed and never overwritten, nothing
outside `eval/`.
