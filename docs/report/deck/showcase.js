// The 15-slide showcase deck: the whole capstone in one sitting.
//
//   SKILL=<path to the pptx skill> node showcase.js "../Project Parrot Showcase.pptx"
//
// Presented in person by Siew Siew (slides 1-7 and 13-15) and Desmond (8-12); the speaker
// notes say who speaks. The palette is the scarlet macaw's, darkened where white text sits on it
// so every word clears contrast: scarlet, sunflower, macaw blue, jungle green and violet on night
// indigo. Type is large and runs edge to edge. Every number names the file it comes from.
"use strict";
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const JSZip = require("jszip");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const Fi = require("react-icons/fi");
const { applyTheme } = require(path.join(process.env.SKILL, "scripts/apply_theme.js"));

const OUT = process.argv[2] || "../Project Parrot Showcase.pptx";
const SHOTS = path.join(__dirname, "../deck-shots");
const ASSETS = path.join(__dirname, "../../../assets");

const THEME = {
  name: "Parrot Macaw",
  headFontFace: "Arial",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "12102B", // night indigo
    lt1: "FFFFFF",
    dk2: "3B3658", // body text on white
    lt2: "F3F1FA",
    accent1: "D7263D", // scarlet
    accent2: "FFC233", // sunflower (dark text on it)
    accent3: "1565D8", // macaw blue
    accent4: "0B8A62", // jungle green
    accent5: "6C2BD9", // violet
    accent6: "262250", // dark card
    hlink: "1565D8",
    folHlink: "D7263D",
  },
};
const HEX = THEME.colors;
const TRACK = "E7E5F0"; // the empty part of a ring
const MIST = "C9C4E6"; // secondary text on indigo

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "PARROT: your family's paperwork, answered";
pres.author = "IGD ILP 2026, Group 1";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const TEAM = ["Christian", "Fauziah", "Desmond", "Siew Siew", "Yew Mun"];

