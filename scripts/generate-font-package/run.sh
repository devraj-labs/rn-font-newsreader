#!/usr/bin/env bash

# run.sh
#
# Creates (or reuses) a Python venv, installs pinned dependencies from
# requirements.txt, then runs generate-font-package.py.
#
# Usage:
#   bash scripts/generate-font-package/run.sh
#   bash scripts/generate-font-package/run.sh --export manropeFonts
#   bash scripts/generate-font-package/run.sh --dry-run

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"
PYTHON_SCRIPT="$SCRIPT_DIR/generate-font-package.py"

REQUIRED_PYTHON="3.10"

# ─── Check Python version ─────────────────────────────────────────────────────

PYTHON_BIN=$(command -v python3 || true)

if [[ -z "$PYTHON_BIN" ]]; then
  echo "✗ python3 not found. Install Python ${REQUIRED_PYTHON}+ from https://python.org"
  exit 1
fi

PYTHON_VERSION=$("$PYTHON_BIN" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_MAJOR=3
REQUIRED_MINOR=10

ACTUAL_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
ACTUAL_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [[ "$ACTUAL_MAJOR" -lt "$REQUIRED_MAJOR" ]] || \
   { [[ "$ACTUAL_MAJOR" -eq "$REQUIRED_MAJOR" ]] && [[ "$ACTUAL_MINOR" -lt "$REQUIRED_MINOR" ]]; }; then
  echo "✗ Python ${REQUIRED_PYTHON}+ required (found ${PYTHON_VERSION})"
  exit 1
fi

# ─── Create venv if needed ────────────────────────────────────────────────────

if [[ ! -d "$VENV_DIR" ]]; then
  echo "→ Creating venv at scripts/.venv (Python ${PYTHON_VERSION})"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

VENV_PYTHON="$VENV_DIR/bin/python3"
VENV_PIP="$VENV_DIR/bin/pip"

# ─── Install / sync dependencies ─────────────────────────────────────────────

echo "→ Installing dependencies from requirements.txt"
"$VENV_PIP" install --quiet --require-virtualenv -r "$REQUIREMENTS"

# ─── Run ──────────────────────────────────────────────────────────────────────

"$VENV_PYTHON" "$PYTHON_SCRIPT" "$@"
