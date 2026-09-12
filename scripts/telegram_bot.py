"""Run the Telegram capture adapter.

    uv run python scripts/telegram_bot.py --check   # does the token work?
    uv run python scripts/telegram_bot.py           # capture photographs until Ctrl+C

Set `TELEGRAM_BOT_TOKEN` in `.env` first. Getting one takes about ten minutes: message
@BotFather on Telegram, send `/newbot`, give it a name, and it replies with the token. Nothing
else is needed — no business verification, no public URL, no hosting. See docs/RUNNING.md.

Long polling, so nothing on this machine listens on a public port.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOISY = ("httpx", "docling", "RapidOCR", "huggingface_hub", "filelock")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the token and exit")
    parser.add_argument(
        "--chat-id",
        type=int,
        action="append",
        default=None,
        help="only accept messages from this chat; repeatable. Default: any chat",
    )
    parser.add_argument(
        "--keep-at-source",
        action="store_true",
        help="do not delete the message after fetching it",
    )
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for name in NOISY:
        logging.getLogger(name).setLevel(logging.WARNING)

    from core import household
    from core.adapters.telegram import TelegramAdapter, TelegramSettings, TelegramUnavailable
    from core.ingest.dispatch import Inline
    from core.ingest.intake import Intake
    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.ollama import Ollama
    from core.runtime.settings import ConfigurationError, Settings, read_env

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    token = read_env(ROOT / ".env").get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print(
            "No TELEGRAM_BOT_TOKEN in .env.\n"
            "  1. Message @BotFather on Telegram and send /newbot\n"
            "  2. Give the bot a name; it replies with a token\n"
            "  3. Put TELEGRAM_BOT_TOKEN=<that token> in .env at the repository root\n"
            "The token is a household secret: .env is git-ignored and must stay that way."
        )
        return 2

    telegram = TelegramSettings(
        token=token,
        allowed_chat_ids=frozenset(args.chat_id or ()),
        delete_after_fetch=not args.keep_at_source,
    )

    try:
        with connect(settings) as conn:

            def attribute(document_id: object, chat_id: int) -> None:
                """Whose phone this arrived on, recorded before anything is read off it.

                Silent when the chat is not linked to anybody: most installs never link one,
                and a bot that refused documents from unmapped chats would be a worse bot.
                """
                person_id = household.person_for_chat(conn, chat_id)
                if person_id is not None:
                    household.attribute(conn, document_id, person_id, source="telegram")
                    conn.commit()  # autocommit is off; the caller commits

            adapter = TelegramAdapter(
                Intake(conn, Inline(conn, Ollama(settings))), telegram, attribute
            )
            try:
                name = adapter.whoami()
            except TelegramUnavailable as error:
                print(str(error))
                return 2
            print(f"Connected as @{name}.")
            if args.check:
                return 0
            if not telegram.allowed_chat_ids:
                print("Accepting documents from any chat. Use --chat-id to restrict that.")
            print("Send a photograph of a document to the bot. Ctrl+C to stop.")
            return _loop(adapter, Path(settings.watch_folder))
    except DatabaseUnavailable as error:
        print(str(error))
        return 2


def _loop(adapter: object, inbox: Path) -> int:
    try:
        while True:
            try:
                adapter.poll_once(inbox)  # type: ignore[attr-defined]
            except Exception as error:  # a transport hiccup must not end the capture
                logging.getLogger(__name__).warning(
                    "Telegram poll failed (%s); retrying", type(error).__name__
                )
                time.sleep(5)
    except KeyboardInterrupt:
        print("Stopped.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
