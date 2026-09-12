"""Run the local diagnostic server, the folder watcher and the ingestion worker together.

Three things start here and they fail independently on purpose. The server is the one a person
is looking at, so it comes up even when the other two cannot. The watcher registers whatever is
dropped into the inbox. The worker reads those documents off the queue, and when it cannot start
— no broker, no Celery — the reason is printed in one line and capture falls back to reading
documents on the watcher thread, which is slower and says so.
"""

from __future__ import annotations

import argparse
import logging
import socket
import subprocess
import sys
import threading
import webbrowser
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.runtime.settings import Settings

ROOT = Path(__file__).resolve().parents[1]


def start_worker(settings: Settings) -> subprocess.Popen[bytes] | None:
    """Start `scripts/worker.py --beat` beside us, or say plainly why it could not.

    It is a child process rather than a thread because that is what Celery is: the whole point
    of moving ingestion off the watcher thread is that a parse cannot stall anything else, and
    a worker inside this interpreter would still share its GIL and its crash.
    """
    from core.runtime.capture import broker_available

    if not broker_available(settings):
        print(
            "Ingestion worker: not started. The queue broker did not answer. Start it with "
            "`docker compose -f infra/docker-compose.yml up -d redis`; until then documents "
            "are read on the watcher thread, a few seconds each.",
            flush=True,
        )
        return None
    try:
        import celery  # noqa: F401
    except ImportError:
        print("Ingestion worker: not started. Celery is not installed; run uv sync.", flush=True)
        return None
    try:
        worker = subprocess.Popen(
            [sys.executable, str(ROOT / "scripts/worker.py"), "--beat"],
            cwd=ROOT,
        )
    except OSError as error:
        print(f"Ingestion worker: not started ({error}).", flush=True)
        return None
    print("Ingestion worker: started, with the nightly Reminder and Alert sweeps.", flush=True)
    return worker


def stop_worker(worker: subprocess.Popen[bytes] | None) -> None:
    if worker is None or worker.poll() is not None:
        return
    worker.terminate()
    try:
        worker.wait(timeout=10)
    except subprocess.TimeoutExpired:
        worker.kill()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bind-address", choices=["127.0.0.1"], default="127.0.0.1")
    # No default here: an unset port means "whatever PARROT_PORT says", which is read from
    # .env below once Settings has loaded. An explicit --port still wins over it.
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument(
        "--no-worker", action="store_true", help="do not start the ingestion worker"
    )
    args = parser.parse_args(argv)
    if args.port is not None and not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        import uvicorn

        from api.main import create_app
        from core.runtime.capture import FolderCapture
        from core.runtime.settings import ConfigurationError, Settings
    except ImportError:
        print("Runtime dependencies are missing. Run uv sync --extra dev.")
        return 2
    try:
        settings = Settings.load(ROOT)
        app = create_app(settings)
    except ConfigurationError as error:
        print(f"Configuration needs attention: {error}")
        return 2
    except (OSError, UnicodeError):
        print("Cannot read local configuration. Check .env access and UTF-8 encoding.")
        return 2
    port = args.port if args.port is not None else settings.api_port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        try:
            listener.bind((args.bind_address, port))
            listener.listen(128)
        except OSError:
            # Naming the fix matters more than naming the failure: on a machine where Docker
            # Desktop holds 8000, every future start hits this unless the port is written down.
            print(
                f"Cannot use local port {port}. Something else on this computer is using it.\n"
                f"Set PARROT_PORT in .env to a free port (8010 is a good second choice), and\n"
                f"put the same port in web/.env.local as PARROT_API_URL so the screens follow."
            )
            return 2
        server = uvicorn.Server(
            uvicorn.Config(
                app, host=args.bind_address, port=port, access_log=False, proxy_headers=False
            )
        )
        finished = threading.Event()

        def open_browser() -> None:
            while not finished.wait(0.1):
                if server.started:
                    url = f"http://127.0.0.1:{port}/"
                    print(
                        f"Parrot engine: {url} — setup checks and the local API.\n"
                        "The screens are a second process: cd web && npm run dev, "
                        "then open http://localhost:3000",
                        flush=True,
                    )
                    if not args.no_browser:
                        try:
                            webbrowser.open(url)
                        except webbrowser.Error:
                            print("Open the setup URL above in your browser.")
                    return

        watcher = threading.Thread(target=open_browser, daemon=True)
        watcher.start()
        worker = None if args.no_worker else start_worker(settings)
        # --no-worker means "I am running the worker myself", so let capture look for the
        # broker rather than assuming there is nothing listening.
        capture = FolderCapture(settings, use_queue=None if args.no_worker else worker is not None)
        capture.start()
        try:
            server.run(sockets=[listener])
        except KeyboardInterrupt:
            pass
        finally:
            capture.stop()
            stop_worker(worker)
            finished.set()
            watcher.join(timeout=1)
        return 0 if server.started else 1


if __name__ == "__main__":
    raise SystemExit(main())
