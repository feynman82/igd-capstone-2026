# Field extraction F1 by document type — 2026-10-01

Metric 6 of `eval/README.md`, split by `doc_type`. Target ≥ 0.90. Scored against `corpus/register/` by `python -m eval.report`; corpus `210231c041def426`, code `f688e9f`.

26 of 50 register rows are indexed in the vault, 3 quarantined, and 23 of them produced facts to score. The catalogue defines 16 document types, the register fills 14, and 7 have an indexed document to score.

| document type | docs | fields | tp | fp | fn | precision | recall | F1 | ≥ target |
|---|---:|---:|---:|---:|---:|---:|---:|---:|:--:|
| `loan_agreement` | 2 | 13 | 8 | 1 | 4 | 0.889 | 0.667 | 0.762 | ✗ |
| `policy_schedule` | 12 | 108 | 85 | 6 | 17 | 0.934 | 0.833 | 0.881 | ✗ |
| `identity_card` | 4 | 12 | 12 | 0 | 0 | 1.000 | 1.000 | 1.000 | ✓ |
| `payslip` | 2 | 12 | 12 | 0 | 0 | 1.000 | 1.000 | 1.000 | ✓ |
| `birth_certificate` | 1 | 3 | 3 | 0 | 0 | 1.000 | 1.000 | 1.000 | ✓ |
| `passport` | 1 | 4 | 4 | 0 | 0 | 1.000 | 1.000 | 1.000 | ✓ |
| `renewal_notice` | 1 | 6 | 6 | 0 | 0 | 1.000 | 1.000 | 1.000 | ✓ |
| **every type** | 23 | 158 | 130 | 7 | 21 | 0.949 | 0.861 | 0.903 | ✓ |

## Which fields hold them down

Only the types under target, and within each only the fields that are not already 1.0. `fn` is a value the register prints and the extractor did not write; `fp` is a value it wrote that the register does not have, or wrote differently.

### `loan_agreement` — F1 0.762 over 2 documents

| field | tp | fp | fn | precision | recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| `agreement_date` | 0 | 0 | 2 | — | 0.000 | — |
| `borrower` | 1 | 1 | 1 | 0.500 | 0.500 | 0.500 |
| `monthly_repayment` | 1 | 0 | 1 | 1.000 | 0.500 | 0.667 |

### `policy_schedule` — F1 0.881 over 12 documents

| field | tp | fp | fn | precision | recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| `excess` | 0 | 0 | 6 | — | 0.000 | — |
| `maturity_date` | 0 | 1 | 1 | 0.000 | 0.000 | — |
| `expiry_date` | 5 | 0 | 6 | 1.000 | 0.455 | 0.625 |
| `product_name` | 8 | 4 | 4 | 0.667 | 0.667 | 0.667 |
| `sum_insured` | 11 | 1 | 0 | 0.917 | 1.000 | 0.957 |

## Types the register fills and the vault has not indexed

Not a weakness and not a zero: there is no document to extract from yet, so they are absent from the table above rather than scored at 0. `benefit_illustration`, `claim_letter`, `cpf_statement`, `donation_receipt`, `notice_of_assessment`, `policy_anniversary_statement`, `srs_statement`.

## Indexed documents no register row claims

3 document(s) in the vault are named for what they are rather than for a register row, so the 17 facts extracted from them are neither hits nor misses — there is nothing to compare them against. `corpus/README.md` makes the file name the register id, so each of these is a rename away from being measurable (`core/ingest/register.py` re-registers on `sha256`, keeping the document id and its citations).

| document in the vault | facts extracted |
|---|---:|
| `Rachel_donation_receipt-v3` | 5 |
| `privatecare_hospital_surgical_full_policy` | 7 |
| `thye_hua_kwan_donation_receipt-v2` | 5 |

## How to read it

The headline `extraction_f1` of 0.903 clears the 0.90 target and the split says not to lean on
it. Eleven of the 23 scored documents are identity cards, passports, birth certificates and
payslips with three to six fields each, every one of them perfect; the type that carries the
corpus, `policy_schedule`, is 108 of the 158 scored fields and sits at 0.881. As the other seven
register types land this number should be expected to **fall**, not rise, because the easy types
are the ones already in the vault.

The failures are recall, not precision: 0.949 against 0.861, 7 false claims against 21 misses.
The extractor is cautious — it rarely writes something the register does not have, and it leaves
a lot out. The misses are also concentrated in three fields rather than spread across the schema,
and each one has a specific cause that this run is enough to name:

- **`expiry_date` — 5 of 11, and the split is the printed date format.** Every schedule that
  prints `Period of Insurance To: 11 April 2027` was extracted; every schedule that prints
  `Period of Insurance To: 2027-02-28` was missed, 6 for 6. Same label, same field, declared
  `date | None` in `core/document_schemas.py`. `b1-0032` and `b2-0004` are the controlled pair:
  the same product with the same expiry, spelled out on one and ISO on the other, extracted on
  one and null on the other.
- **`excess` — 0 of 6, including the plainest case there is.** `b2-0004` is a clean, 519-character
  schedule printing `Excess: 3500.00` on its own line, and nothing was written. It is not a
  missing field: `excess` is in the `policy_schedule` schema as `Decimal | None` and
  `FACT_COLUMNS` maps it to `value_num`. The extractor is returning null for a labelled number
  it was asked for.
- **`product_name` — 8 of 12, and only two of the four misses are the extractor's.** On `b1-0001`
  and `b2-0009` the register's name is printed verbatim on the page and the extractor wrote the
  cover description instead (`Comprehensive Cover` for `Private Car Insurance Policy`) — a real
  error, and the schema already says "not a category". On `b1-0031` and `b1-0033` the register's
  name is not printed on the document at all, which is the register-against-document disagreement
  [issue #19](https://github.com/feynman82/igd-capstone-2026/issues/19) is about. So two of the
  seven false claims in the whole table are the corpus disagreeing with itself, not the extractor
  being wrong, and precision is understated by that much.
- **`agreement_date` — 0 of 2**, on a type with two documents. Two is a sample, not a measurement;
  `loan_agreement`'s 0.762 should not be quoted without that caveat.

Four caveats on the table as a whole. Seven of the fourteen types the register fills have no
indexed document, so this is a report on half a corpus. Three ingested specimens are named for
what they are rather than for a register row, so 17 extracted facts are invisible to the metric
in either direction — a rename joins them. `field_pages` is filled on 0 of 50 register rows, so
this table can say which field was missed but not which page it was missed on. And an indexed
document that yielded no facts at all would now score as a miss on every field rather than
dropping out of the metric, which is new in this run; no document is currently in that state, so
the number is unaffected by the change.
