"""The banded replay, on hand-built rows. No vault, no model: replay is arithmetic over a
result file, so it is tested as arithmetic."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

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
    nothing = _row("a-3", "A", held_back=True)  # no evidence: the recorded outcome
    assert [bands.fixed(r).held_back for r in (above, below, nothing)] == [False, True, True]
    assert bands.fixed(above).shown == ()


def test_a_question_with_no_evidence_keeps_its_recorded_outcome_under_both_schemes() -> None:
    answered = _row("a-1", "A", held_back=False)
    declined = _row("a-2", "A", held_back=True)
    for scheme in (bands.fixed, lambda r: bands.banded(r, _edges_for, "cosine")):
        assert scheme(answered).generated and not scheme(answered).held_back
        assert not scheme(declined).generated and scheme(declined).held_back
        assert scheme(answered).shown == ()
    assert bands.fixed(answered).kind == "answered"
    assert bands.fixed(declined).kind == "abstained"


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
        _row("a-4", "A", _item("b1-0001", 0.50)),  # replay answers
    ]
    production = [
        _row("a-1", "A", _item("b1-0001", 0.50)),
        _row("a-2", "A", _item("b1-0001", 0.40)),  # but production answered: same evidence
        _row("a-3", "A", _item("b1-0001", 0.47)),  # production searched differently
        _row("a-4", "A", _item("b1-0001", 0.50), held_back=True),  # same evidence, model declined
    ]
    compared, mismatches = bands.replay_check(floor_off, production)
    assert compared == 4
    assert [(m.id, m.cause) for m in mismatches] == [
        ("a-2", "documents on file"),
        ("a-3", "retrieval differed"),
        ("a-4", "generation differed"),
    ]
    assert [(m.replayed_held_back, m.actual_held_back) for m in mismatches] == [
        (True, False),
        (True, False),
        (False, True),
    ]


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


def test_a_forbidden_string_cannot_match_across_two_visible_quotes() -> None:
    row = _row(
        "c-1",
        "C",
        _item("x-1", 0.60, quote="pay 8,2"),
        _item("x-2", 0.59, quote="00 now"),
        must_not_say=("8,200", "8,2 00"),
    )
    outcome = bands.banded(row, _edges_for, "cosine")
    assert len(outcome.shown) == 2
    assert bands.leaks(row, outcome) == []


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


def _written(out: Path) -> tuple[str, dict[str, Any]]:
    note = next(out.glob("*-bands-t.md")).read_text(encoding="utf-8")
    saved = json.loads(next(out.glob("*-bands-t.json")).read_text(encoding="utf-8"))
    return note, saved


def _rewrite(path: Path, edit: Callable[[dict[str, Any]], object]) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    edit(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_the_checks_come_before_the_numbers(tmp_path: Path) -> None:
    source, against = _files(tmp_path)
    out = tmp_path / "results"
    assert bands.main(_args(source, against, out)) == 0
    text = _written(out)[0]
    order = [
        "## Replay check",
        "## Set C: leaked via quote",
        "## Are the labels honest?",
        "## Today against banded",
        "## The sweep",
        "## Cosine against relevance",
        "## How to read it",
    ]
    positions = [text.index(heading) for heading in order]
    assert positions == sorted(positions)


def test_a_replay_that_compared_nothing_is_not_trusted(tmp_path: Path) -> None:
    source, against = _files(tmp_path)
    _rewrite(
        against,
        lambda d: [q.update(id="other-" + str(q["id"])) for q in d["per_question"]],
    )
    out = tmp_path / "results"
    assert bands.main(_args(source, against, out)) == 0
    text, saved = _written(out)
    assert "The replay does not reproduce production" in text
    assert "0 of 5 questions compared" in text
    assert "5 of the 5 floor-off questions had no production counterpart" in text
    assert saved["replay_check"]["trustworthy"] is False
    assert saved["replay_check"]["replayed"] == 5


def test_runs_of_different_corpora_are_refused(tmp_path: Path) -> None:
    source, against = _files(tmp_path)
    _rewrite(against, lambda d: d["run"].update(corpus_manifest_sha="different"))
    assert bands.main(_args(source, against, tmp_path / "results")) == 2


def test_a_pack_with_no_edge_is_refused(tmp_path: Path) -> None:
    source, against = _files(tmp_path)

    def retarget(data: dict[str, Any]) -> None:
        for question in data["per_question"]:
            question["governing_pack"] = "iras_tax"
            for item in question["ranked"]:
                item["pack"] = "iras_tax"

    _rewrite(source, retarget)
    _rewrite(against, retarget)
    args = _args(source, against, tmp_path / "results", high="insurance_agent=0.50")
    assert bands.main(args) == 2


def test_labels_that_are_not_honest_are_said_so(tmp_path: Path) -> None:
    wrong_high = _row("a-1", "A", _item("x-1", 0.60), _item("b1-0001", 0.47), doc="b1-0001")
    source, against = _files(tmp_path)
    for path in (source, against):
        _rewrite(path, lambda d: d.update(per_question=[_line(wrong_high)]))
    out = tmp_path / "results"
    assert bands.main(_args(source, against, out)) == 0
    text, saved = _written(out)
    assert "The labels are not honest on this run" in text
    assert saved["honest"] is False


def test_a_rerun_at_another_commit_is_refused_and_at_the_same_commit_is_not(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source, against = _files(tmp_path)
    out = tmp_path / "results"
    monkeypatch.setattr(bands, "_git_sha", lambda: "a")
    assert bands.main(_args(source, against, out)) == 0
    note = next(out.glob("*-bands-t.md"))
    note.write_text(
        note.read_text(encoding="utf-8").replace(bands.PLACEHOLDER, "Written by a person."),
        encoding="utf-8",
    )
    assert "replayed by bands at `a`" in note.read_text(encoding="utf-8")
    assert bands.main(_args(source, against, out)) == 0
    assert "Written by a person." in note.read_text(encoding="utf-8")
    monkeypatch.setattr(bands, "_git_sha", lambda: "b")
    assert bands.main(_args(source, against, out)) == 2
    assert _written(out)[1]["inputs"]["bands_git_sha"] == "a"


def test_an_edge_for_a_pack_that_is_not_in_the_run_is_refused_by_name(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source, against = _files(tmp_path)
    out = tmp_path / "results"
    assert bands.main(_args(source, against, out, high="0.50,iras_taxx=0.48")) == 2
    assert "iras_taxx" in capsys.readouterr().out
    assert bands.main(_args(source, against, out, high="0.50,insurance_agent=0.48")) == 0


def test_runs_with_different_configuration_are_refused_by_key(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source, against = _files(tmp_path)
    for path, keep in ((source, 6), (against, 3)):
        _rewrite(path, lambda d, keep=keep: d["run"].update(keep=keep, candidates=20))
    assert bands.main(_args(source, against, tmp_path / "results")) == 2
    message = capsys.readouterr().out
    assert "keep" in message and "candidates" not in message


def test_a_key_missing_from_one_run_is_not_a_difference(tmp_path: Path) -> None:
    source, against = _files(tmp_path)
    _rewrite(source, lambda d: d["run"].update(keep=6))
    assert bands.main(_args(source, against, tmp_path / "results")) == 0


def test_fewer_than_two_bands_is_said_not_called_honest(tmp_path: Path) -> None:
    only_high = _row("a-1", "A", _item("b1-0001", 0.60))
    source, against = _files(tmp_path)
    for path in (source, against):
        _rewrite(path, lambda d: d.update(per_question=[_line(only_high)]))
    out = tmp_path / "results"
    assert bands.main(_args(source, against, out)) == 0
    text = _written(out)[0]
    assert "Fewer than two bands were shown, so there is nothing to compare." in text
    assert "\nHonest.\n" not in text


def test_the_sweep_prints_every_point_at_two_hundredths_and_leaves_out_no_evidence(
    tmp_path: Path,
) -> None:
    source, against = _files(tmp_path)
    nothing = _row("b-9", "B")
    for path in (source, against):
        _rewrite(path, lambda d: d["per_question"].append(_line(nothing)))
    out = tmp_path / "results"
    assert bands.main(_args(source, against, out)) == 0
    text, saved = _written(out)
    sweep = text[text.index("## The sweep") : text.index("## Cosine against relevance")]
    assert "### none" not in sweep and "none" not in saved["sweeps"]
    assert "none" not in saved["references"]
    cosine = sweep[sweep.index("### insurance_agent") :]
    assert "| 0.31 |" not in cosine and "| 0.32 |" in cosine and "| 0.34 |" in cosine
    # relevance is swept in steps of 0.02: every one is printed
    by_relevance = tmp_path / "relevance"
    assert bands.main([*_args(source, against, by_relevance), "--axis", "relevance"]) == 0
    text = _written(by_relevance)[0]
    assert "| 0.02 |" in text and "| 0.04 |" in text
