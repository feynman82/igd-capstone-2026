# 17 · A pack is grounding and persona; the core owns documents

- **Status:** Accepted
- **Date:** 2026-09-17
- **Decider:** Christian (Lane A, orchestrator). Reviewers: Siew (identity data, data inventory), Yew Mun (catalogue readers, evaluation). Informed: Zee (pack authoring moves)
- **Supersedes:** ADR 0014 on where document types, fields and registers live. Amends ADR 0016: `FactInput.pack` is removed.

## Context

ADR 0014 said a pack supplies what the core knows about a domain. Coding agents read that as
putting the household's document definitions in packs, and built it: `insurance_agent` declares
the policy types, their fields and the register columns. So a household's documents belong to
whichever pack happened to be installed, and disabling that pack would switch them off.

The owner also wants identity questions answered: "What is Rachel's passport number?" for an
airline booking, "When was Marcus born?". No pack is the right home for a passport. And a policy
schedule prints several riders, each with its own sum assured, which one field per fact cannot hold.

## Decision

1. **A pack is knowledge and voice.** A specialised pack (e.g. `insurance_agent`) holds only:
   - `grounding`: its corpus under `packs/<pack>/grounding/<corpus>/` with `sources.yaml`, and
     `grounding.values`;
   - `persona`, and `guardrails` including the disclaimer;
   - its own `answering`, centred on advice: vocabulary, categories, exclusions, `max_sentences`;
   - `advice`.
2. **The core owns documents.** Document types, their fields, `registers` (reminders and alerts)
   and a generic core `answering` move to one catalogue, `core/documents.yaml`, validated by a
   new `DocumentCatalog` contract (its own contracts PR). `python -m packs.build` generates from it
   `core/document_schemas.py` (replacing `packs/*/schemas.py`), `corpus/register/core_columns.csv`
   (replacing the per-pack column files), the batch template and `docs/field-dictionary.md`.
   Every ingested document, extracted fact and identity datum is core's, whichever packs are
   installed or enabled. Classification candidates are the catalogue's types, not qualified by pack.
3. **Facts are written with `pack_id = 'core'`, and `core` is always enabled.** No migration:
   `facts.pack_id` stays NOT NULL and holds the constant. Disabling a pack switches off its
   persona, answering rules, grounding and advice, never the household's documents. Existing rows
   are re-read through the real pipeline with `scripts/reindex.py`.
4. **Two answering layers.** Core `answering` serves everyday questions and always applies. An
   enabled pack's `answering` adds its vocabulary, categories and exclusions. Vocabulary is
   unioned. A pack's categories and exclusions name core fields, checked against the catalogue
   when packs load.
5. **Advice shapes read core facts.** `FactInput.pack` is removed; there is no other pack's fact
   to read. `doc_types` and `field` are catalogue names, checked at load. One catalogue-aware load
   check replaces `core.packs.check_advice_links`.
6. **Identity data is household data.** NRIC/FIN, passport and birth-certificate numbers and
   dates of birth for the owner, partner, children and parents are ingested, chunked, extracted
   and answerable. New core types: `identity_card`, `passport`, `birth_certificate`, and
   `loan_agreement` for the household's loans. A date of birth comes from ingesting the uploaded
   document; no pack declares a type for it. The data stays on-device, behind the app lock, and is
   recorded in `docs/governance/data-inventory.md`, which Siew reviews.
7. **Repeating printed rows.** A new `FieldType` `labelled_money` and `FieldSpec.repeats: bool`
   give one fact row per printed item: `value_text` is the printed label (the rider name),
   `value_num` the amount. The row holds the pairing, so no migration. The register writes a
   repeating cell as `Label=amount;Label=amount`. `DocumentTypeSpec.fields` rises from 12 to 16.

## Alternatives considered

| Option | Why not |
|---|---|
| Keep document types in packs (ADR 0014 as built) | A household's passport would belong to whichever pack was installed, and vanish from answers when that pack is disabled |
| A second datastore, or a table per identity type | "One database" in `AGENTS.md`; the facts table already carries a number, its page and its document |
| One pack called `core` in `packs/` | A pack can be disabled; household data cannot. It would also invite a pack author to edit it |
| A `facts.item` column to pair riders with amounts | An `ALTER` behind rule 4, for a pairing one row already holds in `value_text` and `value_num` |
| `answering` only in core | Insurance words would sit in the everyday layer, and a pack could not specialise |

## Consequences

**Easier:**
- Installing, disabling or removing a pack never loses a document or a fact.
- Identity questions are answerable, with the page cited.
- A pack author writes knowledge and voice only.
- Riders are counted and compared one by one.

**Harder or open:**
- **Identity numbers are the most sensitive data in the vault.** They are protected only by
  on-device storage and the app lock, and need their data-inventory entry before they ship. No
  synthetic passport exists for Rachel yet, so until one is generated the passport question abstains.
- **`labelled_money` extraction of a many-row table depends on the 4B model**, and a dropped rider
  is silent.
- **Field names are now shared** across what were two packs. The catalogue checks uniqueness per
  type only, so the same name meaning different things on two types is a review matter.
- **Every pack-scoped query changes once**, and so does `AGENTS.md` rule 6's list of what
  `pack.yaml` generates.
- ADR 0014's placement of `document_types` and `registers`, and ADR 0016's `FactInput.pack`, are
  superseded.

## Revisit when

- A pack needs a document type the core does not have. The answer is to add it to the catalogue,
  reviewed, not to the pack.
- A repeating table needs more than a label and an amount.
- Identity data leaves the device.
