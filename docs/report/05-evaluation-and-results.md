# §5 · Evaluation and results

**Owner: Yew Mun (Lane B).** Feeds §5, and the retrieval half of §3. About four pages with tables.

> **Draft status.** Written from three committed runs. **Run 3** (19–20 October) scored every
> question on a frozen corpus in a vault of its own. Two things are still outstanding:
> - **the synthetic-to-real gap**, which waits on the holdout (14 of a planned 40 real documents,
>   run on the integration machine);
> - **the five-number headline in §5.2**, which is proposed and awaiting the supervisor's sign-off.
>
> Gaps are marked **⟨holdout⟩**.

---

## 5.1 The claim

A household document assistant is useful because it answers questions like *what is my excess?*,
and dangerous for the same reason: a confident, well-cited, wrong answer about an insurance policy
is worse than no answer.

> **Thesis.** Restraint is not a by-product of accuracy and cannot be measured as one. On this
> corpus, retrieval and generation improved while the system's willingness to decline got *worse*,
> not through any regression: better retrieval supplies plausible evidence for questions that have
> no answer. A system trusted with household documents must be measured on what it refuses to say,
> by a metric not derived from the signals that produce its accuracy.

Three runs support it. Abstention on the unanswerable set fell from 0.76 to 0.52 as retrieval
improved. It then **held at 0.52 through Run 3**, on a vault three and a half times larger, after
three weeks of fixes aimed elsewhere. Twelve of twenty-five hard negatives are still answered, each
citing a page that exists.

## 5.2 What was measured, and what is reported first

Every golden question cites the document and page its answer is printed on, taken from the corpus
register, so all three sets are graded without a human:

| Set | Run 3 | Tests |
|---|---|---|
| A · answerable | 93 | The right evidence is found and answered from |
| B · hard negatives | 25 | The system **declines**: the answer is absent |
| C · adversarial | 15 | Injection, requests to act or advise, stale and absent records |

Nine metrics with targets were fixed in week 1, before any had a value. The four Ragas metrics are
judged by `qwen2.5:7b-instruct` on the local machine. No evaluation question leaves it.

**In mid-October the evaluation was found rewarding the wrong things.** On ten casually phrased
questions, the code scorer passed seven; a person passes four. One "correct" answer opened by saying
no car policy was on file. Another gave a different plan's SGD 3,500 deductible for a 500 one, and
the judge scored it 1.0 for faithfulness, because the passage it quoted was real. The report now
leads with **five numbers, one per aim, scored by code against the register**:
- right and cited;
- unsupported claims, across every set;
- over-caution, meaning held back although the answering page was read;
- the casual-phrasing gap;
- extraction F1.

The nine metrics remain as diagnostics. One line is absolute: **no forbidden string on Set C.** This
is proposed, awaiting the supervisor's sign-off.

**Noise.** The same configuration run twice gives the register-scored numbers identical to four
decimals, while faithfulness and relevancy move by up to 0.05. Below that, a generation metric has
not moved.

## 5.3 The three-run spine

Run 1 and the rebaseline share a configuration, so run 2 changes one variable. **Run 3 is a new
corpus, not a new configuration.** It ran from a frozen Git commit loaded into its own vault, with
93 documents (39 of them unregistered statements kept as realistic noise), and every Set A question
answerable from them.

| Metric | Target | Run 1 · 6 docs | Rebaseline · 26 | Run 2 · hybrid + reranker | **Run 3 · 93 docs** |
|---|---|---|---|---|---|
| Context recall | ≥ 0.85 | 0.895 | 0.821 | **0.897** | 0.848 |
| Context precision | ≥ 0.70 | 0.868 | 0.767 | **0.854** | 0.820 |
| Faithfulness | ≥ 0.90 | 0.819 | 0.810 | **0.967** | 0.892 |
| Answer relevancy | ≥ 0.80 | 0.765 | 0.776 | 0.779 | **0.834** |
| **Abstention (Set B)** | ≥ 0.95 | 0.76 | 0.56 | 0.52 | **0.52** |
| Extraction F1 | ≥ 0.90 | 0.898 | 0.903 | 0.903 | **0.949** |
| _Set A scored_ | | _19_ | _39_ | _39_ | _**93**_ |

