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

    def __init__(self, registrar: Registrar, settings: TelegramSettings) -> None:
        if not settings.configured:
            raise TelegramUnavailable(
                "No Telegram bot token is configured. Set TELEGRAM_BOT_TOKEN in .env."
            )
        self._register = registrar
        self._settings = settings
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
                job = self._capture(client, message, chat_id, inbox)
                if job is not None:
                    jobs.append(job)
        return jobs

    def _capture(
        self, client: httpx.Client, message: dict[str, Any], chat_id: int, inbox: Any
    ) -> IngestJob | None:
        file_id, name = _attachment(message)
        if file_id is None:
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
        job = self.receive(
            payload,
            sniff_mime(payload, name),
            f"telegram:{chat_id}",
            stamp,
            original_name=name,
        )

        if inbox is not None:
            _write_local_copy(inbox, name, payload)
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


def _attachment(message: dict[str, Any]) -> tuple[str | None, str]:
    """The largest photo, or the document. Telegram sends photos in several sizes."""
    document = message.get("document")
    if isinstance(document, dict) and document.get("file_id"):
        return str(document["file_id"]), str(document.get("file_name") or "telegram-document")

    photos = message.get("photo")
    if isinstance(photos, list) and photos:
        largest = max(photos, key=lambda item: int(item.get("file_size", 0) or 0))
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
