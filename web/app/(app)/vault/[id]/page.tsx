import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ProblemState } from "@/components/states";
import { DocumentDetail } from "@/components/vault/document-detail";
import { document } from "@/lib/api";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Document · Parrot",
};

/**
 * One document, its fields, and the page they were read off.
 *
 * Reachable from the vault listing and from any citation chip in the product, which is why the
 * API returns it whether or not its pack is switched off: following a citation to a document
 * and finding nothing there would be a dead end, and the screen would have nothing to say.
 */
export default async function DocumentPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const found = await document(id);

  if (!found.ok) {
    if (found.problem.kind === "error") notFound();
    return <ProblemState problem={found.problem} />;
  }

  return <DocumentDetail document={found.data} />;
}
