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

from datetime import date, datetime, time
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class Source(BaseModel):
    """A document and a page, as a person would cite it — or, for published guidance, who
    published it and when.

    A published rule value (ADR 0016) has no document and no page to open, so `document_id` and
    `page` are null and `publisher`, `title`, `dated` and `url` say where it came from instead.
    """

    document_id: str | None = None
    document_name: str | None = None
    page: int | None = None
    text: str  # "policy.pdf, page 1" — already formatted, so a list renders without work
    # What the citation is evidence of: a page, a document on file, published guidance, a fact
    # read off a document, a published rule value, or a figure worked out from those.
    # A calendar line (ADR 0020) cites the calendar on its date: `url` is that day's page.
    kind: Literal[
        "document", "inventory", "guidance", "fact", "rule", "calculation", "calendar"
    ] = "document"
    publisher: str | None = None
    title: str | None = None
    dated: str | None = None  # as the publisher printed it: "26 September 2023"
    url: str | None = None


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


class Turn(BaseModel):
    """One earlier turn of the conversation. Read to make a follow-up whole; never evidence."""

    role: Literal["user", "assistant"]
    text: str = Field(max_length=4000)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    thread_id: str = Field(default="local", max_length=64)
    history: list[Turn] = Field(default_factory=list, max_length=12)


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


# The streamed form of the same answer. One event per line of an `text/event-stream`, and the
# `kind` on each says which. A client that renders these in order and a client that POSTs
# `/api/ask` are looking at the same answer — `AnswerGraph.ask` is `AnswerGraph.stream` drained.


class ReadingEvent(BaseModel):
    """Evidence gathered and good enough to answer from. Nothing has been claimed yet."""

    kind: Literal["reading"] = "reading"
    passages_read: int
    # Set when the question was first-person and the evidence was narrowed to one member of
    # the household. Shown for the same reason a citation is: whose answer this is.
    person: str | None = None


class SentenceEvent(BaseModel):
    """One sentence that has passed the gate, with the sources it passed on.

    It will never be withdrawn, reworded or re-cited. That is the contract this whole stream
    exists to keep: a screen can render this the moment it arrives and never take it back.
    """

    kind: Literal["sentence"] = "sentence"
    text: str
    chunk_ids: list[int]
    citations: list[Source]


class AbstentionEvent(BaseModel):
    kind: Literal["abstention"] = "abstention"
    reason: str
    missing: str = ""
    passages_read: int = 0
    dropped: int = 0
    person: str | None = None
    disclaimer: str = ""


class RefusalEvent(BaseModel):
    kind: Literal["refusal"] = "refusal"
    text: str


class DeclinedEvent(BaseModel):
    """A request for a recommendation or a judgement, declined by a pack without advice."""

    kind: Literal["declined"] = "declined"
    text: str
    disclaimer: str = ""
    offer: str = ""  # a question Parrot can answer instead; shown, never answered on its own


class FinishedEvent(BaseModel):
    kind: Literal["finished"] = "finished"
    citations: list[Source] = Field(default_factory=list)
    disclaimer: str = ""
    passages_read: int = 0
    dropped: int = 0
    person: str | None = None
    quarantined: int = 0  # documents not checked, when the answer said "none on file"
    truncated: bool = False  # the pack's sentence limit ended the answer
    unanswered: bool = False  # only a line about the documents on file was said, not the answer


# The advice events (ADR 0016). Code chose the verdict and printed every figure on them; the model
# wrote none of it. `consent_required` and `advice_withheld` are the whole stream on their own;
# `advice` is followed by at most three `sentence` events explaining it, then `finished`.


class ConsentRequiredEvent(BaseModel):
    """Advice was asked for before the owner agreed to this pack's current consent wording.

    Nothing was calculated and nothing was recorded. It carries what `POST /api/advice/consents`
    needs back — the pack and the version — so a screen can ask and record the answer without
    looking anything up.
    """

    kind: Literal["consent_required"] = "consent_required"
    pack_id: str
    pack_name: str
    version: str
    consent_text: str
    disclaimer: str
    label: str  # what was asked for, in the pack's own words


class AdviceWithheldEvent(BaseModel):
    """Advice could not be worked out. `missing` names each fact or rule it needed, in the pack's
    own words, because the honest answer to a missing fact is to name it, not estimate around it.
    """

    kind: Literal["advice_withheld"] = "advice_withheld"
    pack_id: str
    label: str
    person: str | None = None
    missing: list[str]
    disclaimer: str


class AdviceFigure(BaseModel):
    """One number a calculator produced, already printed the way the verdict prints it."""

    name: str
    text: str


