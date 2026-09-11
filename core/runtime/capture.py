"""Run the folder capture loop in a background thread, beside the local server.

This is what makes `START.cmd` useful rather than merely informative: a person double-clicks
it, the setup page opens, and anything they drop into the inbox from that moment is filed.
The loop owns its own database connection — a connection is not thread-safe and the server
thread must never wait on it.

Nothing here parses, embeds or extracts. It registers, and says so.
"""

from __future__ import annotations

import logging
import threading
import time
from pathlib import Path

from core.adapters.folder import FolderAdapter, FolderSettings
from core.ingest.intake import Intake
from core.runtime.db import DatabaseUnavailable, connect
from core.runtime.ollama import Ollama
from core.runtime.settings import Settings

log = logging.getLogger("parrot.capture")


class FolderCapture:
    """A daemon thread that polls the watched folder until `stop()` or process exit."""

    def __init__(self, settings: Settings, poll_seconds: float = 1.0) -> None:
        self._settings = settings
        self._poll = poll_seconds
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
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

    def _run(self) -> None:
        try:
            with connect(self._settings) as conn:
                intake = Intake(conn, Ollama(self._settings))
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
