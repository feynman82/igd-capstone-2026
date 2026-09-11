"""Capture adapters.

Every channel a document can arrive through satisfies one interface, so which chat
application carries a photograph is a configuration choice rather than an architectural
one. See `core/adapters/README.md`.
"""

from core.adapters.base import CaptureAdapter, IngestJob

__all__ = ["CaptureAdapter", "IngestJob"]
