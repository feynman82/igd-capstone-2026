"""Configuration for PaperBrain.

Everything is local. Nothing in this file should ever point at a remote service
other than the Ollama server running on this machine.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

# Where PaperBrain keeps its own state (database, cached OCR text, logs).
HOME = Path(os.environ.get("PAPERBRAIN_HOME", Path.home() / ".paperbrain"))

CONFIG_PATH = HOME / "config.json"


@dataclass
class Config:
    # --- storage -----------------------------------------------------------
    db_path: str = str(HOME / "paperbrain.db")
    # Folders that get scanned by `pb ingest --all`.
    library: list[str] = field(default_factory=list)

    # --- ollama ------------------------------------------------------------
    ollama_host: str = "http://127.0.0.1:11434"
    embed_model: str = "nomic-embed-text"
    # 64GB unified memory handles a 14B comfortably alongside the embedder.
    chat_model: str = "qwen2.5:14b-instruct"
    # Vision model used to read scanned receipts/photos when OCR is poor.
    vision_model: str = "llama3.2-vision:11b"

    # --- chunking ----------------------------------------------------------
    chunk_chars: int = 1100
    chunk_overlap: int = 200

    # --- retrieval ---------------------------------------------------------
    top_k: int = 8  # chunks handed to the model
    candidates: int = 40  # per-retriever candidate pool before fusion
    rrf_k: int = 60  # reciprocal-rank-fusion constant

    # --- ingestion ---------------------------------------------------------
    ocr_enabled: bool = True
    ocr_dpi: int = 220
    # Files bigger than this are skipped (bytes). Paperwork is small.
    max_file_bytes: int = 80 * 1024 * 1024

    def save(self) -> None:
        HOME.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(asdict(self), indent=2))

    @classmethod
    def load(cls) -> Config:
        cfg = cls()
        if CONFIG_PATH.exists():
            data = json.loads(CONFIG_PATH.read_text())
            for key, value in data.items():
                if hasattr(cfg, key):
                    setattr(cfg, key, value)
        HOME.mkdir(parents=True, exist_ok=True)
        return cfg


SUPPORTED_SUFFIXES = {
    ".pdf",
    ".txt",
    ".md",
    ".markdown",
    ".csv",
    ".docx",
    ".rtf",
    ".eml",
    ".png",
    ".jpg",
    ".jpeg",
    ".heic",
    ".tif",
    ".tiff",
    ".webp",
}

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".heic", ".tif", ".tiff", ".webp"}
