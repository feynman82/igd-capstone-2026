"""The advise branch: code calculates under consent, the model explains, and the answer is recorded.

ADR 0016. The adviser, the consent book and the log are fakes, and so is the model: what is under
test is the graph's order of refusals and its two model calls, not the arithmetic
(`tests/test_advice_module.py`) or the gate's rules (`tests/test_gate.py`).

The pack is the insurance manifest with an advice block injected here. The real advice wording is
Zee's, reviewed by Siew, so it is never written into `pack.yaml` by a test.
"""

from __future__ import annotations

import hashlib
from dataclasses import replace
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest
import yaml

from core.contracts import AdviceShape, PackManifest
from core.graph.advice import AdviceRecord, Calculation, Figure, Input, Missing
from core.graph.answer import (
    CALCULATION_CITATION,
    NO_OWNER,
    Abstained,
    AdviceCard,
    AdviceWithheld,
    AnswerGraph,
    ConsentRequired,
    Declined,
    Finished,
    Sentence,
    answer_system,
)
from core.graph.scope import Subject
from core.packs import InstalledPack, pack
from core.runtime.ollama import ModelUnavailable
from modules.advice import GAP_WORDS, HELD_WORDS, INCOME_WORDS, TARGET_WORDS
from tests.test_answer_graph import PassThroughReranker, PhrasingRetriever, ScriptedOllama

ROOT = Path(__file__).resolve().parents[1]
TODAY = date(2026, 9, 15)
MARCUS = "Marcus Lim Jun Wei"
PAYSLIP, SCHEDULE = uuid4(), uuid4()

ASKED = "is my critical illness cover enough?"
DISCLAIMER = (
    "A calculation from your own documents and published guidance, not a recommendation from a "
    "licensed adviser."
)
CONSENT = (
    "I agree that Parrot may calculate advice from my household's documents and the published "
    "guidance it holds."
)
DISCLOSURE = "Where a product is named, only what both sides print is compared."

GAP_SHAPE: dict[str, Any] = {
    "id": "ci_gap",
    "calculator": "gap",
    "label": "critical illness cover gap",
    "asked": ["critical illness", "critical illness cover enough"],
    "facts": [
        {
            "role": "income",
            "pack": "iras_tax",
            "doc_types": ["payslip"],
            "field": "gross_salary",
            "per": "month",
            "missing": "A recent payslip, to know your income.",
        },
        {
            "role": "held",
            "doc_types": ["policy_schedule"],
            "field": "sum_insured",
            "category": "critical_illness",
            "take": "sum",
            "missing": "The schedule of each critical illness plan you hold.",
        },
    ],
    "rules": [
        {
            "role": "multiple",
            "key": "ci_multiple",
            "missing": "Reviewed guidance on how much cover to hold.",
        }
    ],
    "disadvantages": ["A larger sum insured is paid for with a higher premium."],
    "never_say": ["guaranteed payout"],
}


def advised_pack() -> InstalledPack:
    raw = yaml.safe_load((ROOT / "packs/insurance_agent/pack.yaml").read_text(encoding="utf-8"))
    raw["answering"] = {
        "categories": {
            "match_field": "product_name",
            "noun": "policies",
            "rules": [
                {
                    "id": "critical_illness",
                    "label": "critical illness plan",
                    "printed": ["critical illness"],
                }
            ],
        }
    }
    raw["grounding"] = {
        "corpus": None,
        "top_k": 0,
        "values": [
            {
                "key": "ci_multiple",
                "unit": "multiple",
                "description": "Multiple of annual income a household is guided to hold as cover",
                "qualifiers": ["age_band"],
            }
        ],
    }
    raw["advice"] = {
        "consent_version": "1.0.0",
        "consent_text": CONSENT,
        "disclaimer": DISCLAIMER,
        "product_disclosure": DISCLOSURE,
        "shapes": [GAP_SHAPE],
    }
    return InstalledPack(PackManifest.model_validate(raw), {}, {})