class AdviceCardEvent(BaseModel):
    """A worked result, sent before any explanation so it stands alone if the model does not.

    `inputs` are what it rests on, each a `Source`: a fact opens its page, a published rule value
    names its publisher, title, date and URL. `rows` is a comparison table with its header row
    first, empty when nothing is compared. `product_disclosure` is empty unless a product is named.
    """

    kind: Literal["advice"] = "advice"
    pack_id: str
    label: str
    person: str | None = None
    verdict: str  # a short code a screen can style by; `verdict_text` is what a person reads
    verdict_text: str
    figures: list[AdviceFigure]
    inputs: list[Source]
    rows: list[list[str]] = Field(default_factory=list)
    estimate: bool = False
    disclaimer: str
    product_disclosure: str = ""
    consent_version: str


class DraftEvent(BaseModel):
    """A calendar entry Parrot wrote down and did not save (ADR 0020). Confirming it is a separate
    request a person makes, `POST /api/calendar/events`, so nothing here has happened yet."""

    kind: Literal["draft"] = "draft"
    title: str
    starts_on: date
    start_time: time | None = None
    end_time: time | None = None
    person_id: int | None = None
    person: str | None = None
    location: str = ""
    note: str


class ErrorEvent(BaseModel):
    """The stream broke after it began. A client cannot read an HTTP status by then."""

    kind: Literal["error"] = "error"
    detail: str


class AskResponse(BaseModel):
    """The whole answer, once. `text` is the consent wording when `kind` is `consent_required`,
    and the verdict followed by its explanation when `kind` is `advice`. The card's figures,
    inputs and table are streamed only: a screen drawing advice reads `/api/ask/stream`."""

    kind: Literal[
        "answer",
        "abstention",
        "refusal",
        "declined",
        "advice",
        "consent_required",
        "advice_withheld",
        "draft",
    ]
    text: str
    verdict_text: str = ""  # the code-written verdict, when advice was given
    draft: DraftEvent | None = None  # the entry to confirm, when `kind` is `draft`
    claims: list[Claim] = Field(default_factory=list)
    citations: list[Source] = Field(default_factory=list)
    disclaimer: str = ""
    reason: str = ""  # why it abstained
    missing: str = ""  # what document would have answered it
    person: str = ""  # whose documents this was narrowed to, when it was
    passages_read: int = 0
    dropped: int = 0
    offer: str = ""  # a question that can be answered instead, when it declined
    quarantined: int = 0  # documents not checked, when the answer said "none on file"
    truncated: bool = False  # the pack's sentence limit ended the answer
    unanswered: bool = False  # only a line about the documents on file was said, not the answer


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
    # Computed in `core/vault.py`, not here and not in the browser: one threshold, one place.
    needs_review: bool = False


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
    never_acts: bool = True
    disclaimer: str = ""


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


# ------------------------------------------------------------------------------- household
#
# Who lives here, what they are called on paper, and which one of them is you. See ADR 0011.
# The interface never touches the database, so this is the only way it learns any of it.


class PersonModel(BaseModel):
    id: int
    display_name: str
    relation: Literal["self", "partner", "child", "parent", "other"]
    is_owner: bool
    external: bool = False
    aliases: list[str] = Field(default_factory=list)


class PendingName(BaseModel):
    """A name off a document that nobody has placed yet, and what the model thinks it is.

    `person_id` is a suggestion and is never treated as settled: nothing unconfirmed scopes an
    answer. It is here so a screen can offer one tap instead of a form.
    """

    id: int
    alias: str
    suggested_person_id: int | None = None
    suggested_person_name: str | None = None
    confidence: float | None = None
    document_id: str | None = None
    document_name: str | None = None


class HouseholdResponse(BaseModel):
    people: list[PersonModel]
    owner: PersonModel | None = None
    pending: list[PendingName] = Field(default_factory=list)
    # False until somebody has said who they are. The interface shows the setup step on this,
    # rather than on whether a passphrase exists — the two are different questions and an
    # install can be past one and not the other.
    configured: bool = False


class OwnerRequest(BaseModel):
    """First run: the name on your documents. One field, because the owner is the one person
    anybody can name without thinking, and everybody else arrives off a document."""

    display_name: str = Field(min_length=1, max_length=120)
    aliases: list[str] = Field(default_factory=list, max_length=12)


class PersonRequest(BaseModel):
    display_name: str = Field(min_length=1, max_length=120)
    relation: Literal["self", "partner", "child", "parent", "other"] = "other"
    aliases: list[str] = Field(default_factory=list, max_length=12)
    external: bool = False


class ConfirmNameRequest(BaseModel):
    """The answer to "who is this?". Either an existing person, or a new one to create."""

    person_id: int | None = None
    display_name: str | None = Field(default=None, max_length=120)
    # Unset means "leave it as it is" for an existing person and `other` for a new one. Set with
    # `person_id`, it places the person the model created off the document in the same tap.
    relation: Literal["partner", "child", "parent", "other"] | None = None
    external: bool = False


class PlaceRequest(BaseModel):
    """How somebody already in the roster is related to the owner. The owner's own is `self`."""

    relation: Literal["partner", "child", "parent", "other"]
    external: bool = False


