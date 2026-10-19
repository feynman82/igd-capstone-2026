"""Extract a document type's declared fields, and attribute every one of them to a page.

The generated Pydantic model is turned into a JSON schema and handed to Ollama as its decode
constraint, so the model cannot return a field the catalogue does not declare, cannot return a
string where the catalogue says money, and cannot omit a required field. That is what
"schema-constrained" means here: the constraint is applied during decoding, not validated
afterwards and retried.

Then every value is given a page. `facts.page` is NOT NULL by design, and the honest way to
fill it is to find the page whose text actually contains the value. A value that appears on no
page is a value the model produced rather than read, and it is dropped with a warning — that is
rule 2 in AGENTS.md doing its job rather than being worked around.
"""

from __future__ import annotations

import copy
import logging
import re
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from core.contracts import FACT_COLUMN, DocumentTypeSpec, FieldSpec
from core.ingest.parse import ParsedPage
from core.packs import Catalog
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


_MONTH_NUMBER: dict[str, int] = {}
for _number, _name in enumerate(_MONTHS, start=1):
    _MONTH_NUMBER[_name.casefold()] = _number
    _MONTH_NUMBER[_name[:3].casefold()] = _number
_MONTH_NUMBER["sept"] = 9

_ISO_DATE = re.compile(r"^\s*(\d{4})-(\d{2})-(\d{2})\s*$")
_DAY_MONTH_YEAR = re.compile(r"^\s*(\d{1,2})\s+([A-Za-z]+)\.?,?\s+(\d{4})\s*$")
_MONTH_DAY_YEAR = re.compile(r"^\s*([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})\s*$")
_NUMERIC_DAY_FIRST = re.compile(r"^\s*(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4})\s*$")


# The same four notations, found inside a longer value rather than as the whole of it.
_DATES_INSIDE = (
    re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)"),
    re.compile(r"(?<!\d)\d{1,2}\s+[A-Za-z]+\.?,?\s+\d{4}(?!\d)"),
    re.compile(r"\b[A-Za-z]+\.?\s+\d{1,2},?\s+\d{4}(?!\d)"),
    re.compile(r"(?<!\d)\d{1,2}[/.\-]\d{1,2}[/.\-]\d{4}(?!\d)"),
)


def printed_date(value: str) -> str | None:
    """A date as a document prints it, as YYYY-MM-DD, or None when it is not a date.

    A value that is a date and something else — "TEST 29 Feb 2024" — gives its date when it holds
    exactly one. On 19 October Rachel's three donation receipts were quarantined because a
    synthetic-record banner crossing the "Date of donation" line put the word TEST into what was
    read; a "PAID" or "COPY" stamp on a real receipt does the same. The date is printed whole, so
    reading it is not inventing one. A value holding two different dates is still None: which one
    was meant is a guess.

    The model copies the date and this converts it, because the conversion is where the model
    failed. With `format: date` in the decode schema Ollama builds a grammar that makes the model
    write four year digits before it has read the whole date, and it copied the day into them:
    "01 March 2026" came back as 0120-03-20 and "31 August 2049" as 3108-08-19. Converting in code
    is exact, and the string the model copied is still the string printed on the page, which is
    what page attribution looks for.

    Numeric dates are read day first, never month first: these are a Singapore household's
    documents, and 01/03/2026 is the first of March. Anything that is not a real calendar date —
    "For the whole of life", 31 February — is None, so it fails validation and says so rather than
    becoming a plausible wrong date.
    """
    whole = _whole_date(value)
    if whole is not None:
        return whole
    inside = {
        found
        for pattern in _DATES_INSIDE
        for match in pattern.finditer(value)
        if (found := _whole_date(match.group(0))) is not None
    }
    return inside.pop() if len(inside) == 1 else None


