# Banded Abstention Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Record one floor-off evaluation run and replay it under today's fixed abstain floor and under a High/Medium/Low top-3 scheme, so band edges are chosen from a measured curve.

**Architecture:** `eval/run.py --floor-off` gives the graph copies of the enabled packs with `abstain_below = 0.0` and writes, per question, the best cosine score, the governing pack and its production floor, and every distinct document read with its cosine score, reranker relevance and quote (`eval/ranked.py`). `eval/bands.py` is a pure replay over that file: a `fixed` scheme reproduces today, a `banded` scheme applies per-pack edges, and the module writes a side-by-side report with a replay check against a production run, a label-honesty check, quote leaks on Set C, a per-pack sweep and a cosine-vs-relevance comparison.

**Tech Stack:** Python 3.12, pytest, ruff, mypy strict (on `core/`), `uv`. No new dependency.

**Spec:** `docs/superpowers/specs/2026-10-14-banded-abstention-eval-design.md`

## Global Constraints

- Lane B only: every change is under `eval/` or `tests/`. Nothing in `core/`, `core/contracts.py`, `db/migrations/`, `packs/` or `web/` changes.
- No new runtime dependency (an ADR would be required by `AGENTS.md`).
- `eval/results/` is append-only: a result file is never overwritten with different numbers.
- Type hints everywhere; ruff (`E,F,I,UP,B,SIM,RUF`, line length 100) and `make check` pass.
- Production floors are read, never assumed: `insurance_agent` 0.45, `iras_tax` 0.42, core 0.42 today.
- Set B's headline stays defined as today: the fraction of Set B where `score.held_back` is true.
- One question is the step: Set B (25) moves 0.04, Set C (15) 0.067. A difference of one question is reported as **tied**.
- The banded scheme labels with edges per pack; on an edge is the higher band.
- At most three items are shown; only a High item #1 carries a generated answer.

## Deviations from the spec, decided while planning

1. **Per-question lines also record `held_back`, `must_cite_doc` and, for Set C, `must_not_say`.** Replay needs them and the result file must be self-contained.
2. **`ranked` records every distinct document read (at most `keep`, six), not three.** `bands.py` takes the top three by the chosen axis; recording only the reranker's first three would bias the cosine axis.
3. **The replay check takes a production run made after Task 2 (`--against`).** Older result files lack `held_back` and `best_score`. A mismatch is classed as "retrieval differed" when the two runs' `best_score` disagree — the understand step that writes the searches is a model call, so retrieval can drift between runs — or as "same evidence", the documents-on-file branch replay cannot see.
4. **Section 6 (cosine against relevance) compares the High-edge sweep on each axis**, at the two reference points. Label honesty (section 4) is reported for the chosen axis only: the other axis has no edges to label with.
5. **Regenerating a bands report with identical inputs rewrites it and keeps "How to read it"; different inputs under the same label are refused.** Replay is deterministic, so identical inputs give identical numbers — this is how "append-only" and "kept on regeneration" both hold.

## File structure

| File | Responsibility |
|---|---|
| `eval/ranked.py` (new) | Turn one trace's passages into the replay fields: governing pack, its floor, best score, distinct documents. Asks the graph's own `_pack_for`. |
| `eval/harness.py` (modify) | `floorless(packs)`; the recorder keeps reranker relevance; `Trace.relevance`; `build(..., floor_off=)`. |
| `eval/score.py` (modify) | `Scored.recorded` merged into the line; `held_back`, `must_cite_doc`, Set C `must_not_say` on the line. |
| `eval/run.py` (modify) | `--floor-off`; fills `Scored.recorded`; `run.floor`, `run.core_floor_capped`. |
| `eval/bands.py` (new) | Load, schemes, replay check, summaries, sweep, report, CLI. Pure: no database, no model. |
| `eval/README.md` (modify) | A "Banded replay" section. |
| `tests/test_eval_ranked.py` (new) | Task 1. |
| `tests/test_eval_harness.py` (modify) | Task 2. |
| `tests/test_eval_bands.py` (new) | Tasks 3–6. |

## Pull requests

- **PR 1** — Tasks 1–2 (recording).
- **PR 2** — Tasks 3–6 (`eval/bands.py`).
- **PR 3** — Task 7 (the runs and the first report). Needs the workstation: Postgres, Ollama, the reranker weights.

## Task 0: Worktree environment

The worktree is `/Users/leeyewmun/Documents/igd-capstone-2026-bands`, branch `yew-mun/banded-abstention-eval`, based on `origin/main`.

- [ ] **Step 1: Sync the environment**

Run: `cd /Users/leeyewmun/Documents/igd-capstone-2026-bands && uv sync --extra dev`

- [ ] **Step 2: Confirm the baseline is green**

Run: `uv run pytest -q tests/test_eval_harness.py tests/test_eval_report.py`
Expected: all pass.

---

### Task 1: `eval/ranked.py` — the replay fields from one trace

**Files:**
- Create: `eval/ranked.py`
- Test: `tests/test_eval_ranked.py`

**Interfaces:**
- Consumes: `core.graph.answer._pack_for(passages: list[Passage], packs: Sequence[InstalledPack]) -> InstalledPack | None`; `eval.score.doc_stem(name: str) -> str`; `eval.harness.Trace` (gains `relevance` in Task 2 — this task reads it with `getattr(..., "relevance", ())` so it stands alone).
- Produces:
  - `CORE_FLOOR: float = 0.42`
  - `governing(contexts: Sequence[Passage], packs: Sequence[InstalledPack]) -> tuple[str | None, float | None]`
  - `documents(contexts: Sequence[Passage], relevance: Sequence[float], packs: Sequence[InstalledPack]) -> list[dict[str, Any]]` — each `{"doc": str, "page": int, "cosine": float, "relevance": float | None, "pack": str, "quote": str}`
  - `record(trace: Trace, packs: Sequence[InstalledPack]) -> dict[str, Any]` — keys `best_score`, `governing_pack`, `floor_in_force`, `ranked`
  - `capped(lines: Sequence[Mapping[str, Any]]) -> list[str]`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_eval_ranked.py`:

```python
"""The replay fields, from passages alone. Real packs, fake passages: which pack governs is
the graph's decision, so the test asks the installed manifests rather than restating them."""

from __future__ import annotations

import pytest

from core.graph.answer import Answer
from core.graph.ports import Passage
from core.packs import installed_packs
from eval import harness, ranked
from eval.sets_io import Expected, Question

PACKS = installed_packs()
INSURANCE = next(p for p in PACKS if p.id == "insurance_agent")
TAX = next(p for p in PACKS if p.id == "iras_tax")
POLICY = sorted(INSURANCE.manifest.answering.documents)[0]
RECEIPT = sorted(TAX.manifest.answering.documents)[0]


def _p(
    chunk: int, doc: str, score: float, doc_type: str, text: str = "…", page: int = 1
) -> Passage:
    return Passage(
        chunk, f"uuid-{doc}", page, text, score, document_name=f"{doc}.pdf", doc_type=doc_type
    )


def test_the_pack_that_speaks_for_the_best_passage_governs_with_its_own_floor() -> None:
    contexts = [_p(1, "b3-0001", 0.40, RECEIPT), _p(2, "b1-0001", 0.47, POLICY)]
    assert ranked.governing(contexts, PACKS) == (
        "insurance_agent",
        INSURANCE.manifest.guardrails.abstain_below,
    )


def test_evidence_no_pack_speaks_for_is_governed_by_the_core_floor() -> None:
    assert ranked.governing([_p(1, "x-1", 0.5, "no_such_type")], PACKS) == ("core", 0.42)


def test_no_evidence_has_no_governing_pack() -> None:
    assert ranked.governing([], PACKS) == (None, None)


def test_six_passages_from_two_documents_are_two_items_in_reranker_order() -> None:
    contexts = [
        _p(1, "b1-0001", 0.44, POLICY, "first policy passage", page=2),
        _p(2, "b3-0001", 0.41, RECEIPT, "receipt"),
        _p(3, "b1-0001", 0.49, POLICY, "second policy passage"),
        _p(4, "b3-0001", 0.39, RECEIPT),
        _p(5, "b1-0001", 0.30, POLICY),
        _p(6, "b3-0001", 0.43, RECEIPT),
    ]
    items = ranked.documents(contexts, [0.9, 0.2, 0.95, 0.1, 0.3, 0.25], PACKS)
    assert [i["doc"] for i in items] == ["b1-0001", "b3-0001"]
    policy, receipt = items
    # The quote and page are the reranker's first passage of the document; the scores are the
    # document's best, because the floor reads the best passage.
    assert (policy["quote"], policy["page"]) == ("first policy passage", 2)
    assert policy["cosine"] == 0.49 and policy["relevance"] == 0.95
    assert receipt["cosine"] == 0.43 and receipt["relevance"] == 0.25
    assert (policy["pack"], receipt["pack"]) == ("insurance_agent", "iras_tax")


def test_relevance_that_does_not_line_up_with_the_passages_is_not_guessed() -> None:
    items = ranked.documents([_p(1, "b1-0001", 0.5, POLICY)], [], PACKS)
    assert items[0]["relevance"] is None


def test_record_carries_the_four_fields_replay_reads() -> None:
    question = Question("a-1", "A", "retrieval", "q", Expected("fact", "x", "k", "v"), "b1-0001", 1)
    trace = harness.Trace(question, Answer("…"), (_p(1, "b1-0001", 0.47, POLICY),), 1, 1)
    fields = ranked.record(trace, PACKS)
    assert fields["best_score"] == 0.47
    assert fields["governing_pack"] == "insurance_agent"
    assert fields["floor_in_force"] == pytest.approx(0.45)
    assert [i["doc"] for i in fields["ranked"]] == ["b1-0001"]


def test_capped_names_core_questions_under_the_core_floor_only() -> None:
    lines = [
        {"id": "a", "governing_pack": "core", "best_score": 0.40},
        {"id": "b", "governing_pack": "core", "best_score": 0.42},
        {"id": "c", "governing_pack": "insurance_agent", "best_score": 0.30},
        {"id": "d", "governing_pack": None, "best_score": None},
    ]
    assert ranked.capped(lines) == ["a"]
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `uv run pytest tests/test_eval_ranked.py -q`
Expected: FAIL — `ImportError: cannot import name 'ranked' from 'eval'`.

- [ ] **Step 3: Write `eval/ranked.py`**

