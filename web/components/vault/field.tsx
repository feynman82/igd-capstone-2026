"use client";

import { Check, Pencil, X } from "lucide-react";
import { useRef, useState } from "react";
import type { CorrectionResponse, VaultFact } from "@/lib/api";

/**
 * One extracted field, and the correction loop.
 *
 * Extraction will be wrong sometimes. Designing for that honestly is what separates a system
 * people keep using from one they abandon after the third bad date — so a field the extractor
 * was unsure of is flagged *before* a person is surprised by it, and fixing it is one click
 * from the place the mistake is visible.
 *
 * Two actions, and the difference between them matters. **Looks right** confirms the value the
 * model read; **Fix** replaces it. Both mark the field checked by a person and both are stored
 * as labelled examples, because "the model was right and a human agreed" is as useful to an
 * evaluation as "the model was wrong and here is the truth". Only one of them is a correction,
 * and `traces` records which.
 */
export function Field({
  fact,
  onPage,
  onCorrected,
  showSubject,
}: {
  fact: VaultFact;
  /** Open the page this field was read off. */
  onPage: (page: number) => void;
  onCorrected: (result: CorrectionResponse) => void;
  /**
   * Whose field this is — shown only when a document is about more than one person.
   * A renewal notice naming Marcus on all six fields does not need his name six times.
   */
  showSubject: boolean;
}) {
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [current, setCurrent] = useState(fact);
  const [was, setWas] = useState<string | number | null>(null);
  const input = useRef<HTMLInputElement>(null);

  async function save(value: string) {
    setBusy(true);
    setError(null);
    const response = await fetch(`/api/parrot/facts/${fact.id}`, {
      method: "PATCH",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ value }),
    }).catch(() => null);

    if (!response?.ok) {
      const body = (await response?.json().catch(() => null)) as { detail?: string } | null;
      // 422 carries the pack's own sentence about what this field is — "not a date. Write it as
      // YYYY-MM-DD". Shown as written rather than replaced with a generic complaint.
      setError(body?.detail ?? "Parrot did not save that.");
      setBusy(false);
      input.current?.focus();
      return;
    }

    const result = (await response.json()) as CorrectionResponse;
    setCurrent({
      ...current,
      value: result.now,
      confidence: 1,
      verified_by_user: true,
      needs_review: false,
    });
    setWas(result.was === result.now ? null : result.was);
    setEditing(false);
    setBusy(false);
    onCorrected(result);
  }

  const flagged = current.needs_review;

  return (
    <div
      className="grid gap-x-[var(--s-3)] border-t border-hairline px-[var(--s-2)] py-[var(--s-2)] sm:grid-cols-[10rem_1fr]"
      style={flagged ? { background: "var(--warn-soft)" } : undefined}
    >
      <dt className="group-label pt-[2px]">{current.key.replace(/_/g, " ")}</dt>

      <dd className="min-w-0">
        {editing ? (
          <form
            onSubmit={(event) => {
              event.preventDefault();
              save(new FormData(event.currentTarget).get("value") as string);
            }}
            className="flex flex-wrap items-center gap-[var(--s-2)]"
          >
            <input
              ref={input}
              name="value"
              defaultValue={String(current.value ?? "")}
              autoFocus
              disabled={busy}
              className="min-w-0 flex-1 rounded-[var(--r-sm)] border border-edge bg-surface px-[var(--s-2)] py-[var(--s-1)] text-body"
            />
            <button
              type="submit"
              disabled={busy}
              className="rounded-[var(--r-sm)] bg-brand px-[var(--s-3)] py-[var(--s-1)] text-meta font-medium text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
            >
              {busy ? "Saving…" : "Save"}
            </button>
            <button
              type="button"
              onClick={() => {
                setEditing(false);
                setError(null);
              }}
              className="grid size-7 place-items-center rounded-[var(--r-sm)] text-ink-3 hover:text-ink"
            >
              <X aria-hidden size={14} />
              <span className="sr-only">Cancel</span>
            </button>
          </form>
        ) : (
          /* A grid, not a wrapping flex: the value may be long and the controls must stay on
             its line rather than dropping below and doubling the height of every row. */
          <div className="grid grid-cols-[1fr_auto] items-baseline gap-[var(--s-3)]">
            <span className="min-w-0">
              <span className={`text-body ${isNumeric(current) ? "num" : ""}`}>
                {format(current)}
              </span>
              {showSubject && current.subject ? (
                <span className="ml-[var(--s-2)] text-meta text-ink-3">{current.subject}</span>
              ) : null}
            </span>

            <span className="flex shrink-0 items-center gap-[var(--s-1)]">
              {flagged ? (
                <button
                  type="button"
                  disabled={busy}
                  onClick={() => save(String(current.value ?? ""))}
                  className="rounded-[var(--r-sm)] border border-edge bg-surface px-[var(--s-3)] py-[var(--s-1)] text-meta font-medium transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
                >
                  {busy ? "Saving…" : "Looks right"}
                </button>
              ) : null}
              <button
                type="button"
                onClick={() => setEditing(true)}
                title="Fix this field"
                className="grid size-7 place-items-center rounded-[var(--r-sm)] text-ink-3 transition-colors hover:bg-surface-2 hover:text-ink"
              >
                <Pencil aria-hidden size={13} />
                <span className="sr-only">Fix {current.key.replace(/_/g, " ")}</span>
              </button>
            </span>
          </div>
        )}

        {error ? (
          <p role="alert" className="mt-[var(--s-1)] text-meta text-crit">
            {error}
          </p>
        ) : null}

        <p className="mt-[var(--s-1)] flex flex-wrap items-center gap-x-[var(--s-2)] text-meta text-ink-2">
          <button
            type="button"
            onClick={() => onPage(current.page)}
            className="num text-accent underline underline-offset-2"
          >
            p.{current.page}
          </button>
          {current.verified_by_user ? (
            <span className="inline-flex items-center gap-[var(--s-1)] text-ok">
              <Check aria-hidden size={12} strokeWidth={3} />
              checked by you
            </span>
          ) : (
            <span className="num">confidence {current.confidence.toFixed(2)}</span>
          )}
          {flagged ? <span className="text-warn">please check this one</span> : null}
          {was !== null ? <span className="text-ink-3">was {String(was)}</span> : null}
        </p>
      </dd>
    </div>
  );
}

function isNumeric(fact: VaultFact): boolean {
  return typeof fact.value === "number" || fact.value_type === "date";
}

/** Money the way a person writes it; everything else as it was extracted. */
function format(fact: VaultFact): string {
  if (fact.value === null) return "—";
  if (fact.value_type === "money" && typeof fact.value === "number") {
    return fact.value.toLocaleString("en-SG", { style: "currency", currency: "SGD" });
  }
  return String(fact.value);
}
