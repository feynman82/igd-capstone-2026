# Notebook prompts — the four full policies for Marcus Lim

> **Superseded for new work** by
> [`notebook-prompt-full-length-policy.md`](notebook-prompt-full-length-policy.md), which
> produces a full-length policy and a page one that survives parsing. Kept because the four
> documents in `corpus/batches/batch1/` were generated from it.

**One notebook per policy, one at a time.** A single prompt asking for four policies produces
four thin documents.

Every figure below is taken from `corpus/register/batch1.csv` and `corpus/canon.md`. Do not
round them, do not "improve" them, and do not let the notebook invent a figure the register
does not carry — the register is the ground truth the evaluation is scored against.

| Prompt | Register row | Output file | Status |
|---|---|---|---|
| 1 | `b1-0031` | `corpus/batches/batch1/b1-0031.pdf` | new row, new document |
| 2 | `b1-0001` | `corpus/batches/batch1/b1-0001.pdf` | **overwrites** the existing one-page schedule |
| 3 | `b1-0032` | `corpus/batches/batch1/b1-0032.pdf` | new row, new document |
| 4 | `b1-0033` | `corpus/batches/batch1/b1-0033.pdf` | new row, new document |

After each one: print to PDF, name it by its `doc_id`, then a second pass over `field_pages`.
Because the schedule is section 1 of every document, every extracted value lands on page 1 and
`field_pages` stays empty — but check that rather than assuming it.

---

## Shared preamble — goes at the top of all four

```
You are a Singapore insurance product drafter. Write a COMPLETE, INTERNALLY CONSISTENT
policy document for the insurer named below. This is synthetic material for a university
project's test corpus.

LIFE ASSURED / INSURED:    Marcus Lim Jun Wei, born 8 May 1987, Singapore
ADDRESS:                   Blk 45B Tampines Ave 8 #07-21 Singapore 521045

STRUCTURE - produce all of these, in this order, with numbered clauses:
  1. Policy schedule (a one-page table: policy number, insured, cover, sums, premium,
     period, and the payment due date)
  2. Definitions
  3. What is covered - the benefit table, with amounts and limits per benefit
  4. What is not covered - exclusions, numbered
  5. Waiting periods, pre-existing conditions, and survival periods where they apply
  6. How to claim - the steps, the documents required, and the notification deadline
  7. Premiums, renewal, lapse and reinstatement
  8. General conditions, including free-look, cancellation and governing law

RULES:
  - Name real Singapore hospitals, schemes and public bodies wherever a real policy would.
  - Use Singapore conventions: SGD, DD Month YYYY dates, CPF/MediSave where realistic.
  - Every figure must be consistent everywhere it appears in the document.
  - Do NOT print a document reference, form number or "Ref:" line anywhere: the
    extractor mistakes them for the policy number.
  - Write it as the policy itself. No commentary, no "here is your document", no notes.
```

---

## Prompt 1 — Whole life · `b1-0031` · `LF-2015-330277`

```
[shared preamble]

REGISTER ROW (do not print in the document): b1-0031
INSURER (fictional):     Lionhead Life Assurance
POLICY:                  Whole Life
PRODUCT NAME:            Heritage Whole Life Plan
POLICY NUMBER:           LF-2015-330277
COVER PERIOD:            from 1 June 2015, for the whole of life
MATURITY:                7 May 2087, the policy anniversary at age 100
SUM ASSURED:             SGD 300,000.00
ANNUAL PREMIUM:          SGD 3,600.00, payable annually on 1 June
PREMIUM PAYING TERM:     to age 70

This document is the original policy contract issued at inception in 2015, so date it
1 June 2015.

Print the maturity date as a MATURITY DATE, not as an expiry date. A whole life policy
does not expire; state in the schedule that cover continues for the whole of life and
that the sum assured is payable on death or on surrender.

MANDATORY - a GUARANTEED SURRENDER VALUE table by policy year. Three rows are fixed and
must appear exactly, because three anniversary statements already in the corpus quote
them and the document must agree with all three:

    policy year  9   surrender value SGD 15,600.00   total premiums paid SGD 32,400.00
    policy year 10   surrender value SGD 20,100.00   total premiums paid SGD 36,000.00
    policy year 11   surrender value SGD 24,800.00   total premiums paid SGD 39,600.00

Build the rest of the table around those three. It must be strictly increasing, must show
nil surrender value in years 1 and 2, and total premiums paid must always equal the policy
year times SGD 3,600.00. Extend it to at least policy year 30.

Include: a death benefit clause, a terminal illness advance clause, a policy loan clause
against the surrender value, a non-forfeiture / automatic premium loan clause, and a
participating-fund bonus clause that states clearly that bonuses are not guaranteed.
```

