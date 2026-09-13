# Notebook prompt — a full-length insurance policy for Marcus Lim

One prompt, one notebook, one policy. It produces a document of the length a real Singapore
policy runs to — schedule, definitions, benefits, exclusions, claims, conditions, endorsements
— rather than the one-page summaries the earlier prompts produced.

**It is written to be ingestible**, which is a harder constraint than it looks and is the reason
this file exists rather than just "make it longer". Everything in the PAGE ONE section below was
derived from watching batch 1 fail:

| What failed | Why | What this prompt does |
|---|---|---|
| `b1-0002` — "no installed pack recognises this document" | Docling parsed the letterhead, signature and footer and **dropped the schedule table entirely** | Page one is plain `Label: value` lines, not a bordered table |
| `b1-0033` — `policy_no` extracted as `b1-0033` | The model took `Ref: b1-0033` from the page footer | No `Ref:` line; the filing reference is not on the page |
| `b1-0033` — `insured` extracted as `LIONHEAD LIFE ASSURANCE` | Letterhead and insured were both prominent company-shaped strings | `Name of Insured` is labelled, and the insurer name appears once |
| `b1-0033` — `cover_from` invented as `0120-01-20` | Dates were buried in prose and parentheticals | Each date is alone on its own labelled line |
| `b1-0031` — `premium_payable` read as `01-JUN` then `0120-06-20` | The amount shared a cell with "Payable annually on 01 June" | One value per line, always |
| `b1-0003`, `b1-0033` | `{{cover_from}} to {{expiry_date}}` in one cell | Period is two lines, From and To |

---

## Before you generate: the register row

Register first — `corpus/README.md`. Add the row to `corpus/register/batch1.csv`, run
`uv run python -m corpus.validate corpus/register/batch1.csv`, and only then open the notebook.
Every value in the prompt below is copied from that row; nothing is invented at generation time.

`doc_type` is **`policy_schedule`** whatever the product is. No pack declares "policy wording",
and a `doc_type` no pack owns goes to quarantine and contributes nothing to `facts`. The
schedule is page one and the wording is the pages behind it.

---

## The prompt

Substitute every bracket. Keep the PAGE ONE block exactly as laid out — its shape is the part
that makes the document ingestible.

```
You are a Singapore insurance product drafter. Write a COMPLETE, FULL-LENGTH policy
contract for a FICTIONAL insurer — the document a policyholder actually receives, not a
summary of one. This is synthetic material for a university project's test corpus.

LENGTH: This must be a substantial document. Write every section in full, with numbered
clauses and sub-clauses, in the register a real policy contract uses. Do not abbreviate,
do not summarise, do not write "etc." and do not leave a section as a heading with one
line under it. If a real policy would spend six clauses on a topic, spend six clauses.
Aim for the length of a genuine policy wording booklet.

INSURER (fictional):     [Meridian Assurance / Lionhead Life Assurance / invent one]
PRODUCT NAME:            [e.g. PrivateCare Hospital and Surgical Plan]
POLICY NUMBER:           [e.g. PH-2022-604188]
INSURED:                 Marcus Lim Jun Wei
DATE OF BIRTH:           8 May 1987
ADDRESS:                 Blk 45B Tampines Ave 8 #07-21 Singapore 521045
COVER FROM:              [e.g. 1 March 2026]
COVER TO:                [e.g. 28 February 2027]
SUM INSURED:             [e.g. SGD 1,000,000.00]
ANNUAL PREMIUM:          [e.g. SGD 1,860.00]
PAYMENT DUE DATE:        [e.g. 20 February 2026]
DATE OF ISSUE:           [e.g. 10 February 2026]

=== PAGE ONE — REPRODUCE THIS SHAPE EXACTLY ===

Page one carries the insurer name as a heading, then the words POLICY SCHEDULE, then the
fields below as PLAIN LINES of "Label: value". Nothing else goes on page one.

Do NOT use a bordered table, a grid, a multi-column layout, or a box on page one. Plain
labelled lines, one per line. A table here is frequently lost in parsing and the whole
document becomes unreadable to the system.

    [INSURER NAME]

    POLICY SCHEDULE

    Policy Number: [policy number]
    Name of Insured: Marcus Lim Jun Wei
    Date of Birth of Insured: 8 May 1987
    Address of Insured: Blk 45B Tampines Ave 8 #07-21 Singapore 521045
    Product Name: [product name]
    Period of Insurance From: [cover from, as DD Month YYYY]
    Period of Insurance To: [cover to, as DD Month YYYY]
    Sum Insured: SGD [amount]
    Excess: SGD [amount]            <- omit this line entirely if there is none
    Annual Premium: SGD [amount]
    Payment Due Date: [date, as DD Month YYYY]
    Date of Issue: [date, as DD Month YYYY]

Rules for page one, all of which matter:
  - ONE value per line. Never put two things on one line. "Annual Premium: SGD 1,860.00"
    and nothing else — not "SGD 1,860.00 (payable annually on 1 March)".
  - Never merge the period into one line. Two lines, From and To.
  - Write every date as DD Month YYYY: 1 March 2026. Never a range, never a
    parenthetical, never a relative date.
  - Write every amount with the SGD prefix and two decimals: SGD 1,860.00.
  - The insurer name appears as the heading. "Name of Insured" is the person. Never put a
    company name against Name of Insured.
  - Do NOT print a document reference, a form number, a "Ref:" line, or a filename
    anywhere in the document. They get mistaken for the policy number.
  - If a value is not applicable, omit the whole line. Never write "null", "N/A" or "-".

=== THE REST OF THE DOCUMENT ===

From page two onward, write the policy in full. Use numbered clauses throughout (1, 1.1,
1.1.1). Tables are fine from page two onward — only page one must avoid them.

  1.  Preamble and the contract of insurance — what forms the contract, the basis of the
      contract, and the effect of the proposal and declaration.
  2.  Definitions — at least 25 defined terms, each a full paragraph, alphabetical.
  3.  Scope of cover — what the policy insures, stated as principles before amounts.
  4.  The benefit table — every benefit with its own limit, sub-limit and any inner limit,
      and a paragraph under each explaining what it does and does not reach.
  5.  Limits, deductibles, co-insurance and how they interact, with two worked examples
      carried through arithmetic to a final payable figure.
  6.  Waiting periods, pre-existing conditions, and survival or qualifying periods.
  7.  Exclusions — numbered, at least 20, each with a sentence of scope.
  8.  Claims — notification deadlines, the documents required, assessment, payment, appeal,
      and what happens to a late claim.
  9.  Premiums — how calculated, when payable, the grace period, lapse, reinstatement, and
      the effect of non-payment on a claim in progress.
  10. Policy changes — endorsements, alterations, and changes in the risk the insured must
      disclose.
  11. Renewal, cancellation, free-look and refunds, with the pro-rata and short-rate basis
      set out.
  12. General conditions — governing law, dispute resolution, arbitration, subrogation,
      fraud, misstatement of age, assignment, nomination, notices, and the contracts
      (rights of third parties) position.
  13. Endorsements attaching to and forming part of this policy — at least three, each
      with its own number, effective date and wording.

RULES throughout:
  - Every organisation you name is invented. Never name a real insurer, hospital, clinic,
    bank, government agency, court, or professional body. Where the wording needs an
    authority, describe it as a class: "a registered medical practitioner holding a
    specialist qualification in the relevant discipline".
  - Singapore conventions: SGD, DD Month YYYY, and CPF or MediSave only as generic
    concepts where a real policy would mention them.
  - Every figure must be identical everywhere it appears. If the sum insured is
    SGD 1,000,000.00 on page one it is SGD 1,000,000.00 in clause 4.
  - No commentary, no preamble, no "here is your document", no notes to the reader.
    Write the policy itself, starting with the insurer name.
```

