# Starting Parrot

On Windows, double-click `START.cmd` in the repository root. The window stays open so
you can read setup problems. It works independently of the terminal's current directory.
It uses the project's Python environment, or Python on PATH for initial diagnostics.
It does not require enabling PowerShell scripts or changing execution policy.

**Current build stage:** double-click startup opens the startup page at
`http://127.0.0.1:8000` within a second **and starts watching the inbox folder**. The page shows
what Parrot is waiting for — the database, filing, the screens and the local model — and moves to
Today by itself once the database and the screens answer; if something is not coming by itself,
that row turns into a sentence saying what to do. While it waits, the local model is loaded in
the background, and the page says whether it landed on the graphics card or the processor. The
dependency table that used to be the whole page is at `/setup`. A document dropped in is
registered, parsed, classified against an installed pack, and either indexed with cited facts
or sent to quarantine with a reason. `scripts/ask.py` answers questions from it with a document
and a page, or abstains. `scripts/today.py` shows what the Reminder and Alert modules have to
say.

The household interface is built: Today, Ask, Vault and Packs are screens under
`web/app/(app)/`, served by a **separate Next.js process** that the launcher starts beside the engine —
see "The screens" below. The pages at `http://127.0.0.1:8000` are the engine's startup page and
its setup diagnostics; they are not the product and never will be.

**After a change to chunking or embedding, rebuild the vault's vectors once:**

```powershell
uv run python scripts/reindex.py
```

It re-parses each indexed document from the inbox, re-chunks it and re-embeds it, and leaves its
facts, obligations and corrections alone. A vault embedded the old way is not searchable the new
way — queries and passages must be embedded alike — so questions answer badly until it has run.
On a processor-only machine it takes a minute or two per long document, mostly parsing.

Hybrid retrieval is still Lane B's and is not built yet. `core/retrieve/` holds a README, and
both `scripts/ask.py` and `api/routes.py` import `DenseRetriever` and `NoReranker` from the
dense-only stopgap in `core/graph/baseline.py`. So answer *quality* is still not a number
anybody should quote — the mechanism works, the ranking is naive on purpose, and the numbers
come from Yew Mun's harness against a golden set.

The Python environment must already contain the project dependencies. No `.env` is
required for diagnostics: the defaults use local services and the example credentials.
For custom local configuration, copy `infra/.env.example` to `.env`. Process environment
variables override file values. File values are literal; shell commands and variable
substitution are never evaluated. Do not put inline comments after values.

If the environment is missing, install Python 3.12 and uv, then run
`uv sync --python 3.12 --extra dev`. Start Docker Desktop and Ollama separately when
checking real dependencies. To start the database and broker from the repository root:

```powershell
docker compose -f infra/docker-compose.yml up -d
```

This command may download container images. The launcher itself does not run it.
An existing database must have the reviewed migration applied by the integration owner;
the diagnostic server only reads schema metadata and never applies migrations.

To restart or stop Parrot from the screens, use **Power** in the header. Restart stops the engine
and starts a fresh one with whatever code is on disk, while the screens stay open and reconnect;
Shut down stops the engine, the ingestion worker, its nightly schedule and the screens, and the
`START.cmd` window closes with it. Neither touches PostgreSQL, Redis or Ollama.

Keep the Parrot terminal open. Press Ctrl+C there to stop the diagnostic server. Existing
PostgreSQL, Redis and Ollama services are not stopped. A second launch refuses a busy port
instead of attaching to an unknown process. For another port or no browser launch:

```powershell
uv run python scripts/run_parrot.py --port 8001 --no-browser
```

For a check that exits without waiting for a key, run:

```bat
START.cmd -CheckOnly
```

For `-CheckOnly`, exit code `0` means startup files are present (not a health guarantee),
`2` means setup or implementation is incomplete, and `1` means a launcher error.
Diagnostics print locally; they do not upload information, read household documents,
print `.env` values, download models, install tools, or change service configuration.
Installed tools are reported separately from runtime readiness.

## The screens

