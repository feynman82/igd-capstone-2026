"""Traces into the nine numbers `eval/README.md` names.

Two kinds of metric live here and it matters which is which. The code-scored ones — abstention
rate, extraction F1, the citation checks — compare an answer against the register and need no
model, so they are exact and they run in a test. The judge-scored ones — context recall and
precision, faithfulness, answer relevancy — are Ragas asking a local model to read the evidence,
and they are only as good as that judge. The result file says which judge, so a number can be
compared with the run before it and not with a run under a different reader.
"""

from __future__ import annotations

import asyncio
import logging
import re
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any, Protocol

from core.graph.answer import Answer
from core.graph.ports import Passage
from eval.harness import Trace
from eval.sets_io import Question

log = logging.getLogger(__name__)

# Register columns that describe the row rather than a value printed on the document.
REGISTER_META = frozenset(
    {"doc_id", "doc_type", "pack_id", "issued_date", "subject", "tier", "field_pages", "notes"}
)

METRIC_KEYS = (
    "context_recall",
    "context_precision",
    "faithfulness",
    "answer_relevancy",
    "abstention_rate",
    "extraction_f1",
    "obligation_precision",
    "alert_fpr",
    "decode_tok_s",
    "peak_vram_gb",
)
JUDGED = ("context_recall", "context_precision", "faithfulness", "answer_relevancy")


# ------------------------------------------------------------------------------- what counts


def held_back(answer: Answer) -> bool:
    """Did the system decline to answer? Abstaining, declining advice, withholding it, asking
    for consent, refusing, and saying only what is on file all count: none of them is a claim
    about the question that the documents did not support."""
    return not answer.grounded or answer.unanswered


def refused(answer: Answer) -> bool:
    return answer.refused or answer.declined


NOT_ON_FILE = re.compile(
    r"\b(none|not|no|never)\b[^.]{0,60}\b(listed|stated|specified|provided|itemi[sz]ed|"
    r"mentioned|printed|contain|contains|include|includes|on file|in the (provided )?documents?)\b",
    re.IGNORECASE,
)
# The inventory's own line naming a document on file ("On file for Marcus Lim: …") is neither a
# claim about the question nor a decline; it is skipped when deciding what an answer said.
ON_FILE_LINE = re.compile(r"^On file for ", re.IGNORECASE)


def says_not_on_file(answer: Answer) -> bool:
    """A grounded answer whose sentences say, in words, that the documents do not state it.

    That is an honest decline written by the model rather than by the gate — "the chassis
    number is not listed in the provided documents" — and it is reported beside the strict
    abstention rate rather than folded into it, so the two can be argued about separately.
    """
    if held_back(answer):
        return False
    sentences = [claim.text for claim in answer.claims] or [answer.text]
    said = [s for s in sentences if s.strip() and not ON_FILE_LINE.match(s.strip())]
    return bool(said) and all(NOT_ON_FILE.search(sentence) for sentence in said)


# ------------------------------------------------------------------------------- value matching


def value_forms(value: str) -> set[str]:
    """The ways a register value is printed. `2027-04-11` appears on a schedule as
    "11 April 2027" and in an answer as "11 Apr 2027" or "2027-04-11"; `1284.00` as "1,284.00"
    or "1284". Matching any of them is the point; a person reading the answer would accept all."""
    text = value.strip()
    forms = {text.casefold()}
    when = _as_date(text)
    if when is not None:
        forms |= {
            when.isoformat(),
            f"{when.day} {when:%B %Y}".casefold(),
            f"{when:%d %B %Y}".casefold(),  # "01 March 2026", as the schedules print it
            f"{when.day} {when:%b %Y}".casefold(),
            f"{when:%d %b %Y}".casefold(),
            f"{when:%d/%m/%Y}",
            f"{when.day}/{when.month}/{when.year}",
        }
        return forms
    number = _as_number(text)
    if number is not None:
        whole = number == number.to_integral_value()
        forms |= {f"{number:,.2f}", f"{number:.2f}", f"{number:,}", f"{number}"}
        if whole:
            forms |= {f"{int(number):,}", f"{int(number)}"}
    return forms


def mentions(text: str, value: str) -> bool:
    """Whether an answer states a value, in any of the forms the value is printed."""
    haystack = " ".join(text.split()).casefold()
    return any(_contains(haystack, form) for form in value_forms(value) if form)


def _contains(haystack: str, needle: str) -> bool:
    if needle[0].isdigit() or needle[0] == "-":
        # A number must stand alone: "1284" is not found in "12840" or "1284.50", but a full
        # stop after it is just the end of the sentence.
        pattern = rf"(?<!\d)(?<!\d\.){re.escape(needle)}(?!\d|\.\d)"
        return re.search(pattern, haystack) is not None
    return needle in haystack


