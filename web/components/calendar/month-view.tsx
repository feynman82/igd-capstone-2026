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
 * shape of the month. So both: the grid says where the busy days are, and the day below it says
 * what is on, in full sentences, with the actions. Picking a day never navigates — it is the
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
      <div className="flex flex-wrap items-center gap-[var(--s-3)]">
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
            className="rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[7px] text-meta font-medium text-ink-2 no-underline hover:bg-surface-2"
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
          className="ml-auto inline-flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] bg-brand px-[var(--s-4)] py-[var(--s-2)] text-meta font-medium text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
        >
          <Plus aria-hidden size={16} />
          New entry
        </button>
      </div>

      {said ? (
        <p role="status" className="mt-[var(--s-3)] text-meta text-ok">
          {said}
        </p>
      ) : null}

      <div className="mt-[var(--s-4)] overflow-hidden rounded-[var(--r)] border border-hairline bg-surface">
        <div className="grid grid-cols-7 border-b border-hairline bg-surface-2" aria-hidden>
          {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((name) => (
            <span key={name} className="px-[var(--s-2)] py-[var(--s-2)] text-label uppercase text-ink-3">
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
                    "num grid size-6 place-items-center self-start rounded-[var(--r-pill)] text-meta",
                    isToday ? "bg-brand font-semibold text-brand-ink" : "",
                  ].join(" ")}
                >
                  {day.getDate()}
                </span>
                {/* On a phone a cell is 50px wide and a title would be three letters: dots say
                    where the busy days are, and the day below the grid says what is on. */}
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
                      "hidden truncate rounded-[4px] px-[var(--s-1)] text-[0.6875rem] leading-[1.35] sm:block",
                      entry.kind === "deadline"
                        ? "bg-accent-soft font-medium text-accent"
                        : inMonth
                          ? "bg-surface-2 text-ink-2"
                          : "text-ink-3",
                    ].join(" ")}
                  >
                    {sentenceCase(entry.title)}
                  </span>
                ))}
                {entries.length > 3 ? (
                  <span className="hidden px-[var(--s-1)] text-[0.6875rem] text-ink-3 sm:block">
                    +{entries.length - 3} more
                  </span>
                ) : null}
              </button>
            );
          })}
        </div>
      </div>

      <section aria-labelledby="day-heading" className="mt-[var(--s-6)]">
        <h2 id="day-heading" className="group-label">
          {selected === today ? "Today, " : ""}
          {longDay(parseDay(selected))}
        </h2>
        {chosen.length === 0 ? (
          <p className="mt-[var(--s-3)] text-body text-ink-3">
            Nothing on.{" "}
            <button
              type="button"
              onClick={() => setOpen({ title: "", starts_on: selected, repeat: "never" })}
              className="font-medium text-brand-strong underline underline-offset-2"
            >
              Add something
            </button>
          </p>
        ) : (
          <ul className="mt-[var(--s-3)] space-y-[var(--s-2)]">
            {chosen.map((entry) => (
              <EntryRow key={entry.id} entry={entry} onEdit={() => edit(entry)} />
            ))}
          </ul>
        )}
      </section>

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
  const meta = [entry.person, entry.location].filter(Boolean).join(" · ");
  if (entry.kind === "deadline") {
    return (
      <li className="flex flex-wrap items-center gap-[var(--s-3)] rounded-[var(--r)] border border-accent-line bg-surface px-[var(--s-4)] py-[var(--s-3)]">
        <FileText aria-hidden size={18} className="shrink-0 text-accent" />
        <div className="min-w-0 flex-1">
          <p className="font-display text-body font-semibold">{sentenceCase(entry.title)}</p>
          <p className="text-meta text-ink-3">
            {entry.sources.some((source) => source.document_id)
              ? "Due · From your documents"
              : "Due · A fixed date a pack's rules set, not read off a document"}
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
        className="flex w-full items-center gap-[var(--s-4)] rounded-[var(--r)] border border-hairline bg-surface px-[var(--s-4)] py-[var(--s-3)] text-left hover:shadow-lift-1"
      >
        <span className="num w-[6.5rem] shrink-0 text-meta text-ink-2">{entry.when}</span>
        <span className="min-w-0 flex-1">
          <span className="block truncate font-display text-body font-semibold">{entry.title}</span>
          {meta ? <span className="block truncate text-meta text-ink-3">{meta}</span> : null}
        </span>
        <span className="sr-only">Edit</span>
      </button>
    </li>
  );
}
