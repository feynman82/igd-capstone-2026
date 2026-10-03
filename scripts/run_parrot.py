"""Run the engine, the folder watcher, the ingestion worker and the screens together.

Four things start here and they fail independently on purpose. The engine is the API and the
setup-check page, so it comes up even when nothing else can. The watcher registers whatever is
dropped into the inbox. The worker reads those documents off the queue, and when it cannot start
— no broker, no Celery — the reason is printed in one line and capture falls back to reading
documents on the watcher thread, which is slower and says so. The screens are the Next.js app in
`web/`, and they are the thing a person actually opens.

The screens used to be a second window somebody had to know to open. They are not any more:
`START.cmd` is the one button, and a button that starts three of the four things a product needs
is a button that does not work. Everything except Docker and Ollama starts from here, and when
those two move into the container set they will start from here too.

Started as a script, this file is two processes. The outer one is a small supervisor: it starts
the screens once, runs the engine as a child, and starts a fresh child whenever the engine exits
asking to be restarted — so Restart in the screens comes back running whatever code is on disk,
with the screens still up to show that it is happening. The child is everything described above.
"""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.runtime.settings import Settings

ROOT = Path(__file__).resolve().parents[1]

# How long this window waits for the screens before saying they did not come up. The browser does
# not wait for them any more: it opens on the engine's startup page at once, and that page moves
# to Today when they answer. A cold `next dev` compiles the first route on the first request,
# which on a laptop is twenty seconds and on a cold npm cache is more.
WEB_READY_TIMEOUT = 120.0


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
        worker = subprocess.Popen(  # type: ignore[call-overload]
            [sys.executable, str(ROOT / "scripts/worker.py"), "--beat"],
            cwd=ROOT,
            # Its own session off Windows, so stopping it can signal the whole group — the worker
            # and the schedule it starts — without signalling this process as well.
            **({} if sys.platform == "win32" else {"start_new_session": True}),
        )
    except OSError as error:
        print(f"Ingestion worker: not started ({error}).", flush=True)
        return None
    print("Ingestion worker: started, with the nightly Reminder and Alert sweeps.", flush=True)
    return worker


def stop(process: subprocess.Popen[bytes] | None) -> None:
    """Stop a child the launcher started -- the worker or the screens -- and everything under it.

    Terminating only the process we launched is not enough on either side. The worker: on Windows
    `sys.executable` is the virtual environment's launcher, which starts the real interpreter as a
    child, and the worker starts its nightly schedule as a child of its own; after one restart and
    one shut-down from the screens, two schedules were still running with no parent. The screens:
    `Popen.terminate()` reaches `npm.cmd` and the `node` it spawned outlives it, still bound to
    3000, so the next double-click reports a busy port.
    """
    if process is None or process.poll() is not None:
        return
    _kill_tree(process)


def _kill_tree(process: subprocess.Popen[bytes]) -> None:
    """Stop a child and everything under it, then make sure it has gone."""
    if sys.platform == "win32":
        taskkill = shutil.which("taskkill")
        if taskkill is not None:
            subprocess.run(
                [taskkill, "/PID", str(process.pid), "/T", "/F"],
                capture_output=True,
                check=False,
                timeout=15,
            )
    else:
        import contextlib
        import signal

        with contextlib.suppress(OSError, ProcessLookupError):
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()


def port_answers(port: int, timeout: float = 0.4) -> bool:
    """Whether something is listening on loopback. Not whether it is ours."""
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except OSError:
        return False


