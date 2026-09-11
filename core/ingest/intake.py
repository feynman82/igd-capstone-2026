"""What every capture channel hands a document to.

An adapter's job ends at "these bytes arrived, with this name, from this channel". Intake takes
it from there: register, then arrange for the document to be read, then say in one line what
happened. Because it satisfies the `Registrar` protocol, the folder adapter and the Telegram
adapter use the same one and cannot drift apart.

Registration commits on its own before anything is read. That is deliberate: parsing a scan
takes seconds and the model may be cold, and a document that is registered but not yet indexed
is a document we can still see and retry. A document lost because the worker died mid-parse is
not.

*How* it is read is the dispatcher's business, not Intake's. `Inline` runs the pipeline on this
thread; `Queued` puts it on Redis and comes straight back. See `core/ingest/dispatch.py`.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from core.ingest.dispatch import Dispatcher
from core.ingest.register import Registration, register_document

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Intake:
    conn: Any
    dispatch: Dispatcher | None = None

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

        if self.dispatch is not None and self._needs_work(registration):
            log.info(
                "  %s",
                self.dispatch(
                    registration, payload=payload, mime=mime, original_name=original_name
                ),
            )
        return registration

    def _needs_work(self, registration: Registration) -> bool:
        """An already-indexed document is not read again. Re-reading it would burn a minute of
        model time to write the same rows, and the SHA-256 says the bytes have not changed.

        This check stays on the capture thread on purpose: the cheapest queue message is the
        one never sent.
        """
        return registration.status != "indexed"
