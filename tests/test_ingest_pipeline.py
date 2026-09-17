"""Parsing, chunking, extraction and the quarantine decision.

The model is faked. What is being tested is the pipeline's judgement: that a page number is
attributed from the page the value is actually printed on, that a value printed on no page is
refused rather than stored, and that anything short of a satisfied pack goes to quarantine
instead of writing half a document.

The fixture document is the payslip from `packs/iras_tax/pack.yaml`'s own examples, so the
expected values are the pack's ground truth rather than something invented here.
"""

from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace
from typing import Any

import pytest

from core.ingest.chunk import TARGET_CHARS, chunk_pages
from core.ingest.classify import CLASSIFY_SAMPLE_CHARS, classification_sample, classify
from core.ingest.extract import extract, find_page
from core.ingest.parse import ParsedPage, parse
from core.packs import CORE, catalog, installed_packs
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
        self.prompts: list[str] = []
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
        self.prompts.append(prompt)
        self.images.append(images or [])
        reply = self._replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        import json

        return Generated(json.dumps(reply), "fake", 1)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 768 for _ in texts]

    def embed_documents(self, items: list[tuple[str, str]]) -> list[list[float]]:
        return self.embed([text for _title, text in items])

    def embed_query(self, text: str) -> list[float]:
        return self.embed([text])[0]


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
    assert "".join(c.text for c in chunks) == "x" * (TARGET_CHARS * 3)


# 13 September: a four-page policy's page was one "paragraph" to the old splitter, so chunks were
# cut every 1,050 characters — "e payment of the required Annual Premium", "llness or accidental
# injury" — and "what is the waiting period for appendicitis?" retrieved the definitions page.

CLAUSE = (
    "6.1\tInitial\tGeneral\tWaiting\tPeriod: A general Waiting Period of thirty days applies from "
    "the Policy Commencement Date. Acute conditions such as appendicitis are covered once it has "
    "passed. "
)


def _policy_page() -> ParsedPage:
    from core.ingest.parse import Block

    blocks = (
        Block("heading", "POLICY SCHEDULE"),
        Block("table", "Policy Number: PH-2022-604188\nName of Insured: Marcus Lim Jun Wei"),
        Block("heading", "6. WAITING PERIODS AND PRE-EXISTING CONDITIONS"),
        *(Block("text", CLAUSE * 2) for _ in range(4)),
        Block("heading", "PrivateCare Hospital and Surgical Plan FULL POLICY CONTRACT"),
    )
    return ParsedPage(3, "\n".join(b.text for b in blocks), blocks)


def test_a_chunk_never_starts_or_ends_inside_a_word() -> None:
    page = _policy_page()
    words = set(" ".join(page.text.split()).split(" "))
    chunks = chunk_pages([page], original_name="privatecare.pdf", doc_type="policy_schedule")
    assert len(chunks) > 2
    for chunk in chunks:
        assert "\t" not in chunk.text, "tabs between words are collapsed"
        assert set(" ".join(chunk.text.split()).split(" ")) <= words, chunk.text[:80]
        assert len(chunk.text) <= TARGET_CHARS


def test_every_chunk_under_a_heading_is_named_by_it_and_a_heading_alone_is_not_kept() -> None:
    chunks = chunk_pages(
        [_policy_page()],
        original_name="privatecare.pdf",
        doc_type="policy_schedule",
        title="Meridian Assurance, PrivateCare Hospital and Surgical Plan",
    )
    schedule, *clauses = chunks
    assert schedule.text.startswith("POLICY SCHEDULE\nPolicy Number: PH-2022-604188")
    assert clauses and all("6. WAITING PERIODS" in c.context_prefix for c in clauses)
    assert clauses[0].text.startswith("6. WAITING PERIODS"), "the first chunk shows its heading"
    assert not any(c.text.startswith("PrivateCare Hospital") for c in chunks)
    assert chunks[0].context_prefix == (
        "Meridian Assurance, PrivateCare Hospital and Surgical Plan — policy schedule — "
        "POLICY SCHEDULE — page 3"
    )
    assert all(c.title.startswith("Meridian Assurance") for c in chunks)


