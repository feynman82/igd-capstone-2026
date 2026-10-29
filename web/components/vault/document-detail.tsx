"use client";

import Link from "next/link";
import { useState } from "react";
import { Field } from "@/components/vault/field";
import { pageImage, type VaultDocument } from "@/lib/api";

/**
 * A document, its fields, and the paper beside them.
 *
 * The page is on screen next to the values rather than behind a click, because this is the one
 * screen whose whole job is comparing the two. Clicking a field's page reference moves the
 * panel to that page — a person checking the premium should not have to remember which page it
 * was on while they look at it.
 */
export function DocumentDetail({ document }: { document: VaultDocument }) {
  const firstFlagged = document.facts.find((fact) => fact.needs_review);
  const [page, setPage] = useState(firstFlagged?.page ?? 1);
  const [corrected, setCorrected] = useState(0);

  const flagged = document.facts.filter((fact) => fact.needs_review).length;
  // One household document is usually about one person. Repeating their name on every field is
  // noise; on a joint policy or a household tax summary it is the thing you are looking for.
  const subjects = new Set(document.facts.map((fact) => fact.subject).filter(Boolean));

  return (
    <>
      <Link href="/vault" className="text-caption text-ink-2 no-underline hover:text-accent">
        ← Vault
      </Link>

      {/* The page role, as on every other surface. A filename is a string a machine produced
          rather than a name somebody would say, so it is allowed to break anywhere. */}
      <h1 className="mt-[var(--s-3)] text-heading font-semibold break-words lg:text-page">
        {document.original_name}
      </h1>

      <p className="mt-[var(--s-2)] flex flex-wrap items-center gap-x-[var(--s-3)] text-caption text-ink-2">
        {document.pack_id ? (
          <span>{document.pack_id.replace(/_/g, " ")}</span>
        ) : (
          <span>no pack: searchable, but no fields extracted</span>
        )}
        {document.doc_type ? <span>{document.doc_type.replace(/_/g, " ")}</span> : null}
        {document.pages ? (
          <span className="num">
            {document.pages} page{document.pages === 1 ? "" : "s"}
          </span>
        ) : null}
        {document.ingested_at ? <span>added {when(document.ingested_at)}</span> : null}
        {document.synthetic ? <span className="text-brass">synthetic test corpus</span> : null}
      </p>

      {subjects.size === 1 ? (
        <p className="mt-[var(--s-1)] text-caption text-ink-2">
          About {[...subjects][0]}
        </p>
      ) : null}

      {!document.pack_enabled ? (
        <p className="mt-[var(--s-3)] rounded-[var(--r)] border border-brass-line bg-brass-soft p-[var(--s-3)] text-caption text-ink-2">
          This document&rsquo;s pack is switched off, so its facts are hidden from Ask and its
          reminders are silent. The document itself is still here and still searchable.
        </p>
      ) : null}

      {document.quarantine_reason ? (
        <p className="mt-[var(--s-3)] rounded-[var(--r)] border border-warn-line bg-warn-soft p-[var(--s-3)] text-body text-ink">
          {document.quarantine_reason}
        </p>
      ) : null}

      <div className="mt-[var(--s-5)] grid gap-[var(--s-5)] lg:grid-cols-[1fr_22rem]">
        <section>
          <div className="flex items-baseline justify-between gap-[var(--s-3)]">
            <h2 className="group-label">Extracted fields</h2>
            {flagged - corrected > 0 ? (
              <p className="text-caption text-warn">
                {flagged - corrected} below the confidence floor
              </p>
            ) : null}
          </div>

          {document.facts.length === 0 ? (
            <p className="mt-[var(--s-3)] text-body text-ink-2">
              Nothing was extracted from this document. It is still searchable, and Ask can quote
              it, but no pack recognised it, so there are no typed fields and no reminders.
            </p>
          ) : (
            <dl className="mt-[var(--s-2)]">
              {document.facts.map((fact) => (
                <Field
                  key={fact.id}
                  fact={fact}
                  onPage={setPage}
                  onCorrected={() => setCorrected((n) => n + 1)}
                  showSubject={subjects.size > 1}
                />
              ))}
            </dl>
          )}

          {flagged > 0 ? (
            <p className="mt-[var(--s-4)] max-w-[var(--measure)] text-caption text-ink-2">
              A field below the floor is flagged rather than trusted. Confirming or fixing it
              takes one click, and either way the answer is stored as a labelled example: what
              the model read, what it actually said, and how sure it was.
            </p>
          ) : null}
        </section>

        <aside className="lg:sticky lg:top-[var(--s-5)] lg:self-start">
          <h2 className="group-label">
            Source, page <span className="num">{page}</span>
          </h2>
          <div className="mt-[var(--s-2)] overflow-hidden rounded-[var(--r)] border border-hairline bg-surface-3 p-[var(--s-2)]">
            {/* eslint-disable-next-line @next/next/no-img-element -- drawn on demand from a
                file this app is not allowed to index. */}
            <img
              src={pageImage(document.document_id, page)}
              alt={`Page ${page} of ${document.original_name}`}
              className="w-full rounded-[var(--r-sm)] border border-hairline bg-white"
            />
          </div>
          {document.pages && document.pages > 1 ? (
            <div className="mt-[var(--s-2)] flex flex-wrap gap-[var(--s-1)]">
              {Array.from({ length: document.pages }, (_, index) => index + 1).map((number) => (
                <button
                  key={number}
                  type="button"
                  onClick={() => setPage(number)}
                  aria-current={number === page ? "true" : undefined}
                  className={`num size-7 rounded-[var(--r-sm)] text-caption ${
                    number === page
                      ? "bg-brand text-brand-ink"
                      : "border border-edge text-ink-2 hover:bg-surface-2"
                  }`}
                >
                  {number}
                </button>
              ))}
            </div>
          ) : null}
        </aside>
      </div>
    </>
  );
}

function when(iso: string): string {
  return new Date(iso).toLocaleDateString("en-SG", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}
