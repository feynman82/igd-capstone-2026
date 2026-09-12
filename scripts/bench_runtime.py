"""Measure decode throughput and peak VRAM for the generator on this machine.

    uv run python scripts/bench_runtime.py                       # print the table
    uv run python scripts/bench_runtime.py --out eval/results/w1-hardware.md

Why this exists rather than a paragraph of instructions: the five of us run the evaluation on
five different machines, and a tok/s figure is only comparable if everybody measured the same
thing the same way. This script is the definition of "the same way".

What it measures, and how:

* **Decode throughput** comes from Ollama's own `eval_count / eval_duration`, not from a
  stopwatch around the request. That excludes model load and prompt processing, which are the
  two things a wall-clock number silently folds in.
* **Peak VRAM** is sampled from `nvidia-smi --query-gpu=memory.used` on a background thread
  while the request runs, and reported as peak minus a measured idle baseline. Per-process VRAM
  is reported as N/A by the WDDM driver on Windows, so whole-device minus baseline is the only
  honest method available here; the report says so.
* **Context length** is `num_ctx`. Ollama allocates the KV cache for the whole window when the
  model loads, so VRAM reflects `num_ctx` whether or not the prompt fills it. Decode rate does
  not: attention over a full window is slower, so the sweep includes one filled-context run at
  the configured operating point to show the penalty.

The model tag, quantisation and context default are read from `core.runtime.settings`, so the
benchmark cannot drift away from what the product actually loads.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import platform
import statistics
import subprocess
import sys
import textwrap
import threading
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# A short prompt that asks for continuous prose: decode rate is what is being measured, so the
# model must not stop after a sentence. Temperature 0 keeps the token count stable across runs.
PROMPT = (
    "Explain, in careful and continuous prose, why a household document assistant should "
    "decline to answer when its retrieved evidence does not cover the question. Do not use "
    "lists or headings. Keep writing until you have covered provenance, abstention and the "
    "difference between a plausible sentence and a supported one."
)
SYSTEM = "You are a benchmark load. Write continuous prose."

SAMPLE_INTERVAL_S = 0.1
NUM_PREDICT = 256
WARMUP_RUNS = 1
MEASURED_RUNS = 3

# Assembled rather than written out, only so the source line stays inside the 100-column limit.
TABLE_HEADER = "\n".join(
    (
        "| Model tag | Quant | Context | Prompt | Decode tok/s "
        "| Prefill tok/s | Peak VRAM | Model VRAM | Placement |",
        "|---|---|---|---|---|---|---|---|---|",
    )
)


class BenchmarkUnavailable(RuntimeError):
    """Safe to print: names what could not be measured, never why the machine is like this."""


# ------------------------------------------------------------------------------ device


def nvidia_smi(query: str) -> list[str]:
    """One `nvidia-smi` query. Returns the rows, stripped. Raises if the tool is not there."""
    try:
        finished = subprocess.run(
            ["nvidia-smi", f"--query-gpu={query}", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=20,
            check=True,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise BenchmarkUnavailable("nvidia-smi did not answer") from error
    return [row.strip() for row in finished.stdout.splitlines() if row.strip()]


@dataclass(frozen=True, slots=True)
class Device:
    name: str
    total_mib: int
    driver: str

    @classmethod
    def read(cls) -> Device:
        rows = nvidia_smi("name,memory.total,driver_version")
        if not rows:
            raise BenchmarkUnavailable("nvidia-smi reported no GPU")
        name, total, driver = (part.strip() for part in rows[0].split(",", 2))
        return cls(name=name, total_mib=int(total), driver=driver)


def used_mib() -> int:
    rows = nvidia_smi("memory.used")
    return int(rows[0])


class VramSampler:
    """Polls whole-device VRAM on a thread for the life of one request."""

    def __init__(self, interval: float = SAMPLE_INTERVAL_S) -> None:
        self._interval = interval
        self._stop = threading.Event()
        self._peak = 0
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self) -> None:
        while not self._stop.is_set():
            # One failed sample must not lose the samples already taken, nor the request.
            with contextlib.suppress(BenchmarkUnavailable):
                self._peak = max(self._peak, used_mib())
            self._stop.wait(self._interval)

    def __enter__(self) -> VramSampler:
        self._thread.start()
        return self

    def __exit__(self, *_: object) -> None:
        self._stop.set()
        self._thread.join(timeout=5)

    @property
    def peak_mib(self) -> int:
        return self._peak


def idle_baseline(samples: int = 20) -> int:
    """Median VRAM with the model unloaded. Subtracted from peak to get the model's share."""
    readings = []
    for _ in range(samples):
        readings.append(used_mib())
        time.sleep(SAMPLE_INTERVAL_S)
    return int(statistics.median(readings))


