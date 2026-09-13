"""Holdings come from `facts`, one per document that prints the name the categories read."""

from __future__ import annotations

from uuid import UUID, uuid4

from core.graph.inventory import holdings
from core.packs import pack

CAR, NOTICE = uuid4(), uuid4()


def row(
    document: UUID,
    name: str,
    doc_type: str,
    fact_id: int,
    key: str,
    page: int,
    value: str,
    subject: str = "Marcus Lim Jun Wei",
) -> tuple[object, ...]:
    return (document, name, doc_type, "insurance_agent", fact_id, key, page, value, subject)


ROWS = [
    row(CAR, "b1-0001.pdf", "policy_schedule", 1, "insurer", 1, "MERIDIAN ASSURANCE"),
    row(CAR, "b1-0001.pdf", "policy_schedule", 2, "policy_no", 1, "MV-2026-448120"),
    row(CAR, "b1-0001.pdf", "policy_schedule", 3, "insured", 1, "Marcus Lim Jun Wei"),
    row(
        CAR,
        "b1-0001.pdf",
        "policy_schedule",
        4,
        "product_name",
        1,
        "Private Car Insurance Policy",
    ),
    row(CAR, "b1-0001.pdf", "policy_schedule", 5, "expiry_date", 1, "2027-04-11"),
    row(NOTICE, "b1-0004.pdf", "renewal_notice", 6, "expiry_date", 1, "2027-04-11"),
]


def test_a_policy_on_file_is_named_categorised_and_cited_to_the_page_its_name_is_on() -> None:
    (car,) = holdings(ROWS, [pack("insurance_agent")])
    assert car.title == "MERIDIAN ASSURANCE, Private Car Insurance Policy"
    assert car.category is not None and car.category.id == "motor"
    assert (car.fact_id, car.page, car.subject) == (4, 1, "Marcus Lim Jun Wei")
    passage = car.passage()
    assert passage.kind == "inventory" and passage.ref == "inventory:4"
    assert "MV-2026-448120" in passage.text and "2027-04-11" in passage.text


def test_a_renewal_notice_is_not_counted_as_a_policy_on_file() -> None:
    assert [h.document_name for h in holdings(ROWS, [pack("insurance_agent")])] == ["b1-0001.pdf"]


def test_a_pack_that_declares_no_categories_holds_nothing() -> None:
    assert holdings(ROWS, [pack("iras_tax")]) == []
