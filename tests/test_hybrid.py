"""Hybrid retrieval: the parts that need no database, and one live check when there is one.

The SQL is hand-written, so what a test can prove without Postgres is what it is *asked*: the
parameters, and what the retriever does with the rows that come back — which passage is lifted
over the floor and which is left where cosine put it. The live test proves the task line itself
against the six documents in a vault, and is skipped where there is no vault to ask.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest

from core.retrieve.hybrid import (
    HYBRID_SEARCH,
    IDENTIFIER_HIT,
    HybridRetriever,
    hybrid_score,
    identifiers,
    prints,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("question", "expected"),
    [
        ("MV-2026-448120", ["MV-2026-448120"]),
        ("what is the premium on policy HM-2024-559013?", ["HM-2024-559013"]),
        ("is SLK 8842 D covered for windscreen", ["SLK 8842 D"]),
        ("is slk8842d covered", ["slk8842d"]),
        ("claim 20260312-7 status", ["20260312-7"]),
        ("when does it expire in 2027", []),  # a year is a date, not a thing
        ("my car cover", []),
        ("the 30-year term plan", []),
        ("blk 45B tampines ave 8", []),
    ],
)
def test_identifiers_are_the_printed_things_in_a_question(
    question: str, expected: list[str]
) -> None:
    assert identifiers(question) == expected


def test_a_chunk_prints_an_identifier_however_it_is_spaced() -> None:
    chunk = "Vehicle Registration Number: SLK 8842 D\nPolicy Number: MV-2026-448120"
    assert prints(chunk, "SLK8842D")
    assert prints(chunk, "slk 8842 d")
    assert prints(chunk, "MV-2026-448120")
    assert not prints(chunk, "MV-2026-448121")


def test_an_exact_hit_is_lifted_to_the_floor_and_nothing_is_lowered() -> None:
    assert hybrid_score(0.38, exact=True) == IDENTIFIER_HIT
    assert hybrid_score(0.97, exact=True) == 0.97
    assert hybrid_score(0.38, exact=False) == 0.38


class FakeCursor:
    def __init__(self, rows: list[tuple[Any, ...]]) -> None:
        self.rows = rows
        self.executed: list[tuple[str, dict[str, Any]]] = []

    def execute(self, sql: str, params: dict[str, Any]) -> None:
        self.executed.append((sql, params))

    def fetchall(self) -> list[tuple[Any, ...]]:
        return self.rows

    def __enter__(self) -> FakeCursor:
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeConn:
    def __init__(self, rows: list[tuple[Any, ...]]) -> None:
        self.cur = FakeCursor(rows)

    def cursor(self) -> FakeCursor:
        return self.cur


class FakeOllama:
    def embed_query(self, text: str) -> list[float]:
        return [0.5, 0.25]


def _row(
    chunk_id: int, text: str, similarity: float, dense: int | None, lexical: int | None
) -> tuple[Any, ...]:
    rrf = (1 / (60 + dense) if dense else 0) + (1 / (60 + lexical) if lexical else 0)
    return (
        chunk_id,
        "uuid",
        1,
        text,
        "",
        "b1-0001.pdf",
        "insurance_agent",
        similarity,
        dense,
        lexical,
        rrf,
    )


def test_the_query_is_asked_once_with_both_arms_and_the_pack_filter() -> None:
    conn = FakeConn([])
    HybridRetriever(conn, FakeOllama(), ("insurance_agent",)).search(
        "MV-2026-448120", candidates=40
    )
    ((sql, params),) = conn.cur.executed
    assert sql is HYBRID_SEARCH
    assert params == {
        "query": "[0.500000,0.250000]",
        "terms": "MV-2026-448120",
        "limit": 40,
        "packs": ["insurance_agent"],
        "k": 60,
    }
    assert "websearch_to_tsquery" in sql and "<=>" in sql and "FULL OUTER JOIN" in sql
    assert "%(packs)s::text[] IS NULL" in sql  # a disabled pack stays invisible


def test_only_the_chunk_that_prints_the_number_is_lifted() -> None:
    rows = [
        _row(1, "Policy Number: MV-2026-448120", 0.41, 2, 1),  # both arms; prints it
        _row(2, "Insured Vehicle: SLK 8842 D", 0.44, 1, None),  # dense only; does not
        _row(3, "Policy Number: PH-2022-604188", 0.30, None, 2),  # lexical only; another number
    ]
    found = HybridRetriever(FakeConn(rows), FakeOllama()).search("MV-2026-448120", candidates=3)
    assert [(p.chunk_id, round(p.score, 2)) for p in found] == [(1, 0.95), (2, 0.44), (3, 0.30)]
    assert found[0].pack_id == "insurance_agent" and found[0].document_name == "b1-0001.pdf"


def test_a_paraphrase_keeps_every_score_where_cosine_put_it() -> None:
    rows = [_row(1, "Private Car Insurance Policy", 0.35, 1, 1), _row(2, "…", 0.33, 2, None)]
    found = HybridRetriever(FakeConn(rows), FakeOllama()).search("my car cover", candidates=2)
    assert [round(p.score, 2) for p in found] == [0.35, 0.33]


# ------------------------------------------------------------------------------- live


LIVE = os.environ.get("PARROT_LIVE_TESTS") == "1"


@pytest.mark.skipif(not LIVE, reason="set PARROT_LIVE_TESTS=1 with the vault and Ollama running")
def test_the_exact_policy_number_is_found_and_the_paraphrase_still_is() -> None:
    """The task line: `MV-2026-448120` finds the motor policy and `my car cover` still does."""
    from core.runtime.db import connect
    from core.runtime.ollama import Ollama
    from core.runtime.settings import Settings

    settings = Settings.load(ROOT)
    with connect(settings) as conn:
        retriever = HybridRetriever(conn, Ollama(settings))
        exact = retriever.search("MV-2026-448120", candidates=10)
        assert exact and exact[0].document_name == "b1-0001.pdf"
        assert exact[0].score >= IDENTIFIER_HIT
        near_miss = retriever.search("MV-2026-448121", candidates=10)
        assert all(p.score < IDENTIFIER_HIT for p in near_miss)
        paraphrase = retriever.search("my car cover", candidates=10)
        assert any(p.document_name == "b1-0001.pdf" for p in paraphrase)
