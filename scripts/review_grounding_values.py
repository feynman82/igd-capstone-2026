"""Show every value a pack's sources printed, and let a person approve or reject it.

    uv run python scripts/review_grounding_values.py --list
    uv run python scripts/review_grounding_values.py --list --pack iras_tax
    uv run python scripts/review_grounding_values.py --approve 12 13 --by Siew
    uv run python scripts/review_grounding_values.py --reject 14 --by Siew --note "wrong year"

Nothing indexed by `scripts/index_grounding.py` may be read by a calculator until it is
`approved` here (ADR 0016). `--list` prints the passage a value claims to come from beside it,
so the decision is made from the same words a calculator would eventually trust.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from core.grounding.review import PendingValue

ROOT = Path(__file__).resolve().parents[1]


def _block(value: PendingValue) -> str:
    """One printed value, with everything a reviewer needs to sign off on it."""
    amount = value.value_text if value.value_text is not None else str(value.value_num)
    qualifiers = ", ".join(f"{k}={v}" for k, v in sorted(value.qualifiers.items())) or "none"
    return "\n".join(
        [
            f"[{value.id}] {value.pack_id} / {value.key}",
            f"  {amount} {value.unit}  qualifiers: {qualifiers}",
            f"  {value.publisher} — {value.source_title}",
            f"  {value.url}",
            f'    "{value.passage}"',
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="show every value still pending")
    parser.add_argument("--pack", help="restrict --list to one pack")
    parser.add_argument("--approve", nargs="+", type=int, metavar="ID", help="approve these ids")
    parser.add_argument("--reject", nargs="+", type=int, metavar="ID", help="reject these ids")
    parser.add_argument("--by", help="the reviewer's name; required with --approve or --reject")
    parser.add_argument("--note", help="why; required with --reject")
    args = parser.parse_args(argv)

    if not (args.list or args.approve or args.reject):
        parser.error("choose one of --list, --approve, --reject")
    if (args.approve or args.reject) and not args.by:
        parser.error("--approve and --reject need --by NAME")
    if args.reject and not args.note:
        parser.error("--reject needs --note TEXT")

    sys.path.insert(0, str(ROOT))

    from core.grounding.review import approve, pending, reject
    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.settings import ConfigurationError, Settings

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    today = date.today()
    try:
        with connect(settings) as conn:
            if args.list:
                values = pending(conn, args.pack)
                if not values:
                    print("Nothing is pending review.")
                    return 0
                print("\n\n".join(_block(value) for value in values))
                return 0
            if args.approve:
                count = approve(conn, args.approve, reviewer=args.by, on=today)
                print(f"{count} value(s) approved.")
                return 0 if count else 1
            assert args.reject is not None and args.note is not None
            count = reject(conn, args.reject, reviewer=args.by, on=today, note=args.note)
            print(f"{count} value(s) rejected.")
            return 0 if count else 1
    except DatabaseUnavailable as error:
        print(str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
