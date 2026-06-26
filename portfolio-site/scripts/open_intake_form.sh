#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORM_PATH="${SCRIPT_DIR}/../assets/intake-form/index.html"

open "$FORM_PATH"
