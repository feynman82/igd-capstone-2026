"use client";

import { useEffect, useRef, useState, type CSSProperties } from "react";
import {
  ArrowUpRight, BookOpen, CalendarDays, Check, CheckCheck,
  ChevronRight, CircleAlert, FileText, FolderOpen, HelpCircle,
  LockKeyhole, Moon, PanelRightClose, RotateCcw, Search, ShieldCheck,
  Sun, ZoomIn, ZoomOut,
} from "lucide-react";
import styles from "./preview.module.css";

type Direction = "civic" | "home" | "desk";
type Screen = "today" | "ask";
type Outcome = "answer" | "abstention" | "refusal";
type Source = { name: string; page: number; context: string };
type Item = { id: number; kind: "overdue" | "alert" | "upcoming"; title: string; person: string; detail: string; source: Source };

const directions = {
  civic: { name: "Civic Register", stance: "Order, clarity and institutional confidence.", tradeoff: "Best for fast scanning. More formal, with denser information." },
  home: { name: "Kitchen Table", stance: "A little less household admin. A little more breathing room.", tradeoff: "Best for a short daily catch-up. Larger cards mean more scrolling." },
  desk: { name: "The Reading Desk", stance: "Understand it. Open the source. See for yourself.", tradeoff: "Best for checking the evidence. The source pane needs more screen space." },
};

// Evaluation-only tokens. Production continues to use app/theme.css.
const palettes = {
  civic: {
    light: ["#F4F6F5", "#FFFFFF", "#E9EEEC", "#172823", "#40534B", "#56675F", "#74867C", "#0F5F52", "#A32626", "#805000"],
    dark: ["#101815", "#19241F", "#233129", "#F0F5F2", "#C3D0C8", "#A2B5A8", "#71897A", "#83D5BB", "#FFAAA2", "#EBC37D"],
  },
  home: {
    light: ["#F7F2E9", "#FFFCF6", "#EEE6D9", "#302B25", "#554C41", "#6A6052", "#8B7D6B", "#0F5F52", "#A32626", "#805000"],
    dark: ["#1B1814", "#25211B", "#302A22", "#F8F0E3", "#D6CBBB", "#BBAE9B", "#998873", "#83D5BB", "#FFAAA2", "#EBC37D"],
  },
  desk: {
    light: ["#F2F4F7", "#FFFFFF", "#E7EBF0", "#18212B", "#3F4D5B", "#576675", "#778697", "#0F5F52", "#A32626", "#805000"],
    dark: ["#11161E", "#1A222D", "#25303D", "#EFF4FA", "#C4D0DF", "#A4B6CC", "#7B90AA", "#83D5BB", "#FFAAA2", "#EBC37D"],
  },
};
const tokenNames = ["canvas", "surface", "inset", "ink", "secondary", "muted", "edge", "accent", "overdue", "alert"];
const renewal = { name: "Motor renewal notice", page: 1, context: "Policy expiry — Marcus Fernandez. Overdue since 30 Nov 2026." };
const schedule = { name: "Motor policy schedule", page: 2, context: "The recorded policy period ends on 30 Nov 2026." };
const tax = { name: "Tax filing notice", page: 1, context: "Filing deadline: 18 Apr 2027." };
const items: Item[] = [
  { id: 1, kind: "overdue", title: "Your motor policy has expired", person: "Marcus Fernandez", detail: "Overdue since 30 Nov 2026", source: renewal },
  { id: 2, kind: "alert", title: "115 days without recorded cover", person: "Marcus Fernandez", detail: "Above the configured limit of 0 days", source: schedule },
  { id: 3, kind: "upcoming", title: "Your tax filing deadline is coming up", person: "Household tax", detail: "Due in 24 days · 18 Apr 2027", source: tax },
];
const answers = [
  { text: "Marcus’s motor policy expired on 30 November 2026.", source: renewal },
  { text: "The renewal notice asks for payment before the existing policy expires.", source: renewal },
  { text: "The policy schedule records the same end date: 30 November 2026.", source: schedule },
];
const questions: Record<Outcome, string> = {
  answer: "When does Marcus’s motor policy expire?",
  abstention: "What does the new motor policy cover?",
  refusal: "Renew Marcus’s motor policy for me.",
};
const disclaimer = "This explains your insurance documents. It is not financial advice.";

