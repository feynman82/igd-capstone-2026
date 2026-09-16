"use client";

import { CircleCheck, CircleDashed, CircleSlash, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";
import { RowSkeleton } from "@/components/states";
import {
  adviceConsents,
  setAdviceConsent,
  type AdviceConsent,
  type ConsentStatus,
} from "@/lib/api";

/**
 * What the owner has agreed to, per pack that advises, and the way back out (ADR 0016).
 *
 * Agreeing happens in the conversation, at the moment advice is first asked for, because that is
 * when the words mean something. Withdrawing happens here, where a person looks for "what have I
 * signed up to". A withdrawal is appended, never an edit, so the record still shows the yes that
 * came before it.
 *
 * Every status has a word and an icon, not just a colour.
 */

const STATUS: Record<
  ConsentStatus,
  { label: string; Icon: typeof CircleCheck; tone: string }
> = {
  granted: { label: "Agreed", Icon: CircleCheck, tone: "border-ok-line bg-ok-soft text-ink" },
  withdrawn: { label: "Withdrawn", Icon: CircleSlash, tone: "border-hairline bg-surface-2 text-ink-2" },
  none: { label: "Not agreed", Icon: CircleDashed, tone: "border-hairline bg-surface-2 text-ink-2" },
  outdated: { label: "Wording changed", Icon: RefreshCw, tone: "border-warn-line bg-warn-soft text-ink" },
};

type Load =
  | { state: "loading" }
  | { state: "failed"; detail: string }
  | { state: "shown"; items: AdviceConsent[] };

export function AdviceConsentSection() {
  const [load, setLoad] = useState<Load>({ state: "loading" });
  const [busy, setBusy] = useState<string | null>(null);
  const [failed, setFailed] = useState<{ pack: string; detail: string } | null>(null);

  async function fetchConsents() {
    setLoad({ state: "loading" });
    const outcome = await adviceConsents();
    setLoad(
      outcome.ok
        ? { state: "shown", items: outcome.data }
        : { state: "failed", detail: outcome.problem.detail },
    );
  }

  useEffect(() => {
    void fetchConsents();
  }, []);

  async function withdraw(item: AdviceConsent) {
    setBusy(item.pack_id);
    setFailed(null);
    const outcome = await setAdviceConsent({
      pack_id: item.pack_id,
      version: item.version,
      action: "withdrawn",
    });
    setBusy(null);
    if (!outcome.ok) {
      setFailed({ pack: item.pack_id, detail: outcome.problem.detail });
      // The wording moved under this screen: show the current state rather than the stale row.
      if (outcome.stale) void fetchConsents();
      return;
    }
    setLoad((current) =>
      current.state === "shown"
        ? {
            state: "shown",
            items: current.items.map((row) =>
              row.pack_id === outcome.data.pack_id ? outcome.data : row,
            ),
          }
        : current,
    );
  }

  // A household whose switched-on packs do not advise has nothing to agree to.
  if (load.state === "shown" && load.items.length === 0) return null;

  return (
    <section className="mt-[var(--s-6)]" aria-busy={load.state === "loading"}>
      <h2 className="group-label">Advice</h2>
      <p className="mt-[var(--s-2)] max-w-[var(--measure)] text-meta text-ink-3">
        Packs that can advise ask for your agreement first. Your agreement covers the people you
        have confirmed in this household.
      </p>

      {load.state === "loading" ? (
        <div className="mt-[var(--s-3)]">
          <RowSkeleton />
        </div>
      ) : null}

      {load.state === "failed" ? (
        <div className="mt-[var(--s-3)] flex flex-wrap items-center gap-[var(--s-3)] rounded-[var(--r)] border border-crit-line bg-crit-soft px-[var(--s-4)] py-[var(--s-3)]">
          <p role="alert" className="flex-1 text-meta text-ink">
            {load.detail}
          </p>
          <button
            type="button"
            onClick={() => void fetchConsents()}
            className="rounded-[var(--r-sm)] border border-edge bg-surface px-[var(--s-3)] py-[var(--s-2)] text-meta font-medium transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
          >
            Try again
          </button>
        </div>
      ) : null}

      {load.state === "shown" ? (
        <ul className="mt-[var(--s-3)] space-y-[var(--s-2)]">
          {load.items.map((item) => {
            const { label, Icon, tone } = STATUS[item.status];
            return (
              <li
                key={item.pack_id}
                className="rounded-[var(--r)] border border-hairline bg-surface px-[var(--s-4)] py-[var(--s-3)]"
              >
                <div className="flex flex-wrap items-center gap-[var(--s-4)]">
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-baseline gap-[var(--s-2)]">
                      <h3 className="font-display text-title font-semibold">{item.display_name}</h3>
                      <span
                        className={`inline-flex items-center gap-[var(--s-1)] self-center rounded-[var(--r-sm)] border px-[var(--s-2)] py-[2px] text-label font-semibold tracking-[var(--tr-label)] uppercase ${tone}`}
                      >
                        <Icon aria-hidden size={12} strokeWidth={2.4} />
                        {label}
                      </span>
                    </div>
                    <p className="mt-[2px] text-meta text-ink-2">
                      <span className="num">Wording version {item.version}</span>
                      {" · "}
                      {item.status === "granted"
                        ? "Parrot can advise when you ask."
                        : item.status === "outdated"
                          ? "The wording changed since you agreed. Parrot will ask again the next time you ask for advice."
                          : "Advice needs your agreement the first time you ask."}
                    </p>
                  </div>

                  {item.status === "granted" ? (
                    <button
                      type="button"
                      disabled={busy !== null}
                      onClick={() => withdraw(item)}
                      className="shrink-0 rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-2)] text-meta font-medium transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-60"
                    >
                      {busy === item.pack_id ? "Withdrawing…" : "Withdraw"}
                      <span className="sr-only"> agreement to {item.display_name} advice</span>
                    </button>
                  ) : null}
                </div>

                <details className="mt-[var(--s-2)]">
                  <summary className="w-fit cursor-pointer text-meta text-ink-2 hover:text-ink">
                    Read the wording
                  </summary>
                  <p className="mt-[var(--s-2)] max-w-[var(--measure)] whitespace-pre-line text-body text-ink">
                    {item.consent_text}
                  </p>
                  <p className="mt-[var(--s-2)] max-w-[var(--measure)] whitespace-pre-line text-meta text-ink-2">
                    {item.disclaimer}
                  </p>
                </details>

                {failed?.pack === item.pack_id ? (
                  <p role="alert" className="mt-[var(--s-2)] text-meta text-crit">
                    {failed.detail}
                  </p>
                ) : null}
              </li>
            );
          })}
        </ul>
      ) : null}
    </section>
  );
}
