import type { Metadata } from "next";
import Link from "next/link";
import { ItemRow } from "@/components/today/item-row";
import { EmptyState, ProblemState } from "@/components/states";
import { OwnerForm } from "@/components/household/owner-form";
import { WhoIsThis } from "@/components/household/who-is-this";
import { Week } from "@/components/today/week";
import { calendarRange, household, quarantine, today, vault, type TodayItem } from "@/lib/api";
import { addDays, iso, parseDay } from "@/lib/days";

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
 *
 * The shape is one hero and a list. The most urgent thing gets a card with the countdown as its
 * figure; everything else is a compact row. Before this, eight equal cards meant a person had to
 * read all eight to find out which one was the problem — the list was sorted and did not look
 * it. A hero says "this one" without asking anybody to compare dates.
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
  // The vault call is for one number — how many documents this is all drawn from — and it is
  // the claim in the footer. `limit=1` because the list itself is not wanted here.
  // The week moves with `as_of` like everything else on this screen (ADR 0020).
  const weekStart = as_of && /^\d{4}-\d{2}-\d{2}$/.test(as_of) ? as_of : iso(new Date());
  const [result, waiting, filed, who, week] = await Promise.all([
    today(as_of),
    quarantine(),
    vault({ limit: "1" }),
    household(),
    calendarRange(weekStart, iso(addDays(parseDay(weekStart), 6))),
  ]);

  // The setup step, and the reason it is here rather than on the unlock screen: the passphrase
  // locks the machine, and this says who you are. They are different questions, an install can
  // be past one and not the other, and asking both on one screen makes the second look like
  // part of signing in.
  if (who.ok && !who.data.configured) {
    return (
      <>
        <Header as_of={as_of ?? null} />
        <div className="mt-[var(--s-6)]">
          <OwnerForm />
        </div>
      </>
    );
  }
  const names = who.ok ? who.data.pending : [];
  const people = who.ok ? who.data.people : [];

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
  // Only a document that can still be read again needs a person. One whose file has left the inbox
  // can only be forgotten, which is a line at the foot of the page, not a thing that needs you.
  const quarantined = waiting.ok ? waiting.data.documents : [];
  const needsEyes = quarantined.filter((document) => document.retryable).length;
  const gone = quarantined.length - needsEyes;
  const attention = urgent.length + (needsEyes > 0 ? 1 : 0);

  // The first urgent thing is the hero, and there is never a second one. If nothing is urgent
  // there is no hero — a "coming up" item promoted to 34px would be telling a person something
  // is wrong when nothing is.
  const [hero, ...rest] = urgent;

  return (
    <>
      <Header as_of={result.data.as_of} />

      <p className="mt-[var(--s-3)] max-w-[var(--measure)] text-lead text-ink-2">
        {summary(attention, later.length)}
      </p>

      {items.length === 0 && needsEyes === 0 ? (
        <div className="mt-[var(--s-6)]">
          <NothingToDo />
        </div>
      ) : null}

      {names.length > 0 ? (
        <Section label={names.length === 1 ? "One name to place" : "Names to place"}>
          {names.map((name, at) => (
            <WhoIsThis key={name.id} name={name} people={people} index={at} />
          ))}
        </Section>
      ) : null}

      {urgent.length > 0 || needsEyes > 0 ? (
        <Section label="Needs you now">
          {hero ? <ItemRow item={hero} asOf={as_of} variant="hero" index={0} /> : null}
          {needsEyes > 0 ? <QuarantineRow count={needsEyes} index={hero ? 1 : 0} /> : null}
          {rest.map((item, at) => (
            <ItemRow
              key={item.id}
              item={item}
              asOf={as_of}
              index={at + (hero ? 1 : 0) + (needsEyes > 0 ? 1 : 0)}
            />
          ))}
        </Section>
      ) : null}

      {/* After what needs you and before what is merely coming: the week is a glance, and a
          failed read of it costs the week only — never the rest of the screen. */}
      {week.ok ? <Week data={week.data} from={weekStart} /> : null}

      {later.length > 0 ? (
        <Section label="Coming up">
          {later.map((item, at) => (
            <ItemRow key={item.id} item={item} asOf={as_of} index={at} />
          ))}
        </Section>
      ) : null}

      {filed.ok ? <Provenance total={filed.data.total} /> : null}
      {gone > 0 ? <GoneNote count={gone} /> : null}
    </>
  );
}

