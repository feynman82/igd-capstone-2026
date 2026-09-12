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

**Do not start the body before week 8.** Sections 5 and 7 cannot be written truthfully
until the evaluation has run three times, and a report drafted early becomes a document
the team defends rather than one that reports what happened.

## Three questions for the supervisors, at the 6 October mid-term

1. Do the twenty pages include title page, contents and references, or is it body only?
2. Is a citation style specified, or is internal consistency sufficient?
3. Should the repository be submitted alongside the report, or referenced?

Each changes how the document is assembled. Ask in October, not in November.
