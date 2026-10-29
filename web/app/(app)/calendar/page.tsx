import type { Metadata } from "next";
import { MonthView } from "@/components/calendar/month-view";
import { PageHeader } from "@/components/page-header";
import { ProblemState } from "@/components/states";
import { calendarRange } from "@/lib/api";
import { iso, monthGrid, monthKey, parseDay } from "@/lib/days";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Calendar · Parrot",
  description: "What the household has on, and the deadlines its documents set.",
};

/**
 * The household's month (ADR 0020).
 *
 * `?d=2026-10-17` opens the month holding that day with the day picked — it is where a calendar
 * chip in Ask and a day on Today's week both lead. `?m=2026-11` opens a month on its first day,
 * or on today when today is in it. With neither, it is this month and today.
 *
 * The range read is the whole grid, Monday before the first to Sunday after the last, so the
 * greyed days either side of the month are filled in too rather than looking empty.
 */
export default async function CalendarPage({
  searchParams,
}: {
  searchParams: Promise<{ d?: string; m?: string }>;
}) {
  const { d, m } = await searchParams;
  const today = iso(new Date());
  const day = d && /^\d{4}-\d{2}-\d{2}$/.test(d) ? d : null;
  const month = day ? day.slice(0, 7) : m && /^\d{4}-\d{2}$/.test(m) ? m : monthKey(new Date());
  const selected = day ?? (today.startsWith(month) ? today : `${month}-01`);
  const { start, end } = monthGrid(parseDay(`${month}-01`));
  const result = await calendarRange(iso(start), iso(end));

  return (
    <>
      <PageHeader
        title="Calendar"
        lead="The household’s own entries, and dates from its documents."
      />
      <div className="mt-[var(--s-5)]">
        {result.ok ? (
          <MonthView data={result.data} month={month} selected={selected} today={today} />
        ) : (
          <ProblemState problem={result.problem}>
            {result.problem.kind === "database"
              ? "Your calendar is safe. Parrot needs Postgres running before it can show it."
              : null}
          </ProblemState>
        )}
      </div>
    </>
  );
}
