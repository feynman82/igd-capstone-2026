"""The five endpoints, against a fake database and the real queries.

The connection is a fake that dispatches on the text of the statement it is handed, so every
test below runs the *actual* SQL constants from `core/` and `modules/` — a query that stops
matching its fake is a query somebody edited without looking at what reads it. The graph and
the model are faked at the seam `api/routes.py` owns; `tests/test_answer_graph.py` already
owns the graph's own behaviour and should not be tested twice.

What these protect, in order of how much it would hurt to lose:

- **Opening Today does not consume a lead window.** `GET /api/today` must never mark.
- **A disabled pack goes quiet.** No reminder, no alert, no document, no passage to cite.
- **Installing does not re-enable.** The upsert leaves the person's choice alone.
- **Every item on Today carries a source**, and the three shapes of `/api/ask` stay distinct.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from api import routes
from api.main import create_app
from core.graph.answer import Answer, Cited
from core.runtime.settings import Settings

ROOT = Path(__file__).resolve().parents[1]

TODAY = date(2026, 9, 11)
DOC = UUID("11111111-1111-1111-1111-111111111111")
SCAN = UUID("22222222-2222-2222-2222-222222222222")


# ----------------------------------------------------------------------------- the fake rows
#
# Keyed by a fragment that appears in exactly one statement. The fragment is chosen to be the
# part of the query that says what it is for, so a rename shows up here as a failing test
# rather than as a silently empty screen.


def rows_for(**overrides: list[tuple[Any, ...]]) -> dict[str, list[tuple[Any, ...]]]:
    """The default database: two packs installed and enabled, and nothing else."""
    table: dict[str, list[tuple[Any, ...]]] = {
        "SELECT id, enabled FROM packs": [("insurance_agent", True), ("iras_tax", True)],
        "o.last_notified_at": [],  # reminder.DUE_SWEEP
        "o.due_date < %(today)s": [],  # reminder.OVERDUE
        "count(*) FROM documents d": [(0,)],  # vault.COUNT_DOCUMENTS
        "d.quarantine_reason": [],  # vault.SELECT_DOCUMENTS
        "f.document_id = ANY": [],  # vault.SELECT_FACTS_FOR_DOCUMENTS
        "WHERE status = 'quarantined'": [],
        "SELECT id, sha256": [],
        "installed_at\n  FROM packs": [],  # registry.SELECT_PACKS
        "FROM modules": [],
        "WHERE pack_id IS NOT NULL": [],
        "count(*) FROM facts": [],
        # The Alert module's metrics. Empty means no threshold is crossed, which is what most
        # of these tests want; the ones that want an alert override the metric they need.
        "max(f.value_date)": [],  # alert.DAYS_UNCOVERED
        "f.value_num, f.value_date, f.subject": [],  # alert.EVIDENCE_FOR_KEY
        "FROM traces": [],  # alert.LAST_FIRED, the debounce
    }
    table.update(overrides)
    return table


class FakeCursor:
    def __init__(self, table: dict[str, list[tuple[Any, ...]]], log: list[str]) -> None:
        self._table = table
        self._log = log
        self._current: list[tuple[Any, ...]] = []

    def execute(self, query: str, params: Any = None) -> None:
        self._log.append(query)
        for needle, rows in self._table.items():
            if needle in query:
                self._current = rows
                return
        self._current = []

    def fetchall(self) -> list[tuple[Any, ...]]:
        return self._current

    def fetchone(self) -> tuple[Any, ...] | None:
        return self._current[0] if self._current else None

    def __enter__(self) -> FakeCursor:
        return self

    def __exit__(self, *exc: object) -> None:
        return None


class FakeConn:
    def __init__(self, table: dict[str, list[tuple[Any, ...]]] | None = None) -> None:
        self.table = table if table is not None else rows_for()
        self.statements: list[str] = []
        self.commits = 0
        self.rollbacks = 0

    def cursor(self) -> FakeCursor:
        return FakeCursor(self.table, self.statements)

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1


@pytest.fixture(scope="module")
def settings() -> Settings:
    return Settings.load(ROOT)


@pytest.fixture
def conn() -> FakeConn:
    return FakeConn()


def client_for(settings: Settings, conn: FakeConn) -> TestClient:
    """A client whose database is `conn`.

    `base_url` is loopback because `TrustedHostMiddleware` rejects anything else, which is the
    app's only network guard and is exercised on its own below. Built without the context
    manager on purpose: entering it runs the lifespan, and the lifespan is tested separately.
    """
    app = create_app(settings)

    def fake_connection() -> Iterator[Any]:
        yield conn

    app.dependency_overrides[routes.connection] = fake_connection
    return TestClient(app, base_url="http://127.0.0.1")


@pytest.fixture
def client(settings: Settings, conn: FakeConn) -> TestClient:
    return client_for(settings, conn)


# ------------------------------------------------------------------------------------ today


def obligation(
    obligation_id: int = 42,
    pack_id: str = "insurance_agent",
    due: date = date(2026, 9, 20),
) -> tuple[Any, ...]:
    return (
        obligation_id,
        pack_id,
        "policy expiry — Marcus Fernandez",
        due,
        [60, 30, 7],
        "pending",
        None,
        DOC,
        1,
        "renewal-notice.pdf",
    )


def uncovered_since(expiry: date) -> dict[str, list[tuple[Any, ...]]]:
    """Enough rows to make `insurance_agent`'s `days_uncovered` threshold fire, with evidence.

    The pack declares `ceiling: 0`, so any gap at all is news — and an alert with nothing to
    cite is dropped by the module, which is why the evidence row is not optional here.
    """
    return {
        "max(f.value_date)": [("Marcus Fernandez", expiry, None)],
        "f.value_num, f.value_date, f.subject": [
            ("policy.pdf", 3, None, expiry, "Marcus Fernandez")
        ],
    }


def test_today_is_ordered_overdue_then_alerts_then_reminders(
    settings: Settings,
) -> None:
    conn = FakeConn(
        rows_for(
            **{
                "o.last_notified_at": [obligation(due=date(2026, 9, 20))],
                "o.due_date < %(today)s": [
                    (7, "iras_tax", "income tax filing", date(2026, 8, 28), "notice.pdf")
                ],
                **uncovered_since(date(2026, 8, 1)),
            }
        )
    )
    body = client_for(settings, conn).get(f"/api/today?as_of={TODAY}").json()

    assert [item["kind"] for item in body["items"]] == ["overdue", "alert", "reminder"]
    assert body["as_of"] == str(TODAY)
    overdue, alert_item, reminder = body["items"]
    assert overdue["days_left"] == -14
    assert alert_item["sources"][0]["page"] == 3, "an alert states a number, so it cites one"
    assert reminder["days_left"] == 9
    assert reminder["urgency"] == 9


def test_opening_today_never_marks_a_reminder_as_notified(settings: Settings) -> None:
    """The nightly sweep owns `last_notified_at`. A screen refresh must not burn a window."""
    conn = FakeConn(rows_for(**{"o.last_notified_at": [obligation()]}))
    response = client_for(settings, conn).get(f"/api/today?as_of={TODAY}")

    assert response.status_code == 200
    assert response.json()["items"], "the reminder should still be shown"
    assert conn.commits == 0, "a GET marked something as said"
    assert not any("UPDATE obligations" in statement for statement in conn.statements)


def test_every_today_item_names_its_source(settings: Settings) -> None:
    conn = FakeConn(rows_for(**{"o.last_notified_at": [obligation()]}))
    body = client_for(settings, conn).get(f"/api/today?as_of={TODAY}").json()

    source = body["items"][0]["sources"][0]
    assert source["document_name"] == "renewal-notice.pdf"
    assert source["page"] == 1
    assert source["text"] == "renewal-notice.pdf, page 1"


def test_a_disabled_pack_stops_its_reminders(settings: Settings) -> None:
    conn = FakeConn(
        rows_for(
            **{
                "SELECT id, enabled FROM packs": [
                    ("insurance_agent", False),
                    ("iras_tax", True),
                ],
                "o.last_notified_at": [obligation(pack_id="insurance_agent")],
                "o.due_date < %(today)s": [
                    (7, "insurance_agent", "policy expiry", date(2026, 8, 28), "old.pdf")
                ],
            }
        )
    )
    body = client_for(settings, conn).get(f"/api/today?as_of={TODAY}").json()

    assert body["items"] == [], "a switched-off pack still reached Today"


def test_an_empty_registry_shows_everything_rather_than_nothing(settings: Settings) -> None:
    """A registry that failed to install must fail loudly, not silently silence the house."""
    conn = FakeConn(
        rows_for(
            **{
                "SELECT id, enabled FROM packs": [],
                "o.last_notified_at": [obligation()],
            }
        )
    )
    body = client_for(settings, conn).get(f"/api/today?as_of={TODAY}").json()

    assert len(body["items"]) == 1


# -------------------------------------------------------------------------------------- ask


class FakeGraph:
    """Stands in for `AnswerGraph` at the seam `api/routes.py` owns."""

    answer = Answer("")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def ask(self, question: str, *, thread_id: str = "local") -> Answer:
        return type(self).answer


@pytest.fixture
def graph(monkeypatch: pytest.MonkeyPatch) -> type[FakeGraph]:
    monkeypatch.setattr(routes, "Ollama", lambda settings: object())
    monkeypatch.setattr(routes, "AnswerGraph", FakeGraph)
    return FakeGraph


def test_ask_returns_claims_with_their_citations(
    client: TestClient, graph: type[FakeGraph]
) -> None:
    graph.answer = Answer(
        "The policy renews on 30 November 2026 [renewal-notice.pdf, page 1].",
        citations=["renewal-notice.pdf, page 1"],
        claims=[
            Cited(
                text="The policy renews on 30 November 2026.",
                chunk_ids=(11,),
                citations=["renewal-notice.pdf, page 1"],
            )
        ],
        passages_read=6,
        disclaimer="This is not financial advice.",
    )
    body = client.post("/api/ask", json={"question": "when does it renew?"}).json()

    assert body["kind"] == "answer"
    assert body["claims"][0]["citations"] == ["renewal-notice.pdf, page 1"]
    assert body["claims"][0]["chunk_ids"] == [11]
    assert body["disclaimer"] == "This is not financial advice."


def test_ask_returns_an_abstention_with_its_reason(
    client: TestClient, graph: type[FakeGraph]
) -> None:
    graph.answer = Answer(
        "I can't answer that from your documents: this is not in your documents.",
        abstained=True,
        reason="nothing in the answer could be traced to a document",
        missing="a utilities bill would answer it",
        passages_read=3,
        dropped=2,
    )
    body = client.post("/api/ask", json={"question": "what is my water bill?"}).json()

    assert body["kind"] == "abstention"
    assert body["reason"] == "nothing in the answer could be traced to a document"
    assert body["missing"] == "a utilities bill would answer it"
    assert body["claims"] == []
    assert body["dropped"] == 2


def test_ask_refuses_a_request_to_act(client: TestClient, graph: type[FakeGraph]) -> None:
    graph.answer = Answer("I can explain what your documents say, but I do not act", refused=True)
    body = client.post("/api/ask", json={"question": "renew the policy for me"}).json()

    assert body["kind"] == "refusal"
    assert body["claims"] == []
    assert body["citations"] == []


def test_ask_requires_a_question(client: TestClient) -> None:
    assert client.post("/api/ask", json={"question": ""}).status_code == 422


# ------------------------------------------------------------------------------------ vault


def document_row(pack_id: str | None = "insurance_agent") -> tuple[Any, ...]:
    return (
        DOC,
        "renewal-notice.pdf",
        "application/pdf",
        2,
        "renewal_notice",
        pack_id,
        "indexed",
        None,
        datetime(2026, 9, 10, 14, 2, 11),
        False,
    )


def fact_row(key: str, text: str | None, num: Any, on: date | None) -> tuple[Any, ...]:
    return (DOC, key, "Marcus Fernandez", text, num, on, 1, 0.93, False, "insurance_agent")


def test_vault_lists_documents_with_their_facts(settings: Settings) -> None:
    conn = FakeConn(
        rows_for(
            **{
                "count(*) FROM documents d": [(1,)],
                "d.quarantine_reason": [document_row()],
                "f.document_id = ANY": [
                    fact_row("expiry_date", None, None, date(2026, 11, 30)),
                    fact_row("annual_premium", None, Decimal("1248.90"), None),
                ],
            }
        )
    )
    body = client_for(settings, conn).get("/api/vault").json()

    assert body["total"] == 1
    document = body["documents"][0]
    assert document["status"] == "indexed"
    assert document["doc_type"] == "renewal_notice"
    assert document["pack_enabled"] is True

    by_key = {fact["key"]: fact for fact in document["facts"]}
    assert by_key["expiry_date"]["value"] == "2026-11-30"
    assert by_key["expiry_date"]["value_type"] == "date"
    assert by_key["annual_premium"]["value"] == 1248.90
    assert by_key["expiry_date"]["page"] == 1, "a fact without a page is not showable"


def test_vault_hides_a_disabled_packs_documents(settings: Settings) -> None:
    conn = FakeConn(
        rows_for(
            **{
                "SELECT id, enabled FROM packs": [("insurance_agent", False)],
                "count(*) FROM documents d": [(0,)],
                "d.quarantine_reason": [],
            }
        )
    )
    client_for(settings, conn).get("/api/vault")

    listing = next(statement for statement in conn.statements if "d.quarantine_reason" in statement)
    assert "%(packs)s::text[]" in listing, "the listing did not filter by enabled pack"


# ------------------------------------------------------------------------------------ packs


def pack_row(pack_id: str, enabled: bool) -> tuple[Any, ...]:
    from core.packs import pack

    return (
        pack_id,
        pack(pack_id).version,
        pack(pack_id).manifest.model_dump(mode="json"),
        enabled,
        datetime(2026, 9, 10, 9, 0, 0),
    )


def test_packs_lists_what_is_installed_and_what_it_has_read(settings: Settings) -> None:
    conn = FakeConn(
        rows_for(
            **{
                "installed_at\n  FROM packs": [pack_row("insurance_agent", True)],
                "WHERE pack_id IS NOT NULL": [("insurance_agent", 7)],
                "count(*) FROM facts": [("insurance_agent", 41)],
            }
        )
    )
    body = client_for(settings, conn).get("/api/packs").json()

    summary = body["packs"][0]
    assert summary["id"] == "insurance_agent"
    assert summary["enabled"] is True
    assert summary["on_disk"] is True
    assert summary["documents"] == 7
    assert summary["facts"] == 41
    assert summary["never_acts"] is True, "v1 advises; the manifest cannot say otherwise"
    assert "renewal_notice" in summary["document_types"]


def test_patching_a_pack_switches_it_off(settings: Settings) -> None:
    conn = FakeConn(rows_for(**{"UPDATE packs": [pack_row("insurance_agent", False)]}))
    response = client_for(settings, conn).patch(
        "/api/packs/insurance_agent", json={"enabled": False}
    )

    assert response.status_code == 200
    assert response.json()["enabled"] is False
    assert conn.commits == 1


def test_patching_an_unknown_pack_is_a_404(client: TestClient) -> None:
    response = client.patch("/api/packs/not_a_pack", json={"enabled": False})

    assert response.status_code == 404
    assert "not_a_pack" in response.json()["detail"]


# ------------------------------------------------------------------------------- quarantine


def test_quarantine_says_what_needs_eyes_and_why(settings: Settings, tmp_path: Path) -> None:
    conn = FakeConn(
        rows_for(
            **{
                "WHERE status = 'quarantined'": [
                    (SCAN, "faint-scan.png", "image/png", "docling produced no text", None)
                ],
                "SELECT id, sha256": [],  # no digest, so no file behind it
            }
        )
    )
    body = client_for(settings, conn).get("/api/quarantine").json()

    assert body["count"] == 1
    document = body["documents"][0]
    assert document["reason"] == "docling produced no text"
    assert document["retryable"] is False
    assert document["blocked"] == "the original file is no longer in the inbox"


def test_retrying_a_document_that_has_no_file_is_refused_rather_than_queued(
    settings: Settings,
) -> None:
    conn = FakeConn(
        rows_for(
            **{
                "WHERE status = 'quarantined'": [
                    (SCAN, "faint-scan.png", "image/png", "docling produced no text", None)
                ],
                "SELECT id, sha256": [],
            }
        )
    )
    response = client_for(settings, conn).post(f"/api/quarantine/{SCAN}/retry")

    assert response.status_code == 409
    assert "no longer in the inbox" in response.json()["detail"]


def test_retrying_something_not_in_quarantine_is_a_404(client: TestClient) -> None:
    response = client.post(f"/api/quarantine/{uuid4()}/retry")

    assert response.status_code == 404


# -------------------------------------------------------------------------------- registry


def test_installing_never_re_enables_a_pack_somebody_switched_off() -> None:
    """Read as a statement: the upsert must not touch `enabled` on conflict."""
    from core import registry

    on_conflict = registry.UPSERT_PACK.split("ON CONFLICT")[1]
    assert "enabled" not in on_conflict
    assert "ON CONFLICT" in registry.UPSERT_MODULE
    assert "enabled" not in registry.UPSERT_MODULE.split("ON CONFLICT")[1]


def test_install_writes_every_pack_and_module_on_disk() -> None:
    from core import registry

    conn = FakeConn()
    done = registry.install(conn)

    assert "insurance_agent" in done.packs
    assert "reminder" in done.modules
    assert "alert" in done.modules
    assert conn.commits == 1
    assert sum("INSERT INTO packs" in s for s in conn.statements) == len(done.packs)


def test_an_empty_registry_reads_as_do_not_filter() -> None:
    from core import registry

    assert (
        registry.enabled_pack_ids(FakeConn(rows_for(**{"SELECT id, enabled FROM packs": []})))
        is None
    )


def test_all_disabled_is_not_the_same_as_empty() -> None:
    from core import registry

    conn = FakeConn(rows_for(**{"SELECT id, enabled FROM packs": [("iras_tax", False)]}))

    assert registry.enabled_pack_ids(conn) == frozenset()


def test_the_server_still_starts_when_the_database_is_not_running(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The setup page exists to say the database is missing. It cannot say it if it did not
    start, so a failed install must not be fatal."""
    from core import registry
    from core.runtime.db import DatabaseUnavailable

    def refuse(*args: Any, **kwargs: Any) -> Any:
        raise DatabaseUnavailable("Cannot reach the local database.")

    monkeypatch.setattr(registry, "connect", refuse)
    assert registry.install_best_effort(settings) is None

    with TestClient(create_app(settings), base_url="http://127.0.0.1") as started:
        assert started.get("/healthz").status_code == 200