`START.cmd` starts them. They are still a separate process — a Next.js server, which fails
and restarts on its own schedule and must not be able to take the engine down with it — but
it is a child of the one you double-clicked, it is stopped with it, and the browser opens on
it rather than on the engine's setup page.

The one thing to do once, before the first start:

```powershell
cd web
npm ci          # first time only, a couple of minutes
```

Without it the Parrot window says so and starts everything else. The screens are on
<http://localhost:3000>; change it with `PARROT_WEB_PORT` in `.env`. You no longer have to
keep `PARROT_API_URL` in `web/.env.local` in step with `PARROT_PORT`: the engine passes its
real port to the screens when it starts them, and Next.js does not override a variable that
is already set. Set `PARROT_API_URL` yourself only when you are running `npm run dev` by hand.

To run them yourself — a second window, a different port, or a production build — start the
engine with `--no-web`. If something is already listening on the port, `START.cmd` leaves it
alone and uses it rather than fighting for the port.

The screens call the same code as `scripts/today.py`, `scripts/ask.py` and
`scripts/quarantine.py`, so they cannot disagree with the terminal about what is due today.
`TRY-PARROT.md` walks through using them; this file is about starting them.

## Dropping a document in

With the database running, `START.cmd` watches `inbox/` at the repository root. Change it
with `WATCH_FOLDER` in `.env`; a relative path is resolved against the repository root.

Drop a file in and the Parrot window prints one line:

```
filed: renewal.pdf [application/pdf] -> d7b451f8-8f19-487a-8ab4-7197cf6cb036
```

Drop the same document in again, under any name, and it prints `already filed` with the
same document id. The SHA-256 of the bytes is the identity, so a file renamed, re-downloaded
or sent through a second channel is recognised as the document it already is.

A file is registered a few seconds after it stops changing, never while it is still being
written, and names that mean "in progress" (`.part`, `.crdownload`, `.tmp`, a leading `.`
or `~$`) are skipped entirely. See
[ADR 0005](adr/0005-polling-the-watched-folder.md) for why this polls rather than subscribing
to filesystem events.

To watch the folder without the web server:

```powershell
uv run python scripts/watch_folder.py
```

The first PDF or photograph takes a minute or two: Docling downloads its layout and OCR
models once, then caches them. Text and markdown need neither.

## Reading a document

Registration is followed by the pipeline, in one transaction:

```
Docling parse → classify against the installed packs → schema-constrained extraction
                                                     → chunks + facts, committed together
```

The window prints one line per document:

```
filed: payslip-2026-01.pdf [application/pdf] -> b22f5bc6-…
  indexed as iras_tax.payslip: 2 page(s), 2 chunk(s), 6 cited fact(s)
```

Every fact carries the page it was printed on. A value the model reports that appears on **no**
page is dropped rather than stored — if it was required, the whole document goes to quarantine
rather than being half-written.

### Quarantine, and the second pass

```powershell
uv run python scripts/quarantine.py           # what needs your eyes, and why
uv run python scripts/quarantine.py --retry   # send the page images to the model
```

A document the parser could not read is not dropped; it queues. `--retry` renders its pages and
sends them to the vision-language model, which reads pixels rather than the text a parser
managed to recover, and then holds the result to exactly the same pack schema. The run prints a
recovery rate. One observed run: a scan Docling recovered nothing from came back with five cited
fields.

The retry matches quarantined rows to files by SHA-256, so the original must still be in the
inbox. See [ADR 0006](adr/0006-pypdfium2-for-the-quarantine-image-pass.md).

A quarantined document whose file has **left** the inbox cannot be retried, so it no longer
counts as something that needs you: Today mentions it in one quiet line, and the Vault lists it
under "No longer in the inbox" with **Forget it**, which removes Parrot's record of it
(`DELETE /api/quarantine/{id}`). Your files are not touched. A document whose file is still in the
inbox is not forgotten — capture would register it again within a minute — so take it out first.

## Asking a question

```powershell
uv run python scripts/ask.py "how much was the gross salary on the payslip?"
```

```
The gross salary on the payslip was SGD 8900.00. [payslip-2026-01.pdf, page 1]

Sources: payslip-2026-01.pdf, page 1

Informational analysis of your own documents and published IRAS guidance. This is not tax
advice. Verify against IRAS before filing.
```

