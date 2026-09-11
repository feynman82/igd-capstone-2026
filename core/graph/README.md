# `core/graph/` — the LangGraph runtime

**Owner: Christian.** Reviewed via `CODEOWNERS`.

The answer path: `route → retrieve → rerank → ground → answer or abstain`.

## What belongs here

- `ports.py` — `Passage`, `Retriever`, `Reranker`. The seam with Lane B, so neither lane
  waits for the other and neither ends up with a copy of the other's work.
- `gate.py` — the grounding gate. A sentence with no supporting passage is dropped; a
  sentence citing a passage that was never retrieved is dropped; below the pack's
  `abstain_below` floor nothing is answered at all. **The feature most worth demonstrating.**
- `answer.py` — the graph itself, its typed state, and the router that refuses a request to
  *act* before retrieval is even attempted. `never_acts` is `Literal[True]`; this is where
  that becomes a behaviour rather than a type.
- `baseline.py` — **disposable.** A dense-only retriever so the graph can run before
  `core/retrieve/` exists. Delete it when Lane B implements the ports; see ADR 0007. It is
  not a baseline measurement and must never be quoted as one.

## What does not

Retrieval implementation (that is `core/retrieve/`, Yew Mun's). Module queries (those are
`modules/<id>/queries.py`). Anything that imports from `web/` or `api/`.

## Rules

Every node writes one line to the `traces` table: node, latency, model, retrieved doc
ids, reranker scores, gate decision. That table is both the evaluation dataset and the
audit trail, so a node that does not log is not finished.

The checkpointer is `MemorySaver` until a reviewed migration creates the LangGraph
checkpoint tables. A library creating tables at runtime is rule 4 broken by a dependency
rather than by a person. ADR 0007 has the reasoning and names the follow-up.
