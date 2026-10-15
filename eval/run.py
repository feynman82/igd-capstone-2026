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
import importlib.util
import json
import logging
import os
import re
import subprocess
import sys
from collections.abc import Callable, Collection, Mapping, Sequence
from datetime import UTC, date, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from eval.sets_io import SetId

ROOT = Path(__file__).resolve().parents[1]
NOISY = ("httpx", "docling", "RapidOCR", "huggingface_hub", "filelock", "openai", "instructor")

# The reference lines in eval/README.md, repeated here only so the terminal can show a number
# beside the line the proposal drew for it. They explain a headline number; none is a line to
# clear, so the terminal prints them as text and marks nothing passed or failed.
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

INDEXED_DOCUMENTS = """
SELECT DISTINCT regexp_replace(original_name, '\\.[^.]+$', '') AS doc_id
  FROM documents
 WHERE status = 'indexed'
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
    parser.add_argument(
        "--retriever",
        choices=["hybrid", "dense"],
        default="hybrid",
        help="dense is the stopgap, kept so a retrieval change is measured on the same vault",
    )
    parser.add_argument(
        "--reranker",
        choices=["cross-encoder", "none"],
        default="cross-encoder",
        help="none is the stopgap that keeps retrieval's order",
    )
    parser.add_argument(
        "--no-modules",
        action="store_true",
        help="skip metrics 7 and 8 (obligation precision, alert FPR); they read the vault only",
    )
    parser.add_argument(
        "--score-missing",
        action="store_true",
        help="score a question whose document is not in the vault, instead of skipping it",
    )
    parser.add_argument(
        "--rerank-floor",
        type=float,
        default=None,
        help="relevance a passage must reach to be read (default: the calibrated one, ADR 0019)",
    )
    parser.add_argument(
        "--floor-off",
        action="store_true",
        help="answer below every pack's floor, for eval.bands to replay (not a production run)",
    )
    parser.add_argument(
        "--vault",
        default="",
        help="score against this database instead of the development vault (eval.setc uses it)",
    )
    parser.add_argument("--candidates", type=int, default=40)
    parser.add_argument("--keep", type=int, default=6)
    args = parser.parse_args(argv)

    # Before anything below imports `core/` or `eval/`: the code a run executes is the code it
    # loads now, and a checkout can move while forty minutes of questions are asked.
    started = {"git_sha": _git_sha(), "corpus_manifest_sha": _corpus_sha(ROOT)}

    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.WARNING, format="%(message)s")
    for name in NOISY:
        logging.getLogger(name).setLevel(logging.ERROR)

    from core.retrieve.rerank import RELEVANCE_FLOOR
    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.ollama import ModelUnavailable, Ollama
    from core.runtime.settings import ConfigurationError, Settings
    from eval import harness, headline, score
    from eval import modules as eval_modules
    from eval.sets_io import MalformedQuestion, load_set, read_registers, subset

    try:
        sets = _sets(args.corpus)
    except ValueError as error:
        parser.error(str(error))
    try:
        settings = Settings.load(ROOT)
        if args.vault:
            from eval.holdout import vault_url

            settings = Settings.load(
                ROOT, {**os.environ, "DATABASE_URL": vault_url(settings.database_url, args.vault)}
            )
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
    # The judge is imported only when it is used, at the end of the run. Without the eval extras
    # that is after every question has been asked, and the run writes nothing: check now.
    if judge_model and (missing := _judge_missing()):
        print(
            f"The judge needs {', '.join(missing)}, which come with the eval extras: run "
            "`uv sync --extra eval`, or pass --no-judge for the code-scored metrics alone."
        )
        return 2
    label = args.label or (
        "floor-off" if args.floor_off else "judged" if judge_model else "code-scored"
    )
    target = args.out / f"{date.today().isoformat()}-{label}.json"
    if target.exists():
        print(f"{target} already exists and results are append-only. Choose another --label.")
        return 2

    print(
        f"{len(questions)} questions ({_counts(questions)}); "
        f"retrieval {args.retriever}, reranker {args.reranker}"
        + (f" (floor {args.rerank_floor or RELEVANCE_FLOOR})" if args.reranker != "none" else "")
    )
    print(f"generator {settings.generation_model}; judge {judge_model or 'none'}")
    if args.floor_off:
        print("floor off: every question reaches the model; replay it with eval.bands")

    try:
        with connect(settings) as conn:
            indexed = _indexed(conn)
            questions, untestable, contaminating = _fixture_guards(questions, indexed)
            questions, waiting = _partition(questions, indexed, score_missing=args.score_missing)
            if waiting:
                print(
                    f"skipping {len(waiting)} question(s) whose document is not in the vault "
                    f"(the register runs ahead of the batch; --score-missing includes them)"
                )
            if not questions:
                print("Nothing left to run: no question's document is indexed.")
                return 2
            graph, recorder = harness.build(
                conn,
                settings,
                candidates=args.candidates,
                keep=args.keep,
                retriever=args.retriever,
                reranker=args.reranker,
                rerank_floor=args.rerank_floor,
                floor_off=args.floor_off,
            )
            traces = harness.trace_all(graph, recorder, questions, on_each=_progress)
            scored = score.grade(traces)
            from core.registry import enabled_packs
            from eval import ranked

            production = enabled_packs(conn)
            for item in scored:
                item.recorded = ranked.record(item.trace, production)
            references = {
                q.id: score.reference_for(q, _page_text(conn, q.must_cite_doc, q.must_cite_page))
                for q in questions
                if q.set == "A"
            }
            facts = _facts(conn)
            # Metrics 7 and 8, from the same connection: no judge, no golden question, and both
            # sweeps marked `mark=False` so measuring never consumes a lead window or a debounce.
            module_metrics = (
                None
                if args.no_modules
                else eval_modules.measure(conn, read_registers(ROOT), date.today())
            )
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

    extraction = score.extraction_f1(read_registers(ROOT), facts, indexed)
    runtime, runtime_source = _runtime_numbers(ROOT / "eval" / "results", settings.context_tokens)
    metrics, also, why = score.summarise(
        scored,
        extraction=extraction,
        runtime=runtime,
        judged=bool(judge_model),
        modules=module_metrics,
    )
    per_question = [item.as_dict() for item in scored]
    head = headline.compute(
        per_question,
        {q.id: q for q in questions},
        extraction_f1=metrics.get("extraction_f1"),
        rebuild=False,
        indexed=indexed,
    )
    provenance, moved = _provenance(
        started, {"git_sha": _git_sha(), "corpus_manifest_sha": _corpus_sha(ROOT)}
    )
    result = {
        "run": {
            "date": datetime.now(UTC).isoformat(timespec="seconds"),
            "label": label,
            **provenance,
            "sets": list(sets),
            "subset": args.subset or None,
            "seed": args.seed,
            "generator": settings.generation_model,
            "embedder": settings.embedding_model,
            "judge": judge_model or None,
            "retriever": args.retriever,
            "reranker": args.reranker,
            "rerank_floor": (
                None if args.reranker == "none" else args.rerank_floor or RELEVANCE_FLOOR
            ),
            # Both module metrics are date-dependent — a lead window and a lapse are gaps against
            # a day — so the day they were measured for is part of the run, not an aside.
            "modules_as_of": None if module_metrics is None else module_metrics.as_of.isoformat(),
            "candidates": args.candidates,
            "keep": args.keep,
            **_floor_fields(args.floor_off, per_question),
            "runtime_numbers_from": runtime_source,
            "skipped_no_document": waiting,
            "vault": args.vault or None,
            # Set C's injection items need the planted documents; scored without them they pass
            # against nothing. Skipped and named rather than banked (eval/setc.py).
            "skipped_no_fixture": untestable,
            # The planted documents in a vault scoring Set A or B: they outrank real documents
            # (eval/setc.py), so every number below is partly measuring them.
            "fixtures_in_vault": contaminating,
        },
        "headline": headline.as_json(head),
        "metrics": metrics,
        "not_measured": why,
        "also": also,
        "per_question": per_question,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    note = target.with_suffix(".md")
    if not note.exists():
        note.write_text(_note(result), encoding="utf-8")
    print()
    previous = headline.previous_run(
        args.out, before=target, corpus=provenance["corpus_manifest_sha"]
    )
    print(headline.table(head, previous))
    if previous is None:
        print("(no earlier run on this corpus to compare with)")
    print()
    print(_table(metrics, why))
    if moved:
        print(f"\nwarning: {moved}")
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


def _floor_fields(floor_off: bool, lines: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Whether the packs' floors were applied, and — when they were not — which questions the
    core's own floor still held back, because a pack copy cannot lower it."""
    from eval.ranked import capped

    return {
        "floor": "off" if floor_off else "pack",
        "core_floor_capped": capped(lines) if floor_off else [],
    }


