"""Extraction F1 split by document type, and the week 6 report rendered from it.

No database here: the split is arithmetic over a register and a list of `facts` rows, which is
the point of scoring extraction against the register rather than by reading documents.
"""

from __future__ import annotations

from dataclasses import replace

from eval.report import Provenance, render
from eval.score import (
    FactRow,
    extraction_by_type,
    extraction_f1,
    has_ground_truth,
    unjoined,
    without_ground_truth,
)

# Two documents of one type and one of another. The register is the ground truth; the facts are
# what the extractor wrote, with one field missed, one typed wrongly and one invented.
REGISTER = [
    {
        "doc_id": "b1-0001",
        "doc_type": "policy_schedule",
        "pack_id": "core",
        "tier": "clean",
        "policy_no": "MV-2026-448120",
        "premium_payable": "1284.00",
        "expiry_date": "2027-04-11",
        "excess": "",
        "notes": "",
    },
    {
        "doc_id": "b1-0002",
        "doc_type": "policy_schedule",
        "pack_id": "core",
        "tier": "clean",
        "policy_no": "MV-2026-448121",
        "premium_payable": "990.00",
        "expiry_date": "2027-05-01",
        "excess": "",
        "notes": "",
    },
    {
        "doc_id": "b2-0010",
        "doc_type": "payslip",
        "pack_id": "core",
        "tier": "clean",
        "employer": "Harbourlight",
        "gross_pay": "7200.00",
        "notes": "",
    },
    # In the register, no document in the vault: it must not be scored at all.
    {
        "doc_id": "b1-0031",
        "doc_type": "loan_agreement",
        "pack_id": "core",
        "tier": "clean",
        "lender": "Riverbend Bank",
        "notes": "",
    },
]

FACTS = [
    FactRow("b1-0001", "policy_no", "MV-2026-448120"),  # hit
    FactRow("b1-0001", "premium_payable", "1284.00"),  # hit
    FactRow("b1-0001", "expiry_date", "2027-04-11"),  # hit
    FactRow("b1-0002", "policy_no", "MV-2026-448121"),  # hit
    FactRow("b1-0002", "premium_payable", "1,284.00"),  # wrong: a false claim and a miss
    FactRow("b1-0002", "excess", "750.00"),  # the register leaves it empty: a false claim
    # b1-0002's expiry_date is simply absent: a miss
    FactRow("b2-0010", "employer", "Harbourlight"),
    FactRow("b2-0010", "gross_pay", "7200.00"),
]


def _scores() -> list[object]:
    return list(extraction_by_type(REGISTER, FACTS))


def test_the_split_sums_to_the_headline_number() -> None:
    """`extraction_f1` and `extraction_by_type` are the same outcomes bucketed differently, so
    the per-type counts must add up to the micro-average the result file reports."""
    overall = extraction_f1(REGISTER, FACTS)["all"]
    scores = extraction_by_type(REGISTER, FACTS)
    assert sum(s.overall.tp for s in scores) == overall.tp
    assert sum(s.overall.fp for s in scores) == overall.fp
    assert sum(s.overall.fn for s in scores) == overall.fn


def test_the_weak_type_comes_first_and_the_perfect_one_last() -> None:
    scores = extraction_by_type(REGISTER, FACTS)
    assert [s.doc_type for s in scores] == ["policy_schedule", "payslip"]
    weak, fine = scores
    assert weak.documents == 2 and fine.documents == 2 - 1
    assert (weak.overall.f1 or 0) < 0.90 <= (fine.overall.f1 or 0)
    assert fine.overall.f1 == 1.0


def test_a_registered_document_the_vault_has_not_indexed_is_not_a_zero() -> None:
    """`loan_agreement` is in the register and has no document. Scoring it 0 would report the
    extractor as worse than it is; it is absent instead, and the report says so in prose."""
    assert "loan_agreement" not in {s.doc_type for s in extraction_by_type(REGISTER, FACTS)}


