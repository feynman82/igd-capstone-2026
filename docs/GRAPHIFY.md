# Graphify — the shared knowledge graph

Graphify builds a knowledge graph of this repository so a coding agent can find the
relevant part of a five-person project without reading all of it. It is how a session
that has never opened `core/contracts.py` still knows that a field name in
`packs/*/pack.yaml` reaches `corpus/register/` and `docs/field-dictionary.md`.

**It is already set up.** The graph is built, committed, and the git hooks are installed
on the integration machine. This page is what everyone else needs to do, and how the
thing works.

The size and the commit it was built from are in the **Graph Freshness** section at the top
of [`graphify-out/GRAPH_REPORT.md`](../graphify-out/GRAPH_REPORT.md). Read it there rather
than here: that section is generated, so it is right, and a number copied into this page is
wrong within a week. (It was `436 nodes · 473 edges · 51 communities` when this page was
written, and it is several times that now, which is the point.)

---

## Setup, once per clone

```bash
uv tool install graphifyy         # or: pip install graphifyy
graphify install --platform claude   # installs the skill into ~/.claude/skills/graphify/
make graph-setup                     # registers the merge driver — see below
graphify hook install                # post-commit and post-checkout hooks
```

`graphify install` writes into **your user config**, not into this repository — it does
not touch our `AGENTS.md` or `CLAUDE.md`. Use `--platform antigravity` or `--platform
cursor` instead if that is what you drive.

---

## Using it

```bash
graphify query "how does a field name in pack.yaml reach the corpus register"
graphify explain "FieldSpec"
graphify path "PackManifest" "corpus/validate.py"
graphify affected "FieldSpec"          # what breaks if I change this
```

Those are worth running at the top of a session in a part of the repository you did not
write. `/orient` will remind you.

`graphify-out/graph.html` is an interactive force-directed view — open it in a browser.
It is not committed (320 KB, and regenerated locally by any of the commands above).

---

## Two kinds of extraction, and which needs what

| | How | Cost | When |
|---|---|---|---|
| **Code** | tree-sitter AST parsing | Free, fully local, no model involved | `graphify update .` — after any code change |
| **Docs, PDFs, images** | a model reads them | Uses whichever backend you configure | `/graphify .` inside Claude Code |
| **Community names** | a model names each cluster | Same | `graphify label . --backend=claude-cli` |

The post-commit hook runs the free code pass automatically. The semantic pass over
markdown — the lane briefs, `AGENTS.md`, the pack guide — is the part that makes the
graph *useful* rather than merely structural, and it runs through your own Claude Code
session: type `/graphify .` in Claude Code at the repository root.

We use the `claude-cli` backend so it runs on the existing Claude Code subscription. No
API key is set on the integration machine and none is needed.

---

## Merge conflicts, solved properly

`graph.json` is regenerated on every commit, so two people committing in the same week
will always touch it. Graphify ships a **union merge driver** for exactly this, and
`.gitattributes` already declares it:

```
graphify-out/graph.json merge=graphify -diff linguist-generated
```

Git will not use a driver it has not been told about, and that registration is per-clone
config rather than something the repository can carry. So run it once:

```bash
make graph-setup
```

which is just:

```bash
git config merge.graphify.driver "graphify merge-driver %O %A %B"
```

With that set, two people's graph updates union-merge silently. **Without it**, you get an
ordinary conflict in a 300 KB generated file. Do not hand-merge that — take either side
and rebuild:

```bash
git checkout --theirs graphify-out/graph.json && graphify update .
```

`-diff linguist-generated` keeps the graph out of pull-request diffs and out of the
repository's language statistics, so a PR that touches it still reads as a two-file change.

---

## What is committed, and what is not

| Path | Committed | Why |
|---|---|---|
| `graphify-out/graph.json` | yes | The graph everyone queries |
| `graphify-out/GRAPH_REPORT.md` | yes | Key concepts and surprising connections, readable |
| `graphify-out/.graphify_labels.json` | yes | Community names — a model call to regenerate |
| `graphify-out/.graphify_analysis.json` | yes | Clustering analysis |
| `graphify-out/graph.html` | no | 320 KB, regenerated locally in seconds |
| `graphify-out/cache/`, `converted/`, dated backup folders | no | Machine-local working state |

---

## What leaves the machine

Code extraction is local: tree-sitter, no model. The semantic pass sends **documentation
and markdown** to whichever backend you have configured — for us, Claude Code.

This matters for Siew's data inventory, so state it precisely: **the repository contains no
personal data.** The synthetic corpus in `corpus/batches/` *is* committed — it is generated
from an invented canon and there is no person behind it. The redacted holdout in
`corpus/holdout/` is gitignored and must never be committed at all; it is real documents
from team members. `.graphifyignore` excludes **both** folders from extraction, so neither
the synthetic batch nor the holdout is ever sent to a model backend — see `NOTICE.md`.

---

## Keeping it fresh

The post-commit hook keeps the code graph current by itself. Two things it cannot do:

- **After editing markdown** — a lane brief, `AGENTS.md`, a skill — run `/graphify .` in
  Claude Code so the semantic layer catches up. The report's **Graph Freshness** section
  names the commit the graph was built from; compare it to `git rev-parse HEAD`.
- **After a refactor that deletes code** — `graphify update . --force`, because the
  rebuild refuses to shrink the graph without it.

### The hook leaves your tree dirty. Amend it into the commit you just made.

The post-commit hook rebuilds the graph *after* the commit lands, so `git status` shows
`graphify-out/` modified immediately after every commit you make. That is the hook working,
not a mistake. **Fold it back into that commit:**

```bash
git commit --amend --no-edit -- graphify-out/
```

This is the convention, not one of two options. The alternative — leaving it for the next
commit to absorb — means every feature commit carries somebody else's graph refresh, which
is the thing that makes a graph commit unreviewable and is what rule 9 exists to prevent.
Amending keeps each commit self-consistent: the graph in a commit describes that commit.

Two things not to do. **Do not revert it**, or the committed graph describes the commit
before last. **Do not amend a commit you have already pushed** — if it is pushed, let the
next commit pick the refresh up and carry on.

The semantic pass over markdown is the part the hook cannot do. Run `/graphify .` in Claude
Code after editing a lane brief, `AGENTS.md` or a skill, and commit that refresh on its own.
The weekly integration session is when that happens as a matter of course.
