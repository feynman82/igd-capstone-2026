# Lane instructions

`docs/TEAM.md` says who owns what and why. These files say **what you do on Monday**.

| Lane | Owner | Instructions |
|---|---|---|
| A · Integration and product | Christian | [lane-a-integration.md](lane-a-integration.md) |
| B · Retrieval and evaluation | Yew Mun | [lane-b-retrieval-eval.md](lane-b-retrieval-eval.md) |
| C · Governance and assurance | Siew | [lane-c-governance.md](lane-c-governance.md) |
| D · Domain packs and interface | Zee | [`packs/README.md`](../../packs/README.md) |
| E · Corpus and adversarial testing | Desmond | [lane-e-corpus.md](lane-e-corpus.md) |

Each file has the same four sections: what you own, the order to do it in, a starter
prompt for your coding agent, and what "done" means. Read `AGENTS.md` first regardless
of lane — it is the working agreement every agent in this repository is given.

## The dependency that matters

```
Zee commits a pack.yaml
        │
        ▼
python -m packs.build generates corpus/register/<pack>_columns.csv
        │
        ▼
Desmond fills the register, then generates documents to match it
        │
        ▼
Yew Mun can measure extraction and retrieval against known ground truth
```

Nothing downstream of a pack can start until its field names are fixed. That is why
Lane D runs first in week 1, and why a field rename in week 6 is a conversation rather
than a commit.
