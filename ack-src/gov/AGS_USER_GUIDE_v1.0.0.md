# AGS User Guide (v1.0.0)

## What This Is
The **Artifact Governance System (AGS)** is a lightweight, enforceable control plane for AI‑assisted development.
It ensures that core documents stay aligned with reality, drift is detected, and changes are traceable—without relying on human discipline.

If the validator passes, the system is in a *known‑good state*.

---

## Core Ideas (First Principles)
- **Humans and agents are inconsistent** → governance must be enforced by tools.
- **Documents are first‑class system components**, not notes.
- **Version control is the enforcement boundary** (Git + validator).
- **“Good enough” is objective**: strict validation passes.

---

## What AGS Does
- Validates required metadata (frontmatter) and controlled vocabularies
- Auto‑allocates and fixes document IDs
- Auto‑generates and verifies the artifact registry
- Detects drift between code changes and documentation
- Enforces governance rules at pre‑commit / CI
- Supports solo dev *and* team workflows

---

## Repository Layout
```
.
├── AGS_VERSION.md
├── docs/                # Human‑readable artifacts (Tier 1 & 2)
├── artifacts/           # Generated outputs (registry, reports)
├── schemas/             # Machine‑readable schemas
├── scripts/
│   └── validate_ags.py  # Enforcement engine
└── Makefile
```

---

## Tiers (What Matters Most)
- **Tier 1 (Canonical)**: architecture, governance, data model
  - Versioned, reviewed, enforced
- **Tier 2 (Supporting)**: guides, examples, visuals
  - Informative, not gating
- **Ephemeral**: outputs, reports
  - Generated, disposable

---

## Daily Workflow (Solo Dev)
1. Make changes (code or docs)
2. Run:
   ```bash
   make ags-validate
   ```
3. If blocked:
   - Fix the issue, or
   - Create an ADR if intent changed
4. Commit when validation passes

---

## Team Workflow
- All Tier 1 changes go through PR
- Validator runs in CI (strict mode)
- Agents may propose changes; humans approve
- Emergency bypass allowed, with 48‑hour reconciliation ADR

---

## Key Commands
```bash
# Validate everything
python scripts/validate_ags.py --profile strict

# Auto‑generate registry
python scripts/validate_ags.py --write-registry

# Detect drift
python scripts/validate_ags.py --auto-check-drift

# Get next document ID
python scripts/validate_ags.py --next-id gov

# Fix TODO doc IDs
python scripts/validate_ags.py --fix-todo-ids
```

---

## New Projects
1. Copy AGS into the repo (or `.ags/`)
2. Set `AGS_VERSION.md`
3. Run validation
4. Start writing Tier 1 docs

---

## Existing Projects (Adoption)
- Start with **minimal profile**
- Promote only 2–3 Tier 1 artifacts
- Add 1 drift rule
- Tighten over time

---

## Versioning Rules
- **System version**: AGS itself (`AGS_VERSION.md`, git tag)
- **Document version**: frontmatter `version`
- **Reviewed** = PR approved by ≥1 human with write access

---

## When Is It “Done”?
When:
- Strict validation passes
- Registry matches the repo
- Drift rules execute
- Git history is the audit trail

At that point, **stop designing and start using**.

---

## Final Mental Model
> AGS is not bureaucracy.
> It is a **seatbelt** for AI‑assisted development.

If you forget about it and it still protects you, it’s working.
