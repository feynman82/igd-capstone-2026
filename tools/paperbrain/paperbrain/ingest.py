"""Walk folders, extract text, chunk, embed, store. Idempotent by content hash.

Re-running `pb ingest` is cheap: a file whose sha256 is unchanged is skipped
entirely. Change the file and it is re-extracted and re-embedded in place.
"""

from __future__ import annotations

import hashlib
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from .chunk import chunk_pages
from .config import SUPPORTED_SUFFIXES, Config
from .db import pack
from .extract import extract
from .ollama import Ollama

# Cheap, deterministic first-pass classification. The LLM refines it later.
TYPE_PATTERNS = [
    ("receipt", r"\b(receipt|invoice|tax invoice|subtotal|gst|amount paid|order no)\b"),
    ("insurance", r"\b(policy|insured|premium|coverage|sum assured|underwrit)\w*\b"),
    ("tax", r"\b(iras|notice of assessment|tax return|taxable income|chargeable income)\b"),
    ("school", r"\b(school|parent|term \d|pta|report card|excursion|semester)\b"),
    ("bank", r"\b(statement|account no|closing balance|transaction history)\b"),
    ("utility", r"\b(electricity|water|gas|utilities|meter reading|bill period)\b"),
    ("medical", r"\b(clinic|prescription|diagnosis|medical certificate|dental)\b"),
]

DATE_PATTERNS = [
    r"\b(\d{4})-(\d{2})-(\d{2})\b",
    r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b",
    r"\b(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+(\d{4})\b",
]

MONTHS = {m: i for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), start=1)}


@dataclass
class IngestResult:
    path: str
    status: str            # added / updated / skipped / empty / error
    chunks: int = 0
    note: str = ""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def guess_type(text: str) -> str:
    head = text[:4000].lower()
    best, best_hits = "other", 0
    for label, pattern in TYPE_PATTERNS:
        hits = len(re.findall(pattern, head, flags=re.I))
        if hits > best_hits:
            best, best_hits = label, hits
    return best


def guess_date(text: str) -> str | None:
    head = text[:4000]
    for pattern in DATE_PATTERNS:
        m = re.search(pattern, head, flags=re.I)
        if not m:
            continue
        a, b, c = m.groups()
        try:
            if pattern.startswith(r"\b(\d{4})"):
                return f"{int(a):04d}-{int(b):02d}-{int(c):02d}"
            if b in MONTHS or b.title() in MONTHS:
                return f"{int(c):04d}-{MONTHS[b.title()]:02d}-{int(a):02d}"
            # Ambiguous d/m/y vs m/d/y — prefer day-first (SG/UK convention).
            day, month = int(a), int(b)
            if month > 12:
                day, month = month, day
            return f"{int(c):04d}-{month:02d}-{day:02d}"
        except (ValueError, KeyError):
            continue
    return None


def discover(roots: list[str]) -> list[Path]:
    found: list[Path] = []
    for root in roots:
        base = Path(root).expanduser()
        if base.is_file():
            found.append(base)
            continue
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.name.startswith("."):
                continue
            if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
                found.append(path)
    return found


def embed_chunks(
    conn: sqlite3.Connection, client: Ollama, model: str, batch: int = 16
) -> int:
    """Embed every chunk that doesn't have a vector yet."""
    done = 0
    while True:
        rows = conn.execute(
            "SELECT id, text FROM chunks WHERE embedding IS NULL LIMIT ?", (batch,)
        ).fetchall()
        if not rows:
            break
        vectors = client.embed(model, [r["text"] for r in rows])
        for row, vec in zip(rows, vectors):
            blob = pack(vec)
            conn.execute(
                "UPDATE chunks SET embedding=?, dim=? WHERE id=?",
                (blob, len(blob) // 4, row["id"]),
            )
        conn.commit()
        done += len(rows)
    return done


def ingest_file(conn: sqlite3.Connection, cfg: Config, path: Path) -> IngestResult:
    path = path.expanduser().resolve()
    try:
        stat = path.stat()
        if stat.st_size > cfg.max_file_bytes:
            return IngestResult(str(path), "skipped", note="larger than max_file_bytes")

        digest = sha256(path)
        existing = conn.execute(
            "SELECT id, sha256 FROM documents WHERE path=?", (str(path),)
        ).fetchone()
        if existing and existing["sha256"] == digest:
            return IngestResult(str(path), "skipped", note="unchanged")

        result = extract(path, ocr_enabled=cfg.ocr_enabled, dpi=cfg.ocr_dpi)
        text = result.text
        if not text.strip():
            return IngestResult(str(path), "empty", note=result.note or "no text found")

        if existing:
            conn.execute("DELETE FROM documents WHERE id=?", (existing["id"],))

        cur = conn.execute(
            """
            INSERT INTO documents
                (path, filename, suffix, sha256, bytes, mtime, doc_type, title,
                 doc_date, page_count, text_chars, ocr_used, raw_text)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                str(path),
                path.name,
                path.suffix.lower(),
                digest,
                stat.st_size,
                stat.st_mtime,
                guess_type(text),
                path.stem.replace("_", " ").replace("-", " "),
                guess_date(text),
                len(result.pages),
                len(text),
                int(result.ocr_used),
                text,
            ),
        )
        doc_id = cur.lastrowid

        chunks = chunk_pages(result.pages, cfg.chunk_chars, cfg.chunk_overlap)
        conn.executemany(
            "INSERT INTO chunks (document_id, ordinal, page, text) VALUES (?,?,?,?)",
            [(doc_id, c.ordinal, c.page, c.text) for c in chunks],
        )
        conn.commit()
        return IngestResult(
            str(path),
            "updated" if existing else "added",
            chunks=len(chunks),
            note=result.note,
        )
    except Exception as exc:
        return IngestResult(str(path), "error", note=str(exc))