// Speaker script, one per slide in order: about a minute and a half each. Every [CLICK] brings in
// the next element, in the order addAnimations() builds; the count on each slide matches it.
const NOTES = [
  // 1 · 1 click
  "SIEW SIEW  ·  1 click\n\nGood morning. A question almost nobody in this room can answer quickly: where, exactly, is your car insurance policy right now? Not roughly. Exactly. An email, a drawer, a photo somewhere on a phone.\n\nWe are Group 1, and this is PARROT. You photograph a document once, it files itself, and when you ask it something it answers with the page the answer came from. And the part we care about most: when it does not know, it says so. It runs on the family's own laptop, so nothing leaves the house.\n\n[CLICK] PARROT was built by five of us: Christian, Fauziah, Desmond, Yew Mun and me, Siew Siew. Desmond and I will take you through the problem, the product, the evidence that it works, and what still has to be true before anyone pays for it.",
  // 2 · 4 clicks
  "SIEW SIEW  ·  4 clicks\n\nLet me introduce three people from our proposal.\n\n[CLICK] Sarah is a working mother, which makes her the household calendar: renewals and due dates spread over six inboxes and a drawer.\n\n[CLICK] Marcus is the sandwich generation. Between himself, his wife, his son and his two parents he tracks eleven policies, and the one question that matters, are we covered, costs him an evening.\n\n[CLICK] Priya saves tax through SRS, once a year, in a narrow window. Miss it and nothing happens: no letter, no alarm. The relief just disappears.\n\n[CLICK] What they share: none of them is missing documents. They are missing a way to ask the pile a question and trust the answer. And a chatbot that confidently invents a policy date is worse than none, because now you have stopped checking.",
  // 3 · 5 clicks
  "SIEW SIEW  ·  5 clicks\n\nHere is the whole product in three moves.\n\n[CLICK] One, capture. You photograph a document and send it to a Telegram chat, or drop it in a folder. That is all the filing you ever do. Docling reads the page and the model extracts typed fields: dates, amounts, policy numbers.\n\n[CLICK] Two, ask. Plain English. Every sentence in the answer carries its own source, the document and the page.\n\n[CLICK] Three, Today. You do not even have to ask. It opens on what needs you now.\n\n[CLICK] And the line to remember: when the documents do not say, PARROT says so. It does not guess.\n\n[CLICK] These are real screens from the running app: on the left, a phone filing photos through Telegram; on the right, an answer with its citation, b1-0001.pdf, page 1. One click opens the original.",
  // 4 · 4 clicks
  "SIEW SIEW  ·  4 clicks\n\nFour screens, and the design principle is that it speaks first.\n\n[CLICK] Today is the home screen: a policy that has expired, something due, and the documents it could not read and wants you to check.\n\n[CLICK] Ask is the conversation, where every answer shows its page.\n\n[CLICK] Vault is honesty about extraction: what it read off each document, with a confidence, and what it could not, in plain words rather than hidden.\n\n[CLICK] Packs is where a family chooses what PARROT knows about. Switch the insurance pack off and its advice goes quiet; the documents stay searchable.\n\nThe interface is Next.js 15 behind a local passphrase, and it never talks to anything outside the laptop.",
  // 5 · 4 clicks
  "SIEW SIEW  ·  4 clicks\n\nLet us zoom into one real answer: when does the car insurance renew?\n\n[CLICK] Number one: every sentence ends in a citation chip, a document and a page. Behind that is a hard rule in the database: a fact row cannot be written without its document and page; both columns are NOT NULL.\n\n[CLICK] Number two: the footer says nothing left this computer. Generation, embedding, reranking, even the model that grades us, all run locally.\n\n[CLICK] Number three: it knows what it is not. It is not a licensed financial adviser, and it says so.\n\n[CLICK] Number four, and the title of this slide: the date 11 April 2027 is read from a typed column in Postgres. The model writes the sentence around the number. It never produces the number itself.",
  // 6 · 5 clicks
  "SIEW SIEW  ·  5 clicks\n\nUnderneath, five layers, one laptop and one database. Let me build it up.\n\n[CLICK] At the top, a launcher starts everything, the Next.js screens are what the family sees, and the FastAPI engine serves them.\n\n[CLICK] Capture: the folder watcher and the Telegram bot hand documents to a Celery worker, Docling parses them, and a page it is not confident about goes to quarantine, where the vision model reads the image itself.\n\n[CLICK] Answering: a LangGraph graph scopes the question to the right person, runs hybrid search fused with reciprocal rank fusion, reranks with a cross-encoder, and an evidence gate decides whether the answer is supported at all.\n\n[CLICK] Runtime: every model is open and local. SEA-LION 4B vision-language from AI Singapore generates, EmbeddingGemma embeds, all in one PostgreSQL with pgvector.\n\n[CLICK] And knowledge: the contracts, the domain packs, the modules and the grounding corpus. Tested on a 32 GB laptop with an RTX 4060.",
  // 7 · 4 clicks
  "SIEW SIEW  ·  4 clicks\n\nWhy call it a platform and not an app? Because we built the hard part once.\n\n[CLICK] The engine in the middle files, finds, checks and cites.\n\n[CLICK] From one side plug in capability modules: Reminder, Alert and Advice. They read the typed facts the engine has filed, and none of them touches the screen.\n\n[CLICK] From the other side plug in domain packs: Tax and Reliefs, and Insurance. A pack is one YAML file, so a new domain means writing, not rebuilding.\n\n[CLICK] Two packs built, nine more specified and checked by a test, three modules running, and zero packs that can act: never_acts is typed Literal True, so a pack that tries to pay, book or file will not even load.\n\nDesmond will now show you one pack at work, and how we proved any of this.",
  // 8 · 4 clicks
  "DESMOND  ·  4 clicks\n\nThank you, Siew Siew. A file of know-how sounds abstract, so here is one at work.\n\n[CLICK] Marcus types one sentence: review my insurance coverage and tell me what is lacking.\n\n[CLICK] The insurance pack reads his income off his payslip and his cover off his policies, and applies the MoneySense rule of thumb: life cover around nine times annual income. He earns 112,800 a year, so the target is just over a million. He holds 300,000. He is short about 715,000.\n\n[CLICK] Critical illness, around four times income: he is short about 251,000.\n\n[CLICK] Plain code does the sums, not the model, and every input on that card links to its page. It names the gap and the kind of plan that closes it, never a product, and Marcus's consent to advice is recorded.",
  // 9 · 5 clicks
  "DESMOND  ·  5 clicks\n\nYou cannot test an assistant like this on real families' payslips, so we built one family, and wrote their whole life down before a single document existed. That ID card is one of our synthetic specimens.\n\n[CLICK] The Lim household in Tampines: Marcus, his wife Rachel, their son Lucas, and Marcus's parents Ah Kow and Mei Ling. Three surnames, one household, which is exactly what makes parent relief and elderly hospital cover interesting.\n\n[CLICK] Run 3's vault holds 93 documents, 39 of them unregistered statements kept as realistic noise.\n\n[CLICK] Across 16 document types, from payslips to policy schedules.\n\n[CLICK] Against it, 118 golden questions: 93 answerable and 25 whose answer is deliberately absent. Every one is graded by code against the register, not by opinion.\n\n[CLICK] And 15 adversarial traps: prompt injection, requests to act, stale and absent records.",
  // 10 · 5 clicks
  "DESMOND  ·  5 clicks\n\nThis is the slide that changed how we evaluate. A confident, well-cited, wrong answer about an insurance policy is worse than no answer. So the first number we report is the unsupported claim. In Run 3 there were 25 in 118 answers; that is the coloured part of the ring.\n\n[CLICK] Twelve were unanswerable questions answered anyway, from a page that was relevant but silent on the point.\n\n[CLICK] Eight were wrong values.\n\n[CLICK] Five were a false 'not on file' when it was on file.\n\n[CLICK] And zero forbidden strings leaked on the adversarial set.\n\n[CLICK] That is why we lead with this number. And with the fixes Run 3 found, the count fell from 25 to 21.",
  // 11 · 6 clicks
  "DESMOND  ·  6 clicks\n\nSo the report leads with five numbers, one per aim, each scored by code against the register. Each ring shows how full it is.\n\n[CLICK] Right and cited: 77 of 93.\n\n[CLICK] Unsupported claims: 21 of 118. This is the one ring we want empty.\n\n[CLICK] Over-caution, meaning it held back although it had read the answering page: 4 of 93.\n\n[CLICK] Extraction F1: 0.961.\n\n[CLICK] And the absolute line: all 15 adversarial traps contained.\n\n[CLICK] Measured on main on 28 October, on the same 93-document vault as Run 3, and every headline moved the right way since. One honest caveat: this five-number headline is proposed and awaiting our supervisor's sign-off.",
  // 12 · 4 clicks
  "DESMOND  ·  4 clicks\n\nThe biggest single lesson came from retrieval. The chart shows recall, precision and faithfulness across our runs.\n\n[CLICK] The headline: faithfulness jumped from 0.81 to 0.97, the largest movement in the project, once hybrid search and a cross-encoder put the answering page reliably in the window. The model stopped borrowing from a neighbouring document.\n\n[CLICK] Why it was needed: grow the corpus from 6 documents to 26, with no code change, and precision fell by 0.10. A score on a small corpus does not predict one on a realistic corpus.\n\n[CLICK] Dense search cannot reliably find a policy by its printed number, so full-text search joined it.\n\n[CLICK] And by Run 3, 19 of the 21 misses had the right page in hand: retrieval is no longer where answers are lost.\n\nBack to Siew Siew on what keeps it safe.",
  // 13 · 6 clicks
  "SIEW SIEW  ·  6 clicks\n\nThank you, Desmond. PARROT advises. It never pays, books or files.\n\n[CLICK] Ask it to renew a policy and pay the premium, and it explains what the documents say and declines to act.\n\n[CLICK] That is enforced in the code, not left to the model's judgement: never_acts is typed Literal True in every pack.\n\nAround that sits a full governance set.\n\n[CLICK] For PDPA: a data inventory, a consent and redaction protocol, retention and erasure, and a breach procedure.\n\n[CLICK] An ISO/IEC 22989 to 5338 map that ties every lifecycle stage to a file in the repository.\n\n[CLICK] A mapping to IMDA's nine generative-AI governance dimensions, with an autonomy statement.\n\n[CLICK] And a model card and terms of use that say plainly what it is for, where it fails, and who it is not for.",
  // 14 · 5 clicks
  "SIEW SIEW  ·  5 clicks\n\nCommercially, PARROT is sold the way it is built: packs are the unit of sale. The core is common; the domain packs are what a family buys.\n\n[CLICK] Now: the prototype, two packs and two modules.\n\n[CLICK] Next: a household product with catalogue packs bought one at a time, once we have a measured minimum hardware spec.\n\n[CLICK] Then: a professional seat, where an insurance agent reviews a client's cover with consent. That first needs a position on the Financial Advisers Act.\n\n[CLICK] Later: a marketplace of packs written by domain experts.\n\n[CLICK] We claim no price or market size. Willingness to pay is a hypothesis, ordered by how countable the loss is: a missed SRS relief, a lapsed motor policy.",
  // 15 · 4 clicks
  "SIEW SIEW  ·  4 clicks  ·  Desmond joins for questions\n\nThree things come next.\n\n[CLICK] First, prove it on real paper: close the synthetic-to-real gap with the holdout set, 14 of a planned 40 real redacted documents so far.\n\n[CLICK] Second, turn on the label check from ADR 0021, which checks each stated value against the printed label beside it: two fewer unsupported claims, and no right answer lost.\n\n[CLICK] Third, measure the minimum machine: fit the full workflow on an 8 GB GPU and publish the spec.\n\n[CLICK] If you remember one line, make it this one: when the documents don't say, PARROT says so. (Optional: click the logo to play the ten-second reveal.)\n\nThank you. Desmond and I are happy to take your questions.",
];

