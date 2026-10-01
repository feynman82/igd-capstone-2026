"""The cross-encoder reranker: forty candidates read against the question, six kept.

A retriever compares two vectors; a cross-encoder reads the question and the passage together
and says how well the one answers the other. That is why it goes last and why it is worth its
cost: it is the only stage that has actually read the passage (ADR 0013). `bge-reranker-v2-m3`
runs in-process with `transformers`, because Ollama cannot serve a cross-encoder (ADR 0018).

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
import math
import threading
from dataclasses import dataclass
from typing import Any

from core.graph.ports import Passage
from core.runtime.ollama import ModelUnavailable

log = logging.getLogger(__name__)

DEFAULT_MODEL = "BAAI/bge-reranker-v2-m3"
# Tokens per question+passage pair. The model itself takes 8192; the cap exists to bound the
# cost of forty pairs, not for the model's sake. Measured on this corpus on 29 September: every
# chunk is under 300 tokens, padding is dynamic, and 512 against 1024 made no difference at all
# (0.27s for forty either way) because the batch is padded to its longest member, not to the cap.
# A cap only costs something when a passage actually reaches it, and then it is buying silence:
# the reranker would score the first half of a dense policy page and never see the table at the
# end. 1024 is three times the largest chunk the corpus has produced, and `score_pairs` says so
# out loud when anything reaches it.
MAX_LENGTH = 1024
BATCH = 16

# The relevance a passage must reach to be worth reading, as a probability rather than a logit.
#
# Zero: off. The mechanism stays because the knob and the measurement are worth having, but the
# experiment it was built for failed. Measured on the full golden sets on 30 September, hybrid
# retrieval and this reranker, one variable:
#
#     floor    abstention (B)   faithfulness   recall   answered (A)   abstention precision
#     0.0            0.52          0.967        0.897       0.974              0.929
#     0.002          0.56          0.936        0.872       0.897              0.778
#     0.02           0.64          0.809        0.821       0.872              0.762
#
# Every setting is a bad trade. Even 0.002 — below Set B's tenth percentile, which should have
# been a pure junk filter — buys one hard negative and costs two answerable questions. The reason
# is not calibration: the hard negatives that get answered are the ones where a genuinely relevant
# page exists, and a cross-encoder is built to score those highly. See ADR 0019.
RELEVANCE_FLOOR = 0.0

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
                "from the Hugging Face cache; see docs/adr/0018."
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
    truncated = 0
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
            truncated += int((encoded["attention_mask"].sum(dim=1) >= MAX_LENGTH).sum())
            logits = model(**encoded).logits.view(-1).float().cpu()
            scores.extend(float(value) for value in logits.tolist())
    if truncated:
        _warn_once(truncated, len(texts))
    return scores


_warned = False


def _warn_once(truncated: int, total: int) -> None:
    """Say it, once per process. A passage cut at the cap is scored on its first part only, and
    the end of a schedule is where the table is — so this is the shape a quiet recall loss takes,
    and it should never be discovered by bisecting an evaluation run."""
    global _warned
    if _warned:
        return
    _warned = True
    log.warning(
        "reranker: %d of %d passages reached the %d-token limit and were scored on their first "
        "part only. Raise MAX_LENGTH in core/retrieve/rerank.py or chunk smaller; the model "
        "itself takes 8192.",
        truncated,
        total,
        MAX_LENGTH,
    )


def passage_text(passage: Passage) -> str:
    """What the reranker reads: the one-line context, when a chunk carries one, then the chunk."""
    return f"{passage.context_prefix}\n{passage.text}" if passage.context_prefix else passage.text


def relevance(logit: float) -> float:
    """The cross-encoder's score as a probability. The model emits a logit; a floor is easier to
    argue about, and to write in a record, on a 0-to-1 scale."""
    return 1.0 / (1.0 + math.exp(-logit))


@dataclass(frozen=True, slots=True)
class CrossEncoderReranker:
    """Implements `core.graph.ports.Reranker`. Reorders by the cross-encoder's score, drops what
    is not relevant at all, and keeps `keep`. Every passage comes back with the score retrieval
    gave it — `Passage.score` stays a cosine similarity, because the graph's own floor reads one.

    `floor` is off by default. It exists because dropping passages is how the cross-encoder's
    opinion *could* reach the abstention decision — `gate.precheck` abstains on an empty list, so
    no port or contract has to change for it to be heard — and because measuring that needed a
    knob. It was measured, and at every setting it trades more answerable questions than hard
    negatives; the numbers and the reason are above and in ADR 0019. Kept so the next attempt
    starts from an apparatus rather than from scratch.
    """

    model_name: str = DEFAULT_MODEL
    floor: float = RELEVANCE_FLOOR

    def rerank(self, question: str, passages: list[Passage], *, keep: int) -> list[Passage]:
        if keep <= 0 or not passages:
            return []
        scores = score_pairs(self.model_name, question, [passage_text(p) for p in passages])
        order = sorted(range(len(passages)), key=lambda i: (-scores[i], i))
        kept = [i for i in order if relevance(scores[i]) >= self.floor]
        if len(kept) < len(order):
            log.info(
                "reranker: %d of %d passages below the %.3f relevance floor",
                len(order) - len(kept),
                len(order),
                self.floor,
            )
        return [passages[i] for i in kept[:keep]]
