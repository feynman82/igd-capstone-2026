## What this changes

<!-- One or two sentences. If this is a vertical slice, say what a user can now do. -->

## Lane

- [ ] A — Christian · contracts, core, ingestion, modules, integration
- [ ] B — Yew Mun · retrieval and evaluation
- [ ] C — Siew · governance and assurance
- [ ] D — Zee · domain packs and interface
- [ ] E — Desmond · corpus and adversarial

## Checks

- [ ] `make check` passes
- [ ] New behaviour is covered by a test using corpus fixtures with known ground truth
- [ ] No change to `core/contracts.py` or `db/migrations/` in this PR
- [ ] No new runtime dependency (or: ADR linked below)

## Evaluation

<!-- Required if this touches retrieval, extraction or the grounding gate.
     Paste the output of `make eval-quick` and say in one line why the numbers moved. -->

| metric | before | after |
|---|---|---|
| context recall |  |  |
| context precision |  |  |
| faithfulness |  |  |
| extraction F1 |  |  |
| abstention rate (Set B) |  |  |
