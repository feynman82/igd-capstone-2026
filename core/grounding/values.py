"""Extract the values a pack's published sources print, and keep only what the text supports.

A pack names the values its advice needs (`ValueKey`) and never types the numbers itself: a
number in YAML has no passage to check and no review date to go stale by (ADR 0016). So the
numbers come from the sources, read by a small local model, and a small model will sometimes
report a figure the text does not print, or copy a passage that is not quite there.

The model is therefore only a proposer. Code keeps a value when the passage it quotes really is
in the text, the value parses for the key's unit, and that number is a whole number printed in
the passage in a form that fits the unit. Everything else is dropped and logged, and what
survives still waits for a person to approve it before any calculator reads it.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from core.contracts import ValueKey
from core.grounding.corpus import SourceText
from core.runtime.ollama import Ollama

log = logging.getLogger(__name__)

SYSTEM = (
    "You read one published source and report only values the text prints, copying the sentence "
    "or table row that prints each one exactly, character for character. Never calculate, round, "
    "convert or infer a value, and never report a value for a key the text does not print. If "
    "the text prints none of the values asked for, report an empty list."
)

# About what a 4B model reads well in one call. Headings are the natural seams of a guidance page,
# so a section is cut at a heading first and only falls back to blank lines, then to line ends.
SECTION_CHARS = 4000

# A value that passed every check below. There is no model-reported confidence to carry, and a kept
# value is not certain either: it is a proposal a person still approves.
KEPT_CONFIDENCE = 0.9

_NUMBER = r"\d[\d,]*(?:\.\d+)?"
_TIMES = "\N{MULTIPLICATION SIGN}"
# A whole number as printed: not preceded by a digit, point or comma, and not followed by a digit,
# so that 4,000 is never found inside 40,000.
_TOKEN = re.compile(rf"(?<![\d.,]){_NUMBER}(?![\d])", re.ASCII)
_UNIT_PATTERNS: dict[str, re.Pattern[str]] = {
    # An optional currency marker before the amount: a code of up to three capitals, a dollar
    # sign, or both, as in $15,300, S$15,300 and SGD 15,300.
    "money": re.compile(rf"(?:[A-Z]{{1,3}}\s?)?\$?\s*({_NUMBER})", re.ASCII),
    "percent": re.compile(rf"({_NUMBER})\s*%?", re.ASCII),
    "rate": re.compile(rf"({_NUMBER})\s*%?", re.ASCII),
    # A letter x, the multiplication sign, or the word: 9x, 9 times.
    "multiple": re.compile(rf"({_NUMBER})\s*(?:x|{_TIMES}|times)?", re.ASCII | re.IGNORECASE),
    "years": re.compile(r"(\d[\d,]*)", re.ASCII),
    "count": re.compile(r"(\d[\d,]*)", re.ASCII),
}
# What may follow a number where it is printed, which says what kind of number it is.
_SCALE_AFTER = re.compile(r"\s*(?:k|m|mn|million|bn|billion)\b", re.ASCII | re.IGNORECASE)
_PERCENT_SIGN_AFTER = re.compile(r"\s*%")
_PERCENT_AFTER = re.compile(r"\s*(?:%|per\s?cent\b)", re.ASCII | re.IGNORECASE)
_PERCENT_UNITS = frozenset({"percent", "rate"})
_PIPE = re.compile(r"\s*\|\s*")
_WHITESPACE = re.compile(r"\s+")
_DIGITS = frozenset("0123456789")


@dataclass(frozen=True, slots=True)
class ExtractedValue:
    key: str
    unit: str
    value_num: Decimal | None
    value_text: str | None
    qualifiers: dict[str, str]
    passage: str
    confidence: float


# ------------------------------------------------------------------------------ sections


def split_sections(text: str, limit: int = SECTION_CHARS) -> list[str]:
    """The text in consecutive sections of at most about `limit` characters.

    A line is never cut, because a table row cut in two is a passage no longer printed anywhere,
    and every value in it would then be dropped. A single line longer than `limit` is kept whole.
    The sections join back to the text exactly, whitespace-only ones aside.
    """
    lines = text.splitlines(keepends=True)
    pieces: list[str] = []
    for block in _groups(lines, _is_heading):
        if len("".join(block)) <= limit:
            pieces.append("".join(block))
            continue
        for paragraph in _groups(block, _starts_paragraph):
            if len("".join(paragraph)) <= limit:
                pieces.append("".join(paragraph))
            else:
                pieces.extend(paragraph)
    return _pack(pieces, limit)


def _is_heading(_previous: str, line: str) -> bool:
    return line.startswith("#")


def _starts_paragraph(previous: str, line: str) -> bool:
    return not previous.strip() and bool(line.strip())


def _groups(lines: list[str], starts_new: Callable[[str, str], bool]) -> list[list[str]]:
    groups: list[list[str]] = []
    previous = ""
    for line in lines:
        if not groups or starts_new(previous, line):
            groups.append([])
        groups[-1].append(line)
        previous = line
    return groups


def _pack(pieces: list[str], limit: int) -> list[str]:
    """Consecutive pieces joined while they fit, so a page of short sections is one call."""
    sections: list[str] = []
    current = ""
    for piece in pieces:
        if current and len(current) + len(piece) > limit:
            sections.append(current)
            current = ""
        current += piece
    if current:
        sections.append(current)
    return [section for section in sections if section.strip()]


# ------------------------------------------------------------------------------ checks


def collapse(text: str) -> str:
    """Text with table pipes and every run of whitespace folded to one space.

    A model copying a table row often drops its `|` characters or its padding, and the row is
    still printed. Case is kept: a passage that differs in case was retyped, not copied.
    """
    return _WHITESPACE.sub(" ", _PIPE.sub(" ", text)).strip()


def printed_in(passage: str, text: str) -> bool:
    """Whether the passage is printed in the text, without starting or ending inside a number.

    The boundary matters for the same reason the number tokens do: "the limit of 40" is a
    substring of "the limit of 40,000", and would otherwise vouch for a 40 the text never prints.
    """
    needle, haystack = collapse(passage), collapse(text)
    if not needle:
        return False
    start = haystack.find(needle)
    while start != -1:
        if not _cuts_a_number(haystack, start, start + len(needle)):
            return True
        start = haystack.find(needle, start + 1)
    return False


def _cuts_a_number(haystack: str, start: int, end: int) -> bool:
    def digit(index: int) -> bool:
        return 0 <= index < len(haystack) and haystack[index] in _DIGITS

    def separator(index: int) -> bool:
        return 0 <= index < len(haystack) and haystack[index] in (",", ".")

    head = digit(start) and (digit(start - 1) or (separator(start - 1) and digit(start - 2)))
    tail = digit(end - 1) and (digit(end) or (separator(end) and digit(end + 1)))
    return head or tail


def number_tokens(passage: str) -> list[Decimal]:
    """Every whole number the passage prints, thousands separators removed."""
    return [Decimal(token.replace(",", "")) for token in _TOKEN.findall(passage)]


def printed_as(unit: str, number: Decimal, passage: str) -> bool:
    """Whether the passage prints this number, at least once, in a form that fits the unit.

    What follows each occurrence decides it. A number followed by a scale word (k, m, mn,
    million, bn, billion) is a different amount for every unit. A percent or rate must be followed
    by `%`, "per cent" or "percent"; money, a count, years or a multiple must not be followed by
    `%`. Years and page numbers can still match a count or money token, and approval is the check
    for those.
    """
    for match in _TOKEN.finditer(passage):
        if Decimal(match.group().replace(",", "")) != number:
            continue
        after = passage[match.end() :]
        if _SCALE_AFTER.match(after):
            continue
        if unit in _PERCENT_UNITS:
            if not _PERCENT_AFTER.match(after):
                continue
        elif _PERCENT_SIGN_AFTER.match(after):
            continue
        return True
    return False


def parse_value(unit: str, value: str) -> Decimal | None:
    """The number a reported value states for its unit, or `None` when it states something else.

    Parsing is a full match, never `Decimal(value)` alone, which would accept NaN, Infinity and
    1e4. A percentage is stored as the number printed, 3.5 for 3.5%, because that is the number
    the passage will be checked for.
    """
    pattern = _UNIT_PATTERNS.get(unit)
    match = pattern.fullmatch(value.strip()) if pattern else None
    if match is None:
        return None
    return Decimal(match.group(1).replace(",", ""))


# ------------------------------------------------------------------------------ extraction


def extract_values(
    client: Ollama, source: SourceText, keys: Sequence[ValueKey]
) -> list[ExtractedValue]:
    """Every value the source prints for these keys, kept only when its passage prints it.

    One model call per section. Anything that keeps a section from being read — the request
    itself failing, or its reply coming back truncated or not JSON at all — raises
    `ModelUnavailable` and is not caught here, whichever section it happened on: the index rolls
    the whole pack back on it and the next run retries, rather than committing a hash for a
    section that was never actually read. An empty or partial list from a section that failed
    would look, to a calculator later, like a source that simply prints fewer values than it does.
    A reply that *is* valid JSON but has no `values` list, or an item in that list that is not an
    object, means the model answered and just proposed nothing usable there; that is logged and
    counts as no values for that section only.
    """
    if not keys:
        return []
    index = {key.key: key for key in keys}
    schema = _schema(keys)
    kept: list[ExtractedValue] = []
    for section in split_sections(source.text):
        # An outage raises from here — including from `.json()` below, on a truncated or
        # non-JSON reply — and is not caught.
        generated = client.constrained(SYSTEM, _prompt(source, keys, section), schema)
        reported = generated.json()
        values = reported.get("values")
        if not isinstance(values, list):
            log.info("no values from a section of %s: the reply had no list", source.document.file)
            continue
        for item in values:
            value = _check(index, item, section)
            if value is not None:
                kept.append(value)
    return kept


def _schema(keys: Sequence[ValueKey]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "values": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string", "enum": [key.key for key in keys]},
                        "value": {"type": "string"},
                        "passage": {"type": "string"},
                        "qualifiers": {
                            "type": "object",
                            "additionalProperties": {"type": "string"},
                        },
                    },
                    "required": ["key", "value", "passage", "qualifiers"],
                },
            }
        },
        "required": ["values"],
    }


def _prompt(source: SourceText, keys: Sequence[ValueKey], section: str) -> str:
    described = [
        f"- {key.key} ({key.unit}): {key.description}"
        + (f" Qualifiers: {', '.join(key.qualifiers)}." if key.qualifiers else "")
        for key in keys
    ]
    return "\n".join(
        [
            f"This text is part of '{source.document.title}'.",
            "Report each of these values the text prints:",
            *described,
            "",
            "For each value, copy into passage the one sentence or table row that prints it.",
            "value: the number only, without currency signs or words.",
            "Give a qualifier only when the key lists it and the text states it. Units: money is",
            "an amount, percent and rate are a number with an optional %, multiple is a number",
            "such as 4 times, years and count are whole numbers.",
            "",
            "<<<",
            section,
            ">>>",
        ]
    )


def _check(index: dict[str, ValueKey], item: Any, section: str) -> ExtractedValue | None:
    """The reported value when the section supports it; otherwise `None`, logged with why."""
    if not isinstance(item, dict):
        log.info("dropping a reported value: it was not an object")
        return None
    name, raw, passage = item.get("key"), item.get("value"), item.get("passage")
    qualifiers = item.get("qualifiers", {})
    passage_text = passage if isinstance(passage, str) else ""

    def drop(reason: str) -> None:
        log.info("dropping %s: %s (passage %r)", name, reason, passage_text[:80])

    key = index.get(name) if isinstance(name, str) else None
    if key is None:
        drop("the key is not one this pack declares")
        return None
    if not isinstance(raw, str):
        drop("the value is not text")
        return None
    if not isinstance(qualifiers, dict):
        drop("qualifiers not an object")
        return None
    if not all(isinstance(k, str) and isinstance(v, str) for k, v in qualifiers.items()):
        drop("the qualifiers are not names and text")
        return None
    undeclared = set(qualifiers) - set(key.qualifiers)
    if undeclared:
        drop(f"qualifiers {sorted(undeclared)} are not declared for this key")
        return None
    empty = sorted(k for k, v in qualifiers.items() if not v.strip())
    if empty:
        drop(f"qualifier {empty[0]!r} is empty")
        return None
    if not printed_in(passage_text, section):
        drop("the passage is not printed in the text")
        return None
    number = parse_value(key.unit, raw)
    if number is None:
        drop(f"the value {raw!r} is not a {key.unit}")
        return None
    if not printed_as(key.unit, number, passage_text):
        drop(f"the passage does not print {raw!r} as a {key.unit}")
        return None
    return ExtractedValue(
        key=key.key,
        unit=key.unit,
        value_num=number,
        value_text=raw,
        qualifiers=dict(qualifiers),
        passage=passage_text,
        confidence=KEPT_CONFIDENCE,
    )
