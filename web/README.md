# `web/` — the interface

**Owner: Zee.** Next.js 15 (App Router), Tailwind, shadcn/ui, AI SDK `useChat`.

Four surfaces. The design pack with the screens and the original user stories is
[`docs/artefacts/interface-design-pack.html`](../docs/artefacts/interface-design-pack.html) —
open it in a browser. The **resolved** interface, which is what is built, is the Kitchen Table
canvas at
[`docs/artefacts/Parrot UIUX refinement/`](../docs/artefacts/Parrot%20UIUX%20refinement/) —
artboard `1o` is the handoff: every token value, the font pairing, and a file-by-file list of
what changes. The buildable version of the stories, with acceptance criteria bound to the
corpus fixtures that test them, is [`docs/user-stories.md`](docs/user-stories.md).

| Surface | What it is for |
|---|---|
| **Today** | What the assistant wants to tell you before you ask. Reminders and alerts. This is what makes it feel alive rather than like a search box. |
| **Ask** | The conversation, with inline citations. Every factual sentence links to a document and page. |
| **Vault** | Everything filed, including the quarantine queue as "needs your eyes". |
| **Packs** | What the assistant knows about, and what it could know about. Where the expansion story becomes visible to a user. |

## Before building any screen

Read [`app/theme.css`](app/theme.css) and open `/tokens`, which renders it back as a specimen.
One colour per job, one radius scale, one type scale. An agent given tokens produces a
consistent interface across sessions; an agent given "make it look clean" produces four
different ones.

Two colours, and they are not interchangeable. **Terracotta `--brand`** is intent: the
wordmark, the current tab, the primary action, the left edge of the card that needs you now.
**Evergreen `--accent`** is evidence, and only evidence: a source chip, a verified field, a
switch that is on. If it is green, there is a document behind it. A screen that spends green
on a button has taken the one signal this product runs on and made it decoration.

## Rules

Login is a **local passphrase**, not federated identity — an offline-capable assistant
that needs a network to open is not offline-capable. Google OAuth appears only for Drive
authorisation, post-MVP.

A screen that only looks right with fixture data is not done. Empty and error states are
part of the deliverable, not polish.