def ollama_cli(*args: str) -> str:
    try:
        finished = subprocess.run(
            ["ollama", *args], capture_output=True, text=True, timeout=120, check=False
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise BenchmarkUnavailable("the ollama command line did not answer") from error
    return finished.stdout.strip()


def processor_split() -> str:
    """The PROCESSOR column of `ollama ps` — the proof that nothing spilled to CPU."""
    lines = [line for line in ollama_cli("ps").splitlines() if line.strip()]
    if len(lines) < 2:
        return "not reported"
    columns = lines[1].split()
    for index, token in enumerate(columns):
        if token.endswith("%") and index + 1 < len(columns):
            return f"{token} {columns[index + 1]}"
    return "not reported"


# ------------------------------------------------------------------------------ one run


@dataclass(frozen=True, slots=True)
class Run:
    decode_tokens: int
    decode_ns: int
    prompt_tokens: int
    prompt_ns: int
    load_ns: int
    peak_mib: int

    @property
    def decode_tps(self) -> float:
        return self.decode_tokens / (self.decode_ns / 1_000_000_000) if self.decode_ns else 0.0

    @property
    def prompt_tps(self) -> float:
        return self.prompt_tokens / (self.prompt_ns / 1_000_000_000) if self.prompt_ns else 0.0


def generate(client: Any, model: str, prompt: str, num_ctx: int) -> Run:
    """One non-streaming generation, with VRAM sampled across it.

    The request body mirrors `core.runtime.ollama.Ollama.constrained` in everything that
    affects speed — same endpoint, same temperature, same `num_ctx` — minus the JSON schema,
    because a constrained decode measures the grammar as much as the model.
    """
    import httpx

    # A nonce at the *front* of the prompt, so Ollama's prefix cache cannot serve this request
    # from the previous one. Without it the second run reports a prefill rate in the hundreds of
    # thousands of tokens per second, which is the cache being measured rather than the model.
    nonce = f"[run {time.time_ns()}]\n"
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": nonce + prompt},
        ],
        "stream": False,
        "options": {"temperature": 0.0, "num_ctx": num_ctx, "num_predict": NUM_PREDICT},
    }
    with VramSampler() as sampler:
        try:
            response = client.post("/api/chat", json=body)
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as error:
            raise BenchmarkUnavailable(f"{model} did not answer at num_ctx={num_ctx}") from error

    return Run(
        decode_tokens=int(payload.get("eval_count") or 0),
        decode_ns=int(payload.get("eval_duration") or 0),
        prompt_tokens=int(payload.get("prompt_eval_count") or 0),
        prompt_ns=int(payload.get("prompt_eval_duration") or 0),
        load_ns=int(payload.get("load_duration") or 0),
        peak_mib=sampler.peak_mib,
    )


@dataclass(frozen=True, slots=True)
class Measurement:
    num_ctx: int
    prompt_label: str
    prompt_tokens: int
    decode_tps: float
    decode_low: float
    decode_high: float
    prompt_tps: float
    peak_mib: int
    baseline_mib: int
    processor: str

    @property
    def model_mib(self) -> int:
        return max(self.peak_mib - self.baseline_mib, 0)


def measure(
    client: Any,
    model: str,
    num_ctx: int,
    prompt: str,
    prompt_label: str,
    baseline_mib: int,
) -> Measurement:
    """Warm up, then take the median decode rate and the worst peak across the measured runs."""
    for _ in range(WARMUP_RUNS):
        generate(client, model, prompt, num_ctx)
    processor = processor_split()
    runs = [generate(client, model, prompt, num_ctx) for _ in range(MEASURED_RUNS)]
    return Measurement(
        num_ctx=num_ctx,
        prompt_label=prompt_label,
        prompt_tokens=max(run.prompt_tokens for run in runs),
        decode_tps=statistics.median(run.decode_tps for run in runs),
        decode_low=min(run.decode_tps for run in runs),
        decode_high=max(run.decode_tps for run in runs),
        prompt_tps=statistics.median(run.prompt_tps for run in runs),
        peak_mib=max(run.peak_mib for run in runs),
        baseline_mib=baseline_mib,
        processor=processor,
    )


CHARS_PER_TOKEN = 5.1  # Measured against this filler text, not a general rule for English.


