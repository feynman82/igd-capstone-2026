# `core/adapters/` — capture adapters

**Owner: Christian.**

One interface, any number of transports:

```python
receive(bytes, mime, sender, ts) -> ingest_job
```

The requirement is that people photograph a document with the phone already in their
hand. Which chat application carries the photograph is a configuration choice, not an
architectural one — that is the whole point of the contract.

| Adapter | Status | Note |
|---|---|---|
| `folder.py` | MVP | Debounced watchdog on a local directory |
| `telegram.py` | MVP | Free, no business verification, one day of work |
| `whatsapp.py` | Post-MVP | Official Cloud API only; per-message cost from 1 Oct 2026 |
| `drive.py` | Post-MVP | Nightly poll, OAuth scoped to one folder, read-only |

## Rules

Capture channels are **transports**. Media is fetched, filed locally, and deleted at
source. Nothing about a document persists off the machine — that is the claim in
`docs/governance/` and this directory is where it is either true or not.
