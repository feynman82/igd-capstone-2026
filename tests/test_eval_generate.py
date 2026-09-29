"""Generated Set A questions: gradeable by construction, one lane each, and reproducible."""

from __future__ import annotations

import json
from pathlib import Path

from eval.generate import choose, hand_written, main, on_file, pool
from eval.phrasings import LANES, SPECS, lane_of
from eval.sets_io import load_set, read_registers

ROOT = Path(__file__).resolve().parents[1]

ROW = {
    "doc_id": "b1-0001",
    "doc_type": "policy_schedule",
    "pack_id": "core",
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

CARD = {
    "doc_id": "b2-0012",
    "doc_type": "identity_card",
    "pack_id": "core",
    "subject": "Marcus Lim Jun Wei",
    "tier": "photo",
    "id_number": "S8714289B",
    "full_name": "Marcus Lim Jun Wei",
    "date_of_birth": "1987-05-08",
    "field_pages": "",
    "notes": "",
}


def _asked(*rows: dict[str, str]) -> dict[str, str]:
    return {item.id: item.question for item, _ in pool(list(rows))}


def test_each_field_is_asked_once_by_its_printed_reference_and_once_by_name() -> None:
    asked = _asked(ROW)
    assert asked["a-gen-b1-0001-expiry_date-printed"] == "When does policy MV-2026-448120 expire?"
    assert (
        asked["a-gen-b1-0001-expiry_date-spoken"]
        == "When does the Private Car Insurance Policy expire?"
    )
    # An empty register cell yields nothing, and a metadata column is not a printed field.
    assert not any(key.startswith("a-gen-b1-0001-excess") for key in asked)
    assert not any("-tier-" in key or "-issued_date-" in key for key in asked)


def test_the_line_is_gradeable_by_construction() -> None:
    item, row = next(i for i in pool([ROW]) if i[0].id == "a-gen-b1-0001-expiry_date-printed")
    line = item.line(row, "retrieval")
    assert line["expected"] == {
        "kind": "fact",
        "pack": "core",
        "key": "expiry_date",
        "value": "2027-04-11",
    }
    assert line["must_cite_doc"] == "b1-0001"
    assert line["must_cite_page"] == 2  # from field_pages; every other field is page 1
    assert line["set"] == "A" and line["lane"] == "retrieval"


def test_a_question_that_prints_its_own_answer_is_not_asked() -> None:
    asked = _asked(ROW)
    # The printed wording names the policy number, so that wording cannot ask for it…
    assert "a-gen-b1-0001-policy_no-printed" not in asked
    assert "a-gen-b1-0001-policy_no-spoken" in asked
    # …and the spoken wording names the product, so it cannot ask what the product is.
    assert "a-gen-b1-0001-product_name-spoken" not in asked
    assert "a-gen-b1-0001-product_name-printed" in asked
    # A document named by whose it is cannot be asked whose name is on it.
    asked = _asked(CARD)
    assert "a-gen-b2-0012-full_name-spoken" not in asked
    assert asked["a-gen-b2-0012-id_number-spoken"] == (
        "What is the identity card number on Marcus Lim Jun Wei's identity card?"
    )


def test_a_wording_that_names_two_documents_is_dropped_from_both() -> None:
    """Marcus has two donation receipts, so "Marcus's donation receipt" names neither."""
    first = {
        "doc_id": "b1-0019",
        "doc_type": "donation_receipt",
        "pack_id": "core",
        "subject": "Marcus Lim Jun Wei",
        "tier": "clean",
        "donor": "Marcus Lim Jun Wei",
        "charity": "Riverbend Community Fund",
        "receipt_no": "RCT-1",
        "field_pages": "",
        "notes": "",
    }
    second = dict(first, doc_id="b1-0021", receipt_no="RCT-2", charity="Harbourlight Education")
    assert "a-gen-b1-0019-charity-spoken" in _asked(first)  # unique while it is the only one
    both = _asked(first, second)
    assert "a-gen-b1-0019-charity-spoken" not in both
    assert "a-gen-b1-0021-charity-spoken" not in both
    # The printed wording names the receipt, so it stays gradeable.
    assert both["a-gen-b1-0019-charity-printed"] == "Which charity issued receipt RCT-1?"


def test_every_register_row_belongs_to_exactly_one_lane() -> None:
    rows = read_registers(ROOT)
    assert rows, "the register is the ground truth; a run without it proves nothing"
    unclaimed = [row["doc_id"] for row in rows if lane_of(row) is None]
    assert not unclaimed, f"no lane claims {unclaimed}"
    # A photographed claim letter is Desmond's; a photographed identity card is not.
    photo_claim = next(r for r in rows if r["doc_type"] == "claim_letter" and r["tier"] == "photo")
    assert lane_of(photo_claim) == "corpus"
    assert lane_of(next(r for r in rows if r["doc_type"] == "identity_card")) == "integration"


def test_choose_alternates_the_two_wordings_and_is_stable() -> None:
    rows = [
        dict(ROW, doc_id=f"b1-000{n}", policy_no=f"MV-{n}", product_name=f"Plan {n}")
        for n in range(1, 9)
    ]
    items = pool(rows)
    first, second = choose(items, 8, seed=3), choose(items, 8, seed=3)
    assert first == second
    forms = [item.form for item, _ in first]
    assert forms.count("printed") == 4 and forms.count("spoken") == 4
    # With more documents than questions, each document is asked at most once…
    assert len({item.doc_id for item, _ in first}) == 8
    # …and with fewer, no field is asked twice of one document.
    keys = {(item.doc_id, item.key) for item, _ in choose(pool(rows[:2]), 8, seed=3)}
    assert len(keys) == 8


def test_a_question_a_person_already_wrote_is_not_generated_again() -> None:
    written = hand_written(ROOT)
    assert "What is the premium on policy MV-2026-448120?" in written  # eval/sets/answerable
    generated = {
        json.loads(line)["question"]
        for path in (ROOT / "eval" / "sets" / "answerable").glob("*-generated.jsonl")
        for line in path.read_text(encoding="utf-8").splitlines()
    }
    assert not (generated & written)


def test_the_committed_files_are_what_the_generator_writes(tmp_path: Path) -> None:
    """Every lane's file regenerates byte for byte, so a reviewer can trust nothing in it was
    typed by hand — and can regenerate once the register gains its `field_pages` pass."""
    for lane in LANES:
        out = tmp_path / f"{lane}.jsonl"
        assert main(["--lane", lane, "--out", str(out)]) == 0
        committed = ROOT / "eval" / "sets" / "answerable" / f"{lane}-generated.jsonl"
        assert out.read_text(encoding="utf-8") == committed.read_text(encoding="utf-8"), lane
        lines = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
        assert len(lines) == 12
        assert all(line["lane"] == lane for line in lines)


def test_set_a_is_complete_gradeable_and_covers_every_lane() -> None:
    questions = load_set(ROOT, "A")
    assert len(questions) >= 60, "the task asks twelve questions of each of five lanes"
    assert {q.lane for q in questions} == set(LANES)
    assert all(q.gradeable_citation for q in questions)
    assert len({q.id for q in questions}) == len(questions)
    assert len({q.question for q in questions}) == len(questions)
    # Every expected value is the register's own, under a key that type is asked about.
    rows = {row["doc_id"]: row for row in read_registers(ROOT)}
    for question in questions:
        row = rows.get(question.must_cite_doc)
        assert row is not None, question.id
        if question.expected.kind == "fact":
            assert (row.get(question.expected.key) or "").strip() == question.expected.value
            assert question.expected.key in SPECS[row["doc_type"]].asks


def test_the_documents_on_file_are_a_subset_of_the_register() -> None:
    """The register runs ahead of the batch. That is expected, and it is why `eval.run` skips a
    question whose document is not in the vault rather than scoring it as a miss."""
    assert on_file(ROOT) <= {row["doc_id"] for row in read_registers(ROOT)}
