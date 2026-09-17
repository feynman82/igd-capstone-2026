# Authoring a domain pack

> **Since ADR 0017 (17 September 2026) document types and fields are the core's.** They are
> written in `core/documents.yaml`, which generates `core/document_schemas.py`,
> `corpus/register/core_columns.csv`, the batch template and `docs/field-dictionary.md`. A pack
> (`packs/<id>/pack.yaml`) now holds only grounding, persona, guardrails, its own answering rules
> and advice. Where this guide says a field goes in `pack.yaml`, it goes in `core/documents.yaml`.

**For Zee.** Everything a pack needs is one YAML file. You never write Python, and you never
edit a generated file. Run one command and the platform stays consistent with you.

---

## 1. What a pack is

The core platform knows nothing about tax or insurance. It knows how to ingest a document,
search it, and answer a question with a citation. A **domain pack** is what teaches it a
subject. It declares five things:

| It declares | Which the platform uses to |
|---|---|
| **document types** and their fields | route a document at ingest, and constrain extraction so a date lands in a date column |
| a **grounding corpus** | index authoritative reference material alongside the user's own documents |
| which **capability modules** it registers with | fire reminders and alerts without the module knowing anything about your domain |
| a **persona** | set the voice of the answer, and nothing else |
| **guardrails** | require citations, set the floor below which the system refuses to answer, and forbid it from acting |

Two packs ship for the capstone: **Tax and Reliefs** and **Insurance and Coverage**. Nine
more are specified against this same file format, which is how we demonstrate that the
platform extends without anyone touching the core.

---

## 2. The one thing to understand before you start

A field name you write in `pack.yaml` becomes **three things at once**:

1. the attribute on the extraction model the AI is constrained to fill,
2. the `facts.key` the value is stored under in the database,
3. **the column header in Desmond's corpus register.**

That third one is why this matters. Desmond fills in a spreadsheet of what is in each
document, and Yew Mun scores the extractor against it. If your field is `pay_period` and his
column says `period`, nothing errors — the evaluation just silently scores zero on that
field, and we find out in week 8.

So the column headers are **generated from your file**. You define the names, Desmond's
spreadsheet inherits them, and they cannot drift. This means:

> **Your field lists need to be settled before Desmond fills in any register rows.**
> That is a week 1 dependency, not a week 3 one.

---

## 3. The workflow

```bash
# 1. edit the pack
code packs/iras_tax/pack.yaml

# 2. regenerate everything downstream
python -m packs.build

# 3. check it, commit both the source and the generated files
python -m pytest -q
git add packs/ corpus/register/ docs/field-dictionary.md
git commit -m "iras_tax: add srs_statement document type"
```

`python -m packs.build` writes three things and you commit all of them:

| Generated | Who consumes it |
|---|---|
| `core/document_schemas.py` | the ingestion worker, as a decode constraint on the AI |
| `corpus/register/core_columns.csv` and the batch template | Desmond, as the header row of his spreadsheet |
| `docs/field-dictionary.md` | everyone, as the human-readable list of every field |

CI fails if you edit a pack and forget to regenerate. That is deliberate.

---

## 4. Writing `pack.yaml`

Start from `packs/_template/pack.yaml`. The two real packs are the worked examples.

### Document types

One entry per kind of document, named in `snake_case`. Keep it to what a household actually
receives — a policy schedule and a renewal notice are two types because they look different
and carry different fields, but "annual policy schedule" and "mid-term policy schedule" are
one type.

```yaml
document_types:
  policy_schedule:
    description: Policy schedule or certificate of insurance setting out cover and premium
    subject_field: insured        # which field says whose document this is
    fields:
      - name: policy_no
        type: identifier
        description: Policy number exactly as printed, not normalised
        example: MV-2026-448120
```

### Field types

Ten types. Pick by what the value *is*, not by how it is printed.

| Type | Use for | Stored in | Format in the register |
|---|---|---|---|
| `string` | names of companies, free text | `value_text` | as printed |
| `identifier` | policy, claim and receipt numbers | `value_text` | **exactly as printed** — no spaces removed, no case changed |
| `person` | who the document is about | `value_text` + `subject` | full name as printed |
| `money` | any SGD amount | `value_num` | `742.00` — no `$`, no commas, two decimals |
| `integer` | counts, years, mileage | `value_num` | `2026` |
| `percent` | a rate or discount, 0–100 | `value_num` | `20` not `0.2` |
| `date` | a specific day | `value_date` | `2027-02-28` |
| `month` | a pay period | `value_text` | `2026-01` |
| `enum` | a fixed set of options | `value_text` | one of your `values` list |
| `boolean` | a yes/no on the face of the document | `value_text` | `true` / `false` |

