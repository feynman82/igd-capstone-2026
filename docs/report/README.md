# `docs/report/` — the final report

**Due 10 November 2026. Twenty pages. 50% of the grade.**

`ILP_Report_Skeleton.docx` is the frame. Open it and read the first four pages before
writing anything — they carry the rubric, the page budget and the writing schedule.

**The skeleton is not in the brief's format.** The course brief sets Arial, 12 pt main text, 14 pt
bold section titles, 1.5 line spacing, justified, 20 pages, and an abstract of 150 to 300 words. At
that format a page holds about 340 words, so the skeleton's page budgets overstate what fits.

`Project Parrot Final Report (draft).docx` is built in the brief's format from the chapters here.
Rebuild it with `python3 docs/report/build_docx.py`; do not edit it by hand. A chapter drafted from
the repository carries a note until its owner has rewritten it. Clear the owner in `CHAPTERS` then.
Chapters `04-packs-and-interface.md` and `07-commercialisation-roadmap.md` are the longer sources
§3.3, §4.3, §4.4 and §7.4 were condensed from; they are not in the build.

## The thing to understand before you write a word

The report rubric in the module brief marks **six categories**: Overall Quality, Content
Development, Organisation, Language, Sources, and Citation. Not one of them marks
technical sophistication.

The engineering earns its marks through the presentation (40%) and the prototype. The
report earns its 50% by being a well-argued piece of writing that happens to be about a
system we built. **Writing it as a build log is the most likely way to lose half the
grade.**

Two consequences that are easy to get wrong:

- **The rubric explicitly requires a thesis statement**, and scores a non-debatable one
  — "a fact or a topic" — as Poor. "We built a household RAG system" is a topic. §1.3 of
  the skeleton carries a working thesis; refine it, do not weaken it.
- **Sources are marked on variety**, and the Poor band is "evidence obtained only from
  sources provided by the instructors." Compile references continuously; a list assembled
  in week 10 is where citation errors come from.

## Ownership

| § | Section | Owner | Written |
|---|---|---|---|
| — | Executive summary | Christian | W10, last |
| 1 | Introduction, problem, thesis | Christian | W8 |
| 2 | Background and landscape | Siew | W6 onward |
| 3 | Solution design and architecture | Christian, Yew Mun | W8 |
| 4 | Implementation | Christian, Zee | W9, after code freeze |
| 5 | Evaluation and results | Yew Mun | W9, after run 3 |
| 6 | Governance, ethics and risk | Siew | W8 |
| 7 | Value creation and readiness | Christian, Zee | W9 |
| 8 | Limitations and future work | Desmond, Yew Mun | W9 |
| 9 | Conclusion | Christian | W10 |
| — | References | All, compiled by Siew | continuously |

## The rule that keeps it honest

Every section is written from something that already exists in this repository — a
committed evaluation result, a governance artefact, an ADR, the corpus register. If a
section cannot point at a file, it is being invented, and invented content is exactly
what the Sources rubric line penalises.

### Source documents written for the report

These exist so that a section can be *written from* something rather than recalled. Each
one carries the argument, not the build log, and each names the decision record behind it.

| Document | Feeds | What it argues |
|---|---|---|
| [`docs/household-and-identity.md`](../household-and-identity.md) | §3, §4, §5, §6, §8 | Why "what is **my** premium?" is the one question citation cannot make safe, and what had to be built so that it could be. Carries the data model, the three-bucket resolution rule, the abstention design, and two limitations stated plainly. Decision: [ADR 0011](../adr/0011-the-household-is-people-and-aliases-and-the-owner-is-one-of-them.md). |
| [`05-evaluation-and-results.md`](05-evaluation-and-results.md) | §5, and the retrieval half of §3 | **§5 itself, on its budget of three and a half pages, in the skeleton's order; the holdout gap is marked ⟨holdout⟩.** That a household assistant should be judged on whether it guesses, not on how often it declines: the headline is five numbers, one per aim, led by unsupported claims (25 of 118 in Run 3, 21 on `main`), with the nine week-1 metrics as diagnostics and four validity threats. Decisions: [ADR 0018](../adr/0018-the-reranker-runs-in-process-because-ollama-cannot-serve-a-cross-encoder.md), [ADR 0019](../adr/0019-the-reranker-drops-what-does-not-answer-the-question.md). |
| [`appendix-c-evaluation-results.md`](appendix-c-evaluation-results.md) | Appendix C | The full results behind §5: every table, the module metrics, extraction by defect, runtime, seven limitations, and a source for each claim in date order. Excluded from the twenty pages. |
| [`appendix-d-golden-set-sample.md`](appendix-d-golden-set-sample.md) | Appendix D | Sample questions from the three sets, chosen by rule, each with its Run 3 outcome, failures included. Excluded from the twenty pages. |
| `00-abstract.md`, `01-introduction.md`, `02-background.md`, `03-design.md`, `04-implementation.md`, `06-governance.md`, `07-value-creation.md`, `09-conclusion.md` | The rest of the report | **Drafts written from the repository, for their owners to rewrite in their own words.** `references-verified.md` holds the reference entries they use. `figures/` holds Figures 1 to 4. |
| [`03-4-technology-selection.md`](03-4-technology-selection.md) | §3.4 | **Draft for Christian to review.** The stack by layer with its reason, and the generator's case: why a 4B vision-language model, what was measured, and why fitting 8 GB is still an estimate. |
| [`08-limitations-and-future-work.md`](08-limitations-and-future-work.md) | §8 | **Draft for Desmond to review.** What ten weeks did not reach, kept apart from what the approach itself cannot do, then the next three things. |
| [`04-packs-and-interface.md`](04-packs-and-interface.md) | §3.3, §4.3, §4.4 | **Draft, to re-check after the 28 October freeze.** A second domain cost a file, not a release, because a pack is data checked against a contract, the core owns the household's documents, and the interface shows where each claim came from. Covers the two axes, what a pack stopped being (documents moved to the core), a table of six rules each enforced by code, the two built packs side by side, the catalogue as evidence for the expansion model, and the three interface decisions that carry the thesis. States that Ask has not been usability-tested. Decisions: [ADR 0014](../adr/0014-a-pack-supplies-knowledge-and-the-core-stays-generic.md), [ADR 0016](../adr/0016-a-pack-advises-code-calculates-under-recorded-consent.md), [ADR 0017](../adr/0017-a-pack-is-grounding-and-persona-the-core-owns-documents.md). |
| [`07-commercialisation-roadmap.md`](07-commercialisation-roadmap.md) | §7.4, and the money slide | **Draft.** Packs are the unit of sale because the contract already makes them one. Covers segments from the five personas, three untested routes to revenue, the two constraints we can defend (on-device hardware, and WhatsApp's per-message cost), and a staged roadmap with what must be true before each stage. Claims no price and no market size. Decisions: [ADR 0016](../adr/0016-a-pack-advises-code-calculates-under-recorded-consent.md), [ADR 0017](../adr/0017-a-pack-is-grounding-and-persona-the-core-owns-documents.md). |

**Do not start the body before week 8.** Sections 5 and 7 cannot be written truthfully
until the evaluation has run three times, and a report drafted early becomes a document
the team defends rather than one that reports what happened.

## Three questions for the supervisors, at the 6 October mid-term

1. Do the twenty pages include title page, contents and references, or is it body only?
2. Is a citation style specified, or is internal consistency sufficient?
3. Should the repository be submitted alongside the report, or referenced?

Each changes how the document is assembled. Ask in October, not in November.
