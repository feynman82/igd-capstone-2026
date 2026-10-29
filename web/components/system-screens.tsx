"use client";

import { ArrowRight, Check } from "lucide-react";
import { useEffect, useState } from "react";

/**
 * The two states Parrot draws about itself: restarting, and off.
 *
 * Neither uses a spinner — there are none in this interface. A row that is still happening is a
 * skeleton with the one looping motion the system allows, and a row that has happened is a tick
 * in the `ok` colour, which in `theme.css` means "handled".
 *
 * **Restarting** covers the content column and leaves the header alone, because the screens
 * stay up through a restart (the supervisor owns them) and the header is what tells a person it
 * is still Parrot. It polls `app/api/system` once a second and moves to Today when the engine is
 * back and can reach the database and the queue.
 *
 * It deliberately does not wait for the ingestion worker to answer a ping. The worker runs a
 * solo pool on Windows, and a solo worker busy reading a document cannot answer anything — on
 * 13 September the readiness check said "No worker is listening" while the worker was twenty
 * minutes into reading seven documents. Waiting on that would hold this screen up for exactly as
 * long as Parrot is doing useful work.
 */

type DependencyCheck = { name: string; state: "available" | "blocked" | "unverified"; detail: string };
type Status = { engine: "running" | "offline"; can_restart?: boolean; checks?: DependencyCheck[] };

type Phase = { stopped: boolean; back: boolean; database: boolean; filing: boolean; slow: boolean };

const POLL_MS = 1000;
/** A fresh engine that answers without ever having been seen stopped is back after this long. */
const ASSUME_STOPPED_AFTER_MS = 15_000;
/** Past this, the screen says so rather than letting a person wonder whether it is stuck. */
const PATIENCE_MS = 180_000;

function stateOf(status: Status, name: string): DependencyCheck["state"] | undefined {
  return status.checks?.find((check) => check.name === name)?.state;
}

