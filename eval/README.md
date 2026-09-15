# Evaluation

Three sets, three runs, one committed results file per run.

| Set | Size | Contents | Scored on |
|---|---|---|---|
| A — answerable | 60 | Questions with a known answer in the corpus, spread across the RAG core, both built modules and both built packs | Ragas retrieval and generation metrics |
| B — hard negatives | 25 | Questions the corpus cannot answer | whether the system abstains |
| C — adversarial | 15 | Prompt injection inside an ingested document, requests to act, invitations to claim something unsupported | refusal and containment |

Runs land in weeks 3, 5 and 8. `eval/results/` is committed so the report can show movement
rather than a single number.

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
