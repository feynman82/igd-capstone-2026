# absence-needs-every-kind — 2026-10-15

Sets A, B; retrieval hybrid, reranker cross-encoder; generator `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M`; judge `none`; corpus `8f7e6c432f1f7497`; code `29b55a9`.

What changed, what moved, and whether that was expected:

One change: `AnswerGraph._absence` no longer writes "None of the N … is X" when any of the N
documents could not be categorised. Compared with
[`2026-10-15-fixtures-removed`](2026-10-15-fixtures-removed.md), the same vault without fixtures.

| Headline | before | after | |
|---|---|---|---|
| Right and cited (Set A) | 36/50 | **40/50** | better |
| Unsupported claims (all sets) | 25/77 | **20/77** | better |
| Over-caution (Set A) | 4/50 | 4/50 | — |
| Casual-phrasing gap | 0.275 | **0.125** | narrower |

**Why it moved.** `b1-0001`'s product name was extracted as "Comprehensive Cover", its
*Coverage Type* line, not the "Private Car Insurance Policy" printed at the head of the schedule.
That names no category, so the inventory counted the car schedule as a policy of no kind, and
every car question opened with "None of the 11 policies … is a car or motor policy" while citing
it. That was defect 2 of #48, alive since run 1, and it accounted for five of the fourteen Set A
misses. `a-b01`, `a-b03`, `a-b13` and `a-b14` are now right and cited; for example, `a-b01`
answers "The car insurance expires on 11 April 2027. [b1-0001.pdf, page 1]". `a-b15` loses its
false absence and abstains (traceability), so it leaves unsupported claims but is still not right.
No question got worse.

**What the headline did not see.** Three Set B items, `b-b03`, `b-b12` and `b-b15`, all about the
car, had been "declined" by that same false sentence. Set B does not count a false absence as a
claim, so they scored as correct abstentions while telling the person they have no car policy.
They now abstain honestly, which the headline cannot show. The cost is `b-b01` ("When does my
travel insurance expire?"). Its "none is a travel policy" was very probably true, and it is now a
floor abstention (0.43 < 0.45). While any policy cannot be categorised, the inventory cannot say
"no", and in this vault three cannot (`b1-0001`; `b2-0005` CareShield ElderPlus Plan, which the
`long_term_care` rule's `careshield life` misses; `b2-0006` Junior HealthProtect Plan).

**Not from this change.** Corpus `8f7e6c432f1f7497` against `79d610547eaca546`: #72 and #74
corrected the CPF and payslip register rows and regenerated those PDFs between the runs, but the
vault still holds the old payslips. Payslip extraction F1 falls 1.00 → 0.67 and the total
0.9028 → 0.875 for that reason, not because of this change. No Set A or B question moved because
of it. Re-ingest the payslips before the next measured run.