def start_web(api_port: int, web_port: int) -> subprocess.Popen[bytes] | None:
    """Start `npm run dev` in `web/`, or say plainly why it could not.

    Three reasons it does not start, and each one is a sentence rather than a stack trace:
    npm is not on PATH, `web/node_modules` has never been installed, or something is already
    listening on the port — which on a developer's machine almost always means their own
    `npm run dev`, so we use theirs rather than fighting it for the port.

    The child is told `PARROT_API_URL` through its environment rather than through
    `web/.env.local`. Next.js does not override a variable that is already set, so this wins,
    and it means the screens follow the engine to whatever port it actually got instead of
    depending on two files being edited together.
    """
    if port_answers(web_port):
        print(
            f"Screens: already running on http://localhost:{web_port} — using that one. "
            "Nothing new was started.",
            flush=True,
        )
        return None
    npm = shutil.which("npm")
    if npm is None:
        print(
            "Screens: not started. npm is not on PATH. Install Node.js 20 or newer; "
            "until then the engine below still answers and the worker still files documents.",
            flush=True,
        )
        return None
    if not (ROOT / "web/node_modules").is_dir():
        print(
            "Screens: not started. Dependencies are not installed. Run `npm ci` in web/ once; "
            "it takes a couple of minutes and is not repeated.",
            flush=True,
        )
        return None
    environment = dict(os.environ)
    environment["PARROT_API_URL"] = f"http://127.0.0.1:{api_port}"
    environment["PORT"] = str(web_port)
    # A new process group, so the whole tree can be signalled at once. npm is a shell wrapper
    # around node: terminating the wrapper leaves node holding the port, and the next
    # double-click then fails with "address already in use" on a port with no visible owner.
    # See `stop`.
    group = (
        {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
        if sys.platform == "win32"
        else {"start_new_session": True}
    )
    try:
        web = subprocess.Popen([npm, "run", "dev"], cwd=ROOT / "web", env=environment, **group)  # type: ignore[call-overload]
    except OSError as error:
        print(f"Screens: not started ({error}).", flush=True)
        return None
    print(f"Screens: starting on http://localhost:{web_port} — first load compiles.", flush=True)
    return web


# Set on the engine child by the supervisor, so the same file knows which of the two it is.
SUPERVISED_ENV = "PARROT_SUPERVISED"


def spawn_child(argv: list[str]) -> int:
    """Run one engine as a child process and wait for it. A fresh interpreter every time."""
    environment = dict(os.environ)
    environment[SUPERVISED_ENV] = "1"
    child = subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve()), *argv], cwd=ROOT, env=environment
    )
    try:
        return child.wait()
    except KeyboardInterrupt:
        # Ctrl+C reaches the child too, because it shares this console. Give it the time its own
        # clean-up takes rather than leaving an engine running with no window behind it.
        try:
            return child.wait(timeout=20)
        except subprocess.TimeoutExpired:
            child.kill()
            return 130