INCOME = Input(
    "fact:12",
    "income",
    "gross salary",
    "SGD 9,400.00",
    "payslip-august.pdf, page 1",
    document_id=PAYSLIP,
    page=1,
)
HELD = Input(
    "fact:31",
    "held",
    "sum insured",
    "SGD 200,000.00",
    "careshield-schedule.pdf, page 2",
    document_id=SCHEDULE,
    page=2,
)
MULTIPLE = Input(
    "rule:7",
    "multiple",
    "ci multiple",
    "4 times",
    "Publisher, Guide title, 26 September 2023",
    publisher="Publisher",
    title="Guide title",
    dated="26 September 2023",
    url="https://example.gov.sg/guide",
)
VERDICT = (
    f"Critical illness cover gap for {MARCUS}: the published guideline works out to "
    "SGD 451,200.00, and SGD 200,000.00 is held, so the gap is SGD 251,200.00."
)
CALCULATION = Calculation(
    pack_id="insurance_agent",
    shape_id="ci_gap",
    label="critical illness cover gap",
    subject=MARCUS,
    person_ids=(1,),
    inputs=(INCOME, HELD, MULTIPLE),
    figures=(
        Figure("annual income", Decimal("112800.00"), "SGD 112,800.00", INCOME_WORDS),
        Figure("target", Decimal("451200.00"), "SGD 451,200.00", TARGET_WORDS),
        Figure("held", Decimal("200000.00"), "SGD 200,000.00", HELD_WORDS),
        Figure("gap", Decimal("251200.00"), "SGD 251,200.00", GAP_WORDS),
    ),
    verdict="short",
    verdict_text=VERDICT,
)
MISSING = Missing(
    pack_id="insurance_agent",
    shape_id="ci_gap",
    label="critical illness cover gap",
    subject=MARCUS,
    items=("A recent payslip, to know your income.", "which age band applies"),
)

# Evidence order in the explain prompt: [1] fact:12, [2] fact:31, [3] rule:7, [4] calculation:0.
THE_GAP = {"text": "The gap is SGD 251,200.00.", "supports": [4]}
THE_GUIDELINE = {
    "text": "The guideline is 4 times the annual income of SGD 112,800.00.",
    "supports": [3, 4],
}


# ---------------------------------------------------------------------------------- fakes


class Household:
    def __init__(self, subject: Subject) -> None:
        self.subject = subject

    def whose(self, question: str) -> Subject:
        return self.subject

    def apply(self, question: str, passages: Any) -> Any:
        raise AssertionError("advice never scopes retrieved passages: nothing is retrieved")


class Adviser:
    def __init__(self, result: Calculation | Missing) -> None:
        self.result = result
        self.calls: list[dict[str, Any]] = []

    def calculate(
        self,
        installed: InstalledPack,
        shape: AdviceShape,
        *,
        person_ids: frozenset[int],
        subject: str,
        today: date,
    ) -> Calculation | Missing:
        self.calls.append(
            {"shape": shape.id, "person_ids": person_ids, "subject": subject, "today": today}
        )
        return self.result


class Consents:
    def __init__(self, consent_id: int | None) -> None:
        self.consent_id = consent_id
        self.asked: list[tuple[str, str]] = []

    def current(self, pack_id: str, version: str) -> int | None:
        self.asked.append((pack_id, version))
        return self.consent_id


class Log:
    def __init__(self) -> None:
        self.records: list[AdviceRecord] = []

    def record(self, entry: AdviceRecord) -> None:
        self.records.append(entry)


OWNER = Subject(frozenset({1}), MARCUS)


