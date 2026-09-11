import type { Metadata, Viewport } from "next";
import { Archivo, JetBrains_Mono, Spectral } from "next/font/google";
import { ThemeProvider } from "@/components/theme-provider";
import "./globals.css";

/**
 * Fonts are downloaded at build time and served from this machine. An assistant that needs
 * Google's servers to render its own type is not the offline-capable thing we said it was.
 */
const archivo = Archivo({
  subsets: ["latin"],
  variable: "--font-archivo",
  display: "swap",
});

const spectral = Spectral({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-spectral",
  display: "swap",
});

const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Parrot",
  description: "Your household's documents, answered with the page they came from.",
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f6f7f5" },
    { media: "(prefers-color-scheme: dark)", color: "#0d1311" },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${archivo.variable} ${spectral.variable} ${jetbrains.variable}`}
    >
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
