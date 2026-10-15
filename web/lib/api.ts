/**
 * The only way in.
 *
 * `web/` never touches the database. Every figure on every screen came through one of these
 * functions, which is the rule the whole lane is built on and also the reason the FastAPI app
 * ships no CORS middleware: from its point of view there is one client, on loopback, and it
 * arrives same-origin because server components call it from this process and the browser
 * calls it through `app/api/parrot/[...path]`.
 *
 * **Nothing here throws.** Every call returns either the data or a `Problem` a screen can
 * render. That is not defensive habit — it is the difference between "the local model is not
 * running, and reminders still work" and a spinner that never stops, and the second one is
 * what a person sees on the day Ollama was not started. The empty and error states are the
 * deliverable, not the polish.
 */

export const PARROT_API = process.env.PARROT_API_URL ?? "http://127.0.0.1:8000";

/* ------------------------------------------------------------------------------- the shapes
 *
 * These mirror `api/models.py` field for field. They are written out rather than generated
 * because a generator is a build step five people would have to run, and this file is small
 * enough that a rename shows up as a type error the moment it lands.
 */

export type Source = {
  document_id: string | null;
  document_name: string | null;
  page: number | null;
  /** "policy.pdf, page 1" — already formatted, so a list renders without work. */
  text: string;
  /**
   * A page of a document, a document on file (the inventory), published guidance, a fact read
   * off a document, a published rule value, or a figure Parrot worked out from those (ADR 0016).
   */
  kind?: "document" | "inventory" | "guidance" | "fact" | "rule" | "calculation" | "calendar";
  /** A rule value's own citation: it has no page to open, only who published it, and when. */
  publisher?: string | null;
  title?: string | null;
  /** As the publisher printed it: "26 September 2023". */
  dated?: string | null;
  url?: string | null;
};

export type TodayItem = {
  id: string;
  kind: "overdue" | "alert" | "reminder";
  urgency: number;
  pack_id: string;
  label: string;
  line: string;
  due_date: string | null;
  days_left: number | null;
  lead: number | null;
  sources: Source[];
};

export type TodayResponse = { as_of: string; items: TodayItem[] };

export type Claim = { text: string; chunk_ids: number[]; citations: Source[] };

export type AskResponse = {
  kind:
    | "answer"
    | "abstention"
    | "refusal"
    | "declined"
    | "advice"
    | "consent_required"
    | "advice_withheld"
    | "draft";
  text: string;
  claims: Claim[];
  citations: Source[];
  disclaimer: string;
  reason: string;
  missing: string;
  passages_read: number;
  dropped: number;
  offer?: string;
  /** The code-written verdict, when `kind` is `advice`. */
  verdict_text?: string;
};

/* ------------------------------------------------------------------------------------ advice
 *
 * ADR 0016. Code chose the verdict and printed every figure on these; the model wrote none of
 * it. They arrive on `/api/ask/stream` like every other event, `kind` discriminating.
 */

/** Advice was asked for before the owner agreed to this pack's current consent wording. */
export type ConsentRequiredEvent = {
  kind: "consent_required";
  pack_id: string;
  pack_name: string;
  /** Sent back as `ConsentRequest.version`, so a yes is to the words that were shown. */
  version: string;
  consent_text: string;
  disclaimer: string;
  /** What was asked for, in the pack's own words. */
  label: string;
};

/** Advice could not be worked out. `missing` names what it needs, in the pack's words. */
export type AdviceWithheldEvent = {
  kind: "advice_withheld";
  pack_id: string;
  label: string;
  person: string | null;
  missing: string[];
  disclaimer: string;
};

/** One number a calculator produced, already printed. */
export type AdviceFigure = { name: string; text: string };

/** A worked result. At most three explaining `sentence` events and a `finished` follow it. */
export type AdviceCardEvent = {
  kind: "advice";
  pack_id: string;
  label: string;
  person: string | null;
  /** A short code to style by; `verdict_text` is what a person reads. */
  verdict: string;
  verdict_text: string;
  figures: AdviceFigure[];
  /** Facts open their page; rule values carry `publisher`, `title`, `dated` and `url`. */
  inputs: Source[];
  /** A comparison table, header row first. Empty when nothing is compared. */
  rows: string[][];
  estimate: boolean;
  disclaimer: string;
  /** Empty unless a product is named. */
  product_disclosure: string;
  consent_version: string;
};

