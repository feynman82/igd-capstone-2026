// The 15-slide showcase deck: the whole capstone in one sitting.
//
//   SKILL=<path to the pptx skill> node showcase.js "../Project Parrot Showcase.pptx"
//
// The palette is the scarlet macaw's: scarlet, sunflower, macaw blue and jungle green on a deep
// night indigo. Backgrounds are glow gradients drawn here as SVG; every slide fades in.
// Every number on a slide is copied from a committed file, and the slide names that file.
"use strict";
const path = require("path");
const pptxgen = require("pptxgenjs");
const JSZip = require("jszip");
const fs = require("fs");
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
    dk1: "120E2A", // night indigo
    lt1: "FFFFFF",
    dk2: "4A4566", // muted indigo body text
    lt2: "F6F4FB",
    accent1: "E8402F", // scarlet
    accent2: "FFB627", // sunflower
    accent3: "1F8FFF", // macaw blue
    accent4: "12B886", // jungle green
    accent5: "E4E1F0", // hairline
    accent6: "2A2450", // dark card
    hlink: "1F8FFF",
    folHlink: "E8402F",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "PARROT: your family's paperwork, answered";
pres.author = "IGD ILP 2026, Group 1";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const MACAW = [C.accent1, C.accent2, C.accent3, C.accent4];

