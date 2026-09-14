import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { FlatCompat } from "@eslint/eslintrc";

/**
 * `next lint` is deprecated and goes away in Next.js 16, so lint runs through the ESLint CLI.
 *
 * `eslint-config-next` 15 still ships its rules as a legacy shareable config; `FlatCompat`
 * is the adapter Next.js documents for reading it from a flat config.
 */
const compat = new FlatCompat({ baseDirectory: dirname(fileURLToPath(import.meta.url)) });

const eslintConfig = [
  { ignores: [".next/**", "node_modules/**", "next-env.d.ts"] },
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  // A `.cjs` script is CommonJS by definition; `require()` is the only import it has.
  { files: ["**/*.cjs"], rules: { "@typescript-eslint/no-require-imports": "off" } },
];

export default eslintConfig;