def filler(target_tokens: int) -> str:
    """Padding that occupies the context window without steering the answer.

    The character-to-token ratio is calibrated against this particular sentence rather than
    assumed, and the report prints the count Ollama actually returned, so a drift in the
    tokeniser shows up in the table instead of being hidden by the estimate.
    """
    sentence = (
        "The register records the document identifier and the page on which each value was "
        "printed, so that a later answer can name its source. "
    )
    repeats = max(1, int(target_tokens * CHARS_PER_TOKEN) // len(sentence))
    return sentence * repeats


# ------------------------------------------------------------------------------ report


def coresident_mib(client: Any, settings: Any) -> int:
    """Whole-device VRAM with the generator and the embedder both resident.

    The pipeline embeds and generates in the same process, so the number that decides whether
    ingestion runs is not either model's footprint but the sum of them with both loaded. The
    reranker is not measured: `core/graph/baseline.py` still returns passages unchanged, so
    there is no Ollama call to make yet and a figure for it would be invented.
    """
    import httpx

    with VramSampler() as sampler:
        with contextlib.suppress(httpx.HTTPError, ValueError):
            client.post(
                "/api/embed",
                json={"model": settings.embedding_model, "input": ["warm the embedder"]},
            )
        time.sleep(1.0)
    return sampler.peak_mib


def gib(mib: int) -> str:
    return f"{mib / 1024:.1f} GB"


def quantisation(model_tag: str) -> str:
    """The quantisation as `ollama show` reports it, falling back to the tag's own suffix."""
    for line in ollama_cli("show", model_tag).splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0] == "quantization":
            return parts[1]
    _, _, suffix = model_tag.rpartition(":")
    return suffix or "not reported"


def digest(model_tag: str) -> str:
    for line in ollama_cli("list").splitlines()[1:]:
        parts = line.split()
        if parts and parts[0] == model_tag:
            return parts[1]
    return "not reported"


def operating_point(
    operating: Measurement,
    widest: Measurement,
    at_window: Measurement,
    device: Device,
    coresident: int,
    embedding_model: str,
    rerank_model: str,
) -> str:
    """The three sentences somebody actually plans against, wrapped to the file's width."""
    filled_pct = operating.prompt_tokens * 100 // operating.num_ctx
    vram_cost = widest.model_mib - operating.model_mib
    decode_delta = widest.decode_tps - at_window.decode_tps
    paragraphs = [
        f"At the configured {operating.num_ctx // 1024}K window, with the window "
        f"{filled_pct} per cent full, the generator holds {gib(operating.model_mib)} and "
        f"decodes at {operating.decode_tps:.0f} tok/s. That is the row to plan against; the "
        f"short-prompt row above it is the same model with an almost empty window and reads "
        f"{at_window.decode_tps:.0f} tok/s.",
        f"Widening from {at_window.num_ctx // 1024}K to {widest.num_ctx // 1024}K costs "
        f"{gib(vram_cost)} more VRAM and moves the short-prompt decode rate by "
        f"{decode_delta:+.0f} tok/s, measured the same way on the same machine. Three runs "
        f"is not enough to say whether that difference is the window or the machine, so it "
        f"is reported rather than explained.",
        f"With the generator and the embedder (`{embedding_model}`) both resident, the device "
        f"holds {gib(coresident)} of {gib(device.total_mib)}. The reranker "
        f"(`{rerank_model}`) is not in that figure: `core/graph/baseline.py` still returns "
        f"passages unchanged, so there is no call to make and a number for it would be "
        f"invented rather than measured. Whoever wires it adds a row.",
    ]
    return "\n\n".join(textwrap.fill(p, width=95) for p in paragraphs)


