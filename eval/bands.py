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

import argparse
import json
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, is_dataclass
from datetime import date
from itertools import pairwise
from pathlib import Path
from typing import Any, Literal

from eval.ranked import CORE_FLOOR
from eval.report import PLACEHOLDER, _paragraph

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


# ------------------------------------------------------------------------------- the sweep


@dataclass(frozen=True, slots=True)
class Point:
    """One edge, used as all three at once. Whether the model writes depends only on the High
    edge and what is visible only on the hard edge, so one sweep answers both questions."""

    edge: float
    answered_a: Count
    abstention_b: Count
    top3_hit_a: Count
    nothing_shown_a: Count
    nothing_shown_b: Count


def sweep(rows: Sequence[Row], axis: Axis) -> list[Point]:
    start, stop, step = SWEEP[axis]
    points: list[Point] = []
    for i in range(round((stop - start) / step) + 1):
        edge = round(start + i * step, 4)
        edges_for = constant(Edges(edge, edge, edge))
        outcomes = {row.id: banded(row, edges_for, axis) for row in rows}
        s = summary(rows, outcomes, listed=True)
        points.append(
            Point(
                edge,
                s["answered_a"],
                s["abstention_b"],
                s["top3_hit_a"],
                s["nothing_shown_a"],
                s["nothing_shown_b"],
            )
        )
    return points


def reference_points(
    points: Sequence[Point], today_answered: Count
) -> tuple[float | None, float | None]:
    """The highest edge that keeps today's Set A answered count, and the lowest that meets Set
    B's target. Marked for a person to read; neither is chosen here."""
    keeps = [p.edge for p in points if p.answered_a.n and p.answered_a.hits >= today_answered.hits]
    meets = [p.edge for p in points if (p.abstention_b.rate or 0.0) >= B_TARGET]
    return (max(keeps) if keeps else None, min(meets) if meets else None)


def by_pack(rows: Sequence[Row]) -> dict[str, list[Row]]:
    """Rows by the pack whose floor governs them; `none` for a question nothing was read for."""
    groups: dict[str, list[Row]] = {}
    for row in rows:
        groups.setdefault(row.governing_pack or "none", []).append(row)
    return groups


def axis_summary(rows: Sequence[Row], today_answered: Count) -> dict[str, dict[str, Any] | None]:
    """Cosine against relevance, at the same two reference points. `None` for an axis the run
    did not record — relevance needs the cross-encoder."""
    result: dict[str, dict[str, Any] | None] = {}
    axes: tuple[Axis, ...] = ("cosine", "relevance")
    for axis in axes:
        if not any(item.score(axis) is not None for row in rows for item in row.items):
            result[axis] = None
            continue
        points = sweep(rows, axis)
        keeps, meets = reference_points(points, today_answered)
        at = {p.edge: p for p in points}
        result[axis] = {
            "keeps_today": keeps,
            "abstention_b_there": at[keeps].abstention_b if keeps is not None else None,
            "meets_b": meets,
            "answered_a_there": at[meets].answered_a if meets is not None else None,
        }
    return result


# ------------------------------------------------------------------------------- edges


def parse_edge(text: str) -> dict[str, float]:
    """`0.50` for every pack, `insurance_agent=0.52,iras_tax=0.48` per pack, or both."""
    edges: dict[str, float] = {}
    for part in (p.strip() for p in text.split(",")):
        if part:
            name, _, value = part.rpartition("=")
            edges[name or "*"] = float(value)
    return edges


def edges_for_packs(
    high: Mapping[str, float], medium: Mapping[str, float], hard: Mapping[str, float]
) -> EdgesFor:
    def pick(edge: Mapping[str, float], pack: str) -> float:
        if pack in edge:
            return edge[pack]
        if "*" in edge:
            return edge["*"]
        raise NotReplayable(
            f"no edge for pack {pack!r}: name it, or give a bare number for every pack"
        )

    def of(pack: str) -> Edges:
        return Edges(pick(high, pack), pick(medium, pack), pick(hard, pack))

    return of


# ------------------------------------------------------------------------------- the report


