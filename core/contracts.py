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
    reads: list[Literal["facts", "obligations", "grounding_values"]]
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


ValueUnit = Literal["multiple", "money", "percent", "rate", "years", "count"]
Qualifier = Literal[
    "age_band",
    "ward_class",
    "insurer",
    "product",
    "residency",
    "assessment_year",
    "band_lower",
    "band_upper",
]


class ValueKey(Strict):
    """A rule or table value a pack's sources publish.

    Extracted automatically, approved by a person. The pack names the key and never the number:
    a number typed into YAML has no passage to be checked against and no review date to go stale
    by (ADR 0016).
    """

    key: Slug
    unit: ValueUnit
    description: str = Field(min_length=8, max_length=240)
    qualifiers: list[Qualifier] = Field(default_factory=list)


class Grounding(Strict):
    corpus: Slug | None = None  # a directory under packs/<pack>/grounding/; null = none
    top_k: int = Field(default=6, ge=0, le=20)
    values: list[ValueKey] = Field(default_factory=list)


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
    """One published source, as `packs/<pack>/grounding/<corpus>/sources.yaml` records it."""

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
    verdict_by_code: Literal[True] = True  # a verdict is chosen by code; the model only explains
    disclaimer: str = Field(min_length=20, max_length=800)
    # What a pack without an `advice` block says when asked to recommend, compare or judge.
    advice_decline: str = Field(default=DEFAULT_DECLINE, min_length=20, max_length=400)


# ---------------------------------------------------------------------------- advice
#
# A pack declares what it can advise on; it never says how to compute it. Each shape names a
# calculator from a closed list, the printed facts it reads and the reviewed rule values it needs,
# so the arithmetic is hand-written code and the model is left only the explaining (ADR 0016).

AdviceCalculator = Literal[
    "gap", "remaining_room", "keep_or_surrender", "compare_own", "compare_market", "estimate_saving"
]


class FactInput(Strict):
    """A printed fact a calculator reads, named by where it is printed rather than what it means."""

    role: Slug
    pack: Slug | None = None  # another installed pack's facts; None means this pack
    doc_types: list[Slug] = Field(min_length=1)
    field: Slug
    category: Slug | None = None  # a category id of this pack's answering.categories
    take: Literal["latest", "sum", "each"] = "latest"
    per: Literal["once", "month", "year"] = "once"  # a month's figure times 12 gives a year's
    missing: str = Field(min_length=8, max_length=240)


class RuleInput(Strict):
    role: Slug
    key: Slug  # declared in this pack's grounding.values
    missing: str = Field(min_length=8, max_length=240)


class AdviceShape(Strict):
    """One kind of advice question, and everything its calculator needs to answer it."""

    id: Slug
    calculator: AdviceCalculator
    label: str = Field(min_length=3, max_length=60)
    asked: list[Phrase] = Field(min_length=1)
    facts: list[FactInput] = Field(min_length=1)
    rules: list[RuleInput] = Field(default_factory=list)
    compare_fields: list[Slug] = Field(default_factory=list)
    order_by: Slug | None = None  # the stated ordering rule; must be one of compare_fields
    order: Literal["asc", "desc"] = "asc"
    estimate: bool = False
    disadvantages: list[str] = Field(default_factory=list)
    never_say: list[Phrase] = Field(default_factory=list)


class Advice(Strict):
    """What a pack that advises must say, once and in its own words, before it may."""

    consent_version: SemVer
    consent_text: str = Field(min_length=40, max_length=1500)
    disclaimer: str = Field(min_length=40, max_length=1200)
    product_disclosure: str = Field(min_length=40, max_length=800)
    max_rule_age_days: int = Field(default=365, ge=1, le=3650)
    max_price_age_days: int = Field(default=120, ge=1, le=3650)
    shapes: list[AdviceShape] = Field(min_length=1)


# The roles each calculator reads. A shape must supply every one; the loader says which is missing.
CALCULATOR_ROLES: dict[str, tuple[frozenset[str], frozenset[str]]] = {
    "gap": (frozenset({"income", "held"}), frozenset({"multiple"})),
    "remaining_room": (frozenset({"used"}), frozenset({"cap"})),
    "keep_or_surrender": (frozenset({"value_now", "paid_to_date"}), frozenset()),
    "compare_own": (frozenset({"items"}), frozenset()),
    "compare_market": (frozenset({"held"}), frozenset({"market"})),
    "estimate_saving": (frozenset({"income", "amount"}), frozenset({"rate"})),
}

