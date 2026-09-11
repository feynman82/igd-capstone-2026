"""Run the local diagnostic server; own its socket and open a browser only after startup."""

from __future__ import annotations

import argparse
import logging
import socket
import sys
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bind-address", choices=["127.0.0.1"], default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        try:
            listener.bind((args.bind_address, args.port))
            listener.listen(128)
        except OSError:
            print(f"Cannot use local port {args.port}. Close the other server or select --port.")
            return 2
        server = uvicorn.Server(
            uvicorn.Config(
                app, host=args.bind_address, port=args.port, access_log=False, proxy_headers=False
            )
        )
        finished = threading.Event()

        def open_browser() -> None:
            while not finished.wait(0.1):
                if server.started:
                    url = f"http://127.0.0.1:{args.port}/"
                    print(f"Parrot setup: {url} (household assistant not yet ready)", flush=True)
                    if not args.no_browser:
                        try:
                            webbrowser.open(url)
                        except webbrowser.Error:
                            print("Open the setup URL above in your browser.")
                    return

        watcher = threading.Thread(target=open_browser, daemon=True)
        watcher.start()
        capture = FolderCapture(settings)
        capture.start()
        try:
            server.run(sockets=[listener])
        except KeyboardInterrupt:
            pass
        finally:
            capture.stop()
            finished.set()
            watcher.join(timeout=1)
        return 0 if server.started else 1


if __name__ == "__main__":
    raise SystemExit(main())
