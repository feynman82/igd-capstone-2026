# `core/retrieve/` — hybrid retrieval

**Owner: Yew Mun.** Reviewed via `CODEOWNERS`.

Dense search alone misses exact identifiers such as policy numbers; lexical search alone
misses paraphrase. So: pgvector HNSW **and** Postgres full-text, fused with reciprocal
rank fusion, then reranked with `bge-reranker-v2-m3`, then cut at the pack's score floor.

## What belongs here

- `hybrid.py` — the two searches and the RRF fusion (k=60)
- `rerank.py` — the cross-encoder, 40 candidates down to 6
- `floor.py` — the score floor the grounding gate reads

## Rules

**No runtime SQL generation.** Queries are hand-written and parameterised. If you think
you need a generated query, open an ADR instead.

Every change here runs `make eval-quick` and pastes the numbers into the PR with one
sentence on the *mechanism* that moved them. One variable per PR — a run that changed
three things has told you nothing about any of them.
