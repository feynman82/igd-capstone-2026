// Christian's segment: the problem, the product, the platform, and the live demonstration.
// DRAFT by Yew Mun's session on 28 October for Christian to rewrite in their own words. Sources:
// docs/report/Parrot Pitch Script.md (midterm), docs/report/07-commercialisation-roadmap.md,
// docs/report/04-packs-and-interface.md, docs/demo-run-sheet.md, and counts taken on 28 October.
const path = require("path");
const SHOTS = path.join(__dirname, "..", "..", "deck-shots");

module.exports = function christian({ pres, C, THEME, M, W, T, card, text, masters }) {
  const S = "Problem and product";
  pres.addSection({ title: S });
  const L = masters("Christian");
  const DRAFT = "DRAFT for Christian to rewrite in their own words. ";

  // ------------------------------------------------------------ 1. title (dark)
  {
    const s = pres.addSlide({ masterName: L.DARK, sectionTitle: S });
    s.addText("IGD ILP · GROUP 1 · FINAL PRESENTATION · 3 NOVEMBER 2026", { placeholder: "eyebrow" });
    text(s, [T("Your family's paperwork, answered. "), T("On your own machine.", { color: C.accent1 })],
      { x: M, y: 2.6, w: 15, h: 3.6, fontFace: "Jost", fontSize: 76, color: C.background1, valign: "top" });
    const names = ["CHRISTIAN", "ZEE", "DESMOND", "YEW MUN", "SIEW"];
    const lanes = ["Product and demo", "Interface and packs", "Corpus and testing", "Retrieval and results", "Governance"];
    names.forEach((n, i) => {
      const x = M + i * 3.6;
      text(s, n, { x, y: 7.9, w: 3.4, h: 0.45, fontFace: "Jost", fontSize: 20, bold: true, charSpacing: 2, color: C.accent1 });
      text(s, lanes[i], { x, y: 8.4, w: 3.4, h: 0.45, fontSize: 16, color: C.background2 });
    });
    s.addNotes(DRAFT +
      "Good morning. Where, exactly, is your car insurance policy right now? Not roughly. Exactly. An email, a drawer, a photo on a phone. " +
      "We are Group 1, and this is PARROT. You give it a document once, it files itself, and when you ask it something it answers with the page the answer came from. " +
      "When it does not know, it says so. It runs on the family's own laptop. Five of us will take you from the problem, to the product, to the evidence, to what still does not work.");
  }

  // ------------------------------------------------------------ 2. the problem
  {
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
    s.addText("THE PROBLEM", { placeholder: "eyebrow" });
    s.addText([T("The family filing system "), T("is a drawer.", { color: C.accent2 })], { placeholder: "title" });
    const people = [
      ["SARAH, 35", "Working mother. She is the household calendar.", "Renewals and due dates live in six inboxes and a drawer."],
      ["MARCUS, 39", "Sandwich generation. Tracks his parents' policies too.", "Eleven policies, five people, and one question: are we covered?"],
      ["PRIYA, 32", "Single professional. Saves tax through SRS, once a year.", "Miss the window and the tax saving is gone, silently."],
    ];
    const cw = 5.75, gap = 0.375, y0 = 3.2, ch = 4.6;
    people.forEach(([who, role, pain], i) => {
      const x = M + i * (cw + gap);
      card(s, "persona" + i, x, y0, cw, ch, THEME.colors.lt2);
      text(s, who, { x: x + 0.4, y: y0 + 0.4, w: cw - 0.8, h: 0.5, fontFace: "Jost", fontSize: 20, bold: true, charSpacing: 2, color: C.accent2 });
      text(s, role, { x: x + 0.4, y: y0 + 1.05, w: cw - 0.8, h: 1.2, fontFace: "Jost", fontSize: 24, color: C.text1, valign: "top" });
      text(s, pain, { x: x + 0.4, y: y0 + 2.6, w: cw - 0.8, h: 1.6, fontSize: 18, color: C.text2, valign: "top" });
    });
    text(s, "None of them is missing documents. They are missing a way to ask the pile a question and trust the answer.",
      { x: M, y: 8.3, w: W, h: 0.9, fontFace: "Jost", fontSize: 26, color: C.text1, valign: "top" });
    s.addNotes(DRAFT +
      "Three people from our five personas. Sarah is the household calendar. Marcus keeps track of eleven policies across five people, and 'are we covered' costs him an evening. " +
      "Priya saves tax through SRS in a narrow window; miss it and nothing happens, the saving just disappears. None of them is missing the documents. " +
      "They are missing a way to ask the pile a question and trust the answer. And a chatbot that confidently invents a policy date is worse than none, because you stop checking.");
  }

  // ------------------------------------------------------------ 3. the solution
  {
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
    s.addText("THE SOLUTION", { placeholder: "eyebrow" });
    s.addText([T("Drop it in. Ask it. "), T("It shows its page.", { color: C.accent2 })], { placeholder: "title" });
    const steps = [
      ["01", "Drop it in. It files itself.", "A watched folder, or a Telegram chat. It reads the type, the fields, and the page each was printed on."],
      ["02", "Ask. Every sentence has a page.", "Each sentence carries its own source. One that cannot be traced is never shown."],
      ["03", "Today: what needs you now.", "Renewals, deadlines and thresholds, in order of urgency. Most days, nearly empty."],
    ];
    steps.forEach(([n, head, body], i) => {
      const y = 3.2 + i * 2.05;
      text(s, n, { x: M, y, w: 0.9, h: 0.6, fontFace: "Jost", fontSize: 24, color: C.accent2 });
      text(s, head, { x: M + 1.0, y, w: 10, h: 0.6, fontFace: "Jost", fontSize: 26, color: C.text1 });
      text(s, body, { x: M + 1.0, y: y + 0.7, w: 10, h: 1.1, fontSize: 18, color: C.text2, valign: "top" });
    });
    card(s, "doesNotGuess", M, 9.25, 11, 0.8, THEME.colors.lt2);
    text(s, "When the documents do not say, PARROT says so. It does not guess.",
      { x: M + 0.3, y: 9.25, w: 10.5, h: 0.8, fontFace: "Jost", fontSize: 20, color: C.accent2, valign: "middle" });
    s.addImage({ path: path.join(SHOTS, "final-ask.jpg"), x: 13.3, y: 1.0, w: 5.7, h: 7.99 });
    s.addNotes(DRAFT +
      "Three things. You drop a document into a folder, or send it to a Telegram chat, and it files itself: what kind of document it is, the fields on it, and the page each one is printed on. " +
      "You ask, and every sentence of the answer carries its own source. And Today tells you what needs you, before you think to ask. When the documents do not say, PARROT says so.");
  }

  // ------------------------------------------------------------ 4. private by design (dark)
  {
    const s = pres.addSlide({ masterName: L.DARK, sectionTitle: S });
    s.addText("WHY YOU CAN TRUST IT", { placeholder: "eyebrow" });
    s.addText([T("Private by design, "), T("not by promise.", { color: C.accent1 })], { placeholder: "title" });
    const cols = [
      ["CAPTURE", "A watched folder on the laptop. Telegram is optional."],
      ["THINKING", "Every model runs on the laptop: the 4B SEA-LION generator from AI Singapore, the embedder, the re-reader."],
      ["STORAGE", "One PostgreSQL database, on the same laptop. Documents stay in the folder you put them in."],
    ];
    const cw = 5.75, gap = 0.375, y0 = 3.3, ch = 3.9;
    cols.forEach(([head, body], i) => {
      const x = M + i * (cw + gap);
      card(s, "trust" + i, x, y0, cw, ch, THEME.colors.dk2);
      text(s, head, { x: x + 0.4, y: y0 + 0.4, w: cw - 0.8, h: 0.5, fontFace: "Jost", fontSize: 18, bold: true, charSpacing: 2, color: C.accent1 });
      text(s, body, { x: x + 0.4, y: y0 + 1.1, w: cw - 0.8, h: 2.6, fontSize: 20, color: C.background1, valign: "top" });
    });
    text(s, [T("Reading, searching, answering, and our own grading: ", { color: C.background2 }), T("all on the laptop.", { color: C.accent1, bold: true })],
      { x: M, y: 7.7, w: W, h: 0.7, fontFace: "Jost", fontSize: 28 });
    text(s, "No evaluation question left the machine either: the judge model runs locally too. Telegram capture, when it is switched on, is the one channel that crosses the network.",
      { x: M, y: 8.6, w: 16, h: 1.0, fontSize: 17, color: C.background2, valign: "top" });
    s.addNotes(DRAFT +
      "Everything that reads, searches and answers runs on the family's own laptop: the generator is a 4-billion-parameter model from AI Singapore, and the embedder and the re-reader run beside it. " +
      "The documents stay in the folder you put them in, and the database is on the same machine. Even our grading ran locally. " +
      "The one channel that crosses the network is Telegram capture, and it is optional: the watched folder needs no network at all.");
  }

  // ------------------------------------------------------------ 5. the platform
  {
    const s = pres.addSlide({ masterName: L.LIGHT, sectionTitle: S });
    s.addText("THE PLATFORM", { placeholder: "eyebrow" });
    s.addText([T("One engine. "), T("Two ways to grow.", { color: C.accent2 })], { placeholder: "title" });
    const cols = [
      ["SKILLS · WHAT IT CAN DO", "Reminder · Alert · Advice", "Each reads the filed facts. None touches the screen. Tracker is specified, not built.", THEME.colors.lt2, C.text1],
      ["THE ENGINE", "File · Find · Check · Cite", "Advice figures are worked out in code, never by the model.", THEME.colors.dk1, C.background1],
      ["SUBJECT PACKS · WHAT IT KNOWS", "Insurance · Tax and Reliefs", "One file of know-how each, checked against a contract. Nine more are specified the same way.", THEME.colors.lt2, C.text1],
    ];
    const cw = 5.75, gap = 0.375, y0 = 3.2, ch = 4.2;
    cols.forEach(([eyebrow, head, body, fill, ink], i) => {
      const x = M + i * (cw + gap);
      card(s, "platform" + i, x, y0, cw, ch, fill);
      text(s, eyebrow, { x: x + 0.4, y: y0 + 0.4, w: cw - 0.8, h: 0.45, fontFace: "Jost", fontSize: 15, bold: true, charSpacing: 2, color: i === 1 ? C.accent1 : C.accent2 });
      text(s, head, { x: x + 0.4, y: y0 + 1.0, w: cw - 0.8, h: 0.9, fontFace: "Jost", fontSize: 28, color: ink, valign: "top" });
      text(s, body, { x: x + 0.4, y: y0 + 2.1, w: cw - 0.8, h: 1.8, fontSize: 17, color: i === 1 ? C.background2 : C.text2, valign: "top" });
    });
    const stats = [["108", "reviewed changes merged"], ["328", "commits on main"], ["1,204", "automated tests"]];
    stats.forEach(([big, label], i) => {
      const x = M + i * 6.125;
      text(s, big, { x, y: 7.85, w: 5.5, h: 1.0, fontFace: "Jost", fontSize: 52, color: C.accent2 });
      text(s, label, { x, y: 8.85, w: 5.5, h: 0.45, fontSize: 16, color: C.text2 });
    });
    text(s, "Counted on 28 October 2026.", { x: M, y: 9.5, w: 8, h: 0.4, fontSize: 13, italic: true, color: C.accent3 });
    s.addNotes(DRAFT +
      "PARROT grows along two axes that do not touch. Skills extend what it can do: Reminder, Alert and the Advice calculator are built, and Tracker is specified. " +
      "Packs extend what it knows about: Insurance and Tax are built, and nine more are specified against the same contract. Because the axes are independent, every skill applies to every pack whose documents print what the skill reads. " +
      "Advice figures are calculated in code, never by the model. 108 reviewed changes, 328 commits, 1,204 automated tests, as of 28 October.");
  }

  // ------------------------------------------------------------ 6. live demonstration (orange)
  {
    const s = pres.addSlide({ masterName: L.ORANGE, sectionTitle: S });
    text(s, "LIVE DEMONSTRATION", { x: M, y: 0.75, w: W, h: 0.45, fontFace: "Jost", fontSize: 16, bold: true, charSpacing: 2, color: C.text1 });
    text(s, "Watch it file, answer, and say no.", { x: M, y: 1.3, w: W, h: 1.4, fontFace: "Jost", fontSize: 56, color: C.text1 });
    const steps = [
      ["1", "Today", "It speaks first"], ["2", "The source chip", "Every claim opens its page"], ["3", "Drop a document in", "The front door is a folder"],
      ["4", "Ask", "Each sentence carries its source"], ["5", "Vault", "What it read, and what it couldn't"], ["6", "The abstention", "It declines rather than invents"],
      ["7", "The refusal to act", "It advises. It never acts"], ["8", "Switch a pack off", "Its voice goes. Your documents stay"], ["9", "Close", "Name what was not shown"],
    ];
    steps.forEach(([n, head, point], i) => {
      const col = Math.floor(i / 3), row = i % 3;
      const x = M + col * 6.1, y = 3.3 + row * 1.9;
      const key = n === "6";
      card(s, "demo" + n, x, y, 5.8, 1.65, key ? THEME.colors.dk1 : THEME.colors.lt1);
      text(s, n, { x: x + 0.3, y: y + 0.25, w: 0.6, h: 0.6, fontFace: "Jost", fontSize: 28, color: key ? C.accent1 : C.accent2 });
      text(s, head, { x: x + 1.0, y: y + 0.22, w: 4.6, h: 0.6, fontFace: "Jost", fontSize: 24, color: key ? C.background1 : C.text1 });
      text(s, point, { x: x + 1.0, y: y + 0.85, w: 4.6, h: 0.6, fontSize: 16, color: key ? C.background2 : C.text2 });
    });
    text(s, "7 minutes 50 seconds. Step 6 is the one we will not cut.", { x: M, y: 9.25, w: W, h: 0.6, fontFace: "Jost", fontSize: 22, color: C.text1 });
    s.addNotes(DRAFT +
      "Switch to the browser. Follow docs/demo-run-sheet.md exactly: nine steps, seven minutes fifty. Step 6, the abstention, is the point of the project; cut step 3 if time runs short. " +
      "Before the room fills: the pre-flight checklist in the run sheet, including no 'Who is ...?' card on Today and no Set C document in the vault.");
  }
};