def build(
    client: ScriptedOllama,
    *,
    result: Calculation | Missing = CALCULATION,
    consent_id: int | None = 41,
    subject: Subject | None = OWNER,
    packs: list[InstalledPack] | None = None,
) -> tuple[AnswerGraph, Adviser, Consents, Log, PhrasingRetriever]:
    adviser, consents, log = Adviser(result), Consents(consent_id), Log()
    retriever = PhrasingRetriever({})
    graph = AnswerGraph(
        client,
        retriever,
        PassThroughReranker(),
        household=Household(subject) if subject is not None else None,  # type: ignore[arg-type]
        today=TODAY,
        packs=packs if packs is not None else [advised_pack()],
        adviser=adviser,
        consents=consents,
        advice_log=log,
    )
    return graph, adviser, consents, log, retriever


# ------------------------------------------------------------------------------ the tests


def test_advice_without_consent_asks_for_it_and_does_nothing_else() -> None:
    client = ScriptedOllama({"intent": "advise"})
    graph, adviser, consents, log, retriever = build(client, consent_id=None)

    got = list(graph.stream(ASKED))

    assert [type(event) for event in got] == [ConsentRequired]
    required = got[0]
    assert isinstance(required, ConsentRequired)
    assert required.consent_text == CONSENT
    assert required.version == "1.0.0"
    assert required.disclaimer == DISCLAIMER
    assert required.label == "critical illness cover gap"
    assert consents.asked == [("insurance_agent", "1.0.0")]
    assert len(client.systems) == 1, "only the router ran"
    assert adviser.calls == [], "nothing is calculated before consent"
    assert log.records == [], "a refusal for want of consent has no consent id to record"
    assert retriever.queries == []


def test_a_missing_input_is_named_recorded_and_never_explained() -> None:
    client = ScriptedOllama({"intent": "advise"})
    graph, _, _, log, _ = build(client, result=MISSING)

    got = list(graph.stream(ASKED))

    assert [type(event) for event in got] == [AdviceWithheld]
    withheld = got[0]
    assert isinstance(withheld, AdviceWithheld)
    assert withheld.missing == list(MISSING.items)
    assert withheld.person == MARCUS
    assert withheld.disclaimer == DISCLAIMER
    assert len(client.systems) == 1, "the answer model is never called"
    [record] = log.records
    assert record.outcome == "withheld" and record.verdict is None
    assert record.consent_id == 41
    assert record.basis == {"missing": list(MISSING.items)}


def test_a_calculation_gives_the_card_then_gated_sentences_then_finished() -> None:
    client = ScriptedOllama({"intent": "advise"}, {"sentences": [THE_GAP, THE_GUIDELINE]})
    graph, adviser, _, log, retriever = build(client)
    installed = advised_pack()

    got = list(graph.stream(ASKED, thread_id="t-1"))

    assert [type(event) for event in got] == [AdviceCard, Sentence, Sentence, Finished]
    card = got[0]
    assert isinstance(card, AdviceCard)
    assert card.verdict_text == VERDICT
    assert card.verdict == "short"
    assert ("gap", "SGD 251,200.00") in card.figures
    assert card.product_disclosure == "", "no product is named"
    assert card.consent_version == "1.0.0"
    assert card.person == MARCUS

    assert len(client.systems) == 2, "route and explain, nothing else"
    assert client.systems[1] == answer_system(installed)
    assert retriever.queries == [], "advice retrieves nothing"
    assert adviser.calls == [
        {"shape": "ci_gap", "person_ids": frozenset({1}), "subject": MARCUS, "today": TODAY}
    ]

    prompt = client.prompts[1]
    assert prompt.startswith("Today is 15 September 2026.")
    assert "Explain this worked result to Marcus Lim Jun Wei in at most three sentences." in prompt
    assert f"Verdict: {VERDICT}" in prompt
    assert "Points to mention if relevant:\n- A larger sum insured" in prompt
    assert "None, page 0" not in prompt and "doc-" not in prompt

    finished = got[-1]
    assert isinstance(finished, Finished)
    assert finished.disclaimer == DISCLAIMER
    assert finished.dropped == 0 and not finished.unanswered

    [record] = log.records
    assert record.outcome == "advised" and record.verdict == "short"
    assert record.thread_id == "t-1" and record.consent_id == 41
    assert record.shape == "ci_gap" and record.person_ids == (1,)
    assert [item["ref"] for item in record.basis["inputs"]] == ["fact:12", "fact:31", "rule:7"]
    assert record.basis["inputs"][2]["citation"] == MULTIPLE.citation
    assert [figure["name"] for figure in record.basis["figures"]] == [
        "annual income",
        "target",
        "held",
        "gap",
    ]
    assert record.basis["kept"] == [THE_GAP["text"], THE_GUIDELINE["text"]]
    assert record.basis["explanation"] == "complete"
    assert record.answer_text == f"{VERDICT} {THE_GAP['text']} {THE_GUIDELINE['text']}"
    assert CALCULATION_CITATION not in finished.citations, (
        "not a source a screen can open; scripts/ask.py must not print it"
    )


