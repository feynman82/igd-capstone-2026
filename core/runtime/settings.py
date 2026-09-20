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


def _port(value: str, name: str, fallback: str) -> int:
    """A port a local process listens on.

    These are configuration rather than arguments because more than one process has to agree
    on each of them. `PARROT_PORT` is the engine's, and the Next.js interface in `web/` is
    told the same number through `PARROT_API_URL`. `PARROT_WEB_PORT` is the interface's, and
    the supervisor in `scripts/run_parrot.py` needs it to know whether the screens are already
    up and where to point the browser. A port that lives only in a command line is a port one
    of them gets wrong.

    Neither default is always free — Docker Desktop binds 8000 on some machines, and 3000 is
    the most contested port on a developer's laptop — so both exist to be changed.
    """
    try:
        port = int(value.strip() or fallback)
    except ValueError as error:
        raise ConfigurationError(f"{name} must be a whole number.") from error
    if not 1 <= port <= 65535:
        raise ConfigurationError(f"{name} must be between 1 and 65535.")
    return port


def _folder(value: str, root: Path) -> str:
    """The watched folder, absolute, so a check and a worker never disagree about where it is."""
    folder = Path(value.strip() or "./inbox").expanduser()
    return str(folder if folder.is_absolute() else (root / folder).resolve())


def _chat_ids(value: str) -> frozenset[int]:
    """Which Telegram chats the bot accepts documents from. Empty means any chat.

    It is configuration rather than a command-line flag for the same reason the ports are: the
    launcher starts the capture now, and an allow list that lives only in a command line is one
    that a double-click cannot honour. ADR 0011 describes the allow list; this is where a
    household writes it down.
    """
    ids: set[int] = set()
    for part in value.replace(";", ",").split(","):
        text = part.strip()
        if not text:
            continue
        try:
            ids.add(int(text))
        except ValueError as error:
            raise ConfigurationError(
                "TELEGRAM_CHAT_IDS must be whole numbers separated by commas."
            ) from error
    return frozenset(ids)


def _flag(value: str, name: str, fallback: bool) -> bool:
    """A yes/no setting. A value that is neither is a configuration error, not a silent false."""
    text = value.strip().lower()
    if not text:
        return fallback
    if text in {"1", "true", "yes", "on"}:
        return True
    if text in {"0", "false", "no", "off"}:
        return False
    raise ConfigurationError(f"{name} must be true or false.")


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
    api_port: int
    web_port: int
    # A household secret. `repr=False` on this dataclass is what keeps it out of a traceback or
    # a log line that prints the settings, and it is the reason this field can live here at all.
    telegram_token: str
    telegram_chat_ids: frozenset[int]
    telegram_delete_at_source: bool

    @property
    def telegram_configured(self) -> bool:
        """Whether Telegram capture should start. An unset token means "not this household"."""
        return bool(self.telegram_token.strip())

    @classmethod
    def load(cls, root: Path, environment: Mapping[str, str] | None = None) -> Settings:
        values = read_env(root / ".env")
        values.update(os.environ if environment is None else environment)
        gen_url = values.get("OLLAMA_GEN_URL", "http://127.0.0.1:11434")
        gen_model = values.get(
            "PARROT_GEN_MODEL", "hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M"
        )
        embed_model = values.get("PARROT_EMBED_MODEL", "embeddinggemma:300m")
        # A Hugging Face model id, not an Ollama tag: the reranker runs in-process (ADR 0018).
        rerank_model = values.get("PARROT_RERANK_MODEL", "BAAI/bge-reranker-v2-m3")
        models = [gen_model, embed_model, rerank_model]
        if any(not model.strip() for model in models):
            raise ConfigurationError("Configured model names must not be empty.")
        if rerank_model.strip().startswith("hf.co/"):
            raise ConfigurationError(
                "PARROT_RERANK_MODEL is an Ollama tag, but Ollama cannot serve a cross-encoder. "
                "Name a Hugging Face model id such as BAAI/bge-reranker-v2-m3 (docs/adr/0018)."
            )
        return cls(
            database_url=local_url(
                values.get("DATABASE_URL")
                or "postgresql://parrot:parrot@127.0.0.1:"
                f"{_port(values.get('PARROT_DB_PORT', '5432'), 'PARROT_DB_PORT', '5432')}/parrot",
                "DATABASE_URL",
                ("postgresql",),
            ),
            redis_url=local_url(
                values.get("REDIS_URL")
                or "redis://127.0.0.1:"
                f"{_port(values.get('PARROT_REDIS_PORT', '6379'), 'PARROT_REDIS_PORT', '6379')}/0",
                "REDIS_URL",
                ("redis",),
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
            api_port=_port(values.get("PARROT_PORT", "8000"), "PARROT_PORT", "8000"),
            web_port=_port(values.get("PARROT_WEB_PORT", "3000"), "PARROT_WEB_PORT", "3000"),
            telegram_token=values.get("TELEGRAM_BOT_TOKEN", "").strip(),
            telegram_chat_ids=_chat_ids(values.get("TELEGRAM_CHAT_IDS", "")),
            telegram_delete_at_source=_flag(
                values.get("TELEGRAM_DELETE_AT_SOURCE", ""), "TELEGRAM_DELETE_AT_SOURCE", True
            ),
        )
