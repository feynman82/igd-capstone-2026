import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { PARROT_API } from "@/lib/api";
import { SESSION_COOKIE, isUnlocked } from "@/lib/lock";

/**
 * The browser's only route to the API, and it is guarded.
 *
 * Server components call FastAPI directly from this process. Anything the *browser* needs —
 * a page image, a correction, a snooze — comes through here instead, for two reasons.
 *
 * The first is same-origin. `api/main.py` ships no CORS middleware on purpose, so a `fetch`
 * from the page to port 8000 would be refused; arriving here it is same-origin and no other
 * origin is ever granted one.
 *
 * The second is the lock, and it is the one that matters. The API answers any request from
 * loopback — it has no idea a passphrase exists. Without this check, a locked screen could be
 * walked straight around by typing a document id into the address bar. So every proxied
 * request is refused unless the session cookie is real and in date.
 */
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// PUT is a calendar entry replaced whole (ADR 0020): an edit is to every date of a series.
const ALLOWED = new Set(["GET", "POST", "PUT", "PATCH", "DELETE"]);

async function forward(request: Request, path: string[]): Promise<Response> {
  const jar = await cookies();
  if (!isUnlocked(jar.get(SESSION_COOKIE)?.value)) {
    return NextResponse.json({ detail: "Parrot is locked." }, { status: 401 });
  }

  if (!ALLOWED.has(request.method)) {
    return NextResponse.json({ detail: "Not something Parrot does." }, { status: 405 });
  }

  // Rebuilt from the matched segments rather than passed through, so a path cannot be talked
  // into leaving `/api/` by way of an encoded traversal.
  const target = new URL(`${PARROT_API}/api/${path.map(encodeURIComponent).join("/")}`);
  target.search = new URL(request.url).search;

  const body = request.method === "GET" || request.method === "DELETE" ? undefined : await request.text();

  let response: Response;
  try {
    response = await fetch(target, {
      method: request.method,
      headers: {
        accept: request.headers.get("accept") ?? "application/json",
        ...(body === undefined ? {} : { "content-type": "application/json" }),
      },
      body,
      cache: "no-store",
    });
  } catch {
    return NextResponse.json(
      { detail: "Parrot is not running on this computer." },
      { status: 503 },
    );
  }

  // Streamed rather than buffered: a page image is a few hundred kilobytes and there is no
  // reason for it to sit in this process's memory on the way past.
  return new Response(response.body, {
    status: response.status,
    headers: {
      "content-type": response.headers.get("content-type") ?? "application/json",
      // The API's own caching answer is kept — a page of a document genuinely cannot change —
      // but it is never widened here.
      ...(response.headers.get("cache-control")
        ? { "cache-control": response.headers.get("cache-control")! }
        : { "cache-control": "no-store" }),
      "x-content-type-options": "nosniff",
    },
  });
}

type Context = { params: Promise<{ path: string[] }> };

export async function GET(request: Request, context: Context) {
  return forward(request, (await context.params).path);
}

export async function POST(request: Request, context: Context) {
  return forward(request, (await context.params).path);
}

export async function PUT(request: Request, context: Context) {
  return forward(request, (await context.params).path);
}

export async function PATCH(request: Request, context: Context) {
  return forward(request, (await context.params).path);
}

export async function DELETE(request: Request, context: Context) {
  return forward(request, (await context.params).path);
}
