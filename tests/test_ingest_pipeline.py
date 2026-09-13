"""Parsing, chunking, extraction and the quarantine decision.

The model is faked. What is being tested is the pipeline's judgement: that a page number is
attributed from the page the value is actually printed on, that a value printed on no page is
refused rather than stored, and that anything short of a satisfied pack goes to quarantine
instead of writing half a document.

The fixture document is the payslip from `packs/iras_tax/pack.yaml`'s own examples, so the
expected values are the pack's ground truth rather than something invented here.
"""

from __future__ import annotations

from typing import Any

import pytest

from core.ingest.chunk import TARGET_CHARS, chunk_pages
from core.ingest.classify import CLASSIFY_SAMPLE_CHARS, classification_sample, classify
from core.ingest.extract import extract, find_page
from core.ingest.parse import ParsedPage, parse
from core.packs import installed_packs, pack
from core.runtime.ollama import Generated, ModelUnavailable

PAGE_ONE = """SALARY ADVICE
Employee: Marcus Fernandez
Employer: Harborline Logistics Pte Ltd
Pay period: 2026-01
Gross salary: SGD 8,900.00
CPF (employee): SGD 1,780.00
Net pay: SGD 7,120.00"""

PAGE_TWO = "Employer declaration: the figures above are as recorded in our payroll system."

PAGES = [ParsedPage(1, PAGE_ONE), ParsedPage(2, PAGE_TWO)]

PAYSLIP_REPLY = {
    "employee": "Marcus Fernandez",
    "employer": "Harborline Logistics Pte Ltd",
    "pay_period": "2026-01",
    "gross_salary": "SGD 8,900.00",
    "cpf_employee": "1780.00",
    "net_pay": "7120.00",
}


class FakeOllama:
    """Answers whatever the test told it to, and records what it was asked."""

    def __init__(self, replies: list[dict[str, Any] | Exception]) -> None:
        self._replies = list(replies)
        self.schemas: list[dict[str, Any]] = []
        self.images: list[list[str]] = []

    def constrained(
        self,
        system: str,
        prompt: str,
        schema: dict[str, Any],
        *,
        images: list[str] | None = None,
        temperature: float = 0.0,
    ) -> Generated:
        self.schemas.append(schema)
        self.images.append(images or [])
        reply = self._replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        import json

        return Generated(json.dumps(reply), "fake", 1)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 768 for _ in texts]


# ----------------------------------------------------------------------------- parsing


def test_text_is_parsed_as_one_page() -> None:
    parsed = parse(b"a household document with enough text to matter", "text/plain", "note.txt")
    assert parsed.ok
    assert [page.page for page in parsed.pages] == [1]


def test_an_empty_text_file_does_not_parse() -> None:
    parsed = parse(b"   \n  ", "text/plain", "empty.txt")
    assert not parsed.ok
    assert parsed.reason is not None


def test_an_unhandled_type_quarantines_rather_than_raising() -> None:
    parsed = parse(b"\x00\x01\x02", "application/x-sqlite3", "household.db")
    assert not parsed.ok
    assert "no parser handles" in (parsed.reason or "")


# ---------------------------------------------------------------------------- chunking


def test_chunks_keep_their_page_number_and_run_in_order() -> None:
    chunks = chunk_pages(PAGES, original_name="payslip.pdf", doc_type="payslip")
    assert [c.page for c in chunks] == [1, 2]
    assert [c.ordinal for c in chunks] == [0, 1]
    assert "page 1" in chunks[0].context_prefix
    assert chunks[0].embedding_input.startswith(chunks[0].context_prefix)


def test_a_long_paragraph_is_cut_but_nothing_is_lost() -> None:
    long_page = [ParsedPage(1, "x" * (TARGET_CHARS * 3))]
    chunks = chunk_pages(long_page, original_name="policy.pdf")
    assert len(chunks) > 1
    assert all(len(c.text) <= TARGET_CHARS for c in chunks)
    assert all(c.page == 1 for c in chunks)


# -------------------------------------------------------------------- page attribution


