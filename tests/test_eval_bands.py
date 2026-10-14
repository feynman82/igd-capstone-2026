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
