"""The owner's consent to a pack's advice, append-only (ADR 0016).

Consent is the owner's decision, not the household's: an adult member's advice is answered under
the owner's say-so, recorded once per pack version, granted or withdrawn, never edited in place.
`current` is what a calculator checks before it is allowed to run at all; `status` is what a
screen shows so a person can tell "withdrawn" from "never asked" from "the wording changed since
you last said yes".

Every write here goes through `core.household.owner`: there is no consent that is not the
owner's, and a household with no owner yet — a fresh install, ADR 0011 — has nothing to read or
grant, which is `NoOwner` rather than a guess.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Literal

from core import household

Channel = Literal["web", "telegram", "cli"]
ConsentStatus = Literal["granted", "withdrawn", "none", "outdated"]


class NoOwner(RuntimeError):
    """No owner is recorded yet, so there is nobody whose consent this could be (ADR 0016)."""


# --------------------------------------------------------------------------------- the SQL
#
# Rule 1: every statement is written here and parameterised. Nothing is assembled at runtime.

LATEST = """
SELECT id, action, version
  FROM advice_consents
 WHERE person_id = %(p)s AND pack_id = %(k)s
 ORDER BY recorded_at DESC, id DESC
 LIMIT 1
"""

INSERT_CONSENT = """
INSERT INTO advice_consents (person_id, pack_id, version, wording_sha256, action, channel)
VALUES (%(person_id)s, %(pack_id)s, %(version)s, %(wording_sha256)s, %(action)s, %(channel)s)
RETURNING id
"""


def _latest(conn: Any, person_id: int, pack_id: str) -> tuple[int, str, str] | None:
    with conn.cursor() as cur:
        cur.execute(LATEST, {"p": person_id, "k": pack_id})
        row = cur.fetchone()
    return (int(row[0]), str(row[1]), str(row[2])) if row is not None else None


def current(conn: Any, pack_id: str, version: str) -> int | None:
    """The granting row's id, only when the owner's latest action for this pack is `granted` at
    exactly this version. Anything else — withdrawn, no owner, no consent at all, or a version
    that has since moved on — reads as `None`, so a calculator that only checks "is this not
    `None`" cannot mistake a stale grant for a current one."""
    person = household.owner(conn)
    if person is None:
        return None
    latest = _latest(conn, person.id, pack_id)
    if latest is None:
        return None
    row_id, action, recorded_version = latest
    return row_id if action == "granted" and recorded_version == version else None


def status(conn: Any, pack_id: str, version: str) -> ConsentStatus:
    """What the owner's latest action for this pack says, read against the version asked for.

    `"outdated"` is its own answer rather than folding into `"none"`, because the two read
    differently on a screen: "you have never said yes" and "you said yes to an older wording"
    ask for different consent text.
    """
    person = household.owner(conn)
    if person is None:
        return "none"
    latest = _latest(conn, person.id, pack_id)
    if latest is None:
        return "none"
    _, action, recorded_version = latest
    if action == "withdrawn":
        return "withdrawn"
    return "granted" if recorded_version == version else "outdated"


def _record(
    conn: Any,
    pack_id: str,
    version: str,
    wording: str,
    channel: Channel,
    action: Literal["granted", "withdrawn"],
) -> int:
    person = household.owner(conn)
    if person is None:
        raise NoOwner("no owner is recorded yet; consent is the owner's to give (ADR 0016)")
    with conn.cursor() as cur:
        cur.execute(
            INSERT_CONSENT,
            {
                "person_id": person.id,
                "pack_id": pack_id,
                "version": version,
                "wording_sha256": hashlib.sha256(wording.encode("utf-8")).digest(),
                "action": action,
                "channel": channel,
            },
        )
        row = cur.fetchone()
    assert row is not None  # RETURNING id always gives back exactly one row
    conn.commit()
    return int(row[0])


def grant(conn: Any, pack_id: str, version: str, wording: str, channel: Channel) -> int:
    """Record the owner saying yes to `wording`, this pack's consent text at `version`."""
    return _record(conn, pack_id, version, wording, channel, "granted")


def withdraw(conn: Any, pack_id: str, version: str, wording: str, channel: Channel) -> int:
    """Record the owner taking it back. Append-only: the grant stays in the table, superseded
    by this row rather than deleted, so the history of who said what and when is never lost."""
    return _record(conn, pack_id, version, wording, channel, "withdrawn")


@dataclass(frozen=True, slots=True)
class HouseholdConsents:
    """`core.graph.advice.ConsentBook` over a live connection, for the graph to ask without
    knowing this module's SQL exists."""

    conn: Any

    def current(self, pack_id: str, version: str) -> int | None:
        return current(self.conn, pack_id, version)
