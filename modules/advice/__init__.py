"""The advice module: hand-written calculators over cited facts and approved published values.

ADR 0016. A pack declares advice shapes, this module does the arithmetic, and the model only
explains. Everything a calculation states is one of three things: printed on a household document
(a fact, cited by document and page), published by a reviewed source (a grounding value, cited by
publisher, title and date), or a figure worked out here from those two, in `Decimal`.

Two layers, so the arithmetic is tested without a database:

- **Pure calculators over rows.** `calculate(Basis)` checks that every declared input is there,
  then dispatches on `shape.calculator`. A missing input is named in the pack's own words
  (`Missing`), never estimated around.
- **`ModuleAdviser(conn)`** runs the hand-written queries in `queries.py`, applies the category
  filter and hands the rows to `calculate`. It is the `core.graph.advice.Adviser` port, injected
  into the graph by its callers, so `core/` never imports this file.

A verdict sentence is written here from fixed templates, and states only printed and calculated
figures. It says what the numbers are. It never says what to do.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Hashable, Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from dataclasses import field as dataclass_field
from datetime import date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any

from core.contracts import Advice, AdviceShape, Categories, FactInput, RuleInput
from core.graph.advice import Adviser, Calculation, Figure, Input, Missing
from core.graph.knowledge import categorise
from core.packs import InstalledPack, installed_packs
from modules.advice import queries

CENT = Decimal("0.01")
ZERO = Decimal("0.00")
MONTHS = Decimal(12)
HUNDRED = Decimal(100)

COMPARING = frozenset({"compare_own", "compare_market"})
NUMERIC = frozenset({"gap", "remaining_room", "keep_or_surrender", "estimate_saving"})

# Not a pack's wording, because no pack input is absent: the inputs are there, and they do not
# make a comparison. Stated plainly rather than dressed as a document to go and find.
FEWER_THAN_TWO = "fewer than two to compare"
NOTHING_SHARED = "a field printed on every one compared"

# Rule values published per qualifier a calculator never matches to the household on its own.
# A product is matched by name, and a rate band by the income it contains.
MARKET_MATCHED = frozenset({"product", "insurer"})
BAND_MATCHED = frozenset({"band_lower", "band_upper"})

ORDER_WORDS = {"asc": "lowest first", "desc": "highest first"}

# The words a sentence must use to state each figure (`core.graph.advice.Figure.words`).
INCOME_WORDS = ("income", "annual", "yearly", "a year")
TARGET_WORDS = ("target", "guideline", "recommended")
HELD_WORDS = ("held", "have", "hold", "current")
GAP_WORDS = ("gap", "short", "shortfall", "more")
# A met guideline or a gain is stated as a positive figure with words that say so, never as a
# negative gap or loss: the gate reads numbers without their sign, so "a gap of -SGD 48,800.00"
# would pass as "a gap of SGD 48,800.00", which says the opposite.
ABOVE_WORDS = ("above", "over", "beyond", "more than")
GAIN_WORDS = ("gain", "more than", "above")
ROOM_WORDS = ("room", "left", "more", "remaining")
LOSS_WORDS = ("loss", "less", "lose", "difference")
SAVING_WORDS = ("save", "saving", "estimated", "less tax")

_UNIT_SUFFIX = {"multiple": " times", "percent": "%", "rate": "%", "years": " years"}

Value = Decimal | date | str | None


# -------------------------------------------------------------------------------- printing


def money(value: Decimal) -> str:
    """`SGD 188,000.00`. Every money figure is printed by this one function, so a figure and the
    sentence stating it can never print the same number two ways."""
    amount = value.quantize(CENT, rounding=ROUND_HALF_UP)
    sign = "-" if amount < 0 else ""
    return f"{sign}SGD {abs(amount):,.2f}"


def number(value: Decimal) -> str:
    """A number as a sentence states it: `4`, `11.5`, `15,300`, never `4.000` or `1.53E+4`."""
    return f"{value.normalize():,f}"


def long_date(value: date) -> str:
    """`26 September 2023`, built by hand because `%-d` does not exist on Windows."""
    return f"{value.day} {value:%B} {value.year}"


def readable(slug: str) -> str:
    return slug.replace("_", " ")


def cents(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _capital(text: str) -> str:
    return text[:1].upper() + text[1:]


# ------------------------------------------------------------------------------------ rows


@dataclass(frozen=True, slots=True)
class FactRow:
    """One row of `queries.FACTS_FOR`, with the declared type of its field.

    The type decides how the value is printed. A money fact prints as `SGD 9,400.00`, which is how
    a sentence about it states it and how the gate's number check finds it again.
    """

    fact_id: int
    document_id: Any
    name: str  # the document's original_name
    doc_type: str
    page: int
    key: str
    value: Value
    subject: str | None
    when: datetime | None  # the document's ingested_at
    field_type: str


@dataclass(frozen=True, slots=True)
class ValueRow:
    """One row of `queries.VALUES_FOR`: an approved value and the reviewed source it came from."""

    value_id: int
    key: str
    unit: str
    value_num: Decimal | None
    value_text: str | None
    qualifiers: Mapping[str, Any]
    passage: str
    effective_from: date | None
    title: str
    publisher: str
    url: str
    published_on: date | None
    retrieved_on: date

    @property
    def value(self) -> Value:
        return self.value_num if self.value_num is not None else self.value_text


def fact_row(raw: Sequence[Any], types: Mapping[tuple[str, str], str]) -> FactRow:
    (fact_id, document_id, name, doc_type, page, key, value_num, value_text, value_date) = raw[:9]
    subject, when = raw[9], raw[10]
    value: Value
    if value_num is not None:
        value = Decimal(str(value_num))
    elif value_date is not None:
        value = value_date
    else:
        value = value_text
    return FactRow(
        fact_id=int(fact_id),
        document_id=document_id,
        name=str(name),
        doc_type=str(doc_type),
        page=int(page),
        key=str(key),
        value=value,
        subject=subject,
        when=when,
        field_type=types.get((str(doc_type), str(key)), "string"),
    )


def value_row(raw: Sequence[Any]) -> ValueRow:
    (value_id, key, unit, value_num, value_text, qualifiers, passage, effective_from) = raw[:8]
    title, publisher, url, published_on, retrieved_on = raw[8:13]
    if isinstance(qualifiers, str):
        qualifiers = json.loads(qualifiers)
    return ValueRow(
        value_id=int(value_id),
        key=str(key),
        unit=str(unit),
        value_num=None if value_num is None else Decimal(str(value_num)),
        value_text=value_text,
        qualifiers=dict(qualifiers or {}),
        passage=str(passage),
        effective_from=effective_from,
        title=str(title),
        publisher=str(publisher),
        url=str(url),
        published_on=published_on,
        retrieved_on=retrieved_on,
    )


def printed(row: FactRow) -> str:
    value = row.value
    if isinstance(value, Decimal):
        if row.field_type == "money":
            return money(value)
        if row.field_type == "percent":
            return f"{number(value)}%"
        return number(value)
    if isinstance(value, date):
        return long_date(value)
    return "" if value is None else value


def printed_value(row: ValueRow) -> str:
    if row.value_num is None:
        return row.value_text or ""
    if row.unit == "money":
        return money(row.value_num)
    return f"{number(row.value_num)}{_UNIT_SUFFIX.get(row.unit, '')}"


def fact_input(role: str, row: FactRow) -> Input:
    return Input(
        ref=f"fact:{row.fact_id}",
        role=role,
        label=readable(row.key),
        value_text=printed(row),
        citation=f"{row.name}, page {row.page}",
        document_id=row.document_id,
        page=row.page,
    )


def rule_input(role: str, row: ValueRow, label: str | None = None) -> Input:
    """A published value's citation is its publisher, title and date: it has no page to open.

    The date is the page's own "last updated" when it prints one, since that is the date the
    reader can check against; otherwise the day it was retrieved.
    """
    dated = long_date(row.published_on or row.retrieved_on)
    return Input(
        ref=f"rule:{row.value_id}",
        role=role,
        label=label or readable(row.key),
        value_text=printed_value(row),
        citation=f"{row.publisher}, {row.title}, {dated}",
        publisher=row.publisher,
        title=row.title,
        dated=dated,
        url=row.url,
    )


# ------------------------------------------------------------------------------- the basis


@dataclass(frozen=True, slots=True)
class Basis:
    """Every row a calculator may read, gathered before it runs, so it can run without a database.

    `facts` and `rules` are keyed by role. `compared` holds, for a comparison, each compared
    field's facts on the same person's documents; `market` holds each compared field's published
    values when that field is also a value key.

    `qualifiers` is each value key's declared qualifiers, in the order `grounding.values` lists
    them. The pure layer has no manifest, so it is carried here: it is what names the qualifier
    that leaves a calculator more than one published value to choose from.
    """

    pack_id: str
    shape: AdviceShape
    subject: str
    person_ids: tuple[int, ...]
    facts: Mapping[str, Sequence[FactRow]]
    rules: Mapping[str, Sequence[ValueRow]]
    compared: Mapping[str, Sequence[FactRow]]
    market: Mapping[str, Sequence[ValueRow]]
    qualifiers: Mapping[str, tuple[str, ...]] = dataclass_field(default_factory=dict)


def take(rows: Sequence[FactRow], how: str) -> list[FactRow]:
    """`latest` is the newest row. `sum` and `each` keep the newest row of each document.

    A document can carry the same field twice, from a re-extraction, and without the
    per-document step one document's figure would be counted twice.

    Known limitation: `sum` counts one row per document, so a document that prints the field
    twice for two different things (a main plan and a rider on one statement, say) is
    undercounted. The facts carry no key telling a second printing from a re-extraction.
    """
    if how == "latest":
        return list(rows[:1])
    seen: set[Any] = set()
    kept: list[FactRow] = []
    for row in rows:
        if row.document_id not in seen:
            seen.add(row.document_id)
            kept.append(row)
    return kept


def in_category(
    rows: Sequence[FactRow],
    printed_names: Mapping[Any, str],
    category: str,
    categories: Categories | None,
) -> list[FactRow]:
    """Only the documents whose printed name the pack's category rules put in `category`.

    A document with no printed name is left out: a hospital cash plan must not be counted as
    critical illness cover because nobody could tell what it was.
    """
    if categories is None:
        return []
    keep = set()
    for document_id, name in printed_names.items():
        rule = categorise(name, categories)
        if rule is not None and rule.id == category:
            keep.add(document_id)
    return [row for row in rows if row.document_id in keep]


def usable(basis: Basis) -> Basis:
    """Drop rows a calculator cannot use, before deciding whether anything is missing.

    An arithmetic calculator needs numbers, so a fact or value with no number counts as not on
    file rather than as zero. A comparison can compare printed text too.
    """
    numeric = basis.shape.calculator in NUMERIC

    def fact_ok(row: FactRow) -> bool:
        return isinstance(row.value, Decimal) if numeric else row.value not in (None, "")

    def value_ok(row: ValueRow) -> bool:
        return row.value_num is not None or (not numeric and bool(row.value_text))

    return replace(
        basis,
        facts={role: [r for r in rows if fact_ok(r)] for role, rows in basis.facts.items()},
        rules={role: [r for r in rows if value_ok(r)] for role, rows in basis.rules.items()},
        compared={
            f: [r for r in rows if r.value not in (None, "")] for f, rows in basis.compared.items()
        },
        market={
            f: [r for r in rows if r.value not in (None, "")] for f, rows in basis.market.items()
        },
    )


def _missing(basis: Basis, items: Iterable[str]) -> Missing:
    """Each wording once, in first order: two inputs a pack says are on the same document share
    their wording, and the household is asked for that document once, not twice."""
    return Missing(
        pack_id=basis.pack_id,
        shape_id=basis.shape.id,
        label=basis.shape.label,
        subject=basis.subject,
        items=tuple(dict.fromkeys(items)),
    )


def _unordered(order_by: str | None) -> str:
    """What is missing when a comparison has nothing to rank: the ordering field, printed on both
    sides. Shared by both comparisons, so a ranking withholds in one wording."""
    return f"{readable(order_by or 'the ordering field')} printed on every one compared"


def withheld(basis: Basis) -> Missing | None:
    """Every fact and rule input with no rows, in the order the shape declares them.

    All of them at once, so a household is told everything it needs to file in one answer, and
    each wording once (`_missing`).
    """
    shape = basis.shape
    items = [fact.missing for fact in shape.facts if not basis.facts.get(fact.role)]
    items += [rule.missing for rule in shape.rules if not basis.rules.get(rule.role)]
    return _missing(basis, items) if items else None


def calculate(basis: Basis) -> Calculation | Missing:
    basis = usable(basis)
    if (missing := withheld(basis)) is not None:
        return missing
    return CALCULATORS[basis.shape.calculator](basis)


# ------------------------------------------------------------------------------ calculators


def _fact(shape: AdviceShape, role: str) -> FactInput:
    return next(fact for fact in shape.facts if fact.role == role)


def _rule(shape: AdviceShape, role: str) -> RuleInput:
    return next(rule for rule in shape.rules if rule.role == role)


def _number_of(value: Value) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(0)


def _calculation(
    basis: Basis,
    inputs: Iterable[Input],
    figures: Iterable[Figure],
    verdict: str,
    text: str,
    *,
    rows: tuple[tuple[str, ...], ...] = (),
    names_product: bool = False,
    estimate: bool = False,
) -> Calculation:
    unique = {item.ref: item for item in inputs}  # one input per fact or value, first use wins
    return Calculation(
        pack_id=basis.pack_id,
        shape_id=basis.shape.id,
        label=basis.shape.label,
        subject=basis.subject,
        person_ids=basis.person_ids,
        inputs=tuple(unique.values()),
        figures=tuple(figures),
        verdict=verdict,
        verdict_text=text,
        rows=rows,
        names_product=names_product,
        estimate=estimate or basis.shape.estimate,
    )


def _amount(
    basis: Basis,
    role: str,
    inputs: list[Input],
    figures: list[Figure],
    *,
    total_figure: bool = True,
) -> Decimal:
    """A role's facts, taken as the shape says, as one number, with every fact read cited.

    A monthly income is made a year's, because every published multiple and rate band is annual,
    and the year's figure is a figure of its own: no document prints it. A total over several
    documents is a figure for the same reason.

    Only income is ever multiplied. The contract refuses `per` on any other role; this refuses it
    again for a shape built without a manifest, rather than silently read a monthly total as once.
    """
    fact = _fact(basis.shape, role)
    if fact.per != "once" and role != "income":
        raise ValueError(
            f"advice shape {basis.shape.id!r} reads {role!r} per {fact.per}, "
            "which only income may be"
        )
    rows = take(basis.facts[role], fact.take)
    inputs.extend(fact_input(role, row) for row in rows)
    total = sum((_number_of(row.value) for row in rows), Decimal(0))
    if role == "income" and fact.per == "month":
        # Named for what it is, not how it was made: a passage printing "12" beside the figure
        # would be a number the gate could match a sentence against.
        yearly = cents(total * MONTHS)
        figures.append(Figure("annual income", yearly, money(yearly), INCOME_WORDS))
        return yearly
    if total_figure and len(rows) > 1:
        figures.append(Figure(role, cents(total), money(total), (readable(role), "total")))
    return total


def _qualified(row: ValueRow, name: str) -> str | None:
    raw = row.qualifiers.get(name)
    return None if raw in (None, "") else str(raw).strip()


def _ambiguous(
    rows: Sequence[ValueRow], matched: Iterable[str], declared: Sequence[str] = ()
) -> str | None:
    """The qualifier that leaves more than one published value to choose from, or `None`.

    A calculator matches some qualifiers itself (`matched`: a product by name, a rate band by
    income). Any other qualifier whose values differ across `rows` (an age band, a year) is one
    it has no household fact to match, and picking the newest row would be confident arithmetic
    on possibly the wrong band. So the first such qualifier is named instead, in the order the
    pack declares them. A row that does not carry a qualifier counts as its own value: a value
    published for every age sits beside one published for 35 to 44 and is not the same answer.
    Qualifiers a row carries that the pack does not declare are checked too, after the declared
    ones, so a `Basis` built without the declaration still refuses to guess.
    """
    skip = set(matched)
    extra = sorted({name for row in rows for name in row.qualifiers} - set(declared))
    for name in [*declared, *extra]:
        if name not in skip and len({_qualified(row, name) for row in rows}) > 1:
            return name
    return None


def _one_value(
    basis: Basis, role: str, rows: Sequence[ValueRow], matched: Iterable[str] = ()
) -> ValueRow | Missing:
    """The current published value among `rows`, or `Missing` naming the qualifier to settle.

    `VALUES_FOR` puts the latest effective value first, so with no qualifier left to settle the
    first row is the current one.
    """
    rule = _rule(basis.shape, role)
    declared = basis.qualifiers.get(rule.key, ())
    if (qualifier := _ambiguous(rows, matched, declared)) is not None:
        return _missing(basis, [rule.missing, f"which {readable(qualifier)} applies"])
    return rows[0]


def _gap(basis: Basis) -> Calculation | Missing:
    """The published guideline against what is held.

    Holding at least the guideline is stated as how far `above` it the holding is, a positive
    figure, never as a negative gap: see `ABOVE_WORDS`.
    """
    inputs: list[Input] = []
    figures: list[Figure] = []
    income = _amount(basis, "income", inputs, figures)
    held = cents(_amount(basis, "held", inputs, figures, total_figure=False))
    row = _one_value(basis, "multiple", basis.rules["multiple"])
    if isinstance(row, Missing):
        return row
    inputs.append(rule_input("multiple", row))
    target = cents(_number_of(row.value_num) * income)
    figures += [
        Figure("target", target, money(target), TARGET_WORDS),
        Figure("held", held, money(held), HELD_WORDS),
    ]
    head = (
        f"{_capital(basis.shape.label)} for {basis.subject}: the published guideline works out "
        f"to {money(target)}, and {money(held)} is held"
    )
    if (gap := target - held) > 0:
        figures.append(Figure("gap", gap, money(gap), GAP_WORDS))
        return _calculation(basis, inputs, figures, "short", f"{head}, so the gap is {money(gap)}.")
    above = held - target
    figures.append(Figure("above", above, money(above), ABOVE_WORDS))
    text = f"{head}, which meets the guideline and is {money(above)} above it."
    return _calculation(basis, inputs, figures, "meets", text)


def _remaining_room(basis: Basis) -> Calculation | Missing:
    inputs: list[Input] = []
    figures: list[Figure] = []
    used = cents(_amount(basis, "used", inputs, figures))
    row = _one_value(basis, "cap", basis.rules["cap"])
    if isinstance(row, Missing):
        return row
    inputs.append(rule_input("cap", row))
    cap = cents(_number_of(row.value_num))
    room = max(cap - used, ZERO)  # over the cap is no room, never negative room
    figures.append(Figure("room", room, money(room), ROOM_WORDS))
    text = (
        f"{_capital(basis.shape.label)} for {basis.subject}: the published cap is {money(cap)}, "
        f"and {money(used)} is used, so the room left is {money(room)}."
    )
    return _calculation(basis, inputs, figures, "room_left" if room > 0 else "no_room", text)


def _newest(rows: Iterable[FactRow]) -> FactRow:
    """The row from the most recently ingested document; the first listed wins a tie."""
    return max(rows, key=lambda row: row.when.timestamp() if row.when is not None else 0.0)


def _keep_or_surrender(basis: Basis) -> Calculation | Missing:
    """What has been paid to date against the value now, both read from one document.

    The two only compare as of the same statement: last year's paid-to-date against this
    year's value is a difference no document prints. So both come from the newest document
    that prints both. If none does, the roles the newest document leaves out are named.

    A value at or above what was paid is stated as a positive `gain`, never as a negative loss:
    see `ABOVE_WORDS`.
    """
    value_rows = basis.facts["value_now"]
    paid_rows = basis.facts["paid_to_date"]
    paid_documents = {row.document_id for row in paid_rows}
    # FACTS_FOR lists rows newest document first, so the first shared document is the newest.
    document = next(
        (row.document_id for row in value_rows if row.document_id in paid_documents), None
    )
    if document is None:
        newest = _newest([*value_rows, *paid_rows]).document_id
        printed_by = {"value_now": value_rows, "paid_to_date": paid_rows}
        absent = [
            fact.missing
            for fact in basis.shape.facts
            if fact.role in printed_by
            and all(row.document_id != newest for row in printed_by[fact.role])
        ]
        return _missing(basis, absent)

    one = replace(
        basis,
        facts={
            **basis.facts,
            "value_now": [row for row in value_rows if row.document_id == document],
            "paid_to_date": [row for row in paid_rows if row.document_id == document],
        },
    )
    inputs: list[Input] = []
    figures: list[Figure] = []
    paid = cents(_amount(one, "paid_to_date", inputs, figures))
    value_now = cents(_amount(one, "value_now", inputs, figures))
    head = (
        f"{_capital(basis.shape.label)} for {basis.subject}: {money(paid)} has been paid to date "
        f"and the value now is {money(value_now)}"
    )
    if (loss := paid - value_now) > 0:
        figures.append(Figure("loss", loss, money(loss), LOSS_WORDS))
        text = f"{head}, a difference of {money(loss)} less than has been paid."
        return _calculation(basis, inputs, figures, "loses", text)
    gain = value_now - paid
    figures.append(Figure("gain", gain, money(gain), GAIN_WORDS))
    text = f"{head}, a gain of {money(gain)} more than has been paid."
    return _calculation(basis, inputs, figures, "gains", text)


def _order_key(value: Value) -> tuple[int, Decimal, str]:
    """One sortable key for a number, a date or a word, so a ranking never compares across types."""
    if isinstance(value, Decimal):
        return (0, value, "")
    if isinstance(value, date):
        return (1, Decimal(value.toordinal()), "")
    return (2, Decimal(0), (value or "").casefold())


def _ordered(entries: Sequence[tuple[str, Hashable, Value]], order: str) -> list[Hashable]:
    """Keys ranked by value in the stated order, ties broken by name so a ranking is repeatable."""
    by_name = sorted(entries, key=lambda entry: entry[0].casefold())
    ranked = sorted(by_name, key=lambda entry: _order_key(entry[2]), reverse=order == "desc")
    return [key for _, key, _ in ranked]


def _latest_per_document(rows: Iterable[FactRow], documents: set[Any]) -> dict[Any, FactRow]:
    cells: dict[Any, FactRow] = {}
    for row in rows:
        if row.document_id in documents and row.document_id not in cells:
            cells[row.document_id] = row
    return cells


def _compare_own(basis: Basis) -> Calculation | Missing:
    """The household's own documents, compared only on fields every one of them prints.

    A field one document leaves out is dropped from the table rather than read as zero or as
    worse: a missing excess is not a low excess.
    """
    shape = basis.shape
    documents = take(basis.facts["items"], "each")
    if len(documents) < 2:
        return _missing(basis, [FEWER_THAN_TWO])
    ids = {row.document_id for row in documents}
    cells = {f: _latest_per_document(basis.compared.get(f, ()), ids) for f in shape.compare_fields}
    shared = [f for f in shape.compare_fields if len(cells[f]) == len(ids)]
    if not shared:
        return _missing(basis, [NOTHING_SHARED])
    order_by = shape.order_by
    if order_by is None or order_by not in shared:
        return _missing(basis, [_unordered(order_by)])

    by_id = {row.document_id: row for row in documents}
    order = _ordered(
        [(row.name, row.document_id, cells[order_by][row.document_id].value) for row in documents],
        shape.order,
    )
    header = ("document", *(readable(f) for f in shared))
    body = tuple((by_id[doc].name, *(printed(cells[f][doc]) for f in shared)) for doc in order)
    inputs = [fact_input("items", cells[f][doc]) for doc in order for f in shared]
    both = "both" if len(order) == 2 else "all"
    names = " then ".join(by_id[doc].name for doc in order)
    text = (
        f"Ranked by {readable(order_by)} ({ORDER_WORDS[shape.order]}), only on fields {both} "
        f"print: {names}."
    )
    return _calculation(basis, inputs, [], "ranked", text, rows=(header, *body))


def _product_name(row: ValueRow) -> str | None:
    """A market product is identified by its `product` and `insurer` qualifiers, both of them.

    A value with either missing cannot be told apart from another product's, so it is left out.
    """
    product = str(row.qualifiers.get("product") or "").strip()
    insurer = str(row.qualifiers.get("insurer") or "").strip()
    return f"{product} ({insurer})" if product and insurer else None


def _compare_market(basis: Basis) -> Calculation | Missing:
    """The held document against published products, on the compared fields both sides print.

    Each compared field is its own value key, read with the same field name from the held
    document's facts. A product enters the table only if it shares at least one field with the
    held document, is ranked only if its row shows `order_by`, and is otherwise listed after the
    ranked rows, alphabetically. The held document is ranked alongside the products.

    What is withheld is named by where it went missing: the held fact's own wording when the held
    document prints none of the compared fields, the market rule's when no product shares one,
    the qualifier to settle when a product publishes more than one value for a field (an age
    band, say), and the ordering field when nothing on either side can be ranked by it.
    """
    shape = basis.shape
    rule = _rule(shape, "market")
    held = take(basis.facts["held"], "latest")[0]
    held_cells: dict[str, FactRow] = {}
    for f in shape.compare_fields:
        rows = [held] if f == held.key else basis.compared.get(f, ())
        if (
            cell := _latest_per_document(rows, {held.document_id}).get(held.document_id)
        ) is not None:
            held_cells[f] = cell
    if not held_cells:
        return _missing(basis, [_fact(shape, "held").missing])

    market = {f: list(basis.market.get(f, ())) for f in shape.compare_fields}
    if rule.key in market and not market[rule.key]:
        market[rule.key] = list(basis.rules["market"])
    candidates: dict[str, dict[str, list[ValueRow]]] = {}
    for f in shape.compare_fields:
        if f not in held_cells:
            continue
        for row in market[f]:
            if (name := _product_name(row)) is not None:
                candidates.setdefault(name, {}).setdefault(f, []).append(row)
    if not candidates:
        return _missing(basis, [rule.missing])

    products: dict[str, dict[str, ValueRow]] = {}
    for name, by_field in candidates.items():
        for f, values in by_field.items():
            declared = basis.qualifiers.get(f, ())
            if (qualifier := _ambiguous(values, MARKET_MATCHED, declared)) is not None:
                return _missing(basis, [rule.missing, f"which {readable(qualifier)} applies"])
            products.setdefault(name, {})[f] = values[0]  # the newest current value

    columns = [f for f in shape.compare_fields if any(f in cells for cells in products.values())]
    order_by = shape.order_by or ""
    held_name = f"{held.name} (held)"
    entries: list[tuple[str, Hashable, Value]] = []
    if order_by in columns:
        entries.append((held_name, held_name, held_cells[order_by].value))
    entries += [
        (name, name, cells[order_by].value) for name, cells in products.items() if order_by in cells
    ]
    ranked = [str(key) for key in _ordered(entries, shape.order)]
    if not ranked:
        return _missing(basis, [_unordered(shape.order_by)])
    unranked = sorted(
        (name for name in [held_name, *products] if name not in ranked), key=str.casefold
    )

    header = ("name", *(readable(f) for f in columns))
    body: list[tuple[str, ...]] = []
    inputs: list[Input] = [fact_input("held", held)]
    for name in [*ranked, *unranked]:
        if name == held_name:
            body.append((name, *(printed(held_cells[f]) for f in columns)))
            inputs += [fact_input("held", held_cells[f]) for f in columns]
            continue
        cells = products[name]
        body.append((name, *(printed_value(cells[f]) if f in cells else "" for f in columns)))
        inputs += [
            rule_input("market", cells[f], f"{readable(f)} for {name}")
            for f in columns
            if f in cells
        ]

    field = readable(order_by)
    text = (
        f"Ranked by {field} ({ORDER_WORDS[shape.order]}), only on fields both print: "
        f"{' then '.join(ranked)}."
    )
    if unranked:
        text += f" Listed without {field}: {', '.join(unranked)}."
    return _calculation(basis, inputs, [], "ranked", text, rows=(header, *body), names_product=True)


def _qualifier(row: ValueRow, name: str) -> Decimal | None:
    raw = row.qualifiers.get(name)
    return None if raw in (None, "") else Decimal(str(raw))


def _band(row: ValueRow) -> tuple[Decimal | None, Decimal | None] | None:
    """A rate's income band, open at either end when a bound is not published. `None` when a
    bound is published but is not a number, so a garbled band never matches every income."""
    try:
        return _qualifier(row, "band_lower"), _qualifier(row, "band_upper")
    except InvalidOperation:
        return None


def _in_band(row: ValueRow, income: Decimal) -> bool:
    band = _band(row)
    if band is None:
        return False
    lower, upper = band
    return (lower is None or lower <= income) and (upper is None or income < upper)


def _band_label(row: ValueRow) -> str:
    band = _band(row) or (None, None)
    lower, upper = band
    if lower is None and upper is None:
        return readable(row.key)
    start = money(lower if lower is not None else Decimal(0))
    end = f"to under {money(upper)}" if upper is not None else "and above"
    return f"{readable(row.key)} for income from {start} {end}"


def _estimate_saving(basis: Basis) -> Calculation | Missing:
    inputs: list[Input] = []
    figures: list[Figure] = []
    income = cents(_amount(basis, "income", inputs, figures))
    amount = cents(_amount(basis, "amount", inputs, figures))
    in_band = [row for row in basis.rules["rate"] if _in_band(row, income)]
    if not in_band:
        return _missing(basis, [_rule(basis.shape, "rate").missing])
    band = _one_value(basis, "rate", in_band, BAND_MATCHED)
    if isinstance(band, Missing):
        return band
    inputs.append(rule_input("rate", band, _band_label(band)))
    saving = cents(amount * _number_of(band.value_num) / HUNDRED)
    figures.append(Figure("saving", saving, money(saving), SAVING_WORDS))
    text = (
        f"Estimated: {basis.shape.label} for {basis.subject}: at the published rate of "
        f"{printed_value(band)} for an income of {money(income)}, {money(amount)} gives an "
        f"estimated saving of {money(saving)}."
    )
    return _calculation(basis, inputs, figures, "estimate", text, estimate=True)


CALCULATORS: dict[str, Callable[[Basis], Calculation | Missing]] = {
    "gap": _gap,
    "remaining_room": _remaining_room,
    "keep_or_surrender": _keep_or_surrender,
    "compare_own": _compare_own,
    "compare_market": _compare_market,
    "estimate_saving": _estimate_saving,
}


# --------------------------------------------------------------------------------- queries


def names_for(conn: Any, person_ids: Iterable[int]) -> list[str]:
    """Each person's display name and confirmed aliases, trimmed and lower-cased the way
    `FACTS_FOR` compares a fact's printed subject."""
    with conn.cursor() as cur:
        cur.execute(queries.NAMES_FOR, {"ids": sorted(person_ids)})
        rows = cur.fetchall()
    names: set[str] = set()
    for _person_id, display_name, alias in rows:
        for name in (display_name, alias):
            if name and name.strip(" "):
                names.add(name.strip(" ").lower())
    return sorted(names)