def test_a_verdict_in_the_explanation_is_dropped_and_the_figure_kept() -> None:
    client = ScriptedOllama(
        {"intent": "advise"},
        {"sentences": [{"text": "You should buy more.", "supports": [4]}, THE_GAP]},
    )
    graph, _, _, log, _ = build(client)

    got = list(graph.stream(ASKED))

    assert [e.text for e in got if isinstance(e, Sentence)] == ["The gap is SGD 251,200.00."]
    finished = got[-1]
    assert isinstance(finished, Finished) and finished.dropped == 1
    assert log.records[0].basis["dropped"][0]["text"] == "You should buy more."


def test_the_explanation_stops_at_three_sentences() -> None:
    client = ScriptedOllama({"intent": "advise"}, {"sentences": [THE_GAP] * 5})
    graph, *_ = build(client)

    got = list(graph.stream(ASKED))

    assert sum(isinstance(event, Sentence) for event in got) == 3
    assert isinstance(got[-1], Finished) and got[-1].truncated


def test_a_pack_without_advice_still_declines_with_every_port_wired() -> None:
    client = ScriptedOllama({"intent": "advise"})
    graph, adviser, consents, log, _ = build(client, packs=[pack("insurance_agent")])

    got = list(graph.stream(ASKED))

    assert [type(event) for event in got] == [Declined]
    assert adviser.calls == [] and consents.asked == [] and log.records == []


def test_a_question_no_shape_asks_for_is_declined() -> None:
    client = ScriptedOllama({"intent": "advise"})
    graph, adviser, consents, _, _ = build(client)

    got = list(graph.stream("should i switch my car insurance?"))

    assert [type(event) for event in got] == [Declined]
    assert adviser.calls == [] and consents.asked == []
    assert len(client.systems) == 1


def test_advice_is_declined_when_the_graph_was_given_no_adviser() -> None:
    client = ScriptedOllama({"intent": "advise"})
    graph = AnswerGraph(
        client, PhrasingRetriever({}), PassThroughReranker(), packs=[advised_pack()]
    )

    assert [type(event) for event in graph.stream(ASKED)] == [Declined]


def test_ask_leads_with_the_verdict_on_the_calculation_path() -> None:
    client = ScriptedOllama({"intent": "advise"}, {"sentences": [THE_GAP]})
    graph, *_ = build(client)

    answer = graph.ask(ASKED)

    assert answer.advice and answer.grounded
    assert answer.text.startswith(VERDICT)
    assert answer.verdict_text == VERDICT
    assert "The gap is SGD 251,200.00." in answer.text
    assert MULTIPLE.citation in answer.citations
    assert answer.disclaimer == DISCLAIMER


def test_ask_maps_consent_and_withheld_to_their_own_flags() -> None:
    graph, *_ = build(ScriptedOllama({"intent": "advise"}), consent_id=None)
    consent = graph.ask(ASKED)
    assert consent.consent_required and not consent.grounded
    assert consent.text == CONSENT

    graph, *_ = build(ScriptedOllama({"intent": "advise"}), result=MISSING)
    withheld = graph.ask(ASKED)
    assert withheld.withheld and not withheld.grounded
    assert withheld.text == (
        "Critical illness cover gap cannot be worked out yet. "
        "A recent payslip, to know your income. Which age band applies."
    )


