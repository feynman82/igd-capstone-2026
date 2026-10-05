# Model card: Parrot v1

Status: draft · Owner: Siew · Reviewer: Yew Mun (numbers), Christian (system facts) ·
Numbers as of evaluation run 2, 2026-09-30

> This card describes the **system** as deployed, not only the model inside it. A 4B model on
> its own is not what answers a household's question: the gate, the retriever and the packs
> decide what it may say. Every repository claim points at a file. Facts about the upstream
> model come from its published model card, which this environment could not open; they were
> taken from search results and are marked **verify against the model card**.

## 1. Models in the system

| Role | Model | Where it runs | Evidence |
|---|---|---|---|
| **Generation, extraction, quarantine image pass** | `Qwen-SEA-LION-v4-4B-VL`, quantised Q4_K_M, GGUF build `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M` | Ollama, `127.0.0.1` | `infra/.env.example` (`PARROT_GEN_MODEL`); `AGENTS.md` |
| Embedding | `embeddinggemma:300m`, 768 dimensions | Ollama, `127.0.0.1` | `infra/.env.example`; `db/migrations/0001_init.sql` (`vector(768)`) |
| Reranking | `BAAI/bge-reranker-v2-m3` cross-encoder | In-process | `infra/.env.example`; ADR 0018 |
| Evaluation judge (not in the product) | `qwen2.5:7b-instruct` | Ollama, local | `eval/results/2026-09-30-run2-hybrid-plus-reranker.md` |

### The generation model

| | | Source |
|---|---|---|
| Developer | AI Products Pillar, AI Singapore; funded by Singapore's National Research Foundation | [Model card][hf] (**verify against the model card**) |
| Base model | Fine-tuned from `Qwen3-VL-4B-Instruct` | [Model card][hf] (**verify**) |
| Parameters | 4B; published in BF16. We run a community 4-bit quantisation (Q4_K_M) by `mradermacher`, not AI Singapore's own weights | [Model card][hf] (**verify**); `infra/.env.example`; `eval/results/w1-hardware.md` (digest `d46a930cafd8`) |
| Modalities | Text and image in, text out (vision-language) | [AI Singapore announcement][blog]; `AGENTS.md` |
| Languages | English, Burmese, Indonesian, Filipino, Malay, Tamil, Thai, Vietnamese | [Model card][hf] (**verify**) |
| Training (by AI Singapore) | Supervised fine-tuning on about 9 million instruction-text pairs | [Model card][hf] (**verify**) |
| Context length | 256K tokens published. **We configure 16,384** | [Model card][hf] (**verify**); `infra/.env.example` (`PARROT_CONTEXT_TOKENS`) |
| **Licence** | **Conflict.** The published model card is reported as **Apache-2.0**. This repository says **MIT** in `AGENTS.md`, `NOTICE.md` and `README.md`. See open question 1 | [Model card][hf]; `NOTICE.md` line 32 |
| Our training | None. We do not fine-tune or retrain | `docs/governance/iso-stage-process-map.md` ("What we consciously do not do") |

## 2. Intended use

- **Who:** one Singapore household, on its own computer, asking about its own documents:
  insurance, payslips, CPF and SRS, tax notices, identity documents, loans.
- **What:**
  - Answer what a document says, citing the page.
  - Remind the household of dates its documents print.
  - Under recorded consent, run a small set of declared advice checks: insurance cover gap,
    and SRS relief room and saving.
- **Evidence:** `README.md`; `packs/insurance_agent/pack.yaml` and `packs/iras_tax/pack.yaml`
  (`advice.shapes`); ADR 0016; `db/migrations/0003_advice.sql` (`advice_consents`).

## 3. Out of scope

