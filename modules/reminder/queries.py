"""Every query the Reminder module runs, hand-written and parameterised.

Rule 1 in AGENTS.md. A module reads typed rows; it never builds a query from a string and never
sees the interface it will be rendered on.

The sweep answers one question: *what is inside a lead window today, and has it already been
said?* A pack declares its lead windows — insurance uses 60, 30 and 7 days — and the
"nothing fires twice" requirement means once per **window**, not once per obligation. A renewal
60 days out should be mentioned again at 30 days, and should not be mentioned twice at 30.

That is computed from the two columns the schema already has. For an obligation due on `D` with
lead days `L`, today `T`:

    days_left    = D - T
    active leads = every l in L where days_left <= l
    current lead = the tightest active one
    window opens = D - current_lead

It is due to be said when `last_notified_at` is null, or predates the day the current window
opened. Nothing else is needed, and in particular nothing needs a new column.
"""

from __future__ import annotations

# Everything not yet done or dismissed, with the fact and document behind it. The lead window
# arithmetic happens in Python because it is easier to read there and easier to test there; the
# database's job is to hand over the rows without a generated predicate.
DUE_SWEEP = """
SELECT o.id,
       o.pack_id,
       o.label,
       o.due_date,
       o.lead_days,
       o.state,
       o.last_notified_at,
       f.document_id,
       f.page,
       d.original_name
  FROM obligations o
  LEFT JOIN facts f     ON f.id = o.fact_id
  LEFT JOIN documents d ON d.id = f.document_id
 WHERE o.state IN ('pending', 'notified')
   AND o.due_date >= %(floor)s
 ORDER BY o.due_date, o.id
"""

MARK_NOTIFIED = """
UPDATE obligations
   SET state = 'notified',
       last_notified_at = %(now)s
 WHERE id = %(obligation_id)s
"""

MARK_DONE = "UPDATE obligations SET state = 'done' WHERE id = %(obligation_id)s"

MARK_DISMISSED = "UPDATE obligations SET state = 'dismissed' WHERE id = %(obligation_id)s"

# Anything whose date has passed and which nobody closed. Not a reminder — a different screen.
OVERDUE = """
SELECT o.id, o.pack_id, o.label, o.due_date, d.original_name
  FROM obligations o
  LEFT JOIN facts f     ON f.id = o.fact_id
  LEFT JOIN documents d ON d.id = f.document_id
 WHERE o.state IN ('pending', 'notified')
   AND o.due_date < %(today)s
 ORDER BY o.due_date
"""

# One open obligation, with what `next_window` needs to say when it will speak again. Used
# before a close or a snooze so that acting on a row that is already done says so, rather than
# reporting success for an UPDATE that matched nothing.
SELECT_OPEN = """
SELECT o.id, o.due_date, o.lead_days
  FROM obligations o
 WHERE o.id = %(obligation_id)s
   AND o.state IN ('pending', 'notified')
"""
