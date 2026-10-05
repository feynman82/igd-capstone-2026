# Evaluation

Three sets, three runs, one committed results file per run.

| Set | Size | Contents | Scored on |
|---|---|---|---|
| A — answerable | 60 | Questions with a known answer in the corpus, spread across the RAG core, both built modules and both built packs | Ragas retrieval and generation metrics |
| B — hard negatives | 25 | Questions the corpus cannot answer | whether the system abstains |
| C — adversarial | 15 | Prompt injection inside an ingested document, requests to act, invitations to claim something unsupported | refusal and containment |

Runs land in weeks 3, 5 and 8. `eval/results/` is committed so the report can show movement
rather than a single number.

## Metrics and targets

Nine metrics. Every run writes all nine to its result file, in this order, under these names,
so that run 1, run 2 and run 3 line up in one table without anyone renaming a column. A
target is a line we intend to cross by run 3, not a claim about run 1 — run 1 is the
baseline, and it is meant to miss.

| # | Metric | Key in the result file | Target | Component | Scored on | How it is computed |
|---|---|---|---|---|---|---|
| 1 | Context recall | `context_recall` | ≥ 0.85 | RAG core | Set A | Ragas `context_recall`. Of the claims in the expected answer, the fraction the retrieved passages support. Low means retrieval did not find the page. |
| 2 | Context precision | `context_precision` | ≥ 0.70 | RAG core | Set A | Ragas `context_precision`. Of the passages retrieved, the fraction ranked above the noise. Low means fusion or reranking is letting junk into the top six. |
| 3 | Faithfulness | `faithfulness` | ≥ 0.90 | RAG core | Set A | Ragas `faithfulness`. Of the sentences in the answer, the fraction the cited passages actually support. The gate should make this near 1.0 by construction; a drop is a gate bug, not a model mood. |
| 4 | Answer relevancy | `answer_relevancy` | ≥ 0.80 | RAG core | Set A | Ragas `answer_relevancy`. Whether the answer addresses the question asked rather than a neighbouring one. |
| 5 | Abstention rate | `abstention_rate` | ≥ 0.95 | Grounding gate | Set B | Not a Ragas metric. Fraction of Set B questions for which the response `kind` is `abstention`. This is the headline number. |
| 6 | Field extraction F1 | `extraction_f1` | ≥ 0.90 | Extraction | Register | Not a Ragas metric. For every `(doc_id, field)` the register fills, compare the `facts` row the extractor wrote. Exact match after type normalisation (dates to ISO, amounts to two decimals). Micro-averaged F1 across all fields, and per `doc_type` and per field in `eval/results/w6-extraction-by-doc-type.md`. |
| 7 | Obligation precision | `obligation_precision` | ≥ 0.95 | Reminder module | Register | Not a Ragas metric. Of the `obligations` rows the reminder module raised, the fraction whose due date and subject match a register row. A reminder about a date that is not printed anywhere is a false obligation. |
| 8 | Alert false-positive rate | `alert_fpr` | ≤ 0.05 | Alert module | Register | Not a Ragas metric. Of the alerts the alert module fired, the fraction where no register value crosses the configured threshold. Reported apart from the RAG metrics: an alert module can be perfect on a system that retrieves badly, and vice versa. |
| 9 | Decode throughput and peak VRAM | `decode_tok_s`, `peak_vram_gb` | Measured and reported | Runtime | `scripts/bench_runtime.py` | Not a quality metric and has no target: it is the number that says whether the other eight were achieved on the hardware we claim. Median with run-to-run spread, from `eval/results/w1-hardware.md`. |

Metrics 1–4 are judged by a model served through Ollama's OpenAI-compatible endpoint on the
same machine — no evaluation question leaves it. The judge is not yet pinned in
`core/runtime/settings.py`; the harness pull request names it, and every result file records
it, because a change of judge moves the numbers as surely as a change of retrieval. Metrics
5–8 need no judge: a register row or a response `kind` is the ground truth. That is deliberate — the four numbers the report leads with are the four
that cannot be argued with.

**Abstention rate, not abstention precision.** The task list once said "abstention
precision". They are different numbers. *Rate* is the fraction of Set B the system
declined — it measures whether the gate holds when the evidence is absent. *Precision* would
be, of everything the system declined across all sets, the fraction it was right to
decline — it measures whether the gate is over-firing on Set A. The second is worth knowing,
so the harness reports it as `abstention_precision` alongside the nine, but it is not a
target: a system that declines everything scores 1.0 on precision and is useless. Rate on
Set B is the claim, and the false abstentions on Set A already show up in metrics 1 and 4.

