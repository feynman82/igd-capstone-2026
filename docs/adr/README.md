# Architecture decision records

One record per non-obvious choice, written when the reasoning is still in someone's head.
Six weeks later nobody remembers whether Postgres-only was considered or accidental, and
the difference matters when a supervisor asks.

`AGENTS.md` requires an ADR for any new runtime dependency.

## Index

| # | Decision | Status |
|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [0002](0002-one-postgres.md) | One PostgreSQL instance for chunks, facts and state | Accepted |
| [0003](0003-paperbrain-pattern-not-module.md) | PaperBrain informs core/retrieve/'s pattern; it is not the core module | Accepted |
| [0004](0004-local-setup-readiness.md) | Local setup runs before assistant readiness; loopback defaults | Accepted |
| [0005](0005-polling-the-watched-folder.md) | The watched folder is polled for stability, not subscribed to for events | Accepted |
| [0006](0006-pypdfium2-for-the-quarantine-image-pass.md) | pypdfium2 renders the page images the quarantine second pass reads | Accepted |
| [0007](0007-the-graph-ships-before-retrieval-and-before-a-checkpoint-table.md) | The answer graph ships before hybrid retrieval and before a checkpoint table | Accepted |
| [0008](0008-ingestion-runs-on-a-celery-worker.md) | Ingestion runs on a Celery worker; the queue carries a digest, not the document | Accepted |
| [0009](0009-two-web-dependencies-beyond-the-stack.md) | `next-themes` and `lucide-react` are the only two web dependencies beyond the named stack | Accepted |
| [0010](0010-main-is-unprotected-by-convention.md) | `main` is unprotected, and the discipline is human | Accepted |
| [0011](0011-the-household-is-people-and-aliases-and-the-owner-is-one-of-them.md) | The household is people and aliases, and the owner is one of them | Accepted |
| [0012](0012-chunks-follow-the-document-and-embeddings-use-task-prompts.md) | Chunks follow the document's headings, and embeddings use the model's task prompts | Accepted |
| [0013](0013-a-question-is-understood-before-it-is-searched.md) | A question is understood before it is searched, and scoped before it is cut | Accepted |
| [0014](0014-a-pack-supplies-knowledge-and-the-core-stays-generic.md) | A pack supplies what the core knows about a domain, and the core stays generic | Proposed |

Add a row when you add a record.

## Writing one

Use the `writing-an-adr` skill, or copy [`TEMPLATE.md`](TEMPLATE.md). Four digits, next in
sequence, short slug: `0003-telegram-as-default-capture.md`.

**Never rewrite an accepted ADR.** Supersede it: write a new one, mark the old one
`Superseded by NNNN`, link both ways. The trail of superseded decisions is itself evidence
for the report — it shows the design was reasoned about rather than assembled.
