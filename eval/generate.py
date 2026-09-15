"""Generate Set A fact questions from the register, for the documents that are on file.

    uv run python -m eval.generate --lane retrieval                 # 12, to eval/sets/answerable/
    uv run python -m eval.generate --lane retrieval --all --dry-run # the whole pool, printed

`eval/README.md` says it: every document was authored *from* a register row, so the register
already holds the correct answer for every extractable field, and questions about dates and
amounts are generated rather than written by hand. Each question comes with `expected`,
`must_cite_doc` and `must_cite_page` filled from the row, so it is gradeable the moment it is
written. What a generator cannot write — the passage questions, the module questions, the
adversarial ones — is still a person's job, and each lane's.

Each field yields two phrasings: one that names the policy number, one that names the product.
That pair is what retrieval is measured on — the exact identifier must be findable and the
paraphrase must still work — so a lane's generated dozen carries both by construction.

A question is only generated for a document that exists under `corpus/batches/`. The register
runs ahead of the batch; a question about a document nobody can ingest would be graded as a
retrieval failure, which it is not.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from eval.score import REGISTER_META
from eval.sets_io import field_page, read_registers

ROOT = Path(__file__).resolve().parents[1]

Row = Mapping[str, str]
Phrasing = Callable[[Row], str | None]


def _named(template: str, *keys: str) -> Phrasing:
    """A phrasing that needs every named key filled, or it does not apply to the row."""

    def phrase(row: Row) -> str | None:
        values = {key: (row.get(key) or "").strip() for key in keys}
        return template.format(**values) if all(values.values()) else None

    return phrase


# Two phrasings per field: by identifier, by name. A field whose value would appear in its own
# question (the policy number, the product name) gets the one form that does not give it away.
INSURANCE: dict[str, tuple[Phrasing | None, Phrasing | None]] = {
    "insurer": (
        _named("Which insurer issued policy {policy_no}?", "policy_no"),
        _named("Who is the insurer for the {product_name}?", "product_name"),
    ),
    "policy_no": (None, _named("What is the policy number of the {product_name}?", "product_name")),
    "insured": (
        _named("Who is the insured on policy {policy_no}?", "policy_no"),
        _named("Who is the policyholder of the {product_name}?", "product_name"),
    ),
    "product_name": (_named("What product is policy {policy_no}?", "policy_no"), None),
    "cover_from": (
        _named("When does cover under policy {policy_no} start?", "policy_no"),
        _named("When did cover under the {product_name} begin?", "product_name"),
    ),
    "expiry_date": (
        _named("When does policy {policy_no} expire?", "policy_no"),
        _named("When does the {product_name} expire?", "product_name"),
    ),
    "maturity_date": (
        _named("When does policy {policy_no} mature?", "policy_no"),
        _named("When does the {product_name} mature?", "product_name"),
    ),
    "premium_payable": (
        _named("What is the premium on policy {policy_no}?", "policy_no"),
        _named("How much is the premium for the {product_name}?", "product_name"),
    ),
    "sum_insured": (
        _named("What is the sum insured under policy {policy_no}?", "policy_no"),
        _named("What is the {product_name} insured for?", "product_name"),
    ),
    "excess": (
        _named("What is the excess on policy {policy_no}?", "policy_no"),
        _named("How much excess applies under the {product_name}?", "product_name"),
    ),
}

DOC_TYPE_LABELS = {
    "policy_schedule": "policy schedule",
    "renewal_notice": "renewal notice",
    "claim_letter": "claim letter",
    "policy_anniversary_statement": "policy anniversary statement",
    "benefit_illustration": "benefit illustration",
    "payslip": "payslip",
    "notice_of_assessment": "notice of assessment",
    "cpf_statement": "CPF statement",
    "srs_statement": "SRS statement",
    "donation_receipt": "donation receipt",
}


def generic(key: str) -> tuple[Phrasing, Phrasing | None]:
    """For a document type without hand-written phrasings: name the field and the document.
    Reads plainly enough to run; a lane that wants it better rewrites it."""
    label = key.replace("_", " ")

    def phrase(row: Row) -> str | None:
        subject = (row.get("subject") or "").strip()
        kind = DOC_TYPE_LABELS.get(
            row.get("doc_type") or "", (row.get("doc_type") or "").replace("_", " ")
        )
        if not kind:
            return None
        return (
            f"What is the {label} on {subject}'s {kind}?"
            if subject
            else f"What is the {label} on the {kind}?"
        )

    return phrase, None


@dataclass(frozen=True, slots=True)
class Generated:
    id: str
    question: str
    doc_id: str
    key: str
    form: str  # "id" names the identifier, "name" names the product or document

    def line(self, row: Row, lane: str) -> dict[str, object]:
        return {
            "id": self.id,
            "set": "A",
            "lane": lane,
            "question": self.question,
            "expected": {
                "kind": "fact",
                "pack": row.get("pack_id") or "",
                "key": self.key,
                "value": (row.get(self.key) or "").strip(),
            },
            "must_cite_doc": self.doc_id,
            "must_cite_page": field_page(row, self.key),
            "notes": f"generated from the register ({self.form} form)",
        }


def on_file(root: Path) -> set[str]:
    """The register ids that have a document under corpus/batches/, by file stem."""
    return {p.stem for p in (root / "corpus" / "batches").rglob("*") if p.is_file()}


def pool(rows: Sequence[Row], present: set[str]) -> list[tuple[Generated, Row]]:
    """Every question the register supports for the documents on file, in register order."""
    out: list[tuple[Generated, Row]] = []
    for row in rows:
        doc_id = (row.get("doc_id") or "").strip()
        if doc_id not in present:
            continue
        for key, value in row.items():
            if key in REGISTER_META or not (value or "").strip():
                continue
            phrasings = INSURANCE.get(key) if row.get("pack_id") == "insurance_agent" else None
            if phrasings is None:
                phrasings = generic(key)
            for form, phrase in zip(("id", "name"), phrasings, strict=True):
                text = phrase(row) if phrase else None
                if text:
                    out.append(
                        (Generated(f"a-gen-{doc_id}-{key}-{form}", text, doc_id, key, form), row)
                    )
    return out


def choose(
    items: list[tuple[Generated, Row]], limit: int, *, seed: int
) -> list[tuple[Generated, Row]]:
    """`limit` questions spread across documents, alternating forms, the same for one seed."""
    if limit >= len(items):
        return list(items)
    rng = random.Random(seed)
    by_doc: dict[str, list[tuple[Generated, Row]]] = defaultdict(list)
    for item in items:
        by_doc[item[0].doc_id].append(item)
    for bucket in by_doc.values():
        rng.shuffle(bucket)
        bucket.sort(key=lambda item: item[0].form)  # ids first, then names — popped from the end
    chosen: list[tuple[Generated, Row]] = []
    asked: dict[str, set[str]] = defaultdict(set)  # fields already asked about, per document
    docs = sorted(by_doc)
    turn = 0
    while len(chosen) < limit and any(by_doc.values()):
        for doc in docs:
            bucket = by_doc[doc]
            if not bucket or len(chosen) >= limit:
                continue
            wanted = ("id", "name")[turn % 2]
            fresh = [i for i, item in enumerate(bucket) if item[0].key not in asked[doc]]
            preferred = [i for i in fresh if bucket[i][0].form == wanted]
            item = bucket.pop((preferred or fresh or [len(bucket) - 1])[0])
            asked[doc].add(item[0].key)
            chosen.append(item)
        turn += 1
    order = {item[0].id: i for i, item in enumerate(items)}
    return sorted(chosen, key=lambda item: order[item[0].id])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--lane", required=True, help="the lane the questions are for, e.g. retrieval"
    )
    parser.add_argument("--limit", type=int, default=12, help="how many (default 12)")
    parser.add_argument("--all", action="store_true", help="the whole pool, ignoring --limit")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--out", type=Path, default=None, help="default eval/sets/answerable/<lane>-generated.jsonl"
    )
    parser.add_argument("--dry-run", action="store_true", help="print, do not write")
    args = parser.parse_args(argv)

    rows = read_registers(ROOT)
    present = on_file(ROOT)
    everything = pool(rows, present)
    skipped = sorted({(r.get("doc_id") or "") for r in rows} - present)
    chosen = everything if args.all else choose(everything, args.limit, seed=args.seed)
    lines = [json.dumps(item.line(row, args.lane), ensure_ascii=False) for item, row in chosen]

    target = args.out or ROOT / "eval" / "sets" / "answerable" / f"{args.lane}-generated.jsonl"
    if args.dry_run:
        print("\n".join(lines))
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(lines) + "\n", encoding="utf-8")
        shown = target.relative_to(ROOT) if target.is_relative_to(ROOT) else target
        print(f"wrote {len(lines)} questions to {shown}")
    documents = len(present & {r.get("doc_id") or "" for r in rows})
    missing = f" ({', '.join(skipped[:5])}{', …' if len(skipped) > 5 else ''})" if skipped else ""
    print(
        f"pool: {len(everything)} questions from {documents} documents on file; "
        f"{len(skipped)} register rows have no document yet{missing}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
