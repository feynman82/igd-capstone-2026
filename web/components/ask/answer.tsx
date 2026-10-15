"use client";

import { Ban, CircleSlash, FileQuestion, Scale } from "lucide-react";
import { AdviceCard, AdviceWithheld } from "@/components/ask/advice-card";
import { ConsentPrompt } from "@/components/ask/consent-prompt";
import { DraftCard } from "@/components/ask/draft-card";
import { SourceChip } from "@/components/source-chip";
import type {
  AdviceCardEvent,
  AdviceWithheldEvent,
  ConsentRequiredEvent,
  DraftEvent,
} from "@/lib/api";
import type { ParrotMessage } from "@/lib/chat";

/**
 * One turn of the conversation, rendered from parts that are already verified.
 *
 * There is no string of prose here to render. A sentence arrived with its citations attached
 * and is drawn with them; there is no code path in this file that can produce a factual
 * sentence without a chip beside it, which is rule 3 surviving all the way to the pixel.
 */

type Part = NonNullable<ParrotMessage["parts"]>[number];

export function Turn({
  message,
  question = "",
  busy = false,
  onConsented,
}: {
  message: ParrotMessage;
  /** The question this turn answers. A consent prompt asks it again once the owner agrees. */
  question?: string;
  /** Another answer is still arriving. */
  busy?: boolean;
  /** Sends `question` again. Owned by the conversation, which owns `useChat`. */
  onConsented?: (question: string) => void;
}) {
  if (message.role === "user") {
    return (
      <li className="flex justify-end">
        <p className="max-w-[85%] rounded-[var(--r)] rounded-br-[var(--r-sm)] bg-surface-2 px-[var(--s-4)] py-[var(--s-3)] text-body">
          {textOf(message)}
        </p>
      </li>
    );
  }

  const parts = (message.parts ?? []) as Part[];
  const sentences = parts.filter((part) => part.type === "data-sentence");
  const abstention = parts.find((part) => part.type === "data-abstention");
  const refusal = parts.find((part) => part.type === "data-refusal");
  const declined = parts.find((part) => part.type === "data-declined");
  const finished = parts.find((part) => part.type === "data-finished");
  const failure = parts.find((part) => part.type === "data-error");
  const reading = parts.find((part) => part.type === "data-reading");
  // Advice (ADR 0016). The stream is the only source of the card: nothing here is fetched or
  // rebuilt from `/api/ask`, which carries no figures, inputs or rows.
  const advice = parts.find((part) => part.type === "data-advice") as
    | { data: Omit<AdviceCardEvent, "kind"> }
    | undefined;
  const consent = parts.find((part) => part.type === "data-consent_required") as
    | { data: Omit<ConsentRequiredEvent, "kind"> }
    | undefined;
  const withheld = parts.find((part) => part.type === "data-advice_withheld") as
    | { data: Omit<AdviceWithheldEvent, "kind"> }
    | undefined;
  // A calendar request (ADR 0020), drafted rather than done. The card is the whole answer.
  const draft = parts.find((part) => part.type === "data-draft") as
    | { data: Omit<DraftEvent, "kind"> }
    | undefined;
  // A consent prompt, withheld advice and a draft are the whole answer: no `finished` follows,
  // and the turn is over the moment one arrives.
  const settled = Boolean(
    abstention || failure || declined || refusal || advice || consent || withheld || draft,
  );

  // A calendar answer (ADR 0020) is read off the rows by code; its footer must not claim a model.
  const fromCalendar =
    sentences.length > 0 &&
    sentences.every((part) =>
      (part as { data: { citations: { kind?: string }[] } }).data.citations.every(
        (source) => source.kind === "calendar" || source.kind === "document",
      ),
    ) &&
    sentences.some((part) =>
      (part as { data: { citations: { kind?: string }[] } }).data.citations.some(
        (source) => source.kind === "calendar",
      ),
    );

  // Whose answer this is, when the question was first-person and the evidence was narrowed to
  // one member of the household. Shown for exactly the reason a citation is shown: the defence
  // against answering about the wrong person is putting the person on the screen that used
  // them, not being careful. A wrong alias is then a thing you can see. See ADR 0011.
  const person = (
    [finished, abstention, reading].find(
      (part) => part && (part as { data: { person?: string | null } }).data.person,
    ) as { data: { person?: string | null } } | undefined
  )?.data.person;

  return (
    /*
     * `aria-live="polite"` on the assistant's turn, and this is not decoration either.
     *
     * The answer arrives one verified sentence at a time. Somebody watching the screen sees
     * that happen; somebody listening would otherwise hear nothing at all until they went
     * looking. `polite` rather than `assertive` so it waits for a gap rather than cutting in,
     * and not `atomic` so each new sentence is read on its own rather than re-reading the whole
     * answer every time one lands.
     */
    <li className="max-w-[var(--measure)]" aria-live="polite" aria-atomic="false">
      {/* Between the question and the first sentence. Not a spinner — a sentence about what is
          happening, because on a 4B model this is several seconds and "reading 6 passages" is
          more reassuring than a shape going round. */}
      {reading && sentences.length === 0 && !settled ? (
        <p className="flex items-center gap-[var(--s-2)] text-meta text-ink-3">
          <span aria-hidden className="inline-block size-1.5 animate-pulse rounded-full bg-accent" />
          Reading {(reading as { data: { passages_read: number } }).data.passages_read} passages
        </p>
      ) : null}

      {/* The advice card names its person in its own heading. */}
      {advice ? (
        <div className="mb-[var(--s-3)]">
          <AdviceCard advice={advice.data} />
        </div>
      ) : null}

      {person && sentences.length > 0 && !advice ? (
        <p className="mb-[var(--s-3)] flex items-center gap-[var(--s-2)] text-meta text-ink-3">
          <span className="rounded-[var(--r-sm)] border border-hairline bg-surface-2 px-[var(--s-2)] py-[2px] font-medium text-ink-2">
            for {person}
          </span>
          <span>only their documents were read</span>
        </p>
      ) : null}

      {sentences.map((part, index) => {
        const { text, citations } = (
          part as { data: { text: string; citations: Parameters<typeof SourceChip>[0]["source"][] } }
        ).data;
        return (
          <p
            key={index}
            style={{ animation: "parrot-rise var(--dur-chip) var(--ease) both" }}
            className="mt-[var(--s-2)] text-lead first:mt-0"
          >
            {text}{" "}
            <span className="inline-flex flex-wrap gap-[var(--s-1)] align-middle">
              {citations.map((source, at) => (
                <SourceChip key={at} source={source} />
              ))}
            </span>
          </p>
        );
      })}

      {abstention ? <Abstention part={abstention} /> : null}
      {refusal ? <Refusal part={refusal} /> : null}
      {declined ? <Declined part={declined} /> : null}
      {consent ? (
        <ConsentPrompt
          consent={consent.data}
          busy={busy}
          onConsented={() => onConsented?.(question)}
        />
      ) : null}
      {withheld ? <AdviceWithheld withheld={withheld.data} /> : null}
      {draft ? <DraftCard draft={draft.data} /> : null}
      {failure ? <Broken part={failure} /> : null}

      {finished && (sentences.length > 0 || advice) ? (
        <Trace part={finished} advised={Boolean(advice)} calendar={fromCalendar} />
      ) : null}
    </li>
  );
}

