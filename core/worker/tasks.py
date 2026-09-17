"""The work the queue carries: read a document, retry quarantine, sweep the two modules.

Every task here is two things stacked. Underneath is a plain function with real type hints
that takes a connection and does the work — callable from a test, from a script, from a REPL,
with no broker in the room. On top, `register()` hands that function to Celery by name.

It is written that way deliberately rather than with `@app.task`. A decorator supplied by an
untyped library erases the signature it decorates, and `mypy --strict` runs over `core/`; more
usefully, a task you can only reach through a broker is a task you can only test through a
broker.

None of these functions reimplement anything. `ingest` calls `core.ingest.pipeline.process`
unchanged, `retry_quarantined` calls `core.ingest.quarantine.retry` unchanged, and the sweeps
call `modules.reminder.sweep` and `modules.alert.sweep` unchanged. This module is plumbing and
should stay that way — logic that appears here is logic that the command-line scripts and the
worker will eventually disagree about.
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import Any

from core import household
from core.ingest.pipeline import process
from core.ingest.quarantine import Recovery, queue, recovery_rate, retry
from core.ingest.source import SourceMissing, bytes_for, digest_of_document
from core.runtime.db import connect
from core.runtime.ollama import Ollama
from core.runtime.settings import Settings

log = logging.getLogger("parrot.worker")

ROOT = Path(__file__).resolve().parents[2]

INGEST = "parrot.ingest_document"
RETRY = "parrot.retry_quarantined"
RETRY_ONE = "parrot.retry_one_quarantined"
SWEEP_REMINDERS = "parrot.sweep_reminders"
SWEEP_ALERTS = "parrot.sweep_alerts"


# --------------------------------------------------------------------------- the work itself


def ingest(
    conn: Any,
    client: Ollama,
    *,
    document_id: str,
    digest: str,
    mime: str,
    original_name: str,
    folder: Path,
) -> str:
    """Read one registered document. The bytes are found again from the digest, not carried."""
    try:
        payload = bytes_for(bytes.fromhex(digest), folder)
    except SourceMissing as error:
        log.warning("%s stays pending: %s", original_name, error)
        return f"{original_name}: {error}"

    outcome = process(
        conn,
        client,
        document_id=document_id,
        payload=payload,
        mime=mime,
        original_name=original_name,
    )
    # Any name on this document that the household does not yet account for becomes a question
    # on Today. Deliberately after the document is filed rather than inside the pipeline: a
    # document that has been read should not also wait on a second model call before it counts
    # as filed, and a name that appears on six documents should be asked about once. A model
    # that is not running costs nothing here — the name is still recorded and still asked
    # about, simply without a suggestion attached. See ADR 0011.
    try:
        asked = household.sweep_unknown_subjects(conn, client)
        conn.commit()  # autocommit is off; `core/household.py` leaves the commit to its caller
        if asked:
            log.info("%s: %d new name(s) to place", original_name, asked)
    except Exception as error:  # placing a name must never fail a document that was read
        log.warning("could not place the names on %s: %s", original_name, error)

    log.info("%s: %s", original_name, outcome.line())
    return outcome.line()


def retry_quarantine(conn: Any, client: Ollama, *, limit: int, folder: Path) -> str:
    """The second pass over everything waiting for a person's eyes. Reports a recovery rate."""
    waiting = queue(conn, limit)
    recoveries: list[Recovery] = []
    for document in waiting:
        digest = digest_of_document(conn, document.document_id)
        if digest is None:
            continue
        try:
            payload = bytes_for(digest, folder)
        except SourceMissing as error:
            log.info("%s: %s", document.original_name, error)
            continue
        recoveries.append(
            retry(
                conn,
                client,
                document_id=document.document_id,
                payload=payload,
                mime=document.mime,
                original_name=document.original_name,
            )
        )
    line = recovery_rate(recoveries)
    log.info("%s", line)
    return line


