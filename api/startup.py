"""The page a person sees while Parrot starts, served by the engine itself.

**Why the engine serves it.** On 13 September the engine answered fourteen seconds after a
double-click, and the screens took longer again: `next dev` compiles each route on its first
request. The launcher used to hold the browser back for up to ninety seconds waiting for the
screens, so a person saw nothing, and then a connection error when a route was still compiling.
The engine is up in about a second and needs no compile, so it opens this page at once, and the
page moves to Today by itself the moment the database and the screens both answer.

**What it shows.** The design approved on the startup canvas (`docs/artefacts/Parrot UIUX
refinement/Startup and power/`): one row per thing Parrot waits for, a skeleton while it is
still coming, a tick in the `ok` colour once it has come, and — the state the canvas was drawn
for — a row that turns into a sentence when something is not coming by itself. No spinner: the
shimmer is the only loop the design system allows, and it stops for reduced motion.

**What it polls.** `/api/system`, the same payload the restart screen reads, from the same
five-second check cache. Nothing on this page loads a model, touches a document or leaves the
machine: no web fonts, no third-party script, and a Content-Security-Policy that says so. The
markup lives in `startup.html` beside this file.

The local model is the one row that does not gate the move to Today. Loading a 4B generator on a
processor takes long enough that holding the screens back for it would be the old ninety-second
wait again; Today opens, and answers get quicker once it has loaded.
"""

from __future__ import annotations

import html
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from core.runtime.ollama import ModelUnavailable, Ollama

log = logging.getLogger(__name__)

ModelPhase = Literal["waiting", "loading", "ready", "unavailable"]

_PAGE = Path(__file__).with_name("startup.html").read_text(encoding="utf-8")


@dataclass(slots=True)
class ModelWarmth:
    """Whether the generator has been loaded yet, and where it landed. Written by one thread."""

    state: ModelPhase = "waiting"
    device: Literal["gpu", "partial", "cpu"] | None = None
    detail: str = ""

    def payload(self) -> dict[str, str | None]:
        return {"state": self.state, "device": self.device, "detail": self.detail}


def warm_models(warmth: ModelWarmth, client: Ollama) -> None:
    """Load the generator and the embedder before the first question, and record the outcome.

    A cold 4B generator costs its load time on whichever request reaches it first — usually a
    person's first question, or a document the worker is reading. Loading it at start moves that
    cost to a moment nobody is waiting on, and asking Ollama where it put the model is how this
    page can say "running on the processor" instead of letting a three-minute answer look broken.
    """
    warmth.state = "loading"
    try:
        placement = client.warm()
    except ModelUnavailable as error:
        warmth.state = "unavailable"
        warmth.detail = str(error)
        log.info("startup: %s", error)
        return
    warmth.device = placement  # type: ignore[assignment]
    warmth.state = "ready"
    log.info("startup: the local model is loaded (%s)", placement or "placement unknown")


def content_security_policy(nonce: str) -> str:
    return (
        "default-src 'none'; "
        f"script-src 'nonce-{nonce}'; style-src 'nonce-{nonce}'; "
        "connect-src 'self'; img-src 'self' data:; "
        "base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
    )


def render(nonce: str, screens_url: str) -> str:
    """The whole page. `screens_url` is escaped into a data attribute, never into script."""
    config = html.escape(json.dumps({"screens": screens_url}), quote=True)
    return _PAGE.replace("__NONCE__", html.escape(nonce, quote=True)).replace("__CONFIG__", config)
