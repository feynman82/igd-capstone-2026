# Artefacts

Everything produced before the repository existed, committed so that every agent session
and every team member is reading the same version.

## Current deliverables

| File | What | Status |
|---|---|---|
| `PARROT_Revised_Proposal_v3.docx` | The revised proposal, 19 pages, 13 sections plus references | **Current.** Supersedes `source-material/00-original-proposal.docx` |
| `PARROT_Proposal_Deck.pptx` | 15-slide proposal deck | **Current** |
| `architecture-review.html` | The full architecture review — expansion model, VRAM budget, pipeline, pack manifest, grounding, golden sets, governance mapping, risk register, sources | **Current.** Open in a browser |
| `interface-design-pack.html` | Interface design pack — the four surfaces, user stories, component inventory | **Current.** Open in a browser |
| `team-split-narrative.md` | The reasoning behind the five-lane split | Reference; `docs/TEAM.md` is the working version |
| `diagrams/` | 13 rendered figures used in the proposal and deck | Regenerated from the review HTML |

## Source material

`source-material/` holds what we started from. Kept for provenance — the report has to be
able to say what changed and why.

| File | Origin |
|---|---|
| `00-original-proposal.docx` | The original proposal, before review |
| `01-teammate-virtual-assistant.docx` | Teammate's virtual assistant write-up |
| `02-teammate-household-chatbot-categories.xlsx` | Teammate's household chatbot category taxonomy |
| `03-course-brief-section1.docx` | SMU IGD ILP brief, Section 1 |

## A note on the model

Every artefact here reflects the current generation model, **`Qwen-SEA-LION-v4-4B-VL`**
(AI Singapore, Qwen3-VL-4B-Instruct base, 4B, MIT licence, 256K context, English plus
seven Southeast Asian languages, vision-language). Earlier drafts named a 12B model on
the demo path with a 27B comparison; those are superseded.

**The 27B is out of scope entirely, not merely off the demo path.** The architecture review
in this folder still asks for it to be benchmarked "for the comparison table", and
`docs/team-tasks.csv` used to say the same. It no longer does. The review is kept as it was
written, because it is a dated record of what was reviewed and rewriting it would falsify
that — but it is not a current instruction, and the 27B line in it is the one thing in this
folder that is known to be wrong. Nothing should benchmark a 27B on the strength of it.

Two consequences carried through every artefact:

- The whole stack — generator, embedder, reranker, parser — fits inside **8 GB**, so the
  demonstration machine and the machine the product claims to run on are the same
  machine. That is a materially stronger claim than a local-first assistant needing an
  18 GB workstation.
- The model is **vision-language**, which turns the quarantine queue into a second pass
  rather than a dead end: anything that fails layout parsing is re-attempted against the
  page image. Docling is not replaced — it stays faster, cheaper and better on digital
  PDFs. The recovery rate is a reportable finding.

All VRAM and throughput figures in these documents are **planning estimates**. The week-1
task in Lane B is to replace every one of them with a measurement from the actual
machine.

## Regenerating

The diagrams and documents are built from scripts kept outside this repository. If a
figure needs to change, raise it with Christian rather than editing a PNG.
