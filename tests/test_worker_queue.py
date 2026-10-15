"""The queue, tested with no broker anywhere.

What is worth asserting here is not that Celery works. It is the three claims this change makes
to a person: that the watcher hands a document over instead of reading it, that it comes
straight back, and that the worker finds the same bytes the watcher saw. Each of those is a
plain function, so each is tested by calling it.

A fake connection stands in for psycopg, as in `tests/test_folder_capture.py`. The one thing
that would need a broker — Celery's own delivery — is the one thing not tested here, and
`core/runtime/checks.py` is what reports it at runtime instead.
"""

from __future__ import annotations

import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from core.adapters.base import sha256
from core.ingest.dispatch import Inline, Queued
from core.ingest.intake import Intake
from core.ingest.register import Registration
from core.ingest.source import SourceMissing, bytes_for, index_folder
from core.worker import schedule, tasks

PDF = b"%PDF-1.7\nnot really a pdf, but it starts like one\n" + b"x" * 400
NOW = datetime(2026, 9, 11, 9, 0, tzinfo=UTC)


class FakeCursor:
    def __init__(self, rows: list[Any]) -> None:
        self._rows = rows

    def execute(self, query: str, params: Any = None, /) -> None:
        self.query = query
        self.params = params

    def fetchone(self) -> Any:
        return self._rows.pop(0) if self._rows else None

    def __enter__(self) -> FakeCursor:
        return self

    def __exit__(self, *exc: object) -> None:
        return None


class FakeConnection:
    """Enough of psycopg to register a document and to count the commits."""

    def __init__(self, rows: list[Any] | None = None) -> None:
        self.rows = rows or []
        self.commits = 0
        self.rollbacks = 0

    def cursor(self) -> FakeCursor:
        return FakeCursor(self.rows)

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1


def registration(status: str = "pending", payload: bytes = PDF) -> Registration:
    return Registration(
        document_id=uuid4(),
        sha256=sha256(payload),
        source_channel="folder",
        original_name="policy-schedule.pdf",
        mime="application/pdf",
        status=status,
        ingested_at=NOW,
        inserted=True,
    )


class RecordingSend:
    def __init__(self) -> None:
        self.messages: list[dict[str, str]] = []

    def __call__(self, **message: str) -> str:
        self.messages.append(message)
        return "task-1"


# -------------------------------------------------------------------- what crosses the broker


def test_the_queue_carries_a_digest_and_never_the_document() -> None:
    send = RecordingSend()
    line = Queued(send)(
        registration(), payload=PDF, mime="application/pdf", original_name="policy-schedule.pdf"
    )

    assert len(send.messages) == 1
    message = send.messages[0]
    assert message["digest"] == sha256(PDF).hex()
    assert message["mime"] == "application/pdf"
    assert message["original_name"] == "policy-schedule.pdf"
    assert "queued" in line
    # The payload is 400-odd bytes here and 64 MB at the folder adapter's limit. Neither travels.
    assert not any(isinstance(value, bytes) for value in message.values())


