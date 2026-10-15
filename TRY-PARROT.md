# Try PARROT

For the five of us, to run PARROT on our own machines and actually use it. You do not need
to understand the code, and you do not need to be in your own lane to do this.

Everything runs **on your computer**. No document, no question and no answer is sent to a
cloud service.

---

## 1 · Install five things

Install these once. All five are free.

| | What | Where | Why |
|---|---|---|---|
| 1 | **Docker Desktop** | <https://docs.docker.com/desktop/> | Runs the database |
| 2 | **Ollama** | <https://ollama.com/download> | Runs the AI models locally |
| 3 | **Python 3.12** | <https://www.python.org/downloads/> | Runs PARROT. On Windows tick **"Add python.exe to PATH"** |
| 4 | **uv** | <https://docs.astral.sh/uv/getting-started/installation/> | Installs the Python packages |
| 5 | **Node.js 20 or newer** | <https://nodejs.org/> — take the LTS | Runs the screens |

On Windows, `uv` installs with one line in PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then **start Docker Desktop and leave it running.** Ollama starts itself and sits in the
system tray. Both must be running before PARROT will work.

> **Intel Macs are not supported.** `torch 2.14.0` publishes no macOS x86_64 wheel, and
> `docling-parse 7.22.1` has to be compiled from source there, so `uv sync` fails.
> Use Windows 11 with an NVIDIA GPU (the tested path) or an Apple Silicon Mac [VERIFY: not yet tested].

---

## 2 · Download the AI models

About **6 GB** in total, downloaded once. In a terminal:

```bash
ollama pull hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M
ollama pull embeddinggemma:300m
ollama pull hf.co/gpustack/bge-reranker-v2-m3-GGUF:latest
```

All three are needed. The first reads and writes, the second is how documents are searched,
the third picks the best passages. The first one is also what reads a *photograph* of a
document, which is why it is a vision model.

> Go and make coffee. This is the slow step, and it only happens once.

---

## 3 · Get the code and set it up

```bash
git clone https://github.com/feynman82/igd-capstone-2026.git
cd igd-capstone-2026

docker compose -f infra/docker-compose.yml up -d
uv sync --python 3.12 --extra dev
docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot < db/migrations/0001_init.sql
docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot < db/migrations/0002_household.sql
docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot < db/migrations/0003_advice.sql
docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot < db/migrations/0004_calendar.sql
```

Then the screens:

```bash
cd web
npm ci
cd ..
```

Line by line: start the database, install the Python packages, create the tables (every file
in `db/migrations/`, in order — there are four today), install the interface.

The migration lines use the database *inside* Docker, so you do not need to install `psql`
yourself. On Windows run them from **Git Bash** or **WSL** rather than `cmd`, because `<` works
differently there. In PowerShell use this instead, once per migration file:

```powershell
Get-Content db/migrations/0001_init.sql | docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot
Get-Content db/migrations/0002_household.sql | docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot
Get-Content db/migrations/0003_advice.sql | docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot
Get-Content db/migrations/0004_calendar.sql | docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot
```

You do **not** need a `.env` file. The defaults already match the Docker setup. Copy
`infra/.env.example` to `.env` only if you want to change a port or a model.

---

## 4 · Put some documents in

Desmond's synthetic corpus is **already in the repository** under `corpus/batches/` — it is
generated from an invented canon with no person behind it, which is what makes committing it
safe. Load a batch with:

```bash
make corpus-load BATCH=batch1
```

That copies the batch's documents into the `inbox` folder, where the engine picks them up
when it starts in step 5. Loading the same batch twice does not duplicate anything.

Want to try your own? Put any PDF or photo of a bill, payslip or insurance letter into the
`inbox` folder in this repository. That is genuinely all the "upload" there is.

---

## 5 · Run it

Two windows. The engine, then the screens.

**Window one — the engine.** On Windows, double-click **`START.cmd`** in the root of the
repository. Everything else:

```bash
make dev
```

That one window starts four things: the engine, the folder watcher, the ingestion worker, and
the screens. It prints a line for each. Then a browser tab opens at
**<http://localhost:3000>**. That is PARROT.

The first load takes twenty seconds or so — the interface compiles itself the first time it
is asked for a page, once per start. After that it is immediate.

The engine also has a page of its own, at <http://127.0.0.1:8000>. It is not the product: it
is the setup page, and it tells you whether the database, Ollama, the three models and the
screens are all found. **If something is missing, this page names it.** If the screens did not
open, this is the page the browser lands on instead, and the row to read is *Household
interface*.

Leave the window open. It is watching the `inbox` folder: anything you drop in there is read
within a few seconds. A document takes roughly five to fifteen seconds depending on your
graphics card.

> **If a port is already taken.** 8000 often is — Docker Desktop binds `127.0.0.1:8000` on
> some machines — and 3000 is the most contested port on a developer's laptop. `START.cmd`
> says `Cannot use local port 8000` for the first, and for the second it quietly uses whatever
> is already on 3000 rather than fighting it.
>
> Move PARROT in `.env` at the repository root, and only there:
>
> ```
> PARROT_PORT=8010
> PARROT_WEB_PORT=3100
> ```
>
> The engine tells the screens which port it got, so there is no second file to keep in step.
> `.env` is per-machine and is not committed, so your ports are yours.

To stop PARROT, press **Ctrl+C** in that window. The screens and the worker stop with it.

---

## 6 · Use it

At <http://localhost:3000>, the first thing you get is **Choose a passphrase**.

That is a local passphrase for this computer — not an account, and nothing is sent anywhere to
check it. Pick something you will remember. It keeps your session for twelve hours.

