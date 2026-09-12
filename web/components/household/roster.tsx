"use client";

import { useState } from "react";
import type { Person } from "@/lib/api";

/**
 * Everybody Parrot has found, and the one control that matters: which of them is you.
 *
 * The owner is a row, not a value baked in at install. Households are handed over — a daughter
 * takes over her father's paperwork — and an install that cannot follow that is an install that
 * gets abandoned rather than corrected. So "This is me" is available on every person here, and
 * pressing it moves the household rather than editing a setting.
 *
 * The aliases are shown rather than hidden behind an edit screen, because they are the thing
 * that makes an answer right or wrong and a person can only spot a bad one by reading it. When
 * "my premium" returns somebody else's policy, this list is the explanation.
 */

const RELATION_WORD: Record<Person["relation"], string> = {
  self: "you",
  partner: "partner",
  child: "child",
  parent: "parent",
  other: "household",
};

export function Roster({ people }: { people: Person[] }) {
  const [busy, setBusy] = useState<number | null>(null);
  const [failed, setFailed] = useState<string | null>(null);

  const household = people.filter((person) => !person.external);
  const outside = people.filter((person) => person.external);

  async function handOver(personId: number) {
    setBusy(personId);
    setFailed(null);
    const response = await fetch(`/api/parrot/household/owner/${personId}`, {
      method: "PUT",
      headers: { "content-type": "application/json" },
    }).catch(() => null);
    if (!response?.ok) {
      const detail = (await response?.json().catch(() => null)) as { detail?: string } | null;
      setFailed(detail?.detail ?? "Parrot did not save that.");
      setBusy(null);
      return;
    }
    window.location.reload();
  }

  return (
    <>
      <section className="mt-[var(--s-6)]">
        <h2 className="group-label">In this household</h2>
        <ul className="mt-[var(--s-3)] space-y-[var(--s-2)]">
          {household.map((person) => (
            <li
              key={person.id}
              className="flex flex-wrap items-center gap-[var(--s-4)] rounded-[var(--r)] border border-hairline bg-surface px-[var(--s-4)] py-[var(--s-3)]"
            >
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-baseline gap-[var(--s-2)]">
                  <h3 className="font-display text-title font-semibold">{person.display_name}</h3>
                  {person.is_owner ? (
                    <span className="rounded-[var(--r-sm)] bg-brand-soft px-[var(--s-2)] py-[2px] font-display text-label font-semibold tracking-[var(--tr-label)] text-brand-strong uppercase">
                      You
                    </span>
                  ) : (
                    <span className="text-meta text-ink-3">{RELATION_WORD[person.relation]}</span>
                  )}
                </div>
                {/* The names their documents print. The reason an answer is right or wrong. */}
                {person.aliases.length > 0 ? (
                  <p className="mt-[2px] text-meta text-ink-2">
                    on documents as{" "}
                    {person.aliases.map((alias, index) => (
                      <span key={alias}>
                        {index > 0 ? ", " : ""}
                        <span className="font-medium text-ink">{alias}</span>
                      </span>
                    ))}
                  </p>
                ) : (
                  <p className="mt-[2px] text-meta text-ink-3">
                    No document has named them yet.
                  </p>
                )}
              </div>

              {person.is_owner ? null : (
                <button
                  type="button"
                  disabled={busy !== null}
                  onClick={() => handOver(person.id)}
                  title="Hand the household over. Parrot will answer 'my' questions as them."
                  className="shrink-0 rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-2)] text-meta font-medium transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-60"
                >
                  {busy === person.id ? "Switching…" : "This is me"}
                </button>
              )}
            </li>
          ))}
        </ul>
        {failed ? (
          <p role="alert" className="mt-[var(--s-2)] text-meta text-crit">
            {failed}
          </p>
        ) : null}
      </section>

      {outside.length > 0 ? (
        <section className="mt-[var(--s-6)]">
          <h2 className="group-label">Not part of this household</h2>
          {/* Kept rather than discarded, so their documents stop raising the same question
              every time one is filed. */}
          <p className="mt-[var(--s-2)] max-w-[var(--measure)] text-meta text-ink-3">
            Names on your documents that are not people who live here — a landlord, an employer,
            an insurer&rsquo;s officer. Parrot remembers them so it stops asking.
          </p>
          <ul className="mt-[var(--s-3)] flex flex-wrap gap-[var(--s-2)]">
            {outside.map((person) => (
              <li
                key={person.id}
                className="rounded-[var(--r-sm)] border border-hairline px-[var(--s-3)] py-[var(--s-2)] text-meta text-ink-2"
              >
                {person.display_name}
              </li>
            ))}
          </ul>
        </section>
      ) : null}
    </>
  );
}
