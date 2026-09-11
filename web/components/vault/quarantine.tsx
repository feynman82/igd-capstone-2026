"use client";

import { RotateCw } from "lucide-react";
import { useState } from "react";
import type { QuarantinedDocument } from "@/lib/api";

/**
 * Needs your eyes.
 *
 * A document that could not be read is not an error — it is a job, and it belongs on a screen
 * that says so. The retry sends the page image to the vision-language model, which is the
 * second stage of quarantine and takes tens of seconds on a 4B, so the API queues it and
 * answers 202. This row says "queued" rather than pretending to have finished.
 *
 * A document whose file has left the inbox cannot be retried at all. Offering a button that is
 * certain to fail is worse than explaining why there is no button, so the API works out which
 * ones are blocked and this renders the reason.
 */
export function QuarantineQueue({ documents }: { documents: QuarantinedDocument[] }) {
  return (
    <ul className="mt-[var(--s-3)] space-y-[var(--s-2)]">
      {documents.map((document) => (
        <QuarantineRow key={document.document_id} document={document} />
      ))}
    </ul>
  );
}

function QuarantineRow({ document }: { document: QuarantinedDocument }) {
  const [state, setState] = useState<"idle" | "queueing" | "queued">("idle");
  const [error, setError] = useState<string | null>(null);

  async function retry() {
    setState("queueing");
    setError(null);
    const response = await fetch(`/api/parrot/quarantine/${document.document_id}/retry`, {
      method: "POST",
    }).catch(() => null);

    if (!response?.ok) {
      const body = (await response?.json().catch(() => null)) as { detail?: string } | null;
      // 409 is "the file is gone", 503 is "the queue is not running" — both are sentences a
      // person can act on, written by the API rather than invented here.
      setError(body?.detail ?? "Parrot could not queue that.");
      setState("idle");
      return;
    }
    setState("queued");
  }

  return (
    <li className="overflow-hidden rounded-[var(--r)] border border-hairline bg-surface">
      <div className="flex gap-[var(--s-3)] p-[var(--s-4)]">
        <span aria-hidden className="w-[3px] shrink-0 rounded-[2px] bg-warn" />
        <div className="min-w-0 flex-1">
          <h3 className="text-lead font-medium break-words">{document.original_name}</h3>
          <p className="mt-[var(--s-1)] text-body text-ink-2">
            {document.reason ?? "This document could not be read."}
          </p>

          <div className="mt-[var(--s-3)] flex flex-wrap items-center gap-[var(--s-3)]">
            {document.retryable ? (
              state === "queued" ? (
                <p className="text-meta text-ok">
                  Queued. The vision pass takes a minute or so — reload to see the result.
                </p>
              ) : (
                <button
                  type="button"
                  disabled={state === "queueing"}
                  onClick={retry}
                  className="inline-flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-1)] text-meta font-medium transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
                >
                  <RotateCw aria-hidden size={13} />
                  {state === "queueing" ? "Queueing…" : "Read it again"}
                </button>
              )
            ) : (
              <p className="text-meta text-ink-2">
                {document.blocked ?? "This one cannot be retried."}
              </p>
            )}
            <span className="num text-meta text-ink-3">{document.mime}</span>
          </div>

          {error ? (
            <p role="alert" className="mt-[var(--s-2)] text-meta text-crit">
              {error}
            </p>
          ) : null}
        </div>
      </div>
    </li>
  );
}
