import type { Metadata } from "next";
import { EmptyState, ProblemState } from "@/components/states";
import { Toggle } from "@/components/packs/toggle";
import { packs, type ModuleSummary, type PackSummary } from "@/lib/api";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Packs · Parrot",
  description: "What this assistant knows about, and what it could know about.",
};

/**
 * Where the platform argument stops being an architecture diagram and becomes something a
 * person can switch.
 *
 * The demonstration this screen exists for is one gesture: turn Insurance Agent off, go to
 * Today, and watch its reminders be gone. Nothing in `core/` changed to make that work — the
 * registry is read once per request and handed to the modules and to retrieval, and neither of
 * them knows a screen exists.
 *
 * Everything here is read from the registry. There is no hard-coded pack name in this file,
 * which is the point: a third pack appears on this screen because somebody dropped a YAML file
 * in, not because anybody edited the interface.
 */
export default async function PacksPage() {
  const result = await packs();

  if (!result.ok) {
    return (
      <>
        <h1 className="font-display text-screen lg:text-display">Packs</h1>
        <div className="mt-[var(--s-4)]">
          <ProblemState problem={result.problem} />
        </div>
      </>
    );
  }

  const { packs: installed, modules } = result.data;
  const off = installed.filter((pack) => pack.enabled === false);

  return (
    <>
      <h1 className="font-display text-screen lg:text-display">Packs</h1>
      <p className="mt-[var(--s-2)] max-w-[var(--measure)] text-lead text-ink-2">
        What this assistant knows about. Switching a pack off silences its reminders and takes
        its documents out of answers. Nothing is deleted, and switching it back on brings all of
        it back.
      </p>

      <AlwaysOn />

      <section className="mt-[var(--s-6)]">
        <h2 className="group-label">Installed</h2>
        {installed.length === 0 ? (
          <div className="mt-[var(--s-3)]">
            <EmptyState title="No packs installed">
              Parrot can still search and quote your documents, but nothing is reading typed
              fields off them and no reminders are being set. A pack is one YAML file in{" "}
              <span className="num">packs/</span>.
            </EmptyState>
          </div>
        ) : (
          <ul className="mt-[var(--s-3)] space-y-[var(--s-3)]">
            {installed.map((pack) => (
              <PackCard key={pack.id} pack={pack} />
            ))}
          </ul>
        )}
      </section>

      {off.length > 0 ? (
        <p className="mt-[var(--s-4)] max-w-[var(--measure)] rounded-[var(--r)] border border-brass-line bg-brass-soft p-[var(--s-3)] text-meta text-ink-2">
          {off.map((pack) => pack.display_name).join(" and ")}{" "}
          {off.length === 1 ? "is" : "are"} switched off.{" "}
          {off.length === 1 ? "Its" : "Their"} reminders are silent,{" "}
          {off.length === 1 ? "its" : "their"} documents are hidden from the vault listing, and
          Ask cannot cite {off.length === 1 ? "them" : "any of them"} — so it will abstain on a
          question only {off.length === 1 ? "that pack" : "they"} could have answered.
        </p>
      ) : null}

      <section className="mt-[var(--s-6)]">
        <h2 className="group-label">Modules</h2>
        <p className="mt-[var(--s-2)] max-w-[var(--measure)] text-meta text-ink-2">
          A pack declares what to watch; a module does the watching. Switching one off here
          silences it for every pack at once.
        </p>
        <ul className="mt-[var(--s-3)] space-y-[var(--s-2)]">
          {modules.map((module) => (
            <ModuleRow key={module.id} module={module} />
          ))}
        </ul>
      </section>

      <section className="mt-[var(--s-6)]">
        <h2 className="group-label">Available</h2>
        <div className="mt-[var(--s-3)]">
          {/* The nine deferred packs are a real deliverable that has not been written yet
              (`docs/team-tasks.csv`, W3). Inventing plausible names here would put product
              scope on a screen that nobody has agreed to. */}
          <EmptyState title="The catalogue is not written yet">
            The expansion story is that a new domain is a YAML file rather than a release — the
            same core, a different pack. The nine packs we specify but do not build are still to
            be named, each against the same manifest the two above use.
          </EmptyState>
        </div>
      </section>
    </>
  );
}

/**
 * What is true no matter what is switched on.
 *
 * Worth its own row: a person switching everything off should be able to see that Parrot has
 * not become useless, and a person reading this screen should understand that packs add typed
 * fields and reminders rather than being the thing that makes search work.
 */
