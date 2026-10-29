"use client";

import { Eye, EyeOff } from "lucide-react";
import { useRef, useState } from "react";
import { Wordmark } from "@/components/wordmark";

/**
 * One field. The same field sets the passphrase on a first run and opens it afterwards, and
 * only the words around it change — a person arriving here should not have to work out which of
 * two screens they are on before they can type anything.
 *
 * Everything sits in one vertical group rather than being spread to the corners of the viewport.
 * A lock screen is read in one glance and the parts of it belong together; pinning the note to
 * the bottom of a 900px window puts a sentence that matters half a screen away from the thing
 * it qualifies.
 *
 * That note is not boilerplate and is not negotiable. This locks a screen; it does not encrypt a
 * document. A person who believes otherwise because the interface implied it is worse off than
 * one who was told plainly, and the honest sentence costs two lines.
 */
export function UnlockForm({ configured }: { configured: boolean }) {
  const field = useRef<HTMLInputElement>(null);
  const [visible, setVisible] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const passphrase = new FormData(event.currentTarget).get("passphrase");
    setBusy(true);
    setError(null);

    const response = await fetch("/api/auth", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ passphrase }),
    }).catch(() => null);

    if (response?.ok) {
      // A full navigation, not a client push: the guard reads the cookie on the server and the
      // cookie was only set by the response we are holding.
      window.location.assign("/today");
      return;
    }

    const body = (await response?.json().catch(() => null)) as { error?: string } | null;
    setError(body?.error ?? "Parrot is not responding on this computer.");
    setBusy(false);
    field.current?.focus();
    field.current?.select();
  }

  return (
    <main className="grid min-h-dvh place-items-center px-[var(--gutter)] py-[var(--s-7)]">
      <div className="w-full max-w-[26rem]">
        <Wordmark className="-ml-[var(--s-2)]" />

        <h1 className="mt-[var(--s-5)] font-display text-heading lg:text-page">
          {configured ? "Unlock this computer" : "Choose a passphrase"}
        </h1>

        <p className="mt-[var(--s-3)] text-body text-ink-2">
          {configured
            ? "Your documents, the dates that come off them, and the answers drawn from them are behind this."
            : "It is set once, on this computer. There is no account and no email address. Pick something you will still have in six months. A short sentence works better than a short word."}
        </p>

        {/* `noValidate`: the browser's own constraint bubble is an unstyled tooltip in a font
            nobody chose, and it fires before the server ever sees the value — so the one place
            a person is told they are wrong would be the one place this design does not reach.
            Every message on this screen comes through the line below the field. */}
        <form onSubmit={submit} noValidate className="mt-[var(--s-5)]">
          <label htmlFor="passphrase" className="group-label">
            Passphrase
          </label>

          {/* The focus ring is on this wrapper, via `focus-within`, not on the field —
              the field has `outline-none` on purpose. A composer is one control made of
              several elements, and ringing the whole thing is what a person expects. An
              automated check that looks only at `document.activeElement` reports this as
              a missing ring; it is not, and this note is here so nobody "fixes" it. */}
          <div className="mt-[var(--s-2)] flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] border border-edge bg-surface pr-[var(--s-2)] focus-within:outline-2 focus-within:outline-offset-2 focus-within:outline-focus">
            <input
              ref={field}
              id="passphrase"
              name="passphrase"
              type={visible ? "text" : "password"}
              autoComplete={configured ? "current-password" : "new-password"}
              autoFocus
              disabled={busy}
              aria-invalid={error !== null}
              aria-describedby={error ? "passphrase-error" : undefined}
              className="min-w-0 flex-1 bg-transparent px-[var(--s-3)] py-[var(--s-3)] text-body outline-none"
            />
            <button
              type="button"
              onClick={() => setVisible((on) => !on)}
              aria-pressed={visible}
              className="grid size-8 place-items-center rounded-[var(--r-sm)] text-ink-3 transition-colors hover:text-ink"
            >
              {visible ? <EyeOff aria-hidden size={16} /> : <Eye aria-hidden size={16} />}
              <span className="sr-only">{visible ? "Hide passphrase" : "Show passphrase"}</span>
            </button>
          </div>

          {/* Reserved rather than inserted: the button must not jump down the page when a
              message appears under a field somebody is still looking at. */}
          <p
            id="passphrase-error"
            role="alert"
            className="mt-[var(--s-2)] min-h-[1.4rem] text-caption text-crit"
          >
            {error}
          </p>

          <button
            type="submit"
            disabled={busy}
            className="mt-[var(--s-1)] w-full rounded-[var(--r-sm)] bg-brand px-[var(--s-4)] py-[var(--s-3)] font-display text-body font-semibold text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.99] disabled:opacity-70"
          >
            {busy ? "Checking…" : configured ? "Unlock" : "Set it and open Parrot"}
          </button>
        </form>

        <p className="mt-[var(--s-6)] border-t border-hairline pt-[var(--s-4)] text-caption text-ink-3">
          This locks the screen. It does not encrypt anything: your documents stay in the folder
          you put them in, and anyone who can use this computer can still open them there.
        </p>
      </div>
    </main>
  );
}