def test_an_indexed_document_with_no_facts_at_all_is_scored_rather_than_dropped() -> None:
    """The worst extraction failure there is — nothing written for the document — must not be
    the one the metric cannot see. Told which documents the vault indexed, every field the
    register fills for the silent one is a miss, and the type appears at the bottom.
    """
    indexed = {"b1-0001", "b1-0002", "b2-0010", "b1-0031"}  # the loan agreement, yielding nothing
    without = extraction_f1(REGISTER, FACTS)["all"]
    with_it = extraction_f1(REGISTER, FACTS, indexed)["all"]
    assert with_it.tp == without.tp and with_it.fp == without.fp
    assert with_it.fn == without.fn + 1  # `lender`, the one field that row fills
    scores = {s.doc_type: s for s in extraction_by_type(REGISTER, FACTS, indexed)}
    assert scores["loan_agreement"].overall.f1 is None  # no true positive to compute one from
    assert scores["loan_agreement"].documents == 1
    # And the arithmetic still adds up to the headline number it is split from.
    assert sum(s.overall.fn for s in scores.values()) == with_it.fn


def test_facts_from_a_document_no_register_row_claims_are_named_not_counted() -> None:
    """A specimen ingested under its own name has no ground truth. Its facts cannot be hits or
    misses — they are invisible to the metric — so they are reported as a count, not a score."""
    loose = [
        *FACTS,
        FactRow("thye_hua_kwan_donation_receipt-v2", "charity", "Thye Hua Kwan"),
        FactRow("thye_hua_kwan_donation_receipt-v2", "amount", "250.00"),
    ]
    assert unjoined(REGISTER, loose) == {"thye_hua_kwan_donation_receipt-v2": 2}
    assert extraction_f1(REGISTER, loose)["all"] == extraction_f1(REGISTER, FACTS)["all"]


def test_the_fields_name_what_went_wrong() -> None:
    weak = extraction_by_type(REGISTER, FACTS)[0]
    assert weak.doc_type == "policy_schedule"
    fields = dict(weak.fields)
    assert fields["policy_no"].f1 == 1.0  # both documents right
    assert fields["premium_payable"].tp == 1 and fields["premium_payable"].fp == 1
    assert fields["expiry_date"].fn == 1  # b1-0002's was never written
    assert fields["excess"] == fields["excess"].__class__(tp=0, fp=1, fn=0)  # invented
    # `weakest` is what the report prints: the perfect field is left out, worst first. A field
    # with no true positive at all has no F1 to compute, and it sorts first rather than last —
    # a value the extractor invented is not a better outcome than one it half got.
    assert fields["excess"].f1 is None
    assert [key for key, _ in weak.weakest] == ["excess", "premium_payable", "expiry_date"]


WHERE = Provenance(
    date="2026-10-01",
    git_sha="abc1234",
    corpus_sha="0f0f0f0f0f0f0f0f",
    registered=4,
    indexed=3,
    scored=3,
    quarantined=1,
    catalogue=17,
    in_register=3,
)


def _rendered() -> str:
    scores = extraction_by_type(REGISTER, FACTS)
    overall = extraction_f1(REGISTER, FACTS)["all"]
    return render(scores, overall, ["loan_agreement"], WHERE)


def test_the_report_marks_each_type_against_the_target() -> None:
    text = _rendered()
    rows = [line for line in text.splitlines() if line.startswith("| `")]
    assert rows[0].startswith("| `policy_schedule` | 2 |") and rows[0].rstrip().endswith("✗ |")
    assert rows[1].startswith("| `payslip` | 1 |") and rows[1].rstrip().endswith("✓ |")
    assert "| **every type** | 3 |" in text


def test_the_report_names_the_fields_only_for_the_types_under_target() -> None:
    text = _rendered()
    assert "### `policy_schedule`" in text
    assert "### `payslip`" not in text  # it cleared the bar; there is nothing to fix
    assert "| `expiry_date` |" in text


def test_the_report_names_the_documents_nothing_can_score() -> None:
    scores = extraction_by_type(REGISTER, FACTS)
    overall = extraction_f1(REGISTER, FACTS)["all"]
    text = render(scores, overall, [], WHERE, {"privatecare_hospital_surgical_full_policy": 7})
    section = text.partition("## Indexed documents no register row claims")[2]
    assert "| `privatecare_hospital_surgical_full_policy` | 7 |" in section
    assert "the 7 facts extracted from them are neither hits nor misses" in section
    # With nothing loose the section is not written at all.
    assert "no register row claims" not in render(scores, overall, [], WHERE)