def _whole_date(value: str) -> str | None:
    """The value as YYYY-MM-DD when the whole of it is one date in a notation read here."""
    patterns = (
        (_ISO_DATE, "ymd"),
        (_DAY_MONTH_YEAR, "dmy"),
        (_MONTH_DAY_YEAR, "mdy"),
        (_NUMERIC_DAY_FIRST, "dmy"),
    )
    for pattern, order in patterns:
        match = pattern.match(value)
        if match is None:
            continue
        parts = dict(zip(order, match.groups(), strict=True))
        month_text = parts["m"]
        month = (
            int(month_text) if month_text.isdigit() else _MONTH_NUMBER.get(month_text.casefold())
        )
        if month is None:
            return None
        try:
            return date(int(parts["y"]), month, int(parts["d"])).isoformat()
        except ValueError:
            return None
    return None


def decode_schema(schema: dict[str, Any], fields: Sequence[FieldSpec]) -> dict[str, Any]:
    """The pack's schema as the model is held to it while it writes: dates are plain strings,
    and every field must be answered, with null for one that is not printed.

    Only the decode constraint changes. The generated Pydantic model still requires a real date,
    and `_prepare` converts what the model copied before that validation runs.

    Every key is required here, and only here, because of what the grammar does with optional
    ones. Ollama writes the required keys first and then offers the optional ones in one fixed,
    alphabetical order, each skippable — and a key passed over cannot be come back to. On
    15 October the 4B reader went from `product_name` straight to `sum_insured` on every policy
    schedule, so `date_of_birth`, `excess`, `expiry_date` and `maturity_date` were never
    written, although the prompt described them and the page printed them: 0 of 6 excesses, 4 of
    11 expiry dates. Required, each key is reached; nullable, an unprinted field is still null,
    and the generated model keeps it optional. A value invented to fill the slot is on no page
    and is dropped there, as any other.
    """
    loosened = copy.deepcopy(schema)
    properties = loosened.get("properties", {})
    loosened["required"] = list(properties)
    for field in fields:
        if field.type == "date" and field.name in properties:
            _drop_format(properties[field.name])
    return loosened


def _drop_format(node: Any) -> None:
    if isinstance(node, dict):
        node.pop("format", None)
        for option in node.get("anyOf", []):
            _drop_format(option)


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
        if spec.type == "labelled_money" and isinstance(value, list):
            prepared[name] = [
                {**item, "amount": _CURRENCY.sub("", item["amount"]).strip() or None}
                if isinstance(item, dict) and isinstance(item.get("amount"), str)
                else item
                for item in value
            ]
        elif spec.type in NUMERIC_TYPES and isinstance(value, str):
            prepared[name] = _CURRENCY.sub("", value).strip() or None
        elif _undated(spec, value):
            del prepared[name]
        elif spec.type == "date" and isinstance(value, str):
            prepared[name] = printed_date(value) or value
    return prepared


def _undated(spec: FieldSpec, value: Any) -> bool:
    """An optional date answered with words: "For the whole of life" on a whole-life policy's
    expiry line. No date is printed there, so the field is not printed, and it is dropped and
    named in `unplaced` rather than failing the document. A *required* date that cannot be read
    still fails validation, as `printed_date` intends: never a plausible wrong date, and never a
    missing one passed off as read. Before every key was required in the decode schema the
    reader skipped this slot; now it must answer it, and it answers with what is printed."""
    return (
        spec.type == "date"
        and not spec.required
        and isinstance(value, str)
        and value.strip().casefold() not in _ABSENT
        and printed_date(value) is None
    )


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


# How much of a document an extraction reads, first and at most.
#
# Every field the pack declares for a policy schedule is printed near the front, and a long
# contract behind it costs a CPU-bound model minutes of prompt evaluation for nothing. On
# 2026-09-13 a four-page policy's extraction was cut off after the engine's 180 seconds: about
# 6,000 tokens of clauses at 31 ms a token, to find values on page 1. The front is read first; the
# whole document, up to the old limit, only when the front did not satisfy the pack.
FRONT_CHARS = 8000
FULL_CHARS = 24000