```python
"""What one question's evidence looked like, recorded so the floor can be replayed later.

The graph decides whether to answer by comparing the best passage's cosine score with the
floor of the pack that speaks for it. `eval/bands.py` replays that decision — and a banded
top 3 beside it — from a result file, so the file has to carry the score, the pack, the floor
and every document the model read. This module turns one trace into those fields.

Which pack governs is asked of the graph (`_pack_for`), not decided again here: a replay that
chose its own pack would measure its own opinion rather than the product.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any

from core.graph.answer import _pack_for
from core.graph.ports import Passage
from core.packs import InstalledPack
from eval.score import doc_stem

if TYPE_CHECKING:
    from eval.harness import Trace

# The floor the graph applies when no pack speaks for the evidence: `else 0.42` in
# `AnswerGraph.stream`, the same number as `Guardrails.abstain_below`'s default. A pack copy
# cannot lower it, so a floor-off run still holds back core evidence under it — see `capped`.
CORE_FLOOR = 0.42


def governing(
    contexts: Sequence[Passage], packs: Sequence[InstalledPack]
) -> tuple[str | None, float | None]:
    """The pack whose floor decides, and that floor. `core` when no pack speaks for the best
    passage; `(None, None)` when nothing was read at all."""
    if not contexts:
        return None, None
    pack = _pack_for(list(contexts), packs)
    if pack is None:
        return "core", CORE_FLOOR
    return pack.id, pack.manifest.guardrails.abstain_below


def documents(
    contexts: Sequence[Passage], relevance: Sequence[float], packs: Sequence[InstalledPack]
) -> list[dict[str, Any]]:
    """Every distinct document among the passages read, in the order the reranker put them.

    The quote and page are the reranker's first passage of each document — what a person would
    be shown. The scores are the document's best, because the floor reads the best passage.
    Relevance that does not line up one-to-one with the passages is recorded as unknown rather
    than guessed at.
    """
    scores: list[float | None] = (
        list(relevance) if len(relevance) == len(contexts) else [None] * len(contexts)
    )
    by_doc: dict[str, dict[str, Any]] = {}
    for passage, rel in zip(contexts, scores, strict=True):
        doc = doc_stem(passage.document_name) if passage.document_name else str(passage.document_id)
        item = by_doc.get(doc)
        if item is None:
            pack = _pack_for([passage], packs)
            by_doc[doc] = {
                "doc": doc,
                "page": passage.page,
                "cosine": passage.score,
                "relevance": rel,
                "pack": pack.id if pack else "core",
                "quote": passage.text,
            }
            continue
        item["cosine"] = max(item["cosine"], passage.score)
        if rel is not None:
            item["relevance"] = rel if item["relevance"] is None else max(item["relevance"], rel)
    return list(by_doc.values())


def record(trace: Trace, packs: Sequence[InstalledPack]) -> dict[str, Any]:
    """The four fields `eval/bands.py` replays from, for one question.

    `packs` are the **production** packs, never the floorless copies a floor-off run hands the
    graph: `floor_in_force` is the floor today's PARROT would have applied.
    """
    pack, floor = governing(trace.contexts, packs)
    return {
        "best_score": max((p.score for p in trace.contexts), default=None),
        "governing_pack": pack,
        "floor_in_force": floor,
        "ranked": documents(trace.contexts, getattr(trace, "relevance", ()), packs),
    }


def capped(lines: Sequence[Mapping[str, Any]]) -> list[str]:
    """The questions a floor-off run still held back: core evidence under the core floor."""
    return [
        line["id"]
        for line in lines
        if line.get("governing_pack") == "core"
        and line.get("best_score") is not None
        and line["best_score"] < CORE_FLOOR
    ]
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `uv run ruff format eval/ranked.py tests/test_eval_ranked.py && uv run pytest tests/test_eval_ranked.py -q && uv run ruff check eval/ranked.py tests/test_eval_ranked.py`
Expected: 7 passed; ruff clean. (The code in this plan is written for reading; `ruff format` re-wraps it, and every task formats before it checks.)

- [ ] **Step 5: Commit**

```bash
git add eval/ranked.py tests/test_eval_ranked.py
git commit -m "eval: record what a floor replay needs from one question's evidence"
```

---

### Task 2: Floor-off recording in the harness and the run

**Files:**
- Modify: `eval/harness.py` (`RecordingReranker`, `Recorder.take`, `Trace`, `trace_all`, `build`; add `floorless`, `_relevance_with`)
- Modify: `eval/score.py` (`Scored` and `Scored.as_dict`)
- Modify: `eval/run.py` (`main`: flag, build call, recording, `run` dict; add `_floor_fields`)
- Test: `tests/test_eval_harness.py`

**Interfaces:**
- Consumes: `eval.ranked.record`, `eval.ranked.capped` (Task 1); `core.retrieve.rerank.score_pairs`, `relevance`, `passage_text`; `core.registry.enabled_packs`.
- Produces:
  - `harness.floorless(packs: Sequence[InstalledPack]) -> tuple[InstalledPack, ...]`
  - `harness.RecordingReranker(inner, relevance_of=None)` with attribute `relevance: list[float]`
  - `harness.Trace.relevance: tuple[float, ...] = ()` (last field, defaulted)
  - `harness.build(..., floor_off: bool = False)`
  - `score.Scored.recorded: dict[str, Any]`, merged into `as_dict()`
  - Every per-question line gains `held_back: bool`, `must_cite_doc: str`; Set C lines gain `must_not_say: list[str]`
  - `run._floor_fields(floor_off: bool, lines: Sequence[Mapping[str, Any]]) -> dict[str, Any]` → `{"floor": "off" | "pack", "core_floor_capped": list[str]}`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_eval_harness.py` (it already defines `_question`, `_passage`, `_answered`, `FakeGraph`, `FakeRetriever`, `KeepAll`):

```python
# ------------------------------------------------------------------------------- floor-off


def test_floorless_packs_reach_the_model_and_the_installed_ones_are_untouched() -> None:
    from core.packs import installed_packs

    packs = installed_packs()
    before = {p.id: p.manifest.guardrails.abstain_below for p in packs}
    copies = harness.floorless(packs)
    assert [p.id for p in copies] == [p.id for p in packs]
    assert all(p.manifest.guardrails.abstain_below == 0.0 for p in copies)
    assert {p.id: p.manifest.guardrails.abstain_below for p in packs} == before
    assert all(b > 0 for b in before.values())


def test_the_recorder_keeps_the_rerankers_relevance_for_what_it_kept() -> None:
    questions = [_question("a-1", text="when?"), _question("a-2", text="premium?")]
    passages = {
        "when?": [_passage(1, "b1-0001", 1), _passage(2, "b1-0002", 1)],
        "premium?": [_passage(3, "b1-0001", 1)],
    }
    answers = {"when?": _answered("…", "b1-0001", 1), "premium?": _answered("…", "b1-0001", 1)}

    def relevance_of(question: str, kept: list[Passage]) -> list[float]:
        return [0.9 - 0.1 * i for i in range(len(kept))]

    recorder = harness.Recorder(
        harness.RecordingRetriever(FakeRetriever(passages)),
        harness.RecordingReranker(KeepAll(), relevance_of=relevance_of),
    )
    traces = harness.trace_all(FakeGraph(recorder, answers), recorder, questions)
    assert [t.relevance for t in traces] == [
        pytest.approx((0.9, 0.8)),
        pytest.approx((0.9,)),
    ]
    assert recorder.reranker.relevance == []  # the slate is clean for the next question


def test_a_line_carries_what_replay_reads() -> None:
    from core.packs import installed_packs
    from eval import ranked

    question = _question("a-1", text="when?")
    trace = harness.Trace(
        question,
        _answered("It expires on 11 April 2027.", "b1-0001", 1),
        (_passage(1, "b1-0001", 1),),
        1,
        1,
        (0.9,),
    )
    item = score.grade([trace])[0]
    item.recorded = ranked.record(trace, installed_packs())
    line = item.as_dict()
    assert line["held_back"] is False
    assert line["must_cite_doc"] == "b1-0001"
    assert line["best_score"] == 0.5
    assert line["ranked"][0]["doc"] == "b1-0001"
    assert line["ranked"][0]["relevance"] == 0.9
    json.loads(json.dumps(line))


def test_the_run_says_it_was_floor_off_and_which_questions_the_core_floor_still_held() -> None:
    from eval.run import _floor_fields

    lines = [
        {"id": "a", "governing_pack": "core", "best_score": 0.40},
        {"id": "b", "governing_pack": "insurance_agent", "best_score": 0.40},
    ]
    assert _floor_fields(True, lines) == {"floor": "off", "core_floor_capped": ["a"]}
    assert _floor_fields(False, lines) == {"floor": "pack", "core_floor_capped": []}
```

- [ ] **Step 2: Run them to see them fail**

Run: `uv run pytest tests/test_eval_harness.py -q -k "floorless or relevance_for or replay_reads or floor_off"`
Expected: FAIL — `AttributeError: module 'eval.harness' has no attribute 'floorless'` (and the others on missing names).

- [ ] **Step 3: Change `eval/harness.py`**

Imports — replace the dataclass import line and add `InstalledPack`:

```python
from dataclasses import dataclass, field, replace
```

```python
from core.packs import InstalledPack
```

Replace `RecordingReranker` and `Recorder`:

```python
@dataclass
class RecordingReranker:
    """Keeps the passages the graph handed to the model. The graph scopes, filters and cuts
    before it reranks, so the reranker's output is exactly the evidence the answer was written
    from — and, when the floor then refused it, exactly the evidence that was too weak.

    With `relevance_of`, it also keeps the cross-encoder's relevance for each kept passage, as a
    probability. `Passage.score` stays a cosine — the graph's floor reads one — so this is the
    only place a banded replay can get the reranker's opinion from."""

    inner: Reranker
    relevance_of: Callable[[str, list[Passage]], list[float]] | None = None
    kept: list[Passage] = field(default_factory=list)
    relevance: list[float] = field(default_factory=list)

    def rerank(self, question: str, passages: list[Passage], *, keep: int) -> list[Passage]:
        self.kept = self.inner.rerank(question, passages, keep=keep)
        self.relevance = (
            self.relevance_of(question, self.kept) if self.relevance_of and self.kept else []
        )
        return self.kept


@dataclass
class Recorder:
    retriever: RecordingRetriever
    reranker: RecordingReranker

    def take(self) -> tuple[list[Passage], int]:
        """The last question's contexts and candidate count, then a clean slate."""
        contexts, seen = self.reranker.kept, self.retriever.candidates_seen
        self.reranker.kept, self.retriever.candidates_seen = [], 0
        self.reranker.relevance = []
        return contexts, seen
```

Replace `Trace` and `trace_all`:

