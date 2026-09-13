import { createUIMessageStream, createUIMessageStreamResponse } from "ai";
import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { PARROT_API, type Source } from "@/lib/api";
import type { ParrotMessage } from "@/lib/chat";
import { SESSION_COOKIE, isUnlocked } from "@/lib/lock";

/**
 * The adapter. Parrot's own event stream in, the AI SDK's protocol out.
 *
 * It exists so that `useChat` on the client is the ordinary `useChat` with nothing special
 * about it, and so that the browser never holds a connection to the Python process. Every
 * event that arrives here has already passed the grounding gate — this handler renames things
 * and forwards them, and there is deliberately no place in it where a sentence could be
 * altered, reordered or dropped.
 *
 * One behaviour worth stating: the upstream connection is **not** abandoned when the reader
 * goes away. A person who closes the tab mid-answer has still had the model run; letting the
 * request finish is cheaper than a half-written generation on a machine with one GPU.
 */
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** What `/api/ask/stream` emits. Mirrors `api/models.py`; `kind` discriminates. */
type ParrotEvent =
  | { kind: "reading"; passages_read: number; person?: string | null }
  | { kind: "sentence"; text: string; chunk_ids: number[]; citations: Source[] }
  | {
      kind: "abstention";
      reason: string;
      missing: string;
      passages_read: number;
      dropped: number;
      person?: string | null;
      disclaimer?: string;
    }
  | { kind: "refusal"; text: string }
  | { kind: "declined"; text: string; disclaimer: string; offer: string }
  | {
      kind: "finished";
      disclaimer: string;
      passages_read: number;
      dropped: number;
      person?: string | null;
      quarantined?: number;
      truncated?: boolean;
      unanswered?: boolean;
    }
  | { kind: "error"; detail: string };

export async function POST(request: Request) {
  const jar = await cookies();
  if (!isUnlocked(jar.get(SESSION_COOKIE)?.value)) {
    return NextResponse.json({ detail: "Parrot is locked." }, { status: 401 });
  }

  const body = (await request.json().catch(() => ({}))) as {
    messages?: ParrotMessage[];
    id?: string;
  };
  const question = lastQuestion(body.messages ?? []);
  if (!question) {
    return NextResponse.json({ detail: "Ask a question." }, { status: 400 });
  }

  const stream = createUIMessageStream<ParrotMessage>({
    execute: async ({ writer }) => {
      let upstream: Response;
      try {
        upstream = await fetch(`${PARROT_API}/api/ask/stream`, {
          method: "POST",
          headers: { "content-type": "application/json", accept: "text/event-stream" },
          // A thread id per conversation: the graph's checkpointer is keyed on it. The earlier
          // turns go too, so "what about 3 nights?" is understood as the question it follows.
          body: JSON.stringify({
            question,
            thread_id: (body.id ?? "local").slice(0, 64),
            history: priorTurns(body.messages ?? []),
          }),
        });
      } catch {
        writer.write({
          type: "data-error",
          data: { detail: `Nothing is answering on ${PARROT_API}.` },
        });
        return;
      }

      if (!upstream.ok || !upstream.body) {
        writer.write({
          type: "data-error",
          data: { detail: await upstreamDetail(upstream) },
        });
        return;
      }

      for await (const event of readEvents(upstream.body)) {
        // `data-<kind>` is the AI SDK's convention for a typed part. The kinds are Parrot's own
        // and the mapping is one to one, so a new event upstream is a compile error here rather
        // than something silently swallowed.
        switch (event.kind) {
          case "reading":
            writer.write({
              type: "data-reading",
              data: { passages_read: event.passages_read, person: event.person },
            });
            break;
          case "sentence":
            writer.write({
              type: "data-sentence",
              data: {
                text: event.text,
                chunk_ids: event.chunk_ids,
                citations: event.citations,
              },
            });
            break;
          case "abstention":
            writer.write({ type: "data-abstention", data: event });
            break;
          case "refusal":
            writer.write({ type: "data-refusal", data: { text: event.text } });
            break;
          case "declined":
            writer.write({
              type: "data-declined",
              data: { text: event.text, disclaimer: event.disclaimer, offer: event.offer },
            });
            break;
          case "finished":
            writer.write({
              type: "data-finished",
              data: {
                disclaimer: event.disclaimer,
                passages_read: event.passages_read,
                dropped: event.dropped,
                person: event.person,
                quarantined: event.quarantined,
                truncated: event.truncated,
                unanswered: event.unanswered,
              },
            });
            break;
          case "error":
            writer.write({ type: "data-error", data: { detail: event.detail } });
            break;
        }
      }
    },
    // Never leak a stack trace to a browser. The states this interface has are the ones in
    // `components/states.tsx`, and "an internal error occurred" is not one of them.
    onError: () => "Parrot stopped answering.",
  });

  return createUIMessageStreamResponse({ stream });
}

