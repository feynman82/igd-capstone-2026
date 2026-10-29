"""Ask's past conversations: a transcript to go back to, never a source.

A conversation is stored as the screen drew it — the question, then each verified sentence with
the citations it arrived with — so reopening one shows exactly what was seen, chips included.
It is written after a turn finishes, by the screen, and read back only to be drawn again.

**Nothing here is evidence.** The answer graph never reads this table: retrieval searches
`chunks`, facts come from `facts` with their page, and an earlier answer cannot be cited by a
later one. A transcript that said something wrong would be reopened saying it, and would not
teach the next answer to.

**The title is the first question**, shortened, and it is set once. A conversation that wanders
is still found by the thing it was opened to ask.

Rule 1 holds: every query is hand-written and parameterised below.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

# The history column is a list a person scrolls, not an archive search.
RECENT = 50
TITLE_CHARS = 80

SELECT_RECENT = """
SELECT id, title, updated_at
  FROM conversations
 ORDER BY updated_at DESC
 LIMIT %(limit)s
"""

SELECT_ONE = """
SELECT id, title, messages, updated_at
  FROM conversations
 WHERE id = %(id)s
"""

# The title is kept from the first save: it names what the conversation was opened to ask.
# `clock_timestamp()` rather than `now()`, which is fixed for a whole transaction and would tie
# two saves made inside one.
UPSERT = """
INSERT INTO conversations (id, title, messages)
VALUES (%(id)s, %(title)s, %(messages)s::jsonb)
ON CONFLICT (id) DO UPDATE
   SET messages = EXCLUDED.messages,
       updated_at = clock_timestamp()
RETURNING id, title, updated_at
"""


@dataclass(frozen=True, slots=True)
class Summary:
    id: str
    title: str
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class Conversation:
    id: str
    title: str
    messages: list[dict[str, Any]]
    updated_at: datetime


def title(messages: list[dict[str, Any]]) -> str | None:
    """The first question asked, on one line and at most `TITLE_CHARS` long. None if there is no
    question in it — a conversation with nothing asked is not one worth listing."""
    for message in messages:
        if message.get("role") != "user":
            continue
        text = " ".join(
            str(part.get("text", ""))
            for part in message.get("parts") or []
            if isinstance(part, dict) and part.get("type") == "text"
        )
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            if len(text) <= TITLE_CHARS:
                return text
            return text[: TITLE_CHARS - 1].rstrip() + "…"
    return None


def recent(conn: Any, limit: int = RECENT) -> list[Summary]:
    with conn.cursor() as cur:
        cur.execute(SELECT_RECENT, {"limit": limit})
        return [Summary(*row) for row in cur.fetchall()]


def get(conn: Any, conversation_id: str) -> Conversation | None:
    with conn.cursor() as cur:
        cur.execute(SELECT_ONE, {"id": conversation_id})
        row = cur.fetchone()
    return Conversation(*row) if row else None


def save(conn: Any, conversation_id: str, messages: list[dict[str, Any]]) -> Summary | None:
    """Write the whole conversation over whatever was there. None if nothing in it was asked."""
    named = title(messages)
    if named is None:
        return None
    with conn.cursor() as cur:
        cur.execute(
            UPSERT,
            {"id": conversation_id, "title": named, "messages": json.dumps(messages)},
        )
        row = cur.fetchone()
    return Summary(*row)