def test_a_page_without_parser_structure_still_breaks_at_capitalised_headings() -> None:
    page = ParsedPage(1, "SALARY ADVICE\nEmployee: Marcus Fernandez\nGross salary: SGD 8,900.00")
    [chunk] = chunk_pages([page], original_name="payslip.pdf", doc_type="payslip")
    assert "SALARY ADVICE" in chunk.context_prefix
    assert chunk.text.startswith("SALARY ADVICE\nEmployee")


def test_docling_headings_become_heading_blocks() -> None:
    from core.ingest.parse import _pages_from

    heading = SimpleNamespace(
        text="6. WAITING PERIODS", label=SimpleNamespace(value="section_header"), prov=[]
    )
    body = SimpleNamespace(text="6.1 Initial General Waiting Period", label="text", prov=[])
    [page] = _pages_from(SimpleNamespace(iterate_items=lambda: [(heading, 0), (body, 0)]))
    assert [(b.kind, b.text) for b in page.blocks] == [
        ("heading", "6. WAITING PERIODS"),
        ("text", "6.1 Initial General Waiting Period"),
    ]
    assert page.text == "6. WAITING PERIODS\n6.1 Initial General Waiting Period"


def test_a_document_is_titled_by_the_string_fields_its_pack_declares(insurance: Any) -> None:
    from core.ingest.pipeline import document_title

    facts = [
        SimpleNamespace(key="policy_no", value_text="PH-2022-604188"),
        SimpleNamespace(key="product_name", value_text="PrivateCare Hospital and Surgical Plan"),
        SimpleNamespace(key="insurer", value_text="Meridian Assurance"),
        SimpleNamespace(key="insured", value_text="Marcus Lim Jun Wei"),
    ]
    title = document_title(insurance, "policy_schedule", facts, "b1-0032.pdf")
    assert title == "Meridian Assurance, PrivateCare Hospital and Surgical Plan"
    assert document_title(insurance, "policy_schedule", [], "b1-0032.pdf") == "b1-0032.pdf"


def test_reindexing_replaces_chunks_and_leaves_facts_alone(insurance: Any) -> None:
    from core.ingest.reindex import IndexedDocument, reindex_document

    class Cursor:
        def __init__(self, log: list[str]) -> None:
            self.log = log

        def execute(self, query: str, params: Any = None) -> None:
            self.log.append(query)

        def fetchall(self) -> list[tuple[Any, ...]]:
            return [("insurer", "Meridian Assurance")]

        def __enter__(self) -> Cursor:
            return self

        def __exit__(self, *exc: object) -> None:
            return None

    class Conn:
        def __init__(self) -> None:
            self.log: list[str] = []
            self.commits = 0

        def cursor(self) -> Cursor:
            return Cursor(self.log)

        def commit(self) -> None:
            self.commits += 1

        def rollback(self) -> None:
            raise AssertionError("nothing failed")

    conn = Conn()
    document = IndexedDocument("doc", "policy.txt", "text/plain", "policy_schedule", CORE)
    count = reindex_document(conn, FakeOllama([]), document, PAGE_ONE.encode())

    assert count == 1
    assert conn.commits == 1
    assert sum("INSERT INTO chunks" in q for q in conn.log) == 1
    assert any("DELETE FROM chunks" in q for q in conn.log)
    assert not any("facts" in q and ("DELETE" in q or "INSERT" in q) for q in conn.log)


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

# The front of Marcus's identity card, as OCR reads it (docs/synthetic-generation-guide.md §2.1).
IDENTITY_CARD_PAGES = [
    ParsedPage(
        1,
        "REPUBLIC OF XINKAPOW\nNATIONAL IDENTITY CARD\nIdentity Number: S8714289B\n"
        "Full Name: MARCUS LIM JUN WEI\nRace: CHINESE\nDate of Birth: 08-05-1987\nSex: M\n"
        "PROJECT PARROT · SYNTHETIC SPECIMEN · FOR RESEARCH EVALUATION ONLY",
    )
]


