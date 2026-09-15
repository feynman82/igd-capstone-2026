"""The golden sets on disk, and the register they were written from.

A question file is JSONL under `eval/sets/<set>/`, one file per lane, in the shape
`eval/README.md` shows. Everything here is validation and shape. Five people write these files
by hand, and the harness would rather refuse one malformed line at load time than score sixty
questions and discover afterwards that one of them was never read.
"""

from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, cast

SetId = Literal["A", "B", "C"]
Kind = Literal["fact", "passage", "abstain"]

SET_FOLDERS: dict[SetId, str] = {"A": "answerable", "B": "hard_negatives", "C": "adversarial"}
KINDS: tuple[Kind, ...] = ("fact", "passage", "abstain")


class MalformedQuestion(ValueError):
    """A line the harness cannot grade. The message names the file and the line."""


@dataclass(frozen=True, slots=True)
class Expected:
    kind: Kind
    pack: str = ""
    key: str = ""
    value: str = ""  # the register's own text for the value: "2027-03-31", "1284.00"


@dataclass(frozen=True, slots=True)
class Question:
    id: str
    set: SetId
    lane: str
    question: str
    expected: Expected
    must_cite_doc: str = ""  # the register's doc_id: "b1-0001"
    must_cite_page: int = 0  # 0 only for an abstention, which has nothing correct to cite
    notes: str = ""

    @property
    def gradeable_citation(self) -> bool:
        return bool(self.must_cite_doc) and self.must_cite_page >= 1


def load_set(root: Path, set_id: SetId) -> list[Question]:
    """Every question in `eval/sets/<folder>/*.jsonl`, in file order, validated.

    An empty folder is an empty list rather than an error: the sets fill up over week 3, and a
    harness that refused to run until all sixty were in would never have been run at all.
    """
    folder = root / "eval" / "sets" / SET_FOLDERS[set_id]
    questions: list[Question] = []
    seen: dict[str, Path] = {}
    for path in sorted(folder.glob("*.jsonl")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            where = f"{path.relative_to(root)}:{number}"
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as error:
                raise MalformedQuestion(f"{where}: not JSON ({error.msg})") from error
            question = _question(raw, where)
            if question.set != set_id:
                raise MalformedQuestion(
                    f"{where}: set {question.set!r} in a file under {SET_FOLDERS[set_id]}/"
                )
            if question.id in seen:
                raise MalformedQuestion(
                    f"{where}: id {question.id!r} already used in {seen[question.id].name}"
                )
            seen[question.id] = path
            questions.append(question)
    return questions


def _question(raw: Any, where: str) -> Question:
    if not isinstance(raw, dict):
        raise MalformedQuestion(f"{where}: expected an object")
    for key in ("id", "set", "lane", "question", "expected"):
        if key not in raw:
            raise MalformedQuestion(f"{where}: missing {key!r}")
    if raw["set"] not in SET_FOLDERS:
        raise MalformedQuestion(f"{where}: set must be A, B or C, not {raw['set']!r}")
    expected = _expected(raw["expected"], where)
    doc = str(raw.get("must_cite_doc") or "")
    page = raw.get("must_cite_page")
    if expected.kind == "abstain":
        if doc or page is not None:
            raise MalformedQuestion(
                f"{where}: an abstain question cites nothing (see eval/sets/README.md)"
            )
        page = 0
    else:
        if not doc:
            raise MalformedQuestion(f"{where}: a {expected.kind} question needs must_cite_doc")
        if not isinstance(page, int) or isinstance(page, bool) or page < 1:
            raise MalformedQuestion(
                f"{where}: must_cite_page must be a page number from the register, 1 or above"
            )
    return Question(
        id=str(raw["id"]),
        set=cast(SetId, raw["set"]),
        lane=str(raw["lane"]),
        question=str(raw["question"]),
        expected=expected,
        must_cite_doc=doc,
        must_cite_page=page,
        notes=str(raw.get("notes") or ""),
    )


def _expected(raw: Any, where: str) -> Expected:
    if not isinstance(raw, dict) or raw.get("kind") not in KINDS:
        raise MalformedQuestion(f"{where}: expected.kind must be fact, passage or abstain")
    kind = cast(Kind, raw["kind"])
    key = str(raw.get("key") or "")
    value = raw.get("value")
    if kind == "fact" and (not key or value is None or value == ""):
        raise MalformedQuestion(f"{where}: a fact question needs expected.key and expected.value")
    return Expected(kind, str(raw.get("pack") or ""), key, "" if value is None else str(value))


def subset(questions: list[Question], size: int, *, seed: int) -> list[Question]:
    """At most `size` questions, spread across lanes, the same choice every run for one seed.

    Round-robin over lanes after shuffling within each, so a 25-question quick run still
    touches every lane rather than the first two files alphabetically.
    """
    if size >= len(questions):
        return list(questions)
    rng = random.Random(seed)
    by_lane: dict[str, list[Question]] = defaultdict(list)
    for question in questions:
        by_lane[question.lane].append(question)
    lanes = sorted(by_lane)
    for lane in lanes:
        rng.shuffle(by_lane[lane])
    chosen: list[Question] = []
    while len(chosen) < size:
        for lane in lanes:
            if by_lane[lane] and len(chosen) < size:
                chosen.append(by_lane[lane].pop())
    order = {question.id: index for index, question in enumerate(questions)}
    return sorted(chosen, key=lambda question: order[question.id])


# ------------------------------------------------------------------------------- the register


def read_register(path: Path) -> list[dict[str, str]]:
    """Desmond's register as rows. Comment lines are skipped; the header is the generated one."""
    with path.open(encoding="utf-8-sig", newline="") as handle:
        lines = [line for line in handle if not line.startswith("#")]
    return [dict(row) for row in csv.DictReader(lines)]


def read_registers(root: Path) -> list[dict[str, str]]:
    """Every batch register, skipping the templates the pack build writes beside them."""
    rows: list[dict[str, str]] = []
    for path in sorted((root / "corpus" / "register").glob("*.csv")):
        if path.name.endswith(("template.csv", "_columns.csv")):
            continue
        rows.extend(read_register(path))
    return rows


def field_page(row: Mapping[str, str], key: str) -> int:
    """Which page a value is printed on. `field_pages` names only the fields that are not on
    page 1, in the form `expiry_date=2;premium_payable=2`."""
    for item in (row.get("field_pages") or "").split(";"):
        name, _, page = item.strip().partition("=")
        if name == key and page.strip().isdigit():
            return int(page)
    return 1
