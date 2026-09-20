"""Generated Set A questions: gradeable by construction, only for documents on file, stable."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from eval.generate import choose, main, on_file, pool
from eval.sets_io import load_set, read_registers

ROOT = Path(__file__).resolve().parents[1]

ROW = {
    "doc_id": "b1-0001",
    "doc_type": "policy_schedule",
    "pack_id": "insurance_agent",
    "issued_date": "2026-03-20",
    "subject": "Marcus Lim Jun Wei",
    "tier": "clean",
    "insurer": "Meridian Assurance",
    "policy_no": "MV-2026-448120",
    "insured": "Marcus Lim Jun Wei",
    "product_name": "Private Car Insurance Policy",
    "expiry_date": "2027-04-11",
    "premium_payable": "1284.00",
    "excess": "",
    "field_pages": "expiry_date=2",
    "notes": "",
}


def test_each_filled_field_gets_an_identifier_form_and_a_name_form() -> None:
    items = pool([ROW], {"b1-0001"})
    by_id = {item.id: item for item, _ in items}
    assert "a-gen-b1-0001-expiry_date-id" in by_id and "a-gen-b1-0001-expiry_date-name" in by_id
    assert (
        by_id["a-gen-b1-0001-expiry_date-id"].question == "When does policy MV-2026-448120 expire?"
    )
    assert (
        by_id["a-gen-b1-0001-expiry_date-name"].question
        == "When does the Private Car Insurance Policy expire?"
    )
    # A field whose value would be in its own question gets one form only.
    assert "a-gen-b1-0001-policy_no-id" not in by_id and "a-gen-b1-0001-policy_no-name" in by_id
    assert "a-gen-b1-0001-product_name-name" not in by_id
    # An empty register cell yields nothing; metadata columns are not fields.
    assert not any(item.key in ("excess", "issued_date", "subject", "tier") for item, _ in items)


def test_the_line_is_gradeable_by_construction() -> None:
    (item, row) = next(
        (i, r) for i, r in pool([ROW], {"b1-0001"}) if i.id == "a-gen-b1-0001-expiry_date-id"
    )
    line = item.line(row, "retrieval")
    assert line["expected"] == {
        "kind": "fact",
        "pack": "insurance_agent",
        "key": "expiry_date",
        "value": "2027-04-11",
    }
    assert line["must_cite_doc"] == "b1-0001"
    assert line["must_cite_page"] == 2  # from field_pages; every other field is page 1
    assert line["set"] == "A" and line["lane"] == "retrieval"


def test_a_document_that_is_not_on_file_yields_nothing() -> None:
    assert pool([ROW], set()) == []
    assert pool([ROW], {"b1-0002"}) == []


def test_choose_spreads_across_documents_alternates_forms_and_is_stable() -> None:
    rows = [dict(ROW, doc_id=f"b1-000{n}", policy_no=f"MV-{n}") for n in range(1, 5)]
    items = pool(rows, {r["doc_id"] for r in rows})
    first, second = choose(items, 8, seed=3), choose(items, 8, seed=3)
    assert first == second
    docs = [item.doc_id for item, _ in first]
    assert all(docs.count(d) == 2 for d in {r["doc_id"] for r in rows})
    forms = [item.form for item, _ in first]
    assert forms.count("id") == 4 and forms.count("name") == 4
    keys = {(item.doc_id, item.key) for item, _ in first}
    assert len(keys) == 8  # never the same field twice for one document


@pytest.mark.xfail(
    strict=True,
    reason=(
        "ADR 0017 killed the hand-written phrasings. eval/generate.py:166 selects them with "
        "`row.get('pack_id') == 'insurance_agent'`, and since ADR 0017 decision 3 every register "
        "row's pack_id is 'core' — so INSURANCE is dead code and every Set A question falls to "
        "generic(), which has no name form and names no identifier. Set A therefore contains no "
        "exact policy number, which is the one thing hybrid RRF was built to find. Lane B's fix: "
        "select on the catalogue doc_type, then regenerate and review the set. Remove this marker "
        "with the fix — strict=True fails the suite once it passes again."
    ),
)
def test_the_committed_lane_b_file_is_what_the_generator_writes(tmp_path: Path) -> None:
    """Regenerating with the defaults reproduces the committed file, so a reviewer can trust
    that nothing in it was typed by hand."""
    out = tmp_path / "gen.jsonl"
    assert main(["--lane", "retrieval", "--out", str(out)]) == 0
    committed = ROOT / "eval" / "sets" / "answerable" / "retrieval-generated.jsonl"
    assert out.read_text(encoding="utf-8") == committed.read_text(encoding="utf-8")
    lines = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert len(lines) == 12
    on_disk = on_file(ROOT)
    assert all(line["must_cite_doc"] in on_disk for line in lines)
    assert all(q.id.startswith("a-gen-") for q in load_set(ROOT, "A") if "generated" in q.notes)
    assert read_registers(ROOT)  # the register the file was generated from is still there
