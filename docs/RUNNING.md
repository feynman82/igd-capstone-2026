# Starting Parrot

On Windows, double-click `START.cmd` in the repository root. The window stays open so
you can read setup problems. It works independently of the terminal's current directory.
It uses the project's Python environment, or Python on PATH for initial diagnostics.
It does not require enabling PowerShell scripts or changing execution policy.

**Current build stage:** startup diagnostics are implemented; the household assistant's
runtime is not. The launcher reports this explicitly and does not open an empty browser
tab or claim the application is running. API, ingestion worker and frontend integration
are required before application startup can be enabled.

For a check that exits without waiting for a key, run:

```bat
START.cmd -CheckOnly
```

Exit codes: `0` means startup files are present (not an application health guarantee),
`2` means setup or implementation is incomplete, and `1` means a launcher error.
Diagnostics print locally; they do not upload information, read household documents,
print `.env` values, download models, install tools, or change service configuration.
Installed tools are reported separately from runtime readiness.

## Startup integration contract

The next runtime slice must provide `scripts/run_parrot.py`, accepting
`--bind-address 127.0.0.1`. This is the supervisor entry point, not a user-authored setting.
Before it is added, the launcher deliberately remains unavailable for application startup.
The supervisor must:

- Validate configuration, database schema and required model capabilities.
- Bind the application to loopback by default; reject unsupported access modes.
- Start or reuse verified services and distinguish them from unrelated processes.
- Start the ingestion worker, API and built frontend; report startup failures.
- Open the browser only after application readiness checks pass.
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