def retry_one(conn: Any, client: Ollama, *, document_id: str, folder: Path) -> Recovery:
    """The second pass over exactly one document, which is what a person clicking Retry means.

    The bytes are found again from the digest rather than carried through the broker, the same
    way `ingest` does it: a message is a reference, never a document.
    """
    digest = digest_of_document(conn, document_id)
    if digest is None:
        raise SourceMissing(f"no document with id {document_id}")
    payload = bytes_for(digest, folder)  # raises SourceMissing when the file has been moved
    waiting = {str(document.document_id): document for document in queue(conn, limit=200)}
    document = waiting.get(str(document_id))
    if document is None:
        raise SourceMissing(f"document {document_id} is not in quarantine")
    recovery = retry(
        conn,
        client,
        document_id=document.document_id,
        payload=payload,
        mime=document.mime,
        original_name=document.original_name,
    )
    log.info(
        "%s: %s", document.original_name, "recovered" if recovery.recovered else "still quarantined"
    )
    return recovery


def sweep_reminders_now(conn: Any, today: date | None = None) -> str:
    from core.registry import enabled_pack_ids
    from modules import reminder

    due = reminder.sweep(conn, today, enabled=enabled_pack_ids(conn))
    for item in due:
        log.info("  %s", item.line())
    return f"{len(due)} reminder(s) due"


def sweep_alerts_now(conn: Any, today: date | None = None) -> str:
    from modules import alert

    firing = alert.sweep(conn, today)
    for item in firing:
        log.info("  ! %s", item.line())
    return f"{len(firing)} alert(s) fired"


# ------------------------------------------------------------------- what Celery actually runs
#
# Each of these opens its own connection and closes it. A worker process that holds a
# connection open between tasks holds it open across a database restart too, and psycopg
# connections are not thread-safe — one task, one connection, no sharing.


def _run_ingest(document_id: str, digest: str, mime: str, original_name: str) -> str:
    settings = Settings.load(ROOT)
    with connect(settings) as conn:
        return ingest(
            conn,
            Ollama(settings),
            document_id=document_id,
            digest=digest,
            mime=mime,
            original_name=original_name,
            folder=Path(settings.watch_folder),
        )


def _run_retry(limit: int = 25) -> str:
    settings = Settings.load(ROOT)
    with connect(settings) as conn:
        return retry_quarantine(
            conn, Ollama(settings), limit=limit, folder=Path(settings.watch_folder)
        )


def _run_retry_one(document_id: str) -> str:
    """One document, by id. The interface's Retry button lands here through the broker."""
    settings = Settings.load(ROOT)
    with connect(settings) as conn:
        try:
            recovery = retry_one(
                conn,
                Ollama(settings),
                document_id=document_id,
                folder=Path(settings.watch_folder),
            )
        except SourceMissing as error:
            return str(error)
    if recovery.recovered:
        return f"recovered {recovery.facts} cited fact(s) from {recovery.pages_read} page(s)"
    return f"still quarantined — {recovery.reason}"


def _run_reminders() -> str:
    settings = Settings.load(ROOT)
    with connect(settings) as conn:
        return sweep_reminders_now(conn)


def _run_alerts() -> str:
    settings = Settings.load(ROOT)
    with connect(settings) as conn:
        return sweep_alerts_now(conn)


def register(app: Any) -> Any:
    """Attach the tasks to a Celery application and return it."""
    app.task(name=INGEST, bind=False)(_run_ingest)
    app.task(name=RETRY, bind=False)(_run_retry)
    app.task(name=RETRY_ONE, bind=False)(_run_retry_one)
    app.task(name=SWEEP_REMINDERS, bind=False)(_run_reminders)
    app.task(name=SWEEP_ALERTS, bind=False)(_run_alerts)
    return app


def application(settings: Settings) -> Any:
    """The configured application with its tasks registered. One per process."""
    from core.worker.app import build

    return register(build(settings))


def sender(settings: Settings) -> Any:
    """Return something that puts one ingestion message on the queue and yields its task id.

    Bound to an application built once, so a folder full of documents costs one connection to
    the broker rather than one per file.
    """
    app = application(settings)

    def send(*, document_id: str, digest: str, mime: str, original_name: str) -> str:
        result = app.send_task(
            INGEST,
            kwargs={
                "document_id": document_id,
                "digest": digest,
                "mime": mime,
                "original_name": original_name,
            },
        )
        return str(result.id)

    return send


def send_retry(settings: Settings, document_id: str) -> str:
    """Put one quarantine retry on the queue and return its task id.

    The vision pass takes tens of seconds on a 4B model, which is longer than a person will
    hold a page open for. The interface gets a task id back and the worker does the reading —
    the same division of labour that stops a parse blocking the watched folder.
    """
    result = application(settings).send_task(RETRY_ONE, kwargs={"document_id": document_id})
    return str(result.id)
