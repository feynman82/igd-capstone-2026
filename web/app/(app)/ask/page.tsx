import type { Metadata } from "next";
import { Conversation } from "@/components/ask/conversation";

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
 */
export default function AskPage() {
  return <Conversation />;
}
