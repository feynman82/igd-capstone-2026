# §4.3–4.4 · Packs and the interface, with the expansion model

**Owner: Zee (Lane D).** It feeds three places in the report:

- §3.3, "Two axes of expansion";
- §4.3, "Domain packs as an enforced contract";
- §4.4, "The interface".

It is the W10 task's chapter of about three pages, with the expansion model and the pack catalogue.

> **Draft status.** Written on 17 October, before the code freeze on 28 October. The skeleton asks
> for §4 after the freeze, so every fact below is tied to a file and should be re-checked then.
> Facts that can still move:
>
> - whether the tax corpus is indexed and its two rule values approved;
> - the usability test of Ask, which has not happened yet;
> - the surface list.
>
> The skeleton budgets half a page each for §4.3 and §4.4, and three-quarters for §3.3. This is
> the longer source they are condensed from.

---

## The argument

A household assistant that answers about insurance can be extended to tax by writing a file,
not a release. That holds only if three things are true. Each section below shows one with a
file.

1. **A pack is data, checked against a contract before it can load.**
2. **The household's documents belong to the core, not to any pack.**
3. **The interface shows where every claim came from, and says plainly what it could not read.**

## 1 · The expansion model (feeds §3.3)

Parrot grows along two axes that do not touch:

- **Capability modules** extend what the assistant can *do*. Three are built: Reminder, Alert
  and the Advice calculator module (`modules/`). Tracker is specified in the core registers
  (`core/documents.yaml`).
- **Domain packs** extend what it *knows about*. Two are built: Insurance and Coverage
  (`packs/insurance_agent/`) and Tax and Reliefs (`packs/iras_tax/`). Nine more are specified
  against the same contract (`packs/catalogue.yaml`).

Because the axes are independent, every module applies to every pack whose documents print what
the module reads. Reminder needs only a printed date. That is why eight of the nine specified
packs use it without a line of new module code.

## 2 · What a pack is, and what it stopped being (ADR 0017)

The proposal's pack owned its document types and their fields (proposal §7.1). Building it showed
why that was wrong. If a pack owns a document, then disabling the pack hides the household's
documents. Two packs that both read a payslip each declare it, and the declarations drift apart.

ADR 0017 split the two:

- **The core owns documents.** Every document type and field is declared once, in
  `core/documents.yaml`. Facts are written as the core's (`pack_id = 'core'`). Switching a pack
  off removes its voice and knowledge, never the household's papers.
- **A pack is knowledge and voice.** It holds:
  - grounding: a corpus of official sources with recorded provenance;
  - a persona, guardrails and a disclaimer;
  - answering rules: vocabulary such as "kena warded" → "hospitalised as an inpatient",
    categories read from printed product names, and exclusions;
  - optionally, advice.

**An example.** The tax pack and the insurance pack both use the payslip, and neither declares
it. The tax pack's `answering.documents` simply names it.

## 3 · Enforced, not agreed (feeds §4.3)

A convention five people agree to is broken by week 6. Each rule below is enforced by code that
fails the build. This list is the substance of §4.3.

| Rule | How it is enforced | Where |
|---|---|---|
| A field name is written in exactly one place | `python -m packs.build` generates the extraction models, the corpus register columns and the field dictionary from `core/documents.yaml`. `--check` fails CI when any output differs from what the YAML generates | `packs/build.py`, `Makefile` |
| v1 advises and never acts | `never_acts: Literal[True]`: a pack that sets anything else does not load | `core/contracts.py` |
| The model never chooses a verdict | `verdict_by_code: Literal[True]`. Advice shapes name a calculator from a closed list; the model only explains the result (ADR 0016) | `core/contracts.py`, `modules/advice/` |
| A pack names only what the core declares | `check_against` runs at load. A misspelt document type or field stops the load, rather than silently withholding an answer | `core/contracts.py` |
| Nothing is cited until a person has reviewed it | A source with no `reviewed_on`, or past its `review_by` date, is excluded in SQL. A rule value is read only once approved | `modules/advice/queries.py`, `scripts/review_grounding_values.py` |
| The specified packs cannot drift from the contract | Each proposed type must validate as the core's own type spec. No field name may land in two different database columns. Each reminder must read a printed date | `tests/test_pack_catalogue.py` |

**The first rule is the one worth a paragraph in the report.** The corpus is scored by comparing
extracted values with a ground-truth spreadsheet whose columns are field names. Had the column
been `period` while the extractor wrote `pay_period`, the comparison would have found nothing.
Extraction would have scored zero, and the cause would have looked like a model failure. The
columns are therefore generated, never typed (`packs/README.md` §3). The team spent no time
hunting that bug, because it could not occur.