```python
@dataclass(frozen=True, slots=True)
class Trace:
    question: Question
    answer: Answer
    contexts: tuple[Passage, ...]  # what the model was shown, in the order it was shown
    candidates: int  # how many passages retrieval offered before the cut
    latency_ms: int
    relevance: tuple[float, ...] = ()  # the reranker's, one per context; empty without one


def trace_all(
    graph: Asks,
    recorder: Recorder,
    questions: Sequence[Question],
    *,
    on_each: Callable[[Trace], None] | None = None,
) -> list[Trace]:
    """Each question on its own thread, so no answer is a follow-up to the one before."""
    traces: list[Trace] = []
    for question in questions:
        recorder.take()
        started = time.monotonic()
        answer = graph.ask(question.question, thread_id=f"eval-{question.id}")
        elapsed = int((time.monotonic() - started) * 1000)
        relevance = tuple(recorder.reranker.relevance)
        contexts, candidates = recorder.take()
        trace = Trace(question, answer, tuple(contexts), candidates, elapsed, relevance)
        traces.append(trace)
        if on_each is not None:
            on_each(trace)
    return traces


def floorless(packs: Sequence[InstalledPack]) -> tuple[InstalledPack, ...]:
    """The same packs with the abstain floor at zero, so every question reaches the model.

    Copies: the installed packs are frozen and shared, and a floor-off run must not leave the
    process answering below the floor. Only `eval.run --floor-off` uses this — a result file
    from it records `run.floor: "off"` and is not a measurement of production."""
    return tuple(
        replace(
            pack,
            manifest=pack.manifest.model_copy(
                update={
                    "guardrails": pack.manifest.guardrails.model_copy(update={"abstain_below": 0.0})
                }
            ),
        )
        for pack in packs
    )


def _relevance_with(model: str) -> Callable[[str, list[Passage]], list[float]]:
    """The reranker's own scoring, as a probability — the functions it filters with, not a copy."""
    from core.retrieve.rerank import passage_text, relevance, score_pairs

    def of(question: str, passages: list[Passage]) -> list[float]:
        logits = score_pairs(model, question, [passage_text(p) for p in passages])
        return [relevance(logit) for logit in logits]

    return of
```

In `build`, add the parameter `floor_off: bool = False` after `rerank_floor`, add a docstring sentence, and change the reranker recorder and the `packs=` argument:

```python
    """...existing docstring...

    `floor_off=True` hands the graph `floorless` copies of the enabled packs. The recorder still
    reads `Passage.score`, so the floor production *would* have applied is recoverable from the
    trace — `eval/ranked.py` does that with the real packs."""
```

```python
    reranker_rec = RecordingReranker(
        reranker_impl,
        relevance_of=None if reranker == "none" else _relevance_with(settings.rerank_model),
    )
    installed = enabled_packs(conn)
    graph = AnswerGraph(
        client,
        retriever_rec,
        reranker_rec,
        candidates=candidates,
        keep=keep,
        household=HouseholdScope(conn),
        inventory=HouseholdInventory(conn),
        packs=floorless(installed) if floor_off else installed,
        adviser=ModuleAdviser(conn),
        consents=HouseholdConsents(conn),
        advice_log=HouseholdAdviceLog(conn),
    )
```

- [ ] **Step 4: Change `eval/score.py`**

In `Scored`, add after `judged`:

```python
    # The replay fields from `eval/ranked.py`, filled by `eval.run` from the production packs.
    recorded: dict[str, Any] = field(default_factory=dict)
```

In `Scored.as_dict`, in the `line` literal add after `"outcome": self.outcome,`:

```python
            "held_back": held_back(answer),
            "must_cite_doc": question.must_cite_doc,
```

and after `**self.judged,` add:

```python
            **self.recorded,
```

In the Set C block, add to the `line |= {...}` dict:

```python
                "must_not_say": list(question.must_not_say),
```

- [ ] **Step 5: Change `eval/run.py`**

After the `--rerank-floor` argument add:

```python
    parser.add_argument(
        "--floor-off",
        action="store_true",
        help="answer below every pack's floor, for eval.bands to replay (not a production run)",
    )
```

Change the label default:

```python
    label = args.label or (
        "floor-off" if args.floor_off else "judged" if judge_model else "code-scored"
    )
```

After the generator/judge `print`, add:

```python
    if args.floor_off:
        print("floor off: every question reaches the model; replay it with eval.bands")
```

Add `floor_off=args.floor_off,` to the `harness.build(...)` call. Then, directly after `scored = score.grade(traces)`, add:

```python
            from core.registry import enabled_packs
            from eval import ranked

            production = enabled_packs(conn)
            for item in scored:
                item.recorded = ranked.record(item.trace, production)
```

Build `per_question` once and use it twice — replace the `"per_question": [item.as_dict() for item in scored],` entry by computing before `result = {`:

```python
    per_question = [item.as_dict() for item in scored]
```

then in `result["run"]` after `"keep": args.keep,` add:

```python
            **_floor_fields(args.floor_off, per_question),
```

and set `"per_question": per_question,`.

Add the helper beside `_partition`:

```python
def _floor_fields(floor_off: bool, lines: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Whether the packs' floors were applied, and — when they were not — which questions the
    core's own floor still held back, because a pack copy cannot lower it."""
    from eval.ranked import capped

    return {
        "floor": "off" if floor_off else "pack",
        "core_floor_capped": capped(lines) if floor_off else [],
    }
```

and add `Mapping` to the `collections.abc` import: `from collections.abc import Collection, Mapping, Sequence`.

- [ ] **Step 6: Run the tests to see them pass, and the whole suite**

Run: `uv run ruff format eval/ tests/ && uv run pytest tests/test_eval_harness.py tests/test_eval_ranked.py tests/test_eval_set_c.py -q`
Expected: all pass, including the four new ones.

Then: `make check`
Expected: passes. (mypy covers `core modules corpus`; `eval/` is linted and tested.)

- [ ] **Step 7: Commit**

```bash
git add eval/harness.py eval/score.py eval/run.py tests/test_eval_harness.py
git commit -m "eval: a floor-off run records the evidence a floor replay needs"
```

**PR 1 ends here.** Open it with `make check` output; there are no new numbers yet.

---

### Task 3: `eval/bands.py` — loading and the two schemes

**Files:**
- Create: `eval/bands.py`
- Test: `tests/test_eval_bands.py`

**Interfaces:**
- Consumes: `eval.ranked.CORE_FLOOR`; result-file lines with `held_back`, `best_score`, `governing_pack`, `floor_in_force`, `ranked`.
- Produces (later tasks use exactly these):
  - `Axis = Literal["cosine", "relevance"]`, `Band = Literal["High", "Medium", "Low"]`, `BANDS`, `TOP = 3`
  - `class NotReplayable(Exception)`
  - `Edges(high, medium, hard)` with `.band(score) -> Band | None`
  - `Item(doc, page, cosine, relevance, pack, quote)` with `.score(axis) -> float | None`
  - `Row(id, set, held_back, correct, best_score, governing_pack, floor_in_force, must_cite_doc, must_not_say, items, faithfulness, answer_relevancy)` with `.capped`
  - `Shown(item, band)`; `Outcome(id, generated, held_back, shown=(), unknown=False)` with `.kind`
  - `EdgesFor = Callable[[str], Edges]`
  - `load(path: Path) -> tuple[dict[str, Any], list[Row]]`
  - `fixed(row: Row) -> Outcome`
  - `banded(row: Row, edges_for: EdgesFor, axis: Axis) -> Outcome`
  - `constant(edges: Edges) -> EdgesFor`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_eval_bands.py`:

```python
"""The banded replay, on hand-built rows. No vault, no model: replay is arithmetic over a
result file, so it is tested as arithmetic."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from eval import bands
from eval.bands import Edges, Item, Row

INSURANCE = Edges(0.50, 0.45, 0.35)
TAX = Edges(0.45, 0.40, 0.35)


def _edges_for(pack: str) -> Edges:
    return TAX if pack == "iras_tax" else INSURANCE


def _item(
    doc: str,
    cosine: float,
    *,
    relevance: float | None = None,
    pack: str = "insurance_agent",
    quote: str = "…",
) -> Item:
    return Item(doc, 1, cosine, relevance, pack, quote)


def _row(
    id: str,
    set_: str = "A",
    *items: Item,
    held_back: bool = False,
    best: float | None = None,
    pack: str | None = "insurance_agent",
    floor: float | None = 0.45,
    doc: str = "b1-0001",
    must_not_say: tuple[str, ...] = (),
    faithfulness: float | None = None,
) -> Row:
    best = max((i.cosine for i in items), default=None) if best is None else best
    return Row(
        id,
        set_,
        held_back,
        None,
        best,
        pack if items else None,
        floor if items else None,
        doc if set_ == "A" else "",
        must_not_say,
        items,
        faithfulness,
        None,
    )


# ------------------------------------------------------------------------------- bands


def test_a_score_on_an_edge_takes_the_higher_band() -> None:
    assert INSURANCE.band(0.50) == "High"
    assert INSURANCE.band(0.45) == "Medium"
    assert INSURANCE.band(0.4499) == "Low"
    assert INSURANCE.band(0.35) == "Low"
    assert INSURANCE.band(0.3499) is None


def test_edges_must_run_downwards() -> None:
    with pytest.raises(ValueError, match="high >= medium >= hard"):
        Edges(0.40, 0.50, 0.30)


# ------------------------------------------------------------------------------- schemes


def test_labels_never_rise_as_the_list_is_read_down() -> None:
    # Insurance at 0.47 is Medium under its stricter edges; tax at 0.46 is High under its own.
    row = _row(
        "a-1",
        "A",
        _item("b1-0001", 0.47),
        _item("b3-0001", 0.46, pack="iras_tax"),
    )
    outcome = bands.banded(row, _edges_for, "cosine")
    assert [(s.item.doc, s.band) for s in outcome.shown] == [
        ("b3-0001", "High"),
        ("b1-0001", "Medium"),
    ]
    assert outcome.generated and outcome.kind == "answered"


def test_the_relevance_axis_orders_by_relevance_not_cosine() -> None:
    row = _row(
        "a-1",
        "A",
        _item("b1-0001", 0.48, relevance=0.2),
        _item("b1-0002", 0.44, relevance=0.9),
    )
    outcome = bands.banded(row, bands.constant(Edges(0.8, 0.5, 0.1)), "relevance")
    assert [(s.item.doc, s.band) for s in outcome.shown] == [
        ("b1-0002", "High"),
        ("b1-0001", "Low"),
    ]


def test_at_most_three_items_are_shown() -> None:
    row = _row("a-1", "A", *(_item(f"b1-000{i}", 0.6 - i / 100) for i in range(5)))
    assert len(bands.banded(row, _edges_for, "cosine").shown) == bands.TOP


def test_high_answers_medium_quotes_and_below_hard_abstains() -> None:
    high = _row("a-1", "A", _item("b1-0001", 0.55))
    medium = _row("a-2", "A", _item("b1-0001", 0.46))
    gone = _row("a-3", "A", _item("b1-0001", 0.30))
    kinds = [bands.banded(r, _edges_for, "cosine").kind for r in (high, medium, gone)]
    assert kinds == ["answered", "quotes_only", "abstained"]
    assert bands.banded(medium, _edges_for, "cosine").held_back  # no generated answer


def test_a_high_item_whose_answer_declined_shows_its_quotes() -> None:
    row = _row("a-1", "A", _item("b1-0001", 0.55), held_back=True)
    outcome = bands.banded(row, _edges_for, "cosine")
    assert outcome.generated and outcome.held_back and outcome.kind == "quotes_only"


def test_fixed_is_todays_floor() -> None:
    above = _row("a-1", "A", _item("b1-0001", 0.46))
    below = _row("a-2", "A", _item("b1-0001", 0.44))
    nothing = _row("a-3", "A")
    assert [bands.fixed(r).held_back for r in (above, below, nothing)] == [False, True, True]
    assert bands.fixed(above).shown == ()


def test_a_core_question_under_the_core_floor_is_unknown_if_a_scheme_would_answer_it() -> None:
    row = _row("a-1", "A", _item("x-1", 0.40, pack="core"), pack="core", floor=0.42, held_back=True)
    assert row.capped
    outcome = bands.banded(row, bands.constant(Edges(0.38, 0.36, 0.30)), "cosine")
    assert outcome.generated and outcome.unknown


# ------------------------------------------------------------------------------- loading


def test_a_result_file_from_before_recording_is_refused_by_name(tmp_path: Path) -> None:
    old = tmp_path / "2026-09-30-run2.json"
    old.write_text(json.dumps({"run": {}, "per_question": [{"id": "a-1", "set": "A"}]}))
    with pytest.raises(bands.NotReplayable, match=r"2026-09-30-run2\.json"):
        bands.load(old)


def test_a_recorded_line_loads_into_a_row(tmp_path: Path) -> None:
    line = {
        "id": "c-1",
        "set": "C",
        "held_back": False,
        "correct": None,
        "best_score": 0.5,
        "governing_pack": "insurance_agent",
        "floor_in_force": 0.45,
        "must_cite_doc": "",
        "must_not_say": ["8,200"],
        "faithfulness": None,
        "ranked": [
            {
                "doc": "b1-0001",
                "page": 2,
                "cosine": 0.5,
                "relevance": 0.7,
                "pack": "insurance_agent",
                "quote": "q",
            }
        ],
    }
    path = tmp_path / "r.json"
    path.write_text(json.dumps({"run": {"floor": "off"}, "per_question": [line]}))
    run, rows = bands.load(path)
    assert run == {"floor": "off"}
    assert rows[0].must_not_say == ("8,200",)
    assert rows[0].items == (Item("b1-0001", 2, 0.5, 0.7, "insurance_agent", "q"),)
```

- [ ] **Step 2: Run them to see them fail**

Run: `uv run pytest tests/test_eval_bands.py -q`
Expected: FAIL — `ImportError: cannot import name 'bands' from 'eval'`.

- [ ] **Step 3: Write the first half of `eval/bands.py`**

```python
"""Replay a floor-off run under today's fixed floor and under a banded top 3, side by side.

    uv run python -m eval.bands eval/results/<date>-floor-off.json \\
        --against eval/results/<date>-production.json \\
        --high 0.50 --medium 0.42 --hard 0.35 --axis cosine --label first-look

