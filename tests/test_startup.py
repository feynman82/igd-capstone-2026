"""Startup tests do not ingest documents or need the corpus: they check process boundaries."""

from pathlib import Path
from unittest.mock import patch

from scripts import start_parrot


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
