"""Run the golden sets through PARROT and write one result file.

    uv run python -m eval.run --corpus a --subset 25 --out /tmp/parrot-eval   # make eval-quick
    uv run python -m eval.run --corpus all --out eval/results --label baseline-dense-only

`--corpus` names the golden sets to run: `a`, `b`, `c`, a comma-separated mix, or `all`.
`--subset N` takes at most N questions from each set, spread across lanes, the same N every
time for one `--seed`. `--judge` names the Ollama model that reads the evidence for the four
Ragas metrics; `--no-judge` skips them and writes the code-scored metrics alone, which is the
mode a laptop without a spare model uses.

The file is `<out>/<date>-<label>.json` and is never overwritten: `eval/results/` is
append-only, and a run that would replace another is asked to pick a different label instead.
A sibling `.md` is started with the run's header, for the paragraph the results README asks
for. The paragraph is yours; the numbers are the file's.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
from collections.abc import Sequence
from datetime import UTC, date, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from eval.sets_io import SetId

ROOT = Path(__file__).resolve().parents[1]
NOISY = ("httpx", "docling", "RapidOCR", "huggingface_hub", "filelock", "openai", "instructor")

# The targets in eval/README.md, repeated here only so the terminal can show a number next to
# the bar it has to clear. The README is the agreed list; this is a courtesy.
TARGETS: dict[str, tuple[str, float] | None] = {
    "context_recall": (">=", 0.85),
    "context_precision": (">=", 0.70),
    "faithfulness": (">=", 0.90),
    "answer_relevancy": (">=", 0.80),
    "abstention_rate": (">=", 0.95),
    "extraction_f1": (">=", 0.90),
    "obligation_precision": (">=", 0.95),
    "alert_fpr": ("<=", 0.05),
    "decode_tok_s": None,
    "peak_vram_gb": None,
}

# Hand-written and parameterised, as AGENTS.md rule 5 requires. The register names a document
# by its file stem, so the stem is what both queries match on.
PAGE_TEXT = """
SELECT string_agg(c.text, E'\\n' ORDER BY c.ordinal)
  FROM chunks c
  JOIN documents d ON d.id = c.document_id
 WHERE regexp_replace(d.original_name, '\\.[^.]+$', '') = %(doc_id)s
   AND c.page = %(page)s
"""

INDEXED_FACTS = """
SELECT regexp_replace(d.original_name, '\\.[^.]+$', '') AS doc_id,
       f.key,
       f.value_text,
       f.value_num,
       f.value_date
  FROM facts f
  JOIN documents d ON d.id = f.document_id
 WHERE d.status = 'indexed'
 ORDER BY f.confidence, f.id
