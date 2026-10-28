# Lane B's deck segment

`build.js` writes the five slides in `../Project Parrot Final - Yew Mun segment.pptx`: retrieval,
the three-run scorecard, the abstention finding, what the measurement got wrong, and where it
stands. It is the source; the `.pptx` is what it produces. Change a number here, not in PowerPoint,
or the next rebuild undoes it.

The slides match the midterm deck: 20" × 11.25", Jost titles, Arial body, the cream, brown and
orange palette. Every figure comes from `docs/report/05-evaluation-and-results.md`, which cites its
result files.

## Rebuilding

It needs Node, `pptxgenjs` and the `apply_theme.js` helper from the pptx skill, which writes the
palette into the deck's theme (without it the colours fall back to Office's defaults):

```
cd docs/report/deck
npm install --no-save pptxgenjs
SKILL=<path to the pptx skill> node build.js "../Project Parrot Final - Yew Mun segment.pptx"
```

Neither is a PARROT dependency; nothing in the product reads this folder. Jost must be installed
on the presenting machine.