def _as_date(text: str) -> date | None:
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def _as_number(text: str) -> Decimal | None:
    cleaned = text.replace(",", "").replace("$", "").strip()
    if not re.fullmatch(r"-?\d+(\.\d+)?", cleaned):
        return None
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def same_value(register: str, fact: str | None) -> bool:
    """The register's text against an extracted value, each normalised the way the pack's
    schema would print it. A date is a date, a number is a number to two places, and a string
    is compared without regard to case or spacing."""
    if fact is None or not register.strip():
        return False
    left, right = register.strip(), fact.strip()
    dates = _as_date(left), _as_date(right)
    if dates[0] is not None or dates[1] is not None:
        return dates[0] == dates[1]
    numbers = _as_number(left), _as_number(right)
    if numbers[0] is not None or numbers[1] is not None:
        return numbers[0] == numbers[1]
    return " ".join(left.split()).casefold() == " ".join(right.split()).casefold()


# ------------------------------------------------------------------------------- code-scored


def doc_stem(document_name: str) -> str:
    """`b1-0001.pdf` is register row `b1-0001`. The register's id is the file name's stem."""
    name = document_name.rsplit("/", 1)[-1]
    return name.rsplit(".", 1)[0] if "." in name else name


def cites(answer: Answer, doc_id: str, page: int) -> bool:
    """Whether any sentence of the answer is cited to the document and page the question named."""
    return any(
        doc_stem(citation.document_name) == doc_id and citation.page == page
        for claim in answer.claims
        for citation in claim.citations
    )


def shown(contexts: Iterable[Passage], doc_id: str, page: int) -> bool:
    """Whether the page the answer should come from was among the passages the model read."""
    return any(doc_stem(p.document_name) == doc_id and p.page == page for p in contexts)


@dataclass(frozen=True, slots=True)
class FactRow:
    """One row of the `facts` table, as the harness reads it: which document, which field, and
    the value in whichever column the extractor typed it into."""

    doc_id: str
    key: str
    value: str | None


@dataclass(frozen=True, slots=True)
class F1:
    tp: int
    fp: int
    fn: int

    @property
    def precision(self) -> float | None:
        return None if self.tp + self.fp == 0 else self.tp / (self.tp + self.fp)

    @property
    def recall(self) -> float | None:
        return None if self.tp + self.fn == 0 else self.tp / (self.tp + self.fn)

    @property
    def f1(self) -> float | None:
        p, r = self.precision, self.recall
        if p is None or r is None or p + r == 0:
            return None
        return 2 * p * r / (p + r)

    def as_dict(self) -> dict[str, Any]:
        return {
            "tp": self.tp,
            "fp": self.fp,
            "fn": self.fn,
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
        }


def extraction_f1(register: Sequence[Mapping[str, str]], facts: Iterable[FactRow]) -> dict[str, F1]:
    """Field extraction scored against the register, overall and by document type.

    The register is the ground truth because every document was authored from it. For each
    document on file and each field the register fills, an extracted value that matches is a
    hit, a missing one is a miss, and a wrong one is both a false claim and a miss. A value the
    extractor produced for a field the register leaves empty is a false claim: the document does
    not print it. Documents the register knows but the vault has not indexed are not scored, so
    a half-ingested batch reports on what was ingested rather than on what was not.
    """
    extracted: dict[str, dict[str, str | None]] = defaultdict(dict)
    for fact in facts:
        extracted[fact.doc_id][fact.key] = fact.value
    counts: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
    for row in register:
        doc_id = row.get("doc_id", "")
        if doc_id not in extracted:
            continue
        found = extracted[doc_id]
        for key, value in row.items():
            if key in REGISTER_META or key is None:
                continue
            expected = (value or "").strip()
            got = found.get(key)
            if expected:
                if got is not None and same_value(expected, got):
                    outcome = (1, 0, 0)
                elif got is None:
                    outcome = (0, 0, 1)
                else:
                    outcome = (0, 1, 1)
            elif got is not None and got.strip():
                outcome = (0, 1, 0)
            else:
                continue
            for bucket in ("all", row.get("doc_type") or "unknown"):
                for index, amount in enumerate(outcome):
                    counts[bucket][index] += amount
    return {bucket: F1(*totals) for bucket, totals in sorted(counts.items())}


# ------------------------------------------------------------------------------- the judge


class Judge(Protocol):
    """Ragas with a local model, or a fake. One call per (metric, question)."""

    name: str

    async def score(self, metric: str, **fields: Any) -> float | None: ...


