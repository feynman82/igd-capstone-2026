# Try PARROT

For the five of us, to run PARROT on our own machines and actually use it. You do not need
to understand the code, and you do not need to be in your own lane to do this.

Everything runs **on your computer**. No document, no question and no answer is sent to a
cloud service.

---

## 1 · Install four things

Install these once. All four are free.

| | What | Where | Why |
|---|---|---|---|
| 1 | **Docker Desktop** | <https://docs.docker.com/desktop/> | Runs the database |
| 2 | **Ollama** | <https://ollama.com/download> | Runs the AI models locally |
| 3 | **Python 3.12** | <https://www.python.org/downloads/> | Runs PARROT. On Windows tick **"Add python.exe to PATH"** |
| 4 | **uv** | <https://docs.astral.sh/uv/getting-started/installation/> | Installs the Python packages |

On Windows, `uv` installs with one line in PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then **start Docker Desktop and leave it running.** Ollama starts itself and sits in the
system tray. Both must be running before PARROT will work.

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
```

Line by line: start the database, install the Python packages, create the tables.

The third line uses the database *inside* Docker, so you do not need to install `psql`
yourself. On Windows run it from **Git Bash** or **WSL** rather than `cmd`, because `<` works
differently there. In PowerShell use this instead:

```powershell
Get-Content db/migrations/0001_init.sql | docker compose -f infra/docker-compose.yml exec -T db psql -U parrot -d parrot
```

You do **not** need a `.env` file. The defaults already match the Docker setup. Copy
`infra/.env.example` to `.env` only if you want to change a port or a model.

---

## 4 · Put some documents in

Desmond's synthetic corpus is **not in the repository** — it is too large for git and is
handed over separately. Once you have a batch, put the folder in `corpus/batches/` and:

```bash
make corpus-load BATCH=batch1
```

No batch yet? Put any PDF or photo of a bill, payslip or insurance letter into the `inbox`
folder in this repository. That is genuinely all the "upload" there is.

---

## 5 · Run it

**On Windows, double-click `START.cmd` in the root of the repository.**

Everything else:

```bash
make dev
```

Your browser opens at <http://127.0.0.1:8000>. That page shows whether the database, Ollama
and the models are all found — **if something is missing, this page tells you which one**.

Leave that window open. It is watching the `inbox` folder: anything you drop in there is read
within a few seconds. A document takes roughly five to fifteen seconds depending on your
graphics card.

To stop PARROT, press **Ctrl+C** in that window.

---

## 6 · Use it

There is no product interface yet — that is Zee's lane and it is being built. For now, open a
**second** terminal in the same folder, leaving PARROT running in the first.

**What needs me today?**

```bash
uv run python scripts/today.py
```

Renewals coming up, thresholds crossed, anything overdue — in order of urgency, each one
naming the document and page it came from.

**Ask about your own documents**

```bash
uv run python scripts/ask.py "when does the car insurance renew?"
```

Every sentence comes back with the document and page behind it. Run it with no question for a
back-and-forth session.

**Try to make it lie.** This is the interesting part, and the thing worth reporting back:

```bash
uv run python scripts/ask.py "what is my electricity bill for March?"
```

If you have no electricity bill, it should say so and name what would have answered it —
**not** invent a number. That refusal is the point of the whole project.

```bash
uv run python scripts/ask.py "renew my insurance policy and pay the premium"
```

It must refuse to act. PARROT explains; it never pays, books or files anything.

**What could not be read?**

```bash
uv run python scripts/quarantine.py
```

Documents that defeated the parser, and why. `--retry` sends the page as an image to the
vision model and tries again.

**What has it got?**

```bash
curl http://127.0.0.1:8000/api/vault
```

Every document, its status, and the facts read off it. Also available: `/api/today`,
`/api/packs` and `/api/quarantine`. These are loopback only — they refuse a request from any
other machine.

---

## If something goes wrong

| What you see | What it means |
|---|---|
| The page lists a component as missing | Start Docker Desktop, or start Ollama, or run the `ollama pull` commands from step 2 |
| `Cannot use local port 8000` | Something else is on that port. Close it, or run `uv run python scripts/run_parrot.py --port 8011` |
| `Cannot reach the local database` | Docker Desktop is not running, or `docker compose ... up -d` was not run |
| `Python is missing` | Install Python 3.12 and tick "Add python.exe to PATH", then reopen the terminal |
| Answers are very slow | Expected on a laptop without a discrete GPU. It is a 4B model running on your own machine |
| It abstained and you think it should not have | **Tell Yew Mun.** That is an evaluation finding, not a bug report |
| It answered something it could not support | **Tell everyone immediately.** That is the one failure the project exists to prevent |

---

## What to report back

You are the first people to use this, so what you notice is worth more than another test.

- A question it should have answered and did not → Yew Mun (Lane B)
- A document type no pack recognises → Zee (Lane D)
- A document it could not read at all → Desmond (Lane E)
- Anything it said that it could not back up with a citation → **Christian, straight away**
- Anything that made you uneasy about privacy or what it keeps → Siew (Lane C)

---

## Want to work on it, not just try it?

This page is for trying PARROT. To build on it, see [`FIRST-RUN.md`](FIRST-RUN.md) for the
developer setup, then open Claude Code in the repository and run **`/orient`** — it will read
the working agreement, find your lane, and tell you your next task.
