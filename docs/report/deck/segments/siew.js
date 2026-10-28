// Siew's segment: governance, the regulatory mapping, and the autonomy boundary.
// DRAFT by Yew Mun's session on 28 October for Siew to rewrite in their own words. Sources:
// docs/governance/*.md (status lines read 28 October), docs/governance/README.md, core/contracts.py,
// and a screenshot of the running app taken on 28 October.
const path = require("path");
const SHOTS = path.join(__dirname, "..", "..", "deck-shots");

module.exports = function siew({ pres, C, THEME, M, W, T, card, text, masters }) {
  const S = "Governance and assurance";
  pres.addSection({ title: S });
  const L = masters("Siew");
  const DRAFT = "DRAFT for Siew to rewrite in their own words. ";

  // ------------------------------------------------------------ 1. the paperwork
  {
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
    s.addText("GOVERNANCE AND ASSURANCE", { placeholder: "eyebrow" });
    s.addText([T("The paperwork "), T("is part of the product.", { color: C.accent2 })], { placeholder: "title" });
    const head = (t) => ({ text: t, options: { bold: true, fontFace: "Jost", fontSize: 14, color: C.accent3, charSpacing: 1 } });
    const cell = (t, o) => ({ text: t, options: Object.assign({ fontSize: 16, color: C.text1 }, o || {}) });
    const ok = (t) => cell(t, { bold: true, color: C.accent4 });
    const draft = (t) => cell(t, { color: C.accent3 });
    const rows = [
      [head("DOCUMENT"), head("WHAT IT ANSWERS"), head("STATUS · 28 OCT")],
      [cell("Consent and redaction"), cell("How real documents were collected for the holdout"), ok("Approved 19 Oct")],
      [cell("Incident and breach procedure"), cell("What happens, and by when, if data leaks"), ok("Approved 17 Oct")],
      [cell("Retention and erasure"), cell("How long documents are kept, and what deleting one removes"), draft("Ready for review")],
      [cell("Data inventory"), cell("What personal data PARROT holds, where, and whose"), draft("Draft for review")],
      [cell("Grounding sources basis"), cell("Which published guidance the packs may quote, and why"), draft("One source removed by rule")],
      [cell("Model card · ISO 22989 to 5338 · IMDA nine dimensions"), cell("How PARROT lines up with AI standards and Singapore's frameworks"), draft("Drafts")],
      [cell("Autonomy statement · Terms of use"), cell("What it may do on its own, and the basis for one adult filing for another"), draft("Drafts")],
    ];
    s.addTable(rows, { x: M, y: 3.1, w: W, colW: [6.2, 8.0, 3.8], rowH: 0.72,
      border: { type: "solid", pt: 0.75, color: THEME.colors.lt2 }, fill: { color: THEME.colors.lt1 }, margin: [0, 0.15, 0, 0.15], valign: "middle" });
    text(s, "A source left the tax corpus because its notice forbids storing it in a retrieval system: removed by a rule, not a judgement call.",
      { x: M, y: 9.15, w: W, h: 0.6, fontSize: 16, italic: true, color: C.accent3 });
    s.addNotes(DRAFT +
      "Governance here is a set of documents a buyer or a regulator would ask for, each tied to the code. Two are approved: the consent and redaction protocol that governed the real-document holdout, and the incident and breach procedure. " +
      "Retention and the data inventory are with Christian for technical review; the model card, the ISO and IMDA mappings, the autonomy statement and the terms of use are drafts. " +
      "One example of a rule doing its job: a tenth IRAS source was removed because its notice forbids storing it in a retrieval system. RE-CHECK every status on 3 Nov: PRs #117 and #118 may have landed.");
  }

  // ------------------------------------------------------------ 2. it never acts (dark)
  {
    const s = pres.addSlide({ masterName: L.DARK, sectionTitle: S });
    s.addText("THE LINE IT WON'T CROSS", { placeholder: "eyebrow" });
    s.addText([T("It advises. "), T("It never acts.", { color: C.accent1 })], { placeholder: "title" });
    card(s, "contract", M, 3.3, 10.2, 1.5, THEME.colors.dk2);
    text(s, [T("# core/contracts.py", { color: C.accent3, breakLine: true }), T("never_acts: ", { color: C.background1 }), T("Literal[True]", { color: C.accent1 })],
      { x: M + 0.4, y: 3.35, w: 9.6, h: 1.4, fontFace: "Courier New", fontSize: 24, valign: "middle" });
    text(s, "A pack that says otherwise will not load. The rule lives in the type system, not in the model's good behaviour.",
      { x: M, y: 5.15, w: 10.2, h: 1.2, fontFace: "Jost", fontSize: 24, color: C.background1, valign: "top" });
    text(s, "A request to pay, renew, book or file is refused at the top of the graph, before anything is retrieved. In Run 3 all three such traps were refused, within 15 of 15 held.",
      { x: M, y: 6.6, w: 10.2, h: 1.5, fontSize: 18, color: C.background2, valign: "top" });
    s.addImage({ path: path.join(SHOTS, "final-refusal-crop.jpg"), x: 12.0, y: 3.3, w: 7.0, h: 2.625 });
    text(s, "ASK, 28 OCTOBER", { x: 12.0, y: 6.05, w: 7.0, h: 0.4, fontFace: "Jost", fontSize: 13, bold: true, charSpacing: 2, color: C.accent3 });
    s.addNotes(DRAFT +
      "Version one advises. It does not pay, book or file, and that is not a promise about the model: every pack manifest must declare never_acts true, and the type system will not load one that says otherwise. " +
      "When someone asks it to renew and pay, it refuses at the top of the graph, before retrieval runs, so it never went looking first. All three such traps in Run 3 were refused.");
  }

  // ------------------------------------------------------------ 3. the frameworks
  {
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
    s.addText("MAPPED TO SINGAPORE'S RULES", { placeholder: "eyebrow" });
    s.addText([T("Each framework "), T("points at a file.", { color: C.accent2 })], { placeholder: "title" });
    const items = [
      ["PDPA", "Consent, retention, and breach notification under Part 6A", "consent-and-redaction · retention-and-erasure · incident-and-breach-procedure"],
      ["IMDA GenAI framework", "The nine dimensions, from accountability to content provenance", "imda-genai-nine-dimensions · model-card"],
      ["Agentic AI framework v1.5", "Bound the risks upfront; keep humans meaningfully accountable", "autonomy-statement"],
      ["ISO/IEC 22989 and 5338", "The AI lifecycle stages, mapped to the processes we ran", "iso-stage-process-map"],
      ["Copyright Act 2021, s 244", "What third-party guidance the packs index, and on what basis", "grounding-sources-basis"],
    ];
    items.forEach(([fw, what, files], i) => {
      const y = 3.15 + i * 1.3;
      card(s, "fw" + i, M, y, W, 1.12, i % 2 ? THEME.colors.lt1 : THEME.colors.lt2);
      text(s, fw, { x: M + 0.35, y, w: 5.2, h: 1.12, fontFace: "Jost", fontSize: 22, color: C.accent2, valign: "middle" });
      text(s, what, { x: M + 5.7, y, w: 6.9, h: 1.12, fontSize: 17, color: C.text1, valign: "middle" });
      text(s, files, { x: M + 12.8, y, w: 5.0, h: 1.12, fontFace: "Courier New", fontSize: 13, color: C.text2, valign: "middle" });
    });
    s.addNotes(DRAFT +
      "Every framework we cite points at a file in docs/governance: PDPA for consent, retention and breach notification; IMDA's generative AI framework and its nine dimensions; " +
      "the Model Governance Framework for Agentic AI, which asks us to bound the risks upfront and keep humans accountable; the ISO lifecycle mapping; and the Copyright Act for the guidance the packs quote.");
  }
};