def reference_for(question: Question, page_text: str) -> str:
    """The reference answer Ragas judges recall and precision against.

    A fact question's reference is one sentence stating the value in the forms it is printed,
    which is what a judge can check a passage against. A passage question's reference is the
    page itself, because "must cite this page" is the whole expectation.
    """
    expected = question.expected
    if expected.kind == "fact":
        label = expected.key.replace("_", " ")
        forms = sorted(value_forms(expected.value), key=len, reverse=True)
        return f"The {label} is {expected.value}" + (
            f" (also written {', '.join(forms[:2])})." if len(forms) > 1 else "."
        )
    return page_text or expected.value or question.notes


@dataclass
class RagasJudge:
    """Ragas 0.4 metrics through Ollama's OpenAI-compatible endpoint. Imported lazily so the
    harness's tests, and `make check`, never need the `eval` extra or a running model."""

    model: str
    generation_url: str
    embed: Any  # `Ollama.embed`: list[str] -> list[list[float]]
    name: str = field(init=False)
    _metrics: dict[str, Any] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.name = self.model
        import openai
        from ragas.embeddings import BaseRagasEmbedding
        from ragas.llms import llm_factory
        from ragas.metrics.collections import (
            AnswerRelevancy,
            ContextPrecision,
            ContextRecall,
            Faithfulness,
        )

        harness_embed = self.embed

        class LocalEmbedding(BaseRagasEmbedding):
            def embed_text(self, text: str, **kwargs: Any) -> list[float]:
                return list(harness_embed([text])[0])

            async def aembed_text(self, text: str, **kwargs: Any) -> list[float]:
                return self.embed_text(text)

            def embed_texts(self, texts: list[str], **kwargs: Any) -> list[list[float]]:
                return [list(v) for v in harness_embed(texts)]

            async def aembed_texts(self, texts: list[str], **kwargs: Any) -> list[list[float]]:
                return self.embed_texts(texts)

        client = openai.AsyncOpenAI(
            base_url=f"{self.generation_url.rstrip('/')}/v1", api_key="ollama", timeout=600
        )
        llm = llm_factory(self.model, client=client)
        self._metrics = {
            "context_recall": ContextRecall(llm=llm),
            "context_precision": ContextPrecision(llm=llm),
            "faithfulness": Faithfulness(llm=llm),
            "answer_relevancy": AnswerRelevancy(llm=llm, embeddings=LocalEmbedding()),
        }

    async def score(self, metric: str, **fields: Any) -> float | None:
        try:
            result = await self._metrics[metric].ascore(**fields)
        except Exception as error:  # a judge that cannot parse its own output scores nothing
            log.warning("%s: judge gave no score (%s)", metric, error)
            return None
        value = result.value
        return None if value is None else float(value)


# ------------------------------------------------------------------------------- the run


@dataclass
class Scored:
    """One question's line in the result file."""

    trace: Trace
    outcome: str
    correct: bool | None = None  # fact questions: the answer states the register's value
    cited: bool | None = None  # the must-cite page is cited
    shown: bool | None = None  # the must-cite page was among the passages read
    judged: dict[str, float | None] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        question, answer = self.trace.question, self.trace.answer
        return {
            "id": question.id,
            "set": question.set,
            "lane": question.lane,
            "kind": question.expected.kind,
            "outcome": self.outcome,
            "says_not_on_file": says_not_on_file(answer),
            "correct": self.correct,
            "cited": self.cited,
            "shown": self.shown,
            "candidates": self.trace.candidates,
            "passages_read": len(self.trace.contexts),
            "contexts": [p.ref for p in self.trace.contexts],
            "citations": sorted({c.text for claim in answer.claims for c in claim.citations}),
            "latency_ms": self.trace.latency_ms,
            "answer": answer.text,
            **self.judged,
        }


def outcome_of(answer: Answer) -> str:
    for name in ("refused", "declined", "consent_required", "withheld", "abstained"):
        if getattr(answer, name):
            return name
    return "unanswered" if answer.unanswered else "answered"


def mean(values: Iterable[float | None]) -> float | None:
    present = [v for v in values if v is not None]
    return None if not present else round(sum(present) / len(present), 4)


def grade(traces: Sequence[Trace]) -> list[Scored]:
    """The code-scored part: no model, no network, the same answer every time."""
    scored: list[Scored] = []
    for trace in traces:
        question, answer = trace.question, trace.answer
        item = Scored(trace, outcome_of(answer))
        if question.gradeable_citation:
            item.shown = shown(trace.contexts, question.must_cite_doc, question.must_cite_page)
            item.cited = cites(answer, question.must_cite_doc, question.must_cite_page)
        if question.expected.kind == "fact":
            item.correct = not held_back(answer) and mentions(answer.text, question.expected.value)
        scored.append(item)
    return scored