| Headline | Run 1 | Run 2 | **Run 3** |
|---|---|---|---|
| Right and cited (A) | 16/19 | 31/39 | **72/93** |
| Unsupported claims (all) | 9/44 | 19/64 | **25/118** |
| Over-caution (A) | 2/19 | 1/39 | **6/93** |
| Casual / formal phrasing | — | — | **8/10 · 64/83** |
| Set C contained | — | — | **15/15** |

The columns are measurements on different corpora, not a series:
- **Run 2:** three of four core targets cleared, extraction cleared.
- **Run 3:** relevancy clears for the first time and extraction reaches 0.949. Recall and
  faithfulness sit just under their lines on a vault three and a half times larger.
- **Abstention:** the one row that does not move.

## 5.4 Retrieval

The naive baseline cleared recall and precision on six documents, which meant nothing. **Growing
the corpus to 26 documents, with no code change, cost 0.074 of recall and 0.101 of precision.** A
retrieval score on a small corpus does not predict one on a realistic corpus.

**Hybrid retrieval and a cross-encoder, added together, recovered both.** Dense search cannot
reliably find a policy by its printed number, so dense and full-text rankings are fused (reciprocal
rank fusion, *k* = 60), and `bge-reranker-v2-m3` keeps six of forty candidates. The largest movement
in the project followed: **faithfulness, 0.810 → 0.967.** With the answering page reliably among the
six, the model stopped reaching for a neighbouring document to say something. Faithfulness is as
much a property of the context window as of the model.

