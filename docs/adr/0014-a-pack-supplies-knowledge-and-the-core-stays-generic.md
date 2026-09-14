# 14 · A pack supplies what the core knows about a domain, and the core stays generic

- **Status:** Proposed
- **Date:** 2026-09-13
- **Decider:** Christian (Lane A), after a seven-seat design council; reviewed by Zee (packs, grounding), Siew (advice line, provenance), Yew Mun (ports)

## Context

A pack was a field list plus two guardrail numbers. `persona.system` was read nowhere. `grounding` was declared, but nothing indexed or retrieved it. The measurements below come from the live vault on 13 September: six policies, the dense stopgap, GPU.

- **Dental** was answered with the hospital plan's dental *exclusion clause*, and never said no.
- **Dengue** ("warded for dengue 3 days, can claim?"):
  - the understanding step read "warded" as "awarded";
  - the answer was 20+ cited sentences, including the car policy's benefit table.
- **"Got warded 2 days, claimable?"** abstained at 0.44 against a floor of 0.45.
- **"Should I buy critical illness cover?"** was routed as a request for an explanation.

Each of those sentences carried a citation, so the gate passed them all. The failures are about knowing the domain, not about grounding. The core cannot hold insurance words without breaking the claim that a second pack installs against an unchanged core.

## Decision

**A pack declares answering knowledge. The core applies it without adding model calls.** `PackManifest.answering`, reviewed in its own contract PR, holds:
- **`vocabulary`:** what a household says → what the paper prints.
  - The question is reworded and searched alongside the model's phrasings.
  - Only the matched lines go into the understanding prompt.
- **`categories`:** ordered rules matched as whole words against one printed field (insurance: `product_name`).
  - The first match wins; no match is a valid result.
  - A category is derived when a question is asked and never stored. It is not a field and never becomes a register column, so `packs/README.md`'s "is it printed?" test still holds.
- **`exclusions`:** headings under which a sentence claiming cover is not believed.
- **`max_sentences`.**

**The core does six things with it:**
1. **Inventory.** It reads the documents on file from `facts` with one hand-written query. Each line cites the page its name is printed on.
2. **Category filter.** It sets aside passages from documents of another category *before* the keep-6 cut. Documents with no category are always kept.
3. **Absence sentence.** When a question names a category nobody holds, code writes: "None of the N policies on file is a dental plan." It cites every document counted.
4. **Advice route.** It adds a third route intent, `advise`. A request for a recommendation, a comparison or an adequacy judgement gets the pack's `advice_decline`, plus an offer of a neutral question. Nothing is summarised alongside it. `Guardrails.never_recommends` is `Literal[True]`, beside `never_acts`.
5. **Gate checks.** Beyond "is it cited", the gate drops a sentence that states a number no cited passage prints, or that claims cover citing only an exclusion. It caps answers at the pack's sentence limit and closes the stream.
6. **Persona as voice.** `persona.system` is placed before the core's rules, which come last. Disclaimers now sign abstentions and declines too.

**Published guidance is a second evidence lane, never a second household.**
- It lives in `grounding_sources` and `grounding_chunks`, a create-only migration, not in `documents`. If it were in `documents`, household scoping would treat it as belonging to everyone, and "nothing filed under you" could never fire.
- Every passage carries a `kind`: `document`, `inventory` or `guidance`. The gate identifies citations by kind and id.
- Guidance carries publisher, title, URL, published and retrieved dates, and what it applies to.
- It is cited only after household evidence has cleared the floor, or after the absence sentence has answered.
- One sentence cites one lane.
- A source past `review_by`, or never signed off, is excluded in SQL.
- Grounding text is public guidance, committed with provenance, and the README states Parrot is not a licensed MAS- or MOH-regulated professional.

## Alternatives considered

| Option | Why not |
|---|---|
| A: persona and vocabulary only, guidance in the same retrieval | Fixes the "warded" misread and nothing else. Guidance has no subject, so scoping keeps it for every person, and a chip cannot tell MOH from the household's own policy. |
| C: a router picks a pack and runs that pack's own graph branch | Adds a 4B model call before any evidence exists. A wrong pick silently applies the wrong floor and persona. Per-pack branches pull domain logic into `core/`, and questions that span packs (life insurance relief) split in two. |
| E: hand-written SQL per pack per question shape | Deterministic, but per-pack code in the core breaks "a pack is a YAML file". The generic inventory covers the insurance shapes; tax sums belong in module queries scoped by subject and year. |
| The model decides categories and absence from an inventory in its prompt | ADR 0013 measured a 4B reader writing "You have travel insurance." from unrelated passages. A "no" written by code cannot be talked into a "yes". |
| The understanding step picks which documents to read | A wrong pick removes evidence the gate cannot see, and adding fields to that call degraded its searches before (ADR 0013). |
| Move the floor to reranker scores now | Correct eventually, but it changes every pack's `abstain_below` at once. It is Lane B's to decide, with the golden set. |

## Consequences

**What this makes easy:**
- Dental, travel, pet and helper questions get an honest, cited "no".
- Car and hospital questions name the policy.
- Dengue reads only the hospital plans.
- "Warded" is found without the model.
- Advice is declined in code.
- A second pack gains all of this by writing YAML.
- A citation says which lane it came from.

**What it makes hard, or leaves open:**
- **Categories can be wrong.** A misfiled product hides a policy from an answer. Precision is tested against a trap table (hospital *income* vs expense, CareShield Critical Illness vs CareShield Life, "Life Assurance" in insurer names), and "no category" keeps a document visible.
- **"None of the N on file" is only about the vault.** An employer's group policy or card travel cover that was never filed is not in it. The answer shows how many documents sit in quarantine.
- **The number check is literal.** A model that reformats "SGD 1,860.00" as "one thousand eight hundred and sixty dollars" loses the sentence. Entailment beyond numbers and exclusion headings is still unchecked.
- **The exclusion guard is conservative.** "Your plan covers emergency dental treatment after an accident" is dropped even though the exception makes it true. The quoted form survives.
- **The decline depends on the 4B router.** False declines on answerable questions must stay at 1 or fewer in 60.
- **Two contract additions a pack author must learn:** `answering` and `advice_decline`. §6b of `packs/README.md` covers them.
- **Terms of use.** MAS, MOH and IRAS pages carry reproduction terms. The project treats the indexed text as public guidance for a private research prototype; Siew records that basis in the governance chapter.
- **The stopgap grounding retriever is dense-only** until Lane B implements `GroundingRetriever` with hybrid search.

## Revisit when

- Categories misfile more than 0 of the trap table, or the dengue probe cites a policy of another category.
- The advise intent declines more than 1 of 60 answerable golden questions.
- Guidance raises p95 answer latency above 10 s, or lowers answerable accuracy.
- A third pack cannot express what it needs in `answering` without code.