**Set C has no numeric target.** Its 15 questions are scored on whether the system refuses
and whether the refusal is correctly reasoned, and that second half is a reading, not a
count. The harness reports `refusal_rate` on Set C for the record; the reasoning is Siew's
test report, not a number in this table.

**Not yet agreed.** These are the targets from the proposal, restated so they can be measured
the same way three times. They stand until DY has signed them off; if a target moves, it
moves here first, and the result files are not re-scored.

## How much of a delta is a delta

A three-run report presents movement, so it needs a stated threshold below which movement means
nothing. Otherwise the first delta table is an invitation to narrate noise.

**Measured, not assumed.** One configuration was run twice an hour apart during run 1, with
nothing changed between the two:

| Metric | First | Second | Moved |
|---|---|---|---|
| `context_recall` | 0.8947 | 0.8947 | **nothing** |
| `context_precision` | 0.8675 | 0.8675 | **nothing** |
| `extraction_f1` | 0.8980 | 0.8980 | **nothing** |
| `faithfulness` | 0.773 | 0.819 | +0.046 |
| `answer_relevancy` | 0.753 | 0.765 | +0.012 |

The committed figures are the second run. The first is not committed, because a baseline should be
one measurement rather than the better of two — but it is what the noise floor below is measured
from, and `eval/results/2026-09-29-baseline-dense-only.md` records it.

So:

- **A change under about 0.05 in `faithfulness` or `answer_relevancy` is noise.** Both are a
  local model reading evidence and scoring it, twice, and getting a slightly different opinion.
  Run 2's faithfulness gain of +0.157 is three times that floor, which is why it is reported as
  real; its relevancy gain of +0.003 is reported as nothing.
- **A change in `context_recall`, `context_precision` or `extraction_f1` is real at any size.**
  These read the database and the register. Nothing samples, so nothing drifts: if they move, the
  vault or the corpus moved.
- The same holds for `abstention_rate`, `obligation_precision` and `alert_fpr` — no judge, no
  sampling — with the arithmetic caveat below.

**Granularity is the other noise, and it is exact rather than measured.** These are small sets, so
one question is a visible step: on Set B's 25 questions one question is 0.04, on Set C's 15 it is
0.067, and on the Set A questions a run can currently score (39 of 72 in run 2, the rest skipped
for want of a document) it is 0.026. A metric that moves by one question has moved by one
question, whatever the third decimal place suggests — and during run 1 exactly one Set A question
flipped between answering and holding back across the two runs.

**A rate over one or two events is not a rate.** `alert_fpr` in week 7 was 1.000 because one alert
fired and it was wrong: the only values available were 0.000 and 1.000. Report that kind of number
as a found defect and say how many events it divides by.

**What this does not cover.** The judge model is not pinned in `core/runtime/settings.py`, so a
change of judge moves metrics 1–4 as surely as a change of retrieval and is not inside this noise
floor at all. Every result file records which judge it used; two runs under different judges are
not comparable, whatever the delta.

## Running the harness

```
make eval-quick        # every set, at most 25 questions each, to /tmp/parrot-eval
make eval              # every set, all questions, appended under eval/results/
```

`python -m eval.run` asks PARROT each question exactly as `scripts/ask.py` would, records the
passages the model was shown, and writes `<date>-<label>.json` with the nine metrics, one line
per question, and a `not_measured` reason for every number it could not produce. The Ragas
metrics need a judge: `--judge MODEL` or `PARROT_JUDGE_MODEL`, served by the same local Ollama
(a larger model than the generator is better — a model marking its own work is generous), and
`--no-judge` writes the code-scored metrics alone. A result file is never overwritten. See the
docstring in `eval/run.py` for every flag.

## The module metrics

```
uv run python -m eval.modules              # writes eval/results/w7-module-metrics.md
uv run python -m eval.modules --as-of 2026-12-31
```

Metrics 7 and 8 need no judge and no golden question — the register is the ground truth, as it is
for extraction — so `eval.run` fills them from the vault on every run and `eval.modules` writes
the table apart from the RAG metrics. Both sweeps run with `mark=False`: measuring must never
consume a lead window or a debounce, or the next real sweep goes quiet.

Three decisions worth knowing, because they change what the numbers mean:

- **Obligation precision is over the obligations a document produced.** A calendar deadline from
  `core/documents.yaml` has no document, so it is checked against the catalogue and counted
  separately rather than scored against a register that cannot speak for it.
- **Precision is not completeness.** An obligation can only exist for a fact the extractor wrote,
  so the report prints how many the register supports beside how many exist. The gap is extraction
  recall, not reminder logic.
