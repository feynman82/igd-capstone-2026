"""Every query the Alert module runs, hand-written and parameterised.

Rule 1 in AGENTS.md, and here it does real work rather than ceremony. A pack declares an alert
against a **metric**, and a metric is not a field — `srs_contributions_ytd` is a thing you work
out from several `contributions_ytd` facts, and `days_uncovered` is a gap between two dates.
Generating those queries from the metric name is exactly the kind of cleverness rule 1 exists to
prevent, so each metric is a named query written out in full below.

Adding a metric means adding a query here and naming it in a pack. That is deliberately a small
amount of friction: a metric nobody wrote down is a number nobody can check.

Every metric query returns **one row per fact, with the document and page it came from**, and
`modules/alert/__init__.py` does the grouping by person. That is what keeps a number and the
documents it cites on the same person: they are the same rows. A household has dozens of these
documents, not millions, so there is nothing to win by aggregating in SQL.
"""

from __future__ import annotations

# --------------------------------------------------------------------------------- metrics

# A year-to-date metric covers the calendar year of the day the sweep runs for. The year lives on
# a sibling fact of the same document — a statement's `statement_year`, a receipt's
# `donation_date`, a payslip's `pay_period` — so each query checks that fact exists and matches.
# Parameters: `year`, `year_text`, `year_start`, `next_year_start`.

# Contributions to the Supplementary Retirement Scheme so far this year. A statement restates the
# year-to-date total, so the figures are not summed: each holder's largest total for the year is
# their latest statement, because contributions within a year only accumulate. Ordering by
# `created_at` instead would let an older statement filed later win.
#
# Rows: subject, value_num, original_name, page.
SRS_CONTRIBUTIONS_YTD = """
SELECT f.subject, f.value_num, d.original_name, f.page
  FROM facts f
  JOIN documents d ON d.id = f.document_id
 WHERE f.pack_id = 'core'
   AND f.key = 'contributions_ytd'
   AND f.value_num IS NOT NULL
   AND EXISTS (
       SELECT 1
         FROM facts y
        WHERE y.document_id = f.document_id
          AND y.pack_id = f.pack_id
          AND y.key = 'statement_year'
          AND y.value_num = %(year)s
   )
 ORDER BY f.subject, f.value_num DESC, f.created_at DESC, f.id DESC
"""

# Tax-deductible donations are separate receipts, so these are added up. A receipt counts only
# when it states it is deductible: `tax_deductible` is stored as text, and a model returning a
# JSON boolean writes "True" where the register writes "true". A receipt that says nothing either
# way is not counted, because relief claimed on a donation that does not qualify is the costlier
# mistake.
#
# Rows: subject, value_num, original_name, page — newest first.
DONATIONS_YTD = """
SELECT f.subject, f.value_num, d.original_name, f.page
  FROM facts f
  JOIN documents d ON d.id = f.document_id
 WHERE f.pack_id = 'core'
   AND f.key = 'donation_amount'
   AND f.value_num IS NOT NULL
   AND EXISTS (
       SELECT 1
         FROM facts y
        WHERE y.document_id = f.document_id
          AND y.pack_id = f.pack_id
          AND y.key = 'donation_date'
          AND y.value_date >= %(year_start)s
          AND y.value_date < %(next_year_start)s
   )
   AND EXISTS (
       SELECT 1
         FROM facts t
        WHERE t.document_id = f.document_id
          AND t.pack_id = f.pack_id
          AND t.key = 'tax_deductible'
          AND lower(btrim(t.value_text)) = 'true'
   )
 ORDER BY f.subject, f.created_at DESC, f.id DESC
"""

# Employee CPF deducted on this year's payslips, added up. `pay_period` is text, as YYYY-MM.
#
# Rows: subject, value_num, original_name, page — newest first.
CPF_CONTRIBUTIONS_YTD = """
SELECT f.subject, f.value_num, d.original_name, f.page
  FROM facts f
  JOIN documents d ON d.id = f.document_id
 WHERE f.pack_id = 'core'
   AND f.key = 'cpf_employee'
   AND f.value_num IS NOT NULL
   AND EXISTS (
       SELECT 1
         FROM facts y
        WHERE y.document_id = f.document_id
          AND y.pack_id = f.pack_id
          AND y.key = 'pay_period'
          AND left(btrim(y.value_text), 4) = %(year_text)s
   )
 ORDER BY f.subject, f.created_at DESC, f.id DESC
"""

# Every expiry date, with the policy number printed on the same document. Days uncovered is
# worked out per person AND per policy: grouped by person alone, a live travel policy made a motor
# policy that lapsed months ago read as covered. `policy_no` is compared exactly as printed, which
# is how the pack declares it. An expiry on a document with no policy number is its own group.
#
# Rows: subject, policy_no, value_date, original_name, page.
DAYS_UNCOVERED = """
SELECT f.subject, p.value_text AS policy_no, f.value_date, d.original_name, f.page
  FROM facts f
  JOIN documents d ON d.id = f.document_id
  LEFT JOIN facts p
         ON p.document_id = f.document_id
        AND p.pack_id = f.pack_id
        AND p.key = 'policy_no'
 WHERE f.pack_id = 'core'
   AND f.key = 'expiry_date'
   AND f.value_date IS NOT NULL
 ORDER BY f.subject, policy_no, f.value_date DESC, f.id DESC
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
