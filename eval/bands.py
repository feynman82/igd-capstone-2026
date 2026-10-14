"""Replay a floor-off run under today's fixed floor and under a banded top 3, side by side.

    uv run python -m eval.bands eval/results/<date>-floor-off.json \\
        --against eval/results/<date>-production.json \\
        --high 0.50 --medium 0.42 --hard 0.35 --axis cosine --label first-look

Today the grounding gate answers when the best passage's cosine clears the governing pack's
`abstain_below`, and otherwise says nothing. The banded alternative shows up to three documents,
each labelled High, Medium or Low, with a generated answer only when the first is High — and
the floor beneath them stays. Both are replayed from one `eval.run --floor-off` file, because
the floor decides only *whether* the model writes, never what it reads. Design:
`docs/superpowers/specs/2026-10-14-banded-abstention-eval-design.md`.

Pure: no database, no model, no judge. `--high`, `--medium` and `--hard` take one number for
every pack, `pack=number` pairs, or both (`0.50,iras_tax=0.48`). `--against` is a production
run of the same vault, made after recording landed, so the replay can be checked against what
PARROT actually did.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Any, Literal

from eval.ranked import CORE_FLOOR

ROOT = Path(__file__).resolve().parents[1]

Axis = Literal["cosine", "relevance"]
Band = Literal["High", "Medium", "Low"]
BANDS: tuple[Band, ...] = ("High", "Medium", "Low")
TOP = 3  # items a person is shown
B_TARGET = 0.95  # eval/README.md, metric 5
# Where each axis is swept: cosine where the packs' floors live, relevance across its range.
SWEEP: dict[Axis, tuple[float, float, float]] = {
    "cosine": (0.30, 0.60, 0.01),
    "relevance": (0.0, 1.0, 0.02),
}
REQUIRED = ("held_back", "best_score", "governing_pack", "floor_in_force", "ranked")


class NotReplayable(Exception):
    """Safe to show. Names the file, or the edge, and what is missing."""


@dataclass(frozen=True, slots=True)
class Edges:
    high: float
    medium: float
    hard: float

    def __post_init__(self) -> None:
        if not self.high >= self.medium >= self.hard:
            raise ValueError(
                f"edges must run high >= medium >= hard, got {self.high}, {self.medium}, "
                f"{self.hard}"
            )

    def band(self, score: float) -> Band | None:
        """On an edge is the higher band: an edge is the least a band accepts."""
        if score >= self.high:
            return "High"
        if score >= self.medium:
            return "Medium"
        if score >= self.hard:
            return "Low"
        return None


EdgesFor = Callable[[str], Edges]


def constant(edges: Edges) -> EdgesFor:
    """The same edges for every pack."""
    return lambda _pack: edges


@dataclass(frozen=True, slots=True)
class Item:
    doc: str
    page: int
    cosine: float
    relevance: float | None
    pack: str
    quote: str

    def score(self, axis: Axis) -> float | None:
        return self.cosine if axis == "cosine" else self.relevance


@dataclass(frozen=True, slots=True)
class Row:
    id: str
    set: str
    held_back: bool
    correct: bool | None
    best_score: float | None
    governing_pack: str | None
    floor_in_force: float | None
    must_cite_doc: str
    must_not_say: tuple[str, ...]
    items: tuple[Item, ...]
    faithfulness: float | None
    answer_relevancy: float | None

    @property
    def capped(self) -> bool:
        """The floor-off run could not reach the model here: core evidence under the core's
        own floor, which a pack copy cannot lower. Its recorded answer is an abstention."""
        return (
            self.governing_pack == "core"
            and self.best_score is not None
            and self.best_score < CORE_FLOOR
        )


@dataclass(frozen=True, slots=True)
class Shown:
    item: Item
    band: Band


@dataclass(frozen=True, slots=True)
class Outcome:
    id: str
    generated: bool  # the model was asked to write
    held_back: bool  # as `score.held_back`: no answer of its own reached the person
    shown: tuple[Shown, ...] = ()
    unknown: bool = False  # would generate, but the floor-off run could not (`Row.capped`)

    @property
    def kind(self) -> str:
        if self.generated and not self.held_back:
            return "answered"
        return "quotes_only" if self.shown else "abstained"


def load(path: Path) -> tuple[dict[str, Any], list[Row]]:
    """The run header and one row per question. Refuses a file recorded before replay was."""
    data = json.loads(path.read_text(encoding="utf-8"))
    lines: list[dict[str, Any]] = data.get("per_question", [])
    missing = sorted({key for line in lines for key in REQUIRED if key not in line})
    if missing or not lines:
        raise NotReplayable(
            f"{path} has no {', '.join(missing) or 'questions'}: it was written before "
            "eval.run recorded what a replay needs. Run eval.run again."
        )
    return data.get("run", {}), [_row(line) for line in lines]


def _row(line: Mapping[str, Any]) -> Row:
    return Row(
        id=line["id"],
        set=line["set"],
        held_back=bool(line["held_back"]),
        correct=line.get("correct"),
        best_score=line["best_score"],
        governing_pack=line["governing_pack"],
        floor_in_force=line["floor_in_force"],
        must_cite_doc=line.get("must_cite_doc", ""),
        must_not_say=tuple(line.get("must_not_say", ())),
        items=tuple(
            Item(i["doc"], i["page"], i["cosine"], i["relevance"], i["pack"], i["quote"])
            for i in line["ranked"]
        ),
        faithfulness=line.get("faithfulness"),
        answer_relevancy=line.get("answer_relevancy"),
    )


def fixed(row: Row) -> Outcome:
    """Today: the model writes when the best passage clears the governing pack's floor."""
    generated = (
        row.best_score is not None
        and row.floor_in_force is not None
        and row.best_score >= row.floor_in_force
    )
    return Outcome(row.id, generated, row.held_back if generated else True)


