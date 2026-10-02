"""What the core and the enabled packs know about how people ask, applied without a model.

Three things, all declared under `answering` — in `core/documents.yaml`, which always applies, and
in each enabled pack's `pack.yaml` (ADR 0017) — and all matched as whole words: the
words a household says for what its documents print, the categories of document a question is
about, and the category a document on file falls in. None of it is a field and none of it is
stored — a category is a reading of a printed name, decided when a question is asked.

Measured on 13 September: the understanding step rewrote "warded for dengue 3 days, can claim?"
as "I was awarded for dengue", searched "dengue award", and the answer cited the car policy. A
4B model's rewrite is a guess; a pack's word list is a fact somebody wrote down. The question
reworded here is searched alongside the model's phrasings, so the model can add a search but can
no longer be the only thing that understood the household's words.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass

from core.contracts import Categories, Category
from core.packs import InstalledPack, catalog


def _pattern(phrase: str) -> re.Pattern[str]:
    return re.compile(rf"(?<!\w){re.escape(phrase)}(?!\w)", re.IGNORECASE)


def mentions(text: str, phrase: str) -> bool:
    return _pattern(phrase).search(text) is not None


def _vocabulary(packs: Sequence[InstalledPack]) -> list[tuple[str, str]]:
    """The catalogue's words and every enabled pack's, unioned; a pack's wording wins a clash."""
    merged = dict(catalog().documents.answering.vocabulary)
    for installed in packs:
        merged.update(installed.manifest.answering.vocabulary)
    return list(merged.items())


def reworded(question: str, packs: Sequence[InstalledPack]) -> str | None:
    """The question with each declared phrase replaced by what the documents print, longest
    phrase first. `None` when nothing matched, so a caller searches nothing twice."""
    pairs = sorted(_vocabulary(packs), key=lambda pair: len(pair[0]), reverse=True)
    out = question
    for said, printed in pairs:
        # Backslashes doubled, so a printed `\1` or `\g` is text, not a backreference.
        out = _pattern(said).sub(printed.replace("\\", "\\\\"), out)
    return out if out != question else None


def glossary(question: str, packs: Sequence[InstalledPack]) -> list[str]:
    """Only the lines the question used, so the prompt grows by what it needs and no more."""
    return [f"{said} = {p}" for said, p in _vocabulary(packs) if mentions(question, said)]


@dataclass(frozen=True, slots=True)
class Asked:
    pack_id: str
    categories: Categories
    category: Category


def categories_asked(question: str, packs: Sequence[InstalledPack]) -> list[Asked]:
    found: list[Asked] = []
    for installed in packs:
        declared = installed.manifest.answering.categories
        if declared is None:
            continue
        found.extend(
            Asked(installed.id, declared, rule)
            for rule in declared.rules
            if any(mentions(question, phrase) for phrase in rule.asked)
        )
    return found


def categorise(printed_name: str, categories: Categories) -> Category | None:
    """The first rule whose printed words appear. `None` is an answer, not a failure."""
    for rule in categories.rules:
        if any(mentions(printed_name, phrase) for phrase in rule.printed):
            return rule
    return None