"""


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=_Formatter)
    parser.add_argument("--corpus", default="all", help="a, b, c, a,b or all (default all)")
    parser.add_argument("--subset", type=int, default=0, help="at most N questions per set")
    parser.add_argument("--seed", type=int, default=0, help="which N; the same N for one seed")
    parser.add_argument("--out", type=Path, default=ROOT / "eval" / "results")
    parser.add_argument("--label", default="", help="what changed; part of the file name")
    parser.add_argument("--judge", default="", help="Ollama model for the Ragas metrics")
    parser.add_argument("--no-judge", action="store_true", help="code-scored metrics only")
    parser.add_argument("--candidates", type=int, default=40)
    parser.add_argument("--keep", type=int, default=6)
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.WARNING, format="%(message)s")
    for name in NOISY:
        logging.getLogger(name).setLevel(logging.ERROR)

    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.ollama import ModelUnavailable, Ollama
    from core.runtime.settings import ConfigurationError, Settings
    from eval import harness, score
    from eval.sets_io import MalformedQuestion, load_set, read_registers, subset

    try:
        sets = _sets(args.corpus)
    except ValueError as error:
        parser.error(str(error))
    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    try:
        questions = [q for set_id in sets for q in _chosen(load_set(ROOT, set_id), args, subset)]
    except MalformedQuestion as error:
        print(f"A golden-set line cannot be graded: {error}")
        return 2
    if not questions:
        print(f"No questions under eval/sets/ for {', '.join(sets)}. Nothing to run.")
        return 2

    judge_model = (
        ""
        if args.no_judge
        else (args.judge or os.environ.get("PARROT_JUDGE_MODEL") or settings.generation_model)
    )
    label = args.label or ("judged" if judge_model else "code-scored")
    target = args.out / f"{date.today().isoformat()}-{label}.json"
    if target.exists():
        print(f"{target} already exists and results are append-only. Choose another --label.")
        return 2

    print(f"{len(questions)} questions ({_counts(questions)}); retrieval: dense-only")
    print(f"generator {settings.generation_model}; judge {judge_model or 'none'}")

    try:
        with connect(settings) as conn:
            graph, recorder = harness.build(
                conn, settings, candidates=args.candidates, keep=args.keep
            )
            traces = harness.trace_all(graph, recorder, questions, on_each=_progress)
            scored = score.grade(traces)
            references = {
                q.id: score.reference_for(q, _page_text(conn, q.must_cite_doc, q.must_cite_page))
                for q in questions
                if q.set == "A"
            }
            facts = _facts(conn)
    except DatabaseUnavailable as error:
        print(error)
        return 2
    except ModelUnavailable as error:
        print(f"A model is unavailable: {error}")
        return 2

    if judge_model:
        print(f"judging Set A with {judge_model}…")
        judge = score.RagasJudge(judge_model, settings.generation_url, Ollama(settings).embed)
        score.judge_sync(scored, judge, references)

    extraction = score.extraction_f1(read_registers(ROOT), facts)
    runtime, runtime_source = _runtime_numbers(ROOT / "eval" / "results", settings.context_tokens)
    metrics, also, why = score.summarise(
        scored, extraction=extraction, runtime=runtime, judged=bool(judge_model)
    )
    result = {
        "run": {
            "date": datetime.now(UTC).isoformat(timespec="seconds"),
            "label": label,
            "git_sha": _git_sha(),
            "corpus_manifest_sha": _corpus_sha(ROOT),
            "sets": list(sets),
            "subset": args.subset or None,
            "seed": args.seed,
            "generator": settings.generation_model,
            "embedder": settings.embedding_model,
            "judge": judge_model or None,
            "retriever": "dense-only",
            "reranker": "none",
            "candidates": args.candidates,
            "keep": args.keep,
            "runtime_numbers_from": runtime_source,
        },
        "metrics": metrics,
        "not_measured": why,
        "also": also,
        "per_question": [item.as_dict() for item in scored],
    }
    args.out.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    note = target.with_suffix(".md")
    if not note.exists():
        note.write_text(_note(result), encoding="utf-8")
    print()
    print(_table(metrics, why))
    print(f"\nwrote {target}")
    return 0


# ------------------------------------------------------------------------------- pieces


class _Formatter(argparse.RawDescriptionHelpFormatter):
    pass


def _sets(spec: str) -> tuple[SetId, ...]:
    from eval.sets_io import SET_FOLDERS

    if spec.strip().lower() == "all":
        return ("A", "B", "C")
    wanted = tuple(part.strip().upper() for part in spec.split(",") if part.strip())
    if not wanted or any(w not in SET_FOLDERS for w in wanted):
        raise ValueError(f"--corpus takes a, b, c or all, not {spec!r}")
    return tuple(cast("SetId", w) for w in wanted)


def _chosen(questions: list[Any], args: argparse.Namespace, pick: Any) -> list[Any]:
    return (
        cast(list[Any], pick(questions, args.subset, seed=args.seed))
        if args.subset
        else (questions)
    )


def _counts(questions: Sequence[Any]) -> str:
    counts: dict[str, int] = {}
    for question in questions:
        counts[question.set] = counts.get(question.set, 0) + 1
    return ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))


def _progress(trace: Any) -> None:
    from eval.score import outcome_of

    print(f"  {trace.question.id:<8} {outcome_of(trace.answer):<16} {trace.latency_ms:>6} ms")


def _page_text(conn: Any, doc_id: str, page: int) -> str:
    if not doc_id or page < 1:
        return ""
    with conn.cursor() as cur:
        cur.execute(PAGE_TEXT, {"doc_id": doc_id, "page": page})
        row = cur.fetchone()
    return str(row[0]) if row and row[0] else ""


def _facts(conn: Any) -> list[Any]:
    from eval.score import FactRow

    with conn.cursor() as cur:
        cur.execute(INDEXED_FACTS)
        rows = cur.fetchall()
    facts: list[FactRow] = []
    for doc_id, key, text, number, when in rows:
        value = (
            when.isoformat()
            if when is not None
            else (f"{number:.2f}" if number is not None else text)
        )
        facts.append(FactRow(str(doc_id), str(key), None if value is None else str(value)))
    return facts


def _runtime_numbers(results: Path, context_tokens: int) -> tuple[dict[str, float | None], str]:
    """Decode rate and peak VRAM from the newest benchmark file `scripts/bench_runtime.py`
    wrote, preferring the row measured at this machine's context size. Read, never typed."""
    files = sorted(results.glob("*hardware*.md"))
    if not files:
        return {"decode_tok_s": None, "peak_vram_gb": None}, ""
    rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in files[-1].read_text(encoding="utf-8").splitlines()
        if line.startswith("| `")
    ]
    wanted = f"{context_tokens // 1024}K"
    rows.sort(key=lambda r: (len(r) < 7 or r[2] != wanted, len(r) < 4 or "short" not in r[3]))
    if not rows or len(rows[0]) < 7:
        return {"decode_tok_s": None, "peak_vram_gb": None}, files[-1].name
    decode = re.match(r"\s*(\d+(?:\.\d+)?)", rows[0][4])
    vram = re.match(r"\s*(\d+(?:\.\d+)?)\s*GB", rows[0][6])
    return {
        "decode_tok_s": float(decode.group(1)) if decode else None,
        "peak_vram_gb": float(vram.group(1)) if vram else None,
    }, files[-1].name


