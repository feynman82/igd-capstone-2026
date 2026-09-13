import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { PARROT_API } from "@/lib/api";
import { SESSION_COOKIE, isUnlocked } from "@/lib/lock";

/**
 * Restart, shut down, and "is Parrot back yet?".
 *
 * A route of its own rather than a path through `app/api/parrot/[...path]`, because stopping the
 * engine is the one request that proxy must never be able to make. The engine refuses a
 * lifecycle request unless it carries `x-parrot-intent` and no `Sec-Fetch-Site`, and only this
 * file adds the one and — calling from the server — never sends the other. A page that talks the
 * generic proxy into forwarding `POST /api/system/shutdown` gets a 403 from the engine.
 *
 * Three checks before anything reaches the engine, cheapest first:
 *
 *   1. **Unlocked.** The same session check every proxied request passes. A locked screen cannot
 *      stop the household's assistant any more than it can open a document.
 *   2. **Same origin.** The session cookie is `SameSite=Lax`, which keeps it off a cross-site
 *      POST — but every other app on `localhost`, whatever its port, counts as the same *site*,
 *      so a page on `localhost:5173` would still send it. An Origin that is not this app's own is
 *      refused.
 *   3. **A known action.** Two verbs, named.
 *
 * `GET` is what the restarting screen polls. It answers 200 with `engine: "offline"` when nothing
 * is listening, because during a restart that is the expected answer rather than an error, and a
 * screen polling once a second should not have to parse failure statuses to learn it.
 */
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const ACTIONS = new Set(["restart", "shutdown"]);

/** Long enough for a busy engine, short enough that a stopped one does not stall the poll. */
const STATUS_TIMEOUT_MS = 4000;

async function unlocked(): Promise<boolean> {
  const jar = await cookies();
  return isUnlocked(jar.get(SESSION_COOKIE)?.value);
}

function sameOrigin(request: Request): boolean {
  const origin = request.headers.get("origin");
  return origin !== null && origin === new URL(request.url).origin;
}

export async function GET() {
  if (!(await unlocked())) {
    return NextResponse.json({ detail: "Parrot is locked." }, { status: 401 });
  }
  try {
    const response = await fetch(`${PARROT_API}/api/system`, {
      cache: "no-store",
      headers: { accept: "application/json" },
      signal: AbortSignal.timeout(STATUS_TIMEOUT_MS),
    });
    if (!response.ok) {
      return NextResponse.json({ engine: "offline" }, { headers: { "cache-control": "no-store" } });
    }
    return NextResponse.json(await response.json(), { headers: { "cache-control": "no-store" } });
  } catch {
    return NextResponse.json({ engine: "offline" }, { headers: { "cache-control": "no-store" } });
  }
}

export async function POST(request: Request) {
  if (!(await unlocked())) {
    return NextResponse.json({ detail: "Parrot is locked." }, { status: 401 });
  }
  if (!sameOrigin(request)) {
    return NextResponse.json(
      { detail: "Restart and shut down are only accepted from Parrot's own screens." },
      { status: 403 },
    );
  }

  const body = (await request.json().catch(() => ({}))) as { action?: unknown };
  const action = typeof body.action === "string" ? body.action : "";
  if (!ACTIONS.has(action)) {
    return NextResponse.json({ detail: "Not something Parrot does." }, { status: 400 });
  }

  try {
    const response = await fetch(`${PARROT_API}/api/system/${action}`, {
      method: "POST",
      cache: "no-store",
      headers: { accept: "application/json", "x-parrot-intent": action },
    });
    const payload = (await response.json().catch(() => ({}))) as Record<string, unknown>;
    return NextResponse.json(payload, {
      status: response.status,
      headers: { "cache-control": "no-store" },
    });
  } catch {
    return NextResponse.json(
      { detail: "Parrot is not running on this computer." },
      { status: 503 },
    );
  }
}