// ---------- images ----------
async function glow(base, blobs) {
  const g = blobs.map((b, i) => `<radialGradient id="g${i}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#${b.c}" stop-opacity="${b.o}"/>
      <stop offset="100%" stop-color="#${b.c}" stop-opacity="0"/></radialGradient>`).join("");
  const e = blobs.map((b, i) => `<ellipse cx="${b.x}" cy="${b.y}" rx="${b.r}" ry="${b.r * 0.8}" fill="url(#g${i})"/>`).join("");
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
    <defs>${g}</defs><rect width="1920" height="1080" fill="#${base}"/>${e}</svg>`;
  return "image/jpeg;base64," + (await sharp(Buffer.from(svg)).jpeg({ quality: 88 }).toBuffer()).toString("base64");
}
// The light slides: a diagonal lavender-to-peach wash with sky and mint glows. Pale enough that
// dark text, white cards and screenshots all keep their contrast.
async function pastel() {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><defs>
    <linearGradient id="w" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#E9E3FF"/><stop offset="0.5" stop-color="#F4EEFB"/>
      <stop offset="1" stop-color="#FFE6D6"/></linearGradient>
    <radialGradient id="a" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#CFE4FF" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#CFE4FF" stop-opacity="0"/></radialGradient>
    <radialGradient id="b" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFD9E2" stop-opacity="0.8"/>
      <stop offset="1" stop-color="#FFD9E2" stop-opacity="0"/></radialGradient>
    <radialGradient id="c" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#D4F5E9" stop-opacity="0.7"/>
      <stop offset="1" stop-color="#D4F5E9" stop-opacity="0"/></radialGradient></defs>
    <rect width="1920" height="1080" fill="url(#w)"/>
    <ellipse cx="1750" cy="90" rx="700" ry="520" fill="url(#a)"/>
    <ellipse cx="120" cy="1040" rx="760" ry="560" fill="url(#c)"/>
    <ellipse cx="1820" cy="1060" rx="560" ry="420" fill="url(#b)"/></svg>`;
  return "image/jpeg;base64," + (await sharp(Buffer.from(svg)).jpeg({ quality: 90 }).toBuffer()).toString("base64");
}
// The logo-reveal still, darkened on the left so the title reads over it.
async function heroImage() {
  const shade = `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><defs>
    <linearGradient id="s" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="#${HEX.dk1}" stop-opacity="0.96"/>
      <stop offset="0.5" stop-color="#${HEX.dk1}" stop-opacity="0.9"/>
      <stop offset="0.78" stop-color="#${HEX.dk1}" stop-opacity="0.2"/>
      <stop offset="1" stop-color="#${HEX.dk1}" stop-opacity="0"/></linearGradient></defs>
    <rect width="1920" height="1080" fill="url(#s)"/></svg>`;
  const buf = await sharp(path.join(SHOTS, "logo-reveal-blueprint.jpg")).resize(1920, 1080, { fit: "cover", position: "right" })
    .composite([{ input: Buffer.from(shade) }]).jpeg({ quality: 88 }).toBuffer();
  return "image/jpeg;base64," + buf.toString("base64");
}
async function icon(Comp, hex, px = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(Comp, { color: "#" + hex, size: px, strokeWidth: 2 }));
  return "image/png;base64," + (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}

// ---------- helpers ----------
const shadow = (dark) => ({ type: "outer", color: "000000", blur: dark ? 20 : 14, offset: 4, angle: 90,
  opacity: dark ? 0.5 : 0.18 });
function card(slide, x, y, w, h, o = {}) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: o.r || 0.16, rotate: o.rotate || 0,
    fill: { color: o.fill || C.background1, transparency: o.transparency || 0 },
    line: { color: o.line || o.fill || C.background1, width: o.lineW || 0.75 },
    shadow: o.noShadow ? undefined : shadow(o.dark), objectName: o.name || "card",
  });
}
function pill(slide, t, x, y, o = {}) {
  const w = o.w || 1.6;
  slide.addText(t, {
    x, y, w, h: o.h || 0.42, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.21,
    fill: { color: o.fill || C.accent3 }, color: o.color || C.background1,
    fontFace: o.mono ? "Courier New" : undefined, fontSize: o.size || 14, bold: o.bold !== false,
    align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "pill",
  });
  return w;
}
function source(slide, t, tone) {
  slide.addText("source · " + t, {
    x: 6.4, y: 7.05, w: 5.75, h: 0.3, fontFace: "Courier New", fontSize: 10, align: "right",
    color: tone === "light" ? C.background1 : tone === "dark" ? C.accent2 : C.accent3,
    margin: 0, isTextBox: true, objectName: "source",
  });
}
async function iconDisc(slide, Comp, x, y, d, fill, fg) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill } });
  const p = d * 0.24;
  slide.addImage({ data: await icon(Comp, fg), x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, objectName: "icon" });
}
function numDisc(slide, n, x, y, d, fill, fg) {
  slide.addText(String(n), { x, y, w: d, h: d, shape: pres.shapes.OVAL, fill: { color: fill },
    line: { color: C.background1, width: 2.5 }, color: fg || C.background1, bold: true, fontFace: "Arial",
    fontSize: Math.round(d * 32), align: "center", valign: "middle", margin: 0, isTextBox: true });
}
function screenshot(slide, file, x, y, w, h, o = {}) {
  const p = o.pad === undefined ? 0.1 : o.pad;
  card(slide, x - p, y - p, w + 2 * p, h + 2 * p, { rotate: o.rotate, dark: o.dark, r: 0.12, name: "frame" });
  slide.addImage({ path: path.join(SHOTS, file), x, y, w, h, rotate: o.rotate || 0, objectName: "screenshot " + file });
}
function text(slide, t, o) {
  slide.addText(t, { margin: 0, isTextBox: true, valign: "top", color: C.text2, fontSize: 18, ...o });
}
// A single-value ring: a doughnut with the value coloured and the rest as a track.
function ring(slide, value, total, x, y, d, col, o = {}) {
  slide.addChart(pres.charts.DOUGHNUT, [{ name: o.name || "ring", labels: ["value", "rest"],
    values: [value, Math.max(total - value, 0.0001)] }], {
    x, y, w: d, h: d, holeSize: o.hole || 72, showValue: false, showPercent: false, showLegend: false,
    showLabel: false, firstSliceAng: 0, dataBorder: { pt: 0.5, color: o.border || "FFFFFF" },
    chartColors: [col, o.track || TRACK], objectName: o.name || "ring",
  });
}

const sections = new Set();
let slideCount = 0;
function newSlide(masterName, sectionTitle) {
  if (!sections.has(sectionTitle)) {
    pres.addSection({ title: sectionTitle });
    sections.add(sectionTitle);
  }
  const slide = pres.addSlide({ masterName, sectionTitle });
  slide.addNotes(NOTES[slideCount++]);
  step = 0;
  // Anything added while a click step is set is named "animN_…"; addAnimations() turns the
  // names into click-triggered fades, in step order.
  for (const m of ["addText", "addShape", "addImage", "addChart", "addMedia"]) {
    const orig = slide[m].bind(slide);
    slide[m] = (...args) => {
      const o = args[args.length - 1];
      if (step > 0 && o && typeof o === "object" && !Array.isArray(o) && !o.placeholder) {
        o.objectName = `anim${step}_${o.objectName || m}`;
      }
      return orig(...args);
    };
  }
  return slide;
}
let step = 0;
const go = (n) => { step = n; };
function heading(slide, kicker, title) {
  slide.addText(kicker.toUpperCase(), { placeholder: "kicker" });
  slide.addText(title, { placeholder: "title" });
}

