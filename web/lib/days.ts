/**
 * Days as the calendar speaks them: "2026-10-17", in the household's own time, never UTC.
 *
 * `new Date("2026-10-17")` is midnight in London, which is the evening before in Singapore —
 * the classic off-by-one a calendar ships with. Every date here is built from its parts instead.
 * The week starts on Monday, as it does on a Singapore wall calendar.
 */

export function iso(day: Date): string {
  const month = String(day.getMonth() + 1).padStart(2, "0");
  return `${day.getFullYear()}-${month}-${String(day.getDate()).padStart(2, "0")}`;
}

export function parseDay(text: string): Date {
  const [year, month, day] = text.split("-").map(Number);
  return new Date(year, month - 1, day);
}

export function addDays(day: Date, count: number): Date {
  return new Date(day.getFullYear(), day.getMonth(), day.getDate() + count);
}

export function startOfWeek(day: Date): Date {
  return addDays(day, -((day.getDay() + 6) % 7));
}

/** The Monday-to-Sunday weeks that hold a month: five or six of them. */
export function monthGrid(month: Date): { start: Date; end: Date } {
  const first = new Date(month.getFullYear(), month.getMonth(), 1);
  const last = new Date(month.getFullYear(), month.getMonth() + 1, 0);
  return { start: startOfWeek(first), end: addDays(startOfWeek(last), 6) };
}

/** "2026-10" for a month's address. */
export function monthKey(day: Date): string {
  return iso(day).slice(0, 7);
}

/** "Thursday 15 October" */
export function longDay(day: Date): string {
  return day.toLocaleDateString("en-SG", { weekday: "long", day: "numeric", month: "long" });
}

/** "Thu 15" */
export function shortDay(day: Date): string {
  return `${day.toLocaleDateString("en-SG", { weekday: "short" })} ${day.getDate()}`;
}

/** "09:30:00" or "09:30" to "9:30 am". */
export function clock(time: string | null): string {
  if (!time) return "";
  const [hours, minutes] = time.split(":").map(Number);
  return `${hours % 12 || 12}:${String(minutes).padStart(2, "0")} ${hours < 12 ? "am" : "pm"}`;
}
