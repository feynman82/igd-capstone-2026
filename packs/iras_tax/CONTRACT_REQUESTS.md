# Tax and Reliefs — contract changes this pack needs

Two pieces of tax advice cannot be calculated with the contract as it stands, so the pack
explains them from the IRAS grounding instead. Each fix is a change to `core/contracts.py`
and `modules/advice/`, which is a separate, reviewed pull request under AGENTS.md hard rule 4.
They are written down here so that pull request can be opened by whoever owns it (Christian).

## 1. A deduction multiplier on `estimate_saving`

**What is wrong.** `estimate_saving` works out *amount × marginal rate*. That is right for SRS,
because each dollar contributed is a dollar of relief. A qualifying donation to an Institution
of a Public Character is deducted at 250% of the amount given, so the saving is
*amount × 2.5 × marginal rate*. The calculator has no input for the 2.5.

**What would fix it.** An optional rule role, say `deduction_multiple`, read from an approved
grounding value (`unit: multiple`), defaulting to 1 when the shape does not declare it. The
number then comes from the IRAS page and goes through the same review as every other value. It
is not typed into YAML.

**What the pack would then add.** A `donation_saving` shape reading
`donation_receipt.donation_amount` (`take: sum`) and `notice_of_assessment.assessable_income`.

## 2. Limiting a fact input to one year

**What is wrong.** CPF cash top-up relief is capped per calendar year, at $8,000 for your own
account and $8,000 for family members. `remaining_room` needs the total topped up *this year*.
A `FactInput` can take the `latest` receipt or the `sum` of every receipt on file. The sum
includes past years, so the room would read as smaller than it is. The same applies to donations
once a household keeps several years of receipts.

**What would fix it.** A `take: sum_this_year` option (or a `year_field` on `FactInput`) that
sums only the rows whose date field falls in the calendar year before the Year of Assessment
being asked about.

**What the pack would then add.** A `cpf_topup_room` shape reading
`cpf_topup_receipt.topup_amount`, with a `cpf_topup_relief_cap` grounding value.

## Not a contract change: parent relief

Parent relief depends on the parent's age, income and where they live. No household document
prints those things, so they are household data and not fields to extract. The pack explains
parent relief from the grounding and calculates nothing for it.