- **The alert rate recomputes each metric from the register rather than reusing
  `modules/alert/queries.py`.** A metric checked by the query that produced it is not checked. The
  *threshold* rule is imported from the module, because what counts as crossing is a declaration
  and two copies of it would only measure their own drift.

Both numbers are dated — a lead window and a lapse are gaps against a day — so a result file
records `modules_as_of`, and a rate over one fired alert is a found defect rather than a measured
rate. `--no-modules` skips them.

## Extraction F1 by document type

```
uv run python -m eval.report        # writes eval/results/w6-extraction-by-doc-type.md
uv run python -m eval.report --out -
```

Metric 6 is one micro-averaged number and a single number cannot say what to fix. `eval.report`
writes the same arithmetic split per document type, worst first, and — for the types under
target — per register field, so the lane that owns extraction is pointed at one field on one
template. It needs the vault and the register only: no generation, no judge, no retrieval, so it
runs in seconds and can be re-run after any ingest. A re-run rewrites every number and **keeps
the paragraph under "How to read it"**, because the numbers are the vault's and the reading of
them is a person's.

Two things the table deliberately does not do. A register row whose document is not in the vault
is absent rather than scored 0 — there is nothing to extract from yet. A document that *is*
indexed and produced no facts at all is scored as a miss on every field, because "the extractor
wrote nothing" must not be the one failure the metric cannot see. Facts from a document no
register row claims are counted and named, not scored: without a register row there is no ground
truth, so they are neither hits nor misses.

## Writing questions

Everyone writes questions for their own lane — it is the highest-value work with the lowest
barrier, and it distributes the one task that otherwise bottlenecks on one person.

A question file is JSONL:

```json
{"id": "a-042", "set": "A", "lane": "packs", "question": "When does the motor policy on SJ4821B expire?",
 "expected": {"kind": "fact", "pack": "insurance_agent", "key": "expiry_date", "value": "2027-03-31"},
 "must_cite_doc": "0001-motor-0007", "must_cite_page": 1, "notes": "on the schedule"}
```

`expected.kind` is `fact` (exact match against a typed column), `passage` (must cite a
specific document), or `abstain` (the system must decline).

`must_cite_page` is the page the value is **printed** on, read from the register's
`field_pages` column — `expiry_date=2` there means `must_cite_page: 2` here, and a field
absent from `field_pages` is on page 1. It is not free text and it is not a guess: it is why
a citation can be graded without a person opening the document. An `abstain` question has
neither `must_cite_doc` nor `must_cite_page`, because there is nothing correct to cite.

### Generating a lane's dozen

```
uv run python -m eval.generate --lane packs           # 12 to eval/sets/answerable/packs-generated.jsonl
uv run python -m eval.generate --all-lanes            # every lane's dozen
uv run python -m eval.generate --lane packs --all --dry-run
```

The register already holds the answer to every printed field, so the fact questions are
generated from it rather than copied by hand. Each field is asked twice — once naming the
printed reference (`policy MV-2026-448120`), once naming the document as a person would
(`the Private Car Insurance Policy`) — because the identifier and the paraphrase measure
different halves of the retriever. Two questions are never written: one that prints its own
answer, and one whose wording names two documents. `eval/phrasings.py` holds the wordings and
the lane each document type belongs to; a lane that wants better wordings edits that file and
regenerates.

A generated file is a **draft for its lane to keep, edit or replace** — it exists so that no
lane starts from an empty file — and it never repeats a question a person has already written
by hand. The passage questions, the module questions and the adversarial ones are still a
person's job.

## Ground truth comes free

Every document was authored *from* a register row, so `corpus/register/*.csv` already
contains the correct answer for every extractable field. Set A
questions about dates and amounts are generated from it rather than written by hand; only
the passage-level questions need a person.

## The register runs ahead of the batch

Questions are written from the register, which is complete, and the documents are mail-merged
from it later. A question whose document does not exist yet is not wrong — it is not yet
answerable — so `eval.run` skips it, says how many it skipped, and records their ids in the
result file under `run.skipped_no_document`. Scoring them would report the retriever as worse
than it is. `--score-missing` includes them, which is the honest way to see how much of the set
the corpus can currently support.

When a batch is mail-merged and its `field_pages` pass is done, regenerate: `must_cite_page`
comes from that column, and a field the column does not name is taken to be on page 1.

## The honesty check

Synthetic documents are cleaner and more consistent than real ones, so a score measured only
on them overstates the system. The `holdout` corpus is 40 real documents from team members,
redacted, never used for tuning, scored once in week 8. Report both numbers and the gap.
