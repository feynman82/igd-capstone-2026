"""Field extraction F1 by document type: the week 6 table, read from the vault rather than typed.

    uv run python -m eval.report                 # writes eval/results/w6-extraction-by-doc-type.md
    uv run python -m eval.report --out -         # print it instead

Metric 6 in `eval/README.md` is one micro-averaged number over every field of every indexed
document, and a single number cannot say what to fix. This writes the same arithmetic split two
ways: per document type, worst first, and — for the types under target — per register column, so
the lane that owns extraction is pointed at one field on one template rather than at a score.

It needs the vault and the register, and nothing else: no generation, no judge, no retrieval.
Extraction F1 compares `facts` rows against register cells, so this runs in seconds and can be
re-run after any ingest. That is also why it is a separate command — asking for the table should
not cost a full evaluation run.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from eval.score import F1, TypeScore, extraction_by_type, unjoined

ROOT = Path(__file__).resolve().parents[1]
TARGET = 0.90  # metric 6 in eval/README.md


@dataclass(frozen=True, slots=True)
class Provenance:
    """What the table was measured against, so a later run can be told from this one."""

    date: str
    git_sha: str
    corpus_sha: str
    registered: int  # register rows
    indexed: int  # documents the vault has indexed
    scored: int  # of those, the ones that both match a register row and produced facts
    quarantined: int  # documents the vault holds and did not extract
    catalogue: int  # document types core/documents.yaml defines
    in_register: int  # of those, the types the register actually fills


def _cell(value: float | None) -> str:
    return "—" if value is None else f"{value:.3f}"


def _row(name: str, documents: str, score: F1, *, bar: bool) -> str:
    fields = score.tp + score.fp + score.fn
    met = ""
    if bar:
        met = " ✓" if (score.f1 or 0.0) >= TARGET else " ✗"
    return (
        f"| {name} | {documents} | {fields} | {score.tp} | {score.fp} | {score.fn} | "
        f"{_cell(score.precision)} | {_cell(score.recall)} | {_cell(score.f1)} |{met} |"
    )


def render(
    scores: Sequence[TypeScore],
    overall: F1,
    unscored: Sequence[str],
    where: Provenance,
    unjoined: Mapping[str, int] | None = None,
) -> str:
    """The report, as markdown. A pure function of the numbers so that a test can check the
    table without a database — and so that nothing in it can be edited by hand without the next
    run putting it back."""
    weak = [score for score in scores if (score.overall.f1 or 0.0) < TARGET]
    lines = [
        f"# Field extraction F1 by document type — {where.date}",
        "",
        f"Metric 6 of `eval/README.md`, split by `doc_type`. Target ≥ {TARGET:.2f}. "
        f"Scored against `corpus/register/` by `python -m eval.report`; corpus "
        f"`{where.corpus_sha}`, code `{where.git_sha}`.",
        "",
        f"{where.indexed} of {where.registered} register rows are indexed in the vault"
        + (f", {where.quarantined} quarantined" if where.quarantined else "")
        + f", and {where.scored} of them produced facts to score. The catalogue defines "
        f"{where.catalogue} document types, the register fills {where.in_register}, and "
        f"{len(scores)} have an indexed document to score.",
        "",
        "| document type | docs | fields | tp | fp | fn | precision | recall | F1 | ≥ target |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|:--:|",
    ]
    lines += [
        _row(f"`{score.doc_type}`", str(score.documents), score.overall, bar=True)
        for score in scores
    ]
    lines.append(_row("**every type**", str(where.scored), overall, bar=True))
    lines.append("")

    if weak:
        lines += [
            "## Which fields hold them down",
            "",
            "Only the types under target, and within each only the fields that are not already "
            "1.0. `fn` is a value the register prints and the extractor did not write; `fp` is a "
            "value it wrote that the register does not have, or wrote differently.",
            "",
        ]
        for score in weak:
            lines += [
                f"### `{score.doc_type}` — F1 {_cell(score.overall.f1)} over "
                f"{score.documents} document{'s' if score.documents != 1 else ''}",
                "",
                "| field | tp | fp | fn | precision | recall | F1 |",
                "|---|---:|---:|---:|---:|---:|---:|",
            ]
            for key, f1 in score.weakest:
                lines.append(
                    f"| `{key}` | {f1.tp} | {f1.fp} | {f1.fn} | {_cell(f1.precision)} | "
                    f"{_cell(f1.recall)} | {_cell(f1.f1)} |"
                )
            lines.append("")

    if unscored:
        lines += [
            "## Types the register fills and the vault has not indexed",
            "",
            "Not a weakness and not a zero: there is no document to extract from yet, so they "
            "are absent from the table above rather than scored at 0. "
            + ", ".join(f"`{name}`" for name in unscored)
            + ".",
            "",
        ]
    if unjoined:
        total = sum(unjoined.values())
        lines += [
            "## Indexed documents no register row claims",
            "",
            f"{len(unjoined)} document(s) in the vault are named for what they are rather than "
            f"for a register row, so the {total} facts extracted from them are neither hits nor "
            "misses — there is nothing to compare them against. `corpus/README.md` makes the "
            "file name the register id, so each of these is a rename away from being measurable "
            "(`core/ingest/register.py` re-registers on `sha256`, keeping the document id and "
            "its citations).",
            "",
            "| document in the vault | facts extracted |",
            "|---|---:|",
        ]
        lines += [f"| `{name}` | {count} |" for name, count in sorted(unjoined.items())]
        lines.append("")
    lines += [
        "## How to read it",
        "",
        "_(one paragraph, written on the day)_",
        "",
    ]
    return "\n".join(lines)


def collect(root: Path) -> tuple[list[TypeScore], F1, list[str], Provenance, dict[str, int]]:
    """Everything the report needs, from the vault and the register."""
    from core.document_schemas import MODELS
    from core.runtime.db import connect
    from core.runtime.settings import Settings
    from eval.run import _corpus_sha, _facts, _git_sha, _indexed
    from eval.sets_io import read_registers

    settings = Settings.load(root)
    register = read_registers(root)
    with connect(settings) as conn:
        facts = _facts(conn)
        indexed = _indexed(conn)
        statuses = _statuses(conn)
    scores = extraction_by_type(register, facts, indexed)
    overall = _overall(scores)
    types = {score.doc_type for score in scores}
    filled = {row.get("doc_type") or "unknown" for row in register}
    where = Provenance(
        date=datetime.now(UTC).date().isoformat(),
        git_sha=_git_sha(),
        corpus_sha=_corpus_sha(root),
        registered=len({row.get("doc_id") for row in register}),
        indexed=statuses.get("indexed", 0),
        scored=sum(score.documents for score in scores),
        quarantined=statuses.get("quarantined", 0),
        catalogue=len(MODELS),
        in_register=len(filled),
    )
    return scores, overall, sorted(filled - types), where, unjoined(register, facts)


def _overall(scores: Sequence[TypeScore]) -> F1:
    return F1(
        tp=sum(score.overall.tp for score in scores),
        fp=sum(score.overall.fp for score in scores),
        fn=sum(score.overall.fn for score in scores),
    )


def _statuses(conn: Any) -> dict[str, int]:
    """How many documents the vault holds in each status. A quarantined document is why an
    `indexed` count and a scored count differ, and the report says both rather than one."""
    with conn.cursor() as cur:
        cur.execute(DOCUMENT_STATUSES)
        return {str(status): int(count) for status, count in cur.fetchall()}


# Hand-written, as AGENTS.md rule 1 requires.
DOCUMENT_STATUSES = """
SELECT status, count(*) FROM documents GROUP BY status
"""


def _summary(scores: Sequence[TypeScore], overall: F1) -> str:
    under = [score for score in scores if (score.overall.f1 or 0.0) < TARGET]
    head = f"extraction_f1 {_cell(overall.f1)} over {len(scores)} document type(s)"
    if not under:
        return f"{head}; every type clears {TARGET:.2f}."
    worst = ", ".join(f"{score.doc_type} {_cell(score.overall.f1)}" for score in under)
    return f"{head}; under target: {worst}"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--out",
        default=str(ROOT / "eval" / "results" / "w6-extraction-by-doc-type.md"),
        help="file to write, or - for stdout (default eval/results/w6-extraction-by-doc-type.md)",
    )
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    from core.runtime.db import DatabaseUnavailable
    from core.runtime.settings import ConfigurationError

    try:
        scores, overall, unscored, where, loose = collect(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2
    except DatabaseUnavailable as error:
        print(error)
        return 2
    if not scores:
        print("No indexed document has a register row to score against. Ingest a batch first.")
        return 2

    report = render(scores, overall, unscored, where, loose)
    if args.out == "-":
        print(report)
        return 0
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    keep = _paragraph(target)
    target.write_text(report.replace(PLACEHOLDER, keep) if keep else report, encoding="utf-8")
    print(_summary(scores, overall))
    print(f"wrote {target}")
    return 0


PLACEHOLDER = "_(one paragraph, written on the day)_"


def _paragraph(target: Path) -> str:
    """The prose under "How to read it" from the file already there, if someone has written it.

    The numbers are the vault's and are rewritten every run; the reading of them is a person's
    and must survive a re-run, or nobody will re-run it.
    """
    if not target.exists():
        return ""
    after = target.read_text(encoding="utf-8").partition("## How to read it")[2].strip()
    return "" if not after or after == PLACEHOLDER else after


if __name__ == "__main__":
    raise SystemExit(main())
