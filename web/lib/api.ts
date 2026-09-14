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
  /** A page of a document, a document on file (the inventory), or published guidance (PR 3). */
  kind?: "document" | "inventory" | "guidance";
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
  kind: "answer" | "abstention" | "refusal" | "declined";
  text: string;
  claims: Claim[];
  citations: Source[];
  disclaimer: string;
  reason: string;
  missing: string;
  passages_read: number;
  dropped: number;
  offer?: string;
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
  document_types: string[];
  reminders: number;
  alerts: number;
  tracker: boolean;
  never_acts: boolean;
  disclaimer: string;
  documents: number;
  facts: number;
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
