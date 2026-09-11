"""Diagnostic API. Liveness is intentionally separate from assistant readiness."""

from __future__ import annotations

import asyncio
import html
import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from core.runtime.checks import Check, collect_checks
from core.runtime.settings import Settings

ROOT = Path(__file__).resolve().parents[1]


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings or Settings.load(ROOT)
    app = FastAPI(title="Parrot local setup", docs_url=None, redoc_url=None, openapi_url=None)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "[::1]"])
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
            "<h1>Parrot local setup</h1><p>The setup server is running on this computer.</p>"
            "<p><strong>The household assistant is still being built.</strong> "
            "Document upload and questions are not available yet.</p>"
            "<table><caption>Local dependency checks</caption>"
            "<thead><tr><th>Component</th><th>Status</th><th>Next step</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>"
            "<p>These checks do not load models, process documents "
            "or send data to cloud services.</p>"
            "<p>Refresh this page after fixing setup. Checks are cached for five seconds.</p>"
            "<p>To stop, press Ctrl+C in the Parrot window. "
            "See docs/RUNNING.md for setup steps.</p>"
            "</main></body></html>",
            headers={
                "Cache-Control": "no-store",
                "X-Content-Type-Options": "nosniff",
                "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
            },
        )

    return app
