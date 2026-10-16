"""The five headline numbers: one for each aim in the README, scored by code.

    uv run python -m eval.headline eval/results/<run>.json [more runs …]

PARROT says it answers from a household's own documents, shows the page every answer came from,
and says so rather than guessing when the evidence does not cover the question. These five
numbers ask whether it does, from the answer text, the register and the question files — no
judge model, so the numbers the report leads with cannot be argued with:

1. **Right and cited** — Set A: the printed value, its page cited, nothing held back, and no
   sentence saying the thing is not on file.
2. **Unsupported claims** — every set: a wrong value, a false "not on file", a claim on a question
   the vault cannot answer, or a forbidden string. Lower is better.
3. **Over-caution** — Set A held back although the page that prints the answer was read. A
   question whose page was never retrieved is a retrieval miss, reported beside it.
4. **Casual-phrasing gap** — number 1 on questions marked `"phrasing": "casual"` against the rest.
5. **Filed correctly** — extraction F1, read from the run's metrics.

`eval.run` puts them in every result file. This module also scores result files written before
it existed: it writes a companion `<run>-headline.json` and `.md` beside each and never touches
the run file. Older runs do not record `held_back`, so it is rebuilt from the recorded answer —
and the rebuild is used only when it agrees, on every question, with every run given on the same
command line that records it. Design:
`docs/superpowers/specs/2026-10-15-aim-headline-metrics-design.md`.
"""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from eval import score
from eval.bands import Count, count, delta
from eval.sets_io import HELD_BACK, SET_FOLDERS, Question, load_set

ROOT = Path(__file__).resolve().parents[1]

# `Answer.text` joins each gated sentence with its citations in brackets, so a bracket is where
# one recorded sentence ends and the next begins.
CITATION = re.compile(r"\s*\[[^\]]*\]\s*")


class NotScorable(Exception):
    """Safe to show. Names the file and what is wrong with it."""


def claims_in(text: str) -> list[str]:
    """The sentences of a recorded answer, without their citations."""
    return [part.strip() for part in CITATION.split(text) if part.strip()]


def rebuilt_held_back(outcome: str, text: str) -> bool:
    """`score.held_back`, read back from a result line. The flag is the recorded outcome; the
    two readings of what the answer said are made over its recorded sentences."""
    said = claims_in(text)
    return (
        outcome in HELD_BACK
        or outcome == "unanswered"
        or score.said_by_code_only(said)
        or score.declines_in_prose(said)
    )


def disagreements(lines: Sequence[Mapping[str, Any]]) -> list[str]:
    """The questions whose recorded `held_back` the rebuild gets wrong."""
    return [
        line["id"]
        for line in lines
        if "held_back" in line
        and rebuilt_held_back(line["outcome"], line["answer"]) != line["held_back"]
    ]


@dataclass(frozen=True, slots=True)
class Row:
    id: str
    set: str
    kind: str
    phrasing: str
    held_back: bool | None  # None: not recorded, and the rebuild is not trusted
    stated: bool  # the register's value appears in the answer (fact questions)
    cited: bool  # the page that prints it is cited
    shown: bool  # that page was among the passages read
    absent: bool  # some sentence says the thing is not on file
    indexed: bool  # the question's document is in the vault (True when the run cannot say)
    leaked: tuple[str, ...]


def read(
    lines: Sequence[Mapping[str, Any]],
    questions: Mapping[str, Question],
    *,
    rebuild: bool,
    indexed: Collection[str] | None = None,
) -> tuple[list[Row], list[str]]:
    """One row per scored question, and the ids no question file holds any longer. `indexed` is
    the set of documents the run's vault held; None when a result file does not say."""
    rows: list[Row] = []
    gone: list[str] = []
    for line in lines:
        question = questions.get(line["id"])
        if question is None:
            gone.append(line["id"])
            continue
        text = str(line.get("answer") or "")
        if "held_back" in line:
            held: bool | None = bool(line["held_back"])
        elif rebuild:
            held = rebuilt_held_back(str(line.get("outcome") or ""), text)
        else:
            held = None
        kind = question.expected.kind
        stated = kind == "fact" and score.mentions(text, question.expected.value)
        said = claims_in(text)
        # The code's own absence line always says "not on file". A model's "not stated" sentence
        # counts only when the answer held back or never gave the value: a false claim on the
        # headline is worse than a missed one, and an aside ("the premium for next year is not
        # stated") is not a claim that the thing asked about is missing.
        code_absent = any(score.ABSENCE_LINE.match(s) for s in said)
        prose_absent = score.says_absent([s for s in said if not score.ABSENCE_LINE.match(s)])
        absent = code_absent or (prose_absent and (held is True or (kind == "fact" and not stated)))
        rows.append(
            Row(
                id=question.id,
                set=question.set,
                kind=kind,
                phrasing=question.phrasing,
                held_back=held,
                stated=stated,
                cited=bool(line.get("cited")),
                shown=bool(line.get("shown")),
                absent=absent,
                indexed=indexed is None or question.must_cite_doc in indexed,
                leaked=tuple(score.leaked_in(text, question.must_not_say)),
            )
        )
    return rows, gone


