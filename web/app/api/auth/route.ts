import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import {
  SESSION_COOKIE,
  SESSION_SECONDS,
  clearFailures,
  isConfigured,
  penalty,
  recordFailure,
  setPassphrase,
  verify,
} from "@/lib/lock";

/**
 * Unlock, set, and lock. Three verbs on one route because they are one concern.
 *
 * `node` runtime explicitly: `lib/lock.ts` needs `node:crypto` and the filesystem, and a route
 * that silently ran on the Edge would fail at the first request rather than at build time.
 */
export const runtime = "nodejs";

/** Never cached, never prerendered — the answer depends on a file that changes. */
export const dynamic = "force-dynamic";

const RATE_KEY = "local"; // one keyboard, one machine; there is nothing else to key on

export async function GET() {
  return NextResponse.json({ configured: isConfigured() });
}

export async function POST(request: Request) {
  const body = (await request.json().catch(() => ({}))) as { passphrase?: unknown };
  const passphrase = typeof body.passphrase === "string" ? body.passphrase : "";

  if (!passphrase) {
    return NextResponse.json({ error: "Enter your passphrase." }, { status: 400 });
  }

  // First run sets it; after that the same box unlocks. Two screens would mean a person had to
  // know which one they were on before they could type anything.
  const configured = isConfigured();
  if (!configured) {
    const created = setPassphrase(passphrase);
    if (!created.ok) {
      return NextResponse.json({ error: created.reason }, { status: 400 });
    }
    await grant(created.token);
    return NextResponse.json({ ok: true, created: true });
  }

  const wait = penalty(RATE_KEY);
  if (wait > 0) {
    await new Promise((resume) => setTimeout(resume, wait));
  }

  const opened = verify(passphrase);
  if (!opened.ok) {
    recordFailure(RATE_KEY);
    // 401 and one sentence. Never "no passphrase is set" versus "wrong passphrase" as separate
    // answers to a stranger — though on a machine they are already sitting at, that is
    // politeness rather than security.
    return NextResponse.json({ error: opened.reason }, { status: 401 });
  }

  clearFailures(RATE_KEY);
  await grant(opened.token);
  return NextResponse.json({ ok: true });
}

/** Lock it now, rather than waiting twelve hours for the session to lapse. */
export async function DELETE() {
  const jar = await cookies();
  jar.delete(SESSION_COOKIE);
  return NextResponse.json({ ok: true });
}

async function grant(token: string) {
  const jar = await cookies();
  jar.set(SESSION_COOKIE, token, {
    httpOnly: true, // no script on any page can read it, including this app's own
    sameSite: "lax",
    path: "/",
    maxAge: SESSION_SECONDS,
    // Loopback http is the normal case here, so `secure` would stop the cookie being set at
    // all. It is switched on if somebody ever puts this behind TLS.
    secure: process.env.NODE_ENV === "production" && process.env.PARROT_HTTPS === "1",
  });
}