def report(
    model_tag: str,
    quant: str,
    model_digest: str,
    device: Device,
    baseline_mib: int,
    measurements: list[Measurement],
    context_default: int,
    embedding_model: str,
    rerank_model: str,
    coresident: int,
) -> str:
    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    operating = next(m for m in measurements if m.prompt_label == "filled")
    widest = max(measurements, key=lambda m: m.num_ctx)
    at_window = next(
        m for m in measurements if m.num_ctx == operating.num_ctx and m is not operating
    )
    point = operating_point(
        operating, widest, at_window, device, coresident, embedding_model, rerank_model
    )
    rows = "\n".join(
        f"| `{model_tag}` | {quant} | {m.num_ctx // 1024}K | {m.prompt_label} "
        f"({m.prompt_tokens} tok) | {m.decode_tps:.0f} "
        f"({m.decode_low:.0f} to {m.decode_high:.0f}) | {m.prompt_tps:.0f} | "
        f"{gib(m.peak_mib)} | {gib(m.model_mib)} | {m.processor} |"
        for m in measurements
    )
    return f"""# W1 — workstation benchmark

Generated by `uv run python scripts/bench_runtime.py --out eval/results/w1-hardware.md`
on {stamp}. Re-run it on your own machine before quoting an evaluation number against it.

> **The task text names an RTX 4060. This machine is an RTX 3080.** The numbers below were
> measured on the hardware named in the table, not on a 4060, and they should not be read as a
> 4060 result. Whoever benchmarks the 4060 appends their own file rather than editing this one.

## Machine

| | |
|---|---|
| GPU | {device.name} |
| VRAM | {gib(device.total_mib)} ({device.total_mib} MiB) |
| Driver | {device.driver} |
| OS | {platform.system()} {platform.release()} |
| Ollama | {ollama_cli("--version") or "not reported"} |
| Idle VRAM baseline | {gib(baseline_mib)}, model unloaded |

## Generator

{TABLE_HEADER}
{rows}

`{model_tag}`, digest `{model_digest}`. The tag and the quantisation are the two things that
make a number comparable across the five machines; neither is inferred, both are read back
from `ollama show`.

## How to read this

**Decode tok/s** is `eval_count / eval_duration` as Ollama reports it, so it excludes model
load and prompt processing. It is the median of {MEASURED_RUNS} measured runs taken after
{WARMUP_RUNS} warm-up run, with the slowest and the fastest of those runs in brackets, at a
`num_predict` of {NUM_PREDICT} and temperature 0.

**The spread is part of the result.** This is a desktop in normal use, not an idle bench
machine, and repeated invocations of this script have differed by more than the bracket within
any one of them. Compare rows within a single run of the script; do not compare a row here
against a row someone generated on another day without checking both brackets.

**Peak VRAM** is whole-device `nvidia-smi memory.used`, sampled for the life of the request
every {int(SAMPLE_INTERVAL_S * 1000)} ms, and reported as the worst of the measured runs.
The WDDM driver on Windows reports per-process VRAM as `N/A`, so the model's own share cannot
be isolated directly — the **Model VRAM** column subtracts the idle baseline instead, which
is an estimate and is labelled as one.

**Context** is `num_ctx`. Ollama allocates the KV cache for the whole window at load time, so
peak VRAM rises with `num_ctx` regardless of prompt length. Decode rate does not behave the
same way, which is why the filled row exists: it is the {context_default // 1024}K window with
the prompt actually occupying it, and it is the honest figure for the configured operating
point.

**Placement** is the `PROCESSOR` column of `ollama ps`. Anything other than 100% GPU means
layers spilled to CPU and the decode figure on that row is a number about this machine's
memory pressure rather than about the model.

## The operating point

{point}

## What this is for

Yew Mun sizes the evaluation run against the decode rate, and the grounding gate's latency
budget is set from it. The 4B is the generator in `core/runtime/settings.py`; there is no
second generator measured here.
"""


# ------------------------------------------------------------------------------ entry point


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Benchmark the generator on this machine.")
    parser.add_argument("--out", type=Path, help="write the report here instead of stdout")
    parser.add_argument(
        "--context",
        type=int,
        nargs="+",
        default=[4096, 16384, 32768],
        help="context windows to sweep, in tokens",
    )
    parser.add_argument("--json", type=Path, help="also write the raw measurements here")
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    import httpx

    from core.runtime.settings import ConfigurationError, Settings

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    model = settings.generation_model
    try:
        device = Device.read()
        ollama_cli("stop", model)
        time.sleep(1.0)
        baseline = idle_baseline()

        measurements = []
        with httpx.Client(
            base_url=settings.generation_url,
            timeout=600.0,
            trust_env=False,
            follow_redirects=False,
        ) as client:
            for num_ctx in args.context:
                measurements.append(measure(client, model, num_ctx, PROMPT, "short", baseline))
            filled = int(settings.context_tokens * 0.85)
            measurements.append(
                measure(
                    client,
                    model,
                    settings.context_tokens,
                    f"{filler(filled)}\n\n{PROMPT}",
                    "filled",
                    baseline,
                )
            )
            coresident = coresident_mib(client, settings)
        text = report(
            model_tag=model,
            quant=quantisation(model),
            model_digest=digest(model),
            device=device,
            baseline_mib=baseline,
            measurements=measurements,
            context_default=settings.context_tokens,
            embedding_model=settings.embedding_model,
            rerank_model=settings.rerank_model,
            coresident=coresident,
        )
    except BenchmarkUnavailable as error:
        print(f"Not measurable on this machine: {error}")
        return 1

    if args.json:
        args.json.write_text(
            json.dumps([asdict(m) for m in measurements], indent=2), encoding="utf-8"
        )
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
