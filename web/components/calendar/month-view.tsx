"use client";

import { ChevronLeft, ChevronRight, FileText, Plus } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { EntryDialog, type EntryDraft } from "@/components/calendar/entry-dialog";
import { SourceChip } from "@/components/source-chip";
import type { CalendarEntry, CalendarResponse } from "@/lib/api";
import { addDays, iso, longDay, monthKey, parseDay } from "@/lib/days";
import { sentenceCase } from "@/lib/utils";

/**
 * The month, and the day you picked in it.
 *
 * A grid on its own makes a person squint at five-character titles; a list on its own loses the
 * shape of the month. So both: the day above the grid says what is on, in full sentences, with
 * the actions, and the grid says where the busy days are. Picking a day never navigates — it is the
 * interaction a person repeats most here, and it should cost nothing.
 *
 * Two kinds of line, told apart the way the rest of Parrot tells them apart. A **deadline** came
 * off a document: it is marked in evidence green and carries its source chip, and it cannot be
 * edited here, because the date is the document's. An **event** is the household's own: it is
 * plain ink, and pressing it opens it for editing. Colour never carries that meaning alone — a
 * deadline also says "From your documents".
 */
export function MonthView({
  data,
  month,
  selected: initiallySelected,
  today,
}: {
  data: CalendarResponse;
  /** "2026-10" */
  month: string;
  /** "2026-10-17": the day open below the grid. */
  selected: string;
  /** "2026-10-15" */
  today: string;
}) {
  const router = useRouter();
  const [selected, setSelected] = useState(initiallySelected);
  const [open, setOpen] = useState<EntryDraft | null>(null);
  const [said, setSaid] = useState<string | null>(null);

  const first = parseDay(`${month}-01`);
  const previous = monthKey(new Date(first.getFullYear(), first.getMonth() - 1, 1));
  const next = monthKey(new Date(first.getFullYear(), first.getMonth() + 1, 1));
  const start = parseDay(data.start);
  const days = Array.from(
    { length: Math.round((parseDay(data.end).getTime() - start.getTime()) / 86_400_000) + 1 },
    (_, index) => addDays(start, index),
  );
  const byDay = new Map<string, CalendarEntry[]>();
  for (const entry of data.entries) {
    byDay.set(entry.on, [...(byDay.get(entry.on) ?? []), entry]);
  }
  const chosen = byDay.get(selected) ?? [];

  function edit(entry: CalendarEntry) {
    const event = data.events.find((candidate) => candidate.id === entry.event_id);
    if (!event) return;
    setOpen({
      id: event.id,
      title: event.title,
      starts_on: event.starts_on,
      ends_on: event.ends_on,
      start_time: event.start_time,
      end_time: event.end_time,
      location: event.location,
      notes: event.notes,
      person_id: event.person_id,
      repeat: event.repeat,
      repeat_until: event.repeat_until,
    });
  }

  return (
    <>
      {/* The day first, and today unless another day is picked: what is on is the question a
          calendar is opened to answer, and the month below is how you go looking for another
          day. The same band as Today's week, so the two screens say "today" the same way. */}
      <section
        aria-labelledby="day-heading"
        className="mt-[var(--s-5)] rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-3)] shadow-lift-1 sm:p-[var(--s-4)]"
      >
        <div
          className={[
            "flex flex-wrap items-baseline gap-x-[var(--s-3)] gap-y-[var(--s-1)] rounded-[var(--r-sm)] px-[var(--s-4)] py-[var(--s-3)]",
            selected === today ? "bg-brand-soft" : "bg-surface-2",
          ].join(" ")}
        >
          <h2
            id="day-heading"
            className={`font-display text-heading font-semibold ${selected === today ? "text-brand-strong" : "text-ink"}`}
          >
            {selected === today
              ? "Today"
              : parseDay(selected).toLocaleDateString("en-SG", { weekday: "long" })}
          </h2>
          <span className="num text-caption text-ink-2">
            {parseDay(selected).toLocaleDateString("en-SG", { day: "numeric", month: "long" })}
          </span>
          {selected === today ? null : (
            <button
              type="button"
              onClick={() => setSelected(today)}
              className="ml-auto text-caption font-semibold text-brand-strong"
            >
              Back to today
            </button>
          )}
        </div>
        {chosen.length === 0 ? (
          <p className="px-[var(--s-4)] pt-[var(--s-3)] pb-[var(--s-1)] text-body text-ink-2">
            Nothing on.{" "}
            <button
              type="button"
              onClick={() => setOpen({ title: "", starts_on: selected, repeat: "never" })}
              className="font-semibold text-brand-strong underline underline-offset-2"
            >
              Add something
            </button>
          </p>
        ) : (
          <ul className="mt-[var(--s-1)] divide-y divide-hairline">
            {chosen.map((entry) => (
              <EntryRow key={entry.id} entry={entry} onEdit={() => edit(entry)} />
            ))}
          </ul>
        )}
      </section>

      <div className="mt-[var(--s-6)] flex flex-wrap items-center gap-[var(--s-3)]">
        <h2 className="font-display text-title font-semibold">
          {first.toLocaleDateString("en-SG", { month: "long", year: "numeric" })}
        </h2>
        <nav aria-label="Months" className="flex items-center gap-[var(--s-1)]">
          <Link
            href={`/calendar?m=${previous}`}
            className="grid size-9 place-items-center rounded-[var(--r-sm)] border border-edge text-ink-2 no-underline hover:bg-surface-2"
          >
            <ChevronLeft aria-hidden size={16} />
            <span className="sr-only">Previous month</span>
          </Link>
          <Link
            href={`/calendar?d=${today}`}
            className="rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[7px] text-caption font-semibold text-ink-2 no-underline hover:bg-surface-2"
          >
            Today
          </Link>
          <Link
            href={`/calendar?m=${next}`}
            className="grid size-9 place-items-center rounded-[var(--r-sm)] border border-edge text-ink-2 no-underline hover:bg-surface-2"
          >
            <ChevronRight aria-hidden size={16} />
            <span className="sr-only">Next month</span>
          </Link>
        </nav>
        <button
          type="button"
          onClick={() => setOpen({ title: "", starts_on: selected, repeat: "never" })}
          className="ml-auto inline-flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] bg-brand px-[var(--s-4)] py-[var(--s-2)] text-caption font-semibold text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
        >
          <Plus aria-hidden size={16} />
          New entry
        </button>
      </div>

      {said ? (
        <p role="status" className="mt-[var(--s-3)] text-caption text-ok">
          {said}
        </p>
      ) : null}

      <div className="mt-[var(--s-4)] overflow-hidden rounded-[var(--r)] border border-hairline bg-surface">
        <div className="grid grid-cols-7 border-b border-hairline bg-surface-2" aria-hidden>
          {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((name) => (
            <span key={name} className="px-[var(--s-2)] py-[var(--s-2)] text-caption font-semibold text-ink-3">
              {name}
            </span>
          ))}
        </div>
        <div className="grid grid-cols-7" role="grid" aria-label="Days of the month">
          {days.map((day) => {
            const key = iso(day);
            const entries = byDay.get(key) ?? [];
            const inMonth = monthKey(day) === month;
            const isToday = key === today;
            const isChosen = key === selected;
            return (
              <button
                key={key}
                type="button"
                role="gridcell"
                aria-selected={isChosen}
                aria-label={`${longDay(day)}, ${entries.length === 0 ? "nothing on" : `${entries.length} on`}`}
                onClick={() => setSelected(key)}
                className={[
                  "flex min-h-[3.25rem] flex-col items-stretch gap-[2px] border-b border-r border-hairline p-[var(--s-1)] text-left align-top sm:min-h-[5.5rem] [&:nth-child(7n)]:border-r-0",
                  isChosen ? "bg-brand-soft" : "hover:bg-surface-2",
                  inMonth ? "" : "text-ink-3",
                ].join(" ")}
              >
                <span
                  className={[
                    "num grid size-6 place-items-center self-start rounded-[var(--r-pill)] text-caption",
                    isToday ? "bg-brand font-semibold text-brand-ink" : "",
                  ].join(" ")}
                >
                  {day.getDate()}
                </span>
                {/* On a phone a cell is 50px wide and a title would be three letters: dots say
                    where the busy days are, and the day above the grid says what is on. */}
                {entries.length > 0 ? (
                  <span aria-hidden className="flex flex-wrap gap-[3px] px-[var(--s-1)] sm:hidden">
                    {entries.slice(0, 4).map((entry) => (
                      <span
                        key={entry.id}
                        className={[
                          "size-[6px] rounded-[var(--r-pill)]",
                          entry.kind === "deadline" ? "bg-accent" : "bg-ink-3",
                        ].join(" ")}
                      />
                    ))}
                  </span>
                ) : null}
                {entries.slice(0, 3).map((entry) => (
                  <span
                    key={entry.id}
                    className={[
                      "hidden truncate rounded-[4px] px-[var(--s-1)] text-caption sm:block",
                      entry.kind === "deadline"
                        ? "bg-accent-soft font-semibold text-accent"
                        : inMonth
                          ? "bg-surface-2 text-ink-2"
                          : "text-ink-3",
                    ].join(" ")}
                  >
                    {sentenceCase(entry.title)}
                  </span>
                ))}
                {entries.length > 3 ? (
                  <span className="hidden px-[var(--s-1)] text-caption text-ink-3 sm:block">
                    +{entries.length - 3} more
                  </span>
                ) : null}
              </button>
            );
          })}
        </div>
      </div>


      {open ? (
        <EntryDialog
          initial={open}
          people={data.people}
          onClose={() => setOpen(null)}
          onSaved={(message) => {
            setOpen(null);
            setSaid(message);
            router.refresh();
          }}
        />
      ) : null}
    </>
  );
}

