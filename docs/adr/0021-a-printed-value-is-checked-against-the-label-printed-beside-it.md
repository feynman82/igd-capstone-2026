# 0021 · A printed value is checked against the label printed beside it, before it is believed

- **Status:** Proposed. The check is built behind a switch that is off; this record decides whether it is turned on.
- **Date:** 2026-10-19
- **Decider:** Yew Mun (Lane B). Reviewers: Christian (the gate, `core/graph/`), Siew (what a refusal claims)
- **Answers:** ADR 0019's "revisit when": refusing an answer for naming something the page does not carry.

## Context

Every Set B claim left after #87–#97 cites a real page and quotes a value that page really prints.
`check_content` confirms the number is there; nothing confirms it *means* what the sentence says.
Measured on 19 October, the car questions are the clearest case:

| Item | The sentence | What the page prints beside that value |
|---|---|---|
| `b-b06` | "The named driver on the car policy is Marcus Lim Jun Wei." | `Name of Insured: Marcus Lim Jun Wei` |
| `b-b14` | "The road tax on SLK 8842 D is due on 12 April 2026." | `Period of Insurance From: 12 April 2026` |

Neither a similarity score nor a relevance score can tell these apart from a right answer (ADR
0019). The label can: it is printed, and it disagrees with the sentence.

## Decision

A sentence that states a value is checked against the **label printed beside that value**:

1. **Code finds the label.** Docling's tables reach the passages as `label: value` lines
   (`core/ingest/parse.py`), so for each printed value the sentence repeats — a name, a date, an
   amount however formatted — on such a line in a cited passage, the label is the text before
   the colon. A value printed with
   no label — a letterhead, a sentence of prose — is not checked, and the sentence keeps its place.
2. **The generator judges meaning.** One constrained call per checked sentence, with the sentence
   and its printed `label: value` lines, asking whether the label supports what the sentence calls
   the value. "No" drops the sentence, as `check_content` drops an unprinted number.

It ships as an `AnswerGraph` option, **off**, with `eval.run --label-check` to turn it on for a
run and every result file recording it — the same apparatus as ADR 0019's floor. It is not a pack
manifest field: that would change `core/contracts.py` for an experiment. It is turned
on only if, on Sets A and B, back to back on one vault:

- unsupported claims fall;
- right and cited, and over-caution, each move by at most one question — the step the evaluation
  README calls a delta;
- the median answer latency, 3.2 s today, rises by no more than one second.

Otherwise it is rejected by measurement and this record says so.

## Alternatives considered

| Option | Why not |
|---|---|
| Match the sentence's words to the label, with a pack glossary for synonyms | "You pay SGD 1,284.00 a year" is right and shares no word with `Annual Premium`. Every paraphrase has to be listed, and the list would be written from the questions it is scored on — tuning to the test set. |
| Have the router name the field the question asks for, and refuse when the document type does not declare it | One call per question, not per sentence, but the catalogue lists what extraction files, not what a page prints. Waiting periods, exclusions and benefit limits are printed and are not fields; refusing them would cost Set A's passage questions. |
| An NLI cross-encoder in-process, as the reranker is (ADR 0018) | Fast and deterministic, and possibly better. It is also a second model to ship, license and evaluate, and a runtime dependency with its own ADR. The generator is already loaded; if it proves too slow, this is the next thing to try. |
| Report these as a known limitation | They are the most convincing errors PARROT makes: a real page, a real number, a citation that checks out. "Every stage behaved as designed and the answer is invented" (ADR 0019) should not be the last word if a printed label can settle it. |

## Consequences

What this makes easy: the label lookup is code and the model only judges meaning, so a dropped
sentence can be explained by showing the label. No new dependency. Nothing changes until the
numbers say so, and the switch outlives a rejection for whoever re-tests.

What it makes hard:

- **Latency.** One more call per checked sentence, before that sentence is released, so each one
  streams later. Answered questions carry about 2.4 cited sentences; the cost is estimated at a few
  tenths of a second each and must be measured before acceptance.
- **A 4B judge errs both ways.** A wrong "no" drops a correct paraphrase. That is exactly what the
  right-and-cited and over-caution limits above are there to catch.
- **It reaches only values printed beside a label.** Of the four car claims it touches two.
  `b-b12` ("your insurance agent is from MERIDIAN ASSURANCE") quotes a letterhead, which has no
  label. `b-b04`'s sentences are true and simply answer a different question. Neither changes.
- It adds a gate check in `core/graph/`, which Christian co-owns, so it lands as its own PR with
  his review.

## Revisit when

The measurement is in, to accept or reject this record. Sooner if a pack can declare which printed
labels carry which field: the check then becomes a lookup and needs no model. Or if an NLI model is
admitted for another reason.