// core/graph/answer.py's `WHOSE_REASON`: advice held back because a question could be about more
// than one household member, not because no document answers it. The abstain event carries no
// field saying which kind of abstention it is, so the reason core sends is matched here, in this
// one place, rather than showing "no document" copy that would misdescribe why Parrot stopped.
// If core's wording changes, this card falls back to the no-document copy.
const WHOSE_REASON = "the question could be about more than one person";

/**
 * Silence beats a guess, and it is designed as a considered state rather than as a failure.
 *
 * Brass, not red. It names why it declined and what would have answered. A person reading this
 * should feel that the system held a line, not that something went wrong — that is the whole
 * reason the trust story works, and a red error box would undo it.
 */
function Abstention({ part }: { part: Part }) {
  const data = (
    part as {
      data: {
        reason: string;
        missing: string;
        passages_read: number;
        dropped: number;
        disclaimer?: string;
      };
    }
  ).data;
  const whoseQuestion = data.reason === WHOSE_REASON;

  return (
    <div className="rounded-[var(--r)] border border-brass-line bg-brass-soft p-[var(--s-4)]">
      <div className="flex items-center gap-[var(--s-2)]">
        <FileQuestion aria-hidden size={16} strokeWidth={2} className="text-brass" />
        <h3 className="text-label font-semibold tracking-[var(--tr-label)] text-brass uppercase">
          {whoseQuestion ? "Whose situation this is about" : "No document supports an answer"}
        </h3>
      </div>
      <p className="mt-[var(--s-2)] text-lead text-ink">
        {whoseQuestion ? (
          sentence(data.reason)
        ) : (
          <>I do not have a document that answers this. {sentence(data.reason)}</>
        )}
      </p>
      {data.missing ? (
        <p className="mt-[var(--s-2)] text-body text-ink-2">{sentence(data.missing)}</p>
      ) : null}
      <p className="mt-[var(--s-3)] text-meta text-ink-2">
        <span className="num">{data.passages_read}</span> passage
        {data.passages_read === 1 ? "" : "s"} read
        {data.dropped > 0 ? (
          <>
            {" · "}
            <span className="num">{data.dropped}</span> sentence
            {data.dropped === 1 ? "" : "s"} written and dropped for having no source
          </>
        ) : null}
        {" · nothing was invented to fill the gap"}
      </p>
      {data.disclaimer ? (
        <p className="mt-[var(--s-2)] text-meta text-ink-2">{data.disclaimer}</p>
      ) : null}
    </div>
  );
}