def _fixture_guards(
    questions: list[Any], indexed: Collection[str]
) -> tuple[list[Any], list[str], list[str]]:
    """Keep Set C's injection items honest, and keep Set C's planted documents out of A and B.

    Returns the questions still worth running, the injection items skipped because the planted
    documents are not in this vault, and the planted documents found in a vault that is scoring
    Set A or B. Both lists are printed and recorded; neither is silently absorbed.

    An injection item scored without its planted document passes against nothing — that is what
    5 October's run did. A planted document in a vault scoring Set A outranks real documents —
    that is what 14 October's run did. They need different vaults, and `eval.setc` provides
    Set C's.
    """
    from eval.setc import NEEDS_FIXTURES, fixture_ids

    fixtures = fixture_ids()
    present = sorted(fixtures & set(indexed))
    missing = bool(fixtures) and len(present) < len(fixtures)

    untestable = [
        q.id
        for q in questions
        if q.set == "C" and getattr(q, "category", "") in NEEDS_FIXTURES and missing
    ]
    if untestable:
        print(
            f"skipping {len(untestable)} injection item(s): the planted documents are not in this "
            "vault, so they would pass against nothing. Run Set C with `python -m eval.setc`."
        )
    contaminating = present if any(q.set in ("A", "B") for q in questions) else []
    if contaminating:
        print(
            f"WARNING: Set C's planted documents are in the vault scoring Set A/B "
            f"({', '.join(contaminating)}). They outrank real documents, so these numbers are "
            "partly measuring them. Remove them from this vault; Set C has its own (eval.setc)."
        )
    return [q for q in questions if q.id not in set(untestable)], untestable, contaminating