def test_an_iso_date_is_found_on_a_page_that_prints_it_in_words() -> None:
    assert find_page("2026-04-12", POLICY_PAGES) == 1, "the page prints 12 April 2026"
    assert find_page("2027-04-11", POLICY_PAGES) == 1, "the page prints 11 April 2027"


def test_a_date_printed_in_other_common_notations_is_also_found() -> None:
    pages = [ParsedPage(1, "Cover from 01/09/2019 to 31 Aug 2049, renewed 2019-09-01.")]
    assert find_page("2019-09-01", pages) == 1, "01/09/2019 is the same day"
    assert find_page("2049-08-31", pages) == 1, "31 Aug 2049 is the same day"


def test_a_date_of_birth_printed_day_first_with_dashes_is_found() -> None:
    assert find_page("1987-05-08", IDENTITY_CARD_PAGES) == 1, "the card prints 08-05-1987"


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


def test_the_classifier_may_only_choose_a_catalogue_document_type() -> None:
    """ADR 0017: candidates are the catalogue's types, unqualified, and every one is `core`'s."""
    client = FakeOllama([{"document_type": "payslip", "confidence": 0.95}])
    result = classify(client, PAGE_ONE)  # type: ignore[arg-type]

    assert result.pack_id == CORE
    assert result.doc_type == "payslip"
    enum = client.schemas[0]["properties"]["document_type"]["enum"]
    assert set(enum) == {*catalog().documents.document_types, "unknown"}
    assert not any("." in candidate for candidate in enum)


def test_identity_documents_and_loans_are_candidates() -> None:
    """ADR 0017 decision 6: these were quarantined because no type fitted them."""
    client = FakeOllama([{"document_type": "identity_card", "confidence": 0.9}])
    assert classify(client, IDENTITY_CARD_PAGES[0].text).doc_type == "identity_card"  # type: ignore[arg-type]
    enum = set(client.schemas[0]["properties"]["document_type"]["enum"])
    assert {"identity_card", "passport", "birth_certificate", "loan_agreement"} <= enum


def test_a_pack_qualified_type_is_not_a_candidate() -> None:
    client = FakeOllama([{"document_type": "iras_tax.payslip", "confidence": 0.95}])
    assert not classify(client, PAGE_ONE).recognised  # type: ignore[arg-type]


def test_a_document_no_pack_recognises_is_not_forced_into_one() -> None:
    client = FakeOllama([{"document_type": "unknown", "confidence": 0.9}])
    result = classify(client, PAGE_ONE)  # type: ignore[arg-type]

    assert not result.recognised
    assert result.reason is not None


def test_a_low_confidence_classification_is_refused() -> None:
    client = FakeOllama([{"document_type": "payslip", "confidence": 0.2}])
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
    return catalog()


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


def test_an_identity_card_front_extracts_its_number_name_and_date_of_birth(iras: Any) -> None:
    reply = {
        "id_number": "S8714289B",
        "full_name": "MARCUS LIM JUN WEI",
        "date_of_birth": "08-05-1987",
    }
    client = FakeOllama([reply])
    result = extract(  # type: ignore[arg-type]
        client, iras, "identity_card", IDENTITY_CARD_PAGES, confidence=0.9
    )
    assert result.ok, result.reason
    by_key = {fact.key: fact for fact in result.facts}
    assert set(by_key) == {"id_number", "full_name", "date_of_birth"}
    assert by_key["id_number"].value_text == "S8714289B"
    assert str(by_key["date_of_birth"].value_date) == "1987-05-08"
    assert all(fact.page == 1 for fact in result.facts)
    assert all(fact.subject == "MARCUS LIM JUN WEI" for fact in result.facts)


