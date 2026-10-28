// The close, after the five segments. DRAFT by Yew Mun's session on 28 October for Christian,
// who opens and closes, to rewrite in their own words. Sources: docs/demo-run-sheet.md step 9,
// docs/report/05-evaluation-and-results.md section 5.10.
module.exports = function close({ pres, C, THEME, M, W, T, card, text, masters }) {
  const S = "Close";
  pres.addSection({ title: S });
  const L = masters("Christian");

  const s = pres.addSlide({ masterName: L.DARK, sectionTitle: S });
  s.addText("WHAT YOU DID NOT SEE", { placeholder: "eyebrow" });
  text(s, [T("It never paid. It never booked. "), T("And it told us no.", { color: C.accent1 })],
    { x: M, y: 1.4, w: W, h: 2.6, fontFace: "Jost", fontSize: 58, color: C.background1, valign: "top" });
  text(s, "Everything you saw ran on one laptop. No document, no question and no answer went to a cloud service.",
    { x: M, y: 3.3, w: 15, h: 1.0, fontSize: 22, color: C.background2, valign: "top" });
  const next = [
    ["The holdout", "14 real, redacted documents: how much of this survives real paper"],
    ["Do not guess", "22 of 118 answers still make an unsupported claim; the label check (ADR 0021) awaits a decision"],
    ["The headline", "Five numbers scored by code, proposed and awaiting the supervisor's sign-off"],
  ];
  text(s, "WHAT COMES NEXT", { x: M, y: 5.9, w: W, h: 0.45, fontFace: "Jost", fontSize: 15, bold: true, charSpacing: 2, color: C.accent1 });
  next.forEach(([head, body], i) => {
    const x = M + i * 6.125;
    card(s, "next" + i, x, 6.5, 5.75, 2.4, THEME.colors.dk2);
    text(s, head, { x: x + 0.35, y: 6.75, w: 5.05, h: 0.55, fontFace: "Jost", fontSize: 22, color: C.background1 });
    text(s, body, { x: x + 0.35, y: 7.4, w: 5.05, h: 1.4, fontSize: 16, color: C.background2, valign: "top" });
  });
  text(s, "Thank you. Questions.", { x: M, y: 9.3, w: W, h: 0.7, fontFace: "Jost", fontSize: 28, color: C.accent1 });
  s.addNotes("DRAFT for Christian to rewrite in their own words. " +
    "Everything you just saw ran on this laptop. It never paid anything, never booked anything, and it told us no. " +
    "What comes next is honest work: the holdout on real documents, teaching it not to guess, and the supervisor's sign-off on how we score it. Thank you. We'd welcome your questions.");
};
