# The final deck, 3 November

`final.js` writes `../Project Parrot Final.pptx`: 21 slides, five segments in the presentation order
of `docs/TEAM.md`, and a close. `build.js` writes Yew Mun's segment on its own, as
`../Project Parrot Final - Yew Mun segment.pptx`. The scripts are the source; the `.pptx` files are
what they produce. Change a slide here, not in PowerPoint, or the next rebuild undoes it.

| File | Slides | Presenter | State |
|---|---|---|---|
| `segments/christian.js` | 1–6: title, problem, solution, privacy, platform, live demo | Christian | **Draft** for Christian |
| `segments/zee.js` | 7–9: four screens, packs, product line | Zee | **Draft** for Zee |
| `segments/desmond.js` | 10–12: corpus, the 15 traps, what synthetic cannot prove | Desmond | **Draft** for Desmond |
| `segments/yew-mun.js` | 13–17: retrieval, the five-number scorecard, what the unsupported claims are, checking the checker, where it stands | Yew Mun | Final |
| `segments/siew.js` | 18–20: governance documents, never acts, the frameworks | Siew | **Draft** for Siew |
| `segments/close.js` | 21: what you did not see, what comes next | Christian | **Draft** for Christian |

The drafts were written on 28 October from what the repository already holds: the midterm script
(`../Parrot Pitch Script.md`), chapters 4, 5 and 7, `docs/governance/`, the corpus register, the
demo run sheet, and screenshots of the running app (`../deck-shots/final-*.jpg`). Each draft slide's
speaker notes begin "DRAFT for …", and several end with what to re-check before the day: the tax
pack's indexing, the governance statuses, and the holdout. **Each owner rewrites their notes in
their own words and edits their own segment file**; nobody else's slides are touched by that.

The look is the midterm deck's: 20" × 11.25", Jost titles, Arial body, the cream, brown and orange
palette, all in `common.js`. Each presenter has their own three layouts, so the footer names
whoever is speaking.

## Rebuilding

It needs Node, `pptxgenjs` and the `apply_theme.js` helper from the pptx skill, which writes the
palette into the deck's theme (without it the colours fall back to Office's defaults):

```
cd docs/report/deck
npm install --no-save pptxgenjs
SKILL=<path to the pptx skill> node final.js "../Project Parrot Final.pptx"
SKILL=<path to the pptx skill> node build.js "../Project Parrot Final - Yew Mun segment.pptx"
```

Neither is a PARROT dependency; nothing in the product reads this folder. Jost must be installed
on the presenting machine.
