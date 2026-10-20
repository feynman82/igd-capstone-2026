# §7.4 · Commercialisation roadmap

**Owner: Zee (Lane D), for Christian's §7.** It feeds §7.4 and the money slide of the final deck.
It claims no price, market size or conversion rate. Measuring those needs users, which a
nine-week prototype does not have (proposal §11). Every other claim points at a file.

## Packs are the unit of sale

Parrot is sold the way it is built. The core is common: retrieval, citation, abstention and the
household. **Domain packs are what a customer buys**, and modules multiply what each pack can
do. This is not a model added afterwards; the contract already enforces it:

- a pack is a YAML file the core loads (ADR 0017);
- two packs are built (`packs/insurance_agent/`, `packs/iras_tax/`);
- nine more are specified and checked by a test (`packs/catalogue.yaml`).

A new domain is a file and a reviewed core change, not a release.

## Segments, from the five personas

Willingness to pay is a hypothesis, ordered by how countable the loss is (proposal §2).

| Persona | Segment | Would buy | What the pain costs |
|---|---|---|---|
| Priya, 32 | Self-directed savers | Tax, Alert | The relief lost on a missed SRS top-up |
| Marcus, 39 | Sandwich generation | Insurance, Caregiving | Not knowing which policy covered a parent's stay |
| Daniel and Rachel | Dual-income, time-poor | Insurance, Vehicle, Reminder | A motor policy that lapsed unnoticed |
| Sarah, 35 | Parents running the calendar | Children and School, Reminder | A school deadline learned on the day |
| Jason, 40 | The self-employed | Tax, Tracker | Business and household spending blurred at tax time |

The two built packs serve the first two segments, whose losses can be counted in dollars.

## The two constraints we can defend

1. **Hardware:** running the model on the device limits buyers to recent, capable machines,
   since the only tested one is a 32 GB laptop with an RTX 4060 (`docs/RUNNING.md`), so the
   product needs a hybrid mode that escalates heavier reasoning only with consent and redaction.
2. **Channel:** Meta began charging for WhatsApp service messages on 1 October 2026 (proposal
   §3.2), so a WhatsApp-first product carries a per-message cost, which is why capture runs
   through Telegram and a watched folder.

`never_acts: true` is a position, not a constraint: Parrot advises and never pays, books or files
(`core/contracts.py`), so a transacting version is off the roadmap.

## Roadmap

Each later stage is one of the three revenue routes named in the pitch. All three are untested.

| Stage | What ships | What must be true first |
|---|---|---|
| **Now: prototype** | Core, Insurance and Tax packs, Reminder and Alert | Run 3 on real redacted documents (§5) |
| **Household product** | Catalogue packs, bought one at a time | A measured minimum hardware spec |
| **Professional seat** | An insurance agent reviews a client's cover, with consent (ADR 0016) | A position on the Financial Advisers Act |
| **Pack marketplace** | Packs written by domain experts | A published pack contract, and provenance review that scales beyond one reviewer |