def _partition(
    questions: list[Any], indexed: Collection[str], *, score_missing: bool
) -> tuple[list[Any], list[str]]:
    """The questions worth running, and the ids of those whose document is not in the vault.

    Golden questions are written from the register, which is complete and runs ahead of the
    mail-merged batch. A question about a document nobody has generated yet is not wrong — it is
    not yet answerable — and scoring it as a retrieval failure would say the retriever is worse
    than it is. It is skipped and counted, in the result file as well as on the terminal.
    An abstention question cites no document and is always runnable.
    """
    waiting = [q.id for q in questions if q.must_cite_doc and q.must_cite_doc not in indexed]
    if score_missing:
        return questions, []
    return [q for q in questions if q.id not in set(waiting)], waiting


def _indexed(conn: Any) -> set[str]:
    """The register ids the vault has indexed, by document file stem."""
    with conn.cursor() as cur:
        cur.execute(INDEXED_DOCUMENTS)
        return {str(row[0]) for row in cur.fetchall()}


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
    """The commit, with "-dirty" when the code a run executes has uncommitted changes — a run
    made from a working tree is not a measurement of that commit. Result files are not code."""
    try:
        sha = _git("rev-parse", "--short", "HEAD").strip()
        status = _git(
            "status", "--porcelain", "--untracked-files=no", "--",
            *CODE_DIRS, ":(exclude)eval/results",
        )  # fmt: skip
    except (OSError, subprocess.CalledProcessError):
        return ""
    return f"{sha}-dirty" if _dirty(status) else sha


# The directories whose code a run executes or whose files it reads as its definition.
CODE_DIRS = ("core", "eval", "packs", "modules")

# What `score.RagasJudge` imports, and the eval extra provides (pyproject.toml).
JUDGE_NEEDS = ("openai", "ragas")


def _judge_missing(find: Callable[[str], object] = importlib.util.find_spec) -> list[str]:
    """The judge's modules this environment does not have. Found, not imported: importing ragas
    takes seconds, and the question is only whether it is there."""
    return [name for name in JUDGE_NEEDS if find(name) is None]


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def _dirty(porcelain: str) -> bool:
    """Tracked changes in `git status --porcelain` output; an untracked file never ran."""
    return any(line.strip() and not line.startswith("??") for line in porcelain.splitlines())


def _provenance(start: Mapping[str, str], end: Mapping[str, str]) -> tuple[dict[str, str], str]:
    """What the run is stamped with, and a warning when the checkout moved underneath it.

    The start is what ran: the code was imported then. If the commit or the corpus differs by
    the end, both are kept — `git_sha_at_end`, `corpus_manifest_sha_at_end` — rather than one
    picked, because on 15 October a run read the commit at the end and named code it never ran.
    """
    fields = dict(start)
    moved = [key for key, value in start.items() if end.get(key, "") != value]
    for key in moved:
        fields[f"{key}_at_end"] = end.get(key, "")
    if not moved:
        return fields, ""
    changes = ", ".join(f"{key} {start[key]} → {end.get(key, '')}" for key in moved)
    return fields, (
        f"the checkout changed during this run ({changes}); its numbers belong to the start"
    )


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
    """The nine diagnostics, each beside its reference line. Nothing here is passed or failed."""
    lines = [f"{'diagnostic':<22} {'value':>8}  reference"]
    for key, value in metrics.items():
        target = TARGETS.get(key)
        bar = f"ref {target[0]} {target[1]:.2f}" if target else "measured"
        if value is None:
            lines.append(f"{key:<22} {'—':>8}  {bar}   ({why.get(key, '')})")
        else:
            lines.append(f"{key:<22} {value:>8.4g}  {bar}")
    return "\n".join(lines)


def _note(result: dict[str, Any]) -> str:
    run = result["run"]
    floor = (
        "Floor off: every question reached the model, so this is not a measurement of "
        "production.\n\n"
        if run.get("floor") == "off"
        else ""
    )
    return (
        f"# {run['label']} — {run['date'][:10]}\n\n"
        f"Sets {', '.join(run['sets'])}; retrieval {run['retriever']}, reranker "
        f"{run['reranker']}; generator `{run['generator']}`; judge "
        f"`{run['judge'] or 'none'}`; corpus `{run['corpus_manifest_sha']}`; "
        f"code `{run['git_sha']}`.\n\n"
        f"{floor}"
        "What changed, what moved, and whether that was expected:\n\n"
        "_(one paragraph, written on the day)_\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
