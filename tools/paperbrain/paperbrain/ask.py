"""Answer a question from retrieved chunks, with citations back to the file.

The prompt is deliberately strict: paperwork answers that quietly invent a
number are worse than no answer. The model is told to cite [1]-style markers
and to say when the documents don't cover the question.
"""

from __future__ import annotations

from .ollama import Ollama
from .retrieve import Hit

SYSTEM = """You are PaperBrain, a private assistant that answers questions strictly from the user's own documents.

Rules:
- Use ONLY the numbered excerpts provided. Never rely on outside knowledge.
- Cite the excerpt number in square brackets after each claim, e.g. [2].
- Quote exact figures, dates, policy and reference numbers verbatim.
- If the excerpts do not contain the answer, say so plainly and name what document would be needed. Do not guess.
- Be concise. Lead with the answer, then the supporting detail.
"""


def build_context(hits: list[Hit], budget_chars: int = 12000) -> str:
    blocks, used = [], 0
    for i, hit in enumerate(hits, start=1):
        where = f"{hit.filename}" + (f", p.{hit.page}" if hit.page else "")
        meta = f" | {hit.doc_type}" if hit.doc_type else ""
        meta += f" | dated {hit.doc_date}" if hit.doc_date else ""
        block = f"[{i}] ({where}{meta})\n{hit.text}"
        if used + len(block) > budget_chars:
            break
        blocks.append(block)
        used += len(block)
    return "\n\n---\n\n".join(blocks)


def answer(client: Ollama, model: str, question: str, hits: list[Hit]) -> str:
    if not hits:
        return (
            "Nothing in your library matches that yet. "
            "Add the relevant folder with `pb add <folder>` and run `pb ingest`."
        )
    context = build_context(hits)
    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": f"Excerpts from my documents:\n\n{context}\n\nQuestion: {question}",
        },
    ]
    return client.chat(model, messages)


def format_sources(hits: list[Hit]) -> str:
    lines = []
    for i, hit in enumerate(hits, start=1):
        page = f" (p.{hit.page})" if hit.page else ""
        lines.append(f"  [{i}] {hit.filename}{page} — {hit.path}")
    return "\n".join(lines)
