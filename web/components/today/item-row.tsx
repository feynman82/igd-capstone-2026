"use client";

import { useState } from "react";
import { SourceChip } from "@/components/source-chip";
import type { ObligationChanged, TodayItem } from "@/lib/api";

/**
 * One thing that needs you, in one of two sizes.
 *
 * **hero** — the first thing in "Needs you now", and only ever one per screen. The countdown is
 * the figure: a 34px number in the tone of the thing, because the question a person opens this
 * app with is "how bad is it" and the answer is a number of days. Everything else on the card
 * arranges itself around that number. Actions are visible without hovering, because this is the
 * card somebody is going to act on.
 *
 * **compact** — everything after it. Title with its status word, sentence, chips, countdown on
 * the right; a normal day fits one screen. The actions are there but quiet until the row is
 * hovered or tabbed into, so eight rows do not read as sixteen buttons.
 *
 * Both are rows of the section's one card (`.row-list`), not cards of their own. Urgency is said
 * twice — a status word beside the title, and the countdown — so the list is scannable without
 * being read and is complete without colour. It used to be said three times, the third being a
 * coloured stripe down each row's left edge; the word does that job and reads as a word.
 */

const TONE = {
  overdue: "crit",
  alert: "warn",
  reminder: "ink-2",
} as const;

/** The status word's tint. A reminder is neutral: it is coming, not wrong. */
const STATUS = {
  overdue: "bg-crit-soft text-crit",
  alert: "bg-warn-soft text-warn",
  reminder: "bg-surface-2 text-ink-2",
} as const;

const WORD = {
  overdue: "Overdue",
  alert: "Needs your eyes",
  reminder: "Coming up",
} as const;

