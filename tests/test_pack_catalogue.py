"""The pack catalogue (packs/catalogue.yaml), checked against the contract the built packs use.

The nine deferred packs are specified, not built, so nothing loads them. Without this test the
catalogue would be prose that drifts: a document type renamed in the core, a reminder pointing at
a field no document prints, or a proposed type that could never be pasted into
core/documents.yaml. Each entry is held to what a real pack and the core catalogue would accept.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pytest
import yaml
from pydantic import Field, model_validator

from core.contracts import FACT_COLUMN, DocumentTypeSpec, Slug, Strict
from core.packs import catalog, installed_packs

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "packs" / "catalogue.yaml"
WRITE_UP = ROOT / "packs" / "CATALOGUE.md"


class Publisher(Strict):
    name: str = Field(min_length=3)
    kind: Literal["regulator", "government", "industry_association"]


class PlannedGrounding(Strict):
    corpus: Slug | None
    publishers: list[Publisher] = Field(default_factory=list)
    covers: str | None = None
    reason: str | None = None

    @model_validator(mode="after")
    def _says_what_or_why_not(self) -> PlannedGrounding:
        if self.corpus is None and not self.reason:
            raise ValueError("a pack with no corpus says why it answers only from documents")
        if self.corpus is not None and not (self.publishers and self.covers):
            raise ValueError(f"corpus {self.corpus!r} names its publishers and what it covers")
        return self


class Documents(Strict):
    core: list[Slug]
    proposed: dict[Slug, DocumentTypeSpec]
    uses: list[Slug]  # types another entry proposes


class Entry(Strict):
    id: Slug
    display_name: str = Field(min_length=3, max_length=60)
    serves: str = Field(min_length=8)
    need: str = Field(min_length=20)
    documents: Documents
    # reminder, alert and advice are built; tracker is specified in the core registers.
    modules: list[Literal["reminder", "alert", "tracker", "advice"]] = Field(min_length=1)
    reminders: list[str]
    grounding: PlannedGrounding
    stance: str = Field(min_length=20)
    open: str | None = None


def _entries() -> list[Entry]:
    raw = yaml.safe_load(CATALOGUE.read_text(encoding="utf-8"))
    return [Entry.model_validate(entry) for entry in raw["packs"]]


ENTRIES = _entries()
CORE_TYPES = catalog().documents.document_types


def _proposed() -> dict[str, DocumentTypeSpec]:
    return {name: spec for e in ENTRIES for name, spec in e.documents.proposed.items()}


def test_the_catalogue_names_nine_packs_none_of_them_built() -> None:
    ids = [entry.id for entry in ENTRIES]
    assert len(ids) == 9 and len(set(ids)) == 9
    assert not set(ids) & {installed.id for installed in installed_packs()}


def test_every_core_document_type_a_pack_reuses_exists() -> None:
    for entry in ENTRIES:
        missing = set(entry.documents.core) - set(CORE_TYPES)
        assert not missing, f"{entry.id} reuses {sorted(missing)}, not in core/documents.yaml"


def test_a_proposed_type_is_new_and_proposed_once() -> None:
    seen: dict[str, str] = {}
    for entry in ENTRIES:
        for name in entry.documents.proposed:
            assert name not in CORE_TYPES, f"{entry.id} proposes {name}, already a core type"
            assert name not in seen, f"{name} proposed by both {seen[name]} and {entry.id}"
            seen[name] = entry.id


def test_a_used_type_is_proposed_by_another_entry() -> None:
    proposed = _proposed()
    for entry in ENTRIES:
        for name in entry.documents.uses:
            assert name in proposed and name not in entry.documents.proposed, (entry.id, name)


@pytest.mark.parametrize("name", sorted(_proposed()))
def test_a_proposed_type_could_be_pasted_into_the_core_catalogue(name: str) -> None:
    spec = _proposed()[name]
    fields = {field.name: field for field in spec.fields}
    assert len(fields) == len(spec.fields), f"{name} declares a field twice"
    if spec.subject_field is not None:
        assert fields[spec.subject_field].type == "person", f"{name}: subject is not a person"


def test_a_field_name_lands_in_one_facts_column_everywhere() -> None:
    """A field name is a `facts.key` with one column. A proposal that reused a core name with a
    different type would split one key across two columns the day it moved into the core."""
    columns = {
        field.name: FACT_COLUMN[field.type] for spec in CORE_TYPES.values() for field in spec.fields
    }
    for name, spec in _proposed().items():
        for field in spec.fields:
            column = FACT_COLUMN[field.type]
            assert columns.setdefault(field.name, column) == column, (
                f"{name}.{field.name} would land in {column}, but the name already lands in "
                f"{columns[field.name]}"
            )


def test_every_reminder_reads_a_date_one_of_the_packs_documents_prints() -> None:
    proposed = _proposed()
    for entry in ENTRIES:
        reachable = {*entry.documents.core, *entry.documents.proposed, *entry.documents.uses}
        for reminder in entry.reminders:
            doc_type, _, field_name = reminder.partition(".")
            assert doc_type in reachable, f"{entry.id}: {reminder} reads a type it does not name"
            spec = CORE_TYPES.get(doc_type) or proposed[doc_type]
            types = {field.name: field.type for field in spec.fields}
            assert types.get(field_name) == "date", f"{entry.id}: {reminder} is not a date field"
        if entry.reminders:
            assert "reminder" in entry.modules, f"{entry.id} lists reminders without the module"


def test_the_write_up_covers_every_pack() -> None:
    text = WRITE_UP.read_text(encoding="utf-8")
    for entry in ENTRIES:
        assert f"`{entry.id}`" in text, f"packs/CATALOGUE.md does not mention {entry.id}"
