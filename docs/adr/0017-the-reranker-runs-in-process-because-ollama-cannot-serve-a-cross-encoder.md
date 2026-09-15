# 17 · The reranker runs in-process, because Ollama cannot serve a cross-encoder

- **Status:** Proposed
- **Date:** 2026-09-15
- **Decider:** Yew Mun (Lane B). Reviewer: Christian (the stack rule in `AGENTS.md`)

## Context

`AGENTS.md` names Ollama for all inference, reranking included, and `PARROT_RERANK_MODEL` defaults
to an Ollama tag for `bge-reranker-v2-m3`. Ollama has no reranking API — upstream issue
ollama/ollama#3368 is open with two unmerged pull requests — and the pulled GGUF cannot serve any
request at all: on 0.33.3 both `/api/embed` and `/api/generate` terminate `llama-server` with a
`GGML_ASSERT`. The readiness check verifies the tag is present and reports the reranker ready
(issue #20). A cross-encoder reads the question and the passage together and emits one score; that
is not generation and not embedding, and Ollama has no third thing.

## Decision

**The reranker is `BAAI/bge-reranker-v2-m3` loaded in-process with `transformers` and `torch`.**

- Both libraries are already in the venv: Docling brought them for its layout models. No new
  dependency is added; the weights (2.27 GB, fp32 on disk, loaded as fp16) are fetched once from
  Hugging Face into the same cache Docling and RapidOCR use.
- It runs on whatever accelerator `torch` finds — CUDA on the workstation's 4060, beside the
  embedder, as the W1 placement intended; MPS on a Mac; CPU as a fallback that still works.
- `PARROT_RERANK_MODEL` keeps its name and now holds a Hugging Face model id. Its default becomes
  `BAAI/bge-reranker-v2-m3`. A tag beginning `hf.co/` is refused with a message naming this record.
- The readiness check verifies the model the way it will be used: weights present, one pair scored.
- `core/graph/ports.Reranker` is unchanged. The graph does not know where the score came from.

## Alternatives considered

| Option | Why not |
|---|---|
| Wait for Ollama | The pull requests have been open for months and W4 is due 29 September. The port is unchanged, so moving back is a one-file change when it lands. |
| `llama-server --reranking` serving the same GGUF | A second model server to install, start and keep alive on five machines, for one call. The failure this project keeps meeting is a component that is not running; adding one is the wrong direction. |
| The 4B generator as a pointwise judge through Ollama | Stays inside the stack, but it is not the model the task names, it is forty short generations per question, and a generator judging relevance is the thing a cross-encoder was trained to do better. |
| Drop the reranker; cut candidates by hybrid score | Loses the whole point of W4: the reranker is what reads the passage against the question rather than comparing two vectors (ADR 0013). |

## Consequences

Easy: the reranker exists, scores 40 candidates in well under a second on a GPU, and the
graph's `Reranker` port is satisfied without touching the graph. The evaluation harness can
measure it against `NoReranker` on the same vault.

Hard: PARROT now holds one model outside Ollama. The worker and the API each load it once, so a
Mac's memory carries a second copy of 1.1 GB when both run; the model loads lazily on the first
question, so the first answer after a start is slower by the load time. The stack sentence in
`AGENTS.md` is no longer literally true and should say so.

## Revisit when

Ollama ships a reranking endpoint (ollama/ollama#3368 closes), or the workstation's VRAM cannot
hold the embedder and the reranker beside each other at the context size the W1 benchmark chose.