/** Quiet on purpose: nothing here needs doing today, and the Vault is where it is forgotten. */
function GoneNote({ count }: { count: number }) {
  return (
    <p className="mt-[var(--s-2)] text-meta text-ink-3">
      {count === 1
        ? "One document left the inbox before Parrot could read it."
        : `${count} documents left the inbox before Parrot could read them.`}{" "}
      <Link href="/vault?status=quarantined" className="text-ink-2">
        Forget {count === 1 ? "it" : "them"} in the Vault
      </Link>
    </p>
  );
}

function Header({ as_of }: { as_of: string | null }) {
  const when = as_of ? new Date(`${as_of}T00:00:00`) : new Date();
  return (
    <div className="flex flex-wrap items-baseline justify-between gap-[var(--s-4)]">
      <h1 className="font-display text-screen lg:text-display">
        {when.toLocaleDateString("en-SG", { weekday: "long", day: "numeric", month: "long" })}
      </h1>
      {/* Not decoration. It is the answer to "is this stale", which is the first thing anybody
          asks of a screen that claims to know what is due. */}
      <span className="num text-meta text-ink-3">
        checked{" "}
        {new Date().toLocaleTimeString("en-SG", {
          hour: "numeric",
          minute: "2-digit",
          hour12: true,
        })}
      </span>
    </div>
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
 * The footer sentence, and the reason it is on the busiest screen rather than in an about box.
 * It is the product's one promise — nothing here came from the internet, and nothing here went
 * to it — and it is worth repeating under the thing it is a promise about.
 */
function Provenance({ total }: { total: number }) {
  return (
    <p className="mt-[var(--s-6)] border-t border-hairline pt-[var(--s-4)] text-meta text-ink-3">
      Based only on your own documents · <span className="num">{total}</span> on this computer ·
      nothing left it
    </p>
  );
}

/**
 * The quarantine queue, as one row rather than as its own screen. It is a thing that needs a
 * person, so it belongs with the other things that need a person.
 */
function QuarantineRow({ count, index }: { count: number; index: number }) {
  return (
    <li
      className="flex items-center gap-[var(--s-4)] rounded-[var(--r)] border border-hairline bg-surface px-[var(--s-4)] py-[var(--s-3)]"
      style={{
        animation: "parrot-rise var(--dur-enter) var(--ease) both",
        animationDelay: `${index * 50}ms`,
      }}
    >
      <span aria-hidden className="w-[3px] shrink-0 self-stretch rounded-[2px] bg-warn" />
      <div className="min-w-0 flex-1">
        <h3 className="font-display text-title font-semibold">
          {count === 1 ? "One document could not be read" : `${count} documents could not be read`}
        </h3>
        <p className="mt-[2px] text-meta text-ink-2">
          Nothing from {count === 1 ? "it" : "them"} has been filed. A minute to confirm.
        </p>
      </div>
      <Link
        href="/vault?status=quarantined"
        className="shrink-0 rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-2)] text-meta font-medium no-underline"
      >
        Review
      </Link>
    </li>
  );
}

/**
 * A success state, and designed as one. "Nothing needs you today" is the outcome this product
 * is for; an empty list with a shrug would read as a failure to load.
 */
function NothingToDo() {
  return (
    <EmptyState title="You are up to date" tick>
      Parrot is watching your inbox folder and will say so here when something is due. Drop a
      document in, or send one to the bot, and it will appear within a minute.
    </EmptyState>
  );
}
