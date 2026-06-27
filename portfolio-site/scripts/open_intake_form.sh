#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORM_PATH="${SCRIPT_DIR}/../assets/intake-form/index.html"

if command -v open >/dev/null 2>&1; then
  open "$FORM_PATH"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$FORM_PATH"
elif command -v cygstart >/dev/null 2>&1; then
  cygstart "$FORM_PATH"
elif command -v powershell.exe >/dev/null 2>&1; then
  powershell.exe -NoProfile -Command "Start-Process '$FORM_PATH'"
else
  printf 'Open this file in your browser:\n%s\n' "$FORM_PATH"
fi