export function DesignPreview() {
  const [direction, setDirection] = useState<Direction>("desk");
  const [dark, setDark] = useState(false);
  const [screen, setScreen] = useState<Screen>("today");
  const [empty, setEmpty] = useState(false);
  const [outcome, setOutcome] = useState<Outcome>("answer");
  const [question, setQuestion] = useState(questions.answer);
  const [submitted, setSubmitted] = useState(questions.answer);
  const [visible, setVisible] = useState(3);
  const [streaming, setStreaming] = useState(false);
  const [removed, setRemoved] = useState<Record<number, "done" | "dismissed">>({});
  const [history, setHistory] = useState(false);
  const [notice, setNotice] = useState<{ id: number; text: string } | null>(null);
  const [source, setSource] = useState<Source | null>(null);
  const sourceTrigger = useRef<HTMLButtonElement | null>(null);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);
  const [notes, setNotes] = useState(false);

  useEffect(() => () => { if (timer.current) clearInterval(timer.current); }, []);
  const stopStream = () => { if (timer.current) clearInterval(timer.current); setStreaming(false); };
  const closeSource = () => { setSource(null); sourceTrigger.current?.focus(); };
  const changeScreen = (next: Screen) => { stopStream(); setVisible(3); setScreen(next); setSource(null); };
  const changeOutcome = (next: Outcome) => { stopStream(); setOutcome(next); setQuestion(questions[next]); setSubmitted(questions[next]); setVisible(3); setSource(null); };
  const runQuestion = () => {
    stopStream(); setSource(null); setSubmitted(question.trim());
    if (outcome !== "answer") return;
    setVisible(0); setStreaming(true);
    let count = 0;
    timer.current = setInterval(() => {
      count += 1; setVisible(count);
      if (count === answers.length) { if (timer.current) clearInterval(timer.current); setStreaming(false); }
    }, 1100);
  };
  const restore = (id: number) => { setRemoved((previous) => { const next = { ...previous }; delete next[id]; return next; }); setNotice(null); };
  const mark = (id: number, state: "done" | "dismissed") => {
    setRemoved((previous) => ({ ...previous, [id]: state }));
    setNotice({ id, text: state === "done" ? "Marked done in PARROT." : "Dismissed from Today." });
  };
  const openSource = (value: Source, trigger: HTMLButtonElement) => { sourceTrigger.current = trigger; setSource(value); };
  const chip = (value: Source) => {
    const selected = source?.name === value.name && source?.page === value.page;
    return <button type="button" className={`${styles.chip} ${selected ? styles.chipOpen : ""}`} aria-expanded={selected} aria-controls={selected ? "source-viewer" : undefined} onClick={(event) => openSource(value, event.currentTarget)}>
      <FileText size={15} aria-hidden="true" /><span>{value.name}<span className={styles.pageNumber}>, p.{value.page}</span></span><ArrowUpRight size={14} aria-hidden="true" />
    </button>;
  };
  const active = empty ? [] : items.filter((item) => !removed[item.id]);
  const palette = palettes[direction][dark ? "dark" : "light"];
  const theme = Object.fromEntries(tokenNames.map((name, index) => [`--p-${name}`, palette[index]])) as CSSProperties;

  return <div className={`${styles.preview} ${styles[direction]}`} style={{ ...theme, colorScheme: dark ? "dark" : "light" }}>
    <a className={styles.skip} href="#preview-content">Skip to preview</a>
    <header className={styles.evaluation} aria-label="Design evaluation controls">
      <div className={styles.evaluationTitle}><span className={styles.sampleDot} />Interface study<span className={styles.sampleLabel}>Sample data only</span></div>
      <div className={styles.directionSwitch} role="group" aria-label="Design direction">
        {(Object.keys(directions) as Direction[]).map((key) => <button key={key} type="button" aria-pressed={direction === key} onClick={() => { setDirection(key); setSource(null); }}>{directions[key].name}</button>)}
      </div>
      <div className={styles.evaluationActions}>
        <button type="button" className={styles.iconButton} aria-label={dark ? "Switch to light theme" : "Switch to dark theme"} onClick={() => setDark(!dark)}>{dark ? <Sun size={18} /> : <Moon size={18} />}</button>
        <button type="button" className={styles.iconButton} aria-label="Design notes" aria-expanded={notes} onClick={() => setNotes(!notes)}><HelpCircle size={18} /></button>
      </div>
    </header>
    <div className={styles.scenarios}>
      <span>Explore the states</span>
      <div className={styles.scenarioButtons} role="group" aria-label="Preview state">
        <button type="button" aria-pressed={screen === "today" && !empty} onClick={() => { changeScreen("today"); setEmpty(false); setHistory(false); setRemoved({}); setNotice(null); }}>Today</button>
        <button type="button" aria-pressed={screen === "today" && empty} onClick={() => { changeScreen("today"); setEmpty(true); setHistory(false); setNotice(null); }}>Quiet day</button>
        {(["answer", "abstention", "refusal"] as Outcome[]).map((value) => <button type="button" key={value} aria-pressed={screen === "ask" && outcome === value} onClick={() => { changeScreen("ask"); changeOutcome(value); }}>{value === "answer" ? "Ask · answer" : value === "abstention" ? "Missing document" : "Request to act"}</button>)}
      </div>
    </div>
    {notes && <aside className={styles.notes}><strong>{directions[direction].name}</strong><p>{directions[direction].stance} {directions[direction].tradeoff}</p><p>Interactive concept, not connected to your documents or an AI model. Questions play the selected sample outcome. Source panels are interface placeholders, not corpus documents. Evaluation date: 25 Mar 2027.</p></aside>}

    <div className={styles.shell}>
      <aside className={styles.navigation} aria-label="Product navigation">
        <div className={styles.brand}><BookOpen size={24} strokeWidth={1.6} aria-hidden="true" /><span>parrot<span className={styles.brandPeriod}>.</span></span></div>
        <nav className={styles.navLinks} aria-label="Screens">
          <button type="button" aria-current={screen === "today" ? "page" : undefined} onClick={() => changeScreen("today")}><CalendarDays size={18} />Today</button>
          <button type="button" aria-current={screen === "ask" ? "page" : undefined} onClick={() => changeScreen("ask")}><Search size={18} />Ask</button>
        </nav>
        <div className={styles.local}><LockKeyhole size={15} aria-hidden="true" /><span>On this computer<span>Private by design</span></span></div>
      </aside>

      <main id="preview-content" className={styles.main}>
        <div className={styles.topline}><span>Fernandez household</span><span>Thursday, 25 March 2027</span></div>
        <div className={`${styles.workspace} ${source ? styles.withSource : ""}`}>
          <div className={styles.content}>
            {screen === "today" ? <>
              <header className={styles.screenHeading}>
                <div><h1>{direction === "home" ? "A moment for today." : "Today"}</h1><p>{active.length ? direction === "home" ? "A few things to look at, then back to your day." : "What needs your attention, in order of urgency." : "Your household, up to date."}</p></div>
                <span className={styles.checked}><CheckCheck size={16} aria-hidden="true" />Checked at 7:04 am</span>
              </header>
              {active.length > 0 && <div className={styles.listSummary}><span>{active.filter((item) => item.kind !== "upcoming").length} need attention</span><span>{active.filter((item) => item.kind === "upcoming").length} coming up</span><span className={styles.sourceHint}><FileText size={14} />Every item has a source</span></div>}
              <div className={styles.itemList}>
                {active.map((item) => <article className={`${styles.item} ${source?.name === item.source.name ? styles.selectedItem : ""}`} key={item.id}>
                  <div className={`${styles.status} ${styles[item.kind]}`}>{item.kind === "upcoming" ? <CalendarDays size={16} /> : <CircleAlert size={16} />}<span>{item.kind === "upcoming" ? "Upcoming" : item.kind === "overdue" ? "Overdue" : "Alert"}</span></div>
                  <div className={styles.itemBody}><p className={styles.person}>{item.person}</p><h2>{item.title}</h2><p className={`${styles.detail} ${item.kind === "overdue" ? styles.overdue : ""}`}>{item.detail}</p><div className={styles.sourceLine}>{chip(item.source)}</div></div>
                  <div className={styles.rowActions}><button type="button" onClick={() => mark(item.id, "done")} aria-label={`Mark done: ${item.title}`}><Check size={16} />Mark done</button><button type="button" onClick={() => mark(item.id, "dismissed")} aria-label={`Dismiss: ${item.title}`}>Dismiss</button></div>
                </article>)}
              </div>
              {active.length === 0 && <section className={styles.empty}><div className={styles.emptyIcon}><Check size={32} strokeWidth={1.5} /></div><h2>Nothing needs you today.</h2><p>No items need attention in the documents<br className={styles.desktopBreak} /> checked at 7:04 am. You can leave it here.</p><span className={styles.emptyScope}><FolderOpen size={16} />12 documents checked on this computer</span></section>}
              {notice && <div className={styles.notice} role="status"><Check size={16} /><span>{notice.text}</span><button type="button" onClick={() => restore(notice.id)}>Undo</button></div>}
              <footer className={styles.todayFooter}><span><LockKeyhole size={14} />Based only on your own documents</span><button type="button" aria-expanded={history} onClick={() => setHistory(!history)}>Completed and dismissed <ChevronRight size={15} /></button></footer>
              {history && <section className={styles.history}><h2>Completed and dismissed</h2>{Object.keys(removed).length === 0 ? <p>No items here yet.</p> : items.filter((item) => removed[item.id]).map((item) => <div key={item.id}><span>{item.title}<small>{removed[item.id] === "done" ? "Marked done" : "Dismissed"}</small></span><button type="button" onClick={() => restore(item.id)}><RotateCcw size={14} />Restore</button></div>)}</section>}
            </> : <>
              <header className={styles.screenHeading}><div><h1>{direction === "home" ? "Let’s make sense of it." : "Ask your documents"}</h1><p>{direction === "desk" ? "An explanation you can check, sentence by sentence." : "One question. An answer with the page it came from."}</p></div></header>
              <form className={styles.questionForm} onSubmit={(event) => { event.preventDefault(); runQuestion(); }}>
                <label htmlFor="preview-question">Your question</label>
                <div><textarea id="preview-question" rows={2} maxLength={2000} value={question} onChange={(event) => setQuestion(event.target.value)} /><button className={styles.primary} type="submit" disabled={!question.trim() || streaming}><ArrowUpRight size={18} />Ask</button></div>
                <span className={styles.formHint}>Sample response selected above · no model connected</span>
              </form>
              <section className={styles.answerArea} aria-label={`Response to: ${submitted}`}>
                {outcome === "answer" ? <>
                  <div className={styles.answerLabel}><BookOpen size={17} /><span>From your documents</span>{!streaming && <span className={styles.answerCount}>2 sources</span>}</div>
                  <div aria-live="polite" aria-relevant="additions" className={styles.sentences}>{answers.slice(0, visible).map((answer, index) => <div key={index} className={`${styles.sentence} ${source?.name === answer.source.name ? styles.selectedSentence : ""}`}><p>{answer.text}</p>{chip(answer.source)}</div>)}</div>
                  {streaming && <p role="status" className={styles.reading}><BookOpen size={16} />{visible === 0 ? "Reading your documents…" : "Checking the next sentence…"}</p>}
                </> : outcome === "abstention" ? <div className={styles.abstention}><FolderOpen size={28} strokeWidth={1.5} /><span className={styles.outcomeLabel}>Evidence needed</span><h2>I can’t answer that from your documents.</h2><p>The renewal notice does not describe the cover in a new policy.</p><div className={styles.missing}><FileText size={22} /><div><strong>New motor policy schedule</strong><span>This would show the cover and the new policy period.</span></div></div><p className={styles.outcomeFootnote}>Add this document to PARROT to ask again.</p></div> : <div className={styles.refusal}><ShieldCheck size={28} strokeWidth={1.5} /><span className={styles.outcomeLabel}>You remain in charge</span><h2>PARROT does not take actions.</h2><p>I can explain the renewal notice. I do not renew policies.</p><div className={styles.boundary}>No payment, renewal, booking or filing is made.</div></div>}
                <p className={styles.disclaimer}>{disclaimer}</p>
                {!streaming && <button type="button" className={styles.another} onClick={() => { setQuestion(""); document.getElementById("preview-question")?.focus(); }}>Ask another question <ArrowUpRight size={15} /></button>}
              </section>
            </>}
          </div>
          {source && <SourceViewer source={source} onClose={closeSource} />}
        </div>
      </main>
    </div>
    <footer className={styles.studyFooter}><span>{directions[direction].name}</span><span>{directions[direction].stance}</span><button type="button" onClick={() => { setRemoved({}); setNotice(null); setHistory(false); setEmpty(false); setSource(null); stopStream(); setVisible(3); }}><RotateCcw size={14} />Reset sample</button></footer>
  </div>;
}