# The system prompt tells the model to "leave it null" for a field that is not printed. A model
# under a JSON-schema decode constraint on a string-typed slot obliges literally, with the four
# characters n-u-l-l. Without this, an absent optional field fails Decimal validation and takes
# the whole document to quarantine — chunks included.
@pytest.fixture
def insurance() -> Any:
    return catalog()


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
    assert set(catalog().documents.document_types) <= set(catalog().models)


def test_the_catalogue_holds_every_type_the_packs_used_to_declare() -> None:
    assert set(catalog().documents.document_types) >= {
        "policy_schedule",
        "renewal_notice",
        "claim_letter",
        "benefit_illustration",
        "policy_anniversary_statement",
        "payslip",
        "donation_receipt",
        "cpf_statement",
        "srs_statement",
        "notice_of_assessment",
    }


# ------------------------------------------------------- the pack's names, and only those


def _page_of_examples(spec: Any) -> list[ParsedPage]:
    """One page printing every field's `example`, so each value is attributable to a page."""
    return [ParsedPage(1, "\n".join(f"{f.name}: {f.example}" for f in spec.fields))]


def _reply_of_examples(spec: Any) -> dict[str, Any]:
    """Each field's example as the model reports it; a repeating one as label and amount rows."""
    return {
        f.name: (
            [
                dict(zip(("label", "amount"), row.split("="), strict=True))
                for row in f.example.split(";")
            ]
            if f.repeats
            else f.example
        )
        for f in spec.fields
    }


def test_each_rider_is_its_own_fact_with_its_name_and_sum_assured() -> None:
    """ADR 0017: several riders on one schedule, each a row pairing its label and its amount."""
    installed = catalog()
    spec = installed.spec("policy_schedule")
    reply = _reply_of_examples(spec)
    reply["riders"] = [
        {"label": "Critical Illness Rider", "amount": "SGD 150,000.00"},
        {"label": "Total Permanent Disability Rider", "amount": "300,000.00"},
    ]
    page = _page_of_examples(spec)[0].text + (
        "\nCritical Illness Rider SGD 150,000.00\nTotal Permanent Disability Rider SGD 300,000.00"
    )
    result = extract(  # type: ignore[arg-type]
        FakeOllama([reply]), installed, "policy_schedule", [ParsedPage(1, page)], confidence=0.9
    )

    riders = [(f.value_text, f.value_num, f.page) for f in result.facts if f.key == "riders"]
    assert riders == [
        ("Critical Illness Rider", Decimal("150000.00"), 1),
        ("Total Permanent Disability Rider", Decimal("300000.00"), 1),
    ]


@pytest.mark.parametrize("doc_type", list(catalog().documents.document_types))
def test_a_fact_is_stored_under_the_name_the_catalogue_declares(doc_type: str) -> None:
    """`FieldSpec.name` is the `facts.key`. Nothing between the manifest and the row renames it.

    Regression: iras_tax renamed `amount` to `donation_amount` at 0.2.0, and rows written by
    0.1.0 still carry the old key. That was stale data rather than a lost key, but the reason
    it was hard to tell apart is that no test pinned the two names together. This one does,
    for every document type in the catalogue.
    """
    installed = catalog()
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
    installed = catalog()
    spec = installed.spec("donation_receipt")

    client = FakeOllama([_reply_of_examples(spec)])
    result = extract(  # type: ignore[arg-type]
        client, installed, "donation_receipt", _page_of_examples(spec), confidence=0.9
    )

    keys = {fact.key for fact in result.facts}
    assert "donation_amount" in keys
    assert "amount" not in keys, "the 0.1.0 name must not come back"


# -------------------------------------------------------------------------- printed dates
#
# On 2026-09-13 the generator wrote cover_from "0120-03-20" for a schedule printing 01 March 2026.
# It had not invented the date. The decode schema marked the field `format: date`, Ollama turned
# that into a grammar, and the grammar made the model write four year digits before it had read
# past "01". Measured on the same page with only the schema changed, the dates came back correct
# once the format was dropped, and exactly as printed once the model was told to copy them. So
# the model copies, and code converts.