Ask something the documents do not cover and it says so, with the reason and the pack's own
floor:

```
I can't answer that from your documents: the closest document is not close enough
(best match 0.21, this pack answers above 0.42).
```

Ask it the way you would say it. Before searching, one model call writes the question out whole
and adds two or three searches in the documents' own words, so "warded for 1 night, can claim?"
finds the inpatient clause that "hospitalised" would. Follow-ups work in the Ask screen and in
`scripts/ask.py`'s interactive mode: "when does it expire?" after asking about the car policy is
answered as a question about the car policy. The conversation is only used to understand the
question; an earlier answer is never cited. See ADR 0013.

"My dad's…", "my son's…" and "my wife's…" questions are answered from that household member's
documents, once they are placed on the Household page with that relation. If nobody holds the
relation yet, Parrot says it does not know who that is, rather than answering from yours.

Ask it to *do* something and it refuses at the router, before retrieval is attempted:

```
I can explain what your documents say, but I do not act on them. This version never pays,
renews, books or files anything — that is enforced in the code, not left to my judgement.
```

Retrieval here is the dense-only stopgap in `core/graph/baseline.py`. It exists so the graph can
be demonstrated before Lane B's hybrid search lands, and it is **not** a baseline measurement —
see [ADR 0007](adr/0007-the-graph-ships-before-retrieval-and-before-a-checkpoint-table.md).

## Today

```powershell
uv run python scripts/today.py
uv run python scripts/today.py --as-of 2026-11-20   # walk forward in time
uv run python scripts/today.py --dry-run            # show it without recording it
```

Reminder sweeps the obligations a pack declared — insurance warns at 60, 30 and 7 days — and
says each window once. Running it twice on the same day says nothing the second time; running it
again when the next window opens speaks again. Alert fires a pack-declared threshold once per
debounce window and cites the documents behind the figure.

## Telegram

Capture from a phone, through the same interface as the folder. **`START.cmd` starts it**, beside
the folder watcher, whenever a bot token is configured — there is no second window to remember.

It needs a bot token, which takes about ten minutes and no business verification: message
**@BotFather** on Telegram, send `/newbot`, give it a name, and it replies with a token. Put
`TELEGRAM_BOT_TOKEN=<that token>` in `.env` at the repository root and restart Parrot. `.env` is
git-ignored and must stay that way — the token is a household secret.

Three settings, all in `.env`, all optional except the first:

| Key | Default | What it does |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | unset | Unset means Telegram capture stays off and only the folder is watched |
| `TELEGRAM_CHAT_IDS` | empty | Comma-separated chat ids the bot accepts from. Empty means any chat. ADR 0011 |
| `TELEGRAM_DELETE_AT_SOURCE` | `true` | `false` keeps the message in the chat after it is filed, which is useful while you are watching what arrives |

The allow list is configuration rather than a command-line flag because the launcher starts the
capture: an allow list that lives only in a command line is one a double-click cannot honour.

The Parrot window says which of the two it is on startup — `Telegram capture: on.` or
`Telegram capture: off.` — and the startup page carries the same row, with a count of how many
documents have actually arrived on this channel. That count is the honest test: a bot that
connects and files nothing looks exactly like a bot that was never started.

Long polling, not a webhook: the laptop makes a request *out*, nothing listens on a public port,
and no tunnel or hosted endpoint is involved. A photograph is written into the inbox, registered,
read, and then **deleted at source**, so Telegram does not keep a copy on the household's behalf.

### The script is now the diagnostic

```powershell
uv run python scripts/telegram_bot.py --check   # names the bot and exits
uv run python scripts/telegram_bot.py           # capture until Ctrl+C, without the launcher
```

`--check` is the one thing the startup page deliberately does not do: it calls `getMe`, and a
diagnostic that reaches out to Telegram on every poll of a page is not the privacy claim
`docs/governance/` makes.

**Do not run the script while Parrot is running.** Telegram gives a bot's messages to one poller,
and the second one gets HTTP 409 — which is also what you get if a webhook was ever set on the
bot. Both now say so in as many words rather than repeating "poll failed"; clear a webhook with
the Bot API's `deleteWebhook`.