async function build() {
  const BG = {
    dark: await glow(HEX.dk1, [
      { c: HEX.accent1, o: 0.42, x: 1900, y: -80, r: 760 },
      { c: HEX.accent5, o: 0.45, x: -60, y: 1120, r: 820 },
    ]),
    light: await pastel(),
    vivid: await glow(HEX.accent1, [
      { c: "FF7A1A", o: 0.9, x: 1750, y: 80, r: 900 },
      { c: HEX.accent5, o: 0.75, x: 40, y: 1120, r: 900 },
    ]),
  };
  pres.defineSlideMaster({ title: "Title", background: { data: await heroImage() }, objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 2.0, w: 8.2, h: 2.8, fontSize: 48,
      bold: true, color: C.background1, valign: "top", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 4.95, w: 7.0, h: 0.85, fontSize: 20,
      color: C.background1, align: "left", margin: 0 }, text: "" } },
  ] });
  for (const [name, bg, tone] of [["Content", BG.light, "white"], ["Content Dark", BG.dark, "dark"],
    ["Content Vivid", BG.vivid, "vivid"]]) {
    const dark = tone !== "white";
    pres.defineSlideMaster({
      title: name, background: { data: bg }, margin: [0.4, 0.5, 0.5, 0.5],
      objects: [
        { placeholder: { options: { name: "kicker", type: "body", x: 0.5, y: 0.32, w: 9, h: 0.32, fontSize: 14,
          bold: true, charSpacing: 3, align: "left", margin: 0,
          color: tone === "vivid" ? C.background1 : dark ? C.accent2 : C.accent1 }, text: "" } },
        { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.66, w: 12.33, h: 0.9, fontSize: 40,
          bold: true, color: dark ? C.background1 : C.text1, valign: "top", align: "left", margin: 0 }, text: "" } },
        { text: { text: "PARROT  ·  SMU IGD · AI in the Digital Economy  ·  2026", options: {
          x: 0.5, y: 7.05, w: 6, h: 0.3, fontSize: 10, margin: 0, color: dark ? MIST : C.text2 } } },
      ],
      slideNumber: { x: 12.3, y: 7.05, w: 0.53, h: 0.3, fontSize: 10, align: "right", color: dark ? MIST : C.text2 },
    });
  }

  // 1 · Title: the logo-reveal still behind the words
  {
    const s = newSlide("Title", "Opening");
    s.addImage({ path: path.join(ASSETS, "parrot-logo.png"), x: 0.6, y: 0.55, w: 3.0, h: 0.91, objectName: "logo" });
    text(s, "IGD ILP 2026  ·  GROUP 1  ·  FINAL PRESENTATION", { x: 0.6, y: 1.55, w: 7.6, h: 0.32,
      fontSize: 14, bold: true, charSpacing: 3, color: C.accent2 });
    s.addText([
      { text: "Your family's paperwork,", options: { breakLine: true } },
      { text: "answered.", options: { color: C.accent2, breakLine: true } },
      { text: "On your own machine." },
    ], { placeholder: "title" });
    s.addText("A local-first household AI that shows its page, and says so when it does not know.",
      { placeholder: "body" });
    go(1);
    let x = 0.6;
    const fills = [C.accent1, C.accent2, C.accent3, C.accent4, C.accent5];
    for (let i = 0; i < TEAM.length; i++) {
      x += pill(s, TEAM[i], x, 6.05, { fill: fills[i], color: i === 1 ? C.text1 : C.background1, w: 1.45,
        h: 0.46, size: 15 }) + 0.12;
    }
    text(s, "Presented by Siew Siew and Desmond  ·  SMU Industry Graduate Diploma  ·  Sep to Nov 2026",
      { x: 0.6, y: 6.7, w: 8.5, h: 0.32, fontSize: 13, color: MIST });
  }

  // 2 · Problem
  {
    const s = newSlide("Content Dark", "The problem");
    heading(s, "The problem", "The family filing system is a drawer");
    const people = [
      [Fi.FiCalendar, "Sarah, 35", "Working mother", "Renewals and due dates live in six inboxes and a drawer.", C.accent1, HEX.accent1],
      [Fi.FiUsers, "Marcus, 39", "Sandwich generation", "Eleven policies, five people. One question: are we covered?", C.accent3, HEX.accent3],
      [Fi.FiPercent, "Priya, 32", "Saves tax through SRS", "Miss the window and the relief is gone, silently.", C.accent4, HEX.accent4],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, name, who, pain, fill, hex] = people[i];
      go(i + 1);
      const x = 0.5 + i * 4.18;
      card(s, x, 1.8, 3.97, 3.7, { fill, dark: true });
      await iconDisc(s, ic, x + 0.35, 2.1, 0.95, C.background1, hex);
      text(s, name, { x: x + 1.45, y: 2.12, w: 2.4, h: 0.5, fontFace: "Arial", bold: true, fontSize: 28, color: C.background1 });
      text(s, who, { x: x + 1.45, y: 2.62, w: 2.4, h: 0.4, fontSize: 17, bold: true, color: C.background1 });
      text(s, pain, { x: x + 0.35, y: 3.35, w: 3.3, h: 2.0, fontSize: 24, color: C.background1 });
    }
    go(4);
    s.addText([
      { text: "Not missing documents. ", options: { bold: true } },
      { text: "Missing a way to ask the pile a question, and trust the answer." },
    ], { x: 0.5, y: 5.75, w: 12.33, h: 1.05, fontSize: 24, color: C.text1, margin: [0.1, 0.35, 0.1, 0.35],
      shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.18, fill: { color: C.accent2 }, valign: "middle",
      isTextBox: true, objectName: "banner" });
    source(s, "corpus/canon.md · proposal §2", "dark");
  }

  // 3 · Solution
  {
    const s = newSlide("Content", "The product");
    heading(s, "The solution", "Photograph it. Ask it. It shows its page");
    const steps = [
      [Fi.FiCamera, "Capture", "Telegram or a folder. It files itself.", C.accent1, HEX.lt1],
      [Fi.FiMessageSquare, "Ask", "Plain English. Every sentence shows its page.", C.accent2, HEX.dk1],
      [Fi.FiSun, "Today", "It speaks first: what expires, what is due.", C.accent3, HEX.lt1],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, h, b, fill, fg] = steps[i];
      go(i + 1);
      const y = 1.85 + i * 1.5;
      await iconDisc(s, ic, 0.5, y, 1.1, fill, fg);
      text(s, `0${i + 1}  ${h}`, { x: 1.85, y: y - 0.02, w: 5.3, h: 0.55, fontFace: "Arial", bold: true, fontSize: 28, color: C.text1 });
      text(s, b, { x: 1.85, y: y + 0.55, w: 5.3, h: 0.6, fontSize: 19 });
    }
    go(4);
    text(s, "When the documents don't say, PARROT says so.", { x: 0.5, y: 6.35, w: 7.0, h: 0.5,
      fontSize: 22, italic: true, bold: true, color: C.accent1 });
    go(5);
    screenshot(s, "03-capture.jpg", 7.55, 1.75, 2.7, 5.1, { rotate: -5 });
    screenshot(s, "final-ask.jpg", 10.15, 2.0, 2.75, 3.85, { rotate: 4 });
    pill(s, "b1-0001.pdf  p.1", 10.4, 6.2, { w: 2.3, fill: C.accent4, mono: true, size: 14 });
    source(s, "docs/report/deck-shots");
  }

  // 4 · Four screens, fanned edge to edge
  {
    const s = newSlide("Content Dark", "The product");
    heading(s, "The interface", "Four screens. It speaks first");
    const screens = [["07-today.png", "Today", C.accent1, "What needs you now"], ["07-ask.png", "Ask", C.accent2, "Every answer shows its page"],
      ["07-vault.png", "Vault", C.accent3, "What it read, and what it couldn't"], ["07-packs.png", "Packs", C.accent4, "Switch one off, its advice goes quiet"]];
    const w = 2.95, h = w * 1255 / 935;
    for (let i = 0; i < 4; i++) {
      const [f, name, col, cap] = screens[i];
      go(i + 1);
      const x = 0.55 + i * 3.18;
      screenshot(s, f, x, 1.8, w, h, { rotate: [-4, 2, -2, 4][i], dark: true });
      pill(s, name, x + 0.15, 1.55, { w: 1.45, h: 0.5, fill: col, color: i === 1 ? C.text1 : C.background1, size: 18 });
      text(s, cap, { x, y: 1.95 + h + 0.12, w: w, h: 0.5, fontSize: 16, bold: true, color: C.background1, align: "center" });
    }
    source(s, "web/ · docs/report/deck-shots", "dark");
  }

  // 5 · Anatomy of an answer
  {
    const s = newSlide("Content", "The product");
    heading(s, "Anatomy of an answer", "Numbers come from Postgres, not the model");
    const sx = 0.6, sy = 1.8, sh = 5.05, sw = sh * 800 / 1121;
    screenshot(s, "final-ask.jpg", sx, sy, sw, sh);
    const at = (px, py) => [sx + px / 800 * sw, sy + py / 1121 * sh];
    const spots = [[505, 297], [540, 423], [715, 485], [740, 981]];
    const cols = [C.accent1, C.accent2, C.accent3, C.accent4];
    const pts = [
      ["Every sentence cites its page", "Fact rows cannot be written without document and page."],
      ["Nothing left this computer", "Every model, even the grader, runs on the laptop."],
      ["It knows what it is not", "Not a licensed adviser, and it says so."],
      ["Typed numbers, not generated ones", "Dates and amounts come from Postgres columns."],
    ];
    for (let i = 0; i < 4; i++) {
      const [px, py] = at(...spots[i]);
      go(i + 1);
      numDisc(s, i + 1, px - 0.25, py - 0.25, 0.5, cols[i], i === 1 ? C.text1 : C.background1);
      const y = 1.8 + i * 1.29;
      card(s, 4.6, y, 8.23, 1.13);
      numDisc(s, i + 1, 4.8, y + 0.22, 0.7, cols[i], i === 1 ? C.text1 : C.background1);
      text(s, pts[i][0], { x: 5.75, y: y + 0.12, w: 6.9, h: 0.45, fontFace: "Arial", bold: true, fontSize: 21, color: C.text1 });
      text(s, pts[i][1], { x: 5.75, y: y + 0.6, w: 6.9, h: 0.42, fontSize: 17 });
    }
    source(s, "AGENTS.md · hard rules 2 and 3");
  }

  // 6 · Architecture
  {
    const s = newSlide("Content Dark", "The platform");
    heading(s, "Architecture", "Five layers. One laptop. One database");
    const rows = [
      ["Launch & UI", HEX.accent2, ["Launcher", "Next.js 15 screens", "FastAPI engine"]],
      ["Capture", HEX.accent1, ["Folder · Telegram", "Celery worker", "Docling parse", "Vision quarantine"]],
      ["Answering", "4F95FF", ["LangGraph", "Hybrid + RRF", "bge reranker", "Evidence gate"]],
      ["Runtime", "2BC48F", ["Redis", "SEA-LION 4B VL", "EmbeddingGemma", "Postgres + pgvector"]],
      ["Knowledge", "A97BFF", ["contracts.py", "Domain packs", "Modules", "Grounding corpus"]],
    ];
    for (let r = 0; r < rows.length; r++) {
      const [label, col, boxes] = rows[r];
      go(r + 1);
      const y = 1.75 + r * 1.03;
      text(s, label.toUpperCase(), { x: 0.5, y, w: 2.2, h: 0.88, fontSize: 16, bold: true, charSpacing: 2, color: col, valign: "middle" });
      const bw = (12.83 - 2.75 - (boxes.length - 1) * 0.15) / boxes.length;
      for (let b = 0; b < boxes.length; b++) {
        s.addText(boxes[b], { x: 2.75 + b * (bw + 0.15), y, w: bw, h: 0.88, shape: pres.shapes.ROUNDED_RECTANGLE,
          rectRadius: 0.12, fill: { color: col, transparency: 70 }, line: { color: col, width: 2 },
          color: C.background1, bold: true, fontSize: 19, align: "center", valign: "middle", margin: 0.05,
          isTextBox: true, objectName: "arch box" });
      }
    }
    source(s, "gitdiagram · README stack table", "dark");
  }

  // 7 · Platform: two axes
  {
    const s = newSlide("Content", "The platform");
    heading(s, "The platform", "One engine. Two ways to grow");
    go(1);
    s.addText([
      { text: "THE CORE ENGINE", options: { fontSize: 14, bold: true, charSpacing: 3, color: C.accent2, breakLine: true } },
      { text: "File · Find", options: { fontSize: 32, bold: true, fontFace: "Arial", color: C.background1, breakLine: true } },
      { text: "Check · Cite", options: { fontSize: 32, bold: true, fontFace: "Arial", color: C.background1 } },
    ], { x: 4.62, y: 1.85, w: 4.1, h: 3.4, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.2,
      fill: { color: C.text1 }, align: "center", valign: "middle", margin: 0.1, isTextBox: true, shadow: shadow(), objectName: "engine" });
    const sides = [
      [0.5, Fi.FiZap, "Modules", "Reminder · Alert · Advice", "Read typed rows. Never see the screen.", C.accent3, HEX.accent3],
      [8.95, Fi.FiPackage, "Domain packs", "Tax · Insurance", "One YAML file of know-how each.", C.accent1, HEX.accent1],
    ];
    for (const [x, ic, h, sub, b, fill, hex] of sides) {
      go(x < 5 ? 2 : 3);
      card(s, x, 1.85, 3.88, 3.4, { fill });
      await iconDisc(s, ic, x + 0.3, 2.1, 0.85, C.background1, hex);
      text(s, h, { x: x + 1.3, y: 2.25, w: 2.5, h: 0.55, fontFace: "Arial", bold: true, fontSize: 26, color: C.background1 });
      text(s, sub, { x: x + 0.3, y: 3.15, w: 3.4, h: 0.45, fontSize: 19, bold: true, color: C.background1 });
      text(s, b, { x: x + 0.3, y: 3.7, w: 3.4, h: 1.2, fontSize: 19, color: C.background1 });
    }
    go(2);
    s.addShape(pres.shapes.LINE, { x: 4.38, y: 3.55, w: 0.24, h: 0, line: { color: C.accent3, width: 4, endArrowType: "triangle" } });
    go(3);
    s.addShape(pres.shapes.LINE, { x: 8.72, y: 3.55, w: 0.23, h: 0, line: { color: C.accent1, width: 4, beginArrowType: "triangle" } });
    go(4);
    const stats = [["2", "packs built", C.accent1], ["9", "more specified", C.accent3], ["3", "modules running", C.accent4],
      ["0", "packs that can act", C.accent5]];
    for (let i = 0; i < 4; i++) {
      text(s, stats[i][0], { x: 0.5 + i * 3.15, y: 5.4, w: 1.2, h: 1.05, fontFace: "Arial", bold: true, fontSize: 64,
        color: stats[i][2], valign: "middle" });
      text(s, stats[i][1], { x: 1.55 + i * 3.15, y: 5.4, w: 1.95, h: 1.05, fontSize: 19, bold: true, color: C.text1, valign: "middle" });
    }
    source(s, "core/contracts.py · packs/catalogue.yaml");
  }

  // 8 · A pack at work
  {
    const s = newSlide("Content Dark", "The evidence");
    heading(s, "A working domain pack", "Ask what's missing. Code does the sums");
    screenshot(s, "06-advice.png", 0.65, 1.9, 5.7, 5.7 * 930 / 1080, { rotate: -2, dark: true });
    go(1);
    text(s, "\u201CReview my insurance coverage and tell me what is lacking.\u201D", { x: 6.9, y: 1.8, w: 5.95, h: 0.95,
      fontSize: 22, italic: true, color: C.accent2 });
    go(2);
    card(s, 6.9, 2.95, 2.88, 2.4, { fill: C.accent1, dark: true });
    text(s, "715k", { x: 7.1, y: 3.05, w: 2.5, h: 1.05, fontFace: "Arial", bold: true, fontSize: 60, color: C.background1, valign: "bottom" });
    text(s, "SGD short on life cover", { x: 7.1, y: 4.15, w: 2.5, h: 1.0, fontSize: 18, bold: true, color: C.background1 });
    go(3);
    card(s, 9.95, 2.95, 2.88, 2.4, { fill: C.accent3, dark: true });
    text(s, "251k", { x: 10.15, y: 3.05, w: 2.5, h: 1.05, fontFace: "Arial", bold: true, fontSize: 60, color: C.background1, valign: "bottom" });
    text(s, "SGD short on critical illness", { x: 10.15, y: 4.15, w: 2.5, h: 1.0, fontSize: 18, bold: true, color: C.background1 });
    go(4);
    text(s, "9 × income, from his payslip, against cover from his policies. Plain code does the sums; every input is cited.",
      { x: 6.9, y: 5.55, w: 5.95, h: 0.95, fontSize: 18, color: C.background1 });
    source(s, "packs/insurance_agent · Pitch Script §06", "dark");
  }

  // 9 · Corpus
  {
    const s = newSlide("Content", "The evidence");
    heading(s, "The corpus", "One synthetic family, written first");
    const iw = 6.0, ih = iw * 1536 / 2816;
    screenshot(s, "09-photo-doc.jpg", 0.75, 1.95, iw, ih, { rotate: -3, pad: 0.12 });
    go(1);
    const fam = [["M", "Marcus"], ["R", "Rachel"], ["L", "Lucas"], ["AK", "Ah Kow"], ["ML", "Mei Ling"]];
    const fc = [C.accent1, C.accent3, C.accent2, C.accent4, C.accent5];
    for (let i = 0; i < 5; i++) {
      const x = 0.6 + i * 1.27;
      s.addText(fam[i][0], { x: x + 0.15, y: 5.55, w: 0.75, h: 0.75, shape: pres.shapes.OVAL, fill: { color: fc[i] },
        line: { color: fc[i] }, color: i === 2 ? C.text1 : C.background1, bold: true, fontSize: 18, align: "center",
        valign: "middle", margin: 0, isTextBox: true });
      text(s, fam[i][1], { x: x - 0.1, y: 6.38, w: 1.25, h: 0.35, fontSize: 15, bold: true, align: "center", color: C.text1 });
    }
    const tiles = [["93", "documents in the vault", C.accent1], ["16", "document types", C.accent3],
      ["118", "golden questions", C.accent4], ["15", "adversarial traps", C.accent2]];
    for (let i = 0; i < 4; i++) {
      go(i + 2);
      const x = 7.2 + (i % 2) * 2.88;
      const y = 1.8 + Math.floor(i / 2) * 2.55;
      const fg = i === 3 ? C.text1 : C.background1;
      card(s, x, y, 2.73, 2.35, { fill: tiles[i][2] });
      text(s, tiles[i][0], { x: x + 0.25, y: y + 0.15, w: 2.3, h: 1.15, fontFace: "Arial", bold: true, fontSize: 66, color: fg, valign: "bottom" });
      text(s, tiles[i][1], { x: x + 0.25, y: y + 1.4, w: 2.3, h: 0.8, fontSize: 19, bold: true, color: fg });
    }
    source(s, "corpus/canon.md · docs/report/05 §5.2");
  }

  // 10 · Thesis: the big doughnut
  {
    const s = newSlide("Content Dark", "The evidence");
    heading(s, "How we judge it", "Judge it on whether it guesses");
    s.addChart(pres.charts.DOUGHNUT, [{ name: "Run 3 answers", labels: ["Unanswerable, answered anyway",
      "Wrong value", "False not on file", "Supported"], values: [12, 8, 5, 93] }], {
      x: 0.35, y: 1.6, w: 5.35, h: 5.35, holeSize: 62, showValue: false, showPercent: false, showLegend: false,
      showLabel: false, firstSliceAng: 0, dataBorder: { pt: 2, color: HEX.dk1 },
      chartColors: [HEX.accent1, HEX.accent2, "4F95FF", HEX.accent6], objectName: "claims doughnut",
    });
    text(s, "25", { x: 1.6, y: 3.35, w: 2.85, h: 1.2, fontFace: "Arial", bold: true, fontSize: 80, color: C.background1, align: "center", valign: "middle" });
    text(s, "unsupported claims\nin 118 answers", { x: 1.6, y: 4.55, w: 2.85, h: 0.7, fontSize: 16, color: MIST, align: "center" });
    const parts = [["12", "unanswerable questions answered anyway", C.accent1], ["8", "wrong values", C.accent2],
      ["5", "false \u201Cnot on file\u201D", "4F95FF"], ["0", "leaks on the adversarial set", "2BC48F"]];
    for (let i = 0; i < 4; i++) {
      go(i + 1);
      const y = 1.75 + i * 1.1;
      text(s, parts[i][0], { x: 6.0, y, w: 1.3, h: 0.95, fontFace: "Arial", bold: true, fontSize: 56, color: parts[i][2], valign: "middle", align: "right" });
      text(s, parts[i][1], { x: 7.55, y, w: 5.3, h: 0.95, fontSize: 22, bold: true, color: C.background1, valign: "middle" });
    }
    go(5);
    s.addText([{ text: "A confident wrong answer is worse than none. ", options: { bold: true, color: C.accent2 } },
      { text: "With Run 3's fixes, 25 fell to 21.", options: { color: C.background1 } }],
    { x: 6.0, y: 6.15, w: 6.85, h: 0.7, fontSize: 19, margin: 0, isTextBox: true, valign: "middle" });
    source(s, "docs/report/05 §5.1 and §5.5", "dark");
  }

  // 11 · Scorecard: five rings
  {
    const s = newSlide("Content", "The evidence");
    heading(s, "The scorecard", "Five numbers, one per aim, scored by code");
    const rings = [
      [77, 93, "77", "/93", "right and cited", HEX.accent4],
      [21, 118, "21", "/118", "unsupported claims", HEX.accent1],
      [4, 93, "4", "/93", "over-cautious", HEX.accent3],
      [0.961, 1, "0.961", "", "extraction F1", HEX.accent2],
      [15, 15, "15", "/15", "traps contained", HEX.accent5],
    ];
    const d = 2.35;
    for (let i = 0; i < 5; i++) {
      const [v, t, big, small, label, col] = rings[i];
      go(i + 1);
      const x = 0.5 + i * 2.5;
      ring(s, v, t, x, 1.85, d, col, { name: label, hole: 76 });
      s.addText([{ text: big, options: { fontSize: i === 3 ? 26 : 34, bold: true, color: C.text1, breakLine: !!small } },
        ...(small ? [{ text: small, options: { fontSize: 14, color: C.text2 } }] : [])],
      { x: x + 0.45, y: 1.85 + d / 2 - 0.5, w: d - 0.9, h: 1.0, fontFace: "Arial", align: "center", valign: "middle", margin: 0, isTextBox: true });
      text(s, label, { x: x - 0.05, y: 4.3, w: d + 0.1, h: 0.45, fontSize: 19, bold: true, color: C.text1, align: "center" });
    }
    go(6);
    s.addText([{ text: "Lower is better on one ring only: ", options: { bold: true, color: C.accent1 } },
      { text: "unsupported claims, from 25 in Run 3 to 21 on 28 October. Every other ring moved up, on the same 93-document vault.", options: { color: C.text2 } }],
    { x: 0.5, y: 5.2, w: 12.33, h: 1.0, fontSize: 19, margin: [0.1, 0.3, 0.1, 0.3], shape: pres.shapes.ROUNDED_RECTANGLE,
      rectRadius: 0.16, fill: { color: C.background2 }, valign: "middle", isTextBox: true });
    text(s, "Five-number headline proposed, awaiting supervisor sign-off.", { x: 0.5, y: 6.4, w: 8, h: 0.4, fontSize: 15, italic: true });
    source(s, "eval/results/2026-10-28-since-run3-on-main");
  }

  // 12 · Retrieval lesson
  {
    const s = newSlide("Content", "The evidence");
    heading(s, "What retrieval taught us", "The right page in the window wins");
    const labels = ["Run 1 · 6 docs", "26 docs", "Hybrid + reranker", "Run 3 · 93 docs"];
    s.addChart(pres.charts.BAR, [
      { name: "Recall", labels, values: [0.895, 0.821, 0.897, 0.848] },
      { name: "Precision", labels, values: [0.868, 0.767, 0.854, 0.82] },
      { name: "Faithfulness", labels, values: [0.819, 0.81, 0.967, 0.892] },
    ], {
      x: 0.4, y: 1.7, w: 7.6, h: 5.2, barDir: "col", barGapWidthPct: 40, chartColors: [HEX.accent3, HEX.accent2, HEX.accent1],
      showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.00", dataLabelFontSize: 12, dataLabelFontBold: true,
      dataLabelColor: HEX.dk2, dataLabelFontFace: "+mn-lt", valAxisMinVal: 0.6, valAxisMaxVal: 1.0, valAxisHidden: true,
      valGridLine: { style: "none" }, catGridLine: { style: "none" }, catAxisLabelColor: HEX.dk2, catAxisLabelFontSize: 14,
      catAxisLabelFontFace: "+mn-lt", showLegend: true, legendPos: "t", legendFontSize: 14, legendColor: HEX.dk2,
      legendFontFace: "+mn-lt", objectName: "retrieval diagnostics",
    });
    go(1);
    card(s, 8.3, 1.8, 4.53, 2.55, { fill: C.accent1 });
    text(s, "FAITHFULNESS", { x: 8.6, y: 2.0, w: 4, h: 0.35, fontSize: 15, bold: true, charSpacing: 3, color: C.background1 });
    text(s, "0.81 \u2192 0.97", { x: 8.6, y: 2.4, w: 4.1, h: 0.95, fontFace: "Arial", bold: true, fontSize: 48, color: C.background1, valign: "middle" });
    text(s, "hybrid search plus a cross-encoder", { x: 8.6, y: 3.4, w: 4.1, h: 0.75, fontSize: 18, color: C.background1 });
    const pts = [["Bigger corpus alone: precision fell 0.10", C.accent3], ["Full text finds policy numbers", C.accent2],
      ["Run 3: 19 of 21 misses had the page", C.accent4]];
    for (let i = 0; i < 3; i++) {
      go(i + 2);
      const y = 4.6 + i * 0.75;
      s.addShape(pres.shapes.OVAL, { x: 8.35, y: y + 0.12, w: 0.3, h: 0.3, fill: { color: pts[i][1] }, line: { color: pts[i][1] } });
      text(s, pts[i][0], { x: 8.85, y, w: 4.0, h: 0.6, fontSize: 18, bold: true, color: C.text1, valign: "middle" });
    }
    source(s, "docs/report/05 §5.4");
  }

  // 13 · Governance
  {
    const s = newSlide("Content Dark", "Trust and what next");
    heading(s, "Governance and assurance", "It advises. It never pays, books or files");
    go(1);
    text(s, "\u201CRenew my policy and pay the premium.\u201D", { x: 0.5, y: 1.8, w: 6, h: 0.5, fontSize: 22, italic: true, color: C.accent2 });
    screenshot(s, "final-refusal-crop.jpg", 0.65, 2.55, 5.7, 5.7 * 300 / 800, { rotate: -2, dark: true });
    go(2);
    text(s, "never_acts: true", { x: 0.5, y: 5.0, w: 6.0, h: 0.8, fontFace: "Courier New", bold: true, fontSize: 36, color: "2BC48F", valign: "middle" });
    text(s, "Typed Literal[True] in every pack: one that can act will not load.", { x: 0.5, y: 5.85, w: 6.0, h: 0.8, fontSize: 18, color: C.background1 });
    const docs = [[Fi.FiLock, "PDPA", "Inventory, consent, retention, breach", HEX.accent1, HEX.lt1],
      [Fi.FiLayers, "ISO/IEC 22989 \u2192 5338", "Every lifecycle stage mapped to a file", HEX.accent2, HEX.dk1],
      [Fi.FiFlag, "IMDA governance", "Nine GenAI dimensions, autonomy statement", HEX.accent3, HEX.lt1],
      [Fi.FiFileText, "Model card and terms", "What it is for, and where it fails", HEX.accent4, HEX.lt1]];
    for (let i = 0; i < 4; i++) {
      const [ic, h, b, col, fg] = docs[i];
      go(i + 3);
      const y = 1.8 + i * 1.27;
      card(s, 6.85, y, 5.98, 1.12, { fill: C.accent6, dark: true });
      await iconDisc(s, ic, 7.05, y + 0.18, 0.76, col, fg);
      text(s, h, { x: 8.0, y: y + 0.12, w: 4.7, h: 0.45, fontFace: "Arial", bold: true, fontSize: 21, color: C.background1 });
      text(s, b, { x: 8.0, y: y + 0.6, w: 4.7, h: 0.42, fontSize: 17, color: MIST });
    }
    source(s, "docs/governance/", "dark");
  }

  // 14 · Roadmap staircase
  {
    const s = newSlide("Content", "Trust and what next");
    heading(s, "Commercialisation", "Packs are the unit of sale");
    const stages = [["Now", "Prototype", "Two packs, two modules", C.accent4],
      ["Next", "Household", "Catalogue packs, one at a time", C.accent3],
      ["Then", "Pro seat", "An agent reviews cover, with consent", C.accent2],
      ["Later", "Marketplace", "Packs by domain experts", C.accent1]];
    for (let i = 0; i < 4; i++) {
      const [when, h, b, col] = stages[i];
      go(i + 1);
      const x = 0.5 + i * 3.13;
      const y = 3.5 - i * 0.55;
      const fg = i === 2 ? C.text1 : C.background1;
      card(s, x, y, 2.95, 6.2 - y, { fill: col });
      text(s, when.toUpperCase(), { x: x + 0.25, y: y + 0.2, w: 2.5, h: 0.35, fontSize: 15, bold: true, charSpacing: 3, color: fg });
      text(s, h, { x: x + 0.25, y: y + 0.6, w: 2.5, h: 0.55, fontFace: "Arial", bold: true, fontSize: 26, color: fg });
      text(s, b, { x: x + 0.25, y: y + 1.25, w: 2.5, h: 1.2, fontSize: 19, color: fg });
    }
    go(5);
    text(s, "No price claimed: willingness to pay is a hypothesis, ordered by how countable the loss is.",
      { x: 0.5, y: 6.35, w: 12.33, h: 0.5, fontSize: 18, italic: true });
    source(s, "docs/report/07-commercialisation-roadmap.md");
  }

  // 15 · Close, with the logo reveal to play
  {
    const s = newSlide("Content Vivid", "Trust and what next");
    heading(s, "Thank you", "When it doesn't know, PARROT says so");
    const next = [["Prove it on real paper", "14 of 40 holdout documents so far"],
      ["Turn the label check on", "ADR 0021: two fewer unsupported claims"],
      ["Measure the minimum machine", "Fit it on an 8 GB GPU, publish the spec"]];
    for (let i = 0; i < 3; i++) {
      const y = 1.85 + i * 1.3;
      go(i + 1);
      numDisc(s, i + 1, 0.5, y, 0.9, C.background1, C.accent1);
      text(s, next[i][0], { x: 1.65, y: y - 0.02, w: 5.6, h: 0.5, fontFace: "Arial", bold: true, fontSize: 26, color: C.background1 });
      text(s, next[i][1], { x: 1.65, y: y + 0.5, w: 5.6, h: 0.45, fontSize: 19, color: C.background1 });
    }
    go(4);
    const vx = 7.45, vy = 1.85, vw = 5.4, vh = vw * 9 / 16;
    card(s, vx - 0.1, vy - 0.1, vw + 0.2, vh + 0.2, { dark: true, r: 0.14, name: "video frame" });
    const cover = await sharp(path.join(SHOTS, "logo-reveal-final.jpg")).png().toBuffer();
    s.addMedia({ type: "video", path: path.join(ASSETS, "parrot logo reveal.mp4"), x: vx, y: vy, w: vw, h: vh,
      cover: "data:image/png;base64," + cover.toString("base64"), objectName: "logo reveal" });
    text(s, "Questions?", { x: 7.45, y: 5.15, w: 5.4, h: 0.8, fontFace: "Arial", bold: true, fontSize: 40, color: C.background1, align: "center" });
    go(0);
    let x = 0.5;
    for (const n of TEAM) {
      x += pill(s, n, x, 6.2, { fill: C.background1, color: C.accent1, w: 1.45, h: 0.46, size: 15 }) + 0.12;
    }
    source(s, "docs/report/05 §5.5 · README.md", "light");
  }

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  await addFades(OUT);
  await addAnimations(OUT);
  console.log("wrote", OUT);
}

