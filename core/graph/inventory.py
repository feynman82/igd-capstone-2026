"""The documents on file, read from `facts` rather than searched for.

"Do I have car insurance?" is not a similarity question, and on 13 September the answer was the
five words "You have car insurance." — true, and useless. The household already has the list:
every document a pack read a name off. One hand-written query returns it (rule 1), and each line
cites the page its name was printed on (rule 2 already guarantees there is one).

It is also what makes "no" sayable. "None of the 5 policies on file is a dental plan" cites the
five, which is a claim about the vault and nothing else — a group policy from an employer that
was never filed is not in it, and the sentence does not pretend otherwise.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from core.contracts import Category
from core.graph.knowledge import categorise
from core.graph.ports import Passage
from core.packs import InstalledPack

INVENTORY = """
SELECT d.id, d.original_name, d.doc_type, d.pack_id,
       f.id, f.key, f.page, coalesce(f.value_text, f.value_num::text, f.value_date::text),
       f.subject
  FROM documents d
  JOIN facts f ON f.document_id = d.id
 WHERE d.status = 'indexed'
   AND d.pack_id = ANY(%(packs)s::text[])
 ORDER BY d.original_name, f.id
"""

QUARANTINED = "SELECT count(*) FROM documents WHERE status = 'quarantined'"


@dataclass(frozen=True, slots=True)
class Holding:
    document_id: Any
    document_name: str
    pack_id: str
    doc_type: str
    title: str  # the document's string fields in the pack's order, as ADR 0012 names a chunk
    subject: str | None
    category: Category | None
    printed_name: str  # the value the categories read, exactly as printed
    fact_id: int  # the fact the name was read from: what a citation points at
    page: int
    details: tuple[tuple[str, str], ...]  # (field, value) in the pack's declared order

    def passage(self) -> Passage:
        lines = "; ".join(f"{name.replace('_', ' ')}: {value}" for name, value in self.details)
        return Passage(
            chunk_id=self.fact_id,
            document_id=self.document_id,
            page=self.page,
            text=f"{self.title}. {lines}.",
            score=1.0,
            document_name=self.document_name,
            context_prefix=(
                f"{self.title} — {self.doc_type.replace('_', ' ')} — on file — page {self.page}"
            ),
            pack_id=self.pack_id,
            kind="inventory",
        )


def holdings(rows: Sequence[Sequence[Any]], packs: Sequence[InstalledPack]) -> list[Holding]:
    """Rows of `INVENTORY`, one holding per document that prints the field its pack's categories
    read. A renewal notice prints no product name, so it is not counted as a second policy."""
    by_pack = {installed.id: installed for installed in packs}
    grouped: dict[Any, list[Sequence[Any]]] = {}
    for found in rows:
        grouped.setdefault(found[0], []).append(found)

    out: list[Holding] = []
    for document_id, facts in grouped.items():
        name, doc_type, pack_id = str(facts[0][1]), str(facts[0][2]), str(facts[0][3])
        installed = by_pack.get(pack_id)
        categories = installed.manifest.answering.categories if installed else None
        if installed is None or categories is None:
            continue
        spec = installed.manifest.document_types.get(doc_type)
        values = {str(f[5]): (int(f[4]), int(f[6]), f[7]) for f in facts if f[7] is not None}
        if spec is None or categories.match_field not in values:
            continue
        fact_id, page, printed = values[categories.match_field]
        strings = [
            str(values[f.name][2]) for f in spec.fields if f.type == "string" and f.name in values
        ]
        subject = (
            str(values[spec.subject_field][2])
            if spec.subject_field and spec.subject_field in values
            else None
        )
        out.append(
            Holding(
                document_id=document_id,
                document_name=name,
                pack_id=pack_id,
                doc_type=doc_type,
                title=", ".join(strings) or name,
                subject=subject,
                category=categorise(str(printed), categories),
                printed_name=str(printed),
                fact_id=fact_id,
                page=page,
                details=tuple(
                    (f.name, str(values[f.name][2])) for f in spec.fields if f.name in values
                ),
            )
        )
    return out


class Inventory(Protocol):
    def holdings(self, packs: Sequence[InstalledPack]) -> list[Holding]: ...

    def quarantined(self) -> int: ...


@dataclass(frozen=True, slots=True)
class HouseholdInventory:
    """Handed to `AnswerGraph` by whoever holds a connection, as `HouseholdScope` is."""

    conn: Any

    def holdings(self, packs: Sequence[InstalledPack]) -> list[Holding]:
        if not packs:
            return []
        with self.conn.cursor() as cur:
            cur.execute(INVENTORY, {"packs": sorted(installed.id for installed in packs)})
            rows = cur.fetchall()
        return holdings(rows, packs)

    def quarantined(self) -> int:
        with self.conn.cursor() as cur:
            cur.execute(QUARANTINED)
            found = cur.fetchone()
        return int(found[0]) if found else 0
