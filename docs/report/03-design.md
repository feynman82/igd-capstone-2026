# §3 · Solution design and architecture

> **Draft.** Written from the repository for Christian to rewrite in their own words.

---

## 3.1 Design principles

Four principles follow from the thesis. Each is a constraint on the build, not an aspiration.

1. **Local by default, with a stated boundary.** Inference and storage stay on the owner's machine,
   and every exception is named.
2. **Provenance on every claim.** Every fact row carries a document and page, and a sentence with no
   supporting passage is dropped.
3. **Calculation in code.** Dates, gaps and estimates come from typed rows, through hand-written
   queries and calculators. Where the model writes a number in an answer, the gate keeps it only if
   a cited passage prints it.
4. **Advise, never act.** Version one does not pay, book or file.

Each makes trust rest on something a person can inspect.

## 3.2 System architecture

Figure 1 shows the layers and the trust boundary.

Documents arrive through a watched folder or a Telegram bot, behind one capture interface. A worker
reads them (§4.2) into one PostgreSQL database, so one transaction spans chunks, facts and obligations (ADR 0002).

Two lanes read that database, with different guarantees. The answer lane can decline. A router turns
away requests to act before anything is searched. A second step restates the question in the
documents' words (ADR 0013), hybrid search returns forty candidates, and a cross-encoder keeps six.
The grounding gate works on both sides of generation. Before the model runs, it asks whether
the evidence is worth answering from. After each sentence, it asks whether to keep it, so nothing reaches the screen only to be withdrawn. In the module lane, Reminder, Alert and
Advice read typed rows, not chunks, and code does the arithmetic.

The boundary claim is narrow. At inference and at rest nothing leaves the machine, and
service addresses are refused at start-up unless they are local. Capture by Telegram does send the
image through a third party, and what Telegram keeps after deletion is unverified. Model weights
download inbound on first use. A claim this specific can be checked, which is what warranted trust
requires.

![**Figure 1.** Inside the dashed line, everything stays on the owner's machine. The one document route across it is named.](figures/figure-1-architecture.png|0.64)

## 3.3 Two axes of expansion: capability modules and domain packs

PARROT grows along two axes that do not touch (Figure 2). Capability modules extend what it can do:
Reminder, Alert and Advice are built, and Tracker is specified. Domain packs extend what it knows
about: insurance and tax are built, and nine more are specified against the
same contract.

The axes are independent because modules read typed rows, whichever domain they concern. Reminder
needs only a printed date, so eight of the nine specified packs use it with no new code.

The proposal's pack owned its document types, so switching a pack off would have hidden the
household's own papers (ADR 0017). The core now owns every document type and field, in one catalogue.
A pack is knowledge and voice: official sources, a persona, guardrails, answering rules and,
optionally, advice. Switching one off removes its voice, never the household's documents.

The model is specified, not proved. A new pack is a file, plus a reviewed core change where it needs
new document types: 29 across the nine. Five of the nine deliberately have no grounding corpus,
because for subjects such as health and law, general guidance would read as advice.

Both axes stop at acting. Growth along either adds knowledge and warnings, never authority.

![**Figure 2.** One core, two axes: every module reaches every pack whose documents print what it reads, and neither axis reaches past advice.](figures/figure-2-two-axes.png|0.66)

## 3.5 Data requirements and the synthetic corpus

The system needs household documents whose correct answers are known: the value of every field, and
the page it is printed on. Real documents could not supply that here. They carry personal data about
people outside the team, including children, whose consent we cannot meaningfully obtain, and we
could not honour a retention promise after the module ends. So the corpus is synthetic.

The method matters more than the decision. The register came first: one spreadsheet row per
document, filled before the document existed, then merged into templates. Ground truth is therefore a
by-product, and answers can be graded without a person reading each one. A one-page canon keeps one
household, the Lims of Tampines, consistent throughout.

The frozen corpus holds 93 documents, against about 360 planned. Of these, 54 have register rows (44
clean, 7 photographed, 3 scanned), and 39 are unregistered statements kept as noise.

The limitation is plain. Synthetic documents are cleaner and more consistent than real ones, so a
score on them overstates the system. A redacted real-document holdout exists to measure that gap. It
holds 14 of a planned 40 and has not been run, so every number in §5 is on synthetic documents.
