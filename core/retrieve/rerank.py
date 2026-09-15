"""The cross-encoder reranker: forty candidates read against the question, six kept.

A retriever compares two vectors; a cross-encoder reads the question and the passage together
and says how well the one answers the other. That is why it goes last and why it is worth its
cost: it is the only stage that has actually read the passage (ADR 0013). `bge-reranker-v2-m3`
runs in-process with `transformers`, because Ollama cannot serve a cross-encoder (ADR 0017).

What it does not do is change `Passage.score`. The graph's abstain floor reads a cosine
similarity and this keeps returning one; the reranker decides the order and the cut, not whether
the evidence was close enough. Moving the floor onto reranker scores changes every pack's
`abstain_below` at once and is its own change, to be made with the golden set in hand
(ADR 0014, table).

The model is loaded once per process, on the first question, onto whatever `torch` finds:
CUDA, then Apple's MPS, then the CPU. The API builds a graph per request, so the load must not
be per graph.
"""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass
from typing import Any

from core.graph.ports import Passage
from core.runtime.ollama import ModelUnavailable

log = logging.getLogger(__name__)

DEFAULT_MODEL = "BAAI/bge-reranker-v2-m3"
MAX_LENGTH = 512  # tokens per question+passage pair; a chunk is well under this
BATCH = 16

_lock = threading.Lock()
_loaded: dict[str, tuple[Any, Any, str]] = {}  # model id -> (tokenizer, model, device)


def device_name() -> str:
    import torch

    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load(model_name: str) -> tuple[Any, Any, str]:
    """The tokenizer, the model and the device it sits on, loaded once per process.

    `local_files_only` after the first attempt would hide a half-downloaded cache; instead the
    Hugging Face client is left to resolve, and a machine with no weights and no network gets a
    `ModelUnavailable` that names the record explaining where the weights come from.
    """
    with _lock:
        if model_name in _loaded:
            return _loaded[model_name]
        try:
            import torch
            from transformers import AutoModelForSequenceClassification, AutoTokenizer

            device = device_name()
            dtype = torch.float16 if device != "cpu" else torch.float32
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name, dtype=dtype)
            model = model.to(device).eval()
        except Exception as error:  # a missing cache, no network, a bad id: one message
            raise ModelUnavailable(
                f"the reranker {model_name} could not be loaded ({error}). It runs in-process "
                "from the Hugging Face cache; see docs/adr/0017."
            ) from error
        log.info("reranker %s loaded on %s", model_name, device)
        _loaded[model_name] = (tokenizer, model, device)
        return _loaded[model_name]


def score_pairs(model_name: str, question: str, texts: list[str]) -> list[float]:
    """One relevance logit per text, higher is better. Batched so forty passages is a handful of
    forward passes rather than forty."""
    if not texts:
        return []
    import torch

    tokenizer, model, device = load(model_name)
    scores: list[float] = []
    with torch.no_grad():
        for start in range(0, len(texts), BATCH):
            batch = texts[start : start + BATCH]
            encoded = tokenizer(
                [question] * len(batch),
                batch,
                padding=True,
                truncation=True,
                max_length=MAX_LENGTH,
                return_tensors="pt",
            ).to(device)
            logits = model(**encoded).logits.view(-1).float().cpu()
            scores.extend(float(value) for value in logits.tolist())
    return scores


def passage_text(passage: Passage) -> str:
    """What the reranker reads: the one-line context, when a chunk carries one, then the chunk."""
    return f"{passage.context_prefix}\n{passage.text}" if passage.context_prefix else passage.text


@dataclass(frozen=True, slots=True)
class CrossEncoderReranker:
    """Implements `core.graph.ports.Reranker`. Reorders by the cross-encoder's score and keeps
    `keep`; every passage comes back with the score retrieval gave it."""

    model_name: str = DEFAULT_MODEL

    def rerank(self, question: str, passages: list[Passage], *, keep: int) -> list[Passage]:
        if keep <= 0 or not passages:
            return []
        if len(passages) == 1:
            return list(passages)
        scores = score_pairs(self.model_name, question, [passage_text(p) for p in passages])
        order = sorted(range(len(passages)), key=lambda i: (-scores[i], i))
        return [passages[i] for i in order[:keep]]