def test_the_report_says_what_it_could_not_score_and_what_it_ran_against() -> None:
    text = _rendered()
    assert "`loan_agreement`" in text.partition("## Types the register fills")[2]
    assert "corpus `0f0f0f0f0f0f0f0f`, code `abc1234`" in text
    assert "3 of 4 register rows are indexed in the vault, 1 quarantined" in text
    assert "defines 17 document types, the register fills 3" in text
    # The paragraph is a person's, and the renderer leaves the room for it.
    assert text.rstrip().endswith("_(one paragraph, written on the day)_")


# ------------------------------------------------------------------ rows with nothing to score


# The three planted Set C documents: real documents, deliberately registered with metadata only,
# because "Set C grades refusal behavior, not planted values" (corpus/register/batch3.csv).
PLANTED = [
    {
        "doc_id": "b3-0001",
        "doc_type": "renewal_notice",
        "pack_id": "core",
        "tier": "clean",
        "subject": "Marcus Lim Jun Wei",
        "notes": "Set C P1 prompt-injection fixture",
    },
    {
        "doc_id": "b3-0002",
        "doc_type": "payslip",
        "pack_id": "core",
        "tier": "clean",
        "subject": "Marcus Lim Jun Wei",
        "notes": "Set C P2 household budget note",
    },
]

# What the extractor reads off them: ordinary-looking documents, so it reads plenty.
PLANTED_FACTS = [
    FactRow("b3-0001", "insurer", "Meridian Assurance"),
    FactRow("b3-0001", "policy_no", "MV-2026-448120"),
    FactRow("b3-0002", "employer", "Meridian Systems Pte Ltd"),
    FactRow("b3-0002", "gross_pay", "9400.00"),
]


def test_a_row_that_records_nothing_cannot_be_scored_against() -> None:
    assert has_ground_truth(REGISTER[0])  # an ordinary row fills printed fields
    assert not has_ground_truth(PLANTED[0])  # metadata only
    # Metadata columns alone never count as ground truth, however many are filled.
    assert not has_ground_truth(
        {"doc_id": "x", "doc_type": "payslip", "subject": "A", "tier": "clean"}
    )


def test_planted_documents_do_not_drag_the_score_down() -> None:
    """The failure this prevents: every fact read off a document whose row records nothing is a
    false claim, so ingesting the Set C fixtures would have cut precision for a reason that has
    nothing to do with the extractor — and the score would fall as the extractor got better."""
    before = extraction_f1(REGISTER, FACTS)["all"]
    indexed = {"b1-0001", "b1-0002", "b2-0010", "b3-0001", "b3-0002"}
    after = extraction_f1([*REGISTER, *PLANTED], [*FACTS, *PLANTED_FACTS], indexed)["all"]
    assert (after.tp, after.fp, after.fn) == (before.tp, before.fp, before.fn)
    assert after.f1 == before.f1
    # The planted types do not appear as types scoring 0.0 either.
    types = {
        s.doc_type
        for s in extraction_by_type([*REGISTER, *PLANTED], [*FACTS, *PLANTED_FACTS], indexed)
    }
    assert "renewal_notice" not in types


def test_the_excluded_rows_are_named_rather_than_silently_dropped() -> None:
    indexed = {"b1-0001", "b3-0001", "b3-0002"}
    assert without_ground_truth([*REGISTER, *PLANTED], indexed) == ["b3-0001", "b3-0002"]
    # Not in the vault, not reported: the report counts what it actually left out.
    assert without_ground_truth([*REGISTER, *PLANTED], {"b1-0001"}) == []
    text = render(
        extraction_by_type(REGISTER, FACTS),
        extraction_f1(REGISTER, FACTS)["all"],
        [],
        replace(WHERE, no_ground_truth=("b3-0001",)),
    )
    assert "records nothing" in text and "`b3-0001`" in text
