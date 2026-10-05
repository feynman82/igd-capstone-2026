"""Startup tests do not ingest documents or need the corpus: they check process boundaries."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts import run_parrot, start_parrot


def test_incomplete_checkout_never_launches_a_process(tmp_path: Path) -> None:
    with (
        patch.object(start_parrot, "ROOT", tmp_path),
        patch.object(start_parrot, "report_hardware"),
        patch.object(start_parrot.subprocess, "call") as launch,
    ):
        assert start_parrot.main([]) == 2
        launch.assert_not_called()


def prepare_checkout(root: Path) -> None:
    python = root / (
        ".venv/Scripts/python.exe" if start_parrot.sys.platform == "win32" else ".venv/bin/python"
    )
    python.parent.mkdir(parents=True)
    python.touch()
    (root / ".env").write_text("SECRET=do-not-print", encoding="utf-8")
    (root / "scripts").mkdir()
    (root / "scripts/run_parrot.py").touch()


def test_check_only_never_launches_even_when_ready(tmp_path: Path) -> None:
    prepare_checkout(tmp_path)
    with (
        patch.object(start_parrot, "ROOT", tmp_path),
        patch.object(start_parrot, "report_hardware"),
        patch.object(start_parrot.subprocess, "call") as launch,
    ):
        assert start_parrot.main(["-CheckOnly"]) == 0
        launch.assert_not_called()


def test_launch_preserves_paths_and_loopback_and_exit_code(tmp_path: Path) -> None:
    root = tmp_path / "Parrot with spaces"
    prepare_checkout(root)
    with (
        patch.object(start_parrot, "ROOT", root),
        patch.object(start_parrot, "report_hardware"),
        patch.object(start_parrot.subprocess, "call", return_value=7) as launch,
    ):
        assert start_parrot.main([]) == 7
        command = launch.call_args.args[0]
        assert command[1:] == [str(root / "scripts/run_parrot.py"), "--bind-address", "127.0.0.1"]
        assert launch.call_args.kwargs == {"cwd": root}


# The screens are a fourth process. These check that the supervisor starts and stops one
# without ever launching npm, so the boundary is testable on a machine with no Node at all.


def test_screens_are_not_started_twice_when_something_already_holds_the_port() -> None:
    """A developer's own `npm run dev` is used rather than fought for the port."""
    with (
        patch.object(run_parrot, "port_answers", return_value=True),
        patch.object(run_parrot.subprocess, "Popen") as launch,
    ):
        assert run_parrot.start_web(8000, 3000) is None
        launch.assert_not_called()


def test_screens_are_not_started_without_dependencies(tmp_path: Path) -> None:
    """`npm run dev` against an empty web/ fails slowly and cryptically. Say so instead."""
    (tmp_path / "web").mkdir()
    with (
        patch.object(run_parrot, "ROOT", tmp_path),
        patch.object(run_parrot, "port_answers", return_value=False),
        patch.object(run_parrot.shutil, "which", return_value="npm"),
        patch.object(run_parrot.subprocess, "Popen") as launch,
    ):
        assert run_parrot.start_web(8000, 3000) is None
        launch.assert_not_called()


def test_screens_are_not_started_without_npm(tmp_path: Path) -> None:
    (tmp_path / "web/node_modules").mkdir(parents=True)
    with (
        patch.object(run_parrot, "ROOT", tmp_path),
        patch.object(run_parrot, "port_answers", return_value=False),
        patch.object(run_parrot.shutil, "which", return_value=None),
        patch.object(run_parrot.subprocess, "Popen") as launch,
    ):
        assert run_parrot.start_web(8000, 3000) is None
        launch.assert_not_called()


def test_screens_are_told_the_engine_port_they_must_actually_reach(tmp_path: Path) -> None:
    """The screens follow the engine to whatever port it got, rather than to web/.env.local.

    This is the whole reason the variable is passed through the environment: a person who set
    PARROT_PORT in one file and not the other used to get screens that could not reach the
    engine, with nothing on either screen saying why.
    """
    (tmp_path / "web/node_modules").mkdir(parents=True)
    with (
        patch.object(run_parrot, "ROOT", tmp_path),
        patch.object(run_parrot, "port_answers", return_value=False),
        patch.object(run_parrot.shutil, "which", return_value="/usr/bin/npm"),
        patch.object(run_parrot.subprocess, "Popen") as launch,
    ):
        run_parrot.start_web(8010, 3100)
        assert launch.call_args.args[0] == ["/usr/bin/npm", "run", "dev"]
        environment = launch.call_args.kwargs["env"]
        assert environment["PARROT_API_URL"] == "http://127.0.0.1:8010"
        assert environment["PORT"] == "3100"
        assert launch.call_args.kwargs["cwd"] == tmp_path / "web"


def test_stopping_the_screens_kills_the_tree_not_the_wrapper() -> None:
    """npm is a wrapper around node. Killing only the wrapper orphans the port."""
    web = MagicMock()
    web.poll.return_value = None
    web.pid = 4242
    with (
        patch.object(run_parrot.sys, "platform", "win32"),
        patch.object(run_parrot.shutil, "which", return_value="taskkill"),
        patch.object(run_parrot.subprocess, "run") as kill,
    ):
        run_parrot.stop(web)
        assert kill.call_args.args[0] == ["taskkill", "/PID", "4242", "/T", "/F"]


def test_stopping_screens_that_were_never_started_does_nothing() -> None:
    with patch.object(run_parrot.subprocess, "run") as kill:
        run_parrot.stop(None)
        kill.assert_not_called()


def test_stopping_the_worker_kills_the_tree_not_the_launcher() -> None:
    """The worker starts its nightly schedule as a process of its own. Terminating only the venv
    launcher in front of the worker left that schedule running with no parent — two of them after
    one restart and one shut-down from the screens on 2026-09-13."""
    worker = MagicMock()
    worker.poll.return_value = None
    worker.pid = 5151
    with (
        patch.object(run_parrot.sys, "platform", "win32"),
        patch.object(run_parrot.shutil, "which", return_value="taskkill"),
        patch.object(run_parrot.subprocess, "run") as kill,
    ):
        run_parrot.stop(worker)
        assert kill.call_args.args[0] == ["taskkill", "/PID", "5151", "/T", "/F"]


def test_a_worker_that_has_already_stopped_is_left_alone() -> None:
    worker = MagicMock()
    worker.poll.return_value = 0
    with patch.object(run_parrot.subprocess, "run") as kill:
        run_parrot.stop(worker)
        run_parrot.stop(None)
        kill.assert_not_called()


def test_the_worker_gets_its_own_session_off_windows(tmp_path: Path) -> None:
    """Stopping it signals its process group. Without a session of its own that group is this
    launcher's, and stopping the worker would stop the engine that asked."""
    from core.runtime.settings import Settings

    with (
        patch.object(run_parrot.sys, "platform", "linux"),
        patch("core.runtime.capture.broker_available", return_value=True),
        patch.object(run_parrot.subprocess, "Popen") as launch,
    ):
        run_parrot.start_worker(Settings.load(tmp_path, {}))
        assert launch.call_args.kwargs.get("start_new_session") is True
