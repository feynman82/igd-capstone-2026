# Terms of use

> **Status: draft. One clause so far. Not yet presented to anyone, and not yet accepted.**
> Owner: Siew. Started 2026-10-01.
>
> These terms are the contractual basis for two decisions in `data-inventory.md` §6: 5a (one
> adult filing another adult's document) and 5d (purpose). Clause A is Siew's text, reproduced
> **verbatim**. Do not edit its wording without Siew. Clause B was drafted for Siew to approve.
> Notes about the clauses sit outside them, under "Status against the code".

---

## Definitions

- **System** refers to PARROT.
- **System Developer** refers to the PARROT team, the party that designs, builds, tests and
  maintains the System.
- **System Deployer** refers to the PARROT team, the party that releases the System to users
  and sets up its environment.

---

## Clause A. Authority and Consent for Submissions on Behalf of Another Adult

1. **Authority to Act.** Where an adult (“Submitting Party”) completes, signs, submits, or
   otherwise provides any document, form, declaration, information or instruction through the
   System on behalf of another adult (“Represented Party”), the Submitting Party represents and
   warrants that they have obtained all necessary authority, consent and authorisation from the
   Represented Party to do so.

2. **Deemed Authorisation.** To the fullest extent permitted by applicable law, any document,
   information, declaration, consent or instruction submitted by the Submitting Party on behalf
   of the Represented Party shall be deemed to have been submitted with the Represented Party’s
   authority and consent. The System Developer may rely on such submission without
   independently verifying the identity, authority or consent of the Submitting Party or
   Represented Party, unless otherwise required by law.

3. **Responsibility for Accuracy.** The Submitting Party shall be responsible for ensuring that
   all information, declarations, consents and documents submitted on behalf of the Represented
   Party are complete, accurate and duly authorised. The System Developer shall not be
   responsible for verifying the accuracy, completeness or validity of information or documents
   supplied by the Submitting Party.

4. **Disputes Between Parties.** Any dispute between the Submitting Party and the Represented
   Party concerning the authority to act, the existence or scope of consent, the accuracy of
   information submitted, or the validity of any document or transaction shall be a matter
   between those parties. To the fullest extent permitted by applicable law, the System
   Developer shall have no liability arising from or in connection with such dispute.

5. **Indemnity.** The Submitting Party shall indemnify and hold harmless the System Developer,
   its officers, employees, agents and contractors from and against any claims, losses,
   liabilities, damages, costs and expenses (including reasonable legal costs) arising out of
   or in connection with:
   - (a) any unauthorised or purportedly authorised submission made on behalf of the
     Represented Party;
   - (b) any dispute between the Submitting Party and Represented Party concerning such
     submission;
   - (c) any inaccurate, incomplete or misleading information provided by the Submitting
     Party; or
   - (d) any breach by the Submitting Party of this clause.

6. **No Independent Verification.** The Submitting Party acknowledges that the System
   Developer is entitled to rely on the information, representations and authorisations
   provided through the System and is not required to independently investigate or verify the
   relationship, authority or consent between the parties, except where such verification is
   expressly required under applicable law or agreed contractual requirements.

7. **Limitation of Liability.** To the fullest extent permitted by applicable law, the System
   Developer shall not be liable for any direct, indirect, incidental, consequential or special
   loss, damage, cost or expense arising from or relating to any dispute, representation,
   submission or transaction between the Submitting Party and the Represented Party, including
   any dispute concerning whether the Represented Party authorised or consented to the
   submission.

8. **Mandatory Rights Preserved.** Nothing in this clause shall exclude or limit any liability,
   obligation or right that cannot lawfully be excluded or limited under applicable law.

---

## Clause B. Purpose

> *Drafted at Siew's request on 2026-10-01 (decision 5d: one purpose statement that names all
> four uses). The wording is for Siew to approve.*

1. **Purpose.** The System holds the documents and information you submit, and the personal
   data in them, for one purpose: to help your household understand and keep track of its own
   documents. It does this in four ways:
   - (a) **Answering**: answering questions you ask about your documents, citing the page each
     answer comes from;
   - (b) **Reminders**: reminding you, without being asked, of dates your documents contain,
     such as a renewal or a payment due date;
   - (c) **Alerts**: alerting you, without being asked, when a figure in your documents nears
     a limit, such as tax relief used against its cap; and
   - (d) **Advice**: calculating and explaining advice, such as a gap in insurance cover,
     **only** for a person who has separately given and not withdrawn their consent to
     advice.
