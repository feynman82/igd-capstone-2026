"""The five endpoints the interface needs, on the existing loopback app.

**Nothing here reimplements anything.** `/api/today` calls the same `modules.reminder.sweep`
and `modules.alert.sweep` that `scripts/today.py` calls, `/api/ask` builds the same
`AnswerGraph` that `scripts/ask.py` builds, `/api/quarantine` reads the same
`core.ingest.quarantine.queue`. Every handler in this file is a translation from a dataclass
to a Pydantic model and back; when one of them starts to contain a rule, that rule has escaped
from `core/` or `modules/` and belongs back there. The command line and the screen must never
be able to disagree about what is due today.

The dependency runs one way only (rule 7): this file imports `core/` and `modules/`, and
nothing in either of them imports this one.

**Two deliberate properties:**

*`GET /api/today` never marks anything as notified.* `reminder.sweep` is always called with
`mark=False`. Opening a screen is not being reminded — the nightly Celery sweep owns
`last_notified_at`, and a GET that consumes a lead window would mean a person who refreshed
twice had used up their 30-day warning.

*The retry is queued, not run.* The vision pass takes tens of seconds on a 4B model. The
handler returns 202 and a task id; the worker does the reading.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import date
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from api.models import (
    AskRequest,
    AskResponse,
    Claim,
    EnabledRequest,
    ModuleSummary,
    PacksResponse,
    PackSummary,
    QuarantinedDocument,
    QuarantineResponse,
    RetryAccepted,
    Source,
    TodayItem,
    TodayResponse,
    VaultDocument,
    VaultFact,
    VaultResponse,
)
from core import registry, vault
from core.graph.answer import Answer, AnswerGraph
from core.graph.baseline import DenseRetriever, NoReranker
from core.ingest import quarantine
from core.runtime.db import DatabaseUnavailable, connect
from core.runtime.ollama import Ollama
from core.runtime.settings import Settings
from modules import alert, reminder

log = logging.getLogger(__name__)

# Which group a Today item sits in. Overdue first because a date that has passed is not a
# warning any more; alerts next because a threshold crossing has no date of its own; then
# reminders by how many days are left. Within a group the module's own urgency orders it.
BUCKET = {"overdue": 0, "alert": 1, "reminder": 2}


def _settings(request: Request) -> Settings:
    settings = getattr(request.app.state, "settings", None)
    if settings is None:  # pragma: no cover - create_app always sets it
        raise HTTPException(status_code=500, detail="the server has no settings")
    return settings  # type: ignore[no-any-return]


def connection(request: Request) -> Iterator[Any]:
    """One connection per request, closed when it ends.

    Handlers are declared `def` rather than `async def`, so FastAPI runs them in a worker
    thread — and psycopg connections are not thread-safe, which is why this is per request
    rather than one held open on the app.
    """
    try:
        with connect(_settings(request)) as conn:
            yield conn
    except DatabaseUnavailable as error:
        # The message never carries the connection string; `core/runtime/db.py` guarantees it.
        raise HTTPException(status_code=503, detail=str(error)) from error


def _cite(text: str) -> Source:
    """Split a formatted citation back into its parts, keeping the text either way.

    The modules format a citation as "policy.pdf, page 3" because that is what a person says.
    A screen wants the page separately so it can link to it, so this recovers what it can and
    never loses the original line.
    """
    name, separator, page = text.rpartition(", page ")
    if separator and page.strip().isdigit():
        return Source(document_name=name, page=int(page.strip()), text=text)
    return Source(document_name=text or None, text=text)


# ------------------------------------------------------------------------------------ today


def _today_items(conn: Any, on: date) -> list[TodayItem]:
    enabled = registry.enabled_pack_ids(conn)
    items: list[TodayItem] = []

    for firing in alert.sweep(conn, on, mark=False, packs=registry.enabled_packs(conn)):
        items.append(
            TodayItem(
                id=firing.key,
                kind="alert",
                urgency=0,
                pack_id=firing.pack_id,
                label=firing.metric.replace("_", " "),
                line=firing.line(),
                sources=[_cite(citation) for citation in firing.citations],
            )
        )

    for due in reminder.sweep(conn, on, mark=False, enabled=enabled):
        items.append(
            TodayItem(
                id=f"obligation:{due.obligation_id}",
                kind="reminder",
                urgency=due.urgency,
                pack_id=due.pack_id,
                label=due.label,
                line=due.line(),
                due_date=due.due_date,
                days_left=due.days_left,
                lead=due.lead,
                sources=[
                    Source(
                        document_id=str(due.document_id) if due.document_id else None,
                        document_name=due.document_name,
                        page=due.page,
                        text=f"{due.document_name}, page {due.page}"
                        if due.document_name
                        else "no document behind this one",
                    )
                ],
            )
        )

    for obligation_id, pack_id, label, due_date, document_name in reminder.overdue(
        conn, on, enabled=enabled
    ):
        days_left = (due_date - on).days
        items.append(
            TodayItem(
                id=f"obligation:{obligation_id}",
                kind="overdue",
                urgency=days_left,
                pack_id=pack_id,
                label=label,
                line=f"{label}: overdue since {due_date}"
                + (f" — {document_name}" if document_name else ""),
                due_date=due_date,
                days_left=days_left,
                sources=[Source(document_name=document_name, text=document_name or "no document")],
            )
        )

    items.sort(key=lambda item: (BUCKET[item.kind], item.urgency))
    return items


# --------------------------------------------------------------------------------- the router
#
# Dependencies are `Annotated` aliases rather than call-in-default arguments. It is the current
# FastAPI idiom, it is what makes the handlers below readable, and it keeps ruff's B008 quiet
# without a per-project ignore that would apply to four other people's code.

Conn = Annotated[Any, Depends(connection)]
Config = Annotated[Settings, Depends(_settings)]


def build_router() -> APIRouter:
    """The API surface. Settings are read from app state per request, not captured here, so a
    test can build one app per configuration without rebuilding the router."""
    router = APIRouter(prefix="/api")

    @router.get("/today", response_model=TodayResponse)
    def today(
        conn: Conn,
        as_of: Annotated[
            date | None, Query(description="YYYY-MM-DD, for the demonstration")
        ] = None,
    ) -> TodayResponse:
        on = as_of or date.today()
        return TodayResponse(as_of=on, items=_today_items(conn, on))

    @router.post("/ask", response_model=AskResponse)
    def ask(ask_request: AskRequest, conn: Conn, config: Config) -> AskResponse:
        client = Ollama(config)
        enabled = registry.enabled_pack_ids(conn)
        graph = AnswerGraph(
            client,
            DenseRetriever(conn, client, None if enabled is None else tuple(sorted(enabled))),
            NoReranker(),
        )
        return _as_response(graph.ask(ask_request.question, thread_id=ask_request.thread_id))

    @router.get("/vault", response_model=VaultResponse)
    def vault_documents(
        conn: Conn,
        status_filter: Annotated[str | None, Query(alias="status")] = None,
        doc_type: Annotated[str | None, Query()] = None,
        pack_id: Annotated[str | None, Query()] = None,
        include_disabled: Annotated[bool, Query()] = False,
        limit: Annotated[int, Query(ge=1, le=200)] = 50,
        offset: Annotated[int, Query(ge=0)] = 0,
    ) -> VaultResponse:
        page = vault.documents(
            conn,
            status=status_filter,
            doc_type=doc_type,
            pack_id=pack_id,
            enabled=registry.enabled_pack_ids(conn),
            include_disabled=include_disabled,
            limit=limit,
            offset=offset,
        )
        return VaultResponse(
            documents=[_as_vault_document(document) for document in page.documents],
            total=page.total,
            limit=page.limit,
            offset=page.offset,
        )

    @router.get("/packs", response_model=PacksResponse)
    def packs(conn: Conn) -> PacksResponse:
        return PacksResponse(
            packs=[_as_pack_summary(row) for row in registry.packs(conn)],
            modules=[_as_module_summary(row) for row in registry.modules(conn)],
        )

    @router.patch("/packs/{pack_id}", response_model=PackSummary)
    def set_pack(pack_id: str, body: EnabledRequest, conn: Conn) -> PackSummary:
        try:
            updated = registry.set_pack_enabled(conn, pack_id, enabled=body.enabled)
        except registry.UnknownPack as error:
            raise HTTPException(
                status_code=404, detail=f"no installed pack with id {pack_id}"
            ) from error
        return _as_pack_summary(updated)

    @router.patch("/modules/{module_id}", response_model=ModuleSummary)
    def set_module(module_id: str, body: EnabledRequest, conn: Conn) -> ModuleSummary:
        try:
            updated = registry.set_module_enabled(conn, module_id, enabled=body.enabled)
        except registry.UnknownModule as error:
            raise HTTPException(
                status_code=404, detail=f"no installed module with id {module_id}"
            ) from error
        return _as_module_summary(updated)

    @router.get("/quarantine", response_model=QuarantineResponse)
    def quarantine_queue(
        conn: Conn,
        config: Config,
        limit: Annotated[int, Query(ge=1, le=200)] = 50,
    ) -> QuarantineResponse:
        waiting = quarantine.queue(conn, limit)
        blocked = quarantine.blocked_reasons(conn, waiting, Path(config.watch_folder))
        documents = [
            QuarantinedDocument(
                document_id=str(document.document_id),
                original_name=document.original_name,
                mime=document.mime,
                pages=document.pages,
                reason=document.reason,
                retryable=blocked.get(document.document_id) is None,
                blocked=blocked.get(document.document_id),
            )
            for document in waiting
        ]
        return QuarantineResponse(documents=documents, count=len(documents))

    @router.post(
        "/quarantine/{document_id}/retry",
        response_model=RetryAccepted,
        status_code=status.HTTP_202_ACCEPTED,
    )
    def retry_one(document_id: str, conn: Conn, config: Config) -> RetryAccepted:
        waiting = [
            item
            for item in quarantine.queue(conn, limit=200)
            if str(item.document_id) == document_id
        ]
        if not waiting:
            raise HTTPException(
                status_code=404, detail=f"document {document_id} is not in quarantine"
            )
        blocked = quarantine.blocked_reasons(conn, waiting, Path(config.watch_folder))
        reason = next(iter(blocked.values()), None)
        if reason is not None:
            # 409 rather than 500: nothing is broken, the file is simply not there to read.
            raise HTTPException(status_code=409, detail=reason)
        try:
            from core.worker.tasks import send_retry

            task_id = send_retry(config, document_id)
        except Exception as error:  # a broker that is not there raises its own class
            log.warning("could not queue a retry for %s: %s", document_id, error)
            raise HTTPException(
                status_code=503,
                detail=(
                    "The queue is not running, so the retry was not started. Start it with "
                    "`docker compose -f infra/docker-compose.yml up -d redis` and a worker."
                ),
            ) from error
        return RetryAccepted(document_id=document_id, task_id=task_id)

    return router


# ------------------------------------------------------------------------------- translation


def _as_response(answer: Answer) -> AskResponse:
    """One `Answer` to one of the three shapes a client has to handle."""
    if answer.refused:
        return AskResponse(kind="refusal", text=answer.text)
    if answer.abstained:
        return AskResponse(
            kind="abstention",
            text=answer.text,
            reason=answer.reason,
            missing=answer.missing,
            passages_read=answer.passages_read,
            dropped=answer.dropped,
        )
    return AskResponse(
        kind="answer",
        text=answer.text,
        claims=[
            Claim(text=claim.text, chunk_ids=list(claim.chunk_ids), citations=claim.citations)
            for claim in answer.claims
        ],
        citations=answer.citations,
        disclaimer=answer.disclaimer,
        passages_read=answer.passages_read,
        dropped=answer.dropped,
    )


def _as_vault_document(document: vault.VaultDocument) -> VaultDocument:
    return VaultDocument(
        document_id=str(document.document_id),
        original_name=document.original_name,
        mime=document.mime,
        pages=document.pages,
        doc_type=document.doc_type,
        pack_id=document.pack_id,
        pack_enabled=document.pack_enabled,
        status=document.status,
        quarantine_reason=document.quarantine_reason,
        ingested_at=document.ingested_at,
        synthetic=document.synthetic,
        facts=[
            VaultFact(
                key=fact.key,
                value=fact.value,
                value_type=fact.value_type,
                subject=fact.subject,
                page=fact.page,
                confidence=fact.confidence,
                verified_by_user=fact.verified_by_user,
            )
            for fact in document.facts
        ],
    )


def _as_pack_summary(row: registry.RegisteredPack) -> PackSummary:
    manifest = row.manifest
    registers = manifest.registers if manifest else None
    return PackSummary(
        id=row.id,
        version=row.version,
        display_name=manifest.display_name if manifest else row.id,
        enabled=row.enabled,
        on_disk=row.on_disk,
        installed_at=row.installed_at,
        document_types=sorted(manifest.document_types) if manifest else [],
        reminders=len(registers.reminder or []) if registers else 0,
        alerts=len(registers.alert or []) if registers else 0,
        tracker=bool(registers and registers.tracker),
        never_acts=manifest.guardrails.never_acts if manifest else True,
        disclaimer=manifest.guardrails.disclaimer if manifest else "",
        documents=row.documents,
        facts=row.facts,
    )


def _as_module_summary(row: registry.RegisteredModule) -> ModuleSummary:
    manifest = row.manifest
    return ModuleSummary(
        id=row.id,
        version=row.version,
        enabled=row.enabled,
        on_disk=row.on_disk,
        surfaces=list(manifest.surfaces) if manifest else [],
        runs_on=manifest.runs.on if manifest else "",
        cron=manifest.runs.cron if manifest else None,
    )
