# 15. A name scopes a question, and a grandparent is not a parent

Date: 2026-09-13 · Status: accepted

Extends [0011](0011-the-household-is-people-and-aliases-and-the-owner-is-one-of-them.md) and
the "possessive relations scope" decision in
[0013](0013-a-question-is-understood-before-it-is-searched.md). Neither is superseded.

## Context

Two questions reached the reader with other people's documents in them, both found by reading
`core/graph/scope.py` on 13 September.

- **"Is my grandpa's hospital plan active?"** `grandpa` made the question not first-person, but it
  was not a relation word, so nothing scoped it. The whole vault answered, and the father's
  policy — Lim Ah Kow is recorded as `parent` — was the best match.
- **"What is Marcus's premium?"**, asked by Marcus. No "my", so not first-person, so not scoped;
  Rachel's and Lim Ah Kow's policies mixed in.

`people.relation` allows `self`, `partner`, `child`, `parent` and `other`, and
`0002_household.sql` says why the list is short: anything finer is `other` plus a display name.
The owner's display name is what setup was typed — the name on their documents, in full.

## Decision

- **A grandparent is a relation nobody can hold.** `grandpa`, `grandma`, `grandfather`,
  `grandmother`, `granny`, `ah gong`, `ah ma`, `popo` and their variants map to `grandparent`,
  which is not a value `people.relation` can take. The question abstains with *Parrot does not
  know who your grandpa is yet*, as "my son's" does when no child is recorded. Mapping to
  `parent` answers from the father's policy; mapping to `other` answers from whoever was demoted
  when the household changed hands.
- **Unless the household has said who that is, by name.** When nobody holds a relation, a
  member whose display name or confirmed alias *is* the word — "Grandpa", placed as `other` — is
  who "my grandpa" means. This applies to every relation word, and only when no holder exists,
  so a recorded relation always wins over a name. No migration: the roster already says it.
- **A question naming exactly one person is theirs.** Named means a whole display name or
  confirmed alias anywhere in the question, or one word of those names written possessively
  ("Rachel's", "Marcus'") that belongs to nobody else and has three letters or more. "Lim's",
  shared by Marcus and his father, names nobody; "premium for rachel" is not possessive and is
  not trusted to be a name.
  - The owner named is scoped to the owner, as "my" is.
  - Anybody else named is scoped to them, and the answer prompt says the question is about them,
    not the person asking — the same failure `about` fixed for "my dad's".
  - Two people named, or another person named alongside "my" ("is my premium higher than
    Rachel's?"), is left unscoped. It is about more than one person, and a filter would drop a
    document that answers it. Before this change the second of those was scoped to the owner.
- **Only confirmed names name anybody**, as only confirmed aliases resolve a document.

## Consequences

Scoping by name reuses `scope_to`, so the three buckets hold: a document with no subject is still
kept, and "nothing filed under Rachel answers that" is the abstention when none of hers does.

A household name that is also an ordinary word ("May", "Hope") can scope a question written with
it possessively. The possessive and three-letter rules make that rare rather than impossible, and
the chip on the answer shows who it was scoped to.

"Does Rachel have hospital cover?" is still unscoped when Rachel is known only by her full name:
a bare given name is not trusted. Adding "Rachel" as an alias on the Household page makes it a
whole-name match.

Grandparents are an abstention on every install until somebody records one by name. That is the
honest answer; the roster's relation list is a migration's to widen, not this change's.
