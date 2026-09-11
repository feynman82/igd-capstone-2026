"""The Celery worker: the process that reads documents, and the nightly sweeps.

Three modules, and the split is the point:

- `app.py` builds the Celery application from `Settings`. Nothing else constructs one.
- `tasks.py` holds the work. Every task is a plain, typed function that is registered with
  Celery afterwards, so it can be called — and tested — with no broker anywhere.
- `schedule.py` is the beat schedule, read from each module's own `module.yaml`.

Why this exists at all is `docs/adr/0008-ingestion-runs-on-a-celery-worker.md`.
"""
