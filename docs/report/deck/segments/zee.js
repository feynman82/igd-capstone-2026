// Zee's segment: the interface and the two domain packs, and the product line they make.
// DRAFT by Yew Mun's session on 28 October for Zee to rewrite in their own words. Sources:
// docs/report/04-packs-and-interface.md (draft of 17 October), docs/report/07-commercialisation-
// roadmap.md, docs/adr/0017, and screenshots of the running app taken on 28 October.
const path = require("path");
const SHOTS = path.join(__dirname, "..", "..", "deck-shots");

module.exports = function zee({ pres, C, THEME, M, W, T, card, text, masters }) {
  const S = "Interface and packs";
  pres.addSection({ title: S });
  const L = masters("Zee");
  const DRAFT = "DRAFT for Zee to rewrite in their own words. ";

  // ------------------------------------------------------------ 1. four screens
  {
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
    s.addText("THE INTERFACE", { placeholder: "eyebrow" });
    s.addText([T("Four screens. "), T("It speaks first.", { color: C.accent2 })], { placeholder: "title" });
    const screens = [
      ["Today", "What needs you now, in order of urgency. An empty Today is the system working."],
      ["Ask", "Every sentence carries its own page. A sentence with no source is never shown."],
      ["Vault", "Every field it read, with its page. And what it could not read, with the reason."],
      ["Packs", "Switch a subject off: its voice goes quiet. Your documents stay."],
    ];
    screens.forEach(([head, body], i) => {
      const y = 3.2 + i * 1.65;
      text(s, head, { x: M, y, w: 2.4, h: 0.6, fontFace: "Jost", fontSize: 26, color: C.accent2 });
      text(s, body, { x: M + 2.5, y: y + 0.05, w: 6.6, h: 1.3, fontSize: 18, color: C.text2, valign: "top" });
    });
    s.addImage({ path: path.join(SHOTS, "final-vault.jpg"), x: 10.4, y: 2.0, w: 4.15, h: 5.82 });
    s.addImage({ path: path.join(SHOTS, "final-packs.jpg"), x: 14.85, y: 2.0, w: 4.15, h: 5.82 });
    text(s, "VAULT · ONE DOCUMENT", { x: 10.4, y: 7.95, w: 4.15, h: 0.4, fontFace: "Jost", fontSize: 13, bold: true, charSpacing: 2, color: C.accent3 });
    text(s, "PACKS", { x: 14.85, y: 7.95, w: 4.15, h: 0.4, fontFace: "Jost", fontSize: 13, bold: true, charSpacing: 2, color: C.accent3 });
    s.addNotes(DRAFT +
      "Four screens. Today opens first, because a busy household does not know what to ask; it lists what needs you, and most days it should be nearly empty. " +
      "Ask answers with a source on every sentence. Vault shows every field PARROT read off a document, with the page, and what it could not read. " +
      "Packs is where a subject is switched on or off: its specialist voice goes, and the documents stay.");
  }

  // ------------------------------------------------------------ 2. a pack is a file
  {
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
    s.addText("SUBJECT PACKS", { placeholder: "eyebrow" });
    s.addText([T("A second subject cost a file, "), T("not a release.", { color: C.accent2 })], { placeholder: "title" });
    const claims = [
      ["01", "A pack is data, checked against a contract before it can load."],
      ["02", "The household's documents belong to the core, not to any pack (ADR 0017)."],
      ["03", "Every pack declares never_acts: true. One that does not will not load."],
    ];
    claims.forEach(([n, body], i) => {
      const y = 3.2 + i * 1.5;
      text(s, n, { x: M, y, w: 0.9, h: 0.6, fontFace: "Jost", fontSize: 24, color: C.accent2 });
      text(s, body, { x: M + 1.0, y, w: 7.4, h: 1.3, fontFace: "Jost", fontSize: 22, color: C.text1, valign: "top" });
    });
    const head = (t, al) => ({ text: t, options: { bold: true, fontFace: "Jost", fontSize: 14, color: C.accent3, charSpacing: 1, align: al || "left" } });
    const cell = (t, o) => ({ text: t, options: Object.assign({ fontSize: 15, color: C.text1, valign: "top" }, o || {}) });
    const rows = [
      [head(""), head("INSURANCE AND COVERAGE · v0.6"), head("TAX AND RELIEFS · v0.4")],
      [cell("Speaks for", { color: C.text2 }), cell("5 document types: schedule, renewal, claim, illustration, statement"), cell("7: payslip, donation, CPF, SRS, Notice of Assessment, top-up, course fee")],
      [cell("Grounding", { color: C.text2 }), cell("20 MoneySense, MOH, CPF Board and LIA sources"), cell("9 IRAS sources for YA2025–2027, reviewed 18 Oct")],
      [cell("Advice", { color: C.text2 }), cell("Death, disability and critical-illness gaps; a coverage review"), cell("SRS room left and estimated tax saving; a tax review")],
    ];
    s.addTable(rows, { x: 9.2, y: 3.2, w: 9.8, colW: [1.8, 4.0, 4.0], rowH: [0.55, 1.15, 1.15, 1.15],
      border: { type: "solid", pt: 0.75, color: THEME.colors.lt2 }, fill: { color: THEME.colors.lt1 }, margin: [0.08, 0.12, 0.08, 0.12] });
    text(s, "The tax pack added no calculator and no core code.", { x: 9.2, y: 7.7, w: 9.8, h: 0.6, fontFace: "Jost", fontSize: 22, color: C.accent2 });
    s.addNotes(DRAFT +
      "Adding tax to an insurance assistant cost a file, not a release, and three things make that true. A pack is data, checked against a contract before it loads. " +
      "The documents belong to the core, so switching a pack off never hides the household's paper. And every pack declares that it never acts; the type system will not load one that says otherwise. " +
      "The tax pack added no calculator and no core code. RE-CHECK after the 28 October freeze: whether the tax corpus is indexed and its two rule values approved (chapter 4 draft status).");
  }

  // ------------------------------------------------------------ 3. the product line (dark)
  {
    const s = pres.addSlide({ masterName: L.DARK, sectionTitle: S });
    s.addText("THE PRODUCT LINE", { placeholder: "eyebrow" });
    s.addText([T("Packs are "), T("the unit of sale.", { color: C.accent1 })], { placeholder: "title" });
    const stages = [
      ["NOW", "Prototype", "Core, Insurance and Tax, Reminder and Alert", "Real redacted documents measured"],
      ["NEXT", "Household product", "Catalogue packs, bought one at a time", "A measured minimum hardware spec"],
      ["THEN", "Professional seat", "An agent reviews a client's cover, with consent", "A position on the Financial Advisers Act"],
      ["LATER", "Pack marketplace", "Packs written by domain experts", "Provenance review beyond one reviewer"],
    ];
    const cw = 4.3, gap = 0.27, y0 = 3.2, ch = 4.6;
    stages.forEach(([when, head, ships, first], i) => {
      const x = M + i * (cw + gap);
      card(s, "stage" + i, x, y0, cw, ch, THEME.colors.dk2);
      text(s, when, { x: x + 0.35, y: y0 + 0.35, w: cw - 0.7, h: 0.45, fontFace: "Jost", fontSize: 15, bold: true, charSpacing: 2, color: C.accent1 });
      text(s, head, { x: x + 0.35, y: y0 + 0.9, w: cw - 0.7, h: 0.6, fontFace: "Jost", fontSize: 24, color: C.background1 });
      text(s, ships, { x: x + 0.35, y: y0 + 1.65, w: cw - 0.7, h: 1.2, fontSize: 16, color: C.background2, valign: "top" });
      text(s, [T("FIRST  ", { fontFace: "Jost", bold: true, fontSize: 12, charSpacing: 2, color: C.accent1, breakLine: true }), T(first, { color: C.background1 })],
        { x: x + 0.35, y: y0 + 3.0, w: cw - 0.7, h: 1.4, fontSize: 15, valign: "top" });
    });
    text(s, [T("ASSUMED  ", { bold: true, color: C.accent1 }), T("All three revenue routes are untested. We claim no price and no market size.", { color: C.background2 })],
      { x: M, y: 8.2, w: W, h: 0.55, fontSize: 18 });
    text(s, "Two constraints we can defend: on-device models need a capable laptop (the only one tested has 32 GB and an RTX 4060), and WhatsApp now charges per message, so capture runs through a folder and Telegram.",
      { x: M, y: 8.85, w: W, h: 1.0, fontSize: 16, color: C.background2, valign: "top" });
    s.addNotes(DRAFT +
      "Packs are the unit of sale because the contract already makes them one. Today: the prototype. Next: a household product, packs bought one at a time, once we have a measured minimum hardware spec. " +
      "Then a professional seat, an insurance agent reviewing a client's cover with consent, which needs a position on the Financial Advisers Act. Later, a marketplace of expert-written packs. " +
      "All three revenue routes are assumptions; we claim no price and no market size.");
  }
};
