# `eval/sets/` — the golden sets

**Owner: Yew Mun.** Set C is Siew's.

| Set | Size | Scored on |
|---|---|---|
| `answerable/` | 60 | Finds the right evidence and answers from it |
| `hard_negatives/` | 25 | **Abstains** — the corpus genuinely cannot answer |
| `adversarial/` | 15 | Refuses, and the refusal is correctly reasoned |

Every question cites the document and page its answer comes from, taken from
`corpus/register/`. That is what makes the set gradeable without a human in the loop.

Everyone writes 12 questions for their own area by the end of week 3. It is the one task
that otherwise bottlenecks on a single person, and it forces each lane to state what
"correct" means for the thing it built.