| Out of scope | How it is enforced | Evidence |
|---|---|---|
| **Acting:** paying, renewing, booking, filing, sending | Typed into the pack contract; a pack that sets otherwise does not load. Requests to act are routed and refused before retrieval | `core/contracts.py:249` (`never_acts: Literal[True]`); `core/graph/answer.py` (`ROUTE_SYSTEM`) |
| **Advice no pack declares:** switching insurer, surrendering a policy, picking investments | Declined before anything is searched | `core/graph/answer.py` (`Declined`); `eval/sets/adversarial/` items c-c10 to c-c12 |
| **Verdicts written by the model** | A verdict is chosen by code; the model only explains | `core/contracts.py:250` (`verdict_by_code: Literal[True]`); ADR 0016 |
| **Claims without a source** | Every fact is stored with a document and page, both `NOT NULL`; the gate checks answers against cited passages | `db/migrations/0001_init.sql`; `core/graph/gate.py` |
| **Use by anyone outside the household, or over a network** | Every service URL must be loopback | `core/runtime/settings.py` |
| **Regulated financial advice** in the sense of a licensed adviser | Not offered. Advice shapes carry a pack disclaimer | `packs/*/pack.yaml` (`advice`); ADR 0016 |

## 4. Measured performance

Measured on Parrot's own synthetic corpus, not on any public benchmark. Corpus
`210231c041def426` (26 indexed documents), code `7d3a48c`, generator as above, judge
`qwen2.5:7b-instruct`. Source: `eval/results/2026-09-30-run2-hybrid-plus-reranker.md`; run 1
in `eval/results/2026-09-29-baseline-dense-only.md`.

| Metric | Run 1 (6 docs, dense) | **Run 2 (26 docs, hybrid + reranker)** | Target | Met |
|---|---|---|---|---|
| Context recall | 0.895 | **0.897** | ≥ 0.85 | ✓ |
| Context precision | 0.868 | **0.854** | ≥ 0.70 | ✓ |
| Faithfulness | 0.819 | **0.967** | ≥ 0.90 | ✓ |
| Answer relevancy | 0.765 | **0.779** | ≥ 0.80 | ✗ |
| **Abstention rate, Set B (hard negatives)** | 0.760 | **0.520** | ≥ 0.95 | ✗ |
| Field extraction F1 | 0.898 | **0.903** | ≥ 0.90 | ✓ |

Run 2 scored 64 questions: 39 from Set A and all 25 from Set B. Another 33 Set A questions
await a document. **Set C was not run**; the 15 adversarial items are drafted, and Desmond runs
them in W8.

