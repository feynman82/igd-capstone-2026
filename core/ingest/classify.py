"""Decide which pack's document type a captured document is, or decline to.

The candidate list is every document type every installed pack declares, qualified by pack id.
The model is constrained to that list plus `unknown` — it cannot invent a type, and it cannot
return the name of a pack nobody has installed.

Declining matters more than choosing. A document classified as the wrong type would be
extracted against the wrong field list and would produce facts that are confidently wrong,
which is worse than a document in quarantine. So a low-confidence answer or `unknown` routes to
quarantine rather than to a best guess.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass

from core.contracts import DocumentTypeSpec
from core.ingest.parse import ParsedPage
from core.packs import document_types
from core.runtime.ollama import ModelUnavailable, Ollama

log = logging.getLogger(__name__)

UNKNOWN = "unknown"
MIN_CONFIDENCE = 0.45

# How much of the document the classifier reads, and how many pages it may span.
#
# Page 1 alone is not enough. A full policy document opens with a letterhead, and on some of them
# the parser recovers only that — b1-0002 in batch 1 parsed to its letterhead, its signature
# block and its footer, with the whole schedule table missing, and the classifier declined it
# correctly on the evidence it was given. Reading a few pages costs one prompt and rescues the
# document whose identifying page is not the first one.
CLASSIFY_SAMPLE_CHARS = 6000
CLASSIFY_SAMPLE_PAGES = 4

SYSTEM = (
    "You identify what kind of household document you are looking at. You only ever choose "
    "from the list you are given. If the document is not clearly one of them, you answer "
    "unknown. You never guess to be helpful."
)


@dataclass(frozen=True, slots=True)
class Classification:
    pack_id: str | None
    doc_type: str | None
    confidence: float
    reason: str | None = None

    @property
    def recognised(self) -> bool:
        return self.pack_id is not None and self.doc_type is not None


def classification_sample(pages: list[ParsedPage]) -> str:
    """The text the classifier reads: the opening pages, labelled, within a fixed budget."""
    parts: list[str] = []
    budget = CLASSIFY_SAMPLE_CHARS
    for page in pages[:CLASSIFY_SAMPLE_PAGES]:
        if budget <= 0:
            break
        body = page.text[:budget]
        parts.append(f"[page {page.page}]\n{body}")
        budget -= len(body)
    return "\n\n".join(parts)[:CLASSIFY_SAMPLE_CHARS]


def _schema(candidates: list[str]) -> dict[str, object]:
    return {
        "type": "object",
        "properties": {
            "document_type": {"type": "string", "enum": [*candidates, UNKNOWN]},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        },
        "required": ["document_type", "confidence"],
    }


def _prompt(candidates: Mapping[str, tuple[str, DocumentTypeSpec]], text: str) -> str:
    lines = ["Candidate document types:"]
    for qualified, (_pack_id, spec) in candidates.items():
        lines.append(f"- {qualified}: {spec.description}")
    lines += [
        "",
        "The opening pages of the document are between the markers.",
        "<<<",
        text[:CLASSIFY_SAMPLE_CHARS],
        ">>>",
        "",
        "Answer with one candidate name exactly as written above, or unknown.",
    ]
    return "\n".join(lines)


def classify(client: Ollama, text: str) -> Classification:
    """Never raises. An unavailable model is a classification failure, so it quarantines."""
    candidates = document_types()
    if not candidates:
        return Classification(None, None, 0.0, "no packs are installed")
    if not text.strip():
        return Classification(None, None, 0.0, "no text to classify")

    try:
        reply = client.constrained(
            SYSTEM, _prompt(candidates, text), _schema(list(candidates))
        ).json()
    except ModelUnavailable as error:
        return Classification(None, None, 0.0, str(error))

    chosen = str(reply.get("document_type", UNKNOWN))
    try:
        confidence = float(reply.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0

    if chosen == UNKNOWN or chosen not in candidates:
        return Classification(None, None, confidence, "no installed pack recognises this document")
    if confidence < MIN_CONFIDENCE:
        return Classification(
            None, None, confidence, f"classified as {chosen} but only {confidence:.2f} confident"
        )
    pack_id, _spec = candidates[chosen]
    doc_type = chosen.split(".", 1)[1]
    return Classification(pack_id, doc_type, confidence)