/** `outdated`: the owner agreed to an earlier wording, so they are asked again. */
export type ConsentStatus = "granted" | "withdrawn" | "none" | "outdated";

/** One item of `GET /api/advice/consents`, and the body `POST` answers with. */
export type AdviceConsent = {
  pack_id: string;
  display_name: string;
  version: string;
  consent_text: string;
  disclaimer: string;
  status: ConsentStatus;
};

/** The body of `POST /api/advice/consents`. */
export type ConsentRequest = {
  pack_id: string;
  version: string;
  action: "granted" | "withdrawn";
};

export type VaultFact = {
  id: number;
  key: string;
  value: string | number | null;
  value_type: string;
  subject: string | null;
  page: number;
  confidence: number;
  verified_by_user: boolean;
  /** Decided in `core/vault.py`. This screen renders the flag; it does not set the threshold. */
  needs_review: boolean;
};

export type VaultDocument = {
  document_id: string;
  original_name: string;
  mime: string;
  pages: number | null;
  doc_type: string | null;
  pack_id: string | null;
  pack_enabled: boolean;
  status: string;
  quarantine_reason: string | null;
  ingested_at: string | null;
  synthetic: boolean;
  facts: VaultFact[];
};

export type VaultResponse = {
  documents: VaultDocument[];
  total: number;
  limit: number;
  offset: number;
};

export type PackSummary = {
  id: string;
  version: string;
  display_name: string;
  enabled: boolean;
  on_disk: boolean;
  installed_at: string | null;
  never_acts: boolean;
  disclaimer: string;
};

export type ModuleSummary = {
  id: string;
  version: string;
  enabled: boolean;
  on_disk: boolean;
  surfaces: string[];
  runs_on: string;
  cron: string | null;
};

export type PacksResponse = { packs: PackSummary[]; modules: ModuleSummary[] };

export type QuarantinedDocument = {
  document_id: string;
  original_name: string;
  mime: string;
  pages: number | null;
  reason: string | null;
  retryable: boolean;
  blocked: string | null;
};

export type QuarantineResponse = { documents: QuarantinedDocument[]; count: number };

export type ObligationChanged = {
  obligation_id: number;
  state: "done" | "dismissed" | "snoozed";
  speaks_again: string | null;
};

export type CorrectionResponse = {
  fact_id: number;
  key: string;
  document_id: string;
  document_name: string;
  page: number;
  was: string | number | null;
  now: string | number | null;
  was_confidence: number;
  value_type: string;
};

/* ------------------------------------------------------------------------------- the result
 *
 * Three kinds of wrong, because a screen says something different about each and "something
 * went wrong" is not a sentence anybody can act on.
 */

export type Problem = {
  /**
   * - `offline` nothing answered on the loopback port — Parrot is not running
   * - `foreign` something answered, but it is not Parrot. A port collision, not a fault
   * - `database` Parrot is up and Postgres is not
   * - `error` Parrot answered and said no
   */
  kind: "offline" | "foreign" | "database" | "error";
  /** Shown to a person. Never a stack trace, never a connection string. */
  detail: string;
};

export type Result<T> = { ok: true; data: T } | { ok: false; problem: Problem };

/**
 * Endpoints that list something. None of them can legitimately 404 — they answer with an empty
 * list when a household has nothing — so a 404 from one of these means the thing on the port is
 * not Parrot. Worth telling apart: 8000 is a popular port, and "Not Found" sends somebody
 * hunting for a bug in code that is working.
 */
const ALWAYS_EXISTS = [
  "/api/today",
  "/api/vault",
  "/api/packs",
  "/api/quarantine",
  "/api/household",
  "/api/calendar",
];

async function get<T>(path: string): Promise<Result<T>> {
  let response: Response;
  try {
    response = await fetch(`${PARROT_API}${path}`, {
      // A household's obligations change when the worker writes, not when a page is cached.
      cache: "no-store",
      headers: { accept: "application/json" },
    });
  } catch {
    return {
      ok: false,
      problem: { kind: "offline", detail: `Nothing is answering on ${PARROT_API}.` },
    };
  }

  if (response.status === 404 && ALWAYS_EXISTS.some((known) => path.startsWith(known))) {
    return {
      ok: false,
      problem: {
        kind: "foreign",
        detail: `Something is answering on ${PARROT_API}, but it is not Parrot.`,
      },
    };
  }

  if (response.status === 503) {
    // `core/runtime/db.py` guarantees this message never carries the connection string.
    const detail = await problemDetail(response);
    return { ok: false, problem: { kind: "database", detail } };
  }

  if (!response.ok) {
    return { ok: false, problem: { kind: "error", detail: await problemDetail(response) } };
  }

  return { ok: true, data: (await response.json()) as T };
}

