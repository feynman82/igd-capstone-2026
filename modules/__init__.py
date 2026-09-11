"""Capability modules.

A module reads typed rows and writes its own namespace. It never touches retrieval, never
writes to `facts`, and — rule 7 in AGENTS.md — never imports from `web/` or `api/`. Each
module is a directory holding `module.yaml` and a hand-written `queries.py`.
"""
