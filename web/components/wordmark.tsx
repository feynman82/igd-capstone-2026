import Image from "next/image";

/**
 * The logo: `web/public/parrot-logo.png`, the mark and the name in one image (891 × 318). `size` is
 * its height; the width follows the image.
 */
export function Wordmark({ size = 40 }: { size?: number }) {
  return (
    <Image
      src="/parrot-logo.png"
      alt="Parrot"
      width={Math.round((size * 891) / 318)}
      height={size}
      className="shrink-0 rounded-[var(--r-1,4px)]"
      priority
    />
  );
}

/** The logo at top-bar size. The image already carries the name, so nothing is set beside it. */
export function WordmarkLockup() {
  return <Wordmark size={32} />;
}
