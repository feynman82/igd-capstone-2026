// Yew Mun's segment of the final deck: retrieval and the evaluation results.
// Matches the midterm deck: 20" x 11.25", cream / dark brown / orange, Jost titles, Arial body.
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.SKILL + "/scripts/apply_theme.js");

const THEME = {
  name: "Parrot",
  headFontFace: "Jost",
  bodyFontFace: "Arial",
  colors: {
    dk1: "241C14", lt1: "FDFAF3", dk2: "4A3220", lt2: "EFE7D6",
    accent1: "F37021", accent2: "A83C0E", accent3: "8A7358",
    accent4: "3F6B3A", accent5: "9E3A38", accent6: "B07B1E",
    hlink: "A83C0E", folHlink: "8A7358",
  },
};

const pres = new pptxgen();
pres.defineLayout({ name: "PARROT", width: 20, height: 11.25 });
pres.layout = "PARROT";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Yew Mun";
pres.title = "PARROT final deck: retrieval and evaluation";
const C = pres.SchemeColor;

const M = 1.0; // side margin
const W = 20 - 2 * M;

function frame(name, bg, ink, eyebrowColor, footColor) {
  pres.defineSlideMaster({
    title: name,
    background: { color: bg },
    objects: [
      { placeholder: { options: { name: "eyebrow", type: "body", x: M, y: 0.75, w: W, h: 0.45,
          fontFace: "Jost", fontSize: 16, bold: true, charSpacing: 2, color: eyebrowColor, margin: 0, valign: "top" }, text: "" } },
      { placeholder: { options: { name: "title", type: "title", x: M, y: 1.3, w: W, h: 1.5,
          fontFace: "Jost", fontSize: 48, color: ink, margin: 0, valign: "top", align: "left" }, text: "" } },
      { text: { text: "PARROT · IGD ILP 2026", options: { x: M, y: 10.45, w: 8, h: 0.35,
          fontFace: "Jost", fontSize: 13, charSpacing: 2, color: footColor, margin: 0 } } },
      { text: { text: "YEW MUN", options: { x: 20 - M - 4, y: 10.45, w: 3.4, h: 0.35, align: "right",
          fontFace: "Jost", fontSize: 13, charSpacing: 2, color: footColor, margin: 0 } } },
    ],
    slideNumber: { x: 20 - M - 0.55, y: 10.45, w: 0.55, h: 0.35, fontFace: "Jost", fontSize: 13, color: footColor, align: "right" },
  });
}
frame("LIGHT", THEME.colors.lt1, C.text1, C.accent2, C.accent3);
frame("DARK", THEME.colors.dk1, C.background1, C.accent1, C.accent3);
pres.defineSlideMaster({
  title: "ORANGE",
  background: { color: THEME.colors.accent1 },
  objects: [
    { text: { text: "PARROT · IGD ILP 2026", options: { x: M, y: 10.45, w: 8, h: 0.35,
        fontFace: "Jost", fontSize: 13, charSpacing: 2, color: C.text1, margin: 0 } } },
    { text: { text: "YEW MUN", options: { x: 20 - M - 4, y: 10.45, w: 4, h: 0.35, align: "right",
        fontFace: "Jost", fontSize: 13, charSpacing: 2, color: C.text1, margin: 0 } } },
  ],
});

const T = (text, opts) => ({ text, options: opts || {} });
const card = (slide, name, x, y, w, h, fill) =>
  slide.addShape(pres.shapes.RECTANGLE, { objectName: name, x, y, w, h, fill: { color: fill }, line: { type: "none" } });

pres.addSection({ title: "Retrieval and evaluation" });
const S = "Retrieval and evaluation";

