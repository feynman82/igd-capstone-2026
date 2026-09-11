"""The watched folder: debounce, mime sniffing, and what happens the second time.

No database here. `register_document` is the seam, and a fake registrar stands in for it so
these tests say something about the adapter rather than about Postgres. The real upsert is
exercised against the real unique index in `tests/test_registration.py`.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from core.adapters.base import FALLBACK_MIME, sha256, sniff_mime
from core.adapters.folder import FolderAdapter, FolderSettings
from core.ingest.register import Registration

PDF = b"%PDF-1.7\nnot really a pdf, but it starts like one\n" + b"x" * 400
JPEG = b"\xff\xd8\xff\xe0" + b"y" * 400

NOW = datetime(2026, 9, 11, 9, 0, tzinfo=UTC)


class FakeRegistrar:
    """The `documents` table, reduced to the one thing it guarantees: sha256 is unique."""

    def __init__(self) -> None:
        self.by_digest: dict[bytes, UUID] = {}
        self.calls: list[tuple[str, str]] = []

    def __call__(
        self,
        *,
        payload: bytes,
        mime: str,
        original_name: str,
        source_channel: str,
        synthetic: bool = False,
    ) -> Registration:
        key = sha256(payload)
        self.calls.append((original_name, mime))
        inserted = key not in self.by_digest
        document_id = self.by_digest.setdefault(key, uuid4())
        return Registration(
            document_id=document_id,
            sha256=key,
            source_channel=source_channel,
            original_name=original_name,
            mime=mime,
            status="pending",
            ingested_at=NOW,
            inserted=inserted,
        )


@pytest.fixture
def watched(tmp_path: Path) -> tuple[FolderAdapter, FakeRegistrar, Path]:
    registrar = FakeRegistrar()
    adapter = FolderAdapter(registrar, FolderSettings(tmp_path, stable_seconds=3.0))
    return adapter, registrar, tmp_path


def test_a_settled_file_is_registered_within_the_stability_window(
    watched: tuple[FolderAdapter, FakeRegistrar, Path],
) -> None:
    adapter, registrar, folder = watched
    (folder / "payslip.pdf").write_bytes(PDF)

    assert adapter.poll(1.0) == []  # first sighting: nothing is known about it yet
    assert adapter.poll(1.0) == []
    assert adapter.poll(1.0) == []
    jobs = adapter.poll(1.0)

    assert [job.original_name for job in jobs] == ["payslip.pdf"]
    assert jobs[0].mime == "application/pdf"
    assert jobs[0].already_registered is False
    assert len(registrar.by_digest) == 1


def test_a_file_still_being_written_is_not_registered(
    watched: tuple[FolderAdapter, FakeRegistrar, Path],
) -> None:
    adapter, registrar, folder = watched
    path = folder / "scan.pdf"

    for chunk in range(5):  # a scanner appending a page at a time
        path.write_bytes(PDF[: 80 * (chunk + 1)])
        assert adapter.poll(1.0) == []

    assert registrar.calls == []


def test_the_same_bytes_twice_are_registered_once(
    watched: tuple[FolderAdapter, FakeRegistrar, Path],
) -> None:
    adapter, registrar, folder = watched
    (folder / "receipt.pdf").write_bytes(PDF)
    first = _settle(adapter)

    (folder / "receipt-copy.pdf").write_bytes(PDF)  # same document, different name
    second = _settle(adapter)

    assert first[0].already_registered is False
    assert second[0].already_registered is True
    assert second[0].document_id == first[0].document_id
    assert len(registrar.by_digest) == 1


def test_a_registered_file_is_not_registered_again_on_every_poll(
    watched: tuple[FolderAdapter, FakeRegistrar, Path],
) -> None:
    adapter, registrar, folder = watched
    (folder / "notice.pdf").write_bytes(PDF)
    _settle(adapter)

    for _ in range(10):
        assert adapter.poll(1.0) == []
    assert len(registrar.calls) == 1


def test_editing_a_registered_file_registers_the_new_bytes(
    watched: tuple[FolderAdapter, FakeRegistrar, Path],
) -> None:
    adapter, registrar, folder = watched
    path = folder / "policy.pdf"
    path.write_bytes(PDF)
    _settle(adapter)

    path.write_bytes(PDF + b"an endorsement was added")
    jobs = _settle(adapter)

    assert jobs[0].already_registered is False
    assert len(registrar.by_digest) == 2


def test_partial_and_hidden_files_are_ignored(
    watched: tuple[FolderAdapter, FakeRegistrar, Path],
) -> None:
    adapter, registrar, folder = watched
    (folder / "bill.pdf.crdownload").write_bytes(PDF)
    (folder / ".DS_Store").write_bytes(PDF)
    (folder / "~$draft.docx").write_bytes(PDF)
    (folder / "half.tmp").write_bytes(PDF)

    for _ in range(6):
        assert adapter.poll(1.0) == []
    assert registrar.calls == []


def test_an_empty_file_never_settles(watched: tuple[FolderAdapter, FakeRegistrar, Path]) -> None:
    adapter, registrar, folder = watched
    (folder / "empty.pdf").write_bytes(b"")

    for _ in range(6):
        assert adapter.poll(1.0) == []
    assert registrar.calls == []


def test_a_file_too_large_for_a_household_document_is_skipped(tmp_path: Path) -> None:
    registrar = FakeRegistrar()
    adapter = FolderAdapter(registrar, FolderSettings(tmp_path, stable_seconds=1.0, max_bytes=100))
    (tmp_path / "enormous.pdf").write_bytes(PDF)

    for _ in range(6):
        assert adapter.poll(1.0) == []
    assert registrar.calls == []


def test_a_file_removed_before_it_settles_is_forgotten(
    watched: tuple[FolderAdapter, FakeRegistrar, Path],
) -> None:
    adapter, registrar, folder = watched
    path = folder / "moved-away.pdf"
    path.write_bytes(PDF)
    adapter.poll(1.0)
    path.unlink()

    for _ in range(6):
        assert adapter.poll(1.0) == []
    assert registrar.calls == []


def test_the_channel_and_the_timestamp_are_carried_through(
    watched: tuple[FolderAdapter, FakeRegistrar, Path],
) -> None:
    adapter, _, folder = watched
    (folder / "letter.pdf").write_bytes(PDF)
    jobs = _settle(adapter, now=NOW)

    assert jobs[0].source_channel == "folder"
    assert jobs[0].received_at == NOW
    assert jobs[0].digest_hex == sha256(PDF).hex()


@pytest.mark.parametrize(
    ("payload", "name", "expected"),
    [
        (PDF, "anything.txt", "application/pdf"),  # magic bytes beat a wrong suffix
        (JPEG, "IMG_0042", "image/jpeg"),  # a phone photograph with no suffix at all
        (b"just text", "notes.txt", "text/plain"),
        (b"unknowable", "mystery", FALLBACK_MIME),
    ],
)
def test_mime_is_sniffed_from_the_bytes_first(payload: bytes, name: str, expected: str) -> None:
    assert sniff_mime(payload, name) == expected


def _settle(adapter: FolderAdapter, now: datetime | None = None) -> list:
    """Poll until the stability window has passed and something comes out."""
    for _ in range(10):
        jobs = adapter.poll(1.0, now)
        if jobs:
            return jobs
    raise AssertionError("nothing settled within ten polls")
