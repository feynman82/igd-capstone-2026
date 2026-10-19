# Consent and redaction protocol: the real-document holdout

Status: **approved 2026-10-19, by Christian on behalf of Siew** · Siew's decisions taken 2026-10-17: exclusions (§3) and deletion date (§8) · Owner: Siew, with Desmond (collection) · Reviewers: Desmond
(it must be workable), Christian (technical accuracy) · Evidence read on `main` at `eb9fc20`
(2026-10-17)

> **This protocol must be approved before a single real document is collected**
> (`team/siew/README.md`, artefact 2). Collection is Desmond's task "Collect and redact the
> holdout corpus", due 2026-10-20 (`docs/team-tasks.csv`). **Approved 2026-10-19**, so collection
> may begin.
>
> Every claim points at a file. Anything that could not be traced is marked **unverified**.
> Statements about the PDPA are marked **to confirm against the Act**. The environment this was
> drafted in cannot reach Singapore Statutes Online, so this draft does not quote the Act, the
> same as the other governance drafts.

## 1. What the holdout is, and why it needs this

The holdout is **40 real household documents, from team members, about themselves**, used once
to measure how far extraction on real paperwork falls short of extraction on the synthetic
corpus (`docs/team-tasks.csv`, "Collect and redact the holdout corpus"; `eval/holdout.py`).
*"The number that matters is not the holdout score but the gap"* (`eval/holdout.py`). It is
the evidence the synthetic corpus cannot give (`docs/governance/synthetic-data-case.md`).

It is the only place in this project where **the team itself collects real personal data**.
`data-inventory.md` §1 ("two capacities") places it inside the team's own work, where the
team is an organisation bound by the PDPA in full. That is not true of a household's own copy.
So it needs a lawful basis before collection, not after.

## 2. Rules at a glance

| # | Rule | Why |
|---|---|---|
| R1 | No document is collected until its contributor has signed the consent record (§4) | Consent before collection, not after (**to confirm against the Act**: Consent Obligation) |
| R2 | Only documents **about the contributor themselves**; no document mainly about anyone else | The task's own definition; it keeps every data subject a person who consented |
| R3 | Excluded outright: documents about a child, and medical letters or reports that state a diagnosis | Higher harm if exposed, and not needed to measure extraction (§3) |
| R4 | Redact before the document reaches any machine but the contributor's own (§5) | Only redacted copies ever exist in the project |
| R5 | Hand over **page images, not PDFs** | A redaction box drawn on a PDF can leave the text readable underneath (§5.3) |
| R6 | File names and ids are neutral codes: `H01.png` … `H40.png`, contributor `C1` … `C5` | The results file records each file name and is committed (§7) |
| R7 | The holdout lives **outside the repository**, in `~/holdout` on the integration machine only | `eval/holdout.py` refuses any folder inside the repository, and `corpus/holdout/README.md` names the integration machine |
| R8 | Nothing about a holdout document is committed except aggregate scores and coded ids | `.gitignore` (`corpus/holdout/`); `NOTICE.md` |
| R9 | Used once, for scoring, never for tuning; deleted on the date in §8 | Purpose limitation and retention (**to confirm against the Act**) |
| R10 | A contributor may withdraw at any time (§4.3) | **To confirm against the Act:** withdrawal of consent |

## 3. What may be contributed

**In:** a document issued to the contributor, about the contributor, of a type the corpus
already models, so that it can be scored against a register row. The 16 document types are in
`core/documents.yaml`, and the generated `docs/field-dictionary.md` lists their fields. Examples:
the contributor's own payslip, insurance policy schedule, renewal notice, donation receipt,
servicing invoice, loan agreement or notice of assessment.

**Out:**

