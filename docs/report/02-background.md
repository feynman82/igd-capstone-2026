# §2 · Background and landscape

> **Draft.** Written from the repository for Siew to rewrite in their own words.

---

## 2.1 How households manage documents today

Research on personal information management has mostly studied the workplace; few studies look at
the home (Balogh et al., 2022). Those that do describe a flow, not a system. Balogh et al. (2022)
followed 30 people's records from arrival through action to filing, with email often serving as to-do list
and archive. In couples, one person usually carried the work. The risks they name are PARROT's
starting point: missed payments, records not found again, deductions left unclaimed. A later survey
linked saving records on a computer or in the cloud to fewer lost documents and late bills (Balogh
et al., 2024).

The work is also cognitive. Daminger (2019) describes anticipating needs, deciding and monitoring:
taxing, often invisible and unevenly shared.

Balogh et al.'s (2022) interviews were mostly in Australia, and we found no Singapore study. Nor did we
measure a household, so §5's baseline is a simpler retrieval system, not this status quo.

## 2.2 Retrieval-augmented generation, and why grounding is the interesting part

Retrieval-augmented generation answers from passages fetched at question time, not from a model's
memory alone (Lewis et al., 2020). For a household, the appeal is that a passage can be shown.

Published results motivated PARROT's retrieval. Anthropic (2024) reported that adding context to
each chunk, then keyword search, then reranking cut retrieval failures by 35, 49 and 67 per cent.
Those are a vendor's figures on code, fiction and research papers, so they motivate the design and
prove nothing about it. §5 supplies our numbers. PARROT's prefix is also simpler: title, type,
heading and page, written by code, not a model (ADR 0012). Fusion follows Cormack et al. (2009),
although Bruch et al. (2023) find rank fusion sensitive to its parameters.

Grounding is the harder problem: what a model does with what it was given. Joren et al. (2025)
found leading models often answer incorrectly instead of abstaining when the context is
insufficient. Magesh et al. (2025) found retrieval-based legal tools hallucinating on 17 to 33 per
cent of queries. A retrieved passage does not make a sentence true, so §5 scores unsupported claims
as well as retrieval.

## 2.3 Existing approaches and where they stop

| Approach | Example | What it offers | Where it stops |
|---|---|---|---|
| Hosted assistant | Gemini Notebook (Google, n.d.) | Answers grounded in uploaded sources, with inline citations | Documents go to the provider; sending feedback can open queries and uploads to human review |
| Document manager | Paperless-ngx (2026) | Self-hosted scanning and indexing; optional AI chat since July 2026, with Ollama support | New, and many AI features are marked beta |
| Local chat | AnythingLLM (Mintplex Labs, n.d.) | Runs locally by default, with source citations | The project page says nothing of what happens when documents lack the answer |

Custody is not a side issue. Zhang et al. (2024) found users trading privacy against usefulness,
often with a poor picture of the risk, and local-first design exists to remove that trade (Kleppmann
et al., 2019). But local chat with citations is becoming common, so it is no longer the gap.

A citation shows where a value came from, not whether it answers the question. None of the pages we
read reports how often its tool answers when it should decline. §5 reports that number.
