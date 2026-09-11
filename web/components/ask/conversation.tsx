"use client";

import { useChat } from "@ai-sdk/react";
import { ArrowUp, Square } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Turn } from "@/components/ask/answer";
import type { ParrotMessage } from "@/lib/chat";

/**
 * The conversation. `useChat` holds the messages; everything it renders arrived verified.
 *
 * The composer is at the bottom and the thread scrolls above it, which is the shape every
 * person already knows. What is different is what a turn contains: not a paragraph with sources
 * listed underneath, but a series of sentences each of which brought its own.
 */

const SUGGESTIONS = [
  "When does the motor policy expire?",
  "What did I donate, and to whom?",
  "What is the renewal premium?",
] as const;

export function Conversation() {
  const { messages, sendMessage, status, stop, error } = useChat<ParrotMessage>({});
  const [draft, setDraft] = useState("");
  const thread = useRef<HTMLDivElement>(null);
  const busy = status === "submitted" || status === "streaming";

  // Follow the answer down as sentences arrive. `smooth` deliberately: this is the one moment
  // the interface moves on its own, and a jump would lose the reader's place.
  useEffect(() => {
    thread.current?.scrollTo({ top: thread.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  function ask(question: string) {
    const asked = question.trim();
    if (!asked || busy) return;
    setDraft("");
    void sendMessage({ text: asked });
  }

  return (
    <div className="flex h-[calc(100dvh-var(--s-8))] flex-col">
      <div ref={thread} className="min-h-0 flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <Opening onPick={ask} />
        ) : (
          <ul className="space-y-[var(--s-6)] pb-[var(--s-6)]">
            {messages.map((message) => (
              <Turn key={message.id} message={message} />
            ))}
          </ul>
        )}
      </div>

      {error ? (
        <p role="alert" className="mb-[var(--s-2)] text-meta text-crit">
          {error.message}
        </p>
      ) : null}

      {/* The focus ring is on this wrapper, via `focus-within`, not on the field — the field
          has `outline-none` on purpose. A composer is one control made of several elements, and
          ringing the whole thing is what a person expects. An automated check that looks only at
          `document.activeElement` reports this as a missing ring; it is not, and this note is
          here so nobody "fixes" it. */}
      <form
        onSubmit={(event) => {
          event.preventDefault();
          ask(draft);
        }}
        className="flex items-end gap-[var(--s-2)] rounded-[var(--r)] border border-edge bg-surface p-[var(--s-2)] focus-within:outline-2 focus-within:outline-offset-2 focus-within:outline-focus"
      >
        <label htmlFor="question" className="sr-only">
          Ask about your documents
        </label>
        <textarea
          id="question"
          value={draft}
          rows={1}
          placeholder="Ask about your documents"
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={(event) => {
            // Enter sends, Shift+Enter breaks the line. Never animate a keyboard action.
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              ask(draft);
            }
          }}
          className="max-h-40 min-h-[2.25rem] flex-1 resize-none bg-transparent px-[var(--s-2)] py-[var(--s-1)] text-body outline-none"
        />
        {busy ? (
          <button
            type="button"
            onClick={() => stop()}
            title="Stop"
            className="grid size-9 shrink-0 place-items-center rounded-[var(--r-sm)] border border-edge transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
          >
            <Square aria-hidden size={14} strokeWidth={2.5} />
            <span className="sr-only">Stop</span>
          </button>
        ) : (
          <button
            type="submit"
            disabled={!draft.trim()}
            className="grid size-9 shrink-0 place-items-center rounded-[var(--r-sm)] bg-accent text-accent-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-40"
          >
            <ArrowUp aria-hidden size={16} strokeWidth={2.5} />
            <span className="sr-only">Ask</span>
          </button>
        )}
      </form>

      <p className="mt-[var(--s-2)] text-meta text-ink-3">
        Parrot answers only from your own documents, and says so when they do not cover a
        question.
      </p>
    </div>
  );
}

/**
 * The empty thread.
 *
 * Three questions rather than a blank box, because a person who does not know what is in their
 * vault does not know what to ask it. The design pack wants these generated from the week's
 * ingest; there is no endpoint for that yet, so these are fixed and honest about being examples
 * rather than dressed up as personalised.
 */
function Opening({ onPick }: { onPick: (question: string) => void }) {
  return (
    <div className="flex h-full flex-col justify-center">
      <h1 className="font-display text-screen lg:text-display">Ask about your documents</h1>
      <p className="mt-[var(--s-3)] max-w-[var(--measure)] text-lead text-ink-2">
        Every sentence in an answer carries the document and page it came from. When nothing in
        your vault covers a question, Parrot says so rather than guessing.
      </p>
      <ul className="mt-[var(--s-5)] flex flex-wrap gap-[var(--s-2)]">
        {SUGGESTIONS.map((question) => (
          <li key={question}>
            <button
              type="button"
              onClick={() => onPick(question)}
              className="rounded-[var(--r-pill)] border border-edge px-[var(--s-4)] py-[var(--s-2)] text-meta transition-colors hover:bg-surface-2"
            >
              {question}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
