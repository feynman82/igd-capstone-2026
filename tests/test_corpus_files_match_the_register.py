"""A document file promises something by its name. This checks the promise is kept.

`corpus/README.md` rule 2: "**`doc_id` is the filename.** `b1-0001` in the register is
`b1-0001.pdf` in the batch folder. Anything else and nothing can join a fact back to the row
it should match."

Nothing enforced that. Two different failures had been sitting in the repository for weeks
before a sweep found them, and neither made anything go red:

- **A file named for a register row that does not exist.** `inbox/b2-0019.pdf` was committed
  on 3 October as "restore b2-0019 policy fixture", and no `b2-0019` row has ever existed in
  any register, in any commit. It reads as ground truth, joins to nothing, and is quarantined
  in the vault because its mail merge never substituted — `premium_payable` extracted as the
  literal string `TotalAnnualPremiumPayable`.
- **Files named for what they are rather than for a row.** Twenty of them, deliberately
  committed so the team could see the capture path work. They are ingestible and unscoreable:
  `eval.generate.unclaimed` and `eval.modules.unjoined` report them, and three are already in
  the vault contributing 17 facts no metric can see.

The second kind is a choice and is only counted here. The first kind is a mistake, so it
fails — but it fails for *new* ones only. `KNOWN_UNREGISTERED` carries the one that exists
today so that the gate stays green for everybody while its issue is open; a gate that is red
on `main` until another lane acts is a gate people learn to ignore.
"""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# A register id: batch number, then four digits. This is the shape that makes a promise.
REGISTER_ID = re.compile(r"^b\d+-\d{4}$")
DOCUMENT_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp"}

# Named for a register row that does not exist. Each entry needs an issue, not an exception.
KNOWN_UNREGISTERED = {
    "b2-0019": "no row in any register, ever; quarantined on a placeholder mail merge",
}


def _tracked_documents() -> list[Path]:
    """Committed document files under the folders a corpus document lives in."""
    out = subprocess.run(
        ["git", "ls-files", "inbox", "corpus"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return [
        Path(line)
        for line in out.stdout.splitlines()
        if Path(line).suffix.lower() in DOCUMENT_SUFFIXES
    ]


def _register_ids() -> set[str]:
    ids: set[str] = set()
    for path in sorted((ROOT / "corpus" / "register").glob("*.csv")):
        if path.name.endswith(("template.csv", "_columns.csv")):
            continue
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = csv.DictReader(line for line in handle if not line.startswith("#"))
            ids |= {(row.get("doc_id") or "").strip() for row in rows}
    return ids - {""}


def test_a_file_named_like_a_register_row_has_one() -> None:
    """The promise rule 2 makes. A file called `b2-0021.pdf` says "I am register row b2-0021";
    if no such row exists, every fact it produces joins to nothing and the name is a lie that
    nothing catches."""
    registered = _register_ids()
    broken = {
        path.stem: str(path)
        for path in _tracked_documents()
        if REGISTER_ID.match(path.stem) and path.stem not in registered
    }
    unexpected = {k: v for k, v in broken.items() if k not in KNOWN_UNREGISTERED}
    assert not unexpected, (
        "named for a register row that does not exist: "
        + ", ".join(f"{k} ({v})" for k, v in sorted(unexpected.items()))
        + ". Either add the row to corpus/register/, or rename the file so it stops claiming "
        "to be ground truth."
    )
    # And the known ones must still be known: fix the data, delete the entry.
    stale = set(KNOWN_UNREGISTERED) - set(broken)
    assert not stale, (
        f"{sorted(stale)} no longer exists or is now registered — delete it from "
        "KNOWN_UNREGISTERED so the next one cannot hide behind it."
    )


def test_documents_that_claim_no_register_row_are_counted_not_hidden() -> None:
    """Specimens named for what they are. A choice, not a defect — but a silent one, so the
    count is pinned: it should move when somebody joins them or drops them, and a change here
    should be a decision rather than a surprise."""
    registered = _register_ids()
    specimens = [
        path
        for path in _tracked_documents()
        if not REGISTER_ID.match(path.stem) and path.stem not in registered
    ]
    # 20 capture-path specimens, plus 24 monthly CPF statements for 2025 that have no
    # monthly fields to be scored against (corpus/batches/cpf-monthly-2025/README.md).
    assert len(specimens) == 44, (
        f"{len(specimens)} documents claim no register row (was 44). They are ingestible and "
        "unscoreable — `eval.generate.unclaimed` names them. Update this number with the "
        "reason in the commit message."
    )
