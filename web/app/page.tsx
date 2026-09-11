import { redirect } from "next/navigation";

/**
 * Temporary. The front door is the passphrase unlock, and behind it is Today; neither exists
 * yet, so for now the only thing built is what everything else gets built against.
 */
export default function Home() {
  redirect("/tokens");
}
