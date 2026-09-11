# Starting Parrot

On Windows, double-click `START.cmd` in the repository root. The window stays open so
you can read setup problems. It works independently of the terminal's current directory.
It uses the project's Python environment, or Python on PATH for initial diagnostics.
It does not require enabling PowerShell scripts or changing execution policy.

**Current build stage:** double-click startup opens a local setup page at
`http://127.0.0.1:8000` **and starts watching the inbox folder**. A document dropped in is
registered, parsed, classified against an installed pack, and either indexed with cited facts
or sent to quarantine with a reason. `scripts/ask.py` answers questions from it with a document
and a page, or abstains. `scripts/today.py` shows what the Reminder and Alert modules have to
say. The household interface — Today, Ask, Vault and Packs as screens — is Lane D's and is not
built yet, and hybrid retrieval is Lane B's and is not built yet, so answer *quality* is not yet
a number anybody should quote.

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

Capture from a phone, through the same interface as the folder:

```powershell
uv run python scripts/telegram_bot.py --check   # does the token work?
uv run python scripts/telegram_bot.py           # capture until Ctrl+C
```

It needs a bot token, which takes about ten minutes and no business verification: message
**@BotFather** on Telegram, send `/newbot`, give it a name, and it replies with a token. Put
`TELEGRAM_BOT_TOKEN=<that token>` in `.env` at the repository root. `.env` is git-ignored and
must stay that way — the token is a household secret.

Long polling, not a webhook: the laptop makes a request *out*, nothing listens on a public port,
and no tunnel or hosted endpoint is involved. A photograph is fetched, written into the inbox,
registered, read, and then **deleted at source**, so Telegram does not keep a copy on the
household's behalf. `--chat-id` restricts which chat is accepted; `--keep-at-source` turns the
deletion off if you want to see what arrived.

## Startup integration contract

`scripts/run_parrot.py` accepts `--bind-address 127.0.0.1` and starts only the setup server
at this stage. Other bind addresses are rejected. Its socket is owned before the browser
opens. The HTTP endpoints have distinct meanings:

- `/healthz`: HTTP 200 means the diagnostic API is alive.
- `/readyz`: HTTP 503 and `ready: false` mean the household assistant is unfinished,
  even when dependency checks succeed. Checks are read-only and cached for five seconds.
- `/`: the human-readable setup page. It remains usable when dependencies are unavailable.

Database checks verify PostgreSQL 17, pgvector and base-table presence, not every column,
constraint or migration state. Model metadata checks do not run inference and therefore
cannot establish successful vision, generation, embeddings or reranking.

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

## Access and privacy

Confirmed with Christian on 2026-09-10: same-computer access first, then an explicitly
enabled household-network mode. Initial target: local inference and loopback access.
The launcher does not enable LAN access, remote access, cloud inference or Telegram.
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
Redis already owned 6379: set `PARROT_REDIS_PORT=6380` and `REDIS_URL=redis://127.0.0.1:6380/0`
in `.env`. The earlier failure below is kept for the record.

Previously, Docker Desktop
failed to start because its transient `sailor-ingest.sock` file could not be accessed.
A targeted cleanup after stopping Docker also failed with the same filesystem error.
Docker must be repaired before starting the project containers and applying the existing
reviewed migration. No factory reset, image removal, volume deletion or schema change was
performed. The diagnostic server remains usable with these dependencies unavailable.
