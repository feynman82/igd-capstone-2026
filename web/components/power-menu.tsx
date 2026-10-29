"use client";

import { Power, RotateCw } from "lucide-react";
import { useCallback, useEffect, useId, useRef, useState } from "react";
import { RestartingScreen, ShutDownScreen } from "@/components/system-screens";

/**
 * Restart and shut down, from the chrome.
 *
 * Beside Lock and in the same voice — a word and a small icon, quiet until it is needed —
 * because they are the same kind of control: something done *to* Parrot rather than inside it.
 * Both ask first. A restart interrupts whatever document the worker is reading, and a shut-down
 * closes these screens, so neither should happen by brushing past a menu. The confirm step puts
 * focus on Cancel, so Enter never shuts anything down by accident.
 *
 * The request goes to `app/api/system`, never through the generic proxy: the engine accepts a
 * lifecycle request only from that route. See the note there.
 */

type Action = "restart" | "shutdown";

type Stage =
  | { kind: "closed" }
  | { kind: "menu" }
  | { kind: "confirm"; action: Action }
  | { kind: "sending"; action: Action }
  | { kind: "failed"; action: Action; detail: string }
  | { kind: "restarting" }
  | { kind: "off" };

const ITEMS: { action: Action; title: string; hint: string; Icon: typeof Power }[] = [
  {
    action: "restart",
    title: "Restart Parrot",
    hint: "Reconnects in about a minute. The screens stay open.",
    Icon: RotateCw,
  },
  {
    action: "shutdown",
    title: "Shut down Parrot",
    hint: "Stops the assistant, its filing and these screens.",
    Icon: Power,
  },
];

const CONFIRM: Record<Action, { title: string; body: string; go: string; going: string }> = {
  restart: {
    title: "Restart Parrot?",
    body: "Parrot stops, starts again with what is on this computer now, and this page reconnects by itself. Nothing is deleted.",
    go: "Restart",
    going: "Restarting…",
  },
  shutdown: {
    title: "Shut down Parrot?",
    body: "Today, Ask, Vault and Packs close, and anything new in the inbox waits until Parrot starts again. Nothing is deleted.",
    go: "Shut down",
    going: "Shutting down…",
  },
};

