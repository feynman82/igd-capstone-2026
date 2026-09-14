# The pack catalogue — eleven packs, two built

**Owner: Zee (Lane D).** Reviewed by Christian.

Two packs are built. Nine are specified here and deliberately not built. That is a
materially different claim from "we could add more": a specified pack names its document
types, the modules it registers and the grounding it would index, against
[`core/contracts.py`](../core/contracts.py) — the same contract the two built packs
validate against. If an entry below cannot be expressed in that contract, the entry says
so rather than quietly inventing a field the contract does not have.

This file supersedes the eleven-pack table in
[`docs/artefacts/architecture-review.html`](../docs/artefacts/architecture-review.html) §06
for the nine deferred packs. That table was written against a draft schema — it uses
`owns_document_types`, a separate `extraction:` block, `obligations:` inside the reminder
registration and a metric called `uncovered_months`, none of which survived into
`PackManifest`. The domains and the module choices there are still right, and are carried
over unchanged. Only the shape has been brought up to date.

---

## 1. What an entry has to name

Every entry fills the same four things a real `pack.yaml` fills.

| Entry says | Manifest field | The rule it has to satisfy |
|---|---|---|
| **Document types** | `document_types` | 3–5 per pack, each a *shape* rather than an issuer. A type is one a person would use one word for. |
| **Anchor date** | `registers.reminder[].from_field` | A reminder reads a **date field printed on one of this pack's own document types**, or a fixed `on_date`. A pack that cannot name one cannot register a reminder. |
| **Modules** | `registers` | Only `reminder`, `alert` and `tracker` exist — `PrimitiveId` is a `Literal`, so there is no fourth. |
| **Grounding** | `grounding.corpus` | An official issuer's published guidance, or `null`. `null` is a designed guardrail, not a gap (`packs/README.md` §7). |

Three things are the same in all eleven and are not restated per entry: `must_cite: true`,
`never_acts: true` and `never_recommends: true`. The first two are `Literal[True]` in the
contract, so a pack that disagrees does not load. Each pack still writes its own persona,
disclaimer and `advice_decline`, because those are domain-specific and Siew reviews them.

**Two costs a specified pack must be honest about.**

- **An alert metric is not a field.** `AlertConfig.metric` names a hand-written query in
  `modules/alert/queries.py` — `METRICS` currently holds four. A deferred pack that
  registers an alert is naming work in Lane A, not in a YAML file, and the entry says which
  metric it would need.
- **The tracker module does not exist.** `modules/` holds `reminder` and `alert`. Five of
  the nine below register a tracker, and all five are blocked on that module being built
  (`web/docs/user-stories.md` §6 is the same gap seen from the interface).

---

## 2. Built

| Pack | Document types | Registers | Grounding |
|---|---|---|---|
| **Tax and Reliefs** `iras_tax` | `payslip`, `donation_receipt`, `cpf_statement`, `srs_statement`, `notice_of_assessment` | Reminder (`filing_deadline`, `srs_contribution_cutoff`, `tax_payment_due`), Alert (`srs_contributions_ytd`), Tracker (specified) | `null` until IRAS pages are recorded and signed off — W6 |
| **Insurance and Coverage** `insurance_agent` | `policy_schedule`, `renewal_notice`, `claim_letter`, `benefit_illustration`, `policy_anniversary_statement` | Reminder (`policy_expiry`, `renewal_payment_due`), Alert (`days_uncovered`) | `null` — answers only from the household's own policies |

Both are the worked examples. A tenth pack copies their shape, not this table.

---

## 3. The nine

### 3.1 `vehicle_road_tax` · Vehicle and Road Tax

Household. The closest of the nine to something buildable, because every document prints a
hard date and the household already holds a car.