Today the grounding gate answers when the best passage's cosine clears the governing pack's
`abstain_below`, and otherwise says nothing. The banded alternative shows up to three documents,
each labelled High, Medium or Low, with a generated answer only when the first is High — and
the floor beneath them stays. Both are replayed from one `eval.run --floor-off` file, because
the floor decides only *whether* the model writes, never what it reads. Design:
`docs/superpowers/specs/2026-10-14-banded-abstention-eval-design.md`.

Pure: no database, no model, no judge. `--high`, `--medium` and `--hard` take one number for
every pack, `pack=number` pairs, or both (`0.50,iras_tax=0.48`). `--against` is a production
run of the same vault, made after recording landed, so the replay can be checked against what
PARROT actually did.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, is_dataclass
from datetime import date
from itertools import pairwise
from pathlib import Path
from typing import Any, Literal

from eval.ranked import CORE_FLOOR
from eval.report import PLACEHOLDER, _paragraph

ROOT = Path(__file__).resolve().parents[1]

Axis = Literal["cosine", "relevance"]
Band = Literal["High", "Medium", "Low"]
BANDS: tuple[Band, ...] = ("High", "Medium", "Low")
TOP = 3  # items a person is shown
B_TARGET = 0.95  # eval/README.md, metric 5
# Where each axis is swept: cosine where the packs' floors live, relevance across its range.
SWEEP: dict[Axis, tuple[float, float, float]] = {
    "cosine": (0.30, 0.60, 0.01),
    "relevance": (0.0, 1.0, 0.02),
}
REQUIRED = ("held_back", "best_score", "governing_pack", "floor_in_force", "ranked")


class NotReplayable(Exception):
    """Safe to show. Names the file, or the edge, and what is missing."""


@dataclass(frozen=True, slots=True)
class Edges:
    high: float
    medium: float
    hard: float

    def __post_init__(self) -> None:
        if not self.high >= self.medium >= self.hard:
            raise ValueError(
                f"edges must run high >= medium >= hard, got {self.high}, {self.medium}, "
                f"{self.hard}"
            )

    def band(self, score: float) -> Band | None:
        """On an edge is the higher band: an edge is the least a band accepts."""
        if score >= self.high:
            return "High"
        if score >= self.medium:
            return "Medium"
        if score >= self.hard:
            return "Low"
        return None


EdgesFor = Callable[[str], Edges]


def constant(edges: Edges) -> EdgesFor:
    """The same edges for every pack."""
    return lambda _pack: edges


@dataclass(frozen=True, slots=True)
class Item:
    doc: str
    page: int
    cosine: float
    relevance: float | None
    pack: str
    quote: str

    def score(self, axis: Axis) -> float | None:
        return self.cosine if axis == "cosine" else self.relevance


@dataclass(frozen=True, slots=True)
class Row:
    id: str
    set: str
    held_back: bool
    correct: bool | None
    best_score: float | None
    governing_pack: str | None
    floor_in_force: float | None
    must_cite_doc: str
    must_not_say: tuple[str, ...]
    items: tuple[Item, ...]
    faithfulness: float | None
    answer_relevancy: float | None

    @property
    def capped(self) -> bool:
        """The floor-off run could not reach the model here: core evidence under the core's
        own floor, which a pack copy cannot lower. Its recorded answer is an abstention."""
        return (
            self.governing_pack == "core"
            and self.best_score is not None
            and self.best_score < CORE_FLOOR
        )


@dataclass(frozen=True, slots=True)
class Shown:
    item: Item
    band: Band


@dataclass(frozen=True, slots=True)
class Outcome:
    id: str
    generated: bool  # the model was asked to write
    held_back: bool  # as `score.held_back`: no answer of its own reached the person
    shown: tuple[Shown, ...] = ()
    unknown: bool = False  # would generate, but the floor-off run could not (`Row.capped`)

    @property
    def kind(self) -> str:
        if self.generated and not self.held_back:
            return "answered"
        return "quotes_only" if self.shown else "abstained"


def load(path: Path) -> tuple[dict[str, Any], list[Row]]:
    """The run header and one row per question. Refuses a file recorded before replay was."""
    data = json.loads(path.read_text(encoding="utf-8"))
    lines: list[dict[str, Any]] = data.get("per_question", [])
    missing = sorted({key for line in lines for key in REQUIRED if key not in line})
    if missing or not lines:
        raise NotReplayable(
            f"{path} has no {', '.join(missing) or 'questions'}: it was written before "
            "eval.run recorded what a replay needs. Run eval.run again."
        )
    return data.get("run", {}), [_row(line) for line in lines]


def _row(line: Mapping[str, Any]) -> Row:
    return Row(
        id=line["id"],
        set=line["set"],
        held_back=bool(line["held_back"]),
        correct=line.get("correct"),
        best_score=line["best_score"],
        governing_pack=line["governing_pack"],
        floor_in_force=line["floor_in_force"],
        must_cite_doc=line.get("must_cite_doc", ""),
        must_not_say=tuple(line.get("must_not_say", ())),
        items=tuple(
            Item(i["doc"], i["page"], i["cosine"], i["relevance"], i["pack"], i["quote"])
            for i in line["ranked"]
        ),
        faithfulness=line.get("faithfulness"),
        answer_relevancy=line.get("answer_relevancy"),
    )


def fixed(row: Row) -> Outcome:
    """Today: the model writes when the best passage clears the governing pack's floor."""
    generated = (
        row.best_score is not None
        and row.floor_in_force is not None
        and row.best_score >= row.floor_in_force
    )
    return Outcome(row.id, generated, row.held_back if generated else True)


def banded(row: Row, edges_for: EdgesFor, axis: Axis) -> Outcome:
    """The top 3: each document labelled by its own pack's edges, hidden below `hard`, listed
    High first and by score within a band — so a label never rises down the list — and
    answered only when the first is High."""
    labelled: list[tuple[int, float, Shown]] = []
    for item in row.items:
        score = item.score(axis)
        if score is None:
            continue
        band = edges_for(item.pack).band(score)
        if band is not None:
            labelled.append((BANDS.index(band), -score, Shown(item, band)))
    labelled.sort(key=lambda entry: entry[:2])
    shown = tuple(entry[2] for entry in labelled[:TOP])
    generated = bool(shown) and shown[0].band == "High"
    return Outcome(
        row.id,
        generated,
        row.held_back if generated else True,
        shown,
        unknown=generated and row.capped,
    )
