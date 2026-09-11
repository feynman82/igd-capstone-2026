"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

/**
 * The switch that turns a pack or a module off.
 *
 * `role="switch"` rather than a styled checkbox, because that is what it is: a screen reader
 * should say "Insurance Agent, switch, on" and the space bar should work without anyone
 * writing a key handler.
 *
 * It refreshes the server components afterwards rather than only updating itself. Switching a
 * pack off changes what Today says and what Ask can cite, and a screen that agreed with the
 * database only about the row you touched would be the most confusing possible outcome.
 */
export function Toggle({
  kind,
  id,
  enabled,
  label,
}: {
  kind: "packs" | "modules";
  id: string;
  enabled: boolean;
  /** Named for a screen reader: the switch on its own says nothing about what it switches. */
  label: string;
}) {
  const router = useRouter();
  const [on, setOn] = useState(enabled);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function flip() {
    const next = !on;
    setOn(next); // optimistic: a switch that waits for a round trip feels broken
    setBusy(true);
    setError(null);

    const response = await fetch(`/api/parrot/${kind}/${id}`, {
      method: "PATCH",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ enabled: next }),
    }).catch(() => null);

    if (!response?.ok) {
      const body = (await response?.json().catch(() => null)) as { detail?: string } | null;
      setOn(!next);
      setError(body?.detail ?? "Parrot did not save that.");
      setBusy(false);
      return;
    }

    setBusy(false);
    router.refresh();
  }

  return (
    <span className="flex flex-col items-end gap-[var(--s-1)]">
      <button
        type="button"
        role="switch"
        aria-checked={on}
        aria-label={label}
        disabled={busy}
        onClick={flip}
        className={[
          "relative h-6 w-11 shrink-0 rounded-[var(--r-pill)] transition-colors duration-[var(--dur-press)]",
          on ? "bg-accent" : "bg-rule",
        ].join(" ")}
      >
        <span
          aria-hidden
          className={[
            "absolute top-[3px] size-[18px] rounded-[var(--r-pill)] bg-surface shadow-lift-1",
            "transition-[left] duration-[var(--dur-press)] ease-[var(--ease)]",
            on ? "left-[26px]" : "left-[3px]",
          ].join(" ")}
        />
      </button>
      {error ? (
        <span role="alert" className="text-meta text-crit">
          {error}
        </span>
      ) : null}
    </span>
  );
}
