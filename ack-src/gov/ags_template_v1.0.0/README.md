# Artifact Governance System (AGS) — Template v1.0.0

This repository is a **drop-in governance harness** for AI-assisted development:
- Tiered artifacts (Tier 1 canonical; Tier 2 derived/ephemeral)
- Machine-enforced frontmatter + controlled vocabularies
- Derived registry (no manual “double entry”)
- Drift rules: code changes that must trigger doc updates or ADRs

## Quick start (new project)

1. Copy this folder into your repo at `.ags/` (recommended) or at repo root.
2. Run validation:

```bash
python3 scripts/validate_ags.py --profile strict --check-registry --check-drift
```

3. Optional: install pre-commit hook (see `docs/ADOPTION_GUIDE.md`).

## Adoption for existing projects

See `docs/ADOPTION_GUIDE.md` for:
- a 30–60 minute “bootstrap” path
- minimal vs strict operating modes
- how to introduce Tier 1 artifacts without slowing delivery

## Release boundary

AGS uses **SemVer** as a *system*:
- Tags: `ags-vX.Y.Z`
- This file: `AGS_VERSION.md` is the in-repo declaration of the current system version.

## Key folders

- `docs/` — governance documents + Tier 1 artifacts + ADRs
- `scripts/` — validator and utilities
- `artifacts/` — derived outputs (registry, change reports)
- `schemas/` — machine-readable schemas (optional; project-specific)

