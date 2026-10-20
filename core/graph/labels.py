"""A printed value, checked against the label printed beside it. ADR 0021, behind a switch.

`check_content` makes sure a number a sentence states is printed on a page it cites. It cannot
make sure the number is what the sentence says it is. On 19 October "The road tax on SLK 8842 D
is due on 12 April 2026" passed every check, citing a page that prints
`Period of Insurance From: 12 April 2026`, and "The named driver on the car policy is Marcus Lim
Jun Wei" passed citing `Name of Insured: Marcus Lim Jun Wei`. Both values are printed; neither
label says what the sentence does.

Finding the label is code: Docling's tables reach a passage as `label: value` lines, and a line
whose value the sentence repeats is the evidence for that part of it. Judging whether the label
*means* what the sentence calls the value is not code — "you pay SGD 1,284.00 a year" is right
and shares no word with `Annual Premium` — so one constrained call to the generator decides,
with the lines in front of it. A value printed without a label (a letterhead, a line of prose)
is not checked, and the sentence keeps its place.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Sequence
from typing import Any, Protocol

from core.graph.gate import _NUMBER, _normal
from core.graph.ports import Passage
from core.runtime.ollama import ModelUnavailable

log = logging.getLogger(__name__)

# A printed `label: value` line: a short label, a colon, the value. Long labels are prose that
# happens to contain a colon ("Notify within 24 hours: ..."), not a field.
_LINE = re.compile(r"^[ \t]*([^:\n]{2,60}?)[ \t]*:[ \t]*(\S[^\n]*?)[ \t]*$", re.MULTILINE)
_CURRENCY = re.compile(r"\b(?:SGD|S\$|USD)\s*|\$", re.IGNORECASE)
_LETTERS = re.compile(r"[A-Za-z]")
SHORTEST = 3  # a value of one or two characters ("1", "No") matches by accident, not evidence

SYSTEM = (
    "You check one sentence against lines a document prints. Each line is a label, a colon and "
    "a value. You decide only whether the printed label says the value is what the sentence "
    "calls it. Paraphrase is fine; a different role, date or amount is not."
)

# Examples from a domain nowhere in PARROT's documents or question sets, so they teach the task
# and cannot teach the answers.
EXAMPLES = (
    "Examples, from a tenancy agreement:\n"
    "- 'Monthly Rent: SGD 2,400.00' supports 'You pay SGD 2,400.00 a month in rent.'\n"
    "- 'Landlord: Alex Tan' does not support 'The tenant is Alex Tan.'\n"
    "- 'Lease Start: 1 March 2026' does not support 'The deposit is due on 1 March 2026.'"
)

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"supported": {"type": "boolean"}},
    "required": ["supported"],
}


class Judge(Protocol):
    def constrained(
        self,
        system: str,
        prompt: str,
        schema: dict[str, Any],
        *,
        images: list[str] | None = None,
        temperature: float = 0.0,
    ) -> Any: ...


def _flat(text: str) -> str:
    return " ".join(text.casefold().split())


def _repeats(value: str, sentence: str, numbers: set[str]) -> bool:
    """Whether the sentence states this printed value: its text verbatim, or — for a value that
    is a figure — the same number, however it was formatted."""
    core = _CURRENCY.sub("", value).strip()
    if len(core) < SHORTEST:
        return False
    if _flat(core) in _flat(sentence):
        return True
    figures = _NUMBER.findall(core)
    return (
        bool(figures)
        and len(_LETTERS.findall(core)) == 0
        and all(_normal(figure) in numbers for figure in figures)
    )


def labelled_lines(sentence: str, cited: Sequence[Passage], question: str = "") -> list[str]:
    """The `label: value` lines, from the document passages a sentence cites, whose value the
    sentence states — in the order they are printed, each once.

    A value the question itself names is not one: "Who is the lender on facility
    HP-2021-448190?" is answered "The lender on facility HP-2021-448190 is Crescent Bank
    Limited", and the facility number there is the sentence pointing at what was asked about, not
    its answer. On 19 October it was checked anyway, against `Agreement No:`, and the right answer
    was dropped."""
    numbers = {_normal(figure) for figure in _NUMBER.findall(sentence)}
    asked = {_normal(figure) for figure in _NUMBER.findall(question)}
    found: list[str] = []
    for passage in cited:
        if passage.kind != "document":
            continue  # the documents-on-file lines are written by code from facts, not printed
        for match in _LINE.finditer(passage.text):
            label, value = match.group(1).strip(), match.group(2).strip()
            line = f"{label}: {value}"
            if (
                line not in found
                and _repeats(value, sentence, numbers)
                and not (question and _repeats(value, question, asked))
            ):
                found.append(line)
    return found


def label_supports(judge: Judge, sentence: str, lines: Sequence[str]) -> bool:
    """Ask the generator whether the printed labels say what the sentence says. One call.

    A call that fails leaves the sentence where it was: unchecked, not refused. On 19 October one
    failed mid-answer and the failure ended the whole answer, taking a right one with it. The
    check is an extra line of defence, and its own failure must not become a reason to say
    nothing."""
    prompt = (
        f"{EXAMPLES}\n\nThe document prints:\n"
        + "\n".join(f"- {line}" for line in lines)
        + f"\n\nThe sentence: {sentence}\n\n"
        "Does a printed label say the value is what the sentence calls it?"
    )
    try:
        reply = judge.constrained(SYSTEM, prompt, SCHEMA).json()
    except (ModelUnavailable, ValueError) as error:  # no answer, or an answer that is not JSON
        log.warning("label check could not run, sentence kept unchecked: %s", error)
        return True
    return bool(reply.get("supported")) if isinstance(reply, dict) else False
