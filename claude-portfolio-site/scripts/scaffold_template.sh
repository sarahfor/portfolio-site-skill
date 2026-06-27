#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $(basename "$0") /absolute/path/to/output-directory" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="${SCRIPT_DIR}/../assets/site-template"
OUTPUT_DIR="$1"

mkdir -p "$OUTPUT_DIR"
cp -R "${TEMPLATE_DIR}/." "$OUTPUT_DIR/"

echo "Scaffolded portfolio template into: $OUTPUT_DIR"
