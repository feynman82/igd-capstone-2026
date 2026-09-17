"""Index a pack's published sources, and stage the values they print for a person to review.

Every source a pack's corpus records is upserted into `grounding_sources` on each run, because
its title, publisher and review date belong to `sources.yaml` and are refreshed even when the
text has not changed. The text itself changes rarely, so its hash decides whether anything else
happens: unchanged, extraction is skipped entirely; changed, whatever a person had approved off
the old text can no longer be trusted, so it is superseded, and the model reads the new text
again. Nothing this module writes is `approved` — that column is `core.grounding.review`'s alone
(ADR 0016).

The model reads a changed source before anything about it is written. If the model is down,
the pack's transaction is rolled back and the error raised, so the stored hash, the approved
values and the review fields stay exactly as they were, and the next run tries again.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from core.grounding.corpus import SourceText, load_corpus
from core.grounding.values import extract_values
from core.packs import PACKS_DIR, InstalledPack
from core.runtime.ollama import ModelUnavailable, Ollama

log = logging.getLogger(__name__)

# --------------------------------------------------------------------------------- the SQL

SELECT_SOURCE = """
SELECT id, sha256
  FROM grounding_sources
 WHERE pack_id = %(pack_id)s AND corpus_id = %(corpus_id)s AND file = %(file)s
"""

UPSERT_SOURCE = """
INSERT INTO grounding_sources
    (pack_id, corpus_id, file, title, publisher, publisher_kind, url, published_on,
     retrieved_on, applies_to, review_by, reviewed_by, reviewed_on, sha256)
VALUES
    (%(pack_id)s, %(corpus_id)s, %(file)s, %(title)s, %(publisher)s, %(publisher_kind)s,
     %(url)s, %(published_on)s, %(retrieved_on)s, %(applies_to)s, %(review_by)s,
     %(reviewed_by)s, %(reviewed_on)s, %(sha256)s)
ON CONFLICT (pack_id, corpus_id, file) DO UPDATE
   SET title          = EXCLUDED.title,
       publisher      = EXCLUDED.publisher,
       publisher_kind = EXCLUDED.publisher_kind,
       url            = EXCLUDED.url,
       published_on   = EXCLUDED.published_on,
       retrieved_on   = EXCLUDED.retrieved_on,
       applies_to     = EXCLUDED.applies_to,
       review_by      = EXCLUDED.review_by,
       reviewed_by    = EXCLUDED.reviewed_by,
       reviewed_on    = EXCLUDED.reviewed_on,
       sha256         = EXCLUDED.sha256,
       indexed_at     = now()
RETURNING id
"""

DELETE_PENDING = "DELETE FROM grounding_values WHERE source_id=%(s)s AND status='pending'"

SUPERSEDE_APPROVED = """
UPDATE grounding_values
   SET status='rejected', note='source text changed', reviewed_by='parrot', reviewed_on=%(today)s
 WHERE source_id=%(s)s AND status='approved'
"""

INSERT_VALUE = """
INSERT INTO grounding_values
    (source_id, pack_id, key, unit, value_num, value_text, qualifiers, passage, extracted_by,
     confidence)
VALUES
    (%(source_id)s, %(pack_id)s, %(key)s, %(unit)s, %(value_num)s, %(value_text)s,
     %(qualifiers)s::jsonb, %(passage)s, 'model', %(confidence)s)
"""


# --------------------------------------------------------------------------------- the report


@dataclass(frozen=True, slots=True)
class IndexReport:
    """What one call to `index_pack` did, so a script can say it in a line per pack."""

    sources: int
    unchanged: int
    pending: int
    superseded: int
    unread: int = 0  # sources the model could not read; no hash is stored, so the next run retries


def index_pack(
    conn: Any,
    client: Ollama,
    installed: InstalledPack,
    *,
    root: Path = PACKS_DIR,
    today: date,
) -> IndexReport:
    """Upsert this pack's sources and stage the values a changed one prints.

    A pack with no corpus (`load_corpus` returns `[]`) returns all zeros: there is nothing to
    upsert and nothing to extract. Every source is upserted whether or not its text changed,
    because `sources.yaml` may have been re-reviewed without the text itself moving.

    A new or changed source is extracted first, and only then are its pending values deleted,
    its approved values superseded, its row upserted with the new hash and the new values
    inserted. A source the model cannot read (`ModelUnavailable`) is skipped before anything of it
    is written, so its stored hash and values stay as they were and the next run retries it; the
    other sources are kept. On 17 September one MoneySense FAQ section hung the 4B model until the
    request timed out, and rolling the pack back threw away the 9x and 4x read from two other
    sources. Any other error rolls the whole pack back and is re-raised.
    """
    sources = 0
    unchanged = 0
    pending = 0
    superseded = 0
    unread = 0
    keys = installed.manifest.grounding.values

    try:
        with conn.cursor() as cur:
            for source in load_corpus(installed, root=root):
                sources += 1
                cur.execute(
                    SELECT_SOURCE,
                    {
                        "pack_id": source.pack_id,
                        "corpus_id": source.corpus.corpus_id,
                        "file": source.document.file,
                    },
                )
                existing = cur.fetchone()

                if existing is not None and existing[1] == source.sha256:
                    _upsert_source(cur, source)
                    unchanged += 1
                    continue

                # The model reads the new text before anything is written. An outage raises
                # here, while the stored hash and approved values are still untouched.
                try:
                    values = extract_values(client, source, keys)
                except ModelUnavailable as error:
                    log.warning("%s not read: %s", source.document.file, error)
                    unread += 1
                    continue

                if existing is not None:
                    cur.execute(DELETE_PENDING, {"s": existing[0]})
                    cur.execute(SUPERSEDE_APPROVED, {"s": existing[0], "today": today})
                    superseded += cur.rowcount

                source_id = _upsert_source(cur, source)
                for value in values:
                    cur.execute(
                        INSERT_VALUE,
                        {
                            "source_id": source_id,
                            "pack_id": source.pack_id,
                            "key": value.key,
                            "unit": value.unit,
                            "value_num": value.value_num,
                            "value_text": value.value_text,
                            "qualifiers": json.dumps(value.qualifiers),
                            "passage": value.passage,
                            "confidence": value.confidence,
                        },
                    )
                    pending += 1
    except Exception:
        conn.rollback()
        raise

    conn.commit()
    return IndexReport(
        sources=sources, unchanged=unchanged, pending=pending, superseded=superseded, unread=unread
    )


def _upsert_source(cur: Any, source: SourceText) -> Any:
    """Insert or refresh the source's row, and return its id."""
    cur.execute(
        UPSERT_SOURCE,
        {
            "pack_id": source.pack_id,
            "corpus_id": source.corpus.corpus_id,
            "file": source.document.file,
            "title": source.document.title,
            "publisher": source.document.publisher,
            "publisher_kind": source.document.publisher_kind,
            "url": source.document.url,
            "published_on": source.document.published,
            "retrieved_on": source.document.retrieved,
            "applies_to": source.document.applies_to,
            "review_by": source.document.review_by,
            "reviewed_by": source.reviewed_by,
            "reviewed_on": source.reviewed_on,
            "sha256": source.sha256,
        },
    )
    row = cur.fetchone()
    assert row is not None  # RETURNING id always gives back exactly one row
    return row[0]
