"""Run the folder capture loop in a background thread, beside the local server.

This is what makes `START.cmd` useful rather than merely informative: a person double-clicks
it, the setup page opens, and anything they drop into the inbox from that moment is filed.
The loop owns its own database connection — a connection is not thread-safe and the server
thread must never wait on it.

Nothing here parses, embeds or extracts, and since ADR 0008 it does not wait for anything that
does. A document is registered and handed to the worker; the thread is back watching the folder
inside a few milliseconds, so five scans dropped at once are five lines in the log, not one line
and a forty-second silence.

When the broker does not answer, capture still works — it falls back to reading documents on
this thread, and says so in as many words. A quiet fallback would be worse than the stall: the
watcher would block for seconds per document and nobody would know why.
"""

from __future__ import annotations

import logging
import threading
import time
from pathlib import Path

from core.adapters.folder import FolderAdapter, FolderSettings
from core.ingest.dispatch import Dispatcher, Inline, queued
from core.ingest.intake import Intake
from core.runtime.db import DatabaseUnavailable, connect
from core.runtime.ollama import Ollama
from core.runtime.settings import Settings

log = logging.getLogger("parrot.capture")


def broker_available(settings: Settings, timeout: float = 2.0) -> bool:
    """Whether Redis answers. Not whether a worker is listening — `core/runtime/checks.py`
    asks that, and it needs Celery to do it."""
    try:
        from redis import Redis
        from redis.exceptions import RedisError
    except ImportError:  # pragma: no cover - the dependency is declared
        return False
    try:
        with Redis.from_url(
            settings.redis_url, socket_connect_timeout=timeout, socket_timeout=timeout
        ) as client:
            client.ping()
        return True
    except (RedisError, ValueError, OSError):
        return False


class FolderCapture:
    """A daemon thread that polls the watched folder until `stop()` or process exit."""

    def __init__(
        self, settings: Settings, poll_seconds: float = 1.0, *, use_queue: bool | None = None
    ) -> None:
        self._settings = settings
        self._poll = poll_seconds
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._use_queue = use_queue
        self.folder = Path(settings.watch_folder)

    def start(self) -> bool:
        """Begin watching. Returns False, with a logged reason, when it cannot."""
        try:
            self.folder.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            log.warning("Capture is off: cannot use %s (%s)", self.folder, error)
            return False
        self._thread = threading.Thread(target=self._run, name="parrot-capture", daemon=True)
        self._thread.start()
        return True

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=self._poll * 3)

    def _dispatcher(self, conn: object) -> Dispatcher:
        """Queue the work when there is somewhere to queue it; otherwise say what we are doing."""
        wanted = broker_available(self._settings) if self._use_queue is None else self._use_queue
        if wanted:
            try:
                dispatch = queued(self._settings)
            except ImportError:
                log.warning("Ingestion is inline: Celery is not installed. Run uv sync.")
            else:
                log.info("Ingestion is queued. Documents are read by the worker, not here.")
                return dispatch
        else:
            log.warning(
                "Ingestion is inline: the queue broker did not answer, so this watcher will "
                "pause for several seconds on each document. Start it with "
                "`docker compose -f infra/docker-compose.yml up -d redis`."
            )
        return Inline(conn, Ollama(self._settings))

    def _run(self) -> None:
        try:
            with connect(self._settings) as conn:
                intake = Intake(conn, self._dispatcher(conn))
                adapter = FolderAdapter(
                    intake, FolderSettings(self.folder, poll_seconds=self._poll)
                )
                log.info("Capture is on. Drop a document into %s", self.folder)
                while not self._stop.wait(self._poll):
                    self._tick(adapter)
        except DatabaseUnavailable as error:
            log.warning("Capture is off: %s", error)

    def _tick(self, adapter: FolderAdapter) -> None:
        try:
            adapter.poll(self._poll)
        except Exception:
            log.exception("Capture skipped a poll and will try again in %.0fs", self._poll)
            time.sleep(self._poll)
