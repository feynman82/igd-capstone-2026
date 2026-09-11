import type { Metadata } from "next";
import Link from "next/link";
import { ItemRow } from "@/components/today/item-row";
import { EmptyState, ProblemState } from "@/components/states";
import { quarantine, today, type TodayItem } from "@/lib/api";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Today · Parrot",
  description: "What needs you, before you ask.",
};

/**
 * The surface Parrot opens on, and the reason it is not a text box.
 *
 * Every AI product opens on an empty prompt, and for these five personas that is precisely
 * wrong: they are time-poor, they do not know what to ask, and the Reminder and Alert modules
 * are proactive. Sarah does not want to ask whether there is a renewal this month. She wants to
 * be told. So chat lives one tab away and this is the front page.
 *
 * **Nothing here is computed.** The ordering, the urgency and the sentence on each row all come
 * from the modules, already sorted, through `/api/today` — so the screen and `scripts/today.py`
 * can never disagree about what is due. The only decision this file makes is where to draw the
 * line between "needs you now" and "coming up", and it is written down below.
 *
 * **Opening this page does not consume a lead window.** `/api/today` is a GET and the handler
 * calls the sweep with `mark=False`; the nightly Celery pass owns `last_notified_at`. A person
 * who refreshes twice has not used up their thirty-day warning.
 */

/**
 * Inside a month is something you act on this week; beyond it is something you are told about.
 * Overdue items and alerts are always urgent — an alert has no date of its own, it is a
 * threshold that has already been crossed.
 */
const URGENT_WITHIN_DAYS = 30;

function isUrgent(item: TodayItem): boolean {
  if (item.kind !== "reminder") return true;
  return item.days_left !== null && item.days_left <= URGENT_WITHIN_DAYS;
}

export default async function TodayPage({
  searchParams,
}: {
  // `?as_of=` moves the whole sweep, not just the heading. It is how the demonstration shows a
  // second lead window opening without anybody editing a database.
  searchParams: Promise<{ as_of?: string }>;
}) {
  const { as_of } = await searchParams;
  const [result, waiting] = await Promise.all([today(as_of), quarantine()]);

  if (!result.ok) {
    return (
      <>
        <Header as_of={as_of ?? null} />
        <ProblemState problem={result.problem}>
          {result.problem.kind === "offline" ? (
            <>
              Start it with <span className="num">make dev</span> in the project folder, then
              reload this page.
            </>
          ) : result.problem.kind === "foreign" ? (
            <>
              Stop whatever is on that port and run <span className="num">make dev</span>, or
              start Parrot elsewhere with{" "}
              <span className="num">uv run python scripts/run_parrot.py --port 8010</span> and set{" "}
              <span className="num">PARROT_API_URL</span> to match.
            </>
          ) : result.problem.kind === "database" ? (
            <>
              Your documents are safe — nothing has been lost. Parrot needs Postgres running
              before it can tell you what is due.
            </>
          ) : null}
        </ProblemState>
      </>
    );
  }

  const items = result.data.items;
  const urgent = items.filter(isUrgent);
  const later = items.filter((item) => !isUrgent(item));
  const needsEyes = waiting.ok ? waiting.data.count : 0;
  const attention = urgent.length + (needsEyes > 0 ? 1 : 0);

  return (
    <>
      <Header as_of={result.data.as_of} />

      <p className="mt-[var(--s-2)] max-w-[var(--measure)] text-lead text-ink-2">
        {summary(attention, later.length)}
      </p>

      {items.length === 0 && needsEyes === 0 ? (
        <div className="mt-[var(--s-6)]">
          <NothingToDo />
        </div>
      ) : null}

      {urgent.length > 0 || needsEyes > 0 ? (
        <Section label="Needs you now">
          {needsEyes > 0 ? <QuarantineRow count={needsEyes} /> : null}
          {urgent.map((item) => (
            <ItemRow key={item.id} item={item} asOf={as_of} />
          ))}
        </Section>
      ) : null}

      {later.length > 0 ? (
        <Section label="Coming up">
          {later.map((item) => (
            <ItemRow key={item.id} item={item} asOf={as_of} />
          ))}
        </Section>
      ) : null}
    </>
  );
}

function Header({ as_of }: { as_of: string | null }) {
  const when = as_of ? new Date(`${as_of}T00:00:00`) : new Date();
  return (
    <h1 className="font-display text-screen lg:text-display">
      {when.toLocaleDateString("en-SG", { weekday: "long", day: "numeric", month: "long" })}
    </h1>
  );
}

/** Said the way a person would say it, and never "0 items". */
function summary(attention: number, later: number): string {
  if (attention === 0 && later === 0) return "Nothing needs you today.";
  if (attention === 0) return "Nothing needs you today. Everything below is further out.";
  const things = attention === 1 ? "One thing needs you" : `${attention} things need you`;
  return later > 0 ? `${things}. Everything else is handled.` : `${things}.`;
}

function Section({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <section className="mt-[var(--s-6)]">
      {/* More space above a group label than below it: the label belongs to what follows. */}
      <h2 className="group-label">{label}</h2>
      <ul className="mt-[var(--s-3)] space-y-[var(--s-2)]">{children}</ul>
    </section>
  );
}

/**
 * The quarantine queue, as one row rather than as its own screen. It is a thing that needs a
 * person, so it belongs with the other things that need a person.
 */
function QuarantineRow({ count }: { count: number }) {
  return (
    <li className="overflow-hidden rounded-[var(--r)] border border-hairline bg-surface">
      <div className="flex gap-[var(--s-3)] p-[var(--s-4)]">
        <span aria-hidden className="w-[3px] shrink-0 rounded-[2px] bg-warn" />
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-baseline gap-x-[var(--s-3)]">
            <h3 className="text-lead font-medium">
              {count === 1 ? "One document could not be read" : `${count} documents could not be read`}
            </h3>
            <span className="num ml-auto shrink-0 text-meta text-warn">now</span>
          </div>
          <p className="mt-[var(--s-1)] text-body text-ink-2">
            Nothing from {count === 1 ? "it" : "them"} has been filed. A minute to confirm.
          </p>
          <Link
            href="/vault?status=quarantined"
            className="mt-[var(--s-3)] inline-block rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-1)] text-meta font-medium no-underline"
          >
            Review
          </Link>
        </div>
      </div>
    </li>
  );
}

/**
 * A success state, and designed as one. "Nothing needs you today" is the outcome this product
 * is for; an empty list with a shrug would read as a failure to load.
 */
function NothingToDo() {
  return (
    <EmptyState title="Nothing needs you today">
      Parrot is watching your inbox folder and will say so here when something is due. Drop a
      document in, or send one to the bot, and it will appear within a minute.
    </EmptyState>
  );
}
