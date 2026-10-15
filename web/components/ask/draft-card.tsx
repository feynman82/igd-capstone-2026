"use client";

import { CalendarPlus, Check } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { EntryDialog, whenText, type EntryDraft } from "@/components/calendar/entry-dialog";
import {
  calendarRangeInBrowser,
  saveEvent,
  type CalendarPerson,
  type DraftEvent,
} from "@/lib/api";

/**
 * "Add Dad's polyclinic review on Friday at 10am", answered with a card and not with an action.
 *
 * v1 never acts, and a calendar entry Parrot wrote by itself would be acting: so the request is
 * drafted (ADR 0020) and this card is where a person decides. **Add to calendar** saves it as
 * drafted, recorded as `ask` so it can always be told apart from an entry somebody typed.
 * **Change first** opens the same form the Calendar uses, filled in, because a misheard date is
 * the likeliest thing to be wrong and the fix should be one field, not a retyped request.
 * **Not now** leaves nothing behind.
 */
export function DraftCard({ draft }: { draft: Omit<DraftEvent, "kind"> }) {
  const [state, setState] = useState<"open" | "saving" | "added" | "dropped">("open");
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState<{ entry: EntryDraft; people: CalendarPerson[] } | null>(
    null,
  );

  const entry: EntryDraft = {
    title: draft.title,
    starts_on: draft.starts_on,
    start_time: draft.start_time,
    end_time: draft.end_time,
    person_id: draft.person_id,
    location: draft.location || null,
    repeat: "never",
    created_via: "ask",
  };

  async function add() {
    setState("saving");
    setError(null);
    const outcome = await saveEvent(entry);
    if (!outcome.ok) {
      setError(outcome.problem.detail);
      setState("open");
      return;
    }
    setState("added");
  }

  async function change() {
    const known = await calendarRangeInBrowser(draft.starts_on, draft.starts_on);
    setEditing({ entry, people: known.ok ? known.data.people : [] });
  }

  if (state === "added") {
    return (
      <p role="status" className="flex flex-wrap items-center gap-[var(--s-2)] text-body text-ok">
        <Check aria-hidden size={16} />
        Added {draft.title} to the calendar.
        <Link href={`/calendar?d=${draft.starts_on}`} className="font-medium text-brand-strong">
          Open it
        </Link>
      </p>
    );
  }
  if (state === "dropped") {
    return <p className="text-body text-ink-3">Not added. Nothing was saved.</p>;
  }

  return (
    <div className="rounded-[var(--r)] border border-brand-line bg-surface p-[var(--s-4)] shadow-lift-1">
      <p className="flex items-center gap-[var(--s-2)] text-label uppercase text-ink-3">
        <CalendarPlus aria-hidden size={14} />
        Draft calendar entry
      </p>
      <p className="mt-[var(--s-2)] font-display text-title font-semibold">{draft.title}</p>
      <p className="mt-[var(--s-1)] text-body text-ink-2">
        {whenText(draft)}
        {draft.person ? ` · ${draft.person}` : " · the whole household"}
        {draft.location ? ` · ${draft.location}` : ""}
      </p>
      <p className="mt-[var(--s-3)] text-meta text-ink-3">{draft.note}</p>
      {error ? (
        <p role="alert" className="mt-[var(--s-2)] text-meta text-crit">
          {error}
        </p>
      ) : null}
      <div className="mt-[var(--s-4)] flex flex-wrap gap-[var(--s-2)]">
        <button
          type="button"
          disabled={state === "saving"}
          onClick={add}
          className="rounded-[var(--r-sm)] bg-brand px-[var(--s-4)] py-[var(--s-2)] text-meta font-medium text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-60"
        >
          {state === "saving" ? "Adding…" : "Add to calendar"}
        </button>
        <button
          type="button"
          onClick={change}
          className="rounded-[var(--r-sm)] border border-edge px-[var(--s-4)] py-[var(--s-2)] text-meta font-medium"
        >
          Change first
        </button>
        <button
          type="button"
          onClick={() => setState("dropped")}
          className="rounded-[var(--r-sm)] px-[var(--s-3)] py-[var(--s-2)] text-meta text-ink-2 hover:bg-surface-2"
        >
          Not now
        </button>
      </div>
      {editing ? (
        <EntryDialog
          initial={editing.entry}
          people={editing.people}
          onClose={() => setEditing(null)}
          onSaved={() => {
            setEditing(null);
            setState("added");
          }}
        />
      ) : null}
    </div>
  );
}
