import type { Metadata } from "next";
import { DesignPreview } from "./preview";

export const metadata: Metadata = {
  title: "PARROT — interface evaluation",
  description: "Three interactive design directions. Sample data only.",
};

export default function DesignPreviewPage() {
  return <DesignPreview />;
}
