import Image from "next/image";

/**
 * The logo: `web/public/parrot-logo.png`, the mark and the name in one image (836 × 298). `size` is
 * its height; the width follows the image.
 *
 * The background is transparent, so the mark sits on whatever the page is and reads in both
 * themes — it used to carry a baked-in cream rectangle, which is why it needed rounded corners
 * to sit on a surface at all, and why it was a pale slab in dark mode.
 */
export function Wordmark({ size = 40 }: { size?: number }) {
  return (
    <Image
      src="/parrot-logo.png"
      alt="Parrot"
      width={Math.round((size * 836) / 298)}
      height={size}
      className="shrink-0"
      priority
    />
  );
}

/** The logo at top-bar size. The image already carries the name, so nothing is set beside it. */
export function WordmarkLockup() {
  return <Wordmark size={32} />;
}