function AlwaysOn() {
  return (
    <div className="mt-[var(--s-5)] rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-4)]">
      <div className="flex items-baseline gap-[var(--s-3)]">
        <h2 className="text-lead font-medium">Retrieval</h2>
        <span className="ml-auto text-meta text-ok">always on</span>
      </div>
      <p className="mt-[var(--s-1)] max-w-[var(--measure)] text-body text-ink-2">
        Reading, chunking and answering are the core, not a pack. A document that belongs to no
        pack is always searchable and can always be quoted — packs add the typed fields and the
        dates worth reminding you about.
      </p>
    </div>
  );
}

function PackCard({ pack }: { pack: PackSummary }) {
  return (
    // A switched-off pack is dimmed by moving it onto a recessed surface, not by fading it.
    // `opacity` degrades every colour inside a card at once, including the muted provenance
    // text that was measured to exactly 4.5:1 — the one row that can least afford it. The card
    // still has to be readable: a person deciding whether to switch it back on is reading it.
    <li
      className={`rounded-[var(--r)] border p-[var(--s-4)] ${
        pack.enabled ? "border-hairline bg-surface" : "border-hairline bg-surface-2"
      }`}
    >
      <div className="flex items-start gap-[var(--s-3)]">
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-baseline gap-x-[var(--s-3)]">
            <h3 className="text-title font-medium">{pack.display_name}</h3>
            <span className="num text-meta text-ink-3">v{pack.version}</span>
            {!pack.on_disk ? (
              <span className="text-meta text-crit">
                installed, but its folder is gone from packs/
              </span>
            ) : null}
          </div>

          <p className="mt-[var(--s-2)] text-body text-ink-2">
            {pack.document_types.map((type) => type.replace(/_/g, " ")).join(" · ")}
          </p>

          <p className="mt-[var(--s-2)] flex flex-wrap gap-x-[var(--s-3)] text-meta text-ink-2">
            <span>
              <span className="num">{pack.documents}</span> document
              {pack.documents === 1 ? "" : "s"}
            </span>
            <span>
              <span className="num">{pack.facts}</span> field
              {pack.facts === 1 ? "" : "s"} read
            </span>
            {pack.reminders > 0 ? (
              <span>
                <span className="num">{pack.reminders}</span> reminder
                {pack.reminders === 1 ? "" : "s"}
              </span>
            ) : null}
            {pack.alerts > 0 ? (
              <span>
                <span className="num">{pack.alerts}</span> alert
                {pack.alerts === 1 ? "" : "s"}
              </span>
            ) : null}
            {pack.tracker ? <span>a tracker</span> : null}
          </p>
        </div>

        <Toggle
          kind="packs"
          id={pack.id}
          enabled={pack.enabled}
          label={`${pack.display_name} pack`}
        />
      </div>

      {/* Not decoration. `never_acts` is `Literal[True]` in the contract, so a pack that set
          anything else would fail to load — this says so to the person it protects. */}
      {pack.never_acts ? (
        <p className="mt-[var(--s-3)] border-t border-hairline pt-[var(--s-3)] text-meta text-ink-2">
          <span className="font-medium text-ink">Advises, never acts.</span> This pack cannot
          pay, renew, book or file anything. That is enforced by the type system rather than by
          its own good behaviour.
        </p>
      ) : null}

      {pack.disclaimer ? (
        <details className="mt-[var(--s-2)]">
          <summary className="cursor-pointer text-meta text-ink-3">
            What this pack says about its own limits
          </summary>
          <p className="mt-[var(--s-2)] max-w-[var(--measure)] text-meta text-ink-2">
            {pack.disclaimer}
          </p>
        </details>
      ) : null}
    </li>
  );
}

function ModuleRow({ module }: { module: ModuleSummary }) {
  return (
    <li className="flex items-center gap-[var(--s-3)] rounded-[var(--r)] border border-hairline bg-surface px-[var(--s-4)] py-[var(--s-3)]">
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-baseline gap-x-[var(--s-3)]">
          <h3 className="text-body font-medium capitalize">{module.id}</h3>
          <span className="num text-meta text-ink-3">v{module.version}</span>
        </div>
        <p className="mt-[var(--s-1)] text-meta text-ink-2">
          {module.runs_on === "schedule" ? "runs nightly" : "runs when a fact is written"}
          {module.surfaces.length > 0 ? ` · shows on ${module.surfaces.join(", ")}` : null}
        </p>
      </div>
      <Toggle
        kind="modules"
        id={module.id}
        enabled={module.enabled}
        label={`${module.id} module`}
      />
    </li>
  );
}
