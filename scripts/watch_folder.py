"""Watch the inbox folder, register and read everything dropped into it.

    uv run python scripts/watch_folder.py                 # follow the folder
    uv run python scripts/watch_folder.py --once          # one pass, for a demo or a test
    uv run python scripts/watch_folder.py --register-only  # skip parsing and extraction

This is the demo path for ingestion: drop a file in `inbox/`, watch it be filed, classified
against an installed pack, and either indexed with cited facts or sent to quarantine with a
reason. Drop the same file again and it says it was already filed.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.adapters.folder import FolderAdapter

ROOT = Path(__file__).resolve().parents[1]
NOISY = ("httpx", "docling", "RapidOCR", "huggingface_hub", "filelock")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--folder", type=Path, default=None, help="default: WATCH_FOLDER or ./inbox"
    )
    parser.add_argument("--stable-seconds", type=float, default=3.0)
    parser.add_argument("--poll-seconds", type=float, default=1.0)
    parser.add_argument("--once", action="store_true", help="run a single pass and exit")
    parser.add_argument(
        "--register-only",
        action="store_true",
        help="register documents without parsing, extracting or embedding them",
    )
    args = parser.parse_args(argv)
    if args.stable_seconds < 0 or args.poll_seconds <= 0:
        parser.error("stable-seconds must be zero or more and poll-seconds must be positive")

    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for name in NOISY:
        logging.getLogger(name).setLevel(logging.WARNING)

    from core.adapters.folder import FolderAdapter, FolderSettings
    from core.ingest.intake import Intake
    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.ollama import Ollama
    from core.runtime.settings import ConfigurationError, Settings

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    folder = args.folder or Path(settings.watch_folder)
    if not folder.is_absolute():
        folder = ROOT / folder
    folder.mkdir(parents=True, exist_ok=True)

    try:
        with connect(settings) as conn:
            adapter = FolderAdapter(
                Intake(conn, Ollama(settings), process_documents=not args.register_only),
                FolderSettings(folder, args.stable_seconds, args.poll_seconds),
            )
            print(f"Watching {folder}. Ctrl+C to stop.")
            return _loop(adapter, args.once, args.poll_seconds, args.stable_seconds)
    except DatabaseUnavailable as error:
        print(str(error))
        return 2


def _loop(adapter: FolderAdapter, once: bool, poll_seconds: float, stable_seconds: float) -> int:
    """Poll until interrupted. `--once` waits out one stability window and then stops."""
    deadline = stable_seconds + poll_seconds * 2 if once else None
    spent = 0.0
    try:
        while True:
            adapter.poll(poll_seconds)  # intake logs what happened to each document
            if deadline is not None and spent >= deadline:
                return 0
            time.sleep(poll_seconds)
            spent += poll_seconds
    except KeyboardInterrupt:
        print("Stopped.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
