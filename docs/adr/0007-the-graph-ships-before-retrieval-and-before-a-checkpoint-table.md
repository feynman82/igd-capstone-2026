# 7. The answer graph ships before hybrid retrieval and before a checkpoint table

Date: 2026-09-11 · Status: accepted

## Context

`team/christian/README.md` gives Lane A the graph — router, retrieve, rerank, grounding gate,
answer or abstain, on a PostgresSaver checkpointer — and gives Lane B (`core/retrieve/`) hybrid
search, RRF fusion, the cross-encoder reranker and the abstain floor. Both are in flight at the
same time, and the graph is worthless without something to retrieve with.

Two things therefore had to be decided rather than assumed.

**Who writes the retriever the graph runs today.** Writing one in `core/retrieve/` would put two
people's agents in the same directory in the same week, which is the exact failure the lane
split exists to prevent — and worse, it would produce a second, unmeasured baseline sitting next
to the one Yew Mun has to publish.

**Where the checkpointer's tables come from.** `PostgresSaver` creates its own tables on
`setup()`. Rule 4 says `db/migrations/` is a separate, reviewed pull request; a library creating
tables at runtime is that rule broken by a dependency rather than by a person, which is worse
because nobody reviews it.

## Decision

**Retrieval is a port, not an import.** `core/graph/ports.py` declares `Passage`, `Retriever`
and `Reranker`. The graph depends only on those. `core/retrieve/` implements them when it lands,
and `scripts/ask.py` changes by two import lines.

**The stopgap lives in `core/graph/`, labelled as disposable.**
`core/graph/baseline.py` is a dense-only pgvector query and a reranker that reorders nothing. It
is in Lane A's directory because it is Lane A's scaffolding, and it is deliberately naive so
that nobody mistakes it for Lane B's baseline. Lane B's baseline is a *measurement*, committed
under `eval/results/` with the corpus manifest it ran against. This is not that and must never
be quoted as if it were.

**The checkpointer is `MemorySaver` until the migration lands.** Conversation state does not
survive a restart, which costs nothing today because nothing yet depends on a thread outliving
a process. Swapping it is one line once a reviewed migration creates the checkpoint tables.

## Consequences

The grounding gate is testable and demonstrable now: `scripts/ask.py` answers with a document
and a page, abstains with a reason and the pack's floor when the evidence is weak, and refuses a
request to act at the router before retrieval is even attempted. Those behaviours are held by
tests that use a fake retriever, so they will not move when real retrieval arrives.

The quality of the answers is not yet a claim anybody should make. Dense-only retrieval over a
handful of documents is not a result; the numbers come from Yew Mun's harness against a golden
set, and until then the honest statement is that the *mechanism* works.

Two follow-ups are owed and are named here so they are not forgotten:

1. **Delete `core/graph/baseline.py`** when `core/retrieve/` implements `Retriever` and
   `Reranker`. The ports do not change.
2. **A migration for the LangGraph checkpoint tables**, as its own reviewed pull request, then
   `MemorySaver` becomes `PostgresSaver` in `core/graph/answer.py`.
