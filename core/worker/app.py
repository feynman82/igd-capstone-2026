"""The one Celery application, built from `Settings`.

Every setting here is a consequence of what this worker actually is: a single local process,
reading household documents, in front of one GPU.

`concurrency=1` because Ollama is one endpoint on one graphics card. Two documents parsing and
embedding at once do not finish sooner; they finish later, together. The queue is what makes
five documents tolerable, not parallelism.

`acks_late` with `reject_on_worker_lost` because a document is worth re-reading if the worker
dies mid-parse. The pipeline is idempotent on a SHA-256 — re-running it rewrites the same rows
— so at-least-once delivery is the safe side to err on.

`solo` on Windows because the prefork pool does not work there; the workstation this runs on
is a Windows machine and a worker that silently fails to start is worse than a slower pool.

JSON only, and no pickle: the message carries a document id and a digest, and a broker that
can be persuaded to unpickle is a broker that can be persuaded to execute.
"""

from __future__ import annotations

import sys
from typing import Any

from core.runtime.settings import Settings
from core.worker.schedule import beat_schedule

INGEST_QUEUE = "ingest"


def build(settings: Settings) -> Any:
    """Construct the Celery application. Imported lazily by callers so that nothing which
    merely registers a document has to load Celery."""
    from celery import Celery

    app = Celery("parrot", broker=settings.redis_url, backend=settings.redis_url)
    app.conf.update(
        task_default_queue=INGEST_QUEUE,
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        result_expires=3600,
        timezone="Asia/Singapore",
        enable_utc=True,
        worker_concurrency=1,
        worker_prefetch_multiplier=1,
        worker_pool="solo" if sys.platform == "win32" else "prefork",
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        task_track_started=True,
        broker_connection_retry_on_startup=True,
        beat_schedule=beat_schedule(),
    )
    return app
