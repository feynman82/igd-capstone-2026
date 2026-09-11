# 8. Ingestion runs on a Celery worker, and the queue carries a digest rather than the document

Date: 2026-09-11 · Status: accepted

## Context

`core/runtime/capture.py` ran the whole pipeline — Docling parse, classify, schema-constrained
extraction, embedding, both lanes committed together — on the thread that noticed the file.
A PDF took about eight seconds. During those eight seconds the watcher was not watching, so a
person dropping five scans at once watched the fifth wait forty seconds behind the first four,
and a restart in the middle of it lost the poll rather than the parse.

Celery and Redis have been in the stack since the proposal and in `infra/docker-compose.yml`
since week 2. Nothing used them. `core/ingest/README.md` has said "FastAPI + Celery + Redis"
the whole time, which made the README a plan rather than a description.

Three things had to be decided.

**What crosses the broker.** The obvious message is the document itself. `MAX_BYTES` in the
folder adapter is 64 MB, and a broker holding 64 MB messages is a broker that falls over on a
day somebody scans a folder of photographs.

**Where the boundary sits.** Registration is one SHA-256 and one upsert — milliseconds. Reading
a document is seconds. Putting both behind the queue would mean a person who drops a file sees
nothing at all until a worker gets to it, and `Intake._needs_work`, which is what stops an
already-indexed document being re-read, would move off the capture thread and stop saving
anything.

**What happens with no broker.** The demonstration machine is a Windows workstation with Docker
on it, and Docker on that machine has failed before (`docs/RUNNING.md`, 2026-09-11).

## Decision

**The pipeline does not change.** `core.ingest.pipeline.process`, `quarantine.retry`,
`modules.reminder.sweep` and `modules.alert.sweep` are called by the worker exactly as the
scripts call them. `core/worker/tasks.py` is plumbing, and logic that appears there is logic the
scripts and the worker will eventually disagree about.

**Registration stays on the capture thread; reading moves off it.** `Intake` is handed a
dispatcher — `Inline` runs the pipeline here, `Queued` sends a message and returns. The
`filed: policy-schedule.pdf [application/pdf]` line still appears immediately, the already-indexed
check still happens before anything is sent, and the watcher is back polling in milliseconds.

**The queue carries `{document_id, digest, mime, original_name}` and the worker finds the file
again by hashing the inbox.** v1 keeps the inbox as the document store, so the bytes are already
on disk and sending them twice would be the only copy in the system. A path was considered and
rejected: a path is a guess the moment somebody tidies their folder, while the SHA-256 is what
the `documents` row is keyed on. `core/ingest/source.py` is the one implementation, and
`scripts/quarantine.py` — which has resolved bytes this way since the quarantine queue landed —
now uses it too. The cost is hashing the inbox once per task: a few milliseconds against eight
seconds of parsing, for a folder that holds a household's week. If the inbox ever grows to
thousands of files, store the path alongside the digest and verify it; do not remove the digest.

**Concurrency is one.** Ollama is one endpoint in front of one graphics card. Two documents
parsing and embedding at once do not finish sooner, they finish later together. Five documents
still take about forty seconds in total. What the queue buys is that the *watcher* is free the
whole time, the five appear as five filed lines at once, and the work survives a restart. Saying
it buys parallelism would be false, and the demonstration should not claim it.

On Windows the pool is `solo`: the prefork pool does not work there, and a worker that silently
fails to start is worse than a slower pool.

**No broker means inline, loudly.** `FolderCapture` pings Redis at startup and logs one of two
lines — queued, or "this watcher will pause for several seconds on each document" with the
command to fix it. A quiet fallback would be the worst of both: the old stall, and nobody
knowing why. `scripts/run_parrot.py` prints the same reasoning when it cannot start the worker,
and the server comes up regardless.

**The beat schedule is read from the modules' manifests.** `modules/reminder/module.yaml`
already declares `cron: "0 7 * * *"`; `core/worker/schedule.py` parses and validates it rather
than writing 07:00 down a second time.

Alert is the exception. Its manifest declares `on: fact_write`, which is the right trigger and
is not built. Until it is, Alert is swept nightly at 07:05 and its own 168-hour debounce is what
stops a nightly sweep becoming a nightly notification. The manifest is not edited to match:
the manifest describes the design, and `ALERT_FALLBACK_CRON` describes today. When `fact_write`
lands, that constant and this paragraph go together.

## Consequences

A document is now read by a process that is not the one that captured it, so a failure there is
one line in the worker's log rather than in the watcher's. `core/runtime/checks.py` grew an
"Ingestion worker" check because a reachable broker and no worker is now a real failure mode —
documents would register, queue, and sit there looking filed while nothing read them. The setup
page reports it.

Tasks are `acks_late` with `reject_on_worker_lost`: a worker killed mid-parse means the document
is read again. That is safe because the pipeline is idempotent on the SHA-256 — it rewrites the
same rows — and it is the right way round, because losing a document is worse than reading one
twice.

`START.cmd` now starts three things. They fail independently, and the one a person is looking at
is the one that always comes up.

No runtime dependency is added: `celery>=5.4` and `redis>=5.2` have been declared since the
first `pyproject.toml`. This record exists because the decision changed, not because rule 5
required it.
