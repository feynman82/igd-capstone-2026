/**
 * The mark. The same glyph as the browser tab icon, drawn rather than imported, so it takes the
 * brand colour from the theme and is correct in both.
 *
 * The tile is terracotta rather than evergreen now. Green is reserved for evidence — a source
 * chip, a verified field — and a logo is not evidence of anything.
 */
export function Wordmark({ size = 40 }: { size?: number }) {
  return (
    <svg
      viewBox="0 0 32 32"
      width={size}
      height={size}
      role="img"
      aria-label="Parrot"
      className="shrink-0"
    >
      {/* rx is in the 32-unit viewBox, so it reads as 11px at the 40px default. */}
      <rect width="32" height="32" rx="8.8" className="fill-brand" />
      <path
        d="M11 24V9.5A1.5 1.5 0 0 1 12.5 8h5.8a5.6 5.6 0 0 1 0 11.2H14"
        fill="none"
        className="stroke-brand-ink"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

/**
 * Mark plus name, for the top bar. Lowercase, because the product is a thing on your kitchen
 * table rather than an institution, and set in the naming face at the one size it is used.
 */
export function WordmarkLockup() {
  return (
    <span className="flex items-center gap-[var(--s-2)]">
      <Wordmark size={28} />
      <span className="font-display text-[1.3125rem] leading-none font-semibold tracking-[var(--tr-display)]">
        parrot
      </span>
    </span>
  );
}
