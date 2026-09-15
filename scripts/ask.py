"""Ask a question of your own documents.

    uv run python scripts/ask.py "when does the car insurance renew?"
    uv run python scripts/ask.py            # interactive, one question per line

Every factual sentence comes back with the document and page it came from. When the documents
do not answer the question, it says so and names what would have — that abstention is the point
of the demonstration, not a failure of it.

Retrieval is Lane B's hybrid search in `core/retrieve/hybrid.py`: dense and full-text, fused
by rank, so an exact policy number is found and a paraphrase still works.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOISY = ("httpx", "docling", "RapidOCR", "huggingface_hub", "filelock")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="*", help="ask one question and exit")
    parser.add_argument("--candidates", type=int, default=40)
    parser.add_argument("--keep", type=int, default=6)
    parser.add_argument("--show-evidence", action="store_true", help="print the passages read")
    args = parser.parse_args(argv)
    if args.candidates < 1 or not 1 <= args.keep <= args.candidates:
        parser.error("keep must be between 1 and candidates")

    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.WARNING, format="%(message)s")
    for name in NOISY:
        logging.getLogger(name).setLevel(logging.ERROR)

    from core.advice_consent import HouseholdConsents
    from core.advice_records import HouseholdAdviceLog
    from core.graph.answer import AnswerGraph
    from core.graph.baseline import NoReranker
    from core.graph.inventory import HouseholdInventory
    from core.graph.scope import HouseholdScope
    from core.registry import enabled_pack_ids, enabled_packs
    from core.retrieve.hybrid import HybridRetriever
    from core.runtime.db import DatabaseUnavailable, connect
    from core.runtime.ollama import Ollama
    from core.runtime.settings import ConfigurationError, Settings
    from modules.advice import ModuleAdviser

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    try:
        with connect(settings) as conn:
            client = Ollama(settings)
            enabled = enabled_pack_ids(conn)
            graph = AnswerGraph(
                client,
                # `None` means the registry is empty, which is "do not filter". An *empty* set
                # means a person has switched every pack off, which is a different thing.
                HybridRetriever(conn, client, None if enabled is None else tuple(sorted(enabled))),
                NoReranker(),
                candidates=args.candidates,
                keep=args.keep,
                household=HouseholdScope(conn),
                inventory=HouseholdInventory(conn),
                packs=enabled_packs(conn),
                # ADR 0016. Calculators are modules, so they are injected here rather than
                # imported by `core/`; consent is read and every advice answer recorded through
                # the same connection.
                adviser=ModuleAdviser(conn),
                consents=HouseholdConsents(conn),
                advice_log=HouseholdAdviceLog(conn),
            )
            if args.question:
                _ask(graph, " ".join(args.question), args.show_evidence)
                # The advice record is written but never committed by its writer: the answer that
                # produced it is the transaction, and it is over.
                conn.commit()
                return 0
            print("Ask about your documents. Ctrl+C or an empty line to stop.\n")
            # The conversation so far, so a follow-up ("when does it expire?") is understood.
            history: list[tuple[str, str]] = []
            while True:
                try:
                    question = input("> ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    return 0
                if not question:
                    return 0
                said = _ask(graph, question, args.show_evidence, history)
                conn.commit()  # each question's advice record is its own transaction
                history += [("user", question), ("assistant", said)]
    except DatabaseUnavailable as error:
        print(str(error))
        return 2


def _ask(
    graph: object,
    question: str,
    show_evidence: bool,
    history: list[tuple[str, str]] | None = None,
) -> str:
    answer = graph.ask(question, history=history or [])  # type: ignore[attr-defined]
    print()
    print(answer.text)
    if getattr(answer, "offer", ""):
        print(f"\nYou could ask: {answer.offer}")
    if answer.citations:
        print("\nSources: " + "; ".join(answer.citations))
    if answer.disclaimer:
        print(f"\n{answer.disclaimer}")
    if show_evidence or answer.dropped:
        detail = f"{answer.passages_read} passage(s) read"
        if answer.dropped:
            detail += f", {answer.dropped} sentence(s) dropped by the grounding gate"
        print(f"\n({detail})")
    print()
    return str(answer.text)


if __name__ == "__main__":
    raise SystemExit(main())
