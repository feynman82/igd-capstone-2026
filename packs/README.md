# Domain packs — start here

**Owner: Zee.** This is your folder. Nobody else edits it.

You do not need to know how to program to do this work. You need to know what a
document *is* and what is written on it. That is the actual scarce skill here, and it
is why this lane is yours.

---

## 1. What we are building, in one paragraph

We are building an assistant that answers questions about the documents in a
household's own filing cabinet. Someone photographs an insurance renewal notice with
their phone, and later asks *"when does my car insurance expire and what am I paying?"*
The assistant answers from that photograph — not from the internet, not from memory —
and shows which document and which page the answer came from.

For that to work, the system has to know **what kinds of documents exist** and **what
is printed on each kind**. That knowledge is what a *domain pack* holds. A pack for tax
knows what a payslip is. A pack for insurance knows what a policy schedule is.

Writing those packs is your job.

---

## 2. What a domain pack actually is

One folder. One file in it. That file is called `pack.yaml`.

Two are already written, as worked examples:

- `packs/iras_tax/pack.yaml` — Tax and Reliefs
- `packs/insurance_agent/pack.yaml` — Insurance and Coverage

Open `packs/iras_tax/pack.yaml` and read it before anything else. It will look more
approachable than you expect. It is a list of document types, and under each one, a
list of the things printed on that document.

Here is the shape, with everything unnecessary stripped away:

```yaml
document_types:

  payslip:
    description: Monthly salary advice issued by an employer
    subject_field: employee          # which field tells us whose payslip this is
    fields:
      - name: employee
        type: person
        description: Name of the employee as printed on the payslip
        example: Marcus Fernandez

      - name: gross_salary
        type: money
        description: Total pay before any deduction, in SGD
        example: "8900.00"
```

That is the whole idea. A document type, and under it the fields you would point at
with a finger if the paper were in front of you.

### The field types you can use

| Type | Use it for | What you write in `example:` |
|---|---|---|
| `person` | Somebody's name | `Marcus Fernandez` |
| `string` | A company or organisation name | `Harborline Logistics Pte Ltd` |
| `identifier` | A reference number, copied **exactly** as printed | `POL-8823-114` |
| `money` | An amount in SGD | `"8900.00"` |
| `integer` | A whole number | `2026` |
| `percent` | A percentage | `"4.5"` |
| `date` | A specific day | `"2026-03-01"` |
| `month` | A month, no day | `"2026-01"` |
| `enum` | A fixed short list of options — you also list them under `values:` | `Motor` |
| `boolean` | A yes/no on the document | `"true"` |

`identifier` matters more than it looks. A policy number is *not* a string to be tidied
up — it is copied character for character, because if the system reformats it, it stops
matching the number the user typed into the search box.

### The rules for a field

- **Between 1 and 12 fields per document type.** If you need more than twelve, it is
  probably two document types.
- **`description` must be at least 8 characters** and should say where on the document
  the thing appears. "Policy number exactly as printed, not normalised" is a good
  description. "The policy number" is a weak one.
- **`required: false`** on anything that is genuinely sometimes absent. Everything else
  is required by default. Do not mark something optional because you are unsure —
  ask instead.
- **Field names are lowercase with underscores**: `annual_premium`, not
  `Annual Premium` or `annualPremium`.

---

## 3. The one thing that matters most

**A field name you write here becomes a column heading in Desmond's spreadsheet.**

Not "similar to". The same word, character for character, generated automatically from
your file.

Here is why that matters. Desmond's lane produces the synthetic documents we test
against, and a spreadsheet recording what is truly written on each one — the answer key.
The system's extraction is scored against that answer key. If you call a field
`pay_period` and Desmond's spreadsheet says `period`, the comparison silently finds
nothing, scores zero, and everyone spends three days hunting a bug that is really a
spelling difference.

So we removed the possibility. Your `pack.yaml` **generates** the column headings.
Desmond does not choose them and cannot get them wrong. You choose them once, and they
propagate.

That is also why you should not rename a field casually after Desmond has started. A
rename is fine early and expensive late. If you want to rename something in week 6,
say so in the group first.

---

## 4. What you do, step by step

**Step 1 — Choose the domain.** The two already written are Tax and Insurance. The next
one might be Household Utilities, or Schooling, or Healthcare Bills. Christian will tell
you which, or you can propose one.

**Step 2 — Collect the real thing.** Find three or four actual examples of each
document type, from anywhere — your own drawer, a public sample, a redacted version a
friend will share. You are not putting these in the repository. You are looking at them
so the field list matches reality rather than what you imagine reality to be.