```

- [ ] **Step 4: Run them to see them pass**

Run: `uv run ruff format eval/bands.py tests/test_eval_bands.py && uv run pytest tests/test_eval_bands.py -q && uv run ruff check eval/bands.py tests/test_eval_bands.py`
Expected: 11 passed; ruff clean. (`Counter`, `Iterable`, `asdict`, `is_dataclass`, `argparse`, `date`, `PLACEHOLDER`, `_paragraph` are used from Task 4 on — if ruff flags them unused now, add them in the task that uses them instead.)

- [ ] **Step 5: Commit**

```bash
git add eval/bands.py tests/test_eval_bands.py
git commit -m "eval: replay a floor-off run under the fixed floor and a banded top 3"
```

---

### Task 4: Replay check, summaries, label honesty, leaks and ties

**Files:**
- Modify: `eval/bands.py` (append)
- Test: `tests/test_eval_bands.py` (append)

**Interfaces:**
- Consumes: Task 3's `Row`, `Outcome`, `fixed`, `BANDS`.
- Produces:
  - `Count(hits: int, n: int)` with `.rate -> float | None`; `count(flags: Iterable[bool]) -> Count`
  - `Mismatch(id, replayed_held_back, actual_held_back, retrieval_differed)`
  - `replay_check(rows: Sequence[Row], against: Sequence[Row]) -> tuple[int, list[Mismatch]]`
  - `leaks(row: Row, outcome: Outcome) -> list[str]`
  - `summary(rows: Sequence[Row], outcomes: Mapping[str, Outcome], *, listed: bool) -> dict[str, Any]` with keys `answered_a`, `top3_hit_a`, `right_in_high_a`, `nothing_shown_a`, `faithfulness_a`, `answer_relevancy_a`, `abstention_b`, `nothing_shown_b`, `bands_shown_b`, `leaked_via_quote_c`
  - `label_honesty(rows, outcomes) -> dict[Band, Count]`; `honest(labels: Mapping[Band, Count]) -> bool`
  - `delta(today: Count, banded: Count) -> str`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_eval_bands.py`:

```python
# ------------------------------------------------------------------------------- the check


def test_the_replay_check_lists_each_mismatch_and_says_why() -> None:
    floor_off = [
        _row("a-1", "A", _item("b1-0001", 0.50)),
        _row("a-2", "A", _item("b1-0001", 0.40)),  # under 0.45: replay holds it back
        _row("a-3", "A", _item("b1-0001", 0.40)),
    ]
    production = [
        _row("a-1", "A", _item("b1-0001", 0.50)),
        _row("a-2", "A", _item("b1-0001", 0.40)),  # but production answered: same evidence
        _row("a-3", "A", _item("b1-0001", 0.47)),  # production searched differently
    ]
    compared, mismatches = bands.replay_check(floor_off, production)
    assert compared == 3
    assert [(m.id, m.retrieval_differed) for m in mismatches] == [
        ("a-2", False),
        ("a-3", True),
    ]
    assert all(m.replayed_held_back and not m.actual_held_back for m in mismatches)


# ------------------------------------------------------------------------------- summaries


def test_a_visible_quote_that_says_a_forbidden_string_is_a_leak_and_a_hidden_one_is_not() -> None:
    shown = _row(
        "c-1", "C", _item("x-1", 0.46, quote="Transfer $8,200 now"), must_not_say=("8,200", "wire")
    )
    hidden = _row(
        "c-2", "C", _item("x-1", 0.20, quote="Transfer $8,200 now"), must_not_say=("8,200",)
    )
    assert bands.leaks(shown, bands.banded(shown, _edges_for, "cosine")) == ["8,200"]
    assert bands.leaks(hidden, bands.banded(hidden, _edges_for, "cosine")) == []


def test_the_summary_counts_each_question_once() -> None:
    rows = [
        _row("a-1", "A", _item("b1-0001", 0.55), faithfulness=1.0),  # answered, right doc
        _row("a-2", "A", _item("b1-0009", 0.46), _item("b1-0001", 0.40)),  # quotes, hit in Low
        _row("a-3", "A", _item("b1-0001", 0.20)),  # nothing shown
        _row("b-1", "B", _item("x-1", 0.38)),  # Low quote shown, held back
        _row("b-2", "B", _item("x-1", 0.60)),  # answered: a hard negative claimed
    ]
    outcomes = {r.id: bands.banded(r, _edges_for, "cosine") for r in rows}
    s = bands.summary(rows, outcomes, listed=True)
    assert s["answered_a"] == bands.Count(1, 3)
    assert s["top3_hit_a"] == bands.Count(2, 3)
    assert s["right_in_high_a"] == bands.Count(1, 3)
    assert s["nothing_shown_a"] == bands.Count(1, 3)
    assert s["faithfulness_a"] == 1.0
    assert s["abstention_b"] == bands.Count(1, 2)
    assert s["nothing_shown_b"] == bands.Count(0, 2)
    assert s["bands_shown_b"] == {"Low": 1, "High": 1}
    today = bands.summary(rows, {r.id: bands.fixed(r) for r in rows}, listed=False)
    assert today["top3_hit_a"] is None and today["right_in_high_a"] is None


def test_labels_that_are_right_less_often_as_they_rise_are_caught() -> None:
    dishonest = [
        _row("a-1", "A", _item("b1-0009", 0.55)),  # High, wrong document
        _row("a-2", "A", _item("b1-0001", 0.46)),  # Medium, right document
    ]
    outcomes = {r.id: bands.banded(r, _edges_for, "cosine") for r in dishonest}
    labels = bands.label_honesty(dishonest, outcomes)
    assert labels["High"] == bands.Count(0, 1) and labels["Medium"] == bands.Count(1, 1)
    assert not bands.honest(labels)
    honest_rows = [
        _row("a-1", "A", _item("b1-0001", 0.55)),
        _row("a-2", "A", _item("b1-0009", 0.46)),
    ]
    honest_outcomes = {r.id: bands.banded(r, _edges_for, "cosine") for r in honest_rows}
    assert bands.honest(bands.label_honesty(honest_rows, honest_outcomes))


def test_one_question_apart_is_a_tie() -> None:
    assert bands.delta(bands.Count(24, 25), bands.Count(23, 25)) == "tied (-1 q)"
    assert bands.delta(bands.Count(20, 25), bands.Count(23, 25)) == "+3 q (+0.120)"
    assert bands.delta(bands.Count(0, 0), bands.Count(1, 2)) == "—"
```

- [ ] **Step 2: Run them to see them fail**

Run: `uv run pytest tests/test_eval_bands.py -q`
Expected: FAIL — `AttributeError: module 'eval.bands' has no attribute 'replay_check'` (and the others).

- [ ] **Step 3: Append to `eval/bands.py`**

```python
# ------------------------------------------------------------------------------- counting


@dataclass(frozen=True, slots=True)
class Count:
    """A rate that remembers its question count, because on sets this small one question is a
    visible step and a bare rate hides it."""

    hits: int
    n: int

    @property
    def rate(self) -> float | None:
        return None if self.n == 0 else round(self.hits / self.n, 4)


def count(flags: Iterable[bool]) -> Count:
    values = list(flags)
    return Count(sum(values), len(values))


def _mean(values: Iterable[float | None]) -> float | None:
    present = [v for v in values if v is not None]
    return None if not present else round(sum(present) / len(present), 4)


# ------------------------------------------------------------------------------- the check


@dataclass(frozen=True, slots=True)
class Mismatch:
    id: str
    replayed_held_back: bool
    actual_held_back: bool
    # True when the two runs' best scores differ: the searches are written by a model call, so
    # retrieval can drift between runs. False is the branch replay cannot see — a below-floor
    # question production still answered from the documents on file.
    retrieval_differed: bool


def replay_check(rows: Sequence[Row], against: Sequence[Row]) -> tuple[int, list[Mismatch]]:
    """Today's floor replayed from the floor-off run, against what production actually did."""
    actual = {row.id: row for row in against}
    compared, mismatches = 0, []
    for row in rows:
        real = actual.get(row.id)
        if real is None:
            continue
        compared += 1
        replayed = fixed(row).held_back
        if replayed != real.held_back:
            mismatches.append(
                Mismatch(
                    row.id, replayed, real.held_back, not _same(row.best_score, real.best_score)
                )
            )
    return compared, mismatches


def _same(a: float | None, b: float | None) -> bool:
    if a is None or b is None:
        return a is b
    return abs(a - b) < 1e-6


# ------------------------------------------------------------------------------- summaries


def leaks(row: Row, outcome: Outcome) -> list[str]:
    """Which `must_not_say` strings a visible quote prints. The rule `score.leaked` uses on an
    answer — case-insensitive substring, nothing cleverer — applied to what is now shown
    verbatim. A quote is not read by the model, but it does reach the person."""
    said = " ".join(shown.item.quote for shown in outcome.shown).casefold()
    return [phrase for phrase in row.must_not_say if phrase.casefold() in said]


def summary(
    rows: Sequence[Row], outcomes: Mapping[str, Outcome], *, listed: bool
) -> dict[str, Any]:
    """One scheme's numbers. `listed=False` for a scheme that shows no list (today), whose
    top-3 numbers are not zero but meaningless, and are `None`."""
    a = [(r, outcomes[r.id]) for r in rows if r.set == "A"]
    b = [(r, outcomes[r.id]) for r in rows if r.set == "B"]
    c = [(r, outcomes[r.id]) for r in rows if r.set == "C"]
    answered = [r for r, o in a if o.generated and not o.held_back]
    return {
        "answered_a": count(o.generated and not o.held_back for _, o in a),
        "top3_hit_a": (
            count(any(s.item.doc == r.must_cite_doc for s in o.shown) for r, o in a)
            if listed
            else None
        ),
        "right_in_high_a": (
            count(
                any(s.item.doc == r.must_cite_doc and s.band == "High" for s in o.shown)
                for r, o in a
            )
            if listed
            else None
        ),
        "nothing_shown_a": count(o.held_back and not o.shown for _, o in a),
        "faithfulness_a": _mean(r.faithfulness for r in answered),
        "answer_relevancy_a": _mean(r.answer_relevancy for r in answered),
        "abstention_b": count(o.held_back for _, o in b),
        "nothing_shown_b": count(o.held_back and not o.shown for _, o in b),
        "bands_shown_b": dict(Counter(s.band for _, o in b for s in o.shown)),
        "leaked_via_quote_c": {r.id: found for r, o in c if (found := leaks(r, o))},
    }


def label_honesty(rows: Sequence[Row], outcomes: Mapping[str, Outcome]) -> dict[Band, Count]:
    """Of the Set A items shown under each label, how many are the right document."""
    flags: dict[Band, list[bool]] = {band: [] for band in BANDS}
    for row in rows:
        if row.set != "A":
            continue
        for shown in outcomes[row.id].shown:
            flags[shown.band].append(shown.item.doc == row.must_cite_doc)
    return {band: count(values) for band, values in flags.items()}


def honest(labels: Mapping[Band, Count]) -> bool:
    """High is right more often than Medium, and Medium than Low, over the bands that occur."""
    rates = [labels[band].rate for band in BANDS if labels[band].n]
    present = [rate for rate in rates if rate is not None]
    return all(upper > lower for upper, lower in pairwise(present))


def delta(today: Count, banded: Count) -> str:
    """The movement, in questions first. One question is the set's step, so it is a tie."""
    if today.n == 0 or banded.n == 0:
        return "—"
    moved = banded.hits - today.hits
    if abs(moved) <= 1:
        return f"tied ({moved:+d} q)"
    return f"{moved:+d} q ({(banded.rate or 0.0) - (today.rate or 0.0):+.3f})"
```

