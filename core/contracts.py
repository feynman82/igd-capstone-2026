"""The two contracts the whole platform is built on.

Nothing else in the repository may define what a pack or a module is. A change here
is its own reviewed pull request, made before any code depends on it.
"""

from __future__ import annotations

from datetime import date as _Date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

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
    corpus: str | None = None  # null = answer only from the user's own documents
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
    disclaimer: str = Field(min_length=20, max_length=800)


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

    def field_index(self) -> dict[tuple[str, str], FieldSpec]:
        """(document_type, field_name) -> FieldSpec. Used by the extractor and the scorer."""
        return {(dt, f.name): f for dt, spec in self.document_types.items() for f in spec.fields}


ModuleManifest.model_rebuild()