**Step 3 — List the document types.** Aim for 3 to 5 per pack. A document type is a
*shape*, not an issuer: every insurer's renewal notice is one type, not one type per
insurer.

**Step 4 — Fill in the fields.** Copy `packs/_template/pack.yaml` into a new folder
named after your pack id, and work through it.

**Step 5 — Write the persona and the disclaimer.** At the bottom of the file. Two short
paragraphs — see section 6 below.

**Step 6 — Run one command.** In a terminal, in this repository:

```
python -m packs.build
```

That regenerates three files from yours. If you made a mistake, it prints what is wrong
and changes nothing. If it prints nothing, it worked.

**Step 7 — Commit both.** Your `pack.yaml` **and** the generated files, in the same
commit. The build server checks they match, and a commit with only one of them fails.

Claude Code will do steps 6 and 7 for you. Section 8 has the prompt.

---

## 5. How your output lets Desmond continue

This is the part worth understanding, because it explains why your lane blocks his.

```
   YOU                          THE BUILD STEP                    DESMOND
   ───                          ──────────────                    ───────

   packs/insurance_agent/       python -m packs.build             corpus/register/
   pack.yaml                                                      insurance_agent_columns.csv
        │                                                                │
        │  you write this by hand          generates                     │  he fills this in
        │                          ────────────────────────►             │
        │                                                                ▼
        │                                                        writes 40 synthetic
        │                                                        documents that match
        │                                                        the spreadsheet exactly
        │
        └──────────────────► packs/insurance_agent/schemas.py ──► the extractor reads
                                                                  a document and must
                             docs/field-dictionary.md             produce these fields
```

Concretely, the moment you commit a pack, three things exist that did not exist before:

1. **`corpus/register/<your_pack>_columns.csv`** — an empty spreadsheet with your field
   names as the column headings. This is Desmond's brief. He does not have to ask what
   to record; the columns tell him.

2. **`packs/<your_pack>/schemas.py`** — the machine-readable version of your field list.
   The extraction step is *constrained* by this: the model is not allowed to return
   anything else. Your file is what makes the extraction reliable.

3. **`docs/field-dictionary.md`** — a readable table of every field in the whole system,
   which is what the rest of the team reads instead of asking you.

Desmond's method, once he has your columns, is *register first*: he fills in the
spreadsheet — inventing forty plausible households, policy numbers, dates and amounts —
and only then writes the documents to match. That way the answer key exists before the
documents do, so it cannot drift from them.

**So the sequence is: you commit the pack → he fills the register → he generates the
documents → Yew Mun can measure the system.** Nothing downstream can start until the
column names are fixed. That is why this lane runs first, and why it is worth spending
an afternoon on the field list rather than an hour.

---

## 6. Persona and guardrails

At the bottom of `pack.yaml`:

```yaml
persona:
  system: >
    You explain what the user's own documents say about their insurance cover.
    You never compare products, recommend a policy, or state a rule you cannot cite.

guardrails:
  must_cite: true
  abstain_below: 0.42
  never_acts: true
  disclaimer: >
    This assistant reads your own documents. It is not licensed financial advice
    and does not recommend or compare insurance products.
```

Three of those four are fixed and you should not change them.

- **`must_cite`** — every factual sentence must point at a document. Non-negotiable.
- **`abstain_below`** — how sure the system must be before it answers rather than saying
  it does not know. Leave it alone unless Yew Mun's evaluation says otherwise.
- **`never_acts`** — the assistant advises; it never pays a bill, books an appointment
  or files a return. This one is enforced by the code itself: a pack that sets it to
  anything else will not load. It is the boundary our governance chapter is built on,
  so it is worth knowing it is there.

The **disclaimer** is yours to write, and it should be specific to the domain. Between
20 and 800 characters. A tax pack disclaims tax advice; an insurance pack disclaims
product recommendation. Siew reviews these, because they are what the report points at
when it argues the system stays inside its lane.

The **persona** is also yours. Two sentences. Say what the assistant explains, and say
what it refuses to do. Resist writing a personality — "friendly and approachable" adds
nothing. "Never states a rule it cannot cite" adds a great deal.

---

## 7. Grounding — the optional second half

Some packs need more than the user's own documents. A tax pack, asked *"can I claim
this donation?"*, needs the actual IRAS relief rules, not a guess.

That is what `grounding/` is for: a small, curated set of official public guidance,
each source recorded with where it came from and when it was retrieved. See
`grounding/README.md` and the two `sources.yaml` files already there.

