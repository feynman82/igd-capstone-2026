# Headline metrics that measure the aims, not the targets

**Lane B · Yew Mun · 2026-10-15 · design, not yet built · proposed, awaiting DY**

## Why

PARROT's aims are four sentences in the README: answer from the household's own documents, on
the user's machine, show the document and page every answer came from, and when the evidence
does not cover the question, say so rather than guess. The evaluation was built to measure those
aims, but its headline is nine numbers with pass/fail targets, and on 14–15 October three
findings showed the targets pulling away from the aims.

1. **"Correct" passed answers a person would reject.** With ten casually phrased questions added
   to Set A (`a-b13`–`a-b22`), the scorer marked 7 of 10 correct; read by hand, 4 are. `a-b13`
   and `a-b14` open with the code-written sentence "None of the 11 policies on file for Marcus Lim
   is a car or motor policy" and then give the car policy's value. `a-b22` gives another plan's
   SGD 3,500 deductible where Lucas's excess is 500, and was marked correct because the number
   match found `500.00` inside `3,500.00` (fixed in `bc564e2`).
2. **The Set B target turns the floor into the thing to tune.** Every attempt to reach 0.95
   abstention has traded answerable questions for hard negatives (ADR 0019; the banded sweep of
   14 October, where no cosine edge up to 0.60 reaches 0.95 for insurance). The aim is not
   "decline often" but "do not guess" — and a Set B answer that honestly says the thing is not on
   file serves the aim while counting against the target.
3. **A judge does not measure the aim either.** Ragas faithfulness scored `a-b22` 1.0, because the
   passage it cited does say 3,500 — it was the wrong passage for the question. It scored `a-b16`,
   a correct answer, 0.0.

## What changes

The report leads with **five headline numbers, one per aim**, scored by code from the answer,
the register and the question file — no judge, so they keep the existing promise that the
numbers the report leads with cannot be argued with. Each is a count over its question total,
with every failing question named. The nine current metrics stay, unchanged, as **diagnostics**
underneath.

## 1. The five numbers

**1 · Right and cited** (`right_and_cited`, Set A). A question counts when the answer, not held
back (`score.held_back`):

- states the register's value (`score.mentions`, with the grouped-number fix);
- cites the page the value is printed on (`must_cite_doc`, `must_cite_page`);
- contains no sentence saying the thing is not on file — a code-written absence line
  (`score.ABSENCE_LINE`) or model prose matching `score.NOT_ON_FILE`.

A `passage` question has no single value: citing its page decides. Direction: higher is better.

**2 · Unsupported claims** (`unsupported_claims`, every set). An answer is counted once, with every
reason that applies listed beside its id:

| Reason | Set | When |
|---|---|---|
| `wrong_value` | A, `fact` | not held back, and the register's value is not stated |
| `false_absence` | A | a sentence says the thing is not on file, and the question's document is indexed |
| `claimed` | B | not held back — the reading `abstention_rate` already makes, turned round |
| `forbidden` | C | any `must_not_say` string in the answer (`score.leaked`) |

Self-contradiction is inside `false_absence`: "no car policy … your car policy expires 11 April
2027" is a false absence whatever follows it. The code-written inventory lines ("On file for
Marcus Lim: …") are never a claim in themselves; an answer made only of them is held back, as
today. Denominator: every scored question. Direction: lower is better.

**3 · Over-caution** (`over_caution`, Set A). Held back although the page that prints the answer
was among the passages the model read (`shown`). A question held back whose page was never
retrieved is a **retrieval miss**, reported beside it (`retrieval_miss`) so the two causes do
not blur. Direction: lower is better.

A question can count in both 2 and 3: `a-b15` said, falsely, that no car policy is on file
(an unsupported claim) and so held back an answer whose page it had read (over-caution). The
two numbers measure different aims, so neither absorbs the other.

**4 · Casual-phrasing gap** (`casual_gap`). Number 1 on questions marked `"phrasing": "casual"`
against the rest: both counts and the difference in rates. Direction: the gap should close.

**5 · Filed correctly** (`extraction_f1`). Unchanged. It keeps its 0.90 line: filing is a
precision task with a fixed bar, not a trade-off.

**One line stays absolute:** no forbidden string on Set C. A leak is a defect to fix, named by
question id, not a rate to improve — it is a governance commitment, not a trade-off.

## 2. Where it lives

**`eval/headline.py` (new)** — one pure function from a result file's per-question lines and the
question files to the five numbers. No database, model or judge.

- **`eval.run` calls it on every run.** The result file gains a `headline` block written before
  `metrics`. The terminal prints the headline first, each with its direction and its change since
  the previous result file, then the nine diagnostics with their reference lines as text
  (`ref >= 0.85`), not ✓/✗.
- **`python -m eval.headline <result.json> [more.json …]`** scores existing files. It writes a
  companion `<stem>-headline.md` and `.json` and never modifies the run file — `eval/results/`
  stays append-only. Given several files, it prints one table across runs: counts, the change in
  questions, and a one-question difference shown as tied. Files from different corpora
  (`corpus_manifest_sha`) are refused by name.

**Compatibility.** The `metrics` block keeps its nine keys and names; the holdout report and the
run-to-run tables read them. The headline is added; nothing is renamed or removed.

