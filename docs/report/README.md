# `docs/report/` — the final report

**Due 10 November 2026. Twenty pages. 50% of the grade.**

`ILP_Report_Skeleton.docx` is the frame. Open it and read the first four pages before
writing anything — they carry the rubric, the page budget and the writing schedule.

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
| [`05-evaluation-and-results.md`](05-evaluation-and-results.md) | §5, and the retrieval half of §3 | **Draft — run 3 is missing and the gaps are marked ⟨run 3⟩.** That restraint is not a by-product of accuracy: every retrieval and generation metric improved while abstention got worse, because better retrieval supplies plausible evidence for unanswerable questions. Carries the delta table with run 3's column empty, the rejected relevance floor, extraction by document type, the two module metrics, and nine limitations. Decisions: [ADR 0018](../adr/0018-the-reranker-runs-in-process-because-ollama-cannot-serve-a-cross-encoder.md), [ADR 0019](../adr/0019-the-reranker-drops-what-does-not-answer-the-question.md). |
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