`--chat-id` and `--keep-at-source` still override `.env` for a single run of the script.

## Startup integration contract

`scripts/run_parrot.py` accepts `--bind-address 127.0.0.1` and starts only the setup server
at this stage. Other bind addresses are rejected. Its socket is owned before the browser
opens. The HTTP endpoints have distinct meanings:

- `/healthz`: HTTP 200 means the diagnostic API is alive.
- `/readyz`: **always** HTTP 503 with `ready: false` and `stage: setup`. It is hardcoded, and
  it does not turn true when the screens are running — this server supervises the engine and
  the worker, never the Next.js process, so it is in no position to declare the product ready.
  Read it as "the setup stage is still the stage", not as a health signal. Checks are read-only
  and cached for five seconds.
- `/`: the startup page. It polls `/api/system`, never waits on the checks to render, and runs
  only its own nonce-tagged script; nothing on it leaves the machine.
- `/setup`: the human-readable setup page. It remains usable when dependencies are unavailable.
- `/api/system`: the checks, whether the engine can restart itself, whether the local model is
  loaded and where (`gpu`, `partial`, `cpu`), and where the screens are.

Database checks verify PostgreSQL 17, pgvector and base-table presence, not every column,
constraint or migration state. Model metadata checks do not run inference and therefore
cannot establish successful vision, generation, embeddings or reranking.

## The ingestion worker

Since ADR 0008 the folder watcher does not read documents; it registers them and queues them,
and `scripts/worker.py` reads them. `scripts/run_parrot.py` starts that worker beside the
server and stops it on shutdown, or prints in one line why it could not — an unreachable
broker, or Celery not installed — and capture then falls back to reading documents on the
watcher thread, several seconds each, saying so.

    uv run python scripts/worker.py --beat        # documents, and the nightly sweeps
    uv run python scripts/worker.py --beat-only   # the schedule alone
    uv run python scripts/run_parrot.py --no-worker

On Windows the worker runs the `solo` pool, and `--beat` starts the schedule as a second
process: Celery refuses `worker -B` there.

The setup page distinguishes two failures that look alike. "Queue broker" is whether Redis
answers. "Ingestion worker" is whether anything is listening to it — a reachable broker with
no worker means documents register, queue, and sit there looking filed while nothing reads
them.

Before full application readiness can be enabled, the supervisor must additionally:

- Validate configuration, database schema and required model capabilities.
- Bind the application to loopback by default; reject unsupported access modes.
- Start or reuse verified services and distinguish them from unrelated processes.
- Start the ingestion worker, API and built frontend; report startup failures.
- Open the product interface only after full application readiness checks pass.
- Track owned processes, clean up partial starts and provide a clean shutdown.
- Report missing setup rather than silently downloading software or models.

No runtime implementation should mark the app ready merely because a port responds.
Startup checks must include dependencies and the worker, not just the web server.

## Hardware qualification

Minimum specifications are **unconfirmed**. The existing proposal's 8 GB GPU claim is a
planning estimate, not a supported-device guarantee. A successful startup check is not a
performance benchmark. Exact model artifacts and versions must be fixed before comparing
results. Windows RAM and GPU names are shown locally; GPU memory is not inferred from
Windows' unreliable `AdapterRAM` field.

For each team test machine, record:

| Category | Record |
|---|---|
| Hardware | OS, CPU or Apple chip, RAM, GPU, actual VRAM or unified memory, storage |
| Runtime | Dependency versions, model artifact and quantization, context, concurrency |
| Startup | Installation steps, cold-start time, failures, human assistance needed |
| Ingestion | Time per page for digital PDFs, scans and photographs; quarantine outcomes |
| Questions | Cold and warm first-response and complete-answer latency |
| Resources | Peak system memory, GPU memory, offloading, failures under ingestion load |
| Quality | Retrieval, field accuracy, citation support, answerable coverage and abstention |

Use the same validated corpus batch and questions across devices. Compare individual
changes, preserve original results, and keep the final holdout out of tuning. Report
quality alongside speed so a faster but less reliable configuration does not appear better.
The corpus is authored by Lane E; do not generate household documents in benchmark code.

