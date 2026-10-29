import type { Metadata } from "next";
import { AdviceConsentSection } from "@/components/household/advice-consent";
import { OwnerForm } from "@/components/household/owner-form";
import { Roster } from "@/components/household/roster";
import { WhoIsThis } from "@/components/household/who-is-this";
import { PageHeader } from "@/components/page-header";
import { ProblemState } from "@/components/states";
import { household } from "@/lib/api";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Household · Parrot",
  description: "Who lives here, and which one of them is you.",
};

/**
 * Not a fifth tab.
 *
 * `components/nav.tsx` says four destinations and means it: a fifth needs a "more" menu, and a
 * household tool that needs a "more" menu has already lost the people it was built for. This
 * screen is reached by pressing your own name in the top bar, which is where somebody looks
 * when the name is wrong — the correction is one tap from the mistake, which is the only place
 * a correction is ever made.
 */
export default async function HouseholdPage() {
  const who = await household();

  if (!who.ok) {
    return (
      <>
        <PageHeader title="Household" />
        <div className="mt-[var(--s-5)]">
          <ProblemState problem={who.problem} />
        </div>
      </>
    );
  }

  const { people, owner, pending } = who.data;

  return (
    <>
      <PageHeader
        title="Household"
        lead={
          owner
            ? "Who Parrot has found on your documents, and which one of them is you."
            : "Parrot does not know who you are yet."
        }
      />

      {owner ? null : (
        <div className="mt-[var(--s-6)]">
          <OwnerForm />
        </div>
      )}

      {pending.length > 0 ? (
        <section className="mt-[var(--s-6)]">
          <h2 className="group-label">
            {pending.length === 1 ? "One name to place" : "Names to place"}
          </h2>
          <ul className="row-list mt-[var(--s-3)]">
            {pending.map((name, index) => (
              <WhoIsThis key={name.id} name={name} people={people} index={index} />
            ))}
          </ul>
        </section>
      ) : null}

      {owner ? <Roster people={people} /> : null}

      {/* Consent is the owner's, so there is nothing to agree to or withdraw until there is one. */}
      {owner ? <AdviceConsentSection /> : null}

      <p className="mt-[var(--s-6)] border-t border-hairline pt-[var(--s-4)] text-caption text-ink-3">
        Parrot never invents a person. Every name here was printed on a document you filed, or
        typed by you.
      </p>
    </>
  );
}
