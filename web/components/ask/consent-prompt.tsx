"use client";

import { ShieldCheck } from "lucide-react";
import { useRef, useState } from "react";
import { AdviceNote } from "@/components/ask/advice-card";
import { adviceConsents, setAdviceConsent, type ConsentRequiredEvent } from "@/lib/api";

/**
 * Advice was asked for before the owner agreed to it (ADR 0016).
 *
 * The stream that produced this has ended — consent does not resume it. So "I understand and
 * agree" records the grant and then asks the same question again, through the conversation's own
 * `sendMessage`, and the new answer arrives as the next turn.
 *
 * **The yes is to the words on the screen.** The grant carries the version that was shown. If the
 * pack's wording moved in the meantime the API refuses it (409), and this prompt fetches the
 * current wording and shows it instead of quietly agreeing to text nobody read.
 */

type Consent = Omit<ConsentRequiredEvent, "kind">;

type State =
  | { step: "asking" }
  | { step: "saving" }
  | { step: "agreed" }
  | { step: "dismissed" };

export function ConsentPrompt({
  consent,
  busy,
  onConsented,
}: {
  consent: Consent;
  /** Another answer is still arriving. The resend would be dropped, so agreeing waits for it. */
  busy: boolean;
  /** Asks the question that produced this prompt again. */
  onConsented: () => void;
}) {
  const [shown, setShown] = useState({
    version: consent.version,
    consent_text: consent.consent_text,
    disclaimer: consent.disclaimer,
  });
  const [state, setState] = useState<State>({ step: "asking" });
  const [failed, setFailed] = useState<string | null>(null);
  const [changed, setChanged] = useState(false);
  const after = useRef<HTMLParagraphElement>(null);

  async function agree() {
    setState({ step: "saving" });
    setFailed(null);
    const outcome = await setAdviceConsent({
      pack_id: consent.pack_id,
      version: shown.version,
      action: "granted",
    });

    if (outcome.ok) {
      settle("agreed");
      onConsented();
      return;
    }

    if (!outcome.stale) {
      setFailed(outcome.problem.detail);
      setState({ step: "asking" });
      return;
    }

    // The wording moved since this prompt was drawn. Show the current words and ask again.
    const current = await adviceConsents();
    const pack = current.ok ? current.data.find((item) => item.pack_id === consent.pack_id) : null;
    if (!pack) {
      setFailed(current.ok ? outcome.problem.detail : current.problem.detail);
      setState({ step: "asking" });
      return;
    }
    if (pack.status === "granted") {
      // Agreed to the current wording elsewhere in the meantime: nothing left to ask.
      settle("agreed");
      onConsented();
      return;
    }
    setShown({
      version: pack.version,
      consent_text: pack.consent_text,
      disclaimer: pack.disclaimer,
    });
    setChanged(true);
    setState({ step: "asking" });
  }

  function settle(step: "agreed" | "dismissed") {
    setState({ step });
    // The buttons are about to go. Focus follows to the sentence that replaced them rather than
    // falling back to the top of the page.
    requestAnimationFrame(() => after.current?.focus());
  }

  const saving = state.step === "saving";
  const settled = state.step === "agreed" || state.step === "dismissed";

  return (
    <section
      aria-label={`${consent.pack_name}: advice needs your agreement`}
      className="rounded-[var(--r)] border border-brand-line bg-surface p-[var(--s-4)]"
    >
      <div className="flex gap-[var(--s-3)]">
        <span aria-hidden className="w-[3px] shrink-0 self-stretch rounded-[2px] bg-brand" />
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-[var(--s-2)]">
            <ShieldCheck aria-hidden size={16} strokeWidth={2} className="text-brand-strong" />
            <h3 className="text-label font-semibold tracking-[var(--tr-label)] text-brand-strong uppercase">
              {consent.pack_name} advice needs your agreement
            </h3>
          </div>
          {consent.label ? (
            <p className="mt-[var(--s-1)] text-meta text-ink-3">You asked about: {consent.label}</p>
          ) : null}

          {changed ? (
            <p role="status" className="mt-[var(--s-3)] text-body font-medium text-ink">
              This wording changed since it was first shown. Read the current version before you
              answer.
            </p>
          ) : null}

          <p className="mt-[var(--s-3)] whitespace-pre-line text-body text-ink">
            {shown.consent_text}
          </p>
          <p className="num mt-[var(--s-2)] text-meta text-ink-3">Wording version {shown.version}</p>

          <AdviceNote disclaimer={shown.disclaimer} />

          {settled ? (
            <p
              ref={after}
              tabIndex={-1}
              role="status"
              className="mt-[var(--s-4)] text-body text-ink-2"
            >
              {state.step === "agreed"
                ? "You agreed. Parrot is asking your question again."
                : "Not agreed. Parrot will ask again the next time you ask for advice."}
            </p>
          ) : (
            <div className="mt-[var(--s-4)] flex flex-wrap items-center gap-[var(--s-2)]">
              <button
                type="button"
                onClick={agree}
                disabled={saving || busy}
                title={busy ? "Wait for the current answer to finish" : undefined}
                className="rounded-[var(--r-sm)] bg-brand px-[var(--s-4)] py-[var(--s-2)] text-meta font-semibold text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-60"
              >
                {saving ? "Saving…" : "I understand and agree"}
              </button>
              <button
                type="button"
                onClick={() => settle("dismissed")}
                disabled={saving}
                className="rounded-[var(--r-sm)] border border-edge px-[var(--s-4)] py-[var(--s-2)] text-meta font-medium transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-60"
              >
                Not now
              </button>
            </div>
          )}

          {failed ? (
            <p role="alert" className="mt-[var(--s-2)] text-meta text-crit">
              {failed}
            </p>
          ) : null}
        </div>
      </div>
    </section>
  );
}