| Excluded | Reason |
|---|---|
| A document mainly about another person (a parent's policy, a partner's payslip) | That person has not consented (R2). |
| Anything about a child | **Approved by Siew, 2026-10-17.** Children cannot give the consent this protocol relies on. Siew decided children for the system in `data-inventory.md` §6, 5b; for the holdout the answer is simply none. |
| Medical letters or reports stating a diagnosis | Health data carries the highest harm if exposed. The extraction gap can be measured without it. **Approved by Siew, 2026-10-17**; medical documents are measured on the synthetic corpus only. |
| Identity documents (NRIC, passport, birth certificate) | Almost every field on them is an identifier that §5 would redact, leaving nothing to score. It is also the data whose exposure does most harm. **Approved by Siew, 2026-10-17.** Its consistency with the PDPC's advisory guidelines on NRIC numbers is still to confirm. |
| A document the contributor cannot redact cleanly | When in doubt, leave it out (§5.4). |

**Spread.** The 40 should cover several document types, so that the gap is not a measure of one
template. `eval/holdout.py` scores by document type (`by_doc_type`), and a type with one or two
documents is a sample, not a finding (`eval/score.py`, `TypeScore`).

## 4. Consent

### 4.1 Who asks, and how

Desmond asks. Contribution is **voluntary**: no team member is required to contribute. The 40
may come from fewer than five people, and declining is not recorded anywhere. The request is
in writing (a message is enough) and links to the consent record below.

### 4.2 The consent record

One record per contributor. It lists the coded ids of the documents they gave, and is kept
**with the holdout, outside the repository**, never in git (it carries a name). The
contributor keeps a copy.

> **PARROT holdout: consent to use my documents**
>
> I, **[name]**, agree that the documents listed below, which are about me, may be used by the
> PARROT capstone team for one purpose only: **to measure how accurately PARROT reads real
> documents**, by comparing what it extracts with what is printed.
>
> I understand that:
> 1. I redact each document myself before handing it over, following the protocol, and the
>    team receives only redacted page images.
> 2. The documents stay on one machine, outside the project's code repository. They are never
>    uploaded, never shared outside the team, and never used to tune or train anything.
> 3. Only scores and coded ids (such as "H07") appear in the project's results. My name and
>    my documents' contents do not.
> 4. The documents and this record will be deleted by **31 December 2026**.
> 5. I may withdraw at any time by telling Desmond or Siew. My documents will then be deleted
>    within 72 hours. If they have already been scored, the published aggregate score cannot be
>    un-published, but nothing in it identifies me.
>
> Documents (coded ids): **H__, H__, H__ …**
>
> Signed: ____________ Date: ________

### 4.3 Withdrawal

On withdrawal:
1. Delete the contributor's documents and register rows within 72 hours, the same window as
   `retention-and-erasure.md` A4.
2. Record the withdrawal against the coded ids in the holdout log (§6), without the name.

If the holdout has already been scored, the committed aggregate stays. It holds no personal
data (§7). The contributor is told this before they consent (record, point 5).

## 5. Redaction

### 5.1 What to redact

Redact **everything that identifies a person**, with one exception: the values the evaluation
scores, where they identify no one.

| Redact (black out) | Keep |
|---|---|
| The contributor's name, NRIC/FIN, passport number, address, phone, email, signature | Dates (issue, expiry, renewal, payment), amounts, premiums, policy and plan names |
| **Every** other person's name and details: beneficiaries, family, an agent, a landlord, an employer's staff | Organisation names: an insurer, bank, employer or charity is not personal data (`data-inventory.md` §6, 5c) |
| Account, policy, facility and member numbers | The document's type and its layout |
| QR codes and barcodes, which can encode any of the above | — |
| Photographs of people | — |

**unverified.** Whether a policy or facility number is personal data on its own is not settled
here. It is redacted as a precaution, which means that field is never scored (§5.2).

### 5.2 What redaction does to the score

A redacted value cannot be extracted, and must not be counted as a miss. So the holdout
register records **only the values left visible**. Every redacted field is left blank in the
register. The scorer only scores fields the register fills (`eval/score.py`, `_outcomes`). A
row with nothing left to score is named in the results as `no_ground_truth` and excluded from
the denominator (`without_ground_truth`).

