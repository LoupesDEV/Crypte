#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"

PYTHON_CMD=""

if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
else
  echo "Python n'est pas installe ou introuvable dans le PATH." >&2
  exit 1
fi

"$PYTHON_CMD" -m pip install -r requirements.txt
"$PYTHON_CMD" main.py
