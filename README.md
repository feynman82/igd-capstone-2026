# PARROT

Local-first household RAG platform. Internal working name.
SMU IGD Integrated Learning Project, Sep–Nov 2026.

## Quick start

```bash
cp infra/.env.example .env
docker compose -f infra/docker-compose.yml up -d     # postgres+pgvector, redis
uv sync                                              # or: pip install -e ".[dev]"
psql "$DATABASE_URL" -f db/migrations/0001_init.sql
python -m corpus.validate corpus/register/batch1.csv  # check a handed-over batch
make dev                                             # api on :8000, web on :3000
```

## Where things live

| Path | What | Owner |
|---|---|---|
| `core/contracts.py` | The pack and module manifests. **Changing this needs a PR review from the integration lead.** | Christian |
| `core/graph/` | LangGraph runtime: router, grounding gate, answer node | Christian |
| `core/adapters/` | Capture adapters: watched folder, Telegram, (WhatsApp, Drive) | Christian |
| `core/ingest/` | Ingestion worker, extraction, quarantine, idempotency | Christian |
| `core/retrieve/` | Hybrid search, RRF fusion, reranking, score floor | Yew Mun |
| `modules/` | Capability modules: reminder, alert, (tracker) | Christian |
| `packs/` | Domain packs: iras_tax, insurance_agent | Desmond |
| `web/` | Next.js 15 interface | Desmond |
| `corpus/` | The document register (ground truth) and its validator | Desmond |
| `eval/` | Golden sets, Ragas harness, committed results | Yew Mun |
| `docs/governance/` | PDPA, ISO, IMDA artefacts | Siew |
| `docs/adr/` | Architecture decision records — one per non-obvious choice | anyone |

## The two rules that matter

1. **Contracts before code.** If a change alters `core/contracts.py` or `db/migrations/`, it is its own PR, reviewed before any code depends on it.
2. **Numbers come from Postgres, never from the model.** Dates, amounts and policy numbers are read from typed columns. The model phrases the sentence around them.
