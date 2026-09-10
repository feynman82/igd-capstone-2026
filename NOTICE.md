# Notice

Coursework produced for the Singapore Management University Industry Graduate Diploma,
*AI in the Digital Economy* — Integrated Learning Project, September to November 2026.

**PARROT** is an internal working name. No commercial name has been chosen. A distinct
published system already carries the name in an adjacent space (Suresh, 2026), cited as
prior art in the report.

## This repository contains no personal data

The corpus is **synthetic**. Every document is generated from an invented household
canon, carries a visible `SYNTHETIC DOCUMENT` footer, and names invented organisations
only — never a real insurer, bank or agency.

The 40-document real-document holdout is collected under the consent and redaction
protocol in `docs/governance/`, is redacted before use, and **is never committed to this
repository**. `corpus/batches/` and `corpus/holdout/` are gitignored, and
`.graphifyignore` excludes them from knowledge-graph extraction as a second lock.

## Third-party components

Runtime dependencies are declared in `pyproject.toml` and `web/package.json` and retain
their own licences. The generation model, `Qwen-SEA-LION-v4-4B-VL` (AI Singapore), is MIT
licensed. Parsing uses Docling (MIT). Grounding corpora reproduce published guidance from
named public bodies with provenance recorded in each `grounding/*/sources.yaml`.

## Use

Not licensed for redistribution. Assessed academic work.
