# Yew Mun — Lane B · Retrieval and evaluation

**Owner: Yew Mun.** Directories: `core/retrieve/`, `eval/`.

> **Your task list:** [`tasks.md`](tasks.md) — generated from `docs/team-tasks.csv`, so tick things off there and regenerate.
> **Everyone else:** [`team/`](../README.md) · **The rules every agent follows:** [`AGENTS.md`](../../AGENTS.md)

You own the numbers that carry the grade. The report's strongest claim is not that the
system works but that we measured it, three times, and can say what moved and why.

---

## What you own

| Path | What |
|---|---|
| `core/retrieve/` | Hybrid search, RRF fusion, the cross-encoder reranker, the abstain floor |
| `eval/sets/` | The three golden sets |
| `eval/run.py` | The Ragas harness |
| `eval/results/` | Every committed run. Never delete one — the trend is the finding |

You also own the *measurement* of extraction quality, though Christian owns the
extraction engine. That separation is deliberate: the person who built a thing should
not be the only person scoring it.

---

## Order of work

**Week 1 — the benchmark nobody else can do.**
Run the machine, not the model. Produce a table: model, quantisation, context length,
decode tokens per second, peak VRAM, for `Qwen-SEA-LION-v4-4B-VL` — the generator named in
`core/runtime/settings.py`, and the only model in scope. Every VRAM number currently in the
proposal is a planning estimate; your table replaces all of them. Commit it as
`eval/results/w1-hardware.md`.

Report the **run-to-run spread**, not a bare median: on a machine in normal desktop use the
spread between invocations is wider than the spread inside one, so a single number is not
comparable across the five of us. `scripts/bench_runtime.py` measures it the same way on
every machine — decode rate from Ollama's own `eval_count / eval_duration`, peak VRAM sampled
against a measured idle baseline — and writes the file. Run it; do not hand-assemble a table.

**Week 2 — retrieval baseline, deliberately naive.**
Dense-only pgvector search, no reranking, no fusion, no contextualisation. Measure it.
This is the number everything later is compared against, so it needs to be honest rather
than flattering. A baseline you tuned is not a baseline.

**Week 3 — first full run.**
Hybrid retrieval with RRF, contextualised chunks, the reranker. Run Ragas against golden
Set A. Commit the results and a paragraph on what changed and why you think so.

**Weeks 4–7 — one change at a time.**
Chunk size, the contextualisation prompt, `top_k` before and after reranking, the abstain
floor. Each is its own pull request with its own numbers. A pull request that changes
three things at once has told you nothing about any of them.

**Week 5, week 8 — full runs.** Same sets, same harness. The report presents movement.

---

## The three golden sets

| Set | Size | What it tests | Who writes it |
|---|---|---|---|
| A · Answerable | 60 | The system finds the right evidence and answers from it | Everyone, 12 each, by end of week 3 |
| B · Hard negatives | 25 | The system **declines** — the answer is genuinely not in the corpus | You |
| C · Adversarial | 15 | Prompt injection, contradictory documents, out-of-scope requests | Siew |

Set B is still the set to care about, but the number it feeds is no longer abstention rate
on its own. The headline counts *unsupported claims* across every set — a hard negative
answered, a wrong value, a false "not on file", a forbidden string — because what the system
must not do is guess, and a decline in honest words serves that as well as a decline at the
gate. Abstention rate on Set B is still reported, as a diagnostic.

Every golden question cites the document and page its answer comes from, taken from
Desmond's register. That is what makes the set gradeable without a human in the loop.

---

## Headline and diagnostics

The report leads with five numbers, one for each aim, scored by code — proposed, awaiting DY.
The full definitions are in [`eval/README.md`](../../eval/README.md#the-headline--proposed-awaiting-dy);
this table is a pointer, so the two cannot drift.

| Headline | Direction |
|---|---|
| Right and cited (Set A) | Higher is better |
| Unsupported claims (every set) | Lower is better; none on Set C, ever |
| Over-caution (Set A) | Lower is better |
| Casual-phrasing gap | Should close |
| Filed correctly (extraction F1) | Line 0.90 |

The nine metrics the proposal named — context recall and precision, faithfulness, answer
relevancy, Set B abstention, extraction F1, obligation precision, alert false-positive rate,
decode throughput and peak VRAM — are still measured on every run, as diagnostics with their
proposal lines as references.

The judge model is served locally through Ollama's OpenAI-compatible endpoint. No
evaluation question leaves the machine — that is a governance commitment, not a
preference, and Siew's data inventory says so.

---

## Starter prompt for your coding agent

> Read `AGENTS.md`, `team/yew-mun/README.md`, `core/contracts.py` and
> `db/migrations/0001_init.sql` completely before writing anything.
>
> I own `core/retrieve/` and `eval/`. Do not modify anything outside those two
> directories — in particular never touch `core/contracts.py` or `db/migrations/`, which
> are separate reviewed pull requests.
>
> Task: [describe one change, e.g. "implement hybrid retrieval fusing pgvector cosine
> search and Postgres full-text search with reciprocal rank fusion, k=60"].
>
> Constraints from `AGENTS.md` that apply here: no runtime SQL generation — queries are
> hand-written and parameterised; no new runtime dependency without an ADR in
> `docs/adr/`; type hints everywhere and `mypy --strict` passes on `core/`.
>
> Work in this order: propose the approach and the function signatures first and wait
> for me; then implement; then write a test that uses the corpus register in
> `corpus/register/` as ground truth rather than live documents; then run `make check`
> and `make eval-quick` and show me the numbers. Change one variable at a time — if the
> task implies two changes, tell me and we will split it into two pull requests.

---

## Done

- [ ] `make check` passes
- [ ] Numbers from `make eval-quick` pasted into the pull request, with one sentence on
      why they moved
- [ ] The change is one variable, not three
- [ ] Results committed under `eval/results/`, never overwritten

**Getting a pass count for the pull request.** `pyproject.toml` already passes `-q` to pytest,
and a second `-q` on the command line suppresses the summary line, so the count never prints.
Clear the configured options instead:

```
uv run pytest -o addopts="" -q tests/test_eval_headline.py tests/test_eval_harness.py
```
