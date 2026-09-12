"use client";

import { useRef, useState } from "react";

/**
 * The one question setup asks.
 *
 * Not "list your household". A person filling in a roster on their first run is typing names
 * from memory, before a single document is filed, with no feedback about whether what they
 * typed matches what their documents actually say — and the match is the only thing that
 * matters. Everybody else arrives off a document and is confirmed a tap at a time.
 *
 * So: one field. The owner is the one person anybody can name without thinking.
 *
 * The label is "the name on your documents", not "your name", and the difference is the whole
 * point. This string is compared against what the extractor read off a page. Somebody who
 * types "Marcus" when every document says "MARCUS LIM JUN WEI" has told Parrot something true
 * and useless. The hint under the field says so in the words a person would use.
 */
export function OwnerForm({ onDone }: { onDone?: () => void }) {
  const field = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const value = String(new FormData(event.currentTarget).get("name") ?? "").trim();
    if (!value) {
      setError("Type the name as it appears on your documents.");
      field.current?.focus();
      return;
    }
    setBusy(true);
    setError(null);

    const response = await fetch("/api/parrot/household/owner", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ display_name: value }),
    }).catch(() => null);

    if (!response?.ok) {
      const body = (await response?.json().catch(() => null)) as { detail?: string } | null;
      setError(body?.detail ?? "Parrot did not save that.");
      setBusy(false);
      return;
    }
    onDone ? onDone() : window.location.reload();
  }

  return (
    <div className="rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-6)]">
      <h2 className="font-display text-screen font-semibold">Who are you?</h2>
      <p className="mt-[var(--s-2)] max-w-[var(--measure)] text-body text-ink-2">
        Your household&rsquo;s documents will name several people. Parrot needs to know which one
        is you, so that &ldquo;when does <em>my</em> policy renew&rdquo; means yours and not
        somebody else&rsquo;s.
      </p>

      <form onSubmit={submit} noValidate className="mt-[var(--s-5)] max-w-[26rem]">
        <label htmlFor="owner-name" className="group-label">
          The name on your documents
        </label>
        <input
          ref={field}
          id="owner-name"
          name="name"
          autoFocus
          disabled={busy}
          aria-invalid={error !== null}
          aria-describedby="owner-name-hint owner-name-error"
          className="mt-[var(--s-2)] w-full rounded-[var(--r-sm)] border border-edge bg-surface px-[var(--s-3)] py-[var(--s-3)] text-lead"
        />
        {/* The sentence that makes the field work. Without it people type their first name. */}
        <p id="owner-name-hint" className="mt-[var(--s-2)] text-meta text-ink-3">
          As it is printed — full name, the way a payslip or a policy writes it. You can add
          other spellings later, and Parrot will ask about any it finds.
        </p>
        <p id="owner-name-error" role="alert" className="mt-[var(--s-2)] min-h-[1.4rem] text-meta text-crit">
          {error}
        </p>
        <button
          type="submit"
          disabled={busy}
          className="mt-[var(--s-1)] rounded-[var(--r-sm)] bg-brand px-[var(--s-5)] py-[var(--s-3)] font-display text-body font-semibold text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.99] disabled:opacity-70"
        >
          {busy ? "Saving…" : "This is me"}
        </button>
      </form>

      <p className="mt-[var(--s-5)] border-t border-hairline pt-[var(--s-4)] text-meta text-ink-3">
        You can change this at any time, and hand the household to somebody else.
      </p>
    </div>
  );
}
