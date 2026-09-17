"""Index a pack's published sources into pending values a reviewer can approve or reject.

    uv run python scripts/index_grounding.py               # every enabled pack with a corpus
    uv run python scripts/index_grounding.py --pack iras_tax

Run this whenever a pack's `grounding/<corpus>/` folder changes, before asking
`scripts/review_grounding_values.py` to show what is new. See `core/grounding/index.py`.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOISY = ("httpx", "huggingface_hub", "filelock", "transformers")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", help="index only this installed pack, whether enabled or not")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for name in NOISY:
        logging.getLogger(name).setLevel(logging.WARNING)

    from core.grounding.corpus import CorpusInvalid
    from core.grounding.index import index_pack
    from core.packs import InstalledPack, PackUnavailable
    from core.packs import pack as pack_by_id
    from core.registry import enabled_packs
    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.ollama import ModelUnavailable, Ollama
    from core.runtime.settings import ConfigurationError, Settings

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    client = Ollama(settings, timeout=600.0)
    today = date.today()

    try:
        with connect(settings) as conn:
            targets: list[InstalledPack]
            if args.pack is not None:
                try:
                    targets = [pack_by_id(args.pack)]
                except PackUnavailable as error:
                    print(str(error))
                    return 1
                if args.pack not in {installed.id for installed in enabled_packs(conn)}:
                    print(f"  warning: {args.pack} is not enabled; indexing it anyway")
            else:
                targets = [
                    installed
                    for installed in enabled_packs(conn)
                    if installed.manifest.grounding.corpus is not None
                ]
                if not targets:
                    print("No enabled pack declares a grounding corpus.")
                    return 0

            failures = 0
            for installed in targets:
                try:
                    report = index_pack(conn, client, installed, today=today)
                except CorpusInvalid as error:
                    failures += 1
                    print(f"  {installed.id}: {error}")
                    continue
                except ModelUnavailable as error:
                    # index_pack rolled this pack back; the stored sources are as they were.
                    print(f"  {installed.id}: nothing indexed, the model is unavailable ({error})")
                    return 2
                print(
                    f"  {installed.id}: {report.sources} source(s), {report.unchanged} "
                    f"unchanged, {report.pending} pending value(s), {report.superseded} "
                    "superseded"
                    + (f", {report.unread} not read (run again to retry)" if report.unread else "")
                )
            return 1 if failures else 0
    except DatabaseUnavailable as error:
        print(str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
