"""The scanner that decides when a streamed sentence is finished.

Everything the Ask surface shows passes through here, so the cases that matter are the ones
where a naïve brace count would be wrong: a brace inside a quoted sentence, a quote escaped
inside one, and a delta boundary that falls in the middle of any of it. A model streams in
whatever chunk sizes it feels like, so "the delta split the object in half" is not an edge case,
it is the normal case.
"""

from __future__ import annotations

import json

import pytest

from core.graph.sentences import SentenceScanner

REPLY = {
    "sentences": [
        {"text": "Great Eastern covered the March admission.", "supports": [2]},
        {"text": "The policy number is GE-7714-2208.", "supports": [2, 5]},
    ],
    "missing": "",
}


def drip(scanner: SentenceScanner, text: str, size: int) -> list[dict[str, object]]:
    """Feed `text` in `size`-character pieces, the way a model actually arrives."""
    found: list[dict[str, object]] = []
    for start in range(0, len(text), size):
        found.extend(scanner.feed(text[start : start + size]))
    return found


def test_sentences_arrive_one_at_a_time() -> None:
    scanner = SentenceScanner()
    found = drip(scanner, json.dumps(REPLY), 7)
    assert [item["text"] for item in found] == [
        "Great Eastern covered the March admission.",
        "The policy number is GE-7714-2208.",
    ]
    assert found[1]["supports"] == [2, 5]


@pytest.mark.parametrize("size", [1, 2, 3, 5, 13, 64, 4096])
def test_the_result_does_not_depend_on_how_the_stream_was_chopped(size: int) -> None:
    """The one property that matters. A model chooses its own chunk boundaries; we cannot."""
    scanner = SentenceScanner()
    found = drip(scanner, json.dumps(REPLY), size)
    assert [item["text"] for item in found] == [item["text"] for item in REPLY["sentences"]]


def test_a_sentence_is_released_before_the_rest_has_been_written() -> None:
    """The whole point: the first sentence reaches a screen while the second is still coming."""
    scanner = SentenceScanner()
    whole = json.dumps(REPLY)
    half = whole.index("The policy number")

    early = drip(scanner, whole[:half], 8)
    assert [item["text"] for item in early] == ["Great Eastern covered the March admission."]

    late = scanner.feed(whole[half:])
    assert [item["text"] for item in late] == ["The policy number is GE-7714-2208."]


def test_a_brace_inside_a_sentence_does_not_end_it() -> None:
    """`He said {this}` is a sentence, not two objects. A brace count alone gets this wrong."""
    text = "The letter reads: pay {the balance} by 14 October."
    reply = {"sentences": [{"text": text, "supports": [1]}]}
    scanner = SentenceScanner()
    found = drip(scanner, json.dumps(reply), 3)
    assert len(found) == 1
    assert found[0]["text"] == text


def test_an_escaped_quote_does_not_end_the_string() -> None:
    text = 'The insurer wrote "no further cover" on it.'
    reply = {"sentences": [{"text": text, "supports": [3]}]}
    scanner = SentenceScanner()
    found = drip(scanner, json.dumps(reply), 4)
    assert len(found) == 1
    assert found[0]["text"] == text


def test_a_backslash_before_a_quote_is_handled() -> None:
    """A backslash escapes the backslash, not the quote after it — a string ending in one is
    where a scanner that tracks escapes carelessly runs off the end of the object."""
    original = "the watched folder is C:\\Users\\parrot\\inbox\\"
    reply = {"sentences": [{"text": original, "supports": [1]}]}
    scanner = SentenceScanner()
    found = drip(scanner, json.dumps(reply), 2)
    assert len(found) == 1
    # Compared against the value that went in, so the test cannot disagree with itself about
    # how many backslashes a literal needs.
    assert found[0]["text"] == original


def test_an_answer_with_no_sentences_yields_nothing_and_keeps_its_missing() -> None:
    """The model's own abstention. It says what document would have answered instead."""
    reply = {"sentences": [], "missing": "a utilities bill would answer it"}
    scanner = SentenceScanner()
    assert drip(scanner, json.dumps(reply), 5) == []
    assert scanner.missing() == "a utilities bill would answer it"


def test_missing_is_read_after_the_array_closed() -> None:
    scanner = SentenceScanner()
    drip(scanner, json.dumps(REPLY), 9)
    assert scanner.missing() == ""


def test_a_truncated_stream_keeps_the_sentences_that_did_arrive() -> None:
    """A model that stops halfway has still said the sentences it finished, and they were cited."""
    scanner = SentenceScanner()
    whole = json.dumps(REPLY)
    cut = whole.index("The policy number") + 10

    found = drip(scanner, whole[:cut], 6)
    assert [item["text"] for item in found] == ["Great Eastern covered the March admission."]
    assert scanner.missing() == "", "an unparseable buffer must not raise"


def test_a_sentence_that_is_not_an_object_is_skipped_rather_than_crashing() -> None:
    scanner = SentenceScanner()
    found = drip(scanner, '{"sentences": [{"text": "kept", "supports": [1]}], "missing": ""}', 5)
    assert [item["text"] for item in found] == ["kept"]


def test_nothing_is_returned_before_the_array_starts() -> None:
    scanner = SentenceScanner()
    assert scanner.feed('{"missi') == []
    assert scanner.feed('ng": "", "sent') == []
    assert scanner.feed('ences": [') == []
    assert [item["text"] for item in scanner.feed('{"text": "a", "supports": [1]}]}')] == ["a"]
