"""The one client that talks to Ollama.

Everything the platform infers goes through here: embeddings, classification, extraction and
the quarantine image pass. One place means one timeout policy, one set of options, and one
place to look when a model answers badly.

`trust_env=False` and `follow_redirects=False` match the diagnostic checks in
`core/runtime/checks.py`: a proxy variable in someone's shell must not silently route a
household document through a company proxy, and a redirect must not move inference off the
machine. Both are the claim `docs/governance/` makes, enforced here.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

import httpx

from core.runtime.settings import Settings

log = logging.getLogger(__name__)

EMBED_DIM = 768  # chunks.embedding is vector(768); a model of another size cannot be stored

# EmbeddingGemma was trained with a task prompt on each side, and scores without them are both
# lower and flatter. Measured on the household vault on 13 September: "do i have a
# hospitalisation plan?" scored 0.42 against the best chunk without prompts and abstained under
# the pack's 0.45 floor; with both prompts and clause-aligned chunks it scored 0.55. The two
# sides must always agree, so a vault embedded one way is re-embedded with
# `scripts/reindex.py` before a query is embedded the other way.
QUERY_PROMPT = "task: search result | query: {text}"
DOCUMENT_PROMPT = "title: {title} | text: {text}"


def uses_task_prompts(model: str) -> bool:
    """Whether this embedding model expects `QUERY_PROMPT` and `DOCUMENT_PROMPT`."""
    return "embeddinggemma" in model.lower()


class ModelUnavailable(RuntimeError):
    """Safe to show: names what could not be done, never the document it was doing it to."""


@dataclass(frozen=True, slots=True)
class Generated:
    text: str
    model: str
    latency_ms: int

    def json(self) -> dict[str, Any]:
        """Parse a schema-constrained reply. A model that returns prose here is a failure."""
        try:
            value = json.loads(self.text)
        except json.JSONDecodeError as error:
            raise ModelUnavailable(f"{self.model} did not return JSON") from error
        if not isinstance(value, dict):
            raise ModelUnavailable(f"{self.model} returned {type(value).__name__}, not an object")
        return value


class Ollama:
    def __init__(self, settings: Settings, timeout: float = 180.0) -> None:
        self._settings = settings
        self._timeout = timeout

    def _client(self, base_url: str) -> httpx.Client:
        return httpx.Client(
            base_url=base_url,
            timeout=self._timeout,
            trust_env=False,
            follow_redirects=False,
        )

    # ------------------------------------------------------------------- embeddings

    def embed(self, texts: list[str]) -> list[list[float]]:
        """One request for the whole batch. Returns vectors in the order given."""
        if not texts:
            return []
        model = self._settings.embedding_model
        try:
            with self._client(self._settings.auxiliary_url) as client:
                response = client.post("/api/embed", json={"model": model, "input": texts})
                response.raise_for_status()
                payload = response.json()
        except (httpx.HTTPError, ValueError) as error:
            raise ModelUnavailable(f"embeddings are unavailable from {model}") from error

        vectors = payload.get("embeddings")
        if not isinstance(vectors, list) or len(vectors) != len(texts):
            raise ModelUnavailable(
                f"{model} returned {len(vectors or [])} vectors for {len(texts)}"
            )
        for vector in vectors:
            if not isinstance(vector, list) or len(vector) != EMBED_DIM:
                raise ModelUnavailable(
                    f"{model} returns {len(vector)}-dimensional vectors; "
                    f"chunks.embedding is vector({EMBED_DIM})"
                )
        return vectors

    def embed_query(self, text: str) -> list[float]:
        """A question, embedded the way the model was trained to embed a search query."""
        model = self._settings.embedding_model
        return self.embed([QUERY_PROMPT.format(text=text) if uses_task_prompts(model) else text])[0]

    def embed_documents(self, items: list[tuple[str, str]]) -> list[list[float]]:
        """Passages as `(title, text)`, embedded the way the model was trained to embed a document.

        The title is the document as a person would name it. It is what lets a chunk from the
        middle of a contract still say which contract it is from.
        """
        if not uses_task_prompts(self._settings.embedding_model):
            return self.embed([text for _title, text in items])
        return self.embed(
            [DOCUMENT_PROMPT.format(title=title or "none", text=text) for title, text in items]
        )

    # ------------------------------------------------------------------- warming up

    def warm(self, keep_alive: str = "30m") -> str | None:
        """Load the generator and the embedder now, and say where the generator landed.

        An empty prompt is Ollama's documented way to load a model without generating anything.
        The answer is `gpu`, `partial` (split between graphics memory and the processor), `cpu`,
        or `None` when Ollama does not report a placement. On 13 September every model call ran
        on the processor because the graphics driver had failed — `size_vram` was 0 — and nothing
        on screen said so; a three-minute answer simply looked broken.
        """
        model = self._settings.generation_model
        try:
            with self._client(self._settings.generation_url) as client:
                client.post(
                    "/api/generate", json={"model": model, "prompt": "", "keep_alive": keep_alive}
                ).raise_for_status()
                listing = client.get("/api/ps")
                listing.raise_for_status()
                running = listing.json().get("models") or []
            with self._client(self._settings.auxiliary_url) as client:
                client.post(
                    "/api/embed",
                    json={
                        "model": self._settings.embedding_model,
                        "input": [QUERY_PROMPT.format(text="warm")],
                        "keep_alive": keep_alive,
                    },
                ).raise_for_status()
        except (httpx.HTTPError, ValueError, AttributeError) as error:
            raise ModelUnavailable(f"{model} could not be loaded") from error

        for entry in running:
            if not isinstance(entry, dict) or model not in (entry.get("name"), entry.get("model")):
                continue
            size, in_vram = int(entry.get("size") or 0), int(entry.get("size_vram") or 0)
            if size <= 0:
                return None
            return "gpu" if in_vram >= size else ("partial" if in_vram else "cpu")
        return None

    # ------------------------------------------------------------------- generation

    def constrained(
        self,
        system: str,
        prompt: str,
        schema: dict[str, Any],
        *,
        images: list[str] | None = None,
        temperature: float = 0.0,
    ) -> Generated:
        """Generate against a JSON schema. This is how extraction is held to a pack's fields.

        `images` are base64 page images: the same vision-language model reads pixels when the
        parser could not recover text. That is the quarantine second pass.
        """
        model = self._settings.generation_model
        body = self._constrained_body(system, prompt, schema, temperature, stream=False)
        if images:
            body["messages"][1]["images"] = images
        try:
            with self._client(self._settings.generation_url) as client:
                response = client.post("/api/chat", json=body)
                response.raise_for_status()
                payload = response.json()
        except (httpx.HTTPError, ValueError) as error:
            raise ModelUnavailable(f"{model} did not answer") from error

        content = (payload.get("message") or {}).get("content")
        if not isinstance(content, str) or not content.strip():
            raise ModelUnavailable(f"{model} returned an empty answer")
        elapsed = payload.get("total_duration") or 0
        return Generated(content.strip(), model, int(elapsed / 1_000_000))

    def _constrained_body(
        self, system: str, prompt: str, schema: dict[str, Any], temperature: float, *, stream: bool
    ) -> dict[str, Any]:
        """The one request body both constrained calls send. See `constrained_stream`."""
        return {
            "model": self._settings.generation_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "format": schema,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_ctx": int(self._settings.context_tokens),
            },
        }

    def constrained_stream(
        self,
        system: str,
        prompt: str,
        schema: dict[str, Any],
        *,
        temperature: float = 0.0,
    ) -> Iterator[str]:
        """The same constrained generation, yielded as it is written.

        The same body as `constrained` but for `stream`, built in one place, deliberately: the
        schema, the temperature and the context window must not differ between the streaming and
        batch paths, or the interface and the command line would be asking two different questions
        of the same model.

        Yields raw content deltas. They are fragments of JSON, not sentences — whoever wants
        sentences reads them through `core.graph.sentences.SentenceScanner`, which is the only
        thing that knows when one has finished.
        """
        model = self._settings.generation_model
        body = self._constrained_body(system, prompt, schema, temperature, stream=True)
        try:
            with (
                self._client(self._settings.generation_url) as client,
                client.stream("POST", "/api/chat", json=body) as response,
            ):
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line.strip():
                        continue
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        # Ollama emits one JSON object per line. A line that is not one is not
                        # a reason to lose the sentences that already arrived.
                        log.info("%s sent a line that was not JSON", model)
                        continue
                    piece = (chunk.get("message") or {}).get("content")
                    if isinstance(piece, str) and piece:
                        yield piece
                    if chunk.get("done"):
                        return
        except httpx.HTTPError as error:
            raise ModelUnavailable(f"{model} did not answer") from error