def test_dates_are_not_held_to_an_iso_grammar_while_the_model_writes(insurance: Any) -> None:
    import json

    client = FakeOllama([SCHEDULE_REPLY])
    extract(client, insurance, "policy_schedule", POLICY_PAGES, confidence=0.9)  # type: ignore[arg-type]
    schema = client.schemas[0]
    for name in ("cover_from", "expiry_date"):
        assert "format" not in json.dumps(schema["properties"][name]), name


@pytest.mark.parametrize(
    "printed,iso",
    [
        ("01 March 2026", "2026-03-01"),
        ("1 June 2015", "2015-06-01"),
        ("31 Aug 2049", "2049-08-31"),
        ("28 February 2027", "2027-02-28"),
        ("01/09/2019", "2019-09-01"),
        ("01-03-2026", "2026-03-01"),
        ("March 1, 2026", "2026-03-01"),
        ("2026-04-12", "2026-04-12"),
        ("08-05-1987", "1987-05-08"),  # an identity card's date of birth
        ("14 JUNE 2019", "2019-06-14"),  # a birth certificate prints the month in capitals
    ],
)
def test_a_printed_date_becomes_iso_in_code_not_in_the_model(printed: str, iso: str) -> None:
    from core.ingest.extract import printed_date

    assert printed_date(printed) == iso


@pytest.mark.parametrize(
    "printed", ["someday", "31 February 2026", "13/13/2026", "For the whole of life"]
)
def test_something_that_is_not_a_date_is_not_turned_into_one(printed: str) -> None:
    from core.ingest.extract import printed_date

    assert printed_date(printed) is None


def test_a_schedule_whose_dates_were_copied_as_printed_extracts(insurance: Any) -> None:
    reply = {**SCHEDULE_REPLY, "cover_from": "12 April 2026", "expiry_date": "11 April 2027"}
    client = FakeOllama([reply])
    result = extract(client, insurance, "policy_schedule", POLICY_PAGES, confidence=0.9)  # type: ignore[arg-type]
    assert result.ok, result.reason
    by_key = {fact.key: fact for fact in result.facts}
    assert str(by_key["cover_from"].value_date) == "2026-04-12"
    assert by_key["expiry_date"].page == 1, "the copied string is on the page exactly as printed"


def test_a_date_that_cannot_be_read_still_quarantines(insurance: Any) -> None:
    reply = {**SCHEDULE_REPLY, "expiry_date": "For the whole of life"}
    client = FakeOllama([reply])
    result = extract(client, insurance, "policy_schedule", POLICY_PAGES, confidence=0.9)  # type: ignore[arg-type]
    assert not result.ok
    assert "expiry_date" in (result.reason or "")


# --------------------------------------------------------------------------------- tables
#
# On 2026-09-13 Docling found a full-length policy's schedule as a table on page 1 — policy number,
# insured, period and premium, every field the pack requires — and the page text handed to the
# classifier and the extractor went straight from "POLICY SCHEDULE" to "1. PREAMBLE". A table's
# content lives in its cells, not in `.text`, and only items with text were being kept.


def _cell(text: str) -> SimpleNamespace:
    return SimpleNamespace(text=text)


def _on_page(page: int) -> list[SimpleNamespace]:
    return [SimpleNamespace(page_no=page)]


def test_a_table_is_kept_as_label_and_value_lines_in_reading_order() -> None:
    from core.ingest.parse import _pages_from

    heading = SimpleNamespace(text="POLICY SCHEDULE", prov=_on_page(1))
    schedule = SimpleNamespace(
        text=None,
        prov=_on_page(1),
        data=SimpleNamespace(
            grid=[
                [_cell("Policy Number"), _cell("PH-2022-604188")],
                [_cell("Period of Insurance From"), _cell("1 March 2026")],
            ]
        ),
    )
    clause = SimpleNamespace(text="1. PREAMBLE AND CONTRACT OF INSURANCE", prov=_on_page(1))
    document = SimpleNamespace(iterate_items=lambda: [(heading, 0), (schedule, 0), (clause, 0)])

    [page] = _pages_from(document)
    assert page.text.splitlines() == [
        "POLICY SCHEDULE",
        "Policy Number: PH-2022-604188",
        "Period of Insurance From: 1 March 2026",
        "1. PREAMBLE AND CONTRACT OF INSURANCE",
    ]


