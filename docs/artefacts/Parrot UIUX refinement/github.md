repo: feynman82/igd-capstone-2026
branch: main
path: web/

## Last sync
date: 2026-09-12T08:10:00Z

### Updated in this project
- Recreated the Kitchen Table direction from `web/app/design-preview/` and resolved it into a final UI pass.
- All type moved to sans (Outfit + Figtree); the evaluation's Georgia is gone.
- Terracotta `#B4462A` added as brand accent; evergreen `#0F5F52` reserved for evidence; overdue red cooled to `#6F2833`.
- Today rebuilt as one hero card plus compact rows; navigation moved from left rail to top bar.

## Screen map
| Project screen | Built from |
|---|---|
| Today (1a, 1b, 1j) | `web/app/(app)/today/page.tsx`, `web/components/today/item-row.tsx`, `web/components/states.tsx`, `web/app/design-preview/preview.module.css` (`.home`) |
| Ask (1c, 1d, 1e, 1k) | `web/components/ask/conversation.tsx`, `web/components/ask/answer.tsx`, `web/app/(app)/ask/page.tsx` |
| Source chip / evidence | `web/components/source-chip.tsx` |
| Vault (1f) | `web/app/(app)/vault/page.tsx`, `web/components/vault/quarantine.tsx` |
| Document detail (1g) | `web/app/(app)/vault/[id]/page.tsx`, `web/components/vault/document-detail.tsx`, `web/components/vault/field.tsx` |
| Packs (1h) | `web/app/(app)/packs/page.tsx`, `web/components/packs/toggle.tsx` |
| Unlock (1i) | `web/app/unlock/page.tsx`, `web/components/unlock-form.tsx`, `web/components/wordmark.tsx` |
| Chrome / nav / tokens | `web/app/(app)/layout.tsx`, `web/app/layout.tsx`, `web/components/nav.tsx`, `web/app/theme.css`, `web/app/globals.css` |
