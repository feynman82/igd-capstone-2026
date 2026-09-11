import { cookies } from "next/headers";
import Link from "next/link";
import { redirect } from "next/navigation";
import { LockButton } from "@/components/lock-button";
import { Rail, TabBar } from "@/components/nav";
import { ThemeToggle } from "@/components/theme-toggle";
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
 */
export default async function AppLayout({ children }: { children: React.ReactNode }) {
  const jar = await cookies();
  if (!isUnlocked(jar.get(SESSION_COOKIE)?.value)) {
    redirect("/unlock");
  }

  return (
    <div className="flex min-h-dvh flex-col">
      {/* Skip link. First thing in the tab order on every surface, visible the moment it has
          focus, because a rail of four links in front of the content is four presses of Tab
          somebody repeats on every page. */}
      <a
        href="#surface"
        className="sr-only focus:not-sr-only focus:fixed focus:top-[var(--s-3)] focus:left-[var(--s-3)] focus:z-50 focus:rounded-[var(--r-sm)] focus:bg-surface focus:px-[var(--s-3)] focus:py-[var(--s-2)] focus:text-body focus:shadow-lift-2"
      >
        Skip to the page
      </a>

      <div className="mx-auto flex w-full max-w-[var(--shell)] flex-1 gap-[var(--s-6)] px-[var(--gutter)]">
        <div className="hidden w-[var(--rail)] shrink-0 flex-col py-[var(--s-5)] lg:flex">
          <Link href="/today" className="mb-[var(--s-6)] font-display text-lead font-semibold no-underline">
            Parrot
          </Link>
          <Rail />
          <div className="mt-auto flex items-center justify-between gap-[var(--s-2)] pt-[var(--s-5)]">
            <LockButton />
            <ThemeToggle />
          </div>
        </div>

        <main id="surface" className="min-w-0 flex-1 py-[var(--s-5)]">
          <div className="mb-[var(--s-5)] flex items-center justify-between lg:hidden">
            <span className="font-display text-lead font-semibold">Parrot</span>
            <div className="flex items-center gap-[var(--s-3)]">
              <LockButton />
              <ThemeToggle />
            </div>
          </div>
          {children}
        </main>
      </div>

      <TabBar />
    </div>
  );
}
