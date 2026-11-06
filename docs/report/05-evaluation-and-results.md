# §5 · Evaluation and results

**Owner: Yew Mun (Lane B).** Budget three and a half pages. The full results, every table and the
source of every claim are in [Appendix C](appendix-c-evaluation-results.md).

> **Status.** Two things are outstanding: **the synthetic-to-real gap**, which waits on the holdout
> (14 of a planned 40 real documents), and **the five-number headline**, which is proposed and
> awaiting the supervisor's sign-off. Gaps are marked **⟨holdout⟩**. §5.6 is Desmond's in the
> skeleton; the paragraph here is a draft for Desmond to take.

---

A household document assistant is useful because it answers *what is my excess?*, and dangerous for
the same reason: a confident, well-cited, wrong answer about an insurance policy is worse than no
answer. So this evaluation judges PARROT on whether it guesses, not on how often it declines.

## 5.1 Method

Every golden question cites the document and page its answer is printed on, taken from a corpus
register written before the documents existed, so all three sets are graded without a human:

| Set | Questions | Tests |
|---|---|---|
| A · answerable | 93 | The right evidence is found and answered from |
| B · hard negatives | 25 | The answer is absent, so any value given is a claim the documents do not support |
| C · adversarial | 15 | Injection, requests to act or advise, stale and absent records |

Nine metrics with targets were fixed in week 1, before any had a value. Four are Ragas metrics
(Es et al., 2023), judged by a model on the local machine, so no evaluation question leaves it.

**In mid-October the evaluation was found rewarding the wrong things.** On ten casually phrased
questions, the code scorer passed seven; a person passes four. One answer gave a different plan's
SGD 3,500 deductible for a 500 one, and the judge scored it 1.0 for faithfulness, because the
passage it quoted was real. The report now leads with five numbers, one per aim, scored by code
against the register (proposed, awaiting sign-off). The nine metrics remain as diagnostics. Run
twice unchanged, the register-scored numbers agree to four decimals, while faithfulness and
relevancy move by up to 0.05.

The runs fall on 29–30 September and 19–20 October. **Run 3 is a new corpus, not a new
configuration:** 93 documents frozen at a Git commit and loaded into a vault of their own.

## 5.2 The baseline

Dense-only retrieval, with no fusion and no reranking, cleared its recall and precision targets on
six documents, which meant nothing. **Growing the corpus to 26 documents, with no code change, cost
0.074 of recall and 0.101 of precision.** That rebaseline is what Run 2 is compared against, so
Run 2 changes the retrieval and nothing else.

## 5.3 Results

| Aim | Headline | Run 1 · 6 docs | Run 2 · 26 | **Run 3 · 93** | On `main`, 28 Oct |
|---|---|---|---|---|---|
| Do not guess | **Unsupported claims** (A, B) | 9/44 | 19/64 | **25/118** | 21/118 |
| Answer with the page | Right and cited (A) | 16/19 | 31/39 | **72/93** | 77/93 |
| Answer when able | Over-caution (A) | 2/19 | 1/39 | **6/93** | 4/93 |
| Serve how people ask | Casual · formal | — | — | **8/10 · 64/83** | 8/10 · 69/83 |
| File correctly | Extraction F1 | 0.898 | 0.903 | **0.949** | 0.961 |
| The absolute line | Set C leaks | — | — | **0 of 15** | 0 of 15 |

The columns are measurements on different corpora, not a series. The last is Run 3's corpus reloaded
with the fixes Run 3 found. The share of answers making an unsupported claim was 0.20, 0.30 and
0.21: it did not grow with a corpus fifteen times larger. On `main` it is 0.18.

| Diagnostic | Target | Run 1 | Rebaseline | Run 2 | **Run 3** |
|---|---|---|---|---|---|
| Context recall | ≥ 0.85 | 0.895 | 0.821 | **0.897** | 0.848 |
| Context precision | ≥ 0.70 | 0.868 | 0.767 | **0.854** | 0.820 |
| Faithfulness | ≥ 0.90 | 0.819 | 0.810 | **0.967** | 0.892 |
| Answer relevancy | ≥ 0.80 | 0.765 | 0.776 | 0.779 | **0.834** |
| Abstention (Set B) | ≥ 0.95 | 0.76 | 0.56 | 0.52 | **0.52** |

**Run 3 missed five lines.** Recall and faithfulness sit just under theirs, on a vault three and a
half times larger. Abstention is far below. Obligation precision was 0.8125 against 0.95. The alert
false-positive rate was 2/2 against 0.05: a courtesy title left in an extracted name matched nobody
and reported two policies as uncovered. Removing it fires no alert and changes none of the 118
answers.
Extraction cleared its line, and would read 0.982 but for a register convention on insurer names.
On the benchmark machine the generator writes 79 tokens a second with a full 16K window (§3.4), and
Run 3's median answer took 4.4 s.