function EntryRow({ entry, onEdit }: { entry: CalendarEntry; onEdit: () => void }) {
  const meta = [entry.person, entry.location].filter(Boolean).join(", ");
  if (entry.kind === "deadline") {
    return (
      <li className="flex flex-col gap-[var(--s-1)] px-[var(--s-4)] py-[var(--s-3)] sm:flex-row sm:flex-wrap sm:items-center sm:gap-[var(--s-4)]">
        <span className="shrink-0 text-caption font-semibold text-accent sm:w-[9.5rem]">
          <FileText aria-hidden size={14} className="mr-[var(--s-1)] inline-block align-[-2px]" />
          Due
        </span>
        <div className="min-w-0 flex-1">
          <p className="font-display text-body font-semibold">{sentenceCase(entry.title)}</p>
          <p className="text-caption text-ink-3">
            {entry.sources.some((source) => source.document_id)
              ? "From your documents"
              : "A fixed date a pack's rules set, not read off a document"}
          </p>
        </div>
        {entry.sources.map((source, at) => (
          <SourceChip key={at} source={source} />
        ))}
      </li>
    );
  }
  return (
    <li>
      <button
        type="button"
        onClick={onEdit}
        className="hoverable flex w-full flex-col gap-[var(--s-1)] rounded-[var(--r-sm)] px-[var(--s-4)] py-[var(--s-3)] text-left sm:flex-row sm:items-center sm:gap-[var(--s-4)]"
      >
        <span className="num shrink-0 text-caption text-ink-2 sm:w-[9.5rem]">{entry.when}</span>
        <span className="w-full min-w-0 flex-1">
          <span className="block truncate font-display text-body font-semibold">{entry.title}</span>
          {meta ? <span className="block truncate text-caption text-ink-3">{meta}</span> : null}
        </span>
        <span className="sr-only">Edit</span>
      </button>
    </li>
  );
}
