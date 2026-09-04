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


class Extraction(Strict):
    model: str  # dotted path to the pack's Pydantic document model
    writes: list[Literal["facts", "obligations"]]


class Grounding(Strict):
    corpus: str | None = None  # a pack with no corpus answers only from user documents
    top_k: int = Field(default=6, ge=0, le=20)


class ReminderConfig(Strict):
    key: Slug
    from_field: str | None = None
    on_date: _Date | None = None   # a fixed calendar date, e.g. a filing deadline
    lead_days: list[int] = Field(min_length=1)


class AlertConfig(Strict):
    metric: Slug
    ceiling: float
    warn_at: float = Field(ge=0.0, le=1.0)


class TrackerConfig(Strict):
    metrics: list[Slug] = Field(min_length=1)


class Registrations(Strict):
    reminder: dict[str, list[ReminderConfig]] | None = None
    alert: dict[str, list[AlertConfig]] | None = None
    tracker: TrackerConfig | None = None


class Persona(Strict):
    system: str = Field(max_length=2000)  # voice only; cannot change retrieval or guardrails


class Guardrails(Strict):
    must_cite: bool = True
    abstain_below: float = Field(default=0.42, ge=0.0, le=1.0)
    never_acts: Literal[True] = True  # v1 advises; the type makes it un-overridable
    disclaimer: str = Field(min_length=1, max_length=800)


class PackManifest(Strict):
    """A domain pack. Declarative: document types, an extraction schema, a grounding
    corpus, which modules it registers with, and its guardrails."""

    id: Slug
    version: SemVer
    display_name: str = Field(max_length=60)
    owns_document_types: list[Slug] = Field(min_length=1)
    extraction: Extraction
    grounding: Grounding = Grounding()
    registers: Registrations = Registrations()
    persona: Persona
    guardrails: Guardrails


ModuleManifest.model_rebuild()
