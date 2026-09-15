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

## 6b. Answering: words, categories, exclusions

This section is optional, and only the insurance pack uses it so far. It teaches the
core three things about how people actually talk, so the assistant does not need a
model to understand them. Nothing you write here is a field — none of it is stored,
and none of it appears in Desmond's spreadsheet.

**1. `vocabulary`** — the word a person says, mapped to the word the document prints.
Someone asks "was I warded?", not "was I an inpatient?". You write:

```yaml
vocabulary:
  warded: hospitalised as an inpatient
```

so the assistant reads the question in the household's own words and the document in
the insurer's.

**2. `categories`** — ordered rules that sort a policy by its printed product name,
never by the insurer's name. The first rule that matches wins, so put the more specific
kind first. Each rule has an `id`, a `label` that completes the sentence "None of the 5
policies on file is a …" — so `label: dental plan` reads as "… is a dental plan" — a
list of `printed` words to look for in the name, and a list of `asked` words a person
might use when asking about it.

**3. The traps that made this a section worth writing.** A Hospital *Income* Protection
Plan pays a fixed cash amount per day in hospital — it is not the same as a plan that
pays the hospital bill, so it gets its own category (`hospital_cash`), separate from
`hospital_expense`. A CareShield *Critical Illness* Plan and CareShield *Life* are two
different kinds of cover from the same brand name — the first is `critical_illness`,
the second `long_term_care`. And an insurer whose own name contains "Life Assurance" —
Lionhead Life Assurance, say — must not be filed as a life policy just because the word
"life" appears; categories match the product name, not the company letterhead.

**4. `exclusions`** — which headings on a document mark an exclusion clause, so a
sentence claiming cover under a heading like "What is not covered" is dropped rather
than quoted as if it were a benefit.

**5. `advice_decline`** — the one sentence the assistant gives when someone asks it to
recommend, compare or judge, rather than explain, in a pack that has no `advice` block
(§6c). Siew reviews this sentence, the same way she reviews the disclaimer.

**6. None of this is a field.** A category is decided fresh each time a question is
asked, from words a person reviewed — it is never written to a fact, never becomes a
register column, and renaming a category `id` costs nothing because nothing downstream
depends on the spelling of it.

---

## 6c. Advice: when a pack answers "is it enough?"

This section is optional too. Without an `advice` block, a pack explains and politely
declines to judge (§6b, point 5). With one, it can answer *"is my critical illness cover
enough?"* — but not the way a person would. **Code does the arithmetic. The model only
explains the result.** And the household's owner agrees once, in words you write, before
any advice is given. ADR 0016 has the reasoning.

**What an `advice` block holds**

| Key | What you write |
|---|---|
| `consent_version` | A version like `1.0.0`. Change it whenever you change `consent_text`, and every household is asked again. |
| `consent_text` | What the owner agrees to, in plain words. 40 to 1,500 characters. Siew reviews it. |
| `disclaimer` | Shown with every piece of advice. 40 to 1,200 characters. Siew reviews it. |
| `product_disclosure` | Shown whenever advice names a product. 40 to 800 characters. |
| `max_rule_age_days` | Optional, default 365. How old a rule value may be and still be used. |
| `max_price_age_days` | Optional, default 120. How old a market price may be and still be used. |
| `shapes` | One entry per kind of advice question — next table. |

**What a shape holds**

| Key | What it means |
|---|---|
| `id` | A short name, lowercase with underscores: `ci_gap`. |
| `calculator` | Which calculation runs. Pick one from the list below. |
| `label` | What the advice is about, in a few words: `critical illness cover gap`. |
| `asked` | Words a person uses when asking this question. They are how a question finds its shape. |
| `facts` | The printed facts the calculation reads — see below. |
| `rules` | The published rule values it reads: a `role`, a `key` from your `grounding.values`, and a `missing` sentence. |
| `compare_fields` | Comparisons only: the fields shown side by side. |
| `order_by`, `order` | Comparisons only: the one field the ranking follows (it must be in `compare_fields`), and `asc` for lowest first or `desc` for highest first. |
| `estimate` | `true` when the result is an estimate. It is labelled as one. |
| `disadvantages` | Known downsides, in your words. |
| `never_say` | Phrases the explanation must never contain. |