export function PowerMenu() {
  const [stage, setStage] = useState<Stage>({ kind: "closed" });
  const wrapper = useRef<HTMLDivElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const panelId = useId();

  const pending =
    stage.kind === "confirm" || stage.kind === "sending" || stage.kind === "failed" ? stage : null;
  const open = stage.kind === "menu" || pending !== null;

  const close = useCallback(() => {
    setStage({ kind: "closed" });
    trigger.current?.focus();
  }, []);

  useEffect(() => {
    if (!open) return;
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") close();
    }
    function onPointer(event: PointerEvent) {
      if (wrapper.current && !wrapper.current.contains(event.target as Node)) close();
    }
    document.addEventListener("keydown", onKey);
    document.addEventListener("pointerdown", onPointer);
    return () => {
      document.removeEventListener("keydown", onKey);
      document.removeEventListener("pointerdown", onPointer);
    };
  }, [open, close]);

  async function send(action: Action) {
    setStage({ kind: "sending", action });
    let response: Response;
    try {
      response = await fetch("/api/system", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ action }),
      });
    } catch {
      setStage({
        kind: "failed",
        action,
        detail: "The screens could not reach Parrot. It may already be stopping.",
      });
      return;
    }
    if (response.status === 401) {
      window.location.assign("/unlock");
      return;
    }
    if (response.status === 202) {
      setStage(action === "restart" ? { kind: "restarting" } : { kind: "off" });
      return;
    }
    const body = (await response.json().catch(() => ({}))) as { detail?: unknown };
    setStage({
      kind: "failed",
      action,
      detail:
        typeof body.detail === "string" && body.detail
          ? body.detail
          : `Parrot answered with ${response.status}.`,
    });
  }

  return (
    <div ref={wrapper} className="relative">
      <button
        ref={trigger}
        type="button"
        aria-haspopup="dialog"
        aria-expanded={open}
        aria-controls={open ? panelId : undefined}
        onClick={() => (open ? close() : setStage({ kind: "menu" }))}
        className={[
          "flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] px-[var(--s-2)] py-[var(--s-1)] text-caption transition-colors",
          open ? "bg-surface-2 text-ink" : "text-ink-3 hover:text-ink",
        ].join(" ")}
      >
        <Power aria-hidden size={14} strokeWidth={1.9} />
        Power
      </button>

      {open ? (
        <div
          id={panelId}
          role="dialog"
          aria-label={pending ? CONFIRM[pending.action].title : "Restart or shut down Parrot"}
          className="absolute top-[calc(100%+var(--s-2))] right-0 z-30 w-[20rem] rounded-[var(--r)] border border-hairline bg-surface shadow-lift-2"
        >
          {pending === null ? (
            <div className="flex flex-col gap-[2px] p-[var(--s-2)]">
              {ITEMS.map(({ action, title, hint, Icon }) => (
                <button
                  key={action}
                  type="button"
                  autoFocus={action === "restart"}
                  onClick={() => setStage({ kind: "confirm", action })}
                  className="flex items-start gap-[var(--s-3)] rounded-[var(--r-sm)] p-[var(--s-3)] text-left transition-colors hover:bg-surface-2 focus-visible:bg-surface-2"
                >
                  <Icon aria-hidden size={16} strokeWidth={1.9} className="mt-[2px] shrink-0 text-ink-2" />
                  <span className="flex flex-col gap-[2px]">
                    <span className="font-display text-body font-semibold text-ink">
                      {title}
                    </span>
                    <span className="text-caption text-ink-3">{hint}</span>
                  </span>
                </button>
              ))}
              <p className="mx-[var(--s-1)] mt-[var(--s-1)] border-t border-hairline px-[var(--s-2)] pt-[var(--s-2)] pb-[var(--s-1)] text-caption text-ink-3">
                Your documents are kept either way.
              </p>
            </div>
          ) : (
            <div className="flex flex-col gap-[var(--s-3)] p-[var(--s-5)]">
              <h2 className="font-display text-body font-semibold">{CONFIRM[pending.action].title}</h2>
              <p className="text-body text-ink-2">{CONFIRM[pending.action].body}</p>
              {pending.action === "shutdown" ? (
                <p className="text-caption text-ink-3">
                  To start again, open <span className="num text-ink-2">START.cmd</span>.
                </p>
              ) : null}
              {pending.kind === "failed" ? (
                <p
                  role="alert"
                  className="rounded-[var(--r-sm)] border border-warn-line bg-warn-soft px-[var(--s-3)] py-[var(--s-2)] text-caption text-ink"
                >
                  {pending.detail}
                </p>
              ) : null}
              <div className="flex justify-end gap-[var(--s-2)] pt-[var(--s-1)]">
                <button
                  type="button"
                  autoFocus
                  onClick={close}
                  className="rounded-[var(--r-sm)] border border-edge bg-surface px-[var(--s-3)] py-[var(--s-2)] text-caption font-semibold text-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  disabled={pending.kind === "sending"}
                  onClick={() => send(pending.action)}
                  className="rounded-[var(--r-sm)] bg-brand px-[var(--s-4)] py-[var(--s-2)] font-display text-caption font-semibold text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97] disabled:opacity-70"
                >
                  {pending.kind === "sending" ? CONFIRM[pending.action].going : CONFIRM[pending.action].go}
                </button>
              </div>
            </div>
          )}
        </div>
      ) : null}

      {stage.kind === "restarting" ? <RestartingScreen /> : null}
      {stage.kind === "off" ? <ShutDownScreen /> : null}
    </div>
  );
}
