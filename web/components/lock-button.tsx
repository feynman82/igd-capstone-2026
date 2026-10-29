"use client";

import { Lock } from "lucide-react";
import { useState } from "react";

/**
 * Lock it now, rather than waiting twelve hours for the session to lapse. Small, quiet, and
 * always in the same place — somebody closing a laptop in a shared kitchen should not have to
 * look for it.
 */
export function LockButton() {
  const [busy, setBusy] = useState(false);

  return (
    <button
      type="button"
      disabled={busy}
      onClick={async () => {
        setBusy(true);
        await fetch("/api/auth", { method: "DELETE" }).catch(() => null);
        window.location.assign("/unlock");
      }}
      className="flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] px-[var(--s-2)] py-[var(--s-1)] text-caption text-ink-3 transition-colors hover:text-ink"
    >
      <Lock aria-hidden size={14} strokeWidth={1.9} />
      {busy ? "Locking…" : "Lock"}
    </button>
  );
}
