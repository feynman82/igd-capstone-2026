# `core/graph/` — the LangGraph runtime

**Owner: Christian.** Reviewed via `CODEOWNERS`.

The answer path: `route → retrieve → rerank → ground → answer or abstain`, with a
PostgresSaver checkpointer and a cross-thread store.

## What belongs here

- `router.py` — picks the lane, the pack and the module. The only generative step before
  the answer node.
- `gate.py` — the grounding gate. Below the pack's `abstain_below` reranker floor, the
  system states it has no document that answers, rather than composing something plausible
  from weak context. **This is the feature most worth demonstrating.**
- `answer.py` — refuses to emit a factual sentence with no supporting chunk id
  (`guardrails.must_cite`).
- `state.py` — the graph state, typed.

## What does not

Retrieval implementation (that is `core/retrieve/`, Yew Mun's). Module queries (those are
`modules/<id>/queries.py`). Anything that imports from `web/` or `api/`.

## Rules

Every node writes one line to the JSONL trace log: node, latency, model, retrieved doc
ids, reranker scores, gate decision. That file is both the evaluation dataset and the
audit trail, so a node that does not log is not finished.