def test_queueing_does_not_read_the_document(monkeypatch: pytest.MonkeyPatch) -> None:
    """The whole point. If `process` is reachable from the capture thread, nothing was gained."""

    def explode(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("the pipeline ran on the capture thread")

    monkeypatch.setattr("core.ingest.dispatch.process", explode)
    Queued(RecordingSend())(
        registration(), payload=PDF, mime="application/pdf", original_name="policy-schedule.pdf"
    )


# ---------------------------------------------------------------------------- the capture side


def test_intake_registers_commits_and_hands_over(monkeypatch: pytest.MonkeyPatch) -> None:
    conn = FakeConnection()
    reg = registration()
    monkeypatch.setattr("core.ingest.intake.register_document", lambda *a, **k: reg)
    send = RecordingSend()

    Intake(conn, Queued(send))(
        payload=PDF,
        mime="application/pdf",
        original_name="policy-schedule.pdf",
        source_channel="folder",
    )

    assert conn.commits == 1  # the document row is safe before anything is queued
    assert len(send.messages) == 1


def test_an_already_indexed_document_is_not_queued_again(monkeypatch: pytest.MonkeyPatch) -> None:
    """The cheapest queue message is the one never sent, and the SHA-256 says these bytes are
    the bytes we already read."""
    conn = FakeConnection()
    monkeypatch.setattr(
        "core.ingest.intake.register_document", lambda *a, **k: registration(status="indexed")
    )
    send = RecordingSend()

    Intake(conn, Queued(send))(
        payload=PDF,
        mime="application/pdf",
        original_name="policy-schedule.pdf",
        source_channel="folder",
    )

    assert send.messages == []
    assert conn.commits == 1


def test_register_only_still_registers_and_dispatches_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    conn = FakeConnection()
    monkeypatch.setattr("core.ingest.intake.register_document", lambda *a, **k: registration())
    Intake(conn, None)(
        payload=PDF,
        mime="application/pdf",
        original_name="policy-schedule.pdf",
        source_channel="folder",
    )
    assert conn.commits == 1


def test_handing_over_is_fast_enough_that_the_watcher_never_stalls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Eight seconds per document is what this change exists to remove. Five documents through
    the capture side must cost milliseconds, because the reading happens somewhere else."""
    conn = FakeConnection()
    monkeypatch.setattr("core.ingest.intake.register_document", lambda *a, **k: registration())
    intake = Intake(conn, Queued(RecordingSend()))

    started = time.perf_counter()
    for _ in range(5):
        intake(
            payload=PDF,
            mime="application/pdf",
            original_name="policy-schedule.pdf",
            source_channel="folder",
        )
    assert time.perf_counter() - started < 1.0  # five documents, not forty seconds


def test_inline_keeps_a_failed_parse_from_killing_the_watcher(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def explode(*args: Any, **kwargs: Any) -> None:
        raise RuntimeError("docling fell over")

    monkeypatch.setattr("core.ingest.dispatch.process", explode)
    conn = FakeConnection()
    inline = Inline(conn, client=None)  # type: ignore[arg-type]
    outcome = inline.run(registration(), PDF, "application/pdf", "scan.pdf")

    assert outcome.status == "pending"
    assert conn.rollbacks == 1


# --------------------------------------------------------------------------- finding it again


def test_the_worker_finds_the_document_by_digest_under_any_name(tmp_path: Path) -> None:
    (tmp_path / "renamed-by-the-household.pdf").write_bytes(PDF)
    assert bytes_for(sha256(PDF), tmp_path) == PDF


def test_a_document_whose_file_has_gone_is_reported_not_guessed(tmp_path: Path) -> None:
    (tmp_path / "something-else.pdf").write_bytes(b"%PDF-1.7\ndifferent bytes entirely\n")
    with pytest.raises(SourceMissing):
        bytes_for(sha256(PDF), tmp_path)


def test_the_same_bytes_under_two_names_resolve_to_one_file(tmp_path: Path) -> None:
    (tmp_path / "b-copy.pdf").write_bytes(PDF)
    (tmp_path / "a-original.pdf").write_bytes(PDF)
    assert index_folder(tmp_path)[sha256(PDF)].name == "a-original.pdf"


def test_ingest_says_so_rather_than_failing_when_the_file_is_gone(tmp_path: Path) -> None:
    line = tasks.ingest(
        FakeConnection(),
        client=None,  # type: ignore[arg-type]
        document_id=str(uuid4()),
        digest=sha256(PDF).hex(),
        mime="application/pdf",
        original_name="policy-schedule.pdf",
        folder=tmp_path,
    )
    assert "no longer in the inbox" in line


# ------------------------------------------------------------------------------- the schedule


def test_the_reminder_cron_is_read_from_its_manifest_not_written_twice() -> None:
    """Rule 6's habit: a schedule is written down in one place, and that place is the module's
    own manifest."""
    assert schedule.cron_expressions()["reminder"] == schedule.manifest("reminder").runs.cron


def test_both_sweeps_and_the_digest_are_scheduled_and_named_after_registered_tasks() -> None:
    entries = schedule.beat_schedule()
    assert {str(entry["task"]) for entry in entries.values()} == {
        tasks.SWEEP_REMINDERS,
        tasks.SWEEP_ALERTS,
        tasks.CALENDAR_DIGEST,
    }


def test_alert_is_swept_nightly_even_though_its_manifest_says_fact_write() -> None:
    """The divergence ADR 0008 records. When `fact_write` lands, this test changes with it."""
    assert schedule.manifest("alert").runs.on == "fact_write"
    assert schedule.cron_expressions()["alert"] == schedule.ALERT_FALLBACK_CRON
