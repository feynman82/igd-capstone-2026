# `web/` — the interface

**Owner: Zee.** Next.js 15 (App Router), Tailwind, shadcn/ui, AI SDK `useChat`.

Four surfaces. The design pack with the screens and the original user stories is
[`docs/artefacts/interface-design-pack.html`](../docs/artefacts/interface-design-pack.html) —
open it in a browser. The buildable version of those stories, with acceptance criteria bound
to the corpus fixtures that test them, is [`docs/user-stories.md`](docs/user-stories.md).

| Surface | What it is for |
|---|---|
| **Today** | What the assistant wants to tell you before you ask. Reminders and alerts. This is what makes it feel alive rather than like a search box. |
| **Ask** | The conversation, with inline citations. Every factual sentence links to a document and page. |
| **Vault** | Everything filed, including the quarantine queue as "needs your eyes". |
| **Packs** | What the assistant knows about, and what it could know about. Where the expansion story becomes visible to a user. |

## Before building any screen

Lock the design tokens: one accent colour, one radius scale, one type scale. An agent
given tokens produces a consistent interface across sessions; an agent given "make it look
clean" produces four different ones.

## Rules

Login is a **local passphrase**, not federated identity — an offline-capable assistant
that needs a network to open is not offline-capable. Google OAuth appears only for Drive
authorisation, post-MVP.

A screen that only looks right with fixture data is not done. Empty and error states are
part of the deliverable, not polish.
