---
type: runbook
description: "Adoption Guide"
version: 1.0.0
updated: 2026-01-01
status: active
depends_on: 
doc_id: gov-050
slug: adoption-guide
title: "Adoption Guide"
tier: tier2
authority: guidance
review_status: accepted
created: 2026-01-01
owner: human
---
## Purpose

Provide a minimal ramp to adopt the **Artifact Governance System (AGS)** in an existing repo.

---

## Minimal adoption (30 minutes)

1. Copy this package into your repo (or a `/governance` folder).
2. Ensure Tier 1 docs live in `docs/` and schemas in `schemas/`.
3. Run:

```bash
python3 scripts/validate_ags.py --write-registry
```

4. Fix any errors until validation passes.
5. Commit changes.

---

## Solo dev mode

- You may commit directly to `main`, but run validation before push.
- Use PRs only when collaboration or risk warrants.

---

## Team mode

- Use PR/MR as the enforcement boundary.
- Require validation to pass before merge.

---

## Next steps (optional)

- Add a pre-commit hook to run the validator.
- Add CI to run the validator on PRs.
- Start populating `drift_rules.yaml` as drift signals become clear.

### Optional: Auto-allocate IDs

If you create a file with `doc_id: TODO`, you can auto-allocate IDs:

```bash
python3 scripts/validate_ags.py --fix-todo-ids
```

This replaces `doc_id: TODO` in-place using prefix-based allocation (`gov`, `adr`, `doc`, etc.).

## Pre-commit Hook Example (Git)

Create `.git/hooks/pre-commit` (make it executable):

```bash
#!/usr/bin/env bash
set -euo pipefail

python3 scripts/validate_ags.py --profile strict --check-registry --auto-check-drift --diff-range --cached
```

Notes:
- Hooks are local to your machine unless you manage them with a tool like `pre-commit` or a repo bootstrap script.
- Teams should also run the same command in CI so enforcement cannot be skipped.
## Using AGS Across Projects

### Recommended packaging pattern

- Put AGS in a dedicated folder (recommended): `.ags/`
- Keep project artifacts in your repo (e.g., `ARCHITECTURE.md`, `DATA_MODEL.md`) and reference them from AGS, or store them under `.ags/docs/` if you prefer a single bundle.

**Rule:** AGS is the harness; your project docs are the governed objects.

### New projects

- Start from this template package.
- Run:

```bash
make ags-validate
make ags-registry
```

- Install pre-commit hook (optional) and adopt strict mode once the project has a real architecture/data model.

### Existing projects

Adopt in phases to avoid “governance fatigue”:

1. **Phase 0 (Minimal)**  
   - Use `--profile minimal`
   - Generate derived registry
   - Do not require PR ceremony if you’re solo

2. **Phase 1 (Canonical subset)**  
   - Promote 3–5 Tier 1 docs that matter most (e.g., ARCHITECTURE, DATA_MODEL, SECURITY_BASELINE, TASKS)
   - Enable 1–2 drift rules that target your highest-risk drift points

3. **Phase 2 (Strict + CI)**  
   - Turn on strict validation in CI
   - Require human approval for agent-submitted changes if you’re multi-person

### When to stop adding governance

Stop when:
- validation passes reliably
- drift rules catch the top 1–2 failure modes
- governance friction is not driving bypasses

Anything else goes to `docs/GOVERNANCE_BACKLOG.md`.

