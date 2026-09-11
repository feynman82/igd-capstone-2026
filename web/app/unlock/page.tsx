import type { Metadata } from "next";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { UnlockForm } from "@/components/unlock-form";
import { SESSION_COOKIE, isConfigured, isUnlocked } from "@/lib/lock";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Parrot",
  description: "Unlock this computer's household assistant.",
};

/**
 * The front door, and the only page outside the guard.
 *
 * First run and every run after it are the same screen with different words, because a person
 * arriving here should not have to work out which of two screens they are on before they can
 * type anything.
 */
export default async function UnlockPage() {
  const jar = await cookies();
  if (isUnlocked(jar.get(SESSION_COOKIE)?.value)) {
    redirect("/today");
  }
  return <UnlockForm configured={isConfigured()} />;
}