/** The text of the newest user turn. `useChat` sends the whole conversation; the graph asks one. */
function lastQuestion(messages: ParrotMessage[]): string {
  for (let index = messages.length - 1; index >= 0; index -= 1) {
    const message = messages[index];
    if (message.role !== "user") continue;
    const text = (message.parts ?? [])
      .filter((part) => part.type === "text")
      .map((part) => (part as { text: string }).text)
      .join(" ")
      .trim();
    if (text) return text.slice(0, 2000);
  }
  return "";
}

/** How many earlier turns the router reads, and how much of each. It resolves a follow-up. */
const HISTORY_TURNS = 6;
const TURN_CHARS = 1200;

/**
 * The conversation before the newest question, as Parrot's `history`: what the person asked,
 * and what Parrot said back — its verified sentences, or why it did not answer.
 *
 * Context for understanding the next question, never evidence for answering it. The graph reads
 * it in the router alone, and nothing an earlier answer said can be cited by a later one.
 */
function priorTurns(messages: ParrotMessage[]): { role: "user" | "assistant"; text: string }[] {
  let last = -1;
  for (let index = messages.length - 1; index >= 0; index -= 1) {
    if (messages[index].role === "user") {
      last = index;
      break;
    }
  }
  const turns: { role: "user" | "assistant"; text: string }[] = [];
  for (const message of messages.slice(0, Math.max(last, 0))) {
    const parts = message.parts ?? [];
    let text = "";
    if (message.role === "user") {
      text = parts
        .filter((part) => part.type === "text")
        .map((part) => (part as { text: string }).text)
        .join(" ");
    } else if (message.role === "assistant") {
      text = parts
        .map((part) => {
          if (part.type === "data-sentence") return (part as { data: { text: string } }).data.text;
          if (part.type === "data-abstention")
            return `I could not answer: ${(part as { data: { reason: string } }).data.reason}.`;
          if (part.type === "data-refusal") return (part as { data: { text: string } }).data.text;
          if (part.type === "data-declined")
            return (part as { data: { text: string } }).data.text;
          return "";
        })
        .filter(Boolean)
        .join(" ");
    }
    text = text.trim();
    if (text && (message.role === "user" || message.role === "assistant")) {
      turns.push({ role: message.role, text: text.slice(0, TURN_CHARS) });
    }
  }
  return turns.slice(-HISTORY_TURNS);
}

async function upstreamDetail(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: unknown };
    if (typeof body.detail === "string" && body.detail) return body.detail;
  } catch {
    // A non-JSON error body is not worth showing a person verbatim.
  }
  return `Parrot answered with ${response.status}.`;
}

/**
 * Server-sent events, parsed.
 *
 * Written out rather than pulled from a library because the whole format is: records separated
 * by a blank line, fields prefixed `data: `. A partial record is held until the rest of it
 * arrives — the one thing a naïve split on `\n\n` gets wrong, and the thing that would show up
 * as a sentence going missing under load rather than as an error.
 */
async function* readEvents(body: ReadableStream<Uint8Array>): AsyncGenerator<ParrotEvent> {
  const reader = body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      let split = buffer.indexOf("\n\n");
      while (split !== -1) {
        const record = buffer.slice(0, split);
        buffer = buffer.slice(split + 2);
        const parsed = parseRecord(record);
        if (parsed) yield parsed;
        split = buffer.indexOf("\n\n");
      }
    }
    const last = parseRecord(buffer);
    if (last) yield last;
  } finally {
    reader.releaseLock();
  }
}

function parseRecord(record: string): ParrotEvent | null {
  const data = record
    .split("\n")
    .filter((line) => line.startsWith("data:"))
    .map((line) => line.slice(5).trimStart())
    .join("\n");
  if (!data) return null;
  try {
    return JSON.parse(data) as ParrotEvent;
  } catch {
    return null;
  }
}
