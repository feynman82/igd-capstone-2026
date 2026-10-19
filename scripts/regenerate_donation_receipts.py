#!/usr/bin/env python3
"""Regenerate the three synthetic donation receipts from their versioned merge data.

Run from repository root:
    python scripts/regenerate_donation_receipts.py
Requires jinja2 and a local Chromium/Chrome executable.
This does not touch the development vault.
"""
import csv
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "corpus/batches/donations-rachel-2024-2025"
TEMPLATES = ROOT / "corpus/templates"
BROWSER = os.environ.get("CHROME_BIN") or next(
    (shutil.which(name) for name in (
        "chromium", "chromium-browser", "google-chrome", "microsoft-edge"
    ) if shutil.which(name)),
    None,
)


def main():
    if not BROWSER:
        raise SystemExit("No Chrome/Chromium found; set CHROME_BIN to its executable")
    template = Environment(
        loader=FileSystemLoader(TEMPLATES), autoescape=True
    ).get_template("donation_receipt.html")
    with (DEST / "merge-data.csv").open(newline="", encoding="utf-8-sig") as source:
        records = list(csv.DictReader(source))
    if len(records) != 3:
        raise SystemExit(f"Expected 3 donation records, found {len(records)}")
    with tempfile.TemporaryDirectory(prefix="parrot-donations-") as tmp:
        tmpdir = Path(tmp)
        for record in records:
            stem = record["file"]
            if not stem.startswith("donation-") or "/" in stem or "\\\\" in stem:
                raise ValueError(f"Unsafe document name: {stem}")
            html = tmpdir / (stem + ".html")
            html.write_text(template.render(**record), encoding="utf-8")
            pdf = DEST / (stem + ".pdf")
            command = [
                BROWSER, "--headless", "--no-sandbox", "--disable-gpu",
                "--disable-dev-shm-usage", "--no-pdf-header-footer",
                f"--print-to-pdf={pdf}", html.as_uri(),
            ]
            result = subprocess.run(command, capture_output=True, text=True, timeout=90)
            if result.returncode or not pdf.exists() or pdf.stat().st_size < 100:
                raise RuntimeError(f"PDF generation failed for {stem}: {result.stderr}")
            print(f"Generated {pdf.relative_to(ROOT)} ({pdf.stat().st_size} bytes)")
    print("Re-run isolated eval.freeze and verify the three donation dates before merging.")


if __name__ == "__main__":
    main()
