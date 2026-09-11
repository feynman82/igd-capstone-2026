"""SQLite storage: documents, chunks, FTS5 keyword index, and dense vectors.

Design notes
------------
* One file, no server, no network. `~/.paperbrain/paperbrain.db`.
* Keyword search uses SQLite's built-in FTS5 (BM25 ranking) — no extra deps.
* Vector search stores float32 embeddings as BLOBs and scores them with numpy.
  For a personal paperwork corpus (tens of thousands of chunks at most) an
  exhaustive cosine scan takes single-digit milliseconds, which is far simpler
  and more portable than bolting on a native ANN extension.
* `facts` and `reminders` are the hooks for the tracking/scheduling phase.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS documents (
    id            INTEGER PRIMARY KEY,
    path          TEXT UNIQUE NOT NULL,
    filename      TEXT NOT NULL,
    suffix        TEXT,
    sha256        TEXT NOT NULL,
    bytes         INTEGER,
    mtime         REAL,
    doc_type      TEXT,              -- receipt / insurance / tax / school / other
    title         TEXT,
    doc_date      TEXT,              -- ISO date the document is *about*
    page_count    INTEGER,
    text_chars    INTEGER,
    ocr_used      INTEGER DEFAULT 0,
    ingested_at   TEXT DEFAULT (datetime('now')),
    raw_text      TEXT
);

CREATE TABLE IF NOT EXISTS chunks (
    id            INTEGER PRIMARY KEY,
    document_id   INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    ordinal       INTEGER NOT NULL,
    page          INTEGER,
    text          TEXT NOT NULL,
    embedding     BLOB,
    dim           INTEGER
);
CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(document_id);

CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
    text,
    content='chunks',
    content_rowid='id',
    tokenize='porter unicode61'
);

CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
    INSERT INTO chunks_fts(rowid, text) VALUES (new.id, new.text);
END;
CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
    INSERT INTO chunks_fts(chunks_fts, rowid, text) VALUES('delete', old.id, old.text);
END;
CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
    INSERT INTO chunks_fts(chunks_fts, rowid, text) VALUES('delete', old.id, old.text);
    INSERT INTO chunks_fts(rowid, text) VALUES (new.id, new.text);
END;

-- Structured facts pulled out of documents (phase 2: tracking).
CREATE TABLE IF NOT EXISTS facts (
    id            INTEGER PRIMARY KEY,
    document_id   INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    kind          TEXT NOT NULL,     -- amount / due_date / policy_no / vendor / event
    value         TEXT NOT NULL,
    value_num     REAL,
    value_date    TEXT,
    confidence    REAL,
    source_chunk  INTEGER REFERENCES chunks(id) ON DELETE SET NULL,
    created_at    TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_facts_kind ON facts(kind);
CREATE INDEX IF NOT EXISTS idx_facts_date ON facts(value_date);

-- Things PaperBrain should nudge you about (phase 3: reminders/scheduling).
CREATE TABLE IF NOT EXISTS reminders (
    id            INTEGER PRIMARY KEY,
    document_id   INTEGER REFERENCES documents(id) ON DELETE CASCADE,
    title         TEXT NOT NULL,
    due_date      TEXT NOT NULL,
    lead_days     INTEGER DEFAULT 14,
    status        TEXT DEFAULT 'open',   -- open / done / dismissed
    notes         TEXT,
    created_at    TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_reminders_due ON reminders(due_date, status);
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


# --- embedding (de)serialisation -----------------------------------------


def pack(vec) -> bytes:
    arr = np.asarray(vec, dtype=np.float32)
    norm = np.linalg.norm(arr)
    if norm > 0:
        arr = arr / norm  # store normalised: cosine becomes a dot product
    return arr.tobytes()


def unpack(blob: bytes) -> np.ndarray:
    return np.frombuffer(blob, dtype=np.float32)


def load_matrix(conn: sqlite3.Connection) -> tuple[np.ndarray, list[int]]:
    """Return (N x D matrix of normalised embeddings, chunk ids)."""
    rows = conn.execute(
        "SELECT id, embedding, dim FROM chunks WHERE embedding IS NOT NULL ORDER BY id"
    ).fetchall()
    if not rows:
        return np.zeros((0, 0), dtype=np.float32), []
    dim = rows[0]["dim"]
    ids, vecs = [], []
    for r in rows:
        if r["dim"] != dim:  # embedding model changed mid-flight
            continue
        ids.append(r["id"])
        vecs.append(unpack(r["embedding"]))
    return np.vstack(vecs), ids


def stats(conn: sqlite3.Connection) -> dict:
    def one(sql: str):
        return conn.execute(sql).fetchone()[0]

    return {
        "documents": one("SELECT COUNT(*) FROM documents"),
        "chunks": one("SELECT COUNT(*) FROM chunks"),
        "embedded": one("SELECT COUNT(*) FROM chunks WHERE embedding IS NOT NULL"),
        "facts": one("SELECT COUNT(*) FROM facts"),
        "reminders_open": one("SELECT COUNT(*) FROM reminders WHERE status='open'"),
    }
