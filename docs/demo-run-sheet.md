# The demonstration run sheet

**Owner: Christian (Lane A).** Reviewed by Zee. This is the script for the live
demonstration in Session 10, and the thing to rehearse against — the W9 task asks for three
timed run-throughs on frozen code, and "timed" means against this sheet.

Nine steps, **7 minutes 50 seconds**, which leaves room to lose twenty seconds somewhere and
still land under eight. Step 6 is the abstention. It is the point of the project, so it is
the one step that must not be cut for time — cut step 3 instead.

---

## Before the room fills

The demonstration fails in the ten minutes before it starts, not during it. Everything below
is done and **checked on the presenting machine**, not on the machine it was built on.

- [ ] `docker compose -f infra/docker-compose.yml up -d` — database up
- [ ] Ollama running, all three models pulled (`ollama list` shows generator, embedder, reranker)
- [ ] Window one: `make dev`, and `http://127.0.0.1:8000` reports every component found
- [ ] Window two: `cd web && npm run dev`, `http://localhost:3000` loads
- [ ] Passphrase already entered. **Do not demonstrate the lock screen.** It is thirty seconds
      of typing that shows nothing, and a forgotten passphrase in front of an audience costs
      the whole slot
- [ ] A corpus batch loaded (`make corpus-load BATCH=batch1`) and **Today is not empty** —
      at least one renewal inside its lead window
- [ ] Both packs switched **on**. Step 8 switches one off; it has to start on
- [ ] One document in quarantine, so step 5 has something to show
- [ ] One unread document staged on the desktop for step 3, *not* already in `inbox/`
- [ ] Browser at 125% zoom, one tab, bookmarks bar hidden, notifications silenced
- [ ] Laptop on mains. The decode rate on battery is roughly half

> **The corpus is the dependency.** Today, Ask and Vault all show nothing without a loaded
> batch, and a batch comes from Lane E. If no batch has landed by the rehearsal, the
> demonstration cannot be rehearsed honestly — say so early rather than discovering it on the
> day. `inbox/` documents will make the screens move, but the answers will not be checkable
> against a register, and step 6 stops being a real abstention.

---

## The shape

| | Step | From | Runs | The point |
|---|---|---|---|---|
| 1 | Today | 0:00 | 0:50 | It speaks first. You did not have to ask |
| 2 | The source chip | 0:50 | 0:40 | Every claim opens to the page it came from |
| 3 | Drop a document in | 1:30 | 1:10 | The front door is a folder |
| 4 | Ask, and get an answer | 2:40 | 1:20 | Each sentence carries its own sources |
| 5 | Vault | 4:00 | 0:50 | What it believes, and what it could not read |
| 6 | **The abstention** | 4:50 | 1:00 | **It declines rather than inventing** |
| 7 | The refusal to act | 5:50 | 0:40 | It advises. It never acts |
| 8 | Switch a pack off | 6:30 | 1:00 | The platform argument, as one gesture |
| 9 | Close | 7:30 | 0:20 | Name what was not shown |

---

## 1 · Today — 0:00, fifty seconds

**Show.** `http://localhost:3000`. It opens on Today. Do not navigate anywhere.

**Say.**

> This is where it opens. Not a prompt box — a household is busy and does not know what to
> ask, so it tells you first. Everything here is in order of urgency: anything overdue, any
> threshold crossed, any renewal coming up. Most days this screen should be nearly empty, and
> an empty Today is the system working rather than a blank page.

**Watch for.** If Today is empty, the corpus did not load. Go to Vault, confirm documents are
there, and continue from step 2 — do not stand in front of an empty screen explaining what
would have been on it.

---

## 2 · The source chip — 0:50, forty seconds

**Show.** Press the source chip on the top row. It reads a document name and a page —
`Motor renewal notice · p.1`. The page opens, drawn, with the row still behind it. Close it.

**Say.**

> That is the whole product in one gesture. Every row names the document and the page it came
> from, and pressing it shows you that page. Nothing on this screen asks you to take its word
> for it. Checking a claim does not cost you the claim — the row is still there behind it.

**Watch for.** If the panel says *"The file is not in your inbox any more"*, the batch was
loaded but the files were moved. That is a correct message, not a crash — say so and move on;
it is honest behaviour and it takes four seconds to explain.

---

## 3 · Drop a document in — 1:30, seventy seconds

**Show.** Drag the staged document from the desktop into the repository's `inbox/` folder.
Return to the browser. Wait. It appears in Vault within five to fifteen seconds.

**Say,** while it is working —

> That is the upload. There is no upload button, because the moment you ask a household to
> log into something and press Choose File, they stop. A watched folder, or a photo sent to a
> Telegram bot — the same interface underneath, `receive(bytes, mime, sender, ts)`.
>
> What is happening in those few seconds: it is parsed, classified against an installed pack,
> embedded, and the fields the pack declares are read off it with the page each one was
> printed on. If the same file arrives twice under two names it updates in place — the key is
> a hash of the bytes, not the filename.

**If it does not appear.** Do not wait past twenty seconds. Say *"this one is queued behind
the worker — it will be in Vault by the time we get there"* and move to step 4. **This is the
most fragile step in the demonstration and it is the one to cut** if the earlier steps ran
long.

---

## 4 · Ask, and get an answer — 2:40, eighty seconds

**Show.** Ask. Type exactly:

```
when does the car insurance renew?
```

Let it stream. Do not talk over the first sentence — let the room watch it arrive with its
chip attached.

**Say,** once two sentences have landed —

> Each sentence carries its own sources, not a list of references at the end. That matters:
> you can put a finger on one sentence and see the page behind that sentence.
>
> And a sentence that cannot be traced to one of your documents is never shown. Not shown and
> then withdrawn — never shown at all. The gate runs before the sentence reaches the screen.

