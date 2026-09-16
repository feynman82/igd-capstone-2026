"use client";

import { ArrowDownRight, ArrowUpRight, ClipboardList, Minus, Scale } from "lucide-react";
import Link from "next/link";
import { SourceChip } from "@/components/source-chip";
import type { AdviceCardEvent, AdviceWithheldEvent } from "@/lib/api";

/**
 * Advice, as code worked it out (ADR 0016).
 *
 * Every word and number on the card came from the event: the verdict sentence was written by a
 * calculator, the figures were printed by it, and the inputs are the facts and published rules
 * it read. This file adds only generic labels — nothing here knows whether the pack is about
 * insurance or tax, and nothing here may, because a domain word written into a component is a
 * word no pack author can correct.
 *
 * Distinct from an explained answer (it is a bordered card, not a run of sentences) and from the
 * abstention and decline cards (evergreen, not brass or grey), because a person must be able to
 * tell at a glance that this is a judgement Parrot is offering, not a line read off a page.
 */

type Advice = Omit<AdviceCardEvent, "kind">;
type Withheld = Omit<AdviceWithheldEvent, "kind">;

/**
 * How a verdict code is marked. Only the mark: the sentence a person reads is `verdict_text`,
 * and every mark has an icon, so no verdict is told apart by colour alone. A code this list does
 * not know is shown neutrally — calculators choose the codes, and a new one must not break here.
 */
const TONES = {
  better: { Icon: ArrowUpRight, bar: "bg-ok", icon: "text-ok" },
  worse: { Icon: ArrowDownRight, bar: "bg-warn", icon: "text-warn" },
  neutral: { Icon: Minus, bar: "bg-rule", icon: "text-ink-3" },
} as const;

const VERDICT_TONE: Record<string, keyof typeof TONES> = {
  meets: "better",
  room_left: "better",
  gains: "better",
  short: "worse",
  no_room: "worse",
  loses: "worse",
};

