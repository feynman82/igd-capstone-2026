/**
 * The top of every surface: its name, an optional fact on the right, and one sentence under it.
 *
 * One component because five surfaces wrote it five slightly different ways — the gap under the
 * name was 8px on two of them and 12px on the rest, and the Calendar put its sentence on the right
 * where nobody else did. The name is what the tab says; the sentence says what is here, in the
 * household's terms, and never more than one line of reading.
 */
export function PageHeader({
  title,
  lead,
  aside,
}: {
  title: React.ReactNode;
  lead?: React.ReactNode;
  /** A short fact beside the name: when Today was checked. */
  aside?: React.ReactNode;
}) {
  return (
    <header>
      <div className="flex flex-wrap items-baseline justify-between gap-[var(--s-4)]">
        <h1 className="font-display text-heading lg:text-page">{title}</h1>
        {aside}
      </div>
      {lead ? (
        <p className="mt-[var(--s-3)] max-w-[var(--measure)] text-body text-ink-2">{lead}</p>
      ) : null}
    </header>
  );
}
