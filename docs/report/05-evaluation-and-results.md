# §5 · Evaluation and results

**Owner: Yew Mun (Lane B).** Feeds §5, and the retrieval half of §3. About four pages with tables.

> **Draft status, because it changes how to read everything below.** This chapter is written from
> two committed runs. **Run 3 has not happened** — due in week 8, blocked on the holdout corpus — so
> the three-run table that is meant to be its spine has an empty third column. Anything marked
> **⟨run 3⟩** is a gap, not an omission; two claims (the synthetic-to-real gap, and adversarial
> containment) cannot be made at all yet.

---

## 5.1 The claim

A retrieval system is normally reported on how often it finds the right evidence and how faithfully
it answers from it. For a household document assistant that is the less important half, because the
question that makes it useful — *what is my excess?* — is the question that makes it dangerous: a
confident, well-cited, wrong answer about an insurance policy is worse than no answer.

> **Thesis.** Restraint is not a by-product of accuracy and cannot be measured as one. On this
> corpus every retrieval and generation metric improved while the system's willingness to decline
> got steadily *worse*, and not through any regression: better retrieval supplies plausible evidence
> for questions that have no answer. A system to be trusted with household documents must be
> measured on what it refuses to say, by a metric not derived from the signals that produce its
> accuracy.

Two findings support it. The metrics that carry the claim are the five that need no judge — they are
arithmetic against the corpus register, so they cannot be argued with. And a measurement can fail in
two directions: the abstention metric was itself wrong and had to be rebuilt from behaviour (§5.5),
while the module false-positive rate was correct and pointed at a defect in another lane (§5.7).

## 5.2 What was measured

Nine metrics with numeric targets were agreed in week 1 and written into `eval/README.md` before any
of them had a value, so that no target could be chosen after seeing a result. Three golden sets:

| Set | Size | Tests | Author |
|---|---|---|---|
| A · answerable | 72 written, **39 scorable** | The right evidence is found and answered from | All five lanes, 12 each |
| B · hard negatives | 25 | The system **declines** — the answer is genuinely absent | Lane B |
| C · adversarial | **0 ⟨run 3⟩** | Injection, contradiction, requests to act | Lane C |

Questions are generated from the register, which is complete, while documents are mail-merged from it
afterwards — so a question whose document does not exist yet is skipped and counted
(`run.skipped_no_document`) rather than scored as a retrieval failure. Metrics 1–4 are judged by
Ragas with `qwen2.5:7b-instruct` on the local Ollama endpoint: no evaluation question leaves the
machine, which is a governance commitment, not a preference.

**How much of a delta is a delta.** One configuration run twice an hour apart with nothing changed
returned context recall, context precision and extraction F1 *identical to four decimal places*,
while faithfulness and relevancy moved by 0.046 and 0.012 on their own. So a change under about 0.05
in the two generation metrics is noise, and any change in a register-scored metric is real. One
question is 0.04 on Set B and 0.026 on Set A, which is the other, exact, kind of noise.

## 5.3 The three-run spine

Run 1 and the rebaseline are the same configuration on different corpora, so that run 2's change is
one variable rather than two.

| Metric | Target | Run 1 · 6 docs | Rebaseline · 26 docs | Run 2 · hybrid + reranker | Run 3 |
|---|---|---|---|---|---|
| Context recall | ≥ 0.85 | 0.895 ✓ | 0.821 ✗ | **0.897 ✓** | ⟨run 3⟩ |
| Context precision | ≥ 0.70 | 0.868 ✓ | 0.767 ✓ | **0.854 ✓** | ⟨run 3⟩ |
| Faithfulness | ≥ 0.90 | 0.819 ✗ | 0.810 ✗ | **0.967 ✓** | ⟨run 3⟩ |
| Answer relevancy | ≥ 0.80 | 0.765 ✗ | 0.776 ✗ | 0.779 ✗ | ⟨run 3⟩ |
| **Abstention rate (Set B)** | ≥ 0.95 | 0.76 ✗ | 0.56 ✗ | **0.52 ✗** | ⟨run 3⟩ |
| Extraction F1 | ≥ 0.90 | 0.898 ✗ | 0.903 ✓ | 0.903 ✓ | ⟨run 3⟩ |
| Obligation precision † | ≥ 0.95 | — | — | **1.000 ✓** | ⟨run 3⟩ |
| Alert false-positive rate † | ≤ 0.05 | — | — | **1.000 ✗** | ⟨run 3⟩ |
| Decode / peak VRAM | measured | 130 tok/s · 7.4 GB | 130 · 7.4 | 130 · 7.4 | ⟨run 3⟩ |
| _Set A questions scored_ | | _19 of 72_ | _39 of 72_ | _39 of 72_ | |