---

## Optional block — the appendicitis demonstration

Add this only to a hospital and surgical plan. It is what
*"can I claim under insurance if I have an appendicitis operation at a private hospital?"*
is answered from.

```
This plan must also contain, in the benefit section:

  - A WARD AND HOSPITAL ENTITLEMENT clause stating that the plan covers treatment at ANY
    PRIVATE HOSPITAL IN SINGAPORE, and at what proportion of eligible charges. State it
    as a CLASS of hospital. Do NOT list hospitals by name and do NOT invent a named
    panel — the plan is deliberately open to any private hospital, and a named list would
    make the answer a name match instead of a reading of the entitlement. Also state the
    entitlement for a public hospital and for treatment outside Singapore.

  - A SURGICAL BENEFIT schedule classifying operations into Table 1 to Table 7 with a
    payable amount for each table, listing APPENDICECTOMY explicitly against its table,
    and several other named operations against each of the other tables. Follow it with a
    clause on what happens when two procedures are performed in one operation.

  - A clause on PRE-AUTHORISATION: when it is required, how far in advance, and the effect
    on a claim if it was not obtained. Then a clause on treatment taken at a hospital
    outside the entitlement — a reduced proportion, not an outright refusal.

  - A clause confirming that an acute condition such as appendicitis is covered once the
    general waiting period has passed.
```

Raffles Hospital is a real institution, so the name belongs **in the question only, never in
the document**. Parrot answers by reading the entitlement clause together with the surgical
table — two citations, two clauses, one answer — which is the harder and more honest retrieval.

---

## After generating

1. Print to PDF and name it by its `doc_id`: `b1-0034.pdf`.
2. Check page one parses. This is the step that is worth the two minutes:

```bash
pdftotext -layout corpus/batches/batch1/b1-0034.pdf - | head -20
```

   You should see every `Label: value` line. If the schedule is missing or mangled, the
   document will quarantine as "no installed pack recognises this document" — regenerate page
   one as plain lines rather than debugging it.

3. Confirm every register value appears, and that `field_pages` is right — for this shape every
   extracted value is on page 1, so the column stays empty, but check rather than assume.
4. Validate and ingest:

```bash
uv run python -m corpus.validate corpus/register/batch1.csv
```

## What this prompt cannot fix

The generator is `Qwen-SEA-LION-v4-4B-VL`, and on a dense document it misreads. On `b1-0033` it
reported the insurer as the insured, took a footer reference as the policy number, and invented
both dates. The page-one shape above removes the ambiguities it trips on, and
`core/ingest/extract.py` now names those mistakes in its prompt — but a 4B model reading a
thirty-page contract is the real ceiling here, and a document that ingests cleanly is partly a
document that made the model's job easy. If extraction stays unreliable at this length, the
question is the extraction model rather than the corpus, and that is an ADR.
