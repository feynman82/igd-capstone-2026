import { FileText } from "lucide-react";
import Link from "next/link";
import type { CalendarEntry, CalendarResponse } from "@/lib/api";
import { addDays, clock, iso, parseDay, shortDay } from "@/lib/days";
import { sentenceCase } from "@/lib/utils";

/**
 * The household's next seven days, on the screen Parrot opens on (ADR 0020).
 *
 * Seven days from today rather than Monday to Sunday: on a Saturday the useful week is the one
 * ahead, not the one nearly over. Each day is a link to that day on the Calendar, where the full
 * sentence and the edit are. Here a line is the time and the title and nothing else — this is a
 * glance, read in the time it takes to put on shoes.
 *
 * A deadline is evidence green with a document mark, as everywhere: it came off a page. An empty
 * day says a dash rather than nothing, so a quiet Wednesday reads as quiet and not as broken.
 */
export function Week({ data, from }: { data: CalendarResponse; from: string }) {
  const start = parseDay(from);
  const days = Array.from({ length: 7 }, (_, index) => iso(addDays(start, index)));
  const byDay = new Map<string, CalendarEntry[]>();
  for (const entry of data.entries) {
    byDay.set(entry.on, [...(byDay.get(entry.on) ?? []), entry]);
  }

  return (
    <section className="mt-[var(--s-6)]" aria-labelledby="week-heading">
      <div className="flex items-baseline justify-between gap-[var(--s-4)]">
        <h2 id="week-heading" className="group-label">
          This week
        </h2>
        <Link href={`/calendar?d=${from}`} className="text-meta font-medium text-brand-strong">
          Open calendar
        </Link>
      </div>
      <ol className="mt-[var(--s-3)] grid grid-cols-1 gap-[var(--s-2)] sm:grid-cols-7">
        {days.map((day, index) => {
          const entries = byDay.get(day) ?? [];
          return (
            <li key={day}>
              <Link
                href={`/calendar?d=${day}`}
                className={[
                  "flex h-full gap-[var(--s-3)] rounded-[var(--r)] border bg-surface px-[var(--s-3)] py-[var(--s-2)] no-underline transition-shadow hover:shadow-lift-1 sm:min-h-[8.5rem] sm:flex-col sm:gap-[var(--s-1)]",
                  index === 0 ? "border-brand-line" : "border-hairline",
                ].join(" ")}
              >
                <span
                  className={[
                    "w-[3.5rem] shrink-0 font-display text-meta font-semibold sm:w-auto",
                    index === 0 ? "text-brand-strong" : "text-ink",
                  ].join(" ")}
                >
                  {index === 0 ? "Today" : shortDay(parseDay(day))}
                </span>
                <span className="min-w-0 flex-1 space-y-[var(--s-1)]">
                  {entries.length === 0 ? <span className="text-meta text-ink-3">—</span> : null}
                  {entries.slice(0, 4).map((entry) => (
                    <Line key={entry.id} entry={entry} />
                  ))}
                  {entries.length > 4 ? (
                    <span className="block text-[0.6875rem] text-ink-3">+{entries.length - 4} more</span>
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

function Line({ entry }: { entry: CalendarEntry }) {
  if (entry.kind === "deadline") {
    return (
      <span className="flex items-start gap-[var(--s-1)] text-[0.75rem] leading-[1.35] font-medium text-accent">
        <FileText aria-hidden size={12} className="mt-[2px] shrink-0" />
        <span className="line-clamp-2">{sentenceCase(entry.title)} due</span>
      </span>
    );
  }
  return (
    <span className="block text-[0.75rem] leading-[1.35] text-ink-2">
      {entry.start_time ? <span className="num text-ink-3">{clock(entry.start_time)} </span> : null}
      <span className="line-clamp-2 sm:inline">{entry.title}</span>
    </span>
  );
}
