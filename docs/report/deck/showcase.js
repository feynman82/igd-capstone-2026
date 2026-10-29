// The 15-slide showcase deck: the whole capstone in one sitting.
//
//   SKILL=<path to the pptx skill> node showcase.js "../Project Parrot Showcase.pptx"
//
// Every number on a slide is copied from a committed file, and the slide says which one in its
// copper "source" chip, the deck's own version of "every claim has a page".
"use strict";
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const Fi = require("react-icons/fi");
const { applyTheme } = require(path.join(process.env.SKILL, "scripts/apply_theme.js"));

const OUT = process.argv[2] || "../Project Parrot Showcase.pptx";
const SHOTS = path.join(__dirname, "../deck-shots");
const ASSETS = path.join(__dirname, "../../../assets");

const THEME = {
  name: "Parrot Showcase",
  headFontFace: "Arial",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F1612", // espresso, the dark slides
    lt1: "FFFFFF",
    dk2: "5E4C42", // muted brown body text
    lt2: "F7F1EA", // the product's own cream
    accent1: "B5562E", // copper, from the logo
    accent2: "2F7D6D", // teal, the citation chip in the app
    accent3: "E0A458", // amber
    accent4: "8C3B1F", // rust
    accent5: "E6D9CC", // sand, hairlines
    accent6: "33251F", // dark card
    hlink: "B5562E",
    folHlink: "8C3B1F",
  },
};
const HEX = THEME.colors;
const W = 13.333;
const H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "PARROT: your family's paperwork, answered";
pres.author = "IGD ILP 2026, Group 1";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

// ---------- layouts ----------
const footer = (dark) => [
  {
    text: {
      text: "PARROT  ·  SMU IGD · AI in the Digital Economy  ·  2026",
      options: {
        x: 0.6, y: 7.02, w: 7, h: 0.3, fontSize: 10, margin: 0,
        color: dark ? C.accent5 : C.text2,
      },
    },
  },
];
const slideNum = (dark) => ({
  x: 12.2, y: 7.02, w: 0.55, h: 0.3, fontSize: 10, align: "right",
  color: dark ? C.accent5 : C.text2,
});

pres.defineSlideMaster({
  title: "Title",
  background: { color: HEX.dk1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.55, w: 8.0, h: 2.1,
      fontSize: 42, bold: true, align: "left", color: C.background1, valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.85, w: 7.6, h: 0.8,
      fontSize: 18, align: "left", color: C.accent3, margin: 0 }, text: "" } },
  ],
});
for (const [name, dark] of [["Content", false], ["Content Dark", true]]) {
  pres.defineSlideMaster({
    title: name,
    background: { color: dark ? HEX.dk1 : HEX.lt2 },
    margin: [0.5, 0.6, 0.6, 0.6],
    objects: [
      { placeholder: { options: { name: "kicker", type: "body", x: 0.6, y: 0.42, w: 9, h: 0.32,
        fontSize: 12, bold: true, charSpacing: 3, color: dark ? C.accent3 : C.accent1, margin: 0,
        align: "left" },
        text: "" } },
      { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.74, w: 12.1, h: 0.85,
        fontSize: 34, bold: true, color: dark ? C.background1 : C.text1, valign: "top", align: "left",
        margin: 0 }, text: "" } },
      ...footer(dark),
    ],
    slideNumber: slideNum(dark),
  });
}

// ---------- helpers ----------
async function icon(Comp, hex, px = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(Comp, { color: "#" + hex, size: px, strokeWidth: 2 }),
  );
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
const shadow = () => ({ type: "outer", color: "5E4C42", blur: 12, offset: 3, angle: 90, opacity: 0.18 });

