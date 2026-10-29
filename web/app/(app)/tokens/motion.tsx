"use client";

import { useState } from "react";

/**
 * The motion specification, running rather than tabulated. Every duration and curve here is
 * read from the theme, so this section is also the test: if a screen's animation feels
 * different from this one, the screen reached past the tokens.
 *
 * The rule underneath all of it, from the design pack: the more often a person sees an
 * interaction, the less it moves. Two of the eight rows below are deliberately zero.
 */

const ROWS = [
  {
    token: "--dur-press",
    ms: "160ms",
    what: "Any button press",
    why: "Confirms the interface heard the press. The one animation always worth it.",
  },
  {
    token: "--dur-chip",
    ms: "180ms",
    what: "A source chip arriving",
    why: "Marks the moment the answer became verifiable. Fires once, after the stream ends — a citation that appears mid-stream and then changes reads as the system changing its story.",
  },
  {
    token: "--dur-collapse",
    ms: "200ms",
    what: "A row snoozed or dismissed",
    why: "A CSS transition, never keyframes, so a fast second dismissal retargets instead of restarting.",
  },
  {
    token: "--dur-panel",
    ms: "220ms",
    what: "The source panel opening",
    why: "transform-origin is set to the chip, so the panel grows out of the thing that was clicked.",
  },
  {
    token: "--dur-enter",
    ms: "300ms",
    what: "Today's rows on load",
    why: "50ms apart. The stagger is what reads as ordering by urgency. Seen once per session.",
  },
  {
    token: "--dur-shimmer",
    ms: "1400ms",
    what: "The skeleton sweep",
    why: "Linear, because constant motion takes linear. Collapses to a flat tint under reduced motion.",
  },
  {
    token: "--dur-none",
    ms: "0ms",
    what: "Switching tabs, Today to Ask",
    why: "Used dozens of times a day. Animation here makes the whole app feel slow.",
  },
  {
    token: "--dur-none",
    ms: "0ms",
    what: "Anything triggered by the keyboard",
    why: "Never animate a keyboard action. It is the fastest way to make a fast app feel sluggish.",
  },
] as const;

