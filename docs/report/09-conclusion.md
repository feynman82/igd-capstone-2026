# §9 · Key findings, recommendations and conclusion

> **Draft.** Written from the repository for Christian to rewrite in their own words.

---

## 9.1 Key findings

This report set out to argue that warranted trust in a household assistant comes from architecture
more than accuracy. The evidence supports part of that claim.

- **Provenance can be enforced.** Every fact cites a document and page, and nothing leaked across
  15 adversarial questions. No code path pays or books, and a pack that declares it acts will not
  load.
- **Guessing cannot be thresholded away.** 21 of 118 answers still make an unsupported claim, and
  the relevance floor built to stop them was rejected. Better retrieval made the system more
  willing to answer, not less.
- **What you measure decides what you build.** Scoring by abstention made the floor the thing to
  tune. Scoring by code against a register found the guesses that a model judge had marked as
  faithful.

## 9.2 Recommendations

1. Treat a citation as a place to check, not as proof.
2. Count unsupported claims against ground truth written in advance, and do not rely on a model
   judging a model.
3. Enforce a boundary in code and types, not in a prompt.
4. Measure on real documents and real users before claiming value. This project has not yet done
   either.

## 9.3 Conclusion

In ten weeks, five people built a working prototype, measured it three times and kept every result.
The hardest problem was not retrieval but knowing when a relevant page does not answer the
question. Architecture can make an assistant's claims checkable and its actions bounded, which is
what trust would have to rest on. Whether households come to trust it is the question the next
stage must answer (§8).
