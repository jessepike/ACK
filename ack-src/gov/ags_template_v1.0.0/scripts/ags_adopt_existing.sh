#!/usr/bin/env bash
set -euo pipefail

# AGS adoption helper for existing repos:
# - runs minimal validation first
# - writes derived registry
# - provides next steps

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[AGS] Running minimal validation (lighter requirements)..."
python3 "$ROOT/scripts/validate_ags.py" --root "$ROOT" --profile minimal --check-registry || true

echo "[AGS] Writing derived registry..."
python3 "$ROOT/scripts/validate_ags.py" --root "$ROOT" --profile minimal --write-registry

cat <<'EOF'

[AGS] Next steps:
1) Promote a small set of Tier 1 docs (architecture, data model, security baseline, tasks) with strict profile.
2) Add/enable drift rules relevant to your stack (see drift_rules.yaml).
3) Turn on strict validation in CI when ready.

EOF
