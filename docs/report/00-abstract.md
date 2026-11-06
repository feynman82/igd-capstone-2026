# Abstract

> **Draft.** Written from the repository for Christian to rewrite in their own words.

---

Households keep their insurance, tax and loan records as paper and PDFs, and the answer to a simple
question sits on a page nobody can find. A general-purpose assistant answers such questions
confidently, and a confident wrong answer about a policy is worse than none. This project asks
whether a household document assistant can be built so that its answers can be checked rather than
taken on trust.

PARROT is a local-first prototype. It reads a household's documents on the owner's machine, files
typed facts with the page each came from, answers only with a citation, and advises without acting.
New subjects are added as domain packs checked against a contract. The work followed the Design
Science Research sequence, and was evaluated three times on a synthetic corpus with a register
written before the documents existed, so that answers could be scored by code.

On 93 documents, the latest check answered 77 of 93 answerable questions right with the right page,
filed fields at an F1 of 0.961, and leaked nothing across 15 adversarial questions. It still made 21
unsupported claims in 118 answers, and most of those were unanswerable questions answered from a
relevant page. A test on real, redacted documents had not been run when this report was completed.

We conclude that architecture can make an assistant's claims checkable and can bound what it does.
It cannot, by itself, stop a system guessing from a relevant page, and whether households come to
trust it remains unmeasured.