export function RestartingScreen() {
  const [phase, setPhase] = useState<Phase>({
    stopped: false,
    back: false,
    database: false,
    filing: false,
    slow: false,
  });
  const ready = phase.back && phase.database && phase.filing;

  useEffect(() => {
    const started = Date.now();
    let sawOffline = false;
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;

    const poll = async () => {
      let status: Status = { engine: "offline" };
      try {
        const response = await fetch("/api/system", { cache: "no-store" });
        if (response.status === 401) {
          window.location.assign("/unlock");
          return;
        }
        status = (await response.json()) as Status;
      } catch {
        // A blip in the screens themselves. It counts as "not back yet"; the next poll decides.
      }
      if (cancelled) return;

      const running = status.engine === "running";
      if (!running) sawOffline = true;
      const elapsed = Date.now() - started;
      // The first poll can still reach the old engine in the quarter-second before it exits, so
      // "running" only means "back" once this screen has seen it stop.
      const back = running && (sawOffline || elapsed > ASSUME_STOPPED_AFTER_MS);
      setPhase({
        stopped: sawOffline || back,
        back,
        database: back && stateOf(status, "Database") === "available",
        filing: back && stateOf(status, "Queue broker") === "available",
        slow: elapsed > PATIENCE_MS,
      });
      timer = setTimeout(poll, POLL_MS);
    };

    void poll();
    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, []);

  useEffect(() => {
    if (!ready) return;
    const timer = setTimeout(() => window.location.assign("/today"), 900);
    return () => clearTimeout(timer);
  }, [ready]);

  return (
    <div
      role="status"
      aria-live="polite"
      className="fixed inset-x-0 top-[var(--bar)] bottom-0 z-40 overflow-y-auto bg-ground"
    >
      <div className="mx-auto w-full max-w-[var(--column)] px-[var(--gutter)] pt-[var(--s-6)] pb-[var(--s-7)]">
        <div className="flex max-w-[35rem] flex-col gap-[var(--s-6)]">
          <div className="flex flex-col gap-[var(--s-2)]">
            <h1 className="font-display text-page font-semibold">Restarting Parrot</h1>
            <p className="text-body text-ink-2">
              Your documents stay exactly where they are. This page reconnects by itself, usually
              within a minute.
            </p>
          </div>

          <div className="flex flex-col overflow-hidden rounded-[var(--r)] border border-hairline bg-surface shadow-lift-1">
            <Row
              first
              title="The running engine"
              detail="Finished what it was doing, then stopped"
              done={phase.stopped}
              doneLabel="Stopped"
            />
            <Row title="A fresh engine" detail="Starting with what is on this computer now" done={phase.back} />
            <Row title="Your documents" detail="Reconnecting" done={phase.database} />
            <Row title="Filing" detail="Picks up where it left off" done={phase.filing} />
          </div>

          {ready ? (
            <p className="flex items-center gap-[var(--s-2)] text-body text-ink-2">
              <ArrowRight aria-hidden size={16} strokeWidth={2.2} className="shrink-0 text-brand" />
              Back. Reloading Today.
            </p>
          ) : null}

          {phase.slow && !ready ? (
            <div className="rounded-[var(--r)] border border-warn-line bg-warn-soft p-[var(--s-4)]">
              <p className="text-body font-semibold text-ink">Parrot has not come back yet.</p>
              <p className="mt-[var(--s-1)] text-body text-ink-2">
                The first start after a restart can take longer while the local model loads. This
                page keeps checking. If the Parrot window shows an error, that is the reason.
              </p>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}

function Row({
  title,
  detail,
  done,
  doneLabel = "Ready",
  first = false,
}: {
  title: string;
  detail: string;
  done: boolean;
  doneLabel?: string;
  first?: boolean;
}) {
  return (
    <div
      className={[
        "flex items-center gap-[var(--s-3)] px-[var(--s-5)] py-[var(--s-3)]",
        first ? "" : "border-t border-hairline",
      ].join(" ")}
    >
      {done ? (
        <span className="grid size-[22px] shrink-0 place-items-center rounded-[var(--r-pill)] border border-ok-line bg-ok-soft text-ok">
          <Check aria-hidden size={13} strokeWidth={3} />
        </span>
      ) : (
        <span aria-hidden className="skeleton size-[22px] shrink-0 rounded-[var(--r-pill)]" />
      )}
      <div className="flex min-w-0 flex-1 flex-col">
        <span className="font-display text-body font-semibold">{title}</span>
        <span className="text-caption text-ink-3">{detail}</span>
      </div>
      {done ? (
        <span className="min-w-[var(--s-8)] text-right text-caption font-semibold text-ok">{doneLabel}</span>
      ) : (
        <span aria-hidden className="skeleton h-[10px] w-14 rounded-[var(--r-sm)]" />
      )}
      <span className="sr-only">{done ? `${title}: ${doneLabel}.` : `${title}: not yet.`}</span>
    </div>
  );
}

/**
 * Parrot is off.
 *
 * Drawn before the screens stop, because after a shut-down there is nothing left to draw it
 * with. No buttons: nothing is running for them to act on, and a button that cannot work is
 * worse than a sentence that says what to do.
 */
export function ShutDownScreen() {
  return (
    <div
      role="status"
      aria-live="polite"
      className="fixed inset-0 z-50 flex justify-center overflow-y-auto bg-ground px-[var(--gutter)] pt-[25vh] pb-[var(--s-8)]"
    >
      <div className="flex w-full max-w-[30rem] flex-col gap-[var(--s-5)]">
        <svg viewBox="0 0 32 32" width={40} height={40} aria-hidden>
          <rect width="32" height="32" rx="8.8" className="fill-surface-3" />
          <path
            d="M11 24V9.5A1.5 1.5 0 0 1 12.5 8h5.8a5.6 5.6 0 0 1 0 11.2H14"
            fill="none"
            className="stroke-ink-3"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        <div className="flex flex-col gap-[var(--s-2)]">
          <h1 className="font-display text-page font-semibold">Parrot is off</h1>
          <p className="text-body text-ink-2">
            The assistant, its filing and these screens have stopped. Your documents are kept, and
            everything Parrot has already read is still there when it starts again.
          </p>
        </div>
        <p className="text-body text-ink-2">
          To start it again, open <span className="num text-ink">START.cmd</span> in the Parrot
          folder.
        </p>
        <p className="text-caption text-ink-3">You can close this tab.</p>
      </div>
    </div>
  );
}