// ---------------------------------------------------------------- 1. how it finds the page
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: S });
  s.addText("HOW IT FINDS THE PAGE", { placeholder: "eyebrow" });
  s.addText([T("Search finds the page. "), T("The gate checks every sentence.", { color: C.accent2 })], { placeholder: "title" });

  const steps = [
    ["01", "Two searches", "Meaning and exact words, fused. A policy number is found by its digits, a paraphrase by its sense."],
    ["02", "Re-read", "A second model reads 40 candidates against the question and keeps the best 6."],
    ["03", "Answer", "The local model writes sentences, each naming the passages it came from."],
    ["04", "Check", "Any sentence with no source, or a figure the page does not print, is dropped before it is shown."],
  ];
  const cw = 2.75, gap = 0.3, y0 = 3.35, ch = 5.9;
  steps.forEach(([n, head, body], i) => {
    const x = M + i * (cw + gap);
    const dark = i === 3;
    card(s, "step" + n, x, y0, cw, ch, dark ? THEME.colors.dk1 : THEME.colors.lt2);
    s.addText(n, { isTextBox: true, x: x + 0.3, y: y0 + 0.3, w: cw - 0.6, h: 0.5, fontFace: "Jost", fontSize: 18,
      color: dark ? C.accent1 : C.accent2, margin: 0 });
    s.addText(head, { isTextBox: true, x: x + 0.3, y: y0 + 0.85, w: cw - 0.6, h: 0.7, fontFace: "Jost", fontSize: 26,
      color: dark ? C.background1 : C.text1, margin: 0 });
    s.addText(body, { isTextBox: true, x: x + 0.3, y: y0 + 1.75, w: cw - 0.6, h: 3.8, fontSize: 18, valign: "top",
      color: dark ? C.background1 : C.text2, margin: 0 });
  });

  const sx = M + 4 * (cw + gap) + 0.5; const sw = 20 - M - sx;
  s.addText([T("0.81", { color: C.accent3 }), T(" → ", { color: C.accent3 }), T("0.97", { color: C.accent2 })],
    { isTextBox: true, x: sx, y: 3.35, w: sw, h: 1.4, fontFace: "Jost", fontSize: 72, margin: 0 });
  s.addText("Faithfulness, once the re-reader put the right page in front of the model. The biggest jump in the project.",
    { isTextBox: true, x: sx, y: 4.8, w: sw, h: 1.0, fontSize: 16, color: C.text2, margin: 0, valign: "top" });
  s.addText([T("19", { color: C.accent2 }), T(" of 21", { color: C.accent3 })],
    { isTextBox: true, x: sx, y: 6.2, w: sw, h: 1.2, fontFace: "Jost", fontSize: 60, margin: 0 });
  s.addText("Run 3's wrong answers that had the right page in hand. Search is no longer where answers are lost.",
    { isTextBox: true, x: sx, y: 7.45, w: sw, h: 1.0, fontSize: 16, color: C.text2, margin: 0, valign: "top" });

  s.addNotes(
    "Two searches, because neither alone works on household paperwork: meaning-search can't find a policy by its number, and word-search can't find 'my car cover' when the page says 'motor vehicle'. " +
    "A second model then re-reads forty candidates and keeps six. The last step is the one that makes this ours: a sentence with no source, or with a figure the page doesn't print, never reaches the screen. " +
    "Faithfulness went from 0.81 to 0.97 when the re-reader arrived, the biggest movement we measured. And by Run 3, 19 of the 21 wrong answers on the answerable set had the right page among the six. Search is no longer where we lose answers.");
}