export function Motion() {
  const [run, setRun] = useState(0);
  const [openPanel, setOpenPanel] = useState(false);
  const [dismissed, setDismissed] = useState(false);

  return (
    <section
      id="motion"
      className="scroll-mt-[var(--s-8)] border-t border-hairline pt-[var(--s-6)] pb-[var(--s-7)]"
    >
      <div className="mb-[var(--s-5)] max-w-[var(--measure)]">
        <h2 className="text-title font-semibold">Nothing moves without a reason</h2>
        <p className="mt-[var(--s-2)] text-caption text-ink-2">
          One easing curve, seven durations, and two of them are zero. Only transform and opacity
          are animated, so everything runs off the main thread while the ingestion worker is busy.
          Nothing ever enters from <span className="num">scale(0)</span> — it starts at{" "}
          <span className="num">0.96</span>, because nothing in the physical world appears from
          nothing.
        </p>
      </div>

      <div className="grid gap-[var(--s-3)] lg:grid-cols-[1fr_1fr]">
        {/* --------------------------------------------------------------- the live demos */}
        <div className="rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-4)]">
          <div className="flex items-center gap-[var(--s-3)]">
            <span className="group-label">Running</span>
            <button
              type="button"
              onClick={() => {
                setRun((n) => n + 1);
                setOpenPanel(false);
                setDismissed(false);
              }}
              className="ml-auto rounded-[var(--r-sm)] border border-edge bg-surface px-[var(--s-3)] py-[var(--s-1)] text-caption font-semibold transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
            >
              Replay
            </button>
          </div>

          {/* Today's rows, staggered by urgency */}
          <ul key={run} className="mt-[var(--s-3)] space-y-[var(--s-2)]">
            {[
              ["crit", "Motor policy expires", "in 11 days"],
              ["warn", "SRS top-up window closes", "120 days"],
              ["accent", "Aircon servicing, quarterly", "19 Sep"],
            ].map(([tone, label, when], i) => (
              <li
                key={label}
                style={{
                  animation: `parrot-rise var(--dur-enter) var(--ease) both`,
                  animationDelay: `${i * 50}ms`,
                }}
                className="flex items-center gap-[var(--s-3)] overflow-hidden rounded-[var(--r-sm)] bg-surface-2 py-[var(--s-2)] pr-[var(--s-3)]"
              >
                <span
                  className="h-8 w-[3px] shrink-0 rounded-r-[2px]"
                  style={{ background: `var(--${tone})` }}
                />
                <span className="min-w-0 flex-1 truncate text-caption">{label}</span>
                <span className="num shrink-0 text-caption text-ink-3">{when}</span>
              </li>
            ))}
          </ul>

          {/* The chip and the panel it grows out of */}
          <div className="mt-[var(--s-4)] border-t border-hairline pt-[var(--s-4)]">
            <button
              type="button"
              onClick={() => setOpenPanel((v) => !v)}
              style={{ animation: `parrot-chip var(--dur-chip) var(--ease) both`, animationDelay: "260ms" }}
              className="rounded-[var(--r-sm)] border border-accent-line bg-accent-soft px-[var(--s-2)] py-[var(--s-1)] text-caption text-accent transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
              aria-expanded={openPanel}
            >
              GE policy schedule <span className="num">p.2</span>
            </button>
            <div
              hidden={!openPanel}
              style={{ transformOrigin: "top left" }}
              className="mt-[var(--s-2)] animate-[parrot-panel_var(--dur-panel)_var(--ease)_both] rounded-[var(--r)] border border-hairline bg-surface-3 p-[var(--s-3)] shadow-lift-2"
            >
              <div className="group-label">Source, page 2</div>
              <pre className="num mt-[var(--s-2)] overflow-x-auto text-caption text-ink-2">
{`Period of insurance
15 Oct 2026 to 14 Oct 2027

Total payable    479.60`}
              </pre>
            </div>
          </div>

          {/* Dismiss, as a transition rather than a keyframe */}
          <div className="mt-[var(--s-4)] border-t border-hairline pt-[var(--s-4)]">
            <div
              className="overflow-hidden transition-all duration-[var(--dur-collapse)] ease-[var(--ease)]"
              style={{
                height: dismissed ? 0 : 40,
                opacity: dismissed ? 0 : 1,
                transform: dismissed ? "translateX(24px)" : "none",
              }}
            >
              <div className="flex h-10 items-center gap-[var(--s-3)] rounded-[var(--r-sm)] bg-surface-2 px-[var(--s-3)] text-caption">
                <span className="flex-1">Home insurance renewal, NTUC Income</span>
                <button
                  type="button"
                  onClick={() => setDismissed(true)}
                  className="rounded-[var(--r-sm)] px-[var(--s-2)] py-[var(--s-1)] font-semibold text-accent"
                >
                  Snooze
                </button>
              </div>
            </div>
            {dismissed ? (
              <p className="text-caption text-ink-3">
                Snoozed.{" "}
                <button type="button" onClick={() => setDismissed(false)} className="text-accent underline">
                  Undo
                </button>
              </p>
            ) : null}
          </div>

          {/* Skeleton */}
          <div className="mt-[var(--s-4)] border-t border-hairline pt-[var(--s-4)]">
            <div className="group-label">Loading takes the shape of what is coming</div>
            <div className="mt-[var(--s-2)] space-y-[var(--s-2)]">
              <div className="skeleton h-4 w-3/5" />
              <div className="skeleton h-3 w-4/5" />
              <div className="skeleton h-3 w-2/5" />
            </div>
          </div>
        </div>

        {/* ------------------------------------------------------------------- the table */}
        <div className="overflow-hidden rounded-[var(--r)] border border-hairline bg-surface">
          {ROWS.map((row, i) => (
            <div
              key={row.what}
              className={`px-[var(--s-4)] py-[var(--s-3)] ${i ? "border-t border-hairline" : ""}`}
            >
              <div className="flex items-baseline gap-[var(--s-3)]">
                <span className="text-caption font-semibold text-ink">{row.what}</span>
                <span className="num ml-auto shrink-0 text-caption text-ink-3">{row.ms}</span>
              </div>
              <p className="mt-[var(--s-1)] text-caption text-ink-2">{row.why}</p>
            </div>
          ))}
          <div className="border-t border-hairline bg-surface-2 px-[var(--s-4)] py-[var(--s-3)] text-caption text-ink-2">
            Under <span className="num">prefers-reduced-motion: reduce</span> the opacity
            transitions stay and every positional one is removed. Reduced means gentler, not
            absent.
          </div>
        </div>
      </div>
    </section>
  );
}
