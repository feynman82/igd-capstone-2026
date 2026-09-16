"use client";

import { Calculator, ExternalLink, FileWarning, ImageOff, X } from "lucide-react";
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
 * Advice (ADR 0016) adds two chips that have no page at all. A **rule** value was published by
 * somebody, on a date, at an address: it shows who, what and when, and links out to the
 * publisher. A **calculation** is Parrot's own arithmetic over the inputs beside it: it is plain
 * text, because there is nothing to open. Neither is ever drawn as a page link — a "p.0" button
 * that opens an error is a citation that lies about what it is.
 *
 * The panel grows out of the chip that opened it, which is the one piece of choreography on
 * this surface: `transform-origin` is set from the chip's own position so the page appears to
 * come from the thing that was pressed rather than from the middle of the screen.
 */
export function SourceChip({ source }: { source: Source }) {
  const [open, setOpen] = useState(false);
  const chip = useRef<HTMLButtonElement>(null);

  if (source.kind === "rule") return <RuleChip source={source} />;

  if (source.kind === "calculation") {
    return (
      <span className="inline-flex max-w-full items-center gap-[var(--s-1)] rounded-[var(--r-sm)] border border-hairline px-[11px] py-[7px] text-meta text-ink-3">
        <Calculator aria-hidden size={13} strokeWidth={2} className="shrink-0" />
        {source.text}
      </span>
    );
  }

  const openable = source.document_id !== null && source.page !== null;
  // A fact read off a page arrives with its document id and page but no name; its `text` is
  // already "payslip-august.pdf, page 1". Without this fallback the chip and its dialog are empty.
  const name = source.document_name || source.text;

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
        className="inline-flex max-w-full items-center gap-[var(--s-2)] rounded-[var(--r-sm)] border border-accent-line bg-accent-soft px-[11px] py-[7px] text-meta font-medium text-accent transition-transform duration-[var(--dur-press)] active:scale-[0.97]"
      >
        <span className="truncate">
          {source.kind === "inventory" ? `On file · ${name}` : name}
        </span>
        <span className="num">p.{source.page}</span>
      </button>

      {open ? (
        <SourcePanel
          source={source}
          name={name}
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

/**
 * A published rule value: who published it, what it is called, and when.
 *
 * A link out rather than a panel, because the page is the publisher's and not a document in
 * the vault. Only an `http(s)` address is ever made a link — the address came from a pack's
 * source list, and a pack is a download.
 */
function RuleChip({ source }: { source: Source }) {
  const title = source.title || source.document_name || source.text;
  const said = [source.publisher, source.dated].filter(Boolean).join(" · ");
  const href = source.url && /^https?:\/\//i.test(source.url) ? source.url : null;

  const body = (
    <>
      <span className="min-w-0">
        <span className="font-medium text-ink">{title}</span>
        {said ? <span className="text-ink-3"> · {said}</span> : null}
      </span>
      {href ? (
        <>
          <ExternalLink aria-hidden size={13} strokeWidth={2} className="shrink-0 text-ink-3" />
          <span className="sr-only">(opens the publisher&rsquo;s page in a new tab)</span>
        </>
      ) : null}
    </>
  );

  const shape =
    "inline-flex max-w-full items-center gap-[var(--s-2)] rounded-[var(--r-sm)] border border-hairline bg-surface px-[11px] py-[7px] text-left text-meta";

  return href ? (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className={`${shape} underline-offset-2 transition-colors hover:bg-surface-2 hover:underline`}
    >
      {body}
    </a>
  ) : (
    <span className={shape}>{body}</span>
  );
}

function SourcePanel({
  source,
  name,
  onClose,
}: {
  source: Source;
  name: string;
  onClose: () => void;
}) {
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
      aria-label={`${name}, page ${source.page}`}
      className="m-auto w-[min(52rem,92vw)] rounded-[var(--r)] border border-hairline bg-surface p-0 text-ink shadow-lift-2 backdrop:bg-[rgb(27_24_20/0.5)]"
    >
      <div className="flex items-center gap-[var(--s-3)] border-b border-hairline px-[var(--s-4)] py-[var(--s-3)]">
        <div className="min-w-0">
          <p className="truncate text-body font-medium">{name}</p>
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
            alt={`Page ${source.page} of ${name}`}
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