## 4 · The two built packs

| | Insurance and Coverage | Tax and Reliefs |
|---|---|---|
| Documents it speaks for | 5: schedule, renewal, claim, illustration, anniversary statement | 7: payslip, donation receipt, CPF, SRS, Notice of Assessment, CPF top-up, course fee |
| Grounding | 20 MoneySense, MOH, CPF Board and LIA sources, reviewed 17 Sep | 9 IRAS sources for YA2025–2027, reviewed 18 Oct |
| Values its calculators read | Protection multiples, MediShield Life premiums, DPS sums assured | SRS contribution cap, resident tax-rate bands |
| Advice | Death/TPD and critical-illness gaps, and one coverage review | SRS room left, estimated SRS tax saving, and one "reduce my tax" review |
| What it explains but does not calculate | — | Donations (250%), CPF top-ups: contract changes proposed in `packs/iras_tax/CONTRACT_REQUESTS.md` |

**Both packs run on the same core and the same calculators.** The tax pack added no calculator
and no core code. Its new document types went through the core catalogue, as ADR 0017 requires.
That is the "same core, two domains" claim, in the form the demonstration can show.

**The review did its job.** Siew signed off the nine IRAS sources on 18 October, after confirming
each URL and recording the copyright basis they are kept on
(`docs/governance/grounding-sources-basis.md`). She removed a tenth, an e-Tax Guide whose notice
forbids storing it in a retrieval system. Nothing depended on it: the 250% donation rate is
cited from the IRAS donations page instead. A source left the corpus because of a rule, not a
judgement call, which is the point of gating citation on review.

**The honest qualifier for §4.1.** Until the corpus is indexed on the integration machine and
the SRS cap and tax-rate values are approved, the tax pack cites no IRAS page and calculates
nothing.

## 5 · The catalogue as the expansion model's evidence

The nine specified packs come from the proposal (§7.3). They are restated in the contract's own
terms in `packs/catalogue.yaml`, with the reasoning in `packs/CATALOGUE.md`.

- **29 new document types**, each written as the core's own type spec, so building a pack starts
  from a reviewed proposal rather than a blank file.
- **5 existing types reused.** Vehicle reads the same motor policy schedule Insurance does. Travel
  reads the passport the core already captures.
- **5 packs deliberately have no grounding corpus.** For Health and Legal, grounding on general
  guidance would read as medical or legal advice, so declining to ground is the guardrail.

The catalogue is checked by a test, not just described. So the report can say the nine are
*specified against the contract* and point at the check that makes it true.

## 6 · The interface (feeds §4.4)

The proposal named four surfaces: Today, Ask, Vault and Packs. Two more have been added since:

- **Calendar** (ADR 0020), for the household's week;
- **Household**, where the people the documents name are recorded (ADR 0011).

The nav labels say what each surface is for: "What needs you", "A question about your
documents", "Everything filed", "What this assistant knows about" (`web/components/nav.tsx`).

Three design decisions carry the thesis into the screen. Each is a sentence for §4.4 and a
candidate screenshot:

- **The citation is a page, not a footnote.** A source chip names the document and the page
  ("Motor renewal notice, p.1"), never "[3]". Pressing it opens that page with the claim still
  on screen (`web/components/source-chip.tsx`).
  - Advice adds two chips that have no page: a **rule** chip says who published a value and
    when, and a **calculation** chip is plain text. A "p.0" button that opens an error would be a
    citation that lies about what it is.
- **What could not be read is a job, not an error.** The Vault's first group is **"Needs your
  eyes"**: documents that failed parsing, each with a reason and a retry through the
  vision-language model against the page image (`web/components/vault/quarantine.tsx`). This is
  the screenshot the skeleton asks for. It is the interface saying when the system could not
  read something.
- **Silence beats a guess.** An abstention is a designed state, not a failure: brass, not red.
  It names why Parrot declined and what would have answered (`web/components/ask/answer.tsx`).
  A red error box would tell the reader something broke, when the point is that the system held
  a line.

**Design tokens.** One accent colour, one radius scale and one type scale were locked before any
screen was built (`web/app/(app)/tokens/`). That is what kept the surfaces consistent across
sessions and people.

## What this chapter does not claim

- **That the interface is easy to use.** It has not been tested with anyone outside the team. The
  "Usability-test the Ask surface with two people who did not build it" task is not started.
  §4.4 should say so, or carry its result once it exists.
- **That the tax pack cites IRAS today.** See §4: its sources are reviewed, but the corpus is
  not yet indexed and its two rule values are not yet approved.
- **That any catalogue pack works.** "Specified" means named and checked against the contract.
  It does not mean built.