Each entry under `facts` points at something printed, the same way a field does:

- **`role`** — what the calculator uses it as, from the list below (`income`, `held`, …).
- **`doc_types`** and **`field`** — where it is printed. The field must be on every listed type.
- **`pack`** — leave it out for this pack's documents. Write another pack's id to read its
  documents instead: an insurance shape reads income from `iras_tax` payslips.
- **`category`** — one of your §6b category `id`s, to read only, say, critical illness plans.
- **`take`** — `latest` (the newest one), `sum` (add them all up) or `each` (keep them apart).
- **`per`** — `once`, `month` or `year`. A monthly figure is multiplied by 12 when a yearly
  one is needed.
- **`missing`** — what the assistant says when that fact is not on file. It names what is
  missing rather than guessing around it.

**The calculators — a closed list**

| `calculator` | The question it answers | Fact roles it needs | Rule roles it needs |
|---|---|---|---|
| `gap` | Is what I hold enough? | `income`, `held` | `multiple` |
| `remaining_room` | How much more can I put in this year? | `used` | `cap` |
| `keep_or_surrender` | Should I keep this plan? | `value_now`, `paid_to_date` | — |
| `compare_own` | Which of my own plans is better? | `items` | — |
| `compare_market` | Is my plan better than one on the market? | `held` | `market` |
| `estimate_saving` | How much would this save me? | `income`, `amount` | `rate` |

You cannot add a calculator in YAML. If a question needs one that is not here, tell
Christian: it is a code change, reviewed like one.

**You name rules. You never type numbers.** Under `grounding:` you list `values` — one
`key` per rule your sources publish, with a `unit` (`multiple`, `money`, `percent`, `rate`,
`years` or `count`), a `description`, and the `qualifiers` it depends on (`age_band`,
`ward_class`, `insurer`, `product`, `residency`, `assessment_year`, `band_lower`,
`band_upper`). The number itself is extracted automatically from the words of your
grounding sources (§7), and nothing uses it until Siew has approved it. A number typed
into `pack.yaml` would have no source to check it against and no date to go stale by, so
there is nowhere to type one.

**Example: a critical illness gap**

```yaml
grounding:
  corpus: null
  values:
    - key: ci_multiple
      unit: multiple
      description: Multiple of annual income a household is guided to hold as cover
      qualifiers: [age_band]

advice:
  # consent_version, consent_text, disclaimer and product_disclosure go here
  shapes:
    - id: ci_gap
      calculator: gap
      label: critical illness cover gap
      asked: [enough critical illness, critical illness gap]
      facts:
        - role: income
          pack: iras_tax
          doc_types: [payslip]
          field: gross_salary
          per: month
          missing: A recent payslip, to know your income.
        - role: held
          doc_types: [policy_schedule]
          field: sum_insured
          category: critical_illness
          take: sum
          missing: The schedule of each critical illness plan you hold.
      rules:
        - role: multiple
          key: ci_multiple
          missing: Reviewed guidance on how much cover to hold.
      never_say: [you must buy]
```

**The build checks your shapes.** `python -m packs.build` refuses a shape that is missing a
role its calculator needs, reads a document type or field the pack does not declare, names
a category or rule key that does not exist, compares without an `order_by`, or repeats an
`id`. The message names the shape. A shape reading another pack is checked when the packs
load, and fails if that pack is not installed.

---

## 7. Grounding — the optional second half

Some packs need more than the user's own documents. A tax pack, asked *"can I claim
this donation?"*, needs the actual IRAS relief rules, not a guess.

