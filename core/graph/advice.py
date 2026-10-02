"""What a calculator returns, and what the graph needs to ask consent and keep a record of it.

ADR 0016: a pack declares advice shapes, a hand-written calculator computes, and the model only
explains. This file is the seam between the two — `Adviser` is implemented by `modules/advice/`,
never imported from here, so `core/` stays ignorant of any calculator's arithmetic and any pack's
domain words, exactly as `core/graph/ports.py` keeps `core/` ignorant of how retrieval works.

`ConsentBook` and `AdviceLog` are the same idea applied to Postgres: the graph asks "may I" and
says "here is what happened" through a protocol, and `core/advice_consent.py` and
`core/advice_records.py` are the only two files that know the tables' names.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Literal, Protocol

from core.contracts import AdviceShape
from core.graph.ports import Kind, Passage
from core.packs import InstalledPack


@dataclass(frozen=True, slots=True)
class Input:
    """One fact or rule value a calculation was built on, carrying its own citation.

    `ref` is `"fact:12"` or `"rule:7"` — the id a calculator read it by, in the same `kind:id`
    shape `Passage.ref` uses, so `passages_for` can turn it back into a passage the gate already
    knows how to check. A rule's citation has no page to open (`document_id` and `page` stay
    `None`); it has a publisher, a title, a date and a URL instead.
    """

    ref: str
    role: str
    label: str  # "annual income", from the fact's field or the value's key, readable
    value_text: str  # as printed: "SGD 9,400.00", "4 times"
    citation: str  # "statement.pdf, page 1" or "Publisher, Guide title, 26 September 2023"
    document_id: Any = None
    page: int | None = None
    publisher: str = ""
    title: str = ""
    dated: str = ""
    url: str = ""


@dataclass(frozen=True, slots=True)
class Figure:
    """One number a calculator produced, and the words a sentence must use to state it.

    `words` is read by the same role-word check ADR 0016 describes for the explanation: a
    sentence may print `value` only alongside one of these, so "the gap is SGD 188,000.00" is
    allowed and a stray SGD 188,000.00 attached to nothing is not.
    """

    name: str  # "target", "held", "gap", "room", "loss", "saving"
    value: Decimal
    text: str  # "SGD 188,000.00"
    words: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Calculation:
    """What a calculator returns when every fact and rule it needed was on file and approved."""

    pack_id: str
    shape_id: str
    label: str
    subject: str
    person_ids: tuple[int, ...]
    inputs: tuple[Input, ...]
    figures: tuple[Figure, ...]
    verdict: str  # a code from the calculator: short, meets, room_left, no_room, loses, gains, ...
    verdict_text: str  # the code-written sentence
    rows: tuple[tuple[str, ...], ...] = ()  # comparison table, header row first
    names_product: bool = False
    estimate: bool = False


@dataclass(frozen=True, slots=True)
class Missing:
    """What a calculator returns when a fact or a rule value it needed was not there to read.

    The honest answer to a missing fact is to name it, not to estimate around it (ADR 0016), so
    `items` is the pack's own wording for each one, in the order the shape declared them.
    """

    pack_id: str
    shape_id: str
    label: str
    subject: str
    items: tuple[str, ...]  # the pack's own `missing` wording, in declared order


class Adviser(Protocol):
    """Implemented by `modules/advice/`. `core/` calls this; it never computes a figure itself."""

    def calculate(
        self,
        installed: InstalledPack,
        shape: AdviceShape,
        *,
        person_ids: frozenset[int],
        subject: str,
        today: date,
    ) -> Calculation | Missing: ...


class ConsentBook(Protocol):
    """Implemented by `HouseholdConsents` in `core/advice_consent.py`."""

    def current(self, pack_id: str, version: str) -> int | None:
        """The granting row's id, or `None` when the owner has not granted this exact version."""
        ...


class AdviceLog(Protocol):
    """Implemented by `HouseholdAdviceLog` in `core/advice_records.py`."""

    def record(self, entry: AdviceRecord) -> None: ...


@dataclass(frozen=True, slots=True)
class AdviceRecord:
    """Every advised or withheld answer's full basis, so it can be reconstructed later without
    trusting that today's rule values are still what they were when it was given (ADR 0016)."""

    thread_id: str
    pack_id: str
    pack_version: str
    shape: str
    subject: str
    person_ids: tuple[int, ...]
    consent_id: int
    outcome: Literal["advised", "withheld"]
    verdict: str | None
    basis: dict[str, Any]
    disclaimer: str
    answer_text: str


def kind_of(ref: str) -> Kind:
    """`"fact:12"` -> `"fact"`, `"rule:7"` -> `"rule"`. Anything else is a calculator bug: an
    `Input.ref` is written by `modules/advice/` and this is the one place that trusts its shape,
    so a malformed one fails loudly here rather than mislabelling a passage's kind."""
    kind, _, _ = ref.partition(":")
    if kind == "fact":
        return "fact"
    if kind == "rule":
        return "rule"
    raise ValueError(f"not a fact or rule ref: {ref!r}")


def passages_for(calc: Calculation) -> list[Passage]:
    """Inputs as kind fact/rule passages (chunk_id from the ref), and the figures as one
    calculation passage (chunk_id 0) whose text prints each figure as "name: text".

    This lets a `Calculation` be explained by the same gate an explained answer is: each input
    is a passage the model may cite, and the figures passage is what lets it state the ones the
    calculator itself produced, cited the same way as anything else it is allowed to say. A fact
    or rule passage's `text` prints its own value ("annual income: SGD 9,400.00") so the gate's
    number check (`core.graph.gate.unprinted_numbers`) finds it there; `context_prefix` carries
    the `Input`'s citation string alongside it, for the same check to search but not to print.

    These passages are evidence for the model and the gate only — never for a citation chip.
    `Passage.cite()` on one of them gives the wrong string (`"doc-1, page 1"` for a fact with no
    document name, `"None, page 0"` for a rule with no page at all); a chip's citation must be
    built from the `Input` itself (`citation`, `publisher`, `title`, `dated`, `url`), which is
    the graph task's to do, not this one's. No change to `answer.py` follows from this.
    """
    passages = [
        Passage(
            chunk_id=int(item.ref.partition(":")[2]),
            document_id=item.document_id,
            page=item.page if item.page is not None else 0,
            text=f"{item.label}: {item.value_text}",
            score=1.0,
            document_name=item.title,
            context_prefix=item.citation,
            pack_id=calc.pack_id,
            kind=kind_of(item.ref),
        )
        for item in calc.inputs
    ]
    figures_text = "\n".join(f"{figure.name}: {figure.text}" for figure in calc.figures)
    passages.append(
        Passage(
            chunk_id=0,
            document_id=None,
            page=0,
            text=figures_text,
            score=1.0,
            pack_id=calc.pack_id,
            kind="calculation",
        )
    )
    return passages
