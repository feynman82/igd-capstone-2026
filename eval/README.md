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
| 6 | Field extraction F1 | `extraction_f1` | ≥ 0.90 | Extraction | Register | Not a Ragas metric. For every `(doc_id, field)` the register fills, compare the `facts` row the extractor wrote. Exact match after type normalisation (dates to ISO, amounts to two decimals). Micro-averaged F1 across all fields; also reported per `doc_type` in week 6. |
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

## Ground truth comes free

Every document was authored *from* a register row, so `corpus/register/*.csv` already
contains the correct answer for every extractable field. Set A
questions about dates and amounts are generated from it rather than written by hand; only
the passage-level questions need a person.

## The honesty check

Synthetic documents are cleaner and more consistent than real ones, so a score measured only
on them overstates the system. The `holdout` corpus is 40 real documents from team members,
redacted, never used for tuning, scored once in week 8. Report both numbers and the gap.
