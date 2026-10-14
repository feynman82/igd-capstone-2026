# §7.4 · Commercialisation roadmap

**Owner: Zee (Lane D), for Christian's §7.** It feeds §7.4, "Readiness and the adoption path",
and the money slide of the final deck. It is one page by design.

> **Draft status.** Nothing on this page is a market measurement. There is no pricing, no market
> size and no unit economics. That is deliberate, for the reason the proposal gave (§11): a price
> tier without evidence behind it is weaker than saying where the evidence stops. Each claim
> below points at a file in this repository.

---

## The claim

Parrot is sold the way it is built. The core is common: retrieval, citation, abstention and
the household. **Domain packs are the unit of sale**, and capability modules multiply what each
pack can do. That is not a business model added afterwards. The contract already enforces it.

- **One file per domain.** A pack is a YAML file the core loads (ADR 0017).
- **Two packs are built.** Insurance and Coverage (`packs/insurance_agent/`) and Tax and Reliefs
  (`packs/iras_tax/`).
- **Nine more are specified and test-checked.** They are written against the same contract
  (`packs/catalogue.yaml`, checked by `tests/test_pack_catalogue.py`).

A new domain is a file and a reviewed core change, not a release. So the product line can grow
without the product changing.

## Segments, from the five personas

Each persona in the proposal (§2) is a segment, and each already maps to a pack and a module.
The cost of the pain is the hypothesis about willingness to pay. It is stated, not measured.

| Persona | Segment | What they would buy | What the pain costs them |
|---|---|---|---|
| Priya, 32 | Self-directed savers | Tax and Reliefs pack, Alert | A missed SRS top-up has a dollar value: the relief forgone |
| Marcus, 39 | The sandwich generation | Insurance, then Caregiving and Health | Not knowing which policy covered a parent's admission |
| Daniel and Rachel | Time-poor dual-income households | Insurance, then Vehicle and Road Tax, Reminder | A lapsed motor policy, found out at the worst moment |
| Sarah, 35 | Parents running the family calendar | Children and School, Reminder | A school deadline learned the morning it falls due |
| Jason, 40 | The self-employed | Tax and Reliefs, Tracker | Business and household spending blurred at tax time |

The table's order is a guess at willingness to pay. The two built packs serve the segments
whose losses can be counted in dollars. That is also why they were built first.

## Three routes to revenue (hypotheses, untested)

These are the three routes named in the pitch (`docs/report/Parrot Pitch Script.md`):

1. **Household.** The core stays on the household's laptop, and packs are bought one at a time.
2. **Professional seat.** An insurance agent reviews a client's cover with the client's
   recorded consent. The coverage review and its consent flow already exist (ADR 0016).
3. **Pack marketplace.** A domain expert publishes their knowledge as a pack. This only works
   because a pack is data: its grounding needs recorded provenance, and its advice is
   calculated by reviewed code, not written by the model.

## The two constraints we can defend

1. **On-device inference narrows the market to recent, capable hardware.** The minimum
   specification is still unconfirmed, and the only test machine is a 32 GB laptop with an
   RTX 4060 (`docs/RUNNING.md`, "Hardware qualification"). The proposal's 8 GB figure for the
   demo card is a planning estimate (§5.4). That points to a hybrid version in
   which retrieval stays local and heavier reasoning escalates only with explicit consent and
   redaction.
2. **A WhatsApp-first product carries a per-message cost.** Meta ended the free
   service-message window on 1 October 2026 (proposal §3.2 and §11). That cost must be
   modelled, not assumed away, which is why the prototype captures through Telegram and a
   watched folder.

**One boundary is a position, not a constraint.** Every pack sets `never_acts: true`, and the
type system enforces it (`core/contracts.py`). Parrot advises; it does not pay, book or file.
Selling a version that transacts would change the governance case completely (§6.4), so it is
off the roadmap, not deferred.

## Roadmap

| Stage | What ships | What must be true first |
|---|---|---|
| **Now: the prototype** | Core, Insurance and Tax packs, Reminder and Alert | Run 3 on real redacted documents, the gap to synthetic stated (§5) |
| **Next: the household product** | Packs from the catalogue, chosen by the segment table above | A minimum hardware specification measured, not estimated |
| **Then: the professional seat** | An insurance-agent seat on the same core | A position on the Financial Advisers Act: the advice wording already says Parrot is not a licensed adviser |
| **Later: the marketplace** | Packs written by others | A published pack contract, and a provenance review that scales beyond Siew |

## What this page does not claim

It claims no price, no market size and no conversion rate. Measuring any of them needs users,
and a nine-week prototype has none. The roadmap is stated at the level the evidence in this
repository supports.