† Measured on 1 October against the same vault and code, not during the 30 September pass: the
harness could not yet produce them, and the run-2 file records them as nulls
(`eval/results/w7-module-metrics.md`). Every later run carries them, with the day swept for recorded
as `modules_as_of`, because both are gaps measured against a date.

Read down the run-2 column and the system looks like one that works: three of four RAG-core targets
cleared, extraction cleared, obligations perfect. Read across the abstention row and it is going
backwards through both changes, by 0.24 in total. Both readings are correct.

## 5.4 Retrieval: what the two changes bought

**The baseline was deliberately naive** — dense pgvector cosine search, no fusion, no reranking, on
six documents. It cleared recall and precision immediately, which meant nothing: six documents of one
type is a haystack with almost no hay. **Quadrupling the corpus to 26 documents then cost 0.074 of
recall and 0.101 of precision with no code change at all** — the most transferable number here, since
it means a retrieval score measured on a small corpus does not predict the same score on a realistic
one, and the only way to know the difference is to re-run the baseline rather than compare against it.

**Hybrid retrieval and a cross-encoder recovered both.** Dense search cannot reliably find a policy
by its printed number — `MV-2026-448120` is a token cosine similarity has no special respect for — so
a dense ranking and a Postgres full-text ranking are fused by reciprocal rank fusion at *k* = 60,
with a boost for an exact identifier match; forty candidates then go to `bge-reranker-v2-m3`, which
reads each against the question and keeps six. Recall returned to 0.897 and precision to 0.854, both
above where they stood on a corpus a quarter of the size.

The unexpected result is **faithfulness, 0.810 → 0.967**, three times the noise floor and the largest
movement in the project. The gate was always meant to make faithfulness high by construction, by
refusing any factual sentence with no supporting chunk attached; what the reranker changed is *which
six passages* the model saw. With the answering page reliably among them it stopped reaching for a
neighbouring document to say something with — so faithfulness is as much a property of the context
window as of the model.

**ADR 0018** records the one architectural consequence: the reranker runs in-process with
`transformers`, because Ollama cannot serve a cross-encoder — the GGUF build crashes `llama-server` on
an assertion about output counts. It is the project's only exception to "Ollama for all inference",
and it is there because of a measured failure rather than a preference.

## 5.5 Abstention: the finding

| | Abstention (Set B) | What changed |
|---|---|---|
| Run 1 | **0.76** | 6 documents |
| Rebaseline | **0.56** | 26 documents, nothing else |
| Run 2 | **0.52** | hybrid retrieval + cross-encoder |

Set B's questions are *about* the household's documents while their answers are genuinely absent. On
six documents most had nothing plausible to retrieve and the gate declined. As documents arrived,
each acquired a page that is topically relevant and silent on the point asked — and a system shown a
relevant page answers from it. Better retrieval made this worse by succeeding: the top six became
genuinely more relevant, which is exactly what makes a non-answer look answerable.

**A relevance floor does not fix it, and this was measured rather than argued.** Having the
cross-encoder drop anything below a threshold, so the gate sees an empty list and declines, was
built, swept over the full golden sets, and rejected:

| Floor | Abstention (B) | Faithfulness | Recall | Abstention precision |
|---|---|---|---|---|
| 0.0 (off) | 0.52 | 0.967 ✓ | 0.897 ✓ | 0.929 |
| 0.002 | 0.56 | 0.936 ✓ | 0.872 ✓ | 0.778 |
| 0.02 | 0.64 | 0.809 ✗ | 0.821 ✗ | 0.762 |

Every setting trades two cleared targets for a fraction of the missing one, and the trade worsens the
harder it is pushed, because the hard negatives that *do* get answered are precisely those with a
genuinely relevant page: their best passage scores like a good passage, and no threshold separates
them from Set A without discarding Set A's evidence too. The mechanism ships, off, pinned by a test;
the decision is **ADR 0019, rejected by measurement** — a rejected ADR with its sweep attached being a
better artefact than a quietly abandoned branch.

**Part of the number was the metric, and in the system's disfavour.** The first implementation counted
an abstention when the gate failed or an `unanswered` flag was set, which misses two behaviours any
user would call declining: a prose refusal in the model's own words, and an answer whose every
sentence is a vault inventory written by the code rather than a claim about the question. Classifying
what the answer *did* instead raised every run — 0.76 against the flag's 0.56 on run 1, 0.56 against
0.36 on the rebaseline, 0.52 against 0.40 on run 2. On run 1, nineteen of twenty-five Set B questions
were held back and the flag recognised fourteen. Both readings are kept in every result file and will
converge when the flag is fixed (issue #16); until then the gap is the measurement error, reported
rather than resolved in favour of whichever number suits. The point cuts opposite to the usual worry
about self-reported metrics: the headline number was wrong by up to 0.20 *against* the system, because
a metric derived from an internal flag measures the flag, whatever it is named after.

## 5.6 Extraction, by document type

Every document was authored *from* a register row, so the correct value of every printed field is
known without a human in the loop. The headline is **0.903 against a 0.90 target**, and the split
shows why it should not be leaned on:

| Document type | Docs | Fields | Precision | Recall | F1 |
|---|---|---|---|---|---|
| `loan_agreement` | 2 | 13 | 0.889 | 0.667 | 0.762 ✗ |
| `policy_schedule` | 12 | 108 | 0.934 | 0.833 | 0.881 ✗ |
| Five identity and payroll types | 9 | 37 | 1.000 | 1.000 | 1.000 ✓ |
| **Every type** | 23 | 158 | 0.949 | 0.861 | **0.903 ✓** |

Eleven of the 23 scored documents are identity documents and payslips with three to six fields each,
all perfect, while `policy_schedule` — 108 of the 158 fields — is below target. As the remaining seven
register types arrive this number should be expected to **fall**, because the easy types are the ones
already indexed.

The failures are recall, not precision (0.949 against 0.861; 7 false claims against 21 misses) and
they concentrate in three fields, which is the shape of a template problem rather than a model one.
`expiry_date` is read on 5 of 11 schedules and the split is exactly the printed date format: every
schedule printing `11 April 2027` was read, every schedule printing `2027-02-28` was missed. `excess`
was read on 0 of 6, including a clean 519-character document printing `Excess: 3500.00` on its own
line. Both are issue #32. Two of `product_name`'s four misses are documents where the register's value
is not printed at all — the corpus disagreeing with itself (issue #19) — so precision is understated.

## 5.7 The two module metrics, and the lesson in them

These are reported apart from the RAG metrics because an alert module can be perfect on a system that
retrieves badly, and the reverse.

**Obligation precision is 1.000, and it is a smaller claim than it looks.** All seven
document-derived obligations name a date their own document prints, for the person it is about — but
the register supports **sixteen** and seven exist, because an obligation can only be created from a
fact the extractor wrote. Precision says what the reminder module raised was true; it says nothing
about completeness, and fewer than half the household's policies can currently produce a reminder.

**The alert false-positive rate is 1.000 against a ceiling of 0.05 — and the alert module has no
defect in it.** One alert fired: `days_uncovered`, claiming 215 days without cover, cited to the
renewal notice it came from. The register says that policy runs to 2027-02-28, with 150 days still to
run. The vault holds the renewal notice's older expiry and not the policy schedule's current one,
because that schedule prints ISO dates — §5.6's missing field. The module took the latest expiry it
could see, found it in the past, and said so correctly.

> A module metric can fail completely on a module containing no defect, because a module reads
> extracted facts and **a missing fact is indistinguishable from a world in which the thing never
> happened**. One unextracted field produced a confident, cited, wrong alert about a person's
> insurance having lapsed.

It is also why the metric is scored against the register and not against the facts table: a module
checked against the same facts it reads would have scored this alert correct.

## 5.8 Runtime

`Qwen-SEA-LION-v4-4B-VL` at Q4_K_M runs entirely on the GPU at every context size tested, decoding at
**130 tok/s (spread 126–133) with 7.4 GB peak VRAM at 16K** — reported as a median with its spread,
because the variation between invocations is wider than the variation within one. The figure that
matters for the product is not that one: on a **realistically filled 13,781-token context the rate
falls to 79 tok/s**, about 40% slower, and that is the configuration a user actually experiences. The
full table by context size and prompt length is `eval/results/w1-hardware.md`; every VRAM number in
the original proposal was a planning estimate and these replace them.

## 5.9 Limitations

Stated here rather than in §8, where they would arrive too late to qualify the numbers above.

1. **⟨run 3⟩ No third run, so no trend.** Two measurements show a delta; three show a direction.
2. **⟨run 3⟩ Set C does not exist** — zero adversarial questions on disk, so injection, contradiction
   and requests to act are **entirely unmeasured**, and no containment claim is made.
3. **⟨run 3⟩ Every number is on synthetic documents**, which are cleaner than real ones; the redacted
   40-document holdout will say by how much, and that gap is the honest result.
4. **Half the corpus is not indexed** — 26 of 50 register rows, 39 of 72 Set A questions — so these
   scores are optimistic in the way run 1's were.
5. **Four lanes' golden questions are unreviewed generated drafts**: correct by construction, but not
   read by the lanes owning the subject matter.
6. **The judge is not pinned** in `core/runtime/settings.py`, so comparability across runs rests on
   convention rather than configuration.
7. **`field_pages` is filled on 0 of 50 register rows**, so citations are graded at document rather
   than page granularity.
8. **One alert is not a rate**: metric 8 had two possible values, and is a found defect reported as a
   rate because the metric list requires one.

## 5.10 What run 3 must add

- The third column of §5.3, same sets, same harness, judge named.
- Set C, and a refusal-and-containment paragraph in §5.5.
- The holdout run: synthetic against real, side by side, gap stated plainly.
- `eval.report` and `eval.modules` re-run once the remaining batch is indexed — §5.6's table is
  expected to fall, and the chapter should say so having seen it rather than having predicted it.
- Whether #32 and #16 landed. If #32 does, extraction F1, obligation completeness and the alert
  false-positive rate all move together from one fix, which is a paragraph in itself.

---

### Sources in this repository

| Claim | File |
|---|---|
| Metrics, targets, noise floor | `eval/README.md` |
| The three runs | `eval/results/2026-09-29-baseline-dense-only.{json,md}`, `2026-09-30-rebaseline-dense-only-26-docs.{json,md}`, `2026-09-30-run2-hybrid-plus-reranker.{json,md}` |
| The floor sweep | `eval/results/2026-09-30-floor-{0002,002}-relevance.{json,md}` |
| Extraction by type and field | `eval/results/w6-extraction-by-doc-type.md` |
| Module metrics | `eval/results/w7-module-metrics.md` |
| Runtime | `eval/results/w1-hardware.md` |
| Reranker in-process | `docs/adr/0018-the-reranker-runs-in-process-because-ollama-cannot-serve-a-cross-encoder.md` |
| Relevance floor rejected | `docs/adr/0019-the-reranker-drops-what-does-not-answer-the-question.md` |
| Retrieval implementation | `core/retrieve/hybrid.py`, `core/retrieve/rerank.py`, `core/retrieve/README.md` |
| Open defects cited | issues #16, #19, #32 |
