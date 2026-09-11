# `core/adapters/` — capture adapters

**Owner: Christian.**

One interface, any number of transports:

```python
receive(payload, mime, sender, ts, *, original_name) -> IngestJob
```

`original_name` is keyword-only and is the one addition to the four-parameter shorthand this
file used to carry. A channel knows both who sent a document and what the file was called,
`documents.original_name` is NOT NULL, and folding a filename into `sender` would lose it.
Nothing in `core/contracts.py` is involved: a capture adapter is transport, not a contract.

The requirement is that people photograph a document with the phone already in their
hand. Which chat application carries the photograph is a configuration choice, not an
architectural one — that is the whole point of the contract.

| Adapter | Status | Note |
|---|---|---|
| `folder.py` | Built | Polled for stability rather than subscribed to events — ADR 0005 |
| `telegram.py` | Built | Long polling, not a webhook: nothing listens on a public port |
| `whatsapp.py` | Post-MVP | Official Cloud API only; per-message cost from 1 Oct 2026 |
| `drive.py` | Post-MVP | Nightly poll, OAuth scoped to one folder, read-only |

## Rules

Capture channels are **transports**. Media is fetched, filed locally, and deleted at
source. Nothing about a document persists off the machine — that is the claim in
`docs/governance/` and this directory is where it is either true or not.
