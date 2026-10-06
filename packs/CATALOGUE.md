# The pack catalogue

Two packs are built: **Tax and Reliefs** (`iras_tax`) and **Insurance and Coverage**
(`insurance_agent`). Nine more are specified here but not built. They are written against the same contract the two
built packs use, so adding one is a YAML file and a reviewed core change, not a release. The core does
not change at all.

The list is the one agreed in the revised proposal (§7.3). It is restated in today's terms. Since ADR
0017 the core owns document types, so a pack reuses the core's types or proposes new ones. It never
declares its own.

**The source of truth is [`catalogue.yaml`](catalogue.yaml).** It names every document type and field,
each reminder date, and each grounding corpus. `tests/test_pack_catalogue.py` holds it to the
contract:

- Every reused type exists in `core/documents.yaml`.
- Every proposed type validates as a `DocumentTypeSpec`, so it can be pasted into the core unchanged.
- No field name would land in two different `facts` columns.
- Every reminder reads a date field one of the pack's documents prints.

This page does not repeat those names, so they are written down in one place.

## The nine packs

| Pack | Serves | New document types | Reuses from the core | Modules | Grounding |
|---|---|---|---|---|---|
| MOE Syllabus Teacher `moe_syllabus_teacher` | Sarah: two young children | 4 | none | Reminder, Tracker | MOE primary and secondary syllabuses |
| Vehicle and Road Tax `vehicle_road_tax` | Daniel and Rachel: motor cover lapsed unnoticed | 3 | the motor policy schedule and renewal notice | Reminder, Alert | LTA road tax, inspection and COE rules |
| Caregiving and Health `caregiving_health` | Marcus: ageing parents | 4 | the policy schedule and claim letter | Reminder, Tracker | None: the household's own documents only |
| Children and School `children_school` | Sarah: the household calendar | 3, plus the school circular | none | Reminder, Tracker | MOE school terms and holidays |
| Home Maintenance `home_maintenance` | Any household with appliances and contractors | 4 | none | Reminder, Alert | None |
| Legal and Estate `legal_estate` | Marcus: a will, an LPA, a title | 3, plus the tenancy agreement | none | Reminder | None: location and contacts, never interpretation |
| Property and Tenancy `property_tenancy` | Households that rent, let or pay off a home | 4 | the housing loan agreement | Reminder, Tracker | None in v1 |
| Groceries and Supplies `groceries_supplies` | Jason: business and household spending blur | 2 | none | Tracker, Alert | None |
| Travel `travel` | Daniel and Rachel, travelling with children | 2 | the passport and the travel policy schedule | Reminder | ICA passport guidance |

That makes 29 new document types across nine packs, and five existing core types reused.

## What the catalogue shows

**One core, two axes.** The modules column is the multiplication table from the proposal. Reminder
alone serves eight of the nine packs, because a date printed on any document can feed it.

**Reuse before addition.** Four packs lean on types the built packs already brought into the core.
Vehicle reads the same motor policy schedule Insurance does. Travel reads the passport the household
section already captures. Two pack types are shared between catalogue entries:

- the school circular, between the MOE and Children packs;
- the tenancy agreement, between the Property and Legal packs.

Each is proposed once and used by the other.

**No corpus is a guardrail, not a gap.** Five packs answer only from the household's own documents,
for one of these reasons:

- **Health and Legal:** grounding on general guidance would read as medical or legal advice.
- **Home Maintenance and Groceries:** there is no official source to ground against.
- **Property:** a later corpus (HDB, URA, IRAS property tax), not a v1 one.

**Every pack only advises.** Each entry's `stance` says what it will not do: grade a child, interpret
a result or a will, value a property, book, renew or pay. `never_acts: true` will apply to all nine
when they are built, as it does now to the two that are.

## What building one involves

1. **Propose its new document types for `core/documents.yaml`.** This is a core change, reviewed by
   Christian. Run `python -m packs.build`, and the register columns and field dictionary are
   regenerated for Desmond.
2. **Write `packs/<id>/pack.yaml`.** It holds the persona, the guardrails and the disclaimer, and the
   types it speaks for under `answering.documents`.
3. **Gather the grounding corpus, where there is one.** Each source needs provenance in
   `sources.yaml`, and Siew reviews it.
4. **Move the entry out of `catalogue.yaml`.** The test stops counting nine.

## Open questions

- **Children and School.** A term calendar prints many dated events. It is undecided whether each
  becomes a fact row (a repeating field) or the MOE grounding supplies the term dates.
- **MOE Syllabus Teacher.** Every subject is a minor, so the core withholds advice. The pack explains
  the syllabus and never grades.
- **Caregiving and Health.** Its documents are sensitive personal data. Siew's data inventory must
  cover it before anything is built.
