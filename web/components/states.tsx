import { Check, CircleSlash, Database, PlugZap, Shuffle } from "lucide-react";
import type { Problem } from "@/lib/api";

/**
 * The states that get skipped are the states people hit on their first day.
 *
 * Three kinds of wrong, and each one says something different because "something went wrong" is
 * not a sentence anybody can act on. The distinction is worth the code: a person whose Postgres
 * is down and a person who never started Parrot need opposite next steps, and guessing wrong
 * costs them the evening.
 *
 * No spinners anywhere in this file, and none anywhere else either — loading takes the shape of
 * what is coming, so the layout does not jump when it lands.
 */

const SHAPES = {
  offline: {
    Icon: PlugZap,
    title: "Parrot is not running on this computer",
    tone: "warn",
  },
  foreign: {
    Icon: Shuffle,
    title: "Another program is using Parrot's port",
    tone: "warn",
  },
  database: {
    Icon: Database,
    title: "Parrot is running, but it cannot reach its database",
    tone: "warn",
  },
  error: {
    Icon: CircleSlash,
    title: "Parrot could not answer that",
    tone: "crit",
  },
} as const;

export function ProblemState({
  problem,
  children,
}: {
  problem: Problem;
  /** What still works despite this, said in the surface's own terms. Optional and usually worth it. */
  children?: React.ReactNode;
}) {
  const { Icon, title, tone } = SHAPES[problem.kind];
  return (
    <div
      className="rounded-[var(--r)] border p-[var(--s-5)]"
      style={{ background: `var(--${tone}-soft)`, borderColor: `var(--${tone}-line)` }}
    >
      <div className="flex items-start gap-[var(--s-3)]">
        <Icon aria-hidden size={20} strokeWidth={1.9} style={{ color: `var(--${tone})` }} />
        <div className="min-w-0">
          <h2 className="text-lead font-medium text-ink">{title}</h2>
          {/* Straight from the API. `core/runtime/db.py` guarantees it never carries a
              connection string, which is the only reason it can be shown to a person at all. */}
          <p className="mt-[var(--s-1)] text-body text-ink-2">{problem.detail}</p>
          {children ? <div className="mt-[var(--s-3)] text-meta text-ink-2">{children}</div> : null}
        </div>
      </div>
    </div>
  );
}

/**
 * Nothing here yet, and why that is fine.
 *
 * An empty state teaches the interface rather than announcing its own emptiness. Filing happens
 * in a watched folder and in Telegram, so the first run says where to put something — the app is
 * for reading, not for filing.
 *
 * `tick` is for the one empty state that is a success: "Nothing needs you today" is the outcome
 * this product is for, and a green mark says so faster than the sentence does. It is off by
 * default, because an empty vault is not an achievement.
 */
export function EmptyState({
  title,
  tick = false,
  children,
}: {
  title: string;
  tick?: boolean;
  children?: React.ReactNode;
}) {
  return (
    <div className="rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-6)]">
      {tick ? (
        <span className="grid size-11 place-items-center rounded-[var(--r-pill)] border border-accent-line bg-accent-soft text-accent">
          <Check aria-hidden size={20} strokeWidth={2.4} />
        </span>
      ) : null}
      <h2 className={`font-display text-screen font-semibold ${tick ? "mt-[var(--s-4)]" : ""}`}>
        {title}
      </h2>
      {children ? (
        <div className="mt-[var(--s-2)] max-w-[46ch] text-body text-ink-2">{children}</div>
      ) : null}
    </div>
  );
}

/** A row-shaped skeleton. Matches what a Today row measures, so nothing shifts when it arrives. */
export function RowSkeleton() {
  return (
    <div className="flex gap-[var(--s-3)] rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-4)]">
      <div className="skeleton h-10 w-[3px] shrink-0" />
      <div className="min-w-0 flex-1 space-y-[var(--s-2)]">
        <div className="skeleton h-4 w-2/5" />
        <div className="skeleton h-3 w-4/5" />
        <div className="skeleton h-5 w-[9rem]" />
      </div>
    </div>
  );
}
