# Speaking notes · Retrieval and evaluation · Yew Mun

Final presentation, 3 November. Five slides, about **8 minutes** (around 1,050 spoken words, at
roughly 1.5 minutes a slide). The speaker notes inside the .pptx are the full written version; this
is what to *say*, shorter and in speaking order.

**Before:** Desmond, on the corpus and the adversarial set. **After:** Siew, on governance and the
autonomy boundary.

---

## Slide 1 · How it finds the page · ~1:45

**Land this:** *search finds the page; the gate checks every sentence.*

> Thanks, Desmond. Desmond built the documents. My part is two questions: does PARROT find the
> right page, and can we trust what it says about it?
>
> Finding the page takes two searches, because neither works alone on household paperwork. Search
> by meaning can't find a policy by its number. Search by words can't find "my car cover" when the
> schedule says "motor vehicle". So we run both and fuse them.
>
> Then a second model, a cross-encoder, re-reads the top forty against the question and keeps six.
>
> The local model writes the answer, and every sentence names the passage it came from. The last
> step is the one that makes this ours: a sentence with no source, or with a figure the page doesn't
> print, is dropped before you ever see it.

*Point at the two numbers on the right.*

> When the re-reader arrived, faithfulness went from 0.81 to 0.97, the biggest jump we measured.
> And by Run 3, nineteen of the twenty-one wrong answers had the right page in hand. Search is no
> longer where we lose answers.

**Bridge:** "So how good is it? Here are the three runs."

---

## Slide 2 · The scorecard · ~1:45

**Land this:** *72 of 93 right and cited, 15 of 15 traps held, and one row that didn't move.*

> We measured three times. Run 1 was on six documents. Run 2 added hybrid search and the re-reader.
> Run 3 used ninety-three documents, loaded from a frozen commit into a database of its own, so
> anyone can rebuild it.
>
> One caution first: each run had a different corpus, so read these as three measurements, not a
> trend.
>
> Run 3: seventy-two of ninety-three questions answered right *and* citing the page the answer is
> printed on. All fifteen adversarial traps held. Nothing leaked.

*Point at the orange row.*

> And this row: saying "I don't know" when the answer isn't there. 0.76, then 0.52, then 0.52.
> That's the finding, and it's the next slide.

*Point at the strip at the bottom.*

> The strip is the same Run 3 corpus measured again on 22 October, with the fixes Run 3 itself
> found: seventy-six right and cited.

**Bridge:** "Why did a better system get worse at saying no?"

---

## Slide 3 · The finding · ~2:00 (the slide to slow down on)

**Land this:** *better search made it worse at saying "I don't know", and no threshold fixes that.*

> On six documents, three in four unanswerable questions were declined. As documents arrived, that
> fell to half, and it stayed there.
>
> Nothing broke. Every new document gives an unanswerable question a page that looks close, and a
> better search engine is exactly the thing that finds it.
>
> The obvious fix is a threshold on the re-reader's score. We built it and swept it. Every setting
> gave up two targets we had already cleared for a fraction of this one, so we rejected it. ADR 0019
> records why.

*Point at the two examples.*

> Look at what the twelve still answered have in common. The value is real and printed, just under
> a different label. "The named driver is Marcus" cites *Name of Insured*. A road-tax date cites the
> start of the insurance period.
>
> A score can't see that, but the printed label can. We built a check for it, ADR 0021. It met its
> own conditions: two fewer unsupported claims, and no right answer lost. But it reaches only some
> cases, so it's switched off until the team reviews it.

**Bridge:** "Every number so far is only worth what it measures, and three times it measured the wrong thing."

---

## Slide 4 · Checking the checker · ~1:30

**Land this:** *three times a number misled us; each time we traced it rather than tuned to it.*

> One. The scorer was too generous. On ten casually worded questions it passed seven; a person
> passes four. The judge model gave a wrong deductible full marks, because the page it quoted was
> real. So the report now leads with five numbers scored by code against the register, one for each
> promise PARROT makes.
>
> Two. The test leaked into the test. The adversarial documents planted for Set C were sitting in
> the database we used to score the ordinary questions, and one of them was outranking the real
> car schedule. Now each set has its own database.
>
> Three. One word made two alerts false. The renewal notices print "Mr Marcus Lim Jun Wei". The "Mr"
> stayed in the name, matched nobody in the household, and PARROT reported his policies as lapsed.
> We strip titles now, and on Run 3's corpus no false alert fires.

