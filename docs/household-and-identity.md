# The household, and the word "my"

**Written for §3 and §4 of the report, and for §8.** This is the source document for the
identity model: what problem it solves, why it is shaped the way it is, what it costs, and what
it does not do. The decision itself is [ADR 0011](adr/0011-the-household-is-people-and-aliases-and-the-owner-is-one-of-them.md);
this is the argument around it.

---

## 1 · The failure this fixes

PARROT's central claim is that every factual sentence carries the document and page it came
from. That claim is enforced in code: `core/graph/gate.py` drops any sentence whose supporting
chunk ids were not among the ones retrieved, and `guardrails.must_cite` is true in every pack
manifest. A user can press a citation and see the page.

There is exactly one way for that mechanism to produce a confidently wrong answer, and it is
not a bug in the gate.

Consider a household with two term life policies filed — one on Marcus, one on Rachel — and the
question **"what is my term life premium?"**

1. Retrieval embeds the question and returns the nearest chunks. Both policies match: they use
   the same vocabulary, describe the same product, and differ only in whose name is on them.
2. Reranking scores question against passage. A cross-encoder has no representation of *which
   human being* a document is about, so it orders by textual relevance.
3. The answer node writes a sentence from the highest-ranked passage and attaches that
   passage's chunk id.
4. The gate checks that the sentence is supported by a retrieved chunk. **It is.**

The answer is delivered with a correct citation to the wrong person's policy. Every check in
the system passes. A user who follows the citation sees a real term life policy with a real
premium on it and has no way to notice that it is not theirs unless they read the name.

This is the only failure mode in the architecture that citation does not defend against, and it
is not exotic: it appears the moment a second person's paperwork enters the vault. For the five
personas in the proposal — all of them households of three or more — that is immediately.

The word `my` had nothing to bind to. `facts.subject` already recorded whose each fact was;
nothing recorded which of those people was holding the keyboard.

## 2 · What already existed

The fix is smaller than it sounds, because the domain model was already half right.

```
pack.yaml           document_types.<type>.subject_field: insured
   │
   ▼
core/ingest/extract.py   reads that field off the page
   │
   ▼
facts.subject            the string the document printed
   │
   ├──► modules/reminder   labels an obligation "policy expiry — Marcus Fernandez"
   ├──► modules/alert      groups a metric by subject
   └──► core/vault.py      shows it beside the field
```

Every pack already declares, per document type, which field says whose document it is. Five of
the Insurance pack's document types and five of the Tax pack's carry a `subject_field`. The
extractor writes it, three consumers read it.

So PARROT knew whose every fact was. What it lacked was a **referent for the first person**.

## 3 · Why a roster is not a setup form

The obvious design is a first-run screen that asks the user to list their household. We rejected
it, and the reasoning generalises beyond this feature.

`facts.subject` is a **printed string**. The same person appears as `MARCUS LIM JUN WEI` on a
payslip, `Lim Jun Wei, Marcus` on a policy schedule, and `M. J. W. Lim` on a renewal notice.
Matching is therefore not a matter of knowing who lives in the house; it is a matter of knowing
which strings their documents actually use.

A person filling in a roster on first run is working from memory, before a single document has
been filed, with no feedback about whether what they typed will match anything. They will type
their own first name. They will spell a parent's name the way they say it rather than the way
IRAS prints it. The output is a roster that looks complete and matches nothing — the worst
possible state, because it is indistinguishable from a working one until an answer is wrong.

So the roster is **derived, then confirmed**:

| | |
|---|---|
| **Setup asks one question** | "The name on your documents." One field. The owner is the one person anybody can name without thinking, and the interface needs something to greet them with. |
| **Everybody else arrives off a document** | Extraction produces a subject string; if no alias covers it, the generator is asked who it is; the proposal is written down **unconfirmed**. |
| **A person answers** | A row on Today, in the same shape as the quarantine queue: *Who is RACHEL NG HUI SHAN?* — That's me · Rachel · Someone else here · Not one of us. |
| **Only then does it count** | `resolve()` and `owner_aliases()` read confirmed aliases only. |

The last line is the one that makes the model safe to use here. An unconfirmed proposal scopes
nothing, so a wrong guess costs a tap. That is why the generator is allowed to guess at all.

This is the same derive-then-confirm loop the product already uses twice — the quarantine queue
and the vault correction — so it teaches no new interaction. That was a design constraint, not a
coincidence.

## 4 · The data model

Two tables, in `db/migrations/0002_household.sql`, plus two for provenance.

```
people                    person_aliases
  id                        id
  display_name              person_id ──────┐
  relation                  alias           │  the literal string a document printed
  is_owner   ◄── exactly    source          │  setup | model | user
  external       one, by    confirmed       │  nothing unconfirmed scopes an answer
                 unique     confidence      │  the generator's own, for tuning later
                 index      document_id     │  the page that raised the question
                                            │
facts.subject  ─────────────────────────────┘  matched on lower(btrim(...)), never rewritten
```

