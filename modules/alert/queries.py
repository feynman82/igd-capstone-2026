"""Every query the Alert module runs, hand-written and parameterised.

Rule 1 in AGENTS.md, and here it does real work rather than ceremony. A pack declares an alert
against a **metric**, and a metric is not a field — `srs_contributions_ytd` is a thing you work
out from several `contributions_ytd` facts, and `days_uncovered` is a gap between two dates.
Generating those queries from the metric name is exactly the kind of cleverness rule 1 exists to
prevent, so each metric is a named query written out in full below.

Adding a metric means adding a query here and naming it in a pack. That is deliberately a small
amount of friction: a metric nobody wrote down is a number nobody can check.
"""

from __future__ import annotations

# --------------------------------------------------------------------------------- metrics

# Contributions to the Supplementary Retirement Scheme so far this year. The statement restates
# the year-to-date total, so the newest statement wins rather than the values being summed.
SRS_CONTRIBUTIONS_YTD = """
SELECT f.value_num, f.subject, f.document_id, f.page, d.original_name
  FROM facts f
  JOIN documents d ON d.id = f.document_id
 WHERE f.pack_id = 'iras_tax'
   AND f.key = 'contributions_ytd'
   AND f.value_num IS NOT NULL
 ORDER BY f.created_at DESC
 LIMIT 1
"""

# Tax-deductible donations are separate receipts, so these are added up.
DONATIONS_YTD = """
SELECT coalesce(sum(f.value_num), 0), count(*)
  FROM facts f
 WHERE f.pack_id = 'iras_tax'
   AND f.key = 'donation_amount'
   AND f.value_num IS NOT NULL
"""

CPF_CONTRIBUTIONS_YTD = """
SELECT coalesce(sum(f.value_num), 0), count(*)
  FROM facts f
 WHERE f.pack_id = 'iras_tax'
   AND f.key = 'cpf_employee'
   AND f.value_num IS NOT NULL
"""

# Days a person has been without cover: the most recent expiry that is already past, when no
# policy for that same subject runs beyond today. Zero when everything is still in force.
DAYS_UNCOVERED = """
SELECT f.subject,
       max(f.value_date) AS last_expiry,
       max(f.value_date) FILTER (WHERE f.value_date >= %(today)s) AS still_covered
  FROM facts f
 WHERE f.pack_id = 'insurance_agent'
   AND f.key = 'expiry_date'
   AND f.value_date IS NOT NULL
 GROUP BY f.subject
"""

# The documents behind a metric, so an alert can cite what it is talking about.
EVIDENCE_FOR_KEY = """
SELECT d.original_name, f.page, f.value_num, f.value_date, f.subject
  FROM facts f
  JOIN documents d ON d.id = f.document_id
 WHERE f.pack_id = %(pack_id)s
   AND f.key = %(key)s
 ORDER BY f.created_at DESC
 LIMIT %(limit)s
"""

# ------------------------------------------------------------------------------- the debounce

# A fired alert is written to `traces`, which is the audit trail the schema already provides.
# The debounce reads the last one back. When Alert earns its own table that is a migration, and
# a migration is its own reviewed pull request.
LAST_FIRED = """
SELECT created_at, payload
  FROM traces
 WHERE node = 'alert'
   AND thread_id = %(key)s
 ORDER BY created_at DESC
 LIMIT 1
"""

RECORD_FIRED = """
INSERT INTO traces (thread_id, node, latency_ms, model, payload)
VALUES (%(key)s, 'alert', 0, NULL, %(payload)s)
"""
