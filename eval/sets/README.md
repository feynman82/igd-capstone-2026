# `eval/sets/` — the golden sets

**Owner: Yew Mun.** Set C is Siew's.

| Set | Size | Scored on |
|---|---|---|
| `answerable/` | 60 | Finds the right evidence and answers from it |
| `hard_negatives/` | 25 | **Abstains** — the corpus genuinely cannot answer |
| `adversarial/` | 15 | Refuses, and the refusal is correctly reasoned |

Every answerable question cites the document and page its answer comes from, taken from
`corpus/register/`: `must_cite_doc` is the row's `doc_id`, and `must_cite_page` comes from
that row's `field_pages` column — which names the page each value is printed on, and means
page 1 for any field it does not name. That is what makes the set gradeable without a human
in the loop.

A question in `hard_negatives/` or `adversarial/` cites neither. There is nothing correct for
it to cite, and inventing a document for it to have abstained *about* would make the set
ungradeable in the one direction that matters.

Everyone writes 12 questions for their own area by the end of week 3. It is the one task
that otherwise bottlenecks on a single person, and it forces each lane to state what
"correct" means for the thing it built.