// ---------------------------------------------------------------- 2. the scorecard
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: S });
  s.addText("THE SCORECARD · THREE RUNS", { placeholder: "eyebrow" });
  s.addText([T("Run 3 cleared more lines. "), T("Abstention did not move.", { color: C.accent2 })], { placeholder: "title" });

  const head = (t, al) => ({ text: t, options: { bold: true, fontFace: "Jost", fontSize: 14, color: C.accent3, charSpacing: 1, align: al || "right" } });
  const cell = (t, o) => ({ text: t, options: Object.assign({ fontSize: 17, color: C.text1, align: "right" }, o || {}) });
  const rows = [
    [head("WHAT WE MEASURE · DOCS", "left"), head("TARGET"), head("RUN 1 · 6"), head("RUN 2 · 26"), head("RUN 3 · 93")],
    [cell("Finds the page that answers", { align: "left" }), cell("≥ 0.85"), cell("0.895"), cell("0.897"), cell("0.848", { bold: true })],
    [cell("Reads only pages on point", { align: "left" }), cell("≥ 0.70"), cell("0.868"), cell("0.854"), cell("0.820", { bold: true })],
    [cell("Sticks to what the page says", { align: "left" }), cell("≥ 0.90"), cell("0.819"), cell("0.967"), cell("0.892", { bold: true })],
    [cell("Answers the question asked", { align: "left" }), cell("≥ 0.80"), cell("0.765"), cell("0.779"), cell("0.834", { bold: true })],
    [cell("Files the fields correctly", { align: "left" }), cell("≥ 0.90"), cell("0.898"), cell("0.903"), cell("0.949", { bold: true })],
    [cell("Says 'I don't know' when it should", { align: "left", bold: true, color: C.accent2 }), cell("≥ 0.95", { color: C.accent2 }),
      cell("0.76", { color: C.accent2 }), cell("0.52", { color: C.accent2 }), cell("0.52", { bold: true, color: C.accent2 })],
  ];
  s.addTable(rows, { x: M, y: 3.2, w: 11.6, colW: [4.4, 1.5, 1.9, 1.9, 1.9], rowH: 0.62,
    border: { type: "solid", pt: 0.75, color: THEME.colors.lt2 }, fill: { color: THEME.colors.lt1 }, margin: [0, 0.12, 0, 0.12], valign: "middle" });

  const px = M + 12.3, pw = 20 - M - px;
  card(s, "run3Panel", px, 3.2, pw, 5.6, THEME.colors.lt2);
  s.addText("RUN 3 · 19–20 OCTOBER", { isTextBox: true, x: px + 0.4, y: 3.5, w: pw - 0.8, h: 0.4, fontFace: "Jost", fontSize: 14,
    bold: true, charSpacing: 2, color: C.accent2, margin: 0 });
  const stat = (big, label, y) => {
    s.addText(big, { isTextBox: true, x: px + 0.4, y, w: pw - 0.8, h: 0.85, fontFace: "Jost", fontSize: 44, color: C.text1, margin: 0 });
    s.addText(label, { isTextBox: true, x: px + 0.4, y: y + 0.85, w: pw - 0.8, h: 0.45, fontSize: 15, color: C.text2, margin: 0 });
  };
  stat("72 of 93", "right, and citing the page it is printed on", 4.05);
  stat("15 of 15", "adversarial traps held, nothing leaked", 5.45);
  stat("93 + 25", "answerable questions and hard negatives, on a frozen corpus", 6.85);
  s.addText("Each run had a different corpus, so the columns are three measurements, not a trend.",
    { isTextBox: true, x: M, y: 7.85, w: 11.6, h: 0.45, fontSize: 14, italic: true, color: C.accent3, margin: 0 });
  card(s, "sinceRun3", M, 8.45, 11.6, 1.1, THEME.colors.lt2);
  s.addText([T("SINCE RUN 3 · 22 OCT", { fontFace: "Jost", fontSize: 13, bold: true, charSpacing: 2, color: C.accent2, breakLine: true }),
    T("Same corpus, with the fixes Run 3 found: ", { color: C.text2 }),
    T("76/93 right and cited · abstention 0.56 · extraction 0.961", { bold: true, color: C.text1 })],
    { isTextBox: true, x: M + 0.3, y: 8.55, w: 11.0, h: 0.9, fontSize: 16, margin: 0, valign: "middle" });

  s.addNotes(
    "Three runs. Run 1 on six documents, run 2 after hybrid search and the re-reader, Run 3 on ninety-three documents loaded from a frozen copy of the corpus in a database of its own. " +
    "Run 3 is the first run where every answerable question had its document present, and it clears answer relevancy and extraction comfortably. Recall and faithfulness sit just under their lines on a vault three and a half times bigger. " +
    "The headline numbers: 72 of 93 answers right and cited, all 15 adversarial traps held. And the row in orange: saying 'I don't know' when it should. 0.76, then 0.52, then 0.52. That is the finding. " +
    "The strip at the bottom is the same Run 3 corpus measured again on 22 October with the fixes Run 3 itself found: 76 right and cited, and abstention moves for the first time, to 0.56.");
}

