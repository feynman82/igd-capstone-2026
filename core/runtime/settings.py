"""Small, literal .env reader with environment overrides and loopback-only endpoints."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit


class ConfigurationError(ValueError):
    """Safe to show to the user: messages never include configuration values."""


def local_url(value: str, key: str, schemes: tuple[str, ...]) -> str:
    try:
        parsed = urlsplit(value)
        valid = (
            parsed.scheme in schemes
            and parsed.hostname in {"127.0.0.1", "localhost", "::1"}
            and not parsed.query
            and not parsed.fragment
            and parsed.port != 0
        )
        if parsed.scheme == "http":
            valid = (
                valid and not parsed.username and not parsed.password and parsed.path in {"", "/"}
            )
    except ValueError:
        valid = False
    if not valid:
        raise ConfigurationError(
            f"{key} must be a loopback URL without query options or fragments."
        )
    return value.rstrip("/")


def read_env(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator or not key.strip().isidentifier():
            raise ConfigurationError(f"Invalid .env assignment at line {number}.")
        value = value.strip()
        if value.startswith(("'", '"')):
            if len(value) < 2 or value[-1] != value[0]:
                raise ConfigurationError(f"Unclosed .env quote at line {number}.")
            value = value[1:-1]
        values[key.strip()] = value
    return values


def _positive(value: str) -> int:
    """A context window is a number of tokens. A bad one is a configuration error, not a crash."""
    try:
        tokens = int(value.strip() or "16384")
    except ValueError as error:
        raise ConfigurationError("PARROT_CONTEXT_TOKENS must be a whole number.") from error
    if not 1024 <= tokens <= 262144:
        raise ConfigurationError("PARROT_CONTEXT_TOKENS must be between 1024 and 262144.")
    return tokens


def _folder(value: str, root: Path) -> str:
    """The watched folder, absolute, so a check and a worker never disagree about where it is."""
    folder = Path(value.strip() or "./inbox").expanduser()
    return str(folder if folder.is_absolute() else (root / folder).resolve())


@dataclass(frozen=True, repr=False)
class Settings:
    database_url: str
    redis_url: str
    generation_url: str
    auxiliary_url: str
    generation_model: str
    embedding_model: str
    rerank_model: str
    context_tokens: int
    watch_folder: str

    @classmethod
    def load(cls, root: Path, environment: Mapping[str, str] | None = None) -> Settings:
        values = read_env(root / ".env")
        values.update(os.environ if environment is None else environment)
        gen_url = values.get("OLLAMA_GEN_URL", "http://127.0.0.1:11434")
        gen_model = values.get(
            "PARROT_GEN_MODEL", "hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M"
        )
        embed_model = values.get("PARROT_EMBED_MODEL", "embeddinggemma:300m")
        rerank_model = values.get(
            "PARROT_RERANK_MODEL", "hf.co/gpustack/bge-reranker-v2-m3-GGUF:latest"
        )
        models = [gen_model, embed_model, rerank_model]
        if any(not model.strip() for model in models):
            raise ConfigurationError("Configured model names must not be empty.")
        return cls(
            database_url=local_url(
                values.get("DATABASE_URL", "postgresql://parrot:parrot@127.0.0.1:5432/parrot"),
                "DATABASE_URL",
                ("postgresql",),
            ),
            redis_url=local_url(
                values.get("REDIS_URL", "redis://127.0.0.1:6379/0"), "REDIS_URL", ("redis",)
            ),
            generation_url=local_url(gen_url, "OLLAMA_GEN_URL", ("http",)),
            auxiliary_url=local_url(
                values.get("OLLAMA_AUX_URL", gen_url), "OLLAMA_AUX_URL", ("http",)
            ),
            generation_model=gen_model,
            embedding_model=embed_model,
            rerank_model=rerank_model,
            context_tokens=_positive(values.get("PARROT_CONTEXT_TOKENS", "16384")),
            watch_folder=_folder(values.get("WATCH_FOLDER", ""), root),
        )
