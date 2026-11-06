# §3.4 · Technology selection, and the reasoning behind it

**Owners: Christian, with Yew Mun.** Budget one page, including the table.

> **Status.** A draft by Yew Mun, for Christian to review. Every line points at a decision record,
> a committed measurement or the model's own card. Where the repository records no reason, the
> table says what the part does rather than guessing why it was chosen.

---

Every layer runs on the owner's machine, and the reasons below are mostly about keeping it there.

| Layer | Choice | Reasoning |
|---|---|---|
| Generation and page images | Qwen-SEA-LION-v4-4B-VL (AI Singapore, 2025), through Ollama | Argued below |
| Embedding | `embeddinggemma:300m` (Schechter Vera et al., 2025), 768 dimensions | A 308-million-parameter model built for on-device use |
| Reranking | `bge-reranker-v2-m3`, in process | Ollama cannot serve a cross-encoder, so this is the one model outside it (ADR 0018) |
| Parsing | Docling (Auer et al., 2024), with OCR | Keeps layout and tables; a page it cannot read goes to the generator as an image (ADR 0006) |
| Storage | PostgreSQL 17 with `pgvector` | The proposal had ChromaDB and FalkorDB. A household's questions are relational selects, not graph traversals, so one database holds chunks, facts and agent state (ADR 0002) |
| Retrieval | Hand-written hybrid search with reciprocal rank fusion | A pattern ported, not a module adopted, so every boundary stays ours (ADR 0003) |
| Orchestration | LangGraph | Routing, retrieval, the grounding gate and the answer are separate steps |
| Background work | Celery with Redis | A PDF took about eight seconds on the capture thread, and nothing was watching the folder meanwhile (ADR 0008) |
| Interface | Next.js 15 and shadcn/ui | Streams each sentence with its citation beside it |

**The generator is the choice that carries the argument.** Qwen-SEA-LION-v4-4B-VL is a
four-billion-parameter vision-language model from AI Singapore, under an MIT licence. Two reasons
for it are on record. One is vision: a page the parser cannot read is tried again against the page
image by the same model, so quarantine is a second pass rather than a dead end. The other is fit,
and that is a design argument, not a specification. The proposal's 27-billion-parameter model
needed two graphics cards, and a local-first assistant that needs a workstation is a research
prototype.

Measured on a 10 GB RTX 3080, at the configured 16K context window, the generator holds 5.7 GB and
writes 79 tokens a second with the window 84 per cent full. With the embedder also loaded the card
holds 7.4 GB, of which 1.7 GB is the idle desktop. The reranker, about 1.1 GB, was not in that
measurement, so the whole stack has not been measured together. The same stack answered on a
MacBook on 28 October, more slowly. **Fitting an 8 GB GPU remains a planning estimate:** the design
aims at hardware a household could own, and the measurement so far reaches a 10 GB card.

### References used in this section

AI Singapore. (2025). *Qwen-SEA-LION-v4-4B-VL* [Model card]. Hugging Face.
https://huggingface.co/aisingapore/Qwen-SEA-LION-v4-4B-VL

Auer, C., Lysak, M., Nassar, A., Dolfi, M., Livathinos, N., Vagenas, P., Berrospi Ramis, C.,
Omenetti, M., Lindlbauer, F., Dinkla, K., Mishra, L., Kim, Y., Gupta, S., Teixeira de Lima, R.,
Weber, V., Morin, L., Meijer, I., Kuropiatnyk, V., & Staar, P. W. J. (2024). *Docling technical
report* (arXiv:2408.09869). arXiv. https://doi.org/10.48550/arXiv.2408.09869

Schechter Vera, H., Dua, S., Zhang, B., Salz, D., Mullins, R., Raghuram Panyam, S., Smoot, S.,
Naim, I., Zou, J., Chen, F., Cer, D., Lisak, A., Choi, M., Gonzalez, L., Sanseviero, O., Cameron,
G., Ballantyne, I., Black, K., Chen, K., . . . Seyedhosseini, M. (2025). *EmbeddingGemma: Powerful
and lightweight text representations* (arXiv:2509.20354). arXiv.
https://doi.org/10.48550/arXiv.2509.20354