function card(slide, x, y, w, h, opts = {}) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.14,
    fill: { color: opts.fill || C.background1 },
    line: { color: opts.line || opts.fill || C.background1, width: 0.75 },
    shadow: opts.noShadow ? undefined : shadow(),
    objectName: opts.name || "card",
  });
}
// The motif: a pill like the app's citation chip.
function chip(slide, text, x, y, opts = {}) {
  const w = opts.w || Math.max(1.2, 0.085 * text.length + 0.35);
  slide.addText(text, {
    x, y, w, h: 0.3, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.15,
    fill: { color: opts.fill || C.accent2 }, color: opts.color || C.background1,
    fontFace: "Courier New", fontSize: 10, align: "center", valign: "middle", margin: 0,
    isTextBox: true, objectName: "chip",
  });
  return w;
}
function source(slide, text, dark) {
  slide.addText("source · " + text, {
    x: 7.6, y: 7.0, w: 4.4, h: 0.32, fontFace: "Courier New", fontSize: 9, align: "right",
    color: dark ? C.accent3 : C.accent1, margin: 0, isTextBox: true, objectName: "source",
  });
}
async function iconDisc(slide, Comp, x, y, d, fill, fg) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill },
    objectName: "icon disc" });
  const pad = d * 0.26;
  slide.addImage({ data: await icon(Comp, fg), x: x + pad, y: y + pad, w: d - 2 * pad,
    h: d - 2 * pad, objectName: "icon" });
}
function screenshot(slide, file, x, y, w, h) {
  card(slide, x - 0.1, y - 0.1, w + 0.2, h + 0.2, { name: "screen frame" });
  slide.addImage({ path: path.join(SHOTS, file), x, y, w, h, objectName: "screenshot " + file });
}
function text(slide, t, o) {
  slide.addText(t, { margin: 0, isTextBox: true, valign: "top", color: C.text2, fontSize: 15, ...o });
}
function bigStat(slide, value, label, x, y, w, o = {}) {
  text(slide, value, { x, y, w, h: 0.95, fontFace: "Arial", bold: true, fontSize: o.size || 54,
    color: o.color || C.accent1, valign: "bottom" });
  text(slide, label, { x, y: y + 1.0, w, h: 0.7, fontSize: 13, color: o.labelColor || C.text2 });
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

// ---------- slides ----------
async function build() {
  // 1 · Title
  {
    const s = newSlide("Title", "Opening");
    s.addImage({ path: path.join(ASSETS, "parrot-icon.png"), x: 8.9, y: 1.4, w: 4.0, h: 3.57,
      transparency: 8, objectName: "parrot mark" });
    s.addImage({ path: path.join(ASSETS, "parrot-logo.png"), x: 0.8, y: 0.9, w: 3.6, h: 1.09,
      objectName: "logo" });
    s.addText("Your family's paperwork, answered. On your own machine.", { placeholder: "title" });
    s.addText("A local-first household RAG platform that shows its page, and says so when it does not know.",
      { placeholder: "body" });
    let x = 0.8;
    for (const n of ["Christian", "Zee", "Desmond", "Siew", "Yew Mun"]) {
      x += chip(s, n, x, 6.15, { fill: C.accent6, color: C.accent5, w: 1.35 }) + 0.15;
    }
    text(s, "SMU Industry Graduate Diploma · Integrated Learning Project · Sep to Nov 2026",
      { x: 0.8, y: 6.65, w: 9, h: 0.3, fontSize: 11, color: C.accent5 });
    s.addNotes("Where, exactly, is your car insurance policy right now? PARROT: photograph a document once, it files itself, and every answer comes with the page it came from. When it does not know, it says so. Nothing leaves the house.");
  }

  // 2 · Problem
  {
    const s = newSlide("Content", "The problem");
    heading(s, "The problem", "The family filing system is a drawer");
    const people = [
      [Fi.FiCalendar, "Sarah, 35", "Working mother, the household calendar",
        "Renewals and due dates live in six inboxes and a drawer."],
      [Fi.FiUsers, "Marcus, 39", "Sandwich generation, supports his parents",
        "Eleven policies, five people, and one question: are we covered?"],
      [Fi.FiPercent, "Priya, 32", "Single professional, saves tax through SRS",
        "Miss the window and the relief is gone, silently."],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, name, who, pain] = people[i];
      const x = 0.6 + i * 4.1;
      card(s, x, 2.0, 3.8, 3.55);
      await iconDisc(s, ic, x + 0.35, 2.35, 0.8, C.accent1, HEX.lt1);
      text(s, name, { x: x + 0.35, y: 3.35, w: 3.1, h: 0.45, fontFace: "Arial", bold: true,
        fontSize: 22, color: C.text1 });
      text(s, who, { x: x + 0.35, y: 3.82, w: 3.1, h: 0.5, fontSize: 13, color: C.accent1 });
      text(s, pain, { x: x + 0.35, y: 4.4, w: 3.1, h: 0.95, fontSize: 16, color: C.text2 });
    }
    s.addText([
      { text: "They are not missing documents. ", options: { bold: true, color: C.text1 } },
      { text: "They are missing a way to ask the pile a question and trust the answer. A chatbot that invents a policy date is worse than none.",
        options: { color: C.text2 } },
    ], { x: 0.6, y: 5.9, w: 12.1, h: 0.8, fontSize: 17, margin: 0, isTextBox: true });
    source(s, "corpus/canon.md · proposal §2");
    s.addNotes("Three personas from the proposal. None of them is missing the documents; they are missing a trustworthy way to ask them a question.");
  }

  // 3 · Solution
  {
    const s = newSlide("Content", "The product");
    heading(s, "The solution", "Photograph it. Ask it. It shows its page");
    const steps = [
      [Fi.FiCamera, "01  Capture", "Snap it to a Telegram chat or drop it in a folder. Docling reads it; the model extracts typed fields."],
      [Fi.FiMessageSquare, "02  Ask", "Plain English. Every sentence carries its document and page; one click opens the original."],
      [Fi.FiSun, "03  Today", "It speaks first: what expires, what is due, what it could not read and wants you to check."],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, h, b] = steps[i];
      const y = 1.95 + i * 1.5;
      await iconDisc(s, ic, 0.6, y, 0.85, C.accent2, HEX.lt1);
      text(s, h, { x: 1.7, y: y - 0.02, w: 5.6, h: 0.42, fontFace: "Arial", bold: true,
        fontSize: 20, color: C.text1 });
      text(s, b, { x: 1.7, y: y + 0.43, w: 5.6, h: 0.85, fontSize: 15 });
    }
    s.addText("When the documents don't say, PARROT says so. It doesn't guess.", {
      x: 0.6, y: 6.25, w: 6.8, h: 0.5, fontSize: 17, italic: true, bold: true, color: C.accent1,
      margin: 0, isTextBox: true });
    screenshot(s, "03-capture.jpg", 8.0, 1.85, 2.31, 4.36);
    screenshot(s, "final-ask.jpg", 10.55, 1.85, 2.18, 3.05);
    chip(s, "b1-0001.pdf p.1", 10.65, 5.15, { w: 1.95 });
    text(s, "Real replies from the running app", { x: 10.55, y: 5.55, w: 2.2, h: 0.6, fontSize: 11 });
    source(s, "docs/report/deck-shots");
  }

  // 4 · Anatomy of an answer
  {
    const s = newSlide("Content", "The product");
    heading(s, "Anatomy of an answer", "Numbers come from Postgres, never from the model");
    screenshot(s, "final-ask.jpg", 0.75, 1.9, 3.55, 4.97);
    const pts = [
      [Fi.FiDatabase, "Typed facts, not generated ones",
        "Dates, amounts and policy numbers are read from typed columns. The model only phrases the sentence around them."],
      [Fi.FiBookmark, "Every fact row cites its source",
        "document_id and page are NOT NULL. No code path writes a fact without provenance."],
      [Fi.FiShield, "No claim without a citation",
        "The answer node refuses to emit a factual sentence with no supporting chunk attached."],
      [Fi.FiHome, "Nothing left this computer",
        "Generation, embedding, reranking and even the evaluation judge run on the laptop."],
    ];
    for (let i = 0; i < 4; i++) {
      const [ic, h, b] = pts[i];
      const x = 4.95 + (i % 2) * 4.0;
      const y = 1.95 + Math.floor(i / 2) * 2.5;
      card(s, x, y, 3.75, 2.2);
      await iconDisc(s, ic, x + 0.3, y + 0.3, 0.62, C.accent1, HEX.lt1);
      text(s, h, { x: x + 1.08, y: y + 0.32, w: 2.45, h: 0.62, fontFace: "Arial", bold: true,
        fontSize: 15, color: C.text1, valign: "middle" });
      text(s, b, { x: x + 0.3, y: y + 1.07, w: 3.2, h: 1.0, fontSize: 13 });
    }
    source(s, "AGENTS.md · hard rules 2 and 3");
  }

  // 5 · Architecture
  {
    const s = newSlide("Content Dark", "The platform");
    heading(s, "Architecture", "Five layers, one laptop, one database");
    const rows = [
      ["Launch & UI", C.accent3, ["start_parrot.py launcher", "Next.js 15 screens", "FastAPI engine"]],
      ["Capture & ingestion", C.accent1, ["Folder watcher · Telegram", "Celery worker", "Docling pipeline", "Quarantine, vision 2nd pass"]],
      ["Answering", C.accent2, ["LangGraph QA graph", "Hybrid retrieval + RRF", "bge reranker", "Evidence gate"]],
      ["Runtime services", C.accent5, ["Redis queue", "Ollama · SEA-LION 4B VL", "PostgreSQL 17 + pgvector"]],
      ["Records & knowledge", C.accent3, ["contracts.py", "Domain packs", "Capability modules", "Grounding corpus"]],
    ];
    const top = 1.9;
    const rh = 0.86;
    for (let r = 0; r < rows.length; r++) {
      const [label, col, boxes] = rows[r];
      const y = top + r * (rh + 0.14);
      text(s, label.toUpperCase(), { x: 0.6, y, w: 2.4, h: rh, fontSize: 12, bold: true,
        charSpacing: 2, color: col, valign: "middle" });
      const bw = (12.73 - 3.1 - (boxes.length - 1) * 0.16) / boxes.length;
      for (let b = 0; b < boxes.length; b++) {
        s.addText(boxes[b], {
          x: 3.1 + b * (bw + 0.16), y, w: bw, h: rh, shape: pres.shapes.ROUNDED_RECTANGLE,
          rectRadius: 0.1, fill: { color: C.accent6 }, line: { color: col, width: 1.25 },
          color: C.background1, fontSize: 14, align: "center", valign: "middle", margin: 0.05,
          isTextBox: true, objectName: "arch box",
        });
      }
    }
    source(s, "gitdiagram · README stack table", true);
    s.addNotes("Launcher starts the engine, watcher and worker. Captured documents queue through Redis to the Docling pipeline; low-confidence pages go to quarantine. Questions run through the LangGraph graph: scoping, hybrid retrieval, reranker, then the evidence gate. Everything lands in one Postgres.");
  }

  // 6 · Platform: two axes
  {
    const s = newSlide("Content", "The platform");
    heading(s, "The platform", "One engine. Two ways to grow");
    // Engine in the middle
    s.addText([
      { text: "THE CORE ENGINE", options: { fontSize: 12, bold: true, charSpacing: 3, color: C.accent3, breakLine: true } },
      { text: "File · Find · Check · Cite", options: { fontSize: 24, bold: true, fontFace: "Arial", color: C.background1, breakLine: true } },
      { text: "Retrieval, citation, abstention, the household", options: { fontSize: 13, color: C.accent5 } },
    ], { x: 4.42, y: 2.75, w: 4.5, h: 1.9, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.16,
      fill: { color: C.text1 }, align: "center", valign: "middle", margin: 0.1, isTextBox: true,
      objectName: "engine" });
    const sides = [
      [0.6, Fi.FiZap, "Capability modules", "Reminder · Alert · Advice",
        "Read typed rows. Never see the interface. Tracker next.", C.accent2],
      [9.3, Fi.FiPackage, "Domain packs", "Tax and Reliefs · Insurance",
        "One YAML file of know-how. Nine more specified and tested.", C.accent1],
    ];
    for (const [x, ic, h, sub, b, col] of sides) {
      card(s, x, 2.0, 3.43, 3.45);
      await iconDisc(s, ic, x + 0.3, 2.3, 0.72, col, HEX.lt1);
      text(s, h, { x: x + 0.3, y: 3.15, w: 2.9, h: 0.42, fontFace: "Arial", bold: true,
        fontSize: 19, color: C.text1 });
      text(s, sub, { x: x + 0.3, y: 3.6, w: 2.9, h: 0.4, fontSize: 14, bold: true, color: col });
      text(s, b, { x: x + 0.3, y: 4.05, w: 2.9, h: 1.0, fontSize: 14 });
    }
    s.addShape(pres.shapes.LINE, { x: 4.03, y: 3.7, w: 0.39, h: 0, line: { color: C.accent2, width: 2.5, endArrowType: "triangle" } });
    s.addShape(pres.shapes.LINE, { x: 8.92, y: 3.7, w: 0.38, h: 0, line: { color: C.accent1, width: 2.5, beginArrowType: "triangle" } });
    const stats = [["2", "packs built"], ["9", "packs specified"], ["2+1", "modules + advice"], ["Literal[True]", "never_acts, enforced by type"]];
    for (let i = 0; i < 4; i++) {
      text(s, stats[i][0], { x: 0.6 + i * 3.1, y: 5.75, w: 2.9, h: 0.55, fontFace: "Arial", bold: true,
        fontSize: i === 3 ? 22 : 30, color: C.accent1, valign: "bottom" });
      text(s, stats[i][1], { x: 0.6 + i * 3.1, y: 6.35, w: 2.9, h: 0.35, fontSize: 13 });
    }
    source(s, "core/contracts.py · packs/catalogue.yaml");
  }

  // 7 · A pack at work
  {
    const s = newSlide("Content", "The platform");
    heading(s, "A working domain pack", "Ask what's missing. Code does the sums");
    screenshot(s, "06-advice.png", 0.75, 1.95, 5.6, 4.82);
    text(s, "Marcus asks", { x: 7.0, y: 1.95, w: 5.7, h: 0.35, fontSize: 13, bold: true, color: C.accent1 });
    text(s, "“Review my insurance coverage and tell me what is lacking.”",
      { x: 7.0, y: 2.3, w: 5.7, h: 0.8, fontSize: 18, italic: true, color: C.text1 });
    bigStat(s, "SGD 715k", "life cover short: 9 × SGD 112,800 income, against SGD 300,000 held", 7.0, 3.2, 2.8, { size: 40 });
    bigStat(s, "SGD 251k", "critical illness short: 4 × income, against SGD 200,000 held", 9.9, 3.2, 2.8,
      { color: C.accent2, size: 40 });
    text(s, "Income from his payslip, cover from his policies, the rule of thumb from MoneySense. Every input is cited. It names the gap, never a product, and says it is not a licensed adviser.",
      { x: 7.0, y: 5.15, w: 5.7, h: 1.2, fontSize: 14 });
    chip(s, "consent recorded", 7.0, 6.45, { w: 1.85, fill: C.accent1 });
    chip(s, "never_acts: true", 9.0, 6.45, { w: 1.85 });
    source(s, "packs/insurance_agent · Pitch Script §06");
  }

  // 8 · Stack
  {
    const s = newSlide("Content", "The platform");
    heading(s, "The stack", "Open models, all local, all on consumer hardware");
    const tiles = [
      [Fi.FiDatabase, "Postgres 17 + pgvector", "One database: chunks, facts, obligations, state"],
      [Fi.FiSearch, "Hybrid retrieval", "HNSW + full text, reciprocal rank fusion k = 60"],
      [Fi.FiFilter, "bge-reranker-v2-m3", "Keeps 6 of 40 candidates (ADR 0018)"],
      [Fi.FiCpu, "EmbeddingGemma-300M", "768-dimension embeddings via Ollama"],
      [Fi.FiGlobe, "Qwen-SEA-LION-v4-4B-VL", "AI Singapore, MIT, English + 7 SEA languages"],
      [Fi.FiGitBranch, "LangGraph", "Router, scoping, grounding gate, answer node"],
      [Fi.FiFileText, "Docling", "CPU parsing; vision second pass on quarantine"],
      [Fi.FiCheckCircle, "Ragas, local judge", "No evaluation question leaves the machine"],
    ];
    for (let i = 0; i < 8; i++) {
      const [ic, h, b] = tiles[i];
      const x = 0.6 + (i % 4) * 3.07;
      const y = 1.95 + Math.floor(i / 4) * 2.3;
      card(s, x, y, 2.85, 2.05);
      await iconDisc(s, ic, x + 0.25, y + 0.25, 0.6, i % 2 ? C.accent2 : C.accent1, HEX.lt1);
      text(s, h, { x: x + 0.25, y: y + 0.98, w: 2.4, h: 0.4, fontFace: "Arial", bold: true,
        fontSize: 13, color: C.text1 });
      text(s, b, { x: x + 0.25, y: y + 1.38, w: 2.4, h: 0.6, fontSize: 12 });
    }
    text(s, "Tested on a 32 GB laptop with an RTX 4060. Next.js 15, Tailwind and shadcn/ui on the front.",
      { x: 0.6, y: 6.55, w: 9, h: 0.35, fontSize: 13, italic: true });
    source(s, "README.md · docs/RUNNING.md");
  }

  // 9 · Corpus
  {
    const s = newSlide("Content", "The evidence");
    heading(s, "The corpus", "A synthetic family, written before any document");
    const fam = [
      ["Marcus", "owner, IT manager", C.accent1], ["Rachel", "wife, physiotherapist", C.accent1],
      ["Lucas", "son, 2019", C.accent2], ["Lim Ah Kow", "father, retiree", C.accent4],
      ["Tan Mei Ling", "mother, retiree", C.accent4],
    ];
    card(s, 0.6, 1.95, 6.2, 4.75);
    text(s, "THE LIM HOUSEHOLD, TAMPINES", { x: 0.95, y: 2.2, w: 5.5, h: 0.3, fontSize: 12, bold: true,
      charSpacing: 2, color: C.accent1 });
    for (let i = 0; i < 5; i++) {
      const [n, r, col] = fam[i];
      const y = 2.7 + i * 0.75;
      s.addShape(pres.shapes.OVAL, { x: 0.95, y, w: 0.55, h: 0.55, fill: { color: col }, line: { color: col } });
      text(s, n.split(" ").map((p) => p[0]).join("").slice(0, 2), { x: 0.95, y, w: 0.55, h: 0.55,
        fontSize: 13, bold: true, color: C.background1, align: "center", valign: "middle" });
      text(s, n, { x: 1.7, y: y - 0.02, w: 2.2, h: 0.3, fontSize: 15, bold: true, color: C.text1 });
      text(s, r, { x: 1.7, y: y + 0.27, w: 2.6, h: 0.28, fontSize: 12 });
    }
    text(s, "Three surnames, one household: parent relief, elderly hospital cover and a child's policy in one register.",
      { x: 4.3, y: 2.75, w: 2.25, h: 2.4, fontSize: 13, italic: true, color: C.accent1 });
    bigStat(s, "93", "documents in the Run 3 vault, 39 of them unregistered statements kept as realistic noise", 7.3, 1.85, 2.6);
    bigStat(s, "16", "document types, from payslips to policy schedules", 10.2, 1.85, 2.5, { color: C.accent2 });
    bigStat(s, "118", "golden questions: 93 answerable, 25 hard negatives", 7.3, 3.85, 2.6);
    bigStat(s, "15", "adversarial traps: injection, act-for-me, stale and absent records", 10.2, 3.85, 2.5, { color: C.accent2 });
    text(s, "Register first: the ground-truth spreadsheet is filled before a document is generated, so every question is graded by code.",
      { x: 7.3, y: 5.9, w: 5.45, h: 0.8, fontSize: 13 });
    source(s, "corpus/canon.md · §5.2");
  }

  // 10 · Thesis
  {
    const s = newSlide("Content Dark", "The evidence");
    heading(s, "How we judge it", "Judge it on whether it guesses");
    text(s, "A confident, well-cited, wrong answer about an insurance policy is worse than no answer. So the first number we report is the unsupported claim: a value the page does not print, a false “not on file”, or an answer to a question nothing on file can answer.",
      { x: 0.6, y: 2.0, w: 6.0, h: 2.6, fontSize: 18, color: C.accent5 });
    const parts = [["12", "unanswerable questions answered anyway"], ["8", "wrong values"], ["5", "false “not on file”"], ["0", "forbidden strings on Set C"]];
    for (let i = 0; i < 4; i++) {
      const y = 1.95 + i * 1.05;
      text(s, parts[i][0], { x: 7.3, y, w: 1.2, h: 0.85, fontFace: "Arial", bold: true, fontSize: 44,
        color: i === 3 ? C.accent2 : C.accent3, valign: "middle", align: "right" });
      text(s, parts[i][1], { x: 8.75, y, w: 4.0, h: 0.85, fontSize: 16, color: C.background1, valign: "middle" });
    }
    s.addText([
      { text: "25 of 118 ", options: { bold: true, color: C.accent3, fontSize: 28, fontFace: "Arial" } },
      { text: "unsupported claims in Run 3, falling to 21 on 28 October with the fixes it found.", options: { color: C.background1, fontSize: 16 } },
    ], { x: 0.6, y: 5.6, w: 12.1, h: 0.8, margin: 0, isTextBox: true, valign: "middle" });
    source(s, "docs/report/05 §5.1 and §5.5", true);
  }

  // 11 · Scorecard
  {
    const s = newSlide("Content", "The evidence");
    heading(s, "The scorecard", "Five numbers, one per aim, scored by code");
    const tiles = [
      ["77/93", "right and cited", "Answer from the documents, with the page", C.accent2],
      ["21/118", "unsupported claims", "Do not guess", C.accent1],
      ["4/93", "over-cautious", "Answer when the evidence is there", C.accent2],
      ["0.961", "extraction F1", "File documents correctly", C.accent2],
      ["0/15", "Set C leaks", "The absolute line", C.accent1],
    ];
    for (let i = 0; i < 5; i++) {
      const [v, l, aim, col] = tiles[i];
      const x = 0.6 + i * 2.47;
      card(s, x, 1.95, 2.27, 2.6);
      text(s, v, { x: x + 0.2, y: 2.15, w: 1.95, h: 0.85, fontFace: "Arial", bold: true, fontSize: 32,
        color: col, valign: "bottom" });
      text(s, l, { x: x + 0.2, y: 3.08, w: 1.95, h: 0.35, fontSize: 15, bold: true, color: C.text1 });
      text(s, aim, { x: x + 0.2, y: 3.5, w: 1.95, h: 0.9, fontSize: 12 });
    }
    s.addChart(pres.charts.BAR, [
      { name: "Run 3 (19 Oct)", labels: ["Right and cited", "Unsupported claims", "Over-caution"], values: [72, 25, 6] },
      { name: "On main (28 Oct)", labels: ["Right and cited", "Unsupported claims", "Over-caution"], values: [77, 21, 4] },
    ], {
      x: 0.6, y: 4.8, w: 8.3, h: 2.05, barDir: "bar", barGapWidthPct: 60,
      chartColors: [HEX.accent5, HEX.accent1], showValue: true, dataLabelPosition: "outEnd",
      dataLabelFontSize: 11, dataLabelColor: HEX.dk2, dataLabelFontFace: "+mn-lt",
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
      x: 0.6, y: 1.9, w: 7.6, h: 4.9, barDir: "col", barGapWidthPct: 55,
      chartColors: [HEX.accent5, HEX.accent3, HEX.accent1],
      showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.00", dataLabelFontSize: 10,
      dataLabelColor: HEX.dk2, dataLabelFontFace: "+mn-lt",
      valAxisMinVal: 0.6, valAxisMaxVal: 1.0, valAxisHidden: true,
      valGridLine: { style: "none" }, catGridLine: { style: "none" },
      catAxisLabelColor: HEX.dk2, catAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt",
      showLegend: true, legendPos: "t", legendFontSize: 11, legendColor: HEX.dk2, legendFontFace: "+mn-lt",
      objectName: "retrieval diagnostics",
    });
    bigStat(s, "0.810 → 0.967", "faithfulness, once hybrid search and a cross-encoder put the answering page among the six passages read",
      8.65, 1.85, 4.1, { size: 36 });
    const pts = [
      "A bigger corpus, no code change: recall fell 0.074, precision 0.101.",
      "Dense search cannot find a policy by its printed number, so full text joins it.",
      "By Run 3, 19 of 21 misses had the right page in hand.",
    ];
    s.addText(pts.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < pts.length - 1 } })),
      { x: 8.65, y: 3.95, w: 4.1, h: 2.8, fontSize: 14, color: C.text2, paraSpaceAfter: 8, margin: 0,
        valign: "top", isTextBox: true });
    source(s, "docs/report/05 §5.4");
  }

  // 13 · Governance
  {
    const s = newSlide("Content", "Trust and what next");
    heading(s, "Governance and assurance", "It advises. It never pays, books or files");
    text(s, "\u201CPay my renewal for me.\u201D", { x: 0.75, y: 1.95, w: 5.3, h: 0.4, fontSize: 18, italic: true, color: C.text1 });
    screenshot(s, "final-refusal-crop.jpg", 0.75, 2.55, 5.3, 1.99);
    bigStat(s, "never_acts: true", "in every pack manifest, typed Literal[True] in core/contracts.py: a pack that sets anything else will not load", 0.75, 4.85, 5.3, { size: 34, color: C.accent2 });
    const docs = [
      [Fi.FiLock, "PDPA", "Data inventory, consent and redaction, retention and erasure, breach procedure"],
      [Fi.FiLayers, "ISO/IEC 22989 → 5338", "Every lifecycle stage mapped to a file in this repository"],
      [Fi.FiFlag, "IMDA Model AI Governance", "The nine generative-AI dimensions, and an autonomy statement"],
      [Fi.FiFileText, "Model card and terms", "What the model is for, where it fails, who it is not for"],
    ];
    for (let i = 0; i < 4; i++) {
      const [ic, h, b] = docs[i];
      const y = 1.95 + i * 1.2;
      await iconDisc(s, ic, 6.75, y + 0.05, 0.7, C.accent2, HEX.lt1);
      text(s, h, { x: 7.7, y, w: 5.05, h: 0.38, fontFace: "Arial", bold: true, fontSize: 17, color: C.text1 });
      text(s, b, { x: 7.7, y: y + 0.4, w: 5.05, h: 0.6, fontSize: 13 });
    }
    source(s, "docs/governance/");
  }

  // 14 · Roadmap
  {
    const s = newSlide("Content", "Trust and what next");
    heading(s, "Commercialisation", "Packs are the unit of sale");
    const stages = [
      ["Now", "Prototype", "Core, Insurance and Tax packs, Reminder and Alert", "Run 3 on real redacted documents"],
      ["Next", "Household product", "Catalogue packs, bought one at a time", "A measured minimum hardware spec"],
      ["Then", "Professional seat", "An insurance agent reviews a client's cover, with consent", "A position on the Financial Advisers Act"],
      ["Later", "Pack marketplace", "Packs written by domain experts", "A published pack contract and scalable provenance review"],
    ];
    s.addShape(pres.shapes.LINE, { x: 0.9, y: 2.42, w: 11.6, h: 0, line: { color: C.accent5, width: 2 } });
    for (let i = 0; i < 4; i++) {
      const [when, h, b, gate] = stages[i];
      const x = 0.6 + i * 3.1;
      s.addShape(pres.shapes.OVAL, { x: x + 0.12, y: 2.2, w: 0.44, h: 0.44,
        fill: { color: i === 0 ? C.accent1 : C.background1 }, line: { color: C.accent1, width: 2 } });
      text(s, when.toUpperCase(), { x: x + 0.7, y: 2.25, w: 2, h: 0.35, fontSize: 12, bold: true,
        charSpacing: 2, color: C.accent1, valign: "middle" });
      card(s, x, 2.95, 2.85, 2.65);
      text(s, h, { x: x + 0.25, y: 3.15, w: 2.4, h: 0.4, fontFace: "Arial", bold: true, fontSize: 17, color: C.text1 });
      text(s, b, { x: x + 0.25, y: 3.6, w: 2.4, h: 0.95, fontSize: 13 });
      text(s, "First: " + gate, { x: x + 0.25, y: 4.6, w: 2.4, h: 0.85, fontSize: 12, italic: true, color: C.accent2 });
    }
    text(s, "Willingness to pay is a hypothesis, ordered by how countable the loss is: a missed SRS relief, a lapsed motor policy, a parent's hospital stay nobody knew was covered.",
      { x: 0.6, y: 5.95, w: 12.1, h: 0.7, fontSize: 14 });
    source(s, "docs/report/07-commercialisation-roadmap.md");
  }

  // 15 · Close
  {
    const s = newSlide("Content Dark", "Trust and what next");
    heading(s, "Thank you", "When the documents don't say, PARROT says so");
    s.addImage({ path: path.join(ASSETS, "parrot-icon.png"), x: 9.4, y: 1.9, w: 3.3, h: 2.95,
      objectName: "parrot mark" });
    const next = [
      ["Prove it on real paper", "Close the synthetic-to-real gap: 14 of 40 holdout documents so far"],
      ["Turn the label check on", "ADR 0021: two fewer unsupported claims, no right answer lost"],
      ["Measure the minimum machine", "Fit the full workflow on an 8 GB GPU, then publish the spec"],
    ];
    for (let i = 0; i < 3; i++) {
      const y = 2.0 + i * 1.35;
      text(s, String(i + 1).padStart(2, "0"), { x: 0.6, y, w: 0.9, h: 0.9, fontFace: "Arial", bold: true,
        fontSize: 36, color: C.accent3 });
      text(s, next[i][0], { x: 1.6, y: y + 0.05, w: 7.2, h: 0.42, fontFace: "Arial", bold: true,
        fontSize: 20, color: C.background1 });
      text(s, next[i][1], { x: 1.6, y: y + 0.5, w: 7.2, h: 0.5, fontSize: 15, color: C.accent5 });
    }
    let x = 0.6;
    for (const n of ["Christian", "Zee", "Desmond", "Siew", "Yew Mun"]) {
      x += chip(s, n, x, 6.25, { fill: C.accent6, color: C.accent5, w: 1.35 }) + 0.15;
    }
    text(s, "Questions?", { x: 9.4, y: 5.4, w: 3.3, h: 0.6, fontFace: "Arial", bold: true, fontSize: 26,
      color: C.accent3, align: "center" });
    source(s, "docs/report/05 §5.5 · README.md", true);
  }

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
}

build().catch((e) => {
  console.error(e);
  process.exit(1);
});