// pptxgenjs writes no transitions; give every slide a fade, placed where the schema wants it.
async function addFades(file) {
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const fade = '<p:transition spd="med"><p:fade/></p:transition>';
  for (const name of Object.keys(zip.files).filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
    let xml = await zip.file(name).async("string");
    if (xml.includes("<p:transition")) continue;
    xml = xml.includes("</p:clrMapOvr>") ? xml.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + fade)
      : xml.replace("</p:cSld>", "</p:cSld>" + fade);
    zip.file(name, xml);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

// Click-triggered fade-ins. Every element named "animN_…" appears on click N; the elements of
// one step appear together. Built as PowerPoint writes it: a main sequence of click groups.
async function addAnimations(file) {
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  for (const name of Object.keys(zip.files).filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
    let xml = await zip.file(name).async("string");
    const steps = new Map();
    const re = /<p:(sp|pic|graphicFrame)>\s*<p:nv\w+Pr>\s*<p:cNvPr id="(\d+)" name="anim(\d+)_/g;
    for (const m of xml.matchAll(re)) {
      const n = Number(m[3]);
      if (!steps.has(n)) steps.set(n, []);
      steps.get(n).push({ kind: m[1], id: m[2] });
    }
    if (!steps.size) continue;
    let id = 3;
    const effect = (sp, first) => `<p:par><p:cTn id="${id++}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="${first ? "clickEffect" : "withEffect"}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:set><p:cBhvr><p:cTn id="${id++}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${sp.id}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="${id++}" dur="500"/><p:tgtEl><p:spTgt spid="${sp.id}"/></p:tgtEl></p:cBhvr></p:animEffect></p:childTnLst></p:cTn></p:par>`;
    const groups = [...steps.keys()].sort((a, b) => a - b).map((n) => {
      const outer = id++;
      const inner = id++;
      const effects = steps.get(n).map((sp, i) => effect(sp, i === 0)).join("");
      return `<p:par><p:cTn id="${outer}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="${inner}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>${effects}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>`;
    }).join("");
    const bld = [...steps.values()].flat().map((sp) => sp.kind === "sp"
      ? `<p:bldP spid="${sp.id}" grpId="0" animBg="1"/>`
      : sp.kind === "graphicFrame" ? `<p:bldGraphic spid="${sp.id}" grpId="0"><p:bldAsOne/></p:bldGraphic>` : "").join("");
    const timing = `<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>${groups}</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>${bld ? `<p:bldLst>${bld}</p:bldLst>` : ""}</p:timing>`;
    xml = xml.replace("</p:transition>", "</p:transition>" + timing);
    zip.file(name, xml);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

build().catch((e) => {
  console.error(e);
  process.exit(1);
});
