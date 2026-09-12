"use client";

import { useState } from "react";
import type { PendingName, Person } from "@/lib/api";

/**
 * A name off a document that nobody has placed yet.
 *
 * This is the mechanism that replaces a setup form. Parrot reads the names off your documents,
 * the generator proposes what each one is, and this row asks. Until somebody answers, the name
 * scopes nothing — `resolve` and `owner_aliases` read confirmed aliases only — so a wrong guess
 * costs a tap, never a wrong answer. That is the whole reason the model is allowed to guess.
 *
 * Three answers, and they are the three that exist: it is me, it is somebody in this house, or
 * it is not one of us. The model's suggestion pre-selects one of them rather than deciding it.
 *
 * The row is deliberately the same shape as the quarantine row it sits beside on Today. Both
 * are "a thing Parrot could not settle on its own"; teaching that shape once is the point.
 */
export function WhoIsThis({
  name,
  people,
  index = 0,
}: {
  name: PendingName;
  people: Person[];
  index?: number;
}) {
  const [busy, setBusy] = useState(false);
  const [gone, setGone] = useState<string | null>(null);
  const [failed, setFailed] = useState<string | null>(null);

  const owner = people.find((person) => person.is_owner);
  const others = people.filter((person) => !person.is_owner && !person.external);

  async function answer(body: Record<string, unknown> | null) {
    setBusy(true);
    setFailed(null);
    const response = await fetch(`/api/parrot/household/names/${name.id}`, {
      method: body === null ? "DELETE" : "POST",
      headers: { "content-type": "application/json" },
      body: body === null ? undefined : JSON.stringify(body),
    }).catch(() => null);

    if (!response?.ok) {
      const detail = (await response?.json().catch(() => null)) as { detail?: string } | null;
      setFailed(detail?.detail ?? "Parrot did not save that.");
      setBusy(false);
      return;
    }
    setGone(
      body === null
        ? "set aside."
        : body.person_id === owner?.id
          ? "is you."
          : `is ${body.display_name ?? people.find((p) => p.id === body.person_id)?.display_name}.`,
    );
  }

  if (gone !== null) {
    return (
      <li className="rounded-[var(--r)] border border-hairline bg-surface px-[var(--s-4)] py-[var(--s-3)] text-meta text-ink-2">
        <span className="font-medium text-ink">{name.alias}</span> {gone}
      </li>
    );
  }

  return (
    <li
      className="rounded-[var(--r)] border border-hairline bg-surface px-[var(--s-4)] py-[var(--s-3)]"
      style={{
        animation: "parrot-rise var(--dur-enter) var(--ease) both",
        animationDelay: `${index * 50}ms`,
      }}
    >
      <div className="flex items-start gap-[var(--s-4)]">
        <span aria-hidden className="mt-[3px] w-[3px] shrink-0 self-stretch rounded-[2px] bg-brass" />
        <div className="min-w-0 flex-1">
          <h3 className="font-display text-title font-semibold">
            Who is <span className="text-brand-strong">{name.alias}</span>?
          </h3>
          <p className="mt-[2px] text-meta text-ink-2">
            {name.document_name
              ? `That name is on ${name.document_name}. `
              : "That name is on a document you filed. "}
            Parrot will not answer &ldquo;my&rdquo; questions with their documents until you say.
          </p>

          <div className="mt-[var(--s-3)] flex flex-wrap items-center gap-[var(--s-2)]">
            {owner ? (
              <button
                type="button"
                disabled={busy}
                onClick={() => answer({ person_id: owner.id })}
                className="rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-2)] text-meta font-medium transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-60"
              >
                That&rsquo;s me
              </button>
            ) : null}

            {others.map((person) => (
              <button
                key={person.id}
                type="button"
                disabled={busy}
                onClick={() => answer({ person_id: person.id })}
                className={[
                  "rounded-[var(--r-sm)] border px-[var(--s-3)] py-[var(--s-2)] text-meta font-medium",
                  "transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-60",
                  // The model's suggestion is offered first, not chosen. It is a pre-selected
                  // answer, and the word for that is "suggestion".
                  person.id === name.suggested_person_id
                    ? "border-brand-line bg-brand-soft text-brand-strong"
                    : "border-edge",
                ].join(" ")}
              >
                {person.display_name}
              </button>
            ))}

            <button
              type="button"
              disabled={busy}
              onClick={() =>
                answer({ display_name: name.alias, relation: "other", external: false })
              }
              className="rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-2)] text-meta font-medium transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-60"
            >
              Someone else here
            </button>

            <button
              type="button"
              disabled={busy}
              onClick={() => answer({ display_name: name.alias, external: true })}
              title="A landlord, an employer, an insurer's officer — not part of this household"
              className="rounded-[var(--r-sm)] px-[var(--s-3)] py-[var(--s-2)] text-meta font-medium text-ink-2 transition-colors hover:bg-surface-2 hover:text-ink disabled:opacity-60"
            >
              Not one of us
            </button>

            <button
              type="button"
              disabled={busy}
              onClick={() => answer(null)}
              className="ml-auto rounded-[var(--r-sm)] px-[var(--s-2)] py-[var(--s-2)] text-meta text-ink-3 transition-colors hover:text-ink disabled:opacity-60"
            >
              Ask me later
            </button>
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
