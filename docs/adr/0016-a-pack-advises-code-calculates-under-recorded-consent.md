# 16 · A pack advises: code calculates from cited facts and reviewed rule values, under recorded consent

- **Status:** Proposed
- **Date:** 2026-09-14
- **Decider:** Christian (Lane A), after a seven-seat design council. Reviewers: Siew (consent, disclaimer, records), Zee (pack authoring, grounding location), Yew Mun (ports, evaluation)
- **Supersedes:** ADR 0014, decision 4 (the advice route declines). Amends ADR 0014 on where a grounding corpus lives.

## Context

ADR 0014 declined every request for a recommendation: `Guardrails.never_recommends: Literal[True]`,
and a code-written decline. The owner has decided that a domain pack exists to be a specialist, and a
specialist answers "is my critical illness cover enough?", "should I keep my whole life plan?",
"which of my hospital plans is better?" and "is my plan better than an Integrated Shield Plan?". The
autonomy statement already said v1 "observes, retrieves and advises" (`docs/governance/README.md:19`).

Four facts shaped how:

- A 4B generator's arithmetic cannot be trusted, and the gate cannot check a figure no page prints.
- A published rule (MoneySense's protection multiples, an SRS cap, an IRAS rate band) is a number with
  a publisher and a date. It changes, and a stale one produces confident wrong advice.
- A pack is a developer-built add-on a household downloads. Its published guidance has to travel with it.
- Advice given on incomplete facts reads as suitability. The honest answer to a missing fact is to
  name it, not to estimate around it.

## Decision

**A pack declares advice shapes. Hand-written calculators compute. The model only explains.**

1. **Contract (its own PR).**
   - `Guardrails.never_recommends` is removed.
   - `Guardrails.verdict_by_code: Literal[True]` is added: a verdict is chosen by code, never written
     by the model.
   - `never_acts: Literal[True]` is unchanged.
   - `PackManifest.advice` declares these, all validated when the pack loads:
     - the consent text and version;
     - the disclaimer;
     - the named-product disclosure;
     - **shapes**, each naming a calculator from a closed list (`gap`, `remaining_room`,
       `keep_or_surrender`, `compare_own`, `compare_market`, `estimate_saving`), the facts it needs
       (document types, field, category, how to take them), the rule values it needs, the fields it
       compares and a **stated ordering rule**, and whether the result is an **estimate**.
   - A pack without `advice` still declines, as today.
2. **Grounding lives inside the pack.** A corpus is `packs/<pack>/grounding/<corpus_id>/`, with its
   `sources.yaml`, so a downloaded pack carries its sources. `Grounding.values` declares the rule and
   table keys its sources publish (key, unit, qualifiers such as age band, ward class, insurer, product,
   residency, assessment year).
3. **Rule and market values are typed rows, extracted automatically and approved by a person.**
   - An indexer reads each source's verbatim text. It asks the model for the declared keys, keeps a
     value only when its passage is a verbatim substring of the source and its number is a whole
     printed token in that passage, and writes it `pending`.
   - A reviewer approves or rejects each row, and records who and when.
   - A calculator reads a value only if all of these hold:
     - it is approved;
     - its source is reviewed;
     - the source's `review_by` has not passed;
     - its effective dates cover today;
     - for prices, it was retrieved within the pack's price age.

   All of this is enforced in SQL. Migration `0003_advice.sql` is CREATE-only.
4. **Calculators are modules.** `modules/advice/` reads facts and approved values with hand-written
   queries, scoped to the subject's confirmed aliases.
   - **What each returns:** a `Calculation` (figures, inputs with their citations, a code-written
     verdict sentence, a comparison table) or a `Missing` (the pack's own wording for each missing
     fact or rule).
   - **Market comparisons** need only a partial product match: the same category and at least one
     field both sides print. They compare only shared fields, and rank only by the shape's declared
     ordering field.
   - **Estimates** are labelled as estimates.
5. **The graph.**
   - `advise` no longer stops at a decline when the asked pack has advice. The shape is matched from
     its `asked` phrases, without a model.
   - The subject is resolved by household scoping: the owner, or a confirmed member.
   - If the owner's consent for the pack's current consent version is not recorded, the stream yields
     `ConsentRequired` and nothing else.
   - A `Missing` yields `AdviceWithheld`.
   - A `Calculation` yields an `AdviceCard` (verdict, figures, cited inputs, comparison rows,
     disclaimer, product disclosure when a product is named). Then at most three model sentences
     explain it. They are gated by a new check: every number must equal a printed input or a figure
     whose role word the sentence uses, no verdict word may appear, and none of the shape's
     `never_say` phrases may appear.
   - Advice costs two model calls: route and explain.
6. **Consent and records.**
   - The owner's consent covers confirmed adult household members.
   - `advice_consents` is append-only (granted or withdrawn, version, wording hash, channel).
   - `advice_records` keeps each advised or withheld answer's full basis: fact ids and values,
     value ids and sources, figures, verdict, disclaimer hash and consent id.

## Alternatives considered

| Option | Why not |
|---|---|
| Keep declining (ADR 0014) | The owner's product decision; a specialist that will not advise is not a specialist |
| Rule values typed into `pack.yaml` by the author | No SQL-enforceable review or staleness; a number nobody can trace to a passage |
| A formula language in `pack.yaml` | A runtime query builder in `core/`; the spirit of rule 1; unauditable by a non-programmer; still needs domain words in core |
| Model-led advice with the number check relaxed | Unverifiable arithmetic; no reproducible basis for a record; rule 3 unenforceable exactly where it matters |
| A fourth model call to pick the shape | Phrase matching is deterministic and free; a wrong shape is correct arithmetic on the wrong question |

## Consequences

**Easier:**
- A household gets a figure it can check: every input is cited, and so is every rule with its
  publisher and date.
- Missing information is named.
- A pack author writes words and keys, not numbers or formulas.
- Every advice answer can be reconstructed from its record.
- The tax pack uses the same mechanism (SRS room, CPF top-up relief, an estimated tax saving).

**Harder or open:**
- **Named products.** Advising on life and health policies may be regulated whatever the disclaimer
  says. The prototype stays private and non-commercial, and Siew's model card must say so.
- **Consent is the owner's.** Advice about an adult member rests on the owner's consent (the
  owner's decision); the data inventory must record that purpose.
- **Extraction is only as good as review.** A misaligned table cell with a printed number passes the
  automatic checks, and only a person catches it.
- **Household facts still come from extraction.** Its substring page check can accept a wrong digit
  (tracked separately), and a calculator trusts facts.
- **The role-word check is lexical.** It catches "shortfall SGD 400,000" when 400,000 is the target
  only if the target figure's role words are absent from the sentence.
- **Facts the packs do not capture yet** (date of birth, bonus, residency, lapse) make shapes that
  need them withhold until Zee's fields and Desmond's batch 2 exist.
- **`grounding/` moves** into each pack; its README becomes a pointer.

## Revisit when

- Siew or a reviewer finds an approved value that no passage supports.
- The explanation drops more than a third of its sentences on the golden set.
- A pack needs a calculation the closed list cannot express.
- The prototype is shown to anyone outside the team as a service.
