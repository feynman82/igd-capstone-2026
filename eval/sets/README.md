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

A question may carry an optional `phrasing` field, `"casual"` or `"formal"` (default
`formal`). Mark a question `casual` when it is worded the way a person types it ("my car
insurance expire when ah?"); the headline's casual-phrasing gap compares "right and cited" on
the casual questions with the rest.

A question in `hard_negatives/` or `adversarial/` cites neither. There is nothing correct for
it to cite, and inventing a document for it to have abstained *about* would make the set
ungradeable in the one direction that matters.

Everyone writes 12 questions for their own area by the end of week 3. It is the one task
that otherwise bottlenecks on a single person, and it forces each lane to state what
"correct" means for the thing it built.

`answerable/<lane>-generated.jsonl` is a generated draft of that dozen, one file per lane, so
that nobody starts from an empty file — see "Generating a lane's dozen" in `eval/README.md`.
Keep it, edit it or replace it; the generator never overwrites a question written by hand.
Each register row belongs to exactly one lane, so two lanes never ask the same question:

| Lane | Documents |
|---|---|
| E · Desmond | every scanned and photographed document, whatever its type |
| A · Christian | identity cards, passports, birth certificates, loan agreements |
| B · Yew Mun | policy schedules |
| D · Zee | renewal notices, claim letters, benefit illustrations, anniversary statements |
| C · Siew | payslips, CPF, SRS, notices of assessment, donation receipts |

Identity documents exist only as photographs, and ADR 0017 gave them to the core, so they stay
with the lane that owns the household rather than with the lane that owns degraded scans.
