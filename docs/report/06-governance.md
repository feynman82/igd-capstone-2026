# §6 · Governance, ethics and risk

> **Draft.** Written from the repository for Siew to rewrite in their own words.

---

## 6.1 Personal data and the PDPA position

The data inventory, still a draft, separates two capacities. A household using its own copy acts in
a personal or domestic capacity, which the Personal Data Protection Act 2012 excludes from its Data
Protection Provisions (Personal Data Protection Commission, 2026). The team is bound in full for
its repository, holdout and demonstration machine. PARROT aims at the Act's standards by choice:
deemed consent under section 15, and explicit, recorded consent before advice (ADR 0016).

At inference and at rest, nothing leaves the machine. Non-loopback model, database and queue
addresses are refused. Model weights arrive on first use. With Telegram on, two things cross:
captured documents and the morning digest. PARROT encrypts nothing; its lock guards a screen.

Erasure is the gap. The policy promises deletion on instruction within 72 hours. Only a quarantined
document can be deleted, leaving the file and copies behind. Saved conversations (migration
0005) appear in neither inventory nor policy.

## 6.2 Life cycle: ISO/IEC 22989 stages and ISO/IEC 5338 processes

Two standards do two jobs. ISO/IEC 22989 names the stages. ISO/IEC 5338 supplies the processes and
"does not prescribe a specific life cycle" (International Organization for Standardization &
International Electrotechnical Commission [ISO/IEC], 2023, p. 4); its stage figure is an example
based on 22989 (ISO/IEC, 2022). The team's map, a draft, keeps them apart.

| 22989 stage | 5338 process | In PARROT |
|---|---|---|
| Design and development | Knowledge acquisition (6.4.7) | Sources dated, signed off before citing |
| Verification and validation | AI data engineering (6.4.8) | Register written before each document |
| Continuous validation | Continuous validation (6.4.14) | Partly: no trigger after a model change |
| Re-evaluation | Validation | Holdout at 14 of 40, not run |
| Retirement | Disposal (6.4.17) | Designed, mostly not built |

The map shows alignment; it is not a certification, and these names were checked against the free
preview of 5338, not the full standards. The last three rows show what a prototype leaves
unfinished.

## 6.3 IMDA frameworks

Each of the nine dimensions of the generative AI framework (Infocomm Media Development Authority
[IMDA] & AI Verify Foundation, 2024) is answered with an artefact, a result or a named gap. Content
provenance is strongest. Testing and assurance is weakest: the framework stresses third-party
testing, and every result here is the team's own, on synthetic data.

The agentic framework, version 1.5 (IMDA, 2026), applies although PARROT takes no outside action,
because it routes, retrieves and runs scheduled jobs. Its advice to "bound by design" (p. 19) fits
PARROT's types. The mapping also names gaps: no screen says answers are AI-generated, the terms
have been presented to nobody, and the incident procedure, approved by Siew on 17 October, is
unexercised.

Both mappings are the team's own reading, awaiting technical review.

## 6.4 The autonomy boundary

Version one advises. It does not pay, book or file. Every pack manifest carries
`never_acts: Literal[True]`, so a pack that sets anything else does not load, and a test asserts it.

That line is a declaration, not a switch: nothing at runtime branches on it. What stops action is
structure. `PrimitiveId` admits no action module, and the answer path has no tools. The
router that refuses requests to act is a model's judgement, so it makes the boundary polite, not
safe. Set C's three requests to act were refused on every reading to 19 October. Siew accepted the
residual risks on 17 October, bar one (§6.5).

## 6.5 Risk register

The incident log is empty, so these five come from evaluation and design records.

| Risk | Early signal | What was done |
|---|---|---|
| Evaluation rewards wrong answers | Scorer passed 7 of 10 casual questions; a person, 4 | Register-scored headline proposed, not agreed |
| Another person's data answered | Set C leaked twice, 19 October | Scoping fixed; no leak since |
| Real document reaches GitHub | `.gitignore` and holdout script disagreed on location | Holdout outside repository; `inbox/` still tracked |
| Real-document evidence short | Protocol approved 19 October, collection due next day | 14 of 40 collected, not run |
| Strangers reach the inbox | Empty Telegram allow list accepts any chat | Siew judged it not tolerable as a default, 17 October; still open |
