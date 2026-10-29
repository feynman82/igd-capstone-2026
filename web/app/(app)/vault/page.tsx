import type { Metadata } from "next";
import Link from "next/link";
import { PageHeader } from "@/components/page-header";
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
        <PageHeader title="Vault" />
        <div className="mt-[var(--s-5)]">
          <ProblemState problem={listing.problem}>
            {listing.problem.kind === "offline" || listing.problem.kind === "foreign" ? (
              <>
                Your documents are untouched: they are files in your watched folder, and Parrot
                only reads them.
              </>
            ) : null}
          </ProblemState>
        </div>
      </>
    );
  }

  const { documents, total } = listing.data;
  const quarantined = waiting.ok ? waiting.data.documents : [];
  // A document whose file has left the inbox cannot be read again, only forgotten, so it is listed
  // quietly under its own label rather than as something that needs a person's eyes.
  const needsEyes = quarantined.filter((document) => document.retryable);
  const gone = quarantined.filter((document) => !document.retryable);

  return (
    <>
      <PageHeader
        title="Vault"
        lead={
          total === 0
            ? "Nothing filed yet."
            : `${total} document${total === 1 ? "" : "s"}, and everything read off ${total === 1 ? "it" : "them"}.`
        }
      />

      {needsEyes.length > 0 ? (
        <section className="mt-[var(--s-6)]">
          <h2 className="group-label">Needs your eyes</h2>
          <QuarantineQueue documents={needsEyes} />
        </section>
      ) : null}

      {gone.length > 0 ? (
        <section className="mt-[var(--s-6)]">
          <h2 className="group-label">No longer in the inbox</h2>
          <QuarantineQueue documents={gone} />
        </section>
      ) : null}

      {documents.length === 0 ? (
        <div className="mt-[var(--s-6)]">
          <EmptyState title="Nothing filed yet">
            Drop a document into your watched folder, or send one to the Parrot bot on Telegram.
            It will appear here within a minute. Nothing is uploaded anywhere; the folder stays
            where it is and Parrot reads it in place.
          </EmptyState>
        </div>
      ) : (
        <section className="mt-[var(--s-6)]">
          <h2 className="group-label">{status ? `Filed, ${status}` : "Filed"}</h2>
          <ul className="row-list mt-[var(--s-3)]">
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
        <span className="min-w-0 flex-1 truncate text-body font-semibold text-ink">
          {document.original_name}
        </span>

        {flagged > 0 ? (
          <span className="status bg-warn-soft text-warn">{flagged} to check</span>
        ) : null}

        {!document.pack_enabled ? (
          <span className="text-caption text-ink-3">pack off</span>
        ) : null}

        <span className="text-caption text-ink-2">
          {document.doc_type?.replace(/_/g, " ") ?? "not recognised"}
        </span>
        <span className="num w-[7rem] shrink-0 text-right text-caption text-ink-3">
          {document.facts.length} field{document.facts.length === 1 ? "" : "s"}
        </span>
      </Link>
    </li>
  );
}
