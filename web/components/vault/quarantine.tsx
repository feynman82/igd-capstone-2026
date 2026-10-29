"use client";

import { RotateCw } from "lucide-react";
import { useRouter } from "next/navigation";
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
 * **A document whose file has left the inbox is not a job.** Nothing can be done with it except
 * forget it, so it gets a quiet one-line row with exactly that button instead of the full row. On
 * 13 September `b1-0032.pdf` had been deleted from the inbox and still sat on Today as something
 * needing attention, with a reason and no action — which is the one thing a row that asks for a
 * person must never be.
 */
export function QuarantineQueue({ documents }: { documents: QuarantinedDocument[] }) {
  return (
    <ul className="row-list mt-[var(--s-3)]">
      {documents.map((document) =>
        document.retryable ? (
          <QuarantineRow key={document.document_id} document={document} />
        ) : (
          <GoneRow key={document.document_id} document={document} />
        ),
      )}
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
    <li>
      <div className="flex gap-[var(--s-3)] p-[var(--s-4)]">
        <div className="min-w-0 flex-1">
          <h3 className="font-display text-body font-semibold break-words">
            {document.original_name}
          </h3>
          <p className="mt-[var(--s-1)] text-body text-ink-2">
            {document.reason ?? "This document could not be read."}
          </p>

          <div className="mt-[var(--s-3)] flex flex-wrap items-center gap-[var(--s-3)]">
            {state === "queued" ? (
              <p className="text-caption text-ok">
                Queued. The vision pass takes a minute or so; reload to see the result.
              </p>
            ) : (
              <button
                type="button"
                disabled={state === "queueing"}
                onClick={retry}
                className="inline-flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] border border-edge px-[var(--s-3)] py-[var(--s-1)] text-caption font-semibold transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
              >
                <RotateCw aria-hidden size={13} />
                {state === "queueing" ? "Queueing…" : "Read it again"}
              </button>
            )}
            <span className="num text-caption text-ink-3">{document.mime}</span>
          </div>

          {error ? (
            <p role="alert" className="mt-[var(--s-2)] text-caption text-crit">
              {error}
            </p>
          ) : null}
        </div>
      </div>
    </li>
  );
}

function GoneRow({ document }: { document: QuarantinedDocument }) {
  const router = useRouter();
  const [state, setState] = useState<"idle" | "forgetting" | "forgotten">("idle");
  const [error, setError] = useState<string | null>(null);

  async function forget() {
    setState("forgetting");
    setError(null);
    const response = await fetch(`/api/parrot/quarantine/${document.document_id}`, {
      method: "DELETE",
    }).catch(() => null);
    if (!response?.ok) {
      const body = (await response?.json().catch(() => null)) as { detail?: string } | null;
      setError(body?.detail ?? "Parrot could not forget that.");
      setState("idle");
      return;
    }
    setState("forgotten");
    router.refresh();
  }

  return (
    <li className="px-[var(--s-4)] py-[var(--s-2)]">
      <div className="flex flex-wrap items-center gap-x-[var(--s-3)] gap-y-[var(--s-1)]">
        <p className="min-w-0 flex-1 text-caption text-ink-3">
          <span className="font-semibold break-words text-ink-2">{document.original_name}</span>{" "}
          {state === "forgotten"
            ? "is forgotten."
            : "left the inbox before Parrot could read it. Nothing from it was filed."}
        </p>
        {state === "forgotten" ? null : (
          <button
            type="button"
            disabled={state === "forgetting"}
            onClick={forget}
            title="Removes Parrot's record of this document. Your files are not touched."
            className="shrink-0 rounded-[var(--r-sm)] px-[var(--s-2)] py-[var(--s-1)] text-caption font-semibold text-ink-2 transition-colors hover:bg-surface-2 hover:text-ink disabled:opacity-60"
          >
            {state === "forgetting" ? "Forgetting…" : "Forget it"}
          </button>
        )}
      </div>
      {error ? (
        <p role="alert" className="mt-[var(--s-1)] text-caption text-crit">
          {error}
        </p>
      ) : null}
    </li>
  );
}
