# Notice

Coursework produced for the Singapore Management University Industry Graduate Diploma,
*AI in the Digital Economy* — Integrated Learning Project, September to November 2026.

**PARROT** is an internal working name. No commercial name has been chosen. A distinct
published system already carries the name in an adjacent space (Suresh, 2026), cited as
prior art in the report.

## This repository contains no personal data

The corpus is **synthetic**. Every document is generated from an invented household
canon and names invented organisations only — never a real insurer, bank or agency. The
household, its members, its employers, its policy numbers and its insurers do not exist.

`corpus/batches/` **is** committed. Those documents are synthetic, so git is the right way
to hand a batch from Lane E to the other four — a batch arrives by pulling rather than by a
USB stick at the weekly session.

The 40-document real-document holdout is different in kind. It is collected under the
consent and redaction protocol in `docs/governance/`, is redacted before use, and **is never
committed to this repository**. `corpus/holdout/` is gitignored, and `.graphifyignore`
excludes both it and `corpus/batches/` from knowledge-graph extraction as a second lock.

That distinction is the whole control, so it is worth stating why it is an ignore rule and
not a convention: deleting a committed file does not remove it from the repository. It stays
in history, in every clone, and in every fork. There is no undo.

## Third-party components

Runtime dependencies are declared in `pyproject.toml` and `web/package.json` and retain
their own licences. The generation model, `Qwen-SEA-LION-v4-4B-VL` (AI Singapore), is MIT
licensed. Parsing uses Docling (MIT). Grounding corpora reproduce published guidance from
named public bodies with provenance recorded in each `grounding/*/sources.yaml`.

## Use

Not licensed for redistribution. Assessed academic work.