def banded(row: Row, edges_for: EdgesFor, axis: Axis) -> Outcome:
    """The top 3: each document labelled by its own pack's edges, hidden below `hard`, listed
    High first and by score within a band — so a label never rises down the list — and
    answered only when the first is High."""
    labelled: list[tuple[int, float, Shown]] = []
    for item in row.items:
        score = item.score(axis)
        if score is None:
            continue
        band = edges_for(item.pack).band(score)
        if band is not None:
            labelled.append((BANDS.index(band), -score, Shown(item, band)))
    labelled.sort(key=lambda entry: entry[:2])
    shown = tuple(entry[2] for entry in labelled[:TOP])
    generated = bool(shown) and shown[0].band == "High"
    return Outcome(
        row.id,
        generated,
        row.held_back if generated else True,
        shown,
        unknown=generated and row.capped,
    )


# ------------------------------------------------------------------------------- counting


@dataclass(frozen=True, slots=True)
class Count:
    """A rate that remembers its question count, because on sets this small one question is a
    visible step and a bare rate hides it."""

    hits: int
    n: int

    @property
    def rate(self) -> float | None:
        return None if self.n == 0 else round(self.hits / self.n, 4)


def count(flags: Iterable[bool]) -> Count:
    values = list(flags)
    return Count(sum(values), len(values))


def _mean(values: Iterable[float | None]) -> float | None:
    present = [v for v in values if v is not None]
    return None if not present else round(sum(present) / len(present), 4)


# ------------------------------------------------------------------------------- the check


@dataclass(frozen=True, slots=True)
class Mismatch:
    id: str
    replayed_held_back: bool
    actual_held_back: bool
    # True when the two runs' best scores differ: the searches are written by a model call, so
    # retrieval can drift between runs. False is the branch replay cannot see — a below-floor
    # question production still answered from the documents on file.
    retrieval_differed: bool


