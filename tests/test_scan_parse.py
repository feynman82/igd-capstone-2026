"""A scanned or photographed document parses to pages with its tables preserved.

Lane B, W2: "Configure Docling parsing and OCR — a scanned PDF returns structured markdown with
tables preserved; a photographed payslip returns markdown in which the gross-pay table is still
a table." Batch 1 is digital PDFs, so the scanned and photographed tiers are made here from one
of them: the page is drawn to pixels and handed back to the parser as an image-only PDF and as
a skewed JPEG. Nothing is authored; the content is Desmond's, and the values checked for are
the register's, not typed into this file.

Docling runs on its defaults (`DocumentConverter()` with no options), which is the thing this
test pins: OCR on, table structure on. If either default ever changes upstream, the scanned
tier stops recovering the schedule and this fails before anyone's evaluation number does.

The OCR engine fetches its weights on first use. On a machine that has ingested once they are
on disk and this runs in about fifteen seconds; on a cold checkout it is skipped with a reason
rather than pulling sixty megabytes inside `make check`. Set `PARROT_OCR_TESTS=1` to force it.
"""

from __future__ import annotations

import csv
import io
import os
from datetime import date
from pathlib import Path

import pytest

from core.ingest.parse import DoclingParser

pypdfium2 = pytest.importorskip("pypdfium2")
Image = pytest.importorskip("PIL.Image")
ImageOps = pytest.importorskip("PIL.ImageOps")

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "corpus/register/batch1.csv"
SOURCE = ROOT / "corpus/batches/batch1/b1-0001.pdf"
DOC_ID = "b1-0001"


def _ocr_weights_present() -> bool:
    try:
        import rapidocr
    except ImportError:
        return False
    models = Path(rapidocr.__file__).parent / "models"
    return models.is_dir() and any(models.glob("*.pth"))


needs_ocr = pytest.mark.skipif(
    not (os.environ.get("PARROT_OCR_TESTS") or _ocr_weights_present()),
    reason="RapidOCR weights not downloaded; ingest one document first, or set PARROT_OCR_TESTS=1",
)


def _register_row(doc_id: str) -> dict[str, str]:
    with REGISTER.open(newline="", encoding="utf-8-sig") as handle:
        lines = [line for line in handle if not line.startswith("#")]
    for row in csv.DictReader(lines):
        if row["doc_id"] == doc_id:
            return row
    raise AssertionError(f"{doc_id} is not in {REGISTER.name}")


def _as_printed(row: dict[str, str]) -> dict[str, str]:
    """The register stores typed values; the page prints them the way a person would."""
    expiry = date.fromisoformat(row["expiry_date"])
    return {
        "policy_no": row["policy_no"],
        "insured": row["insured"],
        "premium_payable": f"{float(row['premium_payable']):,.2f}",
        "sum_insured": f"{float(row['sum_insured']):,.2f}",
        "expiry_date": f"{expiry.day} {expiry:%B %Y}",
    }


@pytest.fixture(scope="module")
def page_pixels() -> Image.Image:
    """Page 1 of the digital schedule, drawn at 200 dpi — the resolution of a desk scanner."""
    pdf = pypdfium2.PdfDocument(str(SOURCE))
    return pdf[0].render(scale=200 / 72).to_pil().convert("RGB")


@pytest.fixture(scope="module")
def scanned(page_pixels: Image.Image) -> bytes:
    """The scanned tier: an image-only PDF. No text layer, so every character comes from OCR."""
    buffer = io.BytesIO()
    page_pixels.save(buffer, "PDF", resolution=200.0)
    return buffer.getvalue()


@pytest.fixture(scope="module")
def photographed(page_pixels: Image.Image) -> bytes:
    """The photographed tier: lower resolution, a slight skew, a grey table showing at the edges,
    and JPEG compression — a phone held over a kitchen table."""
    photo = page_pixels.resize((page_pixels.width * 3 // 4, page_pixels.height * 3 // 4))
    photo = photo.rotate(1.5, resample=Image.BICUBIC, expand=True, fillcolor=(214, 208, 196))
    photo = ImageOps.autocontrast(photo, cutoff=1)
    buffer = io.BytesIO()
    photo.save(buffer, "JPEG", quality=70)
    return buffer.getvalue()


@needs_ocr
@pytest.mark.parametrize("tier", ["scanned", "photographed"])
def test_a_scan_keeps_the_schedule_table_and_its_page(
    tier: str, request: pytest.FixtureRequest
) -> None:
    payload: bytes = request.getfixturevalue(tier)
    name = f"{DOC_ID}-{tier}.{'pdf' if tier == 'scanned' else 'jpg'}"

    parsed = DoclingParser().parse(payload, name)

    assert parsed.ok, parsed.reason
    assert parsed.page_count == 1  # a citation will say "page 1", and page 1 must exist
    page = parsed.pages[0]
    assert page.page == 1

    tables = [block for block in page.blocks if block.kind == "table"]
    assert tables, f"no table block on the {tier} page; kinds were {[b.kind for b in page.blocks]}"

    # The schedule is one table, and every value the register holds for this document is
    # printed in it. Losing the table to OCR would lose all of these at once.
    schedule = "\n".join(block.text for block in tables)
    expected = _as_printed(_register_row(DOC_ID))
    missing = {key: value for key, value in expected.items() if value not in schedule}
    assert not missing, f"{tier}: not in the recovered table: {missing}"

    # And the table is rows, not a blob: `label: value` lines are what chunking and extraction read.
    assert f"Policy Number: {expected['policy_no']}" in schedule
