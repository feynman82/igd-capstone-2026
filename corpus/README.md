# The corpus

Owner: **Desmond** (Lane E). Nothing in here generates documents — documents are authored
with an AI tool and mail-merged. What lives here is the *ground truth* and the discipline
that keeps it usable.

## The order matters

Filling the register **before** generating documents is what turns the corpus into an
evaluation dataset instead of a pile of PDFs.

```
1. canon.md              one page: the facts every document must agree with
2. register/*.csv        one row per document, one column per field   ← GROUND TRUTH
3. templates/            one visual template per document type, with merge fields
4. mail merge            register + template → hundreds of documents, no code
5. field_pages           back into the register: which page each value landed on
6. print and photograph  a subset, on a phone, for the degraded tiers
7. batches/              the finished documents, named by register row id
```

**Start from the generated header.** `corpus/register/batch.template.csv` is written by
`python -m packs.build` from every installed `pack.yaml`, one column per field across all
packs. Copy it and fill rows underneath. Do not write a header by hand and do not merge the
per-pack files yourself — the column names and the field names drift the moment anybody
types one out.

The per-pack `<pack>_columns.csv` files are for reference: they show what one pack can
extract. A batch is a *household's* documents, so it mixes payslips and policy schedules in
one register with one row each, which is why the template spans both packs.

---

## Handing a batch over

```bash
cp corpus/register/batch.template.csv corpus/register/batch1.csv   # then fill it in
mkdir -p corpus/batches/batch1                                     # documents go here
uv run python -m corpus.validate corpus/register/batch1.csv        # must pass before pushing
git add corpus/register/batch1.csv corpus/batches/batch1 && git commit && git push
```

Four things that decide whether the batch is usable:

1. **The register is committed with the documents**, in the same push. A batch without its
   register is a pile of PDFs; the register is the part that makes it an evaluation dataset.
2. **`doc_id` is the filename.** `b1-0001` in the register is `b1-0001.pdf` in the batch
   folder. Anything else and nothing can join a fact back to the row it should match.
3. **Keep the guide lines.** The `#` block at the top of the template can stay exactly where
   it is — the validator skips it. Leaving it in means the next person reads the rules.
4. **Every `doc_type` must be one a pack declares.** The validator lists them. A document
   type no pack owns cannot be registered, and at ingestion it goes to quarantine rather
   than into `facts` — so it contributes no ground truth however good the document is.

The validator is the handover gate. If it passes, push; if it does not, nothing downstream
can use the batch, so there is no value in pushing it early.

**Step 5 is the one that cannot be done in order.** `field_pages` records which page each
value is *printed* on — `expiry_date=2;premium_payable=2`, and anything left out is page 1 —
and the page layout does not exist until the mail merge has run. So it is a second pass over
the register, after step 4 and before the batch is handed over. It is what lets a golden-set
question say which page its answer should be cited from, which is what makes Set A gradeable
without a person reading every answer.

Generate first and someone spends week 8 hand-labelling 400 documents. Fill the register
first and extraction F1 is a direct comparison, most of golden Set A is generated rather
than written, and the corpus is internally consistent by construction.

## Validate before handing over

```bash
uv run python -m corpus.validate register/batch1.csv
```

The validator is the contract between Lane E and the builders. It checks that every row has
a unique id, that dates are ordered sensibly, that every `policy_no` referenced more than
once carries identical values everywhere, that every `doc_type` is owned by an installed
pack, that every column is a field some pack declares, and that `field_pages` names only
fields the row actually fills. A batch that fails validation is not handed over.

## Two rules

1. **Invented organisations only.** Never produce a document bearing the name, logo or
   letterhead of a real insurer, bank or government agency. A realistic fake notice from a
   real institution is a fabricated official record whatever the intent, and it would make
   the corpus unpublishable alongside the report.

   **There is no footer requirement.** Every page used to have to carry a visible
   `SYNTHETIC DOCUMENT — NOT A REAL RECORD` stamp. That was dropped deliberately: the
   protection that matters is the invented issuer above — a document naming an insurer that
   does not exist is not a forgeable record of anything — and the stamp was costing more than
   it bought, landing on the last page only and overlapping the body text where it did land.
   Keep it where a template already prints it; nothing fails for its absence.
2. **State what synthetic data does not prove.** Generated documents are cleaner and more
   consistent than real ones. That is what the 40-document redacted holdout is for. Report
   both numbers and the gap.

## Tiers

| Tier | How | Share of the corpus |
|---|---|---|
| clean | mail merge → print to PDF | ~70% — arrives via the watched folder |
| scanned | print, then scan on a multi-function printer at 200–300 dpi | ~20% |
| photo | print, then photograph on a phone: angled, shadowed, imperfect | ~10% — arrives via Telegram |

Printing and photographing is more realistic than any simulation and needs no engineering.
