"""Pulling finished sentences out of a JSON reply that is still being written.

The answer node is schema-constrained: the model does not write prose, it writes
`{"sentences": [{"text": ..., "supports": [2, 5]}, ...], "missing": ...}`. That is what makes
rule 3 enforceable — a sentence arrives already carrying the passages it came from.

It is also what makes streaming awkward. Streaming the model's tokens straight to a screen would
put JSON syntax on it, and worse, would show sentences before the gate has decided whether they
can be kept. So the stream is read here instead: the buffer is scanned as it grows, and each
`{...}` inside the `sentences` array is handed over the moment its closing brace arrives. One
finished sentence is the smallest unit that can be checked, so it is the unit the interface
receives.

**This is a scanner, not a JSON parser.** It does not validate; `json.loads` does that, per
object, once the object is complete. It only has to know where one object ends, which means
tracking string literals and escapes so that a `}` inside `"text"` is not mistaken for the end
of the sentence containing it. A sentence like `He said "we will not pay {yet}"` is exactly the
case that breaks a naïve brace count, and the corpus has documents with braces in them.
"""

from __future__ import annotations

import json
import logging
from typing import Any

log = logging.getLogger(__name__)

_KEY = '"sentences"'


class SentenceScanner:
    """Feed it deltas; it returns whichever sentences became complete because of them.

    Stateful and single-use, one per generation. The whole reply is kept because `missing` may
    be written after the array closes and is only needed at the end.
    """

    def __init__(self) -> None:
        self._buffer = ""
        self._cursor = 0  # how far the object scanner has consumed
        self._in_array = False
        self._closed = False  # the sentences array has ended
        self._depth = 0
        self._start = -1
        self._in_string = False
        self._escape = False

    @property
    def raw(self) -> str:
        """Everything received so far. Used once, at the end, to read `missing`."""
        return self._buffer

    def feed(self, delta: str) -> list[dict[str, Any]]:
        """Append `delta` and return the sentences it completed. Usually none, sometimes one."""
        self._buffer += delta
        if not self._in_array and not self._locate_array():
            return []
        return self._scan()

    def _locate_array(self) -> bool:
        """Find `"sentences": [` once. Everything before it is of no interest.

        Searching for the key as a literal is safe here because it is the first thing in the
        schema: any later occurrence of the word inside a sentence's own text is behind this
        point, and the cursor never goes backwards.
        """
        key = self._buffer.find(_KEY)
        if key == -1:
            return False
        opened = self._buffer.find("[", key + len(_KEY))
        if opened == -1:
            return False
        self._in_array = True
        self._cursor = opened + 1
        return True

    def _scan(self) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        index = self._cursor

        while index < len(self._buffer):
            char = self._buffer[index]

            if self._in_string:
                if self._escape:
                    self._escape = False
                elif char == "\\":
                    self._escape = True
                elif char == '"':
                    self._in_string = False
            elif char == '"':
                self._in_string = True
            elif char == "{":
                if self._depth == 0:
                    self._start = index
                self._depth += 1
            elif char == "}":
                self._depth -= 1
                if self._depth == 0 and self._start >= 0:
                    sentence = self._parse(self._buffer[self._start : index + 1])
                    if sentence is not None:
                        found.append(sentence)
                    self._start = -1
            elif char == "]" and self._depth == 0:
                # The array is over. Whatever follows is `missing`, read from `raw` at the end.
                self._closed = True
                index += 1
                break

            index += 1

        self._cursor = index
        return found

    @staticmethod
    def _parse(text: str) -> dict[str, Any] | None:
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            # Schema-constrained output should never land here. If it does, one malformed
            # sentence is dropped and the rest of the answer still arrives — which is the same
            # thing the gate does with a sentence it cannot verify.
            log.info("could not parse a streamed sentence: %.80s", text)
            return None
        return value if isinstance(value, dict) else None

    def missing(self) -> str:
        """What document would have answered this, if the model said. Read once, at the end."""
        try:
            whole = json.loads(self._buffer)
        except json.JSONDecodeError:
            return ""
        if not isinstance(whole, dict):
            return ""
        return str(whole.get("missing", "")).strip()
