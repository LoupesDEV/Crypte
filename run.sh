#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
  python3 main.py
elif command -v python >/dev/null 2>&1; then
  python main.py
else
  echo "Python n'est pas installe ou introuvable dans le PATH." >&2
  exit 1
fi