// ---------------------------------------------------------------- 3. the finding (dark)
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: S });
  s.addText("THE FINDING", { placeholder: "eyebrow" });
  s.addText([T("0.76", { color: C.background1 }), T(" → ", { color: C.accent1 }), T("0.52", { color: C.background1 }),
    T(" → ", { color: C.accent1 }), T("0.52", { color: C.accent1 })],
    { isTextBox: true, x: M, y: 1.5, w: 10.2, h: 1.9, fontFace: "Jost", fontSize: 76, margin: 0, fit: "none", wrap: false });
  s.addText("Better search made it worse at saying 'I don't know'. It stayed there through Run 3.",
    { isTextBox: true, x: M, y: 3.7, w: 9.6, h: 1.4, fontFace: "Jost", fontSize: 30, color: C.background1, margin: 0, valign: "top" });
  s.addText("Every document that arrives gives an unanswerable question a page that looks close. A relevant page is the one thing a better search engine always finds.",
    { isTextBox: true, x: M, y: 5.35, w: 9.6, h: 1.4, fontSize: 18, color: C.background2, margin: 0, valign: "top" });
  s.addText([T("12 of 25", { color: C.accent1, bold: true }), T(" unanswerable questions are still answered, each citing a page that exists. No threshold separates them from good answers (ADR 0019).", { color: C.background2 })],
    { isTextBox: true, x: M, y: 7.1, w: 9.6, h: 1.3, fontSize: 18, margin: 0, valign: "top" });

  const qx = 11.4, qw = 20 - M - qx;
  card(s, "labelCard", qx, 1.6, qw, 6.9, THEME.colors.lt1);
  s.addText("WHAT THE TWELVE SHARE", { isTextBox: true, x: qx + 0.45, y: 2.0, w: qw - 0.9, h: 0.4, fontFace: "Jost", fontSize: 14, bold: true, charSpacing: 2, color: C.accent2, margin: 0 });
  s.addText("A real printed value, under a different label.", { isTextBox: true, x: qx + 0.45, y: 2.45, w: qw - 0.9, h: 0.9, fontFace: "Jost", fontSize: 24, color: C.text1, margin: 0, valign: "top" });
  const pair = (said, label, y) => {
    s.addText("PARROT SAID", { isTextBox: true, x: qx + 0.45, y, w: qw - 0.9, h: 0.35, fontFace: "Jost", fontSize: 13, bold: true, charSpacing: 2, color: C.accent3, margin: 0 });
    s.addText(said, { isTextBox: true, x: qx + 0.45, y: y + 0.38, w: qw - 0.9, h: 0.5, fontSize: 19, color: C.text1, margin: 0 });
    card(s, "label" + y, qx + 0.45, y + 0.98, qw - 0.9, 0.62, THEME.colors.lt2);
    s.addText([T("CITING  ", { fontFace: "Jost", fontSize: 13, bold: true, charSpacing: 2, color: C.accent2 }), T(label, { fontFace: "Courier New", fontSize: 17, color: C.text1 })],
      { isTextBox: true, x: qx + 0.7, y: y + 0.98, w: qw - 1.4, h: 0.62, margin: 0, valign: "middle" });
  };
  pair("\u201CThe named driver is Marcus.\u201D", "Name of Insured", 3.45);
  pair("\u201CRoad tax is due 12 April 2026.\u201D", "Period of Insurance From", 5.3);
  s.addText("A score cannot see this; the printed label can. ADR 0021 checks it. It reaches only some cases, and is switched off pending review.",
    { isTextBox: true, x: qx + 0.45, y: 7.2, w: qw - 0.9, h: 1.1, fontSize: 15, color: C.text2, margin: 0, valign: "top" });

  s.addNotes(
    "This is the finding. On six documents, three in four unanswerable questions were declined. As documents arrived, that fell to half, and Run 3 confirms it stays there. Nothing regressed: every new document gives an unanswerable question a page that looks close, and a better search engine is precisely the thing that finds it. " +
    "We tried a threshold on the re-reader's relevance score and measured it: every setting traded away two targets we had cleared for a fraction of this one, so we rejected it, and the ADR records why. " +
    "What the twelve still answered share is on the right. The value is real and printed, just under a different label: 'Name of Insured' read as the named driver, the start of the insurance period read as a road tax date. A score cannot see that; the printed label can. We built a check for it, ADR 0021. It met its own acceptance conditions, two fewer unsupported claims and no right answer lost, but it reaches only some cases, and it is switched off until the team reviews it.");
}

