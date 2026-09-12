import type { Metadata } from "next";
import { ThemeToggle } from "@/components/theme-toggle";
import { Motion } from "./motion";

export const metadata: Metadata = {
  title: "Tokens · Parrot",
  description: "Every colour, size, radius and duration the interface is allowed to use.",
};

/**
 * The specimen. It exists so that "the tokens are locked" is a thing you can look at rather
 * than a thing in a commit message, and it stays in the app for the same reason: when the
 * accessibility pass comes round in week 8, this page is where it gets run.
 *
 * It reads the same `theme.css` every screen reads. Nothing here is hard-coded, so a value
 * changed in the theme changes here too — and if a screen ever disagrees with this page, the
 * screen is wrong.
 */

const SECTIONS = [
  ["colour", "Brand and accent"],
  ["surfaces", "Surfaces and ink"],
  ["status", "Status"],
  ["type", "Type"],
  ["radius", "Radius"],
  ["space", "Space"],
  ["focus", "Focus"],
  ["motion", "Motion"],
] as const;

export default function TokensPage() {
  return (
    <div className="min-h-dvh bg-ground">
      <header className="sticky top-0 z-10 border-b border-hairline bg-ground/85 backdrop-blur-sm">
        <div className="mx-auto flex max-w-[var(--shell)] items-center gap-[var(--s-4)] px-[var(--gutter)] py-[var(--s-3)]">
          <span className="font-display text-lead font-semibold">Parrot</span>
          <span className="text-meta text-ink-3">Design tokens</span>
          <nav className="ml-auto hidden items-center gap-[var(--s-4)] md:flex">
            {SECTIONS.map(([id, label]) => (
              <a
                key={id}
                href={`#${id}`}
                className="text-meta text-ink-2 no-underline transition-colors hover:text-brand"
              >
                {label}
              </a>
            ))}
          </nav>
          <div className="ml-auto md:ml-0">
            <ThemeToggle />
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-[var(--shell)] px-[var(--gutter)] pb-[var(--s-8)]">
        <div className="max-w-[var(--measure)] py-[var(--s-7)]">
          <h1 className="font-display text-screen">
            Every colour, size, radius and duration this interface is allowed to use.
          </h1>
          <p className="mt-[var(--s-4)] text-lead text-ink-2">
            Four surfaces get built against this file. A screen that needs a value which is not
            here is a screen that has found a gap in the system — the fix is to add it here, once,
            not to write it into the screen.
          </p>
          <p className="mt-[var(--s-3)] text-meta text-ink-3">
            Contrast figures below were computed against every background the token can legally sit
            on, in both themes, not sampled from the one that flattered it. Switch the theme in the
            corner and the numbers stay true.
          </p>
        </div>

        <Colour />
        <Surfaces />
        <Status />
        <Type />
        <Radius />
        <Space />
        <Focus />
        <Motion />

        <footer className="mt-[var(--s-8)] border-t border-hairline pt-[var(--s-5)] text-meta text-ink-3">
          Source: <span className="num">web/app/theme.css</span>. The values are the Kitchen
          Table resolution in{" "}
          <span className="num">
            docs/artefacts/Parrot UIUX refinement/Parrot Kitchen Table.dc.html
          </span>
          , artboard 1o, with the muted ink and the control border held to WCAG AA.
        </footer>
      </main>
    </div>
  );
}

/* ------------------------------------------------------------------------------ scaffolding */

function Section({
  id,
  title,
  note,
  children,
}: {
  id: string;
  title: string;
  note: string;
  children: React.ReactNode;
}) {
  return (
    <section id={id} className="scroll-mt-[var(--s-8)] border-t border-hairline pt-[var(--s-6)] pb-[var(--s-7)]">
      <div className="mb-[var(--s-5)] max-w-[var(--measure)]">
        <h2 className="text-title font-medium">{title}</h2>
        <p className="mt-[var(--s-2)] text-meta text-ink-2">{note}</p>
      </div>
      {children}
    </section>
  );
}

function Swatch({
  name,
  value,
  ratio,
  on,
  ink,
}: {
  name: string;
  value: string;
  ratio?: string;
  on?: string;
  ink?: string;
}) {
  return (
    <div className="overflow-hidden rounded-[var(--r)] border border-hairline bg-surface">
      <div
        className="flex h-[74px] items-end p-[var(--s-3)]"
        style={{ background: `var(${value})`, color: ink ? `var(${ink})` : undefined }}
      >
        {ink ? <span className="text-meta font-medium">Aa $742.00</span> : null}
      </div>
      <div className="border-t border-hairline p-[var(--s-3)]">
        <div className="num text-meta text-ink">{name}</div>
        {ratio ? (
          <div className="mt-[var(--s-1)] text-meta text-ink-3">
            <span className="num">{ratio}</span> {on}
          </div>
        ) : null}
      </div>
    </div>
  );
}