**Watch for.** Slow decode. On the benchmarked machine the generator writes about 79 tokens a
second with a full context window, so a four-sentence answer takes a few seconds. That is
normal and worth naming rather than apologising for: it is a 4-billion-parameter model on the
presenter's own graphics card, and nothing left the machine.

---

## 5 · Vault — 4:00, fifty seconds

**Show.** Vault. Open one document. The facts read off it, each with its page. Then scroll to
the quarantined document.

**Say.**

> Everything it has filed, and for each document the facts it read with the page each came
> from. You can check any of them against the page in about two seconds.
>
> And this one it could not read at all. It is not gone and it is not silently dropped — it is
> queued, with the reason. Retry sends the *page image* to the vision model instead of the
> parsed text, which is a second pass at the same document through a different sense. We report
> that as a recovery rate, not as a success.

**Watch for.** Do not press Retry. It takes about thirty seconds and it queues, so pressing it
buys dead air and no visible result inside the slot.

---

## 6 · The abstention — 4:50, one minute

**This is the step the demonstration exists for.** Slow down here. If the room only remembers
one screen, it should be this one.

**Show.** Ask. Type exactly:

```
what is my electricity bill for March?
```

**Expect** a reply of the shape:

> I can't answer that from your documents: *(the reason it gives)*. *(the document that would
> have answered it)*

**Say,** after a pause long enough for the room to read it —

> There is no electricity bill in this household's documents, so it says so, and it names what
> would have answered the question. It did not compose a plausible amount.
>
> That is the whole project. A system like this is not useful because it answers — it is useful
> because you can believe the answers, and you can only believe them if it is willing to say no.
> Every one of those refusals is a question it could have answered plausibly and wrongly.
>
> We measure this. The headline number in the evaluation is not accuracy, it is the abstention
> rate on a set of questions the corpus genuinely cannot answer.

**Why this question.** Neither installed pack covers utilities, so there is no document of that
type for any batch — the abstention is structural rather than lucky, and it survives a corpus
change. **Do not substitute a question you have not tried on the presenting machine with the
loaded batch.**

**A stronger variant for a technical audience,** if the room is the kind that will suspect the
easy case: ask for a field the register leaves blank on a document type the pack *does* cover —
an excess on a policy schedule that does not print one. It abstains inside its own domain,
which is the harder and more convincing case. Rehearse it before choosing it; it depends on the
batch.

**If it answers anyway.** Stop. Say *"that is the failure this project exists to prevent, and it
is the one thing we would want you to see"* — then show the sentence and its chip, and note that
it is a reportable finding. Do not paper over it. An honest failure demonstrated is worth more
than a smooth run, and the room will know.

---

## 7 · The refusal to act — 5:50, forty seconds

**Show.** Ask. Type exactly:

```
renew my insurance policy and pay the premium
```

**Expect,** verbatim:

> I can explain what your documents say, but I do not act on them. This version never pays,
> renews, books or files anything — that is enforced in the code, not left to my judgement.

**Say.**

> It refuses to act, and note *where* it refuses: at the top of the graph, before retrieval
> runs. It did not go and look and then decline.
>
> Every pack manifest declares `never_acts: true`, and the type system will not accept any
> other value — a pack that says otherwise does not load. Version one advises. It does not pay,
> book or file. That is a boundary we can point at in the code, not a promise about the model's
> judgement.

---

## 8 · Switch a pack off — 6:30, one minute

**Show.** Packs. Both are listed with what each recognises and what it has found. Switch
**Insurance and Coverage** off. A banner names what that just did. Go to Today.

**Say,** on Today —

> Its reminders are gone. The insurance documents are hidden from the vault, and Ask will not
> cite them — it will abstain on a question it could have answered a moment ago.
>
> Nothing was deleted. That is what switching a subject off is supposed to mean.

Switch it back on. Return to Today. The rows are back.

> And nothing in the engine changed to make that work. The registry is read once per request
> and handed to the modules and to retrieval, and neither of them knows a screen exists. A pack
> is one YAML file — a third subject appears on that screen because somebody dropped a file in,
> not because anybody edited the interface.
>
> That is the expansion model. Insurance and Tax are the two we built. Utilities, school fees,
> season parking are the same shape.

**Watch for.** **Switch it back on before leaving this screen.** A pack left off silently
breaks the next rehearsal, and it will be blamed on something else for twenty minutes.

---

## 9 · Close — 7:30, twenty seconds

**Say.**

> Everything you just saw ran on this laptop. No document, no question and no answer went to a
> cloud service — that is a property of how it is built, not a setting.
>
> And what you did not see: it never paid anything, never booked anything, and twice it told me
> no.

Stop. Do not offer to show one more thing.

---

## The four things that lose the room

1. **Talking over the stream.** The per-sentence citations arriving is the most persuasive
   four seconds in the demonstration. Let them happen in silence.
2. **Apologising for the speed.** It is a 4B model on a consumer graphics card and nothing left
   the machine. Name that as the trade it is.
3. **Explaining the architecture at step 1.** The architecture lands at step 8, after they have
   seen the thing work. Before that it is a diagram about software.
4. **Recovering a failure by talking.** If a step fails, say what failed in one sentence and go
   to the next step. The run sheet is ordered so that any single step can be dropped without
   breaking the one after it — except step 6, which is why it is fifth from the end rather than
   last.

---

## The backup

The W9 task asks for a three-minute screen recording of the happy path, on a USB stick,
playable on a machine that is not the presenter's. Record it **on frozen code, after the third
rehearsal** — a recording made before the freeze shows a build that no longer exists.

It ends on the abstention. If the live demonstration dies, the recording is what the room sees,
and the last thing it should show them is the system saying no.