def test_the_api_is_loopback_only(client: TestClient) -> None:
    """The only network guard on the app. Zee's interface proxies through Next, so every real
    request arrives same-origin and no other Host is ever legitimate."""
    assert client.get("/api/today", headers={"Host": "parrot.example.com"}).status_code == 400
    assert client.get("/api/today", headers={"Host": "localhost"}).status_code == 200


# ------------------------------------------------------------------------ the sweeps agree


def test_the_retriever_filters_by_enabled_pack() -> None:
    """`hides its facts` reaches an answer through retrieval, not through the API."""
    from core.graph.baseline import DENSE_SEARCH, DenseRetriever

    assert "%(packs)s::text[]" in DENSE_SEARCH
    assert DenseRetriever(FakeConn(), None, ("iras_tax",)).packs == ("iras_tax",)


def test_a_disabled_pack_does_not_reach_the_nightly_sweep() -> None:
    """The Celery beat never goes through the API, so the filter cannot live there."""
    from modules import reminder

    conn = FakeConn(rows_for(**{"o.last_notified_at": [obligation()]}))
    due = reminder.sweep(conn, TODAY, mark=False, enabled=frozenset({"iras_tax"}))

    assert due == []
    assert reminder.sweep(conn, TODAY, mark=False, enabled=None), "None must not filter"


def test_overdue_is_filtered_by_the_same_set() -> None:
    from modules import reminder

    conn = FakeConn(
        rows_for(
            **{
                "o.due_date < %(today)s": [
                    (7, "insurance_agent", "policy expiry", TODAY - timedelta(days=3), "p.pdf")
                ]
            }
        )
    )

    assert reminder.overdue(conn, TODAY, enabled=frozenset({"iras_tax"})) == []
    assert len(reminder.overdue(conn, TODAY, enabled=None)) == 1
