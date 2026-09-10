# Christian — Lane A · Integration and product owner

**Owner: Christian.** Directories: `core/contracts.py`, `core/graph/`, `core/adapters/`,
`core/ingest/`, `modules/`, `db/migrations/`, and the merge queue.

> **Your task list:** [`tasks.md`](tasks.md) — generated from `docs/team-tasks.csv`, so tick things off there and regenerate.
> **Everyone else:** [`team/`](../README.md) · **The rules every agent follows:** [`AGENTS.md`](../../AGENTS.md)

Deliberately the lane with the least new feature code. An integrator who is also
mid-feature stops integrating, and the failure mode of five people and their agents on
one repository is not slow progress — it is five plausible-looking implementations of the
same idea.

---

## Week 1, in order

1. **Freeze the scope in writing** and have both supervisors acknowledge it. Everything
   else assumes this happened.
2. **`core/contracts.py` and `db/migrations/0001_init.sql` land as their own reviewed
   pull requests**, before any feature depends on them. An agent given a schema is
   consistent across sessions and across people; an agent given prose is not.
3. **`docker compose up`** with Postgres 17, pgvector and Ollama. Nothing else yet.
4. **Register the Telegram bot.** Ten minutes, and it retires the largest schedule risk
   in the project — the only item with an external clock nobody on the team controls.
5. **Hand Zee the pack lane.** Everything downstream waits on field names.

---

## The five things you ship

| | Weeks | Note |
|---|---|---|
| Capture adapters | 1–2 | Watched folder (debounced) and Telegram bot, behind one interface: `receive(bytes, mime, sender, ts) → ingest_job`. WhatsApp and Drive are alternate adapters post-MVP, not architecture changes. |
| Ingestion worker | 2–4 | Docling parse → contextualise → embed → schema-constrained extraction → idempotent upsert keyed on a SHA-256 of the source bytes. Both lanes commit in one transaction. |
| Quarantine, two-stage | 4 | Parse failures and low-confidence extractions do not disappear — they queue. The second stage sends the page **image** to the vision-language model, which is a capability the 4B SEA-LION swap bought us. Instrument it: the recovery rate is a reportable number. |
| The graph | 4–6 | Router → retrieve → rerank → grounding gate → answer or abstain. PostgresSaver checkpointer. |
| Two capability modules | 6–8 | Reminder and Alert. Hand-written parameterised queries in `modules/<id>/queries.py`. A module reads typed rows; it never sees the interface. |

---

## What integration actually means here

**Ninety minutes a week, protected.** You merge everything and delete the duplicate
helpers three people's agents wrote in the same week. Cheaper every time than
discovering the divergence in week 8.

**Nobody edits `core/contracts.py` in a feature pull request.** The most common way a
multi-agent repository degrades is a contract quietly widened to make one feature
easier. `CODEOWNERS` enforces the review; you enforce the principle.

**Vertical slices, not layers.** A pull request should let somebody do something new.

**The evaluation is the gate.** Any change to retrieval, extraction or the grounding gate
pastes its numbers into the pull request with one line on why they moved.

---

## Starter prompt for your coding agent

> Read `AGENTS.md`, `core/contracts.py`, `db/migrations/0001_init.sql` and
> `team/christian/README.md` completely before writing anything.
>
> Task: [one vertical slice, e.g. "implement the Telegram capture adapter satisfying the
> `receive(bytes, mime, sender, ts) → ingest_job` contract, with media fetched, written
> to the local inbox and deleted at source"].
>
> Hard rules that apply: no runtime SQL generation; every fact row carries a
> `document_id` and `page`; no new runtime dependency without an ADR in `docs/adr/`;
> nothing in `modules/` or `packs/` may import from `web/` or `api/`.
>
> If this task requires a change to `core/contracts.py` or `db/migrations/`, stop and
> tell me — that is a separate pull request and it is reviewed before anything depends
> on it. Do not widen a contract to make this feature easier.
>
> Order: propose the approach and the interfaces first and wait for me; implement; write
> a test using corpus fixtures with known ground truth from `corpus/register/`; run
> `make check`; then show me a demo path — the sequence of commands that proves a person
> can now do something they could not do before.

---

## Also yours

**Domain reviewer for the Insurance pack.** Nineteen years of wholesale banking is an
unusual advantage for reading a policy schedule. Use it as review of Zee's field list,
not as a second build lane.

**The demonstration.** Record a three-minute screen capture of the full happy path in
week 9, before demo night. It is the cheapest insurance in the project.

**The graph.** See `docs/GRAPHIFY.md` — you regenerate it, at the weekly integration
session, and nobody else commits `graphify-out/`.
