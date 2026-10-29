"use client";

import { useChat } from "@ai-sdk/react";
import { ArrowUp, Square } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Pending, Turn } from "@/components/ask/answer";
import { PageHeader } from "@/components/page-header";
import { saveConversation, type ConversationSummary } from "@/lib/api";
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
  "Analyze my insurance coverage.",
] as const;

export function Conversation({
  id,
  initial,
  onSaved,
  toolbar,
}: {
  /**
   * The thread id, for the life of this conversation. The graph's checkpointer, every advice
   * record and the saved transcript are keyed on it; without it the route falls back to "local"
   * and every conversation on this computer shares one thread.
   */
  id: string;
  /** A past conversation being reopened, as it was drawn. Empty for a new one. */
  initial: ParrotMessage[];
  onSaved: (summary: ConversationSummary) => void;
  /** Above the thread: the history and new-conversation buttons on a phone. */
  toolbar?: React.ReactNode;
}) {
  const [unsaved, setUnsaved] = useState(false);
  const { messages, sendMessage, status, stop, error } = useChat<ParrotMessage>({
    id,
    messages: initial,
    // Saved whole after every turn, stopped ones too: what was shown is what is kept. A save
    // that fails costs the history and never the answer, so it is a line, not an error.
    onFinish: async ({ messages: all }) => {
      const saved = await saveConversation(id, all);
      setUnsaved(!saved.ok);
      if (saved.ok) onSaved(saved.data);
    },
  });
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

  // The question again, after the owner agreed to a pack's advice. Not `ask`: that clears the
  // composer, and whatever the person has started typing meanwhile is theirs.
  function askAgain(question: string) {
    const asked = question.trim();
    if (!asked || busy) return;
    void sendMessage({ text: asked });
  }

  // The one surface that is a viewport rather than a page: the thread scrolls and the composer
  // stays put. The subtraction is the chrome above it and the padding around it, which is why
  // `--bar` is a fixed height rather than whatever the header happens to measure. Below `lg`
  // the bottom tab bar takes another 3.5rem, and without subtracting it the honest sentence
  // under the composer sits behind the tabs.
  return (
    <div className="flex h-[calc(100dvh-var(--bar)-var(--s-6)-var(--s-7)-3.5rem)] flex-col lg:h-[calc(100dvh-var(--bar)-var(--s-6)-var(--s-7))]">
      {toolbar}
      {/* `relative` so an answer's visually hidden text is placed inside the scroll box. Without
          it, an absolutely positioned `sr-only` span takes the page as its container, and a long
          answer makes the whole page scroll beneath a thread that was meant to scroll alone. */}
      <div ref={thread} className="relative min-h-0 flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <Opening onPick={ask} />
        ) : (
          <>
            {/* Every surface has a name for a screen reader to land on; here the questions are
                the visible headings, so the name is only for it. */}
            <h1 className="sr-only">Ask</h1>
            <ul className="pb-[var(--s-6)]">
              {messages.map((message, index) => (
                <Turn
                  key={message.id}
                  message={message}
                  question={questionBefore(messages, index)}
                  busy={busy}
                  onConsented={askAgain}
                />
              ))}
              {busy && messages.at(-1)?.role === "user" ? <Pending /> : null}
            </ul>
          </>
        )}
      </div>

      {error ? (
        <p role="alert" className="mb-[var(--s-2)] text-caption text-crit">
          {error.message}
        </p>
      ) : null}
      {unsaved ? (
        <p role="status" className="mb-[var(--s-2)] text-caption text-ink-3">
          This conversation could not be added to your history. The answers above are unaffected.
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
            className="grid size-9 shrink-0 place-items-center rounded-[var(--r-sm)] bg-brand text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-40"
          >
            <ArrowUp aria-hidden size={16} strokeWidth={2.5} />
            <span className="sr-only">Ask</span>
          </button>
        )}
      </form>

      <p className="mt-[var(--s-2)] text-caption text-ink-3">
        Parrot answers only from your own documents, and says so when they do not cover a
        question.
      </p>
    </div>
  );
}

/** The newest question at or before `index`: what an assistant turn was answering. */
function questionBefore(messages: ParrotMessage[], index: number): string {
  for (let at = index; at >= 0; at -= 1) {
    const message = messages[at];
    if (message.role !== "user") continue;
    return (message.parts ?? [])
      .filter((part) => part.type === "text")
      .map((part) => (part as { text: string }).text)
      .join(" ");
  }
  return "";
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
      <PageHeader
        title="Ask about your documents"
        lead="Every sentence in an answer carries the document and page it came from. When nothing in your vault covers a question, Parrot says so rather than guessing."
      />
      <ul className="mt-[var(--s-5)] flex flex-wrap gap-[var(--s-2)]">
        {SUGGESTIONS.map((question) => (
          <li key={question}>
            <button
              type="button"
              onClick={() => onPick(question)}
              className="rounded-[var(--r-pill)] border border-edge px-[var(--s-4)] py-[var(--s-2)] text-caption transition-colors hover:bg-surface-2"
            >
              {question}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
