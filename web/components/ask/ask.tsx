"use client";

import { History, SquarePen, X } from "lucide-react";
import { useRef, useState } from "react";
import { Conversation } from "@/components/ask/conversation";
import { conversationInBrowser, type ConversationSummary } from "@/lib/api";
import type { ParrotMessage } from "@/lib/chat";

type Open = { id: string; messages: ParrotMessage[] };

/**
 * Ask, with its history beside it.
 *
 * Past conversations are a column on a wide screen and a drawer on a phone — the same list, in
 * the native `<dialog>` so focus, Escape and the backdrop behave as a person's own system does.
 * A conversation is saved by the thread after every turn, and arrives here through `onSaved` so
 * the list moves without a round trip.
 *
 * Switching conversations remounts the thread (`key`), because `useChat` holds its messages
 * from the moment it starts and a conversation is a different chat, not new messages in this
 * one. The address follows along with `?c=`, so a reload lands where the person was.
 */
export function Ask({ past, opened }: { past: ConversationSummary[] | null; opened: Open }) {
  const [list, setList] = useState(past ?? []);
  const [current, setCurrent] = useState(opened);
  const [problem, setProblem] = useState<string | null>(null);
  const [opening, setOpening] = useState<string | null>(null);
  const drawer = useRef<HTMLDialogElement>(null);

  function show(next: Open) {
    setCurrent(next);
    setProblem(null);
    window.history.replaceState(null, "", next.messages.length ? `/ask?c=${next.id}` : "/ask");
    drawer.current?.close();
  }

  async function open(id: string) {
    if (id === current.id) {
      drawer.current?.close();
      return;
    }
    // Marked as chosen the moment it is pressed; the transcript follows a beat later.
    setOpening(id);
    const found = await conversationInBrowser(id);
    setOpening(null);
    if (!found.ok) {
      setProblem(found.problem.detail);
      return;
    }
    show({ id, messages: found.data.messages });
  }

  function fresh() {
    show({ id: crypto.randomUUID(), messages: [] });
  }

  function saved(summary: ConversationSummary) {
    setList((rows) => [summary, ...rows.filter((row) => row.id !== summary.id)]);
    if (!window.location.search.includes(`c=${summary.id}`)) {
      window.history.replaceState(null, "", `/ask?c=${summary.id}`);
    }
  }

  const column = (
    <Past
      rows={list}
      unavailable={past === null}
      current={opening ?? current.id}
      problem={problem}
      onOpen={open}
      onFresh={fresh}
    />
  );

  return (
    <div data-wide className="lg:grid lg:grid-cols-[15rem_minmax(0,1fr)] lg:gap-[var(--s-6)]">
      <aside
        aria-label="Past conversations"
        className="hidden lg:block lg:h-[calc(100dvh-var(--bar)-var(--s-6)-var(--s-7))]"
      >
        {column}
      </aside>

      <Conversation
        key={current.id}
        id={current.id}
        initial={current.messages}
        onSaved={saved}
        toolbar={
          <div className="mb-[var(--s-3)] flex items-center gap-[var(--s-2)] lg:hidden">
            <button
              type="button"
              onClick={() => drawer.current?.showModal()}
              className="inline-flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-2)] text-caption font-semibold"
            >
              <History aria-hidden size={15} strokeWidth={2} />
              History
            </button>
            <button
              type="button"
              onClick={fresh}
              className="inline-flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] px-[var(--s-3)] py-[var(--s-2)] text-caption font-semibold text-ink-2 hover:bg-surface-2 hover:text-ink"
            >
              <SquarePen aria-hidden size={15} strokeWidth={2} />
              New conversation
            </button>
          </div>
        }
      />

      {/* A click on the backdrop lands on the dialog itself, not on anything inside it. */}
      <dialog
        ref={drawer}
        aria-label="Past conversations"
        onClick={(event) => {
          if (event.target === event.currentTarget) event.currentTarget.close();
        }}
        className="m-0 h-dvh max-h-dvh w-[min(20rem,85vw)] bg-surface p-[var(--s-4)] text-ink shadow-lift-2 backdrop:bg-[rgb(27_24_20/0.4)] lg:hidden"
      >
        <div className="mb-[var(--s-2)] flex items-center justify-between">
          <span className="font-display text-title font-semibold">History</span>
          <button
            type="button"
            onClick={() => drawer.current?.close()}
            className="grid size-9 place-items-center rounded-[var(--r-sm)] text-ink-2 hover:bg-surface-2"
          >
            <X aria-hidden size={16} strokeWidth={2} />
            <span className="sr-only">Close</span>
          </button>
        </div>
        {column}
      </dialog>
    </div>
  );
}

/** The list itself, grouped the way a person remembers when they asked: today, yesterday, … */
function Past({
  rows,
  unavailable,
  current,
  problem,
  onOpen,
  onFresh,
}: {
  rows: ConversationSummary[];
  unavailable: boolean;
  current: string;
  problem: string | null;
  onOpen: (id: string) => void;
  onFresh: () => void;
}) {
  return (
    <div className="flex h-full flex-col">
      <button
        type="button"
        onClick={onFresh}
        className="hidden items-center gap-[var(--s-2)] self-start rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-2)] text-caption font-semibold transition-transform duration-[var(--dur-press)] active:scale-[0.97] lg:inline-flex"
      >
        <SquarePen aria-hidden size={15} strokeWidth={2} />
        New conversation
      </button>

      <div className="min-h-0 flex-1 overflow-y-auto lg:mt-[var(--s-5)] lg:pr-[var(--s-2)]">
        {problem ? (
          <p role="alert" className="mb-[var(--s-3)] text-caption text-crit">
            {problem}
          </p>
        ) : null}
        {unavailable ? (
          <p className="text-caption text-ink-3">
            Past conversations are not available while Parrot cannot reach its database.
          </p>
        ) : rows.length === 0 ? (
          <p className="text-caption text-ink-3">
            Questions you ask are kept here, on this computer, so you can come back to them.
          </p>
        ) : (
          groups(rows).map(([label, members]) => (
            <section key={label} className="mb-[var(--s-5)]">
              <h2 className="group-label px-[var(--s-2)]">{label}</h2>
              <ul className="mt-[var(--s-2)] space-y-[2px]">
                {members.map((row) => {
                  const on = row.id === current;
                  return (
                    <li key={row.id}>
                      <button
                        type="button"
                        onClick={() => onOpen(row.id)}
                        aria-current={on ? "true" : undefined}
                        title={row.title}
                        className={[
                          "block w-full truncate rounded-[var(--r-sm)] px-[var(--s-2)] py-[var(--s-2)] text-left text-caption",
                          on
                            ? "bg-brand-soft font-semibold text-brand-strong"
                            : "text-ink-2 hover:bg-surface-2 hover:text-ink",
                        ].join(" ")}
                      >
                        {row.title}
                      </button>
                    </li>
                  );
                })}
              </ul>
            </section>
          ))
        )}
      </div>
    </div>
  );
}

function groups(rows: ConversationSummary[]): [string, ConversationSummary[]][] {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
  const day = 24 * 60 * 60 * 1000;
  const labelled = new Map<string, ConversationSummary[]>();
  for (const row of rows) {
    const at = new Date(row.updated_at).getTime();
    const label =
      at >= today
        ? "Today"
        : at >= today - day
          ? "Yesterday"
          : at >= today - 7 * day
            ? "Previous 7 days"
            : "Earlier";
    labelled.set(label, [...(labelled.get(label) ?? []), row]);
  }
  return [...labelled];
}
