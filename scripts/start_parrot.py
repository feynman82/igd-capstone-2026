"""Local-only startup preflight, using the standard library so setup can be diagnosed."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def startup_gaps(root: Path) -> list[str]:
    """Inspect startup files without importing the application or reading user data."""
    python = root / (".venv/Scripts/python.exe" if sys.platform == "win32" else ".venv/bin/python")
    gaps = []
    if not python.is_file():
        gaps.append("Python environment: install Python 3.12 and uv; run uv sync --extra dev.")
    if not (root / ".env").is_file():
        gaps.append("Local configuration: copy infra/.env.example to .env and review it.")
    if not (root / "scripts/run_parrot.py").is_file():
        gaps.append(
            "Application runtime is not built yet. This checkout contains startup diagnostics only."
        )
    return gaps


def report_hardware() -> None:
    """Report categories only, without hostname, username, serial numbers or file contents."""
    print(f"OS: {platform.system()} {platform.release()} ({platform.machine()})")
    if sys.platform != "win32":
        print("Record CPU/Apple chip, RAM and GPU memory using this computer's system information.")
        return
    shell = shutil.which("powershell.exe")
    if not shell:
        print("Hardware details unavailable; this does not establish a hardware failure.")
        return
    # Read-only commands, with no user values interpolated and no execution-policy change.
    command = (
        "$ErrorActionPreference = 'Stop'; "
        "'RAM (GB): {0:N1}' -f ((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB); "
        "Get-CimInstance Win32_Processor | ForEach-Object { 'CPU: ' + $_.Name }; "
        "Get-CimInstance Win32_VideoController | ForEach-Object { 'GPU: ' + $_.Name }"
    )
    try:
        result = subprocess.run(
            [shell, "-NoLogo", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            errors="replace",
            timeout=15,
            check=False,
        )
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print("Hardware details unavailable; this does not establish a hardware failure.")
    except (OSError, subprocess.TimeoutExpired):
        print("Hardware details unavailable; this does not establish a hardware failure.")
    print("GPU memory: verify with the vendor tool; not inferred from the model name.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-CheckOnly", "--check-only", action="store_true", dest="check_only")
    args = parser.parse_args(argv)
    print("Parrot - local startup", flush=True)
    print("Minimum supported hardware: not yet established by benchmarks.")
    report_hardware()
    print()
    for tool in ("uv", "node", "npm", "docker", "ollama"):
        print(f"{tool}: {'found' if shutil.which(tool) else 'not found on PATH'}")
    print("Tool presence does not mean services are running or models are installed.")
    gaps = startup_gaps(ROOT)
    if gaps:
        print("\nParrot is not ready to start:")
        for gap in gaps:
            print(f"  - {gap}")
        print("See docs/RUNNING.md for the current build stage and next steps.")
        return 2
    if args.check_only:
        print("\nStartup files are present. Runtime health has not been checked.")
        return 0
    python = ROOT / (".venv/Scripts/python.exe" if sys.platform == "win32" else ".venv/bin/python")
    # No settings are evaluated as code; only the project-owned supervisor is executed.
    try:
        return subprocess.call(
            [str(python), str(ROOT / "scripts/run_parrot.py"), "--bind-address", "127.0.0.1"],
            cwd=ROOT,
        )
    except KeyboardInterrupt:
        return 130
    except OSError:
        print("Could not start the runtime. Check the Python environment; see docs/RUNNING.md.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
