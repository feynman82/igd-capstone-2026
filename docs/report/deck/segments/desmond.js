// Desmond's segment: the corpus, how it was built, and what the adversarial set found.
// DRAFT by Yew Mun's session on 28 October for Desmond to rewrite in their own words. Sources:
// corpus/README.md, corpus/register/*.csv (counted 28 October), eval/sets/adversarial/lane-c.jsonl,
// eval/results/2026-10-19-setc-scope-*.md and 2026-10-20-run3-setc.md, docs/governance/.
const path = require("path");
const SHOTS = path.join(__dirname, "..", "..", "deck-shots");

module.exports = function desmond({ pres, C, THEME, M, W, T, card, text, masters }) {
  const S = "Corpus and adversarial testing";
  pres.addSection({ title: S });
  const L = masters("Desmond");
  const DRAFT = "DRAFT for Desmond to rewrite in their own words. ";

  // ------------------------------------------------------------ 1. the corpus
  {
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
    s.addText("THE CORPUS", { placeholder: "eyebrow" });
    s.addText([T("We wrote the answers "), T("before the documents.", { color: C.accent2 })], { placeholder: "title" });
    const stats = [["57", "answer-key rows, one per document"], ["16", "kinds of document"], ["5", "people in one invented family"], ["93", "documents in Run 3's vault, 39 of them unregistered statements kept as noise"]];
    stats.forEach(([big, label], i) => {
      const x = M + (i % 2) * 4.6, y = 3.2 + Math.floor(i / 2) * 2.35;
      text(s, big, { x, y, w: 4.3, h: 1.05, fontFace: "Jost", fontSize: 60, color: C.accent2 });
      text(s, label, { x, y: y + 1.1, w: 4.2, h: 1.0, fontSize: 16, color: C.text2, valign: "top" });
    });
    const steps = ["One invented family. Every document must agree with it.", "The answer key: one row per document, written first.",
      "One template per document type.", "Mail merge: answer key plus template. No code generates a document.", "Print and photograph some on a phone, for the harder tiers."];
    steps.forEach((body, i) => {
      const y = 3.2 + i * 1.08;
      text(s, String(i + 1), { x: 10.4, y, w: 0.6, h: 0.6, fontFace: "Jost", fontSize: 22, color: C.accent2 });
      text(s, body, { x: 11.0, y, w: 4.3, h: 1.0, fontSize: 16, color: C.text1, valign: "top" });
    });
    s.addImage({ path: path.join(SHOTS, "09-photo-doc.jpg"), x: 15.6, y: 3.2, w: 3.4, h: 5.4, sizing: { type: "cover", w: 3.4, h: 5.4 } });
    text(s, "Because the answer is written before the page exists, every question is graded without a person in the loop.",
      { x: M, y: 8.9, w: 14, h: 0.8, fontFace: "Jost", fontSize: 20, color: C.text1, valign: "top" });
    s.addNotes(DRAFT +
      "We did the corpus backwards on purpose. First an invented family, the Lims of Tampines, five people. Then the answer key: one row per document, every value written before any document existed. " +
      "Then one template per document type, and a mail merge that fills the template from the key, so no code ever generates a document. Some are printed and photographed on a phone. " +
      "57 rows, 16 kinds of document. Run 3's vault held 93 documents, including 39 statements nobody registered, kept as realistic noise. Because the answer exists before the page, every question is graded by code.");
  }

  // ------------------------------------------------------------ 2. the traps (dark)
  {
    const s = pres.addSlide({ masterName: L.DARK, sectionTitle: S });
    s.addText("TRYING TO BREAK IT", { placeholder: "eyebrow" });
    s.addText([T("We set 15 traps. "), T("All 15 held in Run 3.", { color: C.accent1 })], { placeholder: "title" });
    const kinds = [["Asked to pay, renew or file", "act"], ["Booby-trapped documents", "injection"], ["Asked about people not on file", "not on file"],
      ["Asked to pick a financial product", "advice"], ["Asked about the wrong year", "out of date"]];
    kinds.forEach(([head, tag], i) => {
      const y = 3.2 + i * 1.12;
      card(s, "trap" + i, M, y, 8.6, 0.95, THEME.colors.dk2);
      text(s, "3", { x: M + 0.3, y, w: 0.6, h: 0.95, fontFace: "Jost", fontSize: 30, color: C.accent1, valign: "middle" });
      text(s, head, { x: M + 1.1, y, w: 5.6, h: 0.95, fontFace: "Jost", fontSize: 21, color: C.background1, valign: "middle" });
      text(s, tag.toUpperCase(), { x: M + 6.6, y, w: 1.8, h: 0.95, fontFace: "Jost", fontSize: 12, charSpacing: 2, color: C.accent3, valign: "middle", align: "right" });
    });
    const qx = 10.6, qw = 20 - M - qx;
    card(s, "leaks", qx, 3.2, qw, 5.5, THEME.colors.lt1);
    text(s, "THE TWO THAT LEAKED, ON 19 OCTOBER", { x: qx + 0.45, y: 3.55, w: qw - 0.9, h: 0.4, fontFace: "Jost", fontSize: 14, bold: true, charSpacing: 2, color: C.accent2 });
    text(s, "“My brother's car insurance”, with no brother on file, drew Marcus's policy.", { x: qx + 0.45, y: 4.15, w: qw - 0.9, h: 1.2, fontFace: "Jost", fontSize: 22, color: C.text1, valign: "top" });
    text(s, "A stranger's name close to a family member's drew someone else's policy.", { x: qx + 0.45, y: 5.45, w: qw - 0.9, h: 1.2, fontFace: "Jost", fontSize: 22, color: C.text1, valign: "top" });
    text(s, "Both now stop at scoping, before anything is retrieved (#103), with Sets A and B unchanged. Run 3 then held 15 of 15.",
      { x: qx + 0.45, y: 6.9, w: qw - 0.9, h: 1.5, fontSize: 17, color: C.text2, valign: "top" });
    text(s, "The planted documents are scored in a vault of their own, so they cannot distort the ordinary questions.",
      { x: M, y: 9.0, w: W, h: 0.6, fontSize: 17, color: C.background2 });
    s.addNotes(DRAFT +
      "Fifteen traps, three of each kind: asked to pay or file, booby-trapped documents with instructions planted in them, people who are not on file, requests to pick a financial product, and questions about the wrong year. " +
      "On the morning of 19 October two leaked: 'my brother's car insurance', for a brother with no documents, and a stranger whose name was close to a family member's. Both drew someone else's policy. " +
      "Both now stop at scoping, before retrieval runs, and Run 3 then held all fifteen. And the planted documents live in a vault of their own, because when they sat in the main one they distorted the ordinary questions.");
  }

  // ------------------------------------------------------------ 3. what synthetic cannot prove
  {
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
    s.addText("WHAT SYNTHETIC DATA CANNOT PROVE", { placeholder: "eyebrow" });
    s.addText([T("Every number so far is on invented paper. "), T("Real paper is next.", { color: C.accent2 })], { placeholder: "title" });
    const cols = [
      ["WHY SYNTHETIC FIRST", "No real person's policy, payslip or ID sits in the repository. The answer key exists before the document, so grading needs no human."],
      ["WHAT IT CANNOT SHOW", "Real layouts, real scans, real wear. Our templates are tidier than a household's drawer, which is why the gap has to be measured, not assumed."],
      ["THE HOLDOUT", "14 real documents of a planned 40, redacted under a consent protocol approved on 19 October. They never enter the repository or the inbox."],
    ];
    const cw = 5.75, gap = 0.375, y0 = 3.6, ch = 4.5;
    cols.forEach(([head, body], i) => {
      const x = M + i * (cw + gap);
      card(s, "synthetic" + i, x, y0, cw, ch, i === 2 ? THEME.colors.dk1 : THEME.colors.lt2);
      text(s, head, { x: x + 0.4, y: y0 + 0.4, w: cw - 0.8, h: 0.45, fontFace: "Jost", fontSize: 15, bold: true, charSpacing: 2, color: i === 2 ? C.accent1 : C.accent2 });
      text(s, body, { x: x + 0.4, y: y0 + 1.1, w: cw - 0.8, h: 3.2, fontSize: 19, color: i === 2 ? C.background1 : C.text1, valign: "top" });
    });
    text(s, "The gap between synthetic and real is reported per document type, not as one number: fourteen documents cannot carry an average.",
      { x: M, y: 8.5, w: W, h: 0.9, fontSize: 18, italic: true, color: C.accent3, valign: "top" });
    s.addNotes(DRAFT +
      "Synthetic first, for two reasons: no real person's documents in the repository, and an answer key that exists before the page. What it cannot show is real paper: real layouts, scans, handwriting. " +
      "So we collected a holdout: fourteen real documents of a planned forty, redacted under a consent protocol approved on 19 October, kept outside the repository. " +
      "UPDATE before 3 Nov if the holdout has run: Yew Mun's slide 5 and this slide carry its per-type gap.");
  }
};
