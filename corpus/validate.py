"""Validate a document register before it is handed over.

    python -m corpus.validate corpus/register/batch1.csv

The register is the ground truth for extraction scoring, so a row that is wrong here is a
wrong answer in the evaluation. This is the contract between Lane E and the builders.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

KNOWN_DOC_TYPES = {
    "iras_tax": {"payslip", "ir8a", "cpf_statement", "srs_statement", "donation_receipt"},
    "insurance_agent": {
        "policy_schedule", "renewal_notice", "claim_letter", "benefit_illustration",
        "servicing_invoice",
    },
}
TIERS = {"clean", "scanned", "photo"}


def _fields(row: dict[str, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for i in range(1, 21):
        name = (row.get(f"field_{i}_name") or "").strip()
        if name:
            out[name] = (row.get(f"field_{i}_value") or "").strip()
    return out


def _as_date(value: str) -> date | None:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d %b %Y", "%d %B %Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    policy_values: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))

    with path.open(encoding="utf-8-sig") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=2):
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
            if pack not in KNOWN_DOC_TYPES:
                errors.append(f"{where}: unknown pack_id {pack!r}")
            elif doc_type not in KNOWN_DOC_TYPES[pack]:
                errors.append(f"{where}: {doc_type!r} is not a document type {pack} owns")

            tier = (row.get("tier") or "").strip()
            if tier not in TIERS:
                errors.append(f"{where}: tier must be one of {sorted(TIERS)}, got {tier!r}")

            issued = _as_date((row.get("issued_date") or "").strip())
            if issued is None:
                errors.append(f"{where}: issued_date is missing or unparseable")

            f = _fields(row)
            if not f:
                errors.append(f"{where}: no fields — this row carries no ground truth")

            start = _as_date(f.get("cover_from", "")) or issued
            expiry = _as_date(f.get("expiry_date", ""))
            if expiry and start and expiry <= start:
                errors.append(f"{where}: expiry_date {expiry} is not after {start}")

            for key in ("annual_premium", "gross_salary", "amount", "net_pay"):
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