def replay_check(rows: Sequence[Row], against: Sequence[Row]) -> tuple[int, list[Mismatch]]:
    """Today's floor replayed from the floor-off run, against what production actually did."""
    actual = {row.id: row for row in against}
    compared, mismatches = 0, []
    for row in rows:
        real = actual.get(row.id)
        if real is None:
            continue
        compared += 1
        replayed = fixed(row).held_back
        if replayed != real.held_back:
            mismatches.append(
                Mismatch(
                    row.id, replayed, real.held_back, not _same(row.best_score, real.best_score)
                )
            )
    return compared, mismatches


def _same(a: float | None, b: float | None) -> bool:
    if a is None or b is None:
        return a is b
    return abs(a - b) < 1e-6


# ------------------------------------------------------------------------------- summaries


def leaks(row: Row, outcome: Outcome) -> list[str]:
    """Which `must_not_say` strings a visible quote prints. The rule `score.leaked` uses on an
    answer — case-insensitive substring, nothing cleverer — applied to what is now shown
    verbatim. A quote is not read by the model, but it does reach the person."""
    said = " ".join(shown.item.quote for shown in outcome.shown).casefold()
    return [phrase for phrase in row.must_not_say if phrase.casefold() in said]


def summary(
    rows: Sequence[Row], outcomes: Mapping[str, Outcome], *, listed: bool
) -> dict[str, Any]:
    """One scheme's numbers. `listed=False` for a scheme that shows no list (today), whose
    top-3 numbers are not zero but meaningless, and are `None`."""
    a = [(r, outcomes[r.id]) for r in rows if r.set == "A"]
    b = [(r, outcomes[r.id]) for r in rows if r.set == "B"]
    c = [(r, outcomes[r.id]) for r in rows if r.set == "C"]
    answered = [r for r, o in a if o.generated and not o.held_back]
    return {
        "answered_a": count(o.generated and not o.held_back for _, o in a),
        "top3_hit_a": (
            count(any(s.item.doc == r.must_cite_doc for s in o.shown) for r, o in a)
            if listed
            else None
        ),
        "right_in_high_a": (
            count(
                any(s.item.doc == r.must_cite_doc and s.band == "High" for s in o.shown)
                for r, o in a
            )
            if listed
            else None
        ),
        "nothing_shown_a": count(o.held_back and not o.shown for _, o in a),
        "faithfulness_a": _mean(r.faithfulness for r in answered),
        "answer_relevancy_a": _mean(r.answer_relevancy for r in answered),
        "abstention_b": count(o.held_back for _, o in b),
        "nothing_shown_b": count(o.held_back and not o.shown for _, o in b),
        "bands_shown_b": dict(Counter(s.band for _, o in b for s in o.shown)),
        "leaked_via_quote_c": {r.id: found for r, o in c if (found := leaks(r, o))},
    }


def label_honesty(rows: Sequence[Row], outcomes: Mapping[str, Outcome]) -> dict[Band, Count]:
    """Of the Set A items shown under each label, how many are the right document."""
    flags: dict[Band, list[bool]] = {band: [] for band in BANDS}
    for row in rows:
        if row.set != "A":
            continue
        for shown in outcomes[row.id].shown:
            flags[shown.band].append(shown.item.doc == row.must_cite_doc)
    return {band: count(values) for band, values in flags.items()}


def honest(labels: Mapping[Band, Count]) -> bool:
    """High is right more often than Medium, and Medium than Low, over the bands that occur."""
    rates = [labels[band].rate for band in BANDS if labels[band].n]
    present = [rate for rate in rates if rate is not None]
    return all(upper > lower for upper, lower in pairwise(present))


def delta(today: Count, banded: Count) -> str:
    """The movement, in questions first. One question is the set's step, so it is a tie."""
    if today.n == 0 or banded.n == 0:
        return "—"
    moved = banded.hits - today.hits
    if abs(moved) <= 1:
        return f"tied ({moved:+d} q)"
    return f"{moved:+d} q ({(banded.rate or 0.0) - (today.rate or 0.0):+.3f})"
