# Why the prototype is evaluated on synthetic data

Status: draft · Owner: Siew with Desmond

## The decision

The demonstration corpus is generated, not collected. No real payslip, policy schedule or
medical letter belonging to a team member or a third party is ingested during development.

## Why

1. **PDPA.** Household documents contain personal data about people who are not on this team
   — spouses, children, elderly parents. Collecting it for a student project would require
   consent we cannot meaningfully obtain from a child, and a retention story we cannot honour
   after the module ends.
2. **Ground truth for free.** Each document is rendered *from* its field values, so the
   correct answer for every extractable field exists before the document does. Extraction F1
   is measured directly rather than by hand-labelling.
3. **Coverage on demand.** Eight years of a household's paperwork, including the rare
   documents (a claim settlement, a lapsed policy, a duplicate renewal) that make retrieval
   interesting, can be produced in minutes.
4. **Reproducibility.** A seed and a generator commit hash reproduce the corpus exactly, so
   an evaluation result is re-runnable by an examiner.

## What we do not do

We do not ingest a real person's document. The people, addresses, policy numbers and figures
on every document come from the household canon.

Two controls that used to sit here have been withdrawn. **Invented organisations only** was
withdrawn on 13 September 2026 at the integration lead's direction: full-length policies name
hospitals, schemes and dispute bodies, and forbidding them made the corpus a weaker test of
retrieval than the documents a household actually holds. A visible
`SYNTHETIC DOCUMENT — NOT A REAL RECORD` footer on every page was withdrawn earlier, because
generators placed it on the final page only and overlapped the body text where it did land.

What follows for publication: a corpus document that names a real insurer is not publishable
as-is alongside the report, so anything published is reviewed for that first. **This is a
change to a stated control and needs Siew's review**, since the case below rests on it.

## What synthetic data does not prove

Generated documents are cleaner, more consistent and more predictable than real ones. A
score measured only on them overstates the system. The `holdout` corpus is 40 genuine
documents contributed by team members about themselves, redacted of third-party data, used
once at the final evaluation and never for tuning. The report states both numbers and the
gap between them; that gap is a finding, not a defect.
