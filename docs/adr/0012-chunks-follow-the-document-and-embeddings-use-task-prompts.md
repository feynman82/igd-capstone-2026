# 12. Chunks follow the document's headings, and embeddings use the model's task prompts

Date: 2026-09-13 · Status: accepted

## Context

"Do I have a hospitalisation plan?" abstained against a vault holding
`privatecare_hospital_surgical_full_policy.pdf`: *the closest document is not close enough (best
match 0.42, this pack answers above 0.45)*. The retriever was not the first thing wrong. Three
ingestion faults sat in front of it, each measured on the live vault (six indexed policies, 35
chunks) with a read-only probe:

1. **Chunks were cut by character count, mid-word.** Docling's items are joined with single
   newlines and `core/ingest/chunk.py` only broke at blank lines, so every page was one
   "paragraph" and was sliced every 1,050 characters. Chunks began "e payment of the required
   Annual Premium" and "llness or accidental injury". A clause cut in two is retrieved by neither
   half.
2. **Every word was separated by a tab.** The PDF's text layer uses tabs; they went into chunks
   and into the embedding input unchanged.
3. **EmbeddingGemma was used without its task prompts** on either side. It was trained with
   `task: search result | query: …` for queries and `title: … | text: …` for documents; without
   them its similarities are lower and flatter.

A chunk's context prefix also named only the document type, filename and page, so a chunk from
clause 6 of a contract could not say which contract, or which section, it came from.

## Decision

- **Chunks follow the document's structure** (`core/ingest/chunk.py`). The parser now keeps
  Docling's heading labels (`ParsedPage.blocks`). A heading starts a chunk and names every chunk
  under it; items and table rows are packed whole to 900 characters; a longer item is split at
  sentence ends and only a longer sentence at a space; whitespace runs collapse; a heading-only
  chunk is not kept. Pages without parser structure fall back to capitalised headings.
- **The prefix names the document and the section**: `title — type — heading — page`. The title
  is the document's `string` fields as extracted, in the pack's declared order — for a policy
  schedule, insurer and product name — so no field name is written in `core/`.
- **Queries and passages use the embedding model's task prompts** (`Ollama.embed_query`,
  `Ollama.embed_documents`), applied only for a model that expects them.
- **`scripts/reindex.py` rebuilds chunks and vectors** from the inbox without re-classifying or
  re-extracting, because the two sides must be embedded alike and re-extraction on a processor
  is minutes per document for facts that did not change.

## Evidence

Cosine similarity of the top passage, and the rank of the passage that holds the answer, on the
same six documents (`rag_probe2`, 13 September, CPU-only Ollama):

| Question | Before: top (answer rank) | After: top (answer rank) |
|---|---|---|
| do i have a hospitalisation plan? | 0.421 abstains | 0.561 answers |
| appendicitis operation at a private hospital | 0.557 (2) | 0.604 (1, clause 4.4) |
| waiting period for appendicitis | 0.332, definitions page | 0.488 (1, clause 6) |
| how do i make a claim | 0.504, wrong clause | 0.510 (1, clause 8) |
| what is not covered | 0.504 | 0.549, clause 7 first |
| when does my hospital plan expire | 0.477 (2) | 0.461 (4) |
| premium for my hospital insurance | 0.459 (1) | 0.503 (3) |
| policy number for the hospital plan | 0.478 (2) | 0.504 (2) |

Prompts alone, on the old chunks, moved the first question to 0.498 but made others worse; the
new chunks without prompts were worse than both together. They are one change for that reason.
A document "card" of extracted facts, embedded as its own chunk, scored 0.43–0.46 and was dropped.

## Consequences

The vault must be re-embedded once (`scripts/reindex.py`); until then questions retrieve badly.

**Schedule questions are still weak.** Expiry, premium and policy number put the right chunk at
rank 2–4: a table of `label: value` lines does not look like a question to a dense model. That is
retrieval's to fix, and the evidence points at it: lexical search matches "premium" and
"expiry" directly, and a cross-encoder reranker reads the table rather than its vector.

**For Lane B (`core/retrieve/`)**, three things that now bind:

- Any retriever embeds the question with `Ollama.embed_query`, never `embed`, or it searches a
  vault embedded one way with a query embedded another.
- `guardrails.abstain_below` was calibrated against un-prompted scores. Scores have moved up
  across the board, so the floor wants re-measuring against the golden set rather than keeping.
- `chunks.tsv` is built from `context_prefix || text`, so the title and heading are now in the
  lexical index too.

`make eval-quick` was not run for this change: on a machine whose generator runs on the processor
a Ragas run is hours, and the numbers above are retrieval-only. The first eval run after this
lands is the one to quote.