# ------------------------------------------------------------------------ whose situation


def test_an_ambiguous_subject_asks_whose_and_is_never_calculated() -> None:
    client = ScriptedOllama({"intent": "advise"})
    graph, adviser, consents, log, _ = build(
        client, subject=Subject(frozenset(), "", ambiguous=True)
    )

    got = list(graph.stream("is our critical illness cover enough?"))

    assert [type(event) for event in got] == [Abstained]
    abstained = got[0]
    assert isinstance(abstained, Abstained)
    assert abstained.reason == "the question could be about more than one person"
    assert abstained.missing == "Name one person, then ask again."
    assert (abstained.passages_read, abstained.dropped, abstained.person) == (0, 0, None)
    assert abstained.disclaimer == DISCLAIMER
    assert adviser.calls == [] and consents.asked == [] and log.records == []
    assert len(client.systems) == 1


def test_ask_reads_naturally_for_an_ambiguous_subject() -> None:
    graph, *_ = build(
        ScriptedOllama({"intent": "advise"}), subject=Subject(frozenset(), "", ambiguous=True)
    )

    answer = graph.ask("is our critical illness cover enough?")

    assert answer.text == (
        "I can't answer that from your documents: the question could be about more than one "
        "person. Name one person, then ask again."
    )
    assert not answer.grounded and answer.disclaimer == DISCLAIMER


def test_nobody_having_said_who_they_are_withholds_advice() -> None:
    graph, adviser, consents, log, _ = build(ScriptedOllama({"intent": "advise"}), subject=None)

    got = list(graph.stream(ASKED))

    assert [type(event) for event in got] == [AdviceWithheld]
    withheld = got[0]
    assert isinstance(withheld, AdviceWithheld)
    assert withheld.missing == [NO_OWNER] and withheld.person is None
    assert adviser.calls == [] and consents.asked == [] and log.records == []


def test_a_relation_nobody_holds_abstains_as_an_explanation_would() -> None:
    graph, adviser, *_ = build(
        ScriptedOllama({"intent": "advise"}),
        subject=Subject(frozenset(), "", unknown_relation="son"),
    )

    got = list(graph.stream("is my son's critical illness cover enough?"))

    assert [type(event) for event in got] == [Abstained]
    assert "who your son is" in got[0].reason  # type: ignore[union-attr]
    assert adviser.calls == []


def test_advice_about_someone_else_is_explained_to_the_asker_about_them() -> None:
    client = ScriptedOllama({"intent": "advise"}, {"sentences": [THE_GAP]})
    rachel = Subject(frozenset({2}), "Rachel Ng Hui Shan", someone_else=True)
    for_rachel = replace(CALCULATION, person_ids=(2,), subject="Rachel Ng Hui Shan")
    graph, adviser, *_ = build(client, subject=rachel, result=for_rachel)

    list(graph.stream("is Rachel's critical illness cover enough?"))

    prompt = client.prompts[1]
    assert "The result is about Rachel Ng Hui Shan, not the person asking" in prompt
    assert 'write "Rachel Ng Hui Shan\'s", not "your"' in prompt
    assert "to the person asking, about Rachel Ng Hui Shan" in prompt
    assert "The person asking is Rachel" not in prompt
    assert adviser.calls[0]["person_ids"] == frozenset({2})


# ---------------------------------------------------------------------------------- chips