**Why the three fixed rows matter.** `b1-0013`, `b1-0014` and `b1-0015` are the same policy
described three times at a rising surrender value. That is deliberately the case that catches a
system answering from one document when the question spans several, and `corpus/canon.md` says
it must not be disturbed. If the notebook invents its own surrender figures, the full policy
contradicts all three statements and the contradiction is a *corpus* defect rather than a
finding.

---

## Prompt 2 — Private car · `b1-0001` · `MV-2026-448120`

```
[shared preamble]

REGISTER ROW (do not print in the document): b1-0001
INSURER (fictional):     Meridian Assurance
POLICY:                  Private Car
PRODUCT NAME:            Private Car Insurance Policy
POLICY NUMBER:           MV-2026-448120
VEHICLE:                 seven-seat MPV, 1.8, registration SLK 8842 D,
                         first registered 12 April 2021
COVER PERIOD:            12 April 2026 to 11 April 2027
SUM INSURED:             SGD 62,000.00
EXCESS:                  SGD 750.00 per claim
ANNUAL PREMIUM:          SGD 1,284.00
PAYMENT DUE DATE:        28 March 2026
DATE OF ISSUE:           20 March 2026

Comprehensive cover. The benefit table must cover: loss or damage to the vehicle,
third party bodily injury, third party property damage, windscreen cover, towing and
recovery, and a personal accident benefit for the driver.

Include a NO CLAIM DISCOUNT clause and a clause on how the discount is affected by a
claim. Include an AUTHORISED DRIVERS clause, a clause on named-driver versus any-driver
cover, and a young or inexperienced driver additional excess.
```

**Two things this must agree with.** `b1-0004` is the renewal notice that led to this period —
expiry 11 April 2026, renewal premium SGD 1,284.00, payment due 28 March 2026. `b1-0007` is a
claim letter: claim `CLM-2026-01887`, incident 14 May 2026, settled SGD 3,480.00, and the policy
renewed anyway. The full policy must not say anything that makes either impossible — in
particular, do not write an exclusion that would have barred that claim.

**This overwrites the existing `b1-0001.pdf`.** The register row does not change.

---

## Prompt 3 — Private hospital and surgical · `b1-0032` · `PH-2022-604188`