// ---------------------------------------------------------------- 4. checking the checker
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: S });
  s.addText("CHECKING THE CHECKER", { placeholder: "eyebrow" });
  s.addText([T("Three times a number misled us. "), T("Each time, we found out why.", { color: C.accent2 })], { placeholder: "title" });

  const items = [
    ["The scorer was too generous",
     "On ten casually worded questions it passed 7; a person passes 4. The judge model scored a wrong deductible 1.0 because the page it quoted was real.",
     "We now lead with five numbers scored by code against the register, one per promise PARROT makes."],
    ["The test documents leaked into the test",
     "Set C's planted adversarial documents sat in the vault scoring Sets A and B. One printed the real car policy number and outranked the real schedule.",
     "Each set now has its own vault, and Run 3 was loaded from a frozen commit anyone can rebuild."],
    ["One word made two alerts false",
     "The new renewal notices print 'Mr Marcus Lim Jun Wei'. The title stayed in the name, matched nobody, and his policies were reported lapsed.",
     "Titles are stripped from names. On Run 3's corpus: no false alert, all 118 answers unchanged."],
  ];
  const cw = 5.75, gap = 0.375, y0 = 3.2, ch = 6.2;
  items.forEach(([head, found, fix], i) => {
    const x = M + i * (cw + gap);
    card(s, "check" + i, x, y0, cw, ch, THEME.colors.lt2);
    s.addText(String(i + 1).padStart(2, "0"), { isTextBox: true, x: x + 0.4, y: y0 + 0.35, w: 1.5, h: 0.5, fontFace: "Jost", fontSize: 18, color: C.accent2, margin: 0 });
    s.addText(head, { isTextBox: true, x: x + 0.4, y: y0 + 0.9, w: cw - 0.8, h: 1.0, fontFace: "Jost", fontSize: 24, color: C.text1, margin: 0, valign: "top" });
    s.addText(found, { isTextBox: true, x: x + 0.4, y: y0 + 2.05, w: cw - 0.8, h: 2.1, fontSize: 16, color: C.text2, margin: 0, valign: "top" });
    s.addText([T("WHAT CHANGED  ", { fontFace: "Jost", bold: true, color: C.accent2, fontSize: 13, charSpacing: 2, breakLine: true }), T(fix, { color: C.text1 })],
      { isTextBox: true, x: x + 0.4, y: y0 + 4.3, w: cw - 0.8, h: 1.7, fontSize: 16, margin: 0, valign: "top" });
  });

  s.addNotes(
    "An evaluation is only worth what it measures. Three times a number told us something false, and each time we traced it rather than tuning to it. " +
    "First, the scorer passed answers a person would reject, and the judge model was no better. So the report now leads with five numbers scored by code, one per promise in our README. " +
    "Second, the adversarial documents planted to test injection were sitting in the database we used to score normal questions, and one of them was winning. Now each set gets its own database, and Run 3 ran on a frozen corpus. " +
    "Third, the module metrics. Both Run 3 alerts were false, and the cause was one word: 'Mr' stayed in an extracted name, matched nobody in the household, and two alerts said Marcus's policies had lapsed. We strip titles now, and measured the fix on Run 3's exact corpus.");
}

// ---------------------------------------------------------------- 5. closing (orange)
{
  const s = pres.addSlide({ masterName: "ORANGE", sectionTitle: S });
  s.addText("WHERE IT STANDS", { isTextBox: true, x: M, y: 0.75, w: W, h: 0.45, fontFace: "Jost", fontSize: 16, bold: true, charSpacing: 2, color: C.text1, margin: 0 });
  s.addText("15 of 15", { isTextBox: true, x: M, y: 2.2, w: 9, h: 2.4, fontFace: "Jost", fontSize: 150, color: C.text1, margin: 0 });
  s.addText("adversarial traps held in Run 3. The one absolute line, kept.", { isTextBox: true, x: M, y: 4.75, w: 8.4, h: 1.2, fontFace: "Jost", fontSize: 26, color: C.text1, margin: 0, valign: "top" });
  s.addText("12 of 25", { isTextBox: true, x: 10.6, y: 2.2, w: 8.4, h: 2.4, fontFace: "Jost", fontSize: 150, color: C.background1, margin: 0 });
  s.addText("unanswerable questions still answered. The work left is teaching it when to stop.", { isTextBox: true, x: 10.6, y: 4.75, w: 8.4, h: 1.2, fontFace: "Jost", fontSize: 26, color: C.background1, margin: 0, valign: "top" });
  s.addText("Next: the holdout, 14 real and redacted documents, tells us how much of this survives real paperwork.",
    { isTextBox: true, x: M, y: 7.6, w: W, h: 1.0, fontFace: "Jost", fontSize: 22, color: C.text1, margin: 0, valign: "top" });

  s.addNotes(
    "Where it stands after Run 3. Fifteen of fifteen adversarial traps held: nothing forbidden leaked, which is the one line we treat as absolute. " +
    "And twelve of twenty-five unanswerable questions still get an answer. The engine finds the page; what it still has to learn is when not to answer from it. " +
    "Everything you've seen is on synthetic documents. The holdout, fourteen real, redacted documents, is the honest test of how much of it survives real paper.");
}

(async () => {
  const out = process.argv[2];
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("wrote", out);
})();
