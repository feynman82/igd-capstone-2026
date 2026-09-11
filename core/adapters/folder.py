"""The watched-folder capture adapter.

A person drops a scan into a folder and it is registered within a minute. That is the whole
behaviour, and almost all of the work is in *not* registering a file too early: a scanner
writing a 4 MB PDF, a phone syncing a photograph and a browser finishing a download all
present a file that exists but is not yet complete.

Debounce is therefore by stability rather than by filesystem event. A file is ready when its
size and modification time have not changed for `stable_seconds`. At the default one-second
poll and three-second window a file is registered about four seconds after the copy finishes,
well inside the sixty seconds the task asks for, and a half-written file is never read.

There is no `watchdog` dependency: see `docs/adr/0005-polling-the-watched-folder.md`.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from core.adapters.base import IngestJob, sniff_mime
from core.ingest.register import Registrar

log = logging.getLogger(__name__)

CHANNEL = "folder"

# Names an operating system or an application is still writing to. Registering one of these
# would capture a fragment and give it a SHA-256 that the finished file will never match.
PARTIAL_SUFFIXES = frozenset({".part", ".crdownload", ".tmp", ".download", ".filepart"})
IGNORED_PREFIXES = (".", "~$")

MAX_BYTES = 64 * 1024 * 1024  # a household document; anything larger is a mistake, not a scan


@dataclass(frozen=True, slots=True)
class FolderSettings:
    root: Path
    stable_seconds: float = 3.0
    poll_seconds: float = 1.0
    max_bytes: int = MAX_BYTES


@dataclass(slots=True)
class _Pending:
    size: int
    mtime: float
    stable_for: float = 0.0
    last_seen: float = 0.0


@dataclass(slots=True)
class _Registered:
    size: int
    mtime: float


class FolderAdapter:
    """Satisfies `CaptureAdapter`. Holds no database handle — it is given a `Registrar`."""

    channel = CHANNEL

    def __init__(self, registrar: Registrar, settings: FolderSettings) -> None:
        self._register = registrar
        self._settings = settings
        self._pending: dict[Path, _Pending] = {}
        self._registered: dict[Path, _Registered] = {}
        self._clock = 0.0

    # ------------------------------------------------------------------ the interface

    def receive(
        self,
        payload: bytes,
        mime: str,
        sender: str,
        ts: datetime,
        *,
        original_name: str,
    ) -> IngestJob:
        registration = self._register(
            payload=payload,
            mime=mime,
            original_name=original_name,
            source_channel=self.channel,
        )
        return IngestJob(
            document_id=registration.document_id,
            sha256=registration.sha256,
            source_channel=registration.source_channel,
            original_name=original_name,
            mime=registration.mime,
            received_at=ts,
            ingested_at=registration.ingested_at,
            already_registered=registration.already_registered,
        )

    # ------------------------------------------------------------------- the debounce

    def candidates(self) -> Iterator[Path]:
        """Every file in the watched folder that is worth looking at at all."""
        root = self._settings.root
        if not root.is_dir():
            return
        for path in sorted(root.iterdir()):
            if not path.is_file():
                continue
            name = path.name
            if name.startswith(IGNORED_PREFIXES):
                continue
            if path.suffix.lower() in PARTIAL_SUFFIXES:
                continue
            yield path

    def observe(self, elapsed: float) -> list[Path]:
        """Advance the debounce by `elapsed` seconds and return the files now ready.

        Time is passed in rather than read from a clock so the behaviour is testable without
        a test that sleeps. The runner in `scripts/watch_folder.py` supplies real time.
        """
        self._clock += elapsed
        ready: list[Path] = []
        seen: set[Path] = set()

        for path in self.candidates():
            try:
                stat = path.stat()
            except OSError:  # vanished or locked between listing and stat; try again next poll
                continue
            seen.add(path)

            done = self._registered.get(path)
            if done is not None and done.size == stat.st_size and done.mtime == stat.st_mtime:
                continue  # unchanged since we filed it

            pending = self._pending.get(path)
            if pending is None or pending.size != stat.st_size or pending.mtime != stat.st_mtime:
                self._pending[path] = _Pending(stat.st_size, stat.st_mtime, 0.0, self._clock)
                continue

            pending.stable_for += elapsed
            pending.last_seen = self._clock
            if pending.stable_for >= self._settings.stable_seconds and stat.st_size > 0:
                ready.append(path)

        for gone in set(self._pending) - seen:
            del self._pending[gone]
        for gone in set(self._registered) - seen:
            del self._registered[gone]
        return ready

    # ------------------------------------------------------------------------ the poll

    def poll(self, elapsed: float, now: datetime | None = None) -> list[IngestJob]:
        """One debounce tick, then register whatever it declared ready."""
        stamp = now or datetime.now(UTC)
        jobs: list[IngestJob] = []
        for path in self.observe(elapsed):
            job = self._capture(path, stamp)
            if job is not None:
                jobs.append(job)
        return jobs

    def _capture(self, path: Path, stamp: datetime) -> IngestJob | None:
        try:
            stat = path.stat()
            if stat.st_size > self._settings.max_bytes:
                log.warning(
                    "skipping %s: %d bytes is larger than a household document", path, stat.st_size
                )
                self._pending.pop(path, None)
                self._registered[path] = _Registered(stat.st_size, stat.st_mtime)
                return None
            payload = path.read_bytes()
        except OSError as error:
            log.warning("could not read %s: %s", path, error)
            self._pending.pop(path, None)
            return None

        job = self.receive(
            payload,
            sniff_mime(payload, path.name),
            str(self._settings.root),
            stamp,
            original_name=path.name,
        )
        self._pending.pop(path, None)
        self._registered[path] = _Registered(stat.st_size, stat.st_mtime)
        return job
