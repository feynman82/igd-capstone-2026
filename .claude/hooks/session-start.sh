#!/bin/bash
# Session start for Claude Code on the web: the Python environment `make check` needs, and
# graphify with its skill, merge driver and git hooks (docs/GRAPHIFY.md, "Setup, once per clone").
# Every step is idempotent, so a resumed session re-runs it cheaply.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# ruff, mypy's type stubs and pytest live in the dev groups; without them `make check` fails.
uv sync --all-extras --all-groups

export PATH="$HOME/.local/bin:$PATH"
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PATH=\"$HOME/.local/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi

if ! command -v graphify >/dev/null 2>&1; then
  uv tool install graphifyy
fi
graphify install --platform claude >/dev/null
make graph-setup >/dev/null
graphify hook install
