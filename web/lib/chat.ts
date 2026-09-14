import type { UIMessage } from "ai";
import type { Source } from "@/lib/api";

/**
 * The shape of an answer in the interface.
 *
 * Parrot does not stream prose, so this is not a text message with citations bolted on. The
 * model writes each sentence together with the passages backing it, the gate verifies one
 * sentence at a time, and what reaches the browser is a sequence of *verified units*. Modelling
 * them as the AI SDK's typed data parts rather than as text is what keeps that true all the way
 * to the screen: there is no field on this type that can hold an unverified sentence.
 *
 * The parts arrive in this order and no other:
 *
 *   reading → sentence* → finished        an answer
 *   abstention                            nothing in the vault supports one
 *   refusal                               a request to act, refused at the router
 *   declined                              a request for advice, declined at the router
 *   …anything → error                     the stream broke after it began
 */
export type ParrotMessage = UIMessage<
  never,
  {
    /**
     * Evidence gathered and above the pack's floor. Nothing is claimed yet.
     *
     * `person` is set when the question was first-person and the evidence was narrowed to one
     * member of the household. It is shown for the same reason a citation is: the defence
     * against answering about the wrong person is showing whose answer this is.
     */
    reading: { passages_read: number; person?: string | null };

    /** One verified sentence. It will not be withdrawn, reworded or re-cited. */
    sentence: { text: string; chunk_ids: number[]; citations: Source[] };

    /** A designed state, not an error. Says why, and what document would have answered. */
    abstention: {
      reason: string;
      missing: string;
      passages_read: number;
      dropped: number;
      person?: string | null;
      disclaimer?: string;
    };

    /** `never_acts` is `Literal[True]` in every pack. This is that, surfaced. */
    refusal: { text: string };

    /** A request for a recommendation or a judgement. `never_recommends`, surfaced. */
    declined: { text: string; disclaimer: string; offer: string };

    /** The trace line under a finished answer, and the pack's disclaimer. */
    finished: {
      disclaimer: string;
      passages_read: number;
      dropped: number;
      person?: string | null;
      quarantined?: number;
      truncated?: boolean;
      /** Only a line about the documents on file was said; the pages read did not answer. */
      unanswered?: boolean;
    };

    /** The connection died mid-answer. Sentences already shown stay; they were verified. */
    error: { detail: string };
  }
>;
