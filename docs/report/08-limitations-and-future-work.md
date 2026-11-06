# §8 · Limitations and future work

**Owners: Desmond and Yew Mun.** Budget three quarters of a page.

> **Status.** A draft by Yew Mun, for Desmond to review and add to. The holdout is marked
> **⟨holdout⟩**.

---

## What ten weeks did not reach

- **Real documents.** ⟨holdout⟩ Every number in §5 is on a synthetic corpus about one household. The
  holdout is 14 real, redacted documents of a planned 40.
- **Real people.** Nobody outside the team has used the interface, and no household has lived with
  it. So this report can show how often the system guesses; it cannot show that a household comes
  to trust it, which is what the thesis is finally about.
- **Breadth.** Two of eleven domain packs and three of four modules are built. Nine packs and the
  Tracker are specified against the contract, not built.
- **Languages.** All 133 golden questions are in English, on a generator built for Southeast Asian
  languages.
- **Our own questions.** Set B was written by the people who built the system. It tests what we
  thought to ask, not what households ask.

## What the approach itself cannot do

**A citation shows where a value came from, not whether it answers the question.** Code can check
the first, and does. The second is a judgement about meaning, and no threshold makes it for us: to
a relevance score, an unanswerable question with a relevant page looks like an answerable one (ADR
0019). That limit does not shrink with more documents, because each one can give such a question
another relevant page, and a household's vault only grows.

**It reads paper, not the world.** PARROT knows what has been filed. A policy renewed last month
reads as expiring until the new schedule arrives, and an error on a printed page is cited
faithfully. A more accurate model changes neither.

**Identity is settled by asking a person.** Names match on case and spacing alone, so a reordered
surname or a romanisation variant becomes a question for the owner. That is right for a system
that advises, and it costs a household several questions in its first week.

**Local-first has a price.** The generator peaks at 7.4 GB of VRAM. Keeping documents on the
owner's hardware assumes hardware not every household owns.

## What comes next

1. **Finish the holdout,** to 40 documents, and report the gap by document type.
2. **Close the guessing that can be closed:** decide ADR 0021, and answer from values already
   extracted (#125).
3. **Watch real use:** a usability test of Ask, then a longitudinal study in a few households, so
   that Set B can be rebuilt from questions people actually asked.
