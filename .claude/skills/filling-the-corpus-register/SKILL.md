---
name: filling-the-corpus-register
description: Build a PARROT corpus batch register-first — fill the ground-truth spreadsheet before generating any synthetic document, then validate it. Use when starting a corpus batch, when corpus.validate fails, or when checking a batch before handover to evaluation.
---

# Filling the corpus register

The corpus is the input to every other lane. This skill covers the discipline that makes
it usable: **the answer key exists before the documents do.**

## Read first

`team/desmond/README.md`, `corpus/validate.py`, and `AGENTS.md`.

## The order, which is not the obvious one

The obvious approach is to generate four hundred documents and then work out what is in
them. Do not. That discards the labels and buys a week of hand-labelling in week 8.

```
1. Household canon      one page: the facts every document must agree with
2. Document register    one row per document, one column per field
                        ← THIS IS THE GROUND TRUTH
3. One template per type  made with an AI tool, with merge fields
4. Mail merge           register + template → hundreds of documents, no code
5. Print and photograph a subset, on a phone
```

Filling the register first gives, at no extra cost: extraction F1 measured directly
rather than by hand; most of golden Set A generated rather than written; internal
consistency the system can be caught failing on; and mass production without code.

## Column headings are not yours to choose

They are generated from the pack manifests into
`corpus/register/<pack_id>_columns.csv`. Open that file and the headings are already
there.

This is deliberate: an invented column called `period` against an extractor producing
`pay_period` scores zero silently, and the team spends three days hunting a spelling
difference. So the possibility was removed rather than documented.

**If a column heading does not make sense, that is a real signal** — the field
description upstream is unclear, and the extractor will struggle with it too. The fix is
a change to `packs/<pack>/pack.yaml`, not to the spreadsheet. Raise it; do not
work around it.

## Validate before handing over

```bash
python -m corpus.validate corpus/register/batch1.csv
```

It checks duplicate ids, expiry before start, non-positive money, columns no pack
declares, and the same identifier described inconsistently across two documents.

When it fails, **show the row numbers and the conflicting values — do not fix them.**
These are ground-truth labels; which value is correct is the author's decision, not
yours. Then say which failures look like spreadsheet mistakes and which look like a
problem with the field definitions upstream.

## Two rules that cannot bend

1. **Invented organisations only.** Never render a document bearing the name, logo or
   letterhead of a real insurer, bank or agency. A realistic fake notice from a real
   institution is a fabricated official record whatever the intent, and it would make the
   corpus unpublishable alongside the report. Invent the issuers. Every page carries a
   visible `SYNTHETIC DOCUMENT` footer.
2. **Never write code that generates corpus documents.** `AGENTS.md` rule: `corpus/`
   holds the register and its validator only. Documents are authored with an AI tool and
   mail merge, outside this repository's code.

## Batches

| Batch | What | When |
|---|---|---|
| 1 | ~120 tax documents | W1–W3 |
| 2 | ~120 insurance documents | W3–W5 |
| 3 | 30 phone-photographed + 30 scanned, from batches 1–2 | W5 |
| 4 | ~60 deliberately hard: faint scans, angled photos, overlapping stamps, two documents on one page | W6 |
| 5 | 40-document redacted holdout, real documents, under the consent protocol | W6–W7 |

Batch 4 is what makes the quarantine number interesting: the pipeline gives anything that
fails parsing a second pass through a vision-language model, and the recovery rate is a
reportable finding. Make batch 4 hard enough to produce it.

## The adversarial half, from week 7

Stop producing; start attacking. Look for a *finding*, not a bug report:

- **Contradiction** — two documents that disagree on a premium. Ask the question that
  spans them. Does it notice, pick one silently, or average them? Silently picking one is
  the finding.
- **Injection** — an instruction printed inside a document, then photographed. Does it
  survive parsing and reach the model?
- **Scope** — ask it to *act* rather than explain. `never_acts` is enforced in the
  manifest; verify it holds in practice and record how the refusal is worded.

Write each attempt up as: what was tried, what happened, what it means.

## Done, per batch

- [ ] Register filled before any document was generated
- [ ] `python -m corpus.validate` passes
- [ ] Every document has a `SYNTHETIC DOCUMENT` footer and an invented issuer
- [ ] Batch committed under `corpus/batches/` with a one-line note
- [ ] Evaluation lane told the batch is ready
