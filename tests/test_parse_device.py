"""Issue #123: Docling on Apple's GPU segfaulted on a committed statement and took ingestion down.

On a Mac the parser asks Docling for the CPU; `DOCLING_DEVICE` still wins; elsewhere Docling
chooses as before.
"""

from __future__ import annotations

import pytest

from core.ingest.parse import docling_device


def test_a_mac_parses_on_the_cpu() -> None:
    assert docling_device("darwin", {}) == "cpu"


@pytest.mark.parametrize("platform", ["win32", "linux"])
def test_elsewhere_docling_chooses(platform: str) -> None:
    assert docling_device(platform, {}) is None


@pytest.mark.parametrize("device", ["mps", "cpu", "cuda"])
def test_docling_device_still_wins(device: str) -> None:
    """Set to `mps`, it is how someone tries the GPU again after an upgrade."""
    assert docling_device("darwin", {"DOCLING_DEVICE": device}) is None


def test_the_converter_is_built_for_the_cpu_on_a_mac(monkeypatch: pytest.MonkeyPatch) -> None:
    pytest.importorskip("docling")
    from docling.datamodel.accelerator_options import AcceleratorDevice
    from docling.datamodel.base_models import InputFormat

    import core.ingest.parse as parse

    monkeypatch.setattr(parse, "docling_device", lambda: "cpu")
    converter = parse._converter()
    for kind in (InputFormat.PDF, InputFormat.IMAGE):
        options = converter.format_to_options[kind].pipeline_options
        assert options.accelerator_options.device == AcceleratorDevice.CPU


def test_a_pdf_whose_text_is_drawn_is_read_whole_page() -> None:
    """`b1-0004` and fifteen others carry no text layer: every word on them is OCR."""
    pdfium = pytest.importorskip("pypdfium2")
    import subprocess
    from pathlib import Path

    from core.ingest.parse import drawn_pdf as parse_drawn
    from core.ingest.parse import has_text_layer

    root = Path(__file__).resolve().parents[1]

    def committed(path: str) -> bytes:
        return subprocess.run(
            ["git", "show", f"HEAD:{path}"], cwd=root, capture_output=True, check=True
        ).stdout

    assert pdfium is not None
    assert not has_text_layer(committed("corpus/batches/batch1/b1-0004.pdf"))
    assert has_text_layer(committed("corpus/batches/batch1/b1-0001.pdf"))
    assert not has_text_layer(b"\x89PNG\r\n\x1a\n"), "an image has no text layer"
    assert not parse_drawn(b"\x89PNG\r\n\x1a\n"), "but it is not a drawn PDF"
    assert parse_drawn(committed("corpus/batches/batch1/b1-0004.pdf"))
    assert has_text_layer(b"%PDF-1.7 not really"), "unreadable: left to Docling, as before"


def test_full_page_ocr_is_asked_for_only_when_there_is_no_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pytest.importorskip("docling")
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import OcrMode

    import core.ingest.parse as parse

    monkeypatch.setattr(parse, "docling_device", lambda: None)
    whole = parse._converter(full_page=True)
    assert whole.format_to_options[InputFormat.PDF].pipeline_options.ocr_options.mode == (
        OcrMode.FULL_PAGE
    )
    # A photograph is never read whole-page: an identity card's "TAN MEI LING" lost a space.
    assert whole.format_to_options[InputFormat.IMAGE].pipeline_options.ocr_options.mode == (
        OcrMode.DEFAULT
    )
    assert (
        parse._converter(full_page=False)
        .format_to_options[InputFormat.PDF]
        .pipeline_options.ocr_options.mode
        == OcrMode.DEFAULT
    )
