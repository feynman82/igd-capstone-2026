"use client";

import { useState } from "react";
import { SourceChip } from "@/components/source-chip";
import type { ObligationChanged, TodayItem } from "@/lib/api";

/**
 * One thing that needs you.
 *
 * Urgency is encoded twice — in the left stripe and in the countdown — so the list is scannable
 * without being read. That is the design pack's call and it is also the accessibility one: a
 * stripe alone would put the whole meaning in a colour, and the countdown is the same
 * information in words for anyone who does not see the stripe.
 *
 * The stripe is 3px. A thicker coloured border on a list item is the decorative version of this
 * and belongs to a different kind of product.
 */

const TONE = {
  overdue: "crit",
  alert: "warn",
  reminder: "accent",
} as const;

const WORD = {
  overdue: "Overdue",
  alert: "Needs your eyes",
  reminder: "Coming up",
} as const;

export function ItemRow({ item, asOf }: { item: TodayItem; asOf?: string }) {
  // Optimistic, then confirmed. A row that waits for a round trip before collapsing feels
  // broken on a machine that is also running a 4B model.
  const [closed, setClosed] = useState<null | { state: string; speaksAgain: string | null }>(null);
  const [failed, setFailed] = useState<string | null>(null);

  const obligationId = item.id.startsWith("obligation:") ? item.id.slice("obligation:".length) : null;

  async function act(what: "snooze" | "done" | "dismissed") {
    if (obligationId === null) return;
    const previous = closed;
    setClosed({ state: what === "snooze" ? "snoozed" : what, speaksAgain: null });
    setFailed(null);

    // `as_of` goes with the write, not just the read. Without it the screen shows December and
    // the snooze stamps whatever today actually is, so the demonstration and the database
    // disagree about what day it is — which is the one thing a reminder system cannot do.
    const path =
      what === "snooze"
        ? `/api/parrot/obligations/${obligationId}/snooze${asOf ? `?as_of=${asOf}` : ""}`
        : `/api/parrot/obligations/${obligationId}/close`;

    const response = await fetch(path, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: what === "snooze" ? undefined : JSON.stringify({ state: what }),
    }).catch(() => null);

    if (!response?.ok) {
      const body = (await response?.json().catch(() => null)) as { detail?: string } | null;
      setClosed(previous);
      setFailed(body?.detail ?? "Parrot did not save that.");
      return;
    }

    const changed = (await response.json()) as ObligationChanged;
    setClosed({ state: changed.state, speaksAgain: changed.speaks_again });
  }

  if (closed !== null) {
    return (
      <li className="rounded-[var(--r)] border border-hairline bg-surface px-[var(--s-4)] py-[var(--s-3)] text-meta text-ink-2">
        <span className="font-medium text-ink">{sentence(item.label)}</span>{" "}
        {closed.state === "snoozed"
          ? closed.speaksAgain
            ? `snoozed — back on ${longDate(closed.speaksAgain)}.`
            : "snoozed. Parrot will not raise it again before it is due."
          : closed.state === "done"
            ? "marked done."
            : "dismissed — Parrot will not raise it again."}
      </li>
    );
  }

  const tone = TONE[item.kind];

  return (
    <li
      className="overflow-hidden rounded-[var(--r)] border border-hairline bg-surface"
      style={{ animation: "parrot-rise var(--dur-enter) var(--ease) both" }}
    >
      <div className="flex gap-[var(--s-3)] p-[var(--s-4)]">
        <span
          aria-hidden
          className="w-[3px] shrink-0 rounded-[2px]"
          style={{ background: `var(--${tone})` }}
        />

        <div className="min-w-0 flex-1">
          {/* An obligation has a label and a sentence about it; an alert has a metric name and a
              sentence that *starts* with it — "days uncovered is 15, over the 0 limit". Giving
              the alert a heading too would print its subject twice and leave the body reading as
              a fragment, so the sentence is the row and the metric goes in the meta line. */}
          {item.kind === "alert" ? (
            <div className="flex flex-wrap items-baseline gap-x-[var(--s-3)] gap-y-[var(--s-1)]">
              <h3 className="min-w-0 flex-1 text-lead font-medium">{sentence(item.line)}</h3>
              <span className="num shrink-0 text-meta" style={{ color: `var(--${tone})` }}>
                {countdown(item)}
              </span>
            </div>
          ) : (
            <>
              <div className="flex flex-wrap items-baseline gap-x-[var(--s-3)] gap-y-[var(--s-1)]">
                <h3 className="text-lead font-medium">{sentence(item.label)}</h3>
                <span
                  className="num ml-auto shrink-0 text-meta"
                  style={{ color: `var(--${tone})` }}
                >
                  {countdown(item)}
                </span>
              </div>
              {/* The module's own sentence, so the command line and the screen can never
                  disagree about what is due — minus the label, which is the heading above it. */}
              <p className="mt-[var(--s-1)] text-body text-ink-2">{detail(item)}</p>
            </>
          )}

          <div className="mt-[var(--s-3)] flex flex-wrap items-center gap-[var(--s-2)]">
            <span className="sr-only">{WORD[item.kind]}.</span>
            {item.sources.map((source, index) => (
              <SourceChip key={`${source.text}-${index}`} source={source} />
            ))}
            <span className="text-meta text-ink-3">{item.pack_id.replace(/_/g, " ")}</span>

            {/* Two actions, and which two depends on where the date is.
                Snooze means "not until this gets more urgent", so it has nothing to say about
                something already late — there is no tighter window left to wait for. An overdue
                row offers the two answers that are actually true of it: I did it, or this was
                never mine to do. */}
            {obligationId !== null ? (
              <span className="ml-auto flex items-center gap-[var(--s-1)]">
                <button
                  type="button"
                  onClick={() => act(item.kind === "overdue" ? "dismissed" : "snooze")}
                  title={
                    item.kind === "overdue"
                      ? "This reminder should not have existed"
                      : "Quiet until it gets more urgent"
                  }
                  className="rounded-[var(--r-sm)] px-[var(--s-2)] py-[var(--s-1)] text-meta font-medium text-ink-2 transition-colors hover:bg-surface-2 hover:text-ink"
                >
                  {item.kind === "overdue" ? "Not mine" : "Snooze"}
                </button>
                <button
                  type="button"
                  onClick={() => act("done")}
                  className="rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-1)] text-meta font-medium transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
                >
                  Done
                </button>
              </span>
            ) : null}
          </div>

          {failed ? (
            <p role="alert" className="mt-[var(--s-2)] text-meta text-crit">
              {failed}
            </p>
          ) : null}
        </div>
      </div>
    </li>
  );
}

