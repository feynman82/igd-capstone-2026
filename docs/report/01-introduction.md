# §1 · Introduction: the problem and the argument

> **Draft.** Written from the repository for Christian to rewrite in their own words.

---

## 1.1 The problem

Daniel and Rachel both work demanding jobs and have no help at home. Their motor cover lapses, and
they find out at the worst moment. Marcus supports ageing parents and cannot recall which policy
covered their father's last admission. Priya misses a Supplementary Retirement Scheme top-up window,
and the relief that came with it.

These are personas from our proposal, not surveyed households, but they share one problem. Insurance
schedules, CPF statements, road tax notices and school circulars sit across drawers, inboxes and
phone galleries. Calendar apps hold the dates without the documents. Note apps hold the documents
but cannot reason across them. The cost is not untidiness. It is the missed renewal, the forfeited
relief, and an administrative load that falls hardest on working parents and caregivers.

## 1.2 Why a general-purpose assistant does not solve it

The obvious objection is that a household could upload these papers to a commercial assistant. Three
reasons say otherwise, and the design answers each.

The first is custody. These are the most sensitive records a household holds, and uploading them
places them on infrastructure it does not control. A household that withholds its CPF statement gets
an assistant that cannot help with tax.

The second is scope. A household cannot hold a general assistant to answering only from its own
documents.

The third is restraint. Such an assistant is built to answer, and declining is hard even by design:
our own system, built to decline, still made an unsupported claim on 21 of 118 questions (§5.3).

None of the three is a shortfall in model capability (§1.3).

## 1.3 Thesis

> The binding constraint on household AI adoption is not model capability but warranted trust, and
> warranted trust is produced by architecture rather than by accuracy.

By warranted trust we mean trust a person can check. The documents stay on the owner's hardware,
each claim names its page, calculations are done in code, and the system can decline. These are
properties of how it is built, not of how well its model performs.

A competent reader can disagree in three ways. Accuracy may dominate trust in practice. Declining
may be a worse experience than a hedged answer. Local deployment may give up more capability than
users value. This report argues against the first. The second and third stay open, because no
household has yet lived with the system (§8).

## 1.4 Scope, and what success means

The ten-week build covers the document core, two capture routes, two domain packs, three capability
modules and an evaluation harness. A module that pays, books or files is excluded on purpose,
because acting changes the governance case completely. WhatsApp capture, Google Drive sync, the
Tracker module and a mobile build are deferred.

Nine metrics were fixed in week 1, before any had a value.

| Metric | Component | Line |
|---|---|---|
| Context recall | RAG core | ≥ 0.85 |
| Context precision | RAG core | ≥ 0.70 |
| Faithfulness | RAG core | ≥ 0.90 |
| Answer relevancy | RAG core | ≥ 0.80 |
| Abstention rate (Set B) | Grounding gate | ≥ 0.95 |
| Field extraction F1 | Extraction | ≥ 0.90 |
| Obligation precision | Reminder module | ≥ 0.95 |
| Alert false-positive rate | Alert module | ≤ 0.05 |
| Decode throughput and peak VRAM | Runtime | Measured and reported |

In mid-October the evaluation was found rewarding the wrong things (§5.1). This report therefore
leads with five numbers, one per aim, scored by code: right and cited, unsupported claims,
over-caution, the casual-phrasing gap and extraction F1. Those five are proposed and await the
supervisor's sign-off. Until then the nine lines stand as the reference. One line is absolute: no
forbidden string on the adversarial set.

## 1.5 How this report is organised

This report follows the Design Science Research sequence (Peffers et al., 2007). Sections 1 and 2
identify the problem, and §1.4 sets the objectives of a solution. Sections 3 and 4 cover design and
development, and the prototype is the demonstration. Section 5 evaluates it. Sections 6 to 8 take up
governance, value and limits, as the brief requires. Section 9 returns to the thesis. The report
itself is the communication step.
