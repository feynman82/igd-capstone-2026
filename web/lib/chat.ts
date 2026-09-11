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
 *   …anything → error                     the stream broke after it began
 */
export type ParrotMessage = UIMessage<
  never,
  {
    /** Evidence gathered and above the pack's floor. Nothing is claimed yet. */
    reading: { passages_read: number };

    /** One verified sentence. It will not be withdrawn, reworded or re-cited. */
    sentence: { text: string; chunk_ids: number[]; citations: Source[] };

    /** A designed state, not an error. Says why, and what document would have answered. */
    abstention: {
      reason: string;
      missing: string;
      passages_read: number;
      dropped: number;
    };

    /** `never_acts` is `Literal[True]` in every pack. This is that, surfaced. */
    refusal: { text: string };

    /** The trace line under a finished answer, and the pack's disclaimer. */
    finished: { disclaimer: string; passages_read: number; dropped: number };

    /** The connection died mid-answer. Sentences already shown stay; they were verified. */
    error: { detail: string };
  }
>;
