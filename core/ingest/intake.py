"""What every capture channel hands a document to.

An adapter's job ends at "these bytes arrived, with this name, from this channel". Intake takes
it from there: register, then run the pipeline, then say in one line what happened. Because it
satisfies the `Registrar` protocol, the folder adapter and the Telegram adapter use the same
one and cannot drift apart.

Registration commits on its own before parsing starts. That is deliberate: parsing a scan takes
seconds and the model may be cold, and a document that is registered but not yet indexed is a
document we can still see and retry. A document lost because the worker died mid-parse is not.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from core.ingest.pipeline import Outcome, process
from core.ingest.register import Registration, register_document
from core.runtime.ollama import Ollama

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Intake:
    conn: Any
    client: Ollama
    process_documents: bool = True

    def __call__(
        self,
        *,
        payload: bytes,
        mime: str,
        original_name: str,
        source_channel: str,
        synthetic: bool = False,
    ) -> Registration:
        registration = register_document(
            self.conn,
            payload=payload,
            mime=mime,
            original_name=original_name,
            source_channel=source_channel,
            synthetic=synthetic,
        )
        self.conn.commit()

        verb = "already filed" if registration.already_registered else "filed"
        log.info("%s: %s [%s] -> %s", verb, original_name, mime, registration.document_id)

        if self.process_documents and self._needs_work(registration):
            outcome = self._run(registration, payload, mime, original_name)
            log.info("  %s", outcome.line())
        return registration

    def _needs_work(self, registration: Registration) -> bool:
        """An already-indexed document is not re-parsed. Re-parsing it would burn a minute of
        model time to write the same rows, and the SHA-256 says the bytes have not changed."""
        return registration.status != "indexed"

    def _run(
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