Three properties are worth stating because each one was a decision:

**`facts.subject` is never normalised or rewritten.** The alias table sits beside it and maps
it. What the page said stays what the page said, so correcting the roster later cannot
retroactively edit the record of what a document claimed. This mirrors the existing rule that
`identifier` fields are stored verbatim.

**Exactly one owner, enforced by a partial unique index** (`CREATE UNIQUE INDEX … WHERE
is_owner`) rather than by application code. "Who is me" is the predicate every first-person
answer is scoped by; two of them is not a state any screen knows how to render, so the database
refuses it.

**The owner is a row, not a config value.** Households are handed over — a daughter takes over
her father's paperwork — and an install that cannot follow that gets abandoned rather than
corrected. `PUT /api/household/owner/{id}` moves it, and demotes the previous owner to `other`
rather than guessing their new relation.

Two further tables record where a document came from rather than what it says.
`telegram_identities` maps a chat to a person, and `document_attribution` records the result.
This is the only ownership signal that arrives *before* parsing: a payslip photographed on
Rachel's phone is Rachel's payslip whatever the OCR makes of the name at the top. Extraction may
still read a different name, and the disagreement becomes a question rather than a silent
overwrite of either.

## 5 · Resolving "my" — three buckets, not two

`core/graph/scope.py` partitions the retrieved passages:

| Bucket | Example | Behaviour |
|---|---|---|
| **Mine** | a fact whose subject resolves to the owner | keep |
| **Someone else's** | resolves to another person | drop |
| **The household's** | `subject IS NULL` — home contents, a utility bill | **keep** |

The third bucket is the one an implementation forgets. A home contents policy names nobody
because it belongs to the address rather than to a person; excluding it would break "my home
insurance" while looking like an empty vault. Presence also wins over exclusion: a joint policy
naming both the owner and their partner is the owner's too.

Detection of the first person is deliberately conservative. `"my term life premium"` is
first-person; `"my wife's term life premium"` is not, and neither is `"when does Rachel's policy
renew"`. A question containing a relationship word, or the display name or alias of any
non-owner, is left unscoped and answered from the whole vault — the behaviour PARROT had before
this existed. An over-eager filter that silently drops the one document which would have
answered is worse than no filter, because it fails as an *absence* rather than as an error.

## 6 · Two safeguards

**Not finding you is an answer.** When a question is first-person and nothing resolving to the
owner survives the filter, PARROT abstains and names what it does hold:

> There are documents for Rachel Ng Hui Shan, but none for Marcus Lim.

This is more useful than the number the user did not ask for, and it tells them something they
did not know. It also converts a silent failure into a designed state, which is the same move
`components/states.tsx` makes for every other failure in this system.

**A scoped answer says whose it is.** When the evidence was narrowed to a person, the answer
carries a chip reading *for Marcus Lim — only their documents were read*. The reasoning is
identical to the citation chip's: the defence against being wrong is showing the working, not
being careful. A bad alias becomes something a user can see on the screen that used it.

## 7 · What this cost, and what it did not

Implemented as one vertical slice across four lanes. `core/contracts.py` was **not** touched: a
household is not a pack and not a module, and the file defining those two has no business
defining a third. `core/graph/ports.py` — the contract with Lane B's `core/retrieve/` — was also
not touched, which is why scoping happens *after* retrieval rather than as a SQL predicate.

That last choice has a measurable cost and it should be reported honestly: **a passage that did
not survive the candidate cut cannot be scoped back in.** With `CANDIDATES = 40` over a
household vault of tens of documents this is not currently reachable, but it is a real ceiling
and it is the right thing to hand to Lane B when hybrid search lands. Pushing the predicate into
the query is a retrieval change and belongs with a retrieval measurement.

This work also made rule 4 of `AGENTS.md` more precise. The rule held `db/migrations/` behind a
separate review; it now admits one narrow exception — a migration whose every statement is
`CREATE` — on the reasoning that a new table nothing reads yet cannot break work in flight.
`ALTER`, `DROP`, backfills and `core/contracts.py` stay behind the original rule.

## 8 · What it enables, for §5 and §8

**A new thing to measure.** The golden set can now hold questions whose correct answer depends
on who is asking, including the abstention case — asking about a policy you do not have. PARROT
previously had no measurement for *whether an answer was about the right person*, because it had
no way to be wrong about it on purpose.

**A limitation to state.** The alias matcher compares on case and surrounding whitespace and
nothing else. Initial expansion, reordered surnames, maiden names and romanisation variants are
all handled by asking a person rather than by an algorithm. That is correct for a v1 whose whole
posture is "advise, never act", and it is a real constraint: a household that files many
documents in a short period will answer several questions in their first week.

**A risk worth naming in §6.** Attributing documents to named individuals creates a record of
who in a household owns what. It is local, it is in the same Postgres as everything else, and it
is covered by the retention policy — but it is a category of personal data the system did not
previously hold in a queryable form, and the data inventory should say so.
