"use client";

import { FileWarning, ImageOff, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { pageImage, type Source } from "@/lib/api";

/**
 * The chip, and the page it opens. The trust surface of the whole product.
 *
 * It names the document and the page, never an index number, because "[3]" asks a person to
 * trust a footnote and "Motor renewal notice, p.1" tells them what to go and look at. Pressing
 * it opens that page, drawn, with the claim still on screen behind it — checking a claim should
 * not cost you the claim.
 *
 * A chip whose document could not be resolved is rendered as plain text rather than as a dead
 * button. The sentence still says what it said; it simply is not a link, which is the honest
 * outcome for a document somebody has since deleted.
 *
 * The panel grows out of the chip that opened it, which is the one piece of choreography on
 * this surface: `transform-origin` is set from the chip's own position so the page appears to
 * come from the thing that was pressed rather than from the middle of the screen.
 */
export function SourceChip({ source }: { source: Source }) {
  const [open, setOpen] = useState(false);
  const chip = useRef<HTMLButtonElement>(null);

  const openable = source.document_id !== null && source.page !== null;

  if (!openable) {
    return (
      <span className="inline-flex items-center gap-[var(--s-1)] rounded-[var(--r-sm)] border border-hairline px-[11px] py-[7px] text-meta text-ink-3">
        {source.text}
      </span>
    );
  }

  return (
    <>
      <button
        ref={chip}
        type="button"
        onClick={() => setOpen(true)}
        className="inline-flex items-center gap-[var(--s-2)] rounded-[var(--r-sm)] border border-accent-line bg-accent-soft px-[11px] py-[7px] text-meta font-medium text-accent transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
      >
        <span className="truncate">{source.document_name}</span>
        <span className="num">p.{source.page}</span>
      </button>

      {open ? (
        <SourcePanel
          source={source}
          onClose={() => {
            setOpen(false);
            // Focus goes back to what opened it. Losing your place in a list of eight rows
            // because you checked one citation is the whole reason people stop checking.
            chip.current?.focus();
          }}
        />
      ) : null}
    </>
  );
}

function SourcePanel({ source, onClose }: { source: Source; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [state, setState] = useState<"loading" | "shown" | "gone" | "norender" | "error">(
    "loading",
  );
  const [detail, setDetail] = useState("");

  useEffect(() => {
    dialog.current?.showModal();
  }, []);

  useEffect(() => {
    // Asked for before it is drawn, so a document whose file has left the inbox says so instead
    // of showing a broken image icon — the browser's own failure glyph belongs to no design
    // system and explains nothing.
    let live = true;
    const url = pageImage(source.document_id!, source.page!);

    fetch(url)
      .then(async (response) => {
        if (!live) return;
        if (response.ok) {
          setState("shown");
          return;
        }
        const body = (await response.json().catch(() => null)) as { detail?: string } | null;
        setDetail(body?.detail ?? "");
        setState(response.status === 409 ? "gone" : response.status === 501 ? "norender" : "error");
      })
      .catch(() => live && setState("error"));

    return () => {
      live = false;
    };
  }, [source]);

  return (
    <dialog
      ref={dialog}
      onClose={onClose}
      // The backdrop closes it, which is what everyone expects of a panel over a page.
      onClick={(event) => event.target === dialog.current && dialog.current?.close()}
      aria-label={`${source.document_name}, page ${source.page}`}
      className="m-auto w-[min(52rem,92vw)] rounded-[var(--r)] border border-hairline bg-surface p-0 text-ink shadow-lift-2 backdrop:bg-[rgb(27_24_20/0.5)]"
    >
      <div className="flex items-center gap-[var(--s-3)] border-b border-hairline px-[var(--s-4)] py-[var(--s-3)]">
        <div className="min-w-0">
          <p className="truncate text-body font-medium">{source.document_name}</p>
          <p className="num text-meta text-ink-3">Page {source.page}</p>
        </div>
        <button
          type="button"
          onClick={() => dialog.current?.close()}
          className="ml-auto grid size-8 shrink-0 place-items-center rounded-[var(--r-sm)] text-ink-3 transition-colors hover:bg-surface-2 hover:text-ink"
        >
          <X aria-hidden size={16} />
          <span className="sr-only">Close</span>
        </button>
      </div>

      <div className="max-h-[70vh] overflow-auto bg-surface-3 p-[var(--s-4)]">
        {state === "loading" ? <div className="skeleton aspect-[1/1.414] w-full" /> : null}

        {state === "shown" ? (
          // A document page is not a static asset; it is drawn on demand from a file this app
          // is not allowed to index.
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={pageImage(source.document_id!, source.page!)}
            alt={`Page ${source.page} of ${source.document_name}`}
            className="mx-auto w-full rounded-[var(--r-sm)] border border-hairline bg-white"
          />
        ) : null}

        {state === "gone" ? (
          <PanelMessage
            Icon={FileWarning}
            title="The file is not in your inbox any more"
            detail={
              detail ||
              "Parrot still knows what this document said, but it cannot show you the page."
            }
          />
        ) : null}

        {state === "norender" ? (
          <PanelMessage
            Icon={ImageOff}
            title="This install cannot draw PDF pages"
            detail={detail}
          />
        ) : null}

        {state === "error" ? (
          <PanelMessage
            Icon={ImageOff}
            title="That page could not be opened"
            detail={detail || "Parrot did not answer."}
          />
        ) : null}
      </div>
    </dialog>
  );
}

function PanelMessage({
  Icon,
  title,
  detail,
}: {
  Icon: typeof FileWarning;
  title: string;
  detail: string;
}) {
  return (
    <div className="flex items-start gap-[var(--s-3)] rounded-[var(--r-sm)] border border-hairline bg-surface p-[var(--s-4)]">
      <Icon aria-hidden size={18} strokeWidth={1.9} className="text-warn" />
      <div>
        <p className="text-body font-medium">{title}</p>
        <p className="mt-[var(--s-1)] text-meta text-ink-2">{detail}</p>
      </div>
    </div>
  );
}
