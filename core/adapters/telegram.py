"""The Telegram capture adapter.

Same interface as the folder: `receive(payload, mime, sender, ts, *, original_name)`. Which chat
application carries a photograph is a configuration choice, and this file is the proof of that
claim — it is the second transport and it changed nothing downstream.

**Long polling, not a webhook.** A webhook needs a public HTTPS URL, which means a tunnel or a
hosted endpoint, which means household documents crossing a machine nobody on this team
controls. `getUpdates` is a request *out* from the laptop; nothing listens on a public port and
nothing is exposed. It costs a few seconds of latency and buys the privacy claim in
`docs/governance/`.

**Media is fetched, filed locally, and deleted at source.** After a photograph is written into
the inbox, the message is deleted from the chat. Telegram keeps no copy on the household's
behalf, which is what `core/adapters/README.md` promises.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import httpx

from core.adapters.base import IngestJob, sniff_mime
from core.ingest.register import Registrar

log = logging.getLogger(__name__)

CHANNEL = "telegram"
API = "https://api.telegram.org"
MAX_BYTES = 20 * 1024 * 1024  # what the bot API will hand back through getFile

# Things a person can send that are not a household document. Listed so that sending one gets an
# answer rather than silence; `photo` and `document` are the two this adapter actually takes.
UNSUPPORTED_MEDIA = frozenset(
    {"video", "video_note", "animation", "audio", "voice", "sticker", "contact", "location"}
)


class TelegramUnavailable(RuntimeError):
    """Safe to show: never contains the token."""


@dataclass(frozen=True, slots=True)
class TelegramSettings:
    token: str
    allowed_chat_ids: frozenset[int] = frozenset()
    poll_seconds: float = 2.0
    delete_after_fetch: bool = True

    @property
    def configured(self) -> bool:
        return bool(self.token.strip())


class TelegramAdapter:
    """Satisfies `CaptureAdapter`. Holds no database handle — it is given a `Registrar`."""

    channel = CHANNEL

    def __init__(
        self,
        registrar: Registrar,
        settings: TelegramSettings,
        attribute: Callable[[Any, int], None] | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if not settings.configured:
            raise TelegramUnavailable(
                "No Telegram bot token is configured. Set TELEGRAM_BOT_TOKEN in .env."
            )
        self._register = registrar
        self._settings = settings
        # The one seam a test needs. Everything else about this class is already injected, and a
        # capture adapter that can only be exercised against the live Bot API is one that is
        # never exercised -- which is how the launcher shipped without starting this at all.
        self._transport = transport
        # Whose chat this was, recorded against the document. Injected rather than imported
        # because attribution needs a connection and this class holds none -- the same reason
        # `registrar` is injected. `None` means nobody has linked any chats to any people,
        # which is every install until somebody does.
        #
        # This is the only ownership signal that arrives BEFORE the document is parsed: a
        # payslip photographed on Rachel's phone is Rachel's payslip, whatever the OCR makes
        # of the name at the top. Extraction may still read a different name off the page, and
        # when it does the disagreement becomes a question on Today rather than a silent
        # overwrite of either. See ADR 0011.
        self._attribute = attribute
        self._offset: int | None = None

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

    # --------------------------------------------------------------------- the transport

    def _client(self) -> httpx.Client:
        return httpx.Client(
            base_url=f"{API}/bot{self._settings.token}",
            timeout=45.0,
            follow_redirects=False,
            transport=self._transport,
        )

    def whoami(self) -> str:
        """Confirm the token works before anything else is attempted."""
        with self._client() as client:
            payload = self._ok(client.get("/getMe"))
        return str(payload.get("username") or payload.get("first_name") or "the bot")

    def poll_once(self, inbox: Any = None) -> list[IngestJob]:
        """One `getUpdates` round. Returns what was captured; replies with what was received."""
        jobs: list[IngestJob] = []
        with self._client() as client:
            params: dict[str, Any] = {"timeout": 30, "allowed_updates": '["message"]'}
            if self._offset is not None:
                params["offset"] = self._offset
            updates = self._ok(client.get("/getUpdates", params=params), expect_list=True)

            for update in updates:
                self._offset = int(update.get("update_id", 0)) + 1
                message = update.get("message") or {}
                chat_id = int((message.get("chat") or {}).get("id", 0))
                if (
                    self._settings.allowed_chat_ids
                    and chat_id not in self._settings.allowed_chat_ids
                ):
                    log.info("ignoring a message from chat %s: not in the allow list", chat_id)
                    continue
                # One bad update must not take the rest of the batch with it. The offset has
                # already moved past this message, so a failure here is a document that will not
                # be seen again -- which is why it is said out loud in the chat rather than only
                # logged. Advancing regardless is deliberate: a message the bot cannot handle
                # would otherwise be retried on every poll forever and nothing behind it would
                # ever be filed.
                try:
                    job = self._capture(client, message, chat_id, inbox)
                except Exception:
                    log.exception("could not file a message from chat %s", chat_id)
                    self._say(client, chat_id, "Something went wrong filing that. Send it again.")
                    continue
                if job is not None:
                    jobs.append(job)
        return jobs

    def _capture(
        self, client: httpx.Client, message: dict[str, Any], chat_id: int, inbox: Any
    ) -> IngestJob | None:
        file_id, name = _attachment(message)
        if file_id is None:
            # Media this adapter does not take used to return here in silence, which is
            # indistinguishable from the bot being switched off. A video note or an animation is
            # a person trying to file something, so they are told; plain chat is left alone.
            carried = UNSUPPORTED_MEDIA.intersection(message)
            if carried:
                log.info("not a document: a message carrying %s", ", ".join(sorted(carried)))
                self._say(
                    client,
                    chat_id,
                    "I can only file photographs and documents. Send it as a photo or a file.",
                )
            return None

        try:
            info = self._ok(client.get("/getFile", params={"file_id": file_id}))
            path = str(info.get("file_path", ""))
            size = int(info.get("file_size", 0) or 0)
            if not path or size > MAX_BYTES:
                self._say(client, chat_id, "That file is too large for me to file.")
                return None
            download = client.get(f"{API}/file/bot{self._settings.token}/{path}")
            download.raise_for_status()
            payload = download.content
        except (httpx.HTTPError, ValueError, TelegramUnavailable) as error:
            log.warning("could not fetch a Telegram attachment: %s", type(error).__name__)
            self._say(client, chat_id, "I could not download that. Try sending it again.")
            return None

        stamp = datetime.fromtimestamp(int(message.get("date", 0)) or 0, tz=UTC)

        # Before registration, not after. `core/ingest/source.py` finds a document's bytes again
        # by hashing the inbox, so a queued worker can start reading the moment the message is on
        # Redis -- and if the file is not on disk yet, it reports the document missing and leaves
        # it pending forever. The old order worked only because this adapter always ran inline.
        if inbox is not None:
            _write_local_copy(inbox, name, payload)

        job = self.receive(
            payload,
            sniff_mime(payload, name),
            f"telegram:{chat_id}",
            stamp,
            original_name=name,
        )

        if self._attribute is not None and not job.already_registered:
            try:
                self._attribute(job.document_id, chat_id)
            except Exception as error:  # attribution is a nicety; capture is not
                log.info("could not attribute %s to chat %s: %s", name, chat_id, error)

        if self._settings.delete_after_fetch:
            self._delete(client, chat_id, int(message.get("message_id", 0)))

        verb = "I already have that one" if job.already_registered else "Filed"
        self._say(client, chat_id, f"{verb}: {name}.")
        return job

    # ------------------------------------------------------------------------- plumbing

    def _ok(self, response: httpx.Response, *, expect_list: bool = False) -> Any:
        try:
            response.raise_for_status()
            body = response.json()
        except httpx.HTTPStatusError as error:
            raise TelegramUnavailable(_status_reason(response.status_code)) from error
        except (httpx.HTTPError, ValueError) as error:
            raise TelegramUnavailable("Telegram did not answer as expected.") from error
        if not body.get("ok"):
            raise TelegramUnavailable("Telegram refused the request.")
        result = body.get("result")
        if expect_list:
            return result if isinstance(result, list) else []
        return result if isinstance(result, dict) else {}

    def _say(self, client: httpx.Client, chat_id: int, text: str) -> None:
        try:
            client.post("/sendMessage", json={"chat_id": chat_id, "text": text})
        except httpx.HTTPError:
            log.info("could not reply in chat %s", chat_id)

    def _delete(self, client: httpx.Client, chat_id: int, message_id: int) -> None:
        """Delete at source. A failure is logged, never raised: the document is already ours."""
        if not message_id:
            return
        try:
            client.post("/deleteMessage", json={"chat_id": chat_id, "message_id": message_id})
        except httpx.HTTPError:
            log.info("could not delete message %s at source", message_id)


def _status_reason(status: int) -> str:
    """What an HTTP status from the Bot API means, in a sentence a person can act on.

    Never contains the token. 409 earns its own line because it is the one failure that looks
    exactly like a network blip and never clears by itself: `getUpdates` refuses while a webhook
    is registered or while a second poller holds the same bot.
    """
    if status == 409:
        return (
            "Telegram will not hand this bot its messages: either a webhook is set on it or "
            "something else is already polling it. Close the other Parrot window, or clear the "
            "webhook with the Bot API's deleteWebhook."
        )
    if status == 401:
        return "Telegram rejected the bot token. Check TELEGRAM_BOT_TOKEN in .env."
    if status == 429:
        return "Telegram is rate-limiting this bot. It will keep trying."
    return f"Telegram answered with HTTP {status}."


def _pixels(item: dict[str, Any]) -> tuple[int, int]:
    """How big a `PhotoSize` is: area first, declared bytes as the tie-break.

    Sorting on `file_size` alone picked the 90-pixel thumbnail whenever Telegram omitted it --
    every candidate scored nought and `max` returned the first, which is the smallest. OCR on a
    thumbnail recovers nothing, so the document quarantined as unreadable and the real
    photograph was never looked at. Width and height are always present on a `PhotoSize`.
    """
    area = int(item.get("width", 0) or 0) * int(item.get("height", 0) or 0)
    return area, int(item.get("file_size", 0) or 0)


def _attachment(message: dict[str, Any]) -> tuple[str | None, str]:
    """The largest photo, or the document. Telegram sends photos in several sizes."""
    document = message.get("document")
    if isinstance(document, dict) and document.get("file_id"):
        return str(document["file_id"]), str(document.get("file_name") or "telegram-document")

    photos = message.get("photo")
    if isinstance(photos, list) and photos:
        largest = max((item for item in photos if isinstance(item, dict)), key=_pixels)
        stamp = int(message.get("date", 0) or 0)
        return str(largest.get("file_id")), f"telegram-photo-{stamp}.jpg"
    return None, ""


def _write_local_copy(inbox: Any, name: str, payload: bytes) -> None:
    """Keep the bytes where the quarantine retry can find them again."""
    from pathlib import Path

    folder = Path(inbox)
    try:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / name).write_bytes(payload)
    except OSError as error:
        log.warning("could not write the local copy of %s: %s", name, error)
