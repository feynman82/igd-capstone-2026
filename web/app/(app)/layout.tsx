import { cookies } from "next/headers";
import Link from "next/link";
import { redirect } from "next/navigation";
import { LockButton } from "@/components/lock-button";
import { TabBar, Tabs } from "@/components/nav";
import { ThemeToggle } from "@/components/theme-toggle";
import { WordmarkLockup } from "@/components/wordmark";
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
            <span className="hidden items-center gap-[var(--s-2)] text-meta text-ink-3 md:flex">
              <span aria-hidden className="size-[7px] rounded-[var(--r-pill)] bg-accent" />
              On this computer
            </span>
            <ThemeToggle />
            <LockButton />
          </div>
        </div>
      </header>

      <main
        id="surface"
        className="mx-auto w-full max-w-[var(--column)] flex-1 px-[var(--gutter)] pt-[var(--s-6)] pb-[var(--s-7)]"
      >
        {children}
      </main>

      <TabBar />
    </div>
  );
}
