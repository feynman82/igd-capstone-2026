"""Today: what the two capability modules have to say, ordered by urgency.

    uv run python scripts/today.py              # the nightly sweep, for real
    uv run python scripts/today.py --dry-run    # show it without recording that it was said
    uv run python scripts/today.py --as-of 2026-11-20

Every line names the document behind it. This is the command-line shape of the Today surface
Lane D will draw; the modules do not know either of them exists.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", type=date.fromisoformat, default=None, help="YYYY-MM-DD")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="do not record that these were said, so they appear again",
    )
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.settings import ConfigurationError, Settings
    from modules import alert, reminder

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    today = args.as_of or date.today()
    try:
        with connect(settings) as conn:
            print(f"Today — {today}\n")

            alerts = alert.sweep(conn, today, mark=not args.dry_run)
            due = reminder.sweep(conn, today, mark=not args.dry_run)
            late = reminder.overdue(conn, today)

            if not (alerts or due or late):
                print("Nothing needs you today.")
                return 0

            for item in alerts:
                print(f"  ! {item.line()}")
            for item in due:
                print(f"  • {item.line()}")
            for _id, _pack, label, due_date, name in late:
                source = f" — {name}" if name else ""
                print(f"  ✗ {label}: overdue since {due_date}{source}")

            if args.dry_run:
                print("\n(dry run: nothing was recorded, so these will appear again)")
            return 0
    except DatabaseUnavailable as error:
        print(str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
