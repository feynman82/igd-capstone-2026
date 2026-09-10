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
decode tokens per second, peak VRAM, for `Qwen-SEA-LION-v4-4B-VL` on one card and for
the 27B variants as the quality comparison. Every VRAM number currently in the proposal
is a planning estimate; your table replaces all of them. Commit it as
`eval/results/w1-hardware.md`.

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

Set B is the one to care about. The headline result we intend to lead with is not
accuracy — it is abstention rate on Set B. A system that declines when its evidence does
not cover the question is making a claim about trustworthiness that an accuracy score
cannot make on its behalf. Target is 0.95, and it is the number most likely to be
disappointing at run 1.

Every golden question cites the document and page its answer comes from, taken from
Desmond's register. That is what makes the set gradeable without a human in the loop.

---

## Targets

| Metric | Component | Target |
|---|---|---|
| Context recall | RAG core | ≥ 0.85 |
| Context precision | RAG core | ≥ 0.70 |
| Faithfulness | RAG core | ≥ 0.90 |
| Answer relevancy | RAG core | ≥ 0.80 |
| Abstention rate on Set B | Grounding gate | ≥ 0.95 |
| Field extraction F1 | Extraction | ≥ 0.90 |
| Decode throughput, peak VRAM | Runtime | Measured and reported |

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