- [ ] **Step 4: Run them to see them pass**

Run: `uv run ruff format eval/bands.py tests/test_eval_bands.py && uv run pytest tests/test_eval_bands.py -q && uv run ruff check eval/bands.py tests/test_eval_bands.py`
Expected: 16 passed.

Note on `test_the_summary_counts_each_question_once`: `a-2` shows `b1-0009` (0.46, Medium) and `b1-0001` (0.40, Low) — a hit, not in High; `b-1` at 0.38 is Low under insurance edges (hard 0.35) — shown, held back. If a count disagrees, re-derive it by hand from `INSURANCE = Edges(0.50, 0.45, 0.35)` before changing code.

- [ ] **Step 5: Commit**

```bash
git add eval/bands.py tests/test_eval_bands.py
git commit -m "eval: check the replay against production and count what each scheme shows"
```

---

### Task 5: The sweep, its reference points and the axis comparison

**Files:**
- Modify: `eval/bands.py` (append)
- Test: `tests/test_eval_bands.py` (append)

**Interfaces:**
- Consumes: `banded`, `constant`, `Edges`, `summary`, `Count`, `SWEEP`, `B_TARGET`.
- Produces:
  - `Point(edge, answered_a, abstention_b, top3_hit_a, nothing_shown_a, nothing_shown_b)` — all `Count` but `edge: float`
  - `sweep(rows: Sequence[Row], axis: Axis) -> list[Point]`
  - `reference_points(points: Sequence[Point], today_answered: Count) -> tuple[float | None, float | None]` — `(keeps_today, meets_b)`
  - `by_pack(rows: Sequence[Row]) -> dict[str, list[Row]]`
  - `axis_summary(rows: Sequence[Row], today_answered: Count) -> dict[str, dict[str, Any] | None]`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_eval_bands.py`:

```python
# ------------------------------------------------------------------------------- the sweep

SWEPT = [
    _row("a-1", "A", _item("b1-0001", 0.55, relevance=0.9)),
    _row("a-2", "A", _item("b1-0001", 0.44, relevance=0.6)),
    _row("a-3", "A", _item("b1-0001", 0.36, relevance=0.3)),
    _row("b-1", "B", _item("x-1", 0.50, relevance=0.2)),
    _row("b-2", "B", _item("x-1", 0.33, relevance=0.1)),
]


def test_a_higher_edge_answers_less_and_declines_more() -> None:
    points = bands.sweep(SWEPT, "cosine")
    assert points[0].edge == 0.30 and points[-1].edge == 0.60 and len(points) == 31
    answered = [p.answered_a.hits for p in points]
    declined = [p.abstention_b.hits for p in points]
    assert answered == sorted(answered, reverse=True)
    assert declined == sorted(declined)
    at = {p.edge: p for p in points}
    assert at[0.44].answered_a == bands.Count(2, 3)  # 0.44 is on the edge: High
    assert at[0.45].answered_a == bands.Count(1, 3)


def test_the_reference_points_are_marked_not_chosen() -> None:
    points = bands.sweep(SWEPT, "cosine")
    keeps, meets = bands.reference_points(points, today_answered=bands.Count(2, 3))
    assert keeps == 0.44  # the highest edge that still answers two of three
    assert meets == 0.51  # the lowest edge that declines both hard negatives
    assert bands.reference_points(points, bands.Count(4, 3)) == (None, 0.51)


def test_rows_are_grouped_by_the_pack_that_governs_them() -> None:
    rows = [
        _row("a-1", "A", _item("b1-0001", 0.5)),
        _row("a-2", "A", _item("b3-0001", 0.5, pack="iras_tax"), pack="iras_tax"),
        _row("b-1", "B"),
    ]
    assert {k: [r.id for r in v] for k, v in bands.by_pack(rows).items()} == {
        "insurance_agent": ["a-1"],
        "iras_tax": ["a-2"],
        "none": ["b-1"],
    }


def test_both_axes_are_compared_and_a_missing_one_says_so() -> None:
    both = bands.axis_summary(SWEPT, bands.Count(2, 3))
    assert both["cosine"] is not None and both["relevance"] is not None
    assert both["cosine"]["keeps_today"] == 0.44
    cosine_only = [_row("a-1", "A", _item("b1-0001", 0.5))]
    assert bands.axis_summary(cosine_only, bands.Count(1, 1))["relevance"] is None
```

- [ ] **Step 2: Run them to see them fail**

Run: `uv run pytest tests/test_eval_bands.py -q -k "edge or reference or grouped or axes"`
Expected: FAIL — `AttributeError: module 'eval.bands' has no attribute 'sweep'`.

- [ ] **Step 3: Append to `eval/bands.py`**

```python
# ------------------------------------------------------------------------------- the sweep


@dataclass(frozen=True, slots=True)
class Point:
    """One edge, used as all three at once. Whether the model writes depends only on the High
    edge and what is visible only on the hard edge, so one sweep answers both questions."""

    edge: float
    answered_a: Count
    abstention_b: Count
    top3_hit_a: Count
    nothing_shown_a: Count
    nothing_shown_b: Count


def sweep(rows: Sequence[Row], axis: Axis) -> list[Point]:
    start, stop, step = SWEEP[axis]
    points: list[Point] = []
    for i in range(round((stop - start) / step) + 1):
        edge = round(start + i * step, 4)
        edges_for = constant(Edges(edge, edge, edge))
        outcomes = {row.id: banded(row, edges_for, axis) for row in rows}
        s = summary(rows, outcomes, listed=True)
        points.append(
            Point(
                edge,
                s["answered_a"],
                s["abstention_b"],
                s["top3_hit_a"],
                s["nothing_shown_a"],
                s["nothing_shown_b"],
            )
        )
    return points


def reference_points(
    points: Sequence[Point], today_answered: Count
) -> tuple[float | None, float | None]:
    """The highest edge that keeps today's Set A answered count, and the lowest that meets Set
    B's target. Marked for a person to read; neither is chosen here."""
    keeps = [p.edge for p in points if p.answered_a.n and p.answered_a.hits >= today_answered.hits]
    meets = [p.edge for p in points if (p.abstention_b.rate or 0.0) >= B_TARGET]
    return (max(keeps) if keeps else None, min(meets) if meets else None)


def by_pack(rows: Sequence[Row]) -> dict[str, list[Row]]:
    """Rows by the pack whose floor governs them; `none` for a question nothing was read for."""
    groups: dict[str, list[Row]] = {}
    for row in rows:
        groups.setdefault(row.governing_pack or "none", []).append(row)
    return groups


def axis_summary(rows: Sequence[Row], today_answered: Count) -> dict[str, dict[str, Any] | None]:
    """Cosine against relevance, at the same two reference points. `None` for an axis the run
    did not record — relevance needs the cross-encoder."""
    result: dict[str, dict[str, Any] | None] = {}
    axes: tuple[Axis, ...] = ("cosine", "relevance")
    for axis in axes:
        if not any(item.score(axis) is not None for row in rows for item in row.items):
            result[axis] = None
            continue
        points = sweep(rows, axis)
        keeps, meets = reference_points(points, today_answered)
        at = {p.edge: p for p in points}
        result[axis] = {
            "keeps_today": keeps,
            "abstention_b_there": at[keeps].abstention_b if keeps is not None else None,
            "meets_b": meets,
            "answered_a_there": at[meets].answered_a if meets is not None else None,
        }
    return result
```

- [ ] **Step 4: Run them to see them pass**

Run: `uv run ruff format eval/bands.py tests/test_eval_bands.py && uv run pytest tests/test_eval_bands.py -q && uv run ruff check eval/bands.py tests/test_eval_bands.py`
Expected: 20 passed.

How `meets == 0.51` comes out: `b-1` is at 0.50, so it is High (answered, not held back) at every edge up to 0.50 and has no visible item above 0.50; `b-2` (0.33) is held back from 0.34 on. Both held back first at 0.51.

- [ ] **Step 5: Commit**

```bash
git add eval/bands.py tests/test_eval_bands.py
git commit -m "eval: sweep the band edges per pack and compare cosine with relevance"
```

---

### Task 6: The report, the CLI and the README

**Files:**
- Modify: `eval/bands.py` (append `Report`, `compute`, `render`, `as_json`, `parse_edge`, `edges_for_packs`, `main`)
- Modify: `eval/README.md` (new section after "Extraction F1 by document type")
- Test: `tests/test_eval_bands.py` (append)

**Interfaces:**
- Consumes: everything from Tasks 3–5; `eval.report.PLACEHOLDER`, `eval.report._paragraph(target: Path) -> str`.
- Produces:
  - `parse_edge(text: str) -> dict[str, float]` (`"*"` is every pack not named)
  - `edges_for_packs(high, medium, hard: Mapping[str, float]) -> EdgesFor`
  - `Report` dataclass; `compute(rows, against, edges_for, axis) -> Report`
  - `render(report: Report, run: Mapping[str, Any], inputs: Mapping[str, Any], paragraph: str) -> str`
  - `as_json(report: Report) -> dict[str, Any]`
  - `main(argv: Sequence[str] | None = None) -> int`; `python -m eval.bands`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_eval_bands.py`:

```python
# ------------------------------------------------------------------------------- the CLI


def test_an_edge_can_be_given_for_every_pack_for_one_or_both() -> None:
    assert bands.parse_edge("0.50") == {"*": 0.50}
    assert bands.parse_edge("0.50,iras_tax=0.48") == {"*": 0.50, "iras_tax": 0.48}
    edges_for = bands.edges_for_packs(
        {"insurance_agent": 0.52}, {"insurance_agent": 0.45}, {"insurance_agent": 0.35}
    )
    assert edges_for("insurance_agent") == Edges(0.52, 0.45, 0.35)
    with pytest.raises(bands.NotReplayable, match="iras_tax"):
        edges_for("iras_tax")


def _line(row: Row) -> dict[str, object]:
    return {
        "id": row.id,
        "set": row.set,
        "held_back": row.held_back,
        "correct": row.correct,
        "best_score": row.best_score,
        "governing_pack": row.governing_pack,
        "floor_in_force": row.floor_in_force,
        "must_cite_doc": row.must_cite_doc,
        "must_not_say": list(row.must_not_say),
        "faithfulness": row.faithfulness,
        "ranked": [
            {
                "doc": i.doc,
                "page": i.page,
                "cosine": i.cosine,
                "relevance": i.relevance,
                "pack": i.pack,
                "quote": i.quote,
            }
            for i in row.items
        ],
    }


def _files(tmp_path: Path) -> tuple[Path, Path]:
    run = {"corpus_manifest_sha": "abc", "generator": "g", "judge": None, "git_sha": "s"}
    source = tmp_path / "floor-off.json"
    source.write_text(
        json.dumps({"run": {**run, "floor": "off"}, "per_question": [_line(r) for r in SWEPT]})
    )
    against = tmp_path / "production.json"
    against.write_text(
        json.dumps({"run": {**run, "floor": "pack"}, "per_question": [_line(r) for r in SWEPT]})
    )
    return source, against


def _args(source: Path, against: Path, out: Path, high: str = "0.50") -> list[str]:
    return [
        str(source),
        "--against",
        str(against),
        "--high",
        high,
        "--medium",
        "0.42",
        "--hard",
        "0.35",
        "--label",
        "t",
        "--out",
        str(out),
    ]


def test_the_report_is_written_and_a_person_s_reading_survives_a_rerun(tmp_path: Path) -> None:
    source, against = _files(tmp_path)
    out = tmp_path / "results"
    assert bands.main(_args(source, against, out)) == 0
    note = next(out.glob("*-bands-t.md"))
    text = note.read_text(encoding="utf-8")
    for heading in (
        "## Replay check",
        "## Today against banded",
        "## Set C: leaked via quote",
        "## Are the labels honest?",
        "## The sweep",
        "## Cosine against relevance",
        "## How to read it",
    ):
        assert heading in text
    note.write_text(text.replace(bands.PLACEHOLDER, "Written by a person."), encoding="utf-8")
    assert bands.main(_args(source, against, out)) == 0
    assert "Written by a person." in note.read_text(encoding="utf-8")
    saved = json.loads(next(out.glob("*-bands-t.json")).read_text(encoding="utf-8"))
    assert saved["inputs"]["high"] == "0.50" and saved["replay_check"]["compared"] == 5


def test_different_inputs_under_the_same_label_are_refused(tmp_path: Path) -> None:
    source, against = _files(tmp_path)
    out = tmp_path / "results"
    assert bands.main(_args(source, against, out)) == 0
    assert bands.main(_args(source, against, out, high="0.55")) == 2


def test_a_production_run_is_not_replayed_and_a_floor_off_one_is_not_the_check(
    tmp_path: Path,
) -> None:
    source, against = _files(tmp_path)
    out = tmp_path / "results"
    assert bands.main(_args(against, against, out)) == 2
    assert bands.main(_args(source, source, out)) == 2
```

- [ ] **Step 2: Run them to see them fail**

Run: `uv run pytest tests/test_eval_bands.py -q -k "edge_can or report_is or same_label or not_replayed"`
Expected: FAIL — `AttributeError: module 'eval.bands' has no attribute 'parse_edge'`.

- [ ] **Step 3: Append to `eval/bands.py`**

```python
# ------------------------------------------------------------------------------- edges


def parse_edge(text: str) -> dict[str, float]:
    """`0.50` for every pack, `insurance_agent=0.52,iras_tax=0.48` per pack, or both."""
    edges: dict[str, float] = {}
    for part in (p.strip() for p in text.split(",")):
        if part:
            name, _, value = part.rpartition("=")
            edges[name or "*"] = float(value)
    return edges


def edges_for_packs(
    high: Mapping[str, float], medium: Mapping[str, float], hard: Mapping[str, float]
) -> EdgesFor:
    def pick(edge: Mapping[str, float], pack: str) -> float:
        if pack in edge:
            return edge[pack]
        if "*" in edge:
            return edge["*"]
        raise NotReplayable(
            f"no edge for pack {pack!r}: name it, or give a bare number for every pack"
        )

    def of(pack: str) -> Edges:
        return Edges(pick(high, pack), pick(medium, pack), pick(hard, pack))

    return of


# ------------------------------------------------------------------------------- the report


@dataclass
class Report:
    axis: Axis
    compared: int
    mismatches: list[Mismatch]
    today: dict[str, dict[str, Any]]  # "all" and each governing pack
    banded: dict[str, dict[str, Any]]
    labels: dict[Band, Count]
    sweeps: dict[str, list[Point]]  # per governing pack, on the chosen axis
    references: dict[str, tuple[float | None, float | None]]
    axes: dict[str, dict[str, Any] | None]
    unknown: list[str]
    capped: list[str]

    @property
    def trustworthy(self) -> bool:
        return len(self.mismatches) <= 1  # one question is the step

    @property
    def honest(self) -> bool:
        return honest(self.labels)


def compute(rows: Sequence[Row], against: Sequence[Row], edges_for: EdgesFor, axis: Axis) -> Report:
    compared, mismatches = replay_check(rows, against)
    today_out = {row.id: fixed(row) for row in rows}
    banded_out = {row.id: banded(row, edges_for, axis) for row in rows}
    packs = by_pack(rows)
    groups = {"all": list(rows), **packs}
    today = {name: summary(g, today_out, listed=False) for name, g in groups.items()}
    band = {name: summary(g, banded_out, listed=True) for name, g in groups.items()}
    sweeps = {name: sweep(g, axis) for name, g in packs.items()}
    references = {
        name: reference_points(points, today[name]["answered_a"]) for name, points in sweeps.items()
    }
    return Report(
        axis=axis,
        compared=compared,
        mismatches=mismatches,
        today=today,
        banded=band,
        labels=label_honesty(rows, banded_out),
        sweeps=sweeps,
        references=references,
        axes=axis_summary(rows, today["all"]["answered_a"]),
        unknown=sorted(o.id for o in banded_out.values() if o.unknown),
        capped=sorted(row.id for row in rows if row.capped),
    )


def _cell(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, Count):
        return "—" if value.rate is None else f"{value.rate:.3f} ({value.hits}/{value.n})"
    return f"{value:.3f}" if isinstance(value, float) else str(value)


SIDE_BY_SIDE = (
    ("Set A answered", "answered_a"),
    ("Set A top-3 hit", "top3_hit_a"),
    ("Set A right document in High", "right_in_high_a"),
    ("Set A nothing shown", "nothing_shown_a"),
    ("Set A faithfulness (answered)", "faithfulness_a"),
    ("Set A answer relevancy (answered)", "answer_relevancy_a"),
    ("Set B generated-answer abstention", "abstention_b"),
    ("Set B nothing shown", "nothing_shown_b"),
    ("Set B bands shown", "bands_shown_b"),
)


def _move(today: Any, banded_value: Any) -> str:
    if isinstance(today, Count) and isinstance(banded_value, Count):
        return delta(today, banded_value)
    if isinstance(today, float) and isinstance(banded_value, float):
        return f"{banded_value - today:+.3f} (judge noise is about 0.05)"
    return ""


def render(
    report: Report, run: Mapping[str, Any], inputs: Mapping[str, Any], paragraph: str
) -> str:
    out = [f"# bands-{inputs['label']} — {date.today().isoformat()}", ""]
    out += [
        f"Replayed from `{inputs['source']}`, checked against `{inputs['against']}`. Generator "
        f"`{run.get('generator')}`; judge `{run.get('judge') or 'none'}`; corpus "
        f"`{run.get('corpus_manifest_sha')}`; git `{run.get('git_sha')}`. Axis **{report.axis}**; "
        f"edges high `{inputs['high']}`, medium `{inputs['medium']}`, hard `{inputs['hard']}`.",
        "",
    ]
    if not report.honest:
        out += [
            "> **The labels are not honest on this run**: a higher band is not right more often "
            "than the one below it. A person would be misled by them. See *Are the labels honest?*",
            "",
        ]
    if not report.trustworthy:
        out += [
            f"> **The replay does not reproduce production**: {len(report.mismatches)} questions "
            "differ, more than one question's step. Read nothing below until *Replay check* is "
            "explained.",
            "",
        ]

    out += [
        "## Replay check",
        "",
        f"Today's fixed floor, replayed from the floor-off run: {report.compared} questions "
        f"compared with production, {len(report.mismatches)} differ.",
        "",
    ]
    for m in report.mismatches:
        said = "held back" if m.actual_held_back else "answered"
        why = (
            "retrieval differed between the runs (the searches are a model call)"
            if m.retrieval_differed
            else "same evidence: the documents-on-file branch replay cannot see"
        )
        out.append(f"- `{m.id}`: production {said}, replay did not — {why}")
    out.append("")

    out += ["## Today against banded", ""]
    for name, today in report.today.items():
        out += [
            f"### {name}",
            "",
            "| | Today (fixed floor) | Banded top 3 | Δ |",
            "|---|---|---|---|",
        ]
        for label, key in SIDE_BY_SIDE:
            t, b = today[key], report.banded[name][key]
            out.append(f"| {label} | {_cell(t)} | {_cell(b)} | {_move(t, b)} |")
        out.append("")

    out += ["## Set C: leaked via quote", ""]
    leaked = report.banded["all"]["leaked_via_quote_c"]
    out += [f"- `{qid}`: {', '.join(repr(s) for s in found)}" for qid, found in leaked.items()]
    out += ["None." if not leaked else "", "These are Siew's to judge.", ""]

    out += [
        "## Are the labels honest?",
        "",
        "| Band | Right document | ",
        "|---|---|",
        *(f"| {band} | {_cell(report.labels[band])} |" for band in BANDS),
        "",
        "Honest." if report.honest else "**Not honest.**",
        "",
    ]

    out += ["## The sweep", ""]
    for name, points in report.sweeps.items():
        keeps, meets = report.references[name]
        out += [
            f"### {name} ({report.axis})",
            "",
            f"Keeps today's Set A answered count up to **{_cell(keeps)}**; meets Set B's "
            f"{B_TARGET} from **{_cell(meets)}**. Neither is chosen here.",
            "",
            "| Edge | A answered | B abstention | A top-3 hit | A nothing shown "
            "| B nothing shown |",
            "|---|---|---|---|---|---|",
        ]
        for i, p in enumerate(points):
            marked = p.edge in (keeps, meets)
            if i % 2 and not marked:
                continue
            edge = f"**{p.edge:.2f}**" if marked else f"{p.edge:.2f}"
            out.append(
                f"| {edge} | {_cell(p.answered_a)} | {_cell(p.abstention_b)} | "
                f"{_cell(p.top3_hit_a)} | {_cell(p.nothing_shown_a)} | {_cell(p.nothing_shown_b)} |"
            )
        out.append("")

    out += [
        "## Cosine against relevance",
        "",
        "| Axis | Keeps today's A at | B abstention there | Meets B's target at "
        "| A answered there |",
        "|---|---|---|---|---|",
    ]
    for axis, found in report.axes.items():
        if found is None:
            out.append(f"| {axis} | not recorded | | | |")
            continue
        out.append(
            f"| {axis} | {_cell(found['keeps_today'])} | {_cell(found['abstention_b_there'])} | "
            f"{_cell(found['meets_b'])} | {_cell(found['answered_a_there'])} |"
        )
    out.append("")

    if report.capped:
        out += [
            "## Held back by the core floor",
            "",
            f"{len(report.capped)} questions had core evidence under 0.42, which a floor-off run "
            "cannot lower: "
            + ", ".join(f"`{q}`" for q in report.capped)
            + ". "
            + (
                f"{len(report.unknown)} of them would be answered under these edges and are "
                "counted as held back — a pessimistic reading."
                if report.unknown
                else "None of them would be answered under these edges."
            ),
            "",
        ]

    out += ["## How to read it", "", paragraph or PLACEHOLDER, ""]
    return "\n".join(out)


def _plain(value: Any) -> Any:
    if isinstance(value, Count):
        return {"hits": value.hits, "n": value.n, "rate": value.rate}
    if is_dataclass(value) and not isinstance(value, type):
        return {k: _plain(v) for k, v in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_plain(v) for v in value]
    return value


def as_json(report: Report) -> dict[str, Any]:
    return {
        "axis": report.axis,
        "replay_check": {
            "compared": report.compared,
            "trustworthy": report.trustworthy,
            "mismatches": [_plain(m) for m in report.mismatches],
        },
        "today": _plain(report.today),
        "banded": _plain(report.banded),
        "labels": _plain(report.labels),
        "honest": report.honest,
        "sweeps": {
            name: [
                {"edge": p.edge, **{k: _plain(v) for k, v in vars_of(p).items()}} for p in points
            ]
            for name, points in report.sweeps.items()
        },
        "references": {
            name: {"keeps_today": keeps, "meets_b": meets}
            for name, (keeps, meets) in report.references.items()
        },
        "axes": _plain(report.axes),
        "unknown": report.unknown,
        "capped": report.capped,
    }


def vars_of(point: Point) -> dict[str, Count]:
    return {
        "answered_a": point.answered_a,
        "abstention_b": point.abstention_b,
        "top3_hit_a": point.top3_hit_a,
        "nothing_shown_a": point.nothing_shown_a,
        "nothing_shown_b": point.nothing_shown_b,
    }


# ------------------------------------------------------------------------------- the CLI


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("source", type=Path, help="a run made with `eval.run --floor-off`")
    parser.add_argument(
        "--against", type=Path, required=True, help="a production run of the same vault"
    )
    parser.add_argument("--high", required=True)
    parser.add_argument("--medium", required=True)
    parser.add_argument("--hard", required=True)
    parser.add_argument("--axis", choices=["cosine", "relevance"], default="cosine")
    parser.add_argument("--label", required=True, help="what these edges are; part of the name")
    parser.add_argument("--out", type=Path, default=ROOT / "eval" / "results")
    args = parser.parse_args(argv)
    axis: Axis = args.axis

    try:
        run, rows = load(args.source)
        against_run, against = load(args.against)
        if run.get("floor") != "off":
            raise NotReplayable(
                f"{args.source} was not run with --floor-off: below the floor it holds no "
                "answers to replay"
            )
        if against_run.get("floor") == "off":
            raise NotReplayable(f"{args.against} is a floor-off run; the check needs production")
        if run.get("corpus_manifest_sha") != against_run.get("corpus_manifest_sha"):
            raise NotReplayable("the two runs read different corpora, so they do not compare")
        edges_for = edges_for_packs(
            parse_edge(args.high), parse_edge(args.medium), parse_edge(args.hard)
        )
        for pack in sorted({item.pack for row in rows for item in row.items}):
            edges_for(pack)
        if not any(item.score(axis) is not None for row in rows for item in row.items):
            raise NotReplayable(f"no {axis} score was recorded in {args.source}")
    except (NotReplayable, ValueError) as error:
        print(error)
        return 2

    inputs = {
        "source": str(args.source),
        "against": str(args.against),
        "high": args.high,
        "medium": args.medium,
        "hard": args.hard,
        "axis": axis,
        "label": args.label,
    }
    stem = args.out / f"{date.today().isoformat()}-bands-{args.label}"
    target, note = Path(f"{stem}.json"), Path(f"{stem}.md")
    if target.exists() and json.loads(target.read_text(encoding="utf-8")).get("inputs") != inputs:
        print(
            f"{target} was written from different inputs and results are append-only. "
            "Choose another --label."
        )
        return 2

    report = compute(rows, against, edges_for, axis)
    args.out.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps({"inputs": inputs, **as_json(report)}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    note.write_text(render(report, run, inputs, _paragraph(note)), encoding="utf-8")
    print(f"wrote {note}")
    if not report.trustworthy:
        print(f"replay differs from production on {len(report.mismatches)} questions — read it")
    if not report.honest:
        print("the labels are not honest on this run — read it")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run them to see them pass**

Run: `uv run ruff format eval/ tests/ && uv run pytest tests/test_eval_bands.py -q && uv run ruff check eval/ tests/`
Expected: 24 passed; ruff clean.

- [ ] **Step 5: Add the README section**

In `eval/README.md`, after the "Extraction F1 by document type" section and before "## Writing questions", add:

~~~markdown
## Banded replay

```
uv run python -m eval.run --corpus all --floor-off --judge <judge> --label floor-off
uv run python -m eval.run --corpus all --no-judge --label production
uv run python -m eval.bands eval/results/<date>-floor-off.json \
    --against eval/results/<date>-production.json \
    --high 0.50 --medium 0.42 --hard 0.35 --axis cosine --label first-look