**The credit most likely belongs to the cross-encoder.** No run separates the two, but the full-text arm
required every word of a question to be printed. On Run 3's vault it found nothing for 60 of the 93
answerable questions. Matching any word, ranked by how many are shared (#126), added two right
answers and removed a retrieval miss, with Sets B and C unchanged.

**Three further fixes were measured and rejected.** Giving the reranker the question in the
documents' own words cost a right answer. Printing each document's reference number in every
chunk's label answered both loan principals, but also answered a policy number that does not exist
with the real policy's premium; those values were already extracted, and issue #125 asks the answer
to use them. A different reranker raised abstention to 0.60 but lost seven right answers.

By Run 3, retrieval is no longer where answers are lost: **19 of Set A's 21 misses had the answering
page among the passages read.**

Measuring this honestly needed a vault of its own. Set C's planted documents had been sitting in
the vault that scores Set A, and one printed the real car policy's number and outranked the real
schedule. Removing them changed four answers *in both directions*. Since then Set C is scored on a
copy of the vault, and Run 3 on a corpus anyone can rebuild from a commit.

## 5.5 Abstention: the finding

| | Run 1 | Rebaseline | Run 2 | Run 3 |
|---|---|---|---|---|
| Abstention (Set B) | 0.76 | 0.56 | 0.52 | 0.52 |

Set B's questions are about the household's documents, but their answers are absent. As documents
arrived, each question acquired a page that is relevant and silent on the point asked, and a system
shown a relevant page answers from it. Better retrieval made this worse by succeeding.

**No threshold fixes it.** A relevance floor on the cross-encoder was built, swept and rejected
(ADR 0019). Every setting traded two cleared targets for a fraction of the missing one, because the
hard negatives that get answered are exactly those with a genuinely relevant page.

**What they share, by Run 3, is a printed value under a different label.** "The named driver is
Marcus" cites `Name of Insured`; "road tax due 12 April 2026" cites `Period of Insurance From`. A
score cannot see this, but the printed label can. ADR 0021 checks each stated value against the
label beside it: two fewer unsupported claims, no right answer lost, a quarter of a second per
answer. It reaches only some cases, and its judge still accepts "Name of Insured" as a named driver.
It is built, measured and switched off, pending review.

**Containment held where it must.** Set C contained all fifteen questions in Run 3. Earlier that day
it had leaked twice: a stranger's name close to a family member's, and "my brother's car", with no
brother on file. Both drew someone else's policy, and both now stop at scoping (#103).

**Part of the number was the metric, against the system.** Counting abstentions from an internal
flag missed prose refusals and inventory-only answers. Classifying behaviour raised every run. In
Run 3, thirteen of twenty-five were held back: five at the gate, seven with only code-written "on
file" lines, one in prose. That is 0.52 against the flag's 0.44.

## 5.6 Extraction

The earlier draft of this chapter predicted that extraction would fall as harder document types
arrived. **It rose, to 0.949 across sixteen types,** because four extractor defects were found and
fixed, each measured before it merged (#77, #79, #80, #110):
- field descriptions never reached the model;
- the decoding grammar let it skip optional fields;
- a title printed mid-page was read last;
- a yes/no field could never be placed on a page.

What remains is a register convention. The extractor copies insurers as printed ("Meridian Assurance
Singapore Pte. Ltd."), as the field's definition asks, while the register records the short brand.
**Without that, Run 3's extraction is 0.982.**

## 5.7 Module metrics

These are kept apart from the RAG metrics, and in Run 3 both failed for a reason outside the module:
**both alerts that fired were false (rate 2/2), and one reminder went to the wrong person (precision
0.875).** The new renewal notices print "Mr Marcus Lim Jun Wei". The title stayed in the extracted
name, which then matched nobody, so his policies were reported uncovered for 262 and 233 days.
Stripping courtesy titles (#120), measured on Run 3's exact corpus:
- no alert fires;
- obligation precision rises to 0.9375;
- all 118 answers are unchanged.

> A module reads extracted facts, so **one extra word in a name is indistinguishable from a person
> whose insurance has lapsed**. That is why these metrics are scored against the register, not
> against the facts the module reads.

## 5.8 Runtime

The 4B generator decodes at 130 tok/s with 7.4 GB peak VRAM, falling to 79 tok/s on a realistically
full context. In Run 3, the median answer took 4.4 s. One committed statement crashes Docling on
Apple's GPU, so Run 3 was loaded on the CPU.

## 5.9 Limitations

1. **⟨holdout⟩ Every number is on synthetic documents.** The holdout (14 real, redacted documents
   of a planned 40) will measure the gap.
2. **Three runs, three corpora:** the columns are not a trend, except where the direction is plain
   (abstention, extraction).
3. **Twelve of twenty-five hard negatives are still answered,** and the one measured remedy is
   switched off.
4. **The headline is proposed, not agreed.** Until it is signed off, the nine metrics and their
   targets remain the agreed basis.
5. **The judge is named in every result file but not pinned in configuration.** Four lanes'
   generated questions are unreviewed drafts. Citations are graded per document where no field
   records its page.
6. **The module metrics rest on two alerts.** Each is a found defect reported as a rate.

## 5.10 What remains

- **The holdout gap** ⟨holdout⟩.
- **The supervisor's sign-off** on the headline.
- **A decision on ADR 0021.**
- **The register's insurer names,** after which extraction can be re-scored from stored facts
  without re-running the system.

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

**Since run 2, in date order.** A source for each finding the chapter will draw on, not yet
written into it. In week 8 the body draws on these; each claim points at a committed file or a
merged pull request, never at memory. Result files are under `eval/results/`.

| Date | Claim | Source |
|---|---|---|
| 5 Oct | Set C's first reading: one genuine leak, and injection items passing against an empty vault | `2026-10-05-set-c-first-reading`, issue #48 |
| 14 Oct | Set C read by behaviour (held back) rather than the Answer flag, which is kept as #16's tracker | `2026-10-14-setc-behaviour-reading`, `2026-10-14-setc-injection-planted`, #60 |
| 14 Oct | Banded replay: no cosine edge up to 0.60 reaches 0.95 abstention without costing answerable questions | `2026-10-14-bands-first-look`, `2026-10-14-floor-off`, `docs/superpowers/specs/2026-10-14-banded-abstention-eval-design.md`, `eval/bands.py` |
| 14 Oct | Ten casual questions: the old scorer passed 7, a person passes 4 | `2026-10-14-production-colloquial` and its `-headline` companion |
| 15 Oct | The headline moves to five aim-based numbers; the nine metrics become diagnostics (proposed, awaiting DY) | `docs/superpowers/specs/2026-10-15-aim-headline-metrics-design.md`, `eval/headline.py`, `eval/README.md`, #67 |
| 15 Oct | Set C's planted documents were distorting Sets A and B in both directions; they now get a vault of their own | `2026-10-15-fixtures-in-vault`, `2026-10-15-fixtures-removed`, `2026-10-15-setc-isolated-vault`, `eval/setc.py`, #71 |
| 15 Oct | A false "none of the policies is a car policy", from one mis-extracted product name, caused 5 of 14 Set A misses | `2026-10-15-absence-needs-every-kind`, #76, issue #48 |
| 15–17 Oct | Extraction: field descriptions never reached the model; optional fields were skipped by the decode grammar; reading order put a title last. Re-extraction 135/7/31 → 164/3/2 | #77, #79, #80 (offline measurements in their pull requests) |
| 17 Oct | The vault rebuilt: extraction 0.875 → 0.976, and better chunks bring car hard negatives over the floor (ADR 0019's trade-off again) | `2026-10-17-vault-rebuilt`, #87 |
| 17 Oct | Two hard negatives the corpus had since made answerable; one moved to Set A, one retired | `eval/sets/hard_negatives/lane-b.jsonl` (comment lines), #88 |
| 17–19 Oct | "Last year" must cite a document from last year; a loan runs on from its signing | `2026-10-17-time-scoped-claims`, `2026-10-19-standing-before`, `2026-10-19-standing-after`, `core/graph/period.py`, #89, #97 |
| 19 Oct | A printed value checked against its printed label: rejected at first (+3 over-caution), accepted on its own conditions after two fixes; reaches two of four car claims and catches one | `docs/adr/0021-a-printed-value-is-checked-against-the-label-printed-beside-it.md`, `2026-10-19-label-check-{off,on}`, `2026-10-19-label-check-{off,on}-2`, #98, #99 |
| 19 Oct | Set C leaked twice (a near-miss name; "my brother's"); fixed to 15/15 with Sets A and B unchanged | `2026-10-19-setc-scope-before`, `2026-10-19-setc-scope-after`, `2026-10-19-scope-strangers`, #103 |
| 19 Oct | Run 3 runs on a frozen commit in an isolated vault, never the shared one; rehearsed end to end | `eval/freeze.py`, `eval/setc.py --from`, `eval/README.md` "Running Run 3", issue #85, #100, #101, #102, #106, #107 |
| 19–20 Oct | **Run 3**: 93 documents from frozen commit `d45f12d`, all 118 Set A/B questions, judged; Set C 15/15; loaded on the CPU after a GPU crash | `2026-10-19-run3-freeze-all`, `2026-10-19-run3` and its `-headline` companion, `2026-10-20-run3-setc`, #119, issue #85 |
| 20 Oct | A courtesy title in a name made both Run 3 alerts false; removing it, measured on Run 3's corpus | `2026-10-20-titles-ab`, `2026-10-20-titles-freeze`, #120 |
| 20 Oct | The full-text arm needed every word and found nothing for 60 of 93 Set A questions; any word, ranked by how many: right and cited 72 → 74, Set C 15/15 | `2026-10-20-lexical-all-words`, `2026-10-20-lexical-any-word`, `2026-10-20-lexical-any-word-setc`, #126 |
| 20 Oct | Four "not stated" answers whose value the extractor had stored | issue #125 |
| 20–21 Oct | Rejected: the reranker reading the documents' words (right and cited 74 → 73); the reference number in every chunk label (a near-miss policy number answered) | `2026-10-20-rerank-printed-words`, `2026-10-21-label-without-reference`, `2026-10-21-label-with-reference`, issue #125 |
| 21 Oct | Four rerankers screened; `mxbai-rerank-large-v1` on the full sets: abstention 0.52 → 0.60, right and cited 74 → 71. Rejected | `2026-10-21-reranker-screen`, `2026-10-21-reranker-mxbai-large-v1` |