def test_card_chips_are_built_from_each_input_not_from_a_passage() -> None:
    client = ScriptedOllama({"intent": "advise"}, {"sentences": [THE_GUIDELINE]})
    graph, *_ = build(client)

    got = list(graph.stream(ASKED))

    card = got[0]
    assert isinstance(card, AdviceCard)
    fact, _, rule = card.inputs
    assert (fact.kind, fact.text, fact.document_id, fact.page) == (
        "fact",
        "payslip-august.pdf, page 1",
        PAYSLIP,
        1,
    )
    assert rule.kind == "rule"
    assert rule.text == "Publisher, Guide title, 26 September 2023"
    assert (rule.publisher, rule.title, rule.dated, rule.url) == (
        "Publisher",
        "Guide title",
        "26 September 2023",
        "https://example.gov.sg/guide",
    )
    texts = [c.text for c in card.inputs]
    assert not any("doc-" in text or "page 0" in text for text in texts)

    sentence = next(event for event in got if isinstance(event, Sentence))
    assert [c.text for c in sentence.citations] == [MULTIPLE.citation, CALCULATION_CITATION]
    assert sentence.citations[1].kind == "calculation"


def test_a_model_that_is_down_still_leaves_the_card_and_finishes() -> None:
    client = ScriptedOllama({"intent": "advise"}, ModelUnavailable("Ollama is not running"))
    graph, _, _, log, _ = build(client)

    got = list(graph.stream(ASKED))

    assert [type(event) for event in got] == [AdviceCard, Finished]
    finished = got[-1]
    assert isinstance(finished, Finished)
    assert finished.unanswered is False and finished.dropped == 0
    assert len(client.systems) == 2, "route, then the explanation that failed"
    [record] = log.records
    assert record.outcome == "advised" and record.basis["kept"] == []
    assert record.basis["explanation"] == "model_unavailable"
    assert record.answer_text == VERDICT


# --------------------------------------------------------------- review round 1: fix 1, recording


def test_a_stream_closed_after_the_card_still_records_what_was_shown() -> None:
    """Fix 1: a consumer that stops reading after the card and one sentence — a `GeneratorExit`
    thrown into the `yield Sentence` below the card — must not lose the advised record. Before the
    fix, `advice_log.record(...)` for the advised outcome ran only after the `try` finished
    normally or with `ModelUnavailable`, so a dropped stream recorded nothing at all."""
    client = ScriptedOllama({"intent": "advise"}, {"sentences": [THE_GAP, THE_GUIDELINE]})
    graph, _, _, log, _ = build(client)

    stream = graph.stream(ASKED)
    assert isinstance(next(stream), AdviceCard)
    sentence = next(stream)
    assert isinstance(sentence, Sentence) and sentence.text == THE_GAP["text"]
    stream.close()

    [record] = log.records
    assert record.outcome == "advised" and record.verdict == "short"
    assert record.basis["kept"] == [THE_GAP["text"]], "only the sentence actually shown"
    assert record.basis["explanation"] == "stopped"


def test_a_stream_closed_exactly_at_the_card_still_records_it() -> None:
    """C5 fix round 2. Before this fix, `yield AdviceCard(...)` sat *before* the explanation's
    `try`, so a `GeneratorExit` thrown into that `yield` — a consumer stopping right at the card,
    before it even reads a sentence — landed outside the `try` and its `finally` never ran: the
    card was shown but nothing was recorded. The card now opens the `try`, so this closes into the
    same `finally` as any later `yield Sentence` does."""
    client = ScriptedOllama({"intent": "advise"}, {"sentences": [THE_GAP, THE_GUIDELINE]})
    graph, _, _, log, _ = build(client)

    stream = graph.stream(ASKED)
    assert isinstance(next(stream), AdviceCard)
    stream.close()

    [record] = log.records
    assert record.outcome == "advised" and record.verdict == "short"
    assert record.basis["explanation"] == "stopped"
    assert record.basis["kept"] == []


def test_the_advised_record_is_never_written_twice() -> None:
    """The `finally` that writes the advised record runs exactly once per stream, whether the
    stream is drained to `Finished` or closed early — so draining it fully must still leave
    exactly one record, not one from an old code path plus one from the fix."""
    client = ScriptedOllama({"intent": "advise"}, {"sentences": [THE_GAP]})
    graph, _, _, log, _ = build(client)

    list(graph.stream(ASKED))

    assert len(log.records) == 1