def facts_for(
    conn: Any,
    pack_id: str,
    doc_types: Sequence[str],
    field: str,
    names: Sequence[str],
    types: Mapping[tuple[str, str], str],
) -> list[FactRow]:
    with conn.cursor() as cur:
        cur.execute(
            queries.FACTS_FOR,
            {"pack": pack_id, "doc_types": list(doc_types), "field": field, "names": list(names)},
        )
        rows = cur.fetchall()
    return [fact_row(row, types) for row in rows]


def product_names(conn: Any, document_ids: Sequence[Any], match_field: str) -> dict[Any, str]:
    with conn.cursor() as cur:
        cur.execute(
            queries.PRODUCT_NAMES_FOR, {"ids": list(document_ids), "match_field": match_field}
        )
        rows = cur.fetchall()
    names: dict[Any, str] = {}
    for document_id, value_text in rows:
        if value_text and document_id not in names:
            names[document_id] = str(value_text)
    return names


def values_for(conn: Any, installed: InstalledPack, key: str, today: date) -> list[ValueRow]:
    """A key's usable published values. How old a value may be depends on what it is: a price
    (a money key qualified by product) goes stale by `max_price_age_days`, anything else by
    `max_rule_age_days`."""
    advice = installed.manifest.advice
    rule_days: int = Advice.model_fields["max_rule_age_days"].default
    price_days: int = Advice.model_fields["max_price_age_days"].default
    if advice is not None:
        rule_days, price_days = advice.max_rule_age_days, advice.max_price_age_days
    declared = next((v for v in installed.manifest.grounding.values if v.key == key), None)
    is_price = (
        declared is not None and declared.unit == "money" and "product" in declared.qualifiers
    )
    oldest = today - timedelta(days=price_days if is_price else rule_days)
    with conn.cursor() as cur:
        cur.execute(
            queries.VALUES_FOR,
            {"pack": installed.id, "key": key, "today": today, "oldest": oldest},
        )
        rows = cur.fetchall()
    return [value_row(row) for row in rows]


