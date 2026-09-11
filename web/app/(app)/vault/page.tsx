import type { Metadata } from "next";
import Link from "next/link";
import { EmptyState, ProblemState } from "@/components/states";
import { QuarantineQueue } from "@/components/vault/quarantine";
import { quarantine, vault, type VaultDocument } from "@/lib/api";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Vault · Parrot",
  description: "Everything filed, and everything read off it.",
};

/**
 * Everything in the house, and what state it is in.
 *
 * The quarantine queue is at the top rather than in a tab of its own: it is the part of this
 * screen that needs a person, and burying "needs your eyes" under a filter is how it stops
 * being seen. Today links straight here.
 */
export default async function VaultPage({
  searchParams,
}: {
  searchParams: Promise<{ status?: string }>;
}) {
  const { status } = await searchParams;
  const [listing, waiting] = await Promise.all([
    vault(status ? { status } : {}),
    quarantine(),
  ]);

  if (!listing.ok) {
    return (
      <>
        <h1 className="font-display text-screen lg:text-display">Vault</h1>
        <div className="mt-[var(--s-4)]">
          <ProblemState problem={listing.problem}>
            {listing.problem.kind === "offline" || listing.problem.kind === "foreign" ? (
              <>
                Your documents are untouched — they are files in your watched folder, and Parrot
                only reads them.
              </>
            ) : null}
          </ProblemState>
        </div>
      </>
    );
  }

  const { documents, total } = listing.data;
  const needsEyes = waiting.ok ? waiting.data.documents : [];

  return (
    <>
      <h1 className="font-display text-screen lg:text-display">Vault</h1>
      <p className="mt-[var(--s-2)] max-w-[var(--measure)] text-lead text-ink-2">
        {total === 0
          ? "Nothing filed yet."
          : `${total} document${total === 1 ? "" : "s"}, and everything read off ${total === 1 ? "it" : "them"}.`}
      </p>

      {needsEyes.length > 0 ? (
        <section className="mt-[var(--s-6)]">
          <h2 className="group-label">Needs your eyes</h2>
          <QuarantineQueue documents={needsEyes} />
        </section>
      ) : null}

      {documents.length === 0 ? (
        <div className="mt-[var(--s-6)]">
          <EmptyState title="Nothing filed yet">
            Drop a document into your watched folder, or send one to the Parrot bot on Telegram.
            It will appear here within a minute. Nothing is uploaded anywhere — the folder stays
            where it is and Parrot reads it in place.
          </EmptyState>
        </div>
      ) : (
        <section className="mt-[var(--s-6)]">
          <h2 className="group-label">{status ? `Filed — ${status}` : "Filed"}</h2>
          <ul className="mt-[var(--s-3)] divide-y divide-hairline overflow-hidden rounded-[var(--r)] border border-hairline bg-surface">
            {documents.map((document) => (
              <Row key={document.document_id} document={document} />
            ))}
          </ul>
        </section>
      )}
    </>
  );
}

function Row({ document }: { document: VaultDocument }) {
  const flagged = document.facts.filter((fact) => fact.needs_review).length;

  return (
    <li>
      <Link
        href={`/vault/${document.document_id}`}
        className="hoverable flex flex-wrap items-baseline gap-x-[var(--s-3)] gap-y-[var(--s-1)] px-[var(--s-4)] py-[var(--s-3)] no-underline"
      >
        <span className="min-w-0 flex-1 truncate text-body font-medium text-ink">
          {document.original_name}
        </span>

        {flagged > 0 ? (
          <span className="rounded-[var(--r-sm)] border border-warn-line bg-warn-soft px-[var(--s-2)] py-[1px] text-meta text-warn">
            {flagged} to check
          </span>
        ) : null}

        {!document.pack_enabled ? (
          <span className="text-meta text-ink-3">pack off</span>
        ) : null}

        <span className="text-meta text-ink-2">
          {document.doc_type?.replace(/_/g, " ") ?? "not recognised"}
        </span>
        <span className="num w-[7rem] shrink-0 text-right text-meta text-ink-3">
          {document.facts.length} field{document.facts.length === 1 ? "" : "s"}
        </span>
      </Link>
    </li>
  );
}
