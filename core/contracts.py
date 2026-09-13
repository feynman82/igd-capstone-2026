"""The two contracts the whole platform is built on.

Nothing else in the repository may define what a pack or a module is. A change here
is its own reviewed pull request, made before any code depends on it.
"""

from __future__ import annotations

from datetime import date as _Date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Slug = Annotated[str, Field(pattern=r"^[a-z][a-z0-9_]{2,31}$")]
SemVer = Annotated[str, Field(pattern=r"^\d+\.\d+\.\d+$")]

PrimitiveId = Literal["reminder", "alert", "tracker"]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


# --------------------------------------------------------------------------- modules


class ModuleManifest(Strict):
    """A capability module. Reads typed rows, writes its own namespace, renders somewhere.

    A module never touches retrieval and never writes to `facts`.
    """

    id: PrimitiveId
    version: SemVer
    reads: list[Literal["facts", "obligations"]]
    writes: list[str]
    runs: ModuleTrigger
    surfaces: list[Literal["today", "notification", "chat_thread", "vault"]]
    config_schema: str  # dotted path to the Pydantic model a pack must satisfy


class ModuleTrigger(Strict):
    on: Literal["schedule", "fact_write"]
    cron: str | None = None  # required when on == "schedule"
    debounce_hours: int = 24  # an alert must not repeat daily


# ----------------------------------------------------------------------------- packs
#
# A pack is authored as ONE YAML file. The fields are declared inline, and
# `python -m packs.build` generates the Pydantic extraction models and the register column
# headers from it. The YAML is the single source of truth: nothing else may define a field.


FieldType = Literal[
    "string",  # free text                     -> str        -> facts.value_text
    "identifier",  # policy no, receipt no      -> str      -> facts.value_text, never normalised
    "person",  # names a family member       -> str      -> facts.value_text + facts.subject
    "money",  # SGD, two decimal places        -> Decimal    -> facts.value_num
    "integer",  # counts, mileage                -> int        -> facts.value_num
    "percent",  # 0-100                          -> float      -> facts.value_num
    "date",  # ISO YYYY-MM-DD                 -> date       -> facts.value_date
    "month",  # YYYY-MM                        -> str        -> facts.value_text
    "enum",  # one of `values`                -> str        -> facts.value_text
    "boolean",  # true / false                   -> bool       -> facts.value_text
]

# Which column of `facts` each type lands in. The extractor and the evaluation both read
# this table, so a type can never be scored against the wrong column.
FACT_COLUMN: dict[str, str] = {
    "string": "value_text",
    "identifier": "value_text",
    "person": "value_text",
    "money": "value_num",
    "integer": "value_num",
    "percent": "value_num",
    "date": "value_date",
    "month": "value_text",
    "enum": "value_text",
    "boolean": "value_text",
}


class FieldSpec(Strict):
    """One extractable field. Its `name` is the column header in Desmond's register and the
    `facts.key` it is stored under. Renaming it renames both."""

    name: Slug
    type: FieldType
    required: bool = True
    description: str = Field(min_length=8, max_length=200)
    values: list[str] | None = None  # required when type == "enum"
    example: str | None = None  # shown to the extraction model and to the corpus author


class DocumentTypeSpec(Strict):
    """One kind of document this pack recognises."""

    description: str = Field(min_length=8, max_length=240)
    subject_field: Slug | None = None  # which field says whose document this is
    fields: list[FieldSpec] = Field(min_length=1, max_length=12)


class Grounding(Strict):
    corpus: Slug | None = None  # a directory under grounding/; null = the user's documents only
    top_k: int = Field(default=6, ge=0, le=20)


class ReminderConfig(Strict):
    key: Slug
    from_field: Slug | None = None  # a date field on one of this pack's document types
    on_date: _Date | None = None  # or a fixed calendar date, e.g. a filing deadline
    lead_days: list[int] = Field(min_length=1)


class AlertConfig(Strict):
    metric: Slug
    ceiling: float
    warn_at: float = Field(ge=0.0, le=1.0)


class TrackerConfig(Strict):
    metrics: list[Slug] = Field(min_length=1)


Phrase = Annotated[str, Field(min_length=2, max_length=60)]

DEFAULT_DECLINE = (
    "I can explain what your documents say, but I do not recommend, compare, or judge whether "
    "something is enough. A licensed professional can help with that."
)