- **Document types** `road_tax_notice`, `inspection_notice`, `servicing_invoice`, `coe_certificate`
- **Anchor date** `road_tax_expiry` on `road_tax_notice`; `inspection_due` on `inspection_notice`
- **Registers** Reminder (`road_tax_expiry`, lead `[30, 14, 3]` — arrange, pay, expires); Alert — would need a `days_unroadworthy` metric, the same shape as `days_uncovered` but keyed on the vehicle plate rather than the insured person
- **Grounding** LTA published renewal and inspection schedules — a named regulator, so admissible
- **Boundary** A motor *policy* is `insurance_agent`'s `policy_schedule`, not this pack's. One document shape, one owning pack: the architecture review listed "motor policy" here, and that is the one change of substance I have made to its table.

### 3.2 `travel` · Travel

Household. Small, seasonal, and the one pack where the most useful answer is about a
document's *validity* rather than its content.

- **Document types** `booking_confirmation`, `travel_policy`, `passport`, `visa`
- **Anchor date** `expiry_date` on `passport` and `visa`; `departure_date` on `booking_confirmation`
- **Registers** Reminder (`passport_expiry`, lead `[180, 90, 30]` — the six-month rule is the point, so the first window is the useful one)
- **Grounding** ICA published passport validity rules
- **Boundary** `travel_policy` overlaps `insurance_agent`. It stays here, because a traveller asks about it beside a visa and a flight rather than beside a car policy — the one deliberate exception to the rule in 3.1, and it is an exception because the question, not the document, decides.
- **Governance** A passport is an identity document. `iras_tax` already refuses to store an NRIC without Siew's sign-off; this pack would put the same question to her before it is built.

### 3.3 `children_school` · Children and School

Household. The pack the Lims would install next, since Lucas is six.

- **Document types** `term_calendar`, `enrichment_invoice`, `consent_form`, `assessment_result`
- **Anchor date** `reply_by` on `consent_form`; `due_date` on `enrichment_invoice`
- **Registers** Reminder (`consent_reply_due`, lead `[7, 2]` — a consent form is short-fused); Tracker (`enrichment_spend_ytd`) — **blocked on the tracker module**
- **Grounding** MOE published school terms and holidays

### 3.4 `caregiving_health` · Caregiving and Health

Household. The sandwich generation's pack, and the one with the sharpest advice boundary in
the whole catalogue.

- **Document types** `discharge_summary`, `prescription`, `lab_report`, `appointment_letter`
- **Anchor date** `appointment_date` on `appointment_letter`; `review_date` on `discharge_summary`
- **Registers** Reminder (`appointment_due`, lead `[7, 1]`); Tracker (`out_of_pocket_ytd`) — **blocked on the tracker module**
- **Grounding** `null`. Deliberately: MOH publishes guidance, but a pack that cites it while reading a lab report is one sentence away from interpreting a result. This pack answers only from the household's own documents.
- **Boundary** `never_recommends` does the heavy lifting here. "Is this reading normal?" is a clinical judgement and is declined, not hedged. Its `advice_decline` is the one Siew should review first.

### 3.5 `home_maintenance` · Home Maintenance

Household. Unglamorous, and the clearest demonstration that a pack needs no grounding at all.

- **Document types** `warranty_card`, `service_contract`, `contractor_invoice`, `appliance_manual`
- **Anchor date** `warranty_expiry` on `warranty_card`; `contract_end` on `service_contract`
- **Registers** Reminder (`warranty_expiry`, lead `[60, 14]` — decide whether to extend, then it lapses); Alert — would need a `repairs_spend_per_appliance` metric, which is the first metric in the catalogue that is a *sum per thing* rather than a gap between dates
- **Grounding** `null`. Nothing published governs whether a fridge is still under warranty; the warranty card does.

### 3.6 `property_tenancy` · Property and Tenancy

Household. Where the money is, and the pack most likely to be asked a question it must refuse.

- **Document types** `tenancy_agreement`, `mortgage_statement`, `mcst_notice`, `valuation_report`
- **Anchor date** `lease_end` on `tenancy_agreement`; `due_date` on `mcst_notice`
- **Registers** Reminder (`lease_end`, lead `[90, 60, 30]` — a tenancy needs notice, so the windows are long); Tracker (`housing_cost_ytd`) — **blocked on the tracker module**
- **Grounding** `null`. A valuation is not advice and this pack must not imply one.

