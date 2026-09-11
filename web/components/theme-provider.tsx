"use client";

import { ThemeProvider as NextThemes } from "next-themes";

/**
 * The class goes on <html> before first paint, so nobody sees a white flash on the way to a
 * dark screen. `defaultTheme="system"` means we follow the machine until a person says
 * otherwise, and then we remember what they said.
 */
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  return (
    <NextThemes
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
      storageKey="parrot-theme"
    >
      {children}
    </NextThemes>
  );
}
