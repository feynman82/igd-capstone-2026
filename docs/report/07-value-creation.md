# §7 · Value creation and organisational readiness

> **Draft.** Written from the repository for Christian and Zee to rewrite in their own words.

---

## 7.1 The individual and the household

This value is argued, not demonstrated: no household has used PARROT. The case is a person who asks
about their own papers and gets a page back, and hears of a date before it passes, with the
reasoning on their own machine (proposal §1). Time saved and money recovered have not been
measured. The corpus shows the shape of the loss, not its size: an invented hospital renewal rises
40 per cent across two documents. Run 3 did not answer the question about it; the check on 28 October did. Obligation
precision was 0.8125 against 0.95.

## 7.2 The organisation

This case is a design argument too. No organisation has tried PARROT, and the roadmap's three revenue
routes are untested.

It rests on the two axes (§3.3). The core is common, so a new domain is a file and a reviewed core
change, not a release. Modules then apply without new code: Reminder needs only a printed date, so
eight of the nine specified packs use it. For an organisation, a new domain would cost knowledge and
review more than engineering.

The nearest setting is on the roadmap: an insurance agent reviewing a client's cover, which would
need client consent (ADR 0016) and a position on the Financial Advisers Act. Any other setting would
need a new pack and document types.

Two controls would matter to a reviewer in any of these. A claim opens on its page, and in advice,
code chooses the verdict while the model only explains.

## 7.3 The industry

PARROT offers a worked pattern, not a market position. Answering runs on the owner's hardware with
an open model from AI Singapore, and the governance is mapped to the PDPA, ISO/IEC 5338 and IMDA's
frameworks. A sector unwilling to hand records to a cloud service gains an option to weigh. It also
carries a warning. A judge scored a wrong deductible 1.0 because the quoted passage was real, and
citation does not cure false claims (Magesh et al., 2025). An adopter should score against ground
truth.

## 7.4 Readiness and the adoption path

| An organisation needs | Why |
|---|---|
| Hardware | The generator and embedder fill 7.4 GB of a 10 GB card before the reranker loads, and no minimum specification is confirmed |
| Its own ground truth | Every number here is on synthetic documents about one household |
| A named pack owner | Nothing is cited until a person reviews it |

The holdout has not been run, and nobody outside the team has used the interface.
Run 3 missed five lines. Each roadmap stage has an unmet condition: a measured hardware
specification, a position on the Financial Advisers Act, and pack review beyond one reviewer. Acting
stays off the roadmap.

After the holdout and usability test (§8), three things must be built:

1. **Per-person access.** One passphrase covers a household, and the API answers any local request
   unauthenticated.
2. **Continuous validation.** Nothing re-runs the evaluation after deployment.
3. **Hybrid mode.** Heavier reasoning escalates only with consent and redaction, for machines that
   cannot hold the stack.
