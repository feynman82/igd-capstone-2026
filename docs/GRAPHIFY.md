# Graphify — the shared knowledge graph

Graphify builds a knowledge graph of this repository so that any coding agent — Claude
Code, Antigravity, Cursor — can find the relevant part of a five-person project without
reading all of it. It is how a session that has never seen `core/contracts.py` still
knows that a field name in `packs/*/pack.yaml` reaches `corpus/register/` and
`docs/field-dictionary.md`.

**It must be run from a local checkout.** It parses files on disk and installs git hooks,
so it cannot be started through the GitHub web interface or the API. Someone with the
repository cloned has to run it. That someone is Christian.

---

## One-time setup — Christian only

```bash
uv tool install graphifyy       # or: pip install graphifyy
cd igd-capstone-2026

graphify install                # writes agent skill files — see the warning below
graphify .                      # first full build
graphify hook install           # post-commit and post-checkout hooks
```

> **Warning before you run `graphify install`.** It writes platform skill files including
> `CLAUDE.md` and, on some versions, appends to `AGENTS.md`. Our `AGENTS.md` is curated
> and its eight hard rules are load-bearing. Check `git diff AGENTS.md` immediately
> afterwards and revert anything it overwrote. If it wants to add its own guidance, let
> it live in `CLAUDE.md` instead.

After the first build you will have:

```
graphify-out/
  graph.json          the queryable graph        ← committed
  GRAPH_REPORT.md     key concepts and links     ← committed
  graph.html          interactive visualisation  ← not committed, regenerate locally
  cache/              extraction cache           ← not committed
  manifest.json       build metadata             ← not committed
```

---

## Everyone else

```bash
git pull
uv tool install graphifyy
graphify update .          # re-extracts only what changed since the last build
```

Then use it from your agent session:

```bash
graphify query "how does a field name in pack.yaml reach the corpus register"
graphify path "PackManifest" "corpus/validate.py"
graphify explain "FieldSpec"
```

Those three commands are worth putting at the top of a session when you are working in a
part of the repository you did not write.

---

## The rule that prevents constant merge conflicts

**Only Christian commits `graphify-out/`.** It is regenerated at the weekly
ninety-minute integration session, in a commit that contains nothing else.

`graph.json` is a large generated file that changes whenever anything changes. Three
people committing it means a conflict in it on nearly every pull request, and merging two
versions of a generated graph is meaningless work. Everyone else runs `graphify update .`
locally and leaves the result uncommitted — `git status` should never show
`graphify-out/` in anybody else's working tree at commit time.

If you do hit a conflict in `graphify-out/`, do not merge it. Take either side, then
regenerate:

```bash
git checkout --theirs graphify-out/ && graphify update . 
```

---

## Extraction and what leaves the machine

Code extraction is local — tree-sitter AST parsing, no model involved. Semantic
extraction of documentation, PDFs and images calls whichever model backend you have
configured, through your own IDE session or API key.

This matters for Siew's data inventory: **the repository contains no personal data**, so
graphify's semantic pass sends only project documentation to a model provider. The
household corpus lives in `corpus/batches/`, which is gitignored and never enters the
graph. Keep it that way — `.graphifyignore` excludes it explicitly, and the same applies
to the 40-document real holdout, which must never be committed to this repository at all.

---

## For CI

`graphify extract .` is the headless form, for a workflow rather than a terminal. We are
not wiring it into CI for the capstone — the weekly regeneration is enough, and a CI job
that calls a model on every pull request is cost with no reader.
