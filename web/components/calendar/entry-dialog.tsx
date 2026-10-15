"use client";

import { Trash2, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import {
  deleteEvent,
  saveEvent,
  type CalendarEventIn,
  type CalendarPerson,
  type Repeat,
} from "@/lib/api";
import { clock, longDay, parseDay } from "@/lib/days";

/**
 * One calendar entry, new or existing, in a dialog over the page.
 *
 * The fields are the ones a household fills in on a paper calendar and no more: what, when, for
 * whom, where, and whether it repeats. An edit is to every date of a repeating entry, and the
 * dialog says so beside the button rather than asking which date was meant (ADR 0020) — a
 * half-edited series is the thing that makes people stop trusting a shared calendar.
 *
 * Native `<input type="date">` and `type="time"`: the browser's own pickers are keyboard- and
 * screen-reader-tested in a way a hand-rolled one would never be, and they cost nothing.
 *
 * Deleting asks once, in the dialog, in words: "Delete every date of Swimming lesson?". There is
 * no undo, so the confirmation names exactly what goes.
 */

export type EntryDraft = CalendarEventIn & { id?: number };

const REPEATS: { value: Repeat; label: string }[] = [
  { value: "never", label: "Does not repeat" },
  { value: "daily", label: "Every day" },
  { value: "weekly", label: "Every week" },
  { value: "monthly", label: "Every month" },
  { value: "yearly", label: "Every year" },
];

export function EntryDialog({
  initial,
  people,
  onClose,
  onSaved,
}: {
  initial: EntryDraft;
  people: CalendarPerson[];
  onClose: () => void;
  /** After a save or a delete, with a sentence saying what happened. */
  onSaved: (message: string) => void;
}) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [entry, setEntry] = useState<EntryDraft>(initial);
  const [allDay, setAllDay] = useState(!initial.start_time);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [confirming, setConfirming] = useState(false);
  const editing = initial.id !== undefined;
  const repeats = (entry.repeat ?? "never") !== "never";

  useEffect(() => {
    dialog.current?.showModal();
  }, []);

  function set<K extends keyof EntryDraft>(key: K, value: EntryDraft[K]) {
    setEntry((current) => ({ ...current, [key]: value }));
  }

  async function save(event: React.FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    const { id, ...fields } = entry;
    const body: CalendarEventIn = {
      ...fields,
      title: fields.title.trim(),
      start_time: allDay ? null : fields.start_time || null,
      end_time: allDay ? null : fields.end_time || null,
      ends_on: fields.ends_on || null,
      repeat_until: repeats ? fields.repeat_until || null : null,
      location: fields.location?.trim() || null,
      notes: fields.notes?.trim() || null,
    };
    const outcome = await saveEvent(body, id);
    setBusy(false);
    if (!outcome.ok) {
      setError(outcome.problem.detail);
      return;
    }
    onSaved(`${editing ? "Saved" : "Added"} ${outcome.data.title}.`);
  }

  async function remove() {
    if (initial.id === undefined) return;
    setBusy(true);
    const outcome = await deleteEvent(initial.id);
    setBusy(false);
    if (!outcome.ok) {
      setError(outcome.problem.detail);
      setConfirming(false);
      return;
    }
    onSaved(`Deleted ${outcome.data.title}.`);
  }

  const label = "text-meta font-medium text-ink-2";
  const input =
    "mt-[var(--s-1)] w-full rounded-[var(--r-sm)] border border-edge bg-surface px-[var(--s-3)] py-[var(--s-2)] text-body text-ink";

  return (
    <dialog
      ref={dialog}
      onClose={onClose}
      onClick={(event) => event.target === dialog.current && dialog.current?.close()}
      aria-labelledby="entry-dialog-title"
      className="m-auto w-[min(34rem,94vw)] rounded-[var(--r)] border border-hairline bg-surface p-0 text-ink shadow-lift-2 backdrop:bg-[rgb(27_24_20/0.5)]"
    >
      <form onSubmit={save}>
        <div className="flex items-center gap-[var(--s-3)] border-b border-hairline px-[var(--s-5)] py-[var(--s-4)]">
          <h2 id="entry-dialog-title" className="font-display text-title font-semibold">
            {editing ? "Edit entry" : "New entry"}
          </h2>
          <button
            type="button"
            onClick={() => dialog.current?.close()}
            className="ml-auto grid size-8 shrink-0 place-items-center rounded-[var(--r-sm)] text-ink-3 transition-colors hover:bg-surface-2 hover:text-ink"
          >
            <X aria-hidden size={16} />
            <span className="sr-only">Close</span>
          </button>
        </div>

        <div className="max-h-[70vh] space-y-[var(--s-4)] overflow-auto px-[var(--s-5)] py-[var(--s-4)]">
          <label className="block">
            <span className={label}>What</span>
            <input
              required
              autoFocus
              maxLength={200}
              value={entry.title}
              onChange={(e) => set("title", e.target.value)}
              placeholder="e.g. Swimming lesson"
              className={input}
            />
          </label>

          <div className="grid grid-cols-1 gap-[var(--s-3)] sm:grid-cols-2">
            <label className="block">
              <span className={label}>Date</span>
              <input
                type="date"
                required
                value={entry.starts_on}
                onChange={(e) => set("starts_on", e.target.value)}
                className={input}
              />
            </label>
            <label className="block">
              <span className={label}>For</span>
              <select
                value={entry.person_id ?? ""}
                onChange={(e) => set("person_id", e.target.value ? Number(e.target.value) : null)}
                className={input}
              >
                <option value="">The whole household</option>
                {people.map((person) => (
                  <option key={person.id} value={person.id}>
                    {person.display_name}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <label className="flex items-center gap-[var(--s-2)] text-body">
            <input
              type="checkbox"
              checked={allDay}
              onChange={(e) => setAllDay(e.target.checked)}
              className="size-4 accent-[var(--brand)]"
            />
            All day
          </label>

          {allDay ? (
            <label className="block">
              <span className={label}>Last day, if it runs over several</span>
              <input
                type="date"
                min={entry.starts_on}
                value={entry.ends_on ?? ""}
                onChange={(e) => set("ends_on", e.target.value || null)}
                className={input}
              />
            </label>
          ) : (
            <div className="grid grid-cols-2 gap-[var(--s-3)]">
              <label className="block">
                <span className={label}>Starts</span>
                <input
                  type="time"
                  required
                  value={entry.start_time?.slice(0, 5) ?? ""}
                  onChange={(e) => set("start_time", e.target.value || null)}
                  className={input}
                />
              </label>
              <label className="block">
                <span className={label}>Ends (optional)</span>
                <input
                  type="time"
                  value={entry.end_time?.slice(0, 5) ?? ""}
                  onChange={(e) => set("end_time", e.target.value || null)}
                  className={input}
                />
              </label>
            </div>
          )}

          <div className="grid grid-cols-1 gap-[var(--s-3)] sm:grid-cols-2">
            <label className="block">
              <span className={label}>Repeats</span>
              <select
                value={entry.repeat ?? "never"}
                onChange={(e) => set("repeat", e.target.value as Repeat)}
                className={input}
              >
                {REPEATS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
            {repeats ? (
              <label className="block">
                <span className={label}>Until (optional)</span>
                <input
                  type="date"
                  min={entry.starts_on}
                  value={entry.repeat_until ?? ""}
                  onChange={(e) => set("repeat_until", e.target.value || null)}
                  className={input}
                />
              </label>
            ) : null}
          </div>

          <label className="block">
            <span className={label}>Where (optional)</span>
            <input
              maxLength={200}
              value={entry.location ?? ""}
              onChange={(e) => set("location", e.target.value)}
              placeholder="e.g. Tampines Polyclinic"
              className={input}
            />
          </label>

          <label className="block">
            <span className={label}>Notes (optional)</span>
            <textarea
              rows={2}
              maxLength={2000}
              value={entry.notes ?? ""}
              onChange={(e) => set("notes", e.target.value)}
              className={input}
            />
          </label>

          {error ? (
            <p role="alert" className="rounded-[var(--r-sm)] border border-crit-line bg-crit-soft px-[var(--s-3)] py-[var(--s-2)] text-meta text-crit">
              {error}
            </p>
          ) : null}
        </div>

        <div className="flex flex-wrap items-center gap-[var(--s-3)] border-t border-hairline px-[var(--s-5)] py-[var(--s-4)]">
          {editing && !confirming ? (
            <button
              type="button"
              onClick={() => setConfirming(true)}
              className="inline-flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] px-[var(--s-3)] py-[var(--s-2)] text-meta font-medium text-crit hover:bg-crit-soft"
            >
              <Trash2 aria-hidden size={15} />
              Delete
            </button>
          ) : null}
          {confirming ? (
            <span className="flex flex-wrap items-center gap-[var(--s-2)] text-meta text-ink-2">
              {repeats ? "Delete every date of" : "Delete"} {initial.title}?
              <button
                type="button"
                disabled={busy}
                onClick={remove}
                className="rounded-[var(--r-sm)] bg-crit px-[var(--s-3)] py-[var(--s-2)] font-medium text-surface"
              >
                Delete
              </button>
              <button
                type="button"
                onClick={() => setConfirming(false)}
                className="rounded-[var(--r-sm)] px-[var(--s-3)] py-[var(--s-2)] text-ink-2 hover:bg-surface-2"
              >
                Keep it
              </button>
            </span>
          ) : null}

          <span className="ml-auto flex items-center gap-[var(--s-3)]">
            {editing && repeats && !confirming ? (
              <span className="hidden text-meta text-ink-3 sm:inline">Changes every date</span>
            ) : null}
            <button
              type="button"
              onClick={() => dialog.current?.close()}
              className="rounded-[var(--r-sm)] border border-edge px-[var(--s-4)] py-[var(--s-2)] text-meta font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={busy || confirming}
              className="rounded-[var(--r-sm)] bg-brand px-[var(--s-4)] py-[var(--s-2)] text-meta font-medium text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-60"
            >
              {busy ? "Saving…" : editing ? "Save" : "Add to calendar"}
            </button>
          </span>
        </div>
      </form>
    </dialog>
  );
}

/** The sentence under a draft or a new entry: when it is, in words. */
export function whenText(entry: Pick<CalendarEventIn, "starts_on" | "start_time" | "end_time">) {
  const day = longDay(parseDay(entry.starts_on));
  if (!entry.start_time) return `${day}, all day`;
  const from = clock(entry.start_time);
  return entry.end_time ? `${day}, ${from} to ${clock(entry.end_time)}` : `${day}, ${from}`;
}