@dataclass(frozen=True, slots=True)
class Claim:
    id: str
    reasons: tuple[str, ...]


def reasons(row: Row) -> tuple[str, ...]:
    """Why an answer is an unsupported claim; empty when it is not one."""
    found: list[str] = []
    if row.set == "A" and row.kind == "fact" and row.held_back is False and not row.stated:
        found.append("wrong_value")
    if row.set == "A" and row.absent and row.indexed:
        found.append("false_absence")
    if row.set == "B" and row.held_back is False:
        found.append("claimed")
    if row.set == "C" and row.leaked:
        found.append("forbidden")
    return tuple(found)


def right(row: Row) -> bool:
    """Right and cited: not held back, the page cited, no "not on file", and — for a fact — the
    value stated. A passage question has no single value, so its citation decides."""
    return (
        row.held_back is False
        and row.cited
        and not row.absent
        and (row.kind != "fact" or row.stated)
    )


@dataclass
class Headline:
    held_back_from: str  # "recorded", "reconstructed" or "not measurable"
    right_and_cited: Count | None
    not_right: list[str]
    unsupported_claims: Count | None
    claims: list[Claim]
    over_caution: Count | None
    over_cautious: list[str]
    retrieval_miss: list[str]
    casual: Count | None
    formal: Count | None
    extraction_f1: float | None
    not_in_sets: list[str]

    @property
    def casual_gap(self) -> float | None:
        if self.casual is None or self.formal is None:
            return None
        if self.casual.rate is None or self.formal.rate is None:
            return None
        return round(self.formal.rate - self.casual.rate, 4)


def compute(
    lines: Sequence[Mapping[str, Any]],
    questions: Mapping[str, Question],
    *,
    extraction_f1: float | None,
    rebuild: bool,
    indexed: Collection[str] | None = None,
) -> Headline:
    rows, gone = read(lines, questions, rebuild=rebuild, indexed=indexed)
    a = [row for row in rows if row.set == "A"]
    measurable = all(row.held_back is not None for row in rows)
    recorded = all("held_back" in line for line in lines)
    source = "recorded" if recorded else "reconstructed" if measurable else "not measurable"
    claims = [Claim(row.id, found) for row in rows if (found := reasons(row))]
    held = [row for row in a if row.held_back]
    return Headline(
        held_back_from=source,
        right_and_cited=count(right(row) for row in a) if measurable else None,
        not_right=[row.id for row in a if not right(row)] if measurable else [],
        unsupported_claims=count(bool(reasons(row)) for row in rows) if measurable else None,
        claims=claims,
        over_caution=count(bool(row.held_back and row.shown) for row in a) if measurable else None,
        over_cautious=[row.id for row in held if row.shown],
        retrieval_miss=[row.id for row in held if not row.shown],
        casual=count(right(row) for row in a if row.phrasing == "casual") if measurable else None,
        formal=count(right(row) for row in a if row.phrasing != "casual") if measurable else None,
        extraction_f1=extraction_f1,
        not_in_sets=gone,
    )


def all_questions(root: Path) -> dict[str, Question]:
    return {q.id: q for set_id in SET_FOLDERS for q in load_set(root, set_id)}


# ------------------------------------------------------------------------------- output


def _cell(value: Count | None) -> str:
    if value is None or value.rate is None:
        return "—"
    return f"{value.rate:.3f} ({value.hits}/{value.n})"


ROWS: tuple[tuple[str, str, str], ...] = (
    ("Right and cited (Set A)", "right_and_cited", "higher is better"),
    ("Unsupported claims (all sets)", "unsupported_claims", "lower is better"),
    ("Over-caution (Set A)", "over_caution", "lower is better"),
    ("Right and cited, casual phrasing", "casual", "the gap should close"),
    ("Right and cited, formal phrasing", "formal", ""),
)