**Bridge:** "So where does that leave us?"

---

## Slide 5 · Where it stands · ~1:00

**Land this:** *the absolute line held; the work left is teaching it when to stop.*

> Fifteen of fifteen adversarial traps held. That is the one line we treat as absolute.
>
> Twelve of twenty-five unanswerable questions still get an answer. The engine finds the page. What
> it still has to learn is when *not* to answer from it.
>
> And everything you've seen is on synthetic documents. The holdout, fourteen real, redacted
> documents, is the honest test of how much of it survives real paper.
>
> Siew will now take you through how we govern what PARROT is allowed to do.

> **If the holdout has run by 3 November**, replace the last paragraph with its number, and update
> slide 5 and the chapter's ⟨holdout⟩ lines to match.

---

## Numbers to have in your head

| | |
|---|---|
| Right and cited, Run 3 | **72 / 93**, then 76 / 93 since Run 3 |
| Adversarial traps held | **15 / 15** |
| Abstention | **0.76 → 0.52 → 0.52**, then 0.56 since Run 3 (target 0.95) |
| Unanswerable still answered | **12 / 25** |
| Faithfulness when the re-reader arrived | **0.810 → 0.967** |
| Misses with the right page in hand | **19 / 21** |
| Extraction F1 | **0.949**, then 0.961 since Run 3; 0.982 without the insurer-name convention |
| Unsupported claims | **25 / 118**, then 22 since Run 3 |
| Median answer time | **4.4 s** |

---

## Likely questions

**"Why not just set a confidence threshold?"**
We built one on the re-reader's score and swept it (ADR 0019). The unanswerable questions that get
answered are exactly the ones with a genuinely relevant page, so every threshold that caught them
also dropped good answers. It cost two targets we'd cleared to gain a fraction of this one.

**"Can you trust an LLM judge?"**
Not on its own, which is why it isn't the headline. Our judge (qwen2.5 7B, on the machine) scored a
wrong deductible 1.0. The headline is five numbers scored by code against the register, and those
come out identical to four decimals when the same configuration runs twice. The judged metrics
move by up to 0.05 between identical runs, so we don't read anything into a smaller change.

**"Abstention went 0.52 → 0.56. Is that real progress?"**
Be honest: that is one more question of twenty-five. The measurement is deterministic, so it isn't
noise, but it's one question, not a trend. The finding stands.

**"Recall and faithfulness fell in Run 3. Did something regress?"**
Run 3 has a different corpus, three and a half times larger, so the columns aren't a series. And
nineteen of the twenty-one misses had the right page among the six passages read, so search isn't
where they were lost.

**"How do you know the expected answers are right?"**
The corpus was built register-first: every field value was written into the register before the
document was generated. Each golden question cites the document and page from that register, so all
three sets are graded without a human judging the answer.

**"Why that re-ranker?"**
`bge-reranker-v2-m3`, run in-process because Ollama can't serve a cross-encoder (ADR 0018). We
screened four alternatives. The best, mxbai-large, raised abstention to 0.60 but lost seven right
answers, so we kept bge.

**"What else did you try?"**
Three fixes measured and rejected: giving the re-ranker the question in the documents' own words
(cost a right answer); printing each document's reference number in every chunk label (answered a
policy number that doesn't exist); and a different re-ranker (above). One was accepted: letting
word-search match any word of the question rather than every word (#126).

**"Why a 4B model?"**
Everything runs locally, so no household document and no evaluation question leaves the machine.
The median answer takes 4.4 seconds.

**"Is the five-number headline agreed?"**
Proposed, awaiting the supervisor's sign-off. Until then, the nine metrics fixed in week 1 are the
agreed basis, and both are reported.

**"How big is the synthetic-to-real gap?"**
That's the holdout: fourteen real, redacted documents of a planned forty. Say the number if it has
run; otherwise, that it's the next measurement, and it's per document type because fourteen
documents can't support one overall figure.

---

## Things not to say

- **Not "abstention is improving."** It held at 0.52, and 0.56 is one question.
- **Not "ADR 0021 fixes abstention."** It reaches only some cases, and it's switched off.
- **Not "the runs show a trend."** Three corpora, three measurements.
- **Not "it's been tested on real documents"**, until the holdout has run.