// ---------- backgrounds ----------
async function glow(base, blobs) {
  const g = blobs.map((b, i) => `<radialGradient id="g${i}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#${b.c}" stop-opacity="${b.o}"/>
      <stop offset="100%" stop-color="#${b.c}" stop-opacity="0"/></radialGradient>`).join("");
  const e = blobs.map((b, i) => `<ellipse cx="${b.x}" cy="${b.y}" rx="${b.r}" ry="${b.r * 0.8}" fill="url(#g${i})"/>`).join("");
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
    <defs>${g}</defs><rect width="1920" height="1080" fill="#${base}"/>${e}</svg>`;
  const buf = await sharp(Buffer.from(svg)).jpeg({ quality: 88 }).toBuffer();
  return "image/jpeg;base64," + buf.toString("base64");
}

// ---------- helpers ----------
async function icon(Comp, hex, px = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(Comp, { color: "#" + hex, size: px, strokeWidth: 2 }),
  );
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
const shadow = (dark) => ({ type: "outer", color: dark ? "000000" : "4A4566", blur: dark ? 18 : 14,
  offset: 4, angle: 90, opacity: dark ? 0.45 : 0.16 });

function card(slide, x, y, w, h, opts = {}) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: opts.r || 0.16, rotate: opts.rotate || 0,
    fill: { color: opts.fill || C.background1, transparency: opts.transparency || 0 },
    line: { color: opts.line || opts.fill || C.background1, width: opts.lineW || 0.75,
      transparency: opts.line ? 0 : opts.transparency || 0 },
    shadow: opts.noShadow ? undefined : shadow(opts.dark),
    objectName: opts.name || "card",
  });
}
function chip(slide, t, x, y, opts = {}) {
  const w = opts.w || Math.max(1.2, 0.085 * t.length + 0.35);
  slide.addText(t, {
    x, y, w, h: opts.h || 0.32, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.16,
    fill: { color: opts.fill || C.accent3 }, color: opts.color || C.background1,
    fontFace: opts.mono === false ? undefined : "Courier New", fontSize: opts.size || 10,
    bold: !!opts.bold, align: "center", valign: "middle", margin: 0, isTextBox: true,
    objectName: "chip",
  });
  return w;
}
function source(slide, t, dark) {
  slide.addText("source · " + t, {
    x: 6.6, y: 7.02, w: 5.4, h: 0.3, fontFace: "Courier New", fontSize: 9, align: "right",
    color: dark === "vivid" ? C.background1 : dark ? C.accent2 : C.accent3, margin: 0, isTextBox: true, objectName: "source",
  });
}
async function iconDisc(slide, Comp, x, y, d, fill, fg) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill },
    objectName: "icon disc" });
  const pad = d * 0.25;
  slide.addImage({ data: await icon(Comp, fg), x: x + pad, y: y + pad, w: d - 2 * pad,
    h: d - 2 * pad, objectName: "icon" });
}
function numDisc(slide, n, x, y, d, fill, fg) {
  slide.addText(String(n), { x, y, w: d, h: d, shape: pres.shapes.OVAL, fill: { color: fill },
    line: { color: C.background1, width: 2 }, color: fg || C.background1, bold: true,
    fontFace: "Arial", fontSize: Math.round(d * 30), align: "center", valign: "middle", margin: 0,
    isTextBox: true, objectName: "number disc" });
}
// A screenshot in a white device frame, optionally tilted.
function screenshot(slide, file, x, y, w, h, opts = {}) {
  const pad = opts.pad === undefined ? 0.1 : opts.pad;
  card(slide, x - pad, y - pad, w + 2 * pad, h + 2 * pad,
    { rotate: opts.rotate, dark: opts.dark, r: 0.12, name: "screen frame" });
  slide.addImage({ path: path.join(SHOTS, file), x, y, w, h, rotate: opts.rotate || 0,
    objectName: "screenshot " + file });
}
function text(slide, t, o) {
  slide.addText(t, { margin: 0, isTextBox: true, valign: "top", color: C.text2, fontSize: 15, ...o });
}
function bigStat(slide, value, label, x, y, w, o = {}) {
  text(slide, value, { x, y, w, h: o.h || 0.95, fontFace: "Arial", bold: true, fontSize: o.size || 54,
    color: o.color || C.accent1, valign: "bottom" });
  text(slide, label, { x, y: y + (o.h || 0.95) + 0.05, w, h: o.lh || 0.7, fontSize: o.lsize || 13,
    color: o.labelColor || C.text2 });
}

const sections = new Set();
function newSlide(masterName, sectionTitle) {
  if (!sections.has(sectionTitle)) {
    pres.addSection({ title: sectionTitle });
    sections.add(sectionTitle);
  }
  return pres.addSlide({ masterName, sectionTitle });
}
function heading(slide, kicker, title) {
  slide.addText(kicker.toUpperCase(), { placeholder: "kicker" });
  slide.addText(title, { placeholder: "title" });
}

async function build() {
  // ---------- layouts ----------
  const BG = {
    title: await glow(HEX.dk1, [
      { c: HEX.accent1, o: 0.75, x: 1550, y: 330, r: 760 },
      { c: HEX.accent3, o: 0.55, x: 180, y: 1050, r: 700 },
      { c: HEX.accent2, o: 0.35, x: 1100, y: 1080, r: 420 },
    ]),
    dark: await glow(HEX.dk1, [
      { c: HEX.accent1, o: 0.38, x: 1880, y: -60, r: 720 },
      { c: HEX.accent3, o: 0.33, x: -40, y: 1120, r: 760 },
    ]),
    light: await glow("FFFFFF", [
      { c: HEX.accent2, o: 0.22, x: 1900, y: -40, r: 620 },
      { c: HEX.accent3, o: 0.12, x: -60, y: 1120, r: 680 },
      { c: HEX.accent1, o: 0.1, x: 1900, y: 1100, r: 420 },
    ]),
    vivid: await glow(HEX.accent1, [
      { c: HEX.accent2, o: 0.85, x: 1700, y: 120, r: 820 },
      { c: "8E1B4E", o: 0.8, x: 60, y: 1100, r: 900 },
    ]),
  };
  pres.defineSlideMaster({
    title: "Title",
    background: { data: BG.title },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.35, w: 7.6, h: 2.6,
        fontSize: 50, bold: true, color: C.background1, valign: "top", align: "left", margin: 0 },
        text: "" } },
      { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 5.0, w: 7.2, h: 0.8,
        fontSize: 18, color: C.accent5, align: "left", margin: 0 }, text: "" } },
    ],
  });
  for (const [name, bg, dark] of [["Content", BG.light, false], ["Content Dark", BG.dark, true],
    ["Content Vivid", BG.vivid, true]]) {
    const vivid = name === "Content Vivid";
    pres.defineSlideMaster({
      title: name,
      background: { data: bg },
      margin: [0.5, 0.6, 0.6, 0.6],
      objects: [
        { placeholder: { options: { name: "kicker", type: "body", x: 0.6, y: 0.42, w: 9, h: 0.32,
          fontSize: 12, bold: true, charSpacing: 3, align: "left", margin: 0,
          color: vivid ? C.background1 : dark ? C.accent2 : C.accent1 }, text: "" } },
        { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.74, w: 12.1, h: 0.85,
          fontSize: 36, bold: true, color: dark ? C.background1 : C.text1, valign: "top",
          align: "left", margin: 0 }, text: "" } },
        { text: { text: "PARROT  ·  SMU IGD · AI in the Digital Economy  ·  2026", options: {
          x: 0.6, y: 7.02, w: 6, h: 0.3, fontSize: 10, margin: 0,
          color: dark ? C.accent5 : C.text2 } } },
      ],
      slideNumber: { x: 12.2, y: 7.02, w: 0.55, h: 0.3, fontSize: 10, align: "right",
        color: dark ? C.accent5 : C.text2 },
    });
  }

  // 1 · Title
  {
    const s = newSlide("Title", "Opening");
    s.addImage({ path: path.join(ASSETS, "parrot-icon.png"), x: 7.55, y: 0.9, w: 5.6, h: 5.0,
      objectName: "parrot mark" });
    s.addImage({ path: path.join(ASSETS, "parrot-logo.png"), x: 0.8, y: 0.7, w: 2.9, h: 0.88,
      objectName: "logo" });
    text(s, "IGD ILP 2026  ·  GROUP 1  ·  FINAL PRESENTATION", { x: 0.8, y: 1.9, w: 7, h: 0.3,
      fontSize: 12, bold: true, charSpacing: 3, color: C.accent2 });
    s.addText([
      { text: "Your family's paperwork, ", options: { breakLine: false } },
      { text: "answered.", options: { color: C.accent2 } },
      { text: " On your own machine." },
    ], { placeholder: "title" });
    s.addText("A local-first household AI that shows its page, and says so when it does not know.",
      { placeholder: "body" });
    let x = 0.8;
    const team = ["Christian", "Zee", "Desmond", "Siew", "Yew Mun"];
    for (let i = 0; i < team.length; i++) {
      const fill = [C.accent1, C.accent2, C.accent3, C.accent4, C.background1][i];
      x += chip(s, team[i], x, 6.05, { fill, color: i === 1 || i === 4 ? C.text1 : C.background1,
        w: 1.35, h: 0.38, size: 12, bold: true, mono: false }) + 0.14;
    }
    text(s, "SMU Industry Graduate Diploma · Integrated Learning Project · Sep to Nov 2026",
      { x: 0.8, y: 6.6, w: 8, h: 0.3, fontSize: 11, color: C.accent5 });
    s.addNotes("Where, exactly, is your car insurance policy right now? PARROT: photograph a document once, it files itself, and every answer comes with the page it came from. When it does not know, it says so. Nothing leaves the house.");
  }

  // 2 · Problem
  {
    const s = newSlide("Content", "The problem");
    heading(s, "The problem", "The family filing system is a drawer");
    const people = [
      [Fi.FiCalendar, "Sarah, 35", "Working mother, the household calendar",
        "Renewals and due dates live in six inboxes and a drawer.", C.accent1, HEX.accent1],
      [Fi.FiUsers, "Marcus, 39", "Sandwich generation, supports his parents",
        "Eleven policies, five people, and one question: are we covered?", C.accent3, HEX.accent3],
      [Fi.FiPercent, "Priya, 32", "Single professional, saves tax through SRS",
        "Miss the window and the relief is gone, silently.", C.accent4, HEX.accent4],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, name, who, pain, fill, hex] = people[i];
      const x = 0.6 + i * 4.1;
      card(s, x, 1.95, 3.8, 3.65, { fill });
      await iconDisc(s, ic, x + 0.35, 2.3, 0.85, C.background1, hex);
      text(s, name, { x: x + 0.35, y: 3.35, w: 3.1, h: 0.5, fontFace: "Arial", bold: true,
        fontSize: 26, color: C.background1 });
      text(s, who, { x: x + 0.35, y: 3.87, w: 3.1, h: 0.4, fontSize: 13, bold: true, color: C.background1 });
      text(s, pain, { x: x + 0.35, y: 4.4, w: 3.1, h: 1.0, fontSize: 17, color: C.background1 });
    }
    s.addText([
      { text: "They are not missing documents.  ", options: { bold: true, color: C.accent2 } },
      { text: "They are missing a way to ask the pile a question and trust the answer. A chatbot that invents a policy date is worse than none.",
        options: { color: C.background1 } },
    ], { x: 0.6, y: 5.85, w: 12.1, h: 0.9, fontSize: 16, margin: [0.15, 0.3, 0.15, 0.3],
      shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.16, fill: { color: C.text1 },
      valign: "middle", isTextBox: true, objectName: "banner" });
    source(s, "corpus/canon.md · proposal §2");
    s.addNotes("Three personas from the proposal. None of them is missing the documents; they are missing a trustworthy way to ask them a question.");
  }

  // 3 · Solution
  {
    const s = newSlide("Content Dark", "The product");
    heading(s, "The solution", "Photograph it. Ask it. It shows its page");
    const steps = [
      [Fi.FiCamera, "Capture", "Snap it to a Telegram chat or drop it in a folder. Docling reads it; typed fields are extracted.", HEX.accent1],
      [Fi.FiMessageSquare, "Ask", "Plain English. Every sentence carries its document and page; one click opens the original.", HEX.accent2],
      [Fi.FiSun, "Today", "It speaks first: what expires, what is due, what it could not read and wants you to check.", HEX.accent3],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, h, b, hex] = steps[i];
      const y = 1.95 + i * 1.45;
      await iconDisc(s, ic, 0.6, y, 0.95, hex, i === 1 ? HEX.dk1 : HEX.lt1);
      text(s, `0${i + 1}  ${h}`, { x: 1.8, y: y - 0.02, w: 5.2, h: 0.45, fontFace: "Arial", bold: true,
        fontSize: 22, color: C.background1 });
      text(s, b, { x: 1.8, y: y + 0.45, w: 5.2, h: 0.85, fontSize: 15, color: C.accent5 });
    }
    text(s, "When the documents don't say, PARROT says so. It doesn't guess.", {
      x: 0.6, y: 6.3, w: 7.0, h: 0.45, fontSize: 16, italic: true, bold: true, color: C.accent2 });
    screenshot(s, "03-capture.jpg", 7.7, 1.75, 2.45, 4.63, { rotate: -5, dark: true });
    screenshot(s, "final-ask.jpg", 10.15, 2.05, 2.55, 3.57, { rotate: 4, dark: true });
    chip(s, "b1-0001.pdf  p.1", 10.45, 6.0, { w: 2.0, fill: C.accent4, size: 11, h: 0.36 });
    source(s, "docs/report/deck-shots", true);
  }

  // 4 · Four screens
  {
    const s = newSlide("Content", "The product");
    heading(s, "The interface", "Four screens. It speaks first");
    const screens = [
      ["07-today.png", "Today", "What needs you now", C.accent1],
      ["07-ask.png", "Ask", "Every answer shows its page", C.accent2],
      ["07-vault.png", "Vault", "What it read, and what it couldn't", C.accent3],
      ["07-packs.png", "Packs", "Switch one off; its advice goes quiet", C.accent4],
    ];
    const w = 2.62;
    const h = w * 1255 / 935;
    for (let i = 0; i < 4; i++) {
      const [f, name, cap, col] = screens[i];
      const x = 0.95 + i * 3.08;
      screenshot(s, f, x, 1.95, w, h, { rotate: i % 2 ? 2.5 : -2.5 });
      chip(s, name, x + 0.12, 5.75, { w: 1.3, h: 0.4, fill: col, size: 14, bold: true, mono: false,
        color: i === 1 ? C.text1 : C.background1 });
      text(s, cap, { x: x + 0.12, y: 6.25, w: 2.6, h: 0.5, fontSize: 13, color: C.text2 });
    }
    source(s, "web/ · docs/report/deck-shots");
  }

  // 5 · Anatomy of an answer
  {
    const s = newSlide("Content", "The product");
    heading(s, "Anatomy of an answer", "Numbers come from Postgres, not the model");
    const sx = 0.75, sy = 1.85, sw = 3.6, sh = sw * 1121 / 800;
    screenshot(s, "final-ask.jpg", sx, sy, sw, sh);
    const at = (px, py) => [sx + px / 800 * sw, sy + py / 1121 * sh];
    const spots = [[505, 297], [540, 423], [715, 485], [740, 981]];
    const pts = [
      ["Every sentence cites its page", "Document and page on every claim. Fact rows cannot be written without them: both are NOT NULL."],
      ["Nothing left this computer", "Generation, embedding, reranking and even the evaluation judge run on the laptop."],
      ["It knows what it is not", "Not a licensed adviser, and it says so on every advice answer."],
      ["Only your documents", "Dates and amounts are read from typed columns; the model only phrases the sentence."],
    ];
    for (let i = 0; i < 4; i++) {
      const [px, py] = at(...spots[i]);
      numDisc(s, i + 1, px - 0.22, py - 0.22, 0.44, MACAW[i], i === 1 ? C.text1 : C.background1);
      const y = 1.95 + i * 1.22;
      card(s, 5.1, y, 7.6, 1.05);
      numDisc(s, i + 1, 5.3, y + 0.24, 0.56, MACAW[i], i === 1 ? C.text1 : C.background1);
      text(s, pts[i][0], { x: 6.1, y: y + 0.14, w: 6.4, h: 0.38, fontFace: "Arial", bold: true,
        fontSize: 17, color: C.text1 });
      text(s, pts[i][1], { x: 6.1, y: y + 0.52, w: 6.4, h: 0.48, fontSize: 13 });
    }
    source(s, "AGENTS.md · hard rules 2 and 3");
  }

  // 6 · Architecture
  {
    const s = newSlide("Content Dark", "The platform");
    heading(s, "Architecture", "Five layers, one laptop, one database");
    const rows = [
      ["Launch & UI", HEX.accent2, ["start_parrot.py launcher", "Next.js 15 screens", "FastAPI engine"]],
      ["Capture & ingestion", HEX.accent1, ["Folder watcher · Telegram", "Celery worker", "Docling pipeline", "Quarantine, vision 2nd pass"]],
      ["Answering", HEX.accent3, ["LangGraph QA graph", "Hybrid search + RRF", "bge-reranker-v2-m3", "Evidence gate"]],
      ["Runtime", HEX.accent4, ["Redis queue", "Ollama · SEA-LION 4B VL", "EmbeddingGemma-300M", "PostgreSQL 17 + pgvector"]],
      ["Records & knowledge", "C9B8FF", ["contracts.py", "Domain packs", "Capability modules", "Grounding corpus"]],
    ];
    for (let r = 0; r < rows.length; r++) {
      const [label, col, boxes] = rows[r];
      const y = 1.9 + r * 1.0;
      text(s, label.toUpperCase(), { x: 0.6, y, w: 2.4, h: 0.86, fontSize: 12, bold: true,
        charSpacing: 2, color: col, valign: "middle" });
      const bw = (12.73 - 3.1 - (boxes.length - 1) * 0.16) / boxes.length;
      for (let b = 0; b < boxes.length; b++) {
        s.addText(boxes[b], {
          x: 3.1 + b * (bw + 0.16), y, w: bw, h: 0.86, shape: pres.shapes.ROUNDED_RECTANGLE,
          rectRadius: 0.12, fill: { color: col, transparency: 72 }, line: { color: col, width: 1.5 },
          color: C.background1, bold: true, fontSize: 14, align: "center", valign: "middle",
          margin: 0.05, isTextBox: true, objectName: "arch box",
        });
      }
    }
    source(s, "gitdiagram · README stack table", true);
    s.addNotes("Launcher starts the engine, watcher and worker. Captured documents queue through Redis to the Docling pipeline; low-confidence pages go to quarantine. Questions run through the LangGraph graph: scoping, hybrid retrieval, reranker, then the evidence gate. Everything lands in one Postgres, and every model is open and local: SEA-LION 4B VL from AI Singapore for generation and vision, EmbeddingGemma for embeddings, bge for reranking. Tested on a 32 GB laptop with an RTX 4060.");
  }

  // 7 · Platform: two axes
  {
    const s = newSlide("Content", "The platform");
    heading(s, "The platform", "One engine. Two ways to grow");
    s.addText([
      { text: "THE CORE ENGINE", options: { fontSize: 12, bold: true, charSpacing: 3, color: C.accent2, breakLine: true } },
      { text: "File · Find · Check · Cite", options: { fontSize: 26, bold: true, fontFace: "Arial", color: C.background1, breakLine: true } },
      { text: "Retrieval, citation, abstention, the household", options: { fontSize: 13, color: C.accent5 } },
    ], { x: 4.42, y: 2.6, w: 4.5, h: 2.0, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.18,
      fill: { color: C.text1 }, align: "center", valign: "middle", margin: 0.1, isTextBox: true,
      shadow: shadow(), objectName: "engine" });
    const sides = [
      [0.6, Fi.FiZap, "Capability modules", "Reminder · Alert · Advice",
        "Read typed rows. Never see the interface. Tracker next.", C.accent3, HEX.accent3],
      [9.3, Fi.FiPackage, "Domain packs", "Tax and Reliefs · Insurance",
        "One YAML file of know-how. Nine more specified and tested.", C.accent1, HEX.accent1],
    ];
    for (const [x, ic, h, sub, b, fill, hex] of sides) {
      card(s, x, 1.95, 3.43, 3.4, { fill });
      await iconDisc(s, ic, x + 0.3, 2.25, 0.75, C.background1, hex);
      text(s, h, { x: x + 0.3, y: 3.15, w: 2.9, h: 0.45, fontFace: "Arial", bold: true,
        fontSize: 21, color: C.background1 });
      text(s, sub, { x: x + 0.3, y: 3.62, w: 2.9, h: 0.4, fontSize: 14, bold: true, color: C.background1 });
      text(s, b, { x: x + 0.3, y: 4.05, w: 2.9, h: 1.0, fontSize: 14, color: C.background1 });
    }
    s.addShape(pres.shapes.LINE, { x: 4.03, y: 3.6, w: 0.39, h: 0, line: { color: C.accent3, width: 3, endArrowType: "triangle" } });
    s.addShape(pres.shapes.LINE, { x: 8.92, y: 3.6, w: 0.38, h: 0, line: { color: C.accent1, width: 3, beginArrowType: "triangle" } });
    const stats = [["2", "packs built", C.accent1], ["9", "packs specified", C.accent3],
      ["3", "modules: Reminder, Alert, Advice", C.accent4], ["Literal[True]", "never_acts, enforced by type", C.accent2]];
    for (let i = 0; i < 4; i++) {
      text(s, stats[i][0], { x: 0.6 + i * 3.1, y: 5.6, w: 2.9, h: 0.65, fontFace: "Arial", bold: true,
        fontSize: i === 3 ? 26 : 40, color: stats[i][2], valign: "bottom" });
      text(s, stats[i][1], { x: 0.6 + i * 3.1, y: 6.3, w: 2.9, h: 0.35, fontSize: 13 });
    }
    source(s, "core/contracts.py · packs/catalogue.yaml");
  }

  // 8 · A pack at work
  {
    const s = newSlide("Content Dark", "The platform");
    heading(s, "A working domain pack", "Ask what's missing. Code does the sums");
    screenshot(s, "06-advice.png", 0.8, 2.0, 5.5, 4.74, { rotate: -2, dark: true });
    text(s, "MARCUS ASKS", { x: 7.0, y: 1.95, w: 5.7, h: 0.3, fontSize: 12, bold: true, charSpacing: 3, color: C.accent2 });
    text(s, "“Review my insurance coverage and tell me what is lacking.”",
      { x: 7.0, y: 2.3, w: 5.7, h: 0.8, fontSize: 17, italic: true, color: C.background1 });
    bigStat(s, "SGD 715k", "life cover short: 9 × SGD 112,800 income, against SGD 300,000 held",
      7.0, 3.3, 2.85, { size: 38, color: C.accent2, labelColor: C.accent5 });
    bigStat(s, "SGD 251k", "critical illness short: 4 × income, against SGD 200,000 held",
      9.9, 3.3, 2.85, { size: 38, color: C.accent3, labelColor: C.accent5 });
    text(s, "Income from his payslip, cover from his policies, the rule of thumb from MoneySense. Every input is cited. It names the gap, never a product.",
      { x: 7.0, y: 5.15, w: 5.7, h: 0.95, fontSize: 14, color: C.accent5 });
    chip(s, "consent recorded", 7.0, 6.3, { w: 1.9, fill: C.accent1, h: 0.36 });
    chip(s, "never_acts: true", 9.05, 6.3, { w: 1.9, fill: C.accent4, h: 0.36 });
    source(s, "packs/insurance_agent · Pitch Script §06", true);
  }

  // 9 · Corpus
  {
    const s = newSlide("Content", "The evidence");
    heading(s, "The corpus", "A synthetic family, written before any document");
    const iw = 5.5, ih = iw * 1536 / 2816;
    screenshot(s, "09-photo-doc.jpg", 0.85, 2.05, iw, ih, { rotate: -3, pad: 0.12 });
    text(s, "Every document is synthetic, authored against a register filled in first.",
      { x: 0.75, y: 5.25, w: 5.7, h: 0.35, fontSize: 13, italic: true });
    const fam = [["M", "Marcus"], ["R", "Rachel"], ["L", "Lucas"], ["AK", "Ah Kow"], ["ML", "Mei Ling"]];
    for (let i = 0; i < 5; i++) {
      const x = 0.75 + i * 1.15;
      const fill = [C.accent1, C.accent3, C.accent2, C.accent4, "8E1B4E"][i];
      s.addText(fam[i][0], { x, y: 5.75, w: 0.6, h: 0.6, shape: pres.shapes.OVAL, fill: { color: fill },
        line: { color: fill }, color: i === 2 ? C.text1 : C.background1, bold: true, fontSize: 14,
        align: "center", valign: "middle", margin: 0, isTextBox: true });
      text(s, fam[i][1], { x: x - 0.25, y: 6.4, w: 1.1, h: 0.3, fontSize: 11, align: "center" });
    }
    const tiles = [
      ["93", "documents in the Run 3 vault, 39 of them realistic noise", C.accent1],
      ["16", "document types, from payslips to policy schedules", C.accent3],
      ["118", "golden questions: 93 answerable, 25 hard negatives", C.accent4],
      ["15", "adversarial traps: injection, act-for-me, stale records", C.accent2],
    ];
    for (let i = 0; i < 4; i++) {
      const x = 7.0 + (i % 2) * 2.92;
      const y = 1.95 + Math.floor(i / 2) * 2.45;
      const fg = i === 3 ? C.text1 : C.background1;
      card(s, x, y, 2.75, 2.25, { fill: tiles[i][2] });
      text(s, tiles[i][0], { x: x + 0.25, y: y + 0.15, w: 2.3, h: 0.95, fontFace: "Arial", bold: true,
        fontSize: 54, color: fg, valign: "bottom" });
      text(s, tiles[i][1], { x: x + 0.25, y: y + 1.2, w: 2.3, h: 0.9, fontSize: 13, color: fg });
    }
    source(s, "corpus/canon.md · docs/report/05 §5.2");
  }

  // 10 · Thesis
  {
    const s = newSlide("Content Dark", "The evidence");
    heading(s, "How we judge it", "Judge it on whether it guesses");
    s.addChart(pres.charts.DOUGHNUT, [{ name: "Unsupported claims, Run 3",
      labels: ["Unanswerable, answered anyway", "Wrong value", "False “not on file”", "Supported"],
      values: [12, 8, 5, 93] }], {
      x: 0.5, y: 1.85, w: 3.9, h: 3.9, holeSize: 66, showValue: false, showPercent: false,
      showLegend: false, showLabel: false, dataBorder: { pt: 1, color: HEX.dk1 },
      chartColors: [HEX.accent1, HEX.accent2, HEX.accent3, HEX.accent6], objectName: "claims doughnut",
    });
    text(s, "25", { x: 1.45, y: 3.05, w: 2.0, h: 0.9, fontFace: "Arial", bold: true, fontSize: 54,
      color: C.background1, align: "center", valign: "middle" });
    text(s, "of 118 answers", { x: 1.45, y: 3.95, w: 2.0, h: 0.35, fontSize: 13, color: C.accent5, align: "center" });
    const parts = [["12", "unanswerable questions answered anyway", C.accent1],
      ["8", "wrong values", C.accent2], ["5", "false “not on file”", C.accent3],
      ["0", "forbidden strings on Set C", C.accent4]];
    for (let i = 0; i < 4; i++) {
      const y = 1.95 + i * 0.95;
      text(s, parts[i][0], { x: 4.55, y, w: 0.8, h: 0.75, fontFace: "Arial", bold: true, fontSize: 36,
        color: parts[i][2], valign: "middle", align: "right" });
      text(s, parts[i][1], { x: 5.5, y, w: 2.3, h: 0.75, fontSize: 14, color: C.background1, valign: "middle" });
    }
    text(s, "A confident, well-cited wrong answer is worse than none. So the first number we report is the unsupported claim. Run 3: 25 of 118; on 28 October, 21.",
      { x: 0.6, y: 5.95, w: 7.2, h: 0.85, fontSize: 15, color: C.accent5 });
    screenshot(s, "15-abstain.png", 8.35, 2.1, 4.3, 4.3 * 870 / 1080, { rotate: 3, dark: true });
    text(s, "What a good “no” looks like: nothing invented to fill the gap.",
      { x: 8.35, y: 5.95, w: 4.4, h: 0.6, fontSize: 14, italic: true, color: C.accent2 });
    source(s, "docs/report/05 §5.1 and §5.5", true);
  }

  // 11 · Scorecard
  {
    const s = newSlide("Content", "The evidence");
    heading(s, "The scorecard", "Five numbers, one per aim, scored by code");
    const tiles = [
      ["77/93", "right and cited", "Answer from the documents, with the page", C.accent4],
      ["21/118", "unsupported claims", "Do not guess", C.accent1],
      ["4/93", "over-cautious", "Answer when the evidence is there", C.accent3],
      ["0.961", "extraction F1", "File documents correctly", C.accent2],
      ["0/15", "Set C leaks", "The absolute line", C.text1],
    ];
    for (let i = 0; i < 5; i++) {
      const [v, l, aim, col] = tiles[i];
      const x = 0.6 + i * 2.47;
      const fg = i === 3 ? C.text1 : C.background1;
      card(s, x, 1.95, 2.27, 2.65, { fill: col });
      text(s, v, { x: x + 0.2, y: 2.1, w: 1.95, h: 0.9, fontFace: "Arial", bold: true, fontSize: 34,
        color: fg, valign: "bottom" });
      text(s, l, { x: x + 0.2, y: 3.08, w: 1.95, h: 0.35, fontSize: 15, bold: true, color: fg });
      text(s, aim, { x: x + 0.2, y: 3.5, w: 1.95, h: 0.9, fontSize: 12, color: fg });
    }
    const labels = ["Right and cited", "Unsupported claims", "Over-caution"];
    s.addChart(pres.charts.BAR, [
      { name: "Run 3 (19 Oct)", labels, values: [72, 25, 6] },
      { name: "On main (28 Oct)", labels, values: [77, 21, 4] },
    ], {
      x: 0.6, y: 4.8, w: 8.3, h: 2.05, barDir: "bar", barGapWidthPct: 50,
      chartColors: [HEX.accent5, HEX.accent1], showValue: true, dataLabelPosition: "outEnd",
      dataLabelFontSize: 11, dataLabelColor: HEX.dk2, dataLabelFontFace: "+mn-lt", dataLabelFontBold: true,
      catAxisLabelColor: HEX.dk2, catAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt",
      valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
      showLegend: true, legendPos: "r", legendFontSize: 11, legendColor: HEX.dk2, legendFontFace: "+mn-lt",
      objectName: "run 3 vs main",
    });
    text(s, "Same 93-document vault, same 118 questions. The fixes Run 3 found moved every headline the right way, and Set C never leaked.",
      { x: 9.2, y: 5.05, w: 3.55, h: 1.6, fontSize: 13, italic: true });
    source(s, "eval/results/2026-10-28-since-run3-on-main");
  }

  // 12 · Retrieval lesson
  {
    const s = newSlide("Content", "The evidence");
    heading(s, "What retrieval taught us", "Faithfulness is a property of the context window");
    const labels = ["Run 1 · 6 docs", "Rebaseline · 26", "Run 2 · hybrid + reranker", "Run 3 · 93 docs"];
    s.addChart(pres.charts.BAR, [
      { name: "Context recall", labels, values: [0.895, 0.821, 0.897, 0.848] },
      { name: "Context precision", labels, values: [0.868, 0.767, 0.854, 0.82] },
      { name: "Faithfulness", labels, values: [0.819, 0.81, 0.967, 0.892] },
    ], {
      x: 0.6, y: 1.9, w: 7.6, h: 4.9, barDir: "col", barGapWidthPct: 45,
      chartColors: [HEX.accent3, HEX.accent2, HEX.accent1],
      showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.00", dataLabelFontSize: 10,
      dataLabelColor: HEX.dk2, dataLabelFontFace: "+mn-lt",
      valAxisMinVal: 0.6, valAxisMaxVal: 1.0, valAxisHidden: true,
      valGridLine: { style: "none" }, catGridLine: { style: "none" },
      catAxisLabelColor: HEX.dk2, catAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt",
      showLegend: true, legendPos: "t", legendFontSize: 11, legendColor: HEX.dk2, legendFontFace: "+mn-lt",
      objectName: "retrieval diagnostics",
    });
    card(s, 8.55, 1.95, 4.2, 2.0, { fill: C.accent1 });
    text(s, "0.810 → 0.967", { x: 8.8, y: 2.1, w: 3.8, h: 0.8, fontFace: "Arial", bold: true,
      fontSize: 36, color: C.background1, valign: "bottom" });
    text(s, "faithfulness, once hybrid search and a cross-encoder put the answering page among the six passages read",
      { x: 8.8, y: 2.95, w: 3.75, h: 0.9, fontSize: 13, color: C.background1 });
    const pts = [
      ["A bigger corpus, no code change: recall fell 0.074, precision 0.101.", C.accent3],
      ["Dense search cannot find a policy by its printed number, so full text joins it.", C.accent2],
      ["By Run 3, 19 of 21 misses had the right page in hand.", C.accent4],
    ];
    for (let i = 0; i < 3; i++) {
      const y = 4.2 + i * 0.85;
      s.addShape(pres.shapes.OVAL, { x: 8.6, y: y + 0.08, w: 0.22, h: 0.22, fill: { color: pts[i][1] },
        line: { color: pts[i][1] } });
      text(s, pts[i][0], { x: 9.0, y, w: 3.75, h: 0.75, fontSize: 14 });
    }
    source(s, "docs/report/05 §5.4");
  }

  // 13 · Governance
  {
    const s = newSlide("Content Dark", "Trust and what next");
    heading(s, "Governance and assurance", "It advises. It never pays, books or files");
    text(s, "“Renew my insurance policy and pay the premium.”", { x: 0.75, y: 1.95, w: 5.6, h: 0.4,
      fontSize: 17, italic: true, color: C.accent2 });
    screenshot(s, "final-refusal-crop.jpg", 0.85, 2.6, 5.3, 1.99, { rotate: -2, dark: true });
    bigStat(s, "never_acts: true", "in every pack manifest, typed Literal[True] in core/contracts.py: a pack that sets anything else will not load",
      0.75, 4.95, 5.5, { size: 34, h: 0.7, color: C.accent4, labelColor: C.accent5 });
    const docs = [
      [Fi.FiLock, "PDPA", "Data inventory, consent and redaction, retention and erasure, breach procedure", HEX.accent1],
      [Fi.FiLayers, "ISO/IEC 22989 → 5338", "Every lifecycle stage mapped to a file in this repository", HEX.accent2],
      [Fi.FiFlag, "IMDA Model AI Governance", "The nine generative-AI dimensions, and an autonomy statement", HEX.accent3],
      [Fi.FiFileText, "Model card and terms", "What the model is for, where it fails, who it is not for", HEX.accent4],
    ];
    for (let i = 0; i < 4; i++) {
      const [ic, h, b, hex] = docs[i];
      const y = 1.95 + i * 1.2;
      card(s, 6.85, y, 5.9, 1.02, { fill: C.accent6, dark: true });
      await iconDisc(s, ic, 7.05, y + 0.18, 0.66, hex, i === 1 ? HEX.dk1 : HEX.lt1);
      text(s, h, { x: 7.95, y: y + 0.13, w: 4.65, h: 0.36, fontFace: "Arial", bold: true, fontSize: 16, color: C.background1 });
      text(s, b, { x: 7.95, y: y + 0.5, w: 4.65, h: 0.45, fontSize: 12, color: C.accent5 });
    }
    source(s, "docs/governance/", true);
  }

  // 14 · Roadmap
  {
    const s = newSlide("Content", "Trust and what next");
    heading(s, "Commercialisation", "Packs are the unit of sale");
    const stages = [
      ["Now", "Prototype", "Core, Insurance and Tax packs, Reminder and Alert", "Run 3 on real redacted documents", C.accent4],
      ["Next", "Household product", "Catalogue packs, bought one at a time", "A measured minimum hardware spec", C.accent3],
      ["Then", "Professional seat", "An insurance agent reviews a client's cover, with consent", "A position on the Financial Advisers Act", C.accent2],
      ["Later", "Pack marketplace", "Packs written by domain experts", "A published pack contract and scalable provenance review", C.accent1],
    ];
    for (let i = 0; i < 4; i++) {
      const [when, h, b, gate, col] = stages[i];
      const x = 0.6 + i * 3.1;
      const y = 3.35 - i * 0.45;
      const fg = i === 2 ? C.text1 : C.background1;
      card(s, x, y, 2.85, 5.85 - y, { fill: col });
      text(s, when.toUpperCase(), { x: x + 0.25, y: y + 0.2, w: 2.4, h: 0.3, fontSize: 12, bold: true,
        charSpacing: 3, color: fg });
      text(s, h, { x: x + 0.25, y: y + 0.55, w: 2.4, h: 0.42, fontFace: "Arial", bold: true, fontSize: 18, color: fg });
      text(s, b, { x: x + 0.25, y: y + 1.0, w: 2.4, h: 0.8, fontSize: 13, color: fg });
      text(s, "First: " + gate, { x: x + 0.25, y: 5.85 - 0.85, w: 2.4, h: 0.75, fontSize: 12, italic: true,
        color: fg, valign: "bottom" });
    }
    text(s, "Willingness to pay is a hypothesis, ordered by how countable the loss is: a missed SRS relief, a lapsed motor policy, a parent's hospital stay nobody knew was covered.",
      { x: 0.6, y: 6.1, w: 12.1, h: 0.7, fontSize: 14 });
    source(s, "docs/report/07-commercialisation-roadmap.md");
  }

  // 15 · Close
  {
    const s = newSlide("Content Vivid", "Trust and what next");
    heading(s, "Thank you", "When the documents don't say, PARROT says so");
    s.addShape(pres.shapes.OVAL, { x: 9.05, y: 1.75, w: 3.7, h: 3.7, fill: { color: C.background1 },
      line: { color: C.background1 }, shadow: shadow(true), objectName: "mark disc" });
    s.addImage({ path: path.join(ASSETS, "parrot-icon.png"), x: 9.45, y: 2.25, w: 2.9, h: 2.59,
      objectName: "parrot mark" });
    const next = [
      ["Prove it on real paper", "Close the synthetic-to-real gap: 14 of 40 holdout documents so far"],
      ["Turn the label check on", "ADR 0021: two fewer unsupported claims, no right answer lost"],
      ["Measure the minimum machine", "Fit the full workflow on an 8 GB GPU, then publish the spec"],
    ];
    for (let i = 0; i < 3; i++) {
      const y = 2.0 + i * 1.3;
      numDisc(s, i + 1, 0.6, y, 0.8, C.background1, C.accent1);
      text(s, next[i][0], { x: 1.65, y: y + 0.0, w: 7.0, h: 0.42, fontFace: "Arial", bold: true,
        fontSize: 21, color: C.background1 });
      text(s, next[i][1], { x: 1.65, y: y + 0.45, w: 7.0, h: 0.45, fontSize: 15, color: C.background1 });
    }
    let x = 0.6;
    for (const n of ["Christian", "Zee", "Desmond", "Siew", "Yew Mun"]) {
      x += chip(s, n, x, 6.2, { fill: C.background1, color: C.accent1, w: 1.35, h: 0.38, size: 12,
        bold: true, mono: false }) + 0.14;
    }
    text(s, "Questions?", { x: 9.0, y: 5.6, w: 3.8, h: 0.6, fontFace: "Arial", bold: true, fontSize: 30,
      color: C.background1, align: "center" });
    source(s, "docs/report/05 §5.5 · README.md", "vivid");
  }

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  await addFades(OUT);
  console.log("wrote", OUT);
}

// pptxgenjs writes no transitions; give every slide a fade, placed where the schema wants it.
async function addFades(file) {
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const fade = '<p:transition spd="med"><p:fade/></p:transition>';
  for (const name of Object.keys(zip.files).filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
    let xml = await zip.file(name).async("string");
    if (xml.includes("<p:transition")) continue;
    xml = xml.includes("</p:clrMapOvr>")
      ? xml.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + fade)
      : xml.replace("</p:cSld>", "</p:cSld>" + fade);
    zip.file(name, xml);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

build().catch((e) => {
  console.error(e);
  process.exit(1);
});