**Consequence, to state in the report.** The holdout measures extraction of dates, amounts and
names of products and organisations. It does not measure identifiers. That is a limit of the
holdout, not a defect.

### 5.3 How to redact: images, not PDFs

1. **Work from the original on the contributor's own machine.** Nothing unredacted is sent to
   anyone, uploaded, or opened on a shared machine.
2. **Turn each page into an image** (a screenshot or an export at a readable resolution), then
   black out the fields in §5.1 with **solid, opaque boxes** in an image editor.
3. **Hand over the images** (`H07-p1.png`, `H07-p2.png`, or one multi-page file). Never hand
   over the PDF.
4. **A contributor may choose to have an AI assistant redact their own documents.** It is their
   data and their choice, recorded in their consent record. It means the unredacted content is
   processed by that assistant's provider, so the contributor, not the team, makes that call, and
   only for their own documents. The checks in §5.4 still apply to what comes out.

Why images: a PDF often carries a text layer under the picture of the page. A box drawn over
it hides the text from the eye but not from a reader, and **Docling, which PARROT uses to
parse, reads that text layer** (`AGENTS.md`, stack). A flattened image has nothing underneath.
The trade-off is that every holdout document becomes image-only, so the holdout also exercises
OCR. That is the realistic case for photographed household paperwork, and the report should
say so.

### 5.4 Check before handover

The **contributor**, then **Desmond**, check each image:
- every item in §5.1 is covered, including small print, headers, footers and the back page;
- the box is opaque at full zoom;
- the file name is the coded id and nothing else (R6);
- the image's metadata carries no name. Screenshots can embed a device or user name; re-save
  without metadata if unsure.

If any check fails and cannot be fixed, the document is left out.

## 6. Storage, access and the register