def as_json(head: Headline) -> dict[str, Any]:
    def plain(value: Count | None) -> dict[str, Any] | None:
        return None if value is None else {"hits": value.hits, "n": value.n, "rate": value.rate}

    return {
        "held_back_from": head.held_back_from,
        "right_and_cited": plain(head.right_and_cited),
        "not_right": head.not_right,
        "unsupported_claims": plain(head.unsupported_claims),
        "claims": [{"id": c.id, "reasons": list(c.reasons)} for c in head.claims],
        "over_caution": plain(head.over_caution),
        "over_cautious": head.over_cautious,
        "retrieval_miss": head.retrieval_miss,
        "casual": plain(head.casual),
        "formal": plain(head.formal),
        "casual_gap": head.casual_gap,
        "extraction_f1": head.extraction_f1,
        "not_in_sets": head.not_in_sets,
    }


def change(before: Count | None, after: Count | None) -> str:
    """The movement between two runs, in questions. Only counts over the same number of
    questions compare: a set that grew changes the count without anything having moved."""
    if before is None or after is None:
        return ""
    if before.n != after.n:
        return f"questions changed ({before.n} → {after.n})"
    return delta(before, after)


def table(head: Headline, previous: Headline | None = None) -> str:
    """The headline for a terminal, with the change since `previous` when there is one."""
    lines = [f"{'headline':<34} {'value':>16}  direction"]
    for label, key, direction in ROWS:
        value = getattr(head, key)
        moved = f"  {change(getattr(previous, key), value)}" if previous is not None else ""
        lines.append(f"{label:<34} {_cell(value):>16}  {direction}{moved}")
    misses = (
        None
        if head.right_and_cited is None
        else Count(len(head.retrieval_miss), head.right_and_cited.n)
    )
    lines.insert(
        4, f"{'Retrieval misses (Set A)':<34} {_cell(misses):>16}  the page was never retrieved"
    )
    f1 = "—" if head.extraction_f1 is None else f"{head.extraction_f1:.4f}"
    lines.append(f"{'Filed correctly (extraction F1)':<34} {f1:>16}  line 0.90")
    if head.held_back_from != "recorded":
        lines.append(f"(held back: {head.held_back_from})")
    return "\n".join(lines)


def render(name: str, head: Headline) -> str:
    out = [f"# Headline — {name}", "", f"Held back read from: **{head.held_back_from}**.", ""]
    out += ["| Number | Value | Direction |", "|---|---|---|"]
    for label, key, direction in ROWS:
        out.append(f"| {label} | {_cell(getattr(head, key))} | {direction} |")
    f1 = "—" if head.extraction_f1 is None else f"{head.extraction_f1:.4f}"
    out += [f"| Filed correctly (extraction F1) | {f1} | line 0.90 |", ""]
    out += ["## Unsupported claims", ""]
    out += [f"- `{c.id}`: {', '.join(c.reasons)}" for c in head.claims] or ["None."]
    out += ["", "## Over-caution", ""]
    out += [f"- `{qid}`" for qid in head.over_cautious] or ["None."]
    out += ["", "## Retrieval misses", ""]
    out += [f"- `{qid}`" for qid in head.retrieval_miss] or ["None."]
    out += ["", "## Not right and cited (Set A)", ""]
    out += [f"- `{qid}`" for qid in head.not_right] or ["None."]
    if head.not_in_sets:
        out += [
            "",
            f"{len(head.not_in_sets)} questions in the run are no longer in the question files "
            "and were not scored: " + ", ".join(f"`{q}`" for q in head.not_in_sets) + ".",
        ]
    return "\n".join(out) + "\n"