## Moving a corpus between machines

**The database is a derived artifact. Nobody ships one.** Each of the five runs their own
Postgres in their own Docker, and none of them are networked to each other. What travels is
the corpus batch and the register that describes it; the database is rebuilt from those.

| Input | Where | In git? |
|---|---|---|
| Schema | `db/migrations/0001_init.sql` | yes |
| Services | `infra/docker-compose.yml` | yes |
| Ground truth | `corpus/register/*.csv` | yes |
| Pack definitions | `packs/*/pack.yaml` | yes |
| **The documents themselves** | `corpus/batches/<batch>/` | yes |
| The real-document holdout | `corpus/holdout/` | **no — gitignored, and never committed** |

`corpus/batches/` is committed, so a batch arrives by pulling rather than by a USB stick at
the weekly session. The documents in it are synthetic — generated from an invented canon,
with no person behind them — which is what makes that safe.

Watch the weight. Hundreds of scans and phone photographs are binaries that git stores whole
and forever, so a batch that is pushed is a batch nobody can un-push. Keep the photo tier to
the sample the evaluation actually needs, and raise it at the weekly before pushing a batch
that runs to hundreds of megabytes.

`corpus/holdout/` is the opposite case and is gitignored: 40 real documents from team
members, redacted under the consent protocol. See `NOTICE.md`. Put a batch in
`corpus/batches/<batch>/` and load it:

```bash
uv run python -m corpus.validate corpus/register/batch1.csv   # never load an invalid batch
make corpus-load BATCH=batch1                                 # copy into the watched folder
make dev                                                      # the watcher registers and reads
```

Re-reading the same bytes updates in place, because `documents.sha256` is unique, so loading
a batch twice costs time and changes nothing.

### Three things that decide whether two people's numbers are comparable

**Score against the register, never against a `facts` table.** Extraction is a model call,
not a pure function. `core/runtime/ollama.py` asks for `temperature=0.0` but sets no seed, so
greedy decoding is near-deterministic for one model and quantisation and is *not* guaranteed
identical across different GPUs and drivers. Two people can therefore hold slightly different
`facts` rows for the same document, and only `corpus/register/*.csv` is the same on both
machines. `eval/README.md` already states this — "ground truth comes free" — and it is the
reason evaluation never reads anybody's live database for an expected answer.

**Record the models, not just the scores.** Embeddings depend on the embedding model and its
quantisation; a different pull is a different vector space and therefore a different ranking.
Every file in `eval/results/` names the model, the quantisation and the context length, which
is what the week-1 hardware table is for.

**The holdout is different in kind.** `corpus/holdout/` is 40 real, redacted documents from
team members — personal data under the consent and redaction protocol, scored once in week 8.
It does not travel on the same terms as a synthetic batch, and it is never used for tuning.

## Access and privacy

Confirmed with Christian on 2026-09-10: same-computer access first, then an explicitly
enabled household-network mode. Initial target: local inference and loopback access.
The launcher does not enable LAN access, remote access or cloud inference. It does start
Telegram capture when `TELEGRAM_BOT_TOKEN` is set, and only then: registering a bot is an
explicit act by the household, the poll is a request *out* from the laptop, and media is
deleted at source once filed. With no token configured nothing leaves the machine.
Model/software installation can need internet access, which is separate from processing
documents locally after setup.

A household-network option is the next access target for weaker browser clients. It requires an
explicit design for authentication, transport protection and access to household records
before exposure is enabled. Remote access outside the home and external capture services
need their own documented data paths and user choices. `START.cmd` is Windows-only;
macOS can run `python3 scripts/start_parrot.py --check-only` for preflight, but its
double-click launcher and application runtime remain untested and unimplemented.

## First test machine: Christian's Legion

Inventory recorded on 2026-09-10; this is not a performance result.