2. **Advises, never acts.** The System does not pay, book, renew, file or otherwise act on your
   behalf. It informs and advises only.
3. **No other purpose.** The System does not use your documents or information for any purpose
   not listed in paragraph 1.

---

## Status against the code

These notes are not part of the terms. Each one is something the code does today, or does not
do yet, that the clause relies on.

| What the clause relies on | State today | Evidence | Whose |
|---|---|---|---|
| A screen that presents these terms before anything is submitted | **Missing.** Neither the unlock screen nor household setup shows any terms. | `web/app/unlock/`, `web/app/(app)/household/` | Zee (`web/`) |
| A record of acceptance: who accepted, which version, and when | **Missing.** No table holds it. `advice_consents` records advice consent by version and wording hash, and could be the model. A new table needs a migration (AGENTS.md rule 4). | `db/migrations/0003_advice.sql` | Christian |
| Knowing who the Submitting Party was for a given document | **Partly.** Telegram from a mapped chat is recorded. Folder capture is not. | `data-inventory.md` §1, "Lawful basis"; gap 7 | Christian |
| Clause B (a) Answering cites a page | **Enforced.** A fact without a document and a page cannot be written, and the answer gate drops a factual sentence with no supporting chunk. | `db/migrations/0001_init.sql` (`facts.document_id`, `facts.page` `NOT NULL`); `core/graph/answer.py` | — |
| Clause B (b) Reminders | **Built.** Runs daily at 07:00 and shows on Today. | `modules/reminder/module.yaml` (`cron: "0 7 * * *"`, `surfaces: [today, notification]`) | — |
| Clause B (c) Alerts | **Built, as a nightly sweep.** The trigger on a new document (`fact_write`) is not built yet. Repeats are held back for 168 hours. | `modules/alert/module.yaml`; `core/worker/schedule.py` docstring; ADR 0008 | — |
| Clause B (b), (c) "without being asked": how a notification reaches the person beyond the Today screen | **`unverified`.** `grep` finds no delivery code for the `notification` surface. | `core/contracts.py` (`surfaces`) | Christian |
| Clause B (d) Advice only under consent | **Enforced.** Consent is checked in the same transaction as the advice record. | `core/advice_consent.py`; `core/advice_records.py`; ADR 0016 | — |
| Clause B 2: never acts | **Enforced by type.** A pack that sets anything else will not load. | `core/contracts.py` (`never_acts: Literal[True]`) | — |
| Clause B 3: no other purpose | **Policy.** Nothing in the code uses documents for anything outside (a) to (d). This should be re-checked whenever a module is added. | `modules/` (reminder, alert, advice); `core/graph/` | — |
| A minor is never a Represented Party under this clause | **Policy, not code.** The clause speaks of adults. A child's document is filed by a parent under decision 5b. Nothing stops an adult's filing being recorded against a person with `relation = 'child'`, or the reverse. | `data-inventory.md` §6, 5b | — |

## Not yet written

These terms need more than Clauses A and B:
- **Definitions.** Siew defined "System", "System Developer" and "System Deployer" on
  2026-10-01. On 2026-10-02 they were cut back to one line each, at Siew's request. A note against the code:
  today the household runs the installer itself (`FIRST-RUN.md`, `START.cmd`). The terms
  should say whether the team sets up each household's copy or supplies the installer that
  does, so this definition matches what actually happens.
  The data inventory supports clauses 6 and 7. At inference and at rest, household data stays
  on the household's own computer (`data-inventory.md` §3), so the System Developer never
  receives it.
- Retention and erasure (from `retention-and-erasure.md` when it exists).
- The advise-only boundary (`never_acts`, `core/contracts.py`).
- Governing law.

## For review

**Legal review** is needed before the report relies on clauses 2, 4, 5 and 7. The specific
questions are listed in `data-inventory.md` §6, 5a, point 3. Clauses 1 and 8 already answer
part of them. Clause 1 makes the Submitting Party warrant their authority, and clause 8
preserves rights the law does not allow to be excluded.