/**
 * The module's sentence with the heading taken off the front.
 *
 * A module writes one line for the command line, where there is no heading, so it repeats the
 * label. On screen the label is already the heading.
 *
 * Stripped **only** when a separator follows the label, which is how a module signals it has
 * prefixed a title rather than started a sentence with one. "policy expiry — Marcus Fernandez:
 * overdue since…" loses its prefix; a line that simply begins with its own subject keeps it and
 * stays a sentence. If a module ever rewords itself this quietly does nothing.
 */
function detail(item: TodayItem): string {
  const line = item.line;
  if (!line.startsWith(item.label)) return line;
  const rest = line.slice(item.label.length);
  if (!/^\s*[:—–-]/.test(rest)) return line;
  return rest.replace(/^[\s:—–-]+/, "") || line;
}

/** A module's key is `days_uncovered`; a person reads "Days uncovered". Casing, not rewording. */
function sentence(label: string): string {
  return label.charAt(0).toUpperCase() + label.slice(1);
}

/**
 * The countdown, in the words a person would use.
 *
 * An alert has no date of its own — it is a threshold that has been crossed — so it says what it
 * is rather than inventing a day.
 */
function countdown(item: TodayItem): string {
  if (item.kind === "alert") return "now";
  if (item.days_left === null) return "";
  if (item.days_left < 0) return `${Math.abs(item.days_left)} days ago`;
  if (item.days_left === 0) return "today";
  if (item.days_left === 1) return "tomorrow";
  return `in ${item.days_left} days`;
}

function longDate(iso: string): string {
  return new Date(`${iso}T00:00:00`).toLocaleDateString("en-SG", {
    day: "numeric",
    month: "long",
  });
}