def test_a_value_is_attributed_to_the_page_it_is_printed_on() -> None:
    assert find_page("Marcus Fernandez", PAGES) == 1
    assert find_page("payroll system", PAGES) == 2


def test_punctuation_does_not_prevent_a_match() -> None:
    assert find_page("8900.00", PAGES) == 1, "the document prints 8,900.00"


def test_a_value_on_no_page_has_no_page() -> None:
    assert find_page("Marcus Fernandes", PAGES) is None


# A real policy schedule prints "12 April 2026", and `extract` instructs the model to report
# dates as YYYY-MM-DD. Page attribution has to bridge those two, or every date field is dropped
# as "on no page" and every document whose pack requires a date quarantines. The payslip fixture
# above hides this because it prints its period as "2026-01" already.
POLICY_PAGE = """MERIDIAN ASSURANCE
POLICY SCHEDULE
Policy Number             MV-2026-448120
Name of Insured           Marcus Lim Jun Wei
Product                   Private Car Insurance Policy
Period of Insurance From  12 April 2026
Period of Insurance To    11 April 2027
Sum Insured               SGD 62,000.00
Total Premium Payable     SGD 1,284.00"""

POLICY_PAGES = [ParsedPage(1, POLICY_PAGE)]


def test_an_iso_date_is_found_on_a_page_that_prints_it_in_words() -> None:
    assert find_page("2026-04-12", POLICY_PAGES) == 1, "the page prints 12 April 2026"
    assert find_page("2027-04-11", POLICY_PAGES) == 1, "the page prints 11 April 2027"


def test_a_date_printed_in_other_common_notations_is_also_found() -> None:
    pages = [ParsedPage(1, "Cover from 01/09/2019 to 31 Aug 2049, renewed 2019-09-01.")]
    assert find_page("2019-09-01", pages) == 1, "01/09/2019 is the same day"
    assert find_page("2049-08-31", pages) == 1, "31 Aug 2049 is the same day"


def test_a_date_on_no_page_still_has_no_page() -> None:
    assert find_page("2030-01-01", POLICY_PAGES) is None, "no rendering of it is printed"


# ------------------------------------------------------------------------ classification


# A full policy document opens with a letterhead and a contents page, and the schedule that
# actually says what kind of document it is can be several pages in. Classifying on page 1 alone
# declines those, and a declined document contributes no chunks either — so the sample the
# classifier reads has to span more than the first page.
def test_the_classifier_reads_beyond_a_thin_first_page() -> None:
    thin = ParsedPage(1, "MERIDIAN ASSURANCE\nRef: b1-0002")
    schedule = ParsedPage(2, "POLICY SCHEDULE\nPolicy Number MV-2026-448120\nSum Insured SGD 1.00")
    sample = classification_sample([thin, schedule])
    assert "POLICY SCHEDULE" in sample, "the page that identifies the document must be included"
    assert "MERIDIAN ASSURANCE" in sample


def test_the_classification_sample_is_bounded() -> None:
    many = [ParsedPage(n, "x" * 5000) for n in range(1, 20)]
    assert len(classification_sample(many)) <= CLASSIFY_SAMPLE_CHARS


def test_the_classifier_may_only_choose_an_installed_document_type() -> None:
    client = FakeOllama([{"document_type": "iras_tax.payslip", "confidence": 0.95}])
    result = classify(client, PAGE_ONE)  # type: ignore[arg-type]

    assert result.pack_id == "iras_tax"
    assert result.doc_type == "payslip"
    enum = client.schemas[0]["properties"]["document_type"]["enum"]
    assert "unknown" in enum
    assert all("." in candidate for candidate in enum if candidate != "unknown")


def test_a_document_no_pack_recognises_is_not_forced_into_one() -> None:
    client = FakeOllama([{"document_type": "unknown", "confidence": 0.9}])
    result = classify(client, PAGE_ONE)  # type: ignore[arg-type]

    assert not result.recognised
    assert result.reason is not None


def test_a_low_confidence_classification_is_refused() -> None:
    client = FakeOllama([{"document_type": "iras_tax.payslip", "confidence": 0.2}])
    result = classify(client, PAGE_ONE)  # type: ignore[arg-type]

    assert not result.recognised
    assert "0.20" in (result.reason or "")