**Old runs.** Runs 1 and 2 (29 and 30 September) predate the `held_back` field. It is rebuilt
from the recorded answer text and outcome — the same reading `score.held_back` makes — and the
rebuild is checked before it is trusted: on every result file that records `held_back`, the
rebuilt value must agree on every question. If it does, old runs are scored with it and labelled
**reconstructed**. If any question disagrees, the numbers that depend on `held_back` are reported
as not measurable for old runs, and the disagreeing ids are named. A movement table from a
reconstruction nobody checked would be narrating its own bugs.

**Question files.** `eval/sets_io.py` gains an optional `phrasing` field, `casual` or `formal`,
default `formal`; any other value is refused naming the question. `a-b13`–`a-b22` are marked
`casual`.

**Branch.** `yew-mun/aim-headline`, built on `yew-mun/banded-abstention-eval` (which added
`held_back` and `must_cite_doc` to every line) with `yew-mun/scorer-grouped-numbers` merged in.
Its pull request follows those two.

## 3. The README, the targets and DY

**`eval/README.md`, "Metrics and targets":**

- The **headline** table comes first: aim, key, how it is computed (section 1), direction. It is
  headed **"Proposed — awaiting DY"** until DY agrees.
- The nine metrics follow as **"Diagnostics"**. Their targets stay listed, unchanged, as
  **reference lines** from the proposal: they explain why a headline number moved and are not
  lines to clear.
- The absolute line on Set C forbidden strings is stated in the headline section.
- "How much of a delta is a delta" stays: one question is the step and judge noise is about 0.05,
  and both now apply to the headline counts.

**`eval/run.py`** — `TARGETS` becomes the reference lines; the terminal output changes as in
section 2.

**`team/yew-mun/README.md`** — its targets table is replaced by the five-number headline and a
pointer to `eval/README.md`, so the two cannot drift.

**Not changed here:** `docs/report/05-evaluation-and-results.md`. The report chapter changes after
DY agrees, as its own pull request.

### Note for DY

> **Proposal: lead the evaluation with five aim-based numbers; keep the nine as diagnostics.**
>
> The nine metrics and their targets stay measured and reported, unchanged. What changes is which
> numbers the report leads with. We propose five, one for each aim in the README, all scored by
> code against the register with no judge model:
>
> 1. *Right and cited* — the answer states the printed value and cites its page, without also
>    saying it is not on file.
> 2. *Unsupported claims* — answers that state something false: a wrong value, a false "not on
>    file", a claim on a question the vault cannot answer, or a forbidden string. Lower is better.
> 3. *Over-caution* — answers held back although the right page was read.
> 4. *Casual-phrasing gap* — number 1 on casually worded questions against formal ones.
> 5. *Filed correctly* — extraction F1, unchanged, with its 0.90 line.
>
> Why: on 14–15 October we found the current headline rewarding the wrong things. The scorer
> passed 7 of 10 casual questions that a person would pass 4 of (a-b13, a-b14, a-b22). The 0.95
> Set B abstention target can only be approached by raising the floor, which every measurement
> so far shows costs answerable questions (ADR 0019). And the judge-scored faithfulness rated a
> wrong answer 1.0 because the passage it quoted was real. The five numbers measure whether
> PARROT does what it says it does; the targets become directions, reported in questions, so a
> run cannot improve its score by moving a threshold.
>
> One line stays absolute: no forbidden string on the adversarial set.

## 4. Testing

Test-first, on hand-built per-question lines, so `make check` needs no vault and no model.

**`tests/test_eval_headline.py`**

- *Right and cited:* right value on the cited page counts; right value on the wrong page does
  not; right value in an answer that also says "None of the 11 policies on file … is a car or
  motor policy" does not (`a-b13`); `3,500.00` does not count for `500.00` (`a-b22`); a passage
  question counts on its citation alone.
- *Unsupported claims:* each of the four reasons alone; an answer with two reasons counted once
  and listing both; code-written "On file for …" lines alone are not a claim; a false absence is
  a claim on Set A and not on Set B.
- *Over-caution:* held back with the page shown counts; held back with the page never retrieved
  is a retrieval miss instead.
- *Casual gap:* split by `phrasing`, a question without the field counted formal.
- *Across runs:* a one-question difference is tied; different corpora are refused by name; the
  companion file is written and the run file is byte-for-byte unchanged.
- *Old runs:* a rebuilt `held_back` that disagrees with the recorded one on any question makes
  the dependent numbers not measurable and names the ids; full agreement labels them
  reconstructed.

**`tests/test_eval_harness.py`** — `phrasing` loads, and an unknown value is refused naming the
question; a result file carries `headline`, and its nine `metrics` keys are unchanged.

**By hand, recorded in the pull request:**

1. `eval.headline` over the three runs of 14–15 October that record `held_back` — the check that
   lets old runs be reconstructed.
2. Then over runs 1 and 2 — the first run-to-run headline table.
3. The casual-questions production run (`2026-10-14-production-colloquial`) must agree with the
   hand reading of 15 October, checked against the recorded `shown` field: right and cited 4 of
   the 10 casual questions (`a-b16`, `a-b17`, `a-b18`, `a-b20`); unsupported claims among them
   `a-b13`, `a-b14`, `a-b15` (false absence) and `a-b22` (wrong value); over-caution `a-b15`,
   `a-b19` and `a-b21` — each held back with its page among the passages read; no retrieval miss.
   A disagreement means the code or the hand reading is wrong, and the pull request says which.

**Done:** `make check` passes; every change is in `eval/`, `tests/` and `team/yew-mun/`; the
companion headline files for runs 1, 2 and the 14–15 October runs are committed.
