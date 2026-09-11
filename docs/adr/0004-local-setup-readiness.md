# 4. Local setup can run before the household assistant is ready

Date: 2026-09-10 · Status: accepted

## Context

Christian approved building startup and diagnostics first, with same-computer access
before a household-network mode. `START.cmd` previously required a nonexistent runtime
supervisor. A missing database or model must be understandable to nontechnical teammates
without claiming that the unfinished assistant works.

## Decision

The launcher starts a loopback-only FastAPI diagnostic server. It owns its listening
socket, refuses a busy port and opens the browser only once that server has started.
`/healthz` reports server liveness; `/readyz` returns HTTP 503 and `ready: false` throughout
this setup stage. A read-only setup page shows database, Redis and Ollama metadata checks
and explicitly identifies missing document processing and the household interface.

This small operational page is not the product frontend. Today, Ask, Vault and Packs
remain Next.js work in Lane D. No runtime dependency is added.

Use one local Ollama endpoint by default. Accept only loopback service URLs in this stage,
ignore HTTP proxy environment variables for Ollama checks and do not follow redirects.
Publish Docker's database and broker ports on loopback. The checker does not install
dependencies, download/load models, apply migrations or start other services. It never
processes household documents. Existing services remain running when the setup server stops.

Model metadata is not proof that an inference operation works. Installed models remain
unverified until generation, embeddings, reranking and image-input smoke tests exist.
The base-table check is a schema presence check, not full migration integrity validation.

## Consequences

Teammates can inspect missing prerequisites in a browser now. Application readiness must
later include the real worker, graph, model operations and built Next.js interface before
the assistant can be declared ready. The original startup integration contract is therefore
delivered in stages, explicitly separated in the user-facing status.

The external RTX 3080 is development-only. No setup result establishes an RTX 4060 demo
benchmark or minimum consumer specification. Local-network access remains disabled until
its authentication and transport design is implemented.