def _git_sha() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def _corpus_sha(root: Path) -> str:
    """One hash over every corpus file and register, so two runs can be told to have scored the
    same documents. The results README asks for the manifest; this is it."""
    digest = hashlib.sha256()
    corpus = root / "corpus"
    folders = (corpus / "batches", corpus / "holdout", corpus / "register")
    for path in sorted(p for folder in folders for p in folder.rglob("*") if p.is_file()):
        if path.name.startswith(".") or path.suffix == ".md":
            continue
        digest.update(str(path.relative_to(root)).encode())
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()[:16]


def _table(metrics: dict[str, float | None], why: dict[str, str]) -> str:
    lines = [f"{'metric':<22} {'value':>8}  target"]
    for key, value in metrics.items():
        target = TARGETS.get(key)
        bar = f"{target[0]} {target[1]:.2f}" if target else "measured"
        if value is None:
            lines.append(f"{key:<22} {'—':>8}  {bar}   ({why.get(key, '')})")
        else:
            met = ""
            if target:
                ok = value >= target[1] if target[0] == ">=" else value <= target[1]
                met = "  ✓" if ok else "  ✗"
            lines.append(f"{key:<22} {value:>8.4g}  {bar}{met}")
    return "\n".join(lines)


def _note(result: dict[str, Any]) -> str:
    run = result["run"]
    return (
        f"# {run['label']} — {run['date'][:10]}\n\n"
        f"Sets {', '.join(run['sets'])}; retrieval {run['retriever']}, reranker "
        f"{run['reranker']}; generator `{run['generator']}`; judge "
        f"`{run['judge'] or 'none'}`; corpus `{run['corpus_manifest_sha']}`; "
        f"code `{run['git_sha']}`.\n\n"
        "What changed, what moved, and whether that was expected:\n\n"
        "_(one paragraph, written on the day)_\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