_COMPARING: frozenset[str] = frozenset({"compare_own", "compare_market"})


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
    advice: Advice | None = None  # None: a request for a recommendation gets advice_decline

    def field_index(self) -> dict[tuple[str, str], FieldSpec]:
        """(document_type, field_name) -> FieldSpec. Used by the extractor and the scorer."""
        return {(dt, f.name): f for dt, spec in self.document_types.items() for f in spec.fields}

    def undeclared(self, doc_types: list[str], field: str) -> str | None:
        """Why this pack cannot supply `field` from every one of `doc_types`, or None if it can.

        Shared by the manifest's own check and `core.packs.check_advice_links`, so a fact read
        from another pack is held to exactly the rule a fact read from this one is.
        """
        for doc_type in doc_types:
            spec = self.document_types.get(doc_type)
            if spec is None:
                return f"document type {doc_type!r} is not declared by pack {self.id!r}"
            if field not in {f.name for f in spec.fields}:
                return f"field {field!r} is not declared on {self.id}.{doc_type}"
        return None

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

    @model_validator(mode="after")
    def _advice_reads_what_the_pack_declares(self) -> PackManifest:
        """An advice shape that names a missing role, field, category or key fails at load time.

        Caught here it is a message naming the shape; caught at question time it would be a
        calculator withholding advice for a reason no author could see. Facts read from another
        pack are checked once every pack is loaded, by `core.packs.check_advice_links`.
        """
        if self.advice is None:
            return self
        categories = self.answering.categories
        category_ids = {rule.id for rule in categories.rules} if categories else set()
        value_keys = {value.key for value in self.grounding.values}
        seen: set[str] = set()
        for shape in self.advice.shapes:
            where = f"advice shape {shape.id!r}"
            if shape.id in seen:
                raise ValueError(f"duplicate {where}: shape ids must be unique")
            seen.add(shape.id)

            fact_roles, rule_roles = CALCULATOR_ROLES[shape.calculator]
            for needed, supplied, kind in (
                (fact_roles, {f.role for f in shape.facts}, "fact"),
                (rule_roles, {r.role for r in shape.rules}, "rule"),
            ):
                if missing := sorted(needed - supplied):
                    raise ValueError(
                        f"{where}: calculator {shape.calculator!r} needs {kind} role(s) {missing}"
                    )

            for fact in shape.facts:
                if fact.pack is None and (reason := self.undeclared(fact.doc_types, fact.field)):
                    raise ValueError(f"{where}, fact {fact.role!r}: {reason}")
                if fact.category is not None and fact.category not in category_ids:
                    raise ValueError(
                        f"{where}, fact {fact.role!r}: category {fact.category!r} is not a rule "
                        "id in answering.categories"
                    )
            for rule in shape.rules:
                if rule.key not in value_keys:
                    raise ValueError(
                        f"{where}, rule {rule.role!r}: key {rule.key!r} is not declared in "
                        "grounding.values"
                    )

            if shape.calculator in _COMPARING and (not shape.compare_fields or not shape.order_by):
                raise ValueError(
                    f"{where}: calculator {shape.calculator!r} needs compare_fields and an "
                    "order_by, so a ranking always states the rule it ranks by"
                )
            if shape.order_by is not None and shape.order_by not in shape.compare_fields:
                raise ValueError(
                    f"{where}: order_by {shape.order_by!r} is not one of compare_fields"
                )
            self._compares_what_its_documents_declare(shape, value_keys)
        return self

    def _compares_what_its_documents_declare(
        self, shape: AdviceShape, value_keys: set[str]
    ) -> None:
        """A compared field no document type of the shape declares can never be printed.

        The calculator compares only fields both sides print, so a misspelt field would not fail:
        it would silently drop out of every table. A field needs declaring on at least one of the
        compared fact's document types, because a shape comparing a schedule with a renewal
        notice legitimately compares the fields only some of them print. A market comparison may
        also compare a field its sources publish as a value key and no document of this pack
        prints. Facts read from another pack are left to `core.packs.check_advice_links`.
        """
        role = {"compare_own": "items", "compare_market": "held"}.get(shape.calculator)
        compared = next((f for f in shape.facts if f.role == role), None)
        if compared is None or compared.pack is not None:
            return
        declared = {
            f.name for doc_type in compared.doc_types for f in self.document_types[doc_type].fields
        }
        for field in shape.compare_fields:
            if field in declared:
                continue
            if shape.calculator == "compare_market" and field in value_keys:
                continue
            published = " or grounding.values" if shape.calculator == "compare_market" else ""
            where = ", ".join(f"{self.id}.{doc_type}" for doc_type in compared.doc_types)
            raise ValueError(
                f"advice shape {shape.id!r} compares {field!r}, which is not declared on "
                f"{where}{published}"
            )


ModuleManifest.model_rebuild()
