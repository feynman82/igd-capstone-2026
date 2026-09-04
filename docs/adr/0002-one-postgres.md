# 2. One PostgreSQL instance for everything

Date: 2026-09-08 · Status: accepted

## Context
The original proposal specified ChromaDB for vectors and FalkorDB with generated Cypher for
structured queries. The questions a household assistant answers ("which policies expire in
the next sixty days", "what did we spend on servicing") are relational selects and
aggregates, not graph traversals. Generated Cypher from a quantised local model is the
highest-variance component we could put on a live demo path.

## Decision
PostgreSQL 17 with `pgvector` holds chunks (dense plus `tsvector` lexical), typed facts and
obligations, LangGraph's agent state, and the pack and module registry. Retrieval fuses the
dense and lexical rankings with reciprocal rank fusion. Module queries are hand-written and
parameterised; nothing generates SQL at runtime.

## Rejected
- ChromaDB: no built-in keyword search, prototyping-tier persistence.
- A separate graph database: a second query language and a second failure mode for no gain.

## Consequences
One container, one backup, transactions spanning chunks and facts. Also the stack with the
deepest representation in training data, which matters when agents write most of the code.