@dataclass
class Report:
    axis: Axis
    compared: int
    replayed: int
    mismatches: list[Mismatch]
    today: dict[str, dict[str, Any]]  # "all" and each governing pack
    banded: dict[str, dict[str, Any]]
    labels: dict[Band, Count]
    sweeps: dict[str, list[Point]]  # per governing pack, on the chosen axis
    references: dict[str, tuple[float | None, float | None]]
    axes: dict[str, dict[str, Any] | None]
    unknown: list[str]
    capped: list[str]

    @property
    def trustworthy(self) -> bool:
        return self.compared > 0 and len(self.mismatches) <= 1  # one question is the step

    @property
    def honest(self) -> bool:
        return honest(self.labels)


def compute(rows: Sequence[Row], against: Sequence[Row], edges_for: EdgesFor, axis: Axis) -> Report:
    compared, mismatches = replay_check(rows, against)
    today_out = {row.id: fixed(row) for row in rows}
    banded_out = {row.id: banded(row, edges_for, axis) for row in rows}
    packs = by_pack(rows)
    groups = {"all": list(rows), **packs}
    today = {name: summary(g, today_out, listed=False) for name, g in groups.items()}
    band = {name: summary(g, banded_out, listed=True) for name, g in groups.items()}
    sweeps = {name: sweep(g, axis) for name, g in packs.items()}
    references = {
        name: reference_points(points, today[name]["answered_a"]) for name, points in sweeps.items()
    }
    return Report(
        axis=axis,
        compared=compared,
        replayed=len(rows),
        mismatches=mismatches,
        today=today,
        banded=band,
        labels=label_honesty(rows, banded_out),
        sweeps=sweeps,
        references=references,
        axes=axis_summary(rows, today["all"]["answered_a"]),
        unknown=sorted(o.id for o in banded_out.values() if o.unknown),
        capped=sorted(row.id for row in rows if row.capped),
    )


def _cell(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, Count):
        return "—" if value.rate is None else f"{value.rate:.3f} ({value.hits}/{value.n})"
    return f"{value:.3f}" if isinstance(value, float) else str(value)


SIDE_BY_SIDE = (
    ("Set A answered", "answered_a"),
    ("Set A top-3 hit", "top3_hit_a"),
    ("Set A right document in High", "right_in_high_a"),
    ("Set A nothing shown", "nothing_shown_a"),
    ("Set A faithfulness (answered)", "faithfulness_a"),
    ("Set A answer relevancy (answered)", "answer_relevancy_a"),
    ("Set B generated-answer abstention", "abstention_b"),
    ("Set B nothing shown", "nothing_shown_b"),
    ("Set B bands shown", "bands_shown_b"),
)


def _move(today: Any, banded_value: Any) -> str:
    if isinstance(today, Count) and isinstance(banded_value, Count):
        return delta(today, banded_value)
    if isinstance(today, float) and isinstance(banded_value, float):
        return f"{banded_value - today:+.3f} (judge noise is about 0.05)"
    return ""


