# Zee — Lane D · Domain packs and interface

**Owner: Zee.** Directories: `packs/`, `grounding/`, `web/`.

> **Your task list:** [`tasks.md`](tasks.md) — generated from `docs/team-tasks.csv`, so tick things off there and regenerate.
> **Everyone else:** [`team/`](../README.md) · **The rules every agent follows:** [`AGENTS.md`](../../AGENTS.md)

You do not need to know how to program to do this work. You need to know what a
document *is* and what is printed on it. That is the actual scarce skill here, and it
is why this lane is yours.

**Your lane runs first.** Nothing downstream can start until your field names are fixed,
because a field name you write becomes a column heading in Desmond's spreadsheet,
generated automatically. Section 3 of the pack guide explains why.

---

## Read this first

**[`packs/README.md`](../../packs/README.md)** is the full guide, written for you rather
than for a developer. It covers the field types, the rules, the persona and disclaimer,
grounding sources, and what "done" looks like for a pack. Everything below is the
shorter framing around it.

Then open [`packs/iras_tax/pack.yaml`](../../packs/iras_tax/pack.yaml). It will look
more approachable than you expect.

---

## The two halves of this lane

### Half one — domain packs (weeks 1 to 7)

A pack is one YAML file describing a kind of document and what is printed on it. Two are
already written as worked examples: **Tax and Reliefs** and **Insurance and Coverage**.
Your job is to make them right, and then to author the catalogue entries for the nine
packs we specify but do not build.

The mechanism that makes this lane matter:

```
packs/<pack>/pack.yaml   ──►  python -m packs.build  ──►  corpus/register/<pack>_columns.csv
   you write this                                              Desmond fills this in
                                    │
                                    ├──►  packs/<pack>/schemas.py      the extractor's constraint
                                    └──►  docs/field-dictionary.md     what everyone else reads
```

You write one file. Three are generated. A field name is written down in exactly one
place in this repository, which is what stops your pack and Desmond's corpus drifting
apart — a failure that otherwise surfaces as a silently zero evaluation score in week 8.

### Half two — the interface (weeks 4 to 8)

Four surfaces: **Today**, **Ask**, **Vault**, **Packs**. The design pack in
[`docs/artefacts/interface-design-pack.html`](../../docs/artefacts/interface-design-pack.html)
has the screens and user stories — open it in a browser.

Lock the design tokens before building any screen: one accent colour, one radius scale,
one type scale. An agent given tokens produces a consistent interface across sessions;
an agent given "make it look clean" produces four different ones.

---

## Your Claude Code skills

This repository ships skills that teach a Claude Code session how this project works.
Yours is **`/authoring-a-domain-pack`** — type it and it will walk you through a pack
step by step, stopping for your answer at each stage rather than running to the end.

The full starter prompt, if you would rather paste one in, is in
[`packs/README.md` §8](../../packs/README.md).

---

## Rules that apply to you specifically

1. **`pack.yaml` is the only file you author.** Never hand-edit `schemas.py`, the register
   CSV, or `docs/field-dictionary.md` — they are generated. Change the YAML, run
   `python -m packs.build`, commit both together.
2. **Do not rename a field after Desmond has started.** Free in week 1, expensive in
   week 6. Raise it in the group first.
3. **`must_cite`, `abstain_below` and `never_acts` are not yours to change.**
   `never_acts` is enforced by the type system — a pack that sets anything else will not
   load. The disclaimer and the persona *are* yours.
4. **Grounding sources must be official issuers.** IRAS, CPF Board, MAS, MOH, a named
   regulator. Not a blog, not a comparison site. Record the retrieval date; Siew reviews
   provenance with you.
5. **Stay inside `packs/`, `grounding/` and `web/`.** `CODEOWNERS` enforces it, so a PR
   that respects it merges without a fight.

---

## What "done" looks like

**For a pack:** 3–5 document types, 4–8 fields each, every field with a description that
says where the value appears on the paper and a realistic Singaporean example.
`python -m packs.build --check` passes. The generated register CSV reads sensibly to
somebody who has not seen the YAML. Siew has read the disclaimer. You have told Desmond
the columns are ready.

**For the interface:** the four surfaces work against real data from the corpus, empty
and error states included. A screen that only looks right with fixture data is not done.

---

## What you present

The interface and the two domain packs. Roughly five minutes of the final presentation.
The strongest thing you can show is the *same core* answering two completely different
domains because two YAML files were dropped in — that is the platform argument, and you
are the person who can demonstrate it.