class Category(Strict):
    """A kind of document a household holds, recognised by words printed in its name.

    Decided when a question is asked and never stored. No schedule prints "motor", so a category
    is a person-reviewed reading of a printed name, not a field — `packs/README.md` §8, test 1.
    """

    id: Slug
    label: str = Field(min_length=3, max_length=40)  # completes "is a …": "dental plan"
    printed: list[Phrase] = Field(min_length=1)  # any of these, as whole words, in the name
    asked: list[Phrase] = Field(default_factory=list)  # any of these in a question


class Categories(Strict):
    match_field: Slug  # the printed field the rules read, e.g. product_name
    noun: str = Field(min_length=3, max_length=30)  # what is counted on file: "policies"
    rules: list[Category] = Field(min_length=1)  # first match wins, so the order is reviewed


class Exclusions(Strict):
    """A sentence claiming cover whose every citation sits under one of `headings` is dropped."""

    headings: list[Phrase] = Field(min_length=1)
    claims: list[Phrase] = Field(min_length=1)
    negations: list[Phrase] = Field(min_length=1)


class Answering(Strict):
    """What a pack knows about how people ask. Applied by the core without a model."""

    vocabulary: dict[str, str] = Field(default_factory=dict)  # said -> printed
    categories: Categories | None = None
    exclusions: Exclusions | None = None
    max_sentences: int = Field(default=6, ge=1, le=30)


class GroundingDocument(Strict):
    """One published source, as `grounding/<corpus>/sources.yaml` records it."""

    file: str = Field(pattern=r"^[a-z0-9][a-z0-9_.-]*\.md$")
    title: str = Field(min_length=3, max_length=200)
    publisher: str = Field(min_length=2, max_length=120)
    publisher_kind: Literal["regulator", "government", "industry_association"]
    url: str = Field(pattern=r"^https://")
    published: _Date | None = None  # the page's own "last updated", when it prints one
    retrieved: _Date
    applies_to: str = Field(min_length=3, max_length=120)
    review_by: _Date  # after this date the source is not cited
    reviewed_by: str | None = None
    reviewed_on: _Date | None = None  # nothing is cited until a person has signed it off
    note: str | None = None


class GroundingCorpus(Strict):
    corpus_id: Slug
    applies_to: str
    maintained_by: str
    reviewed_by: str
    reviewed_on: _Date | None = None
    documents: list[GroundingDocument] = Field(default_factory=list)


class Registrations(Strict):
    reminder: list[ReminderConfig] | None = None
    alert: list[AlertConfig] | None = None
    tracker: TrackerConfig | None = None


class Persona(Strict):
    system: str = Field(min_length=20, max_length=2000)  # voice only


class Guardrails(Strict):
    must_cite: bool = True
    abstain_below: float = Field(default=0.42, ge=0.0, le=1.0)
    never_acts: Literal[True] = True  # v1 advises; the type makes it un-overridable
    never_recommends: Literal[True] = True  # v1 explains; a request for a judgement is declined
    disclaimer: str = Field(min_length=20, max_length=800)
    advice_decline: str = Field(default=DEFAULT_DECLINE, min_length=20, max_length=400)


class PackManifest(Strict):
    """A domain pack, authored as one YAML file."""

    id: Slug
    version: SemVer
    display_name: str = Field(min_length=3, max_length=60)
    document_types: dict[Slug, DocumentTypeSpec] = Field(min_length=1)
    grounding: Grounding = Grounding()
    registers: Registrations = Registrations()
    persona: Persona
    guardrails: Guardrails
    answering: Answering = Answering()

    def field_index(self) -> dict[tuple[str, str], FieldSpec]:
        """(document_type, field_name) -> FieldSpec. Used by the extractor and the scorer."""
        return {(dt, f.name): f for dt, spec in self.document_types.items() for f in spec.fields}

    @model_validator(mode="after")
    def _categories_read_a_declared_field(self) -> PackManifest:
        categories = self.answering.categories
        if categories is None:
            return self
        declared = {f.name for spec in self.document_types.values() for f in spec.fields}
        if categories.match_field not in declared:
            raise ValueError(
                f"answering.categories.match_field {categories.match_field!r} is not a field on "
                "any document type in this pack"
            )
        return self


ModuleManifest.model_rebuild()
