# 6. pypdfium2 renders the page images the quarantine second pass reads

Date: 2026-09-11 · Status: accepted

## Context

`team/christian/README.md` describes quarantine as two-stage, and the second stage as the
capability the 4B SEA-LION swap bought us: when the parser cannot recover a document's text,
the **page image** goes to the vision-language model, which reads pixels rather than the text
a parser managed to recover.

A photograph is already a page image and needs nothing. A PDF is not. Something has to
rasterise page 3 of a faint scan into a PNG before it can be sent, and rendering a PDF is not
something the standard library does.

Three options were available:

1. **Ask Docling for the page images.** Docling can produce them, but it produces them as part
   of a conversion — the conversion that has already failed. Asking the component that could
   not read the document to prepare the evidence for the component that might is the wrong
   dependency direction, and it makes the recovery rate a measurement of Docling twice.
2. **Shell out to `pdftoppm` or ImageMagick.** No Python dependency, but a system dependency
   that every teammate has to install, on Windows, before `START.cmd` works. That trades a
   declared dependency for an undeclared one, which is worse.
3. **`pypdfium2`.** Google's PDFium — the renderer in Chrome — with a thin Python binding. It
   is already installed in this repository as one of Docling's own dependencies, so it adds no
   download and no new code provenance. It is Apache-2.0/BSD-3-Clause.

## Decision

`pypdfium2` becomes a **direct** runtime dependency in `pyproject.toml`, used only by
`core/ingest/quarantine.py` to render pages at 150 dpi, capped at the first four pages of a
document.

It was already present transitively. Declaring it directly is the point of this record: code we
call is a dependency we own, and a transitive dependency that Docling drops in a minor release
must break a lock file rather than break quarantine silently.

150 dpi is legible for 8 pt print. 300 dpi quadruples the image tokens and there is no measured
quality gain to justify it — when Yew Mun's harness can measure one, that is the number to
revisit and this is the ADR to supersede.

Four pages is a household document. A forty-page policy wording that fails to parse is a
different problem from the one this pass solves, and sending forty page images to a 16K context
would fail in a way that looks like a model problem rather than a design choice.

## Consequences

The image pass works on PDFs and on photographs, which is every capture channel we have.

It does **not** work on a document whose original bytes are gone. v1 keeps the inbox as the
document store — nothing is copied into the database — so `scripts/quarantine.py --retry` matches
quarantined rows back to files by SHA-256 and reports the ones it cannot find rather than
pretending. If the corpus work makes that limitation bite, storing the bytes is its own decision
and its own migration, not a quiet change here.

The recovery rate is now measurable: `core/ingest/quarantine.py` returns it per run. A rate over
three documents is not a finding, so the count is reported next to it.
