# `api/` — the FastAPI application

**Owner: Christian.**

Thin. Routes, request and response models, dependency wiring. Everything it exposes is
implemented in `core/` or `modules/`; nothing is implemented here.

```
api/
  main.py       app factory, middleware, the /healthz nobody thinks about until demo night
  routes/       ask.py · documents.py · packs.py · obligations.py
  deps.py       db session, the Ollama client, the current pack registry
  schemas.py    request/response models — NOT the extraction schemas, those are generated
```

## Rules

`packs/` and `modules/` must never import from here. The dependency runs one way: the API
knows about the core; the core does not know an API exists.