That is what a pack's `grounding/` folder is for: a small, curated set of official public
guidance, each source recorded with where it came from and when it was retrieved. It lives
**inside the pack**, at `packs/<pack_id>/grounding/<corpus_id>/`, so a pack someone
downloads carries its sources with it. See the two `sources.yaml` files already there, in
`packs/iras_tax/grounding/iras_reliefs_ya2026/` and
`packs/insurance_agent/grounding/mas_fair_dealing/`.

In your pack, you point at it by its id, never by a path:

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

Siew reviews each pack's `grounding/` folder with you, because provenance is a governance
artefact as much as a technical one.

### What a corpus holds

Authoritative reference material, indexed under a pack's namespace and kept separate from
the user's own documents. This is ISO/IEC 5338's **knowledge acquisition** process (6.4.7),
so it is a governance artefact as well as a build artefact.

```
packs/<pack_id>/grounding/<corpus_id>/
  sources.yaml        provenance for every file — required, no exceptions
  *.md                extracted text, one file per source document
  *.pdf               the original, only where the licence clearly allows it
```

### The rules for a corpus

1. **Every file has a `sources.yaml` entry.** Title, publisher, URL, the date it was
   retrieved, and a licence note. A passage the assistant cites has to be traceable to a
   real publication with a date, or the citation is worthless.
2. **Prefer extracted text over the original PDF.** Committing the text you actually index
   keeps the repository small, makes diffs readable, and avoids redistributing a third
   party's file. Keep the original only where the licence plainly allows it.
3. **Version by what the guidance applies to, not by when you downloaded it.** Tax relief
   rules change by Year of Assessment, so the corpus id carries it: `iras_reliefs_ya2026`.
   When YA2027 guidance appears it is a new corpus, not an edit to this one.
4. **Never paraphrase a rule into the corpus.** Index what the publisher wrote. If you find
   yourself summarising, you have moved from grounding into authorship, and the assistant
   will cite your summary as if it were the source.
5. **Do not publish the corpus with the report.** Cite the sources; link them. The corpus
   lives in a private repository.

### Owner

Zee assembles the corpora. Siew reviews `sources.yaml` and writes the paragraph in the
report explaining what third-party material the system indexes and on what basis.

---

## 8. Starter prompt for Claude Code

Open a terminal in this repository, run `claude`, and paste this in. Replace the two
bracketed parts.

The benchmark it points at is **`packs/insurance_agent/pack.yaml`**. Every rule below
carries the real defect it was written against, because an agent that knows *why*
`policy_type` was deleted behaves differently from one that only knows it was.

````markdown
I work in Lane D of this repository — domain packs and interface. I am not a
programmer. Explain things in plain language and ask me before doing anything I
have not asked for.

Read these completely, in this order, before you say anything:
1. `packs/README.md`
2. `packs/insurance_agent/pack.yaml`  ← the benchmark. Every later pack copies its shape.
3. `AGENTS.md`
Then invoke the `/authoring-a-domain-pack` skill and follow it.

I want to author a domain pack for **[DOMAIN, e.g. MOE teacher employment, or
tax advisers]**. The document types I have in mind are **[LIST]**. Challenge that
list — tell me if two of them are really one shape, or if one of them does not
belong in a household filing cabinet.

## Work in stages and STOP for my answer at each one

Do not run to the end. Stage 1 is a proposal with no files written.

1. **Propose.** A table per document type: field name, type, and one sentence on
   where on the paper the value appears. Write nothing.
2. **Write** `packs/<pack_id>/pack.yaml` once I have agreed the list.
3. **Draft** the persona and disclaimer for my approval, separately.
4. **Generate**: `python -m packs.build`.
5. **Check**: `python -m packs.build --check`, then `make check`, then show me
   `corpus/register/<pack_id>_columns.csv`.
6. **Propose** a commit. Do not commit until I say so.

## The four tests every field must pass

Apply these out loud, field by field. They are what the insurance pack was fixed
against, and each one caught a real defect there.

