"""Every statement the ingestion worker runs, written out in full.

Rule 1 in AGENTS.md: no SQL is generated at runtime. These are parameterised and hand-written,
and a query that is not here does not exist. If a feature seems to need a query built from a
string, that is an ADR, not a helper function.
"""

from __future__ import annotations

# Re-ingesting a document replaces its derived rows rather than accumulating them. The document
# row itself is never deleted, so its id - and therefore every citation that points at it -
# survives a re-parse.
DELETE_CHUNKS = "DELETE FROM chunks WHERE document_id = %(document_id)s"
DELETE_FACTS = "DELETE FROM facts WHERE document_id = %(document_id)s"

INSERT_CHUNK = """
INSERT INTO chunks (document_id, page, ordinal, context_prefix, text, embedding)
VALUES (%(document_id)s, %(page)s, %(ordinal)s, %(context_prefix)s, %(text)s, %(embedding)s)
ON CONFLICT (document_id, page, ordinal) DO UPDATE
   SET context_prefix = EXCLUDED.context_prefix,
       text           = EXCLUDED.text,
       embedding      = EXCLUDED.embedding
"""

# facts.document_id and facts.page are NOT NULL in the schema. There is deliberately no
# statement in this file that writes a fact without both.
INSERT_FACT = """
INSERT INTO facts (
    document_id, page, pack_id, pack_version, key, subject,
    value_text, value_num, value_date, confidence
)
VALUES (
    %(document_id)s, %(page)s, %(pack_id)s, %(pack_version)s, %(key)s, %(subject)s,
    %(value_text)s, %(value_num)s, %(value_date)s, %(confidence)s
)
RETURNING id
"""

MARK_INDEXED = """
UPDATE documents
   SET status = 'indexed',
       pages = %(pages)s,
       doc_type = %(doc_type)s,
       pack_id = %(pack_id)s,
       quarantine_reason = NULL
 WHERE id = %(document_id)s
"""

MARK_QUARANTINED = """
UPDATE documents
   SET status = 'quarantined',
       pages = %(pages)s,
       quarantine_reason = %(reason)s
 WHERE id = %(document_id)s
"""

SELECT_QUARANTINED = """
SELECT id, original_name, mime, quarantine_reason, pages
  FROM documents
 WHERE status = 'quarantined'
 ORDER BY ingested_at
 LIMIT %(limit)s
"""

COUNT_BY_STATUS = "SELECT status, count(*) FROM documents GROUP BY status ORDER BY status"

# The idempotency keys for a set of documents at once, so a screen listing the quarantine queue
# can say which of them still have a file behind them without a query per row.
SELECT_DIGESTS = """
SELECT id, sha256
  FROM documents
 WHERE id = ANY(%(document_ids)s::uuid[])
"""

INSERT_TRACE = """
INSERT INTO traces (thread_id, node, latency_ms, model, payload)
VALUES (%(thread_id)s, %(node)s, %(latency_ms)s, %(model)s, %(payload)s)
"""

# An obligation hangs off the fact that created it, and `obligations.fact_id` cascades on
# delete, so re-extracting a document replaces its obligations without a second statement.
INSERT_OBLIGATION = """
INSERT INTO obligations (fact_id, pack_id, label, due_date, lead_days, recurrence)
VALUES (%(fact_id)s, %(pack_id)s, %(label)s, %(due_date)s, %(lead_days)s, %(recurrence)s)
RETURNING id
"""

# A pack-level obligation - a filing deadline - belongs to no document, so it is inserted once
# and recognised by the pack, label and date it already has.
INSERT_FIXED_OBLIGATION = """
INSERT INTO obligations (fact_id, pack_id, label, due_date, lead_days, recurrence)
SELECT NULL, %(pack_id)s, %(label)s, %(due_date)s, %(lead_days)s, %(recurrence)s
 WHERE NOT EXISTS (
     SELECT 1 FROM obligations
      WHERE pack_id = %(pack_id)s AND label = %(label)s AND due_date = %(due_date)s
 )
RETURNING id
"""
