# 11. The household is people and aliases, and the owner is one of them

Date: 2026-09-12 · Status: accepted

## Context

Parrot could not answer "what is my term life premium?".

Not because the question is hard, but because `my` had nothing to attach to. `facts.subject`
already carries whose document a fact came off — `pack.yaml` declares `subject_field` per
document type, the extractor writes it, the Reminder module labels with it, the Alert module
groups by it, and the vault shows it. Parrot knew whose every fact was. It did not know which
of those people was the person typing.

With two term life policies filed — one on Marcus, one on Rachel — the question retrieves
both. Reranking picks by text similarity, which has no opinion about people, and the answer
node writes a sentence from whichever passage ranked first, with a citation.

**That citation is correct.** The passage says what the sentence says. The grounding gate
checks that a sentence is supported by a retrieved chunk, and this sentence is. So the one
defence this architecture has — no claim without a citation — passes a confidently wrong
answer about the wrong person straight through to a household that has no way to tell.

It is the only failure mode in the system that citation does not catch, and it appears the
moment a second person's paperwork is in the vault, which for the households this is built for
is immediately.

A second problem sits underneath it. `facts.subject` is the string the document printed:
`MARCUS LIM JUN WEI` on the payslip, `Lim Jun Wei, Marcus` on the policy schedule,
`M. J. W. Lim` on the renewal notice. Three strings, one man. Knowing the owner's name is not
enough; the names have to be reconciled.

## Decision

**A person is a row. The strings on documents are aliases pointing at it.**

`people` holds the person: a display name, a relation to the owner, and whether they *are* the
owner. `person_aliases` holds every literal string seen on a document, each resolving to a
person, each carrying how it was decided and by whom.

**`facts.subject` does not change.** It keeps the printed string, unnormalised, exactly as
`identifier` fields are kept. The alias table maps it at query time. No backfill, no rewrite,
and the audit trail stays honest: the document said what it said, and a later correction to the
roster cannot retroactively edit what was on the page.

**The roster is derived, then confirmed — not enumerated.**

The instinct is a setup form: list your household before you begin. It is the wrong shape. On
first run a person is typing names from memory, before a single document is filed, with no
feedback about whether what they typed matches what their documents actually say — and the
match is the only thing that matters.

So setup asks one question: the name on your documents. One field, because the owner is the one
person anybody can name without thinking, and because the interface needs something to greet
them with. Every other person arrives the way every other fact arrives: off a document.

**The model proposes; the person disposes.** When extraction produces a subject string no alias
covers, the generator is asked one constrained question — is this the owner, someone in this
household, or someone outside it — given the roster so far and the document it came off. Its
answer is written as an *unconfirmed* alias and surfaces on Today in the shape quarantine
already uses: here is what I think, is that right. Nothing the model decided is treated as
settled until a person has said so, and the resolver ignores unconfirmed aliases when it scopes
a question. A wrong guess costs a tap, never a wrong answer.

**Three buckets, not two.** A question about "my" documents includes facts whose subject
resolves to the owner, excludes facts that resolve to another person, and **includes facts with
no subject at all** — the home contents policy, the utility bill, the things that belong to the
household rather than to anyone in it. Two buckets would silently break "my home insurance",
and it would break quietly, which is the worst way.

**Not finding you is an answer.** When a question is first-person and nothing in the vault
resolves to the owner, Parrot abstains and says what it does have: *you have no term life
policy filed; there is one for Rachel Ng Hui Shan*. That is more use than the number, and it is
the difference between a system that is honest about people and one that is merely confident.

**A resolved person is shown, like a citation.** When a question was scoped to somebody, the
answer carries a chip saying to whom. A wrong alias should be visible on the screen that used
it, for the same reason a claim carries its page: the defence against being wrong is showing
your working, not being careful.

**The owner can change.** It is a row, not a config value baked at install. Households are
handed over — a daughter takes over her father's paperwork — and an install that cannot follow
that is an install that gets abandoned rather than corrected.

**Telegram chats map to people.** The bot already allowlists `chat_id`. Mapping a chat to a
person means a document's owner is known at capture, before anything is parsed, which is a
better signal than anything inferable from the page and costs one table.

## Consequences

`my` works, and it works through the retriever rather than through prompt wording, so it holds
when Lane B replaces the dense-only stopgap.

The first-person question becomes evaluable. `eval/sets/` can hold questions whose correct
answer depends on who is asking, and the abstention case — asking about a policy you do not
have — is a golden-set row rather than an anecdote. It also becomes a way to measure something
this project had no measurement for: whether an answer is about the right person.

The roster is a new thing a person can get wrong. A household with two Lims, or a maiden name
on one document and a married name on another, will need corrections. That is why aliases are
confirmed rather than inferred, why the resolved person is shown in the answer, and why the
roster is editable from the Vault rather than only at setup.

`db/migrations/0002_household.sql` is additive — four `CREATE TABLE`s and their indexes, no
change to anything that exists — which is what the amended rule 4 now allows inside a feature
PR. `core/contracts.py` is untouched: a household is not a pack and not a module, and the file
that defines those two things has no business defining a third.

The cost is a table nobody can see the value of until the second person's paperwork arrives.
For a single-person household it is dead weight, and it is still right to build, because the
households in the proposal all have at least three people in them.
