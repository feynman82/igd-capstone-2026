"""Run the capture loops in background threads, beside the local server.

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

**Two channels, one shape.** `FolderCapture` watches the inbox and `TelegramCapture` long-polls
the bot, and past their transport they are the same thread doing the same thing: own a
connection, pick a dispatcher, register what arrives. Telegram used to start only from
`scripts/telegram_bot.py`, so a household that double-clicked `START.cmd` had a bot that
received photographs and a Parrot that never saw one. A capture channel nothing starts is not a
capture channel.
"""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from core.adapters.folder import FolderAdapter, FolderSettings
from core.adapters.telegram import TelegramAdapter, TelegramSettings, TelegramUnavailable
from core.ingest.dispatch import Dispatcher, Inline, queued
from core.ingest.intake import Intake
from core.runtime.db import DatabaseUnavailable, connect
from core.runtime.ollama import Ollama
from core.runtime.settings import Settings

log = logging.getLogger("parrot.capture")

# How long the Telegram loop waits after a failed poll before asking again. Long enough that a
# bot Telegram will never hand messages to -- a webhook is set, another poller holds it -- does
# not fill the window with the same sentence, short enough that a dropped connection recovers
# without a person noticing.
TELEGRAM_RETRY_SECONDS = 15.0


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


def dispatcher_for(
    settings: Settings, conn: object, use_queue: bool | None, channel: str
) -> Dispatcher:
    """Queue the work when there is somewhere to queue it; otherwise say what we are doing.

    Shared by both capture channels so they cannot disagree about where a document is read. The
    channel name is in the log line because two threads say this on startup and "ingestion is
    inline" means something different depending on which loop is about to block.
    """
    wanted = broker_available(settings) if use_queue is None else use_queue
    if wanted:
        try:
            dispatch = queued(settings)
        except ImportError:
            log.warning("%s ingestion is inline: Celery is not installed. Run uv sync.", channel)
        else:
            log.info("%s ingestion is queued. Documents are read by the worker, not here.", channel)
            return dispatch
    else:
        log.warning(
            "%s ingestion is inline: the queue broker did not answer, so this loop will pause "
            "for several seconds on each document. Start it with "
            "`docker compose -f infra/docker-compose.yml up -d redis`.",
            channel,
        )
    return Inline(conn, Ollama(settings))


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

    def _run(self) -> None:
        try:
            with connect(self._settings) as conn:
                intake = Intake(
                    conn, dispatcher_for(self._settings, conn, self._use_queue, "Folder")
                )
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


class TelegramCapture:
    """A daemon thread that long-polls the Telegram bot until `stop()` or process exit.

    The same shape as `FolderCapture` and for the same reasons: its own connection, because one
    is not thread-safe and the server thread must never wait on it; a dispatcher chosen the same
    way, so a photograph from a phone and a scan from the inbox are read by the same worker.

    It starts only when a token is configured. A household that has not registered a bot is the
    normal case, and a thread that exists to log "no token" every few seconds is noise.
    """

    def __init__(self, settings: Settings, *, use_queue: bool | None = None) -> None:
        self._settings = settings
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._use_queue = use_queue
        self.inbox = Path(settings.watch_folder)

    def start(self) -> bool:
        """Begin polling. Returns False, with a logged reason, when it cannot or should not.

        Deliberately does not call `getMe` first. A network round trip on the startup path
        delays the engine for a check the first poll makes anyway, and `_run` reports a bad
        token in the same sentence it would report any other refusal.
        """
        if not self._settings.telegram_configured:
            log.info("Telegram capture: off. No TELEGRAM_BOT_TOKEN in .env — see docs/RUNNING.md.")
            return False
        self._thread = threading.Thread(target=self._run, name="parrot-telegram", daemon=True)
        self._thread.start()
        return True

    def stop(self) -> None:
        self._stop.set()
        # Long polling holds a request open for up to 30 seconds, so this thread does not stop
        # promptly and is not waited on for long. It is a daemon and holds nothing a shutdown
        # needs: the document it may be mid-way through is registered or it is not, and either
        # way the bytes are in the inbox and the message is still in the chat.
        if self._thread is not None:
            self._thread.join(timeout=2.0)

    def _adapter(self, conn: Any) -> TelegramAdapter:
        settings = TelegramSettings(
            token=self._settings.telegram_token,
            allowed_chat_ids=self._settings.telegram_chat_ids,
            delete_after_fetch=self._settings.telegram_delete_at_source,
        )
        intake = Intake(conn, dispatcher_for(self._settings, conn, self._use_queue, "Telegram"))
        return TelegramAdapter(intake, settings, attribution(conn))

    def _run(self) -> None:
        try:
            with connect(self._settings) as conn:
                adapter = self._adapter(conn)
                where = "any chat" if not self._settings.telegram_chat_ids else "the allowed chats"
                log.info("Telegram capture is on, accepting documents from %s.", where)
                while not self._stop.is_set():
                    self._tick(adapter)
        except DatabaseUnavailable as error:
            log.warning("Telegram capture is off: %s", error)
        except TelegramUnavailable as error:
            log.warning("Telegram capture is off: %s", error)

    def _tick(self, adapter: TelegramAdapter) -> None:
        """One long poll. A failure waits rather than hammering the API with the same request."""
        try:
            adapter.poll_once(self.inbox)
        except TelegramUnavailable as error:
            # Already a sentence a person can act on — `_status_reason` in the adapter turns a
            # 409 into "a webhook is set or something else is polling this bot".
            log.warning("Telegram capture paused: %s", error)
            self._stop.wait(TELEGRAM_RETRY_SECONDS)
        except Exception:
            log.exception("Telegram capture skipped a poll and will try again")
            self._stop.wait(TELEGRAM_RETRY_SECONDS)


def attribution(conn: Any) -> Callable[[Any, int], None]:
    """Whose phone this arrived on, recorded before anything is read off it. See ADR 0011.

    Silent when the chat is not linked to anybody: most installs never link one, and a bot that
    refused documents from unmapped chats would be a worse bot.
    """

    def attribute(document_id: Any, chat_id: int) -> None:
        from core import household

        person_id = household.person_for_chat(conn, chat_id)
        if person_id is not None:
            household.attribute(conn, document_id, person_id, source="telegram")
            conn.commit()  # autocommit is off; the caller commits

    return attribute
