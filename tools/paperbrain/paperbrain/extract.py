"""Turn a file on disk into plain text, page by page. All local, no network.

Order of attack for PDFs:
  1. Embedded text layer (pypdf) — instant, exact.
  2. If a page yields almost nothing, it's a scan: rasterise and OCR it.

Images go straight to OCR. Optional dependencies degrade gracefully: if
pytesseract or pdf2image are missing, PaperBrain still ingests everything that
has a text layer and tells you which files need OCR.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import IMAGE_SUFFIXES

# Below this many characters a PDF page is treated as a scan, not text.
SCAN_THRESHOLD = 40


@dataclass
class Extracted:
    pages: list[str]
    ocr_used: bool
    note: str = ""

    @property
    def text(self) -> str:
        return "\n\n".join(p.strip() for p in self.pages if p and p.strip())


def _ocr_image(img) -> str:
    import pytesseract

    return pytesseract.image_to_string(img)


def _ocr_pdf_pages(path: Path, page_numbers: list[int], dpi: int) -> dict[int, str]:
    """OCR only the pages that need it."""
    from pdf2image import convert_from_path

    out: dict[int, str] = {}
    for pageno in page_numbers:
        images = convert_from_path(str(path), dpi=dpi, first_page=pageno + 1, last_page=pageno + 1)
        if images:
            out[pageno] = _ocr_image(images[0])
    return out


def extract_pdf(path: Path, ocr_enabled: bool, dpi: int) -> Extracted:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")

    needs_ocr = [i for i, t in enumerate(pages) if len(t.strip()) < SCAN_THRESHOLD]
    ocr_used = False
    note = ""

    if needs_ocr and ocr_enabled:
        try:
            recovered = _ocr_pdf_pages(path, needs_ocr, dpi)
            for i, text in recovered.items():
                if text.strip():
                    pages[i] = text
                    ocr_used = True
        except Exception as exc:  # missing poppler / tesseract, or a bad page
            note = f"OCR unavailable for {len(needs_ocr)} scanned page(s): {exc}"
    elif needs_ocr:
        note = f"{len(needs_ocr)} page(s) look scanned; OCR is disabled"

    return Extracted(pages=pages, ocr_used=ocr_used, note=note)


def extract_image(path: Path, ocr_enabled: bool) -> Extracted:
    if not ocr_enabled:
        return Extracted(pages=[], ocr_used=False, note="OCR disabled; image skipped")
    try:
        from PIL import Image

        with Image.open(path) as img:
            text = _ocr_image(img)
        return Extracted(pages=[text], ocr_used=True)
    except Exception as exc:
        return Extracted(pages=[], ocr_used=False, note=f"OCR failed: {exc}")


def extract_docx(path: Path) -> Extracted:
    import docx  # python-docx

    document = docx.Document(str(path))
    parts = [p.text for p in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            cells = [c.text.strip() for c in row.cells]
            if any(cells):
                parts.append(" | ".join(cells))
    return Extracted(pages=["\n".join(parts)], ocr_used=False)


def extract_eml(path: Path) -> Extracted:
    import email
    from email import policy

    msg = email.message_from_bytes(path.read_bytes(), policy=policy.default)
    header = "\n".join(
        f"{k}: {msg.get(k)}" for k in ("From", "To", "Date", "Subject") if msg.get(k)
    )
    try:
        body = msg.get_body(preferencelist=("plain", "html"))
        body_text = body.get_content() if body else ""
    except Exception:
        body_text = ""
    return Extracted(pages=[f"{header}\n\n{body_text}"], ocr_used=False)


def extract_text_file(path: Path) -> Extracted:
    return Extracted(pages=[path.read_text(encoding="utf-8", errors="replace")], ocr_used=False)


def extract(path: Path, ocr_enabled: bool = True, dpi: int = 220) -> Extracted:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(path, ocr_enabled, dpi)
    if suffix in IMAGE_SUFFIXES:
        return extract_image(path, ocr_enabled)
    if suffix == ".docx":
        return extract_docx(path)
    if suffix == ".eml":
        return extract_eml(path)
    return extract_text_file(path)
