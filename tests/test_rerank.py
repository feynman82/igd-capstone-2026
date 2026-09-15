"""The cross-encoder reranker: what it does with scores, and that the scores are real."""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import pytest

from core.graph.ports import Passage
from core.retrieve import rerank
from core.retrieve.rerank import CrossEncoderReranker, passage_text
from core.runtime.settings import ConfigurationError, Settings

ROOT = Path(__file__).resolve().parents[1]


def _passage(chunk_id: int, text: str, score: float, prefix: str = "") -> Passage:
    return Passage(
        chunk_id, "uuid", 1, text, score, document_name="b1-0001.pdf", context_prefix=prefix
    )


@pytest.fixture
def scored(monkeypatch: pytest.MonkeyPatch) -> Iterator[list[tuple[str, list[str]]]]:
    """A scorer that ranks by the number the passage text ends with, and records what it was
    asked. The model is not loaded; that is the live test's job."""
    calls: list[tuple[str, list[str]]] = []

    def fake(model_name: str, question: str, texts: list[str]) -> list[float]:
        calls.append((question, texts))
        return [float(text.rsplit(" ", 1)[-1]) for text in texts]

    monkeypatch.setattr(rerank, "score_pairs", fake)
    yield calls


def test_reorders_by_the_cross_encoder_and_keeps_retrievals_score(
    scored: list[tuple[str, list[str]]],
) -> None:
    passages = [
        _passage(1, "weak match 0.2", 0.95),  # retrieval loved it; the reader does not
        _passage(2, "the answer 0.9", 0.41),
        _passage(3, "nearby 0.5", 0.44),
        _passage(4, "noise 0.1", 0.43),
    ]
    kept = CrossEncoderReranker("any").rerank("q", passages, keep=2)
    assert [p.chunk_id for p in kept] == [2, 3]
    assert [p.score for p in kept] == [0.41, 0.44]  # untouched: the floor still reads cosine
    assert scored == [("q", ["weak match 0.2", "the answer 0.9", "nearby 0.5", "noise 0.1"])]


def test_ties_keep_retrievals_order_and_edges_cost_no_model_call(
    scored: list[tuple[str, list[str]]],
) -> None:
    passages = [_passage(1, "a 0.5", 0.5), _passage(2, "b 0.5", 0.6)]
    assert [p.chunk_id for p in CrossEncoderReranker("any").rerank("q", passages, keep=5)] == [1, 2]
    assert CrossEncoderReranker("any").rerank("q", [], keep=6) == []
    assert CrossEncoderReranker("any").rerank("q", passages, keep=0) == []
    only = [_passage(9, "solo 0.1", 0.3)]
    assert CrossEncoderReranker("any").rerank("q", only, keep=6) == only
    assert len(scored) == 1  # the one real rerank; not the empty, zero or single cases


def test_the_reader_sees_the_context_prefix_before_the_chunk() -> None:
    assert passage_text(_passage(1, "Excess: SGD 750.00", 0.5)) == "Excess: SGD 750.00"
    assert (
        passage_text(_passage(1, "Excess: SGD 750.00", 0.5, prefix="motor schedule, 2026"))
        == "motor schedule, 2026\nExcess: SGD 750.00"
    )


def test_an_ollama_tag_for_the_reranker_is_refused_with_the_reason(tmp_path: Path) -> None:
    settings = Settings.load(tmp_path, {})
    assert settings.rerank_model == "BAAI/bge-reranker-v2-m3"
    with pytest.raises(ConfigurationError, match=r"adr/0017"):
        Settings.load(tmp_path, {"PARROT_RERANK_MODEL": "hf.co/gpustack/bge-reranker-v2-m3-GGUF"})


LIVE = os.environ.get("PARROT_LIVE_TESTS") == "1"


@pytest.mark.skipif(not LIVE, reason="set PARROT_LIVE_TESTS=1 with the weights in the HF cache")
def test_the_real_model_puts_the_answering_passage_first() -> None:
    passages = [
        _passage(1, "Policy Number: MV-2026-448121 Vehicle Model: Seven-seat MPV", 0.5),
        _passage(2, "Death Benefit: Upon the death of the Life Assured while in force", 0.5),
        _passage(
            3, "Period of Insurance From: 12 April 2026 Period of Insurance To: 11 April 2027", 0.4
        ),
    ]
    kept = CrossEncoderReranker().rerank("when does the car policy expire", passages, keep=1)
    assert [p.chunk_id for p in kept] == [3]