def render(
    report: Report, run: Mapping[str, Any], inputs: Mapping[str, Any], paragraph: str
) -> str:
    out = [f"# bands-{inputs['label']} — {date.today().isoformat()}", ""]
    out += [
        f"Replayed from `{inputs['source']}`, checked against `{inputs['against']}`. Generator "
        f"`{run.get('generator')}`; judge `{run.get('judge') or 'none'}`; corpus "
        f"`{run.get('corpus_manifest_sha')}`; git `{run.get('git_sha')}`. Axis **{report.axis}**; "
        f"edges high `{inputs['high']}`, medium `{inputs['medium']}`, hard `{inputs['hard']}`.",
        "",
    ]
    if not report.honest:
        out += [
            "> **The labels are not honest on this run**: a higher band is not right more often "
            "than the one below it. A person would be misled by them. See *Are the labels honest?*",
            "",
        ]
    if not report.trustworthy:
        out += [
            f"> **The replay does not reproduce production**: {report.compared} of "
            f"{report.replayed} questions compared, {len(report.mismatches)} differ. Read "
            "nothing below until *Replay check* is explained.",
            "",
        ]

    out += [
        "## Replay check",
        "",
        f"Today's fixed floor, replayed from the floor-off run: {report.compared} questions "
        f"compared with production, {len(report.mismatches)} differ.",
        "",
    ]
    if report.compared < report.replayed:
        out += [
            f"{report.replayed - report.compared} of the {report.replayed} floor-off questions had "
            "no production counterpart, so nothing was checked for them.",
            "",
        ]
    for m in report.mismatches:
        said = "held back" if m.actual_held_back else "answered"
        why = (
            "retrieval differed between the runs (the searches are a model call)"
            if m.retrieval_differed
            else "same evidence: the documents-on-file branch replay cannot see"
        )
        out.append(f"- `{m.id}`: production {said}, replay did not — {why}")
    out.append("")

    out += ["## Set C: leaked via quote", ""]
    leaked = report.banded["all"]["leaked_via_quote_c"]
    out += [f"- `{qid}`: {', '.join(repr(s) for s in found)}" for qid, found in leaked.items()]
    out += ["None." if not leaked else "", "These are Siew's to judge.", ""]

    out += [
        "## Are the labels honest?",
        "",
        "| Band | Right document | ",
        "|---|---|",
        *(f"| {band} | {_cell(report.labels[band])} |" for band in BANDS),
        "",
        "Honest." if report.honest else "**Not honest.**",
        "",
    ]

    out += ["## Today against banded", ""]
    for name, today in report.today.items():
        out += [
            f"### {name}",
            "",
            "| | Today (fixed floor) | Banded top 3 | Δ |",
            "|---|---|---|---|",
        ]
        for label, key in SIDE_BY_SIDE:
            t, b = today[key], report.banded[name][key]
            out.append(f"| {label} | {_cell(t)} | {_cell(b)} | {_move(t, b)} |")
        out.append("")

    out += ["## The sweep", ""]
    for name, points in report.sweeps.items():
        keeps, meets = report.references[name]
        out += [
            f"### {name} ({report.axis})",
            "",
            f"Keeps today's Set A answered count up to **{_cell(keeps)}**; meets Set B's "
            f"{B_TARGET} from **{_cell(meets)}**. Neither is chosen here.",
            "",
            "| Edge | A answered | B abstention | A top-3 hit | A nothing shown "
            "| B nothing shown |",
            "|---|---|---|---|---|---|",
        ]
        for i, p in enumerate(points):
            marked = p.edge in (keeps, meets)
            if i % 2 and not marked:
                continue
            edge = f"**{p.edge:.2f}**" if marked else f"{p.edge:.2f}"
            out.append(
                f"| {edge} | {_cell(p.answered_a)} | {_cell(p.abstention_b)} | "
                f"{_cell(p.top3_hit_a)} | {_cell(p.nothing_shown_a)} | {_cell(p.nothing_shown_b)} |"
            )
        out.append("")

    out += [
        "## Cosine against relevance",
        "",
        "| Axis | Keeps today's A at | B abstention there | Meets B's target at "
        "| A answered there |",
        "|---|---|---|---|---|",
    ]
    for axis, found in report.axes.items():
        if found is None:
            out.append(f"| {axis} | not recorded | | | |")
            continue
        out.append(
            f"| {axis} | {_cell(found['keeps_today'])} | {_cell(found['abstention_b_there'])} | "
            f"{_cell(found['meets_b'])} | {_cell(found['answered_a_there'])} |"
        )
    out.append("")

    if report.capped:
        out += [
            "## Held back by the core floor",
            "",
            f"{len(report.capped)} questions had core evidence under 0.42, which a floor-off run "
            "cannot lower: "
            + ", ".join(f"`{q}`" for q in report.capped)
            + ". "
            + (
                f"{len(report.unknown)} of them would be answered under these edges and are "
                "counted as held back — a pessimistic reading."
                if report.unknown
                else "None of them would be answered under these edges."
            ),
            "",
        ]

    out += ["## How to read it", "", paragraph or PLACEHOLDER, ""]
    return "\n".join(out)


