# §4 · Implementation

> **Draft.** Written from the repository for Christian to rewrite in their own words.

---

## 4.1 What was built, and what was not

Built: capture through a watched folder and a Telegram bot, the document pipeline, hybrid retrieval
with reranking, the grounding gate, three modules, two packs, the interface and an evaluation
harness. Advice, Calendar and Household were added after the proposal.

The boundary needs stating, because a demonstration will expose it:

- Tracker and nine packs are specified, not built.
- WhatsApp capture, Google Drive sync and calendar sync are not built (ADR 0020).
- The chunk prefix is deterministic (title, type, heading, page), not the model-written description
  proposed.
- Agent state sits in memory, not PostgreSQL, until a reviewed migration creates its tables
  (ADR 0007).
- Alert runs as a nightly sweep, not on each fact write (ADR 0008).
- The check of a value against its printed label is built, measured and switched off, pending
  review (ADR 0021).

The tax pack's sources carry review dates, but its advice is not live-verified. Whether its rule
values are approved is held in each machine's database, not in the repository.

## 4.2 The document pipeline

The pipeline has one rule: a document is either fully read or visibly not read (Figure 3).

Capture computes a SHA-256 of the file's bytes and commits a document row, so a file arriving under
two names is not read twice. A Redis message then hands the work to a Celery worker
(ADR 0008).

Docling parses each page and keeps its number, because a citation needs one. A PDF with no text layer
is read with full-page OCR. The generator classifies the document against the catalogue's 16 types,
constrained to that list plus `unknown`. Extraction runs under a schema applied during decoding, so
the model cannot return an undeclared field. Every value must then be found on a page; one found on
none is dropped, as produced rather than read.

Only then is the document chunked and embedded. Chunks follow headings, and a page boundary always
ends one (ADR 0012). Chunks, facts and obligations commit in one transaction, so a reminder cannot
disagree with a search result.

Anything that fails goes to quarantine with a reason: a parser failure, under 40 characters a page,
an unrecognised type, classifier confidence under 0.45, or a failed extraction. Quarantine has two
stages. A person can send a document back, and the generator transcribes up to four page images,
which then face the same classification and extraction. The weakness is known: on this path the page
is the model's own transcription, so placing a value on it checks the model against itself. A misread
name has been stored as a cited fact this way.

![**Figure 3.** Extraction is judged before anything is embedded, then both lanes commit together, so a document is never half-read.](figures/figure-3-pipeline.png|0.72)

## 4.3 Domain packs as an enforced contract

The rules that matter are enforced by code, because a convention among five people is easily broken.

The corpus is scored by comparing extracted values with a spreadsheet whose columns are field names.
Had a column been `period` while the extractor wrote `pay_period`, extraction would have scored zero
and looked like a model failure. So every field is written once, in `core/documents.yaml`.
`python -m packs.build` generates the extraction models, the register columns and the field
dictionary from it, and `--check` fails CI when an output differs.

The contract holds three more. `never_acts` and `verdict_by_code` are `Literal[True]`, so a pack
that sets anything else does not load. A pack naming a type or field the core does not declare stops
at load. Advice names a calculator from a closed list,
which is why the tax pack explains donations and CPF top-ups but does not calculate them.

A source with no review date, or past its `review_by` date, is excluded in SQL.

A reader can point at each of these in code.

## 4.4 The interface

The proposal named four surfaces. The interface has five, Today, Calendar (ADR 0020), Ask, Vault and
Packs, plus a Household page reached from the header, which records the people the documents name
(ADR 0011). Capture is deliberately absent: filing happens in the folder or in Telegram.

Three decisions carry the thesis onto the screen. A citation is a page, not a footnote: a source
chip names the document and page, and pressing it opens that page with the claim still on screen.
What could not be read is a job, not an error: the Vault opens with "Needs your eyes", listing each
quarantined document with its reason and a retry. An abstention is a designed state, in brass rather
than red: it names why PARROT declined and what would have answered.

![**Figure 4.** A cited answer on the Ask surface, from the synthetic corpus. Each sentence carries its own source chip.](figures/figure-4-ask.jpg|0.44)

Whether any of this works as intended is unknown. The interface has not been usability-tested with
anyone outside the team, so this section describes a design, not its effect on users.

## 4.5 How the team worked

Five people, three of them building, worked with coding agents on one repository. Ownership was by
directory, written in `CODEOWNERS`. Changes to contracts and the database schema were kept in their
own pull requests, every agent read one `AGENTS.md`, and generated files held each field list in one
place. One limit matters: GitHub could not enforce review on this private repository, so `CODEOWNERS`
requests a reviewer but cannot block a merge. ADR 0010 names convention and a weekly integration pass
as what replaces it.