1. **Is it PRINTED?** Would Desmond fill this column by *reading* the document, or
   by *judging* it? If judging, delete it.
   *The insurance pack had `policy_type` as an enum of motor/home/life. No schedule
   anywhere prints the word "motor" — it prints "Private Car Insurance Policy". It
   was replaced with `product_name`, a printed string. Anything downstream that
   wants a category derives one; that is not the pack's job.*

2. **Does the NAME assert something the paper does not?** The column heading must
   mean the same thing to me as to the extractor.
   *`annual_premium` on a policy schedule was wrong: the paper prints "Total Premium
   Payable" for the period of insurance, which is only annual on a 1-year policy. It
   became `premium_payable`. It kept the name `annual_premium` on the documents where
   it genuinely is annual.*

3. **Is the MOST ACTIONABLE date on the document actually captured?** Not just the
   obvious one.
   *The renewal notice captured `expiry_date` but not `payment_due_date` — the
   "please pay by" date, which falls 7–14 days earlier and is the date the household
   must act on.*

4. **Is a document type earning its place?** A type whose fields mostly duplicate
   another type, or whose interesting numbers are *projections* rather than printed
   facts, is weak. Say so and propose a better one.

## Registers — do not accept the defaults

- **`reminder.lead_days`**: every window must map to a distinct thing the household
  *does*. Say what each one is for. If a window fires after the deadline it is
  warning about, it is wrong.
  *Insurance went 60/30/7 → 60/30/14/1: shop, read the notice, pay, cover ends
  tomorrow. The old 7-day window fired after the typical pay-by date, and there was
  no reminder on the day cover lapsed.*

- **`alert.metric`**: metrics are NOT fields. Open `modules/alert/queries.py` and
  `modules/alert/__init__.py`, read the actual SQL, and tell me in one plain sentence
  what it computes — then ask me whether that is what I meant. Do not assume.
  *`days_uncovered` groups by insured person only, so one live travel policy masks a
  motor policy that lapsed three months ago. The metric reports "0 days uncovered"
  for an uninsured car.*
  Any fix there is in `modules/` — Christian's lane, not mine. Raise it, don't edit it.

## Grounding — real or null, never in between

Official issuers only (IRAS, CPF Board, MAS, MOH, a named regulator), every source
recorded in `packs/<pack_id>/grounding/<corpus>/sources.yaml` with its retrieval date.

An empty corpus directory with `top_k: 6` is a lie the pack tells. If there are no
real sources yet, set `corpus: null, top_k: 0` and say so in a comment — section 7
of `packs/README.md` calls that a designed guardrail, not a gap.

Also check the corpus actually answers the question the pack gets asked. *The
insurance pack pointed at the MAS Fair Dealing Guidelines, which govern how insurers
must behave — they cannot answer "am I covered for flood damage".*

## Hard rules

- **`pack.yaml` is the only file I author.** `schemas.py`, `corpus/register/*_columns.csv`
  and `docs/field-dictionary.md` are generated by `python -m packs.build`. Never
  hand-edit one. If one looks wrong, the YAML is wrong.
- **Stay in `packs/` and `web/`.** If a rename breaks something in
  `corpus/` or `modules/`, stop and tell me — do not quietly fix it in someone
  else's lane. *(A rename in the insurance pack broke one token in
  `corpus/register/register.template.csv`. That needed Desmond's review.)*
- **`must_cite`, `abstain_below`, `never_acts` are not mine to change.** The persona
  and the disclaimer are. Siew reviews the disclaimer.
- **Renaming a field is free this week and expensive in week six** — it is a column
  heading in Desmond's spreadsheet. If you are unsure of a name, ask me. Never invent
  one I did not agree to.
- Bump `version:` when field names change.
- **Quote every `example:`** for a date, month, money or boolean — bare `2026-03-01`
  becomes a date object and fails validation.
- No new dependencies.

## Shape to aim for

3–5 document types, 4–8 fields each (the contract allows up to 12; going over 8
should be a decision, not an accident). Every description says *where on the paper*
the value appears. Every example realistically Singaporean.
````

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
