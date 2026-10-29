import { FileText } from "lucide-react";
import Link from "next/link";
import type { CalendarEntry, CalendarResponse } from "@/lib/api";
import { addDays, clock, iso, parseDay, shortDay } from "@/lib/days";
import { sentenceCase } from "@/lib/utils";

/**
 * The household's next seven days, and the first thing Today shows (ADR 0020).
 *
 * It leads the screen because it is the one thing on it that is never empty in a way that
 * matters: a quiet week of documents is still a week with swimming and a polyclinic review in
 * it, and the question a person opens this with at 7am is "what is on" before it is "what is
 * late". What is late follows directly underneath, in its own card.
 *
 * Today is a band across the top of the card, the only tinted part of it and the only one that
 * lists everything with its time. The other six sit under it as columns and are a glance — a
 * time and a title, three at most. Every day is a link to that day on the Calendar, where the
 * full sentence and the edit are.
 *
 * Seven days from today rather than Monday to Sunday: on a Saturday the useful week is the one
 * ahead, not the one nearly over. One card with hairlines between the days rather than seven
 * cards, because a week is one thing and seven boxes read as seven.
 *
 * A deadline is evidence green with a document mark, as everywhere: it came off a page. An empty
 * day says so rather than nothing, so a quiet Wednesday reads as quiet and not as broken.
 */
export function Week({ data, from }: { data: CalendarResponse; from: string }) {
  const start = parseDay(from);
  const days = Array.from({ length: 7 }, (_, index) => iso(addDays(start, index)));
  const byDay = new Map<string, CalendarEntry[]>();
  for (const entry of data.entries) {
    byDay.set(entry.on, [...(byDay.get(entry.on) ?? []), entry]);
  }
  const [first, ...rest] = days;
  const today = byDay.get(first) ?? [];

  return (
    <section
      aria-labelledby="week-heading"
      className="mt-[var(--s-5)] rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-3)] shadow-lift-1 sm:p-[var(--s-4)]"
    >
      <div className="flex flex-wrap items-baseline gap-x-[var(--s-3)] gap-y-[var(--s-1)] px-[var(--s-2)] pt-[var(--s-1)]">
        <h2 id="week-heading" className="font-display text-title font-semibold">
          This week
        </h2>
        <span className="num text-caption text-ink-3">{range(start)}</span>
        <Link
          href={`/calendar?d=${from}`}
          className="ml-auto text-caption font-semibold text-brand-strong"
        >
          Open calendar
        </Link>
      </div>

      <ol className="mt-[var(--s-3)] grid grid-cols-1 sm:grid-cols-6">
        <li className="mb-[var(--s-2)] sm:col-span-6">
          <Link
            href={`/calendar?d=${first}`}
            className="flex flex-col gap-[var(--s-2)] rounded-[var(--r-sm)] bg-brand-soft px-[var(--s-4)] py-[var(--s-3)] no-underline sm:flex-row sm:gap-[var(--s-5)]"
          >
            <span className="flex shrink-0 items-baseline gap-[var(--s-2)] sm:w-[7rem] sm:flex-col sm:gap-0">
              <span className="font-display text-heading font-semibold text-brand-strong">Today</span>
              <span className="num text-caption text-ink-2">{shortDay(start)}</span>
            </span>
            <span className="grid min-w-0 flex-1 content-center gap-x-[var(--s-5)] gap-y-[var(--s-2)] md:grid-cols-2">
              {today.length === 0 ? (
                <span className="text-body text-ink-2">Nothing on today.</span>
              ) : null}
              {today.map((entry) => (
                <Line key={entry.id} entry={entry} large />
              ))}
            </span>
          </Link>
        </li>

        {rest.map((day) => {
          const entries = byDay.get(day) ?? [];
          return (
            <li
              key={day}
              className="border-t border-hairline sm:border-t-0 sm:border-l sm:[&:nth-child(2)]:border-l-0"
            >
              <Link
                href={`/calendar?d=${day}`}
                className="hoverable flex h-full gap-[var(--s-3)] rounded-[var(--r-sm)] px-[var(--s-3)] py-[var(--s-2)] no-underline sm:min-h-[7.5rem] sm:flex-col sm:gap-[var(--s-1)] sm:py-[var(--s-3)]"
              >
                <span className="w-[3.5rem] shrink-0 font-display text-caption font-semibold text-ink sm:w-auto">
                  {shortDay(parseDay(day))}
                </span>
                <span className="min-w-0 flex-1 space-y-[var(--s-1)]">
                  {entries.length === 0 ? <span className="text-caption text-ink-3">Nothing on</span> : null}
                  {entries.slice(0, 3).map((entry) => (
                    <Line key={entry.id} entry={entry} />
                  ))}
                  {entries.length > 3 ? (
                    <span className="block text-caption text-ink-3">+{entries.length - 3} more</span>
                  ) : null}
                </span>
              </Link>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

/** One entry. `large` is today's: body size, with the time in its own column. */
function Line({ entry, large = false }: { entry: CalendarEntry; large?: boolean }) {
  const size = large ? "text-body" : "text-caption";
  if (entry.kind === "deadline") {
    return (
      <span className={`flex items-start gap-[var(--s-1)] font-semibold text-accent ${size}`}>
        <FileText aria-hidden size={large ? 14 : 12} className="mt-[0.2em] shrink-0" />
        <span className="line-clamp-2">{sentenceCase(entry.title)} due</span>
      </span>
    );
  }
  if (large) {
    return (
      <span className="flex gap-[var(--s-3)] text-body">
        <span className="num w-[4.5rem] shrink-0 text-body text-ink-2">
          {entry.start_time ? clock(entry.start_time) : "All day"}
        </span>
        <span className="min-w-0 text-ink">
          {entry.title}
          {entry.person ? <span className="text-ink-2"> · {entry.person}</span> : null}
        </span>
      </span>
    );
  }
  return (
    <span className={`block text-ink-2 ${size}`}>
      {entry.start_time ? <span className="num text-ink-3">{clock(entry.start_time)} </span> : null}
      <span className="line-clamp-2 sm:inline">{entry.title}</span>
    </span>
  );
}

/** "29 Oct to 4 Nov" */
function range(start: Date): string {
  const short = (day: Date) => day.toLocaleDateString("en-SG", { day: "numeric", month: "short" });
  return `${short(start)} to ${short(addDays(start, 6))}`;
}
