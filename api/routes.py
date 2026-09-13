"""The endpoints the interface needs, on the existing loopback app.

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

**The three writes a person can make.** Everything above reads. Three endpoints here write, and
each one is a person disagreeing with the system rather than the system changing its own mind:
`PATCH /api/facts/{id}` is "that is not what the paper says", `POST /api/obligations/{id}/close`
is "done" or "this was never mine to do", and `.../snooze` is "not yet". None of them can write
a row that did not already exist, and none of them can write a fact without provenance —
`core/corrections.py` never touches `document_id` or `page`, so rule 2 holds through the one
path that lets a human edit a fact.

**A citation is something you can open.** The modules and the answer graph format a citation the
way a person says it — "policy.pdf, page 1" — and by the time it arrives here the document id
has been thrown away. `vault.resolve_names` puts it back, once per response rather than once per
chip, so `GET /api/documents/{id}/page/{n}` has something to be called with. That endpoint is
the only one in this file that returns bytes instead of JSON.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import date
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from fastapi.responses import StreamingResponse

from api.models import (
    AbstentionEvent,
    AskRequest,
    AskResponse,
    Claim,
    CloseRequest,
    ConfirmNameRequest,
    CorrectionRequest,
    CorrectionResponse,
    DeclinedEvent,
    EnabledRequest,
    ErrorEvent,
    FinishedEvent,
    ForgottenDocument,
    HouseholdResponse,
    ModuleSummary,
    ObligationChanged,
    OwnerRequest,
    PacksResponse,
    PackSummary,
    PendingName,
    PersonModel,
    PersonRequest,
    PlaceRequest,
    QuarantinedDocument,
    QuarantineResponse,
    ReadingEvent,
    RefusalEvent,
    RetryAccepted,
    SentenceEvent,
    Source,
    TelegramLinkRequest,
    TodayItem,
    TodayResponse,
    VaultDocument,
    VaultFact,
    VaultResponse,
)
from core import corrections, household, registry, vault
from core.graph import answer as graph
from core.graph.answer import Answer, AnswerGraph
from core.graph.baseline import DenseRetriever, NoReranker
from core.graph.inventory import HouseholdInventory
from core.graph.scope import HouseholdScope
from core.ingest import quarantine, source
from core.pages import PageUnavailable, RendererUnavailable, render_page
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


def _link(conn: Any, groups: list[list[Source]]) -> None:
    """Fill in `document_id` on every source, in one query for the whole response.

    Mutates in place because the alternative is rebuilding three nested lists to change one
    field on some of them. A name that resolves to nothing is left alone: the citation still
    says what it said, it simply is not a link, which is the right outcome for a document
    somebody has since deleted.
    """
    flat = [source_ for group in groups for source_ in group]
    resolved = vault.resolve_names(conn, [item.document_name or "" for item in flat])
    for item in flat:
        if item.document_id is None and item.document_name in resolved:
            item.document_id = str(resolved[item.document_name].document_id)


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

    for late in reminder.overdue(conn, on, enabled=enabled):
        days_left = (late.due_date - on).days
        items.append(
            TodayItem(
                id=f"obligation:{late.obligation_id}",
                kind="overdue",
                urgency=days_left,
                pack_id=late.pack_id,
                label=late.label,
                line=late.line(),
                due_date=late.due_date,
                days_left=days_left,
                sources=[
                    Source(
                        document_id=str(late.document_id) if late.document_id else None,
                        document_name=late.document_name,
                        page=late.page,
                        text=f"{late.document_name}, page {late.page}"
                        if late.document_name and late.page is not None
                        else (late.document_name or "no document behind this one"),
                    )
                ],
            )
        )

    items.sort(key=lambda item: (BUCKET[item.kind], item.urgency))
    _link(conn, [item.sources for item in items])
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

    def _graph_for(conn: Any, config: Settings) -> AnswerGraph:
        """One construction, used by both ask endpoints. They must not differ in what they read."""
        client = Ollama(config)
        enabled = registry.enabled_pack_ids(conn)
        return AnswerGraph(
            client,
            DenseRetriever(conn, client, None if enabled is None else tuple(sorted(enabled))),
            NoReranker(),
            inventory=HouseholdInventory(conn),
            packs=registry.enabled_packs(conn),
            # Who is asking. Built here because this is where the connection is; the graph
            # itself holds none. See `core/graph/scope.py` and ADR 0011.
            household=HouseholdScope(conn),
        )

    @router.post("/ask", response_model=AskResponse)
    def ask(ask_request: AskRequest, conn: Conn, config: Config) -> AskResponse:
        """The whole answer, once. For `scripts/ask.py`, for tests, and for anything that would
        rather wait than render progressively."""
        return _as_response(
            _graph_for(conn, config).ask(
                ask_request.question,
                thread_id=ask_request.thread_id,
                history=_history(ask_request),
            )
        )

    @router.post("/ask/stream")
    def ask_stream(ask_request: AskRequest, conn: Conn, config: Config) -> StreamingResponse:
        """The same answer, one verified sentence at a time.

        Server-sent events rather than a websocket: this is one question producing a short
        ordered burst of events and then ending, which is exactly what SSE is, and it survives
        being proxied by the Next.js route handler without either side holding a socket open.

        The sentences are already gated when they arrive here, so the only thing this handler
        does is turn a dataclass into a line of JSON. A `ModelUnavailable` that escapes the graph
        becomes an `error` event, because by the time it happens the response has begun and
        there is no status code left to send.
        """

        def events() -> Iterator[str]:
            try:
                for event in _graph_for(conn, config).stream(
                    ask_request.question,
                    thread_id=ask_request.thread_id,
                    history=_history(ask_request),
                ):
                    yield _sse(_as_event(event))
            except Exception as error:  # the stream has started; a 500 would never be seen
                log.exception("the answer stream failed")
                yield _sse(ErrorEvent(detail=f"Parrot stopped answering: {error}"))

        return StreamingResponse(
            events(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-store",
                # Nginx and friends buffer an event stream into uselessness by default. Nothing
                # sits in front of this today; the header costs nothing and stops a later
                # deployment quietly turning streaming back into waiting.
                "X-Accel-Buffering": "no",
            },
        )

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

    # -------------------------------------------------------------------------- documents
    #
    # Two endpoints, and the second is the point of the first. A person who clicked a citation
    # is asking to see the paper; nothing else in this file can show it to them.

    @router.get("/documents/{document_id}", response_model=VaultDocument)
    def one_document(document_id: str, conn: Conn) -> VaultDocument:
        """One document and everything read off it.

        Not filtered by the enabled set, unlike the listing. Somebody who followed a citation
        here is looking at a named thing; hiding it because its pack is switched off would be a
        dead end. `pack_enabled` says so instead, and the screen can be honest about it.
        """
        found = vault.document(conn, document_id, enabled=registry.enabled_pack_ids(conn))
        if found is None:
            raise HTTPException(status_code=404, detail=f"no document with id {document_id}")
        return _as_vault_document(found)

    @router.get("/documents/{document_id}/page/{page}")
    def document_page(document_id: str, page: int, conn: Conn, config: Config) -> Response:
        """The page itself, drawn. The one endpoint here that returns bytes.

        Four things can go wrong and a person is told which, because "could not open" is not an
        answer anybody can act on:

        * **404** there is no such document, or no such page in it
        * **409** the document is registered but its file has left the inbox. v1 keeps the
          inbox as the document store, so this is a real state and not a fault, and it is the
          same sentence the quarantine queue uses because it is the same situation
        * **501** this install has no PDF renderer

        The bytes are content-addressed: a document id is bound to one SHA-256, so a given page
        of a given document can never change and the response says so.
        """
        found = vault.document(conn, document_id)
        if found is None:
            raise HTTPException(status_code=404, detail=f"no document with id {document_id}")

        digest = source.digest_of_document(conn, document_id)
        if digest is None:  # pragma: no cover - the row was just read
            raise HTTPException(status_code=404, detail=f"no document with id {document_id}")

        try:
            payload = source.bytes_for(digest, Path(config.watch_folder))
        except source.SourceMissing as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

        try:
            drawn, media_type = render_page(payload, found.mime, page)
        except RendererUnavailable as error:
            raise HTTPException(status_code=501, detail=str(error)) from error
        except PageUnavailable as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

        return Response(
            content=drawn,
            media_type=media_type,
            headers={
                "Cache-Control": "private, max-age=86400, immutable",
                "Content-Disposition": "inline",
                "X-Content-Type-Options": "nosniff",
            },
        )

    # ------------------------------------------------------------------------------- facts

    @router.patch("/facts/{fact_id}", response_model=CorrectionResponse)
    def correct_fact(fact_id: int, body: CorrectionRequest, conn: Conn) -> CorrectionResponse:
        """That is not what the paper says. The only human write to `facts` in the system.

        422 rather than a coercion when the value does not fit the field's declared type. A
        premium quietly stored as the text "four hundred" would be worse than the wrong number
        it replaced, and the person is standing in front of the document and can retype it.
        """
        try:
            changed = corrections.correct(conn, fact_id, body.value)
        except corrections.UnknownFact as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except corrections.CorrectionRejected as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        return CorrectionResponse(
            fact_id=changed.fact_id,
            key=changed.key,
            document_id=str(changed.document_id),
            document_name=changed.document_name,
            page=changed.page,
            was=changed.was,
            now=changed.now,
            was_confidence=changed.was_confidence,
            value_type=changed.value_type,
        )

    # -------------------------------------------------------------------------- obligations

    @router.post("/obligations/{obligation_id}/close", response_model=ObligationChanged)
    def close_obligation(obligation_id: int, body: CloseRequest, conn: Conn) -> ObligationChanged:
        """Done, or dismissed. Both final, neither destructive.

        The distinction is kept because an evaluation that counts missed obligations has to
        tell "I renewed it" from "this reminder should never have existed" — the second is a
        finding about the pack, the first is the system working.
        """
        try:
            reminder.close(conn, obligation_id, state=body.state)
        except reminder.UnknownObligation as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        return ObligationChanged(obligation_id=obligation_id, state=body.state)

    @router.post("/obligations/{obligation_id}/snooze", response_model=ObligationChanged)
    def snooze_obligation(
        obligation_id: int,
        conn: Conn,
        as_of: Annotated[
            date | None, Query(description="YYYY-MM-DD, for the demonstration")
        ] = None,
    ) -> ObligationChanged:
        """Quiet until it gets more urgent, and say when that is.

        `speaks_again` is the day the next lead window opens, computed from the pack's own
        declared windows. Null means there is no tighter window left: the next thing this
        obligation does is go overdue.
        """
        try:
            speaks_again = reminder.snooze(conn, obligation_id, as_of)
        except reminder.UnknownObligation as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        return ObligationChanged(
            obligation_id=obligation_id, state="snoozed", speaks_again=speaks_again
        )

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

    @router.delete("/quarantine/{document_id}", response_model=ForgottenDocument)
    def forget_one(document_id: str, conn: Conn, config: Config) -> ForgottenDocument:
        """Forget a document whose file has left the inbox, so it stops asking for attention.

        409 while the file is still there, because capture would register it again at once.
        """
        try:
            name = quarantine.forget(conn, document_id, Path(config.watch_folder))
        except quarantine.StillInInbox as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        if name is None:
            raise HTTPException(
                status_code=404, detail=f"document {document_id} is not in quarantine"
            )
        return ForgottenDocument(document_id=document_id, original_name=name)

    # ------------------------------------------------------------------------ household
    #
    # Who lives here, and which one of them is you. The interface never touches the database,
    # so every one of these exists because a screen needs it. See ADR 0011.
    #
    # The shape to notice: there is no endpoint that *enumerates* the household. Setup names
    # one person -- you -- and everybody else arrives off a document, is classified by the
    # generator, and is confirmed by a person through `/household/names/{id}`. A roster you
    # type from memory before filing anything does not match what your documents say, and the
    # match is the only thing that matters.

    def _household(conn: Any) -> HouseholdResponse:
        people = household.roster(conn)
        owner = next((p for p in people if p.is_owner), None)
        return HouseholdResponse(
            people=[_as_person(p) for p in people],
            owner=_as_person(owner) if owner else None,
            pending=[
                PendingName(
                    id=row.id,
                    alias=row.alias,
                    suggested_person_id=row.person_id,
                    suggested_person_name=row.person_name,
                    confidence=row.confidence,
                    document_id=str(row.document_id) if row.document_id else None,
                    document_name=row.document_name,
                )
                for row in household.pending(conn)
            ],
            configured=owner is not None,
        )

    # `core/runtime/db.py` opens with autocommit off and says "the caller commits". For the
    # household the caller is the request: one screen action is one transaction, and a person
    # answering "who is this?" must not have it undone by the next handler that raises.
    # `core/registry.py` and `core/corrections.py` commit inside the domain function instead —
    # the difference is that those are called from a worker and a script as well as from here,
    # and `core/household.py` is deliberately kept free of that decision so its own tests can
    # roll back.
    def _saved(conn: Any) -> HouseholdResponse:
        conn.commit()
        return _household(conn)

    @router.get("/household", response_model=HouseholdResponse)
    def get_household(conn: Conn) -> HouseholdResponse:
        return _household(conn)

    @router.post("/household/owner", response_model=HouseholdResponse)
    def set_owner(request: OwnerRequest, conn: Conn) -> HouseholdResponse:
        """First run, and every later change of hands.

        Names an existing person as owner if one of their aliases already matches what was
        typed -- so correcting a spelling does not create a second copy of the same person --
        and otherwise creates them.
        """
        existing = household.resolve(conn, request.display_name)
        if existing is not None:
            household.set_owner(conn, existing.id)
        else:
            household.add_person(
                conn,
                request.display_name,
                "self",
                is_owner=True,
                aliases=tuple(request.aliases),
            )
        return _saved(conn)

    @router.put("/household/owner/{person_id}", response_model=HouseholdResponse)
    def hand_over(person_id: int, conn: Conn) -> HouseholdResponse:
        """Hand the household to somebody already in it. A daughter takes over her father's
        paperwork; the install follows rather than being abandoned."""
        try:
            household.set_owner(conn, person_id)
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        return _saved(conn)

    @router.post("/household/people", response_model=HouseholdResponse)
    def add_person(request: PersonRequest, conn: Conn) -> HouseholdResponse:
        household.add_person(
            conn,
            request.display_name,
            request.relation,
            aliases=tuple(request.aliases),
            external=request.external,
        )
        return _saved(conn)

    @router.post("/household/names/{alias_id}", response_model=HouseholdResponse)
    def confirm_name(alias_id: int, request: ConfirmNameRequest, conn: Conn) -> HouseholdResponse:
        """The answer to "who is this?" -- an existing person, or a new one in the same tap."""
        person_id = request.person_id
        if person_id is None:
            if not request.display_name:
                raise HTTPException(
                    status_code=400,
                    detail="Name an existing person, or give a name for a new one.",
                )
            person_id = household.add_person(
                conn,
                request.display_name,
                request.relation or "other",
                external=request.external,
            ).id
        elif request.relation is not None or request.external:
            # The person the model created off the document, placed in the same tap: "my
            # parent" or "not one of us" answers both who the name is and where they sit.
            try:
                household.place(
                    conn, person_id, request.relation or "other", external=request.external
                )
            except ValueError as error:
                raise HTTPException(status_code=404, detail=str(error)) from error
        try:
            household.confirm(conn, alias_id, person_id)
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        return _saved(conn)

    @router.patch("/household/people/{person_id}", response_model=HouseholdResponse)
    def place_person(person_id: int, request: PlaceRequest, conn: Conn) -> HouseholdResponse:
        """Correct how somebody is related to the owner, after the question was answered."""
        try:
            household.place(conn, person_id, request.relation, external=request.external)
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        return _saved(conn)

    @router.delete("/household/names/{alias_id}", response_model=HouseholdResponse)
    def dismiss_name(alias_id: int, conn: Conn) -> HouseholdResponse:
        """None of the answers was right. The name is forgotten and asked about again when it
        is next seen, which is better than recording something nobody agreed with."""
        household.dismiss(conn, alias_id)
        return _saved(conn)

    @router.post("/household/telegram", response_model=HouseholdResponse)
    def link_telegram(request: TelegramLinkRequest, conn: Conn) -> HouseholdResponse:
        """Whose phone is whose. The only ownership signal that arrives before parsing."""
        household.link_telegram(conn, request.chat_id, request.person_id)
        return _saved(conn)

    return router


# ------------------------------------------------------------------------------- translation


def _history(ask_request: AskRequest) -> list[tuple[str, str]]:
    """The conversation so far, as the graph reads it. Empty for a first question."""
    return [(turn.role, turn.text) for turn in ask_request.history]


def _sse(event: Any) -> str:
    """One event, in the wire format. `kind` is on the payload, so no `event:` line is needed."""
    return f"data: {event.model_dump_json()}\n\n"


def _as_source(citation: graph.Citation) -> Source:
    """A citation that never lost its document id, so the chip opens the page without a lookup."""
    return Source(
        document_id=str(citation.document_id) if citation.document_id else None,
        document_name=citation.document_name or None,
        page=citation.page,
        text=citation.text,
        kind=citation.kind,
    )


def _as_event(event: graph.Event) -> Any:
    if isinstance(event, graph.Reading):
        return ReadingEvent(passages_read=event.passages_read, person=event.person)
    if isinstance(event, graph.Sentence):
        return SentenceEvent(
            text=event.text,
            chunk_ids=list(event.chunk_ids),
            citations=[_as_source(citation) for citation in event.citations],
        )
    if isinstance(event, graph.Abstained):
        return AbstentionEvent(
            reason=event.reason,
            missing=event.missing,
            passages_read=event.passages_read,
            dropped=event.dropped,
            person=event.person,
            disclaimer=event.disclaimer,
        )
    if isinstance(event, graph.Refused):
        return RefusalEvent(text=event.text)
    if isinstance(event, graph.Declined):
        return DeclinedEvent(text=event.text, disclaimer=event.disclaimer, offer=event.offer)
    return FinishedEvent(
        citations=[],  # every source is already on the sentence that used it
        disclaimer=event.disclaimer,
        passages_read=event.passages_read,
        dropped=event.dropped,
        person=event.person,
        quarantined=event.quarantined,
        truncated=event.truncated,
        unanswered=event.unanswered,
    )


def _as_response(answer: Answer) -> AskResponse:
    """One `Answer` to one of the shapes a client has to handle."""
    if answer.declined:
        return AskResponse(
            kind="declined", text=answer.text, disclaimer=answer.disclaimer, offer=answer.offer
        )
    if answer.refused:
        return AskResponse(kind="refusal", text=answer.text)
    if answer.abstained:
        return AskResponse(
            kind="abstention",
            text=answer.text,
            disclaimer=answer.disclaimer,
            reason=answer.reason,
            missing=answer.missing,
            person=answer.person,
            passages_read=answer.passages_read,
            dropped=answer.dropped,
        )
    return AskResponse(
        kind="answer",
        text=answer.text,
        claims=[
            Claim(
                text=claim.text,
                chunk_ids=list(claim.chunk_ids),
                citations=[_as_source(citation) for citation in claim.citations],
            )
            for claim in answer.claims
        ],
        # Deduplicated across the answer, in the order a person met them.
        citations=list(
            {
                citation.text: _as_source(citation)
                for claim in answer.claims
                for citation in claim.citations
            }.values()
        ),
        disclaimer=answer.disclaimer,
        person=answer.person,
        passages_read=answer.passages_read,
        dropped=answer.dropped,
        quarantined=answer.quarantined,
        truncated=answer.truncated,
        unanswered=answer.unanswered,
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
                id=fact.id,
                key=fact.key,
                value=fact.value,
                value_type=fact.value_type,
                subject=fact.subject,
                page=fact.page,
                confidence=fact.confidence,
                verified_by_user=fact.verified_by_user,
                needs_review=fact.needs_review,
            )
            for fact in document.facts
        ],
    )


def _as_person(person: household.Person) -> PersonModel:
    return PersonModel(
        id=person.id,
        display_name=person.display_name,
        relation=person.relation,
        is_owner=person.is_owner,
        external=person.external,
        aliases=list(person.aliases),
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
