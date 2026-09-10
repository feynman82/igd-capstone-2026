# Working agreement for coding agents

This file is read by Antigravity, Claude Code and any other agent working in this
repository. Humans should read it too — it is the shortest description of how we build.

## Stack — do not substitute

- Python 3.12, FastAPI, Celery, Pydantic v2
- PostgreSQL 17 with `pgvector`. **One database.** No second datastore, no graph database,
  no separate vector store. Chunks, facts, obligations, agent state and the registry all
  live here.
- LangGraph for orchestration. **No LlamaIndex, no LangChain agents.** Retrieval is one
  tool call we wrote ourselves.
- Ollama for all inference: generation, embedding, reranking, schema-constrained extraction.
  Generator is `Qwen-SEA-LION-v4-4B-VL` (AI Singapore, MIT, vision-language). It is also the
  model used for the quarantine second pass, which reads the page image rather than parsed text.
- Next.js 15 (App Router), Tailwind, shadcn/ui, AI SDK `useChat`.
- Docling for parsing. Ragas for evaluation.

## Hard rules

1. **Never generate SQL at runtime.** Module queries are hand-written and parameterised in
   `modules/<id>/queries.py`. If you think you need a generated query, open an ADR instead.
2. **Every fact row cites its source.** `document_id` and `page` are NOT NULL. There is no
   code path that writes a fact without provenance.
3. **No claim without a citation.** The answer node refuses to emit a factual sentence that
   has no supporting chunk id attached.
4. **Do not edit `core/contracts.py` or `db/migrations/` as part of a feature PR.** Those are
   separate, reviewed PRs.
5. **No new runtime dependency without an ADR** in `docs/adr/`. Dev/test dependencies are fine.
6. **Sources of truth generate their outputs; never edit the output.** `pack.yaml`
   generates `packs/*/schemas.py`, `corpus/register/*_columns.csv` and
   `docs/field-dictionary.md` via `python -m packs.build`. `docs/team-tasks.csv`
   generates `team/*/tasks.md` via `python scripts/build_team_tasks.py`. Change the
   source and regenerate. A field name — and a task — is written down in exactly one
   place in this repository.
7. **Nothing in `packs/` or `modules/` may import from `web/` or `api/`.** Packs are data plus
   a schema; modules read typed rows. Neither knows the interface exists.
8. **`never_acts: true` in every pack manifest.** v1 advises. It does not pay, book or file.
   This is enforced by the type system, not by convention: `core/contracts.py` declares it
   `Literal[True]`, so a pack that sets anything else will not load.
9. **Do not commit `graphify-out/`.** Only the integration lead regenerates it, at the weekly
   session, in a commit containing nothing else. See `docs/GRAPHIFY.md`.

## Style

- Type hints everywhere; `mypy --strict` on `core/`.
- `ruff` for lint and format. Line length 100.
- **Never write code that generates corpus documents.** The corpus is authored by Lane E and
  handed over as a validated register plus files. `corpus/` holds the register and its
  validator only.
- Tests use the register in `corpus/register/` and the batches it describes, never live documents.
- One vertical slice per PR. A PR should be demoable, not a layer.

## Definition of done

- [ ] `make check` passes (ruff, mypy, pytest, and the generated-files-in-sync gate)
- [ ] New behaviour has a test that uses corpus fixtures with known ground truth
- [ ] If it touches retrieval, extraction or the gate: `make eval-quick` run and the numbers
      pasted into the PR body, with a sentence on why they moved
- [ ] If it changes a decision: an ADR
- [ ] CODEOWNERS review from the owning lane

## Before you read files at random

This is a five-person repository. Ask the knowledge graph first:

```
graphify query "how does a field name in pack.yaml reach the corpus register"
graphify explain "PackManifest"
```

If it is not installed, `docs/field-dictionary.md` and `core/contracts.py` explain most of
the system between them.

## What to do when you are unsure

Stop and open an issue using `.github/ISSUE_TEMPLATE/decision.yml`. Do not invent a second
way of doing something that already has one way.