/** `never_acts` is `Literal[True]` in every pack manifest. This is that reaching a person. */
function Refusal({ part }: { part: Part }) {
  const { text } = (part as { data: { text: string } }).data;
  return (
    <div className="rounded-[var(--r)] border border-hairline bg-surface-2 p-[var(--s-4)]">
      <div className="flex items-center gap-[var(--s-2)]">
        <Ban aria-hidden size={16} strokeWidth={2} className="text-ink-2" />
        <h3 className="text-label font-semibold tracking-[var(--tr-label)] text-ink-2 uppercase">
          Parrot does not act
        </h3>
      </div>
      <p className="mt-[var(--s-2)] text-lead text-ink">{text}</p>
    </div>
  );
}

/**
 * A pack without advice declines a recommendation. This is that reaching a person — and it
 * offers the question it *can* answer rather than answering it, because a summary of a policy
 * placed under "should I buy?" reads as a yes or a no.
 */
function Declined({ part }: { part: Part }) {
  const { text, disclaimer, offer } = (
    part as { data: { text: string; disclaimer: string; offer: string } }
  ).data;
  return (
    <div className="rounded-[var(--r)] border border-hairline bg-surface-2 p-[var(--s-4)]">
      <div className="flex items-center gap-[var(--s-2)]">
        <Scale aria-hidden size={16} strokeWidth={2} className="text-ink-2" />
        <h3 className="text-label font-semibold tracking-[var(--tr-label)] text-ink-2 uppercase">
          Parrot explains, it does not recommend
        </h3>
      </div>
      <p className="mt-[var(--s-2)] text-lead text-ink">{text}</p>
      {offer ? (
        <p className="mt-[var(--s-2)] text-body text-ink-2">
          You could ask: <span className="text-ink">{offer}</span>
        </p>
      ) : null}
      {disclaimer ? <p className="mt-[var(--s-3)] text-meta text-ink-2">{disclaimer}</p> : null}
    </div>
  );
}

function Broken({ part }: { part: Part }) {
  const { detail } = (part as { data: { detail: string } }).data;
  return (
    <div className="mt-[var(--s-3)] rounded-[var(--r)] border border-crit-line bg-crit-soft p-[var(--s-4)]">
      <div className="flex items-center gap-[var(--s-2)]">
        <CircleSlash aria-hidden size={16} strokeWidth={2} className="text-crit" />
        <h3 className="text-body font-medium text-ink">Parrot stopped answering</h3>
      </div>
      <p className="mt-[var(--s-1)] text-meta text-ink-2">{detail}</p>
    </div>
  );
}

/**
 * The line beneath a finished answer.
 *
 * Worth leaving on. It is what lets the system account for itself — how many passages it read,
 * how many sentences it wrote and then refused to show. A reader who can see that number trusts
 * the ones that got through more, not less.
 */
function Trace({
  part,
  advised = false,
  calendar = false,
}: {
  part: Part;
  advised?: boolean;
  /** Every sentence was read off the calendar by code (ADR 0020): no passage, no model. */
  calendar?: boolean;
}) {
  const data = (
    part as {
      data: {
        disclaimer: string;
        passages_read: number;
        dropped: number;
        quarantined?: number;
        truncated?: boolean;
        unanswered?: boolean;
      };
    }
  ).data;
  return (
    <div className="mt-[var(--s-4)] border-t border-hairline pt-[var(--s-3)]">
      <p className="text-meta text-ink-3">
        {/* After advice the "passages" are the card's own inputs, so the line says that. */}
        {calendar ? (
          "read off your calendar by code, not written by a model"
        ) : advised ? (
          "explained from the inputs on the card"
        ) : (
          <>
            answered from <span className="num">{data.passages_read}</span> passage
            {data.passages_read === 1 ? "" : "s"}
          </>
        )}
        {data.dropped > 0 ? (
          <>
            {" · "}
            <span className="num">{data.dropped}</span> unsourced sentence
            {data.dropped === 1 ? "" : "s"} dropped
          </>
        ) : null}
        {data.truncated ? " · shortened to the pack's limit" : null}
        {data.unanswered ? " · the pages read do not answer the rest of this question" : null}
        {data.quarantined ? (
          <>
            {" · "}
            <span className="num">{data.quarantined}</span> document
            {data.quarantined === 1 ? "" : "s"} in quarantine not checked
          </>
        ) : null}
        {calendar ? " · nothing left this computer" : " · local model, nothing left this computer"}
      </p>
      {/* Advice already shows its disclaimer on the card, where it cannot be missed. */}
      {data.disclaimer && !advised ? (
        <p className="mt-[var(--s-2)] text-meta text-ink-2">{data.disclaimer}</p>
      ) : null}
    </div>
  );
}

function textOf(message: ParrotMessage): string {
  return (message.parts ?? [])
    .filter((part) => part.type === "text")
    .map((part) => (part as { text: string }).text)
    .join(" ");
}

/** The modules and the gate write lower-case fragments; a sentence on screen starts with a capital. */
function sentence(text: string): string {
  if (!text) return "";
  const trimmed = text.trim();
  const capitalised = trimmed.charAt(0).toUpperCase() + trimmed.slice(1);
  return /[.!?]$/.test(capitalised) ? capitalised : `${capitalised}.`;
}
