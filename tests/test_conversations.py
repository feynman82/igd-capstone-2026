"""Ask's history column: a conversation is saved whole, listed newest first and reopened as drawn.

The title is pure and runs anywhere. The API runs the real SQL against Postgres, inside a
temporary copy of `conversations`, so a test never sees — or leaves — a row in the live household.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api import routes
from api.main import create_app
from core import conversations
from core.runtime.settings import Settings

ROOT = Path(__file__).resolve().parents[1]


def asked(text: str, id: str = "m1") -> dict[str, Any]:
    return {"id": id, "role": "user", "parts": [{"type": "text", "text": text}]}


def answered(text: str, id: str = "m2") -> dict[str, Any]:
    sentence = {"text": text, "chunk_ids": [7], "citations": [{"text": "b1-0028.pdf, page 1"}]}
    return {"id": id, "role": "assistant", "parts": [{"type": "data-sentence", "data": sentence}]}


def test_the_title_is_the_first_question_on_one_line() -> None:
    messages = [asked("When does the\n  motor policy expire?"), answered("30 November.")]
    assert conversations.title(messages) == "When does the motor policy expire?"


def test_a_long_first_question_is_shortened_and_a_conversation_without_one_has_no_title() -> None:
    long = conversations.title([asked("Analyze my insurance coverage " * 10)])
    assert long is not None and len(long) == conversations.TITLE_CHARS and long.endswith("…")
    assert conversations.title([answered("Nothing was asked.")]) is None


@pytest.fixture
def api() -> Iterator[TestClient]:
    psycopg = pytest.importorskip("psycopg")
    try:
        url = Settings.load(ROOT).database_url
        conn = psycopg.connect(url, autocommit=False, connect_timeout=3)
    except psycopg.OperationalError as error:
        pytest.skip(f"no local database: {type(error).__name__}")
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass('public.conversations')")
            row = cur.fetchone()
            if row is None or row[0] is None:
                pytest.skip("the 0005_conversations migration has not been applied")
            cur.execute("CREATE TEMP TABLE conversations (LIKE public.conversations INCLUDING ALL)")
        app = create_app(Settings.load(ROOT))

        def temporary() -> Iterator[Any]:
            yield conn

        app.dependency_overrides[routes.connection] = temporary
        yield TestClient(app, base_url="http://127.0.0.1")
    finally:
        conn.rollback()
        conn.close()


def test_a_conversation_is_saved_whole_listed_and_reopened_as_drawn(api: TestClient) -> None:
    first = [asked("When does the motor policy expire?")]
    assert api.put("/api/conversations/thread-a", json={"messages": first}).status_code == 200
    api.put("/api/conversations/thread-b", json={"messages": [asked("What did I donate?")]})

    # The second save of a thread replaces its messages, keeps its title and moves it to the top.
    whole = [*first, answered("Your motor policy expires on 30 November 2026.")]
    saved = api.put("/api/conversations/thread-a", json={"messages": whole})
    assert saved.json()["title"] == "When does the motor policy expire?"

    listed = api.get("/api/conversations").json()["conversations"]
    assert [row["id"] for row in listed] == ["thread-a", "thread-b"]

    reopened = api.get("/api/conversations/thread-a").json()
    assert reopened["messages"] == whole


def test_the_api_refuses_what_is_not_a_conversation(api: TestClient) -> None:
    nothing_asked = {"messages": [answered("Unprompted.")]}
    assert api.put("/api/conversations/thread-c", json=nothing_asked).status_code == 422
    assert api.put("/api/conversations/thread-c", json={"messages": []}).status_code == 422
    bad_id = api.put("/api/conversations/not%20an%20id", json={"messages": [asked("Hi?")]})
    assert bad_id.status_code == 422
    assert api.get("/api/conversations/never-saved").status_code == 404
