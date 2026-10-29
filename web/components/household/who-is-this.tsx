"use client";

import { useState } from "react";
import type { PendingName, Person, Relation } from "@/lib/api";

/**
 * A name off a document that nobody has placed yet.
 *
 * This is the mechanism that replaces a setup form. Parrot reads the names off your documents,
 * the generator proposes what each one is, and this row asks. Until somebody answers, the name
 * scopes nothing — `resolve` and `owner_aliases` read confirmed aliases only — so a wrong guess
 * costs a tap, never a wrong answer. That is the whole reason the model is allowed to guess.
 *
 * Four answers: it is me, it is somebody already here, it is somebody new in this house — and
 * then how they are related — or it is not one of us. The model's suggestion pre-selects one of
 * them rather than deciding it.
 *
 * **The person the model created is not offered as a name.** When the generator decides a name
 * is a new household member it creates a person row for it, called by that same name and with
 * no confirmed alias. Offering that row as a button put "Lim Ah Kow" beside the question "Who is
 * Lim Ah Kow?", and pressing it answered "Lim Ah Kow is Lim Ah Kow" with no way to say he is the
 * owner's father (13 September 2026). That row is what "someone new in this house" places.
 *
 * The row is deliberately the same shape as the quarantine row it sits beside on Today. Both
 * are "a thing Parrot could not settle on its own"; teaching that shape once is the point.
 */

type Place = Exclude<Relation, "self">;

const PLACES: { relation: Place; label: string; said: string }[] = [
  { relation: "parent", label: "My parent", said: "is your parent." },
  { relation: "partner", label: "My partner", said: "is your partner." },
  { relation: "child", label: "My child", said: "is your child." },
  { relation: "other", label: "Someone else who lives here", said: "lives in your household." },
];

const choice =
  "rounded-[var(--r-sm)] border px-[var(--s-3)] py-[var(--s-2)] text-caption font-semibold transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-60";
const suggested = "border-brand-line bg-brand-soft text-brand-strong";

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
  const [placing, setPlacing] = useState(false);
  const [gone, setGone] = useState<string | null>(null);
  const [failed, setFailed] = useState<string | null>(null);

  const owner = people.find((person) => person.is_owner);
  // A person with no confirmed name is a proposal the model made, not somebody anyone has met.
  const proposed = people.find((person) => person.id === name.suggested_person_id);
  const created = proposed && !proposed.is_owner && proposed.aliases.length === 0 ? proposed : undefined;
  const others = people.filter(
    (person) => !person.is_owner && !person.external && person.aliases.length > 0,
  );
  const suggestedPlace: Place | null =
    created && !created.external && created.relation !== "self" ? created.relation : null;

  async function answer(body: Record<string, unknown> | null, said: string) {
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
    setGone(said);
  }

  function somebodyNew(relation: Place, said: string) {
    return answer(
      created
        ? { person_id: created.id, relation }
        : { display_name: name.alias, relation },
      said,
    );
  }

  function notOneOfUs() {
    return answer(
      created
        ? { person_id: created.id, relation: "other", external: true }
        : { display_name: name.alias, relation: "other", external: true },
      "is not part of your household. Parrot will stop asking.",
    );
  }

  if (gone !== null) {
    return (
      <li className="px-[var(--s-4)] py-[var(--s-3)] text-caption text-ink-2">
        <span className="font-semibold text-ink">{name.alias}</span> {gone}
      </li>
    );
  }

  return (
    <li
      className="px-[var(--s-4)] py-[var(--s-3)]"
      style={{
        animation: "parrot-rise var(--dur-enter) var(--ease) both",
        animationDelay: `${index * 50}ms`,
      }}
    >
      <div className="flex items-start gap-[var(--s-4)]">
        <div className="min-w-0 flex-1">
          <h3 className="font-display text-body font-semibold">
            {placing ? (
              <>
                How is <span className="text-brand-strong">{name.alias}</span> related to you?
              </>
            ) : (
              <>
                Who is <span className="text-brand-strong">{name.alias}</span>?
              </>
            )}
          </h3>
          <p className="mt-[2px] text-caption text-ink-2">
            {placing
              ? "This decides which of your packs apply to their documents: parent relief needs a parent."
              : `${
                  name.document_name
                    ? `That name is on ${name.document_name}. `
                    : "That name is on a document you filed. "
                }Parrot will not answer “my” questions with their documents until you say.`}
          </p>

          {placing ? (
            <div className="mt-[var(--s-3)] flex flex-wrap items-center gap-[var(--s-2)]">
              {PLACES.map((place) => (
                <button
                  key={place.relation}
                  type="button"
                  disabled={busy}
                  onClick={() => somebodyNew(place.relation, place.said)}
                  className={[choice, place.relation === suggestedPlace ? suggested : "border-edge"].join(" ")}
                >
                  {place.label}
                </button>
              ))}
              <button
                type="button"
                disabled={busy}
                onClick={() => setPlacing(false)}
                className="ml-auto rounded-[var(--r-sm)] px-[var(--s-2)] py-[var(--s-2)] text-caption text-ink-3 transition-colors hover:text-ink disabled:opacity-60"
              >
                Back
              </button>
            </div>
          ) : (
            <div className="mt-[var(--s-3)] flex flex-wrap items-center gap-[var(--s-2)]">
              {owner ? (
                <button
                  type="button"
                  disabled={busy}
                  onClick={() => answer({ person_id: owner.id }, "is you.")}
                  className={[choice, "border-edge"].join(" ")}
                >
                  That&rsquo;s me
                </button>
              ) : null}

              {others.map((person) => (
                <button
                  key={person.id}
                  type="button"
                  disabled={busy}
                  onClick={() =>
                    answer({ person_id: person.id }, `is ${person.display_name}, already in your household.`)
                  }
                  // The model's suggestion is offered first, not chosen. It is a pre-selected
                  // answer, and the word for that is "suggestion".
                  className={[choice, person.id === name.suggested_person_id ? suggested : "border-edge"].join(" ")}
                >
                  {person.display_name}
                </button>
              ))}

              <button
                type="button"
                disabled={busy}
                onClick={() => setPlacing(true)}
                className={[choice, suggestedPlace ? suggested : "border-edge"].join(" ")}
              >
                Someone new in this house
              </button>

              <button
                type="button"
                disabled={busy}
                onClick={notOneOfUs}
                title="A landlord, an employer, an insurer's officer. Not part of this household"
                className={[
                  "rounded-[var(--r-sm)] px-[var(--s-3)] py-[var(--s-2)] text-caption font-semibold transition-colors hover:bg-surface-2 hover:text-ink disabled:opacity-60",
                  created?.external ? "text-brand-strong" : "text-ink-2",
                ].join(" ")}
              >
                Not one of us
              </button>

              <button
                type="button"
                disabled={busy}
                onClick={() => answer(null, "set aside. Parrot will ask again next time it sees the name.")}
                className="ml-auto rounded-[var(--r-sm)] px-[var(--s-2)] py-[var(--s-2)] text-caption text-ink-3 transition-colors hover:text-ink disabled:opacity-60"
              >
                Ask me later
              </button>
            </div>
          )}

          {failed ? (
            <p role="alert" className="mt-[var(--s-2)] text-caption text-crit">
              {failed}
            </p>
          ) : null}
        </div>
      </div>
    </li>
  );
}
