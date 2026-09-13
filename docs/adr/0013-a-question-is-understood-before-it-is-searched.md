# 13. A question is understood before it is searched, and scoped before it is cut

Date: 2026-09-13 · Status: accepted

## Context

"If i had a fall, and warded for 1 night, does my insurance cover the cost?" abstained: *best
match 0.42, this pack answers above 0.45*. The same question with "in the hospital" added
answered. The right clause was already ranked first; it scored 0.416. A person should not have to
guess the documents' vocabulary, and "warded", "kena" and "can claim?" are how this household
talks.

Three more failures surfaced while measuring it, on the live vault (six policies):

- A follow-up ("when does it expire?") was searched on its own, because the web chat sent only
  the newest message.
- "How much is my son's life insurance?" answered from the owner's own whole life policy, cited,
  calling the owner "your son". "My son's" was left unscoped by design, so nothing narrowed it.
- "Is my dad's hospital cover still active?" was scoped after the list had already been cut to
  six passages, all the owner's, and the prompt then told the model the parent was the one asking
  and never said what today's date was.

## Decision

- **Understand, then search.** After the router, one model call writes the question as a whole
  question, using the conversation so far, plus two or three short search queries in the
  documents' own words. Every phrasing, the person's own words always among them, is searched; a
  passage keeps its best score, so the pack's floor stays a similarity.
- **The router is unchanged and separate.** Folding understanding into it made "how much is my
  pet insurance premium?" a request to act, and wrote weaker search wording.
- **The conversation travels.** `AskRequest.history` carries up to twelve earlier turns; the web
  chat sends the person's questions and Parrot's verified sentences. History is read only by the
  understanding step. It is never evidence and cannot be cited.
- **Possessive relations scope.** "My son's", "my dad's" scope to household members holding that
  relation; nobody holding it, or somebody who works for the household ("my maid's"), is an
  abstention that says Parrot does not know who that is. Scoping moved before the cut to six.
- **The answer prompt carries today's date**, and names a scoped relation as who the question is
  about, never as the asker. It also says never to claim a kind of cover exists unless a passage
  names it.
- **The floor stays at 0.45.** Lowering it was measured and rejected.

## Evidence

Retrieval, fused best score against the 0.45 floor (13 September, GPU):

| | answerable, over floor with the document in the top six | near-miss negatives over floor |
|---|---|---|
| the question as asked | 10 of 12 | 0 of 8 |
| plus one rewrite | 8 of 10 (a different, harder set) | 1 of 8 |
| plus two or three document-worded searches | **10 of 10**, fall question 0.511 | 3 of 8 |

With the floor lowered instead, the reader answered "do i have travel insurance?" (0.38) with
"You have travel insurance." and quoted the hospital premium for "how much is my pet insurance
premium?". A separate model call grading relevance before answering fixed one of five
near-misses and added 1.4 s; an `answerable` flag in the answer schema emptied six of eight real
answers. Both were dropped.

End to end after the change: the fall question and its "what about 3 nights?" follow-up answer
from the room-and-board clause; "when does it expire?" after the car policy answers "11 April
2027"; "is my dad's hospital cover still active?" answers from Lim Ah Kow's policy with its dates;
son's, maid's, travel and pet questions abstain; "ok renew it for me" is refused. Two to ten
seconds each on the GPU.

## Consequences

One more model call per question, about a second on the GPU.

**Still weak, and retrieval's to fix.** "Warded for dengue 3 days, can claim?" answered from the
critical illness policy rather than the hospital plan; "got warded 2 days, claimable?" said the
passages do not address falls; "do i have car insurance?" and schedule-table questions rank by
luck. A cross-encoder reranker reads the passage against the question instead of comparing two
vectors, and lexical search matches "car insurance" to a title. Both are Lane B's, and the
`Retriever` port is unchanged so they drop in. Three near-miss negatives now reach the reader, so
the reranker is also what should keep them out.