def supervise(
    argv: list[str],
    *,
    spawn: Callable[[list[str]], int] = spawn_child,
    start_screens: Callable[[int, int], Any] = start_web,
    stop_screens: Callable[[Any], None] = stop,
    load_settings: Callable[[], Settings] | None = None,
) -> int:
    """Keep Parrot running across restarts, and own the screens so they outlive them.

    The screens start here, before the first engine, so `next dev` is compiling while the engine
    boots rather than after it. Each engine runs as a child; an exit with `RESTART_EXIT_CODE`
    starts another one with `--no-browser`, because a restart must not open a second tab. Any
    other exit — a clean shut-down, a failed start, a crash — ends the loop, and only then do the
    screens stop. A crash is not retried: a supervisor that restarts a crashing engine forever
    turns one clear error into a scrolling window nobody can read.
    """
    args = parse_args(argv)  # a bad argument stops here, before anything has started
    sys.path.insert(0, str(ROOT))
    from core.runtime.lifecycle import RESTART_EXIT_CODE
    from core.runtime.settings import ConfigurationError, Settings

    web: Any = None
    child_argv = list(argv)
    if not args.no_web:
        settings: Settings | None
        try:
            settings = load_settings() if load_settings is not None else Settings.load(ROOT)
        except (ConfigurationError, OSError, UnicodeError):
            settings = None  # the engine explains this properly on its first launch
        if settings is not None:
            port = args.port if args.port is not None else settings.api_port
            web_port = args.web_port if args.web_port is not None else settings.web_port
            web = start_screens(port, web_port)
        child_argv.append("--web-managed")
    try:
        first = True
        while True:
            code = spawn(child_argv if first else [*child_argv, "--no-browser"])
            if code != RESTART_EXIT_CODE:
                return code
            first = False
            print("Parrot is restarting. The screens stay up and will reconnect.", flush=True)
    except KeyboardInterrupt:
        return 130
    finally:
        stop_screens(web)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bind-address", choices=["127.0.0.1"], default="127.0.0.1")
    # No default here: an unset port means "whatever PARROT_PORT says", which is read from
    # .env below once Settings has loaded. An explicit --port still wins over it.
    parser.add_argument("--port", type=int, default=None)
    # Same reasoning as --port: unset means "whatever PARROT_WEB_PORT says".
    parser.add_argument("--web-port", type=int, default=None)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument(
        "--no-worker", action="store_true", help="do not start the ingestion worker"
    )
    parser.add_argument("--no-web", action="store_true", help="do not start the screens in web/")
    # Set by the supervisor, never by a person: the screens are already started and owned by the
    # process above this one, so this engine must neither start them nor stop them.
    parser.add_argument("--web-managed", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.port is not None and not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    if args.web_port is not None and not 1 <= args.web_port <= 65535:
        parser.error("web port must be between 1 and 65535")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    sys.path.insert(0, str(ROOT))
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        import uvicorn

        from api.main import create_app
        from core.runtime.capture import FolderCapture, TelegramCapture
        from core.runtime.lifecycle import Lifecycle
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
    web_port = args.web_port if args.web_port is not None else settings.web_port
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
        # The screens ask for a restart or a shut-down through the engine, and this carries it out:
        # the engine records the request and uvicorn exits, and the exit code below tells the
        # supervisor which of the two it was.
        lifecycle = Lifecycle(lambda: setattr(server, "should_exit", True))
        app.state.lifecycle = lifecycle
        finished = threading.Event()
        # Set by the supervisor below once it knows whether there are screens to wait for.
        screens = threading.Event()

        def open_browser() -> None:
            """Open the startup page the moment the engine answers, then report the screens.

            The engine's `/` is the startup page (`api/startup.py`): it shows what Parrot is
            waiting for and moves to Today by itself. It used to be a setup check that the
            browser was only sent to when the screens failed, and the browser waited up to
            ninety seconds for the screens first, so a double-click showed nothing at all.
            """
            while not finished.wait(0.1):
                if not server.started:
                    continue
                engine = f"http://127.0.0.1:{port}/"
                print(f"Parrot engine: {engine} — the startup page and the local API.", flush=True)
                if not args.no_browser:
                    try:
                        webbrowser.open(engine)
                    except webbrowser.Error:
                        print("Open the URL above in your browser.")
                if screens.is_set():
                    deadline = time.monotonic() + WEB_READY_TIMEOUT
                    while not finished.is_set() and time.monotonic() < deadline:
                        if port_answers(web_port):
                            print(
                                f"Parrot: http://localhost:{web_port}/ — the screens.", flush=True
                            )
                            return
                        finished.wait(0.5)
                    if not finished.is_set():
                        print(
                            "The screens did not answer in time. The startup page says so; "
                            f"they may still come up on http://localhost:{web_port}.",
                            flush=True,
                        )
                return

        watcher = threading.Thread(target=open_browser, daemon=True)
        watcher.start()
        app.state.screens = {"url": f"http://localhost:{web_port}/", "expected": not args.no_web}
        # Load the local model while nobody is waiting on it. See `api/startup.py`.
        from api.startup import warm_models
        from core.runtime.ollama import Ollama

        threading.Thread(
            target=warm_models, args=(app.state.model, Ollama(settings, timeout=600.0)), daemon=True
        ).start()
        worker = None if args.no_worker else start_worker(settings)
        # Under the supervisor the screens belong to the process above this one, so they stay up
        # while this engine restarts underneath them.
        web = None if args.no_web or args.web_managed else start_web(port, web_port)
        # The browser waits for the screens whenever they are expected to appear — whether we
        # started them, the supervisor did, or somebody else already had them running.
        if not args.no_web and (args.web_managed or web is not None or port_answers(web_port)):
            screens.set()
        # --no-worker means "I am running the worker myself", so let capture look for the
        # broker rather than assuming there is nothing listening.
        queueing = None if args.no_worker else worker is not None
        capture = FolderCapture(settings, use_queue=queueing)
        capture.start()
        # The second capture channel, on the same terms as the first. It starts only when a bot
        # token is configured, and says which in one line either way: a household that has
        # registered a bot and sees nothing arrive has no other way to tell whether the
        # launcher is polling it. See `core/runtime/capture.py`.
        telegram = TelegramCapture(settings, use_queue=queueing)
        if telegram.start():
            print("Telegram capture: on. Send a photograph to your bot.", flush=True)
        else:
            print(
                "Telegram capture: off. Put TELEGRAM_BOT_TOKEN in .env to file documents from "
                "your phone; see docs/RUNNING.md.",
                flush=True,
            )
        try:
            server.run(sockets=[listener])
        except KeyboardInterrupt:
            pass
        finally:
            capture.stop()
            telegram.stop()
            stop(worker)
            stop(web)
            finished.set()
            watcher.join(timeout=1)
        if lifecycle.requested == "restart":
            print("Parrot is restarting.", flush=True)
        elif lifecycle.requested == "shutdown":
            print("Parrot has shut down. Start it again with START.cmd.", flush=True)
        return lifecycle.exit_code(started=server.started)


if __name__ == "__main__":
    if os.environ.get(SUPERVISED_ENV) == "1":
        raise SystemExit(main())
    raise SystemExit(supervise(sys.argv[1:]))