async function problemDetail(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: unknown };
    if (typeof body.detail === "string" && body.detail) return body.detail;
  } catch {
    // A non-JSON error body is not worth showing a person verbatim.
  }
  return `Parrot answered with ${response.status}.`;
}

/* ------------------------------------------------------------------------------ the reads */

/** `asOf` exists for the demonstration: it moves the whole sweep, not just the display. */
export function today(asOf?: string): Promise<Result<TodayResponse>> {
  return get<TodayResponse>(`/api/today${asOf ? `?as_of=${asOf}` : ""}`);
}

export function vault(params: Record<string, string> = {}): Promise<Result<VaultResponse>> {
  const query = new URLSearchParams(params).toString();
  return get<VaultResponse>(`/api/vault${query ? `?${query}` : ""}`);
}

export function document(id: string): Promise<Result<VaultDocument>> {
  return get<VaultDocument>(`/api/documents/${encodeURIComponent(id)}`);
}

export function packs(): Promise<Result<PacksResponse>> {
  return get<PacksResponse>("/api/packs");
}

export function quarantine(): Promise<Result<QuarantineResponse>> {
  return get<QuarantineResponse>("/api/quarantine");
}

/**
 * Where the browser goes for a page image.
 *
 * Through this app rather than straight at the API, so the request carries the session cookie
 * and a locked screen cannot be walked around by typing a document id into the address bar.
 */
export function pageImage(documentId: string, page: number): string {
  return `/api/parrot/documents/${encodeURIComponent(documentId)}/page/${page}`;
}

/* ---------------------------------------------------------------------------- advice consent
 *
 * Called from the browser, so through the guarded proxy rather than at `PARROT_API`: a yes to
 * advice is exactly the kind of request a locked screen must not be walked around for.
 */

/** A failed consent call. `stale` is the 409: the wording moved since it was shown. */
export type ConsentFailure = { ok: false; problem: Problem; stale: boolean };

/** Every switched-on pack that advises, its consent wording, and the owner's standing answer. */
export async function adviceConsents(): Promise<Result<AdviceConsent[]>> {
  const outcome = await throughProxy<AdviceConsent[]>("/api/parrot/advice/consents", {
    method: "GET",
    headers: { accept: "application/json" },
  });
  return outcome.ok ? outcome : { ok: false, problem: outcome.problem };
}

/**
 * Agree to, or withdraw from, one pack's consent wording at `version`.
 *
 * A grant at a version that is no longer current is refused with 409 (`stale`), and the only
 * right answer to that is to fetch the wording again and show it — never to retry with the new
 * version, which would record a yes to words nobody read.
 */
export function setAdviceConsent(
  request: ConsentRequest,
): Promise<{ ok: true; data: AdviceConsent } | ConsentFailure> {
  return throughProxy<AdviceConsent>("/api/parrot/advice/consents", {
    method: "POST",
    headers: { accept: "application/json", "content-type": "application/json" },
    body: JSON.stringify(request),
  });
}

async function throughProxy<T>(
  path: string,
  init: RequestInit,
): Promise<{ ok: true; data: T } | ConsentFailure> {
  let response: Response;
  try {
    response = await fetch(path, { ...init, cache: "no-store" });
  } catch {
    return {
      ok: false,
      problem: { kind: "offline", detail: "Parrot is not running on this computer." },
      stale: false,
    };
  }
  if (!response.ok) {
    return {
      ok: false,
      problem: { kind: "error", detail: await problemDetail(response) },
      stale: response.status === 409,
    };
  }
  return { ok: true, data: (await response.json()) as T };
}

/* --------------------------------------------------------------------------------- household
 *
 * Who lives here, and which one of them is you. Without it "what is my term life premium?"
 * answers from whichever term life policy ranked first — with a correct citation to the wrong
 * person's document, which is the one wrong answer the grounding gate cannot catch. See
 * ADR 0011.
 */

export type Relation = "self" | "partner" | "child" | "parent" | "other";

