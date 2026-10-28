// The final deck's frame, shared by every segment: 20" x 11.25", cream / dark brown / orange,
// Jost titles, Arial body — the midterm deck's look. A segment file adds slides to a deck made here.
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

const M = 1.0; // side margin
const W = 20 - 2 * M;

function newDeck({ title, author }) {
  const pres = new pptxgen();
  pres.defineLayout({ name: "PARROT", width: 20, height: 11.25 });
  pres.layout = "PARROT";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.author = author;
  pres.title = title;
  const C = pres.SchemeColor;
  const defined = new Set();

  const footer = (presenter, color) => [
    { text: { text: "PARROT · IGD ILP 2026", options: { x: M, y: 10.45, w: 8, h: 0.35,
        fontFace: "Jost", fontSize: 13, charSpacing: 2, color, margin: 0 } } },
    { text: { text: presenter.toUpperCase(), options: { x: 20 - M - 4, y: 10.45, w: 3.4, h: 0.35, align: "right",
        fontFace: "Jost", fontSize: 13, charSpacing: 2, color, margin: 0 } } },
  ];
  const titled = (name, bg, ink, eyebrowColor, footColor, presenter) =>
    pres.defineSlideMaster({
      title: name,
      background: { color: bg },
      objects: [
        { placeholder: { options: { name: "eyebrow", type: "body", x: M, y: 0.75, w: W, h: 0.45,
            fontFace: "Jost", fontSize: 16, bold: true, charSpacing: 2, color: eyebrowColor, margin: 0, valign: "top" }, text: "" } },
        { placeholder: { options: { name: "title", type: "title", x: M, y: 1.3, w: W, h: 1.5,
            fontFace: "Jost", fontSize: 48, color: ink, margin: 0, valign: "top", align: "left" }, text: "" } },
        ...footer(presenter, footColor),
      ],
      slideNumber: { x: 20 - M - 0.55, y: 10.45, w: 0.55, h: 0.35, fontFace: "Jost", fontSize: 13, color: footColor, align: "right" },
    });

  // Three layouts per presenter, so the footer names whoever is speaking: LIGHT, DARK and ORANGE.
  const masters = (presenter) => {
    const key = presenter.toUpperCase().replace(/[^A-Z]/g, "");
    const names = { LIGHT: "LIGHT " + key, DARK: "DARK " + key, ORANGE: "ORANGE " + key };
    if (!defined.has(key)) {
      defined.add(key);
      titled(names.LIGHT, THEME.colors.lt1, C.text1, C.accent2, C.accent3, presenter);
      titled(names.DARK, THEME.colors.dk1, C.background1, C.accent1, C.accent3, presenter);
      pres.defineSlideMaster({ title: names.ORANGE, background: { color: THEME.colors.accent1 },
        objects: footer(presenter, C.text1) });
    }
    return names;
  };

  const T = (text, opts) => ({ text, options: opts || {} });
  const card = (slide, name, x, y, w, h, fill) =>
    slide.addShape(pres.shapes.RECTANGLE, { objectName: name, x, y, w, h, fill: { color: fill }, line: { type: "none" } });
  const text = (slide, value, opts) => slide.addText(value, Object.assign({ isTextBox: true, margin: 0 }, opts));

  const finish = async (out) => {
    await pres.writeFile({ fileName: out });
    await applyTheme(out, THEME);
    console.log("wrote", out);
  };

  return { pres, C, THEME, M, W, T, card, text, masters, finish };
}

module.exports = { newDeck, THEME, M, W };