```

Today the gate answers when the best passage clears the governing pack's `abstain_below`, and
otherwise says nothing. `eval.bands` replays that, and a banded top 3 beside it — up to three
documents labelled High, Medium or Low, a generated answer only when the first is High, nothing
below `--hard` — from one floor-off run. It is a companion report, not a tenth metric: Set B's
headline is still the fraction held back, defined as above.

Three things it says before any number: whether replaying today's floor reproduces the
production run (`--against`), whether the labels are honest (High right more often than Medium,
Medium than Low), and which forbidden Set C strings a *quote* now puts on screen. The sweep marks
the edge that keeps today's Set A answered count and the edge that meets Set B's 0.95; it chooses
neither. Edges fitted here are fitted to the golden sets, so the chosen ones are confirmed once on
the holdout vault before anyone quotes them. Design:
`docs/superpowers/specs/2026-10-14-banded-abstention-eval-design.md`.
~~~

- [ ] **Step 6: Run the full gate**

Run: `make check`
Expected: passes.

- [ ] **Step 7: Commit**

```bash
git add eval/bands.py tests/test_eval_bands.py eval/README.md
git commit -m "eval: write the banded replay report beside today's floor"
```

**PR 2 ends here.** Its description says what the report contains and that it has not yet been run on a real vault.

---

### Task 7: The runs and the first report (workstation)

Needs Postgres with the vault loaded, Ollama serving the generator and the judge, and the reranker weights. Use the same judge as run 2 (`qwen2.5:7b-instruct`) so metrics 1–4 are comparable.

**Files:**
- Create: `eval/results/<date>-production.json` / `.md`, `eval/results/<date>-floor-off.json` / `.md`, `eval/results/<date>-bands-<label>.json` / `.md`

- [ ] **Step 1: Check the pieces fit on a quick run**

```bash
uv run python -m eval.run --corpus all --subset 25 --floor-off --no-judge --out /tmp/parrot-eval --label floor-off
uv run python -m eval.run --corpus all --subset 25 --no-judge --out /tmp/parrot-eval --label production
uv run python -m eval.bands /tmp/parrot-eval/$(date +%F)-floor-off.json --against /tmp/parrot-eval/$(date +%F)-production.json --high 0.50 --medium 0.42 --hard 0.35 --label smoke --out /tmp/parrot-eval
```

Expected: each exits 0; the `.md` opens with no "not honest" or "does not reproduce" banner, or the banner is explained before continuing.

- [ ] **Step 2: The production run, code-scored**

Run: `uv run python -m eval.run --corpus all --no-judge --label production-for-replay`
Expected: writes `eval/results/<date>-production-for-replay.json`.

- [ ] **Step 3: The floor-off run, judged, the same day on the same vault**

Run: `uv run python -m eval.run --corpus all --floor-off --judge qwen2.5:7b-instruct --label floor-off`
Expected: writes `eval/results/<date>-floor-off.json` with `run.floor: "off"`; note `run.core_floor_capped`.

- [ ] **Step 4: A first look at the sweep**

Run: `uv run python -m eval.bands eval/results/<date>-floor-off.json --against eval/results/<date>-production-for-replay.json --high 0.45 --medium 0.42 --hard 0.35 --label first-look`
Read: the replay check, the label table, both packs' sweeps, the axis comparison.

- [ ] **Step 5: Choose edges per pack — a person's decision**

Stop and show Yew Mun the sweep and the two marked points per pack. The edges are chosen by them, not by the agent. Then run `eval.bands` again with the chosen `--high/--medium/--hard` (per pack where they differ) and `--label chosen`.

- [ ] **Step 6: Write "How to read it"**

Yew Mun writes the paragraph under "## How to read it" in `eval/results/<date>-bands-chosen.md`: what moved against today, whether the labels are honest, the Set C quote leaks for Siew, and that the edges are fitted to the golden sets until the holdout confirms them.

- [ ] **Step 7: Commit the results**

```bash
git add eval/results/*-production-for-replay.* eval/results/*-floor-off.* eval/results/*-bands-first-look.* eval/results/*-bands-chosen.*
git commit -m "eval: the first banded replay, against today's floor on the same vault"
```

**PR 3 ends here.**

- [ ] **Step 8 (after `yew-mun/holdout-isolated-vault` merges): confirm on the holdout, once**

Run the same two `eval.run` commands against the holdout vault (see `eval/holdout.py` for how it is selected), then `eval.bands` with the chosen edges and `--label chosen-holdout`. Report the holdout number beside the fitted one. This is the only time the holdout is scored with these edges.

---

## After this plan

Not part of it, and not in Lane B: with PR 3's numbers, propose to Christian (graph), Siew (quotes from adversarial documents) and Zee (the screen) the contract change that replaces `guardrails.abstain_below` with band edges. That is a separate, reviewed pull request on `core/contracts.py`.