def _plain(value: Any) -> Any:
    if isinstance(value, Count):
        return {"hits": value.hits, "n": value.n, "rate": value.rate}
    if is_dataclass(value) and not isinstance(value, type):
        return {k: _plain(v) for k, v in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_plain(v) for v in value]
    return value


def as_json(report: Report) -> dict[str, Any]:
    return {
        "axis": report.axis,
        "replay_check": {
            "compared": report.compared,
            "replayed": report.replayed,
            "trustworthy": report.trustworthy,
            "mismatches": [_plain(m) for m in report.mismatches],
        },
        "today": _plain(report.today),
        "banded": _plain(report.banded),
        "labels": _plain(report.labels),
        "honest": report.honest,
        "sweeps": {
            name: [
                {"edge": p.edge, **{k: _plain(v) for k, v in vars_of(p).items()}} for p in points
            ]
            for name, points in report.sweeps.items()
        },
        "references": {
            name: {"keeps_today": keeps, "meets_b": meets}
            for name, (keeps, meets) in report.references.items()
        },
        "axes": _plain(report.axes),
        "unknown": report.unknown,
        "capped": report.capped,
    }


def vars_of(point: Point) -> dict[str, Count]:
    return {
        "answered_a": point.answered_a,
        "abstention_b": point.abstention_b,
        "top3_hit_a": point.top3_hit_a,
        "nothing_shown_a": point.nothing_shown_a,
        "nothing_shown_b": point.nothing_shown_b,
    }


# ------------------------------------------------------------------------------- the CLI


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("source", type=Path, help="a run made with `eval.run --floor-off`")
    parser.add_argument(
        "--against", type=Path, required=True, help="a production run of the same vault"
    )
    parser.add_argument("--high", required=True)
    parser.add_argument("--medium", required=True)
    parser.add_argument("--hard", required=True)
    parser.add_argument("--axis", choices=["cosine", "relevance"], default="cosine")
    parser.add_argument("--label", required=True, help="what these edges are; part of the name")
    parser.add_argument("--out", type=Path, default=ROOT / "eval" / "results")
    args = parser.parse_args(argv)
    axis: Axis = args.axis

    try:
        run, rows = load(args.source)
        against_run, against = load(args.against)
        if run.get("floor") != "off":
            raise NotReplayable(
                f"{args.source} was not run with --floor-off: below the floor it holds no "
                "answers to replay"
            )
        if against_run.get("floor") == "off":
            raise NotReplayable(f"{args.against} is a floor-off run; the check needs production")
        if run.get("corpus_manifest_sha") != against_run.get("corpus_manifest_sha"):
            raise NotReplayable("the two runs read different corpora, so they do not compare")
        edges_for = edges_for_packs(
            parse_edge(args.high), parse_edge(args.medium), parse_edge(args.hard)
        )
        for pack in sorted({item.pack for row in rows for item in row.items}):
            edges_for(pack)
        if not any(item.score(axis) is not None for row in rows for item in row.items):
            raise NotReplayable(f"no {axis} score was recorded in {args.source}")
    except (NotReplayable, ValueError) as error:
        print(error)
        return 2

    inputs = {
        "source": str(args.source),
        "against": str(args.against),
        "high": args.high,
        "medium": args.medium,
        "hard": args.hard,
        "axis": axis,
        "label": args.label,
    }
    stem = args.out / f"{date.today().isoformat()}-bands-{args.label}"
    target, note = Path(f"{stem}.json"), Path(f"{stem}.md")
    if target.exists() and json.loads(target.read_text(encoding="utf-8")).get("inputs") != inputs:
        print(
            f"{target} was written from different inputs and results are append-only. "
            "Choose another --label."
        )
        return 2

    report = compute(rows, against, edges_for, axis)
    args.out.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps({"inputs": inputs, **as_json(report)}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    note.write_text(render(report, run, inputs, _paragraph(note)), encoding="utf-8")
    print(f"wrote {note}")
    if not report.trustworthy:
        print(f"replay differs from production on {len(report.mismatches)} questions — read it")
    if not report.honest:
        print("the labels are not honest on this run — read it")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
