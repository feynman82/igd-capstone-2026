import type { Metadata } from "next";
import { randomUUID } from "node:crypto";
import { Ask } from "@/components/ask/ask";
import { conversation, conversations } from "@/lib/api";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Ask · Parrot",
  description: "A question about your documents, answered with the page it came from.",
};

/**
 * The conversational surface, one tab away from Today.
 *
 * It exists for Marcus's question — the one with a specific answer buried in a specific
 * document — rather than as the front door. Retrieval is still the core of the product; Today
 * is what the Reminder and Alert modules put on top of it.
 *
 * `?c=` reopens a past conversation, so one can be bookmarked or come back to after a reload.
 * A new one gets its id here rather than in the browser, so the server and the browser start
 * from the same thread.
 */
export default async function AskPage({
  searchParams,
}: {
  searchParams: Promise<{ c?: string }>;
}) {
  const { c } = await searchParams;
  const [past, opened] = await Promise.all([
    conversations(),
    c ? conversation(c) : Promise.resolve(null),
  ]);

  return (
    <Ask
      past={past.ok ? past.data.conversations : null}
      opened={
        opened?.ok
          ? { id: opened.data.id, messages: opened.data.messages }
          : { id: randomUUID(), messages: [] }
      }
    />
  );
}