def movement(columns: Sequence[tuple[str, str, Headline]]) -> str:
    """One table across runs: (name, corpus sha, headline) in order. A change is shown only
    between neighbouring runs on the same corpus; across a corpus boundary there is none."""
    header = "| Number | " + " | ".join(name for name, _, _ in columns) + " |"
    out = [header, "|---|" + "---|" * len(columns)]
    for label, key, _ in ROWS:
        cells: list[str] = []
        for i, (_, corpus, head) in enumerate(columns):
            cell = _cell(getattr(head, key))
            if i:
                _, before_corpus, before = columns[i - 1]
                moved = (
                    "new corpus"
                    if before_corpus != corpus
                    else change(getattr(before, key), getattr(head, key))
                )
                cell += f" · {moved}" if moved else ""
            cells.append(cell)
        out.append(f"| {label} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def previous_run(results: Path, *, before: Path, corpus: str) -> Headline | None:
    """The headline of the run in `results` that ran last before `before`, on the same corpus
    (`corpus` is its manifest sha), if one has a headline. A run on another corpus is skipped,
    and so is one with no recorded sha: a change is only read between runs on one corpus.

    "Last" is the time each run recorded (`run.date`), not its file name: two runs on one day
    sort by their labels, and a label says nothing about which ran first. A file with no
    recorded time falls back to the date its name starts with."""
    if not corpus:
        return None
    ceiling = _ran_at(_read(before), before) if before.exists() else "~"  # "~" sorts last
    best: tuple[str, dict[str, Any]] | None = None
    for path in results.glob("*.json"):
        if path == before:
            continue
        data = _read(path)
        run = data.get("run") or {}
        if str(run.get("corpus_manifest_sha") or "") != corpus:
            continue
        if "per_question" not in data or not isinstance(data.get("headline"), dict):
            continue
        when = _ran_at(data, path)
        if when < ceiling and (best is None or when > best[0]):
            best = (when, data["headline"])
    return None if best is None else from_json(best[1])


def _read(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _ran_at(data: Mapping[str, Any], path: Path) -> str:
    """When a run ran, as an ISO string that sorts in time order."""
    return str((data.get("run") or {}).get("date") or path.name[:10])


def from_json(raw: Mapping[str, Any]) -> Headline:
    def count_of(value: Any) -> Count | None:
        return None if value is None else Count(int(value["hits"]), int(value["n"]))

    return Headline(
        held_back_from=str(raw.get("held_back_from", "recorded")),
        right_and_cited=count_of(raw.get("right_and_cited")),
        not_right=list(raw.get("not_right", [])),
        unsupported_claims=count_of(raw.get("unsupported_claims")),
        claims=[Claim(c["id"], tuple(c["reasons"])) for c in raw.get("claims", [])],
        over_caution=count_of(raw.get("over_caution")),
        over_cautious=list(raw.get("over_cautious", [])),
        retrieval_miss=list(raw.get("retrieval_miss", [])),
        casual=count_of(raw.get("casual")),
        formal=count_of(raw.get("formal")),
        extraction_f1=raw.get("extraction_f1"),
        not_in_sets=list(raw.get("not_in_sets", [])),
    )


# ------------------------------------------------------------------------------- the CLI


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("runs", nargs="+", type=Path, help="result files from eval.run")
    args = parser.parse_args(argv)

    runs: list[tuple[Path, dict[str, Any]]] = []
    try:
        for path in args.runs:
            data = json.loads(path.read_text(encoding="utf-8"))
            if "per_question" not in data:
                raise NotScorable(f"{path} has no per_question lines; it is not an eval.run file")
            runs.append((path, data))
    except (OSError, json.JSONDecodeError, NotScorable) as error:
        print(error)
        return 2

    recording = [line for _, data in runs for line in data["per_question"] if "held_back" in line]
    wrong = disagreements(recording)
    trusted = bool(recording) and not wrong
    if wrong:
        print(f"the rebuilt held_back disagrees on {len(wrong)} question(s): {', '.join(wrong)}")
    elif not recording:
        print("no run records held_back, so a rebuild cannot be checked and is not used")

    questions = all_questions(ROOT)
    columns: list[tuple[str, str, Headline]] = []
    for path, data in runs:
        metrics = data.get("metrics") or {}
        head = compute(
            data["per_question"],
            questions,
            extraction_f1=metrics.get("extraction_f1"),
            rebuild=trusted,
        )
        stem = path.with_suffix("")
        companion = Path(f"{stem}-headline.json")
        body = {"source": path.name, "headline": as_json(head)}
        text = json.dumps(body, indent=2, ensure_ascii=False) + "\n"
        if companion.exists() and companion.read_text(encoding="utf-8") != text:
            print(f"{companion} exists with different numbers and results are append-only")
            return 2
        companion.write_text(text, encoding="utf-8")
        Path(f"{stem}-headline.md").write_text(render(path.name, head), encoding="utf-8")
        corpus = str((data.get("run") or {}).get("corpus_manifest_sha") or "")
        columns.append((path.stem, corpus, head))
        print(f"wrote {companion}")

    if len(columns) > 1:
        print()
        print(movement(columns))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
