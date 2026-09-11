"use client";

import { Bell, Files, MessageSquare, Package } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

/**
 * Four destinations. The count is the design pack's, and it is deliberate: a fifth would need a
 * "more" menu, and a household tool that needs a "more" menu has already lost the people it was
 * built for.
 *
 * Capture is not here. Filing happens in Telegram and in a watched folder, outside the app
 * entirely, because asking an overloaded person to open an app in order to file something is how
 * filing stops happening.
 *
 * Nothing animates on a tab change. It is the interaction a person performs dozens of times a
 * day, and motion there is what makes a fast app feel slow.
 */

const SURFACES = [
  { href: "/today", label: "Today", Icon: Bell, hint: "What needs you" },
  { href: "/ask", label: "Ask", Icon: MessageSquare, hint: "A question about your documents" },
  { href: "/vault", label: "Vault", Icon: Files, hint: "Everything filed" },
  { href: "/packs", label: "Packs", Icon: Package, hint: "What this assistant knows about" },
] as const;

export function Rail() {
  const here = usePathname();
  return (
    <nav aria-label="Surfaces" className="hidden lg:block">
      <ul className="space-y-[var(--s-1)]">
        {SURFACES.map(({ href, label, Icon, hint }) => {
          const on = here.startsWith(href);
          return (
            <li key={href}>
              <Link
                href={href}
                aria-current={on ? "page" : undefined}
                title={hint}
                className={[
                  "flex items-center gap-[var(--s-3)] rounded-[var(--r-sm)] px-[var(--s-3)] py-[var(--s-2)] no-underline",
                  on
                    ? "bg-accent-soft font-medium text-accent"
                    : "text-ink-2 hover:bg-surface-2 hover:text-ink",
                ].join(" ")}
              >
                <Icon aria-hidden size={17} strokeWidth={on ? 2.2 : 1.9} />
                <span className="text-body">{label}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

/**
 * The same four, at the bottom, on a phone. Bottom rather than top because this is opened
 * one-handed on the way out of the door, and the top of a phone is the part a thumb cannot
 * reach.
 */
export function TabBar() {
  const here = usePathname();
  return (
    <nav
      aria-label="Surfaces"
      className="sticky bottom-0 z-10 border-t border-hairline bg-ground/95 backdrop-blur-sm lg:hidden"
      style={{ paddingBottom: "env(safe-area-inset-bottom)" }}
    >
      <ul className="mx-auto flex max-w-[var(--shell)]">
        {SURFACES.map(({ href, label, Icon }) => {
          const on = here.startsWith(href);
          return (
            <li key={href} className="flex-1">
              <Link
                href={href}
                aria-current={on ? "page" : undefined}
                className={[
                  "flex flex-col items-center gap-[var(--s-1)] py-[var(--s-2)] no-underline",
                  on ? "text-accent" : "text-ink-3",
                ].join(" ")}
              >
                <Icon aria-hidden size={19} strokeWidth={on ? 2.2 : 1.9} />
                <span className="text-label font-medium tracking-normal normal-case">{label}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
