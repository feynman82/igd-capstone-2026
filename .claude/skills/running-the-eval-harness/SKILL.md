---
name: running-the-eval-harness
description: Run and interpret the PARROT Ragas evaluation, or change retrieval and report the effect. Use when running a golden-set evaluation, changing chunking, fusion, reranking or the abstain floor, benchmarking the model on the workstation, or writing the numbers into a pull request.
---

# Running the evaluation harness

The evaluation is the gate. Any change to retrieval, extraction or the grounding gate
pastes its numbers into the pull request with one line on why they moved.

## Read first

`team/yew-mun/README.md`, `AGENTS.md`, `core/contracts.py`, `db/migrations/0001_init.sql`.

## Commands

```bash
make eval-quick        # 25-item subset, for a pull request
make eval              # full run, results committed under eval/results/
python -m eval.run --corpus a --out eval/results
```

The judge model is served locally through Ollama's OpenAI-compatible endpoint. **No
evaluation question leaves the machine** — that is a governance commitment recorded in
the data inventory, not a preference. Do not substitute a hosted judge to make a run
faster.

## The three sets

| Set | Size | Scored on | Author |
|---|---|---|---|
| A · Answerable | 60 | Whether it finds the right evidence and answers from it | Everyone, 12 each |
| B · Hard negatives | 25 | Whether it **abstains** | Yew Mun |
| C · Adversarial | 15 | Whether it refuses, and whether the refusal is well reasoned | Siew |

Set B is the one that matters most. The headline result is **abstention rate on Set B**,
not accuracy: a system that declines when its evidence does not cover the question makes
a claim about trustworthiness that an accuracy score cannot make on its behalf.

Every golden question cites the document and page its answer comes from, taken from
`corpus/register/`. That is what makes the set gradeable without a human in the loop.

## Targets

| Metric | Component | Target |
|---|---|---|
| Context recall | RAG core | ≥ 0.85 |
| Context precision | RAG core | ≥ 0.70 |
| Faithfulness | RAG core | ≥ 0.90 |
| Answer relevancy | RAG core | ≥ 0.80 |
| Abstention rate, Set B | Grounding gate | ≥ 0.95 |
| Field extraction F1 | Extraction | ≥ 0.90 |
| Obligation precision | Reminder module | ≥ 0.95 |
| Alert false-positive rate | Alert module | ≤ 0.05 |
| Decode throughput, peak VRAM | Runtime | Measured and reported |

## One variable per run

If a task implies two changes — chunk size *and* the reranker's `top_k` — say so and
split it into two pull requests. A run that changed three things has told you nothing
about any of them.

The baseline must be honest rather than flattering: dense-only pgvector, no fusion, no
reranking, no contextualisation. A baseline that was tuned is not a baseline.

## Never overwrite a result

`eval/results/` is append-only. The trend across weeks 3, 5 and 8 is the finding; a
single number is not. Name runs by date and what changed.

## Reporting a change

In the pull request body:

1. The metric table, before and after
2. **One sentence** on why it moved — a mechanism, not a restatement of the delta
3. What you expected, if it differed from what happened

"Context precision rose 0.06 because the reranker now drops passages below the floor
before fusion rather than after, so noise no longer occupies fusion slots" is useful.
"Context precision improved" is not.

## Staying in lane

Own `core/retrieve/` and `eval/`. Never modify `core/contracts.py` or `db/migrations/` —
those are separate reviewed pull requests. If a retrieval change appears to need a schema
change, stop and say so.

## Done

- [ ] `make check` passes
- [ ] Numbers pasted into the PR with one sentence on the mechanism
- [ ] The change is one variable
- [ ] Results committed under `eval/results/`, nothing overwritten
