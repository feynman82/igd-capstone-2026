"""Generate Set A fact questions from the register, one lane's dozen at a time.

    uv run python -m eval.generate --lane retrieval             # 12, to eval/sets/answerable/
    uv run python -m eval.generate --all-lanes                  # every lane's dozen
    uv run python -m eval.generate --lane packs --all --dry-run # that lane's whole pool

`eval/README.md` says it: every document is authored *from* a register row, so the register
already holds the correct answer for every printed field, and Set A's questions about dates and
amounts are generated rather than written by hand. Each question carries `expected`,
`must_cite_doc` and `must_cite_page` from the row, so it is gradeable the moment it is written.
What a generator cannot write — the passage questions, the module questions, the adversarial
ones — is still a person's job, and each lane's.

Two wordings per field, one naming the printed reference and one naming the document as a
person would (`eval/phrasings.py`), because the identifier and the paraphrase measure different
halves of the retriever.

Questions are generated **from the register, not from the documents on disk**. The register is
the ground truth and it is complete; the batch is mail-merged from it later. A question whose
document has not been generated yet is still correct — `eval.run` skips it and says how many it
skipped, rather than scoring a missing document as a retrieval failure.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from eval.phrasings import LANES, SPECS, lane_of
from eval.score import REGISTER_META
from eval.sets_io import field_page, read_registers

ROOT = Path(__file__).resolve().parents[1]

Row = Mapping[str, str]
FORMS = ("printed", "spoken")


@dataclass(frozen=True, slots=True)
class Generated:
    id: str
    question: str
    doc_id: str
    key: str
    form: str  # "printed" names the reference on the page, "spoken" names the document

    def line(self, row: Row, lane: str) -> dict[str, object]:
        return {
            "id": self.id,
            "set": "A",
            "lane": lane,
            "question": self.question,
            "expected": {
                "kind": "fact",
                "pack": row.get("pack_id") or "",
                "key": self.key,
                "value": (row.get(self.key) or "").strip(),
            },
            "must_cite_doc": self.doc_id,
            "must_cite_page": field_page(row, self.key),
            "notes": f"generated from the register ({self.form} wording)",
        }


def on_file(root: Path) -> set[str]:
    """The register ids that have a document under `corpus/batches/`, by file stem."""
    folder = root / "corpus" / "batches"
    if not folder.is_dir():
        return set()
    return {p.stem for p in folder.rglob("*") if p.is_file() and not p.name.startswith(".")}


def hand_written(root: Path) -> set[str]:
    """The question texts a person has already written into `eval/sets/answerable/`.

    A generated question that repeats one of those adds nothing and scores the same evidence
    twice, so the hand-written file wins and the generator fills around it.
    """
    folder = root / "eval" / "sets" / "answerable"
    texts: set[str] = set()
    for path in sorted(folder.glob("*.jsonl")) if folder.is_dir() else []:
        if path.name.endswith("-generated.jsonl"):
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("{"):
                texts.add(str(json.loads(line).get("question", "")))
    return texts


def pool(rows: Sequence[Row]) -> list[tuple[Generated, Row]]:
    """Every gradeable question the register supports, in register order.

    Two things are dropped here, and both would otherwise produce a question nobody could mark:

    **A question that prints its own answer.** "What name is printed on Marcus Lim Jun Wei's
    identity card?" is not a question, and a system that answered it from the question rather
    than the document would score the same as one that read the page.

    **A wording that names two documents.** Marcus has two donation receipts, so "Marcus's
    donation receipt" names neither; the answer would be graded against one `doc_id` while a
    correct system cited the other. Only wordings unique across the whole register survive,
    which is why this is judged over every row rather than one lane's.

    A field the catalogue marks as repeating prints several labelled amounts, so there is no one
    value to check an answer against; `eval/phrasings.py` leaves those out by not asking about
    them, and anything the register fills but no wording covers is skipped.
    """
    out: list[tuple[Generated, Row]] = []
    for row in rows:
        doc_id = (row.get("doc_id") or "").strip()
        spec = SPECS.get(row.get("doc_type") or "")
        if not doc_id or spec is None:
            continue
        for key, value in row.items():
            if key in REGISTER_META or not (value or "").strip():
                continue
            for form in FORMS:
                text = spec.question(row, key, form)
                if text and value.strip().casefold() not in text.casefold():
                    generated = Generated(f"a-gen-{doc_id}-{key}-{form}", text, doc_id, key, form)
                    out.append((generated, row))
    return [item for item in out if item[0].question not in _ambiguous(out)]


def _ambiguous(items: Sequence[tuple[Generated, Row]]) -> frozenset[str]:
    """Question texts that arise from more than one document."""
    documents: dict[str, set[str]] = defaultdict(set)
    for generated, _ in items:
        documents[generated.question].add(generated.doc_id)
    return frozenset(text for text, docs in documents.items() if len(docs) > 1)


def choose(
    items: list[tuple[Generated, Row]], limit: int, *, seed: int
) -> list[tuple[Generated, Row]]:
    """`limit` questions spread across documents, alternating wordings, the same for one seed."""
    if limit >= len(items):
        return list(items)
    rng = random.Random(seed)
    by_doc: dict[str, list[tuple[Generated, Row]]] = defaultdict(list)
    for item in items:
        by_doc[item[0].doc_id].append(item)
    for bucket in by_doc.values():
        rng.shuffle(bucket)
    chosen: list[tuple[Generated, Row]] = []
    asked: dict[str, set[str]] = defaultdict(set)  # fields already asked about, per document
    docs = sorted(by_doc)
    while len(chosen) < limit and any(by_doc.values()):
        for doc in docs:
            bucket = by_doc[doc]
            if not bucket or len(chosen) >= limit:
                continue
            # Alternating per question rather than per pass: with more documents than questions
            # the first pass fills the quota, and a set in one wording measures half a retriever.
            wanted = FORMS[len(chosen) % 2]
            fresh = [i for i, item in enumerate(bucket) if item[0].key not in asked[doc]]
            preferred = [i for i in fresh if bucket[i][0].form == wanted]
            item = bucket.pop((preferred or fresh or [len(bucket) - 1])[0])
            asked[doc].add(item[0].key)
            chosen.append(item)
    order = {item[0].id: i for i, item in enumerate(items)}
    return sorted(chosen, key=lambda item: order[item[0].id])


def write_lane(
    lane: str,
    every_question: Sequence[tuple[Generated, Row]],
    present: set[str],
    already: set[str],
    args: argparse.Namespace,
) -> tuple[int, int, int]:
    """One lane's file. Returns (written, pool size, how many have no document yet)."""
    everything = [
        item
        for item in every_question
        if lane_of(item[1]) == lane and item[0].question not in already
    ]
    chosen = list(everything) if args.all else choose(everything, args.limit, seed=args.seed)
    lines = [json.dumps(item.line(row, lane), ensure_ascii=False) for item, row in chosen]
    waiting = sum(1 for item, _ in chosen if item.doc_id not in present)

    target = args.out or ROOT / "eval" / "sets" / "answerable" / f"{lane}-generated.jsonl"
    if args.dry_run:
        print("\n".join(lines))
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(lines) + "\n", encoding="utf-8")
        shown = target.relative_to(ROOT) if target.is_relative_to(ROOT) else target
        print(f"{lane:<12} {len(lines):>3} questions -> {shown}")
    return len(lines), len(everything), waiting


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    lanes = parser.add_mutually_exclusive_group(required=True)
    lanes.add_argument("--lane", choices=sorted(LANES), help="which lane's questions to write")
    lanes.add_argument("--all-lanes", action="store_true", help="every lane's dozen")
    parser.add_argument("--limit", type=int, default=12, help="how many per lane (default 12)")
    parser.add_argument("--all", action="store_true", help="the whole pool, ignoring --limit")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--out", type=Path, default=None, help="one lane only; default eval/sets/answerable/"
    )
    parser.add_argument("--dry-run", action="store_true", help="print, do not write")
    args = parser.parse_args(argv)
    if args.all_lanes and args.out:
        parser.error("--out writes one file, so it cannot be used with --all-lanes")

    rows = read_registers(ROOT)
    present = on_file(ROOT)
    every_question = pool(rows)
    already = hand_written(ROOT)
    written = waiting = 0
    for lane in sorted(LANES) if args.all_lanes else [args.lane]:
        count, size, missing = write_lane(lane, every_question, present, already, args)
        written += count
        waiting += missing
        if args.all_lanes and not args.dry_run:
            print(f"             from a pool of {size}; {missing} await their document")
    if not args.dry_run:
        print(f"\n{written} questions written; {waiting} of them await a document.")
        print(
            f"{len(present)} of {len({r.get('doc_id') for r in rows})} register rows have a "
            "document under corpus/batches/. `eval.run` skips a question whose document is not "
            "in the vault and says how many it skipped."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
