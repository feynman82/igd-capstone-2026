"""Which stretch of time a question asks about, and which stretch a document speaks for.

"What was the premium on the car policy last year?" has one car schedule on file, and it covers
12 April 2026 to 11 April 2027. On 17 October the answer was "The premium on the car policy last
year was SGD 1,284.00" — a number the schedule prints, cited to the page that prints it, and every
check the gate makes passed. What was wrong was the year. The model had been told the date and
still answered about 2025 from a document that begins in 2026.

So when a question names a past period in so many words, a sentence answering it must cite a
document whose own dates reach into that period. The dates are the facts extraction read off the
page, so this is decided by code from what is printed, not by asking the model again.

Only relative periods are read: "last year", "last month". A question naming a year outright —
"YA2025", "my 2025 CPF statement" — is asking for a document by its label, and retrieval already
finds it by that label; refusing it here would only be a second way to be wrong.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from core.packs import catalog


@dataclass(frozen=True, slots=True)
class Period:
    """A stretch of days, both ends included."""

    start: date
    end: date

    def overlaps(self, other: Period) -> bool:
        return self.start <= other.end and other.start <= self.end

    def __str__(self) -> str:
        if self.end == date.max:
            return f"{self.start:%d %b %Y} onwards"
        return f"{self.start:%d %b %Y} to {self.end:%d %b %Y}"


# Document types whose printed dates mark the start of an arrangement that then runs on, with no
# end printed: a housing loan's letter is dated 2021 and the loan is still being repaid. Their span
# runs from that start with no end, so a 2021 loan answers "last year" and a loan signed after it
# does not. On 17 October `b2-0010` re-extracted with its agreement date and became a single day in
# 2021, so "how much did I repay on my home loan last year?" would have been refused as being about
# another year. This belongs in the catalogue, beside each type's fields — `core/documents.yaml` has
# no place for it yet, and giving it one is a change to `core/contracts.py`, its own reviewed PR.
STANDING = frozenset({"loan_agreement"})

_LAST_YEAR = re.compile(r"\b(?:last|previous|past)\s+year'?s?\b", re.IGNORECASE)
_LAST_MONTH = re.compile(r"\b(?:last|previous|past)\s+month'?s?\b", re.IGNORECASE)


def asked_period(question: str, today: date) -> Period | None:
    """The calendar period a question names relative to today, or None when it names none.

    "Last year" is the previous calendar year and "last month" the previous calendar month: the
    way a person filing a household's papers means them, not the trailing twelve months.
    """
    if _LAST_MONTH.search(question):
        first = today.replace(day=1)
        year, month = (first.year - 1, 12) if first.month == 1 else (first.year, first.month - 1)
        return Period(date(year, month, 1), date.fromordinal(first.toordinal() - 1))
    if _LAST_YEAR.search(question):
        return Period(date(today.year - 1, 1, 1), date(today.year - 1, 12, 31))
    return None


def _month(value: str) -> Period | None:
    match = re.fullmatch(r"\s*(\d{4})-(\d{2})\s*", value)
    if match is None:
        return None
    year, month = int(match.group(1)), int(match.group(2))
    if not 1 <= month <= 12:
        return None
    following = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    return Period(date(year, month, 1), date.fromordinal(following.toordinal() - 1))


def _year(value: str | float | int | Decimal, *, before: bool) -> Period | None:
    try:
        year = int(float(value)) - (1 if before else 0)
    except (TypeError, ValueError):
        return None
    return Period(date(year, 1, 1), date(year, 12, 31)) if 1900 <= year <= 2200 else None


def document_period(doc_type: str, facts: Iterable[tuple[str, object]]) -> Period | None:
    """The span of time a document's own printed dates cover, or None when it prints none.

    `facts` are (key, value) pairs as `facts` stores them. What counts is decided by the type the
    catalogue declares for the field, so a new document type is covered without a change here:

    - a `date` is a day the document speaks for, except a date of birth, which is a person's;
    - a `month` (a payslip's pay period) is that whole month;
    - an integer `..._year` (a statement year) is that whole year, except an assessment year,
      which assesses the income of the year before it — YA2026 is about 2025.

    The span runs from the earliest to the latest of these: a policy from its cover date to its
    expiry, a receipt for its one day. A `STANDING` type runs from its earliest date with no end.
    """
    spec = catalog().documents.document_types.get(doc_type)
    if spec is None:
        return None
    types = {field.name: field.type for field in spec.fields}
    found = [
        span for key, value in facts if (span := _span(key, types.get(key), value)) is not None
    ]
    if not found:
        return None
    start = min(p.start for p in found)
    return Period(start, date.max if doc_type in STANDING else max(p.end for p in found))


def _span(key: str, kind: str | None, value: object) -> Period | None:
    """The stretch of time one printed fact speaks for, by the type the catalogue declares."""
    if kind == "date" and "birth" not in key and isinstance(value, date):
        return Period(value, value)
    if kind == "month" and isinstance(value, str):
        return _month(value)
    # `facts.value_num` comes back as a Decimal: a statement year is read from there.
    numeric = (str, int, float, Decimal)
    if kind == "integer" and key.endswith("_year") and isinstance(value, numeric):
        return _year(value, before=key == "assessment_year")
    return None


def outside(asked: Period, cited: Iterable[object], periods: Mapping[str, Period | None]) -> bool:
    """Whether a sentence citing these documents is answering about some other time.

    True when no cited document's period reaches into the one asked about — including when a
    cited document prints no date at all, because a claim about last year that cannot be placed
    in last year is not supported by being placed nowhere.
    """
    spans = [periods.get(str(document_id)) for document_id in cited]
    return not any(span is not None and span.overlaps(asked) for span in spans)
