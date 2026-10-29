import Image from "next/image";

/**
 * The logo: `web/public/parrot-logo.png`, the mark and the name in one image (836 × 298). `size` is
 * its height; the width follows the image.
 *
 * The image is transparent, and in light mode it sits straight on the paper. In dark mode it sits
 * on a small light plate (`.logo-plate`, `--logo-plate`): the terracotta it is drawn in measured
 * 2.0 to 2.3:1 on the dark surfaces, too faint to read as the product's name. It once carried a
 * cream rectangle baked into the image, which was a pale slab in both themes; the plate is the
 * same idea kept to the one theme that needs it, and drawn by CSS so the image stays clean.
 */
export function Wordmark({ size = 40, className = "" }: { size?: number; className?: string }) {
  return (
    <span className={`logo-plate ${className}`}>
      <Image
        src="/parrot-logo.png"
        alt="Parrot"
        width={Math.round((size * 836) / 298)}
        height={size}
        priority
      />
    </span>
  );
}

/** The logo at top-bar size. The image already carries the name, so nothing is set beside it. */
export function WordmarkLockup() {
  return <Wordmark size={32} />;
}

/** The mark alone, beside a reply in Ask: the same plate, a quarter of the padding. */
export function Mark({ size = 18 }: { size?: number }) {
  return (
    <span className="logo-plate p-[2px]">
      <Image src="/icon.png" alt="" width={size} height={size} unoptimized />
    </span>
  );
}
