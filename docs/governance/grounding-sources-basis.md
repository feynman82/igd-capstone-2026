# Third-party material the system indexes, and on what basis

**Owner: Siew.** Decided 2026-10-18. Report chapter: governance, provenance of grounding.

Ground every claim in a file in this repository or in a cited instrument. Where the evidence
could not be read, it says `unverified`.

---

## What is indexed

Besides the household's own documents, PARROT indexes a small corpus of published regulator
guidance per domain pack, so that it can explain a rule as well as a document. Each corpus sits
in `packs/<pack_id>/grounding/<corpus_id>/`, as extracted text, one file per source, with a
`sources.yaml` recording title, publisher, URL, published and retrieved dates, the years it
applies to, a review-by date after which it is not cited, and a licence note
(`GroundingDocument` in `core/contracts.py`). No original PDF is committed.

| Pack | Corpus | Sources | Publisher |
|---|---|---|---|
| `iras_tax` | `iras_tax_ya2025_ya2027` | 9 (8 web pages, 1 factsheet PDF) | Inland Revenue Authority of Singapore |
| `insurance_agent` | `sg_protection_guidance` | 20 | MoneySense, MAS, MOH, CPF Board, LIA |

This document settles the IRAS corpus. The insurance corpus was signed off by Christian on
2026-09-17; its licence basis is not yet reviewed against this one (open item 3).

## The obstacle

IRAS's website Terms of Use reserve the reproduction, republication, posting or distribution of
the site's contents to IRAS's prior written permission. `unverified`: the page could not be
opened from the working environment on 2026-10-18, so this is taken from a search engine's
summary of https://www.iras.gov.sg/terms-of-use-browser-compatibility and must be read in full
before the report quotes it.

Keeping a verbatim copy of a page in a retrieval index is reproduction. Linking to the page
alone would not support the pack: the two rule values it uses, the resident tax bands
(`tax_rate`) and the SRS contribution cap (`srs_contribution_cap`), are extracted from the
stored text and approved by a person before use (`core/grounding/values.py`,
`scripts/review_grounding_values.py`).

## The basis: the computational data analysis exception

The Copyright Act 2021 makes it a permitted use to copy a work for **computational data
analysis**, defined in s 243 to include using a computer program to identify, extract and
analyse information or data from the work. Under s 244(2), as summarised in commentary
(`unverified` against the Act's text, which could not be opened):

| Condition | How PARROT meets it |
|---|---|
| The copy is made for computational data analysis, or to prepare for it | The text is chunked, embedded and searched by program, and rule values are extracted from it (`core/grounding/index.py`) |
| The copy is not used for any other purpose | It is kept only as the input to that index; it is not published with the report (`packs/README.md`, §7 rule 5) |
| The copy is supplied to no one, except to verify results or for collaborative research | It lives in a private repository shared only by the five members of the project team |
| The user had lawful access to the source | Every page is publicly available on iras.gov.sg without login, and was captured from a browser print or the published PDF; no access control was circumvented |
| The source is not an infringing copy | Each source is IRAS's own publication, at the URL recorded in `sources.yaml` and confirmed in a browser by Siew on 2026-10-18 |

Commentary also states that a contract term is void to the extent that it purports to exclude
or restrict this permitted use, so the website's Terms of Use do not by themselves defeat it.
`unverified`: the section that says so has not been read in the Act itself.

## Where the exception stops

- **What an answer shows.** s 244 covers the copy made for analysis. An answer that quotes a
  passage of IRAS guidance to the user is a different act. That relies on the passage being
  short and attributed, with the citation naming IRAS, the page title and its URL
  (`core/grounding/index.py`), which is an argument under fair use, not under s 244.
- **Publication.** The corpus is not published or redistributed, with the report or otherwise.
  The report cites and links the sources.
- **Beyond the prototype.** A product that shipped this corpus to households would be supplying
  the copy to others, which s 244(2) does not allow. Commercial use needs IRAS's written
  permission or a corpus fetched on each user's own machine. This belongs in the
  commercialisation section's constraints.

## The e-Tax Guide

The IRAS e-Tax Guide *Tax Deductibility of Donations* was removed from the corpus on
2026-10-18. Its own notice requires written permission before any part of it is stored in a
retrieval system. On the reasoning above s 244 would likely cover it too, but nothing depended on
it: the 250% deduction is cited from IRAS's *Donations and tax deductions* page. A source the
pack does not need is not worth relying on an exception for, and a smaller corpus retrieves
better (`packs/README.md`, §7).

## Open items

1. Read the IRAS Terms of Use in full and replace the `unverified` summary above with a quotation.
2. Read ss 243–244 of the Copyright Act 2021 on Singapore Statutes Online, and the section that
   voids contract terms excluding permitted uses, and cite them by section. Ask the supervisors
   to confirm the reading before the report relies on it.
3. Apply the same basis to the insurance corpus, whose MAS source already notes that reuse
   beyond this private prototype is to be confirmed.
