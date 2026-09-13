"""Extract a pack's declared fields, and attribute every one of them to a page.

The generated Pydantic model is turned into a JSON schema and handed to Ollama as its decode
constraint, so the model cannot return a field the pack does not declare, cannot return a
string where the pack says money, and cannot omit a required field. That is what
"schema-constrained" means here: the constraint is applied during decoding, not validated
afterwards and retried.

Then every value is given a page. `facts.page` is NOT NULL by design, and the honest way to
fill it is to find the page whose text actually contains the value. A value that appears on no
page is a value the model produced rather than read, and it is dropped with a warning — that is
rule 2 in AGENTS.md doing its job rather than being worked around.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from core.contracts import FACT_COLUMN, FieldSpec
from core.ingest.parse import ParsedPage
from core.packs import InstalledPack
from core.runtime.ollama import ModelUnavailable, Ollama

log = logging.getLogger(__name__)

SYSTEM = (
    "You read one household document and report only what is printed on it. You copy values "
    "exactly as they appear: policy numbers, receipt numbers and amounts are transcribed, never "
    "reformatted or corrected. If a field is not printed on the document, omit it rather than "
    "inferring it, and never write the word null as if it were the value."
)

# A value the model reports must be findable on a page. Numbers are compared with punctuation
# stripped, because a document prints 8,900.00 and the model reports 8900.00 - the same value.
_PUNCTUATION = re.compile(r"[^0-9a-z]")


@dataclass(frozen=True, slots=True)
class ExtractedFact:
    key: str
    page: int
    subject: str | None
    value_text: str | None
    value_num: Decimal | None
    value_date: date | None
    confidence: float

    @property
    def column(self) -> str:
        if self.value_num is not None:
            return "value_num"
        if self.value_date is not None:
            return "value_date"
        return "value_text"


@dataclass(frozen=True, slots=True)
class Extraction:
    ok: bool
    facts: list[ExtractedFact]
    model: str | None = None
    latency_ms: int = 0
    reason: str | None = None
    unplaced: list[str] | None = None  # reported fields no page could support


def _normalise(value: str) -> str:
    return _PUNCTUATION.sub("", value.casefold())


_MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def _date_renderings(value: str) -> list[str]:
    """Every common way a household document prints this date, given it as YYYY-MM-DD.

    `extract` instructs the model to report dates as YYYY-MM-DD, and almost no document prints
    them that way — a Singapore policy schedule says "12 April 2026". Looking the ISO string up
    on the page therefore finds nothing, the field is dropped as "on no page", and a pack that
    requires the date sends the whole document to quarantine with its chunks. So the page lookup
    compares against the renderings rather than against the one notation the model was asked for.

    An empty list means the value is not a date, and the caller falls back to a literal match.
    """
    try:
        printed = date.fromisoformat(value.strip()[:10])
    except ValueError:
        return []
    month = _MONTHS[printed.month - 1]
    day, year = printed.day, printed.year
    return [
        value,
        f"{day:02d} {month} {year}",
        f"{day} {month} {year}",
        f"{day:02d} {month[:3]} {year}",
        f"{day} {month[:3]} {year}",
        f"{month} {day}, {year}",
        f"{day:02d}/{printed.month:02d}/{year}",
        f"{year}/{printed.month:02d}/{day:02d}",
    ]


def find_page(value: str, pages: list[ParsedPage]) -> int | None:
    """The first page whose text contains this value. None means no page supports it.

    A date matches any notation it might be printed in; everything else matches literally, with
    punctuation ignored so that a page printing 8,900.00 supports a reported 8900.00.
    """
    needles = [
        needle
        for needle in (_normalise(rendering) for rendering in _date_renderings(value) or [value])
        if len(needle) >= 2
    ]
    if not needles:
        return None
    for page in pages:
        haystack = _normalise(page.text)
        if any(needle in haystack for needle in needles):
            return page.page
    return None


NUMERIC_TYPES = frozenset({"money", "integer", "percent"})
_CURRENCY = re.compile(r"(?i)\b(sgd|usd|myr|rm)\b|[$,\s]")


# What a model writes when it means "this field is not printed on the document".
_ABSENT = frozenset(
    {
        "",
        "-",
        "--",
        "n/a",
        "na",
        "nil",
        "none",
        "not applicable",
        "not printed",
        "not stated",
        "null",
    }
)


def _prepare(index: dict[str, FieldSpec], reported: dict[str, Any]) -> dict[str, Any]:
    """Strip currency and thousands separators from numeric fields before validation.

    A document prints "SGD 8,900.00" and a model that transcribes it faithfully reports that
    string. The pack declares the field as money, so the presentation is removed and the value
    kept. Only fields the pack itself declares numeric are touched, and the raw reply is kept
    for page attribution: a page must contain what was printed, not what was normalised.

    A field the model says is absent is *removed* rather than passed through. Under a JSON-schema
    decode constraint a model asked to leave a field null will write the four characters `null`
    into a string slot, and `Decimal("null")` is a validation error that quarantines the whole
    document — chunks included — over a field that was legitimately not printed. An absent key
    says "not printed" in the one way the generated model understands: optional fields stay
    optional, and a required one fails as missing rather than as malformed.
    """
    prepared = {
        name: value
        for name, value in reported.items()
        if not (isinstance(value, str) and value.strip().casefold() in _ABSENT)
    }
    for name, spec in index.items():
        value = prepared.get(name)
        if spec.type in NUMERIC_TYPES and isinstance(value, str):
            prepared[name] = _CURRENCY.sub("", value).strip() or None
    return prepared


def _coerce(spec: FieldSpec, raw: Any) -> tuple[str | None, Decimal | None, date | None] | None:
    """Put the value in the one `facts` column its declared type maps to, or reject it."""
    column = FACT_COLUMN[spec.type]
    text = str(raw).strip()
    if not text:
        return None
    if column == "value_num":
        try:
            return None, Decimal(text.replace(",", "").replace("SGD", "").strip()), None
        except (InvalidOperation, ArithmeticError):
            return None
    if column == "value_date":
        try:
            return None, None, date.fromisoformat(text[:10])
        except ValueError:
            return None
    return text, None, None


def extract(
    client: Ollama,
    installed: InstalledPack,
    doc_type: str,
    pages: list[ParsedPage],
    *,
    confidence: float,
) -> Extraction:
    """Never raises. A failure is a reason, and a reason routes the document to quarantine."""
    spec = installed.spec(doc_type)
    model_cls = installed.models[doc_type]
    schema = model_cls.model_json_schema()

    # The rules below are not generic prompt padding: each one names a mistake the 4B generator
    # actually made on batch 1's full policy documents. On b1-0033 it reported the insurer as the
    # insured, took "Ref: b1-0033" from the page footer as the policy number, and invented
    # cover_from 0120-01-20 and expiry_date 0120-12-31 — dates in the year 120 that appear
    # nowhere. Page attribution caught the invented dates, but a document only has to lose one
    # required field to quarantine with its chunks, so it is cheaper to say what not to do.
    prompt = "\n".join(
        [
            f"This document is a {doc_type.replace('_', ' ')}: {spec.description}.",
            "Report the fields defined by the schema, copying each value exactly as printed.",
            "Write amounts as plain numbers: 8900.00, not SGD 8,900.00. Write dates as YYYY-MM-DD.",
            "",
            "The document may run to many pages. The schedule table near the front is where these",
            "fields are printed; the wording, benefit tables and clauses after it are not.",
            "",
            "Rules, each of which has been got wrong before:",
            "- The company on the letterhead is the insurer. The person the policy covers is the",
            "  insured. They are never the same value.",
            "- A reference like 'Ref: b1-0007' is a filing reference, not a policy number.",
            "- Every date you report must be printed on the document. Convert 12 April 2026 to",
            "  2026-04-12; never construct a date, and never report a year before 1900.",
            "- Read an amount digit by digit. 2,040.00 is 2040.00, not 2000.00.",
            "- If a field is not printed anywhere, omit it. Do not write null as the value.",
            "",
            "<<<",
            "\n\n".join(f"[page {p.page}]\n{p.text}" for p in pages)[:24000],
            ">>>",
        ]
    )
    try:
        generated = client.constrained(SYSTEM, prompt, schema)
        reported = generated.json()
    except ModelUnavailable as error:
        return Extraction(False, [], reason=str(error))

    index = {f.name: f for f in spec.fields}
    try:
        validated = model_cls.model_validate(_prepare(index, reported))
    except Exception as error:  # pydantic ValidationError, kept broad: any failure quarantines
        return Extraction(False, [], generated.model, generated.latency_ms, f"schema: {error}")

    subject_field = spec.subject_field
    subject_value: str | None = None
    if subject_field:
        raw_subject = getattr(validated, subject_field, None)
        subject_value = str(raw_subject).strip() if raw_subject else None

    facts: list[ExtractedFact] = []
    unplaced: list[str] = []
    for name, field_spec in index.items():
        raw = getattr(validated, name, None)
        if raw is None:
            continue
        coerced = _coerce(field_spec, raw)
        if coerced is None:
            unplaced.append(f"{name} (not a valid {field_spec.type})")
            continue
        printed = reported.get(name)
        page = find_page(str(printed) if printed is not None else str(raw), pages)
        if page is None:
            unplaced.append(f"{name} (on no page)")
            log.info("dropping %s: no page in the document contains it", name)
            continue
        value_text, value_num, value_date = coerced
        facts.append(
            ExtractedFact(
                key=name,
                page=page,
                subject=subject_value,
                value_text=value_text,
                value_num=value_num,
                value_date=value_date,
                confidence=confidence,
            )
        )

    required_missing = [
        name for name, f in index.items() if f.required and name not in {fact.key for fact in facts}
    ]
    if required_missing:
        return Extraction(
            False,
            facts,
            generated.model,
            generated.latency_ms,
            f"required fields not found on any page: {', '.join(sorted(required_missing))}",
            unplaced or None,
        )
    return Extraction(True, facts, generated.model, generated.latency_ms, None, unplaced or None)