export function ItemRow({
  item,
  asOf,
  variant = "compact",
  index = 0,
}: {
  item: TodayItem;
  asOf?: string;
  variant?: "hero" | "compact";
  /** Position in the list. Rows enter 50ms apart, hero first. */
  index?: number;
}) {
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
      <li className="px-[var(--s-4)] py-[var(--s-3)] text-caption text-ink-2">
        <span className="font-semibold text-ink">{sentence(item.label)}</span>{" "}
        {closed.state === "snoozed"
          ? closed.speaksAgain
            ? `snoozed until ${longDate(closed.speaksAgain)}.`
            : "snoozed. Parrot will not raise it again before it is due."
          : closed.state === "done"
            ? "marked done."
            : "dismissed. Parrot will not raise it again."}
      </li>
    );
  }

  const tone = TONE[item.kind];
  const enter = {
    animation: "parrot-rise var(--dur-enter) var(--ease) both",
    animationDelay: `${index * 50}ms`,
  } as const;

  const actions =
    obligationId === null ? null : (
      <>
        <button
          type="button"
          onClick={() => act(item.kind === "overdue" ? "dismissed" : "snooze")}
          title={
            item.kind === "overdue"
              ? "This reminder should not have existed"
              : "Quiet until it gets more urgent"
          }
          className="rounded-[var(--r-sm)] px-[var(--s-3)] py-[var(--s-2)] text-caption font-semibold text-ink-2 transition-colors hover:bg-surface-2 hover:text-ink"
        >
          {item.kind === "overdue" ? "Not mine" : "Snooze"}
        </button>
        <button
          type="button"
          onClick={() => act("done")}
          className={
            variant === "hero"
              ? "rounded-[var(--r-sm)] bg-brand px-[var(--s-4)] py-[10px] font-display text-caption font-semibold text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
              : "rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-1)] text-caption font-semibold transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
          }
        >
          {variant === "hero" ? "Mark done" : "Done"}
        </button>
      </>
    );

  const problem = failed ? (
    <p role="alert" className="mt-[var(--s-2)] text-caption text-crit">
      {failed}
    </p>
  ) : null;

  /* ------------------------------------------------------------------------------- hero */

  if (variant === "hero") {
    const { value, unit, word } = figure(item);
    return (
      <li style={enter}>
        <div className="flex flex-col gap-[var(--s-5)] p-[var(--s-5)] sm:flex-row sm:items-start">
          {/* The countdown, as the figure. Not a badge and not a decoration — it is the
              sentence "this is 115 days late" said in the fewest possible glyphs, and it is
              repeated in words below so nothing lives in the number alone. */}
          <div
            className="shrink-0 self-start rounded-[12px] px-[var(--s-5)] py-[var(--s-3)] text-center sm:w-[7rem] sm:px-[var(--s-2)] sm:py-[var(--s-4)]"
            style={{
              background: item.kind === "reminder" ? "var(--surface-2)" : `var(--${tone}-soft)`,
              color: item.kind === "reminder" ? "var(--ink)" : `var(--${tone})`,
            }}
          >
            <p className={`num ${word ? "text-heading" : "text-figure"}`}>{value}</p>
            <p className="group-label mt-[var(--s-1)]" style={{ color: "inherit" }}>
              {unit}
            </p>
          </div>

          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-x-[var(--s-3)] gap-y-[var(--s-1)]">
              <h3 className="font-display text-heading font-semibold">{sentence(item.label)}</h3>
              <span className={`status ${STATUS[item.kind]}`}>{WORD[item.kind]}</span>
            </div>
            <p className="mt-[var(--s-2)] max-w-[var(--measure)] text-body text-ink-2">
              {detail(item)}
            </p>

            <div className="mt-[var(--s-4)] flex flex-wrap items-center gap-[var(--s-2)]">
              {item.sources.map((source, at) => (
                <SourceChip key={`${source.text}-${at}`} source={source} />
              ))}
              <span className="text-caption text-ink-3">{item.pack_id.replace(/_/g, " ")}</span>
              {actions ? (
                <span className="ml-auto flex items-center gap-[var(--s-2)]">{actions}</span>
              ) : null}
            </div>

            {problem}
          </div>
        </div>
      </li>
    );
  }

  /* ---------------------------------------------------------------------------- compact */

  return (
    <li
      className="group flex items-center gap-[var(--s-4)] px-[var(--s-4)] py-[var(--s-3)]"
      style={enter}
    >
      <div className="min-w-0 flex-1">
        {/* An obligation has a label and a sentence about it; an alert has a metric name and a
            sentence that *starts* with it — "days uncovered is 15, over the 0 limit". Giving
            the alert a heading too would print its subject twice and leave the body reading as
            a fragment, so the alert's sentence is the heading and there is no second line. */}
        <div className="flex flex-wrap items-center gap-x-[var(--s-2)] gap-y-[var(--s-1)]">
          <h3 className="font-display text-body font-semibold">
            {sentence(item.kind === "alert" ? item.line : item.label)}
          </h3>
          <span className={`status ${STATUS[item.kind]}`}>{WORD[item.kind]}</span>
        </div>
        {item.kind === "alert" ? null : (
          <p className="mt-[2px] text-caption text-ink-2">{detail(item)}</p>
        )}
        {problem}
      </div>

      <div className="hidden shrink-0 items-center gap-[var(--s-2)] lg:flex">
        {item.sources.map((source, at) => (
          <SourceChip key={`${source.text}-${at}`} source={source} />
        ))}
      </div>

      {actions ? <span className="row-actions flex shrink-0 items-center">{actions}</span> : null}

      <span
        className="num w-[5.5rem] shrink-0 text-right text-caption font-semibold"
        style={{ color: item.kind === "reminder" ? "var(--ink-2)" : `var(--${tone})` }}
      >
        {countdown(item)}
      </span>
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

/**
 * The same countdown split into a number and a unit, for the hero.
 *
 * `word` is set when the value is not a numeral, because "today" at 34px does not fit the tile
 * and does not want to — a word is read, a number is measured, and they take different sizes.
 */
function figure(item: TodayItem): { value: string; unit: string; word: boolean } {
  if (item.kind === "alert") return { value: "now", unit: "needs your eyes", word: true };
  if (item.days_left === null) return { value: "Undated", unit: "no due date", word: true };
  const days = Math.abs(item.days_left);
  if (item.days_left < 0) {
    return { value: String(days), unit: days === 1 ? "day overdue" : "days overdue", word: false };
  }
  if (item.days_left === 0) return { value: "today", unit: "due", word: true };
  return { value: String(days), unit: days === 1 ? "day left" : "days left", word: false };
}

function longDate(iso: string): string {
  return new Date(`${iso}T00:00:00`).toLocaleDateString("en-SG", {
    day: "numeric",
    month: "long",
  });
}
