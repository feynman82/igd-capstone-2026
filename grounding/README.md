# Grounding corpora

Authoritative reference material, indexed under a pack's namespace and kept separate from
the user's own documents. This is ISO/IEC 5338's **knowledge acquisition** process (6.4.7),
so it is a governance artefact as well as a build artefact.

## Structure

```
grounding/<corpus_id>/
  sources.yaml        provenance for every file — required, no exceptions
  *.md                extracted text, one file per source document
  *.pdf               the original, only where the licence clearly allows it
```

A pack points at a corpus by directory:

```yaml
grounding:
  corpus: iras_reliefs_ya2026    # the directory name, not a path — `Grounding.corpus` is a slug
  top_k: 8
```

A pack with no signed-off sources points at nothing — `corpus: null, top_k: 0` — rather than at
an empty directory. Both packs are in that state today, and `packs/README.md` §7 explains why
that is a designed guardrail and not a gap.

## Rules

1. **Every file has a `sources.yaml` entry.** Title, publisher, URL, the date it was
   retrieved, and a licence note. A passage the assistant cites has to be traceable to a
   real publication with a date, or the citation is worthless.
2. **Prefer extracted text over the original PDF.** Committing the text you actually index
   keeps the repository small, makes diffs readable, and avoids redistributing a third
   party's file. Keep the original only where the licence plainly allows it.
3. **Version by what the guidance applies to, not by when you downloaded it.** Tax relief
   rules change by Year of Assessment, so the corpus id carries it: `iras_reliefs_ya2026`.
   When YA2027 guidance appears it is a new corpus, not an edit to this one.
4. **Never paraphrase a rule into the corpus.** Index what the publisher wrote. If you find
   yourself summarising, you have moved from grounding into authorship, and the assistant
   will cite your summary as if it were the source.
5. **Do not publish the corpus with the report.** Cite the sources; link them. The corpus
   lives in a private repository.

## Owner

Zee assembles the corpora. Siew reviews `sources.yaml` and writes the paragraph in the
report explaining what third-party material the system indexes and on what basis.