In your pack, you point at it:

```yaml
grounding:
  corpus: iras_reliefs_ya2026     # or: null, to answer only from the user's documents
  top_k: 6
```

Rules for grounding sources:

- **Official issuers only.** IRAS, CPF Board, MAS, MOH, a named regulator. Not a blog,
  not a comparison site, not a forum answer, however good it looks.
- **Record the retrieval date.** Rules change by assessment year, and the report has to
  say which year the system was grounded in.
- **Keep it small.** Twenty well-chosen pages beat two hundred scraped ones. Every
  irrelevant page is a chance for the retriever to surface it instead of the right one.

Siew reviews `grounding/` with you, because provenance is a governance artefact as much
as a technical one.

---

## 8. Starter prompt for Claude Code

Open a terminal in this repository, run `claude`, and paste this in. Replace the two
bracketed parts.

> I am working on the domain packs lane of this repository. I am not a programmer, so
> explain what you are doing in plain language and ask me before doing anything I have
> not asked for.
>
> First, read these three files completely, in this order:
> `packs/README.md`, `packs/iras_tax/pack.yaml`, `docs/PACK_AUTHORING.md`.
> Then read `AGENTS.md` for the repository's working rules.
>
> I want to author a new domain pack for **[DOMAIN, e.g. household utilities and
> telecoms]**. The document types I have in mind are **[LIST, e.g. an electricity bill,
> a water bill, a mobile phone bill, a broadband contract]** — challenge that list if
> you think it is wrong, and tell me if two of them are really the same shape.
>
> Work like this, and stop for my answer at each numbered step rather than running to
> the end:
>
> 1. Propose the document types and, for each, the fields you think are printed on it.
>    Show me the field name, the type, and one sentence on where it appears on the
>    document. Do not write any file yet.
> 2. When I have agreed the list, create `packs/<pack_id>/pack.yaml` by copying the
>    structure of `packs/iras_tax/pack.yaml`. Every field needs a `description` of at
>    least eight characters and a realistic Singaporean `example`.
> 3. Draft the `persona` and the `disclaimer` for me to approve. Leave `must_cite`,
>    `abstain_below` and `never_acts` exactly as they are in the existing packs.
> 4. Run `python -m packs.build` and show me what it generated. If it errors, explain
>    the error in plain language and fix the YAML — never edit a generated file.
> 5. Run `python -m packs.build --check` to confirm everything is in sync, then show me
>    the new columns in `corpus/register/<pack_id>_columns.csv`, because that spreadsheet
>    is the brief for a teammate and I want to check it reads sensibly to a person.
> 6. Stage `pack.yaml` and every generated file together and propose a commit message.
>    Do not commit until I say so.
>
> Rules you must follow: `pack.yaml` is the only file I author — everything else in
> `packs/` is generated. Never hand-edit `schemas.py`, the register CSV or
> `docs/field-dictionary.md`. Do not touch anything outside `packs/` and `grounding/`.
> Do not add dependencies. If you are unsure about a field name, ask me rather than
> guessing, because a field name here becomes a column heading in someone else's
> spreadsheet and renaming it later is expensive.

### If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ValidationError` mentioning a field name | Something in the YAML is not the shape the contract expects | Read the message — it names the field. Usually a missing `description` or a type that is not in the table above. |
| `--check` fails in CI | You committed `pack.yaml` without the regenerated files | Run `python -m packs.build`, commit the changed files too |
| A date is being read as a date, not text | YAML turns bare `2026-03-01` into a date object | Put quotes around it: `"2026-03-01"`. All `example:` values for dates, months, money and booleans are quoted. |
| You are unsure whether two things are one document type | They are one type if a person would use the same word for both | Ask in the group rather than guessing |

---

## 9. What "done" looks like for a pack

- [ ] 3 to 5 document types, each with 4 to 8 fields
- [ ] Every field has a description that says where the value appears on the paper
- [ ] Every field has a realistic Singaporean example, quoted where it is a date or amount
- [ ] `python -m packs.build --check` passes
- [ ] The generated register CSV reads sensibly to somebody who has not seen the YAML
- [ ] Persona and disclaimer written, and Siew has read the disclaimer
- [ ] `pack.yaml` and the generated files committed together
- [ ] You have told Desmond the columns are ready

---

**Full technical detail, if you want it:** `docs/PACK_AUTHORING.md`.
**Who owns what:** `docs/TEAM.md`.
**Questions:** ask Christian. A question costs five minutes; a wrong field name costs
three days in week eight.
