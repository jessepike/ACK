#!/usr/bin/env bash
set -euo pipefail

# AGS init: install pre-commit hook (optional) and generate initial registry
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[AGS] Running strict validation..."
python3 "$ROOT/scripts/validate_ags.py" --root "$ROOT" --profile strict --check-registry --check-drift

echo "[AGS] Writing derived registry..."
python3 "$ROOT/scripts/validate_ags.py" --root "$ROOT" --profile strict --write-registry

echo "[AGS] Done."