class ForgottenDocument(BaseModel):
    """A quarantined document Parrot no longer remembers."""

    document_id: str
    original_name: str
    status: Literal["forgotten"] = "forgotten"


class TelegramLinkRequest(BaseModel):
    chat_id: int
    person_id: int


# ---------------------------------------------------------------------------------- advice
#
# The owner's consent to a pack's advice (ADR 0016). Read and recorded here, never by an answer:
# an answer that needs consent ends on `consent_required`, and a person answers it on this screen.


class AdviceConsent(BaseModel):
    """One advising pack, the wording a person is asked to agree to, and what the owner last said.

    `outdated` means the owner agreed to an earlier `version`: the wording has changed since, so
    they are asked again, with this text.
    """

    pack_id: str
    display_name: str
    version: str
    consent_text: str
    disclaimer: str
    status: Literal["granted", "withdrawn", "none", "outdated"]


class ConsentRequest(BaseModel):
    """Yes or no to one pack's consent wording, at the version the screen showed.

    `version` is sent back rather than assumed, so a person who read one wording is never
    recorded as agreeing to a newer one that arrived while the screen was open: that is a 409.
    """

    pack_id: str = Field(min_length=1, max_length=64)
    version: str = Field(min_length=1, max_length=32)
    action: Literal["granted", "withdrawn"]


# --------------------------------------------------------------------------------- calendar


class CalendarEventIn(BaseModel):
    """What a person sets on an entry. The same shape creates and replaces one: an edit is to the
    whole series (ADR 0020), so there is no partial update to get half right."""

    title: str = Field(min_length=1, max_length=200)
    starts_on: date
    ends_on: date | None = None  # last day, inclusive, of an entry spanning several
    start_time: time | None = None  # none is all day
    end_time: time | None = None
    location: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=2000)
    person_id: int | None = None  # none is the whole household
    repeat: Literal["never", "daily", "weekly", "monthly", "yearly"] = "never"
    repeat_until: date | None = None
    # `ask` when a person confirmed a draft Parrot wrote; the audit of what Parrot proposed.
    created_via: Literal["form", "ask"] = "form"

    @model_validator(mode="after")
    def _ordered(self) -> CalendarEventIn:
        if not self.title.strip():
            raise ValueError("an entry needs a title")
        if self.ends_on is not None and self.ends_on < self.starts_on:
            raise ValueError("an entry cannot end before it starts")
        if self.end_time is not None and (
            self.start_time is None or self.end_time <= self.start_time
        ):
            raise ValueError("an end time needs a start time before it")
        if self.repeat_until is not None and self.repeat_until < self.starts_on:
            raise ValueError("a repeat cannot stop before the entry starts")
        return self


class CalendarEvent(BaseModel):
    """One stored entry, every date of it. Occurrences are `CalendarEntry` rows."""

    id: int
    title: str
    starts_on: date
    ends_on: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    location: str | None = None
    notes: str | None = None
    person_id: int | None = None
    person: str | None = None
    repeat: Literal["never", "daily", "weekly", "monthly", "yearly"]
    repeat_until: date | None = None
    created_via: str
    source: str  # `local` today; a sync adapter would set `google` or `icloud`


class CalendarEntry(BaseModel):
    """One line on one day: an event's occurrence, or a deadline read off a document.

    A deadline is never editable and always cited; an event is editable through `event_id` and
    cites nothing, because nothing about it is a claim about a document."""

    kind: Literal["event", "deadline"]
    id: str  # "event:12:2026-10-17" or "obligation:3"
    on: date
    title: str
    when: str  # "9:00 am to 10:00 am", "all day", "due"
    start_time: time | None = None
    person: str | None = None
    location: str | None = None
    event_id: int | None = None
    pack_id: str | None = None
    sources: list[Source] = Field(default_factory=list)


class CalendarPerson(BaseModel):
    id: int
    display_name: str


class CalendarResponse(BaseModel):
    start: date
    end: date
    entries: list[CalendarEntry]
    events: list[CalendarEvent]  # each series once, for the edit form
    people: list[CalendarPerson]  # who an entry can be for


class DeletedEvent(BaseModel):
    id: int
    title: str


# ------------------------------------------------------------------------- conversations


class ConversationSummary(BaseModel):
    """One line in Ask's history column: what was first asked, and when it was last used."""

    id: str
    title: str
    updated_at: datetime


class ConversationsResponse(BaseModel):
    conversations: list[ConversationSummary]


class Conversation(ConversationSummary):
    """A past conversation as the screen drew it. A transcript to reopen, never a source: these
    messages are the AI SDK's own shape and nothing on the server reads inside them but the
    first question, for the title."""

    messages: list[dict[str, Any]]


class ConversationIn(BaseModel):
    """The whole conversation, written over what was stored. 400 messages is a long evening of
    questions; the cap is there so a runaway client cannot fill the disk."""

    messages: list[dict[str, Any]] = Field(min_length=1, max_length=400)
