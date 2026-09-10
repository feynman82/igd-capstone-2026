#!/usr/bin/env bash
# One-shot setup for PaperBrain on macOS. Safe to re-run.
set -euo pipefail

cd "$(dirname "$0")/.."
echo "==> PaperBrain setup in $(pwd)"

# --- system dependencies --------------------------------------------------
if command -v brew >/dev/null 2>&1; then
  for pkg in ollama tesseract poppler; do
    if brew list --formula "$pkg" >/dev/null 2>&1; then
      echo "    $pkg already installed"
    else
      echo "==> brew install $pkg"
      brew install "$pkg"
    fi
  done
else
  echo "!!  Homebrew not found. Install ollama, tesseract and poppler manually."
fi

# --- python ---------------------------------------------------------------
if [ ! -d .venv ]; then
  echo "==> creating .venv"
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
echo "==> installing python dependencies"
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# --- models ---------------------------------------------------------------
if command -v ollama >/dev/null 2>&1; then
  if ! curl -sf http://127.0.0.1:11434/api/tags >/dev/null; then
    echo "!!  Ollama isn't running. Start it (open -a Ollama, or 'ollama serve &')"
    echo "    then re-run this script to pull the models."
  else
    for model in nomic-embed-text qwen2.5:14b-instruct; do
      if ollama list | awk '{print $1}' | grep -q "^${model%%:*}"; then
        echo "    model $model already pulled"
      else
        echo "==> ollama pull $model"
        ollama pull "$model"
      fi
    done
  fi
fi

chmod +x pb
echo
./pb init || true
echo
echo "Next:  source .venv/bin/activate && ./pb add ~/Documents/Paperwork && ./pb ingest"
