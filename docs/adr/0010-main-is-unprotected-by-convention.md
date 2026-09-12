# 10. `main` is unprotected, and the discipline is human

Date: 2026-09-12 · Status: accepted

## Context

The repository is private, under Christian's personal GitHub account. GitHub does not
enforce branch protection or rulesets on a private repository on a personal free plan, so
any ruleset saved here is inert: it renders on the settings page, and merges land unchecked
anyway.

This was not theoretical. `FIRST-RUN.md` listed "the branch ruleset" among the items already
configured, while also carrying a note that it does not enforce — two statements a reader had
to reconcile for themselves. Meanwhile the repository has had exactly one pull request in its
life (merged with zero reviewers requested), and two commits of corpus documents
(`8ec421d`, `25dba71`) landed directly on `main` from a collaborator, unreviewed, carrying a
batch with no register and real organisations named on the documents' faces — the precise
class of problem `CODEOWNERS` was meant to route to Desmond's reviewer.

So the choice was not "protect `main` or not". It was: keep a control that looks real and is
not, or write down that there is no control and say what replaces it.

## Decision

**`main` is unprotected and we stop trying to protect it.** No ruleset is saved, because a
saved-but-inert ruleset is worse than an empty settings page: it tells the next person a gate
exists.

**`CODEOWNERS` stays.** It still auto-requests the right reviewer on a pull request, which is
real value. It simply cannot block a merge, and the file's header no longer implies it can.

**The task is removed from `docs/team-tasks.csv`.** Its *Done when* — "main is protected, one
review required" — cannot become true on this plan. A task that can never go green is a
permanent false red that trains the team to ignore the board.

**What carries the weight instead** is convention, stated in `CONTRIBUTING.md`: branch per
lane, one vertical slice per PR, the `CODEOWNERS` review requested and given before merge, and
a same-day note in the team channel for anything landed directly. The weekly integration pass
is the backstop that catches what convention misses.

## Alternatives considered

| Option | Why not |
|---|---|
| Move the repo to a GitHub Team org | Buys real enforcement, but costs money and an admin migration mid-project, and moves the repository out from under the account every collaborator, hook and local checkout is already wired to. Not worth it for the six weeks remaining. |
| Make the repository public, which makes protection free | The corpus is not publishable in its current state — `corpus/batches/batch0-personas/` names real insurers and agencies on synthetic documents, which is exactly what `corpus/README.md` rule 1 forbids going out. Publishing to buy a merge gate would trade a governance problem for a process one. |
| Keep the saved-but-inert ruleset as aspirational configuration | This is the status quo we are leaving. It cost us once already: the setup doc read as "configured", so nobody treated unreviewed merges as the open risk they were. |
| A CI check or pre-commit hook as a substitute gate | Neither blocks a push to `main`; CI reports after the fact and a local hook is opt-in per machine. Useful, and we keep `make check` in CI — but it is not a review, and calling it one would repeat the same mistake in a different place. |

## Consequences

**Easier.** No plan change, no migration, no admin. The setup documentation now matches what
the settings page actually does, which means the next person to read `FIRST-RUN.md` is not
quietly misled. One permanently-unachievable task leaves the board.

**Harder, and this is the real cost.** An unreviewed change to another lane's directory is
invisible until someone notices — up to a week, if it lands just after an integration session.
`CODEOWNERS` becomes advisory, so the guarantee that a `packs/` change reaches Zee is now a
habit rather than a mechanism, and habits degrade under deadline pressure precisely when the
review matters most. The weekly integration pass is no longer a tidy-up; it is the only
control, and skipping one has a cost it did not have before.

We are accepting that trade knowingly rather than papering over it, which is the whole point
of writing it down.

## Revisit when

The repository moves to a Team org, goes public after the report is submitted, or a second
unreviewed cross-lane merge causes real rework — whichever comes first. Any of the three
changes the arithmetic above.
