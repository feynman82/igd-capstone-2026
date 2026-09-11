"""The idempotent upsert, against the real unique index.

`documents.sha256 UNIQUE` is the only thing standing between a household and four copies of
the same insurance schedule, so it is tested against Postgres rather than against a fake.
Every test runs inside a transaction that is rolled back, so the database is left exactly as
it was found; when no database is running the module skips rather than fails, because
`make check` has to pass on a laptop with nothing started.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from core.adapters.base import sha256
from core.ingest.register import register_document
from core.runtime.settings import Settings

ROOT = Path(__file__).resolve().parents[1]

PAYSLIP = b"%PDF-1.7\npayslip september 2026\n"
POLICY = b"%PDF-1.7\nhome insurance schedule\n"


@pytest.fixture(scope="module")
def database_url() -> str:
    return Settings.load(ROOT).database_url


@pytest.fixture
def conn(database_url: str) -> Iterator[Any]:
    psycopg = pytest.importorskip("psycopg")
    try:
        connection = psycopg.connect(database_url, autocommit=False, connect_timeout=3)
    except psycopg.OperationalError as error:
        pytest.skip(f"no local database: {type(error).__name__}")
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT to_regclass('public.documents')")
            row = cur.fetchone()
        if row is None or row[0] is None:
            pytest.skip("the 0001_init migration has not been applied")
        yield connection
    finally:
        connection.rollback()  # nothing this test did survives
        connection.close()


def test_a_new_document_is_inserted(conn: Any) -> None:
    result = register_document(
        conn,
        payload=PAYSLIP,
        mime="application/pdf",
        original_name="payslip-2026-09.pdf",
        source_channel="folder",
    )

    assert result.inserted is True
    assert result.already_registered is False
    assert result.sha256 == sha256(PAYSLIP)
    assert result.status == "pending"
    assert result.source_channel == "folder"


def test_the_same_bytes_update_in_place_and_do_not_insert_a_second_row(conn: Any) -> None:
    first = register_document(
        conn,
        payload=PAYSLIP,
        mime="application/pdf",
        original_name="payslip-2026-09.pdf",
        source_channel="folder",
    )
    second = register_document(
        conn,
        payload=PAYSLIP,
        mime="application/pdf",
        original_name="payslip (1).pdf",  # the browser's name for the second download
        source_channel="telegram",
    )

    assert second.inserted is False
    assert second.already_registered is True
    assert second.document_id == first.document_id
    assert second.source_channel == "folder", "the channel that first captured it is the truth"

    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM documents WHERE sha256 = %s", (sha256(PAYSLIP),))
        assert cur.fetchone()[0] == 1
        cur.execute("SELECT original_name FROM documents WHERE sha256 = %s", (sha256(PAYSLIP),))
        assert cur.fetchone()[0] == "payslip (1).pdf", "the newest name wins"


def test_different_bytes_are_different_documents(conn: Any) -> None:
    payslip = register_document(
        conn,
        payload=PAYSLIP,
        mime="application/pdf",
        original_name="payslip.pdf",
        source_channel="folder",
    )
    policy = register_document(
        conn,
        payload=POLICY,
        mime="application/pdf",
        original_name="policy.pdf",
        source_channel="folder",
    )

    assert payslip.document_id != policy.document_id


def test_an_empty_payload_is_refused(conn: Any) -> None:
    with pytest.raises(ValueError, match="empty document"):
        register_document(
            conn,
            payload=b"",
            mime="application/pdf",
            original_name="nothing.pdf",
            source_channel="folder",
        )


def test_a_document_must_arrive_with_a_name(conn: Any) -> None:
    with pytest.raises(ValueError, match="original_name"):
        register_document(
            conn,
            payload=PAYSLIP,
            mime="application/pdf",
            original_name="   ",
            source_channel="folder",
        )