## 5.4 What each component contributed

**Hybrid retrieval and a cross-encoder, added together, recovered what the larger corpus cost.**
Dense search cannot reliably find a policy by its printed number, so dense and full-text rankings
are fused by reciprocal rank (Cormack et al., 2009, *k* = 60), and a reranker keeps six of forty
candidates. Faithfulness rose from 0.810 to 0.967, the largest movement in the project: with the
answering page reliably among the six, the model stopped reaching for a neighbouring document.

No run separates the two, and none measures the chunks' context prefix alone. The credit most likely
belongs to the cross-encoder, because the full-text arm then required every word of a question to
be printed, and found nothing for 60 of Run 3's 93 answerable questions. Matching any word added two
right answers. Three further changes were measured and rejected, one of them a different reranker
that raised abstention to 0.60 at a net cost of three right answers.

**The relevance floor** was swept at three settings on Run 2's corpus (ADR 0019). Off, abstention
was 0.52. At 0.002 it was 0.56, and the share of Set A answered fell from 0.974 to 0.897. At 0.02 it
was 0.64, and faithfulness and recall fell back under their lines. It was rejected. By Run 3,
retrieval is no longer where answers are lost:
**19 of Set A's 21 misses had the answering page among the passages read.**

## 5.5 Unsupported claims

| Unsupported claim | Set | Run 3 | 28 Oct |
|---|---|---|---|
| Answered, with no answer on file | B | 12 | 10 |
| Wrong value | A | 8 | 7 |
| False "not on file" | A | 5 | 4 |
| **Total, of 118** | | **25** | **21** |

The largest share is the hard negatives. As documents arrived, each question acquired a page that
is relevant and silent on the point asked, and a system shown a relevant page answers from it. That
is why abstention, read alone, fell as retrieval improved, and why no threshold fixes it: the
questions that get answered are exactly those with a relevant page. Citation does not cure this.
Magesh et al. (2025) found retrieval-based legal research tools hallucinating on 17 to 33 per cent of
queries, and a false claim beside a real source is precisely what a citation makes convincing.

What these share, by Run 3, is a printed value under a different label: "the named driver is
Marcus" cites `Name of Insured`. ADR 0021 checks each value against the label beside it, for two
fewer claims and no right answer lost. It reaches only some cases, and it is built, measured and
switched off, pending review.

## 5.6 Adversarial findings

Set C contained all fifteen questions in Run 3, and nothing leaked. Earlier that day it had leaked
twice: a stranger's name close to a family member's, and "my brother's car", with no brother on
file. Both drew someone else's policy, and both now stop at scoping. Set C's planted documents had
also been distorting the other sets: one printed the real car policy's number and outranked the real
schedule, changing four answers in both directions. Set C is now scored on a clone of the vault.

## 5.7 Threats to validity

These follow the frame of Wohlin et al. (2012).

- **Construct.** The five numbers proxy for a household's trust; none measures it. A code scorer
  sees only what the register records, and citations are graded per document where no field records
  its page. The headline is proposed, so the nine metrics remain the agreed basis.
- **Internal.** Hybrid retrieval and the reranker arrived together. The team that built the system
  wrote the questions, and four lanes' generated questions are unreviewed drafts. The judge is named
  in every result file but not pinned in configuration.
- **External.** ⟨holdout⟩ **Every number here is on synthetic documents about one household.** The
  holdout will measure the gap.
- **Conclusion.** Three runs on three corpora are not a trend, except where the direction is plain.
  The casual gap rests on ten questions, the alert rate on two alerts.

---

### References used in this section

Cormack, G. V., Clarke, C. L. A., & Büttcher, S. (2009). Reciprocal rank fusion outperforms Condorcet
and individual rank learning methods. In *Proceedings of the 32nd international ACM SIGIR conference
on research and development in information retrieval* (pp. 758–759). ACM.
https://doi.org/10.1145/1571941.1572114

Es, S., James, J., Espinosa-Anke, L., & Schockaert, S. (2023). *Ragas: Automated evaluation of
retrieval augmented generation* (arXiv:2309.15217). arXiv.
https://doi.org/10.48550/arXiv.2309.15217

Magesh, V., Surani, F., Dahl, M., Suzgun, M., Manning, C. D., & Ho, D. E. (2025). Hallucination-free?
Assessing the reliability of leading AI legal research tools. *Journal of Empirical Legal Studies*,
*22*(2), 216–242. https://doi.org/10.1111/jels.12413

Wohlin, C., Runeson, P., Höst, M., Ohlsson, M. C., Regnell, B., & Wesslén, A. (2012). *Experimentation
in software engineering*. Springer. https://doi.org/10.1007/978-3-642-29044-2
