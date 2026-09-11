"""What happens to a document between "these bytes are registered" and "this document is read".

Registration is milliseconds: one SHA-256 and one upsert. Reading a document is seconds —
Docling parses it, the classifier looks at it, the generator extracts against a pack's schema,
the embedder walks its chunks. Doing the second on the thread that noticed the file means a
person dropping five scans watches the fifth wait forty seconds behind the first four.

So `Intake` is handed a dispatcher, and there are two.

`Inline` is the original behaviour, kept because it is what a one-shot demo, a test and a
machine with no broker actually want, and because it is the only one that can report the
outcome in the same breath as the filing.

`Queued` puts a small message on Redis and returns. The bytes do not travel: the message
carries the document id and the digest, and the worker finds the file again through
`core/ingest/source.py`. A 64 MB scan has no business in a broker, and the inbox is already
the document store.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Protocol

from core.ingest.pipeline import Outcome, process
from core.ingest.register import Registration
from core.runtime.ollama import Ollama

log = logging.getLogger(__name__)


class Dispatcher(Protocol):
    """Given a registered document, arrange for it to be read. Says what it arranged."""

    def __call__(
        self, registration: Registration, *, payload: bytes, mime: str, original_name: str
    ) -> str: ...


class Send(Protocol):
    """Put one ingestion message on the queue and return its task id."""

    def __call__(self, *, document_id: str, digest: str, mime: str, original_name: str) -> str: ...


@dataclass(frozen=True, slots=True)
class Inline:
    """Run the pipeline here and now, and report what it decided."""

    conn: Any
    client: Ollama

    def __call__(
        self, registration: Registration, *, payload: bytes, mime: str, original_name: str
    ) -> str:
        return self.run(registration, payload, mime, original_name).line()

    def run(
        self, registration: Registration, payload: bytes, mime: str, original_name: str
    ) -> Outcome:
        try:
            return process(
                self.conn,
                self.client,
                document_id=registration.document_id,
                payload=payload,
                mime=mime,
                original_name=original_name,
            )
        except Exception:
            # The document row survives with status 'pending'. Losing the worker is worse than
            # losing the parse, and a pending document is visible and retryable.
            self.conn.rollback()
            log.exception("the pipeline failed on %s; it stays pending", original_name)
            return Outcome(registration.document_id, "pending", 0, None, None, 0, 0, "not yet read")


@dataclass(frozen=True, slots=True)
class Queued:
    """Hand the document to the worker and go back to watching the folder."""

    send: Send

    def __call__(
        self, registration: Registration, *, payload: bytes, mime: str, original_name: str
    ) -> str:
        task_id = self.send(
            document_id=str(registration.document_id),
            digest=registration.sha256.hex(),
            mime=mime,
            original_name=original_name,
        )
        return f"queued for the worker as {task_id}"


def queued(settings: Any) -> Queued:
    """A `Queued` bound to this configuration's broker.

    Celery is imported here rather than at module scope so that a machine with no broker —
    a test, a one-shot demo — never loads it at all.
    """
    from core.worker.tasks import sender

    return Queued(sender(settings))
