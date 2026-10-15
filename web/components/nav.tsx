"use client";

import { Bell, CalendarDays, Files, MessageSquare, Package } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

/**
 * Five destinations. The design pack held it at four, on the ground that a fifth would need a
 * "more" menu; the Calendar (ADR 0020) is the fifth, and it fits without one — five short words
 * on a wide screen, five icons on a phone's bottom bar. A sixth would need the menu, and a
 * household tool that needs a "more" menu has already lost the people it was built for.
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
  { href: "/calendar", label: "Calendar", Icon: CalendarDays, hint: "What the household has on" },
  { href: "/ask", label: "Ask", Icon: MessageSquare, hint: "A question about your documents" },
  { href: "/vault", label: "Vault", Icon: Files, hint: "Everything filed" },
  { href: "/packs", label: "Packs", Icon: Package, hint: "What this assistant knows about" },
] as const;

/**
 * The five, as pills in the top bar, on a wide screen.
 *
 * This was a left rail. It moved for one reason: a rail 13.5rem wide inside a 68rem shell pushes
 * the content column off centre, so the thing a person is actually reading sits to the right of
 * the middle of their screen all day. Four words do not need a column of their own. With the
 * navigation on one line above, the content can be a single centred column of a readable width,
 * which is what `--column` is.
 *
 * No icons here. In a rail an icon gives the eye something to land on down a vertical list; in a
 * horizontal row of five short words it is decoration beside a word that already says it. The
 * bottom bar below keeps them, because there the label is 11px and the icon is the target.
 */
export function Tabs() {
  const here = usePathname();
  return (
    <nav aria-label="Surfaces" className="hidden lg:block">
      <ul className="flex items-center gap-[var(--s-1)]">
        {SURFACES.map(({ href, label, hint }) => {
          const on = here.startsWith(href);
          return (
            <li key={href}>
              <Link
                href={href}
                aria-current={on ? "page" : undefined}
                title={hint}
                className={[
                  "inline-flex items-center rounded-[var(--r-pill)] px-[var(--s-4)] py-[10px]",
                  "font-display text-[0.90625rem] leading-[var(--lh-flat)] no-underline",
                  on
                    ? "bg-brand-soft font-semibold text-brand-strong"
                    : "font-medium text-ink-2 hover:bg-surface-2 hover:text-ink",
                ].join(" ")}
              >
                {label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

/**
 * The same five, at the bottom, on a phone. Bottom rather than top because this is opened
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
                  on ? "text-brand" : "text-ink-3",
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
