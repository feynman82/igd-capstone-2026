"""Every query the advice module runs, hand-written and parameterised.

Rule 1 in AGENTS.md. A pack names the document types, fields and value keys a shape reads; it
never supplies SQL. The field and key arrive as bound parameters to the four fixed statements
below, so a pack author can change what is read and never how.

Two properties of advice live in this SQL rather than in Python, because a calculator trusts
whatever rows it is handed:

- **Whose facts.** A fact counts only when its printed subject is one of the person's names: the
  display name or a *confirmed* alias. An alias the model proposed and nobody confirmed scopes
  nothing, and a document with no subject is never advised on.
- **Which published values.** A value counts only when it is approved, its source has been
  reviewed and is not past `review_by`, its effective dates cover today, and it was retrieved
  recently enough (ADR 0016, decision 3).
"""

from __future__ import annotations

# The facts one field of one person's indexed documents prints, newest document first.
# Parameters: `pack`, `doc_types` (text[]), `field`, `names` (text[], trimmed and lower-cased).
#
# Rows: id, document_id, original_name, doc_type, page, key, value_num, value_text, value_date,
# subject, ingested_at.
FACTS_FOR = """
SELECT f.id, f.document_id, d.original_name, d.doc_type, f.page, f.key,
       f.value_num, f.value_text, f.value_date, f.subject, d.ingested_at
  FROM facts f
  JOIN documents d ON d.id = f.document_id
 WHERE d.status = 'indexed'
   AND f.pack_id = %(pack)s
   AND d.doc_type = ANY(%(doc_types)s::text[])
   AND f.key = %(field)s
   AND lower(btrim(f.subject)) = ANY(%(names)s::text[])
 ORDER BY d.ingested_at DESC, f.id DESC
"""

# The printed name a category is read from, for each document. Newest fact first, so the first
# row per document is the one a re-extraction wrote last.
#
# Rows: document_id, value_text.
PRODUCT_NAMES_FOR = """
SELECT document_id, value_text
  FROM facts
 WHERE document_id = ANY(%(ids)s::uuid[])
   AND key = %(match_field)s
 ORDER BY id DESC
"""

# Each person's display name and confirmed aliases. A person with no confirmed alias still
# returns one row, with a null alias, so the display name is never lost.
#
# Rows: id, display_name, alias.
NAMES_FOR = """
SELECT p.id, p.display_name, a.alias
  FROM people p
  LEFT JOIN person_aliases a ON a.person_id = p.id AND a.confirmed
 WHERE p.id = ANY(%(ids)s::bigint[])
"""

# Approved, reviewed, current values of one key, newest first. `oldest` is today less the pack's
# `max_price_age_days` for a price (a money key qualified by product), otherwise less
# `max_rule_age_days`: a premium goes stale in months, a published multiple in a year.
#
# Rows: id, key, unit, value_num, value_text, qualifiers, passage, effective_from, title,
# publisher, url, published_on, retrieved_on.
VALUES_FOR = """
SELECT v.id, v.key, v.unit, v.value_num, v.value_text, v.qualifiers, v.passage, v.effective_from,
       s.title, s.publisher, s.url, s.published_on, s.retrieved_on
  FROM grounding_values v
  JOIN grounding_sources s ON s.id = v.source_id
 WHERE v.pack_id = %(pack)s
   AND v.key = %(key)s
   AND v.status = 'approved'
   AND s.reviewed_on IS NOT NULL
   AND s.review_by >= %(today)s
   AND (v.effective_from IS NULL OR v.effective_from <= %(today)s)
   AND (v.effective_to IS NULL OR v.effective_to >= %(today)s)
   AND s.retrieved_on >= %(oldest)s
 ORDER BY v.effective_from DESC NULLS LAST, s.retrieved_on DESC, v.id DESC
"""