def test_an_unavailable_model_is_a_classification_failure_not_a_crash() -> None:
    client = FakeOllama([ModelUnavailable("the model is not running")])
    result = classify(client, PAGE_ONE)  # type: ignore[arg-type]

    assert not result.recognised
    assert "not running" in (result.reason or "")


# ---------------------------------------------------------------------------- extraction


@pytest.fixture
def iras() -> Any:
    return pack("iras_tax")


def test_every_extracted_fact_carries_a_page_and_the_right_column(iras: Any) -> None:
    client = FakeOllama([PAYSLIP_REPLY])
    result = extract(client, iras, "payslip", PAGES, confidence=0.95)  # type: ignore[arg-type]

    assert result.ok
    by_key = {fact.key: fact for fact in result.facts}
    assert by_key["gross_salary"].page == 1
    assert str(by_key["gross_salary"].value_num) == "8900.00"
    assert by_key["gross_salary"].column == "value_num"
    assert by_key["employee"].value_text == "Marcus Fernandez"
    assert by_key["pay_period"].value_text == "2026-01", "a month is text, not a number"
    assert all(fact.subject == "Marcus Fernandez" for fact in result.facts)


def test_the_generated_pydantic_model_is_the_decode_constraint(iras: Any) -> None:
    client = FakeOllama([PAYSLIP_REPLY])
    extract(client, iras, "payslip", PAGES, confidence=0.9)  # type: ignore[arg-type]

    schema = client.schemas[0]
    assert set(schema["properties"]) == {
        "employee",
        "employer",
        "pay_period",
        "gross_salary",
        "cpf_employee",
        "net_pay",
    }


def test_a_value_printed_on_no_page_is_dropped_not_stored(iras: Any) -> None:
    invented = {**PAYSLIP_REPLY, "employer": "Some Other Company Pte Ltd"}
    client = FakeOllama([invented])
    result = extract(client, iras, "payslip", PAGES, confidence=0.9)  # type: ignore[arg-type]

    assert not result.ok, "employer is required and is on no page"
    assert "employer" in (result.reason or "")
    assert "employer" not in {fact.key for fact in result.facts}


def test_an_optional_field_on_no_page_is_dropped_without_failing(iras: Any) -> None:
    reply = {**PAYSLIP_REPLY, "cpf_employee": "9999.99"}
    client = FakeOllama([reply])
    result = extract(client, iras, "payslip", PAGES, confidence=0.9)  # type: ignore[arg-type]

    assert result.ok, "cpf_employee is optional in the pack"
    assert "cpf_employee" not in {fact.key for fact in result.facts}
    assert any("cpf_employee" in item for item in result.unplaced or [])


def test_a_reply_that_does_not_satisfy_the_pack_is_a_failure(iras: Any) -> None:
    client = FakeOllama([{"employee": "Marcus Fernandez"}])
    result = extract(client, iras, "payslip", PAGES, confidence=0.9)  # type: ignore[arg-type]

    assert not result.ok
    assert result.reason is not None


# The system prompt tells the model to "leave it null" for a field that is not printed. A model
# under a JSON-schema decode constraint on a string-typed slot obliges literally, with the four
# characters n-u-l-l. Without this, an absent optional field fails Decimal validation and takes
# the whole document to quarantine — chunks included.
@pytest.fixture
def insurance() -> Any:
    return pack("insurance_agent")


SCHEDULE_REPLY = {
    "insurer": "Meridian Assurance",
    "policy_no": "MV-2026-448120",
    "insured": "Marcus Lim Jun Wei",
    "product_name": "Private Car Insurance Policy",
    "cover_from": "2026-04-12",
    "expiry_date": "2027-04-11",
    "premium_payable": "1284.00",
    "sum_insured": "62000.00",
}


