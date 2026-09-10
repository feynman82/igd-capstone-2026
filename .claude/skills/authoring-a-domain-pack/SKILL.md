---
name: authoring-a-domain-pack
description: Author or revise a PARROT domain pack — a pack.yaml describing a kind of household document and the fields printed on it. Use when creating a new pack, adding a document type, changing a field list, or when packs.build fails. Written for a non-technical author.
---

# Authoring a domain pack

A domain pack is **one file you write** — `packs/<pack_id>/pack.yaml` — and three files
generated from it. It tells the system what a kind of document is and what is printed
on it.

## Before anything else

Read, completely, in this order:

1. `packs/README.md` — the guide, written for a non-technical author
2. `packs/iras_tax/pack.yaml` — a worked example, 4 document types
3. `AGENTS.md` — the repository's working rules

Do not skip these. A pack written without them will fail validation in ways that are
tedious to explain afterwards.

## The rule that governs everything

A field name written in `pack.yaml` becomes **three things at once**: the attribute on
the extraction model, the `facts.key` it is stored under, and **the column heading in
the corpus register that a teammate fills in by hand**.

So a rename is not a rename — it is a rename in three places plus a conversation with
whoever has already started filling the spreadsheet. Get the names right the first time,
and when unsure, **ask the author rather than guessing**.

## Work in this order, stopping for the author at each step

**1 · Propose, do not write.** List the document types and, under each, the fields you
believe are printed on it: field name, type, and one sentence on where on the page it
appears. Show this as a table. Write no files. Wait.

Challenge the author's list if it is wrong. Two document types that a person would call
by the same word are one type — every insurer's renewal notice is one `renewal_notice`,
not one type per insurer. Say so.

**2 · Write the YAML.** Copy the structure of `packs/iras_tax/pack.yaml`. Constraints
the contract enforces (`core/contracts.py`):

- 1–12 fields per document type; 3–5 document types per pack
- `description` at least 8 characters, at most 200 — say *where on the document* the
  value appears, not just what it is
- `type` is one of: `string` `identifier` `person` `money` `integer` `percent` `date`
  `month` `enum` `boolean`
- `identifier` is copied character for character, never normalised — policy numbers and
  receipt references are `identifier`, not `string`
- `enum` also needs a `values:` list
- field names are lowercase with underscores
- **quote every `example:` for a date, month, money or boolean** — bare `2026-03-01` is
  parsed by YAML as a date object and fails validation
- `subject_field` names the field that says whose document this is

**3 · Draft the persona and guardrails for approval.** Two sentences of persona: what
the assistant explains, and what it refuses to do. Resist writing a personality.
The disclaimer is 20–800 characters and specific to the domain.

Leave `must_cite: true`, `abstain_below` and `never_acts: true` exactly as the existing
packs have them. `never_acts` is typed `Literal[True]` — a pack that sets anything else
will not load, and that boundary is what the governance chapter is built on.

**4 · Generate.** `python -m packs.build`. Show the author what it produced.
If it errors, explain the error in plain language and fix the **YAML** — never a
generated file.

**5 · Check the human-readable output.** `python -m packs.build --check`, then show the
author the new `corpus/register/<pack_id>_columns.csv`. That spreadsheet is a teammate's
brief. If the column headings do not read sensibly to a person, the field descriptions
are unclear, and the extractor will struggle with them too. Fix them now.

**6 · Stage and propose a commit.** `pack.yaml` **and** every generated file, together.
CI fails a commit with one and not the other. Do not commit until told to.

## Grounding, when the pack needs it

Some domains need authoritative reference material beyond the user's own documents
(a tax pack asked "can I claim this?"). Point at it:

```yaml
grounding:
  corpus: iras_reliefs_ya2026   # or: null, to answer only from the user's documents
  top_k: 6
```

Official issuers only — IRAS, CPF Board, MAS, MOH, a named regulator. Never a blog or a
comparison site. Record the retrieval date in `grounding/<corpus>/sources.yaml`; rules
change by assessment year and the report must say which year was used. Twenty
well-chosen pages beat two hundred scraped ones.

`corpus: null` is a designed guardrail, not a gap — say so if the author asks.

## Never

- Hand-edit `packs/*/schemas.py`, `corpus/register/*_columns.csv` or
  `docs/field-dictionary.md`. They are generated.
- Touch anything outside `packs/` and `grounding/`.
- Add a dependency.
- Invent a field name the author did not agree to.

## Done

- [ ] 3–5 document types, 4–8 fields each
- [ ] Every description says where on the paper the value appears
- [ ] Realistic Singaporean examples, quoted where they are dates, amounts or booleans
- [ ] `python -m packs.build --check` passes
- [ ] The register CSV reads sensibly to someone who has not seen the YAML
- [ ] Persona and disclaimer written; the disclaimer is domain-specific
- [ ] `pack.yaml` and the generated files staged together
