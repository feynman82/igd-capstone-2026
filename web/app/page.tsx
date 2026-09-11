import { redirect } from "next/navigation";

/** Today is the front door once you are through the lock. The lock screen sends you here too. */
export default function Home() {
  redirect("/today");
}
