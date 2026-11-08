#!/bin/zsh
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required. No installation was attempted."
  echo "Install Python 3.9 or later, then run this launcher again."
  read "?Press Enter to close."
  exit 1
fi
python3 launcher.py
