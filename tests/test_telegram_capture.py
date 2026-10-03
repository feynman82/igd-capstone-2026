"""Telegram capture: what arrives, what is answered, and what is written where.

No live Telegram and no database. The Bot API is an `httpx.MockTransport` that answers the four
calls this adapter makes, and a fake registrar stands in for the `documents` table exactly as in
`tests/test_folder_capture.py`. What is worth asserting here is the set of claims the launcher
now makes to a person: that a photograph sent to the bot becomes a registered document on the
`telegram` channel, that its bytes are on disk *before* anything is asked to read them, that the
largest size is the one fetched, and that a message the adapter cannot file is answered rather
than dropped in silence.

The last of those is why this file exists. Every failure this suite covers was previously a
photograph that vanished between the chat and the vault with nothing written down anywhere.
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import httpx
import pytest

from core.adapters.base import sha256
from core.adapters.telegram import TelegramAdapter, TelegramSettings, TelegramUnavailable
from core.ingest.register import Registration
from core.ingest.source import index_folder
from core.runtime.settings import ConfigurationError, Settings

JPEG = b"\xff\xd8\xff\xe0" + b"y" * 4000
THUMBNAIL = b"\xff\xd8\xff\xe0" + b"t" * 90
PDF = b"%PDF-1.7\nnot really a pdf, but it starts like one\n" + b"x" * 400

CHAT = 4242
STAMP = 1789000000
NAME = f"telegram-photo-{STAMP}-77.jpg"  # the message id too, so an album keeps every page


class FakeRegistrar:
    """The `documents` table, reduced to the one thing it guarantees: sha256 is unique."""

    def __init__(self) -> None:
        self.by_digest: dict[bytes, UUID] = {}
        self.calls: list[dict[str, Any]] = []
        # What was on disk at the moment each registration was asked for. This is how the
        # ordering claim is tested: a queued worker finds bytes by hashing the inbox, so the
        # file has to exist before the document is registered, not after.
        self.inbox_at_call: list[list[str]] = []
        self.inbox: Path | None = None

    def __call__(
        self,
        *,
        payload: bytes,
        mime: str,
        original_name: str,
        source_channel: str,
        synthetic: bool = False,
    ) -> Registration:
        key = sha256(payload)
        self.calls.append(
            {"name": original_name, "mime": mime, "channel": source_channel, "payload": payload}
        )
        self.inbox_at_call.append(
            sorted(path.name for path in self.inbox.iterdir()) if self.inbox else []
        )
        inserted = key not in self.by_digest
        document_id = self.by_digest.setdefault(key, uuid4())
        return Registration(
            document_id=document_id,
            sha256=key,
            source_channel=source_channel,
            original_name=original_name,
            mime=mime,
            status="pending",
            ingested_at=datetime.now(UTC),
            inserted=inserted,
        )


class FakeTelegram:
    """The four Bot API calls this adapter makes, and a record of what it asked for."""

    def __init__(self, updates: list[dict[str, Any]], files: dict[str, bytes]) -> None:
        self._updates = updates
        self._files = files
        self.said: list[str] = []
        self.deleted: list[int] = []
        self.fetched: list[str] = []
        self.updates_status = 200

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self._handle)

    def _handle(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("/getUpdates"):
            if self.updates_status != 200:
                return httpx.Response(self.updates_status, json={"ok": False})
            updates, self._updates = self._updates, []
            return httpx.Response(200, json={"ok": True, "result": updates})
        if path.endswith("/getFile"):
            file_id = request.url.params["file_id"]
            self.fetched.append(file_id)
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {"file_path": f"photos/{file_id}", "file_size": 4004},
                },
            )
        if "/file/bot" in path:
            return httpx.Response(200, content=self._files[path.rsplit("/", 1)[-1]])
        if path.endswith("/sendMessage"):
            self.said.append(json.loads(request.content)["text"])
            return httpx.Response(200, json={"ok": True, "result": {}})
        if path.endswith("/deleteMessage"):
            self.deleted.append(json.loads(request.content)["message_id"])
            return httpx.Response(200, json={"ok": True, "result": {}})
        raise AssertionError(f"the adapter called something unexpected: {path}")


def photo_update(update_id: int = 1, chat_id: int = CHAT) -> dict[str, Any]:
    """A photograph as Telegram actually sends one: the same image in several sizes.

    `file_size` is absent from every size on purpose. Telegram omits it often enough that
    selecting on it alone picked the 90-pixel thumbnail, and a thumbnail OCRs to nothing.
    """
    return {
        "update_id": update_id,
        "message": {
            "message_id": 77,
            "date": STAMP,
            "chat": {"id": chat_id},
            "photo": [
                {"file_id": "thumb", "width": 90, "height": 67},
                {"file_id": "middle", "width": 320, "height": 240},
                {"file_id": "largest", "width": 1280, "height": 960},
            ],
        },
    }


def build(
    tmp_path: Path,
    updates: list[dict[str, Any]],
    *,
    allowed: frozenset[int] = frozenset(),
    delete: bool = True,
    files: dict[str, bytes] | None = None,
) -> tuple[TelegramAdapter, FakeRegistrar, FakeTelegram, Path]:
    api = FakeTelegram(updates, files or {"largest": JPEG, "thumb": THUMBNAIL, "middle": JPEG})
    registrar = FakeRegistrar()
    registrar.inbox = tmp_path
    adapter = TelegramAdapter(
        registrar,
        TelegramSettings(token="test-token", allowed_chat_ids=allowed, delete_after_fetch=delete),
        None,
        api.transport(),
    )
    return adapter, registrar, api, tmp_path


# ------------------------------------------------------------------------------- the happy path


def test_a_photograph_becomes_a_document_on_the_telegram_channel(tmp_path: Path) -> None:
    adapter, registrar, _api, inbox = build(tmp_path, [photo_update()])

    jobs = adapter.poll_once(inbox)

    assert len(jobs) == 1
    assert registrar.calls[0]["channel"] == "telegram"
    assert registrar.calls[0]["mime"] == "image/jpeg"  # sniffed from the magic bytes, not the name
    assert registrar.calls[0]["name"] == NAME
    assert jobs[0].source_channel == "telegram"


def test_the_largest_size_is_fetched_when_telegram_omits_file_size(tmp_path: Path) -> None:
    adapter, registrar, api, inbox = build(tmp_path, [photo_update()])

    adapter.poll_once(inbox)

    assert api.fetched == ["largest"]
    assert registrar.calls[0]["payload"] == JPEG


def test_the_bytes_are_on_disk_before_the_document_is_registered(tmp_path: Path) -> None:
    """The claim the queued dispatcher depends on. See `core/ingest/source.py`."""
    adapter, registrar, _api, inbox = build(tmp_path, [photo_update()])

    adapter.poll_once(inbox)

    assert registrar.inbox_at_call == [[NAME]]
    assert (inbox / NAME).read_bytes() == JPEG


def test_the_message_is_deleted_at_source_and_the_person_is_told(tmp_path: Path) -> None:
    adapter, _registrar, api, inbox = build(tmp_path, [photo_update()])

    adapter.poll_once(inbox)

    assert api.deleted == [77]
    assert api.said == [f"Filed: {NAME}."]


def test_the_same_photograph_twice_is_filed_once_and_said_so(tmp_path: Path) -> None:
    adapter, registrar, api, inbox = build(tmp_path, [photo_update()])
    adapter.poll_once(inbox)
    api._updates = [photo_update(update_id=2)]

    adapter.poll_once(inbox)

    assert len(registrar.by_digest) == 1
    assert api.said[-1] == f"I already have that one: {NAME}."


def test_every_photograph_in_an_album_keeps_its_own_file(tmp_path: Path) -> None:
    """An album arrives as one message per photograph, all stamped with the same second.

    Named by the second alone, the second page overwrote the first on disk. Both were registered,
    so the first became a document whose bytes are nowhere -- the quarantine retry and a queued
    worker both find a document by hashing the inbox, and they found nothing.
    """
    first, second = photo_update(update_id=1), photo_update(update_id=2)
    second["message"]["message_id"] = 78
    second["message"]["photo"] = [{"file_id": "page-two", "width": 1280, "height": 960}]
    page_two = b"\xff\xd8\xff\xe0" + b"z" * 4000
    adapter, registrar, _api, inbox = build(
        tmp_path, [first, second], files={"largest": JPEG, "page-two": page_two}
    )

    adapter.poll_once(inbox)

    assert len(registrar.by_digest) == 2
    assert set(index_folder(inbox)) == set(registrar.by_digest)


def test_a_photograph_that_cannot_be_kept_is_neither_filed_nor_deleted(tmp_path: Path) -> None:
    """The inbox copy is the only copy once the chat's is deleted, so failing to write it stops
    everything after it. It used to be logged and carried on: registered, deleted at source,
    and told "Filed" -- a document with no bytes anywhere."""
    blocked = tmp_path / "inbox"
    blocked.write_bytes(b"a file where the folder should be")
    adapter, registrar, api, _inbox = build(tmp_path, [photo_update()])

    adapter.poll_once(blocked)

    assert registrar.calls == []
    assert api.deleted == []
    assert api.said == ["Something went wrong filing that. Send it again."]


def test_the_token_never_reaches_the_log(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """The Bot API puts the token in the URL path, and httpx logs every URL at INFO -- the level
    the launcher runs at. A START.cmd window, or a screen recording of the demo, showed it."""
    adapter, _registrar, _api, inbox = build(tmp_path, [photo_update()])

    with caplog.at_level(logging.INFO):
        adapter.poll_once(inbox)

    assert "test-token" not in caplog.text


def test_a_document_keeps_the_name_it_was_sent_under(tmp_path: Path) -> None:
    update = {
        "update_id": 1,
        "message": {
            "message_id": 78,
            "date": STAMP,
            "chat": {"id": CHAT},
            "document": {"file_id": "scan", "file_name": "policy-schedule.pdf"},
        },
    }
    adapter, registrar, _api, inbox = build(tmp_path, [update], files={"scan": PDF})

    adapter.poll_once(inbox)

    assert registrar.calls[0]["name"] == "policy-schedule.pdf"
    assert registrar.calls[0]["mime"] == "application/pdf"


# ------------------------------------------------------------- the ways a document used to vanish


def test_a_chat_outside_the_allow_list_is_ignored(tmp_path: Path) -> None:
    adapter, registrar, api, inbox = build(
        tmp_path, [photo_update(chat_id=999)], allowed=frozenset({CHAT})
    )

    assert adapter.poll_once(inbox) == []
    assert registrar.calls == []
    assert api.said == []  # an unknown chat is told nothing at all, deliberately


def test_media_this_adapter_cannot_file_is_answered_rather_than_dropped(tmp_path: Path) -> None:
    update = {
        "update_id": 1,
        "message": {
            "message_id": 79,
            "date": STAMP,
            "chat": {"id": CHAT},
            "video": {"file_id": "clip"},
        },
    }
    adapter, registrar, api, inbox = build(tmp_path, [update])

    assert adapter.poll_once(inbox) == []
    assert registrar.calls == []
    assert api.said == ["I can only file photographs and documents. Send it as a photo or a file."]


def test_plain_chat_is_left_alone(tmp_path: Path) -> None:
    update = {
        "update_id": 1,
        "message": {"message_id": 80, "date": STAMP, "chat": {"id": CHAT}, "text": "hello"},
    }
    adapter, _registrar, api, inbox = build(tmp_path, [update])

    assert adapter.poll_once(inbox) == []
    assert api.said == []


def test_one_failing_update_does_not_take_the_rest_of_the_batch_with_it(tmp_path: Path) -> None:
    """The offset has already moved, so the survivors are all that is left to save."""
    calls: list[str] = []

    def explode_once(**kwargs: Any) -> Registration:
        calls.append(kwargs["original_name"])
        if len(calls) == 1:
            raise RuntimeError("the database went away")
        return FakeRegistrar()(**kwargs)

    api = FakeTelegram(
        [photo_update(update_id=1), photo_update(update_id=2)],
        {"largest": JPEG},
    )
    adapter = TelegramAdapter(
        explode_once, TelegramSettings(token="test-token"), None, api.transport()
    )
    # The two updates carry the same bytes, so give the second a different stamp to tell them
    # apart on disk; the adapter names a photograph after the message date.
    api._updates[1]["message"]["date"] = STAMP + 1

    jobs = adapter.poll_once(tmp_path)

    assert len(calls) == 2  # the second was attempted
    assert len(jobs) == 1  # and it is the one that survived
    assert "Something went wrong filing that. Send it again." in api.said


def test_a_conflict_names_the_webhook_rather_than_saying_nothing(tmp_path: Path) -> None:
    """409 is the one poll failure that never clears by itself, so it must not read as a blip."""
    adapter, _registrar, api, inbox = build(tmp_path, [photo_update()])
    api.updates_status = 409

    with pytest.raises(TelegramUnavailable) as raised:
        adapter.poll_once(inbox)

    message = str(raised.value)
    assert "webhook" in message
    assert "test-token" not in message  # a reason a person may paste anywhere


def test_a_rejected_token_says_which_setting_is_wrong(tmp_path: Path) -> None:
    adapter, _registrar, api, inbox = build(tmp_path, [photo_update()])
    api.updates_status = 401

    with pytest.raises(TelegramUnavailable) as raised:
        adapter.poll_once(inbox)

    assert "TELEGRAM_BOT_TOKEN" in str(raised.value)
    assert "test-token" not in str(raised.value)


def test_an_adapter_without_a_token_refuses_to_be_built() -> None:
    with pytest.raises(TelegramUnavailable):
        TelegramAdapter(FakeRegistrar(), TelegramSettings(token="  "))


# ---------------------------------------------------------------------------------- the settings


def test_telegram_is_off_until_a_token_is_configured(tmp_path: Path) -> None:
    settings = Settings.load(tmp_path, {})

    assert settings.telegram_configured is False
    assert settings.telegram_chat_ids == frozenset()
    assert settings.telegram_delete_at_source is True


def test_the_allow_list_is_configuration_so_a_double_click_can_honour_it(tmp_path: Path) -> None:
    settings = Settings.load(
        tmp_path, {"TELEGRAM_BOT_TOKEN": "t", "TELEGRAM_CHAT_IDS": "111, -222"}
    )

    assert settings.telegram_configured is True
    assert settings.telegram_chat_ids == frozenset({111, -222})


def test_a_malformed_allow_list_is_a_configuration_error_not_an_empty_one(tmp_path: Path) -> None:
    """Silently reading "everyone" out of a typo would be the opposite of what was asked for."""
    with pytest.raises(ConfigurationError):
        Settings.load(tmp_path, {"TELEGRAM_CHAT_IDS": "111, not-a-chat"})


def test_delete_at_source_can_be_turned_off(tmp_path: Path) -> None:
    settings = Settings.load(tmp_path, {"TELEGRAM_DELETE_AT_SOURCE": "false"})

    assert settings.telegram_delete_at_source is False


def test_a_token_never_appears_in_the_settings_repr(tmp_path: Path) -> None:
    settings = Settings.load(tmp_path, {"TELEGRAM_BOT_TOKEN": "super-secret-token"})

    assert "super-secret-token" not in repr(settings)
