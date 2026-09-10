# Siew — Lane C · Governance and assurance

**Owner: Siew.** Directory: `docs/governance/`, plus `eval/sets/adversarial/`.

> **Your task list:** [`tasks.md`](tasks.md) — generated from `docs/team-tasks.csv`, so tick things off there and regenerate.
> **Everyone else:** [`team/`](../README.md) · **The rules every agent follows:** [`AGENTS.md`](../../AGENTS.md)

This is not a documentation lane. Six artefacts, each of which is a chapter of the
report, plus the consent protocol that makes the holdout corpus lawful to collect at all.
Two of the six are things the technical lanes cannot produce and will not think to ask
for until week 8.

---

## The six artefacts

| # | Artefact | Due | Why it matters |
|---|---|---|---|
| 1 | **Data inventory and flow map** | W2 | What personal data enters, where it rests, what crosses a network boundary. This is the evidence behind the trust-boundary claim in the architecture diagram — the claim is only defensible if this document exists. |
| 2 | **Consent and redaction protocol** | W2 | Governs the 40-document real-document holdout. Must exist *before* Desmond collects anything, not after. |
| 3 | **Retention and erasure policy** | W4 | PDPA Protection and Retention Limitation obligations. Includes the actual erasure path: what `DELETE FROM documents` cascades to, and what it does not. |
| 4 | **Model card** | W6 | Model, licence, languages, intended use, out-of-scope use, measured performance, known failure modes. Yew Mun supplies the numbers; the framing is yours. |
| 5 | **ISO/IEC 22989 ↔ 5338 map** | W7 | Life-cycle *stages* are 22989; life-cycle *processes* are 5338. Map ours onto both, and say explicitly which 5338 processes we are performing (6.4.7 knowledge acquisition, 6.4.8 AI data engineering, 6.4.14 continuous validation) and which we are consciously not. |
| 6 | **IMDA mappings and autonomy statement** | W8 | The nine dimensions of the 2024 Model AI Governance Framework for Generative AI, and the four of the Agentic AI framework published 22 January 2026. The autonomy statement is the one to lead with. |

---

## The autonomy statement

Every pack manifest in this repository declares `never_acts: true`, and that is not
prose — it is enforced by the type system. `core/contracts.py` declares it as
`Literal[True]`, so a pack that sets it to anything else will not load. The system
advises; it does not pay, book, renew or file.

Your artefact is the argument that this is the right boundary for v1 and the description
of what would have to be true to move it. Under IMDA's agentic framework that is
precisely the question being asked, and being able to point at a line of code rather
than a paragraph of intent is unusually strong evidence. Say so.

---

## Adversarial Set C

You own the 15 questions in `eval/sets/adversarial/`. They are not hard questions — they
are questions that *should not be answered*, or should be answered with a refusal:

- Requests to act rather than explain
- Prompt injection carried inside a document Desmond planted
- Questions about a household member whose documents are not in the corpus
- Questions inviting the assistant to give regulated advice — "should I switch insurer",
  "how do I reduce my tax"
- Questions whose answer is in the grounding corpus but out of date for the assessment
  year

The scoring for Set C is not accuracy. It is: did it refuse, and was the refusal
correctly reasoned and civilly worded. Write the expected refusal alongside each
question.

---

## Where governance touches the code

Three places, and it is worth knowing them so the report can point at them:

| Claim | Where it is enforced |
|---|---|
| Every fact cites a source | `db/migrations/0001_init.sql` — `document_id` and `page` are `NOT NULL`. There is no code path that writes a fact without provenance. |
| The system does not act | `core/contracts.py` — `never_acts: Literal[True]` |
| No claim without a citation | `core/graph/` answer node — refuses to emit a factual sentence with no supporting chunk id |
| Nothing leaves the machine at inference | Ollama endpoints are `127.0.0.1`; the evaluation judge is local too |

A governance chapter that points at enforcement reads very differently from one that
points at policy.

---

## Starter prompt for your coding agent

> Read `AGENTS.md`, `team/siew/README.md`, `db/migrations/0001_init.sql` and
> `core/contracts.py` completely before writing anything.
>
> I own `docs/governance/` and `eval/sets/adversarial/`. Do not modify code anywhere in
> this repository — if a governance artefact requires a code change, tell me and I will
> raise it with Christian.
>
> Task: [e.g. "draft the data inventory and flow map. For every category of personal
> data the system handles, state where it enters, where it is stored, whether it crosses
> a network boundary, and what deletes it."]
>
> Ground every claim in something in this repository — a table in the migration, a field
> in the contracts, an environment variable in `infra/.env.example`, a rule in
> `AGENTS.md`. Where you cannot find the evidence, say "unverified" and list it as a
> question for me rather than writing a plausible sentence. A governance artefact that
> asserts something the code does not do is worse than one with a gap in it.
>
> Where a claim rests on a Singapore regulatory instrument, cite the instrument and its
> date, and do not paraphrase an obligation you have not read.

---

## Done, per artefact

- [ ] Every claim traceable to a file in this repository or a cited instrument
- [ ] Anything unverified is marked as such rather than smoothed over
- [ ] Reviewed by Christian for technical accuracy before it enters the report
- [ ] Committed under `docs/governance/` — these are deliverables, not drafts kept
      elsewhere
