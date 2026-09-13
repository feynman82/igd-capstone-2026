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

We do not render documents bearing the name, logo or letterhead of a real insurer, bank or
government agency. A realistic-looking fake notice from a real institution is a fabricated
official record regardless of the intent behind it, and it would also make the corpus
unpublishable alongside the report. All organisations in the corpus are invented.

A visible `SYNTHETIC DOCUMENT — NOT A REAL RECORD` footer on every page was part of this
control and has been withdrawn. The reasoning: the invented issuer is what makes a document
unusable as a record of anything, and it is verifiable by inspection, whereas the footer was
not being produced reliably — generators placed it on the final page only, and where it was
placed it overlapped the body text. A control that is asserted but not met is worse than one
that is not claimed. **This is a change to a stated control and needs Siew's review**, since
the case below rests on it.

## What synthetic data does not prove

Generated documents are cleaner, more consistent and more predictable than real ones. A
score measured only on them overstates the system. The `holdout` corpus is 40 genuine
documents contributed by team members about themselves, redacted of third-party data, used
once at the final evaluation and never for tuning. The report states both numbers and the
gap between them; that gap is a finding, not a defect.