# ------------------------------------------------------------------------------ the adviser


class ModuleAdviser:
    """The `core.graph.advice.Adviser` port over Postgres.

    `packs` is where a fact read from another pack finds its field types; it defaults to the
    installed packs. It is a parameter so a test can hand in a fixture pack.
    """

    def __init__(self, conn: Any, packs: Sequence[InstalledPack] | None = None) -> None:
        self._conn = conn
        self._packs = packs

    def calculate(
        self,
        installed: InstalledPack,
        shape: AdviceShape,
        *,
        person_ids: frozenset[int],
        subject: str,
        today: date,
    ) -> Calculation | Missing:
        """One person's advice. The graph asks whose first when a question names several people
        or nobody, so more or fewer than one here is a caller's mistake, not a household to sum:
        one person's guideline set against two people's cover is no figure anyone could check."""
        if len(person_ids) != 1:
            raise ValueError(f"advice is calculated for exactly one person, not {len(person_ids)}")
        names = names_for(self._conn, person_ids)
        facts = {fact.role: self._facts(installed, fact, names) for fact in shape.facts}
        rules = {
            rule.role: values_for(self._conn, installed, rule.key, today) for rule in shape.rules
        }
        declared = {
            value.key: tuple(value.qualifiers) for value in installed.manifest.grounding.values
        }
        basis = usable(
            Basis(
                installed.id,
                shape,
                subject,
                tuple(sorted(person_ids)),
                facts,
                rules,
                {},
                {},
                declared,
            )
        )
        if (missing := withheld(basis)) is not None:
            return missing  # nothing further is read for a shape that cannot be answered
        if shape.calculator in COMPARING:
            basis = replace(
                basis,
                compared=self._compared(installed, shape, names),
                market=self._market(installed, shape, today),
            )
        return calculate(basis)

    def _types(self, installed: InstalledPack, pack_id: str) -> dict[tuple[str, str], str]:
        source: InstalledPack | None = installed
        if pack_id != installed.id:
            packs = self._packs if self._packs is not None else installed_packs()
            source = next((candidate for candidate in packs if candidate.id == pack_id), None)
        if source is None:
            return {}
        return {key: spec.type for key, spec in source.manifest.field_index().items()}

    def _facts(
        self, installed: InstalledPack, fact: FactInput, names: Sequence[str]
    ) -> list[FactRow]:
        pack_id = fact.pack or installed.id
        types = self._types(installed, pack_id)
        rows = facts_for(self._conn, pack_id, fact.doc_types, fact.field, names, types)
        if fact.category is None or not rows:
            return rows
        categories = installed.manifest.answering.categories
        if categories is None:
            return []
        document_ids = list(dict.fromkeys(row.document_id for row in rows))
        printed_names = product_names(self._conn, document_ids, categories.match_field)
        return in_category(rows, printed_names, fact.category, categories)

    def _compared(
        self, installed: InstalledPack, shape: AdviceShape, names: Sequence[str]
    ) -> dict[str, list[FactRow]]:
        fact = _fact(shape, "items" if shape.calculator == "compare_own" else "held")
        pack_id = fact.pack or installed.id
        types = self._types(installed, pack_id)
        return {
            field: facts_for(self._conn, pack_id, fact.doc_types, field, names, types)
            for field in shape.compare_fields
        }

    def _market(
        self, installed: InstalledPack, shape: AdviceShape, today: date
    ) -> dict[str, list[ValueRow]]:
        if shape.calculator != "compare_market":
            return {}
        keys = {value.key for value in installed.manifest.grounding.values}
        return {
            field: values_for(self._conn, installed, field, today)
            for field in shape.compare_fields
            if field in keys
        }


def _is_an_adviser(conn: Any) -> Adviser:
    """Never called. It is here so `mypy` proves `ModuleAdviser` satisfies the port `core/`
    calls; a signature drifting on either side fails the type check, not a request."""
    return ModuleAdviser(conn)
