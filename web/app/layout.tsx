import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import { ThemeProvider } from "@/components/theme-provider";
import "./globals.css";

// One face for everything, served from this machine: Parrot works with no network, so the type
// it is set in does too. Figtree, SIL Open Font License (`fonts/OFL.txt`).
const figtree = localFont({
  src: [
    { path: "./fonts/figtree-latin.woff2", weight: "300 900", style: "normal" },
    { path: "./fonts/figtree-latin-ext.woff2", weight: "300 900", style: "normal" },
  ],
  variable: "--font-figtree",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Parrot",
  description: "Your household's documents, answered with the page they came from.",
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f7f2e9" },
    { media: "(prefers-color-scheme: dark)", color: "#1b1814" },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={figtree.variable} suppressHydrationWarning>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
