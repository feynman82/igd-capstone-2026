import { cookies } from "next/headers";
import Link from "next/link";
import { redirect } from "next/navigation";
import { LockButton } from "@/components/lock-button";
import { PowerMenu } from "@/components/power-menu";
import { TabBar, Tabs } from "@/components/nav";
import { ThemeToggle } from "@/components/theme-toggle";
import { WordmarkLockup } from "@/components/wordmark";
import { household } from "@/lib/api";
import { SESSION_COOKIE, isUnlocked } from "@/lib/lock";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * The guard, and the chrome every surface sits inside.
 *
 * The check is here rather than in `middleware.ts` because middleware runs on the Edge runtime,
 * where neither `node:crypto` nor the filesystem exists — so it could only ask whether a cookie
 * is present, not whether it is one we issued. A layout is a server component with both, and
 * every page in this group renders through it.
 *
 * The chrome is one bar and one column. The bar is `--surface` on a `--ground` page, full width
 * so it reads as the edge of the application rather than as a card; the column is `--column`
 * wide and centred, which is the whole reason navigation left the left-hand rail. See the note
 * on `Tabs`.
 */
export default async function AppLayout({ children }: { children: React.ReactNode }) {
  const jar = await cookies();
  if (!isUnlocked(jar.get(SESSION_COOKIE)?.value)) {
    redirect("/unlock");
  }

  // Who is asking. Read once, in the chrome, because the header greets them on every surface
  // and because the setup step is gated on it. A household Parrot cannot reach is not an error
  // here — the name simply does not appear, and every screen below still works.
  const who = await household();
  const owner = who.ok ? who.data.owner : null;

  return (
    <div className="flex min-h-dvh flex-col">
      {/* Skip link. First thing in the tab order on every surface, visible the moment it has
          focus, because four links in front of the content is four presses of Tab somebody
          repeats on every page. */}
      <a
        href="#surface"
        className="sr-only focus:not-sr-only focus:fixed focus:top-[var(--s-3)] focus:left-[var(--s-3)] focus:z-50 focus:rounded-[var(--r-sm)] focus:bg-surface focus:px-[var(--s-3)] focus:py-[var(--s-2)] focus:text-body focus:shadow-lift-2"
      >
        Skip to the page
      </a>

      <header className="border-b border-hairline bg-surface">
        <div className="mx-auto flex h-[var(--bar)] w-full max-w-[var(--shell)] items-center gap-[var(--s-6)] px-[var(--gutter)]">
          <Link href="/today" className="no-underline">
            <WordmarkLockup />
          </Link>

          <Tabs />

          <div className="ml-auto flex items-center gap-[var(--s-4)]">
            {/* Said once, in the chrome, because it is the claim the whole product rests on and
                it is true on every surface. It is not a status that can change. */}
            {/* One item, two facts. The phrase is the privacy claim the whole product rests
                on; the name is who Parrot thinks you are, and putting them in one line is what
                stops the right-hand side becoming a row of five things. No coloured dot before
                it: the words make the claim, and a dot only looked like a status light.
                It is a link because the place to correct it is one tap from seeing it wrong. */}
            <Link
              href="/household"
              className="hidden items-center gap-[var(--s-2)] text-caption text-ink-3 no-underline transition-colors hover:text-ink md:flex"
            >
              {owner ? (
                <span>
                  <span className="font-semibold text-ink-2">{owner.display_name}</span>, on this
                  computer
                </span>
              ) : (
                "On this computer"
              )}
            </Link>
            <ThemeToggle />
            <LockButton />
            <PowerMenu />
          </div>
        </div>
      </header>

      {/* A surface with a column of its own beside the content (Ask's history) marks itself
          `data-wide` and gets the shell's width, so the content keeps the reading column's. */}
      <main
        id="surface"
        className="mx-auto w-full max-w-[var(--column)] flex-1 px-[var(--gutter)] pt-[var(--s-6)] pb-[var(--s-7)] lg:has-[[data-wide]]:max-w-[var(--shell)]"
      >
        {children}
      </main>

      <TabBar />
    </div>
  );
}