# ------------------------------------------------------------------ review round 1: fix 2, safety


def test_a_never_say_phrase_is_dropped_even_when_correctly_labelled() -> None:
    """Fix 2(a). The sentence names the gap figure with its own word ("gap") and cites the
    calculation passage, so nothing but the pack's `never_say` list catches it: remove
    `never_say=shape.never_say` from the `check_advice` call and this sentence is kept."""
    client = ScriptedOllama(
        {"intent": "advise"},
        {
            "sentences": [
                {"text": "The gap is SGD 251,200.00, a guaranteed payout.", "supports": [4]}
            ]
        },
    )
    graph, *_ = build(client)

    got = list(graph.stream(ASKED))

    assert [event for event in got if isinstance(event, Sentence)] == []
    finished = got[-1]
    assert isinstance(finished, Finished) and finished.dropped == 1


def test_a_mislabelled_figure_through_the_graph_is_dropped() -> None:
    """Fix 2(c). SGD 451,200.00 is the *target*, not a gap: "short by" states it without the
    target's own words, so `check_advice`'s mislabelled-figure check drops it."""
    client = ScriptedOllama(
        {"intent": "advise"},
        {"sentences": [{"text": "You are short by SGD 451,200.00.", "supports": [4]}]},
    )
    graph, *_ = build(client)

    got = list(graph.stream(ASKED))

    assert [event for event in got if isinstance(event, Sentence)] == []
    finished = got[-1]
    assert isinstance(finished, Finished) and finished.dropped == 1


def test_a_named_product_carries_its_disclosure_and_its_hash() -> None:
    """Fix 2(b), and minor 6: `names_product=True` puts the pack's own disclosure on the card and
    in `ask()`'s disclaimer, and the record's basis carries its sha256 rather than the text a
    second time."""
    named = replace(CALCULATION, names_product=True)

    client = ScriptedOllama({"intent": "advise"}, {"sentences": [THE_GAP]})
    graph, _, _, log, _ = build(client, result=named)
    got = list(graph.stream(ASKED))
    card = got[0]
    assert isinstance(card, AdviceCard)
    assert card.product_disclosure == DISCLOSURE
    [record] = log.records
    assert (
        record.basis["product_disclosure_sha256"]
        == hashlib.sha256(DISCLOSURE.encode("utf-8")).hexdigest()
    )

    client2 = ScriptedOllama({"intent": "advise"}, {"sentences": [THE_GAP]})
    graph2, *_ = build(client2, result=named)
    answer = graph2.ask(ASKED)
    assert DISCLOSURE in answer.disclaimer


def test_no_product_named_gives_no_disclosure_or_hash() -> None:
    """Fix 2(b): `names_product=False` (the default `CALCULATION` fixture) gives an empty card
    disclosure and no hash in the record's basis."""
    client = ScriptedOllama({"intent": "advise"}, {"sentences": [THE_GAP]})
    graph, _, _, log, _ = build(client)  # CALCULATION: names_product=False

    got = list(graph.stream(ASKED))
    card = got[0]
    assert isinstance(card, AdviceCard)
    assert card.product_disclosure == ""
    [record] = log.records
    assert "product_disclosure_sha256" not in record.basis


# ------------------------------------------------------------- review round 1: minor 4, the guard


def test_a_calculation_for_the_wrong_person_is_never_shown() -> None:
    """Minor 4: `_advise` already guarantees a single-person subject before `calculate` runs, so a
    result naming a different person, pack or shape is a calculator bug — shown, it would be one
    household reading another's figures. The graph refuses to show it."""
    mismatched = replace(CALCULATION, person_ids=(99,))
    client = ScriptedOllama({"intent": "advise"})
    graph, *_ = build(client, result=mismatched)

    with pytest.raises(ValueError, match="does not match the question asked"):
        list(graph.stream(ASKED))
