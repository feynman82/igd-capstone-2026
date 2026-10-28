// Yew Mun's segment: retrieval and the evaluation results. Every figure comes from
// docs/report/05-evaluation-and-results.md, which cites its result files.
module.exports = function yewMun({ pres, C, THEME, M, W, T, card, masters }) {
  const S = "Retrieval and evaluation";
    pres.addSection({ title: S });
    const L = masters("Yew Mun");

  // ---------------------------------------------------------------- 1. how it finds the page
  {
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
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
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
    s.addText("THE SCORECARD · ONE NUMBER PER PROMISE", { placeholder: "eyebrow" });
    s.addText([T("Scored by code, not by a judge. "), T("Do not guess comes first.", { color: C.accent2 })], { placeholder: "title" });

    const head = (t, al) => ({ text: t, options: { bold: true, fontFace: "Jost", fontSize: 14, color: C.accent3, charSpacing: 1, align: al || "right" } });
    const cell = (t, o) => ({ text: t, options: Object.assign({ fontSize: 17, color: C.text1, align: "right" }, o || {}) });
    const key = { bold: true, color: C.accent2 };
    const rows = [
      [head("THE PROMISE · DOCS", "left"), head("RUN 1 · 6"), head("RUN 2 · 26"), head("RUN 3 · 93"), head("SINCE RUN 3")],
      [cell("Do not guess: unsupported claims", Object.assign({ align: "left" }, key)), cell("9/44", key), cell("19/64", key), cell("25/118", key), cell("22/118", key)],
      [cell("Right, and citing its page", { align: "left" }), cell("16/19"), cell("31/39"), cell("72/93", { bold: true }), cell("76/93")],
      [cell("Holds back when the page was read", { align: "left" }), cell("2/19"), cell("1/39"), cell("6/93", { bold: true }), cell("5/93")],
      [cell("Casual vs formal questions", { align: "left" }), cell("—"), cell("—"), cell("8/10 · 64/83", { bold: true }), cell("8/10 · 68/83")],
      [cell("Files the fields correctly (F1)", { align: "left" }), cell("0.898"), cell("0.903"), cell("0.949", { bold: true }), cell("0.961")],
      [cell("Leaks on the 15 traps", { align: "left" }), cell("—"), cell("—"), cell("0", { bold: true }), cell("0")],
    ];
    s.addTable(rows, { x: M, y: 3.2, w: 11.6, colW: [4.6, 1.5, 1.6, 2.0, 1.9], rowH: 0.62,
      border: { type: "solid", pt: 0.75, color: THEME.colors.lt2 }, fill: { color: THEME.colors.lt1 }, margin: [0, 0.12, 0, 0.12], valign: "middle" });

    const px = M + 12.3, pw = 20 - M - px;
    card(s, "run3Panel", px, 3.2, pw, 5.6, THEME.colors.lt2);
    s.addText("RUN 3 · 19–20 OCTOBER", { isTextBox: true, x: px + 0.4, y: 3.5, w: pw - 0.8, h: 0.4, fontFace: "Jost", fontSize: 14,
      bold: true, charSpacing: 2, color: C.accent2, margin: 0 });
    const stat = (big, label, y, color) => {
      s.addText(big, { isTextBox: true, x: px + 0.4, y, w: pw - 0.8, h: 0.85, fontFace: "Jost", fontSize: 44, color: color || C.text1, margin: 0 });
      s.addText(label, { isTextBox: true, x: px + 0.4, y: y + 0.85, w: pw - 0.8, h: 0.45, fontSize: 15, color: C.text2, margin: 0 });
    };
    stat("25 of 118", "answers made a claim the documents do not support", 4.05, C.accent2);
    stat("72 of 93", "right, and citing the page it is printed on", 5.45);
    stat("0 of 15", "adversarial traps leaked", 6.85);
    s.addText("Each run had a different corpus, so the columns are measurements, not a trend.",
      { isTextBox: true, x: M, y: 7.75, w: 11.6, h: 0.45, fontSize: 14, italic: true, color: C.accent3, margin: 0 });
    card(s, "proposed", M, 8.35, 11.6, 1.2, THEME.colors.lt2);
    s.addText([T("PROPOSED · AWAITING SIGN-OFF", { fontFace: "Jost", fontSize: 13, bold: true, charSpacing: 2, color: C.accent2, breakLine: true }),
      T("The nine week-1 metrics, abstention among them, are still measured every run, as diagnostics beneath these five.", { color: C.text2 })],
      { isTextBox: true, x: M + 0.3, y: 8.4, w: 11.0, h: 1.1, fontSize: 16, margin: 0, valign: "middle" });

    s.addNotes(
      "We score PARROT on its promises, one number each, and every one is counted by code against the answer key, not by a judge model. " +
      "The first is the one that matters most: do not guess. An unsupported claim is a value the page doesn't print, a false 'not on file', or an answer to a question nothing on file can answer. Run 3 made 25 in 118 answers; since the fixes Run 3 found, 22. " +
      "72 of 93 answerable questions were right and cited, 76 since. It held back only six times when it had the page. And nothing leaked on the fifteen traps. " +
      "This headline is proposed and awaiting our supervisor's sign-off; the nine metrics we set in week one, abstention among them, are still measured underneath as diagnostics.");
  }

  // ---------------------------------------------------------------- 3. the finding (dark)
  {
    const s = pres.addSlide({ masterName: L.DARK, sectionTitle: S });
    s.addText("THE FINDING", { placeholder: "eyebrow" });
    s.addText([T("One answer in five still guesses. ", { color: C.background1 }), T("Half are questions with no answer on file.", { color: C.accent1 })],
      { isTextBox: true, x: M, y: 1.3, w: 9.8, h: 2.3, fontFace: "Jost", fontSize: 40, margin: 0, valign: "top" });
    const parts = [
      ["12", "answered, though nothing on file answers them"],
      ["8", "wrong values: a number the page does not print"],
      ["5", "false 'not on file' for something that is"],
    ];
    parts.forEach(([n, label], i) => {
      const y = 3.95 + i * 1.05;
      s.addText(n, { isTextBox: true, x: M, y, w: 1.3, h: 0.9, fontFace: "Jost", fontSize: 48, color: i === 0 ? C.accent1 : C.background1, margin: 0, valign: "middle" });
      s.addText(label, { isTextBox: true, x: M + 1.4, y, w: 8.2, h: 0.9, fontSize: 19, color: C.background2, margin: 0, valign: "middle" });
    });
    s.addText([T("The old headline saw only the first group. ", { color: C.background1 }),
      T("Abstention fell 0.76 → 0.52 → 0.52 as search improved: every document gives an unanswerable question a page that looks close. No threshold separates them (ADR 0019).", { color: C.background2 })],
      { isTextBox: true, x: M, y: 7.3, w: 9.6, h: 1.6, fontSize: 17, margin: 0, valign: "top" });

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
    pair("“The named driver is Marcus.”", "Name of Insured", 3.45);
    pair("“Road tax is due 12 April 2026.”", "Period of Insurance From", 5.3);
    s.addText("A score cannot see this; the printed label can. ADR 0021 checks it. It reaches only some cases, and is switched off pending review.",
      { isTextBox: true, x: qx + 0.45, y: 7.2, w: qw - 0.9, h: 1.1, fontSize: 15, color: C.text2, margin: 0, valign: "top" });

    s.addNotes(
      "This is the finding. Run 3's 25 unsupported claims are three kinds. Twelve are questions nothing on file can answer, answered anyway. Eight are wrong values. Five say something is not on file when it is. " +
      "Our old headline, abstention, only ever saw the first group, and it fell from 0.76 to 0.52 as search improved, because every new document gives an unanswerable question a page that looks close. A threshold on the re-reader's score could not separate those from good answers; we measured it and rejected it, and ADR 0019 records why. " +
      "What the twelve share is on the right: a real printed value under a different label. 'Name of Insured' read as the named driver; the start of the insurance period read as a road tax date. A score can't see that; the printed label can. ADR 0021 checks it: two fewer unsupported claims and no right answer lost, but it reaches only some cases, so it is switched off until the team reviews it.");
  }

  // ---------------------------------------------------------------- 4. checking the checker
  {
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
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
    const s = pres.addSlide({ masterName: L.ORANGE, sectionTitle: S });
    s.addText("WHERE IT STANDS", { isTextBox: true, x: M, y: 0.75, w: W, h: 0.45, fontFace: "Jost", fontSize: 16, bold: true, charSpacing: 2, color: C.text1, margin: 0 });
    s.addText("0 of 15", { isTextBox: true, x: M, y: 2.2, w: 9, h: 2.4, fontFace: "Jost", fontSize: 150, color: C.text1, margin: 0 });
    s.addText("adversarial traps leaked in Run 3. The one absolute line, kept.", { isTextBox: true, x: M, y: 4.75, w: 8.4, h: 1.2, fontFace: "Jost", fontSize: 26, color: C.text1, margin: 0, valign: "top" });
    s.addText("22 of 118", { isTextBox: true, x: 10.6, y: 2.2, w: 8.4, h: 2.4, fontFace: "Jost", fontSize: 130, color: C.background1, margin: 0 });
    s.addText("answers still make an unsupported claim, since the fixes Run 3 found. The work left is teaching it not to guess.", { isTextBox: true, x: 10.6, y: 4.75, w: 8.4, h: 1.6, fontFace: "Jost", fontSize: 26, color: C.background1, margin: 0, valign: "top" });
    s.addText("Next: the holdout, 14 real and redacted documents, tells us how much of this survives real paperwork.",
      { isTextBox: true, x: M, y: 7.6, w: W, h: 1.0, fontFace: "Jost", fontSize: 22, color: C.text1, margin: 0, valign: "top" });

    s.addNotes(
      "Where it stands. Nothing leaked on the fifteen traps: that is the one line we treat as absolute. " +
      "And since the fixes Run 3 found, 22 of 118 answers still make a claim the documents don't support, down from 25. The engine finds the page; what is left is teaching it not to guess from it. " +
      "Everything you've seen is on synthetic documents. The holdout, fourteen real, redacted documents, is the honest test of how much of it survives real paper.");
  }
};
