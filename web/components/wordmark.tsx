/**
 * The mark. The same glyph as the browser tab icon, drawn rather than imported, so it takes the
 * accent from the theme and is correct in both.
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
      <rect width="32" height="32" rx="7" className="fill-accent" />
      <path
        d="M11 24V9.5A1.5 1.5 0 0 1 12.5 8h5.8a5.6 5.6 0 0 1 0 11.2H14"
        fill="none"
        className="stroke-accent-ink"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
