---
description: Write a handover note for the next session in this lane
---

Write a short handover so the next Claude Code session in this lane starts where this one
stopped. Print it in the chat; do not commit it unless asked.

Cover, in this order and no more than a screen:

1. **What changed** — the files touched and why, one line each
2. **What state the working tree is in** — run `git status --short` and `make check`, and
   say plainly whether it is clean or mid-change
3. **The next concrete step** — a specific action, not a direction. "Add the `cover_from`
   field to `renewal_notice` and regenerate" rather than "continue with the insurance pack"
4. **Anything discovered that is not written down yet** — a constraint, a gotcha, a
   surprising test result. If it is durable, say which file it belongs in: an ADR, the
   lane brief, or `AGENTS.md`
5. **Anything left broken on purpose**, and why

Do not summarise the whole project. The next session reads `AGENTS.md` for that.