| | Rule | Evidence |
|---|---|---|
| **Where** | `~/holdout` on the integration machine (Christian's workstation), **outside the repository**. | `corpus/holdout/README.md` (integration machine); `eval/holdout.py` (`check_outside_the_repository`) |
| **Never** | In `inbox/`, which is watched and committed; in `corpus/`; on a shared drive; in chat or email attachments after handover. | `.gitignore` (`inbox/` is committed); `eval/holdout.py` docstring |
| **Who** | Desmond (collects and registers) and whoever runs `eval.holdout` (Yew Mun). No one else needs to open the files. | `docs/team-tasks.csv` |
| **Register** | `register.csv`, beside the documents and outside the repository. Built from the generated template (`corpus/register/batch.template.csv`); `doc_id` = the coded id; only visible values filled (§5.2). | `eval/holdout.py` (`--register`); `eval/sets_io.py` (`read_register`) |
| **Holdout log** | A short note **in the same folder**: coded ids, document type, contributor code (`C1`…), date received, withdrawn or deleted. Names live only in the consent records. | — |

### A contradiction in the repository — resolved 2026-10-19

`.gitignore` says a real document *"goes to corpus/holdout/"*, and `NOTICE.md` describes that
folder as where the holdout is kept. But `eval/holdout.py` refuses any holdout folder **inside
the repository**: *"The holdout must live outside it: the watcher reads … inbox, and a document
the development vault has seen is no longer a holdout."* `corpus/holdout/` is inside the
repository, so this protocol follows the code (R7). The `.gitignore` comment, `NOTICE.md` and
`corpus/holdout/README.md` should be brought into line (Christian, Desmond). The gitignore rule
itself should stay as a second lock.

**Resolved 2026-10-19:** `.gitignore` and `NOTICE.md` now say the holdout lives in `~/holdout`,
outside the repository, and `temp/` is ignored too. `corpus/holdout/README.md` is still to be
brought into line.

## 7. The run, and what may be committed

`eval/holdout.py` scores the holdout in a **separate database** (`parrot_holdout`). It
ingests each document directly and never through `inbox/`, and drops the database at the end
unless `--keep` is given. Generation and parsing run locally: every model endpoint must be
loopback (`core/runtime/settings.py`, `local_url`).

**What it writes, and whether it may be committed:**

| Output | Contents | Commit? |
|---|---|---|
| `eval/results/<date>-holdout.json` (`eval/holdout.py`) | Counts, F1 by document type, `no_ground_truth` document ids, and **each document's file name** | **Yes**, *if and only if* R6 was followed. Then it holds coded ids and scores, and no personal data. Check the file before committing. |
| Any `eval.run` results on the holdout vault (retrieval and generation questions, `eval/holdout.py` docstring) | **Each answer's full text** and its cited passages (`eval/score.py`, `as_dict`: `"answer"`, `"contexts"`) | **No.** Write them outside the repository (`--out`), and commit only a table of aggregate scores, typed by hand. |
| The `parrot_holdout` database, when kept with `--keep` | Every extracted fact | Drop it as soon as the run is checked. |

## 8. Retention and deletion

**Decided by Siew, 2026-10-17:** delete the documents, the register, the holdout log and the
consent records **by 31 December 2026, the end of the MVP** (Siew, 2026-10-17). The holdout is
kept for as long as the MVP it measures, and no longer. That is after the final report, whose
governance chapter is due 2026-11-10 (W10, `docs/team-tasks.csv`). Desmond deletes; Siew
confirms in writing. The
committed aggregate results stay, since they hold no personal data (§7).

This fills the row that `retention-and-erasure.md` left open: *"The 40-document real holdout
(team members) | — | Governed by `consent-and-redaction.md`, which does not exist yet."*

## 9. If something goes wrong

A holdout document leaving the integration machine, or being committed, is an incident
(`incident-and-breach-procedure.md` §1, "Holdout exposure"). It is notifiable to the course
supervisors in every case, and possibly a notifiable breach (§3 of that procedure). **Committing
one cannot be undone by deleting it: git keeps it** (`.gitignore`; `NOTICE.md`). Follow the
containment step for "Data published to GitHub" in the incident procedure.

## 10. PDPA obligations this protocol answers

**To confirm against the Act.** These are the obligations as commonly named. Each must be
checked, with section numbers, against the Act on Singapore Statutes Online before the chapter
cites them.

| Obligation | Where this protocol answers it |
|---|---|
| Consent | §4: written, before collection, one record per contributor |
| Notification of purpose | §4.2: one stated purpose, in the record itself |
| Purpose limitation | R9; §7: scored once, never tuned on |
| Withdrawal of consent | §4.3 |
| Protection | R4–R8; §§5–6: redaction, one machine, outside git |
| Retention limitation | §8 |
| Data breach notification | §9, via `incident-and-breach-procedure.md` |

## Open questions

1. ~~**Siew:** approve the exclusions in §3 (children, diagnoses, identity documents).~~ **Approved
   2026-10-17, all three as drafted.**
2. ~~**Siew:** decide the deletion date in §8.~~ **Decided 2026-10-17: by 31 December 2026.**
3. **Desmond:** is images-not-PDFs (§5.3) workable for each contributor, and is the 2026-10-20
   collection date still realistic with consent first?
4. ~~**Christian:** which machine is the integration machine, and confirm that `eval.holdout`
   will be run there with `--documents` outside the repository.~~ **Answered 2026-10-19:**
   Christian's workstation, `--documents ~/holdout`. `.gitignore` and `NOTICE.md` are in line;
   `corpus/holdout/README.md` is not yet (§6).
5. **Yew Mun:** if retrieval questions are run on the holdout, their results file holds answer
   text (§7). Agree that it is written outside the repository.
6. **unverified:** whether a policy or account number alone is personal data (§5.1). Redacting
   it is the safe default either way.
