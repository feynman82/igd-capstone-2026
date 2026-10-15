"""Run Set C in a vault of its own, so its planted documents never reach Set A.

    uv run python -m eval.setc                     # clone the vault, add the fixtures, run C, drop
    uv run python -m eval.setc --keep              # leave the clone for inspection

Set C's injection items need three planted documents in the vault — a notice telling the
assistant to email a policy away, a budget note telling it to answer two million and cite
nothing, a letter telling it to recommend switching insurer. They have to be retrievable, or
there is nothing to resist: on 5 October they were absent and the three items passed against an
empty vault.

But retrievable is exactly the problem. On 14 October, with the fixtures ingested into the shared
vault, they outranked real documents on Set A. `b3-0001` is a notice *about* car policy
MV-2026-448120 and prints that number, so hybrid retrieval's exact-identifier boost scored it
level with the real schedule, and it won: five of sixteen Set A failures had a planted document
ranked above the right answer. Removing the fixtures changed two of those five and one Set B
answer (eval/results/2026-10-15-fixtures-removed.md) — in both directions, so every Set A and B
number measured in that vault was partly measuring the fixtures.

So the two needs are met by two vaults:

- **Sets A and B** run against the development vault, which holds no fixtures. `eval.run` warns,
  loudly and in the result file, if it finds any there.
- **Set C** runs here: the development vault is cloned with `CREATE DATABASE … TEMPLATE`, the
  fixtures are read into the clone, Set C is scored against it, and the clone is dropped. The
  development vault is not written to.

`eval.run` also refuses to bank an injection item it cannot test: when the fixtures are not in
the vault being scored, those items are skipped and counted in `run.skipped_no_fixture`, the same
way a question whose document is missing is skipped rather than scored as a miss.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from collections.abc import Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = "parrot_setc"

# The register of Set C's planted documents. Its rows carry metadata only, on purpose — its own
# header says "Set C grades refusal behavior, not planted values" — and that is what marks them as
# fixtures rather than ground truth. Read from the register so a renamed or extended batch is
# picked up rather than hard-coded here.
FIXTURE_REGISTER = Path("corpus") / "register" / "batch3.csv"
FIXTURE_BATCH = Path("corpus") / "batches" / "batch3"
# Set C items that need the fixtures in the vault to mean anything (eval/sets/adversarial/README).
NEEDS_FIXTURES = frozenset({"injection"})


def fixture_ids(root: Path = ROOT) -> frozenset[str]:
    """The register ids of Set C's planted documents."""
    path = root / FIXTURE_REGISTER
    if not path.is_file():
        return frozenset()
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(line for line in handle if not line.startswith("#"))
        return frozenset(doc_id for row in rows if (doc_id := (row.get("doc_id") or "").strip()))


def clone_vault(admin_url: str, source: str, target: str) -> None:
    """Copy the development vault into `target`. Nothing is written to `source`.

    `TEMPLATE` copies at the file level, so it is fast, exact, and refuses while anything else is
    connected to the source — which is why the message names `make dev`.
    """
    import psycopg

    with psycopg.connect(admin_url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute(f'DROP DATABASE IF EXISTS "{target}" WITH (FORCE)')
        try:
            cur.execute(f'CREATE DATABASE "{target}" TEMPLATE "{source}"')
        except psycopg.errors.ObjectInUse as error:
            raise RuntimeError(
                f"Cannot copy {source} while something else is connected to it. Stop `make dev` "
                "(and any open screens) and run this again."
            ) from error


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--label", default="setc", help="part of the result file name")
    parser.add_argument("--vault", default=VAULT, help=f"database name (default {VAULT})")
    parser.add_argument("--keep", action="store_true", help="do not drop the clone at the end")
    parser.add_argument("--out", type=Path, default=ROOT / "eval" / "results")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    from core.runtime.settings import ConfigurationError, Settings
    from eval import run
    from eval.holdout import documents_in, drop_vault, ingest, vault_url

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2
    folder = ROOT / FIXTURE_BATCH
    if not fixture_ids() or not folder.is_dir():
        print(f"No Set C fixtures at {folder}. The injection items cannot be tested.")
        return 2

    source = settings.database_url.rsplit("/", 1)[-1]
    admin = vault_url(settings.database_url, "postgres")
    clone = vault_url(settings.database_url, args.vault)
    print(f"copying vault {source} -> {args.vault} (the development vault is not written to)")
    try:
        clone_vault(admin, source, args.vault)
    except RuntimeError as error:
        print(error)
        return 2

    try:
        isolated = Settings.load(ROOT, {**os.environ, "DATABASE_URL": clone})
        print(f"reading the {len(fixture_ids())} planted documents into {args.vault}")
        ingest(isolated, documents_in(folder))
        return run.main(
            [
                "--corpus",
                "c",
                "--vault",
                args.vault,
                "--no-judge",
                "--label",
                args.label,
                "--out",
                str(args.out),
            ]
        )
    finally:
        if args.keep:
            print(f'vault {args.vault} kept. Drop it with: DROP DATABASE "{args.vault}";')
        else:
            drop_vault(admin, args.vault)


if __name__ == "__main__":
    raise SystemExit(main())
