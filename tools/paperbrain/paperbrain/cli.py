"""PaperBrain command line.

pb init                       one-time setup, checks Ollama
pb add ~/Documents/Paperwork  register a folder in the library
pb ingest [path ...]          extract + chunk + embed (idempotent)
pb search "water damage"      show matching excerpts, no model needed
pb ask "when is my policy due"  retrieval-augmented answer with citations
pb docs                       list what's in the library
pb stats / pb doctor          health checks
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .ask import answer, format_sources
from .config import CONFIG_PATH, Config
from .db import connect, stats
from .ingest import discover, embed_chunks, ingest_file
from .ollama import Ollama, OllamaUnavailable
from .retrieve import search

BOLD, DIM, RESET = "\033[1m", "\033[2m", "\033[0m"


def _client(cfg: Config) -> Ollama:
    return Ollama(cfg.ollama_host)


# --- commands -------------------------------------------------------------


def cmd_init(args, cfg: Config) -> int:
    cfg.save()
    print(f"{BOLD}PaperBrain {__version__}{RESET}")
    print(f"  config   {CONFIG_PATH}")
    print(f"  database {cfg.db_path}")
    connect(cfg.db_path).close()
    return cmd_doctor(args, cfg)


def cmd_doctor(args, cfg: Config) -> int:
    ok = True
    try:
        installed = _client(cfg).models()
        print(f"  ollama   reachable at {cfg.ollama_host}")
        for label, model in (("embed", cfg.embed_model), ("chat", cfg.chat_model)):
            have = any(m.split(":")[0] == model.split(":")[0] for m in installed)
            mark = "ok" if have else "MISSING"
            print(f"  {label:8} {model} [{mark}]")
            if not have:
                print(f"           -> ollama pull {model}")
                ok = False
    except OllamaUnavailable as exc:
        print(f"  ollama   {exc}")
        ok = False

    try:
        import pypdf  # noqa: F401

        print("  pypdf    ok")
    except ImportError:
        print("  pypdf    MISSING -> pip install pypdf")
        ok = False
    try:
        import pytesseract  # noqa: F401

        print("  ocr      ok (pytesseract)")
    except ImportError:
        print(f"  ocr      {DIM}not installed — scanned PDFs and photos will be skipped{RESET}")
    return 0 if ok else 1


def cmd_add(args, cfg: Config) -> int:
    for raw in args.paths:
        path = str(Path(raw).expanduser().resolve())
        if path not in cfg.library:
            cfg.library.append(path)
            print(f"  added to library: {path}")
        else:
            print(f"  already in library: {path}")
    cfg.save()
    return 0


def cmd_ingest(args, cfg: Config) -> int:
    roots = args.paths or cfg.library
    if not roots:
        print("Nothing to ingest. Add a folder first:  pb add ~/Documents/Paperwork")
        return 1

    files = discover(roots)
    if not files:
        print("No supported files found under:", ", ".join(roots))
        return 1

    conn = connect(cfg.db_path)
    counts: dict[str, int] = {}
    print(f"{BOLD}Ingesting {len(files)} file(s){RESET}")
    for i, path in enumerate(files, start=1):
        result = ingest_file(conn, cfg, path)
        counts[result.status] = counts.get(result.status, 0) + 1
        if result.status in ("added", "updated"):
            print(f"  [{i}/{len(files)}] {result.status:8} {path.name} ({result.chunks} chunks)")
        elif result.status in ("error", "empty"):
            print(f"  [{i}/{len(files)}] {result.status:8} {path.name} — {result.note}")
        if result.note and result.status in ("added", "updated"):
            print(f"           {DIM}{result.note}{RESET}")

    summary = "  ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    print(f"{BOLD}Files:{RESET} {summary}")

    if not args.no_embed:
        try:
            print("Embedding new chunks...")
            n = embed_chunks(conn, _client(cfg), cfg.embed_model)
            print(f"  embedded {n} chunk(s)")
        except OllamaUnavailable as exc:
            print(f"  {exc}")
            print("  Text is stored; run `pb ingest` again once Ollama is up.")
    conn.close()
    return 0


def cmd_search(args, cfg: Config) -> int:
    conn = connect(cfg.db_path)
    hits = search(conn, _client(cfg), cfg, args.query, args.k)
    if not hits:
        print("No matches.")
        return 1
    for i, hit in enumerate(hits, start=1):
        page = f" p.{hit.page}" if hit.page else ""
        print(f"{BOLD}[{i}] {hit.filename}{page}{RESET}  {DIM}{hit.score:.4f}{RESET}")
        snippet = hit.text.strip().replace("\n", " ")
        print(f"    {snippet[:280]}{'...' if len(snippet) > 280 else ''}\n")
    conn.close()
    return 0


def cmd_ask(args, cfg: Config) -> int:
    conn = connect(cfg.db_path)
    client = _client(cfg)
    try:
        hits = search(conn, client, cfg, args.question, args.k)
        text = answer(client, cfg.chat_model, args.question, hits)
    except OllamaUnavailable as exc:
        print(exc)
        return 1
    print(f"\n{text}\n")
    if hits:
        print(f"{DIM}Sources:{RESET}")
        print(format_sources(hits))
    conn.close()
    return 0


def cmd_docs(args, cfg: Config) -> int:
    conn = connect(cfg.db_path)
    rows = conn.execute(
        """
        SELECT d.filename, d.doc_type, d.doc_date, d.ocr_used,
               COUNT(c.id) AS chunks
        FROM documents d LEFT JOIN chunks c ON c.document_id = d.id
        GROUP BY d.id
        ORDER BY (d.doc_date IS NULL), d.doc_date DESC, d.filename
        """
    ).fetchall()
    if not rows:
        print("Library is empty. Try:  pb add ~/Documents/Paperwork && pb ingest")
        return 1
    print(f"{BOLD}{'date':<12}{'type':<12}{'chunks':<8}file{RESET}")
    for r in rows:
        ocr = " (ocr)" if r["ocr_used"] else ""
        print(
            f"{(r['doc_date'] or '—'):<12}{(r['doc_type'] or '—'):<12}"
            f"{r['chunks']:<8}{r['filename']}{ocr}"
        )
    conn.close()
    return 0


def cmd_stats(args, cfg: Config) -> int:
    conn = connect(cfg.db_path)
    for key, value in stats(conn).items():
        print(f"  {key:<16}{value}")
    print(f"  {'library':<16}{len(cfg.library)} folder(s)")
    for folder in cfg.library:
        print(f"    {folder}")
    conn.close()
    return 0


# --- entry point ----------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pb", description="PaperBrain — local paperwork brain")
    p.add_argument("--version", action="version", version=f"PaperBrain {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="set up config and database").set_defaults(fn=cmd_init)
    sub.add_parser("doctor", help="check Ollama and dependencies").set_defaults(fn=cmd_doctor)
    sub.add_parser("stats", help="database statistics").set_defaults(fn=cmd_stats)
    sub.add_parser("docs", help="list ingested documents").set_defaults(fn=cmd_docs)

    a = sub.add_parser("add", help="add a folder or file to the library")
    a.add_argument("paths", nargs="+")
    a.set_defaults(fn=cmd_add)

    g = sub.add_parser("ingest", help="index the library (or specific paths)")
    g.add_argument("paths", nargs="*")
    g.add_argument("--no-embed", action="store_true", help="extract only, skip embeddings")
    g.set_defaults(fn=cmd_ingest)

    s = sub.add_parser("search", help="hybrid keyword+vector search, no LLM")
    s.add_argument("query")
    s.add_argument("-k", type=int, default=None, help="number of excerpts")
    s.set_defaults(fn=cmd_search)

    q = sub.add_parser("ask", help="answer a question with citations")
    q.add_argument("question")
    q.add_argument("-k", type=int, default=None, help="number of excerpts")
    q.set_defaults(fn=cmd_ask)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cfg = Config.load()
    try:
        return args.fn(args, cfg)
    except KeyboardInterrupt:
        print("\ninterrupted")
        return 130


if __name__ == "__main__":
    sys.exit(main())
