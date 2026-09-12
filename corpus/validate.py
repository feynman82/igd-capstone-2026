"""Validate a document register before it is handed over.

    python -m corpus.validate corpus/register/batch1.csv

The register is the ground truth for extraction scoring, so a row that is wrong here is a
wrong answer in the evaluation. This is the contract between Lane E and the builders.

The register is **one column per field**, which is the shape `python -m packs.build` writes
into `corpus/register/<pack>_columns.csv` from `pack.yaml`. Start a batch by copying that
header; do not invent one. A register in the superseded `field_1_name,field_1_value` shape is
rejected by name rather than read as empty.

`field_pages` is the column that makes a golden-set question gradeable: it records which page
each value is *printed* on, for the fields that are not on page 1. It is the one column that
cannot be filled while the register is being written, because the page layout does not exist
until the mail merge has run — so it is a second pass over the register, after the documents
are generated and before the batch is handed over.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from collections.abc import Sequence
from datetime import date, datetime
from pathlib import Path


def _known_doc_types() -> dict[str, set[str]]:
    """Derived from the pack manifests, never hardcoded.

    A register row can only name a document type some installed pack actually owns, so a
    typo here is caught before the corpus is built rather than at extraction time.
    """
    import yaml

    from core.contracts import PackManifest

    out: dict[str, set[str]] = {}
    for pack_yaml in sorted(Path("packs").glob("*/pack.yaml")):
        if pack_yaml.parent.name.startswith("_"):
            continue
        m = PackManifest.model_validate(yaml.safe_load(pack_yaml.read_text(encoding="utf-8")))
        out[m.id] = set(m.document_types)
    return out


def _known_fields() -> dict[tuple[str, str], object]:
    import yaml

    from core.contracts import PackManifest

    out: dict[tuple[str, str], object] = {}
    for pack_yaml in sorted(Path("packs").glob("*/pack.yaml")):
        if pack_yaml.parent.name.startswith("_"):
            continue
        m = PackManifest.model_validate(yaml.safe_load(pack_yaml.read_text(encoding="utf-8")))
        out.update(m.field_index())
    return out


TIERS = {"clean", "scanned", "photo"}
FIXED = {"doc_id", "doc_type", "pack_id", "issued_date", "subject", "tier", "field_pages", "notes"}


def _fields(row: dict[str, str], declared: set[str]) -> dict[str, str]:
    """The filled field columns of one row, in the format `packs.build` generates.

    One column per field name, which is the format `corpus/register/<pack>_columns.csv` is
    written in and the reason a field name is written down in exactly one place. A column that
    is not a declared field name anywhere is ignored here and caught by the header check, so a
    typo shows up as a named problem rather than as a silently missing fact.
    """
    return {
        name: value.strip()
        for name, value in row.items()
        if name in declared and (value or "").strip()
    }


def _wide_format(fieldnames: Sequence[str]) -> bool:
    """The superseded `field_1_name,field_1_value,...` shape.

    It is worth detecting by name rather than letting it fall through as a row with no fields:
    a register in this shape is fully populated ground truth that this validator used to read,
    and "no fields" would be a baffling thing to tell the person who just filled one in.
    """
    return any(name.startswith("field_") and name.endswith("_name") for name in fieldnames)


def _pages(raw: str) -> tuple[dict[str, int], list[str]]:
    """Parse `field_pages`: semicolon-separated `name=page`, 1-based. Empty means page 1."""
    out: dict[str, int] = {}
    problems: list[str] = []
    for entry in raw.split(";"):
        entry = entry.strip()
        if not entry:
            continue
        name, separator, page = entry.partition("=")
        if not separator:
            problems.append(f"{entry!r} is not name=page")
            continue
        try:
            number = int(page.strip())
        except ValueError:
            problems.append(f"page {page.strip()!r} for {name.strip()!r} is not a whole number")
            continue
        if number < 1:
            problems.append(f"page {number} for {name.strip()!r} is not 1 or greater")
            continue
        out[name.strip()] = number
    return out, problems


def _as_date(value: str) -> date | None:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d %b %Y", "%d %B %Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    known = _known_doc_types()
    fields = _known_fields()
    seen_ids: set[str] = set()
    policy_values: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))

    declared = {name for _, name in fields}

    with path.open(encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        if _wide_format(header):
            return [
                f"{path} is in the superseded field_1_name/field_1_value format. The register "
                "is one column per field now — start from the header in "
                "corpus/register/<pack>_columns.csv, which `python -m packs.build` generates "
                "from pack.yaml so the column names cannot drift from the field names."
            ]
        if "field_pages" not in header:
            errors.append(
                "the header has no field_pages column — regenerate it with "
                "`python -m packs.build` and copy the new header. Without it a golden-set "
                "question cannot say which page its answer is printed on."
            )
        for name in header:
            if name and name not in FIXED and name not in declared:
                errors.append(f"column {name!r} is not a field any installed pack declares")

        for n, row in enumerate(reader, start=2):
            doc_id = (row.get("doc_id") or "").strip()
            where = f"row {n} ({doc_id or 'no id'})"

            if not doc_id:
                errors.append(f"{where}: doc_id is empty")
            elif doc_id in seen_ids:
                errors.append(f"{where}: duplicate doc_id")
            else:
                seen_ids.add(doc_id)

            pack = (row.get("pack_id") or "").strip()
            doc_type = (row.get("doc_type") or "").strip()
            if pack not in known:
                errors.append(f"{where}: unknown pack_id {pack!r} (known: {sorted(known)})")
            elif doc_type not in known[pack]:
                errors.append(
                    f"{where}: {doc_type!r} is not a document type {pack} owns "
                    f"(it owns: {sorted(known[pack])})"
                )
            else:
                for name in _fields(row, declared):
                    if (doc_type, name) not in fields:
                        errors.append(
                            f"{where}: field {name!r} is not declared on {doc_type} in pack.yaml"
                        )

            tier = (row.get("tier") or "").strip()
            if tier not in TIERS:
                errors.append(f"{where}: tier must be one of {sorted(TIERS)}, got {tier!r}")

            issued = _as_date((row.get("issued_date") or "").strip())
            if issued is None:
                errors.append(f"{where}: issued_date is missing or unparseable")

            f = _fields(row, declared)
            if not f:
                errors.append(f"{where}: no fields — this row carries no ground truth")

            # Which page each value is printed on. Absent means page 1, so a single-page
            # document leaves the column empty; a page named for a field this row does not
            # carry is a typo that would otherwise become an ungradeable golden question.
            pages, page_problems = _pages(row.get("field_pages") or "")
            for problem in page_problems:
                errors.append(f"{where}: field_pages {problem}")
            for name in pages:
                if name not in f:
                    errors.append(
                        f"{where}: field_pages names {name!r}, which this row does not fill"
                    )

            start = _as_date(f.get("cover_from", "")) or issued
            expiry = _as_date(f.get("expiry_date", ""))
            if expiry and start and expiry <= start:
                errors.append(f"{where}: expiry_date {expiry} is not after {start}")

            for key in ("premium_payable", "gross_salary", "donation_amount", "net_pay"):
                if key in f:
                    try:
                        if float(f[key].replace(",", "").lstrip("$")) <= 0:
                            errors.append(f"{where}: {key} must be positive")
                    except ValueError:
                        errors.append(f"{where}: {key}={f[key]!r} is not a number")

            # The same policy must look identical everywhere it appears.
            pol = f.get("policy_no")
            if pol:
                for key in ("insurer", "insured", "vehicle", "property"):
                    if key in f:
                        policy_values[pol][key].add(f[key])

    for pol, keys in policy_values.items():
        for key, values in keys.items():
            if len(values) > 1:
                errors.append(f"policy {pol}: {key} differs across documents: {sorted(values)}")

    return errors


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("register", type=Path)
    args = ap.parse_args()

    errors = validate(args.register)
    if errors:
        print(f"{len(errors)} problem(s) in {args.register}:\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"{args.register}: register is consistent and ready to hand over")


if __name__ == "__main__":
    main()
