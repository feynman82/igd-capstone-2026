"""The local API. Liveness is intentionally separate from assistant readiness.

Loopback only, in two ways that are not the same. `TrustedHostMiddleware` rejects a request
whose Host header is not this machine, which is what stops a browser on the network reaching
it by IP; binding is `scripts/run_parrot.py`'s business. There is no CORS middleware and that
is deliberate — Zee's Next.js interface proxies through its own route handlers, so every
request arrives same-origin and no other origin is ever granted one.

The registry is installed at startup, best-effort. A database that is not running must not
stop the server coming up: the setup page below exists to tell a person exactly that, and a
server that refused to start could not tell them anything.
"""

from __future__ import annotations

import asyncio
import html
import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from api.routes import build_router
from core.registry import install_best_effort
from core.runtime.checks import Check, collect_checks
from core.runtime.settings import Settings

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings or Settings.load(ROOT)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # Off the event loop: it opens a socket to Postgres and writes a handful of rows.
        await asyncio.to_thread(install_best_effort, config)
        yield

    app = FastAPI(
        title="Parrot local setup",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan,
    )
    app.state.settings = config
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "[::1]"])
    app.include_router(build_router())
    lock = asyncio.Lock()
    cached: list[Check] = []
    checked_at = 0.0

    async def checks() -> list[Check]:
        nonlocal cached, checked_at
        async with lock:
            if not cached or time.monotonic() - checked_at > 5:
                cached = await collect_checks(config)
                checked_at = time.monotonic()
            return cached

    @app.get("/healthz")
    async def health() -> dict[str, str]:
        return {"service": "parrot", "stage": "setup", "status": "alive"}

    @app.get("/readyz")
    async def ready() -> JSONResponse:
        return JSONResponse(
            {
                "service": "parrot",
                "ready": False,
                "stage": "setup",
                "checks": [check.payload() for check in await checks()],
            },
            status_code=503,
            headers={"Cache-Control": "no-store"},
        )

    @app.get("/", response_class=HTMLResponse)
    async def setup() -> HTMLResponse:
        rows = "".join(
            f"<tr><th scope='row'>{html.escape(check.name)}</th>"
            f"<td>{html.escape(check.state)}</td><td>{html.escape(check.detail)}</td></tr>"
            for check in await checks()
        )
        return HTMLResponse(
            "<!doctype html><html lang='en'><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>Parrot local setup</title><body><main>"
            "<h1>Parrot local setup</h1>"
            "<p>This is the engine, and it is running. <strong>This is not the product.</strong>"
            "</p>"
            "<p>The screens are a separate process, started beside this one by "
            "<code>START.cmd</code>: open "
            "<a href='http://localhost:3000'>http://localhost:3000</a>. The "
            "<em>Household interface</em> row below says whether they are answering; if they "
            "are not, the window that started Parrot says why, and you can always run "
            "<code>npm run dev</code> in <code>web</code> yourself.</p>"
            "<p>Drop a document into the <code>inbox</code> folder and it is read "
            "automatically. Everything the screens show is also available from a terminal "
            "in this folder:</p>"
            "<ul>"
            "<li><code>uv run python scripts/today.py</code> — what needs you, by urgency</li>"
            '<li><code>uv run python scripts/ask.py "when does the car insurance renew?"</code>'
            " — ask about your own documents</li>"
            "<li><code>uv run python scripts/quarantine.py</code> — what could not be read, "
            "and why</li>"
            "</ul>"
            "<p>The same answers are served as JSON on this port: "
            "<code>/api/today</code>, <code>/api/ask</code>, <code>/api/vault</code>, "
            "<code>/api/packs</code> and <code>/api/quarantine</code>. "
            "They are loopback only and refuse a request from any other machine.</p>"
            "<table><caption>Local dependency checks</caption>"
            "<thead><tr><th>Component</th><th>Status</th><th>Next step</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>"
            "<p>These checks do not load models, process documents "
            "or send data to cloud services.</p>"
            "<p>Refresh this page after fixing setup. Checks are cached for five seconds.</p>"
            "<p>Everything runs on this computer. Nothing is sent to a cloud service.</p>"
            "<p>To stop, press Ctrl+C in the Parrot window. "
            "See TRY-PARROT.md to get started, or docs/RUNNING.md for detail.</p>"
            "</main></body></html>",
            headers={
                "Cache-Control": "no-store",
                "X-Content-Type-Options": "nosniff",
                "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
            },
        )

    return app
