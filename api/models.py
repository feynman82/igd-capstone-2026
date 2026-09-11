"""What the interface is promised. Response types only — nothing here queries anything.

These are the shapes Lane D draws against, so they are written down separately from the
handlers that fill them. Two conventions run through all of them:

**Every item that states something carries its source.** A `TodayItem` has `sources`, a
`VaultFact` has a `page`, a `Claim` has `citations`. There is no response type in this file
that can express a fact without saying where it came from, which is rule 2 and rule 3 showing
up in the API surface rather than only in the database.

**One response type per endpoint, discriminated by `kind` where it varies.** `/api/ask` can
answer, abstain or refuse, and a client should not have to guess from which fields are absent.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class Source(BaseModel):
    """A document and a page, as a person would cite it."""

    document_id: str | None = None
    document_name: str | None = None
    page: int | None = None
    text: str  # "policy.pdf, page 1" — already formatted, so a list renders without work


# ------------------------------------------------------------------------------------ today


class TodayItem(BaseModel):
    id: str  # "obligation:42" or "iras_tax.days_uncovered.Marcus Fernandez"
    kind: Literal["overdue", "alert", "reminder"]
    urgency: int  # the sort key, smaller is more urgent; the list is already in this order
    pack_id: str
    label: str
    line: str  # the module's own sentence, so the CLI and the screen say the same thing
    due_date: date | None = None
    days_left: int | None = None
    lead: int | None = None
    sources: list[Source] = Field(default_factory=list)


class TodayResponse(BaseModel):
    as_of: date
    items: list[TodayItem]


# -------------------------------------------------------------------------------------- ask


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    thread_id: str = Field(default="local", max_length=64)


class Claim(BaseModel):
    """One sentence and the passages it was traced to. Never emitted without `citations`.

    A citation is a `Source` rather than a string. The answer graph formats it the way a person
    says it — "policy.pdf, page 1" — and that sentence survives as `Source.text`; what is added
    is the document id, looked up once per response, so the chip beside the sentence is
    something a person can open rather than something they have to go and find.
    """

    text: str
    chunk_ids: list[int]
    citations: list[Source]


class AskResponse(BaseModel):
    kind: Literal["answer", "abstention", "refusal"]
    text: str
    claims: list[Claim] = Field(default_factory=list)
    citations: list[Source] = Field(default_factory=list)
    disclaimer: str = ""
    reason: str = ""  # why it abstained
    missing: str = ""  # what document would have answered it
    passages_read: int = 0
    dropped: int = 0


# ------------------------------------------------------------------------------------ vault


class VaultFact(BaseModel):
    id: int  # what `PATCH /api/facts/{id}` addresses
    key: str
    value: str | float | None
    value_type: str
    subject: str | None = None
    page: int
    confidence: float
    verified_by_user: bool


class VaultDocument(BaseModel):
    document_id: str
    original_name: str
    mime: str
    pages: int | None = None
    doc_type: str | None = None
    pack_id: str | None = None
    pack_enabled: bool = True
    status: str
    quarantine_reason: str | None = None
    ingested_at: datetime | None = None
    synthetic: bool = False
    facts: list[VaultFact] = Field(default_factory=list)


class VaultResponse(BaseModel):
    documents: list[VaultDocument]
    total: int
    limit: int
    offset: int


# ------------------------------------------------------------------------------------ packs


class PackSummary(BaseModel):
    id: str
    version: str
    display_name: str
    enabled: bool
    on_disk: bool  # false when the row outlived the directory
    installed_at: datetime | None = None
    document_types: list[str] = Field(default_factory=list)
    reminders: int = 0
    alerts: int = 0
    tracker: bool = False
    never_acts: bool = True
    disclaimer: str = ""
    documents: int = 0
    facts: int = 0


class ModuleSummary(BaseModel):
    id: str
    version: str
    enabled: bool
    on_disk: bool
    surfaces: list[str] = Field(default_factory=list)
    runs_on: str = ""
    cron: str | None = None


class PacksResponse(BaseModel):
    packs: list[PackSummary]
    modules: list[ModuleSummary]


class EnabledRequest(BaseModel):
    enabled: bool


# ------------------------------------------------------------------------------- corrections


class CorrectionRequest(BaseModel):
    """What the person typed. The pack decides what type it is; the caller does not get to say.

    One field, deliberately. A screen cannot ask for the value to be stored as text, or move it
    to another page, or set its own confidence — those are the three ways a correction endpoint
    turns into a way of writing arbitrary rows into `facts`.
    """

    value: str = Field(min_length=1, max_length=500)


class CorrectionResponse(BaseModel):
    """What changed, in the words the screen confirms it with.

    `was` is returned rather than discarded because the screen says "was $486.00" under the
    corrected field: a person who mistypes needs to see what they replaced.
    """

    fact_id: int
    key: str
    document_id: str
    document_name: str
    page: int
    was: str | float | None
    now: str | float | None
    was_confidence: float
    value_type: str


# ------------------------------------------------------------------------------- obligations


class CloseRequest(BaseModel):
    state: Literal["done", "dismissed"]


class ObligationChanged(BaseModel):
    """The row is gone from Today. `speaks_again` is null when it will not come back.

    A snooze that cannot say when it ends is a snooze a person will not trust, so the date is
    computed from the pack's own lead windows and returned rather than left to the interface to
    guess.
    """

    obligation_id: int
    state: Literal["done", "dismissed", "snoozed"]
    speaks_again: date | None = None


# ------------------------------------------------------------------------------- quarantine


class QuarantinedDocument(BaseModel):
    document_id: str
    original_name: str
    mime: str
    pages: int | None = None
    reason: str | None = None  # why it needs eyes
    retryable: bool = True
    blocked: str | None = None  # why it cannot be retried, when it cannot


class QuarantineResponse(BaseModel):
    documents: list[QuarantinedDocument]
    count: int


class RetryAccepted(BaseModel):
    """202. The vision pass is slower than a page load, so it is queued and this is the receipt."""

    document_id: str
    task_id: str
    status: Literal["queued"] = "queued"
