# Terms of use

> **Status: draft. One clause so far. Not yet presented to anyone, and not yet accepted.**
> Owner: Siew. Started 2026-10-01.
>
> These terms are the contractual basis for decision 5a in `data-inventory.md` §6: one adult
> filing another adult's document. Clause A is Siew's text, reproduced **verbatim**. Do not
> edit its wording without her. Notes about the clause sit outside it, under "Status against
> the code".

---

## Definitions

**System Developer** refers to the PARROT team. *(The team's members are listed in
`team/README.md`.)* The System Developer is the party that designs, builds, tests and maintains
the system so that it meets what users need. Their main tasks are:

- Gathering requirements: working with stakeholders to learn what the system must do
  (functional requirements) and how well it must do it (non-functional requirements).
- Analysis and design: planning the architecture, data structures, interfaces and workflows,
  often using diagrams such as UML or flowcharts.
- Building: writing code and connecting the parts together.
- Testing: checking that the system works correctly and meets the requirements through unit,
  integration and user acceptance testing.
- Deployment: releasing the system to users and setting up its environment.
- Documentation: writing technical documents and user guides.
- Maintenance: fixing bugs, making improvements and adapting the system as needs change.
- Communication: working with designers, clients, testers and other developers throughout the
  project.

**System**: *not yet defined.*

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

## Status against the code

These notes are not part of the terms. Each one is something the code does today, or does not
do yet, that the clause relies on.

| What the clause relies on | State today | Evidence | Whose |
|---|---|---|---|
| A screen that presents these terms before anything is submitted | **Missing.** Neither the unlock screen nor household setup shows any terms. | `web/app/unlock/`, `web/app/(app)/household/` | Zee (`web/`) |
| A record of acceptance: who accepted, which version, and when | **Missing.** No table holds it. `advice_consents` records advice consent by version and wording hash, and could be the model. A new table needs a migration (AGENTS.md rule 4). | `db/migrations/0003_advice.sql` | Christian |
| Knowing who the Submitting Party was for a given document | **Partly.** Telegram from a mapped chat is recorded. Folder capture is not. | `data-inventory.md` §1, "Lawful basis"; gap 7 | Christian |
| A minor is never a Represented Party under this clause | **Policy, not code.** The clause speaks of adults. A child's document is filed by a parent under decision 5b. Nothing stops an adult's filing being recorded against a person with `relation = 'child'`, or the reverse. | `data-inventory.md` §6, 5b | — |

## Not yet written

These terms need more than Clause A:
- **Definitions.** "System Developer" was defined by Siew on 2026-10-01 (above). "System" is
  not yet defined. Siew decided on 2026-10-01 that the System Developer is the PARROT team.
  One point is still open:
  - The definition includes "deployment" and "setting up its environment". On a copy that
     runs on a household's own computer, the household runs the installer
     (`FIRST-RUN.md`, `START.cmd`). Does that make the household its own deployer for these
     terms?
  The data inventory supports clauses 6 and 7. At inference and at rest, household data stays
  on the household's own computer (`data-inventory.md` §3), so the System Developer never
  receives it.
- The purpose statement (§6 question 5d).
- Retention and erasure (from `retention-and-erasure.md` when it exists).
- The advise-only boundary (`never_acts`, `core/contracts.py`).
- Governing law.

## For review

**Legal review** is needed before the report relies on clauses 2, 4, 5 and 7. The specific
questions are listed in `data-inventory.md` §6, 5a, point 3. Clauses 1 and 8 already answer
part of them. Clause 1 makes the Submitting Party warrant their authority, and clause 8
preserves rights the law does not allow to be excluded.