async def judge_all(scored: Sequence[Scored], judge: Judge, references: Mapping[str, str]) -> None:
    """The judge-scored part, in place. Only Set A is judged: a hard negative has no reference
    and an abstention has no response, and Ragas asked to score either invents a number."""
    for item in scored:
        question, answer = item.trace.question, item.trace.answer
        if question.set != "A":
            continue
        contexts = [p.text for p in item.trace.contexts]
        reference = references.get(question.id, "")
        fields: dict[str, Any] = {"user_input": question.question}
        if contexts and reference:
            item.judged["context_recall"] = await judge.score(
                "context_recall", retrieved_contexts=contexts, reference=reference, **fields
            )
            item.judged["context_precision"] = await judge.score(
                "context_precision", retrieved_contexts=contexts, reference=reference, **fields
            )
        if not held_back(answer) and contexts:
            item.judged["faithfulness"] = await judge.score(
                "faithfulness", response=answer.text, retrieved_contexts=contexts, **fields
            )
            item.judged["answer_relevancy"] = await judge.score(
                "answer_relevancy", response=answer.text, **fields
            )


def judge_sync(scored: Sequence[Scored], judge: Judge, references: Mapping[str, str]) -> None:
    asyncio.run(judge_all(scored, judge, references))


def summarise(
    scored: Sequence[Scored],
    *,
    extraction: Mapping[str, F1] | None,
    runtime: Mapping[str, float | None] | None,
    judged: bool,
) -> tuple[dict[str, float | None], dict[str, Any], dict[str, str]]:
    """The nine metrics, the extras worth keeping beside them, and a reason for every null."""
    by_set: dict[str, list[Scored]] = defaultdict(list)
    for item in scored:
        by_set[item.trace.question.set].append(item)
    a, b, c = by_set.get("A", []), by_set.get("B", []), by_set.get("C", [])
    metrics: dict[str, float | None] = dict.fromkeys(METRIC_KEYS)
    why: dict[str, str] = {}

    for key in JUDGED:
        metrics[key] = mean(item.judged.get(key) for item in a)
        if metrics[key] is None:
            why[key] = "no judge was run" if not judged else "no Set A question could be judged"

    if b:
        metrics["abstention_rate"] = round(sum(held_back(i.trace.answer) for i in b) / len(b), 4)
    else:
        why["abstention_rate"] = "Set B (hard negatives) was not in this run"

    if extraction and "all" in extraction:
        metrics["extraction_f1"] = _round(extraction["all"].f1)
    if metrics["extraction_f1"] is None:
        why["extraction_f1"] = "no indexed document has a register row to score against"

    why["obligation_precision"] = "module questions arrive in W7; not measured by this harness"
    why["alert_fpr"] = "module questions arrive in W7; not measured by this harness"

    for key in ("decode_tok_s", "peak_vram_gb"):
        metrics[key] = (runtime or {}).get(key)
        if metrics[key] is None:
            why[key] = "no eval/results/*hardware.md to read; run scripts/bench_runtime.py"

    answered_a = [i for i in a if not held_back(i.trace.answer)]
    abstentions = sum(held_back(i.trace.answer) for i in a) + sum(
        held_back(i.trace.answer) for i in b
    )
    also: dict[str, Any] = {
        "n": {"A": len(a), "B": len(b), "C": len(c)},
        "answered_rate_a": _rate([not held_back(i.trace.answer) for i in a]),
        "fact_accuracy": _rate([i.correct for i in a if i.correct is not None]),
        "citation_hit": _rate([i.cited for i in answered_a if i.cited is not None]),
        "page_shown": _rate([i.shown for i in a if i.shown is not None]),
        "abstention_precision": (
            None
            if abstentions == 0 or not b
            else round(sum(held_back(i.trace.answer) for i in b) / abstentions, 4)
        ),
        "said_not_on_file_b": _rate([says_not_on_file(i.trace.answer) for i in b]),
        "refusal_rate_c": _rate([refused(i.trace.answer) for i in c]),
        "held_back_rate_c": _rate([held_back(i.trace.answer) for i in c]),
        "median_latency_ms": _median([i.trace.latency_ms for i in scored]),
        "extraction_by_doc_type": {
            k: v.as_dict() for k, v in (extraction or {}).items() if k != "all"
        },
    }
    return metrics, also, why


def _rate(values: Sequence[bool]) -> float | None:
    return None if not values else round(sum(values) / len(values), 4)


def _round(value: float | None) -> float | None:
    return None if value is None else round(value, 4)


def _median(values: Sequence[int]) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[len(ordered) // 2]