def test_a_schedule_printing_dates_in_words_extracts(insurance: Any) -> None:
    client = FakeOllama([SCHEDULE_REPLY])
    result = extract(  # type: ignore[arg-type]
        client, insurance, "policy_schedule", POLICY_PAGES, confidence=0.9
    )
    assert result.ok, result.reason
    by_key = {fact.key: fact for fact in result.facts}
    assert by_key["cover_from"].value_date is not None
    assert by_key["expiry_date"].page == 1


@pytest.mark.parametrize("absent", ["null", "NULL", "none", "N/A", "-", "not applicable"])
def test_a_null_shaped_string_is_an_absent_field_not_a_bad_number(
    insurance: Any, absent: str
) -> None:
    reply = {**SCHEDULE_REPLY, "excess": absent}
    client = FakeOllama([reply])
    result = extract(  # type: ignore[arg-type]
        client, insurance, "policy_schedule", POLICY_PAGES, confidence=0.9
    )
    assert result.ok, result.reason
    assert "excess" not in {fact.key for fact in result.facts}


def test_a_null_shaped_string_in_a_required_field_is_still_a_failure(insurance: Any) -> None:
    reply = {**SCHEDULE_REPLY, "premium_payable": "null"}
    client = FakeOllama([reply])
    result = extract(  # type: ignore[arg-type]
        client, insurance, "policy_schedule", POLICY_PAGES, confidence=0.9
    )
    assert not result.ok, "a required field really is missing"
    assert "premium_payable" in (result.reason or "")
    assert "decimal" not in (result.reason or "").casefold(), "say it is missing, not malformed"


# --------------------------------------------------------------------------------- packs


def test_the_template_directory_is_not_an_installed_pack() -> None:
    ids = {installed.id for installed in installed_packs()}
    assert ids == {"iras_tax", "insurance_agent"}


def test_every_document_type_has_a_generated_model() -> None:
    for installed in installed_packs():
        assert set(installed.manifest.document_types) <= set(installed.models)


# ------------------------------------------------------- the pack's names, and only those


def _page_of_examples(spec: Any) -> list[ParsedPage]:
    """One page printing every field's `example`, so each value is attributable to a page."""
    return [ParsedPage(1, "\n".join(f"{f.name}: {f.example}" for f in spec.fields))]


def _reply_of_examples(spec: Any) -> dict[str, Any]:
    return {f.name: f.example for f in spec.fields}


@pytest.mark.parametrize(
    ("pack_id", "doc_type"),
    [
        (installed.id, doc_type)
        for installed in installed_packs()
        for doc_type in installed.manifest.document_types
    ],
)
def test_a_fact_is_stored_under_the_name_the_pack_declares(pack_id: str, doc_type: str) -> None:
    """`FieldSpec.name` is the `facts.key`. Nothing between the manifest and the row renames it.

    Regression: iras_tax renamed `amount` to `donation_amount` at 0.2.0, and rows written by
    0.1.0 still carry the old key. That was stale data rather than a lost key, but the reason
    it was hard to tell apart is that no test pinned the two names together. This one does,
    for every document type of every installed pack.
    """
    installed = pack(pack_id)
    spec = installed.spec(doc_type)
    declared = {field.name for field in spec.fields}

    client = FakeOllama([_reply_of_examples(spec)])
    result = extract(  # type: ignore[arg-type]
        client, installed, doc_type, _page_of_examples(spec), confidence=0.9
    )

    assert result.ok, result.reason
    keys = {fact.key for fact in result.facts}
    assert keys <= declared, f"extraction invented {sorted(keys - declared)}"
    assert {f.name for f in spec.fields if f.required} <= keys
    assert set(client.schemas[0]["properties"]) == declared


def test_a_donation_receipt_stores_donation_amount_and_never_amount() -> None:
    """The named regression, spelled out so a future rename cannot quietly reintroduce it."""
    installed = pack("iras_tax")
    spec = installed.spec("donation_receipt")

    client = FakeOllama([_reply_of_examples(spec)])
    result = extract(  # type: ignore[arg-type]
        client, installed, "donation_receipt", _page_of_examples(spec), confidence=0.9
    )

    keys = {fact.key for fact in result.facts}
    assert "donation_amount" in keys
    assert "amount" not in keys, "the 0.1.0 name must not come back"