| Item | Evidence |
|---|---|
| Laptop | Legion 7 16IRX9, reported by Christian |
| CPU | Core i9-14900HX, reported and confirmed by Windows diagnostics |
| RAM | 32 GB DDR5-5600 reported; Windows reports approximately 31.7 GB available physical capacity |
| OS | Windows 11, AMD64, observed locally |
| Laptop GPU | RTX 4060 Laptop GPU; confirmed demo target; appears in Windows hardware inventory |
| Additional GPU | External RTX 3080, build phase only; NVIDIA reports 10240 MiB VRAM |
| NVIDIA visibility | `nvidia-smi` currently lists only the RTX 3080; laptop GPU execution is unverified |
| Driver | 591.86, reported by NVIDIA |
| Ollama | 0.34.0, observed locally |

Installed candidate model tags observed locally:

- `hf.co/mradermacher/Qwen-SEA-LION-v4-4B-VL-GGUF:Q4_K_M` (local ID `d46a930cafd8`)
- `embeddinggemma:300m` (local ID `85462619ee72`)
- `hf.co/gpustack/bge-reranker-v2-m3-GGUF:latest` (local ID `97902f7b65cf`)

Presence is not validation of generation, vision, embeddings or reranking. Record full
artifact digests when benchmarking. Confirm which GPU actually executes each request;
results using the RTX 3080 cannot be presented as Legion RTX 4060-only results. Resolve
the visibility discrepancy without disabling devices or changing drivers automatically.

Christian confirmed the hardware roles on 2026-09-10:

- **Build:** the external RTX 3080 may accelerate development and experiments. Label
  results as development hardware, not evidence of typical consumer performance.
- **Demo and first consumer baseline:** use the onboard RTX 4060 without assistance
  from the external RTX 3080. Verify actual device use for generation, embeddings,
  reranking and vision retries, including during concurrent ingestion and questions.
- **Minimum specification:** remains unconfirmed. The Legion's CPU and 32 GB RAM also
  matter; passing on this machine does not establish support for weaker laptops,
  GTX 1060/RTX 2060 systems or Apple laptops.

Before accepting a demo benchmark, record the active GPUs and model placement and
confirm the full workflow runs with the external GPU disconnected or otherwise
unavailable to the runtime. Device disconnection is a manual preparation step.

## Local validation notes, 2026-09-11

The setup server was tested on the existing Python 3.13 environment. The repository now
pins new uv setups to Python 3.12 via `.python-version`; Python 3.12 execution remains to
be verified. The current environment was not replaced during the startup build.

Real HTTP checks confirmed API liveness, explicit HTTP 503 assistant readiness, refusal
of a second server on an occupied port, and orderly Ctrl+C shutdown. Ollama returned
metadata for all three configured models; no inference benchmark was performed.

Database and broker integration were verified on 2026-09-11: the compose stack starts,
`db/migrations/0001_init.sql` applies, and all seven base tables are present. A file
dropped into `inbox/` produced a `documents` row, and a copy of it was recognised as
already filed. Redis needed a host-port change on this machine because another project's
Redis already owned 6379: set **`PARROT_REDIS_PORT=6380`** in `.env`, then start the containers
with `docker compose --env-file .env -f infra/docker-compose.yml up -d`.

`PARROT_REDIS_PORT` is the one variable for the broker port and `PARROT_DB_PORT` the one for the
database, and `core/runtime/settings.py` derives the client URL from it. `infra/docker-compose.yml`
publishes the container on it **only when the root `.env` is passed with `--env-file`**: Compose
reads `${...}` from its project directory, which is `infra/`, so without the flag a changed port is
silently ignored and the engine dials a port nothing is listening on — "the queue broker did not
answer", and ingestion dropped to inline. On a machine with no `.env`, leave the flag off: Compose
refuses a file that does not exist, and the defaults already agree. `REDIS_URL` and `DATABASE_URL`
still override outright if you need a different host or database. The earlier failure below is
kept for the record.

Previously, Docker Desktop
failed to start because its transient `sailor-ingest.sock` file could not be accessed.
A targeted cleanup after stopping Docker also failed with the same filesystem error.
Docker must be repaired before starting the project containers and applying the existing
reviewed migration. No factory reset, image removal, volume deletion or schema change was
performed. The diagnostic server remains usable with these dependencies unavailable.