```
[shared preamble]

REGISTER ROW (do not print in the document): b1-0032
INSURER (fictional):     Meridian Assurance
POLICY:                  Private Hospital and Surgical
PRODUCT NAME:            PrivateCare Hospital and Surgical Plan
POLICY NUMBER:           PH-2022-604188
COVER PERIOD:            1 March 2026 to 28 February 2027, annually renewable
FIRST TAKEN OUT:         1 March 2022
ANNUAL LIMIT:            SGD 1,000,000.00
DEDUCTIBLE:              SGD 3,500.00 per policy year
CO-INSURANCE:            10 per cent, capped at SGD 3,000.00 per policy year
ANNUAL PREMIUM:          SGD 1,860.00
PAYMENT DUE DATE:        20 February 2026
DATE OF ISSUE:           10 February 2026

THESE THREE CLAUSES CARRY THE WHOLE DEMONSTRATION. Write them carefully:

  - A WARD AND HOSPITAL ENTITLEMENT clause stating that the plan covers treatment at
    ANY PRIVATE HOSPITAL IN SINGAPORE, and at what proportion. State it as a CLASS of
    hospital. Do NOT list hospitals by name and do NOT invent a named panel - the plan
    is deliberately open to any private hospital, and a named list would make the
    answer a name-match instead of a reading of the entitlement. State the entitlement
    for a private hospital, for a public hospital, and for treatment outside Singapore.

  - A SURGICAL BENEFIT schedule classifying operations by table, Table 1 to Table 7,
    with a payable amount per table. List APPENDICECTOMY explicitly with its table.
    Put a representative handful of other named operations against each table so the
    classification is legible, and state what happens when two procedures are performed
    in one operation.

  - A clause on PRE-AUTHORISATION: when it is required, how far in advance, and what
    happens to a claim if it was not obtained. Then a clause on what happens if
    treatment is taken at a hospital OUTSIDE the entitlement - reduced proportion, not
    outright refusal.

Also include: room and board, intensive care, surgeon and anaesthetist fees, operating
theatre, implants, pre-hospitalisation consultations and post-hospitalisation follow-up
each with its own limit and window; a day surgery benefit; an emergency overseas
benefit; and a clause on how the deductible and co-insurance interact so a worked
example is possible.

Waiting periods: 30 days general, 12 months for specified conditions, and state where
appendicitis falls. Pre-existing conditions excluded unless declared and accepted.
```

**This is the one the demo question turns on.** *"If I have appendicitis, can I claim the
operation at Raffles Hospital?"* — the entitlement clause states the class (any private
hospital) so the answer is a reading rather than a name match. Parrot must answer by reading
the entitlement clause together with the surgical benefit table (appendicectomy, and which
table it sits in).
Two citations, two clauses, one answer.

**`PH-2022-604188` must not touch `HS-2023-771904`.** That is Lim Ah Kow's hospital income plan
with Lionhead, and the 40 per cent jump at its 2027 renewal is the Alert module's
demonstration. Different insurer, different prefix, different person. Nothing in this document
refers to it.

---

## Prompt 4 — Critical illness · `b1-0033` · `CI-2019-215736`

```
[shared preamble]

REGISTER ROW (do not print in the document): b1-0033
INSURER (fictional):     Lionhead Life Assurance
POLICY:                  Critical Illness
PRODUCT NAME:            CareShield Critical Illness Plan
POLICY NUMBER:           CI-2019-215736
COVER PERIOD:            1 September 2019 to 31 August 2049, a 30-year term
SUM ASSURED:             SGD 200,000.00
ANNUAL PREMIUM:          SGD 2,040.00, payable annually on 1 September
DATE OF ISSUE:           1 September 2019

This is the original policy contract issued at inception, so date it 1 September 2019.
The term expires on the policy anniversary after the life assured's 62nd birthday.

MANDATORY - a SCHEDULE OF COVERED CRITICAL ILLNESSES, numbered, with a one-paragraph
diagnostic definition for each. Cover at least 30 conditions across the usual groups:
cancer, heart and circulatory, neurological, organ failure and transplant, and loss of
independent existence. Each definition must state what evidence establishes the
diagnosis.

MANDATORY - state the SURVIVAL PERIOD in its own clause, and apply it consistently
everywhere it is mentioned.

Include: a multi-stage benefit that pays a stated proportion of the sum assured on an
early or intermediate stage diagnosis and the balance on a severe stage diagnosis, with
the proportions stated as percentages AND as amounts in SGD; a 90-day initial waiting
period for cancer and heart conditions; an exclusion for pre-existing conditions; an
exclusion for conditions arising from self-inflicted injury; and a clause stating
clearly that the policy has NO surrender value and NO maturity benefit, because it is a
term plan.
```

---

## After all four

```bash
uv run python -m corpus.validate corpus/register/batch1.csv
```

Then check, per document, before committing:

- [ ] No `Ref:` line anywhere — it gets extracted as the policy number
- [ ] Every figure matches the register row character for character
- [ ] `b1-0031`: the surrender table's years 9, 10 and 11 match `b1-0013`/`b1-0014`/`b1-0015`
- [ ] `b1-0032`: appendicectomy is named, and the private-hospital entitlement is stated
- [ ] `field_pages` checked, not assumed