function SourceViewer({ source, onClose }: { source: Source; onClose: () => void }) {
  const [zoom, setZoom] = useState(100);
  const [textView, setTextView] = useState(false);
  const panel = useRef<HTMLElement>(null);
  useEffect(() => {
    panel.current?.focus();
    setZoom(100);
    const narrow = window.matchMedia("(max-width: 1199px)").matches;
    const previousOverflow = document.body.style.overflow;
    if (narrow) document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = previousOverflow; };
  }, [source]);
  return <aside ref={panel} id="source-viewer" tabIndex={-1} className={styles.sourceViewer} role="dialog" aria-label={`${source.name}, page ${source.page}`} onKeyDown={(event) => {
    if (event.key === "Escape") { event.preventDefault(); onClose(); }
    if (event.key === "Tab" && window.matchMedia("(max-width: 1199px)").matches) {
      const buttons = Array.from(panel.current?.querySelectorAll<HTMLButtonElement>("button:not(:disabled)") ?? []);
      const first = buttons[0], last = buttons[buttons.length - 1];
      if (event.shiftKey && (document.activeElement === first || document.activeElement === panel.current)) { event.preventDefault(); last?.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    }
  }}>
    <header className={styles.viewerHeader}><div><span>Source document</span><h2>{source.name}</h2><p>Page {source.page}</p></div><button type="button" className={styles.iconButton} onClick={onClose} aria-label="Close source document"><PanelRightClose size={20} /></button></header>
    <div className={styles.sourceContext}><FileText size={16} /><p>{source.context}</p></div>
    <div className={styles.viewerTools}><button type="button" aria-pressed={textView} onClick={() => setTextView(!textView)}>{textView ? "Page view" : "Text view"}</button><div><button type="button" className={styles.iconButton} disabled={zoom <= 75} aria-label="Zoom out" onClick={() => setZoom(Math.max(75, zoom - 25))}><ZoomOut size={17} /></button><span>{zoom}%</span><button type="button" className={styles.iconButton} disabled={zoom >= 150} aria-label="Zoom in" onClick={() => setZoom(Math.min(150, zoom + 25))}><ZoomIn size={17} /></button></div></div>
    <div className={styles.documentWell}>
      {textView ? <div className={styles.textView}><strong>Sample source context</strong><p>{source.context}</p><p>This is an interface demonstration. No real document has been opened.</p></div> : <div className={styles.pagePlaceholder} style={{ width: `${zoom}%` }}><div className={styles.pageStamp}><FileText size={18} /><span>Source preview</span></div><div className={styles.documentLines} aria-hidden="true"><i /><i /><i /></div><div className={styles.placeholderCallout}><FileText size={32} strokeWidth={1.3} /><h3>Your document, on the page.</h3><p>The original rendered page appears here in PARROT.</p><span>Interface placeholder · no document loaded</span></div><div className={styles.documentLines} aria-hidden="true"><i /><i /><i /><i /></div><span className={styles.pageFooter}>Page {source.page}</span></div>}
    </div>
    <div className={styles.viewerFoot}><LockKeyhole size={14} />The original stays on your computer.</div>
  </aside>;
}