> It locks the **screen**, and nothing more. It does not encrypt anything: the documents are
> still in the `inbox` folder and the facts are still in Postgres, and anyone who can open a
> terminal on this machine can read both without going near the browser. What it buys is that a
> laptop left open in a kitchen does not show a stranger the household's policy numbers.
>
> Forgotten it? Delete `web/.parrot/lock.json` and choose a new one. It guards a screen, not a
> key to any data, so nothing is lost.

Then there are four surfaces down the side.

### Today — where it opens

Not a prompt box, deliberately. You are busy and you do not know what to ask, so PARROT tells
you first: anything overdue, any threshold crossed, any renewal coming up — already in order of
urgency.

**Press a source chip on any row.** That is the whole product in one gesture. The chip names a
document and a page — *"Motor renewal notice, p.1"* — and pressing it shows you that page,
drawn, with the row still behind it. Nothing on this screen asks you to take its word for it.

Most days it should say nothing needs you. That is the system working, not an empty screen.

### Ask — a question about your own documents

```
when does the car insurance renew?
```

The answer arrives a sentence at a time, and **each sentence carries its own sources**. A
sentence that cannot be traced to one of your documents is never shown at all — not shown and
then withdrawn, never shown.

**Now try to make it lie.** This is the interesting part, and the thing worth reporting back:

```
what is my electricity bill for March?
```

If you have no electricity bill, it must say so and name what would have answered it — **not**
invent a plausible number. That refusal is the point of the whole project, so treat a clean
abstention as a pass, not a failure.

```
renew my insurance policy and pay the premium
```

It must refuse to act. PARROT explains what your documents say; it never pays, renews, books or
files anything. That is enforced in the code, not left to the model's judgement.

### Vault — everything it has filed

Every document, its status, and the facts read off each one with the page each came from. Open
a document to see what PARROT believes about it and check it against the page.

Anything it could not read at all shows here too, with the reason. **Retry** sends the page to
the vision model as an image and tries again — useful for a phone photo or a faint scan. It
takes half a minute, so it queues rather than making you wait.

### Packs — what this assistant knows about

A pack is a subject PARROT understands: Insurance, Tax. Each one lists what it recognises and
what it has found so far.

**Switch one off.** Go back to Today and its reminders are gone; go to Vault and its documents
are hidden; ask a question and it will not answer from them. Switch it back on and everything
returns. Nothing was deleted — that is what turning a subject off is supposed to mean, and it
is worth seeing once.

### Without the screens

Everything above works from a terminal too, which is handy if the UI will not start. Leave
window one running and open another terminal in the repository:

```bash
uv run python scripts/today.py                                    # what needs you
uv run python scripts/ask.py "when does the car insurance renew?" # ask; no argument = a session
uv run python scripts/quarantine.py                               # what could not be read
```

The screens and these commands call exactly the same code, so they cannot disagree about what
is due today. The raw JSON is on the engine's port as well — `/api/today`, `/api/ask`,
`/api/vault`, `/api/packs`, `/api/quarantine` — loopback only, refused from any other machine.

---

## If something goes wrong

| What you see | What it means |
|---|---|
| The setup page lists a component as missing | Start Docker Desktop, or start Ollama, or run the `ollama pull` commands from step 2 |
| `Cannot use local port 8000` | Something else is on it, often Docker Desktop. Set `PARROT_PORT` in `.env` — see the note in step 5 |
| `Cannot reach the local database` | Docker Desktop is not running, or `docker compose ... up -d` was not run |
| `Python is missing` | Install Python 3.12 and tick "Add python.exe to PATH", then reopen the terminal |
| **"Parrot is not running on this computer"** on every screen | The engine stopped. Close the PARROT window and double-click `START.cmd` again |
| `Screens: not started. Dependencies are not installed` | You skipped `npm ci` in `web/`. Run it once; everything else started without it |
| `Screens: already running on http://localhost:3000` | Another Next app has the port. PARROT used it rather than starting a second one — if it is not PARROT, stop it, or set `PARROT_WEB_PORT` in `.env` |
| **You forgot the passphrase** | Delete `web/.parrot/lock.json` and choose a new one. Nothing is lost |
| **Today is empty** | Either nothing is due — which is the normal state — or no documents have been read yet. Check Vault |
| Answers are very slow | Expected on a laptop without a discrete GPU. It is a 4B model running on your own machine |
| **On a Mac**, the window repeats `exited with 'signal 6 (SIGABRT)'` and every document stays pending | Your copy predates 14 September. `git pull`, then start PARROT again — the worker now uses a pool that is safe on macOS. If you were running the worker by hand with `--pool=solo`, you can stop doing that |
| It abstained and you think it should not have | **Tell Yew Mun.** That is an evaluation finding, not a bug report |
| It answered something it could not support | **Tell everyone immediately.** That is the one failure the project exists to prevent |

---

## What to report back

You are the first people to use this, so what you notice is worth more than another test.

- A question it should have answered and did not → Yew Mun (Lane B)
- A document type no pack recognises → Zee (Lane D)
- A screen that was confusing, or a source chip that did not open → Zee (Lane D)
- A document it could not read at all → Desmond (Lane E)
- Anything it said that it could not back up with a citation → **Christian, straight away**
- Anything that made you uneasy about privacy or what it keeps → Siew (Lane C)

---

## Want to work on it, not just try it?

This page is for trying PARROT. To build on it, see [`FIRST-RUN.md`](FIRST-RUN.md) for the
developer setup, then open Claude Code in the repository and run **`/orient`** — it will read
the working agreement, find your lane, and tell you your next task.