export function AdviceCard({ advice }: { advice: Advice }) {
  const tone = TONES[VERDICT_TONE[advice.verdict] ?? "neutral"];
  const [header, ...body] = advice.rows;

  return (
    <section
      aria-label={`Advice for ${advice.person ?? "you"}`}
      style={{ animation: "parrot-rise var(--dur-chip) var(--ease) both" }}
      className="rounded-[var(--r)] border border-accent-line bg-surface p-[var(--s-4)]"
    >
      <div className="flex flex-wrap items-center gap-[var(--s-2)]">
        <Scale aria-hidden size={16} strokeWidth={2} className="text-accent" />
        <h3 className="text-label font-semibold tracking-[var(--tr-label)] text-accent uppercase">
          Advice for {advice.person ?? "you"}
        </h3>
        {advice.estimate ? (
          <span className="rounded-[var(--r-sm)] border border-warn-line bg-warn-soft px-[var(--s-2)] py-[2px] text-label font-semibold tracking-[var(--tr-label)] text-ink uppercase">
            Estimate
          </span>
        ) : null}
      </div>
      {advice.label ? (
        <p className="mt-[var(--s-1)] text-meta text-ink-3">{capitalise(advice.label)}</p>
      ) : null}

      <div className="mt-[var(--s-3)] flex gap-[var(--s-3)]">
        <span aria-hidden className={`w-[3px] shrink-0 self-stretch rounded-[2px] ${tone.bar}`} />
        <p className="flex-1 text-lead text-ink">
          <tone.Icon
            aria-hidden
            size={18}
            strokeWidth={2.2}
            className={`mr-[var(--s-1)] inline-block align-[-3px] ${tone.icon}`}
          />
          {advice.verdict_text}
        </p>
      </div>

      {advice.figures.length > 0 ? (
        <table className="mt-[var(--s-4)] w-full border-collapse text-body">
          <caption className="sr-only">Figures</caption>
          <thead className="sr-only">
            <tr>
              <th scope="col">Figure</th>
              <th scope="col">Value</th>
            </tr>
          </thead>
          <tbody>
            {advice.figures.map((figure, index) => (
              <tr key={`${figure.name}-${index}`} className="border-t border-hairline first:border-t-0">
                <th scope="row" className="py-[var(--s-2)] pr-[var(--s-4)] text-left font-normal text-ink-2">
                  {capitalise(figure.name.replace(/_/g, " "))}
                </th>
                <td className="num py-[var(--s-2)] text-right text-ink">{figure.text}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}

      {header && body.length > 0 ? (
        <div
          // Scrolls sideways on a phone rather than squashing the columns. Focusable, so a
          // keyboard can scroll it too.
          tabIndex={0}
          role="region"
          aria-label="Comparison"
          className="mt-[var(--s-4)] overflow-x-auto rounded-[var(--r-sm)] border border-hairline"
        >
          <table className="w-full min-w-max border-collapse text-meta">
            <thead className="bg-surface-2">
              <tr>
                {header.map((cell, index) => (
                  <th
                    key={index}
                    scope="col"
                    className="px-[var(--s-3)] py-[var(--s-2)] text-left font-semibold text-ink-2"
                  >
                    {cell}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {body.map((row, at) => (
                <tr key={at} className="border-t border-hairline">
                  {row.map((cell, index) =>
                    index === 0 ? (
                      <th
                        key={index}
                        scope="row"
                        className="px-[var(--s-3)] py-[var(--s-2)] text-left font-medium text-ink"
                      >
                        {cell}
                      </th>
                    ) : (
                      <td key={index} className="num px-[var(--s-3)] py-[var(--s-2)] text-ink">
                        {cell}
                      </td>
                    ),
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}

      {advice.inputs.length > 0 ? (
        <div className="mt-[var(--s-4)]">
          <h4 className="group-label">Inputs</h4>
          <ul className="mt-[var(--s-2)] flex flex-wrap gap-[var(--s-1)]">
            {advice.inputs.map((source, index) => (
              <li key={index} className="max-w-full">
                <SourceChip source={source} />
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      <AdviceNote disclosure={advice.product_disclosure} disclaimer={advice.disclaimer} />
    </section>
  );
}

/**
 * Advice that could not be worked out, and what it would take.
 *
 * Neutral rather than brass: it is not the vault failing to answer a question, it is Parrot
 * declining to guess a figure it was not given. The list is the pack's own wording for each
 * missing fact or rule, and the vault is where a person goes to add one.
 */
export function AdviceWithheld({ withheld }: { withheld: Withheld }) {
  return (
    <section
      aria-label="Parrot needs more to advise on this"
      className="rounded-[var(--r)] border border-hairline bg-surface-2 p-[var(--s-4)]"
    >
      <div className="flex items-center gap-[var(--s-2)]">
        <ClipboardList aria-hidden size={16} strokeWidth={2} className="text-ink-2" />
        <h3 className="text-label font-semibold tracking-[var(--tr-label)] text-ink-2 uppercase">
          Parrot needs more to advise on this
        </h3>
      </div>
      {withheld.label || withheld.person ? (
        <p className="mt-[var(--s-1)] text-meta text-ink-3">
          {withheld.label ? capitalise(withheld.label) : "Advice"}
          {withheld.person ? ` · for ${withheld.person}` : ""}
        </p>
      ) : null}

      {withheld.missing.length > 0 ? (
        <ul className="mt-[var(--s-3)] list-disc space-y-[var(--s-1)] pl-[var(--s-5)] text-body text-ink">
          {withheld.missing.map((item, index) => (
            <li key={index}>{sentence(item)}</li>
          ))}
        </ul>
      ) : null}

      <p className="mt-[var(--s-3)] text-body text-ink-2">
        Nothing was estimated to fill the gap.{" "}
        <Link href="/vault" className="font-medium text-ink underline underline-offset-2">
          Open your vault
        </Link>{" "}
        to see what is on file, or the{" "}
        <Link href="/household" className="font-medium text-ink underline underline-offset-2">
          Household page
        </Link>{" "}
        to say who is who.
      </p>

      <AdviceNote disclaimer={withheld.disclaimer} />
    </section>
  );
}

/**
 * The disclaimer, and the named-product disclosure when there is one.
 *
 * Always rendered, never collapsed, never behind a toggle: advice without its caveat is a
 * different statement from advice with it, and only the second one was agreed to.
 */
export function AdviceNote({
  disclaimer,
  disclosure = "",
}: {
  disclaimer: string;
  disclosure?: string;
}) {
  return (
    <div
      role="note"
      className="mt-[var(--s-4)] space-y-[var(--s-2)] rounded-[var(--r-sm)] border border-edge bg-surface-2 p-[var(--s-3)] text-meta text-ink-2"
    >
      {disclosure.trim() ? <p className="whitespace-pre-line text-ink">{disclosure}</p> : null}
      <p className="whitespace-pre-line">{disclaimer}</p>
    </div>
  );
}

function capitalise(text: string): string {
  const trimmed = text.trim();
  return trimmed.charAt(0).toUpperCase() + trimmed.slice(1);
}

/** A withheld item arrives lower-case and unpunctuated, in the pack's own words -- read as a
 * sentence on screen, the way `answer.tsx`'s `sentence()` helper reads an abstention's. */
function sentence(text: string): string {
  if (!text) return "";
  const capitalised = capitalise(text);
  return /[.!?]$/.test(capitalised) ? capitalised : `${capitalised}.`;
}
