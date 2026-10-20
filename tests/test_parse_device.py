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