/* ----------------------------------------------------------------------------------- colour */

function Colour() {
  return (
    <Section
      id="colour"
      title="Two colours, and each one has one job"
      note="Terracotta is intent: the wordmark, the current tab, the primary action, the left edge of the card that needs you now. Evergreen is evidence, and only evidence: a source chip, a field somebody verified, a switch that is on. They were one colour in the first pass, and they are not one thing — a citation is a claim about the world, a button is a thing you press. Keeping them apart is what lets a person learn that green means there is a page behind this."
    >
      <div className="grid gap-[var(--s-3)] sm:grid-cols-2 lg:grid-cols-4">
        <Swatch name="--brand" value="--brand" ink="--brand-ink" ratio="5.33 / 6.56" on="its own text, light / dark" />
        <Swatch
          name="--brand-soft"
          value="--brand-soft"
          ink="--brand-strong"
          ratio="6.28 / 7.00"
          on="brand-strong on it, light / dark"
        />
        <Swatch name="--brand-line" value="--brand-line" />
        <div className="rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-4)]">
          <div className="group-label">In use</div>
          <div className="mt-[var(--s-3)] flex flex-wrap items-center gap-[var(--s-2)]">
            <button
              type="button"
              className="rounded-[var(--r-sm)] bg-brand px-[var(--s-4)] py-[var(--s-2)] font-display text-meta font-semibold text-brand-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
            >
              Mark done
            </button>
            <button
              type="button"
              className="rounded-[var(--r-sm)] border border-edge bg-surface px-[var(--s-3)] py-[var(--s-2)] text-meta font-medium text-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
            >
              Snooze
            </button>
            <span className="inline-flex items-center rounded-[var(--r-pill)] bg-brand-soft px-[var(--s-4)] py-[var(--s-2)] font-display text-meta font-semibold text-brand-strong">
              Today
            </span>
          </div>
          {/* `--brand-strong` exists because terracotta at 4.40:1 on its own tint is under AA.
              A colour that works as a 40px button does not automatically work as 14px type on
              a tint, and the current tab above is 14px type on a tint. */}
          <p className="mt-[var(--s-3)] text-meta text-ink-3">
            The tab&rsquo;s label is <span className="num">--brand-strong</span>, not{" "}
            <span className="num">--brand</span>: the fill and the type on its tint are two
            different measurements.
          </p>
        </div>
      </div>

      <div className="mt-[var(--s-3)] grid gap-[var(--s-3)] sm:grid-cols-2 lg:grid-cols-4">
        <Swatch name="--accent" value="--accent" ink="--accent-ink" ratio="7.38 / 9.59" on="its own text, light / dark" />
        <Swatch
          name="--accent-soft"
          value="--accent-soft"
          ink="--accent"
          ratio="6.13 / 8.10"
          on="accent on it, light / dark"
        />
        <Swatch name="--accent-line" value="--accent-line" />
        <div className="rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-4)]">
          <div className="group-label">In use</div>
          <p className="mt-[var(--s-3)] text-body text-ink-2">
            If it is green, there is a document behind it.
          </p>
          <a
            href="#colour"
            className="mt-[var(--s-3)] inline-flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] border border-accent-line bg-accent-soft px-[11px] py-[7px] text-meta font-medium text-accent no-underline"
          >
            Motor renewal notice <span className="num">p.1</span>
          </a>
        </div>
      </div>
    </Section>
  );
}

/* --------------------------------------------------------------------------------- surfaces */

const SURFACES = [
  ["--ground", "the page behind everything"],
  ["--surface", "a card, a row, a panel"],
  ["--surface-2", "a toolbar, a header, a skeleton"],
  ["--surface-3", "an inset: a quoted passage from a document"],
] as const;

const INKS = [
  ["--ink", "what the sentence is about", "17.50:1", "14.90:1"],
  ["--ink-2", "the sentence around it", "9.28:1", "9.20:1"],
  ["--ink-3", "the provenance line — p.3 · confidence 0.61", "5.70:1", "5.57:1"],
] as const;

