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

Add a row when you add a record.

## Writing one

Use the `writing-an-adr` skill, or copy [`TEMPLATE.md`](TEMPLATE.md). Four digits, next in
sequence, short slug: `0003-telegram-as-default-capture.md`.

**Never rewrite an accepted ADR.** Supersede it: write a new one, mark the old one
`Superseded by NNNN`, link both ways. The trail of superseded decisions is itself evidence
for the report — it shows the design was reasoned about rather than assembled.