`identifier` versus `string` is the distinction that matters most. An identifier is matched
exactly and never cleaned up, because `MV-2026-448120` and `mv2026448120` are different
policies as far as a claim is concerned.

### How many fields

**Five to eight per document type. Twelve is the hard limit.**

A field earns its place by being used: a module needs it, or a user would plausibly ask
about it. Every extra field is a field Desmond has to fill in for hundreds of documents and
a field the extractor can get wrong, so breadth costs accuracy twice.

Mark a field `required: false` when a real document sometimes omits it. A required field
that is missing sends the whole document to quarantine, which is right for a policy number
and wrong for an optional excess.

### Descriptions are prompts

The `description` is shown to the extraction model. Write it as an instruction to someone
looking at the document for the first time:

- Good: `Last day of the period of insurance`
- Bad: `The expiry date`

The `example` is shown too, and it is what Desmond copies the format from. Get it right.

### Registering with capability modules

This is how a pack gets reminders and alerts without writing any logic.

```yaml
registers:
  reminder:
    - key: policy_expiry
      from_field: expiry_date     # a date field you declared above
      lead_days: [60, 30, 7]      # warn at 60, 30 and 7 days out
  alert:
    - metric: srs_contributions_ytd
      ceiling: 15300
      warn_at: 0.9                # fire at 90% of the ceiling
```

`from_field` must name a `date` field on one of your document types. If you register a
module that is not installed, it is ignored rather than an error, so it is safe to declare
`tracker` now even though we are not building it.

### Persona

Voice only. It cannot change retrieval, the score floor or the guardrails, so do not try to
smuggle behaviour into it. Two or three sentences saying what this assistant does and,
importantly, what it does not do:

```yaml
persona:
  system: >
    You explain what the user's own insurance documents say: what is covered, what is
    excluded, what it costs and when it ends. You compare only against the documents in
    front of you and the published guidance in your corpus, never against products you
    recall but cannot cite.
```

### Guardrails

```yaml
guardrails:
  must_cite: true          # no claim without a document and page
  abstain_below: 0.45      # below this retrieval score, the system says it does not know
  never_acts: true         # cannot be set to false — the type system rejects it
  disclaimer: >            # rendered under every answer from this pack
    Informational analysis of your own policy documents. This does not constitute advice
    under the Financial Advisers Act. Confirm cover with your insurer or a licensed adviser.
```

Raise `abstain_below` for a domain where being wrong is expensive. Insurance sits at 0.45
and tax at 0.42 for that reason — a wrong answer about cover is worse than an unhelpful one.

The disclaimer is where regulatory framing belongs, not the persona. Siew reviews both
disclaimers before they ship.

---

## 5. The grounding corpus

Authoritative reference material indexed alongside the user's own documents, so the
assistant can say what the published rule is and cite it.

```
packs/iras_tax/grounding/iras_reliefs_ya2026/
  sources.yaml        provenance for every file — required, no exceptions
  individual-reliefs.md
```

Five rules, in `packs/README.md` §7. The two that catch people out:

- **Never paraphrase a rule into the corpus.** Index what the publisher wrote. The moment
  you summarise, the assistant starts citing your summary as though it were IRAS.
- **Version by what the guidance applies to.** `iras_reliefs_ya2026`, not
  `iras_reliefs_september`. When YA2027 guidance appears it is a new corpus, not an edit.

Every file needs a `sources.yaml` entry: title, publisher, URL, retrieval date, licence
note. Siew reviews it and writes the report paragraph explaining what third-party material
we index and on what basis.

A pack with no corpus is fine and sometimes correct — several of the roadmap packs answer
only from the user's own documents, which is a designed guardrail rather than a gap.

---

## 6. Definition of done

A pack is finished when all of these are true.

- [ ] `python -m packs.build` runs clean and the generated files are committed
- [ ] `python -m pytest -q` passes
- [ ] Every document type has 5–8 fields and every field is used by a module or answers a
      plausible question
- [ ] Every `description` reads as an instruction to someone seeing the document for the
      first time, and every `example` is correctly formatted
- [ ] The grounding corpus has a complete `sources.yaml`, reviewed by Siew
- [ ] The disclaimer has been read by Siew
- [ ] Desmond has the generated `corpus/register/core_columns.csv` and has confirmed he can
      fill it in
- [ ] Three real documents from the corpus extract correctly end to end

---

## 7. Where to ask

- The field format, or whether a value is an `identifier` or a `string` → **Christian**
- Whether a field is worth extracting at all → **Yew Mun**, who scores it
- Disclaimers, the grounding corpus and anything regulatory → **Siew**
- What a document type actually looks like in the wild → **Desmond**

If a decision feels bigger than a pack — a new field type, a change to how registration
works — open an issue with the *Decision needed* template rather than working around it.
That file is the contract five people build against.
