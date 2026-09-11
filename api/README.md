# `api/` — the FastAPI application

**Owner: Christian.**

Thin. Routes, response models, dependency wiring. Everything it exposes is implemented in
`core/` or `modules/`; nothing is implemented here. When a handler starts to contain a rule,
that rule has escaped from the core and belongs back there.

```
api/
  main.py     app factory, TrustedHost, the lifespan, the setup page, /healthz and /readyz
  models.py   the response shapes Lane D draws against. Nothing here queries anything
  routes.py   one handler per endpoint, each a translation from a dataclass and back
```

There is no CORS middleware and that is deliberate: the Next.js interface in `web/` proxies
every call through its own route handlers, so each request arrives same-origin from 127.0.0.1
and no other origin is ever granted one.

## The surface

| | | |
|---|---|---|
| `GET` | `/api/today` | Reminders, alerts and overdue items, already ordered by urgency |
| `POST` | `/api/ask` | One question. Answers, abstains or refuses — `kind` says which |
| `GET` | `/api/vault` | A page of documents with the facts read off each |
| `GET` | `/api/documents/{id}` | One document and its facts, shown even if its pack is off |
| `GET` | `/api/documents/{id}/page/{n}` | **The page, drawn.** The only endpoint returning bytes |
| `PATCH` | `/api/facts/{id}` | "That is not what the paper says" |
| `POST` | `/api/obligations/{id}/close` | `done`, or `dismissed` |
| `POST` | `/api/obligations/{id}/snooze` | Quiet until the next lead window, and says when that is |
| `GET` | `/api/packs` | Installed packs and modules |
| `PATCH` | `/api/packs/{id}` · `/api/modules/{id}` | Switch one on or off |
| `GET` | `/api/quarantine` | What needs a person's eyes, and what cannot be retried |
| `POST` | `/api/quarantine/{id}/retry` | 202 and a task id. The worker does the reading |

## Five properties worth knowing before you change anything

**`GET /api/today` never marks anything as notified.** `reminder.sweep` is always called with
`mark=False`. Opening a screen is not being reminded, and a GET that consumed a lead window
would mean somebody who refreshed twice had used up their thirty-day warning.

**Every response that states something carries its source.** A `TodayItem` has `sources`, a
`VaultFact` has a `page`, a `Claim` has `citations` — and each of those is a `Source` carrying
a `document_id`, so a citation chip is something a person can open rather than something they
have to go and find. `models.py` has no type that can express a fact without saying where it
came from, which is rules 2 and 3 showing up in the API surface rather than only in the
database.

**The names in a citation are resolved once per response, not once per chip.** The modules and
the answer graph format a citation the way a person says it, "policy.pdf, page 1", and by the
time it reaches a handler the id has been thrown away. `vault.resolve_names` puts it back in
one query. Where two documents share a name the most recently filed one wins — a guess, and the
only one in the file. The real fix is for a citation to carry the id, which is a change to the
answer graph.

**Three endpoints let a person write, and none of them can invent a row.** A correction never
touches `document_id` or `page`, so rule 2 survives the one path where a human edits a fact,
and what the field used to say is written to `traces` under `node = 'correction'` — an UPDATE
on its own would lose the labelled example that is most of the reason for collecting it.

**Snooze means "not until this gets more urgent", not "not for N days".** It stamps
`last_notified_at`, which is what `already_said` already reads, so a pack's own lead windows
decide when the row comes back and no column was added. A person cannot say "next Tuesday";
that needs `obligations.snoozed_until`, which is a migration and therefore its own pull request.

## Rules

`packs/` and `modules/` must never import from here. The dependency runs one way: the API
knows about the core; the core does not know an API exists.
