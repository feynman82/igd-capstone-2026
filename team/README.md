# The team

Five people, ten weeks, three committers. Ownership is by **directory**, not by task, so
the split is written down in [`CODEOWNERS`](../.github/CODEOWNERS) rather than left to
memory. `CODEOWNERS` requests the right reviewer automatically, but it cannot block a
merge — `main` is unprotected, see
[ADR 0010](../docs/adr/0010-main-is-unprotected-by-convention.md).

Each folder here holds a person's **brief** and their **task list**. Their actual work
lives in the functional directories — that is deliberate, and section "Why work does not
live here" explains why.

| Person | Lane | Owns | Brief | Tasks |
|---|---|---|---|---|
| **Christian** | A · Integration and product | `core/contracts.py`, `core/graph/`, `core/adapters/`, `core/ingest/`, `modules/`, `db/migrations/`, the merge queue | [brief](christian/README.md) | [tasks](christian/tasks.md) |
| **Yew Mun** | B · Retrieval and evaluation | `core/retrieve/`, `eval/` | [brief](yew-mun/README.md) | [tasks](yew-mun/tasks.md) |
| **Siew** | C · Governance and assurance | `docs/governance/`, `eval/sets/adversarial/` | [brief](siew/README.md) | [tasks](siew/tasks.md) |
| **Zee** | D · Domain packs and interface | `packs/` (including each pack's `grounding/`), `web/` | [brief](zee/README.md) | [tasks](zee/tasks.md) |
| **Desmond** | E · Corpus and adversarial testing | `corpus/` | [brief](desmond/README.md) | [tasks](desmond/tasks.md) |

The reasoning behind the split — why these five lanes and not some other five — is in
[`docs/TEAM.md`](../docs/TEAM.md).

---

## The dependency that sets the order

```
Zee commits a pack.yaml
        │
        ▼
python -m packs.build  generates  corpus/register/<pack>_columns.csv
        │
        ▼
Desmond fills the register, then generates documents to match it
        │
        ▼
Yew Mun measures extraction and retrieval against known ground truth
        │
        ▼
Siew's model card and test report cite those numbers
```

Nothing downstream of a pack can start until its field names are fixed. That is why
Lane D runs first in week 1, and why a field rename in week 6 is a conversation rather
than a commit.

Christian's lane is orthogonal: contracts and the database schema land in week 1, before
anything depends on them, and then he integrates rather than building features.

---

## Why work does not live here

`team/<name>/` holds a brief, a task list and a status log. It does **not** hold code,
packs, corpus batches or governance documents.

The reason is mechanical. A field name written in `packs/iras_tax/pack.yaml` generates a
column heading in `corpus/register/iras_tax_columns.csv` and an attribute in
`packs/iras_tax/schemas.py`. If those three files lived under `zee/` and `desmond/`, the
generator, the CI gate, the imports and `CODEOWNERS` would all have to be rewritten per
person — and the moment somebody left a lane, every path would move again.

Accountability comes from `CODEOWNERS`, which maps each directory to the person who
reviews changes to it. It is better than folder naming, because GitHub applies it to every
pull request rather than leaving it to everyone remembering — but it *requests* a review,
it does not require one. `main` is unprotected and a merge can happen without the owner's
approval, so the last step is still a person choosing to wait for it. See
[ADR 0010](../docs/adr/0010-main-is-unprotected-by-convention.md).

---

## The task lists are generated

`docs/team-tasks.csv` is the single source of truth for all 80 tasks, and it is also the
file imported into Notion. Per-member lists are generated from it:

```bash
python scripts/build_team_tasks.py          # regenerate team/<slug>/tasks.md
python scripts/build_team_tasks.py --check  # CI gate: fails if stale
```

To change a task, edit the CSV and regenerate. Editing `tasks.md` directly gets
overwritten and fails CI, for the same reason hand-editing `schemas.py` does.

The same CSV is what gets imported into Notion — see [`docs/NOTION.md`](../docs/NOTION.md)
for the property mapping and the weekly sync loop.

---

## Everyone, regardless of lane

**Twelve golden-set questions for your own area, by the end of week 3.** Highest-value
work with the lowest barrier to entry, it is the one task that otherwise bottlenecks on
a single person, and it forces each of us to state what "correct" means for the thing we
built.

**Ninety minutes a week for integration, protected.** Christian merges everything and
deletes the duplicate helpers three people's agents wrote in the same week. Cheaper every
time than discovering the divergence in week 8.

**One vertical slice per pull request.** A PR should let somebody do something new, not
add a layer.

---

## The presentation split

The rubric scores each presenter individually, and its top band requires that the
presenter "spoke and participated at a very high and balanced level". A team where one
person narrates 25 slides cannot reach it.

| Segment | Owner |
|---|---|
| Problem, personas, expansion model, live demonstration | Christian |
| The interface and the two domain packs | Zee |
| The corpus, how it was built, and the adversarial findings | Desmond |
| Retrieval design and the evaluation results | Yew Mun |
| Governance, the regulatory mapping, the autonomy boundary | Siew |