def test_a_wider_table_keeps_every_column_and_a_spanned_cell_once() -> None:
    from core.ingest.parse import _pages_from

    benefits = SimpleNamespace(
        text=None,
        prov=_on_page(3),
        data=SimpleNamespace(
            grid=[
                [_cell("Table 2"), _cell("Appendicectomy"), _cell("SGD 6,000.00")],
                [_cell("Surgical benefit"), _cell("Surgical benefit"), _cell("per operation")],
            ]
        ),
    )
    document = SimpleNamespace(iterate_items=lambda: [(benefits, 0)])

    [page] = _pages_from(document)
    assert page.page == 3
    assert page.text.splitlines() == [
        "Table 2 | Appendicectomy | SGD 6,000.00",
        "Surgical benefit: per operation",
    ]


def test_an_item_with_neither_text_nor_cells_is_still_skipped() -> None:
    from core.ingest.parse import _pages_from

    picture = SimpleNamespace(text=None, prov=_on_page(1))
    letterhead = SimpleNamespace(text="Meridian Assurance", prov=_on_page(1))
    document = SimpleNamespace(iterate_items=lambda: [(picture, 0), (letterhead, 0)])

    assert [page.text for page in _pages_from(document)] == ["Meridian Assurance"]


# ----------------------------------------------------------------------- the front first
#
# On a CPU-only machine on 2026-09-13 a four-page policy's extraction ran for three minutes and was
# cut off: the prompt carried every page, about 6,000 tokens of clauses, to find fields printed on
# page 1. The front of a document is read first, and the rest only when the front was not enough.

LONG_POLICY = [
    ParsedPage(1, POLICY_PAGE),
    ParsedPage(2, "The wording of the policy. " * 400),
    ParsedPage(3, "LATE-PAGE-MARKER General conditions."),
]


def test_a_long_document_whose_front_is_enough_is_read_once(insurance: Any) -> None:
    from core.ingest.extract import FRONT_CHARS

    client = FakeOllama([SCHEDULE_REPLY])
    result = extract(client, insurance, "policy_schedule", LONG_POLICY, confidence=0.9)  # type: ignore[arg-type]
    assert result.ok, result.reason
    assert len(client.prompts) == 1
    assert "LATE-PAGE-MARKER" not in client.prompts[0]
    assert len(client.prompts[0]) < FRONT_CHARS + 2000, "the window, plus the instructions"


def test_a_long_document_whose_front_is_not_enough_is_read_in_full(insurance: Any) -> None:
    missing = {key: value for key, value in SCHEDULE_REPLY.items() if key != "premium_payable"}
    client = FakeOllama([missing, SCHEDULE_REPLY])
    result = extract(client, insurance, "policy_schedule", LONG_POLICY, confidence=0.9)  # type: ignore[arg-type]
    assert result.ok, result.reason
    assert len(client.prompts) == 2
    assert "LATE-PAGE-MARKER" in client.prompts[1]


def test_a_short_document_is_read_once_even_when_it_fails(insurance: Any) -> None:
    client = FakeOllama([{"insurer": "Meridian Assurance"}])
    result = extract(client, insurance, "policy_schedule", POLICY_PAGES, confidence=0.9)  # type: ignore[arg-type]
    assert not result.ok
    assert len(client.prompts) == 1, "there is nothing further to read"


def test_a_model_that_does_not_answer_is_not_asked_a_longer_question(insurance: Any) -> None:
    client = FakeOllama([ModelUnavailable("the generator did not answer")])
    result = extract(client, insurance, "policy_schedule", LONG_POLICY, confidence=0.9)  # type: ignore[arg-type]
    assert not result.ok
    assert len(client.prompts) == 1