### 3.7 `legal_estate` · Legal and Estate

Household. The narrowest pack in the catalogue, on purpose.

- **Document types** `will`, `lasting_power_of_attorney`, `title_deed`, `insurance_nomination`
- **Anchor date** `review_date`, where the document prints one. Most do not — so this pack is the catalogue's example of a reminder that may have nothing to read, and `registers.reminder` is therefore optional rather than assumed.
- **Registers** Reminder (`document_review_due`) only where a date is printed
- **Grounding** `null`
- **Boundary** **Location and named contacts only, never interpretation.** "Where is the will and who is the executor" is answerable from the paper. "What does clause 4 mean" is legal advice, and `never_recommends` declines it. If a future version cannot hold that line, the pack should not ship.

### 3.8 `groceries_supplies` · Groceries and Supplies

Household. The weakest of the nine, and worth saying so rather than padding the number.

- **Document types** `grocery_receipt`, `delivery_order`
- **Anchor date** none printed that anybody acts on
- **Registers** Tracker (`grocery_spend_by_month`) — **blocked on the tracker module**; Alert (`grocery_spend_vs_ceiling`)
- **Grounding** `null`
- **Honest assessment** Two document types, below the 3–5 the guide asks for; no reminder, because a receipt has no actionable date; and its whole value is a total, which is the one module that does not exist. It is in the catalogue because a household genuinely holds these documents, but it should be the last of the nine built, not the first — and if the tracker module is never built, it should be dropped rather than shipped hollow.

### 3.9 `moe_syllabus` · Teaching and Syllabus

**Professional, not household** — and the only one of the nine that is. That is the reason
it is interesting and the reason it needs a decision before it is built.

- **Document types** `test_paper`, `worksheet`, `report_card`, `school_circular`
- **Anchor date** `reply_by` on `school_circular`; `submission_date` on `report_card`
- **Registers** Reminder (`circular_reply_due`, lead `[14, 3]`); Tracker (`papers_by_topic`) — **blocked on the tracker module**
- **Grounding** MOE published primary and secondary Mathematics and Science syllabus documents
- **The decision it forces** Every other pack reads the filing cabinet of a household of five. This one reads a teacher's professional filing cabinet: the subject of a `report_card` is a pupil, who is not a member of the household that holds the document. Household scoping (ADR 0011, ADR 0015) is built on the opposite assumption. Until that is resolved this pack is specified, not deferred-but-ready — and the resolution is a contract question for Christian, not a field-list question for me.

---

## 4. What the nine say as a set

**Five of nine register a tracker, and the tracker module does not exist.** Children and
School, Caregiving, Property, Groceries and Teaching all want a running total. That is the
single highest-leverage unbuilt thing in the system, and it is one module rather than five
packs' worth of work. It should be an ADR before it is a pull request.

**Six of nine need no grounding at all.** Caregiving, Home Maintenance, Property, Legal,
Groceries and — today — both built packs answer from the household's own documents. The
platform argument does not depend on indexing the internet, and the expansion model is
cheaper than it looks because of it.

**Three would need a new alert metric**, one hand-written query each, in Lane A: a
roadworthiness gap, a spend-per-appliance sum, a spend-against-ceiling sum. Two of those
three are the same shape as each other, which suggests the second metric written will be
easier than the first.

**One is a household-scoping question, not a pack.** Teaching and Syllabus reads documents
about people who are not in the household. It stays in the catalogue as the example of a
domain the contract does not yet reach, which is more useful than pretending it does.

---

## 5. How to build one

Copy `packs/_template/pack.yaml`, follow [`packs/README.md`](README.md), and use the
`/authoring-a-domain-pack` skill — it stops for an answer at each stage rather than running
to the end. The entry above gives the document types and the modules; it does not give the
field list, because that comes from looking at three or four real examples of each document
(`packs/README.md` §4, step 2) rather than from a table.
