"""Run the ingestion worker, and optionally the nightly schedule with it.

    uv run python scripts/worker.py                # read documents off the queue
    uv run python scripts/worker.py --beat         # and run the Reminder and Alert sweeps
    uv run python scripts/worker.py --beat-only    # just the schedule, no document reading
    uv run python scripts/worker.py --purge        # drop anything already queued, then run

This is the other half of `scripts/watch_folder.py`. The watcher registers documents and puts
them on the queue; this reads them off it. Run both and a person can drop five scans at once
without the fifth waiting behind the first four.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
# Beat keeps a small file recording when it last ran each sweep. It is local state, so it
# lives under var/ rather than in the repository root where it was landing as untracked noise.
BEAT_STATE = ROOT / "var" / "celerybeat-schedule"
NOISY = ("httpx", "docling", "RapidOCR", "huggingface_hub", "filelock")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--beat", action="store_true", help="run the nightly sweeps too")
    parser.add_argument(
        "--beat-only", action="store_true", help="run only the schedule, reading no documents"
    )
    parser.add_argument("--purge", action="store_true", help="discard anything already queued")
    parser.add_argument("--loglevel", default="INFO", choices=["DEBUG", "INFO", "WARNING"])
    args = parser.parse_args(argv)

    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=args.loglevel, format="%(message)s")
    for name in NOISY:
        logging.getLogger(name).setLevel(logging.WARNING)

    from core.runtime.settings import ConfigurationError, Settings

    try:
        settings = Settings.load(ROOT)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2

    try:
        from core.worker.tasks import application
    except ImportError:
        print("Celery is not installed. Run uv sync --extra dev.")
        return 2

    # The nightly sweeps read the enabled flag out of `packs`, so a worker started on its own
    # against a fresh database installs the registry too. Idempotent, and it never re-enables
    # a pack somebody switched off.
    from core.registry import install_best_effort

    install_best_effort(settings)

    BEAT_STATE.parent.mkdir(parents=True, exist_ok=True)
    app = application(settings)
    if args.beat_only:
        print(f"Running the nightly schedule against {settings.redis_url}. Ctrl+C to stop.")
        return _run(app, celery_argv(args, beat_only=True))

    print(f"Worker ready on {settings.redis_url}. Ctrl+C to stop.")
    beat = _start_beat(args) if args.beat and _beat_needs_its_own_process() else None
    try:
        return _run(app, celery_argv(args, beat_only=False))
    finally:
        _stop_beat(beat)


def celery_argv(args: argparse.Namespace, *, beat_only: bool) -> list[str]:
    """The arguments the Celery command-line would have been given. Built here so a test can
    read them without starting anything."""
    if beat_only:
        return ["beat", f"--loglevel={args.loglevel}", f"--schedule={BEAT_STATE}"]
    argv = ["worker", f"--loglevel={args.loglevel}", "--concurrency=1"]
    if sys.platform == "win32":
        argv.append("--pool=solo")  # the prefork pool does not work on Windows
    if args.beat and not _beat_needs_its_own_process():
        argv.extend(["--beat", f"--schedule={BEAT_STATE}"])
    if args.purge:
        argv.append("--purge")
    return argv


def _beat_needs_its_own_process() -> bool:
    """Celery refuses `worker --beat` on Windows — "-B option does not work on Windows" — so
    there the schedule runs as a second process. Everywhere else one process does both."""
    return sys.platform == "win32"


def _start_beat(args: argparse.Namespace) -> subprocess.Popen[bytes] | None:
    try:
        return subprocess.Popen(
            [
                sys.executable,
                str(ROOT / "scripts/worker.py"),
                "--beat-only",
                f"--loglevel={args.loglevel}",
            ],
            cwd=ROOT,
        )
    except OSError as error:
        print(f"The nightly schedule did not start ({error}). The worker is running without it.")
        return None


def _stop_beat(beat: subprocess.Popen[bytes] | None) -> None:
    if beat is None or beat.poll() is not None:
        return
    beat.terminate()
    try:
        beat.wait(timeout=10)
    except subprocess.TimeoutExpired:
        beat.kill()


def _run(app: Any, argv: list[str]) -> int:
    try:
        return int(app.start(argv=argv) or 0)
    except KeyboardInterrupt:
        print("Stopped.")
        return 0
    except Exception as error:  # a broker that is not there raises its own class
        print(f"The worker stopped: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
