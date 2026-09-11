"""Minimal Ollama client over stdlib urllib — no third-party HTTP dependency.

Talks only to the loopback address in Config.ollama_host. If Ollama isn't
running, every call raises OllamaUnavailable with a human-readable hint rather
than a stack trace.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request


class OllamaUnavailable(RuntimeError):
    pass


class Ollama:
    def __init__(self, host: str = "http://127.0.0.1:11434", timeout: int = 600):
        self.host = host.rstrip("/")
        self.timeout = timeout

    # --- plumbing ---------------------------------------------------------

    def _post(self, path: str, payload: dict) -> dict:
        req = urllib.request.Request(
            f"{self.host}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise OllamaUnavailable(
                f"Could not reach Ollama at {self.host} ({exc}). "
                "Start it with `ollama serve`, or install it from ollama.com."
            ) from exc

    def _get(self, path: str) -> dict:
        try:
            with urllib.request.urlopen(f"{self.host}{path}", timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise OllamaUnavailable(f"Could not reach Ollama at {self.host} ({exc}).") from exc

    # --- api --------------------------------------------------------------

    def models(self) -> list[str]:
        data = self._get("/api/tags")
        return [m["name"] for m in data.get("models", [])]

    def embed(self, model: str, inputs: list[str]) -> list[list[float]]:
        """Batch embeddings. Falls back to the legacy endpoint on old servers."""
        try:
            data = self._post("/api/embed", {"model": model, "input": inputs})
            if "embeddings" in data:
                return data["embeddings"]
        except OllamaUnavailable:
            raise
        except Exception:
            pass
        # Legacy: one request per input.
        out = []
        for text in inputs:
            data = self._post("/api/embeddings", {"model": model, "prompt": text})
            out.append(data["embedding"])
        return out

    def chat(
        self,
        model: str,
        messages: list[dict],
        temperature: float = 0.1,
        num_ctx: int = 8192,
    ) -> str:
        data = self._post(
            "/api/chat",
            {
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature, "num_ctx": num_ctx},
            },
        )
        return data.get("message", {}).get("content", "")