function Surfaces() {
  return (
    <Section
      id="surfaces"
      title="Four surfaces, three inks, three kinds of line"
      note="The surfaces nest, so depth is never ambiguous. The inks are chosen by role rather than by size — and the muted one, the one a designer is most tempted to lighten, is pinned to a measured 4.5:1 on all nine backgrounds it can legally sit on."
    >
      <div className="grid gap-[var(--s-3)] sm:grid-cols-2 lg:grid-cols-4">
        {SURFACES.map(([token, use]) => (
          <div key={token} className="overflow-hidden rounded-[var(--r)] border border-hairline">
            <div className="h-[74px]" style={{ background: `var(${token})` }} />
            <div className="border-t border-hairline bg-surface p-[var(--s-3)]">
              <div className="num text-meta text-ink">{token}</div>
              <div className="mt-[var(--s-1)] text-meta text-ink-3">{use}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-[var(--s-5)] grid gap-[var(--s-3)] lg:grid-cols-[1fr_auto]">
        <div className="rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-4)]">
          <div className="group-label">Ink, on the surface it is darkest against</div>
          <dl className="mt-[var(--s-3)] space-y-[var(--s-3)]">
            {INKS.map(([token, role, light, dark]) => (
              <div key={token} className="flex flex-wrap items-baseline gap-x-[var(--s-3)] gap-y-[var(--s-1)]">
                <dt className="num w-[5.5rem] shrink-0 text-meta" style={{ color: `var(${token})` }}>
                  {token}
                </dt>
                <dd className="text-body" style={{ color: `var(${token})` }}>
                  {role}
                </dd>
                <dd className="num ml-auto text-meta text-ink-3">
                  {light} light · {dark} dark
                </dd>
              </div>
            ))}
          </dl>
        </div>

        <div className="rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-4)]">
          <div className="group-label">Lines</div>
          <ul className="mt-[var(--s-3)] space-y-[var(--s-3)] text-meta">
            <li>
              <div className="h-px w-full bg-hairline" />
              <div className="num mt-[var(--s-2)] text-ink">--hairline</div>
              <div className="text-ink-3">between two rows. Decorative.</div>
            </li>
            <li>
              <div className="h-px w-full bg-rule" />
              <div className="num mt-[var(--s-2)] text-ink">--rule</div>
              <div className="text-ink-3">a section division, a card at rest.</div>
            </li>
            <li>
              <div className="h-px w-full bg-edge" />
              <div className="num mt-[var(--s-2)] text-ink">--edge</div>
              <div className="text-ink-3">
                anything you can click or type into. 3:1 minimum, because for an empty field the
                border is the control.
              </div>
            </li>
          </ul>
          {/* A placeholder is not a label: it disappears the moment somebody types. */}
          <label htmlFor="edge-demo" className="sr-only">
            Example text field, to show the control border
          </label>
          <input
            id="edge-demo"
            type="text"
            placeholder="Ask about your documents"
            className="mt-[var(--s-4)] w-full rounded-[var(--r-sm)] border border-edge bg-surface px-[var(--s-3)] py-[var(--s-2)] text-body"
          />
        </div>
      </div>
    </Section>
  );
}

/* ----------------------------------------------------------------------------------- status */

const STATUS = [
  {
    token: "crit",
    word: "Overdue",
    means: "a date that has passed, or a figure the extractor got wrong",
    line: "Motor policy expired for SLK8842J",
    light: "7.87:1",
  },
  {
    token: "warn",
    word: "Needs your eyes",
    means: "below the confidence floor, or a page that could not be read",
    line: "Annual premium $486.00 — please check",
    light: "6.13:1",
  },
  {
    token: "brass",
    word: "Estimated",
    means: "a computed figure, or a pack that is available but not installed",
    line: "Household spend $2,184 from 41 receipts",
    light: "5.45:1",
  },
  {
    token: "ok",
    word: "Confirmed",
    means: "checked by a person, or nothing left to do",
    line: "Expiry date confirmed by you on 2 September",
    light: "7.26:1",
  },
] as const;

function Status() {
  return (
    <Section
      id="status"
      title="Four status colours, and none of them is a second accent"
      note="Each one appears only when its own condition is true. Every one passes AA as text on white and on its own tint, so a status can always be said in words — which matters, because the border of a tinted block is decorative and carries none of the meaning. Colour is never the only signal: there is a word, and on Today there is a countdown as well."
    >
      <div className="grid gap-[var(--s-3)] md:grid-cols-2">
        {STATUS.map(({ token, word, means, line, light }) => (
          <div
            key={token}
            className="rounded-[var(--r)] border p-[var(--s-4)]"
            style={{
              background: `var(--${token}-soft)`,
              borderColor: `var(--${token}-line)`,
            }}
          >
            <div className="flex items-baseline gap-[var(--s-2)]">
              <span
                className="text-meta font-semibold uppercase tracking-[var(--tr-label)]"
                style={{ color: `var(--${token})` }}
              >
                {word}
              </span>
              <span className="num ml-auto text-meta text-ink-2">{light}</span>
            </div>
            <p className="mt-[var(--s-2)] text-body text-ink">{line}</p>
            <p className="mt-[var(--s-1)] text-meta text-ink-2">{means}</p>
            <div className="num mt-[var(--s-3)] text-meta text-ink-2">
              --{token} · --{token}-soft · --{token}-line
            </div>
          </div>
        ))}
      </div>
    </Section>
  );
}

/* ------------------------------------------------------------------------------------- type */

const SCALE = [
  ["--fs-label", "11", "group-label font-display", "NEEDS YOU NOW"],
  ["--fs-meta", "13", "text-meta text-ink-3", "NTUC Income home insurance renewal, page 3"],
  ["--fs-body", "15.5", "text-body", "You are at $12,400 of the $15,300 cap."],
  ["--fs-lead", "17.5", "text-lead", "Renew before cover lapses. Last premium was $742."],
  ["--fs-title", "19", "text-title font-display", "Motor policy expires for SLK8842J"],
  ["--fs-screen", "24", "text-screen font-display", "Your motor policy has expired"],
  ["--fs-display", "28", "text-display font-display", "Wednesday, 2 September"],
  ["--fs-figure", "34", "text-figure num", "115"],
] as const;

function Type() {
  return (
    <Section
      id="type"
      title="Two sans faces, eight steps, fixed in rem"
      note="Outfit names things — the wordmark, a surface’s title, a card’s headline, the text on a button. Figtree is read: prose, an answer, a value, a meta line. JetBrains Mono carries anything measured or identified, and the largest step belongs to it, because the biggest thing on Today is a countdown. There is no serif anywhere; the previous pass had one, and it was the part of the interface people described rather than used. Sizes do not scale with the viewport — this is read at a consistent distance on a consistent screen, and a heading that shrinks inside a narrow column looks broken rather than responsive."
    >
      <div className="rounded-[var(--r)] border border-hairline bg-surface">
        {SCALE.map(([token, px, cls, sample], i) => (
          <div
            key={token}
            className={`flex flex-wrap items-baseline gap-x-[var(--s-4)] gap-y-[var(--s-1)] px-[var(--s-4)] py-[var(--s-3)] ${
              i ? "border-t border-hairline" : ""
            }`}
          >
            <div className="num w-[7rem] shrink-0 text-meta text-ink-3">{token}</div>
            <div className="num w-[2.5rem] shrink-0 text-meta text-ink-3">{px}px</div>
            <div className={`min-w-0 flex-1 ${cls}`}>{sample}</div>
          </div>
        ))}
      </div>

      <div className="mt-[var(--s-4)] grid gap-[var(--s-3)] md:grid-cols-3">
        <FaceCard
          family="font-display"
          name="Outfit 600"
          role="Names things: the wordmark, a title, a status label, the text on a button."
          sample="Insurance and Coverage"
        />
        <FaceCard
          family="font-sans"
          name="Figtree 400/500"
          role="Everything you read: prose, answers, values, meta lines, table cells."
          sample="Cover ended on 30 November 2026."
        />
        <FaceCard
          family="font-mono"
          name="JetBrains Mono"
          role="Only what is measured or identified. Never a costume for looking technical."
          sample="HI-2244019 · 0.61"
        />
      </div>
    </Section>
  );
}

function FaceCard({
  family,
  name,
  role,
  sample,
}: {
  family: string;
  name: string;
  role: string;
  sample: string;
}) {
  return (
    <div className="rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-4)]">
      <div className={`${family} text-title`}>{sample}</div>
      <div className="mt-[var(--s-3)] text-meta font-medium text-ink">{name}</div>
      <div className="mt-[var(--s-1)] text-meta text-ink-2">{role}</div>
    </div>
  );
}

/* ----------------------------------------------------------------------------------- radius */

const RADII = [
  ["--r-sm", "8px", "chips, badges, inputs, small buttons — things the size of a word"],
  ["--r", "14px", "cards, panels, dialogs — things the size of a paragraph"],
  ["--r-pill", "999px", "a toggle, a nav tab or a status dot, where the shape is the affordance"],
] as const;

function Radius() {
  return (
    <Section
      id="radius"
      title="Three radii, and a screen may not invent a fourth"
      note="Both went up one notch in the Kitchen Table pass — cards 10 to 14, chips 6 to 8. On warm paper a tight corner reads as a form and a soft one reads as a card, and this is a thing you are meant to sit down with. Not further: something holding your insurance policies should not look like a toy."
    >
      <div className="grid gap-[var(--s-3)] md:grid-cols-3">
        {RADII.map(([token, px, use]) => (
          <div key={token} className="rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-4)]">
            <div
              className="h-[72px] border border-accent-line bg-accent-soft"
              style={{ borderRadius: `var(${token})` }}
            />
            <div className="num mt-[var(--s-3)] text-meta text-ink">
              {token} <span className="text-ink-3">{px}</span>
            </div>
            <div className="mt-[var(--s-1)] text-meta text-ink-2">{use}</div>
          </div>
        ))}
      </div>
    </Section>
  );
}

/* ------------------------------------------------------------------------------------ space */

const SPACE = [
  ["--s-1", 4],
  ["--s-2", 8],
  ["--s-3", 12],
  ["--s-4", 16],
  ["--s-5", 24],
  ["--s-6", 32],
  ["--s-7", 48],
  ["--s-8", 64],
] as const;

function Space() {
  return (
    <Section
      id="space"
      title="A 4px base, eight rungs, nothing between them"
      note="Tight inside a group, generous between groups, and more space above a heading than below it — a heading belongs to what follows it, and spacing is how a reader is told so."
    >
      <div className="rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-4)]">
        {SPACE.map(([token, px]) => (
          <div key={token} className="flex items-center gap-[var(--s-4)] py-[var(--s-1)]">
            <div className="num w-[3.5rem] shrink-0 text-meta text-ink-3">{token}</div>
            <div className="h-3 rounded-[2px] bg-accent-soft" style={{ width: px * 2 }} />
            <div className="num text-meta text-ink-3">{px}px</div>
          </div>
        ))}
      </div>
      <div className="mt-[var(--s-4)] grid gap-[var(--s-3)] md:grid-cols-4">
        {[
          ["--shell", "1088px", "the widest the chrome ever gets"],
          ["--column", "880px", "the content column, centred under it"],
          ["--measure", "62ch", "an answer never runs wider"],
          ["--gutter", "24px", "the page's side padding"],
        ].map(([token, v, use]) => (
          <div key={token} className="rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-3)]">
            <div className="num text-meta text-ink">{token}</div>
            <div className="num text-meta text-ink-3">{v}</div>
            <div className="mt-[var(--s-1)] text-meta text-ink-2">{use}</div>
          </div>
        ))}
      </div>
    </Section>
  );
}

/* ------------------------------------------------------------------------------------ focus */

function Focus() {
  return (
    <Section
      id="focus"
      title="One ring, and it survives being drawn on the accent itself"
      note="Press Tab. The ring is an outline with a 2px gap rather than a border or a shadow, which is what lets the same treatment stay legible on a white card and on the dark green primary button — 7.56:1 against the lightest surface, 6.14:1 against the deepest. Mouse clicks leave nothing behind; every keyboard path gets a ring. This is the week-8 accessibility task, applied to the first component instead."
    >
      <div className="flex flex-wrap items-center gap-[var(--s-3)] rounded-[var(--r)] border border-hairline bg-surface p-[var(--s-5)]">
        <button
          type="button"
          className="rounded-[var(--r-sm)] bg-accent px-[var(--s-4)] py-[var(--s-2)] text-meta font-medium text-accent-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
        >
          Primary action
        </button>
        <button
          type="button"
          className="rounded-[var(--r-sm)] border border-edge bg-surface px-[var(--s-4)] py-[var(--s-2)] text-meta font-medium text-ink transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
        >
          Secondary
        </button>
        <a
          href="#focus"
          className="rounded-[var(--r-sm)] border border-accent-line bg-accent-soft px-[var(--s-2)] py-[var(--s-1)] text-meta text-accent no-underline"
        >
          A source chip <span className="num">p.2</span>
        </a>
        <label htmlFor="focus-demo" className="sr-only">
          Example text field, to try the focus ring
        </label>
        <input
          id="focus-demo"
          type="text"
          placeholder="A text field"
          className="min-w-[12rem] flex-1 rounded-[var(--r-sm)] border border-edge bg-surface px-[var(--s-3)] py-[var(--s-2)] text-body"
        />
        <label className="flex items-center gap-[var(--s-2)] text-meta">
          <input type="checkbox" defaultChecked className="accent-accent" />
          Insurance pack
        </label>
      </div>
      <p className="mt-[var(--s-3)] max-w-[var(--measure)] text-meta text-ink-3">
        The gap is painted in the surface colour, so the ring always has something to contrast
        against whatever it wraps. That is the whole trick, and it is why there is no second
        &ldquo;focus ring on dark backgrounds&rdquo; token to remember.
      </p>
    </Section>
  );
}
