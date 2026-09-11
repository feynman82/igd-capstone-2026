import { createHmac, pbkdf2Sync, randomBytes, timingSafeEqual } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

/**
 * The local passphrase.
 *
 * Login is a passphrase on this computer, not an account somewhere else. An offline-capable
 * assistant that needs a network round trip to open is not offline-capable, and a household
 * document vault has no business knowing an email address. Google OAuth appears exactly once
 * in the plan — authorising Drive, post-MVP — and it is not this.
 *
 * **What this protects, said plainly, because the setup screen says it too.** It locks the
 * screen. It does not encrypt anything: the documents sit in the watched folder and the facts
 * sit in Postgres, and anyone who can open a terminal on this machine can read both without
 * going near a browser. What it buys is that a laptop left open in a kitchen does not show a
 * stranger the household's policy numbers. Claiming more than that would be worse than
 * claiming nothing, and Siew reviews this.
 *
 * **Why a file and not the database.** `web/` never touches Postgres — that is the rule this
 * whole lane is built on — and localStorage would put the lock inside the thing being locked,
 * where clearing site data unlocks it. So the verifier lives in a file beside the app, which
 * is also what makes "I forgot it" recoverable: delete the file and set a new one, since it
 * guards a screen rather than a key to any data.
 *
 * PBKDF2-HMAC-SHA256 at 210,000 iterations, which is the OWASP figure for this construction.
 * Argon2id would be better and is a native dependency; the threat here is a person at the
 * keyboard, not an offline attack on a stolen hash, and the hash is on the same disk as the
 * documents anyway.
 */

const ITERATIONS = 210_000;
const KEY_LENGTH = 32;
const DIGEST = "sha256";

/** Twelve hours: long enough not to be asked twice in a day, short enough to matter overnight. */
export const SESSION_SECONDS = 12 * 60 * 60;

export const SESSION_COOKIE = "parrot_session";

type Stored = {
  version: 1;
  salt: string;
  iterations: number;
  hash: string;
  /** Signs the session cookie. Rotating it — setting a new passphrase — logs every tab out. */
  secret: string;
};

function lockFile(): string {
  // Beside the app rather than in it, so `next build` never sweeps it into a bundle.
  return process.env.PARROT_LOCK_FILE ?? join(process.cwd(), ".parrot", "lock.json");
}

function read(): Stored | null {
  try {
    const parsed = JSON.parse(readFileSync(lockFile(), "utf8")) as Stored;
    return parsed.version === 1 && parsed.salt && parsed.hash ? parsed : null;
  } catch {
    // Missing is the first-run case and is not an error. Malformed is treated the same way:
    // an unreadable lock file must not be a wall a person cannot get past on their own machine.
    return null;
  }
}

function write(stored: Stored): void {
  const path = lockFile();
  mkdirSync(dirname(path), { recursive: true });
  // 0600 where the platform honours it. Windows ignores the mode, which is why the docstring
  // above does not promise anything this file cannot deliver.
  writeFileSync(path, JSON.stringify(stored, null, 2), { encoding: "utf8", mode: 0o600 });
}

function derive(passphrase: string, salt: Buffer, iterations: number): Buffer {
  return pbkdf2Sync(passphrase.normalize("NFKC"), salt, iterations, KEY_LENGTH, DIGEST);
}

/** True once a passphrase has been chosen. The unlock screen asks a different question if not. */
export function isConfigured(): boolean {
  return read() !== null;
}

export type Rejected = { ok: false; reason: string };
export type Accepted = { ok: true; token: string; expiresAt: number };

/** Minimum length, stated as a sentence rather than as a regex nobody can satisfy. */
export function setPassphrase(passphrase: string): Accepted | Rejected {
  const chosen = passphrase.normalize("NFKC");
  if (chosen.length < 8) {
    return { ok: false, reason: "Use at least 8 characters. A short phrase beats a short word." };
  }
  const salt = randomBytes(16);
  const secret = randomBytes(32);
  write({
    version: 1,
    salt: salt.toString("base64"),
    iterations: ITERATIONS,
    hash: derive(chosen, salt, ITERATIONS).toString("base64"),
    secret: secret.toString("base64"),
  });
  return mint(secret);
}

export function verify(passphrase: string): Accepted | Rejected {
  const stored = read();
  if (stored === null) {
    return { ok: false, reason: "No passphrase has been set on this computer yet." };
  }
  const salt = Buffer.from(stored.salt, "base64");
  const expected = Buffer.from(stored.hash, "base64");
  const actual = derive(passphrase, salt, stored.iterations);
  // Constant time, so the number of correct leading bytes cannot be read off the clock.
  if (actual.length !== expected.length || !timingSafeEqual(actual, expected)) {
    return { ok: false, reason: "That is not the passphrase for this computer." };
  }
  return mint(Buffer.from(stored.secret, "base64"));
}

function mint(secret: Buffer): Accepted {
  const expiresAt = Date.now() + SESSION_SECONDS * 1000;
  return { ok: true, token: `${expiresAt}.${sign(String(expiresAt), secret)}`, expiresAt };
}

function sign(payload: string, secret: Buffer): string {
  return createHmac(DIGEST, secret).update(payload).digest("base64url");
}

/**
 * Is this cookie one we issued, and is it still in date?
 *
 * Called by the layout every app page renders through, which is deliberate: a middleware check
 * would run on the Edge runtime where `node:crypto` and the filesystem are both absent, so it
 * could only look at whether a cookie exists rather than whether it is real.
 */
export function isUnlocked(token: string | undefined): boolean {
  const stored = read();
  if (stored === null) return false;
  if (!token) return false;

  const [expiry, signature] = token.split(".");
  if (!expiry || !signature) return false;

  const expiresAt = Number(expiry);
  if (!Number.isFinite(expiresAt) || expiresAt <= Date.now()) return false;

  const expected = Buffer.from(sign(expiry, Buffer.from(stored.secret, "base64")), "utf8");
  const actual = Buffer.from(signature, "utf8");
  return expected.length === actual.length && timingSafeEqual(expected, actual);
}

/**
 * A deliberate pause after a wrong passphrase, growing with each one.
 *
 * In-process and per-process, so restarting the server clears it. That is the honest scope: it
 * makes guessing at the keyboard tedious, which is the threat this screen has. It is not a
 * defence against anything automated, and the rest of the file explains why there is nothing
 * here worth automating against.
 */
const failures = new Map<string, number>();

export function penalty(key: string): number {
  const seen = failures.get(key) ?? 0;
  return Math.min(seen, 5) * 400;
}

export function recordFailure(key: string): void {
  failures.set(key, (failures.get(key) ?? 0) + 1);
}

export function clearFailures(key: string): void {
  failures.delete(key);
}