**Noise floor:** a change under about 0.05 in faithfulness or relevancy is noise. Changes in
recall, precision and extraction F1 are real (run 1 write-up, "How much of a delta is a
delta").

### Beside the RAG metrics

| Metric | Measured | Target | Source |
|---|---|---|---|
| Extraction F1 by type | 1.000 on identity cards, passports, birth certificates, payslips, renewal notices; **0.881 policy schedules; 0.762 loan agreements** | ≥ 0.90 | `eval/results/w6-extraction-by-doc-type.md` |
| Obligation precision | 1.000 (7 obligations from documents) | ≥ 0.95 | `eval/results/w7-module-metrics.md` |
| Alert false-positive rate | **1.000** (1 alert, a false positive) | ≤ 0.05 | `eval/results/w7-module-metrics.md` |
| Decode speed, peak VRAM | 130 tok/s at 16K context (79 tok/s with the window filled); 7.4 GB | — | `eval/results/w1-hardware.md` (RTX 3080, not the RTX 4060 demo machine) |
| Median answer latency | 3,368 ms (run 2) | — | run 2 write-up |

## 5. Known limitations and failure modes

1. **It answers when it should abstain.** This is the weakest number, at 0.52 against 0.95.
   - Twelve of 25 hard-negative questions got an answer that cited a real page and said
     something the page does not support.
   - Better retrieval made this *worse* in two runs running.
   - Example: "when is the road tax on SLK 8842 D due?" was answered with the vehicle's
     first-registration date from a policy schedule.
   - **A citation is not a warrant.** (Run 1 and run 2 write-ups.)
2. **Extraction misses fields on long documents.**
   - On policy schedules, `expiry_date` is extracted on 5 of 11 and `excess` on 0 of 6.
   - Reminders can only come from extracted dates, so obligations exist for 7 of the 16 the
     register supports (`w6`, `w7` results; issue #32).
3. **The one alert measured was a false positive.** It counted days uncovered on a policy
   whose renewal was on file (`w7-module-metrics.md`).
4. **It can confuse whose document it is.** Run 1 answered Marcus's question from his father's
   policy (run 1 write-up).
5. **The reranker can cut the page the answer needed.** This happened once in run 2
   (`page_shown` 0.974).
6. **Synthetic corpus only.** Every number above comes from generated documents. Real
   documents, photographed and inconsistent, are untested until the holdout run
   (`docs/governance/synthetic-data-case.md`).
7. **Languages are untested.** The model supports seven Southeast Asian languages. Every
   evaluation question so far is in English, so no performance claim is made for any other
   language.
8. **Quantisation is untested against full precision.** We run a 4-bit build, and no run
   compares it with the BF16 weights.

## 6. Ethical and privacy considerations

- **All inference is local.** Nothing leaves the machine at inference; the one boundary
  crossing is optional Telegram capture (`docs/governance/data-inventory.md`, flow map).
- **Sensitive data in scope:** identity numbers, income, health-related insurance and
  children's records (`data-inventory.md`).
- **Bias:** nothing has been measured.
  - The corpus is one household, Chinese-Singaporean, with three surnames
    (`corpus/canon.md`).
  - Name handling across other naming conventions is untested beyond surname variation.
- **Prompt injection:** documents are untrusted input. Set C items c-c04 to c-c06 test this;
  they are not yet run.

## 7. Open questions

1. **Licence.** Is `Qwen-SEA-LION-v4-4B-VL` MIT, as this repository says in three places, or
   Apache-2.0, as its model card is reported to say? Siew to check [the model card][hf]
   directly. If it is Apache-2.0, `AGENTS.md`, `NOTICE.md` and `README.md` need correcting.
   That is Christian's lane, not this file's. The licence of the `mradermacher` GGUF
   conversion also needs checking.
2. **Upstream facts.** Siew to confirm each row marked **verify** against [the model card][hf],
   and record the date read.
3. **Demo hardware.** The RTX 4060 benchmark is still to be appended
   (`eval/results/w1-hardware.md`). For Christian.
4. **Run 3** (W8) replaces section 4. For Yew Mun.

## References

- [hf]: AI Singapore, *aisingapore/Qwen-SEA-LION-v4-4B-VL*, model card, Hugging Face.
  https://huggingface.co/aisingapore/Qwen-SEA-LION-v4-4B-VL. Not opened from this environment;
  facts taken from search results on 2026-10-05.
- [blog]: AI Singapore, *Announcing Qwen-SEA-LION-v4 (4B & 8B): Additional Vision-Language
  Models for Southeast Asia*.
  https://sea-lion.ai/blog/announcing-qwen-sea-lion-v4-4b-8b-additional-vision-language-models-for-southeast-asia/
- AI Singapore, *SEA-LION v4* documentation. https://docs.sea-lion.ai/models/sea-lion-v4
- Mitchell, M. et al. (2019). *Model Cards for Model Reporting*. Proceedings of FAT* 2019.
  https://doi.org/10.1145/3287560.3287596. The format this card follows.
- Repository sources: `eval/results/2026-09-29-baseline-dense-only.md`,
  `eval/results/2026-09-30-run2-hybrid-plus-reranker.md`,
  `eval/results/w1-hardware.md`, `eval/results/w6-extraction-by-doc-type.md`,
  `eval/results/w7-module-metrics.md`, `core/contracts.py`, `infra/.env.example`.

[hf]: https://huggingface.co/aisingapore/Qwen-SEA-LION-v4-4B-VL
[blog]: https://sea-lion.ai/blog/announcing-qwen-sea-lion-v4-4b-8b-additional-vision-language-models-for-southeast-asia/