def field_lines(spec: DocumentTypeSpec) -> list[str]:
    """Every field the catalogue declares, with its description, in declared order.

    The decode schema holds the model to the field names, not to what they mean. Ollama turns
    the schema into a grammar, so the model writes `"product_name": ` without ever reading
    "Product name as printed at the head of the schedule, not a category". On 15 October it
    filled that slot with the car schedule's "Coverage Type: Comprehensive Cover" line. It also
    left out every policy's expiry date and excess, because optional keys come after the required
    ones in the grammar, in alphabetical order, with nothing to say they matter. The descriptions
    are written in `core/documents.yaml` for exactly this reader, so they are given to it.
    """
    return [
        f"- {field.name}{'' if field.required else ' (if printed)'}: {field.description}"
        for field in spec.fields
    ]


def extract(
    client: Ollama,
    documents: Catalog,
    doc_type: str,
    pages: list[ParsedPage],
    *,
    confidence: float,
) -> Extraction:
    """Never raises. A failure is a reason, and a reason routes the document to quarantine."""
    spec = documents.spec(doc_type)
    model_cls = documents.models[doc_type]
    schema = decode_schema(model_cls.model_json_schema(), spec.fields)

    full_text = "\n\n".join(f"[page {p.page}]\n{p.text}" for p in pages)
    windows = [full_text[:FRONT_CHARS]]
    if len(full_text) > FRONT_CHARS:
        windows.append(full_text[:FULL_CHARS])
    result = Extraction(False, [], reason="there was no text to read")
    for document_text in windows:
        result = _read(client, spec, model_cls, schema, doc_type, pages, document_text, confidence)
        # A model that did not answer a short prompt will not answer a longer one.
        if result.ok or result.model is None:
            return result
    return result


def _read(
    client: Ollama,
    spec: DocumentTypeSpec,
    model_cls: Any,
    schema: dict[str, Any],
    doc_type: str,
    pages: list[ParsedPage],
    document_text: str,
    confidence: float,
) -> Extraction:
    """One extraction attempt against one window of the document's text.

    Page attribution still searches every page: a window limits what the model reads, not where a
    value it reports is allowed to be found.
    """
    # The rules below are not generic prompt padding: each one names a mistake the 4B generator
    # actually made on batch 1's full policy documents. On b1-0033 it reported the insurer as the
    # insured and took "Ref: b1-0033" from the page footer as the policy number. Its year-120
    # dates were not invented but forced — see `printed_date` — which is why dates are copied
    # as printed and converted afterwards rather than converted by the model.
    prompt = "\n".join(
        [
            f"This document is a {doc_type.replace('_', ' ')}: {spec.description}.",
            "Report these fields, copying each value exactly as printed:",
            *field_lines(spec),
            "Write amounts as plain numbers: 8900.00, not SGD 8,900.00.",
            "",
            "The document may run to many pages. The schedule table near the front is where these",
            "fields are printed; the wording, benefit tables and clauses after it are not.",
            "",
            "Rules, each of which has been got wrong before:",
            "- The company on the letterhead is the insurer. The person the policy covers is the",
            "  insured. They are never the same value.",
            "- A reference like 'Ref: b1-0007' is a filing reference, not a policy number.",
            "- Copy every date exactly as it is printed, for example 12 April 2026. Do not",
            "  convert it to another format, and never construct a date that is not printed.",
            "- Read an amount digit by digit. 2,040.00 is 2040.00, not 2000.00.",
            "- If a field is not printed anywhere, omit it. Do not write null as the value.",
            "",
            "<<<",
            document_text,
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
    unplaced: list[str] = [
        f"{name} {reported[name]!r} (not a date)"
        for name, field_spec in index.items()
        if _undated(field_spec, reported.get(name))
    ]
    for name, field_spec in index.items():
        raw = getattr(validated, name, None)
        if raw is None:
            continue
        if field_spec.type == "labelled_money":
            # One fact per printed row: the label in value_text, the amount in value_num, so the
            # pairing lives in the row (ADR 0017). A row is placed by its amount, as money is.
            for item in raw:
                page = find_page(f"{item.amount}", pages)
                if page is None or not item.label.strip():
                    unplaced.append(f"{name} {item.label!r} (on no page)")
                    continue
                facts.append(
                    ExtractedFact(
                        key=name,
                        page=page,
                        subject=subject_value,
                        value_text=item.label.strip(),
                        value_num=Decimal(item.amount),
                        value_date=None,
                        confidence=confidence,
                    )
                )
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