export type Person = {
  id: number;
  display_name: string;
  relation: Relation;
  is_owner: boolean;
  external: boolean;
  aliases: string[];
};

/** A name off a document that nobody has placed yet, and what the model thinks it is. */
export type PendingName = {
  id: number;
  alias: string;
  suggested_person_id: number | null;
  suggested_person_name: string | null;
  confidence: number | null;
  document_id: string | null;
  document_name: string | null;
};

export type HouseholdResponse = {
  people: Person[];
  owner: Person | null;
  pending: PendingName[];
  /** False until somebody has said who they are. The setup step is shown on this. */
  configured: boolean;
};

export function household(): Promise<Result<HouseholdResponse>> {
  return get<HouseholdResponse>("/api/household");
}

/* ---------------------------------------------------------------------------------- calendar
 *
 * ADR 0020. Two kinds of line: an event the household typed in, which can be changed here, and a
 * deadline read off a document, which is cited and cannot. Writes go through the guarded proxy,
 * so a locked screen cannot add to the calendar any more than it can read it.
 */

export type Repeat = "never" | "daily" | "weekly" | "monthly" | "yearly";

/** One stored entry, every date of it. */
export type CalendarEvent = {
  id: number;
  title: string;
  starts_on: string;
  ends_on: string | null;
  start_time: string | null;
  end_time: string | null;
  location: string | null;
  notes: string | null;
  person_id: number | null;
  person: string | null;
  repeat: Repeat;
  repeat_until: string | null;
  created_via: string;
  source: string;
};

/** What a person sets. Creates and replaces alike: an edit is to the whole series. */
export type CalendarEventIn = {
  title: string;
  starts_on: string;
  ends_on?: string | null;
  start_time?: string | null;
  end_time?: string | null;
  location?: string | null;
  notes?: string | null;
  person_id?: number | null;
  repeat?: Repeat;
  repeat_until?: string | null;
  created_via?: "form" | "ask";
};

/** One line on one day. */
export type CalendarEntry = {
  kind: "event" | "deadline";
  id: string;
  on: string;
  title: string;
  /** "9:00 am to 10:00 am", "all day", "due" — already worded. */
  when: string;
  start_time: string | null;
  person: string | null;
  location: string | null;
  event_id: number | null;
  pack_id: string | null;
  sources: Source[];
};

export type CalendarPerson = { id: number; display_name: string };

export type CalendarResponse = {
  start: string;
  end: string;
  entries: CalendarEntry[];
  events: CalendarEvent[];
  people: CalendarPerson[];
};

/** A calendar entry Parrot wrote down from a request in Ask and has not saved. */
export type DraftEvent = {
  kind: "draft";
  title: string;
  starts_on: string;
  start_time: string | null;
  end_time: string | null;
  person_id: number | null;
  person: string | null;
  location: string;
  note: string;
};

export function calendarRange(start: string, end: string): Promise<Result<CalendarResponse>> {
  return get<CalendarResponse>(`/api/calendar?start=${start}&end=${end}`);
}

/** The same range, from the browser: the Ask draft card needs the household's names. */
export async function calendarRangeInBrowser(
  start: string,
  end: string,
): Promise<Result<CalendarResponse>> {
  const outcome = await throughProxy<CalendarResponse>(
    `/api/parrot/calendar?start=${start}&end=${end}`,
    { method: "GET", headers: { accept: "application/json" } },
  );
  return outcome.ok ? outcome : { ok: false, problem: outcome.problem };
}

/** Create, or with `id` replace, one entry. */
export async function saveEvent(
  body: CalendarEventIn,
  id?: number,
): Promise<Result<CalendarEvent>> {
  const outcome = await throughProxy<CalendarEvent>(
    id === undefined ? "/api/parrot/calendar/events" : `/api/parrot/calendar/events/${id}`,
    {
      method: id === undefined ? "POST" : "PUT",
      headers: { accept: "application/json", "content-type": "application/json" },
      body: JSON.stringify(body),
    },
  );
  return outcome.ok ? outcome : { ok: false, problem: outcome.problem };
}

export async function deleteEvent(id: number): Promise<Result<{ id: number; title: string }>> {
  const outcome = await throughProxy<{ id: number; title: string }>(
    `/api/parrot/calendar/events/${id}`,
    { method: "DELETE", headers: { accept: "application/json" } },
  );
  return outcome.ok ? outcome : { ok: false, problem: outcome.problem };
}
